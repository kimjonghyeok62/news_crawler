document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let pressData = [];
    let newsData = [];

    // --- Elements ---
    const btnFetchPress = document.getElementById('btn-fetch-press');
    const btnFetchPressToday = document.getElementById('btn-fetch-press-today');
    const btnExportPressExcel = document.getElementById('btn-export-press-excel');
    const tablePressBody = document.querySelector('#table-press tbody');
    const inputKeywords = document.getElementById('input-keywords');
    
    const btnSearchNews = document.getElementById('btn-search-news');
    const inputDays = document.getElementById('input-days');
    const progressArea = document.getElementById('progress-area');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.getElementById('progress-text');
    const resultControls = document.getElementById('result-controls');
    const tableNewsBody = document.querySelector('#table-news tbody');
    const btnExportNewsExcel = document.getElementById('btn-export-news-excel');
    const btnExportNewsWord = document.getElementById('btn-export-news-word');

    // --- Helper Functions ---
    const renderPressTable = (data) => {
        tablePressBody.innerHTML = '';
        if (data.length === 0) {
            tablePressBody.innerHTML = '<tr><td colspan="4" class="empty">데이터가 없습니다.</td></tr>';
            return;
        }
        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item.date}</td>
                <td>${item.title}</td>
                <td><span class="badge">${item.keyword_gui}</span></td>
                <td><a href="${item.link}" target="_blank">링크</a></td>
            `;
            // Add double-click event to add keyword
            tr.addEventListener('dblclick', () => {
                const currentVal = inputKeywords.value;
                const newVal = currentVal ? `${currentVal}, ${item.keyword_gui}` : item.keyword_gui;
                inputKeywords.value = newVal;
            });
            tablePressBody.appendChild(tr);
        });
    };

    const renderNewsTable = (data) => {
        tableNewsBody.innerHTML = '';
        if (data.length === 0) {
            tableNewsBody.innerHTML = '<tr><td colspan="4" class="empty">검색 결과가 없습니다.</td></tr>';
            return;
        }
        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item['보도일']}</td>
                <td>${item['보도매체']}</td>
                <td>${item['보도제목']}</td>
                <td><a href="${item['링크']}" target="_blank">보기</a></td>
            `;
            tableNewsBody.appendChild(tr);
        });
    };

    const downloadFile = async (url, data, filename) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: data })
            });
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = filename; // This might be overridden by server header
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (error) {
            alert('다운로드 실패: ' + error);
        }
    };

    // --- Event Listeners ---

    // 1. Press Releases
    const fetchPress = async (filterToday) => {
        btnFetchPress.disabled = true;
        btnFetchPressToday.disabled = true;
        tablePressBody.innerHTML = '<tr><td colspan="4" class="empty">로딩 중...</td></tr>';

        try {
            const response = await fetch('/api/crawl/press', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter_today: filterToday })
            });
            const result = await response.json();
            if (result.status === 'success') {
                pressData = result.data;
                renderPressTable(pressData);
                btnExportPressExcel.disabled = pressData.length === 0;
            } else {
                alert('오류: ' + result.message);
            }
        } catch (error) {
            alert('요청 실패: ' + error);
        } finally {
            btnFetchPress.disabled = false;
            btnFetchPressToday.disabled = false;
        }
    };

    btnFetchPress.addEventListener('click', () => fetchPress(false));
    btnFetchPressToday.addEventListener('click', () => fetchPress(true));

    btnExportPressExcel.addEventListener('click', () => {
        if (pressData.length > 0) {
            downloadFile('/api/export/excel', pressData, 'press_releases.xlsx');
        }
    });

    // 2. News Search
    btnSearchNews.addEventListener('click', async () => {
        const keywords = inputKeywords.value.split(',').map(k => k.trim()).filter(k => k);
        if (keywords.length === 0) {
            alert('검색어를 입력해주세요.');
            return;
        }

        const days = parseInt(inputDays.value) || 1;
        const sources = Array.from(document.querySelectorAll('.checkbox-group input:checked')).map(cb => cb.value);

        btnSearchNews.disabled = true;
        progressArea.classList.remove('hidden');
        resultControls.classList.add('hidden');
        tableNewsBody.innerHTML = '<tr><td colspan="4" class="empty">검색 중...</td></tr>';
        newsData = [];

        try {
            const response = await fetch('/api/crawl/news', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ keywords, days_limit: days, sources })
            });
            const result = await response.json();
            
            if (result.status === 'success') {
                const jobId = result.job_id;
                pollJobStatus(jobId);
            } else {
                alert('오류: ' + result.message);
                btnSearchNews.disabled = false;
            }
        } catch (error) {
            alert('요청 실패: ' + error);
            btnSearchNews.disabled = false;
        }
    });

    const pollJobStatus = (jobId) => {
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`/api/status/${jobId}`);
                const job = await response.json();

                progressFill.style.width = `${job.progress}%`;
                progressText.innerText = `${job.message} (${job.progress}%)`;

                if (job.status === 'completed' || job.status === 'failed') {
                    clearInterval(interval);
                    btnSearchNews.disabled = false;
                    
                    if (job.status === 'completed') {
                        newsData = job.results;
                        renderNewsTable(newsData);
                        resultControls.classList.remove('hidden');
                    } else {
                        alert('작업 실패: ' + job.message);
                    }
                }
            } catch (error) {
                clearInterval(interval);
                alert('상태 확인 실패: ' + error);
                btnSearchNews.disabled = false;
            }
        }, 1000);
    };

    btnExportNewsExcel.addEventListener('click', () => {
        if (newsData.length > 0) {
            downloadFile('/api/export/excel', newsData, 'news_results.xlsx');
        }
    });

    btnExportNewsWord.addEventListener('click', () => {
        if (newsData.length > 0) {
            downloadFile('/api/export/word', newsData, 'news_summary.docx');
        }
    });
});
