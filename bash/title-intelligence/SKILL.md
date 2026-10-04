---
name: title-intelligence
description: Orchestrates data collection from Korean webtoon/webnovel platforms (Naver, Kakao, Manta, etc.) and fan engagement sources (Reddit, AO3). This skill should be used when collecting platform metrics for titles, updating title data from source platforms, or gathering intelligence for new titles.
---

# Title Intelligence

This skill orchestrates data collection from multiple platforms to gather metrics, metadata, and fan engagement data for titles.

## When to Use This Skill

- Collecting platform metrics for a new title
- Updating metrics for existing titles
- Batch collection for titles missing data
- Gathering fan engagement data (Reddit, AO3)
- Debugging data collection issues

## Supported Platforms

### Official Platforms (Korean)

| Platform | Domain | Data Collected |
|----------|--------|----------------|
| Naver Webtoon | comic.naver.com | Views, subscribers, rating, episodes, synopsis |
| Naver Series | series.naver.com | Views, subscribers, rating, episodes |
| Kakao Page | page.kakao.com | Views, likes, comments, episodes |
| Kakao Webtoon | webtoon.kakao.com | Views, likes, rating |
| Ridibooks | ridibooks.com | Rating, reviews |
| Bomtoon | bomtoon.com | Views, rating |

### Official Platforms (English)

| Platform | Domain | Data Collected |
|----------|--------|----------------|
| Manta | manta.net | Views, likes, rating |
| Lezhin Comics | lezhinus.com | Views, subscribers, chapters, tags, genre, authors, synopsis, completed status, cover |
| Webtoons | webtoons.com | NOT wired into the live edge function — scraper exists only in packages/title-intelligence |

**Lezhin notes:**
- URL format: `https://www.lezhinus.com/{lang}/comic/{alias}` (legacy lezhin.com also accepted)
- Data comes from the Next.js flight data embedded in the page HTML (server-rendered)
- Adult-gated titles require the `LEZHIN_COOKIE` edge function secret — the Cookie header from a logged-in lezhinus.com session with content mode "all". Set via `npx supabase secrets set LEZHIN_COOKIE='...'`. Without it, gated titles return a descriptive error; non-gated titles work without the secret.

### Fan Engagement Sources

| Source | Domain | Data Collected |
|--------|--------|----------------|
| Reddit | reddit.com | Subreddit mentions, posts, comments |
| AO3 | archiveofourown.org | Fanfic count, kudos, bookmarks |
| Comick | comick.live | Unofficial aggregator stats |

## Commands

```
/title-intelligence --title="Title Name"           # Collect by title name
/title-intelligence --url="https://..."            # Collect from specific URL
/title-intelligence --platform=kakao --batch=20    # Batch by platform
/title-intelligence --missing-views                # Titles without view data
/title-intelligence --fan-engagement="Title Name"  # Reddit + AO3 only
```

## Data Collection Workflows

### Single Title Collection (by URL)

The most accurate method - provide direct platform URL:

```bash
# Via edge function
curl -X POST "$SUPABASE_URL/functions/v1/title-intelligence" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [{
      "platform": "naver_webtoon",
      "platformId": "783052",
      "originalUrl": "https://comic.naver.com/webtoon/list?titleId=783052"
    }],
    "collectedBy": "admin@example.com",
    "contentType": "webtoon"
  }'
```

### Single Title Collection (by Name)

Search-based collection (less reliable):

```bash
curl -X POST "$SUPABASE_URL/functions/v1/title-intelligence" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "titleNameInput": "재벌집 막내아들",
    "titleNameEn": "Reborn Rich",
    "sources": ["naver", "kakao", "reddit"],
    "collectedBy": "admin@example.com",
    "contentType": "webnovel"
  }'
```

### Batch Collection Script

For collecting multiple titles:

```bash
# Use the batch collection script
node scripts/batch-collect-kakao-metrics.js
```

### Fan Engagement Only

Collect Reddit and AO3 data without platform metrics:

```bash
curl -X POST "$SUPABASE_URL/functions/v1/title-intelligence" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [],
    "collectedBy": "admin@example.com",
    "fanEngagement": {
      "titleName": "Solo Leveling",
      "sources": ["reddit", "ao3"]
    }
  }'
```

## Database Schema

### intelligence_titles

Central record for each title being tracked:

```sql
CREATE TABLE intelligence_titles (
  id UUID PRIMARY KEY,
  title_ko TEXT,
  title_en TEXT,
  slug TEXT UNIQUE,
  content_type TEXT,  -- webtoon, webnovel, light_novel, manga
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
);
```

### intelligence_sources

Platform connections for each title:

```sql
CREATE TABLE intelligence_sources (
  id UUID PRIMARY KEY,
  intelligence_title_id UUID REFERENCES intelligence_titles,
  platform TEXT,           -- naver_webtoon, kakao, manta, etc.
  platform_id TEXT,        -- Platform-specific ID
  platform_url TEXT,       -- Original URL
  source_category TEXT,    -- official_platform, fandom_forum, fanfiction
  is_primary BOOLEAN,
  last_scraped_at TIMESTAMPTZ
);
```

### intelligence_metrics

Time-series snapshots:

