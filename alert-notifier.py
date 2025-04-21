from http.client import HTTPException
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/sendtel', methods=['POST'])
def sendtel():
    try:
        TOKEN = os.environ.get("TELEGRAM_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHATID")
        req_data = request.get_json()

        print("Received Telegram alert:", req_data)

        state = req_data.get('state')
        messages = req_data.get('message')
        title = req_data.get('title')

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"title: {title}\nstate: {state}\nmessage: {messages}"
        }

        print("Sending Telegram message...")
        response = requests.post(url, json=payload)
        print(response.json())

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)})
    except HTTPException as e:
        return jsonify({"http_error": str(e)})

@app.route('/sendmsg', methods=['POST'])
def sendmsg():
    try:
        req_data = request.get_json()

        state = req_data.get('state', 'unknown').upper()
        title = req_data.get('title', 'No Title')
        body = req_data.get('message', '')

        message = f"[{state}] {title}: {body}"

        receptors = req_data.get('receptors')
        if not receptors:
            receptors = os.environ.get("RECEPTORS", "").split(',')

        if isinstance(receptors, str):
            receptors = [receptors]

        api_key = os.environ.get("KAVE_TOKEN")
        sender = os.environ.get("KAVE_SENDER")

        url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"
        payload = {
            'receptor': ','.join(receptors),
            'sender': sender,
            'message': message
        }

        print("Sending Kavenegar SMS:", payload)
        response = requests.post(url, data=payload)
        print("Response:", response.json())

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
