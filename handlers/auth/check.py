from flask import Flask, request


def check():
    token = request.args.get('token')
    if token == "token":
        return 'true'
    else:
        return 'false'


def setup(app: Flask):
    app.add_url_rule("/auth/check/", 'check', check)
