import json
import os

from flask import Flask, request

from services.smtp_mail_sender import EmailService

app = Flask(__name__)
sender = EmailService()

dirname = os.path.dirname(__file__)
credentials_file_path = os.path.join(dirname, './credentials.json')
with open(credentials_file_path) as json_file:
    file = json.load(json_file)
    credential = file["server"]
    api_key = credential["api_key"]


@app.route("/", methods=["GET", "GET"])
def healthcheck():
    return "Alive"


@app.route("/send_mail", methods=["POST"])
def send_mail():
    request_data = request.get_json()

    status = False
    if api_key == request_data['apiKey']:
        receiver = request_data['receiver']
        subject = request_data['subject']
        message = request_data['message']

        status = sender.send_mail(receiver, subject, message)
    return {'status': status}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
