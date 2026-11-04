---
name: benchmark-e2e
description: End-to-end benchmark suite for vercel-plugin. Runs realistic projects through skill injection, launches dev servers, verifies everything works, analyzes conversation logs, and produces an improvement report for overnight self-improvement loops.
---

# Benchmark E2E

Single-command pipeline that creates projects, exercises skill injection via `claude --print`, launches dev servers, verifies they work, analyzes conversation logs, and generates actionable improvement reports.

## Quick Start

```bash
# Full suite (9 projects, ~2-3 hours)
bun run scripts/benchmark-e2e.ts

# Quick mode (first 3 projects, ~30-45 min)
bun run scripts/benchmark-e2e.ts --quick
```

Options:

| Flag | Description | Default |
|------|-------------|---------|
| `--quick` | Run only first 3 projects | `false` |
| `--base <path>` | Override base directory | `~/dev/vercel-plugin-testing` |
| `--timeout <ms>` | Per-project timeout (forwarded to runner) | `900000` (15 min) |

## Pipeline Stages

The orchestrator chains four stages sequentially, aborting on failure:

1. **runner** — Creates test dirs, installs plugin, runs `claude --print` with `VERCEL_PLUGIN_LOG_LEVEL=trace`
2. **verify** — Detects package manager, launches dev server, polls for 200 with non-empty HTML
3. **analyze** — Matches JSONL sessions to projects via `run-manifest.json`, extracts metrics
4. **report** — Generates `report.md` and `report.json` with scorecards and recommendations

## Contracts

### `run-manifest.json`

Written by the runner at `<base>/results/run-manifest.json`. Links all downstream stages to the same run.

```typescript
interface BenchmarkRunManifest {
  runId: string;           // UUID for this pipeline run
  timestamp: string;       // ISO 8601
  baseDir: string;         // Absolute path to base directory
  projects: Array<{
    slug: string;          // e.g. "01-recipe-platform"
    cwd: string;           // Absolute path to project dir
    promptHash: string;    // SHA hash of the prompt text
    expectedSkills: string[];
  }>;
}
```

The analyzer and verifier read this manifest to correlate sessions precisely instead of guessing from directory listings.

### `events.jsonl`

The orchestrator writes NDJSON events to `<base>/results/events.jsonl` tracking pipeline lifecycle:

```jsonc
// Each line is one JSON object:
{ "stage": "pipeline", "event": "start", "timestamp": "...", "data": { "baseDir": "...", "quick": false } }
{ "stage": "runner",   "event": "start", "timestamp": "...", "data": { "script": "...", "args": [...] } }
{ "stage": "runner",   "event": "complete", "timestamp": "...", "data": { "exitCode": 0, "durationMs": 120000 } }
// On failure:
{ "stage": "verify",   "event": "error", "timestamp": "...", "data": { "exitCode": 1, "durationMs": 5000, "slug": "04-conference-tickets" } }
{ "stage": "pipeline", "event": "abort", "timestamp": "...", "data": { "failedStage": "verify", "exitCode": 1, "slug": "04-conference-tickets" } }
```

### `report.json`

Machine-readable report at `<base>/results/report.json` for programmatic consumption:

```typescript
interface ReportJson {
  runId: string | null;
  timestamp: string;
  verdict: "pass" | "partial" | "fail";
  gaps: Array<{
    slug: string;
    expected: string[];
    actual: string[];
    missing: string[];
  }>;
  recommendations: string[];
  suggestedPatterns: Array<{
    skill: string;   // Skill that was expected but not injected
    glob: string;    // Suggested pathPattern glob
    tool: string;    // Tool name that should trigger injection
  }>;
}
```

## Overnight Automation Loop

Run the pipeline repeatedly with a cooldown between iterations:

```bash
while true; do
  bun run scripts/benchmark-e2e.ts
  sleep 3600
done
```

Each run produces timestamped `report.json` and `report.md` files. Compare across runs to track improvement.

## Self-Improvement Cycle

The pipeline enables a closed feedback loop:

1. **Run** — `bun run scripts/benchmark-e2e.ts` exercises the plugin against realistic projects
2. **Read gaps** — `report.json` lists which skills were expected but never injected, with exact slugs
3. **Apply fixes** — Use `suggestedPatterns` entries (copy-pasteable YAML) to add missing frontmatter patterns; use `recommendations` to fix hook logic
4. **Re-run** — Execute the pipeline again to verify the gaps are closed
5. **Compare** — Diff `report.json` across runs: `verdict` should trend from `"fail"` → `"partial"` → `"pass"`

For overnight automation, combine with the loop above. Wake up to reports showing exactly what improved and what still needs work.

## Prompt Table

Prompts never name specific technologies — they describe the product and features, letting the plugin infer which skills to inject.

| # | Slug | Expected Skills |
|---|------|----------------|
| 01 | recipe-platform | auth, vercel-storage, nextjs |
| 02 | trivia-game | vercel-storage, nextjs |
| 03 | code-review-bot | ai-sdk, nextjs |
| 04 | conference-tickets | payments, email, auth |
| 05 | content-aggregator | cron-jobs, ai-sdk |
| 06 | finance-tracker | cron-jobs, email |
| 07 | multi-tenant-blog | routing-middleware, cms, auth |
| 08 | status-page | cron-jobs, vercel-storage, observability |
| 09 | dog-walking-saas | payments, auth, vercel-storage, env-vars |

## Cleanup

```bash
rm -rf ~/dev/vercel-plugin-testing
```
