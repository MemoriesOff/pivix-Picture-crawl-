#encoding:UTF-8
import urllib.request
import urllib
import re
import time
import os

#注意更改cookies
cookies='请更改此处'
'''
函数名:findImgUrl
功能:找到图片地址
传入参数:p站图片页面地址
传出参数:图片地址
'''
def findImgUrl(url):
    try:
        req=urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0')
        req.add_header('Cookie',cookies)
        res=urllib.request.urlopen(req)
    except:
        print('图片页加载失败')
        return 0
    html=res.read().decode('utf8')
    imgUrls=re.findall( r'data-src=".*?" class="original-image"', html, 0)
    #print(len(imgUrls))
    if len(imgUrls)!=1:
            return['imgUrl ERROW']
    for imgUrl in imgUrls:
        imgUrl=re.sub(r'data-src="',"",imgUrl)
        imgUrl=re.sub(r'" class="original-image"',"",imgUrl)
        print(imgUrl)
        return imgUrl
'''
函数名:downlownImg
功能:下载图片
传入参数:p站图片地址,图片所在页面地址,文件名(不含文件格式)
传出参数:1成功,0失败
'''   
def downlownImg(imgUrl,imgPageUrl,name):
    try:
        req=urllib.request.Request(imgUrl)
        req.add_header('Referer',imgPageUrl)
        req.add_header('User-Agent','Mozilla/5.0')
        req.add_header('Cookie',cookies)
        res=urllib.request.urlopen(req)
    except:
        print(imgPageUrl)
        print(imgUrl)
        print('ERROR')
        return 0
    postfix=re.findall(r'\.\w{2,4}$',imgUrl,0)
    name=name+postfix[0]
    print(name)
    print("downlownding")
    f=open(name,'wb')
    f.write(res.read())
    f.close()
    return 1
'''
函数名:findIdfromSerch
功能:从搜索中找到id并转化为地址
传入参数:p站搜索地址
传出参数:id地址
'''
def findIdfromSerch(searchUrl):
    try:
        req=urllib.request.Request(searchUrl,headers={'User-Agent':'Mozilla/5.0'})
        res=urllib.request.urlopen(req)
        html=res.read().decode('utf8')
    except:
        print('搜索页打开失败')
        return 0
    #正则匹配
    x=0
    ids = re.findall( r'illust_id=\d{5,12}">', html, 0)
    for id in ids:
        id=re.sub(r'illust_id=',"",id)
        id=re.sub(r'">',"",id)
        id='http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+id
        print(id)
        x=x+1
    print(x)
    return [ids]
'''
函数名:downlodeFromImgpage
功能:从图片网页中下载图片
传入参数:图片网页地址,保存文件路径名(不含后缀名)
传出参数:无
'''
def downlodeFromImgpage(imgPageUrl,fileName):
    imgUrl=findImgUrl(imgPageUrl)
    if(1==downlownImg(imgUrl,imgPageUrl,fileName)):
        print("succees")

'''
函数名:findImgUrlFromRSS
功能:从排行榜抓取图片页面地址
传入参数:p站图片页面地址
传出参数:图片页面地址
'''
def findImgUrlFromRSS(RSSUrl):
    try:
        req=urllib.request.Request(RSSUrl)
        req.add_header('User-Agent','Mozilla/5.0')
        res=urllib.request.urlopen(req)
        html=res.read().decode('utf8')
    except:
        print("RSS加载出现问题")
        return 0
    imgUrls=re.findall( r'<link>.*?\d{2,8}</link>', html, 0)
    '''
    for imgUrl in imgUrls:
        imgUrl=re.sub(r'<link>',"",imgUrl)
        imgUrl=re.sub(r'</link>',"",imgUrl)
        print(imgUrl)
    ''' 
    print(len(imgUrls))
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


if(cookies=='请更改此处'):
    print("请更改cookies")
    os._exit()
rssUrl=modeChoose()
filePith=getFilePath()
imgUrls=findImgUrlFromRSS(rssUrl)
i=1;
if(os.path.exists(filePith)==False):
    try:
        os.makedirs(filePith)
    except:
        print("文件夹创建失败")
        os._exit()
for imgUrl in imgUrls:
    fileName=filePith+str(i)
    imgUrl=re.sub(r'<link>',"",imgUrl)
    imgUrl=re.sub(r'</link>',"",imgUrl)
    print(i)
    print(imgUrl)
    downlodeFromImgpage(imgUrl,fileName)
    i=i+1;
    time.sleep(3)
print('end')
