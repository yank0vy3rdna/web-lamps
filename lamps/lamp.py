import socket

from services import clickhouse
from utils import config

getDataRequest = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lampOFFRequest = [1, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lampONRequest = [1, 160, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ku = 0.306
ki = 0.0245


class Lamp:
    lamp_id = None
    ip = None
    amperage = 0
    enable = False
    voltage = 0
    connected = None
    map_x = None
    map_y = None
    disable_control = None
    disable_sun_control = None
    lamp_line = None
    lamp_type = None

    def __init__(self, lamp_id, map_x, map_y, lamp_line, lamp_type, disable_control=False, disable_sun_control=False):
        self.lamp_id = lamp_id
        self.map_x = map_x
        self.lamp_type = lamp_type
        self.lamp_line = lamp_line
        self.map_y = map_y
        self.disable_control = disable_control
        self.disable_sun_control = disable_sun_control
        self.ip = '10.200.120.' + str(self.lamp_id)

    def request(self, body):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(bytes(body), 0, (self.ip, 8888))
            return list(sock.recv(1024))
        except Exception:
            self.connected = 0

    def update(self):
        data = self.request(getDataRequest)
        if data:
            self.get_data(data)
        if config.CLICKHOUSE_LOGGING_ENABLED:
            try:
                clickhouse.clickhouse.record(self)
            except Exception as e:
                print(e)

    def get_data(self, data):
        highByte = data[28] << 8
        lowByte = data[27] & 0x00ff
        self.amperage = highByte | lowByte
        highByte = data[20] << 8
        lowByte = data[21] & 0x00ff
        self.voltage = highByte | lowByte
        self.voltage = ku * self.voltage
        if self.amperage - 512 < 0:
            self.amperage = (512 - self.amperage) * ki
        else:
            self.amperage = (self.amperage - 512) * ki
        self.enable = data[29] == 0
        self.connected = 1

    def on(self):
        if not self.disable_control:
            data = self.request(lampONRequest)
            if data:
                self.get_data(data)
            if config.CLICKHOUSE_LOGGING_ENABLED:
                clickhouse.record(self)

    def off(self):
        if not self.disable_control:
            data = self.request(lampOFFRequest)
            if data:
                self.get_data(data)
            if config.CLICKHOUSE_LOGGING_ENABLED:
                clickhouse.record(self)

    def to_dict(self):
        return {
            "amperage": self.amperage,
            "connected": self.connected,
            "enable": self.enable,
            "id": self.lamp_id,
            "lampline": self.lamp_line,
            "lampx": self.map_x,
            "lampy": self.map_y,
            "type": self.lamp_type,
            "voltage": self.voltage
        }
