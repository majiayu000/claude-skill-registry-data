---
name: indexnow
description: Work with IndexNow SEO submissions for myimageupscaler.com, including submitting changed URLs, batch submissions, key file setup, API route checks, CLI scripts, tests, and debugging indexing notifications.
---

# IndexNow SEO Skill

Use this skill when you need to submit URLs to IndexNow for faster search engine indexing. IndexNow is a protocol that instantly notifies search engines about content changes.

## When to Use

- After publishing new blog posts or pages
- After making significant content updates
- When running bulk URL submission campaigns
- When setting up IndexNow for the first time
- When debugging IndexNow integration issues

## Overview

- **Library**: `lib/seo/indexnow.ts` - Core IndexNow functions
- **API Route**: `app/api/seo/indexnow/route.ts` - Protected API endpoint
- **Scripts**:
  - `scripts/submit-indexnow.ts` - CLI for batch submission
  - `scripts/create-indexnow-keyfile.ts` - Generate key file
- **Tests**: `tests/seo/indexnow.test.ts`

## Key Components

### Environment Configuration

Add to `.env.api`:

```bash
# Generate with: tsx scripts/submit-indexnow.ts --generate-key
INDEXNOW_KEY=your32characterkeyhere
```

### Library Functions

```typescript
import {
  submitUrl,
  submitBatch,
  submitFromCSV,
  getSubmissionStatus,
  generateIndexNowKey,
  validateIndexNowKey,
  getKeyFileContent,
} from '@lib/seo/indexnow';

// Submit single URL
const result = await submitUrl('https://myimageupscaler.com/blog/new-post');

// Submit batch
const result = await submitBatch(
  ['https://myimageupscaler.com/blog/post-1', 'https://myimageupscaler.com/blog/post-2'],
  { batchSize: 100, delayMs: 1000 }
);

// Submit from CSV
const csvContent = await fs.readFile('./urls.csv', 'utf-8');
const result = await submitFromCSV(csvContent);

// Check status
const status = await getSubmissionStatus();

// Generate new key
const key = generateIndexNowKey(32);
```

### API Endpoint

Protected by `x-cron-secret` header (uses CRON_SECRET from env).

```bash
# GET - Check status
curl -H "x-cron-secret: $CRON_SECRET" \
  https://myimageupscaler.com/api/seo/indexnow

# POST - Submit single URL
curl -X POST \
  -H "x-cron-secret: $CRON_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://myimageupscaler.com/blog/new-post"}' \
  https://myimageupscaler.com/api/seo/indexnow

# POST - Submit batch
curl -X POST \
  -H "x-cron-secret: $CRON_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://myimageupscaler.com/page1","https://myimageupscaler.com/page2"]}' \
  https://myimageupscaler.com/api/seo/indexnow
```

### CLI Scripts

```bash
# Generate new key and see instructions
tsx scripts/submit-indexnow.ts --generate-key

# Check configuration status
tsx scripts/submit-indexnow.ts --status

# Submit single URL
tsx scripts/submit-indexnow.ts --single https://myimageupscaler.com/blog/post

# Submit from CSV
tsx scripts/submit-indexnow.ts --csv ./urls.csv

# Create key verification file in public/
tsx scripts/create-indexnow-keyfile.ts abc123def456
# or
tsx scripts/create-indexnow-keyfile.ts --generate
```

## Setup Checklist

1. **Generate IndexNow Key**

   ```bash
   tsx scripts/submit-indexnow.ts --generate-key
   ```

2. **Add to environment**

   ```bash
   # .env.api
   INDEXNOW_KEY=your32characterkeyhere
   ```

3. **Create verification file**

   ```bash
   tsx scripts/create-indexnow-keyfile.ts $INDEXNOW_KEY
   ```

   This creates `public/{key}.txt` which is accessible at `https://myimageupscaler.com/{key}.txt`

4. **Verify setup**

   ```bash
   tsx scripts/submit-indexnow.ts --status
   ```

5. **Test submission**
   ```bash
   tsx scripts/submit-indexnow.ts --single https://myimageupscaler.com/
   ```

## IndexNow Response Codes

| Status | Meaning                    |
| ------ | -------------------------- |
| 200    | URL submitted successfully |
| 202    | URL received (duplicate)   |
| 400    | Invalid format             |
| 403    | Key not valid              |
| 422    | URLs not from host         |
| 429    | Rate limited               |

## Batch Submission Options

```typescript
interface IIndexNowBatchOptions {
  batchSize?: number; // Default: 1000, max: 10000
  delayMs?: number; // Delay between batches, default: 1000ms
  signal?: AbortSignal; // For cancellation
}
```

## Integration Points

### After Blog Post Publish

```typescript
// In blog publish workflow
await submitUrl(`https://myimageupscaler.com/blog/${slug}`);
```

### After Sitemap Generation

```typescript
// After generating new sitemap
const urls = await getAllPSEOPages().map(p => p.url);
await submitBatch(urls);
```

### Cron Job for New Pages

```typescript
// In a cron job that tracks new pages
const newPageUrls = await getNewlyCreatedPageUrls();
if (newPageUrls.length > 0) {
  await submitBatch(newPageUrls);
}
```

## Search Engines Supported

IndexNow is supported by:

- Bing (Microsoft) - Primary endpoint used
- Yandex
- Naver
- Seznam.cz
- Yep

Note: Google has its own submission API but also monitors IndexNow submissions.

## Troubleshooting

### "INDEXNOW_KEY not configured"

- Ensure `INDEXNOW_KEY` is set in `.env.api`
- Restart the server after changing env vars

### "Key not valid" (403)

- Verify the key file exists at `public/{key}.txt`
- Check the key file content matches the INDEXNOW_KEY value
- Ensure the file is deployed (not gitignored)

### Rate Limited (429)

- Add delays between batch submissions
- Use smaller batch sizes
- Wait and retry with exponential backoff

## Key Files

- `lib/seo/indexnow.ts` - Core implementation
- `lib/seo/index.ts` - Exports IndexNow functions
- `app/api/seo/indexnow/route.ts` - API endpoint
- `scripts/submit-indexnow.ts` - CLI tool
- `scripts/create-indexnow-keyfile.ts` - Key file generator
- `tests/seo/indexnow.test.ts` - Unit tests
- `shared/config/env.ts` - INDEXNOW_KEY definition
- `shared/config/security.ts` - /api/seo/\* in PUBLIC_API_ROUTES

## Commands

```bash
# Run IndexNow tests
npx vitest run tests/seo/indexnow.test.ts

# Generate key
tsx scripts/submit-indexnow.ts --generate-key

# Check status
tsx scripts/submit-indexnow.ts --status

# Submit URL
tsx scripts/submit-indexnow.ts --single <url>
```
