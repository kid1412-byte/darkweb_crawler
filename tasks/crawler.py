from core.celery import app
from celery import chord
from scrapers.qilin_scraper import QilinScraper
import pipeline as pipelines
from database.db import check_duplicate

def get_scraper(site_name):
    scrapers = {
        'qilin': QilinScraper,
        # 'lockbit': LockBitScraper, 
    }
    return scrapers.get(site_name)()

@app.task(bind=True, max_retries=5)
def crawl_site_task(self, site_name, page_num=1):
    try:
        scraper = get_scraper(site_name)
        result = scraper.scrape_page(page_num)
        
        if result.get('error') == 'timeout':
            raise self.retry(countdown=60)

        data_list = result.get('data', [])

        has_new_data = False
        for data in data_list:
            if not check_duplicate(data.get('data_key')):
                has_new_data = True
                save_to_db_task.delay(data)
            
        return has_new_data
               
    except Exception as e:
        raise self.retry(exc=e, countdown=300)

@app.task
def save_to_db_task(data):
    pipeline = [p() for p in pipelines.__all__]
    for pipe in pipeline:
        data = pipe.process(data)
        if data is None:
            break
        
@app.task
def start_parallel_crawl(site_name, start_page=1, batch_size=2):
    pages = list(range(start_page, start_page + batch_size))
    header = [crawl_site_task.si(site_name, p) for p in pages]
    callback = handle_batch_result.s(site_name, start_page, batch_size)
    chord(header)(callback)

@app.task
def handle_batch_result(results, site_name, start_page, batch_size):
    if any(results):
        next_page = start_page + batch_size
        print(f"[+] {site_name}: {start_page}p 배치 완료. 신규 데이터가 있어 다음 배치({next_page}p)를 시작")
        start_parallel_crawl.delay(site_name, next_page, batch_size)
    else:
        print(f"[*] {site_name}: {start_page}p 배치 내 모든 데이터 중복. 종료")

