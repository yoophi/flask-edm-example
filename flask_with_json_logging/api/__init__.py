from flask import Blueprint, jsonify, request

from flask_with_json_logging import commands
from flask_with_json_logging.bus import bus

api = Blueprint('api', __name__)


@api.route('/')
def index():
    message = request.args.get('message')
    command = commands.SayHello(message=message)
    resp = bus.handle(command)
    if not resp:
        return 'error occurred', 400

    return jsonify(message=resp)
