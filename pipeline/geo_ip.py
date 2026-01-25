from .pipeline import BasePipeline
from utils.get_country import get_country

class GeoIPPipeline(BasePipeline):
    def process(self, data):
        #print(f"[*] 국가 정보 추출 중: {data['company_name']}")
        data['country'] = get_country(data['company_name'], data['company_url'])
        return data