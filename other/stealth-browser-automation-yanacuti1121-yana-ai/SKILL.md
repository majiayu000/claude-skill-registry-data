---
name: stealth-browser-automation
description: "Use when asked to scrape a bot-protected website, bypass anti-bot detection, run Playwright with stealth patches, automate a site that blocks normal browsers, or simulate human-like browser behavior. Triggers on: 'scrape protected site', 'bypass bot detection', 'stealth playwright', 'anti-bot browser', 'cloudflare bypass', 'captcha avoidance', 'humanized browser', 'fingerprint evasion', 'botasaurus', 'python scraper', 'scraper ui', 'parallel scraping', 'trình duyệt chống phát hiện', 'vượt qua bot detection', 'cào dữ liệu trang bảo vệ'."
---

# Stealth Browser Automation Skill
# Source: CloakHQ/CloakBrowser (MIT) — stealth Chromium pattern adapted for YAMTAM
# Tier: TIER 3 — PRODUCTIVITY

Hướng dẫn automation trên các website có anti-bot protection.
Pattern từ CloakBrowser: stealth Chromium + Playwright drop-in + humanized behavior.

**QUAN TRỌNG — ĐẠO ĐỨC:** Chỉ dùng cho web scraping được phép (own data, public data, authorized testing). Không dùng để bypass auth, spam, hoặc scrape dữ liệu riêng tư mà không được phép.

## Khi nào dùng

- Crawl trang web có Cloudflare, Datadome, PerimeterX
- Test automation trên sites có bot detection
- Nghiên cứu fingerprinting và evasion techniques
- Screenshot/capture trang web protected

**Do NOT use for:** bypass authentication, unauthorized data collection, DDOS, spam.

---

## Core Concepts (từ CloakBrowser)

CloakBrowser là Chromium với 58+ C++ patches để erase browser automation markers:

```
Bị detect vì:                    Fix của CloakBrowser:
──────────────────────────────────────────────────────
navigator.webdriver = true    → patch to false/undefined
CDP protocol visible          → hide Chrome DevTools Protocol
Canvas fingerprint unique     → randomize canvas noise
WebGL renderer reveals VM     → spoof GPU renderer string
AudioContext fingerprint      → add slight noise
Headless mode tells           → patch UA + screen size
Mouse moves robotic           → Bezier curve humanization
Keyboard too fast             → random inter-key delays
```

---

## Implementation Patterns (Playwright drop-in)

### Pattern 1 — playwright-extra + stealth plugin (recommended, no CloakBrowser needed)

```typescript
// Không cần CloakBrowser binary — plugin-based approach
import { chromium } from 'playwright-extra'
import StealthPlugin from 'playwright-extra-plugin-stealth'

chromium.use(StealthPlugin())

const browser = await chromium.launch({
  headless: true,  // stealth plugin fixes headless detection
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-blink-features=AutomationControlled',
  ]
})
const page = await browser.newPage()

// Fake a real viewport
await page.setViewportSize({ width: 1366, height: 768 })

// Spoof user agent
await page.setExtraHTTPHeaders({
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept-Language': 'en-US,en;q=0.9',
})
```

### Pattern 2 — Humanized typing

```typescript
async function humanType(page, selector: string, text: string) {
  await page.click(selector)
  for (const char of text) {
    await page.keyboard.type(char)
    // Random delay: 80-220ms between keystrokes
    await page.waitForTimeout(80 + Math.random() * 140)
  }
}
```

### Pattern 4 — Random delays between actions

```typescript
const delay = (min: number, max: number) =>
  new Promise(r => setTimeout(r, min + Math.random() * (max - min)))

// Usage
await page.goto(url)
await delay(1500, 3000)  // wait like a human reads the page
await humanMove(page, 500, 400)
await delay(300, 800)
await page.click('#button')
await delay(1000, 2500)
```

---

## Fingerprint Checks (verify evasion works)

```javascript
// Chạy trong page context để kiểm tra
const fingerprint = await page.evaluate(() => ({
  webdriver: navigator.webdriver,          // should be false/undefined
  chrome: !!window.chrome,                 // should be true (like real Chrome)
  plugins: navigator.plugins.length,       // should be > 0
  languages: navigator.languages,          // should have values
  platform: navigator.platform,            // should match OS
  hardwareConcurrency: navigator.hardwareConcurrency,  // should be > 0
  deviceMemory: navigator.deviceMemory,    // should be defined
}))

console.log('Fingerprint check:', fingerprint)
// webdriver: false ← critical, means stealth worked
```

---

## Common Sites + Approach

```
Cloudflare (5s challenge):
  → playwright-extra stealth + wait for JS challenge to complete (3-5s)
  → page.waitForSelector('.cf-challenge-running', { state: 'detached' })

Datadome:
  → real residential proxy + stealth headers + slow interactions

PerimeterX:
  → rotate user agents + add cookie from fresh session + humanized scroll

Simple bot checks (User-Agent only):
  → just set a real User-Agent header, no full stealth needed
```

---

## Python / Botasaurus Pattern
# Source: omkarcloud/botasaurus (MIT) — omit browser when not needed, auto-generate UI

Botasaurus là Python framework tích hợp sẵn evasion + parallelization + UI generation.
Dùng khi: cần Python, cần scale, hoặc cần expose scraper thành web app.

### HTTP-mode (không cần browser — 97% rẻ hơn)

```python
from botasaurus.request import request, Request

@request  # dùng HTTP thay vì browser — nhanh hơn, không bị fingerprint
def scrape_api(request: Request, data):
    response = request.get("https://example.com/api/data")
    return response.json()

# Chạy với caching built-in
scrape_api()
```

### Browser-mode với evasion tự động

```python
from botasaurus.browser import browser, Driver

@browser(block_images=True, reuse_driver=True)
def scrape_page(driver: Driver, data):
    driver.get("https://cloudflare-protected.com")
    driver.wait_for_element(".content")
    return driver.get_text(".content")

# Parallel scraping — tự động chia URLs ra nhiều workers
scrape_page(["https://site.com/page1", "https://site.com/page2", ...])
```

### Auto-generate Web UI từ scraper

```python
# Thêm @browser hoặc @request + chạy: python run.py
# → Tự tạo web interface cho phép user nhập URL, xem kết quả, export CSV
from botasaurus import *

@browser
def scrape(driver: Driver, data):
    driver.get(data["url"])
    return {"title": driver.title, "text": driver.get_text("body")}
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu navigator.webdriver = true sau khi apply stealth (stealth không hoạt động)
❌ FAIL nếu dùng stealth để bypass auth hoặc thu thập dữ liệu riêng tư — unauthorized use
❌ FAIL nếu không có random delays (robotic timing = detected ngay)
❌ FAIL nếu claim CloakBrowser available mà không có binary (cần install riêng)
✅ PASS khi: fingerprint check cho webdriver=false + page load thành công + không có captcha trigger
```

## See also
- `playwright-e2e` — standard automation không cần stealth
- `web-scraper` — scraping pattern (data extraction)
- `crawl4ai` — AI-native crawling với LLM extraction
- `firecrawl` — managed scraping API (no infra)
