from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header
import os
import smtplib
from email.mime.base import MIMEBase
from email import encoders


class SendEmail:
    def __init__(self,
                 user,
                 pwd,
                 client):
        self.user = user
        self.pwd = pwd
        self.client = client

    def attach_image(self, msg, path, id):
        with open(path, 'rb') as file:
            msg_image = MIMEImage(file.read(), name = path)
            msg_image.add_header('Content-ID', '<{}>'.format(id))
        msg.attach(msg_image)
        # return msg_image

    def attach_file(self, filename):
        part = MIMEBase('application', 'octect-stream')
        part.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(filename))
        return part

    def generate_email(self, html_txt, subject, to_list, data_paths):

        self.to_list = to_list
        self.subject = subject
        self.html_txt = html_txt
        # self.html_txt_ai = html_txt_ai
        self.data_paths = data_paths
        # self.images = images

        msg =MIMEMultipart('related')
        msg['Subject'] = Header(self.subject, 'utf-8')
        msg['From'] = self.user
        msg['To'] = ','.join(self.to_list)
        msg_alternative = MIMEMultipart('alternative')
        # msg_text = MIMEText(u'Image not working - maybe next time', 'plain', 'utf-8')
        msg_text = MIMEText(self.html_txt, 'html')
                    
        msg_alternative.attach(msg_text)
        msg.attach(msg_alternative)
        msg_html = u'<h1>Some images coming up</h1>'
        
        if self.data_paths != []:
            for dp in self.data_paths:
                msg.attach(self.attach_file(dp))
        return msg

    def send_email(self, msg):
        mailServer = smtplib.SMTP(self.client, 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.user, self.pwd)
        mailServer.sendmail(self.user, self.to_list, msg.as_string())
        mailServer.quit()