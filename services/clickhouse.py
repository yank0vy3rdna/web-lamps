import time
from threading import Thread

from clickhouse_driver import Client

from lamps.lamp import Lamp
from utils import config


class ClickHouse:
    def __init__(self):
        self.queue = []
        try:
            self.client = Client(
                host=config.CLICKHOUSE_HOST,
                database=config.CLICKHOUSE_DB,
                user=config.CLICKHOUSE_USER,
                port=config.CLICKHOUSE_PORT,
                password=config.CLICKHOUSE_PASSWORD
            )
            self.client.execute("""CREATE TABLE IF NOT EXISTS lamps (
                           d DateTime DEFAULT now(),
                           lamp_id Int,
                           amperage Float32,
                           voltage Float32,
                           power Float32,
                           isConnected UInt8,
                           isEnabled UInt8
                           )
                            ENGINE MergeTree
                            ORDER BY d
                            TTL d + INTERVAL 2 WEEK
                            """)
        except Exception as e:
            print(e)

    def requests(self):
        while True:
            if len(self.queue) != 0:
                queue = self.queue.copy()
                self.queue.clear()
                try:
                    self.client.execute("OPTIMIZE TABLE lamps")
                    self.client.execute(
                        "INSERT INTO lamps.lamps (* EXCEPT(d)) VALUES",
                        queue
                    )
                except Exception as e:
                    print(e)
            time.sleep(3)

    def record(self, lamp: Lamp):
        if lamp.connected:
            data = (
                int(lamp.lamp_id),
                lamp.amperage,
                lamp.voltage,
                lamp.amperage * lamp.voltage,
                lamp.connected,
                int(lamp.enable)
            )
            self.queue.append(data)


clickhouse = ClickHouse()


def process(clickhouse_instance):
    clickhouse_instance.requests()


dbThread = Thread(target=process, args=(clickhouse,))
dbThread.start()
