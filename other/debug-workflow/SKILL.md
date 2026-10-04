---
name: debug-workflow
description: Systematically debug failing n8n workflows — expression errors, node type mismatches, pinned data issues, sub-workflow failures, authentication problems, rate limit errors, and silent data loss. Use this skill whenever the user reports an n8n workflow problem — phrases like "my n8n workflow is failing", "this expression isn't working", "why is this node returning empty", "debug this error", "n8n execution log shows", "workflow runs but no output". Also use when pasted error messages reference n8n concepts (ItemLists, expressions, credentials). Apply this skill before guessing a fix — n8n failures have specific diagnostic patterns, and guessing typically makes the problem worse.
---

# n8n Workflow Debugging

Fix n8n workflows the way a senior engineer does — systematically, not by guessing.

## Triage: identify the failure class first

Ask the user (or infer from error text) which class:

| Class | Symptom | Common root causes |
|---|---|---|
| **Expression error** | `Cannot read property X of undefined`, red node badge | Wrong expression syntax, missing `=` prefix, accessing undefined fields |
| **Type mismatch** | `Expected string, got array`, downstream weirdness | `Item Lists` vs single item confusion, `Split In Batches` output shape |
| **Silent empty** | Workflow runs green but no output/side effect | Filter condition wrong, pinned stale data, credential scope |
| **Auth failure** | `401`, `403`, `Invalid API key` | Wrong credential selected, expired token, OAuth refresh not configured |
| **Rate limit** | Intermittent 429, works manually, fails in batch | No backoff, batch too large, shared credential across workflows |
| **Sub-workflow** | `Execute Workflow` returns nothing or errors | Parameters not passed, return value not set, wrong workflow ID |

## Expression errors

**The single biggest footgun**: `={{ $json.field }}` vs `{{ $json.field }}`. The leading `=` makes the field an expression. Without it, the literal string `{{ $json.field }}` is sent.

Check:
1. Click the field — does it show the "expression" toggle (fx icon) highlighted? If not, it's literal mode.
2. In code-view JSON, the value should start with `=`: `"value": "={{ $json.id }}"`

**Accessing undefined paths**: `$json.customer.email` throws if `customer` is null. Use optional chaining: `$json.customer?.email ?? 'unknown'`.

**Referencing earlier nodes**: Use `$('Node Name').item.json.field`, NOT `$node['Node Name'].json.field` (deprecated). Quote exact node name including spaces.

**Common expression patterns**:

```javascript
// Array access
{{ $json.items[0].name }}
{{ $json.items?.[0]?.name ?? 'empty' }}

// Previous node output
{{ $('Webhook').item.json.body.email }}

// All items from previous node (for loops)
{{ $('Split In Batches').all().map(i => i.json.id) }}

// Conditional
{{ $json.amount > 100 ? 'high' : 'low' }}

// Date formatting (n8n uses Luxon)
{{ $now.toISO() }}
{{ $now.minus({ days: 7 }).toFormat('yyyy-MM-dd') }}

// Environment vars (self-hosted)
{{ $env.MY_SECRET }}
```

## Type mismatch diagnosis

n8n passes data as an **array of items**, each with `{ json: {...}, binary: {...} }`. Many bugs come from treating a single item as an array or vice versa.

Inspection routine:
1. Open the failing node's input view (left panel)
2. Check: is it ONE item with an array inside (`{ json: { list: [...] } }`), or MULTIPLE items (`[ { json: {} }, { json: {} } ]`)?
3. These require different handling:
   - Array-inside-one-item → use `Item Lists` → "Split Out Items" to fan out
   - Already multiple items → operate per-item

`Split In Batches` outputs different shapes on main vs "done" outputs — the main output is a batch, the done output is empty. Wire accordingly.

## Silent empty — the worst kind

Workflow shows green checkmarks but nothing happened downstream. Diagnostic order:

1. **Check execution data retention.** Settings → "Save data successful executions" must be "All" during debugging, not "None".
2. **Inspect each node's output.** Click each node → "Output" panel. Find the first one that's empty when you expected data.
3. **Pinned data?** If a node has a pin icon, it's returning pinned test data, NOT real data. Right-click → Unpin Data.
4. **Filter / IF conditions.** An `IF` evaluating false silently skips the branch. Check the condition value at runtime.
5. **Credential scope.** Google/Microsoft OAuth credentials often have limited scopes. A "Google Sheets" credential won't let you read Gmail. Re-auth with correct scopes.

## Authentication failures

- 401 on a previously-working workflow → token expired. Re-authenticate the credential.
- 401 immediately on a new workflow → wrong credential type. E.g., "Header Auth" vs "OAuth2" — check the API's docs.
- 403 with valid token → missing scope OR wrong account. OAuth credentials are per-account; confirm you authed with the right Google/Meta account.

**Self-hosted n8n specific**: if a credential suddenly stops working after a container restart, check that the encryption key (`N8N_ENCRYPTION_KEY` env var) is persisted. Losing it = all credentials corrupt.

## Rate limit failures

Symptom: works on 10 items, fails on 100. Classic.

Fix pattern:
1. Wrap the API call in `Split In Batches` with `batchSize` matching the vendor's per-second limit
2. Add `Wait` node between batches: `waitBetweenBatches: ceil(60000 / requests_per_minute)`
3. Set `retry.maxTries: 3` with `retry.waitBetweenTries: 5000` on the HTTP Request node
4. Check response headers (`X-RateLimit-Remaining`, `Retry-After`) and dynamically back off via a `Code` node

For cron-triggered workflows hitting the same vendor from multiple cron jobs, centralize the API call in ONE sub-workflow with a semaphore pattern (MySQL row as lock).

## Sub-workflow failures

`Execute Workflow` returns `null` or undefined most often because:

1. **Parent didn't pass data.** Check "Workflow Inputs" in the Execute Workflow node — must reference `{{ $json }}` or explicit fields.
2. **Child didn't set output.** The LAST node in the sub-workflow's output becomes the return value. If the last node is a `MySQL` insert returning nothing, parent gets nothing. Add a final `Set` node that constructs the return payload.
3. **Wrong workflow ID.** Sub-workflow got deleted and recreated → new ID → reference stale.

## Reading n8n execution logs

Execution log shows per-node input and output. Debug pattern:

1. Find the first failing node (red).
2. Look at ITS input (left). Is the shape what you expected?
3. If input is wrong, the bug is UPSTREAM — trace back.
4. If input is right but output is wrong/error, the bug is IN THIS NODE — check parameters.

Most bugs are upstream shape issues masquerading as downstream errors. The error message lies about where the bug is.

## Quick-fix checklist for common cases

- Expression not interpolating → add leading `=`
- Node says "No items to process" → upstream IF is filtering everything, or previous node returned empty
- Google Sheets append inserting duplicates → no unique constraint, add idempotency check (see `mysql-checkpointing` skill)
- LLM returns garbage JSON → switch from raw HTTP to `Information Extractor` with schema (see `chain-llm-pattern`)
- Webhook times out → move heavy work behind `Respond to Webhook` (respond first, process async)

## When stuck

Ask the user for:
1. Screenshot of the execution log (the red-bordered panel)
2. The exact error message (copy-paste from the node)
3. The node's parameters (settings tab, JSON view if possible)
4. Whether this ever worked before (regression vs new bug)

Don't guess without these. n8n errors are specific — vague guesses waste time.
