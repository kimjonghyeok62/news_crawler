from scrapers_common import *
import feedparser

def shorten_google_url(url):
    if "google.com/url?" in url:
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            if 'url' in query_params:
                return query_params['url'][0]
        except Exception:
            return url
    return url

def fetch_google_news_feed(keywords, date_limit, days_limit, progress_callback=None):
    source_name = "Google뉴스"
    results = []
    found_for_keyword = {keyword: False for keyword in keywords}
    driver = None
    
    print(f"[GoogleNews] Starting fetch for {keywords}")
    if progress_callback: progress_callback(0, "Google News: Initializing driver...")

    try:
        driver = setup_driver_compatible(headless=True)
        print("[GoogleNews] Driver initialized")
    except Exception as e:
        print(f"[GoogleNews] Driver init failed: {e}")
        pass

    total_keywords = len(keywords)
    for k_idx, keyword in enumerate(keywords):
        if progress_callback: 
            progress_callback(int((k_idx / total_keywords) * 100), f"Google News: Searching '{keyword}'...")
            
        search_keyword = keyword
        if keyword == "광주하남":
            search_keyword = "광주하남교육지원청"
        
        query = f'"{search_keyword}"'
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_limit)
        query += f" after:{start_date.strftime('%Y-%m-%d')} before:{end_date.strftime('%Y-%m-%d')}"

        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        print(f"[GoogleNews] Fetching RSS: {url}")

        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                print(f"[GoogleNews] No entries for {keyword}")
                continue

            total_entries = len(feed.entries)
            print(f"[GoogleNews] Found {total_entries} entries for {keyword}")
            
            for e_idx, entry in enumerate(feed.entries):
                # Update progress within the keyword loop too if it's taking long
                if progress_callback and e_idx % 5 == 0:
                     current_progress = int((k_idx / total_keywords) * 100) + int((e_idx / total_entries) * (100 / total_keywords))
                     progress_callback(current_progress, f"Google News: Processing '{keyword}' ({e_idx+1}/{total_entries})...")

                try:
                    pub_date_parsed = entry.get("published_parsed")
                    if not pub_date_parsed: continue
                    
                    pub_date = datetime.fromtimestamp(time.mktime(pub_date_parsed))
                    if pub_date < date_limit: continue

                    title = entry.title
                    original_link = entry.link
                    final_link = original_link

                    if driver and "news.google.com/rss/articles/" in original_link:
                        try:
                            driver.set_page_load_timeout(15)
                            driver.get(original_link)
                            WebDriverWait(driver, 10).until(
                                lambda d: d.current_url != original_link and "google.com" not in d.current_url
                            )
                            final_link = driver.current_url
                        except Exception as e:
                            print(f"[GoogleNews] Redirect resolution failed: {e}")
                            final_link = original_link
                    else:
                        final_link = shorten_google_url(original_link)

                    results.append({
                        "보도일": pub_date.strftime("%Y-%m-%d"),
                        "보도매체": source_name,
                        "보도제목": title,
                        "링크": final_link,
                        "검색어": keyword
                    })
                    found_for_keyword[keyword] = True

                except Exception as e:
                    print(f"[GoogleNews] Entry error: {e}")
                    continue
        except Exception as e:
            print(f"[GoogleNews] Feed error: {e}")
            continue

    if driver:
        driver.quit()

    for keyword, found in found_for_keyword.items():
        if not found:
            results.append({
                "보도일": "없음",
                "보도매체": source_name,
                "보도제목": f"최근 {days_limit}일 이내 '{keyword}' 관련 기사가 없습니다.",
                "링크": "",
                "검색어": keyword
            })
            
    print(f"[GoogleNews] Finished. Found {len(results)} results.")
    return results
