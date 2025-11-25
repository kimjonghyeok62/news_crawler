from scrapers_common import *

# --- 경기핫타임스 (Gyeonggi Hot Times) ---
def fetch_ght_multi(keywords, date_limit, days_limit):
    source_name = "경기핫타임스"
    base_url = "http://www.ghtimes.kr"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.ghtimes.kr/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 하남타임즈 (Hanam Times) ---
def fetch_hanamtimes_multi(keywords, date_limit, days_limit):
    source_name = "하남타임즈"
    base_url = "http://www.hanamtimes.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.hanamtimes.com/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 시티뉴스 (City News) ---
def fetch_citynews_multi(keywords, date_limit, days_limit):
    source_name = "시티뉴스"
    base_url = "http://www.ctnews.co.kr"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.ctnews.co.kr/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 광주뉴스 (Gwangju News) ---
def fetch_gjnews_multi(keywords, date_limit, days_limit):
    source_name = "광주뉴스"
    base_url = "http://www.gjnews.net"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.gjnews.net/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 하남신문 (Hanam News) ---
def fetch_hanamnews_multi(keywords, date_limit, days_limit):
    source_name = "하남신문"
    base_url = "http://www.ehanam.net"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.ehanam.net/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 하남경제 (Hanam Economy) ---
def fetch_hanameconomy_multi(keywords, date_limit, days_limit):
    source_name = "하남경제"
    base_url = "http://www.hanameconomy.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.hanameconomy.com/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 미사뉴스 (Misa News) ---
def fetch_misanews_multi(keywords, date_limit, days_limit):
    source_name = "미사뉴스"
    base_url = "http://www.misanews.net"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.misanews.net/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 하남일보 (Hanam Ilbo) ---
def fetch_hanamilbo_multi(keywords, date_limit, days_limit):
    source_name = "하남일보"
    base_url = "http://www.hanamilbo.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.hanamilbo.com/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 하남정론 (Hanam Jungron) ---
def fetch_hanamjungron_multi(keywords, date_limit, days_limit):
    source_name = "하남정론"
    base_url = "http://www.hnjr.co.kr"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.hnjr.co.kr/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 광주in (Gwangju In) ---
def fetch_gwangjuin_multi(keywords, date_limit, days_limit):
    source_name = "광주in"
    base_url = "http://www.gwangjuin.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"http://www.gwangjuin.com/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-block")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-block")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("div.list-titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_tag = article.select_one("div.list-dated")
                        if not date_tag: continue
                        date_str_raw = date_tag.get_text(strip=True)
                        date_str = date_str_raw.split(" ")[-1]
                        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results
