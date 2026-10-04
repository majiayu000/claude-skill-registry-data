---
name: fallback
description: Graceful degradation when primary approach fails. Try alternates in priority order; record which path succeeded for future routing.
triggers:
  - "try fallback"
  - "primary failed"
  - "alternate approach"
  - "plan b"
---

# Fallback

Graceful degradation when primary approach fails. If preferred agent/skill/tool fails, try alternates in priority order. Record which path succeeded for future routing decisions.

## Purpose

Increase resilience. Instead of crashing on first failure, attempt a ladder of fallback strategies. Log outcomes for analytics and future routing optimization.

## When to use

- Primary API rate-limited → try cheaper model or cached result
- Preferred tool unavailable (Playwright, Firecrawl) → shell equivalent or simpler approach
- Test framework broken → manual verification or other test harness
- Deployment target down → try alternate region or staging

## Fallback Ladder Pattern

1. **Try primary** — Execute preferred approach.
2. **On failure** — Capture error, severity, and root cause.
3. **Try secondary** — Run alternate (lower cost, lower latency, or lower feature fidelity).
4. **Try tertiary** — Final fallback (minimal viable approach).
5. **Escalate** — If all fail, ask user or escalate to architect.
6. **Record** — Log which path succeeded + why for future routing.

## Example Ladder

```
Task: "Extract text from PDF at https://example.com/doc.pdf"

Primary: Firecrawl + advanced extraction (costs $0.10, ~2s)
  → Fails: Rate limit / unavailable

Secondary: pypdf + manual page parse (costs $0, ~5s)
  → Succeeds: Extracts text (lower quality)
  → Log: "fallback-pdf-extraction:pypdf" for next time

---

Task: "Validate auth flow under load"

Primary: k6 load test (needs staging env)
  → Fails: Staging DB offline

Secondary: Locust (Python, lower overhead)
  → Succeeds: Simulates load
  → Log: "fallback-loadtest:locust" for future

Tertiary: Manual curl loop (minimal viable)
  → Would execute if Locust also failed
```

## Invocation

```bash
fallback --task "Extract data" --primary "firecrawl" --secondary "pypdf" --tertiary "pdfplumber"
```

Or via skill trigger: "Try fallback for PDF extraction"

## Logging Format

Each fallback attempt logs to `~/.claude/logs/fallback.jsonl`:

```json
{
  "timestamp": "2026-04-16T14:22:00Z",
  "task": "pdf-extraction",
  "primary": "firecrawl",
  "status": "failed",
  "error": "rate_limit_exceeded",
  "fallback_used": "pypdf",
  "result": "success",
  "cost_saved": 0.10,
  "latency_impact": "+3s"
}
```

## References

- Smart model select: `smart-model-select` (similar fallback for model choice)
- Dispatch skill: `dispatch` (routes to alternates)
- Error handling patterns: `packages/core/best-practices/error-handling.md`
