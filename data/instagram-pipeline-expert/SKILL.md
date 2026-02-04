---
name: instagram-pipeline-expert
description: Expert knowledge on Instagram search providers (Serper vs Apify), rate limiting, data normalization, and cost optimization. Use this skill when user asks about "instagram search", "serper", "apify", "scraping instagram", "provider selection", "instagram pipeline", "instagram reels", or "normalize creators".
allowed-tools: Read, Grep, Glob
---

# Instagram Pipeline Expert

You are an expert in the Instagram US Reels search pipeline for this influencer discovery platform. This skill provides comprehensive knowledge about search providers, rate limits, normalization logic, and cost optimization strategies.

## When To Use This Skill

This skill activates when users:
- Ask about Instagram search functionality or providers
- Need to compare Serper vs Apify for Instagram scraping
- Debug issues with Instagram creator discovery
- Want to understand rate limiting and cost optimization
- Need help with creator data normalization
- Work on Instagram US Reels pipeline improvements
- Troubleshoot duplicate creators or missing data

## Core Knowledge

### Provider Comparison: Serper vs Apify

**Serper (Primary Provider)**
- **Use Case**: Lightweight handle discovery via Google Search
- **Endpoint**: `https://google.serper.dev/search`
- **Cost**: ~$0.001 per search query
- **Rate Limit**: ~100 requests/second
- **Response Time**: 1-3 seconds
- **Data Quality**: Returns Instagram URLs from Google SERP
- **Best For**: Initial handle discovery, keyword expansion

**Key Implementation:**
```typescript
// lib/instagram-us-reels/clients/serper.ts
const SERPER_ENDPOINT = 'https://google.serper.dev/search';

export async function fetchSerperHandles(
  params: SerperHandleParams,
  options: SerperOptions = {},
): Promise<string[]> {
  const apiKey = resolveSerperKey(options);
  const body = {
    q: params.query,
    location: params.location ?? 'United States',
    gl: params.gl ?? 'us',
    hl: params.hl ?? 'en',
    num: Math.min(Math.max(params.num ?? 10, 1), 20),
  };

  const response = await fetch(SERPER_ENDPOINT, {
    method: 'POST',
    headers: {
      'X-API-KEY': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(15000),
  });

  // Extract handles from organic results
  const payload = await response.json();
  const organic = Array.isArray(payload?.organic) ? payload.organic : [];

  for (const entry of organic) {
    push(extractInstagramHandle(entry?.link ?? ''));
  }

  return handles.slice(0, body.num);
}
```

**Apify (Legacy/Alternative Provider)**
- **Use Case**: Deep profile scraping with full metadata
- **Cost**: ~$0.01-0.05 per profile
- **Rate Limit**: Actor-dependent, typically 10-50 concurrent runs
- **Response Time**: 10-60 seconds per profile
- **Data Quality**: Complete profile data including bio, followers, engagement
- **Best For**: Deep enrichment after handle discovery

**Apify is NOT currently active in the main pipeline but available in:**
- `/lib/platforms/instagram-similar/api.ts`
- `/scripts/test-apify-instagram-*.js`

### Rate Limit Handling

**Serper Rate Limits:**
- **Limit**: 100 requests/second, 2500 requests/month (free tier)
- **Strategy**: Sequential keyword processing with fair distribution
- **Implementation**: `/lib/instagram-us-reels/index.ts`

```typescript
// Sequential processing to avoid rate limits
for (const kw of keywords) {
  const handles = await fetchSerperHandles({
    query: `site:instagram.com "${kw}" reels`,
    num: Math.min(resultsPerKeyword, 20)
  });

  // Rate limit pause between keywords
  if (i < keywords.length - 1) {
    await sleep(config.keywordDelayMs);
  }
}
```

**Best Practices:**
1. **Batch Processing**: Process keywords sequentially, not in parallel
2. **Exponential Backoff**: Retry with increasing delays on 429 errors
3. **Circuit Breaker**: Stop processing after N consecutive failures
4. **Fair Distribution**: Distribute results evenly across keywords

### Creator Normalization Logic

