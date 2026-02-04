---
name: qstash-job-processing
description: Expert knowledge on QStash async job processing, job lifecycle (pending → processing → completed/error), retry logic, timeout handling, continuation scheduling, and debugging stuck jobs. Use this skill when user asks about "qstash", "async job", "background job", "search processing", "stuck job", "job status", or "continuation".
allowed-tools: Read, Grep, Bash
---

# QStash Job Processing Expert

You are an expert in QStash-based asynchronous job processing for this platform. This skill provides knowledge about job lifecycle, retry logic, continuation patterns, and troubleshooting stuck jobs.

## When To Use This Skill

This skill activates when users:
- Work with QStash job scheduling
- Debug stuck or timeout jobs
- Implement continuation logic for long-running searches
- Understand job status transitions
- Need retry and error handling patterns
- Investigate job processing delays
- Optimize job throughput

## Core Knowledge

### Job Lifecycle

**States:**
- `pending` - Job created, waiting to start
- `processing` - Job actively running
- `completed` - Job finished successfully
- `error` - Job failed with error
- `timeout` - Job exceeded time limit

**State Transitions:**
```
pending → processing → completed
               ↓
            error
               ↓
            timeout
```

**Job Table:** `/lib/db/schema.ts`
```typescript
scraping_jobs {
  id: uuid
  userId: text
  status: 'pending' | 'processing' | 'completed' | 'error' | 'timeout'
  qstashMessageId: text
  processedRuns: integer
  processedResults: integer
  targetResults: integer
  timeoutAt: timestamp
  createdAt: timestamp
  startedAt: timestamp
  completedAt: timestamp
  error: text
}
```

### QStash Integration

**Client:** `/lib/queue/qstash.ts`
```typescript
import { Client } from '@upstash/qstash';

export const qstash = new Client({
  token: process.env.QSTASH_TOKEN!
});
```

**Publishing Job:**
```typescript
import { qstash } from '@/lib/queue/qstash';
import { getWebhookUrl } from '@/lib/utils/url-utils';

// Schedule job
await qstash.publishJSON({
  url: `${getWebhookUrl()}/api/qstash/process-search`,
  body: { jobId: job.id },
  delay: '5s', // Optional delay
  retries: 3, // Automatic retries
  notifyOnFailure: true
});
```

**Receiving Job:** `/app/api/qstash/process-search/route.ts`
```typescript
import { Receiver } from '@upstash/qstash';

const receiver = new Receiver({
  currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
  nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
});

export async function POST(req: Request) {
  // 1. Verify signature
  const rawBody = await req.text();
  const signature = req.headers.get('Upstash-Signature');

  if (shouldVerifySignature()) {
    const valid = await receiver.verify({
      signature,
      body: rawBody,
      url: callbackUrl
    });
    if (!valid) {
      return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
    }
  }

  // 2. Parse body
  const { jobId } = JSON.parse(rawBody);

  // 3. Process job
  const execution = await runSearchJob(jobId);

  // 4. Schedule continuation if needed
  if (execution.result.hasMore) {
    await qstash.publishJSON({
      url: callbackUrl,
      body: { jobId },
      delay: '10s'
    });
  }

  return NextResponse.json({ status: execution.result.status });
}
```

### Continuation Pattern

**For Long-Running Jobs:**

Instagram US Reels searches target 1000 results but can only fetch 20 per API call. Continuation pattern allows job to process in chunks.

```typescript
// In job processor
export async function runSearchJob(jobId: string) {
  const service = await SearchJobService.load(jobId);
  const snapshot = service.snapshot();

  // Check if job is complete
  if (snapshot.processedResults >= snapshot.targetResults) {
    await service.complete('completed', {});
    return { status: 'completed', hasMore: false };
  }

  // Process one batch (e.g., 20 results)
  const results = await fetchNextBatch(snapshot);

  await service.recordResults(results);

  // Check if more work needed
  const hasMore = snapshot.processedResults < snapshot.targetResults;

  if (!hasMore) {
    await service.complete('completed', {});
  }

  return { status: 'processing', hasMore };
}

// In QStash handler
if (execution.result.hasMore) {
  await qstash.publishJSON({
    url: callbackUrl,
    body: { jobId },
    delay: `${config.continuationDelayMs}ms`, // e.g., 10000ms = 10s
    retries: 3
  });
}
```

**Configuration:**
```typescript
{
  continuationDelayMs: 10000, // 10 seconds between batches
  maxRuns: 50, // Stop after 50 continuations
  batchSize: 20, // Results per batch
  timeout: 300000 // 5 minutes per batch
}
```

### Retry Logic

**QStash Automatic Retries:**
- Configurable via `retries` parameter
- Exponential backoff between retries
- Retry on 5xx errors only

```typescript
await qstash.publishJSON({
  url: callbackUrl,
  body: { jobId },
  retries: 3, // Will retry 3 times on failure
  notifyOnFailure: true
});
```

