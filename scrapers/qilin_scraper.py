from core.browser import TorBrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pipeline as pipelines

class QilinScraper:
    def __init__(self):
        self.browser_factory = TorBrowser()
        self.base_url = os.getenv("BASE_URL")
        self.pipelines = [p() for p in pipelines.__all__]
    
    def _wait_content(self, driver):
        try:
            wait = WebDriverWait(driver, 90)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "item_box")))
            return True
        except:
            return False
    
    def _extract_data(self, item):
        parent_div = item.find_element(By.XPATH, "./..") 
        data_key = parent_div.get_attribute("data-key")
        # 기업명
        company_name = item.find_element(By.CLASS_NAME, "item_box-title").text.strip()
        # 게시 날짜
        info_elements = item.find_elements(By.CLASS_NAME, "item_box-info__item")
        date = next((el.text.strip() for el in info_elements if "202" in el.text), "N/A")
        # 산업
        industry = item.find_element(By.TAG_NAME, "p").text.strip()
        if not industry or industry == "0":
            industry = "Unknown"
        # 회사 URL
        company_url = item.find_element(By.CLASS_NAME, "item_box-info__link").get_attribute("href")
        return {
            "data_key": data_key,
            "company_name": company_name,
            "leaked_date": date,
            "company_url": company_url,
            "industry": industry,
            "country": None
        }

    def scrape_page(self, page_num):
        driver = self.browser_factory.get_driver()
        try:
            target_url = f"{self.base_url}?page={page_num}"
            driver.get(target_url)
            
            if not self._wait_content(driver):
                return {"data": [], "error": "timeout"}
            
            items = driver.find_elements(By.CLASS_NAME, "item_box")
            data = [self._extract_data(item) for item in items]
            
            return {"data": data, "count": len(data)}
        finally:
            driver.quit()