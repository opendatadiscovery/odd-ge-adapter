import os

from odd_models.models import DataEntityType
from oddrn_generator.generators import S3Generator

from odd_ge_adapter.domain import Suite
from odd_ge_adapter.mappers import map_suite
from odd_ge_adapter.oddrn import GreatExpectationGenerator
from tests import test_folder_path

FILE_PATH = os.path.join(test_folder_path, "resources/suites/notification_suite.json")


def test_map_suite():
    with open(FILE_PATH) as f:
        suite = Suite.parse_raw(f.read())

        oddrn_generator = GreatExpectationGenerator(
            cloud_settings={
                "account": "foo",
                "region": "bar",
            }
        )

        s3_oddrn_generator = S3Generator(
            cloud_settings={
                "account": "foo",
                "region": "bar",
            }
        )

        expectations_list = map_suite(suite, oddrn_generator, s3_oddrn_generator)

        assert len(expectations_list) == 4

        first_entity = expectations_list[0]
        assert first_entity.type == DataEntityType.JOB

        dataset_list = first_entity.data_quality_test.dataset_list

        assert len(dataset_list) == 1
        assert (
            dataset_list[0]
            == "//s3/cloud/aws/account/foo/region/bar/buckets/bucket/keys/folder"
        )

        oddrns = {de.oddrn for de in expectations_list}
        assert len(expectations_list) == len(oddrns)
