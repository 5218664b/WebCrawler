# WebCrawler
各种爬虫

### 1.目前写了以下几个网站的爬取

500px.com

pornhub.com

dytt8.net

toptxt.net

whatismybrowser.com

qzone.qq.com

### 2.代码运行说明：

在windows下安装anaconda和scrapy，参考[博客](http://www.purepure.top/index.php/%E7%88%AC%E8%99%AB/91.html)

进入项目路径，例如

    cd ./WebCrawler/px/

    scrapy crawl pxs -o pxs.json -s FEED_EXPORT_ENCODING=utf-8 

运行命令都在spilders/xxx.py文件的class上面写着

### 3.项目创建备注
    #无需创建文件夹
    scrapy startproject sina
    scrapy genspider sinaSpider sina.com
    