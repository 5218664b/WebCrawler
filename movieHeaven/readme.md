项目说明

1.运行项目
	切换到项目根目录,执行scrapy的运行命令
	
	cd D:\WebCrawler\movieHeaven
	scrapy crawl movie -o dy8item.json -s FEED_EXPORT_ENCODING=utf-8

2.这个爬虫抓取的是电影天堂的电影下载链接，可能很多链接都不能用了，dy8item.json存的json格式的数据，movie.links里面仅仅是ftp或者磁力链接，可以直接拷贝到迅雷下载