The pipeline normalizes creator data from multiple sources into a unified format.

**Normalization File:** `/lib/instagram-us-reels/utils/creator-normalizer.ts`

**Key Fields:**
```typescript
interface NormalizedCreator {
  username: string;           // Primary identifier
  displayName?: string;       // Full name
  platform: 'instagram';
  profileUrl: string;         // https://instagram.com/{username}
  avatarUrl?: string;
  followers?: number;
  isVerified?: boolean;
  bio?: string;
  email?: string;

  // Search metadata
  source: 'serper' | 'apify' | 'scrapecreators';
  keyword?: string;           // Which keyword found this creator
  searchScore?: number;       // Relevance score
}
```

**Duplicate Detection:**
```typescript
// Deduplication by username
const seen = new Set<string>();
const dedupedCreators = creators.filter(c => {
  const key = c.username.toLowerCase();
  if (seen.has(key)) return false;
  seen.add(key);
  return true;
});
```

**Handle Extraction from URLs:**
```typescript
const DISALLOWED_SEGMENTS = new Set([
  'p', 'reel', 'reels', 'tv', 'explore', 'tags', 'tag',
  'directory', 'accounts', 'about', 'legal', 'privacy',
  'developers', 'business', 'topics', 'guide', 'stories'
]);

function extractInstagramHandle(url: string): string | null {
  const parsed = new URL(url);
  if (!parsed.hostname.includes('instagram.com')) return null;

  const segments = parsed.pathname.split('/').filter(Boolean);
  const handle = segments[0]?.replace('@', '').trim();

  if (!handle || handle.length > 50) return null;
  if (!/^[a-z0-9._]+$/i.test(handle)) return null;
  if (DISALLOWED_SEGMENTS.has(handle.toLowerCase())) return null;

  return handle.toLowerCase();
}
```

### Cost Optimization Strategies

**Cost Breakdown:**
- Serper: $0.001/query x 10 keywords = $0.01 per search job
- Apify: $0.03/profile x 1000 profiles = $30 per deep enrichment

**Optimization Techniques:**

1. **Keyword Expansion (Cheap)**
   - Use GPT-4o-mini to expand 1 keyword → 10 keywords
   - Cost: $0.0001 per expansion
   - File: `/lib/instagram-us-reels/steps/keyword-expansion.ts`

2. **Handle Discovery (Serper)**
   - 10-20 handles per keyword
   - Cost: $0.001 per keyword
   - Total: $0.01 for 10 keywords

3. **Profile Screening (ScapeCreators)**
   - Filter handles before deep enrichment
   - Cost: $0.005 per profile check
   - Saves money by avoiding Apify for irrelevant profiles

4. **Lazy Enrichment**
   - Enrich only when user clicks on creator
   - Reduces upfront costs by 90%

**Example Cost Calculation:**
```
Search Job: "fitness influencers"
├─ Keyword Expansion: $0.0001 (1 keyword → 10)
├─ Handle Discovery: $0.01 (10 Serper queries)
├─ Profile Screening: $0 (not implemented yet)
└─ Total: $0.0101 per search job

With 1000 results target:
- Current: ~$0.01 per job
- With Apify: ~$30 per job (300x more expensive)
```

## Common Patterns

### Pattern 1: Sequential Keyword Processing

```typescript
// Good: Sequential processing with rate limiting
async function processKeywordsSequentially(keywords: string[]) {
  const allHandles: string[] = [];

  for (let i = 0; i < keywords.length; i++) {
    const kw = keywords[i];

    try {
      const handles = await fetchSerperHandles({
        query: `site:instagram.com "${kw}" reels`,
        num: 20
      });

      allHandles.push(...handles);

      // Rate limit pause between keywords
      if (i < keywords.length - 1) {
        await sleep(2000); // 2 second delay
      }
    } catch (error) {
      console.error(`Failed to fetch handles for "${kw}":`, error);
      // Continue with next keyword
    }
  }

  return allHandles;
}
```

**When to use**: Always for Serper queries to respect rate limits

### Pattern 2: Fair Result Distribution