```sql
CREATE TABLE intelligence_metrics (
  id UUID PRIMARY KEY,
  source_id UUID REFERENCES intelligence_sources,
  scraped_at TIMESTAMPTZ,
  views BIGINT,
  subscribers BIGINT,
  likes BIGINT,
  rating_score NUMERIC,
  rating_count INTEGER,
  episode_count INTEGER,
  comment_count INTEGER,
  -- Platform-specific JSON
  raw_data JSONB
);
```

## Field Mapping to Titles Table

When data is collected, it can be mapped to the main `titles` table:

| Intelligence Field | Titles Field |
|-------------------|--------------|
| views | views |
| subscribers | likes |
| rating_score | rating |
| episode_count | chapters |
| synopsis_kr | synopsis_kr |
| genre | genre |
| author | story_author |
| thumbnail | title_image |
| tags | keywords |

### Mapping via Admin UI

In the Dashboard admin panel, use the "Collect Data" button in TitleEditModal to:
1. Trigger intelligence collection
2. Preview collected data
3. Map fields to title record

### Mapping via SQL

```sql
-- Update title with intelligence data
UPDATE titles t
SET
  views = m.views,
  likes = m.subscribers,
  rating = m.rating_score,
  chapters = m.episode_count,
  updated_at = NOW()
FROM intelligence_metrics m
JOIN intelligence_sources s ON m.source_id = s.id
JOIN intelligence_titles it ON s.intelligence_title_id = it.id
WHERE it.title_en = t.title_name_en
  AND s.is_primary = true
  AND m.scraped_at = (
    SELECT MAX(scraped_at)
    FROM intelligence_metrics
    WHERE source_id = s.id
  );
```

## Rate Limiting

To avoid detection and blocking:

| Platform | Rate Limit | Notes |
|----------|------------|-------|
| Naver | 1 req/3s | Strict bot detection |
| Kakao | 1 req/3s | Strict bot detection |
| Manta | 1 req/2s | Moderate detection |
| Reddit | No limit | Uses official API |
| AO3 | 1 req/5s | Community respect |

## Error Handling

### Platform Blocks

If a platform blocks requests:
1. Wait 5-10 minutes before retrying
2. Use different request headers
3. Consider using platform-specific cookies

### Missing Data

Some fields may not be available:
```json
{
  "views": 1234567,
  "rating": null,        // Not available on this platform
  "subscribers": 45000,
  "error_fields": ["rating"]
}
```

### Scraper Failures

Check edge function logs:
```bash
npx supabase functions logs title-intelligence --scroll
```

## Verification

### Check Collection Results

```sql
-- Recent collections
SELECT
  it.title_en,
  s.platform,
  m.views,
  m.scraped_at
FROM intelligence_metrics m
JOIN intelligence_sources s ON m.source_id = s.id
JOIN intelligence_titles it ON s.intelligence_title_id = it.id
ORDER BY m.scraped_at DESC
LIMIT 20;
```

### Find Titles Missing Data

```sql
-- Titles without any intelligence data
SELECT t.title_name_en, t.views
FROM titles t
LEFT JOIN intelligence_titles it ON t.title_name_en = it.title_en
WHERE it.id IS NULL
ORDER BY t.views DESC NULLS LAST
LIMIT 50;
```

## Console Output

```
Collecting title intelligence...

[1/4] Parsing request
      Title: "재벌집 막내아들"
      Platforms: naver, kakao

[2/4] Scraping Naver Webtoon
      URL: https://comic.naver.com/...
      Views: 12,345,678
      Subscribers: 890,123
      Rating: 9.8
      Episodes: 156

[3/4] Scraping Kakao Page
      URL: https://page.kakao.com/...
      Views: 8,901,234
      Likes: 234,567
      Episodes: 156

[4/4] Storing results
      Intelligence title: created
      Sources: 2 created
      Metrics: 2 snapshots saved

Collection complete!
Total platforms: 2
Total views: 21,246,912
```

## Slack Notification

```json
{
  "text": "Title Intelligence Collected",
  "attachments": [{
    "color": "good",
    "fields": [
      {"title": "Title", "value": "Reborn Rich", "short": true},
      {"title": "Platforms", "value": "2", "short": true},
      {"title": "Total Views", "value": "21.2M", "short": true},
      {"title": "Rating", "value": "9.8", "short": true}
    ]
  }]
}
```

## Tips

1. **Use URLs when possible** - More reliable than title name search
2. **Collect during off-peak hours** - Less likely to be rate-limited
3. **Verify data accuracy** - Cross-reference with platform
4. **Monitor for platform changes** - Scrapers may need updates
5. **Batch responsibly** - Don't overwhelm platforms

## Related Documentation

- **Creator App**: Full TitleInvestigator tool at `/tools/title-investigator`
- **Dashboard Admin**: "Collect Data" button in TitleEditModal
- **Edge Function**: `supabase/functions/title-intelligence/`

## Related Skills

- `/find-english-release` - Resolve a Korean title URL to its English counterpart (Webtoons, Manta, Lezhin, Tappytoon) before running intelligence collection on the English side
- `/regenerate-embeddings` - Regenerate after data collection
- `/health-check` - Verify intelligence system health
- `/cost-report` - Track collection operations
