from wtj.items import WtjItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class TopAchatSpider(CrawlSpider):
	name = 'wtj'
	starturl = ['https://www.welcometothejungle.co/companies']
	