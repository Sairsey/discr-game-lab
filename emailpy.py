#===============================================================================
#
# MIT License
#
# Emailpy
# Copyright (c) [2019] [Sebastiano Campisi - ianovir]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#===============================================================================

import os
import sys
import datetime
import time
import socket
import ntpath
import smtplib
import imaplib
import email
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from xml.dom import minidom
from email import encoders

version = "0.0"
version_info = (0,0)

class Constants:
    '''
    Wraps search criterias' constants for IMAP protocol
    '''
    ALL="ALL"
    ANSWERED="ANSWERED"
    DELETED="DELETED"
    FLAGGED="FLAGGED"
    NEW="NEW"
    OLD="OLD"
    RECENT="RECENT"
    SEEN="SEEN"
    UNANSWERED="UNANSWERED"
    UNDELETED="UNDELETED"
    UNFLAGGED="UNFLAGGED"
    UNKEYWORD="UNKEYWORD"
    UNSEEN="UNSEEN"
    
    #require string arg:
    BCC="BBC"
    CC="CC"
    BODY="BODY"
    FROM="FROM"
    KEYWORD="KEYWORD"
    SUBJECT="SUBJECT"
    TEXT="TEXT"
    TO="TO" 
    
    #require date arg:
    ON="ON"
    SINCE="SINCE"
    BEFORE="BEFORE"

class ServiceManager:
    '''
    Loads and provides email services, as declared in ./services.xml
    '''
    __services = dict()
    __path =  os.path.dirname(__file__) + "/services.xml"

    def __init__(self, customServices = None):
        try:
            if customServices != None:
                self.__path = customServices
            
            xmldoc = minidom.parse(self.__path)
            itemList = xmldoc.getElementsByTagName('service')
            for s in itemList:
                id = s.attributes['id'].value
                smtp_address = s.attributes['smtp_address'].value
                smtp_port = int(s.attributes['smtp_port'].value)
                imap_address = s.attributes['imap_address'].value
                imap_port = int(s.attributes['imap_port'].value)       
                nservice = MailService(id, smtp_address, smtp_port, imap_address, imap_port)
                self.__services[id] = nservice   
        except Exception as e:
            print(("Error while loading %s: %s"  % (self.__path ,repr(e))))
            
    def get_service(self, id):
        if id in self.__services:
            return self.__services[id]
        else:
            print(("Error: service '%s' not declared in %s" % (id, self.__path )))
            return None
    
		
class EMessage:		
    '''
    Class wrapping major parts of a message
    '''    
    Body= None
    Attachments = None
    def __init__(self, fromAddr, toaddrs, subject, date):
        self.From = str(fromAddr)
        self.Subject = str(subject)
        self.Date = date
        self.To = toaddrs

class MailService:
    '''
    Class providing connection to email service, messages sending 
    and reading
    '''
    id = ""
    smtp_addr = None
    smtp_port = 0
    imap_addr = None
    imap_port = 0

    def __init__(self, id, smtp_addr, smtp_port, imap_addr, imap_port):
        self.id = id
        self.smtp_addr = smtp_addr
        self.smtp_port = smtp_port
        self.imap_addr = imap_addr
        self.imap_port = imap_port

    def setup(self, user, pwd):
        self.__user = user
        self.__pwd = pwd
     
    @staticmethod 
    def path_leaf(path):
        h, t = ntpath.split(path)
        return t or ntpath.basename(h)

    def send(self, toaddrs, subject, body="", attachments = None): 
        try:
            msg = MIMEMultipart()
            msg['Subject']= subject
            msg['From']= self.__user
            msg['To']=  ', '.join(toaddrs)

            body = MIMEText(body)
            msg.attach(body)
            
            if attachments != None:
                for a in attachments:        
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(a, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", ('attachment; filename="%s"' % MailService.path_leaf(a)))
                    msg.attach(part)
                    
            server = smtplib.SMTP(self.smtp_addr, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.login(self.__user, self.__pwd)
            server.sendmail(self.__user, toaddrs, msg.as_string())
            server.quit()
            return True
                    
        except Exception as e:
            print(("Error while sending message: %s"  % repr(e)))
            return False 
    

    def read(self, criteria = "ALL", download_attachments = False):    
        try:
            m = imaplib.IMAP4_SSL(self.imap_addr, self.imap_port)
            m.login(self.__user,self.__pwd)
            m.select()
            
            retval = []

            result, data = m.uid('search', None, criteria)
            if result == 'OK':
                for num in data[0].split():   
                    result, data = m.uid('fetch', num, '(RFC822)')
                    if result == 'OK':
                        if sys.version_info[0] < 3:
                            e_msg = email.message_from_string(data[0][1]) 
                        else:
                            e_msg = email.message_from_bytes(data[0][1])   
                        
                        # Date:
                        _date = None
                        date_t = email.utils.parsedate_tz(e_msg['Date'])
                        if date_t:
                            _date = datetime.datetime.fromtimestamp(
                            email.utils.mktime_tz(date_t))

                        newEmsg = EMessage(e_msg['From'], e_msg['To'], e_msg['Subject'], _date )
                        newEmsg.Body = []

                        #content:
                        if e_msg.is_multipart():                            
                            for payload in e_msg.get_payload():                            
                                newEmsg.Body.append(payload.get_payload())
                        else:
                            newEmsg.Body.append(e_msg.get_payload())

                        #attachments:
                        newEmsg.Attachments = []
                        for part in e_msg.walk():
                            #ignoring parts multi-part without attachments
                            if part.get_content_maintype() == 'multipart':
                                continue
                            if part.get('Content-Disposition') is None:
                                continue

                            fileName = part.get_filename()

                            if fileName!=None:

                                if download_attachments:                              
                                    if platform.system()=="Windows":
                                        os.system("if not exist attachments mkdir attachments")
                                    else:
                                        os.system("mkdir -p ./attachments/")
                                    filePath = os.path.join('./attachments/', fileName)
                                    if not os.path.isfile(filePath) :
                                        fp = open(filePath, 'wb')
                                        fp.write(part.get_payload(decode=True))
                                        fp.close()
                                        print("Downloaded attachment: " + filePath)
                                    else:
                                        index = 0
                                        fpath, ext = os.path.splitext(filePath)
                                        fname, ext = os.path.splitext(fileName)
                                        while os.path.isfile(fpath + str(index) + ext):
                                            index += 1
                                        filePath = fpath + str(index) + ext
                                        fileName = fname + str(index) + ext

                                        fp = open(filePath, 'wb')
                                        fp.write(part.get_payload(decode=True))
                                        fp.close()
                                        print("Downloaded attachment: " + filePath)

                                newEmsg.Attachments.append(str(fileName))
                        retval.append(newEmsg)

            return retval
            m.close()
            m.logout()
        except Exception as e:
            print(("Error while reading message(s): %s"  % repr(e)))
            return []
