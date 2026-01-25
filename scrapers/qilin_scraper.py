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
            #target_url = "http://localhost:8000/index.html"
            print(f"[*] 접속 중: {target_url}")
            driver.get(target_url)
            
            # 다크웹 로딩 대기
            if not self._wait_content(driver):
                print(f"[!] {page_num}페이지 로딩 타임아웃 (내용을 찾을 수 없음)")
                return False
            
            items = driver.find_elements(By.CLASS_NAME, "item_box")
            if not items:
                print(f"[-] {page_num}페이지에 게시글이 없습니다.")
                return False
            print(f"[+] 성공! {page_num}페이지에서 {len(items)}개의 게시글 발견")
            
            for item in items:
                data = self._extract_data(item)
                #print(f"   - 발견된 기업: {data['company_name']}")
                for pipe in self.pipelines:
                    data = pipe.process(data)
                    if data is None:
                        return False
                            
                #print(data)
            return True
                    
        except Exception as e:
            return False
        finally:
            driver.quit()