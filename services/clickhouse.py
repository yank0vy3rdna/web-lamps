from clickhouse_driver import Client

from lamps.lamp import Lamp
from utils import config


class ClickHouse:
    def __init__(self):
        self.client = Client(
            host=config.CLICKHOUSE_HOST,
            database=config.CLICKHOUSE_DB,
            user=config.CLICKHOUSE_USER,
            port=config.CLICKHOUSE_PORT,
            password=config.CLICKHOUSE_PASSWORD
        )
        self.client.execute("CREATE TABLE IF NOT EXISTS lamps (\
                       d DateTime,\
                       lamp_id Int,\
                       amperage Float32,\
                       voltage Float32,\
                       power Float32,\
                       isConnected UInt8,\
                       isEnabled UInt8\
                       )\
                        ENGINE MergeTree\
                        ORDER BY d\
                        TTL d + INTERVAL 1 YEAR;")

    def record(self, lamp: Lamp):
        a = self.client.execute(
            "INSERT INTO lamps (* EXCEPT(d)) VALUES",
            [(
                lamp.lamp_id,
                lamp.amperage,
                lamp.voltage,
                lamp.amperage * lamp.voltage,
                lamp.connected,
                int(lamp.enable)
            )]
        )
        print(a)



clickhouse = ClickHouse()
