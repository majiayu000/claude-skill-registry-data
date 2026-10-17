---
name: vane-research
description: Air-gapped web search and cited QA using local Vane (SearXNG + Ollama).
compatibility: |
  - Runtime: Node.js 20+
  - Dependencies: modules/wiki/vane-infra.mjs
  - Permissions: network:loopback
---

# Vane Research Skill Specification

**ID**: `vane-research`
**Version**: 1.0.0
**Status**: Active
**Owner**: soren

---

## Purpose

Performs air-gapped web search synthesis and source extraction via local Vane instance (`http://127.0.0.1:3000`). Enforces loopback network boundaries, cross-process GPU concurrency locking (`.vane-gpu-worker.lock`), and deterministic content hashing.

---

## Trigger

Exact prompt that invokes this skill:

```
Perform air-gapped web research for query: <query> using local Vane in <speed|balanced|quality> mode.
```

---

## Input Schema

```typescript
interface VaneSkillInput {
  query: string;                             // Required. Minimum 3 characters
  mode?: "speed" | "balanced" | "quality";  // Optional. Default: "balanced"
  max_sources?: number;                     // Optional. Default: 8
}
```

---

## Output Schema

```typescript
interface ToolResult {
  execution_id: string;
  success: boolean;
  type: "READ_ONLY";
  data?: {
    query: string;
    answer: string;
    sources: Array<{
      source_id: string;
      title: string;
      url: string;
      snippet_preview: string;
    }>;
    mode: "speed" | "balanced" | "quality";
    timing_ms: number;
    content_hash: string;
  };
  error?: {
    code: string;
    message: string;
    fallback_recommended: boolean;
  };
  telemetry: {
    duration_ms: number;
    timestamp: string;
    worker_id: string;
  };
}
```

---

## Timeout Tiers & Resource Limits

| Mode | Timeout | Target Workload |
|---|---|---|
| `speed` | 10,000 ms | Rapid fact checks, quick keyword verification |
| `balanced` | 30,000 ms | Standard multi-source retrieval & synthesis (default) |
| `quality` | 60,000 ms | Deep multi-step crawl & synthesis with full context |

Host GPU semaphore allows exactly 1 active worker across all processes via atomic `.vane-gpu-worker.lock` (65s stale eviction threshold).

---

## Security & Loopback Boundary

- Target endpoints must resolve strictly to the local loopback interface: `127.0.0.1`, `localhost`, `::1`, or `[::1]`.
- Any external, broadcast (`0.0.0.0`), or remote IP triggers `SECURITY_BOUNDARY_VIOLATION`.
- Air-gapped execution isolates research workflows from unvetted network telemetry.

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional errors:

| Code | Cause | Fallback Recommended |
|---|---|---|
| `INVALID_INPUT` | Query length < 3 or non-string | `false` |
| `VRAM_CONCURRENCY_SATURATED` | Another process holds GPU semaphore | `true` |
| `EXECUTION_TIMEOUT` | Request exceeded tier timeout | `true` |
| `VANE_SERVICE_UNAVAILABLE` | Connection refused on loopback port | `true` |
| `UPSTREAM_SEARCH_ERROR` | Upstream Vane HTTP error | `true` |

---

## Full Reference

For Setup, Requirements, Configuration, and Testing:
→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)
