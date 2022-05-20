from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime


class Metadata(BaseModel):
    schema_url: str = "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/ge.json#/definitions/GEMetadataExtension"
    metadata: Optional[Dict] = {}


class Expectation(BaseModel):
    type: str
    additionalProperties: str


class DataQualityTest(BaseModel):
    suite_name: str
    dataset_list: List[str]
    expectation: Expectation
    suite_url: Optional[str]
    linked_url_list: Optional[List]


class DataQualityTestRun(BaseModel):
    data_quality_test_oddrn: str
    start_time: str
    end_time: str
    status_reason: Optional[str]
    status: str


class DataEntity(BaseModel):
    oddrn: str
    name: str
    description: str = Field(None, alias="desc")
    owner: str = None
    metadata: Optional[List[Metadata]] = [Metadata()]
    updated_at: datetime = datetime.now().isoformat()
    created_at: datetime = datetime.now().isoformat()
    data_quality_test: Optional[DataQualityTest]
    data_quality_test_run: Optional[DataQualityTestRun]
