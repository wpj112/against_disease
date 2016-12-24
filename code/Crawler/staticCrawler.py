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

        self.testMaxNum = 100;
        self.curCnt = 0;
        self.fhPrefix = "http://wap.fh21.com.cn"

    def GetPage(self,url):
        if self.crawleredDict.has_key(url):
            print url+" has crawered skip it..."
            return
        if self.curCnt > self.testMaxNum:
            return

        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header =  {'User-Agent' : userAgent}
        req = urllib2.Request(url, headers = header)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        #unicodePage = myPage.decode("utf-8")
        soup = BeautifulSoup(myPage, 'html.parser');
        self.extractFh21Content(soup)
        print url + " del finish is the " + str(self.curCnt) + "ed page"
        self.crawleredDict [url] = 1;
        self.curCnt += 1
        #recursive
        curPageUrls = self.getFhUrls(soup, url)
       # print curPageUrls
        for url in curPageUrls:
            self.GetPage(url)

    def getFhTotalNum(self, soup):
        totalPageNum = int(soup.find_all("span",class_="total")[0].string);
        return totalPageNum

    def getFhUrls(self, soup, curUrl):
        allAtags = soup.find_all(href=re.compile('view'));
        urls = []
        for a in allAtags:
            if a['href'].find("fh21") > 1:
                urls.append(a['href'])
            else:
                urls.append(self.fhPrefix + a['href'])
        return urls
        #print a['href']

    def extractFh21Content(self, pageContent):
        #    print title
        #contents = re.findall('<ul.*?detail03.*?FhwapContent.*?ul>', pageContent)
        #for content in contents:
        #    print content
        soupTitle = pageContent.title
        curTitle = "\nno title";
        if soupTitle:
            curTitle = soupTitle.get_text()

        self.contentTargetFile.write(curTitle)

        Maincontent = pageContent.find_all(id="FhwapContent")
        if Maincontent:
            content = Maincontent[0].find_all("p")
            if content:
                self.contentTargetFile.write(content[0].get_text()+"\n")
      #  for p in content:
      #      print p
        #print content[0].get_text()

reload(sys)
sys.setdefaultencoding('utf-8')
spriderHander = SpiderModel()
spriderHander.GetPage("http://wap.fh21.com.cn/view/764718.html")
