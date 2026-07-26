# darkweb_crawler

Qilin 랜섬웨어 그룹의 다크웹 유출 사이트를 자동 모니터링하는 위협 인텔리전스 크롤러

---

## Overview

Tor 네트워크를 통해 Qilin 랜섬웨어 그룹의 다크웹 리크 사이트에 접속하고, 피해 기업 정보(기업명, 유출 날짜, 업종, 국가)를 주기적으로 수집·저장하는 분산 크롤링 시스템입니다.

보안 연구 및 위협 인텔리전스 수집 목적으로 구축되었습니다.

---

## Architecture

```
Celery Beat (주기 스케줄러)
        ↓
   Redis (메시지 브로커)
        ↓
 Celery Worker × 3 (병렬 처리)
        ↓
  Tor Proxy (:49050)
        ↓
  Qilin 다크웹 사이트 (.onion)
        ↓
  Pipeline (GeoIP 조회 → DB 저장)
```

---

## Tech Stack

| 구분 | 기술 |
|---|---|
| 스크래핑 | Python, Selenium (JS 렌더링 대응) |
| 작업 스케줄링 | Celery (Worker × 3 + Beat) |
| 메시지 브로커 | Redis |
| 익명 접속 | Tor Proxy |
| 인프라 | Docker, Docker Compose |
| 데이터 보강 | GeoIP (피해 기업 국가 추적) |

---

## Project Structure

```
darkweb_crawler/
├── scrapers/
│   └── qilin_scraper.py    # Qilin 다크웹 스크래퍼 (Selenium + Tor)
├── pipeline/
│   ├── pipeline.py         # 추상 파이프라인 베이스 클래스
│   ├── database.py         # DB 저장 파이프라인
│   └── geo_ip.py           # GeoIP 조회 파이프라인
├── tasks/                  # Celery 작업 정의
├── core/                   # Tor 드라이버 팩토리 등 핵심 모듈
├── database/               # DB 연결 및 모델
├── utils/                  # 유틸리티 함수
├── geo_country_data/       # GeoIP 데이터
├── docker-compose.yml
└── requirements.txt
```

---

## Collected Data

| 필드 | 설명 |
|---|---|
| 기업명 | 유출된 피해 기업 이름 |
| 유출 날짜 | 데이터 공개 일시 |
| 업종 | 피해 기업 산업 분류 |
| 기업 URL | 피해 기업 웹사이트 |
| 국가 | GeoIP 기반 국가 정보 |

---

## Setup

### 사전 요구사항

- Docker & Docker Compose

### 환경변수 설정 (`.env`)

```env
TARGET_URL=<Qilin .onion URL>
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

### 실행

```bash
docker-compose up -d
```

Celery Worker 3개 + Beat 스케줄러가 자동으로 실행되며, 설정된 주기로 Qilin 사이트를 크롤링합니다.

---

## Disclaimer

본 프로젝트는 **보안 연구 및 위협 인텔리전스 수집 목적**으로 제작되었습니다.  
불법적인 용도로의 사용을 금지합니다.
