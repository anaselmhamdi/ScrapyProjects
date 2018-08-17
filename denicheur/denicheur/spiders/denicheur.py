import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from denicheur.items import DenicheurItem
import numpy as np
from datetime import datetime


class TopAchatSpider(CrawlSpider):
	name = "denicheur"
	start_urls = [
	"https://ledenicheur.fr/category.php?k=298",
	"https://ledenicheur.fr/category.php?k=328",
	"https://ledenicheur.fr/category.php?k=626",
	"https://ledenicheur.fr/category.php?k=480"]
	#,'298','328','626','480'
	rules = (
		Rule(LinkExtractor(allow = (),restrict_xpaths = ("//div[@class['show-on-hover']]/h3/a"))),
		Rule(LinkExtractor(allow = (),restrict_xpaths = ("//div[@class['show-on-hover']]/h3/a"))), 
		Rule(LinkExtractor(allow = (),restrict_xpaths = ("//div[@class['show-on-hover']]/h3/a"))), 
		Rule(LinkExtractor(allow = (), restrict_xpaths = ("//div[@class='page-nav-area']//a[@rel='next']")),follow = True),
		Rule(LinkExtractor(allow=('product\.php')),callback = "parse_item")
		)


	def parse_item(self, response):

		item = DenicheurItem()
		item["url"] = response.request.url
		item["price"] = response.xpath("//li[@id ='big_tab_priser']/a/p//span/text()").extract()
		try:
			item["price"] = item["price"][1].replace("\xa0","").replace(",",".")
		except:
			pass
		item["name"] = response.xpath("//span[@itemprop='name']/text()").extract()[-1]
		item["category"] = response.xpath("//span[@itemprop='name']/text()").extract()[:-1]
		item["specs"] = response.xpath("//li[@id ='big_tab_eg']/a/p//span/text()").extract()
		item['date_scraped'] = datetime.now()
		try:
			item['date_referenced'] = response.xpath("//td[@class='cell-bar']/a/@title").extract_first().replace("Mis à jour ","")
		except:
			item['date_referenced'] = np.nan
		return item