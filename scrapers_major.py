from scrapers_common import *

# --- 기호일보 (Kiho Ilbo) ---
def fetch_kiho_multi(keywords, date_limit, days_limit):
    ARTICLE_LIST_SELECTOR = "li.altlist-text-item"
    TITLE_SELECTOR = "h2.altlist-subject a"
    DATE_SELECTOR = "div.altlist-info div.altlist-info-item"
    IS_DATE_IN_LIST = True 
    DATE_INDEX = 2 
    source_name = "기호일보"
    
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    
    try:
        for keyword in keywords:
            url = f"https://www.kihoilbo.co.kr/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ARTICLE_LIST_SELECTOR)))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select(ARTICLE_LIST_SELECTOR)
                found_count = 0
                for item in articles:
                    try:
                        title_tag = item.select_one(TITLE_SELECTOR)
                        if not title_tag: continue 
                        title = title_tag.get_text(strip=True)
                        link = title_tag["href"]
                        if not link.startswith("http"): link = urljoin("https://www.kihoilbo.co.kr", link) 
                        
                        date_str_raw = "" 
                        if IS_DATE_IN_LIST:
                            info_items = item.select(DATE_SELECTOR)
                            if len(info_items) > DATE_INDEX: date_str_raw = info_items[DATE_INDEX].get_text(strip=True) 
                        else:
                            date_tag = item.select_one(DATE_SELECTOR)
                            if date_tag: date_str_raw = date_tag.get_text(strip=True)
                        
                        if not date_str_raw: continue 
                        date_str = date_str_raw.split(" ")[0] 
                        
                        if re.match(r"^\d{4}\.\d{2}\.\d{2}$", date_str): date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                        elif re.match(r"^\d{4}-\d{2}-\d{2}$", date_str): date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        else: continue
                        
                        if date_obj >= date_limit:
                            results.append({"보도일": date_obj.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0:
                    results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException:
                results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 인천일보 (Incheon Ilbo) ---
def fetch_incheonilbo_multi(keywords, date_limit, days_limit):
    source_name = "인천일보"
    base_url = "https://www.incheonilbo.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"https://www.incheonilbo.com/news/articleList.html?sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.type1 > li")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("ul.type1 > li")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("h2.titles")
                        link_tag = article.select_one("a")
                        if not title_tag or not link_tag: continue
                        title = title_tag.text.strip()
                        link = urljoin(base_url, link_tag["href"])
                        date_str_tag = article.select_one("em.info.dated")
                        pub_date = None
                        if date_str_tag:
                            date_text = date_str_tag.text.strip()
                            try: pub_date = datetime.strptime(date_text.split(" ")[0], "%Y.%m.%d")
                            except ValueError:
                                if "분 전" in date_text: pub_date = datetime.now() - timedelta(minutes=int(re.search(r'(\d+)', date_text).group(1)))
                                elif "시간 전" in date_text: pub_date = datetime.now() - timedelta(hours=int(re.search(r'(\d+)', date_text).group(1)))
                        if pub_date and pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 경기일보 (Kyeonggi Ilbo) ---
def fetch_kyeonggi_multi(keywords, date_limit, days_limit):
    source_name = "경기일보"
    base_url = "https://www.kyeonggi.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"https://www.kyeonggi.com/search?searchText={quote(keyword)}"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.article_list div.media")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.article_list div.media")
                found_count = 0
                for article in articles: 
                    try:
                        title_tag = article.select_one("h3 a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag.get("href", "")) 
                        date_tag = article.select_one("span.byline") 
                        if not date_tag: continue
                        date_text_raw = date_tag.get_text() 
                        date_match = re.search(r"(\d{4}\.\d{2}\.\d{2})", date_text_raw)
                        if date_match: date_str = date_match.group(1).replace(".", "-")
                        else: continue
                        pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 경인일보 (Kyeongin Ilbo) ---
def fetch_kyeongin_multi(keywords, date_limit, days_limit):
    source_name = "경인일보"
    base_url = "https://www.kyeongin.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"https://www.kyeongin.com/search?query={quote(keyword)}"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-arl-001 ul li")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.search-arl-001 ul li")
                found_count = 0
                for item in articles:
                    try:
                        a_tag = item.select_one("h4.title a")
                        if not a_tag: continue
                        title = a_tag.get_text(strip=True)
                        href = a_tag["href"]
                        link = "https:" + href if href.startswith("//") else urljoin(base_url, href)
                        date_tag = item.select_one("span.date") 
                        if not date_tag: continue
                        pub_date = datetime.strptime(date_tag.get_text(strip=True), "%Y-%m-%d")
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 경기신문 (KG News) ---
def fetch_kgnews_multi(keywords, date_limit, days_limit):
    source_name = "경기신문"
    base_url = "https://www.kgnews.co.kr"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"https://www.kgnews.co.kr/news/search_result.html?search_mode=multi&s_title=1&s_sub_title=1&s_body=1&search={quote(keyword)}"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.art_list_all > li")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("ul.art_list_all > li")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("h2.clamp.c2")
                        link_tag = article.select_one("a")
                        info_tag = article.select_one("ul.ffd.art_info")
                        if not title_tag or not link_tag or not info_tag: continue
                        title = title_tag.text.strip()
                        link = urljoin(base_url, link_tag["href"]) 
                        date_match = re.search(r"\d{4}\.\d{2}\.\d{2}", info_tag.text)
                        if not date_match: continue
                        pub_date = datetime.strptime(date_match.group(), "%Y.%m.%d")
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results

# --- 중부일보 (Joongbu Ilbo) ---
def fetch_joongbu_multi(keywords, date_limit, days_limit):
    source_name = "중부일보"
    base_url = "https://www.joongboo.com"
    driver = setup_driver(headless=True)
    if not driver: return []
    results = []
    try:
        for keyword in keywords:
            url = f"https://www.joongboo.com/news/articleList.html?sc_area=A&sc_word={quote(keyword)}&sc_order_by=E"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-content")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                articles = soup.select("div.list-content")
                found_count = 0
                for article in articles:
                    try:
                        title_tag = article.select_one("h4.titles a")
                        if not title_tag: continue
                        title = title_tag.get_text(strip=True)
                        link = urljoin(base_url, title_tag["href"])
                        date_elements = article.select("span.byline em")
                        if len(date_elements) < 2: continue
                        date_str = date_elements[1].text.strip().split(" ")[0]
                        pub_date = datetime.strptime(date_str, "%Y.%m.%d")
                        if pub_date >= date_limit:
                            results.append({"보도일": pub_date.strftime("%Y-%m-%d"), "보도매체": source_name, "보도제목": title, "링크": link, "검색어": keyword})
                            found_count += 1
                    except Exception: continue
                if found_count == 0: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
            except TimeoutException: results.append({"보도일": "없음", "보도매체": source_name, "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.", "링크": url, "검색어": keyword})
    except Exception as e: print(f"[{source_name}] Error: {e}")
    finally: driver.quit()
    return results
