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
        "text": "\n    - - - - Қазақстан - - - -\n\n    🤙 За текущий месяц:\n\n\n    🤙 За прошлый месяц:\n1.       Sulpak:  490 17.23%\n2.          KFC:  360 12.66%\n3. Заммлер Казахстан:  264 9.28%\n4.        Small:  221 7.77%\n5.      My Mart:  213 7.49%\n6. Леруа Мерлен:  161 5.66%\n7. I'm (Food Solutions KZ):  156 5.49%\n8.  Спортмастер:  131 4.61%\n9.  Zeta Almaty:  127 4.47%\n10. Золотое Яблоко:  125 4.4%\n11.    AVATARIYA:  82 2.88%\n12.  Airba Fresh:  67 2.36%\n13.         Zara:  48 1.69%\n14.       Adidas:  47 1.65%\n15.        Рядом:  45 1.58%\n16.        Arbuz:  33 1.16%\n17.   LC Waikiki:  33 1.16%\n18.          FLO:  30 1.05%\n19.         Zeta:  25 0.88%\n20.        Ostin:  23 0.81%\n21. Arbuz Астана:  19 0.67%\n22.     Benetton:  18 0.63%\n23.    KARI Kids:  14 0.49%\n24.  WomenSecret:  11 0.39%\n25.    Magnum GO:  11 0.39%\n26.        METRO:  10 0.35%\n27. Hampton by Hilton Astana Triumphal Arch:  9 0.32%\n28.      Арсенал:  9 0.32%\n29. Гипермаркет Комфорт:  9 0.32%\n30.         KARI:  8 0.28%\n31.      Qaganat:  7 0.25%\n32.  DNS Shop KZ:  6 0.21%\n33.      Котофей:  6 0.21%\n34.       Whoosh:  5 0.18%\n35.    Zara Home:  5 0.18%\n36. ALS Казгеохимия:  4 0.14%\n37. Rixos Hotel Astana:  4 0.14%\n38. Рядом Астана:  3 0.11%\n39.   Copa store:  2 0.07%\n40.     Вкусмарт:  2 0.07%\n41.      Hardees:  1 0.04%\n\n    - - - - Кыргызстан - - - -\n\n    🤙 За текущий месяц:\n\n\n    🤙 За прошлый месяц:\n1. Супермаркет Азия Ритейл:  83 33.6%\n2.   Умай Групп:  77 31.17%\n3.       Globus:  54 21.86%\n4. Супермаркет Азбука:  19 7.69%\n5. LC Waikiki KG:  14 5.67%\n\n    - - - - O'zbekiston - - - -\n\n    🤙 За текущий месяц:\n\n\n    🤙 За прошлый месяц:\n1.     Safia UZ:  88 62.41%\n2. Korzinka GO UZ:  48 34.04%\n3.   M Cosmetic:  4 2.84%\n4.       JET UZ:  1 0.71%\n"
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
