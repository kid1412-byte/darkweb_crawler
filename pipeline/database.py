from .pipeline import BasePipeline
from database.db import save_to_db, get_connection
from utils.date_parser import parse_leaked_date

class DatabasePipeline(BasePipeline):
    def is_duplicate(self, data_key):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id FROM victims WHERE data_key = %s"
                cursor.execute(sql, data_key)
                return cursor.fetchone() is not None
        finally:
            conn.close()
    
    def process(self, data):
        if not data:
            return None
        processed_date = parse_leaked_date(data.get('leaked_date'))
        data_key = data.get('data_key')
        if self.is_duplicate(data_key):
            return None
        
        row = (
            data_key,
            data.get('company_name'),
            processed_date,
            data.get('company_url'),
            data.get('industry'),
            data.get('country')
        )
        
        save_to_db([row])
        return data