from typing import Literal, Optional, Union

import pydantic
from odd_collector_sdk.domain.plugin import Plugin
from pydantic import SecretStr
from typing_extensions import Annotated


class LocalStoragePlugin(Plugin):
    type: Literal["local"]
    suites_path: pydantic.FilePath
    results_path: pydantic.FilePath


class S3StoragePlugin(Plugin):
    type: Literal["s3"]
    bucket: str
    results_key: str
    suites_key: str
    aws_access_key_id: Optional[SecretStr]
    aws_secret_access_key: Optional[SecretStr]
    aws_region: Optional[str]


AvailablePlugin = Annotated[
    Union[S3StoragePlugin, LocalStoragePlugin],
    pydantic.Field(discriminator="type"),
]
