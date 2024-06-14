# coding: utf-8

# Import libraries
import re
import smtplib
import socket
import json
from email.message import EmailMessage
from email.headerregistry import Address
from colorama import Fore, Style

class Mail():
    #-------------------------------------------------------------------------------------------------------------------
    #
    #   Send email
    #
    #-------------------------------------------------------------------------------------------------------------------
    def send(self, subject: str, body: str, recipient: list, logfile = None):
        msg = EmailMessage()

        # If logfile is set, then clean it from ANSI escape codes
        # sed 's,\x1B[[(][0-9;]*[a-zA-Z],,g' "$LOG" > "$LOG_REPORT_MAIL"
        if logfile:
            # Read logfile content
            with open(logfile, 'r') as f:
                content = f.read()

            # Get logfile real filename
            attachment = logfile.split('/')[-1]

            # Replace ANSI escape codes
            # content = re.sub(r'\x1B[[(][0-9;]*[a-zA-Z]', '', content)


            # Create json attachment.
            attachment = json.dumps({'This': 'is json'})

            # Encode to bytes
            bs = attachment.encode('utf-8')

            msg.add_attachment(bs, maintype='application', subtype='json', filename='test.json')



            # msg.add_attachment(content, maintype='text', subtype='plain', filename=attachment)
            # msg.add_attachment('test'.encode('utf-8'),  maintype='text', subtype='plain', filename=attachment)

        # Define email content and headers
        msg.set_content(body)
        msg['Subject'] = subject
        # msg['From'] = Address('Linupdate', 'noreply', socket.gethostname())
        msg['From'] = Address('Linupdate', 'noreply', 'example.com')
        msg['To'] = ','.join(recipient)

        # Send the message via our own SMTP server
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

