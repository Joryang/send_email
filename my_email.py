#!/usr/bin/env python
# -*- coding:utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr,formataddr
import smtplib, os, mimetypes

class my_email():

    def __init__(self, use_ssl=True, debug=False):
        self.from_addr = raw_input('From: ')
        self.sender_name = raw_input('Sender name: ')
        self.to_addr = raw_input('To: ')
        self.receiver_name = raw_input('Receiver name: ')
        self.smtp_server = raw_input('SMTP server: ')
        self.server_port = int(raw_input('Server port: '))
        self.password = raw_input('Password: ')

        self.use_ssl = use_ssl
        self.debug = debug
    
    def _server_login(self):
        if self.use_ssl:
            self.server = smtplib.SMTP_SSL(self.smtp_server, self.server_port)
        else:
            self.server = smtplib.SMTP(self.smtp_server, self.server_port)

        if self.debug:
            self.server.set_debuglevel(1)

        self.server.login(self.from_addr, self.password)

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))
        
    def send_simple_email(self, subject=u'hello', text='hello...'):
        
        
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = self._format_addr(u'%s <%s>' % (self.sender_name,self.from_addr))
        msg['To'] = self._format_addr(u'%s <%s>' % (self.receiver_name, self.to_addr))
        msg['Subject'] = Header(subject, 'utf-8').encode()
        
        self._server_login()
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        self.server.quit()

    def send_email_with_attachment(self, subject=u'hello', text='hello...'):
        path = raw_input('File path: ')
        
        
        msg = MIMEMultipart()
        
        msg['From'] = self._format_addr(u'%s <%s>' % (self.sender_name,self.from_addr))
        msg['To'] = self._format_addr(u'%s <%s>' % (self.receiver_name, self.to_addr))
        msg['Subject'] = Header(subject, 'utf-8').encode()

        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        ctype,encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype,subtype = ctype.split('/',1)
        
        fullname = os.path.basename(path)
        
        # 添加附件就是加上一个MIMEBase，从本地读取一个文件:
        with open(path, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase(maintype, subtype, filename=fullname)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=fullname)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
            
        self._server_login()
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        self.server.quit()

    def send_email_with_image(self, subject=u'hello', text='hello...'):
        from_addr =  self.from_addr
        sender_name = self.sender_name
        password = self.password
        to_addr =  self.to_addr
        receiver_name = self.receiver_name
        smtp_server = self.smtp_server

        msg = MIMEMultipart()
        msg['From'] = self._format_addr(u'%s <%s>' % (sender_name, from_addr))
        msg['To'] = self._format_addr(u'%s <%s>' % (receiver_name,to_addr))
        msg['Subject'] = Header(u'Image mail...', 'utf-8').encode()

        path = raw_input('Image path: ')
        fullname = os.path.basename(path)
        filename, filetype = fullname.split('.')     

        # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
        with open(path, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('image', filetype, filename=fullname)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=fullname)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
        
        msg.attach(MIMEText('<html><body><h1>Hello</h1>'+
            '<p><img src="cid:0"></p>'+
            '</body></html>', 'html', 'utf-8'))

        self._server_login()
        self.server.sendmail(from_addr, [to_addr], msg.as_string())
        self.server.quit()


if __name__ == '__main__':
    mail1 = my_email()
    mail1.send_simple_email(subject=u'no1', text='no1 mail')
    #mail1.send_email_with_attachment(subject=u'attachment', text='hello...attachment')
    #mail1.send_email_with_image(subject=u'hello', text='hello...')
    
