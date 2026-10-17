---
name: kb-sync-nightly
description: Nightly knowledge base sync to NotebookLM and Obsidian with interactive artifact generation. Runs multi-target sync pipeline with fail-soft behavior.
compatibility: |
  - Runtime: bash 4.0+
  - Dependencies: Node.js 18+, npm
  - Permissions: read:repo, write:artifacts
---

# KB Sync Nightly

Syncs CIC and project docs to NotebookLM and Obsidian on nightly schedule. Generates interactive HTML reports with broken link detection and impact scoring.

## Trigger

```
bash C:\dev\skills\kb-sync-nightly\src\run.sh
```

Or invoke via Cowork automation on schedule (default: daily 21:00).

## Input Schema

```typescript
interface SkillInput {
  schedule?: string;        // Optional. Cron expression or "daily"
  targets?: "notebooklm" | "obsidian" | "all";  // Optional. Default: "all"
  verbose?: boolean;        // Optional. Enable debug logging
}
```

## Scheduled Task Configuration & Timeout Policy

```yaml
scheduled-task:
  name: obsidian-kb-sync-nightly
  timeout_ms: 90000              # Central policy override (configs/global.yaml)
  retry_attempts: 3
  retry_strategy: exponential_backoff
  on_failure: 
    action: notify
    recipients: ["sorensencc@gmail.com"]
    message: "Obsidian KB-Sync failed after retries. Manual execution needed."
```


## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error" | "partial";
  message: string;
  outputs: {
    wiki_path?: string;
    report_path?: string;
    staging_path?: string;
  };
  timestamp: string;
}
```

---

## Full Reference

For Setup, Requirements, Configuration, Testing, Error Handling, and Troubleshooting:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For workflow examples and integration patterns:

**→ See [docs/USAGE.md](./docs/USAGE.md)
