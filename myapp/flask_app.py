from flask import Flask

from flask_view import base_bp


app = Flask(__name__)

app.register_blueprint(base_bp)
