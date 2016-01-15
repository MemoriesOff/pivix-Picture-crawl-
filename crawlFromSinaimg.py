#encoding:UTF-8
import urllib.request
import urllib
import re
import time
import os
'''
函数名:downlownImg
功能:下载图片
传入参数:图片地址,文件名
传出参数:1成功,2失败
'''   
def downlownImg(imgUrl,name):
    try:
        req=urllib.request.Request(imgUrl)
        req.add_header('User-Agent','Mozilla/5.0')
        res=urllib.request.urlopen(req)
    except:
        print("下载遇到问题")
        return 0
    postfix=re.findall(r'\.\w{2,4}$',imgUrl,0)
    name=name+postfix[0]
    print(name)
    print("downlownding")
    try:
        f=open(name,'wb')
        f.write(res.read())
        f.close()
    except:
        print("文件读写遇到问题")
        return 0
    return 1
'''
函数名:findImgUrlFromRSS
功能:从排行榜抓取图片新浪图床地址
传入参数:p站图片页面地址
传出参数:图片页面地址
'''
def findImgUrlFromRSS(RSSUrl):
    try:
        req=urllib.request.Request(RSSUrl)
        req.add_header('User-Agent','Mozilla/5.0')
        res=urllib.request.urlopen(req)
    except:
        print("RSS加载出现问题")
        return 0
    html=res.read().decode('utf8')
    imgUrls=re.findall( r'http://ww\d.sinaimg.cn/large/.*?"', html, 0)
    '''
    for imgUrl in imgUrls:
        imgUrl=re.sub(r'"',"",imgUrl)
        print(imgUrl)
    '''
    print("总计%d幅图像",len(imgUrls))
    return imgUrls

'''
函数名:findImgUrlFromRSS
功能:输入存储文件路径
传入参数:无
传出参数:存储文件路径
'''
def getFilePath():
    while(True):
        print("请输入文件存储路径(c:\example\):")
        filePath=re.findall( r'^((?:[a-zA-Z]:)?\\(?:[^\\\?\/\*\|<>:"]+\\)*?)$', input(), 0)
        if(len(filePath)==1):
            break
        print("文件路径存储错误,请重新输入")
        print("例: c:\example\\")
    os.mkdir('d:\hello')
    return filePath[0]
'''
函数名:modeChoose
功能:模式选择
传入参数:无
传出参数:rss地址
'''
def modeChoose():
    while(True):
        print("请选择模式(1-6):")
        print("1.本日排行\n2.本周排行\n3.本月排行\n4.原创排行\n5.新人排行\n6.男性向排行\n7.女性向排行\n")
        i=input()
        filePath=re.findall( r'^[1-7]$', i, 0)
        if(len(filePath)==1):
            break
        print("模式输入错误,请重新输入")
    address=('daily','weekly','monthly','original','rookie','male','female')
    while(True):
        print("请选择数量(1-5):")
        print("1.10\n2.20\n3.30\n4.40\n5.50\n")
        j=input()
        filePath=re.findall( r'^[1-5]$', j, 0)
        if(len(filePath)==1):
            break
        print("数量输入错误,请重新输入")
    rssUrl='http://rakuen.thec.me/PixivRss/'+address[int(i)]+'-'+str(j)+'0'
    print(rssUrl)
    return rssUrl

rssUrl=modeChoose()
filePith=getFilePath()
imgUrls=findImgUrlFromRSS(rssUrl)
i=1;
if(os.path.exists(filePith)==False):
    os.makedirs(filePith)
for imgUrl in imgUrls:
    fileName=filePith+str(i)
    imgUrl=re.sub(r'"',"",imgUrl)
    print(i)
    print(imgUrl)
    if(downlownImg(imgUrl,fileName)==1):
        print("succees")
    i=i+1;
    time.sleep(3)
print('end')
