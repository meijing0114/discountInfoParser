discountInfoParser
==================
这个程序分别从上海和北京分别抓取商场和品牌的打折信息：
- 对于上海主要来源是mplife.com
- 对于北京是55bbs.com

由于mplife搜索的url有规律，所以对于商场和品牌一律采用加关键词的url请求的方式进行打折信息抓取，再将抓取到的信息进行格式化后存入数据库：
- brand/shopmall-Name
- addr
- startDate
- endDate
- content
- link
- city

而55bbs无法利用搜索功能，所以只有从入口页将所有商场和品牌单独的url抓取下来，然后再进行进一步的页面解析操作：
- 对于北京商场，以行政区划分作为入口页
- 对于品牌，则是分为14个品牌类别作为入口页

抓取下来存入数据库的字段同上