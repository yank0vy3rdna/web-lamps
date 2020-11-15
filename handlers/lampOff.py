from flask import request, Flask

from lamps.lampsRepository import lampsRepository


def lampOff():
    lamp_id = request.args.get('lamp_id')
    lampsRepository.getLampById(lamp_id).off()
    return {"success": True}


def setup(app: Flask):
    app.add_url_rule("/lampOff/", 'lampOff', lampOff)
