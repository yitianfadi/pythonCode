from lxml import etree
import openpyxl   
import requests
import random
import time
import datetime
import os
import sys

BASE_DOMAN = "https://www.dytt8.net"

HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }

def get_text_html(url,HEADERS):
    try:
        response = requests.get(url,headers=HEADERS)
        text = response.content.decode(encoding='gbk',errors='ignore')  #errors 忽略错误
        html = etree.HTML(text)
        return html
    except Exception :
        #print(re)
        #quit()
        pass

def get_detail_urls(url):
   # url = "https://www.dytt8.net/html/gndy/china/list_4_1.html"
    html = get_text_html(url,HEADERS)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = list(set(detail_urls)) 
    try:
        detail_urls.remove('/html/gndy/dyzz/index.html') 
        detail_urls.remove('/html/gndy/jddy/index.html') 
    except Exception :
        pass

    detail_urls = map(lambda url:BASE_DOMAN+url,detail_urls)
    return detail_urls
    
def parse_detial_page(url):
    
    movie = {}
    html = get_text_html(url,HEADERS)

    try:
        title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
        if (title):
            movie['title'] = title
            
    except Exception :
        title = "未获取到title"
        movie['title'] = title
    print(movie['title'])
    
    try:
        zoomE = html.xpath("//div[@id='Zoom']")[0]
        img = zoomE.xpath(".//img/@src")
        movie['img'] = img
    except Exception :
        img = "未获取到img"
        movie['img'] = img
    print(movie['img'])

    try:
        zoomEe = html.xpath("//div[@id='Zoom']")[0]
        infos = zoomEe.xpath(".//text()")
        for info in infos:
            if info.startswith("◎片　　名"):
                info = parse_info(info,"◎片　　名")
                movie['moveName'] = info
            elif info.startswith("◎年　　代"):
                info = parse_info(info,"◎年　　代")
                movie['year'] = info
            elif info.startswith("◎产　　地"):
                info = parse_info(info,"◎产　　地")
                movie['country'] = info
            elif info.startswith("◎类　　别"):
                info = parse_info(info,"◎类　　别")
                movie['category'] = info
            elif info.startswith("◎语　　言"):
                info = parse_info(info,"◎语　　言")
                movie['language'] = info
            elif info.startswith("◎上映日期"):
                info = parse_info(info,"◎上映日期")
                movie['createTime'] = info
    except Exception :
        error = "未获取到数据"
        movie['moveName'] = error
        movie['year'] = error
        movie['country'] = error
        movie['category'] = error
        movie['language'] = error
        movie['createTime'] = error
    print(movie['moveName'])
    print(movie['year'])
    
    try:
        infosa = html.xpath("//div[@id='Zoom']//p//text()")
        #print("infosa",infosa)
        for info in infosa:
            if info.startswith("◎片　　长"):  #//*[@id="Zoom"]/span/p[1]/text()[12]
                info = parse_info(info,"◎片　　长")
                movie['time'] = info
            else:
                movie['time'] = "无片长"
           # print(info)
    except Exception :
        error = "未获取到数据"
        movie['time'] = error
    print(movie['time'])

    try:
        infosb = html.xpath("//div[@id='Zoom']//p//text()")
        #print("infosb",infosb)
        for info in infosb:
            if info.startswith("◎导　　演"):
                info = parse_info(info,"◎导　　演")
                movie['direct'] = info
            else:
                movie['direct'] = "无导演信息"
    except Exception :
        error = "未获取到数据"
        movie['direct'] = error
    print(movie['direct'])

    try:
        zoomEec = html.xpath("//div[@id='Zoom']")[0]
        infosc = html.xpath(".//text()")
        for index,info in enumerate(infosc):
            if info.startswith("◎编　　剧"):
                info = parse_info(info,"◎编　　剧")
                movie['bianju'] = info
                print(info)
            elif info.startswith("◎主　　演"):
                info = parse_info(info,"◎主　　演")
                actors = [info]
                for x in range(index+1,len(infosc)):
                    actor = infosc[x].strip()
                    if actor.startswith("◎"):
                        break
                    actors.append(actor)
                movie['zhuyan'] = actors
                print(actors)
            elif info.startswith("◎简　　介"):
                info = parse_info(info,"◎简　　介")
                jianjies = [info]
                if len(jianjies):
                    for x in range(index+1,len(infosc)):
                        jianjie = infosc[x].strip()
                        if jianjie.startswith("◎获奖情况"):
                            break
                        elif jianjie.startswith("【下载地址】"):
                            break
                        jianjies.append(jianjie)
                else:
                    jianjies="无简介"
                #print(jianjies)
                movie['jianjie'] = jianjies   
    except Exception: #as re
        error = "未获取到数据"
        movie['bianju'] = error
        movie['zhuyan'] = error
        movie['jianjie'] = error
        
    
    try:
        download_magnet_url = html.xpath("//div[@id='Zoom']/span/p[1]/a/@href")   # //*[@id="zhongdian"]
        print("download_magnet_url",download_magnet_url)
        if 'magnet:?xt=urn:btih' in download_magnet_url:
            movie['download_magnet_url'] = download_magnet_url
        else:
            movie['download_magnet_url'] = "无迅雷下载链接"
    except Exception:
        movie['download_magnet_url'] = "未获取到磁力链下载地址"

    try:
        download_thunder_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@fieediwh") # //*[@id="Zoom"]/span/table/tbody/tr/td/a
        movie['download_thunder_url'] = download_thunder_url
        print(download_thunder_url)
    except Exception:
        movie['download_thunder_url'] = "未获取到迅雷下载地址"

    try:
        download_ftp_url = html.xpath("//td[@bgcolor='#fdfddf']/a/text()")[0]  
        movie['download_ftp_url'] = download_ftp_url
    except Exception:
        movie['download_ftp_url'] = "未获取到下载ftp地址"

    return movie

