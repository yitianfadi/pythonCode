#测试服务器是否正常
import requests
import os
import urllib3
import shutil
import configparser
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def  isConnected():
  try:
   html = requests.get("https://www.baidu.com",timeout=3)
   return True
  except:
   return False
  

def down(filename,Download_addres): #下载地址 #把下载地址发送给requests模块
    try:
        f=requests.get(Download_addres,verify=False,timeout=10) #下载文件
        with open(filename,"wb") as code:
            code.write(f.content)
    except:
        #print(filename,Download_addres,"无法访问")
        pass

         
def down_main(workname,downurl): 
        workname = workname.replace('\n', '').replace('\r', '').replace('\t', '').replace(" ", "")        
        downurl = downurl.replace('\n', '').replace('\r', '').replace('\t', '').replace(" ", "") 
        filename = os.path.basename(downurl)
        down(filename,downurl)
        if os.path.exists(filename):
            try:
                os.remove(filename) # 删除文件
                print(workname,downurl,"访问成功！")
                return 1
                
            except:
                print("删除文件失败")
                return 2
        else:
            print(workname,downurl,"访问失败！")
            return workname+downurl
            
def send_email(mail_host,mail_user,mail_pass,to,sender,text):
# 第三方 SMTP 服务
    # mail_host="smtp.XXX.com"  #设置服务器
    # mail_host="XXXX"    #用户名
    # mail_pass="XXXXXX"   #口令 
 
    #sender = 'from@runoob.com'
     # to 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    tosend =[to]
    message = MIMEText(text, 'plain', 'utf-8')
   # message['From'] = Header("菜鸟教程", 'utf-8')
   # message['To'] =  Header("测试", 'utf-8')
 
    subject = text
    message['Subject'] = Header(subject, 'utf-8')
 
    try:
        smtpObj = smtplib.SMTP(mail_host) 
        #smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, tosend, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
   
def conn_ini(fileini): #读取配置文件函数
    try:
        cf = configparser.ConfigParser()
        cf.read(fileini, encoding='utf8')  #注意setting.ini配置文件的路径
    except :
        pass
    return cf
    
def get_section(fileini): # 获取文件中所有的section
    
    cf = conn_ini(fileini)
    secs = cf.sections() 
    return secs

def get_option(fileini,key): # 获取某个section名为Mysql-Database所对应的键
    
    cf = conn_ini(fileini)
    options = cf.options(key) 
    return options

def get_item(fileini,key): # 获取某个section名为Mysql-Database所对应的键
    
    cf = conn_ini(fileini)
    items = cf.items(key) 
    return items

def get_config(fileini,item, key): # 获取[Mysql-Database]中host对应的值
    cf = conn_ini(fileini)
    value = cf.get(item, key)

    return value


if __name__ == '__main__':
    fileini = 'config.ini'
    sections = get_section(fileini)
    items = get_item(fileini,sections[0])
    mail_host = get_config(fileini,sections[1],'host')
    mail_user = get_config(fileini,sections[1],'user')
    mail_pass= get_config(fileini,sections[1],'pwd')
    to = get_config(fileini,sections[1],'to')
    sender = get_config(fileini,sections[1],'sender')
    times = get_config(fileini,sections[2],get_option(fileini,sections[2])[0])
    times = int(times)
    while True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if(isConnected()):

            for k,v in items:
                i = down_main(k,v)
                if(i==1):
                    pass
                elif(i==2):
                    pass
                else:
                    #print(i)
                    send_email(mail_host,mail_user,mail_pass,to,sender,i)
            print("***"*10)
        else:
            print("本地网络不通！")
        print("休眠",times,"秒")
        time.sleep(times)
