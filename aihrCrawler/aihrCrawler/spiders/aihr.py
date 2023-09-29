import os.path

import scrapy
# from scrapy.cmdline import execute
# execute("scrapy crawl aihr".split())
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy import cmdline

# if not os.path.exists('/files'):
#     os.makedirs('/files')


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
    # allowed_domains = ["https://www.aihr.com"]
    start_url = """https://www.aihr.com/wp-admin/admin-ajax.php?action=alm_get_posts&query_type=standard&id=&post_id=114
    &slug=articles&canonical_url=https:%2F%2Fwww.aihr.com%2Fblog%2Fcategory%2Farticles%2F&posts_per_page=6
    &offset=0&post_type=post&repeater=template_4&seo_start_page=1&category=articles&order=DESC&orderby=date"""

    def start_requests(self):
        yield scrapy.Request(url=self.start_url + "&page=0", callback=self.parse, headers=self.headers)

    def parse(self, response):
        html = response.json()['html']
        totalNumberOfPages = int(response.json()['meta']['totalposts'] / 6)
        selector = Selector(text=html)
        urlsList = list(set(selector.xpath('//a/@href').getall()))
        for i in urlsList:
            yield response.follow(i, callback=self.ajax_request)

        for i in range(1, totalNumberOfPages + 1):
            yield response.follow(self.start_url + f"&page={i}")

    def ajax_request(self, response):
        text = response.text
        # all_texts = response.xpath('//*[(@id = "content")]//text()').getall()
        # all_texts_string = " ".join(all_texts)
        # all_texts_css = response.css('#content p::text').getall()
        # test_2 = response.css("#content > div.content-body > *::text").getall()
        # test_parsed = [" ".join(i.split()) for i in test_2 if not i.isspace()]
        # test_parsed_string = "\n".join(test_parsed)
        # with open('test_parsed.docx','w') as text:
        #     text.write(test_parsed_string)
        #
        # test_html = response.css("#content > div.content-body").get()
        # with open('test_html.html','w') as text:
        #     text.write(test_html)
        file_name = response.url.split('/')[-2]

        with open(f"/../../files/{file_name}.html",mode = 'w',encoding="utf-8") as f:
            f.write(text)
        # //*[contains(@class, "content-body")]//p
        ##content > div.content-body.\33 3 > *
        # yield {
        #     'text' : all_texts
        # }


# cmdline.execute("scrapy parse --spider=aihrSpider -c ajaxRequest https://www.aihr.com/blog/pto-policy/".split())

process = CrawlerProcess()
process.crawl(AihrSpider)
process.start()
