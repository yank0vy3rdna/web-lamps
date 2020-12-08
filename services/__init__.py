from .clickhouse import clickhouse
from . import lamps_checker, suntime

def setup():
    lamps_checker.setup()
    suntime.setup()