**Manual Retry in Handler:**
```typescript
export async function POST(req: Request) {
  try {
    const { jobId } = JSON.parse(await req.text());
    const execution = await runSearchJob(jobId);

    return NextResponse.json({ status: execution.result.status });
  } catch (error) {
    logger.error('Job failed', error, { jobId });

    // Mark job as error
    try {
      const service = await SearchJobService.load(jobId);
      await service.complete('error', { error: error.message });
    } catch (completionError) {
      logger.error('Failed to mark job as error', completionError);
    }

    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
```

### Timeout Handling

**Setting Timeout:**
```typescript
import { db } from '@/lib/db';
import { scrapingJobs } from '@/lib/db/schema';

// When creating job
const timeoutAt = new Date(Date.now() + 5 * 60 * 1000); // 5 minutes

const [job] = await db.insert(scrapingJobs)
  .values({
    userId,
    status: 'pending',
    timeoutAt,
    targetResults: 1000
  })
  .returning();
```

**Checking for Timeout:**
```typescript
export async function runSearchJob(jobId: string) {
  const service = await SearchJobService.load(jobId);
  const snapshot = service.snapshot();

  // Check timeout
  if (snapshot.timeoutAt && new Date() > new Date(snapshot.timeoutAt)) {
    await service.complete('timeout', { error: 'Job exceeded timeout limit' });
    throw new Error('Job timeout');
  }

  // Process job...
}
```

**Timeout Cleanup Job (Scheduled):**
```typescript
// Run every 5 minutes
export async function cleanupTimeoutJobs() {
  const timeoutJobs = await db.query.scrapingJobs.findMany({
    where: and(
      eq(scrapingJobs.status, 'processing'),
      lt(scrapingJobs.timeoutAt, new Date())
    )
  });

  for (const job of timeoutJobs) {
    await db.update(scrapingJobs)
      .set({ status: 'timeout', error: 'Job timeout', completedAt: new Date() })
      .where(eq(scrapingJobs.id, job.id));
  }
}
```

## Common Patterns

### Pattern 1: Idempotent Job Processing

```typescript
// Good: Check if already processed
export async function POST(req: Request) {
  const { jobId } = JSON.parse(await req.text());

  const service = await SearchJobService.load(jobId);
  const snapshot = service.snapshot();

  // Skip if already completed or error
  if (snapshot.status === 'completed' || snapshot.status === 'error') {
    return NextResponse.json({
      status: snapshot.status,
      message: 'Job already processed'
    });
  }

  // Process job...
}
```

**When to use**: Always, to handle duplicate QStash deliveries

### Pattern 2: Progress Tracking

```typescript
// Good: Update progress as job runs
export async function runSearchJob(jobId: string) {
  const service = await SearchJobService.load(jobId);

  while (service.snapshot().processedResults < service.snapshot().targetResults) {
    const batch = await fetchNextBatch();

    await service.recordResults(batch);

    // Update progress
    const progress = (service.snapshot().processedResults / service.snapshot().targetResults) * 100;
    await db.update(scrapingJobs)
      .set({ progress: progress.toFixed(2) })
      .where(eq(scrapingJobs.id, jobId));

    logger.info('Job progress', {
      jobId,
      progress: `${progress.toFixed(1)}%`
    });
  }
}
```

**When to use**: Long-running jobs where users need visibility

### Pattern 3: Exponential Backoff Continuation

```typescript
// Good: Increase delay for rate-limited APIs
const baseDelay = 10000; // 10 seconds
const run = service.snapshot().processedRuns;
const delay = Math.min(baseDelay * Math.pow(1.5, run), 60000); // Max 60s

await qstash.publishJSON({
  url: callbackUrl,
  body: { jobId },
  delay: `${delay}ms`
});
```

**When to use**: APIs with aggressive rate limits

## Anti-Patterns (Avoid These)

### Anti-Pattern 1: No Continuation Limit

```typescript
// BAD: Infinite continuation loop
if (hasMoreResults) {
  await qstash.publishJSON({ url: callbackUrl, body: { jobId } });
}
```

**Why it's bad**: Job never stops, wastes resources, costs money

**Do this instead:**
```typescript
// GOOD: Limit continuations
const MAX_RUNS = 50;
if (hasMoreResults && service.snapshot().processedRuns < MAX_RUNS) {
  await qstash.publishJSON({ url: callbackUrl, body: { jobId } });
} else {
  await service.complete('completed', { reason: 'Max runs reached' });
}
```

### Anti-Pattern 2: Updating Status to Completed on Error

```typescript
// BAD: Masking errors
try {
  await runSearchJob(jobId);
} catch (error) {
  // Still marks as completed!
  await service.complete('completed', {});
}
```

**Why it's bad**: Users think job succeeded when it failed

