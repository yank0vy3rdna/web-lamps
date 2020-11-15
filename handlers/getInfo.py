import json

from flask import Flask

from lamps.lampsRepository import lampsRepository


def getInfo():
    return lampsRepository.to_json()


def setup(app: Flask):
    app.add_url_rule("/getInfo/", 'getInfo', getInfo)
