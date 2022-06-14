import os

from odd_ge_adapter.domain import RunResult
from tests import test_folder_path

FILE_PATH = os.path.join(test_folder_path, "resources/runs/notification_suite_run.json")


def test_run_result():
    with open(FILE_PATH) as f:
        run_result = RunResult.parse_raw(f.read())

        assert len(run_result.results) == 4
