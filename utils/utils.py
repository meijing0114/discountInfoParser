#encoding=utf-8
import re

def urlGenerate(Dict_sh):
    UrlDict_sh = {}
    shopIDs = Dict_sh.keys()
    urlBase = 'http://www.mplife.com/temai/Search.aspx?query=0-0-0-0-0-0-4-1&keyword='
    for shopID in shopIDs:
        info = []
        keyword = Dict_sh[shopID]
        keyword = re.sub(' ','+',keyword)
        print "keyword:"
        print keyword.encode('utf-8')
        url = urlBase + keyword
        info.append(url)
        info.append(keyword)
        UrlDict_sh[shopID] = info
    
    return UrlDict_sh
