import os

from oddrn_generator.generators import S3Generator
from odd_models.models import DataEntityType


from odd_ge_adapter.domain import RunResult
from odd_ge_adapter.mappers import map_result
from odd_ge_adapter.oddrn import GreatExpectationGenerator
from tests import test_folder_path

FILE_PATH = os.path.join(test_folder_path, "resources/runs/notification_suite_run.json")


def test_map_results():
    with open(FILE_PATH) as f:
        run_result = RunResult.parse_raw(f.read())

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

        expectations_list = map_result(run_result, oddrn_generator, s3_oddrn_generator)

        assert len(expectations_list) == 4
        assert expectations_list[0].type == DataEntityType.JOB_RUN

        oddrns = {de.oddrn for de in expectations_list}
        assert len(expectations_list) == len(oddrns)

        metadata = expectations_list[0].metadata[0].metadata
        assert "dataset" in metadata
        assert len(metadata.get("dataset")) == 1
        assert (
            metadata.get("dataset")[0]
            == "//s3/cloud/aws/account/foo/region/bar/buckets/bucket/keys/folder:file.csv"
        )
