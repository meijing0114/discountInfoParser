#encoding= utf-8
import database.mysql as mysql
import utils.utils as utils
import discountParser.discountparser_sh as exampleParser
import urllib2
import time
import re
from bs4 import BeautifulSoup
import discountParser.pkParser as pkParser

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'

def main():
    mysql_inst = mysql.sqlDB('discount')
    
    shopmallDict_sh = {}
    shopmallResultDict_sh = {}
    
    shopmallDict_sh = mysql_inst.readShopmallList('sh');
    shopmallUrlDict_sh = utils.urlGenerate(shopmallDict_sh)
    
    parser = exampleParser.discountParser(shopmallUrlDict_sh)
    shopmallResultDict_sh = parser.parse()
    # keyword -> addr startDate endDate title
    mysql_inst.writeShopmallResult(shopmallResultDict_sh,'sh')
    
    
    # Parsing shanghai brand
    brandDict_sh = {}
    brandDict_sh = mysql_inst.readBrandDict('sh')
    brandUrlDict_sh = utils.urlGenerate(brandDict_sh)
    
    parser_new = exampleParser.discountParser(brandUrlDict_sh)
    brandResultDict_sh = parser_new.parse()
    
    mysql_inst.writeBrandResult(brandResultDict_sh,'sh')
    
    #############################Beijing#################
    
    # PK shopmall
    districtUrlPage_pk = 'http://shopping.55bbs.com/market/list_0__1.html'
    parser_shopmall_pk = pkParser.pkShopmallParser()
    
    districtUrls = parser_shopmall_pk.retrieveDistrictUrls(districtUrlPage_pk)
    parser_shopmall_pk.retrieveValidShopmallUrls(districtUrls)
    shopmallResultDict_pk = parser_shopmall_pk.parseShopmallUrls()
    mysql_inst.writeShopmallResult(shopmallResultDict_pk,'pk')
    
    # PK brand
    parser_brand_pk = pkParser.pkShopmallParser()
    brandResultDict_pk = parser_brand_pk.parseBrandContents()
    mysql_inst.writeBrandResult(brandResultDict_pk,'pk')
    

if __name__ == '__main__' : 
    main()


