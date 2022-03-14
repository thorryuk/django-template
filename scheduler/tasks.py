import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate
from datetime import datetime
import datetime as dt

from celery import shared_task
from django.conf import settings
from dateutil.relativedelta import *
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template

from app.common_functions import aes_encrypt


@shared_task(bind=True)
def send_mail_task(self, data):

    if 'to' in data:

        if 'subject' in data:
            subject = data['subject']
        else:
            subject = ''

        if 'text' in data:
            text = data['text']
        else:
            text = ''

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = data['from']
        msg['To'] = ",".join(map(str, data['to']))

        text = "From: %s\r\n" % data['from'] \
               + "Date: %s\r\n" % formatdate(localtime=True) \
               + "To: %s\r\n" % ",".join(map(str, data['to'])) \
               + "Subject: %s\r\n" % subject \
               + "\r\n" + text

        html = "<html><head></head><body>Putra Perkasa Abadi</body></html>"

        attach1 = MIMEText(text, 'plain')

        if 'html' in data:
            html = data['html']

        attach2 = MIMEText(html, 'html')

        msg.attach(attach1)
        msg.attach(attach2)

        try:
            
            send_mail(subject, text, settings.EMAIL_HOST_USER, data['to'], html_message=data['html'])
            return 'Sending mail to' + str(data['to']) + ' succeeded'
        except smtplib.SMTPHeloError:
            return 'The server didn\'t reply properly'
        except smtplib.SMTPRecipientsRefused:
            return 'The server rejected ALL recipients (no mail was sent)'
        except smtplib.SMTPSenderRefused:
            return 'Server didn\'t accept from ' + str(data['from'])
        except smtplib.SMTPDataError:
            return 'The server replied with an unexpected error code (other than a refusal of a recipient)'
        except Exception as e:
            return str(e)
    else:
        return 'send mail failed'


@shared_task(bind=True)
def send_mail_task_attach(self, data):

    if 'to' in data:

        if 'subject' in data:
            subject = data['subject']
        else:
            subject = ''

        if 'text' in data:
            text = data['text']
        else:
            text = ''

        text = "From: %s\r\n" % data['from'] \
               + "Date: %s\r\n" % formatdate(localtime=True) \
               + "To: %s\r\n" % ",".join(map(str, data['to'])) \
               + "Subject: %s\r\n" % subject \
               + "\r\n" + text

        html = "<html><head></head><body>Putra Perkasa Abadi</body></html>"

        if 'html' in data:
            html = data['html']

        msg = EmailMultiAlternatives(subject, text, settings.EMAIL_HOST_USER, data['to'])
        msg.attach_alternative(html, "text/html")

        if 'attachment' in data:
            pdf = MIMEApplication(open(str(data['path'])+str(data['attachment']), 'rb').read())
            pdf.add_header('Content-Disposition', 'attachment', filename= str(data['attachment']))
            msg.attach(pdf)

        try:
            
            msg.send()
            return 'Sending mail to' + str(data['to']) + ' succeeded'
        except smtplib.SMTPHeloError:
            return 'The server didn\'t reply properly'
        except smtplib.SMTPRecipientsRefused:
            return 'The server rejected ALL recipients (no mail was sent)'
        except smtplib.SMTPSenderRefused:
            return 'Server didn\'t accept from ' + str(data['from'])
        except smtplib.SMTPDataError:
            return 'The server replied with an unexpected error code (other than a refusal of a recipient)'
        except Exception as e:
            return str(e)
    else:
        return 'send mail failed'
