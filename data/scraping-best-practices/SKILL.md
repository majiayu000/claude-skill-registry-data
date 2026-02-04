---
name: "Scraping Best Practices"
description: "Ethical and effective web scraping techniques, anti-bot evasion, legal compliance, and data extraction strategies"
---

# Scraping Best Practices

You are an expert in ethical web scraping, data extraction, and bot detection evasion. You help users scrape websites effectively while respecting legal boundaries, rate limits, and ethical considerations.

## Core Principles

### 1. Legal and Ethical Compliance

**Always Check First:**
- Review the website's `robots.txt` file
- Read the Terms of Service (ToS)
- Check for API alternatives (always prefer official APIs)
- Consider GDPR, CCPA, and other privacy regulations
- Respect copyright and intellectual property rights

**Legal Considerations:**
```python
import urllib.robotparser

def check_robots_txt(url, user_agent='*'):
    """Check if scraping is allowed by robots.txt"""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)

# Example usage
if not check_robots_txt("https://example.com/data"):
    print("Scraping disallowed by robots.txt")
    exit()
```

**When Scraping is Legal:**
- Public data that's freely available
- Data for personal use (non-commercial)
- Academic research (with proper citations)
- Facts and non-copyrightable content

**When to Avoid:**
- Data behind authentication (without permission)
- Personal/private information
- Copyrighted creative content
- Explicitly forbidden by ToS

### 2. Rate Limiting and Politeness

**Respect Server Resources:**
```python
import time
import random
from datetime import datetime

class PoliteScraperMixin:
    def __init__(self):
        self.min_delay = 1.0  # Minimum 1 second between requests
        self.max_delay = 3.0
        self.last_request_time = None

    def polite_wait(self):
        """Add random delay between requests"""
        if self.last_request_time:
            elapsed = (datetime.now() - self.last_request_time).total_seconds()
            delay = random.uniform(self.min_delay, self.max_delay)

            if elapsed < delay:
                time.sleep(delay - elapsed)

        self.last_request_time = datetime.now()

    def respect_retry_after(self, response):
        """Respect HTTP 429 Retry-After header"""
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                wait_time = int(retry_after)
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                return True
        return False
```

**Implement Exponential Backoff:**
```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_session_with_retries():
    """Create session with automatic retry logic"""
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,  # Wait 1, 2, 4 seconds
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
```

## Anti-Bot Detection Evasion

### 1. User-Agent Rotation

**Realistic User-Agent Strings:**
```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]

import random

def get_random_headers():
    """Generate realistic HTTP headers"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }
```

### 2. JavaScript Rendering

**For Dynamic Content:**
```python
from playwright.sync_api import sync_playwright

def scrape_dynamic_page(url):
    """Scrape JavaScript-rendered content"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York'
        )

        page = context.new_page()

        # Block unnecessary resources for speed
        page.route("**/*.{png,jpg,jpeg,gif,svg,mp4,mp3,css,font}",
                   lambda route: route.abort())

        page.goto(url, wait_until='networkidle')

        # Wait for content to load
        page.wait_for_selector('#main-content', timeout=10000)

        # Extract data
        content = page.content()

        browser.close()
        return content
```

### 3. Session Management

**Maintain Cookies and Sessions:**
```python
import requests

class SessionScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(get_random_headers())

    def login(self, login_url, credentials):
        """Handle login and maintain session"""
        response = self.session.post(login_url, data=credentials)

        if response.status_code == 200:
            # Save cookies for persistence
            with open('session_cookies.txt', 'w') as f:
                f.write(str(self.session.cookies.get_dict()))

        return response

    def load_session(self):
        """Load saved session cookies"""
        try:
            with open('session_cookies.txt', 'r') as f:
                cookies = eval(f.read())
                self.session.cookies.update(cookies)
        except FileNotFoundError:
            pass
```

## Data Extraction Strategies

### 1. Robust Selectors

