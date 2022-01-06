import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ClientGMail:

    def __init__(self, login, password):
        self.GMAIL_SMTP = "smtp.gmail.com"
        self.GMAIL_IMAP = "imap.gmail.com"
        self.login = login
        self.password = password
        self.header = None

    def send(self, subject, message, recipients):
        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.GMAIL_SMTP, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()

        ms.login(self.login, self.password)
        ms.sendmail(self.login,
                    recipients, msg.as_string())

        ms.quit()

    def receive(self):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")

        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)

        mail.logout()

        return email_message


if __name__ == '__main__':
    mail_client = ClientGMail('login@gmail.com', 'qwerty')

    mail_client.send('Subject',
                     'Message',
                     ['vasya@email.com', 'petya@email.com'])

    mail_client.receive()
