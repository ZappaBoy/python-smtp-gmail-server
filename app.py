from flask import Flask, request

from services.smtp_mail_sender import EmailService

app = Flask(__name__)
sender = EmailService()


@app.route("/", methods=["GET", "GET"])
def healthcheck():
    return "Alive"


@app.route("/send_mail", methods=["POST"])
def send_mail():
    request_data = request.get_json()

    receiver = request_data['receiver']
    subject = request_data['subject']
    message = request_data['message']

    status = sender.send_mail(receiver, subject, message)
    return {'status': status}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
