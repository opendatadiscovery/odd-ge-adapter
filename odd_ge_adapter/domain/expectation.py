from typing import Any, Dict

import pydantic


class Expectation(pydantic.BaseModel):
    expectation_type: str
    kwargs: Dict[str, Any]
    meta: Dict[str, Any]

    @property
    def unique_type(self):
        """
        Returns
        self.expectation_type -> for common expectations
        self.expectation_type + column_name -> for columns expectations, because need to generate unique oddrn
        """

        if self.expectation_type.startswith("expect_column_values"):
            return f"{self.expectation_type}:{self.kwargs.get('column')}"

        return self.expectation_type