def parse_info(info,rule):
    return info.replace(rule,"").strip()

def spider(base_url,start,end):
    #base_url "https://www.dytt8.net/html/gndy/china/list_4_{}.html"
    movies = []
    for x in range(start,end): #控制总页数
        url = base_url.format(x)
        print(datetime.datetime.now())
        print("正在采集第"+str(x)+"页，请稍后。。。")
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls: #遍历一页中的所有详情的url
            movie = parse_detial_page(detail_url)
            movies.append(movie)
        times = random.randint(5,20)    
        print("休眠"+str(times)+"秒")
        #print(datetime.datetime.now())
        time.sleep(times) #随机休眠几秒
    print("采集结束")
    return movies

if __name__ == "__main__":

    movies=[]
    base_url = "https://www.dytt8.net/html/gndy/china/list_4_{}.html"
    wb = openpyxl.Workbook()  # 创建Excel对象
    ws = wb.active  # 获取当前正在操作的表对象
    # 往表中写入标题行,以列表形式写入！
    ws.append(['title', '海   报', '片　　名', '年　　代', '产　　地',
               '类　　别', '语　　言', '上映日期', '片　　长', '导　　演',
               '编　　剧','主　　演','简　　介','磁力链','迅雷下载','下载地址'])
    movies = spider(base_url,1,125) #控制总页数 1 125
    i = 1
    for move in movies:
        #print(move)
        listmovie = []
        for key,vals in move.items():
            if type(vals) == list:
                val = ' '.join([item for item in vals])
            else:
                val = str(vals)
            listmovie.append(val)
            #print(key, val)
        print("正在写入第"+str(i)+"条数据")
        #print(listmovie)
        ws.append(listmovie)
        i = i+1
        #print("***"*20)
    today=str(datetime.date.today())
    wb.save(sys.path[0]+'/'+today+'.xlsx')
    print("数据写入完成")
