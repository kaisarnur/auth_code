from flask import Flask, jsonify, request
from asgiref.wsgi import WsgiToAsgi
import random
import hmac
import hashlib
import time

app = Flask(__name__)

SLACK_SIGNING_SECRET = 'c5e5338e943f98d86bbf8c5b32974032'


def verify_slack_signature(slack_post_request, slack_signing_secret):
    slack_signing_secret = bytes(slack_signing_secret, 'utf-8')
    slack_signature = slack_post_request.headers.get('X-Slack-Signature')
    slack_request_timestamp = slack_post_request.headers.get('X-Slack-Request-Timestamp')

    if not slack_signature or not slack_request_timestamp:
        return False

    if abs(time.time() - int(slack_request_timestamp)) > 60 * 5:
        return False

    request_body = slack_post_request.get_data(as_text=True)
    basestring = f"v0:{slack_request_timestamp}:{request_body}".encode('utf-8')
    my_signature = 'v0=' + hmac.new(slack_signing_secret, basestring, hashlib.sha256).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)


@app.route('/auth_code', methods=['POST'])
def auth_code():
    if not verify_slack_signature(request, SLACK_SIGNING_SECRET):
        return jsonify({"error": "Invalid request signature"}), 400

    data = {
        "text": "\n        - - - - Қазақстан - - - -\n        \nСОП:\n        🤙 За этот месяц - 0 смен\n        🤙 За прошлый месяц - 2849 смен\n        🤙 За все время - 105475 смен\n        🤙 Запрошено в этом месяце - None исполнителей\n        \nБОП:\n        🤙 За этот месяц - 0 заявок\n        🤙 За прошлый месяц - 54 заявок\n        🤙 За все время - 3209 заявок\n        \n        - - - - Кыргызстан - - - -\n        \nСОП:\n        🤙 За этот месяц - 0 смен\n        🤙 За прошлый месяц - 247 смен\n        🤙 За все время - 6014 смен\n        🤙 Запрошено в этом месяце - None исполнителей\n        \nБОП:\n        🤙 За этот месяц - 0 заявок\n        🤙 За прошлый месяц - 0 заявок\n        🤙 За все время - 24 заявок\n        \n        - - - - O'zbekiston - - - -\n        \nСОП:\n        🤙 За этот месяц - 0 смен\n        🤙 За прошлый месяц - 141 смен\n        🤙 За все время - 1038 смен\n        🤙 Запрошено в этом месяце - None исполнителей\n        \nБОП:\n        🤙 За этот месяц - 0 заявок\n        🤙 За прошлый месяц - 0 заявок\n        🤙 За все время - 31 заявок\n        "
    }
    return jsonify(data)

    # code = random.randint(1000, 9999)
    #
    # return jsonify({
    #     "response_type": "ephemeral",
    #     "text": f"Ваш код: {code}"
    # })


asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(debug=True)