**Do this instead:**
```typescript
// GOOD: Preserve error status
try {
  await runSearchJob(jobId);
  await service.complete('completed', {});
} catch (error) {
  await service.complete('error', { error: error.message });
}
```

### Anti-Pattern 3: No Signature Verification

```typescript
// BAD: Accepting unauthenticated requests
export async function POST(req: Request) {
  const { jobId } = await req.json();
  await runSearchJob(jobId); // Anyone can trigger this!
}
```

**Why it's bad**: Anyone can forge requests and run expensive jobs

**Do this instead:**
```typescript
// GOOD: Verify QStash signature
const signature = req.headers.get('Upstash-Signature');
if (!signature) {
  return NextResponse.json({ error: 'Missing signature' }, { status: 401 });
}

const valid = await receiver.verify({ signature, body: rawBody, url: callbackUrl });
if (!valid) {
  return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
}
```

## Troubleshooting Guide

### Problem: Job Stuck in "processing"

**Symptoms:**
- Job status is "processing" for hours
- No new results added
- No error logged

**Diagnosis:**
1. Check QStash dashboard for failed deliveries
2. Look for errors in application logs
3. Check if continuation was scheduled
4. Verify job hasn't timed out

**Solution:**
```bash
# 1. Inspect job state
node scripts/inspect-user-state.js --email user@example.com

# 2. Check job details manually
curl http://localhost:3000/api/jobs/{jobId} \
  -H "x-dev-auth: dev-bypass"

# 3. Manually complete job if truly stuck
# Use debug endpoint or database update
```

### Problem: Jobs Not Processing

**Symptoms:**
- Jobs stay in "pending" status
- QStash webhook never fires
- No logs from job processor

**Diagnosis:**
1. Verify QStash credentials are set
2. Check if webhook URL is accessible
3. Look for signature verification failures
4. Check QStash dashboard for delivery errors

**Solution:**
```bash
# 1. Verify environment variables
echo $QSTASH_TOKEN
echo $QSTASH_CURRENT_SIGNING_KEY
echo $QSTASH_NEXT_SIGNING_KEY

# 2. Test webhook locally with ngrok
ngrok http 3000
# Update NEXT_PUBLIC_SITE_URL to ngrok URL

# 3. Manually trigger job
curl -X POST http://localhost:3000/api/qstash/process-search \
  -H "Content-Type: application/json" \
  -d '{"jobId":"xxx-xxx-xxx"}'
```

### Problem: Continuation Loop

**Symptoms:**
- Job runs 100+ times
- Never completes
- `processedRuns` keeps increasing

**Diagnosis:**
1. Check if `hasMore` logic is correct
2. Verify target results are achievable
3. Look for off-by-one errors

**Solution:**
```typescript
// Add max runs check
const MAX_RUNS = 50;
const needsContinuation =
  result.status !== 'error' &&
  result.hasMore &&
  snapshot.processedRuns < MAX_RUNS &&
  snapshot.processedResults < snapshot.targetResults;

if (!needsContinuation) {
  await service.complete('completed', {
    reason: snapshot.processedRuns >= MAX_RUNS ? 'Max runs reached' : 'Target met'
  });
}
```

## Related Files

- `/lib/queue/qstash.ts` - QStash client
- `/lib/search-engine/runner.ts` - Search job runner
- `/lib/search-engine/job-service.ts` - Job state management
- `/app/api/qstash/process-search/route.ts` - Job processor endpoint
- `/app/api/qstash/process-results/route.ts` - Results processor
- `/app/api/jobs/[id]/route.ts` - Job status endpoint
- `/scripts/debug/job/route.ts` - Debug script

## Testing QStash Jobs

**Test Locally:**
```bash
# 1. Skip signature verification
export SKIP_QSTASH_SIGNATURE=true

# 2. Trigger job manually
curl -X POST http://localhost:3000/api/qstash/process-search \
  -H "Content-Type: application/json" \
  -d '{"jobId":"your-job-id"}'

# 3. Check job status
curl http://localhost:3000/api/jobs/your-job-id \
  -H "x-dev-auth: dev-bypass"
```

**Test with ngrok:**
```bash
# 1. Start ngrok
ngrok http 3000

# 2. Update .env.local
NEXT_PUBLIC_SITE_URL=https://your-id.ngrok.io
VERIFY_QSTASH_SIGNATURE=true

# 3. Create job via API (will auto-schedule QStash)
curl -X POST http://localhost:3000/api/scraping/instagram-us-reels \
  -H "x-dev-auth: dev-bypass" \
  -H "Content-Type: application/json" \
  -d '{"keywords":["fitness"],"targetResults":100}'
```

**Expected Behavior:**
1. Job created with status "pending"
2. QStash webhook fires within 5-10 seconds
3. Status changes to "processing"
4. Results accumulate over time
5. Continuation scheduled if needed
6. Status changes to "completed" when target met
