from .pipeline import BasePipeline
from database.db import save_to_db, check_duplicate
from utils.date_parser import parse_leaked_date

class DatabasePipeline(BasePipeline):    
    def process(self, data):
        if not data:
            return None
        processed_date = parse_leaked_date(data.get('leaked_date'))
        data_key = data.get('data_key')
        if check_duplicate(data_key):
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