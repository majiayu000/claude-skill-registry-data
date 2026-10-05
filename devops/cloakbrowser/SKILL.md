---
name: cloakbrowser
description: Debug and troubleshoot CloakBrowser stealth scraping in ettametta. Use when investigating scraping failures, platform detection issues, parse errors, fallback chain problems, or discovery-scraper service connectivity.
---
# CloakBrowser Stealth Scraping

## Architecture

Two-tier stealth scraping:
```
Python Scanner (cloak_scanner.py)
  -> HTTP GET -> discovery-scraper container (port 8010)
    -> Playwright with anti-detection
  -> Parse with platform-specific parser
  -> On failure: fall back to httpx-based scanner
```

The Playwright/stealth service code is NOT in this repo — `discovery-scraper` is deployed separately.

## Quick Diagnostics

```bash
# Test scraper
curl "http://discovery-scraper:8010/scrape/youtube?search_query=test"

# Generic endpoint
curl "http://discovery-scraper:8010/scrape/web?url=https://tiktok.com/search/video?q=test&platform=tiktok&wait_selector=[data-e2e='search_video-item']&scroll=true"
```

## Platform Configuration

| Platform | Endpoint | Wait Selector | Scroll | Timeout |
|---|---|---|---|---|
| YouTube | /scrape/youtube (dedicated) | ytd-video-renderer | No | 45s |
| TikTok | /scrape/web | [data-e2e="search_video-item"] | Yes | 40s |
| Instagram | /scrape/web | article | Yes | 40s |
| Facebook | /scrape/web | [role="article"] | Yes | 45s |
| X/Twitter | /scrape/web | [data-testid="tweet"] | Yes | 35s |
| LinkedIn | /scrape/web | .search-result__wrapper | Yes | 40s |

Concurrency: `asyncio.Semaphore(3)` — max 3 concurrent scans.

## Key Files

| File | Purpose |
|---|---|
| src/services/discovery/cloak_scanner.py | CloakBrowserScanner — HTTP client, retry, 6 parsers |
| src/services/discovery/cloak_platform_config.py | Platform config registry |
| src/services/discovery/cloak_tiktok_scanner.py | TikTok: Cloak -> httpx fallback |
| src/services/discovery/cloak_instagram_scanner.py | Instagram: Cloak -> httpx fallback |
| src/services/discovery/cloak_facebook_scanner.py | Facebook: Cloak -> httpx fallback |
| src/services/discovery/cloak_x_scanner.py | X: Cloak -> httpx fallback |
| src/services/discovery/cloak_linkedin_scanner.py | LinkedIn: Cloak -> httpx fallback |
| src/services/discovery/scanner_service.py | Per-platform circuit breakers (3 failures -> 600s recovery) |

## Fallback Chain

```
1. Try CloakBrowserScanner (stealth Playwright)
2. On exception: log warning, fall back to httpx-based *Scanner
```

At scanner service level: per-platform CircuitBreaker, asyncio.wait_for with timeout, gather with return_exceptions.

At discovery service level: live scan -> DB cache -> scraper swarm.

## Parser Details

- **YouTube**: id, url, channel, title, thumbnail, views (handles "1.2M", "500K")
- **TikTok**: Multiple field variants, viral score: `min(max(int((views/5000)*(1+engagement*10)),1),95)`
- **Instagram**: Estimates views as likes*20, URLs: `instagram.com/reel/{shortcode}/`
- **X/Twitter**: Estimates views as engagement_total*15
- **LinkedIn**: Estimates views as engagement_total*30

## Cookie Management

CloakBrowser does NOT use cookies — anonymous stealth browsing only.

Cookies used by httpx fallback:
- `src/services/infrastructure/cookie_manager.py` — YouTube cookies for yt-dlp
- `src/services/optimization/cookie_manager.py` — Multi-platform cookies
- `src/services/optimization/auth.py` — TokenManager with Fernet-encrypted OAuth

## Common Issues

### discovery-scraper unreachable
```bash
curl -s http://discovery-scraper:8010/health || echo "Service down"
docker compose exec api getent hosts discovery-scraper
```

### All platforms returning empty
Scraper service likely down. Check: service running, Playwright browsers installed, network connectivity.

### Platform-specific detection
Check if wait selector is still valid (platforms update HTML). Increase timeout in cloak_platform_config.py.

### Circuit breaker open
3 failures -> 600s recovery. Check: `docker compose logs api | grep -i circuit`

### Concurrency bottleneck
Semaphore = 3. For large batches, increase in cloak_scanner.py if scraper can handle more.
