#encoding:utf-8
import sys
import urllib2
import re
from bs4 import BeautifulSoup
import thread
import time

class SpiderModel:
    def __init__(self):
        self.page = 1

        #load frawered url dict
        self.fcrawerlist = open("./craweredlist.txt",'r');
        if not self.fcrawerlist:
            print "no fraweredlist.txt\n will exit..."
            exit(-1)
        self.crawleredDict = {}
        for line in self.fcrawerlist.readlines():
            curline = line.split();
            self.crawleredDict [curline] = 1;

        self.contentTargetFile = open("./contentFile.txt",'w+');

        self.testMaxNum = 10;
        self.curCnt = 0;
        self.fhPrefix = "http://wap.fh21.com.cn"

    def GetPageRecur(self,url):
        if self.crawleredDict.has_key(url):
            print url+" has crawered skip it..."
            return
        if self.curCnt > self.testMaxNum:
            return

        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header =  {'User-Agent' : userAgent,
                   'refer': url}
        req = urllib2.Request(url, headers = header)
        #try:
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
            #unicodePage = myPage.decode("utf-8")
        soup = BeautifulSoup(myPage, 'html.parser')

        title = self.getFh21Title(soup)
        totalPagenNum = self.getFh21TotalNum(soup)
        content = ""
        print totalPagenNum
        if totalPagenNum > 1 and totalPagenNum < 20:
            content = self.mergeMutiPageContent(url, totalPagenNum)
        else:
            content = self.extractFh21Content(myPage,soup)

        self.contentTargetFile.write(title)
        self.contentTargetFile.write(content)

            #self.extractFh21Content(soup)
        print url + " del finish is the " + str(self.curCnt) + "ed page"
        self.crawleredDict [url] = 1
        self.curCnt += 1
        #recursive
        curPageUrls = self.getFh21Urls(soup, url)
       # print curPageUrls
            #for url in curPageUrls:
            #    self.GetPageRecur(url)
        #except Exception,e:
        #    print Exception,":",e



    def GetPageNumContent(self,url):
        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header =  {'User-Agent' : userAgent}
        req = urllib2.Request(url, headers = header)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        #unicodePage = myPage.decode("utf-8")
        #print myPage
        soup = BeautifulSoup(myPage, 'html.parser')
        #print soup
        curContent = self.extractFh21Content(myPage, soup);
        return curContent

    def mergeMutiPageContent(self, url, maxNum):
        halfUrl = url[:-5]
        totalContent = ""
        for i in range(maxNum):
            if i == 0:
                curUrl = url
            else:
                curUrl = halfUrl + '_' + str(i+1) + ".html";
            print "will crawl " + curUrl
            totalContent += (self.GetPageNumContent(curUrl) + "--")
            #time.sleep(5)
        return totalContent

    def getFh21TotalNum(self, soup):
        totalPageNum = int(soup.find_all("span",class_="total")[0].string)
        return totalPageNum

    def getFh21Urls(self, soup, curUrl):
        allAtags = soup.find_all(href=re.compile('view'))
        urls = []
        for a in allAtags:
            if a['href'].find("fh21") > 1:
                urls.append(a['href'])
            else:
                urls.append(self.fhPrefix + a['href'])
        return urls
        #print a['href']

    def getFh21Title(self, pageContent):
        soupTitle = pageContent.title
        curTitle = "\nno title";
        if soupTitle:
            curTitle = soupTitle.get_text()
        return curTitle

        #self.contentTargetFile.write(curTitle)

    def extractFh21Content(self, pageContent, soupData):
        #    print title
        curPageContent = ""
        allUlTags = soupData.find_all("ul");
        for ulTag in allUlTags:
            ulStr = str(ulTag)
            ulStr = ulStr.replace("\n","").replace("\r\n", "")
           # pageContent = pageContent.replace("\r\n","").replace("\n","");
            contentR = re.compile(r'FhwapContent.*?yunying_block');
            contentTag = contentR.findall(ulStr)
            if contentTag:
                allPtags= ulTag.find_all("p")
                if allPtags:
                    for curP in allPtags:
                        tmp = curP.get_text()
                        if tmp.find("yunying_block") > 0:
                           continue
                        if curP.has_attr('id') and curP['id'] == "yunying_block":
                           continue
                        curPageContent += curP.get_text()+"++"

                #print ulTag.get_text();
        print curPageContent
        return curPageContent
           # print contentTag[0]
        #for content in contents:

        #Maincontent =soupData.find_all(id="FhwapContent")

#        if Maincontent:
#            allPtags= Maincontent[0].find_all("p")
#            if allPtags:
#                for curP in allPtags:
#                    tmp = curP.get_text()
#                    if tmp.find("yunying_block") > 0:
#                        continue
#                    if curP.has_attr('id') and curP['id'] == "yunying_block":
#                        continue
#                    print curP
#                    curPageContent += curP.get_text()+"++"

        #self.contentTargetFile.write(curPageContent+"\n")
        #return curPageContent
      #  for p in content:
      #      print p
        #print content[0].get_text()

reload(sys)
sys.setdefaultencoding('utf-8')
spriderHander = SpiderModel()
spriderHander.GetPageRecur("http://wap.fh21.com.cn/view/764718.html")
