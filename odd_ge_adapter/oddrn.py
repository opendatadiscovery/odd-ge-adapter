from typing import Optional

from oddrn_generator import Generator
from oddrn_generator.path_models import BasePathsModel
from oddrn_generator.server_models import AWSCloudModel


class GreatExpectationPathsModel(BasePathsModel):
    suites: Optional[str]
    types: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            "suites": ("suites",),
            "types": ("suites", "types"),
            "runs": ("suites", "types", "runs"),
        }


class GreatExpectationGenerator(Generator):
    source = "greatexpectation"
    paths_model = GreatExpectationPathsModel
    server_model = AWSCloudModel
