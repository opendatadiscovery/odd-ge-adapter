import os
from odd_ge_adapter.domain import Suite

from tests import test_folder_path

FILE_PATH = os.path.join(test_folder_path, "resources/suites/notification_suite.json")


def test_suite():
    with open(FILE_PATH) as f:
        suite = Suite.parse_raw(f.read())

        assert suite.expectation_suite_name == "notification"
        assert len(suite.expectations) == 4
