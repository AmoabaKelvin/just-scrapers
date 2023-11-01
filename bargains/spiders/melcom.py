import scrapy


class MelcomSpider(scrapy.Spider):
    name = "melcom"
    allowed_domains = ["melcom.com"]
    start_urls = ["https://melcom.com/categories/electronics-appliances.html"]

    def start_requests(self):
        url = "https://melcom.com/categories/electronics-appliances.html"

        self.cookies = {
            "sucuri_cloudproxy_uuid_602afc787": "746bb93c459742a66072cd0f08eadc1f",
            "PHPSESSID": "na9i8ettlutkdi7ck7q7m2dapf",
            "__zlcmid": "1IcmEsVswE4IEC5",
            "form_key": "W32xUSQYTJxkqsOe",
            "mage-cache-storage": "%7B%7D",
            "mage-cache-storage-section-invalidation": "%7B%7D",
            "mage-cache-sessid": "true",
            "searchsuiteautocomplete": "%7B%7D",
            "mage-messages": "",
            "recently_viewed_product": "%7B%7D",
            "recently_viewed_product_previous": "%7B%7D",
            "recently_compared_product": "%7B%7D",
            "recently_compared_product_previous": "%7B%7D",
            "product_data_storage": "%7B%7D",
            "section_data_ids": "%7B%22cart%22%3A1698826471%7D",
            "amp_6e403e": "GrbSqKvpyV0ybbzub0DTx-...1he4v5kgi.1he4v5kgi.0.0.0",
        }

        self.headers = {
            "authority": "melcom.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            # 'cookie': 'sucuri_cloudproxy_uuid_602afc787=746bb93c459742a66072cd0f08eadc1f; PHPSESSID=na9i8ettlutkdi7ck7q7m2dapf; __zlcmid=1IcmEsVswE4IEC5; form_key=W32xUSQYTJxkqsOe; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; searchsuiteautocomplete=%7B%7D; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; section_data_ids=%7B%22cart%22%3A1698826471%7D; amp_6e403e=GrbSqKvpyV0ybbzub0DTx-...1he4v5kgi.1he4v5kgi.0.0.0',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": "https://melcom.com/",
            "sec-ch-ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }

        yield scrapy.Request(
            url=url,
            callback=self.parse,
            headers=self.headers,
            cookies=self.cookies,
        )

    def parse(self, response):
        product_infos = response.xpath("//div[@class='product-info']")

        for product_info in product_infos:
            yield {
                "name": product_info.css("a.product-item-link::text").get().strip(),
                "link": product_info.css("a.product-item-link::attr(href)").get(),
                "price": product_info.css("span.price::text").get(),
            }

        next_page = response.css("li.pages-item-next a::attr(href)").get()
        if next_page is not None:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                headers=self.headers,
                cookies=self.cookies,
            )
