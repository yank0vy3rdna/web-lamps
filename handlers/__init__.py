from flask import Flask

from handlers import getInfo, lampOff, lampOn


def setup(app: Flask):
    getInfo.setup(app)
    lampOff.setup(app)
    lampOn.setup(app)
