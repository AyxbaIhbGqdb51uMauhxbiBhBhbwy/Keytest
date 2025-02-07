from flask import Flask, jsonify
from api.key_generator import key

app = Flask(__name__)

@app.route('/get-key', methods=['GET'])
def get_key():
    return jsonify({"key": key})

def handler(event, context):
    return app(event, context)
