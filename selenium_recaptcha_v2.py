import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configuration
CAPSOLVER_API_KEY = os.getenv('CAPSOLVER_API_KEY', 'YOUR_CAPSOLVER_API_KEY')
CAPSOLVER_API = 'https://api.capsolver.com'

class CapsolverClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def create_task(self, task: dict) -> str:
        payload = {
            "clientKey": self.api_key,
            "task": task
        }
        response = self.session.post(f"{CAPSOLVER_API}/createTask", json=payload)
        result = response.json()
        if result.get('errorId', 0) != 0:
            raise Exception(f"Capsolver error: {result.get('errorDescription')}")
        return result['taskId']

    def get_task_result(self, task_id: str, timeout: int = 120) -> dict:
        for _ in range(timeout):
            payload = {
                "clientKey": self.api_key,
                "taskId": task_id
            }
            response = self.session.post(f"{CAPSOLVER_API}/getTaskResult", json=payload)
            result = response.json()
            if result.get('status') == 'ready':
                return result['solution']
            if result.get('status') == 'failed':
                raise Exception("CAPTCHA solving failed")
            time.sleep(1)
        raise Exception("Timeout waiting for solution")

    def solve_recaptcha_v2(self, website_url: str, site_key: str) -> str:
        task = {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": site_key
        }
        task_id = self.create_task(task)
        solution = self.get_task_result(task_id)
        return solution['gRecaptchaResponse']

class RecaptchaV2Crawler:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.capsolver = CapsolverClient(CAPSOLVER_API_KEY)

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

    def detect_recaptcha(self) -> str:
        try:
            element = self.driver.find_element(By.CLASS_NAME, "g-recaptcha")
            return element.get_attribute("data-sitekey")
        except:
            return None

    def inject_token(self, token: str):
        self.driver.execute_script(f"""
            var responseField = document.getElementById('g-recaptcha-response');
            if (responseField) {{
                responseField.style.display = 'block';
                responseField.value = '{token}';
            }}
            var textareas = document.querySelectorAll('textarea[name="g-recaptcha-response"]');
            for (var i = 0; i < textareas.length; i++) {{
                textareas[i].value = '{token}';
            }}
        """)

    def crawl(self, url: str) -> dict:
        result = {'url': url, 'success': False, 'captcha_solved': False}
        try:
            self.driver.get(url)
            time.sleep(2)
            site_key = self.detect_recaptcha()
            if site_key:
                token = self.capsolver.solve_recaptcha_v2(url, site_key)
                self.inject_token(token)
                result['captcha_solved'] = True
                time.sleep(2)
            result['success'] = True
            result['title'] = self.driver.title
        except Exception as e:
            result['error'] = str(e)
        return result

if __name__ == "__main__":
    crawler = RecaptchaV2Crawler(headless=True)
    try:
        crawler.start()
        res = crawler.crawl("https://example.com/protected-page")
        print(json.dumps(res, indent=2))
    finally:
        crawler.stop()
