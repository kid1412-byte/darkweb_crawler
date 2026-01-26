from celery import Celery
import os

app = Celery('darklight',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/0',
             include=['tasks.crawler'])

# 시간대 설정
app.conf.timezone = 'Asia/Seoul'

app.conf.beat_schedule = {
    'crawl-qilin-parallel-every-30min': {
        'task': 'tasks.crawler.start_parallel_crawl', 
        'schedule': 1800.0,
        'args': ('qilin', 1, 2) 
    },
}