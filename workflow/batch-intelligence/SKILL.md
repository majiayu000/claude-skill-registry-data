---
name: batch-intelligence
description: Batch data collection from Korean webtoon/webnovel platforms (Naver, Kakao, Manta) with auto-ingest to titles table. This skill should be used for collecting metrics on multiple titles, refreshing stale data, or gathering data for titles missing views/ratings.
---

# Batch Intelligence

This skill orchestrates batch data collection from Korean platforms, enabling large-scale metric updates without manual UI interaction.

## When to Use This Skill

- Collecting data for multiple titles at once (50+)
- Refreshing stale data (older than 30 days)
- Filling gaps (titles missing views, ratings, or chapters)
- Platform-specific bulk collection (all Kakao titles, all Naver titles)
- Pipeline automation (collect → embed → analyze)
- Porting the feature to another app

## Supported Platforms

| Platform | Domain | Data Collected | Rate Limit |
|----------|--------|----------------|------------|
| Naver Webtoon | comic.naver.com | Views, subscribers, rating, episodes | 1 req/3s |
| Naver Series | series.naver.com | Views, subscribers, rating, episodes | 1 req/3s |
| Kakao Page | page.kakao.com | Views, likes, comments, episodes | 1 req/3s |
| Kakao Webtoon | webtoon.kakao.com | Views, likes, rating | 1 req/3s |
| Manta | manta.net | Views, likes, rating | 1 req/2s |
| Reddit | reddit.com | Subreddit mentions, posts | No limit |
| AO3 | archiveofourown.org | Fanfic count, kudos | 1 req/5s |

## Commands

```
/batch-intelligence --missing-views              # Titles without view data
/batch-intelligence --missing-rating             # Titles without rating
/batch-intelligence --stale=30                   # Data older than 30 days
/batch-intelligence --platform=kakao             # Specific platform
/batch-intelligence --limit=50                   # Limit batch size
/batch-intelligence --auto-ingest                # Auto-update titles table
/batch-intelligence --dry-run                    # Preview without executing
/batch-intelligence --fan-engagement             # Include Reddit/AO3
```

## Edge Function Reference

**Location**: `supabase/functions/title-intelligence/index.ts`

**Endpoint**: `POST /functions/v1/title-intelligence`

**Request Body**:
```typescript
interface IntelligenceRequest {
  // URL-based collection (preferred)
  urls?: Array<{
    platform: 'naver_webtoon' | 'naver_series' | 'kakao_page' | 'kakao_webtoon' | 'manta';
    platformId: string;
    originalUrl: string;
  }>;

  // Name-based collection (fallback)
  titleNameInput?: string;
  titleNameEn?: string;
  sources?: string[];

  // Fan engagement
  fanEngagement?: {
    titleName: string;
    sources: ('reddit' | 'ao3' | 'comick')[];
  };

  // Metadata
  collectedBy: string;
  contentType: 'webtoon' | 'webnovel' | 'light_novel' | 'manga';
}
```

**Response**:
```typescript
interface IntelligenceResponse {
  success: boolean;
  intelligenceTitle: {
    id: string;
    title_ko: string;
    title_en: string;
  };
  sources: Array<{
    platform: string;
    metrics: {
      views: number;
      subscribers: number;
      rating: number;
      episodes: number;
    };
    error?: string;
  }>;
  fanEngagement?: {
    reddit: { mentions: number; posts: number };
    ao3: { works: number; kudos: number };
  };
}
```

## Batch Workflow

### Step 1: Identify Titles to Process

```sql
-- Titles missing views
SELECT title_id, title_name_en, title_url
FROM titles
WHERE views IS NULL OR views = 0
ORDER BY created_at DESC
LIMIT 50;

-- Titles with stale data (30+ days)
SELECT t.title_id, t.title_name_en, im.scraped_at
FROM titles t
LEFT JOIN intelligence_sources s ON t.title_name_en = s.intelligence_title_id
LEFT JOIN intelligence_metrics im ON s.id = im.source_id
WHERE im.scraped_at < NOW() - INTERVAL '30 days'
   OR im.scraped_at IS NULL
LIMIT 50;

-- Platform-specific (Kakao titles)
SELECT title_id, title_name_en, title_url
FROM titles
WHERE title_url LIKE '%kakao%'
  AND (views IS NULL OR views = 0);
```

