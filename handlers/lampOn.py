from flask import request, Flask

from lamps.lampsRepository import lampsRepository


def lampOn():
    lamp_id = request.args.get('lamp_id')
    lampsRepository.getLampById(lamp_id).on()
    return {"success": True}


def setup(app: Flask):
    app.add_url_rule("/lampOn/", 'lampOn', lampOn)
