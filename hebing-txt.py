#合并一个文件夹下的多个txt文件
#coding=utf-8
import os
#获取目标文件夹的路径
filedir = 'E:\\temp\\count'
#获取当前文件夹中的文件名称列表
filenames=os.listdir(filedir)
#打开当前目录下的hebing.txt文件，如果没有则创建
f=open('E:\\temp\\count\\hebing.txt','w')
i=0
#先遍历文件名
for filename in filenames:
    i+=1
    print(i)
    if i>0:
        filepath = filedir+'\\'+filename
        print(filepath)
        #遍历单个文件，读取行数
        f.writelines(filename.replace('.txt',''))
        #print(filename.strip('/n').replace('.txt',''))
        f.write('\n')
        for line in open(filepath,encoding='gbk', errors='ignore'):
            print(str(line))
            f.writelines(line)
            #f.write('\n')
#关闭文件
f.close()
