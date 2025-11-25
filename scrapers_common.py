import time
import re
import ssl
from datetime import datetime, timedelta
from urllib.parse import quote, urlencode, urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from functools import lru_cache

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class LegacyTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        try:
            context.set_ciphers('DEFAULT@SECLEVEL=1')
        except ssl.SSLError:
            print("Warning: Failed to set ciphers 'DEFAULT@SECLEVEL=1'. Using default.")
        kwargs['ssl_context'] = context
        return super(LegacyTLSAdapter, self).init_poolmanager(*args, **kwargs)

@lru_cache(maxsize=1)
def get_driver_path():
    try:
        return ChromeDriverManager().install()
    except Exception as e:
        print(f"WebDriverManager Error: {e}")
        return "chromedriver"

def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.cookies": 2,
        "profile.managed_default_content_settings.javascript": 1,
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.notifications": 2,
        "profile.managed_default_content_settings.media_stream": 2,
    }
    options.add_experimental_option("prefs", prefs)
    
    try:
        service = Service(get_driver_path()) 
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Driver Start Error: {e}")
        return None

def setup_driver_compatible(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    try:
        service = Service(get_driver_path()) 
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Compatible Driver Start Error: {e}")
        return None
