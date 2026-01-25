from datetime import datetime

def parse_leaked_date(raw_date_str):
    if not raw_date_str or raw_date_str == "N/A":
        return None
        
    try:
        date = datetime.strptime(raw_date_str.strip(), "%b %d, %Y")
        return date.date()
    except Exception as e:
        print(f"[!] 날짜 파싱 에러 ({raw_date_str}): {e}")
        return None