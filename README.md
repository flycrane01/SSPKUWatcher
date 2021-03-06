# PageWatcher使用说明 #

## 一、需求和功能
包括我在内的很多同学经常错过学校官网上的通知。因此，本人用Python编写了一个小程序运行在阿里云上，自动在每分钟整时打开相关网站查询最新的通知，如果有新的通知则马上把通知内容发送到我的邮箱。与此同时，微信上的QQ邮箱提醒会将此邮件推送给我。这样以来，可以保证自己不会错过任何通知。

## 二、程序分析
程序主要使用了urllib库、smtplib库、email库和BeautifulSoup库。发信模块较为简单，直接使用Python自带的smtplib库通过QQ邮箱代发邮件。下面主要介绍程序是如何实现对网页内容的定时更新的。
首先，程序定义了基类Page，并通过设置__init__方法使其必须有link参数才能实例化。创建Page对象的同时，这个网页的内容也已经打开并被BeautifulSoup解析保存在self.cont属性中，网页链接保存在self.link属性中供后期查询使用。
基类定义完成之后，针对不同学校的页面建立不同的子类。我在程序中创建了SSPKU和WHPage两个子类。每个子类均定义了四个方法，其具体实现均是借助于BeautifulSoup库：

* get_latestitem
获取当前页面最新通知的标题
*	get_newsdate
获取当前页面最新通知的时间
*	get_newslink
获取当前页面最新通知的链接
*	get_newscontent
打开最新通知并获取正文内容

随后，我定义了newsupdate函数，使用randompage和user两个参数。randompage是任何一个前面的子类实例化的对象，user是通知需要发送的目标。主要运行逻辑如下：

1.	利用randompage.get_latestitem()获取当前最新的通知标题
2.	通过randompage.link向字典查询该通知是不是此页面已保存的最新通知
3.	若不是，则更新字典中的最新通知。同时将randompage.get_newsdate()和randompage.get_latestitem()作为邮件的标题，将randompage.get_newscontent()作为邮件的正文发送到user中。

定义完类和函数后，只需初始化相关变量，用While True写一个死循环并设置好判断条件，在每分钟整时实例化各子类对象对调用newsupdate函数，即可实现实时接收学校通知的目的。
