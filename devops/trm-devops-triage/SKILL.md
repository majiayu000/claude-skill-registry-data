---
name: trm-devops-triage
description: Use when inspecting, claiming, investigating, annotating, or resolving operational defects in the TRM DevOps triage queue, or when executing trm-devops sync and prune workflows.
compatibility: |
  - Runtime: Node.js 18+, GitHub CLI (`gh`), PowerShell/Bash
  - Dependencies: `@toolforge/trm-devops`
  - Permissions: read/write workspace, execute CLI commands
---

# TRM DevOps Triage Operator Workflow

This skill guides the operator through the 4-step triage lifecycle for resolving operational defects, CI/CD failures, and infrastructure issues ingested into `dev/triage/queue.md` by the TRM DevOps pipeline.

---

## Artifact locations

| Artifact | File path | Purpose |
|---|---|---|
| **Primary active queue** | `dev/triage/queue.md` | Active defects requiring investigation or resolution |
| **Archived records** | `dev/triage/archive/YYYY-MM/resolved-defects.md` | Monthly archive of closed and pruned defects |
| **Global archive index** | `dev/triage/archive/index.json` | Searchable index of all historical resolutions |
| **Runtime cache & locks** | `dev/triage/.cache/` | Concurrency locks (`queue.md.lock`), dead-letter queue, and pending buffers |

---

## Operator action lifecycle

```
┌────────────────────┐     ┌───────────────────────┐     ┌────────────────────────┐     ┌─────────────────────┐
│ 1. Inspect queue   │ ──> │ 2. Claim & run steps  │ ──> │ 3. Annotate notes      │ ──> │ 4. Resolve & prune  │
│ dev/triage/queue.md│     │ gh / pwsh / npm test  │     │ status: IN_PROGRESS    │     │ node modules/trm-devops/dist/cli/index.js prune│
└────────────────────┘     └───────────────────────┘     └────────────────────────┘     └─────────────────────┘
```

---

## Step-by-step execution guide

### 1. Inspect and claim the defect

To inspect active items, open `dev/triage/queue.md`. Claim the target defect by updating the header metadata:

```markdown
### [DEV-001] CI/CD Failure across main and feat/openrouter-oxalpha-integration
- **Status:** IN_PROGRESS
- **Owner:** soren
- **Severity:** HIGH
- **Ingested:** 2026-08-28T16:45:00Z

<!-- operator-notes-start -->
Investigating release token scope and commitlint rules on main.
<!-- operator-notes-end -->
```

### 2. Execute deterministic action steps

Run the diagnostic commands extracted directly into the defect block:

```bash
# 1. View raw failure logs for the repository
gh run view --repo sorensencc-dotcom/toolforge --log-failed

# 2. Inspect the latest 5 runs across workflows
gh run list --repo sorensencc-dotcom/toolforge --limit 5

# 3. Test local repo governance and branch validation
npm run lint
```

### 3. Implement and verify the fix

1. Apply the necessary code, workflow configuration, secret scope, or branch rule changes in `sorensencc-dotcom/toolforge`.
2. Run local tests to verify the fix:
   ```bash
   npm test
   ```
3. Push a verification commit or trigger the workflow dispatch to confirm a green build.

### 4. Mark resolved and prune remote sources

Once the fix is verified green in CI:

1. In `dev/triage/queue.md`, update the defect status:
   ```markdown
   - **Status:** RESOLVED
   ```
2. Run the pruning cycle to archive locally and purge the remote buffer in NotebookLM:
   ```bash
   # Dry-run validation
   node modules/trm-devops/dist/cli/index.js prune --dry-run

   # Execute prune and archive
   node modules/trm-devops/dist/cli/index.js prune
   ```

Pruning automatically performs the following actions:
- Removes the resolved defect block from `dev/triage/queue.md`.
- Appends the defect record with duration metrics into `dev/triage/archive/YYYY-MM/resolved-defects.md`.
- Updates `dev/triage/archive/index.json`.
- Deletes the corresponding source note from the remote NotebookLM operational buffer.

---

## CLI & MCP command reference

### Pipeline CLI commands

```bash
# Ingest and sync latest defects into queue.md
node modules/trm-devops/dist/cli/index.js sync

# Inspect active queue status and count summary
node modules/trm-devops/dist/cli/index.js status

# Prune all RESOLVED items
node modules/trm-devops/dist/cli/index.js prune
```

### MCP tools

If interacting via an MCP client, call the following tools:
- `sync_dev_triage`: Syncs un-ingested failure logs and updates `queue.md`.
- `prune_triage_source`: Prunes resolved defects and deletes remote notebook sources.
- `query_dev_notebook`: Queries the NotebookLM operational buffer for historical context.

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For detailed workflow:** See [docs/USAGE.md](docs/USAGE.md).
