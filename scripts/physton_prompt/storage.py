import os
import json
import time
import shutil
from pathlib import Path


class Storage:
    storage_path = ''

    def __init__():
        Storage.__dispose_all_locks()

    def import_from_old(overwrite=False):
        """
        Import JSON data from older sibling versions of the extension.

        Returns a dict with import statistics. By default, existing files in
        the current storage are preserved. If overwrite=True, matching JSON
        files are replaced by the older-extension copies.
        """
        storage_path = Storage.__get_storage_path(skip_auto_import=True)
        current_root = Path(storage_path).resolve().parent

        candidates = [
            current_root.parent / 'sd-webui-prompt-all-in-one' / 'storage',
            current_root.parent / 'sd-webui-prompt-all-in-one-forgeneo' / 'storage',
        ]

        imported = []
        overwritten = []
        skipped = []
        sources_found = []

        for candidate in candidates:
            candidate = candidate.resolve()
            if candidate == Path(storage_path).resolve():
                continue
            if not candidate.exists() or not candidate.is_dir():
                continue

            sources_found.append(str(candidate))

            try:
                for src_file in candidate.iterdir():
                    if not src_file.is_file():
                        continue
                    if src_file.suffix.lower() != '.json':
                        continue

                    dst_file = Path(storage_path) / src_file.name

                    if dst_file.exists() and not overwrite:
                        skipped.append(src_file.name)
                        continue

                    shutil.copy2(src_file, dst_file)
                    if dst_file.exists() and src_file.name in skipped:
                        skipped.remove(src_file.name)

                    if overwrite and dst_file.exists():
                        overwritten.append(src_file.name)
                    else:
                        imported.append(src_file.name)
            except Exception as e:
                print(f"[sd-webui-prompt-all-in-one] Import skipped for {candidate}: {e}")

        return {
            'sources_found': sources_found,
            'imported': sorted(set(imported)),
            'overwritten': sorted(set(overwritten)),
            'skipped': sorted(set(skipped)),
        }

    def __auto_import_storage(storage_path):
        sentinel = os.path.join(storage_path, '.auto_import_done')
        if os.path.exists(sentinel):
            return

        result = Storage.import_from_old(overwrite=False)

        try:
            with open(sentinel, 'w', encoding='utf8') as f:
                f.write('1')
        except Exception:
            pass

        count = len(result['imported'])
        if count:
            print('[sd-webui-prompt-all-in-one] Storage auto import completed.')
            print(f'  imported files: {count}')
            for name in result['imported']:
                print(f'  - {name}')
        else:
            print('[sd-webui-prompt-all-in-one] Storage auto import: nothing to import.')

    def __get_storage_path(skip_auto_import=False):
        Storage.storage_path = os.path.dirname(os.path.abspath(__file__)) + '/../../storage'
        Storage.storage_path = os.path.normpath(Storage.storage_path)
        if not os.path.exists(Storage.storage_path):
            os.makedirs(Storage.storage_path)

        if not skip_auto_import:
            Storage.__auto_import_storage(Storage.storage_path)

        return Storage.storage_path

    def __get_data_filename(key):
        return Storage.__get_storage_path() + '/' + key + '.json'

    def __get_key_lock_filename(key):
        return Storage.__get_storage_path() + '/' + key + '.lock'

    def __dispose_all_locks():
        directory = Storage.__get_storage_path()
        for filename in os.listdir(directory):
            if filename.endswith('.lock'):
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                    print(f"Disposed lock: {file_path}")
                except Exception as e:
                    print(f"Dispose lock {file_path} failed: {e}")

    def __lock(key):
        file_path = Storage.__get_key_lock_filename(key)
        with open(file_path, 'w') as f:
            f.write('1')

    def __unlock(key):
        file_path = Storage.__get_key_lock_filename(key)
        if os.path.exists(file_path):
            os.remove(file_path)

    def __is_locked(key):
        file_path = Storage.__get_key_lock_filename(key)
        return os.path.exists(file_path)

    def __get(key):
        filename = Storage.__get_data_filename(key)
        if not os.path.exists(filename):
            return None
        if os.path.getsize(filename) == 0:
            return None
        try:
            import launch
            if not launch.is_installed("chardet"):
                with open(filename, 'r') as f:
                    data = json.load(f)
            else:
                import chardet
                with open(filename, 'rb') as f:
                    data = f.read()
                    encoding = chardet.detect(data).get('encoding')
                    data = json.loads(data.decode(encoding))
        except Exception as e:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(e)
                return None
        return data

    def __set(key, data):
        file_path = Storage.__get_data_filename(key)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=True)

    def set(key, data):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            Storage.__set(key, data)
            Storage.__unlock(key)
        except Exception as e:
            Storage.__unlock(key)
            raise e

    def get(key):
        return Storage.__get(key)

    def delete(key):
        file_path = Storage.__get_data_filename(key)
        if os.path.exists(file_path):
            os.remove(file_path)

    def __get_list(key):
        data = Storage.get(key)
        if not data:
            data = []
        return data

    def list_push(key, item):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            data.append(item)
            Storage.__set(key, data)
            Storage.__unlock(key)
        except Exception as e:
            Storage.__unlock(key)
            raise e

    def list_pop(key):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            item = data.pop()
            Storage.__set(key, data)
            Storage.__unlock(key)
            return item
        except Exception as e:
            Storage.__unlock(key)
            raise e

    def list_shift(key):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            item = data.pop(0)
            Storage.__set(key, data)
            Storage.__unlock(key)
            return item
        except Exception as e:
            Storage.__unlock(key)
            raise e

    def list_remove(key, index):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        data = Storage.__get_list(key)
        data.pop(index)
        Storage.__set(key, data)
        Storage.__unlock(key)

    def list_get(key, index):
        data = Storage.__get_list(key)
        return data[index]

    def list_clear(key):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            Storage.__set(key, [])
            Storage.__unlock(key)
        except Exception as e:
            Storage.__unlock(key)
            raise e
