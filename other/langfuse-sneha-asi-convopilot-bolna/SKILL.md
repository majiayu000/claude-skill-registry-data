---
name: langfuse
description: Look up ConvoPilot traces in Langfuse by run_id — debug test runs, inspect turn-by-turn spans, and identify evaluation failures
argument-hint: "<run_id> [optional: region in/us]"
allowed-tools: Bash(curl *) WebFetch
---

You are debugging a ConvoPilot test run using Langfuse traces.

Run ID: **$ARGUMENTS**

## Langfuse Environment

Read from environment variables:
```
LANGFUSE_PUBLIC_KEY   — Langfuse project public key
LANGFUSE_SECRET_KEY   — Langfuse project secret key
LANGFUSE_HOST         — Langfuse host URL (e.g. https://cloud.langfuse.com)
```

If env vars are not set, inform the user: "Langfuse is not configured — set LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY and LANGFUSE_HOST in .env." Do not proceed with API calls.

## ConvoPilot Trace Hierarchy

```
TestRun  (root trace — session_id = run_id)
  └── TestCase  (span)
        └── ConversationTurn  (span — one per turn)
              └── ToolCall  (event — one per tool call)
```

Key fields to look for:
| Span | What it tells you |
|------|------------------|
| `TestRun` | Overall status, total turns, run duration |
| `ConversationTurn` | role (user/agent), message, latency_ms |
| `ToolCall` | tool_name, arguments, output, validation_status (pass/fail/missing) |
| `EvaluationResult` | verdict, confidence_score, metric_results |

## Step 1 — Fetch the session

```bash
AUTH=$(echo -n "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64)
HOST="${LANGFUSE_HOST:-https://cloud.langfuse.com}"
RUN_ID="<run_id from arguments>"

# Get session (contains list of traces)
curl -s "$HOST/api/public/sessions/$RUN_ID" \
  -H "Authorization: Basic $AUTH"
```

## Step 2 — Fetch observations for each trace

```bash
# Get all spans for a trace
curl -s "$HOST/api/public/observations?traceId=$TRACE_ID&limit=100" \
  -H "Authorization: Basic $AUTH"

# Get only evaluation generations (LLM judge calls)
curl -s "$HOST/api/public/observations?traceId=$TRACE_ID&type=GENERATION&limit=20" \
  -H "Authorization: Basic $AUTH"
```

## Step 3 — What to look for

1. **Failed turns:** Any `ConversationTurn` span with `level=ERROR`
2. **Slow LLM calls:** Evaluation generation spans > 3s latency
3. **Tool call failures:** `ToolCall` events with `validation_status=fail` or `validation_status=missing`
4. **Low confidence:** `EvaluationResult` span with `confidence_score < 0.7` → triggers human review
5. **Run stuck in `running`:** Check if agent returned 5xx — look for `statusMessage` on `TestRun` span
6. **Evaluation inconsistency:** Check `raw_judge_response` — if contradicts the verdict, `temperature` may not be 0

## Step 4 — Present findings

Show the user:
- **Run status:** pass / partial / fail / stuck
- **Timeline:** chronological list of turns with role + latency
- **Issues found:** any errors, slow spans, failed tool calls
- **Confidence score** and which metrics dragged it down
- **Direct Langfuse link:**
  `$LANGFUSE_HOST/project/<project_id>/sessions/<run_id>`

## Error handling

| Error | Action |
|-------|--------|
| Session returns empty | Check that `LANGFUSE_HOST` points at the Langfuse instance/region the backend writes to |
| Auth fails (401) | Check that `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` are set correctly |
| No spans found | Run may still be `running` — check `GET /simulation/runs/{run_id}` on the backend API |
| `confidence_score` missing | Evaluation hasn't run yet — trigger `GET /evaluation/{run_id}` |
