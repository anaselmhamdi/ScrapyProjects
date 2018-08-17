import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from TopAchat.items import TopachatItem
import numpy as np
import datetime

class TopAchatSpider(CrawlSpider):
	name = "TopAchat1"
	start_urls = ["https://www.topachat.com/pages/marque.php"]
	
	rules = ( Rule(LinkExtractor(restrict_xpaths=('//*[@id="content"]/section/ul[@class="listProduct"]//a'))),
		Rule(LinkExtractor(allow  = ('detail2'), restrict_xpaths=("//div[@id='lexik']//li//a")),callback='parse_item'),
		)

	def parse_item(self, response):
		
		item = TopachatItem()
		item["brandname"] = response.xpath("//div[@class='small']/div/text()").extract_first()[4:].split(" ")[0]
		item["href"] = response.request.url 
		item["name"] = response.xpath("//div[@class='libelle']/h1/text()").extract_first()
		item["specs"] = response.xpath("//strong[@class='big short-descr']/text()").extract_first()
		item["product_type"] = response.xpath("//nav[@class='meta small']//p//b/text()").extract_first()
		item["date_scraped"] = datetime.datetime.now()
		item["date_referenced"] = response.xpath("//nav[@class='meta small']//p//a/b/text()").extract()[-1:][0]
		try :
			item["price"] = response.xpath("//div[@class='prix']//span/text()").extract()[1].replace("\xa0","")
		except:
			item["price"] = np.nan
		return item