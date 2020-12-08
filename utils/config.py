from envparse import env

from . import cli

env.read_envfile(cli.CONFIG_FILE)

CLICKHOUSE_LOGGING_ENABLED = env.bool("CLICKHOUSE_LOGGING_ENABLED", default=False)
CLICKHOUSE_HOST = env.str("CLICKHOUSE_HOST", default="localhost")
CLICKHOUSE_USER = env.str("CLICKHOUSE_USER", default="default")
CLICKHOUSE_PASSWORD = env.str("CLICKHOUSE_PASSWORD", default="")
CLICKHOUSE_PORT = env.int("CLICKHOUSE_PORT", default=9000)
CLICKHOUSE_DB = env.str("CLICKHOUSE_DB", default="default")
