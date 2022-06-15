import pydantic
from typing import Dict, Any, List

from odd_ge_adapter.domain import Expectation


class Suite(pydantic.BaseModel):
    expectation_suite_name: str
    expectations: List[Expectation]
    meta: Dict[str, Any]
