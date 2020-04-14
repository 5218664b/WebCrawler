项目说明

1.运行项目
	切换到项目根目录,执行scrapy的运行命令
	
	cd D:\WebCrawler\pornhub
	scrapy crawl porn -o porn.json -s FEED_EXPORT_ENCODING=utf-8 

2.国内不能直接访问，请自备fanqiang技能，ssr需要设置全局代理，爬虫没有直接下载视频，爬了链接到pornhub.links文件中，将关键词查询结果页面下所有视频的下载链接爬了下来
修改endPageNum变量的值改变爬取页数
修改searchKey变量改变查询关键词