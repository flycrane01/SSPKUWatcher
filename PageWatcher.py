#*- coding:utf-8 -*
import smtplib  
import email.mime.multipart  
import email.mime.text  
import urllib.request
import urllib.parse
import urllib.error
import time
from bs4 import BeautifulSoup


"""
Written by flycrane01
Finished on Dec.2, 2017

TODO: Add logging module.
"""


class Page(object):                                                                  # 所有页面的父类对象
    def __init__(self,link):                                                         # 实例化类时需要提供一个链接，链接会被打开并解析
        self.link = link
        self.pg = urllib.request.urlopen(link).read().decode('utf-8')
        self.cont = BeautifulSoup(self.pg,'html5lib')


class SSPKUPage(Page):                                                                # 子类。软微官网
    def get_latestitem(self):                                                         # 获取当前页面最新通知的标题
        item = self.cont.find(name='div',attrs={'class':"event-info"})
        latestnews = item.p.string
        return latestnews

    def get_newsdate(self):                                                           # 获取当前页面最新通知的时间
        t = self.cont.find(name='div',attrs={'class':'calendar-div pull-left'})
        newsdate = t.h5.string + '/' + t.h4.string
        return newsdate

    def get_newslink(self):                                                            # 获取当前页面最新通知的链接
        htmlname = urllib.parse.quote(self.cont.find(name='div',attrs={'class':"event-info"}).a['href'])        # urllib库无法打开含中文字符的链接，需先进行转义
        link = 'http://www.ss.pku.edu.cn' + htmlname
        return link

    def get_newscontent(self):                                                          # 打开最新通知并获取正文内容
        pg = urllib.request.urlopen(self.get_newslink()).read().decode('utf-8')
        cont = BeautifulSoup(pg, 'html5lib')
        info = cont.find(name='div', attrs={'class': 'article-content'})
        return info


def now():                                                                                   # 格式化输出当前系统时间
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t


def send_the_msg(title,content,user):                                                        # 利用smtplib库使用smtp协议发送邮件
    try:
        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = 'flycrane01@qq.com'
        msg['subject'] = title
        txt = email.mime.text.MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)
        smtp = smtplib.SMTP_SSL()
        smtp.connect('smtp.qq.com', '465')
        smtp.login('flycrane01@qq.com', 'mypassword')                                     # 密码已做加密处理 :)
        smtp.sendmail('flycrane01@qq.com', to_addrs=user, msg=msg.as_string())
        smtp.quit()
    except:
        print(now() + ' Message delivery failed.')


def newsupdate(randompage,user):                                                               # 查询对应页面有无更新，若有更新则发送邮件提醒
    latestnews = randompage.get_latestitem()
    if latestnews != savednews[randompage.link]:
        savednews[randompage.link] = latestnews
        sentnews.append(latestnews)
        title = randompage.get_newsdate() + latestnews
        content = randompage.get_newscontent()
        print(now() + ' Sending the news...' + title)
        send_the_msg(title, content, user)


if __name__ == '__main__':
    homepage = 'http://www.ss.pku.edu.cn/'
    savednews = {homepage:'关于2018届本科毕业生图像采集的补拍通知'}
    success = 0
    failure = 0
    while True:
        time.sleep(0.1)                                                                         # 控制while循环的判断频率，避免占用CPU过多
        if int(time.strftime("%H", time.localtime())) > 20:                                    # 一般20点之后不会再有通知，程序进入休眠状态
            print(now() + 'Sleeping...')
            time.sleep(32400)
        if time.strftime("%S", time.localtime()) == '00':                                      # 每分钟整时，开始实例化各页面对象并检查更新
            try:
                SSPKU = SSPKUPage(homepage)
                newsupdate(SSPKU,['flycrane01@qq.com'])
                success += 1
                print('Successfully run %s times.' % success)
                print(now() + ' On hold...')
                time.sleep(50)                                                                  # 每轮验证的时间在5秒钟左右。检验完毕自动休眠50秒，最大限度降低无用功耗。
            except (TimeoutError,ConnectionResetError,AttributeError,urllib.error.URLError) as err:         # 捕获打开网页时可能出现的异常
                print(now() + ' Failed!')
                print(err)
                failure += 1
                if failure > 43200:                                                             # 若累计12个小时无法正常运行，程序中断并最后发送邮件提醒
                    break
    send_the_msg(title='Program Stopped',content='Program stopped at ' + now(),user=['flycrane01@qq.com'])