### Step 2: Extract Platform URLs

Parse URLs from titles table to get platform IDs:

```javascript
function parseUrl(url) {
  // Naver Webtoon: https://comic.naver.com/webtoon/list?titleId=783052
  if (url.includes('comic.naver.com')) {
    const match = url.match(/titleId=(\d+)/);
    return { platform: 'naver_webtoon', platformId: match?.[1] };
  }

  // Kakao Page: https://page.kakao.com/content/12345678
  if (url.includes('page.kakao.com')) {
    const match = url.match(/content\/(\d+)/);
    return { platform: 'kakao_page', platformId: match?.[1] };
  }

  // Manta: https://manta.net/series/123456
  if (url.includes('manta.net')) {
    const match = url.match(/series\/(\d+)/);
    return { platform: 'manta', platformId: match?.[1] };
  }

  return null;
}
```

### Step 3: Batch Collection

```javascript
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

async function collectBatch(titles, options = {}) {
  const results = { success: [], failed: [], skipped: [] };

  for (const title of titles) {
    // Rate limiting
    await delay(3000); // 3 seconds between requests

    try {
      const parsed = parseUrl(title.title_url);
      if (!parsed) {
        results.skipped.push({ title: title.title_name_en, reason: 'Unparseable URL' });
        continue;
      }

      const response = await fetch(`${SUPABASE_URL}/functions/v1/title-intelligence`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          urls: [{
            platform: parsed.platform,
            platformId: parsed.platformId,
            originalUrl: title.title_url
          }],
          collectedBy: 'batch-intelligence-skill',
          contentType: 'webtoon'
        })
      });

      const data = await response.json();

      if (data.success) {
        results.success.push({
          title: title.title_name_en,
          metrics: data.sources[0]?.metrics
        });

        // Auto-ingest if enabled
        if (options.autoIngest) {
          await ingestToTitle(title.title_id, data.sources[0]?.metrics);
        }
      } else {
        results.failed.push({ title: title.title_name_en, error: data.error });
      }
    } catch (error) {
      results.failed.push({ title: title.title_name_en, error: error.message });
    }
  }

  return results;
}
```

### Step 4: Auto-Ingest to Titles Table

```javascript
async function ingestToTitle(titleId, metrics) {
  const updates = {};

  if (metrics.views) updates.views = metrics.views;
  if (metrics.subscribers) updates.likes = metrics.subscribers;
  if (metrics.rating) updates.rating = metrics.rating;
  if (metrics.episodes) updates.chapters = metrics.episodes;

  updates.updated_at = new Date().toISOString();

  const { error } = await supabase
    .from('titles')
    .update(updates)
    .eq('title_id', titleId);

  return !error;
}
```

## Cost Estimation

**This skill is FREE** - No AI API calls, only web scraping.

| Batch Size | Time Estimate | API Cost |
|------------|---------------|----------|
| 10 titles | ~30 seconds | $0 |
| 50 titles | ~2.5 minutes | $0 |
| 100 titles | ~5 minutes | $0 |
| 500 titles | ~25 minutes | $0 |

Note: Time estimates assume 3-second rate limiting per request.

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Platform blocked request` | Too many requests | Increase rate limit delay to 5s |
| `Title not found` | Invalid platform ID | Verify URL is correct |
| `Timeout` | Slow platform response | Retry with longer timeout |
| `Parse error` | Page structure changed | Check if scraper needs update |

### Retry Logic

```javascript
async function collectWithRetry(title, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await collect(title);
      return result;
    } catch (error) {
      if (attempt === maxRetries) throw error;
      await delay(5000 * attempt); // Exponential backoff
    }
  }
}
```

## Console Output

```
Starting batch intelligence collection...

Configuration:
  Filter: missing-views
  Limit: 50
  Auto-ingest: enabled

[1/50] Processing "재벌집 막내아들"
       Platform: kakao_page
       Views: 12,345,678
       Rating: 9.8
       ✅ Collected + ingested

[2/50] Processing "Solo Leveling"
       Platform: naver_webtoon
       Views: 89,012,345
       Rating: 9.9
       ✅ Collected + ingested

[3/50] Processing "Unknown Title"
       ❌ Skipped: Unparseable URL

...

Summary:
  ✅ Success: 45 titles
  ❌ Failed: 3 titles
  ⏭️ Skipped: 2 titles
  ⏱️ Duration: 2m 34s

