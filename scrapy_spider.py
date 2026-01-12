import scrapy
import requests
import time
import os

CAPSOLVER_API_KEY = os.getenv('CAPSOLVER_API_KEY', 'YOUR_CAPSOLVER_API_KEY')
CAPSOLVER_API = 'https://api.capsolver.com'

class CapsolverMiddleware:
    def __init__(self):
        self.api_key = CAPSOLVER_API_KEY

    def solve_recaptcha_v2(self, url: str, site_key: str) -> str:
        response = requests.post(
            f"{CAPSOLVER_API}/createTask",
            json={
                "clientKey": self.api_key,
                "task": {
                    "type": "ReCaptchaV2TaskProxyLess",
                    "websiteURL": url,
                    "websiteKey": site_key
                }
            }
        )
        task_id = response.json()['taskId']
        for _ in range(120):
            result = requests.post(
                f"{CAPSOLVER_API}/getTaskResult",
                json={"clientKey": self.api_key, "taskId": task_id}
            ).json()
            if result.get('status') == 'ready':
                return result['solution']['gRecaptchaResponse']
            time.sleep(1)
        raise Exception("Timeout")

class CaptchaSpider(scrapy.Spider):
    name = "captcha_spider"
    start_urls = ["https://example.com/protected"]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capsolver = CapsolverMiddleware()

    def parse(self, response):
        site_key = response.css('.g-recaptcha::attr(data-sitekey)').get()
        if site_key:
            token = self.capsolver.solve_recaptcha_v2(response.url, site_key)
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'g-recaptcha-response': token},
                callback=self.after_captcha
            )
        else:
            yield from self.extract_data(response)

    def after_captcha(self, response):
        yield from self.extract_data(response)

    def extract_data(self, response):
        yield {
            'title': response.css('title::text').get(),
            'url': response.url,
        }
