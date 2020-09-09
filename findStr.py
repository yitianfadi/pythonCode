#python 查找文件指定内容并输出
import urllib 
fi = open("1110.sql","r",encoding="utf-8") #读取的文件名称 自定义文件编码
fo = open("0909sti0906.txt","w",encoding="gbk") #输出的文件名称

newline = []                #创建一个新的列表

#fi = fi.read()
for line in fi :            #按行读入文件，此时line的type是str
    if "2020-09-06" in line:     #检验是否到了要写入的内容
        #继续查找里面的内容如果没有可以不写
        #line = line[line.rfind('/swyy/appService/userLogin.html?'):] 
        line = urllib.parse.unquote(line)
        newline.append(line)
        print(line)
newlines = list(set(newline))
strlist = "".join(newline)      #合并列表元素
newlines = str(strlist)         #list转化成str
fo.write(newlines)

fo.close()
fi.close()
