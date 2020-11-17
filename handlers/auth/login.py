from flask import Flask, request, Response


def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == "admin" and password == "qwerty123":
        return "token"
    return Response(status=403)


def setup(app: Flask):
    app.add_url_rule("/auth/login/", 'login', login, methods=['POST'])
