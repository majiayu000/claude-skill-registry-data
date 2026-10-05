---
name: ctxora-context-health
description: Diagnose and repair CTXORA local context health and run repository-safe CI checks. Use when indexing is stale, retrieval quality drops, local state is damaged, or a user asks for a CTXORA health report.
---

# CTXORA Context Health

Start with non-destructive diagnostics:

```bash
npx ctxora doctor --workspace <repository>
npx ctxora context-score --workspace <repository>
npx ctxora status --workspace <repository>
```

Explain failed checks and affected local state before changing anything. Use repair only when diagnostics identify a recoverable CTXORA state problem:

```bash
npx ctxora repair --workspace <repository>
npx ctxora index --workspace <repository>
```

For pull-request or branch checks, run:

```bash
npx ctxora ci --workspace <repository> --base <base-ref> --head <head-ref>
```

CTXORA state belongs under `.ctxora/`. Do not delete repository files, client configuration, or local indexes unless the user explicitly requests the corresponding destructive action.