```typescript
// Good: Distribute results evenly across keywords
function distributeFairly(keywords: string[], targetResults: number) {
  const basePerKeyword = Math.floor(targetResults / keywords.length);
  const remainder = targetResults % keywords.length;

  return keywords.map((kw, i) => ({
    keyword: kw,
    limit: basePerKeyword + (i < remainder ? 1 : 0)
  }));
}

// Example: 100 results across 7 keywords
// Results: [15, 15, 14, 14, 14, 14, 14]
```

**When to use**: When processing multiple keywords to ensure balanced coverage

### Pattern 3: Handle Validation

```typescript
// Good: Validate handles before processing
function isValidHandle(handle: string): boolean {
  if (!handle || handle.length > 50) return false;
  if (!/^[a-z0-9._]+$/i.test(handle)) return false;
  if (DISALLOWED_SEGMENTS.has(handle.toLowerCase())) return false;
  return true;
}

const validHandles = rawHandles.filter(isValidHandle);
```

**When to use**: Always after extracting handles from URLs

## Anti-Patterns (Avoid These)

### Anti-Pattern 1: Parallel Serper Requests

```typescript
// BAD: Parallel requests will hit rate limits
const promises = keywords.map(kw =>
  fetchSerperHandles({ query: kw, num: 20 })
);
const results = await Promise.all(promises);
```

**Why it's bad**: Exceeds Serper's 100 req/sec limit, causes 429 errors

**Do this instead**:
```typescript
// GOOD: Sequential processing
const results = [];
for (const kw of keywords) {
  const handles = await fetchSerperHandles({ query: kw, num: 20 });
  results.push(handles);
  await sleep(1000); // Rate limit pause
}
```

### Anti-Pattern 2: Using Apify for Discovery

```typescript
// BAD: Expensive and slow for initial discovery
const profiles = await apifyClient.call('instagram-profile-scraper', {
  usernames: allHandles // 1000 handles
});
// Cost: $30-50, Time: 30+ minutes
```

**Why it's bad**: 300x more expensive than Serper, much slower

**Do this instead**:
```typescript
// GOOD: Use Serper for discovery, Apify for enrichment
const handles = await fetchSerperHandles({ query: keyword });
// Cost: $0.001, Time: 2 seconds

// Only enrich when user clicks
if (userClickedOnCreator) {
  const profile = await apifyClient.call('instagram-profile-scraper', {
    username: creator.username
  });
}
```

### Anti-Pattern 3: No Handle Validation

```typescript
// BAD: Processing invalid handles wastes API calls
const handles = urls.map(url => url.split('/').pop());
const profiles = await fetchProfiles(handles);
```

**Why it's bad**: Wasting API calls on URLs like `/p/abc123`, `/reel/xyz789`

**Do this instead**:
```typescript
// GOOD: Validate handles first
const handles = urls
  .map(extractInstagramHandle)
  .filter(Boolean)
  .filter(isValidHandle);
const profiles = await fetchProfiles(handles);
```

## Troubleshooting Guide

### Problem: Duplicate Creators in Results

**Symptoms:**
- Same username appears multiple times
- Different keywords return same creators
- Result count doesn't match unique creators

**Diagnosis:**
1. Check if deduplication is running:
   ```typescript
   // Look for this in the pipeline
   const uniqueCreators = dedupeCreators(allCreators);
   ```
2. Verify username normalization (lowercase)
3. Check if keywords are too similar

**Solution:**
```typescript
// lib/utils/dedupe-creators.ts
import { dedupeCreators } from '@/lib/utils/dedupe-creators';

const dedupedCreators = dedupeCreators(creators, {
  by: 'username', // or 'profileUrl'
  keepFirst: true // Keep first occurrence
});
```

### Problem: Rate Limit Errors (429)

**Symptoms:**
- `Error: Serper error 429: Rate limit exceeded`
- Jobs failing after first few keywords
- Inconsistent results

**Diagnosis:**
1. Check if parallel requests are being made
2. Verify delay between keywords
3. Check Serper dashboard for quota usage

