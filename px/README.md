项目说明

1.运行项目
	切换到项目根目录,执行scrapy的运行命令
	
	cd D:\WebCrawler\px
	scrapy crawl pxs -o pxs.json -s FEED_EXPORT_ENCODING=utf-8

2.爬取的是500px上搜索关键词“woman”返回的图片,从第11页开始到111页,图片存储在crawlImage文件夹
修改searchKey变量改变搜索关键词
修改pageCount变量改变爬取的页数
修改setting.py文件中的IMAGES_STORE变量的值改变存储路径