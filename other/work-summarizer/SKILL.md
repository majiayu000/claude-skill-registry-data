---
name: work-summarizer
description: Daily/weekly development work summaries with repo scans, transcript analysis, and optional LLM reasoning synthesis. Classifies file changes by 17-category taxonomy, detects drift signals, aggregates weekly snapshots.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: npm (built)
  - Permissions: read:repo, read:config, write:artifacts
---

# Work Summarizer

Generates structured daily/weekly work reports from repo scans and transcript analysis, with optional Claude API synthesis.

## Trigger

```bash
node dist/index.js { mode: "daily" | "weekly" }
```

## Input Schema

```typescript
interface SkillInput {
  mode?: "daily" | "weekly";              // Default: "daily"
  registryPath?: string;                  // Default: C:\dev\repo-registry.json
  outputDir?: string;                     // Default: C:\dev\CIP\CIC\logs\work-summaries
  includeRoutingArtifact?: boolean;       // Default: false
  reasoningEnabled?: boolean;             // Default: false
  anthropicModel?: string;                // Default: claude-haiku-4-5
  reasoningTimeoutMs?: number;            // Default: 30000
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "ok" | "error";
  message: string;
  data?: {
    schema_version: string;
    period: "daily" | "weekly";
    repos_scanned: number;
    modified_files: number;
    work_by_category: Record<string, number>;
    drift_signals: { count: number; score: number; summary: string };
    repo_deltas: Array<any>;
    subsystem_impacts: Array<any>;
    cross_repo_impacts: Array<any>;
    risks_or_followups: string[];
  };
}
```

## Features

- **Deterministic Pipeline**: Git diff analysis + transcript scanning (no LLM required)
- **17-Category Taxonomy**: Consistent file classification across all repos
- **Weekly Aggregation**: Loads last 7 daily reports; falls back to full scan if < 50% coverage
- **Drift Detection**: Keyword matching in transcripts (drift, driftScore, etc.)
- **LLM Reasoning** (optional): Per-category Claude API call with fallback on failure

## Error Handling

| Code | Message | Handler | Escalation |
|------|---------|---------|------------|
| `REGISTRY_NOT_FOUND` | Registry JSON missing/empty | Fail | Create C:\dev\repo-registry.json |
| `NO_MODIFIED_FILES` | No changes detected | Fail | Run in test env with mock repos |
| `OUTPUT_DIR_INVALID` | Cannot write output | Fail | Check directory permissions |

---

## Full Reference

For Setup, Requirements, Configuration, Testing, Environment Variables:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For examples, schema versioning, troubleshooting, and detailed workflows:

**→ See [docs/USAGE.md](./docs/USAGE.md)**
