#encoding= utf-8
import MySQLdb

class sqlDB(object):
    def __init__(self,db):
        try:
            self.conn = MySQLdb.Connect(host='localhost',user='root',passwd = 'root',port=3306,charset='utf8')
            self.conn.select_db(db)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" %(e.args[0],e.args[1])
            
    def readShopmallList(self,city):
        shopmallNameDict = {}
        cur = self.conn.cursor()
        sql = 'select shopID,shopmallName from shopmall where shopmall.city = "%s"' %city 
        print sql
        try:
            count = cur.execute(sql) 
        except Exception:
            print "selecting shopmallName failure"
        results = cur.fetchall()
        for result in results:
            key = result[0]
            shopmallNameDict[key] = result[1]
        cur.close()
        return shopmallNameDict
    
    def writeShopmallResult(self,shopmallResultDict,city):
        cur = self.conn.cursor()
        sql = 'insert into shopmallresult (shopmallName,shopmallAddr,startDate,endDate,content,link,city) values (%s,%s,%s,%s,%s,%s,%s)'
        keywords = shopmallResultDict.keys()
        for keyword in keywords:
            infos = shopmallResultDict[keyword]
            for info in infos:
                value = (keyword,info[0],info[1],info[2],info[3],info[4],city)
                try:
                    cur.execute(sql,value)
                except Exception:
                    print "insert into shopmallresult error!"
                
        self.conn.commit()
        cur.close()

    def readBrandDict(self,city):
        brandDict = {}
        cur = self.conn.cursor()
        sql = 'select Id,brandName from brand where brand.city = "%s"' %city 
        print sql
        try:
            count = cur.execute(sql) 
        except Exception:
            print "selecting brand failure"
        results = cur.fetchall()
        for result in results:
            key = result[0]
            brandDict[key] = result[1]
        cur.close()
        return brandDict
    def readBrandUrls_pk(self):
        brandUrls = []
        cur = self.conn.cursor()
        sql = 'select brandUrl from brandurls' 
        print sql
        try:
            count = cur.execute(sql) 
        except Exception:
            print "selecting brand url failure"
        results = cur.fetchall()
        for result in results:
            brandUrls.append(result[0])
        cur.close()
        return brandUrls
    
    def writeBrandUrls_pk(self,brandUrls):
        cur = self.conn.cursor()
        sql = 'insert into brandurls (brandUrl) values (%s)'
        for brandUrl in brandUrls:
            value = (brandUrl)
            try:
                cur.execute(sql,value)
            except Exception:
                print "insert into brandurl error!"        
        self.conn.commit()
        cur.close()
    
    def writeBrandResult(self, brandResultDict,city ):
        cur = self.conn.cursor()
        sql = 'insert into brandresult (brandName,brandAddr,startDate,endDate,content,link,city) values (%s,%s,%s,%s,%s,%s,%s)'
        keywords = brandResultDict.keys()
        for keyword in keywords:
            infos = brandResultDict_sh[keyword]
            for info in infos:
                value = (keyword,info[0],info[1],info[2],info[3],info[4],city)
                try:
                    cur.execute(sql,value)
                except Exception:
                    print "insert into brandresult error!"
                
        self.conn.commit()
        cur.close()
        
    def __del__(self):
        self.conn.close()
        