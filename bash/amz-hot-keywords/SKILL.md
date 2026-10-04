---
name: amz-hot-keywords
description: 从 AMZ123 抓取亚马逊品牌分析（ABA）周热搜词排名数据，输出包含关键词、本周排名、上周排名及趋势（上升/下降/持平）的结构化 CSV 文件，快速掌握搜索热度变化。
title: 热词抓取
example: |-
  抓取关键词"sneakers"的相关热搜词及其排名趋势，保存为 CSV 文件：

  ```bash
  python3 scripts/amz_scraper.py --keyword "sneakers" --max-results 200 --output-dir ./data
  ```

  运行后将生成类似 `amz123_hotwords_sneakers_20250410_153022.csv` 的文件，包含搜索词、本周排名、上周排名和趋势方向，便于分析市场热度变化。
version: 2.0.2
---
# Amazon Hot Keywords Scraper

Scrape ABA weekly search term rankings from AMZ123 for any keyword. Outputs structured CSV data with search term, current week rank, last week rank, and trend direction.

## How It Works

AMZ123 is now a **Nuxt.js SPA** (since ~2025). The scraper uses the BrowserWorker daemon + Chrome extension plugin transport to:

1. Navigate to AMZ123's US top keywords page with keyword search
2. Wait 20s for Nuxt SSR + async API data to populate `window.__NUXT__`
3. Scroll to trigger virtual-scroll table rendering
4. Extract rendered DOM rows inside the real browser through `browser.evaluate(...)`
5. Fall back to `document.body.innerText` + Python regex when DOM row extraction fails
6. Calculate trend (up/down/flat/new) and save as timestamped CSV

The skill must not use the old Chrome/CDP attach flow. Browser control goes through BrowserWorker `/execute` with `action_search_path=<skill>/scripts/actions`.

## Usage

Run the scraper script with the target keyword:

```bash
python <SKILL_DIR>/scripts/amz_scraper.py --keyword "women shoes"
```

### Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--keyword` | Yes | Search keyword (**MUST be English** for US site) | `--keyword "women shoes"` |
| `--max-results` | No | Max results to scrape (default: 200) | `--max-results 100` |
| `--output-dir` | No | Output directory for CSV (default: current dir) | `--output-dir ./data` |

### Output

The script produces a CSV file named `amz123_hotwords_<keyword>_<timestamp>.csv`:

| Column | Description |
|--------|-------------|
| search_term | The keyword/search term |
| current_rank | This week's ranking position |
| last_rank | Last week's ranking position |
| trend | Calculated direction: up / down / flat / new |

Trend logic: rank number decreasing = rising popularity ("up"), rank number increasing = falling popularity ("down"), same = "flat", no previous rank = "new".

## Pitfalls & Troubleshooting

### 1. Chinese Keywords Return 0 Results
**Chinese keywords on the US site always return 0 results.** AMZ123 US scrapes Amazon.com (English marketplace). Always convert to English:

| Chinese | English |
|---------|---------|
| 女鞋 | women shoes |
| 运动鞋 | sneakers |
| 瑜伽垫 | yoga mat |
| 手机壳 | phone case |

### 2. BrowserWorker HTTP Unavailable
The script uses Python stdlib `urllib` to POST to BrowserWorker `/execute`. Port discovery order:

1. `BrowserWorker_PORT`
2. `MANAI_BROWSER_CONTROL_PORT`
3. `BrowserWorker_LOCK_FILE`
4. `MANAI_WORKSPACE_ROOT/MANAI_HOME` + `storage/browser_daemon.lock`
5. legacy `~/.BrowserWorker/BrowserWorker.lock`
6. default `12321`

If the daemon is down, the script attempts to start project-local `BrowserWorker` with `--transport auto`. Do not switch to CDP or direct Chrome control unless the user explicitly asks for CDP debugging.

### 3. Table Not Rendering (Timeout)
AMZ123 uses Nuxt.js with virtual scrolling. The table only renders after:
- API data loads into `window.__NUXT__.state`
- User scrolls (IntersectionObserver triggers render)

The current approach handles this with: **20s wait → scroll 800px → 3s wait → extract innerText**. If this fails, increase wait time or try the Nuxt state extraction method below.

### 4. Nuxt State Extraction (Alternative)
When text extraction fails, extract directly from Nuxt SSR state in the browser:

```js
const nuxt = window.__NUXT__;
const keys = Object.keys(nuxt.state).filter(k => k.includes('word'));
const data = nuxt.state[keys[0]]; // Contains { rows: [...], total: N }
```

### Runtime Requirements

- Python 3.9+
- Project-local BrowserWorker daemon and extension
- No Playwright, Selenium, ChromeDriver, pandas, or beautifulsoup4 dependency is required by this skill

## Data Source

[AMZ123 US Top Keywords](https://www.amz123.com/usatopkeywords) - sourced from Amazon Brand Analytics (ABA) weekly reports covering ~250,000 search terms.
