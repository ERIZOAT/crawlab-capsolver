import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Configuration
CAPSOLVER_API_KEY = os.getenv('CAPSOLVER_API_KEY', 'YOUR_CAPSOLVER_API_KEY')
CAPSOLVER_API = 'https://api.capsolver.com'

class TurnstileSolver:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def solve(self, website_url: str, site_key: str) -> str:
        task_data = {
            "clientKey": self.api_key,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteURL": website_url,
                "websiteKey": site_key
            }
        }
        response = self.session.post(f"{CAPSOLVER_API}/createTask", json=task_data)
        result = response.json()
        if result.get('errorId', 0) != 0:
            raise Exception(f"Capsolver error: {result.get('errorDescription')}")
        
        task_id = result['taskId']
        for i in range(120):
            result_data = {"clientKey": self.api_key, "taskId": task_id}
            response = self.session.post(f"{CAPSOLVER_API}/getTaskResult", json=result_data)
            result = response.json()
            if result.get('status') == 'ready':
                return result['solution']['token']
            if result.get('status') == 'failed':
                raise Exception("Turnstile solving failed")
            time.sleep(1)
        raise Exception("Timeout waiting for solution")

class TurnstileCrawler:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.solver = TurnstileSolver(CAPSOLVER_API_KEY)

    def start(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def stop(self):
        if self.driver:
            self.driver.quit()

    def detect_turnstile(self) -> str:
        try:
            turnstile = self.driver.find_element(By.CLASS_NAME, "cf-turnstile")
            return turnstile.get_attribute("data-sitekey")
        except NoSuchElementException:
            return None

    def inject_token(self, token: str):
        self.driver.execute_script(f"""
            var token = '{token}';
            var field = document.querySelector('[name="cf-turnstile-response"]');
            if (field) field.value = token;
            var inputs = document.querySelectorAll('input[name*="turnstile"]');
            for (var i = 0; i < inputs.length; i++) inputs[i].value = token;
        """)

    def crawl(self, url: str) -> dict:
        result = {'url': url, 'success': False, 'captcha_solved': False}
        try:
            self.driver.get(url)
            time.sleep(3)
            site_key = self.detect_turnstile()
            if site_key:
                token = self.solver.solve(url, site_key)
                self.inject_token(token)
                result['captcha_solved'] = True
                time.sleep(2)
            result['success'] = True
            result['title'] = self.driver.title
        except Exception as e:
            result['error'] = str(e)
        return result

if __name__ == "__main__":
    crawler = TurnstileCrawler(headless=True)
    try:
        crawler.start()
        res = crawler.crawl("https://example.com/turnstile-protected")
        print(json.dumps(res, indent=2))
    finally:
        crawler.stop()
