import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"
recipients = ['vasya@email.com', 'petya@email.com']


class MyMail:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.subject = 'Subject'
        self.recipients = []
        self.message_text = 'Message'
        self.header = None

    def send_message(self, message, recipients_list):
        self.message_text = message
        self.recipients = recipients_list
        message_body = MIMEMultipart()
        message_body['From'] = self.login
        message_body['To'] = ', '.join(self.recipients)
        message_body['Subject'] = self.subject
        message_body.attach(MIMEText(self.message_text))

        sender = smtplib.SMTP(GMAIL_SMTP, 587)
        # identify ourselves to smtp gmail client
        sender.ehlo()
        # secure our email with tls encryption
        sender.starttls()
        # re-identify ourselves as an encrypted connection
        sender.ehlo()

        sender.login(self.login, self.password)
        sender.sendmail(self.login, sender, message_body.as_string())
        sender.quit()

    def receive(self, header):
        self.header = header
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
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
    my_mail = MyMail('login@gmail.com', 'qwerty')
    my_mail.send_message('Privet', recipients)
    my_message = my_mail.receive('Job')
