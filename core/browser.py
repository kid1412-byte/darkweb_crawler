from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class TorBrowser:
    def __init__(self):
        self.proxy = os.getenv("PROXY_SERVER")

    def get_driver(self):
        options = Options()
        options.add_argument(f'--proxy-server={self.proxy}')
        
        # 다크웹 크롤링 안정성을 위한 추가 옵션
        options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(options=options)