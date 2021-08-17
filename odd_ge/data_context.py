import re
import logging
import requests

from datetime import datetime
from typing import List
from great_expectations import DataContext

from .settings import CATALOG_URL, METADATA_SCHEMA_URL
from .dataclasses import DataEntity, Metadata, DataQualityTestRun, DataQualityTest, Expectation
from .oddrn import get_datasource_oddrn, get_quality_test_run_oddrn, get_quality_test_oddrn

logger = logging.getLogger(__name__)

class DataContext(DataContext):
    def run_validation_operator(self, *args, **kwargs):
        logger.info("Run ODD GE adapter run_validation_operator")
        start_time = datetime.now().isoformat()

        response = super().run_validation_operator(*args, **kwargs)

        run_name = response["run_id"].run_name
        end_time = datetime.now().isoformat()

        data = []
        identifier, run_results = [(key,value) for key, value in response["run_results"].items()][0]
        suite_name = self._get_suite_name(identifier)
        for item in run_results["validation_result"]["results"]:
            expectation_type = item["expectation_config"]["expectation_type"]
            qt_oddrn = get_quality_test_oddrn(suit_name=suite_name, expectation_type=expectation_type)

            qt_run = DataQualityTestRun(
                data_quality_test_oddrn=qt_oddrn,
                start_time=start_time,
                end_time=end_time,
                status="SUCCESS" if item["success"] else "FAILED"
            )

            qt_run_entity = DataEntity(
                oddrn=get_quality_test_run_oddrn(run_name=run_name, expectation_type=expectation_type),
                name=f"{run_name}.{expectation_type}",
                metadata=[Metadata(
                    metadata=item["meta"],
                    schema_url=METADATA_SCHEMA_URL
                )],
                data_quality_test_run=qt_run
            )

            data.append(qt_run_entity.dict(exclude_none=True))

        self._send_data(data)
        return response

    def save_expectation_suite(self, expectation_suite, expectation_suite_name=None):
        logger.info("Run ODD GE adapter save_expectation_suite")
        suite_name = expectation_suite_name or expectation_suite["expectation_suite_name"]

        data = []
        dataset = expectation_suite["meta"]["BasicSuiteBuilderProfiler"]["batch_kwargs"]["data_asset_name"]
        for item in expectation_suite["expectations"]:
            qt = DataQualityTest(
                suite_name=suite_name,
                expectation=Expectation(
                    type=item["expectation_type"],
                    additionalProperties=str(item["kwargs"])
                ),
                dataset_list=[dataset]
            )

            qt_entity = DataEntity(
                oddrn=get_quality_test_oddrn(suit_name=expectation_suite_name, expectation_type=item["expectation_type"]),
                name=f"{suite_name}.{item['expectation_type']}",
                metadata=[Metadata(
                    metadata=item["meta"],
                    schema_url=METADATA_SCHEMA_URL
                )],
                data_quality_test=qt
            )

            data.append(qt_entity.dict(exclude_none=True))

        self._send_data(data)
        super().save_expectation_suite(expectation_suite, expectation_suite_name=None)


    def _get_suite_name(self, identifier) -> str:
        return identifier._expectation_suite_identifier._expectation_suite_name

    def _send_data(self, data: List[dict]):
        request_data = {
            "data_source_oddrn": get_datasource_oddrn(),
            "items": data
        }

        url = CATALOG_URL

        r = requests.post(url, json=request_data)

        if r.status_code == 200:
            logger.info(f"Data transfer success")
        else:
            logger.error(f"Error on catalog request. Code: {r.status_code}, Message: {r.text}")
