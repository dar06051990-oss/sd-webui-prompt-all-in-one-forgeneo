"""Explicit backup/import helpers for Prompt AIO JSON files.

This module deliberately does not depend on a sibling extension installation.
Only flat, valid JSON files are accepted: never extract paths from an archive.
"""
from datetime import datetime
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2] / 'storage'
SAFE_JSON = re.compile(r'^[a-zA-Z0-9_.-]+\.json$')
MAX_FILES = 512
MAX_ZIP_BYTES = 24 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_FILE_BYTES = 12 * 1024 * 1024


def _name_ok(name):
    return bool(SAFE_JSON.fullmatch(name)) and name not in ('.json', '..json')


def _ensure_storage():
    ROOT.mkdir(parents=True, exist_ok=True)
    return ROOT


def create_backup():
    """Return a downloadable ZIP path containing the current JSON storage."""
    root = _ensure_storage()
    sources = [p for p in sorted(root.iterdir()) if p.is_file() and _name_ok(p.name)]
    if len(sources) > MAX_FILES:
        raise ValueError('Слишком много JSON-файлов в storage.')
    if not sources:
        raise ValueError('Не найдено JSON-файлов для резервного копирования.')
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup_dir = root / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    result = backup_dir / f'Prompt-AIO-backup-{timestamp}.zip'
    total = 0
    try:
        with zipfile.ZipFile(result, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for source in sources:
                raw = source.read_bytes()
                total += len(raw)
                if len(raw) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                    raise ValueError('Объём данных превышает лимит резервного копирования.')
                json.loads(raw.decode('utf-8-sig'))
                archive.writestr(source.name, raw)
    except Exception:
        result.unlink(missing_ok=True)
        raise
    return str(result), f'Резервная копия создана: {len(sources)} JSON-файлов. Сохрани ZIP в надёжном месте.'


def _read_archive(blob):
    if not isinstance(blob, (bytes, bytearray)) or not blob:
        raise ValueError('Сначала выбери ZIP-файл с резервной копией.')
    if len(blob) > MAX_ZIP_BYTES:
        raise ValueError('ZIP слишком большой (максимум 24 МБ).')
    files = {}
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            infos = archive.infolist()
            if len(infos) > MAX_FILES:
                raise ValueError('Слишком много файлов в ZIP.')
            total = 0
            for entry in infos:
                if entry.is_dir():
                    continue
                # Allow a single conventional "storage/" prefix, but never
                # arbitrary subfolders, path traversal or drive path values.
                name = entry.filename.replace('\\', '/')
                if name.startswith('storage/'):
                    name = name[len('storage/'):]
                if '/' in name or not _name_ok(name):
                    raise ValueError(f'Недопустимое имя файла в ZIP: {entry.filename}')
                if name in files:
                    raise ValueError(f'Повторяется JSON-файл: {name}')
                total += entry.file_size
                if entry.file_size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                    raise ValueError('Объём распакованных данных превышает безопасный лимит.')
                raw = archive.read(entry)
                if len(raw) > MAX_FILE_BYTES:
                    raise ValueError(f'Слишком большой JSON-файл: {name}')
                json.loads(raw.decode('utf-8-sig'))
                files[name] = raw
    except zipfile.BadZipFile as exc:
        raise ValueError('Файл не является корректным ZIP-архивом.') from exc
    if not files:
        raise ValueError('В ZIP нет JSON-файлов для переноса.')
    return files


def _read_folder(folder):
    source = Path(str(folder).strip().strip('"')).expanduser()
    if not source.is_dir():
        raise ValueError('Указанная папка не найдена.')
    if (source / 'storage').is_dir():
        source = source / 'storage'
    if source.name.lower() != 'storage':
        raise ValueError('Укажи папку storage или корень старого расширения с папкой storage.')
    if source.resolve() == _ensure_storage().resolve():
        raise ValueError('Это текущая папка storage. Для импорта выбери другую.')
    files = {}
    total = 0
    for path in sorted(source.iterdir()):
        if not path.is_file() or not path.name.lower().endswith('.json'):
            continue
        if not _name_ok(path.name):
            raise ValueError(f'Недопустимое имя JSON: {path.name}')
        if len(files) >= MAX_FILES:
            raise ValueError('Слишком много файлов для импорта.')
        raw = path.read_bytes()
        total += len(raw)
        if len(raw) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            raise ValueError('Слишком большой объём JSON-данных.')
        json.loads(raw.decode('utf-8-sig'))
        files[path.name] = raw
    if not files:
        raise ValueError('В выбранной папке не найдено JSON-файлов.')
    return files


def _write_import(files):
    """Transfer all source JSON, preserving an automatic backup of current data.

    Import is one unambiguous operation: matching files are replaced, missing
    files are added. Unrelated files in the destination are not deleted.
    Validation of all source data happens before calling this function.
    """
    root = _ensure_storage()

    # Write only changed files to avoid unnecessary filesystem activity.
    changed = {}
    new_files = 0
    replaced = 0
    unchanged = 0
    for name, raw in files.items():
        target = root / name
        if target.exists() and target.read_bytes() == raw:
            unchanged += 1
            continue
        changed[name] = raw
        if target.exists():
            replaced += 1
        else:
            new_files += 1

    if not changed:
        return (f'Данные уже совпадают с источником: {unchanged} JSON-файлов. '
                f'Перенос не требуется.')

    # A pre-import snapshot of every existing JSON is the user's rollback
    # point, including their history and favorites. Never write anything if
    # backup creation fails. No snapshot is necessary for a brand-new storage
    # directory with no existing JSON at all.
    current_json = any(p.is_file() and _name_ok(p.name) for p in root.iterdir())
    if current_json:
        backup_path, _ = create_backup()
        backup_note = f' Резервная копия: {backup_path}.'
    else:
        backup_note = ' Папка была пустой, резервная копия не требовалась.'

    for name, raw in changed.items():
        target = root / name
        fd, tmpname = tempfile.mkstemp(prefix='.prompt-aio-', suffix='.tmp', dir=str(root))
        try:
            with os.fdopen(fd, 'wb') as output:
                output.write(raw)
            os.replace(tmpname, target)
        finally:
            if os.path.exists(tmpname):
                os.unlink(tmpname)

    return (f'Перенос завершён: новых файлов {new_files}, '
            f'заменено {replaced}, уже совпадали {unchanged}.'
            f'{backup_note} Полностью перезапусти Forge Neo для обновления истории.')


# In this mode, history and favorites are *added*, not replaced. All other
# JSON files (such as current settings and translation preferences) are ignored.
HISTORY_OR_FAVORITE = re.compile(r'^(?:history|favorite)\.[a-zA-Z0-9_.-]+\.json$')


def _entry_identity(entry, filename):
    """Find repeat imports without discarding genuinely separate history items.

    Prompt AIO creates a stable UUID for each item; that is the primary key.
    For older entries lacking IDs we compare the item's stored content,
    excluding the calculated `is_favorite` UI flag.
    """
    if not isinstance(entry, dict):
        raise ValueError(f'Запись в {filename} должна быть JSON-объектом.')
    identifier = entry.get('id')
    if identifier is not None and str(identifier).strip():
        return ('id', str(identifier))
    stable = {k: v for k, v in entry.items() if k != 'is_favorite'}
    return ('content', json.dumps(stable, ensure_ascii=False, sort_keys=True))


def _merge_import(files):
    """Append unique history/favorite records from ZIP or folder.

    The current settings are unchanged; current history items retain their
    order. All target files are validated BEFORE creating a backup or writing.
    No arbitrary truncation is applied to merged lists.
    """
    root = _ensure_storage()
    chosen = {name: raw for name, raw in files.items() if HISTORY_OR_FAVORITE.fullmatch(name)}
    if not chosen:
        raise ValueError('В источнике нет файлов истории или избранного (history.*.json / favorite.*.json).')

    staged = {}
    total_added = 0
    total_duplicates = 0
    imported_groups = 0

    for name, raw in sorted(chosen.items()):
        incoming = json.loads(raw.decode('utf-8-sig'))
        if not isinstance(incoming, list):
            raise ValueError(f'{name}: ожидается JSON-массив записей.')
        target = root / name
        if target.exists():
            existing = json.loads(target.read_text(encoding='utf-8-sig'))
            if not isinstance(existing, list):
                raise ValueError(f'{name}: текущий файл не содержит список записей.')
        else:
            existing = []

        # Validate even the items we will ultimately skip. Never rewrite an
        # old record or silently discard repeated records already in storage.
        seen = {_entry_identity(item, name) for item in existing}
        combined = list(existing)
        new_in_group = 0
        for item in incoming:
            identity = _entry_identity(item, name)
            if identity in seen:
                total_duplicates += 1
                continue
            seen.add(identity)
            combined.append(item)
            new_in_group += 1

        if new_in_group:
            output = json.dumps(combined, ensure_ascii=True, indent=4).encode('utf-8')
            if len(output) > MAX_FILE_BYTES:
                raise ValueError(f'Объединённый файл {name} слишком большой для безопасного сохранения.')
            staged[name] = output
            imported_groups += 1
            total_added += new_in_group

    if not staged:
        return (f'Новых записей нет. Совпадений по ID или содержимому: {total_duplicates}. '
                'Настройки и существующие данные не изменены.')

    # Snapshot the entire current storage so the merge can be rolled back.
    # If backup fails (e.g., corrupt JSON), absolutely nothing is imported.
    if any(p.is_file() and _name_ok(p.name) for p in root.iterdir()):
        backup_path, _ = create_backup()
        backup_note = f' Резервная копия: {backup_path}.'
    else:
        backup_note = ' Текущая папка была пустой.'

    for name, raw in staged.items():
        fd, tmpname = tempfile.mkstemp(prefix='.prompt-aio-', suffix='.tmp', dir=str(root))
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
            os.replace(tmpname, root / name)
        finally:
            if os.path.exists(tmpname):
                os.unlink(tmpname)

    return (f'Объединено: новых записей {total_added}, дубликатов пропущено {total_duplicates}, '
            f'обновлено файлов истории/избранного {imported_groups}. '
            f'Настройки не изменены.{backup_note} Перезапусти Forge Neo.')


def import_backup(blob, *, merge=False):
    files = _read_archive(blob)
    return _merge_import(files) if merge else _write_import(files)


def import_folder(folder, *, merge=False):
    files = _read_folder(folder)
    return _merge_import(files) if merge else _write_import(files)
