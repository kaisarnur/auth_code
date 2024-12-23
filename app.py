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

    # code = random.randint(1000, 9999)
    # print(request.form)
    # print(request.form.get('token'))
    # return jsonify({
    #     "response_type": "in_channel",
    #     "text": f"Ваш код: {code}"
    # })
    data = request.form
    user_id = data.get('user_id')
    command_text = data.get('text')  # Содержит ссылку из команды
    response_url = data.get('response_url')  # URL для ответа

    message = {
        "response_type": "in_channel",
        "text": f"<@{user_id}> начал deploy: {command_text}",
        "attachments": [
            {
                "text": "Когда закончите, нажмите на кнопку:",
                "callback_id": "deploy_action",
                "actions": [
                    {
                        "name": "done",
                        "text": "Закончил",
                        "type": "button",
                        "value": "done"
                    }
                ]
            }
        ]
    }

    return jsonify(message)

@app.route('/slack/actions', methods=['POST'])
def handle_actions():
    payload = request.form.get('payload')
    if not payload:
        return jsonify({"error": "No payload received"}), 400

    action_data = json.loads(payload)
    user_id = action_data['user']['id']
    callback_id = action_data['callback_id']

    if callback_id == "deploy_action":
        action = action_data['actions'][0]
        if action['value'] == 'done':
            return jsonify({
                "response_type": "in_channel",
                "text": f"<@{user_id}> закончил deploy!"
            })

    return jsonify({"error": "Unknown action"}), 400

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(debug=True)