Failed titles:
  - "Title A": Platform blocked request
  - "Title B": Timeout after 60s
  - "Title C": Title not found on platform
```

## Database Tables

### intelligence_titles
```sql
CREATE TABLE intelligence_titles (
  id UUID PRIMARY KEY,
  title_ko TEXT,
  title_en TEXT,
  slug TEXT UNIQUE,
  content_type TEXT,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
);
```

### intelligence_sources
```sql
CREATE TABLE intelligence_sources (
  id UUID PRIMARY KEY,
  intelligence_title_id UUID REFERENCES intelligence_titles,
  platform TEXT,
  platform_id TEXT,
  platform_url TEXT,
  source_category TEXT,
  is_primary BOOLEAN,
  last_scraped_at TIMESTAMPTZ
);
```

### intelligence_metrics
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
  raw_data JSONB
);
```

## Porting Guide

To port this feature to another app (e.g., Creator):

### 1. Service File Template

Create `apps/[app]/src/services/intelligenceService.ts`:

```typescript
import { supabase } from '@/integrations/supabase/client';

const FUNCTION_URL = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/title-intelligence`;

export interface CollectionRequest {
  urls: Array<{
    platform: string;
    platformId: string;
    originalUrl: string;
  }>;
  collectedBy: string;
  contentType: 'webtoon' | 'webnovel';
  fanEngagement?: {
    titleName: string;
    sources: string[];
  };
}

export interface CollectionResult {
  success: boolean;
  sources: Array<{
    platform: string;
    metrics: {
      views: number;
      subscribers: number;
      rating: number;
      episodes: number;
    };
  }>;
  error?: string;
}

export async function collectTitleData(request: CollectionRequest): Promise<CollectionResult> {
  const { data: { session } } = await supabase.auth.getSession();

  const response = await fetch(FUNCTION_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${session?.access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(request)
  });

  return response.json();
}

export function parseplatformUrl(url: string): { platform: string; platformId: string } | null {
  // Naver Webtoon
  if (url.includes('comic.naver.com')) {
    const match = url.match(/titleId=(\d+)/);
    if (match) return { platform: 'naver_webtoon', platformId: match[1] };
  }

  // Kakao Page
  if (url.includes('page.kakao.com')) {
    const match = url.match(/content\/(\d+)/);
    if (match) return { platform: 'kakao_page', platformId: match[1] };
  }

  // Manta
  if (url.includes('manta.net')) {
    const match = url.match(/series\/(\d+)/);
    if (match) return { platform: 'manta', platformId: match[1] };
  }

  return null;
}
```

### 2. UI Component Template

Create `apps/[app]/src/components/CollectDataButton.tsx`:

```typescript
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { collectTitleData, parseplatformUrl } from '@/services/intelligenceService';
import { Database } from 'lucide-react';

interface Props {
  titleUrl: string;
  titleId: string;
  onSuccess?: (metrics: any) => void;
}

export function CollectDataButton({ titleUrl, titleId, onSuccess }: Props) {
  const [loading, setLoading] = useState(false);

  const handleCollect = async () => {
    const parsed = parseplatformUrl(titleUrl);
    if (!parsed) {
      toast.error('Unable to parse platform URL');
      return;
    }

    setLoading(true);
    try {
      const result = await collectTitleData({
        urls: [{
          platform: parsed.platform,
          platformId: parsed.platformId,
          originalUrl: titleUrl
        }],
        collectedBy: 'user',
        contentType: 'webtoon'
      });

      if (result.success) {
        toast.success('Data collected successfully');
        onSuccess?.(result.sources[0]?.metrics);
      } else {
        toast.error(result.error || 'Collection failed');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={handleCollect}
      disabled={loading}
    >
      <Database className="w-4 h-4 mr-2" />
      {loading ? 'Collecting...' : 'Collect Data'}
    </Button>
  );
}
```

### 3. Integration Points

- Add button next to URL input fields
- Wire up to title edit form
- Handle metrics update in parent component

## Related Skills

- `/batch-comps` - Run after collecting data for better comps
- `/batch-format-fit` - Run after collecting data for format analysis
- `/title-pipeline` - Orchestrate full data → analysis workflow
- `/regenerate-embeddings` - Regenerate embeddings after data update
