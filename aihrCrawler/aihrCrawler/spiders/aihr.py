import scrapy
# from scrapy.cmdline import execute
# execute("scrapy crawl aihr".split())
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector


class AihrSpider(scrapy.Spider):
    name = "aihrSpider"
    headers = {
        'authority': 'www.aihr.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
        'referer': 'https://www.aihr.com/blog/category/articles/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    allowed_domains = ["https://www.aihr.com"]
    start_url = """https://www.aihr.com/wp-admin/admin-ajax.php?action=alm_get_posts&query_type=standard&id=&post_id=114
    &slug=articles&canonical_url=https:%2F%2Fwww.aihr.com%2Fblog%2Fcategory%2Farticles%2F&posts_per_page=6
    &offset=0&post_type=post&repeater=template_4&seo_start_page=1&category=articles&order=DESC&orderby=date"""

    def start_requests(self):
        yield scrapy.Request(url=self.start_url+"&page=0",callback=self.parse,headers=self.headers)

    def parse(self, response):
        html = response.json()['html']
        totalNumberOfPages = int(response.json()['meta']['totalposts'] / 6)
        selector = Selector(text=html)
        urlsList = list(set(selector.xpath('//a/@href').getall()))
        for i in urlsList:
            yield response.follow(i,callback=self.ajaxRequest)

        for i in range(1,totalNumberOfPages + 1):
            yield response.follow(self.start_url+f"&page={i}")

    def ajaxRequest(self,response):
        pass

# process = CrawlerProcess()
# process.crawl(AihrSpider)
# process.start()
