import json

from lamps.lamp import Lamp


class LampsRepository:
    lamps = {}

    def __init__(self):
        data = self.read_file()
        self.make_lamps(data)

    def make_lamps(self, data):
        for i in data:
            disable_control = data[i].get("disable_control", False)
            disable_sun_control = data[i].get("disable_sun_control", False)
            lamp = Lamp(i, data[i]["lampx"], data[i]["lampy"], data[i]["lampline"], data[i]["type"], disable_control,
                        disable_sun_control)
            self.lamps.update({i: lamp})

    def allOn(self, sun=False):
        for i in self.lamps:
            lamp = self.getLampById(i)
            if not lamp.disable_sun_control and sun:
                lamp.on()

    def allOff(self, sun=False):
        for i in self.lamps:
            lamp = self.getLampById(i)
            if not lamp.disable_sun_control and sun:
                lamp.off()

    def getLampById(self, lamp_id) -> Lamp:
        return self.lamps.get(lamp_id)

    def read_file(self):
        with open('lamps.json', 'r') as file:
            return json.loads(file.read())

    def to_json(self):
        lamps_list = [(i, self.lamps[i].to_dict()) for i in self.lamps]
        return json.dumps(dict(lamps_list))


lampsRepository = LampsRepository()
