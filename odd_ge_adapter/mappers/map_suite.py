import logging
from typing import List

from odd_models.models import (
    DataEntity,
    DataQualityTest,
    DataQualityTestExpectation,
    DataEntityType,
)
from oddrn_generator.generators import S3Generator

from odd_ge_adapter.domain import Suite, Expectation, S3Uri
from odd_ge_adapter.mappers.s3_uri_to_oddrn import s3_uri_to_oddrn
from odd_ge_adapter.oddrn import GreatExpectationGenerator


def _dataset_list_to_oddrn(
    dataset_list: List[str], oddrn_gen: S3Generator
) -> List[str]:
    s3_uris = [S3Uri(dataset) for dataset in dataset_list]
    return [s3_uri_to_oddrn(s3_uri, oddrn_gen) for s3_uri in s3_uris]


def _get_dataset_list(suite: Suite, oddrn: S3Generator) -> List[str]:
    """
    Try to get dataset list. Wait that dataset list set in:  meta -> batch_kwargs -> odd_metadata

    Examples:
        ['s3://bucket/folder','s3://bucket/folder/sub_folder']
    """

    try:
        datasets = suite.meta.get("batch_kwargs").get("odd_metadata")
        return _dataset_list_to_oddrn(datasets, oddrn)
    except KeyError as e:
        logging.exception("Couldn't take meta data")


def _map_expectation(
    expectation: Expectation,
    dataset_list: List[str],
    oddrn_generator: GreatExpectationGenerator,
) -> DataEntity:
    """
    Map expectation to DataEntity

    Args:
        expectation: odd_ge_adapter.domain.Expectation
        oddrn_generator: GreatExpectationGenerator

    """

    suite_name = oddrn_generator.get_oddrn_by_path("suites")

    expectation_type = expectation.unique_type
    qt = DataQualityTest(
        suite_name=suite_name,
        expectation=DataQualityTestExpectation(
            type=expectation_type,
            additionalProperties=str(expectation.kwargs),
        ),
        dataset_list=dataset_list,
    )

    oddrn_generator.set_oddrn_paths(types=expectation_type)
    return DataEntity(
        oddrn=oddrn_generator.get_oddrn_by_path("types"),
        name=f"{suite_name}.{expectation_type}",
        type=DataEntityType.JOB,
        metadata=[],
        data_quality_test=qt,
    )


def map_suite(
    suite: Suite,
    oddrn_generator: GreatExpectationGenerator,
    s3_oddrn_generator: S3Generator,
) -> List[DataEntity]:
    """
    Returns list of mapped odd_ge_adapter.domain.Expectation.
    Traiting each expectation as is an individual entity with oddrn

    Args:
        suite: odd_ge_adapter.domain.Suite
        oddrn_generator: GreatExpectationGenerator
        s3_oddrn_generator: S3Generator - needs for cast datasets to oddrn
    """

    dataset_list = _get_dataset_list(suite, s3_oddrn_generator)

    oddrn_generator.set_oddrn_paths(suites=suite.expectation_suite_name)

    return [
        _map_expectation(exp, dataset_list, oddrn_generator)
        for exp in suite.expectations
    ]