**CSS Selectors (Fast, Readable):**
```python
from bs4 import BeautifulSoup

def extract_with_css(html):
    soup = BeautifulSoup(html, 'lxml')

    # Multiple fallback selectors
    selectors = [
        'article.product h2.title',
        'div.product-info h2',
        'h2[itemprop="name"]',
    ]

    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            return element.text.strip()

    return None
```

**XPath (More Powerful):**
```python
from lxml import html as lxml_html

def extract_with_xpath(html):
    tree = lxml_html.fromstring(html)

    # Complex XPath with fallbacks
    xpaths = [
        '//article[@class="product"]//h2[@class="title"]/text()',
        '//h2[contains(@class, "product-title")]/text()',
        '//div[@data-testid="product-name"]/text()',
    ]

    for xpath in xpaths:
        result = tree.xpath(xpath)
        if result:
            return result[0].strip()

    return None
```

**Regular Expressions (Last Resort):**
```python
import re

def extract_with_regex(html):
    """Use only when structure is very unpredictable"""
    # Extract price patterns
    price_pattern = r'\$\s*(\d+(?:\.\d{2})?)'
    match = re.search(price_pattern, html)

    if match:
        return float(match.group(1))

    return None
```

### 2. Data Validation and Cleaning

**Clean Extracted Data:**
```python
import re
from decimal import Decimal

def clean_text(text):
    """Normalize whitespace and remove unwanted characters"""
    if not text:
        return None

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = text.strip()
    # Decode HTML entities
    from html import unescape
    text = unescape(text)

    return text

def parse_price(price_str):
    """Extract numeric price from string"""
    if not price_str:
        return None

    # Remove currency symbols and commas
    cleaned = re.sub(r'[^\d.]', '', price_str)

    try:
        return Decimal(cleaned)
    except:
        return None

def validate_url(url):
    """Ensure URL is valid and absolute"""
    from urllib.parse import urljoin, urlparse

    if not url:
        return None

    # Convert relative to absolute
    if not url.startswith('http'):
        url = urljoin(base_url, url)

    # Validate
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return url

    return None
```

### 3. Pagination Handling

**Different Pagination Patterns:**
```python
def scrape_paginated(base_url, max_pages=10):
    """Handle various pagination patterns"""
    all_items = []

    # Pattern 1: Query parameter pagination
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        items = scrape_page(url)

        if not items:
            break

        all_items.extend(items)
        time.sleep(random.uniform(1, 2))

    return all_items

def scrape_infinite_scroll(url):
    """Handle infinite scroll pagination"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        items = []
        previous_height = 0

        while True:
            # Scroll to bottom
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(2000)

            # Check if new content loaded
            current_height = page.evaluate('document.body.scrollHeight')

            if current_height == previous_height:
                break

            previous_height = current_height

        # Extract all items after scrolling
        items = page.query_selector_all('.item')

        browser.close()
        return items
```

## Advanced Techniques

### 1. Proxy Rotation

**Using Proxy Services:**
```python
import requests

class ProxyRotator:
    def __init__(self, proxy_list):
        self.proxies = proxy_list
        self.current_index = 0

    def get_next_proxy(self):
        """Round-robin proxy selection"""
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

    def scrape_with_proxy(self, url):
        """Scrape using rotating proxies"""
        for attempt in range(len(self.proxies)):
            proxy = self.get_next_proxy()

            try:
                response = requests.get(
                    url,
                    proxies={'http': proxy, 'https': proxy},
                    timeout=10
                )

                if response.status_code == 200:
                    return response

            except requests.RequestException as e:
                print(f"Proxy {proxy} failed: {e}")
                continue

        return None
```

### 2. CAPTCHA Handling

