from core.celery import app
from scrapers.qilin_scraper import QilinScraper

@app.task(bind=True, max_retries=3)
def crawl_site_task(self, site_name, page_num=1):
    try:
        if site_name == 'qilin':
            scraper = QilinScraper()
            
            is_new_data = scraper.scrape_page(page_num)
            
            if is_new_data:
                crawl_site_task.delay(site_name, page_num + 1)
            else:
                print(f"[*] {site_name}: 중복 발견 또는 마지막 페이지. 크롤링 종료.")
                
    except Exception as exc:
        # 에러 발생 시 5분 뒤 재시도
        raise self.retry(exc=exc, countdown=300)