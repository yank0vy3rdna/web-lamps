from flask import Flask

from handlers.auth import login, check


def setup(app: Flask):
    login.setup(app)
    check.setup(app)
