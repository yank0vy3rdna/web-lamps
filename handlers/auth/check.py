from flask import Flask


def check():
    return "token"


def setup(app: Flask):
    app.add_url_rule("/auth/check/", 'check', check)
