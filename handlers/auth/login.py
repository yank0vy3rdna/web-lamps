from flask import Flask


def login():
    return "token"


def setup(app: Flask):
    app.add_url_rule("/auth/login/", 'login', login)
