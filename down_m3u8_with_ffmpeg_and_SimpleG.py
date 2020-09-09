# pyhon 根据指定内容分割文本 + m3u8下载器
# 下载需要的下载器 https://github.com/nilaoda/N_m3u8DL-CLI
# 下载器下载命令参数 https://nilaoda.github.io/N_m3u8DL-CLI/SimpleGUI.html
# downUrl.txt示例
# 小猪佩奇第一集 https://moviets.tc.qq.com/p0027jbwye1.321004.ts.m3u8?ver=4
# import win32api
# import win32event
# import win32process
import time
import os
import shutil
# pip3 install pypiwin32
def main():
    fi = open("W:/downUrl.txt","r",encoding="utf-8")  #读取txt内容
    i=1
    workPath = "W:/Bv/"          #保存位置
    findtxt = "http"            #指定分割内容
    for line in fi :            #按行读入文件，此时line的type是str
        #line = str(line)        #
        pos = line.find(findtxt)    # 获取到 findtxt 的角标
        lenline = len(line)         # 获取到 line 的长度
        workdir = line[0:pos].replace('\n', '').replace('\r', '').replace('\t', '').replace(" ", "")       # 0到pos1角标是前段文字
        downurl = line[pos:lenline].replace('\n', '').replace('\r', '').replace('\t', '')
        #print(line)
        #print(workdir)         
        #print(downurl) 
        print("开始下载 "+str(i))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        delDir = workPath+workdir
        file = delDir+'.mp4'
        print(file)
        if os.path.exists(file):
            print("文件已存在，跳过")
        else:
            down(downurl,workPath,workdir,workdir)
            #print(downurl,workPath,workdir,workdir)
            try:
                shutil.rmtree(delDir) # 删除文件夹以及里面的所有文件
            except:
                print("下载失败！")
                pass
        print("结束下载 "+str(i))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        t = 30
        print("延时"+str(t))
        time.sleep(t)
        print("****"*15)
        i=i+1
    fi.close()



def down(downurl,workpath,workdir,fileName):

    m3u8DownExePath = "C:/N_m3u8DL-CLI_v2.6.3_with_ffmpeg_and_SimpleG/N_m3u8DL-CLI_v2.6.3.exe"
    workDir = ' --workDir '+workpath
    saveName = ' --saveName '+'"'+fileName+'"'
    threads = " --maxThreads 32 --minThreads 16"
    #baseUrl = "--baseUrl "+
    headers = ' --headers '+ '"User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"'
    options = m3u8DownExePath+' '+downurl+workDir+saveName+headers+threads
    #print(options)
    #win32api.ShellExecute(0,"open",m3u8DownExePath,options,'',1)
    print(options)
    os.system(options)


#https://blog.csdn.net/weiwei9363/article/details/50210599
#如果报错 在PATH和程序路径下找不到 ffmpeg.exe 就把 m3u8下载程序F:\N_m3u8DL-CLI_v2.6.3_with_ffmpeg_and_SimpleG 放到path 环境变量下面即可

if __name__ == '__main__':
    main()
    
