#!/usr/bin/env python

import socket
from sysadmin.myshell import run, remote_run


#
# FIXME !!
# remove all hardcode variables (hostnames, email addresses, ...)
# and make them input parameters
#


def sendemail_from_file(f, subject, adddress):
    """
    :param f: filename with email body
    :param subject: email subject
    :param address: destination
    """
    if socket.gethostname().startswith('lcgui'):
        cmd = "cat /tmp/email_body | mail -s \"%s\" -r \"jose.caballero@stfc.ac.uk\" %s" %(subject, adddress)
        run(cmd)
        cmd = "rm -f /tmp/email_body"
        run(cmd)
    else:
        cmd = 'scp %s josecaballero@lcgui06.gridpp.rl.ac.uk:/tmp/email_body' %f
        run(cmd)
        cmd = "cat /tmp/email_body | mail -s \"%s\" -r \"jose.caballero@stfc.ac.uk\" %s" %(subject, adddress)
        remote_run(cmd, 'lcgui06.gridpp.rl.ac.uk', 'josecaballero')
        cmd = "rm -f /tmp/email_body"
        remote_run(cmd, 'lcgui06.gridpp.rl.ac.uk', 'josecaballero')

def send_email(subject, body):
    sender = f'root@{socket.gethostname()}'
    to = 'ESCPSCSGridServicesteam@stfc.ac.uk'
    message = MIMEText(body)
    message['subject'] = subject
    message['From'] = sender
    message['To'] = to
    to = [to]
    server = smtplib.SMTP("localhost")
    server.sendmail(sender, to, message.as_string())
    server.close()
