#*- coding:utf-8 -*
import smtplib  
import email.mime.multipart  
import email.mime.text  
import urllib.request
import urllib.parse
import urllib.error
import time
from bs4 import BeautifulSoup

class Page(object):
    def __init__(self,link):
        self.pg = urllib.request.urlopen(link).read().decode('utf-8')
        self.cont = BeautifulSoup(self.pg,'html5lib')
    def get_latestitem(self):
        item = self.cont.find(name='div',attrs={'class':"event-info"})
        latestnews = item.p.string
        return latestnews
    def get_newsdate(self):
        t = self.cont.find(name='div',attrs={'class':'calendar-div pull-left'})
        newsdate = t.h5.string + '/' + t.h4.string
        return newsdate
    def get_newslink(self):
        htmlname = urllib.parse.quote(self.cont.find(name='div',attrs={'class':"event-info"}).a['href'])
        link = 'http://www.ss.pku.edu.cn' + htmlname
        return link
    def get_newscontent(self):
        info = self.cont.find(name='div', attrs={'class': 'article-content'})
        return info

def send_the_msg(title,content):
    try:
        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = 'flycrane01@163.com'
        msg['to'] = 'flycrane01@qq.com'
        msg['subject'] = title
        txt = email.mime.text.MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)
        smtp = smtplib.SMTP_SSL()
        smtp.connect('smtp.163.com', '994')
        smtp.login('flycrane01@163.com', 'mypassword')
        smtp.sendmail('flycrane01@163.com', to_addrs='flycrane01@qq.com', msg=msg.as_string())
        smtp.quit()
    except:
        print(now() + ' Message deliverary failed.')

def now():
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t

homepage = 'http://www.ss.pku.edu.cn/'
savednews = ''
success = 0
failure = 0
while True:
    time.sleep(0.1)
    if time.strftime("%S", time.localtime()) == '00':
        try:
            noticePage = Page(homepage)
            latestnews = noticePage.get_latestitem()
            if latestnews != savednews:
                savednews = latestnews
                newslink = noticePage.get_newslink()
                title = noticePage.get_newsdate() + latestnews
                content = Page(newslink).get_newscontent()
                print(now() + ' Sending the news...' + title)
                send_the_msg(title,content)
                success += 1
                print('Successfully run %s times.' % success)
            print(now() + ' On hold...')
            time.sleep(55)
        except TimeoutError as err:
            print(now() + ' Failed!' + err)
            failure += 1
            if failure > 100:
                break
send_the_msg(title='Program Stopped',content='Program stopped at ' + now())
