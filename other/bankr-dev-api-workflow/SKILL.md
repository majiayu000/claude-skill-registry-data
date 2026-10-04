---
name: Bankr Dev - API Workflow
description: This skill should be used when building the async job workflow, implementing polling loops, handling job status transitions, processing rich data, managing conversation threads, or understanding the full submit-poll-complete lifecycle of the Bankr Agent API.
version: 1.0.0
---

# API Workflow

Complete reference for the asynchronous job pattern used by the Bankr Agent API.

## Core Pattern: Submit-Poll-Complete

```
1. SUBMIT  -> POST /agent/prompt   -> Get jobId + threadId
2. POLL    -> GET /agent/job/{id}  -> Check status every 2s
3. COMPLETE -> Terminal status      -> Process response + richData
```

## Endpoints

### POST /agent/prompt

```typescript
const response = await fetch(`${API_URL}/agent/prompt`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: "What is my ETH balance?",
    threadId: "thr_XYZ789", // optional: continue conversation
  }),
});
// → { success: true, jobId: "job_abc123", threadId: "thr_XYZ789", status: "pending" }
```

**Request fields:**
- `prompt` (string, required): Natural language prompt (max 10,000 chars)
- `threadId` (string, optional): Continue existing conversation. Omit for new thread.

### GET /agent/job/{jobId}

```typescript
const status = await fetch(`${API_URL}/agent/job/${jobId}`, {
  headers: { "x-api-key": API_KEY },
});
```

### POST /agent/job/{jobId}/cancel

```typescript
const cancel = await fetch(`${API_URL}/agent/job/${jobId}/cancel`, {
  method: "POST",
  headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
});
```

## Job Status States

| Status | Description | Action |
|--------|-------------|--------|
| `pending` | Job queued, not started | Keep polling |
| `processing` | Job running | Keep polling, show statusUpdates |
| `completed` | Finished successfully | Read response and richData |
| `failed` | Encountered error | Check error field |
| `cancelled` | Was cancelled | No further action |

## Response Fields

### Standard (all states)
- `success`, `jobId`, `threadId`, `status`, `prompt`, `createdAt`

### Completed
- `response` — Natural language text
- `richData` — Array of structured data (charts, social cards)
- `transactions` — Array of executed transactions
- `completedAt`, `processingTime`

### Processing
- `statusUpdates` — Array of `{ message, timestamp }`
- `startedAt`, `cancellable`

### Failed
- `error` — Error message
- `completedAt`

### Cancelled
- `cancelledAt`

## Polling Implementation

```typescript
async function waitForCompletion(
  jobId: string,
  onProgress?: (message: string) => void
): Promise<JobStatusResponse> {
  const POLL_INTERVAL = 2000; // 2 seconds
  const MAX_POLLS = 150;      // 5 minutes max
  let lastUpdateCount = 0;

  for (let i = 0; i < MAX_POLLS; i++) {
    const status = await getJobStatus(jobId);

    // Report new status updates
    if (onProgress && status.statusUpdates) {
      for (let j = lastUpdateCount; j < status.statusUpdates.length; j++) {
        onProgress(status.statusUpdates[j].message);
      }
      lastUpdateCount = status.statusUpdates.length;
    }

    // Terminal states
    if (["completed", "failed", "cancelled"].includes(status.status)) {
      return status;
    }

    await new Promise((r) => setTimeout(r, POLL_INTERVAL));
  }

  throw new Error("Job timed out");
}
```

### Polling Best Practices

- **2-second interval** — don't poll faster
- **5-minute timeout** — suggest cancellation after that
- **Track shown updates** — only display new statusUpdates
- **Handle network errors** — retry with backoff on fetch failures

## Conversation Threads

```typescript
// Start a conversation
const first = await submitPrompt("What is the price of ETH?");
const threadId = first.threadId;

// Continue the conversation (agent remembers context)
const second = await submitPrompt("And what about BTC?", threadId);

// Each response includes the same threadId
```

## Rich Data

Completed jobs may include `richData`:

```typescript
type RichData = {
  type?: string;          // "social-card", "chart", etc.
  [key: string]: unknown;
};
```

The `response` field always has a text summary regardless of richData content.

## Error Handling

| Status | Error | Resolution |
|--------|-------|------------|
| 400 | Invalid request / Prompt too long | Check input (max 10,000 chars) |
| 401 | Authentication required | Check API key |
| 403 | Agent API not enabled | Enable at bankr.bot/api |
| 404 | Job not found | Check jobId is correct |
| 429 | Rate limit exceeded | Wait for `resetAt` timestamp |

```typescript
// Handle rate limits
if (response.status === 429) {
  const error = await response.json();
  const waitMs = error.resetAt - Date.now();
  console.log(`Rate limited. Resets in ${Math.ceil(waitMs / 60000)} minutes`);
}
```

## Complete Example

```typescript
import { submitPrompt, waitForCompletion } from "./bankr-client";

async function main() {
  // Submit
  const { jobId } = await submitPrompt("Swap 0.1 ETH for USDC on Base");
  console.log(`Job: ${jobId}`);

  // Poll with progress
  const result = await waitForCompletion(jobId, (msg) => {
    console.log(`Progress: ${msg}`);
  });

  // Handle result
  if (result.status === "completed") {
    console.log(result.response);
    for (const tx of result.transactions || []) {
      console.log(`Transaction: ${tx.type}`);
    }
  } else if (result.status === "failed") {
    console.error(`Failed: ${result.error}`);
  }
}
```

## Related Skills

- `bankr-api-basics` - Endpoint documentation and TypeScript interfaces
- `bankr-client-patterns` - Reusable client code with `execute()` helper
- `bankr-sign-submit-api` - Synchronous endpoints (no polling needed)
