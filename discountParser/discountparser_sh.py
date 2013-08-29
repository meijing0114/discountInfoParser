#encoding= utf-8
import urllib, urllib2
import re
import time
from bs4 import BeautifulSoup#放在lib里面

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'
class discountParser(object):
    def __init__(self, urlDict):
        self.urlDict = urlDict
        self.ResultDict_sh = {}
            
    def parse(self):
        shopIDs = self.urlDict.keys()
        for shopID in shopIDs:
            info = self.urlDict[shopID]
            url = info[0].encode('utf-8')
            keyword = info[1]

            #keyword = '太平洋百货徐汇店'
            #url = 'http://www.mplife.com/temai/Search.aspx?query=0-0-0-0-0-0-4-1&keyword=Nine+West'
            #url = url.encode('utf-8')
            print "url"
            print url
            self.parseContent(url,shopID,keyword)
            time.sleep(3)    
        return self.ResultDict_sh
    
    def parseContent(self,url,shopID,keyword):
        key = shopID
        request = urllib2.Request(url)
        request.add_header('User-agent', user_agent)
        request.set_proxy('192.168.8.87:3128','http')
        try:
            response = urllib2.urlopen(request)
            html = response.read()
            soup = BeautifulSoup(html)
    
            div = soup.find_all('div',attrs={"class":"seach-result"})
            div_soup = BeautifulSoup(str(div))
            text = div_soup.get_text().encode('utf-8')
            pattern = re.compile(r'有.*个')
            match = re.findall(pattern,text)
            print "match"
            print match
            result_num = int(match[0][3:len(match[0])-3])
            print result_num
                
            if result_num == 0:
                print "no result!"
                return
            elif result_num <= 15:
                print "one page"
                self.parsePage(soup,keyword)
            else:
                print "multiple page"
                page_num = result_num/15
                page_index = 2
                while page_index <= page_num:
                    url = 'http://www.mplife.com/temai/Search.aspx?query=0-0-0-0-0-0-4-%s&keyword=%s' %(str(page_index),keyword)
                    url = url.encode('utf-8')
                    request = urllib2.Request(url)
                    request.add_header('User-agent', user_agent)
                    request.set_proxy('192.168.8.87:3128','http')
                    response = urllib2.urlopen(request)
                    html = response.read()
                    soup = BeautifulSoup(html)
                    discount_boxes = soup.find_all('div',attrs={"class":"box1"})
                    self.parsePage(soup,keyword)
                    page_index = page_index + 1
                    time.sleep(3)    
        except Exception:
            print "url open and parsing error!"
        
    def parsePage(self,soup,keyword):
        print "parsing page"
        discount_boxes = soup.find_all('div',attrs={"class":"box1"})
        infos = []
        for discount_box in discount_boxes:
            info = []
            if discount_box.h3.get_text() == None:
                print "empty"
                continue
            title = discount_box.h3.get_text().encode('utf-8')
            h3_soup = BeautifulSoup(str(discount_box.h3))
            link = h3_soup.find_all('a',attrs={"class":"red"})[0]['href']
            print "link:"
            print link
            p2 = discount_box.find_all('p')
            date = p2[0].get_text().encode('utf-8')
            addr = p2[1].get_text().encode('utf-8')
            addr = self.elimSpace(addr)
            title = self.elimSpace(title)
            date = self.elimSpace(date)
            startDate,endDate = self.getDate(date)
            info.append(addr)
            info.append(startDate)
            info.append(endDate)
            info.append(title)
            info.append(link)
            infos.append(info)
        self.ResultDict_sh[keyword] = infos
    
    def elimSpace(self,string):
        string = string.strip()
        tmp = string.split(' ')
        result = ''.join(tmp)
        return result
    def getDate(self, date):
        pattern = re.compile(r'\d{4}\/\d{1,2}\/\d{1,2}')
        results = re.findall(pattern,date)
        startDate = results[0]
        endDate = results[1]
        print startDate
        print endDate
        return startDate,endDate
    
    