import json
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from services.logger import LoggerService

logging_service = LoggerService(name=__name__)
logger = logging_service.get_logger()


class EmailService:
    """
    Provide methods for send email to users
    """

    def __init__(self):
        self.local_domain = "localhost"
        self.local_port = "5000"
        dirname = os.path.dirname(__file__)
        credentials_file_path = os.path.join(dirname, '../credentials.json')
        with open(credentials_file_path) as json_file:
            file = json.load(json_file)
            self.credential = file["email"]
            self.context = ssl.create_default_context()
            self.smtp_server = smtplib.SMTP(host=self.credential["host"], port=self.credential["port"])

    def send_mail(self, receiver, subject, message):
        """
        Send email to an user with a subject and a message

        :param receiver: The receiver
        :param subject: The subject
        :param message: The message
        :return: Boolean | SMTPException
        """

        try:
            self.smtp_server.connect(host=self.credential["host"], port=self.credential["port"])
            self.smtp_server.ehlo()
            self.smtp_server.starttls(context=self.context)
            self.smtp_server.ehlo()
            self.smtp_server.login(self.credential["address"], self.credential["password"])

            msg = MIMEMultipart()

            msg["From"] = self.credential["address"]
            msg["To"] = receiver
            msg["Subject"] = subject

            msg.attach(MIMEText(message, 'plain'))

            self.smtp_server.send_message(msg)
            del msg

        except smtplib.SMTPException as e:
            logger.exception("email_service -> send_message")
            return False

        finally:
            self.smtp_server.quit()
            return True
