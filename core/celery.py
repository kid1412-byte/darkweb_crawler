from celery import Celery
import os

app = Celery('darklight',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/0',
             include=['tasks.crawler'])

# 시간대 설정
app.conf.timezone = 'Asia/Seoul'

app.conf.beat_schedule = {
    'crawl-qilin-every-30min': {
        'task': 'tasks.crawler.crawl_site_task',
        'schedule': 1800.0,  # 1800초(30분)
        'args': ('qilin', 1)  # 사이트 이름과 시작 페이지
    },
}