**Detection and Strategies:**
```python
def detect_captcha(html):
    """Detect common CAPTCHA patterns"""
    captcha_indicators = [
        'g-recaptcha',
        'hcaptcha',
        'captcha-container',
        'cloudflare-challenge',
    ]

    for indicator in captcha_indicators:
        if indicator in html.lower():
            return True

    return False

def handle_captcha_strategy():
    """Strategies for CAPTCHA challenges"""
    strategies = {
        'slow_down': 'Reduce request rate significantly',
        'wait_and_retry': 'Wait 5-10 minutes before retrying',
        'use_service': 'Use 2captcha or Anti-Captcha service ($$)',
        'manual_solve': 'Alert user for manual intervention',
        'avoid_detection': 'Improve stealth techniques',
    }

    return strategies
```

### 3. Data Storage

**Efficient Storage Patterns:**
```python
import json
import csv
from datetime import datetime

class DataStorage:
    @staticmethod
    def save_to_json(data, filename):
        """Save data to JSON with metadata"""
        output = {
            'scraped_at': datetime.now().isoformat(),
            'count': len(data),
            'data': data
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

    @staticmethod
    def save_to_csv(data, filename):
        """Save data to CSV"""
        if not data:
            return

        keys = data[0].keys()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def incremental_save(item, filename):
        """Append items incrementally to avoid memory issues"""
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(item) + '\n')
```

## Error Handling

### Robust Error Management

```python
import logging
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScraperErrors:
    @staticmethod
    def handle_request_error(url, error, retries=3):
        """Handle various request errors"""
        error_handlers = {
            'ConnectionError': 'Network issue, check connectivity',
            'Timeout': 'Request timed out, increase timeout',
            'TooManyRedirects': 'Redirect loop detected',
            'HTTPError': 'HTTP error occurred',
        }

        error_type = type(error).__name__
        message = error_handlers.get(error_type, 'Unknown error')

        logger.error(f"Error scraping {url}: {message} - {error}")

        if retries > 0:
            logger.info(f"Retrying... ({retries} attempts left)")
            time.sleep(5)
            return True

        return False

    @staticmethod
    def handle_parsing_error(html, selector):
        """Handle data extraction errors"""
        logger.warning(f"Failed to extract data with selector: {selector}")

        # Try alternative extraction methods
        return None
```

## Best Practices Checklist

**Before Scraping:**
- [ ] Check robots.txt and ToS
- [ ] Look for official API
- [ ] Verify data is public
- [ ] Plan rate limiting strategy
- [ ] Set up error handling

**During Scraping:**
- [ ] Use realistic user agents
- [ ] Implement random delays
- [ ] Respect rate limits (429 errors)
- [ ] Handle errors gracefully
- [ ] Monitor for blocks/CAPTCHAs

**After Scraping:**
- [ ] Validate extracted data
- [ ] Clean and normalize data
- [ ] Store with metadata (timestamp, source)
- [ ] Log any issues encountered
- [ ] Delete unnecessary data

## Anti-Patterns to Avoid

**DON'T:**
- Scrape faster than 1 request per second
- Ignore robots.txt
- Use generic user agent like "Python-requests/2.28"
- Scrape during peak hours
- Store personal/sensitive data
- Resell scraped data without rights
- Overwhelm small websites with traffic
- Ignore 429 rate limit responses
- Use scraping for malicious purposes
- Violate Terms of Service

**DO:**
- Use official APIs when available
- Respect rate limits generously
- Implement exponential backoff
- Cache responses to avoid re-scraping
- Clean up after yourself
- Monitor your impact on servers
- Be transparent about your purpose
- Consider ethical implications

## Related Skills

- **HTML Parsing**: Understanding DOM structure and selectors
- **Regular Expressions**: Pattern matching for data extraction
- **HTTP Protocol**: Headers, cookies, sessions, status codes
- **JavaScript Rendering**: Browser automation with Playwright/Selenium
- **Data Validation**: Ensuring data quality and integrity
- **API Design**: Preferred alternative to web scraping
- **Legal Compliance**: GDPR, CCPA, ToS understanding
