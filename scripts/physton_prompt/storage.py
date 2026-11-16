"""Prompt All-in-One JSON storage (Forge Neo compatibility).

v1.1.0 test: no longer searches sibling extensions or automatically imports
another install's files. Manual, explicit import/export lives in portable.py.
"""
import os
import json
import time
from pathlib import Path


class Storage:
    storage_path = ''

    def __init__(self):
        Storage.__dispose_all_locks()

    @staticmethod
    def __get_storage_path(skip_auto_import=False):
        # Keep the old layout and signature for compatibility with earlier
        # releases. In particular, NEVER auto-copy from other extensions.
        Storage.storage_path = str(Path(__file__).resolve().parents[2] / 'storage')
        os.makedirs(Storage.storage_path, exist_ok=True)
        return Storage.storage_path

    @staticmethod
    def __get_data_filename(key):
        return os.path.join(Storage.__get_storage_path(), key + '.json')

    @staticmethod
    def __get_key_lock_filename(key):
        return os.path.join(Storage.__get_storage_path(), key + '.lock')

    @staticmethod
    def __dispose_all_locks():
        directory = Storage.__get_storage_path()
        for filename in os.listdir(directory):
            if filename.endswith('.lock'):
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                    print(f'Disposed lock: {file_path}')
                except Exception as exc:
                    print(f'Dispose lock {file_path} failed: {exc}')

    @staticmethod
    def __lock(key):
        with open(Storage.__get_key_lock_filename(key), 'w') as stream:
            stream.write('1')

    @staticmethod
    def __unlock(key):
        path = Storage.__get_key_lock_filename(key)
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def __is_locked(key):
        return os.path.exists(Storage.__get_key_lock_filename(key))

    @staticmethod
    def __get(key):
        filename = Storage.__get_data_filename(key)
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return None
        try:
            import launch
            if not launch.is_installed('chardet'):
                with open(filename, 'r') as stream:
                    return json.load(stream)
            import chardet
            with open(filename, 'rb') as stream:
                data = stream.read()
            encoding = chardet.detect(data).get('encoding') or 'utf-8'
            return json.loads(data.decode(encoding))
        except Exception:
            try:
                with open(filename, 'r') as stream:
                    return json.load(stream)
            except Exception as exc:
                print(exc)
                return None

    @staticmethod
    def __set(key, data):
        with open(Storage.__get_data_filename(key), 'w') as stream:
            json.dump(data, stream, indent=4, ensure_ascii=True)

    @staticmethod
    def set(key, data):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            Storage.__set(key, data)
        finally:
            Storage.__unlock(key)

    @staticmethod
    def get(key):
        return Storage.__get(key)

    @staticmethod
    def delete(key):
        filename = Storage.__get_data_filename(key)
        if os.path.exists(filename):
            os.remove(filename)

    @staticmethod
    def __get_list(key):
        data = Storage.get(key)
        return data if data else []

    @staticmethod
    def list_push(key, item):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            data.append(item)
            Storage.__set(key, data)
        finally:
            Storage.__unlock(key)

    @staticmethod
    def list_pop(key):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            item = data.pop()
            Storage.__set(key, data)
            return item
        finally:
            Storage.__unlock(key)

    @staticmethod
    def list_shift(key):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            item = data.pop(0)
            Storage.__set(key, data)
            return item
        finally:
            Storage.__unlock(key)

    @staticmethod
    def list_remove(key, index):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            data = Storage.__get_list(key)
            data.pop(index)
            Storage.__set(key, data)
        finally:
            Storage.__unlock(key)

    @staticmethod
    def list_get(key, index):
        return Storage.__get_list(key)[index]

    @staticmethod
    def list_clear(key):
        while Storage.__is_locked(key):
            time.sleep(0.01)
        Storage.__lock(key)
        try:
            Storage.__set(key, [])
        finally:
            Storage.__unlock(key)
