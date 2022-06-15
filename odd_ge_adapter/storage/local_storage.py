import os
from typing import Type, TypeVar

from pydantic import BaseModel, FilePath, DirectoryPath

from odd_ge_adapter.domain import Suite, RunResult
from odd_ge_adapter.storage import Storage

U = TypeVar("U", bound=BaseModel)


class LocalStorage(BaseModel, Storage):
    suites_path: DirectoryPath
    results_path: DirectoryPath

    def load_suites(self):
        yield from self._get_files(self.suites_path, Suite)

    def load_results(self):
        yield from self._get_files(self.results_path, RunResult)

    @staticmethod
    def _get_files(folder_path: DirectoryPath, cls: Type[U]):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                yield cls.parse_raw(file.read())