**Solution:**
```typescript
// Add exponential backoff
async function fetchWithRetry(params: SerperHandleParams, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fetchSerperHandles(params);
    } catch (error) {
      if (error.message.includes('429') && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await sleep(delay);
        continue;
      }
      throw error;
    }
  }
}
```

### Problem: Missing Creator Data

**Symptoms:**
- Creators have no bio or follower count
- Profile URLs are invalid
- Avatar images missing

**Diagnosis:**
1. Check which provider returned the data
2. Verify normalization is running
3. Look for null/undefined fields in raw data

**Solution:**
```typescript
// Normalize with fallbacks
function normalizeCreator(raw: any): NormalizedCreator {
  return {
    username: raw.username || raw.handle || 'unknown',
    displayName: raw.displayName || raw.fullName || raw.username,
    profileUrl: raw.profileUrl || `https://instagram.com/${raw.username}`,
    avatarUrl: raw.avatarUrl || raw.profilePicUrl || null,
    followers: parseInt(raw.followers) || 0,
    isVerified: raw.isVerified || raw.verified || false,
    bio: raw.bio || raw.biography || null,
    platform: 'instagram',
    source: raw.source || 'unknown'
  };
}
```

### Problem: Search Returns No Results

**Symptoms:**
- Empty array returned
- "No creators found" message
- Job completes but 0 results

**Diagnosis:**
1. Test query directly in Google: `site:instagram.com "keyword" reels`
2. Check if keyword is too specific
3. Verify Serper API key is valid
4. Look for errors in logs

**Solution:**
```typescript
// Add keyword validation and expansion
async function searchWithFallback(keyword: string) {
  // Try exact keyword first
  let handles = await fetchSerperHandles({ query: keyword });

  if (handles.length === 0) {
    // Try broader search
    const broader = keyword.split(' ')[0]; // First word only
    handles = await fetchSerperHandles({ query: broader });
  }

  if (handles.length === 0) {
    // Try without site: filter
    handles = await fetchSerperHandles({
      query: `${keyword} instagram influencer`
    });
  }

  return handles;
}
```

## Related Files

Understand these files to work with the Instagram pipeline:

- `/lib/instagram-us-reels/clients/serper.ts` - Serper API client
- `/lib/instagram-us-reels/index.ts` - Main pipeline orchestration
- `/lib/instagram-us-reels/steps/keyword-expansion.ts` - GPT-4 keyword expansion
- `/lib/instagram-us-reels/utils/creator-normalizer.ts` - Data normalization
- `/lib/platforms/instagram-similar/api.ts` - Apify integration (legacy)
- `/lib/utils/dedupe-creators.ts` - Deduplication logic
- `/scripts/test-both-hashtag-scrapers.js` - Provider comparison script
- `/scripts/quick-test-instagram-apis.js` - Manual testing script

## Testing & Validation

**Test Serper Directly:**
```bash
curl -X POST 'https://google.serper.dev/search' \
  -H 'X-API-KEY: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "q": "site:instagram.com \"fitness\" reels",
    "num": 10,
    "gl": "us"
  }'
```

**Test Full Pipeline:**
```bash
node scripts/quick-test-instagram-apis.js
```

**Expected Results:**
- 10-20 handles per keyword
- <3 seconds per Serper query
- 90%+ valid handles after filtering
- No duplicates in final results

## Performance Benchmarks

**Typical Search Job (10 keywords, 1000 results target):**
- Keyword Expansion: 2-5 seconds
- Handle Discovery: 20-30 seconds (10 Serper queries)
- Deduplication: <1 second
- Total: 25-40 seconds
- Cost: ~$0.01

**Comparison (1000 Instagram Profiles):**
| Provider | Time | Cost | Data Quality |
|----------|------|------|--------------|
| Serper | 30s | $0.01 | Handles only |
| Apify | 30min | $30 | Full profiles |
| ScapeCreators | 5min | $5 | Basic profiles |

## Additional Resources

- [Serper.dev Documentation](https://serper.dev/docs)
- [Apify Instagram Scrapers](https://apify.com/store?search=instagram)
- Internal: `/instagram-us-reels-search/` directory (archived docs)
