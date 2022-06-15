import logging
from itertools import chain
from typing import Generator, Type, TypeVar

import boto3
from odd_collector_sdk.domain.adapter import AbstractAdapter
from odd_models.models import DataEntityList
from oddrn_generator.generators import S3Generator

from odd_ge_adapter.domain import Suite, RunResult
from odd_ge_adapter.domain.plugin import S3StoragePlugin
from odd_ge_adapter.mappers import map_result, map_suite
from odd_ge_adapter.oddrn import GreatExpectationGenerator

K = TypeVar("K", Suite, RunResult)


class Adapter(AbstractAdapter):
    def __init__(self, config: S3StoragePlugin):
        self._suites_key = config.suites_key
        self._results_key = config.results_key
        self._bucket = config.bucket

        self._s3 = boto3.client(
            "s3",
            aws_access_key_id=config.aws_access_key_id.get_secret_value(),
            aws_secret_access_key=config.aws_secret_access_key.get_secret_value(),
            region_name=config.aws_region,
        )
        account_id = boto3.client(
            "sts",
            aws_access_key_id=config.aws_access_key_id.get_secret_value(),
            aws_secret_access_key=config.aws_secret_access_key.get_secret_value(),
        ).get_caller_identity()["Account"]

        self._ge_oddrn = GreatExpectationGenerator(
            cloud_settings={
                "account": account_id,
                "region": config.aws_region,
            }
        )
        self._s3_oddrn = S3Generator(
            cloud_settings={
                "account": account_id,
                "region": config.aws_region,
            }
        )

    def get_data_entity_list(self) -> DataEntityList:
        items = list(chain(*self.load_suites(), *self.load_results()))

        return DataEntityList(
            data_source_oddrn=self.get_data_source_oddrn(), items=items
        )

    def get_data_source_oddrn(self) -> str:
        return self._ge_oddrn.get_data_source_oddrn()

    def load_results(self):
        results = self._fetch_list(prefix=self._results_key, cls=RunResult)

        return [
            map_result(result, self._ge_oddrn, self._s3_oddrn) for result in results
        ]

    def load_suites(self):
        suites = self._fetch_list(prefix=self._suites_key, cls=Suite)

        result = []
        for suite in suites:
            mapped_suite = map_suite(suite, self._ge_oddrn, self._s3_oddrn)

            result.append(mapped_suite)

        return result

    def _load_contents(self, key: str) -> str:
        response = self._s3.get_object(Bucket=self._bucket, Key=key)
        return response["Body"].read().decode("utf-8")

    def _fetch_list(self, prefix: str, cls: Type[K]) -> Generator[K, None, None]:
        paginator = self._s3.get_paginator("list_objects_v2")

        responses = list(paginator.paginate(Bucket=self._bucket, Prefix=prefix))
        contents = [c for r in responses for c in r.get("Contents")]

        return (
            cls.parse_raw(self._load_contents(c["Key"]))
            for c in contents
            if not c["Key"].endswith("/")
        )
