from typing import Dict, Any, List
from datetime import datetime
import pydantic

from odd_ge_adapter.domain import Expectation


class RunIdentifier(pydantic.BaseModel):
    run_name: str
    run_time: datetime


class RunResultMeta(pydantic.BaseModel):
    batch_kwargs: Dict[Any, Any]
    expectation_suite_name: str
    great_expectations_version: str
    run_id: RunIdentifier


class ExceptionInfo(pydantic.BaseModel):
    exception_message: str
    exception_traceback: str
    raised_exception: bool


class Result(pydantic.BaseModel):
    expectation_config: Expectation
    meta: Dict[Any, Any]
    result: Dict[Any, Any]
    success: bool


class RunResult(pydantic.BaseModel):
    meta: RunResultMeta
    results: List[Result]
