---
name: trm-status
description: Instant status table across all TRM research topics — counts, staging backlog, extract lag, staleness, uncommitted files, next steps.
compatibility: |
  - Runtime: Node.js 18+, git on PATH
  - Dependencies: (see package.json)
---

# TRM Status

One-shot status dashboard for every TRM research topic in `trm-vault`. Answers
"what are all our TRMs and what state are they in" without a manual directory
crawl.

## Trigger

"what are all our trms", "trm status", "status of the vault", "what's left to
ingest", or before starting a new research session on any existing TRM.

## Flow

1. Call `findAllTopics(vaultRoot)` — walks `<vaultRoot>/topics/**` and returns
   every leaf directory that has both a `topic.json` and a `sources/` dir
   (container nodes like the person-level `charlie/` are excluded).
2. For each topic dir, call `scanTopicDir(dir)` to get source/extract counts,
   staging-batch dirs, and vision-analysis/trm-ingest/crosslink presence.
3. Call `deriveStatus(stats)` to classify state:
   - `stub` — zero sources (new placeholder topic, awaiting a research trip)
   - `staging-pending` — has `_staging-batch*` dirs not yet ingested
   - `extract-lag` — extracts < 50% of sources (ingest ran, extraction didn't keep up)
   - `stale` — fully caught up but `topic.json.updated_at` is >14 days old
   - `active` — caught up and recently touched
4. Call `attachGitInfo(vaultRoot, statuses)` to append an uncommitted-file
   warning per topic (via `git status --porcelain -- <relPath>`), per
   [[feedback_trm_vault_commit_per_run]].
5. Call `renderTable(statuses)` and print it.

Creating a new TRM later (new person, new research thread) is normal — a
`stub` state is not a problem to fix, just a placeholder waiting for intake.

## Input Schema

```typescript
interface Input {
  vaultRoot?: string; // defaults to C:\Users\soren\trm-vault
}
```

## Output Schema

```typescript
interface Output {
  statusTable: string; // tab-separated: TRM, STATE, COUNTS, NEXT STEPS
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For detailed workflow:** See [docs/USAGE.md](docs/USAGE.md).
