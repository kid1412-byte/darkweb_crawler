import pycountry
import socket
import geoip2.database
import re
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH")

geolocator = Nominatim(user_agent="my_darkweb_crawler_v1")

def get_country(company_name, company_url):
    if company_url and "http" in company_url:
        country = get_country_by_ip(company_url)
        if country:
            return country

    return get_country_by_name(company_name)

def get_country_by_ip(url):
    try:
        # URL에서 도메인만 추출
        clean_url = re.sub(r'^https?://', '', url).split('/')[0]
        ip_addr = socket.gethostbyname(clean_url)
        
        with geoip2.database.Reader(DB_PATH) as reader:
            response = reader.country(ip_addr)
            country_code = response.country.iso_code
            
            country = pycountry.countries.get(alpha_2=country_code)
            return country.name if country else country_code
    except Exception as e:
        return None

def get_country_by_name(company_name):
    clean_name = re.sub(r'(?i)www\.', '', company_name)
    clean_name = re.sub(r'(?i)\.(com|net|org|edu|gov|at|ca|us|biz|info|io|co\.kr|kr|me|tv)', '', clean_name)
    clean_name = clean_name.replace('.', ' ').strip()
    try:
        location = geolocator.geocode(clean_name, language='en', timeout=10)
        if location:
            country = location.address.split(',')[-1].strip()
            return country
        return "Unknown"
    except:
        return "Unknown"