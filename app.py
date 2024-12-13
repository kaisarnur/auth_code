from flask import Flask, jsonify
from asgiref.wsgi import WsgiToAsgi
import random

app = Flask(__name__)

@app.route('/auth_code', methods=['GET'])
def auth_code():
    code = random.randint(1000, 9999)
    return jsonify({
        "response_type": "ephemeral",
        "text": f"Ваш код: {code}"
    })

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(debug=True)
