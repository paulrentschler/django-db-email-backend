# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO

from django.core.files.storage import Storage


class TestStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.reset()

    def _open(self, name, mode='rb'):
        if not self.exists(name):
            if 'w' in mode:
                self.save(name, '')
                return self._file_system[name]
            else:
                raise IOError("[Errno 2] No such file or directory: '{}'".format(name))
        return self._file_system[name]

    def _save(self, name, content):
        f = BytesIO()
        f.write(content.read())
        f.seek(0)
        if self.exists(name):
            name = self.get_available_name(name)
        self._file_system[name] = f
        return name

    def delete(self, name):
        """
        Deletes the specified file from the storage system.
        """
        if self.exists(name):
            del self._file_system['name']
        else:
            raise OSError("[Errno 2] No such file or directory: '{}'".format(name))

    def exists(self, name):
        return name in self._file_system

    def reset(self):
        self._file_system = {}
