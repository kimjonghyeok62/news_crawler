import time
import re
import pandas as pd
import traceback
from datetime import datetime, timedelta
from urllib.parse import quote, urlencode, urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import os
import sys
import requests
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import uuid

# Import scrapers
from scrapers_common import *
from scrapers_major import *
from scrapers_minor import *
from scrapers_google import *

# --- Helper Functions ---

def extract_keyword(title):
    try:
        specific_schools = ["한사랑학교", "성광학교", "광주새롬학교", "동현학교", "인덕학교"]
        for school in specific_schools:
            if school in title:
                return school
        if "광주하남교육지원청" in title:
            return "광주하남교육"
        
        match = re.search(r'\b([\w]+(초|중|고|유|병설유|초병설유|병설유치원|초등학교|중학교|고등학교|유치원))\b', title)
        if match:
            return match.group(1)
        
        first_part = title.split(',')[0].strip()
        first_word = first_part.split(' ')[0].strip()
        if len(first_word) > 10:
            return first_word[:10]
        return first_word
    except Exception:
        return title[:5]

def extract_institution(title):
    try:
        specific_schools = ["한사랑학교", "성광학교", "광주새롬학교", "동현학교", "인덕학교"]
        for school in specific_schools:
            if school in title:
                return school 
        if "광주하남교육지원청" in title:
            return "광주하남교육"
        match = re.search(r'\b([\w]+(초|중|고|유|병설유|초병설유|병설유치원|초등학교|중학교|고등학교|유치원))\b', title)
        if match:
            return match.group(1)
        first_part = title.split(',')[0].strip()
        first_word = first_part.split(' ')[0].strip()
        return first_word[:10] if len(first_word) > 10 else first_word
    except Exception:
        return title[:5]

def scrape_press_releases(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    session.mount("https://", LegacyTLSAdapter())
    session.mount("http://", LegacyTLSAdapter())
    results_list = []

    try:
        page_url = f"{base_url}&pageIndex=1"
        response = session.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('a.selectNttInfo')

        if not articles:
            return []

        for article in articles:
            original_title = article.get('title', '제목 없음').strip()
            
            date_tag = article.find('span', class_='date')
            date_str_raw = date_tag.get_text(strip=True) if date_tag else '날짜 없음'
            date = "날짜없음"
            
            date_match = re.search(r"(\d{4}\.\d{2}\.\d{2})", date_str_raw)
            if date_match:
                date = date_match.group(0)
            else:
                continue

            nttSn = article.get('data-param') 
            link = "링크 추출 실패" 
            if nttSn and nttSn.isdigit():
                link = f"https://www.goegh.kr/goegh/na/ntt/selectNttInfo.do?mi=8686&bbsId=5041&nttSn={nttSn}"

            clean_title = original_title 
            title_match = re.search(r'^보도자료\((.*)\)$', original_title)
            if title_match:
                clean_title = title_match.group(1).strip() 
            
            region = "교육지원청"
            if clean_title.startswith("광주 "): region = "광주"
            elif clean_title.startswith("하남 "): region = "하남"
            elif "광주하남" in clean_title: region = "교육지원청"

            institution = extract_institution(clean_title)
            keyword_gui = extract_keyword(clean_title) 
            
            results_list.append({
                "priority": "",
                "region": region,
                "date": date,
                "time": datetime.now().strftime('%H:%M'),
                "title": clean_title,
                "institution": institution,
                "keyword_gui": keyword_gui,
                "link": link, 
                "notes": ""
            })
        
        return results_list

    except Exception as e:
        print(f"Error scraping press releases: {e}")
        return []

# --- Job Manager ---

class JobManager:
    def __init__(self):
        self.jobs = {}
        self.lock = threading.Lock()

    def create_job(self):
        job_id = str(uuid.uuid4())
        with self.lock:
            self.jobs[job_id] = {
                "status": "running",
                "progress": 0,
                "message": "Starting...",
                "results": [],
                "created_at": datetime.now()
            }
        return job_id

    def update_job(self, job_id, status=None, progress=None, message=None, results=None):
        with self.lock:
            if job_id in self.jobs:
                if status: self.jobs[job_id]["status"] = status
                if progress is not None: self.jobs[job_id]["progress"] = progress
                if message: self.jobs[job_id]["message"] = message
                if results is not None: self.jobs[job_id]["results"] = results

    def get_job(self, job_id):
        with self.lock:
            return self.jobs.get(job_id)

job_manager = JobManager()

def run_crawler_task(job_id, keywords, days_limit, sources):
    try:
        job_manager.update_job(job_id, message="Initializing crawler...", progress=5)
        
        today = datetime.today()
        date_limit = (today - timedelta(days=days_limit)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        all_results = []
        tasks = []
        
        # 1. Google News
        if "google" in sources:
             def google_progress(p, msg):
                 # Map 0-100 progress of Google News to 10-90 of total job
                 # But since we have other tasks, we should be careful.
                 # For now, let's just update the message and keep progress dynamic if it's the only task.
                 # If multiple tasks, this might be noisy, but better than stuck.
                 job_manager.update_job(job_id, message=msg)
                 
             tasks.append(lambda: fetch_google_news_feed(keywords, date_limit, days_limit, progress_callback=google_progress))

        # 2. Major 6
        if "major6" in sources:
            tasks.append(lambda: fetch_kiho_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_incheonilbo_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_kyeonggi_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_kyeongin_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_kgnews_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_joongbu_multi(keywords, date_limit, days_limit))

        # 3. Other 16 (Partial list implemented in scrapers_minor.py)
        if "other16" in sources:
            tasks.append(lambda: fetch_ght_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_hanamtimes_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_citynews_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_gjnews_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_hanamnews_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_hanameconomy_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_misanews_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_hanamilbo_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_hanamjungron_multi(keywords, date_limit, days_limit))
            tasks.append(lambda: fetch_gwangjuin_multi(keywords, date_limit, days_limit))
            # Add more if implemented...
        
        total_tasks = len(tasks)
        completed_tasks = 0
        
        # Use fewer workers to avoid overwhelming the system/network
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(task) for task in tasks]
            
            for future in as_completed(futures):
                try:
                    res = future.result()
                    all_results.extend(res)
                except Exception as e:
                    print(f"Task error: {e}")
                
                completed_tasks += 1
                progress = 10 + int((completed_tasks / total_tasks) * 80)
                job_manager.update_job(job_id, progress=progress, message=f"Processed {completed_tasks}/{total_tasks} sources")

        # Sort results
        df = pd.DataFrame(all_results)
        if not df.empty and '보도제목' in df.columns:
             def clean_date(d):
                 try:
                     return pd.to_datetime(d)
                 except:
                     return pd.Timestamp.min
             
             df['date_dt'] = df['보도일'].apply(clean_date)
             df = df.sort_values(by=['보도제목', 'date_dt', '보도매체'], ascending=[True, False, True])
             all_results = df.drop(columns=['date_dt']).to_dict('records')

        job_manager.update_job(job_id, status="completed", progress=100, message="Done", results=all_results)

    except Exception as e:
        traceback.print_exc()
        job_manager.update_job(job_id, status="failed", message=str(e))
