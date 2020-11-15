from flask import Flask

from handlers import getInfo


def setup(app: Flask):
    getInfo.setup(app)
