from oddrn import Generator

from .settings import *

ge_generator = Generator(data_source=GE_SOURCE, cloud=CLOUD)


def get_datasource_oddrn() -> str:
    return ge_generator.get_base()

def get_quality_test_oddrn(suit_name: str, expectation_type: str) -> str:
    return ge_generator.get_qt(suit_name, expectation_type)

def get_quality_test_run_oddrn(run_name: str, expectation_type: str) -> str:
    return ge_generator.get_qt_run(run_name, expectation_type)
