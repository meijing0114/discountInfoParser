#encoding= utf-8
import time
import urllib2
from bs4 import BeautifulSoup
import re
import math

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'
class pkParser(object):
    def __init__(self):
       pass
    def extractDate(self,timeinfo):
        startDate = '2013/' 
        endDate = '2013/'
        pattern = re.compile(r'\d{1,2}')
        results = re.findall(pattern,timeinfo)
        startDate = startDate+results[0]+'/'+results[1]
        endDate = endDate + results[2] + '/' + results[3]
    
        return startDate,endDate
class pkShopmallParser(pkParser):
    def __init__(self):
        pkParser.__init__()
        
    def parseShopmallUrls(self):
        shopmallResultDict_pk = {}
        for shopmallUrl in self.shopmallUrls:
            try:
                request = urllib2.Request(shopmallUrl)
                request.add_header('User-agent', user_agent)
                request.set_proxy('192.168.8.87:3128','http')
                response = urllib2.urlopen(request)
                html = response.read()
                soup = BeautifulSoup(html)
                ul = soup.find('ul',attrs={"class":"zklt_tab clearfix"})
                if ul == None:
                    print "No valid results"
                else:
                    print "valid results"
                    try:
                        # get shop adddr
                        div = soup.find('div',attrs={"class":"dpzk_yysj"})
                        div_soup = BeautifulSoup(str(div))
                        ps = div_soup.find_all('p')
                        p_addr = ps[2]
                        addr_tmp = p_addr.get_text().encode('utf-8')
                        addr = re.sub('商场地址','',addr_tmp)[3:]
                        ul_soup = BeautifulSoup(str(ul))
                        lis = ul_soup.find_all('li')
                        infos = []
                        for li in lis:
                            info = []
                            info.append(addr)
                            li_soup = BeautifulSoup(str(li))
                            ps = BeautifulSoup(str(li_soup.find('div',attrs={"class":"info"}))).find_all('p')
                            timeinfo = ps[2].string.encode('utf-8')
                            key = ps[1].string.encode('utf-8')
                            key = key[9:]
                            startDate, endDate = self.extractDate(timeinfo)
                            info.append(startDate)
                            info.append(endDate)
                            tag = li.span.string.encode('utf-8')
                            content = li.p.string.encode('utf-8')
                            activity = '['+tag+']'+content
                            info.append(activity)
                            link = li.p.a['href']
                            info.append(link)
                            infos.append(info)
                        shopmallResultDict_pk[key] = infos  
                    except Exception:
                        print "parsing valid results shopmall pk failure"   
            except Exception:
                print "url request error!"
            time.sleep(5)
        return shopmallResultDict_pk

    def retrieveValidShopmallUrls(self,districtUrls):
        shopmallUrls = []
        for districtUrl in districtUrls:
            try:
                request = urllib2.Request(districtUrl)
                request.add_header('User-agent', user_agent)
                request.set_proxy('192.168.8.87:3128','http')
                response = urllib2.urlopen(request)
                html = response.read()
                soup = BeautifulSoup(html)
                ul = soup.find('ul',attrs={"class":"brand_lt clearfix"})
                ul_soup = BeautifulSoup(str(ul))
                lis = ul_soup.find_all('li')
                for li in lis:
                    link = li.a['href']
                    link = re.sub('all','go',link)
                    shopmallUrls.append(link)    
            except:
                print "retrieve valid shopmall url failure!"
            time.sleep(2);
        self.shopmallUrls = shopmallUrls

    def retrieveDistrictUrls(self,districtUrlPage_pk):
        districtUrls = []
        request = urllib2.Request(districtUrlPage_pk)
        request.add_header('User-agent', user_agent)
        request.set_proxy('192.168.8.87:3128','http')
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html)
        ul = soup.find('ul',attrs={"class":"brand_tags clearfix"})
        ul_soup = BeautifulSoup(str(ul))
        lis = ul_soup.find_all('li')
        for li in lis:
            link = li.a['href']
            districtUrls.append(link)
        return districtUrls
    
class pkBrandParser(pkParser):
    def __init__(self):
        pkParser.__init__()
        self.brandUrls=  self.parseBrandUrls()
    
    def parseBrandContents(self):
        brandResultDict_pk = {}
        for brandUrl in self.brandUrls:
            try:
                request = urllib2.Request(brandUrl)
                request.add_header('User-agent', user_agent)
                request.set_proxy('192.168.8.87:3128','http')
                response = urllib2.urlopen(request)
                html = response.read()
                soup = BeautifulSoup(html)
                ul = soup.find('ul',attrs={"class":"zklt_lt clearfix"})
                key_div = soup.find('div',attrs={"class":"crumb"})
                key = BeautifulSoup(str(key_div)).find_all('a')[1].get_text().encode('utf-8')
                if ul == None:
                    print "No valid results"
                else:
                    print "valid results"
                    ul_soup = BeautifulSoup(str(ul))
                    lis = ul_soup.find_all('li')
                    infos = []
                    for li in lis:
                        info = []
                        li_soup = BeautifulSoup(str(li))
                        ps = BeautifulSoup(str(li_soup.find('div',attrs={"class":"info"}))).find_all('p')
                        timeinfo = ps[1].get_text().encode('utf-8')
                        addr = ps[2].get_text().encode('utf-8')
                        addr =  addr[15:]
                        info.append(addr)
                        startDate, endDate = self.extractDate(timeinfo)
                        info.append(startDate)
                        info.append(endDate)
                        content = ps[0].a.string.encode('utf-8')
                        info.append(content)
                        link = ps[0].a['href']
                        info.append(link)
                        infos.append(info)
                    brandResultDict_pk[key] = infos
                    time.sleep(5)
            except Exception:
                print "parse brand content falure"
        return brandResultDict_pk
    
    def parseBrandUrls(self):
        brandUrls = []
        catagory = 1    
        while catagory <= 14:
            pageNum = 1
            url = 'http://shopping.55bbs.com/categorylist_%d_0__%d.html' %(catagory,pageNum)
            url = url.encode('utf-8')
            brandUrls,soup = self.getPageUrl(url,brandUrls)
            totalPage = self.getTotalPage(soup)
            while pageNum < totalPage:
                pageNum = pageNum + 1
                url = 'http://shopping.55bbs.com/categorylist_%d_0__%d.html' %(catagory,pageNum)
                url = url.encode('utf-8')
                brandUrls,soup = self.getPageUrl(url,brandUrls)    
            catagory = catagory + 1
            time.sleep(6)   
    
        return brandUrls

    def getTotalPage(self,soup):
        num = soup.find('div',attrs={"class":"brand_tit"}).span.em.string.encode('utf-8')
        totalPage = math.ceil(int(num)/36)
        return totalPage

    def getPageUrl(self,url,brandUrls):
        request = urllib2.Request(url)
        request.add_header('User-agent', user_agent)
        request.set_proxy('192.168.8.87:3128','http')
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html)
        ul = soup.find('ul',attrs={"class":"brand_lt clearfix "})
        ul_soup = BeautifulSoup(str(ul))
        lis = ul_soup.find_all('li')
        for li in lis:
            link = li.a['href']
            link = re.sub('all','go',link)
            if self.brandValid(li):
                brandUrls = list(brandUrls)
                brandUrls.append(link)
        return brandUrls,soup
    
    def brandValid(self,li):
        num = li.div.i.string.encode('utf-8')
        if num == '0':
            print 'No valid discount for brand'
            return False
        return True