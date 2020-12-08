from flask import Flask

import services
import handlers

app = Flask(__name__)

services.setup()
handlers.setup(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
