from flask import Flask, request


def login():
    login = request.args.get('login')
    password = request.args.get('password')
    if login == "admin" and password == "qwerty123":
        return "token"
    raise ValueError("Auth error")


def setup(app: Flask):
    app.add_url_rule("/auth/login/", 'login', login, methods=['POST'])
