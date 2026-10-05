---
name: content-discovery
description: Debug and troubleshoot ettametta's content discovery and trend scanning system. Use when investigating scan failures, scoring anomalies, platform scanner issues, data normalization problems, or the discovery-to-video pipeline flow.
---
# Content Discovery Debugging

## Architecture

Dual-language: Python orchestrator + Go high-performance scanner.

**Python** (`src/services/discovery/service.py`): DiscoveryService — scanning, caching, filtering, persistence, AI ranking, recursive expansion.

**Go** (legacy, removed): High-performance scanner was previously in `src/services/discovery-go/` — consolidated into Python orchestrator.

## Quick Diagnostics

```bash
# Trigger scan
curl -X POST http://localhost:8000/api/v1/discovery/scan \
  -H "Content-Type: application/json" \
  -d '{"niche": "tech", "platforms": ["youtube"]}'

# Go service health
curl http://discovery-go:8080/health

# Monitored niches
curl http://localhost:8000/api/v1/discovery/niches
```

## Scan Pipeline

1. Redis cache check (skipped on deep scans)
2. Parallel multi-platform scanning (asyncio.gather)
3. DB fallback if no live results
4. Scraper swarm fallback (video_lead_scanner)
5. Quality auditing per candidate
6. Monetization-mode filtering
7. Batch persistence to PostgreSQL
8. Viral score recalculation (70% velocity / 30% original)
9. Recursive AI expansion (Groq identifies sub-niches)

## Platform Scanners (19 total)

### Primary (every scan)
| Scanner | Method |
|---|---|
| YouTube Shorts | YouTube Data API v3 |
| YouTube Long | YouTube Data API v3 |
| CloakBrowser YouTube | Stealth Playwright via discovery-scraper |
| CloakTikTok | Cloak + httpx fallback |
| DuckDuckGo | Free web scraping fallback |

### Secondary (deep scans / premium)
| Scanner | Method |
|---|---|
| Reddit | JSON API |
| CloakX/Instagram/Facebook/LinkedIn | Cloak + httpx |
| Twitch, Pinterest, Snapchat, Bilibili, Rumble, Skool | Web scrape |
| Google Trends, Google Search | API/scrape |
| Public Domain (Pexels, Archive.org) | Stock content |

## Viral Scoring

### Base viral score (0-100)
- Velocity (max 50): `min(velocity/10, 50)`
- Engagement (max 25): `min(engagement_score/10, 25)`
- Duration bonus (max 15): +15 for 15-60s, +10 for 60-180s

### Platform-specific
- YouTube: `(velocity/100) * (1 + engagement*10)`, clamped 1-99
- TikTok: `(views/5000) * (1 + engagement*10)`, clamped 1-95
- Go service: 35% VPH + 35% engagement + 20% momentum + 10% recency

### AI pattern deconstruction (deconstructor.py)
Groq llama3-70b extracts: hook_score, retention_estimate, pacing_bpm, style_keywords, emotional_triggers.

### Quality auditing (eligibility.py)
30+ indicators with penalty scoring. Below 0.6 = flagged low quality. Freshness: 1-30 days = "viral sweet spot".

## Data Normalization

All platforms normalize to `ContentCandidate` (models.py):
- id (prefixed: "yt_", "tt_", "cloak_yt_"), platform, source_uri
- view_count, like_count, comment_count, share_count
- velocity (views/hour), engagement_score, viral_score (0-100)
- quality_score, quality_flags, analysis_results

## Discovery-to-Video Pipeline

| Path | Trigger | Flow |
|---|---|---|
| ViralContentPipeline | API call | Discover -> Analyze -> AI Video -> Compile |
| Nexus Trigger | Every 1h (Celery) | High-potential candidates -> NexusJob -> cinema_video |
| Sentinel Auto-Pilot | Every 4h (Celery) | Full Viral Loop: Discover -> Pick -> Render -> Publish |
| Batch Download | Manual/trigger | yt-dlp -> Stock fallback -> Safety asset |

## Periodic Tasks

| Task | Schedule | Purpose |
|---|---|---|
| discovery.sentinel_watcher | 4h | Full viral loop or trend scan per niche |
| scan_trending_content | 2h | ScannerService with circuit breakers |
| discovery.process_high_potential | 1h | High-potential -> Nexus video |

## Key Files

| File | Purpose |
|---|---|
| src/services/discovery/service.py | Main DiscoveryService orchestrator |
| src/services/discovery/scanner_base.py | ABC with velocity/score methods |
| src/services/discovery/models.py | ContentCandidate, ViralPattern |
| src/services/discovery/tasks.py | Celery tasks |
| src/services/discovery/scanner_service.py | Periodic scan with circuit breakers |
| src/services/discovery/analysis_service.py | AI content analysis |
| src/services/discovery/deconstructor.py | Pattern deconstruction |
| src/services/discovery/eligibility.py | Quality auditing |
| src/services/discovery/video_content_pipeline.py | End-to-end pipeline |

## Common Issues

### All platforms returning empty
Scraper service down? Circuit breakers open? Check discovery-scraper connectivity.

### Stale discovery cache
`discovery:trends:*` keys have no TTL. Clear manually:
```bash
redis-cli -p 7204 -a "$REDIS_PASSWORD" --scan --pattern "discovery:trends:*" | xargs redis-cli del
```

### Recursive expansion causes scan storm
Groq identifies 3 sub-niches per scan, each triggers a background Celery task. Can snowball.

### Scanner circuit breaker open
Per-platform (3 failures, 600s recovery). Check logs.

### Quality audit too aggressive
30+ penalties. Check eligibility.py thresholds.

## Debugging Checklist

1. Is discovery-scraper reachable?
2. Circuit breakers open? `docker compose logs api | grep circuit`
3. Redis cache: `redis-cli --scan --pattern "discovery:*"`
4. Go service: `curl http://discovery-go:8080/health`
5. Celery tasks active: `celery -A src.api.utils.celery inspect active`
6. DB candidates: `SELECT count(*) FROM content_candidates;`
7. Niche expansion: `SELECT distinct niche FROM content_candidates;`
