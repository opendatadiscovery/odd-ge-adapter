from datetime import datetime
import logging
from typing import List

from oddrn_generator.generators import S3Generator
from odd_models.models import (
    DataEntity,
    DataQualityTestRun,
    QualityRunStatus,
    DataEntityType,
    MetadataExtension,
)

from odd_ge_adapter.domain import RunResult, Result, RunResultMeta
from odd_ge_adapter.domain.s3_uri import S3Uri
from odd_ge_adapter.mappers.s3_uri_to_oddrn import s3_uri_to_oddrn
from odd_ge_adapter.oddrn import GreatExpectationGenerator


def map_result(
    run_result: RunResult,
    oddrn_generator: GreatExpectationGenerator,
    s3_oddrn_generator: S3Generator,
) -> List[DataEntity]:
    """
    Mapping through each validation result

    Args:
        run_result: odd_ge_adapter.domain.RunResult
        oddrn_generator: GreatExpectationGenerator
    Returns:
        List[DataEntity]
    """
    suite_name = run_result.meta.expectation_suite_name

    run_id = run_result.meta.run_id
    run_name = run_id.run_name
    run_time = run_id.run_time

    metadata = _map_metadata(run_result.meta, s3_oddrn_generator)

    oddrn_generator.set_oddrn_paths(suites=suite_name)

    return [
        _map_result(result, run_name, run_time, run_time, metadata, oddrn_generator)
        for result in run_result.results
    ]


def _map_result(
    result: Result,
    run_name: str,
    start_time: datetime,
    end_time: datetime,
    metadata: MetadataExtension,
    oddrn_generator: GreatExpectationGenerator,
) -> DataEntity:
    expectation_type = result.expectation_config.unique_type

    oddrn_generator.set_oddrn_paths(types=expectation_type, runs=run_name)

    qt_run = DataQualityTestRun(
        data_quality_test_oddrn=oddrn_generator.get_oddrn_by_path("types"),
        start_time=start_time,
        end_time=end_time,
        status=_map_status(result.success),
    )

    return DataEntity(
        oddrn=oddrn_generator.get_oddrn_by_path("runs"),
        name=f"{run_name}.{expectation_type}",
        type=DataEntityType.JOB_RUN,
        metadata=[metadata],
        data_quality_test_run=qt_run,
    )


def _map_status(success: bool):
    return QualityRunStatus.SUCCESS if success else QualityRunStatus.FAILED


def _map_metadata(
    run_meta: RunResultMeta, s3_oddrn_generator: S3Generator
) -> MetadataExtension:
    run_id = run_meta.run_id

    try:
        uris = run_meta.batch_kwargs.get("odd_metadata")
        datasets = [s3_uri_to_oddrn(S3Uri(uri), s3_oddrn_generator) for uri in uris]
    except KeyError:
        datasets = []
        logging.exception("Could not get dataset name")

    meta = {
        "version": run_meta.great_expectations_version,
        "expectation_suite_name": run_meta.expectation_suite_name,
        "run_name": run_id.run_name,
        "run_time": run_id.run_time,
        "dataset": datasets,
    }

    return MetadataExtension(
        schema_url="https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/great_expectations.json#/definitions/GreatExpectationsMetadata",
        metadata=meta,
    )
