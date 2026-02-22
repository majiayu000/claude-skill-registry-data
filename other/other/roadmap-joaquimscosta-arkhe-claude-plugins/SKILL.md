---
name: roadmap
description: >
  Synthesize project documentation and codebase into comprehensive roadmap status, gaps analysis,
  and blockers. Use when assessing project health, identifying blockers, tracking progress,
  comparing plan vs reality, documenting risks, or planning next milestones.
  Triggers: "roadmap", "project status", "blockers", "risks", "progress", "next milestone",
  "gaps", "what's done".
argument-hint: status | gaps | next | delta | blockers | risks | update | specs
allowed-tools: Read, Glob, Grep, Write
---

# Roadmap Analyst

Synthesize project documentation and codebase state into actionable status reports.

## Context Discovery

**Run this protocol before any analysis to understand the project.**

### Priority 1: Explicit Configuration

Read `.arkhe.yaml` from project root. Extract `roadmap:` section:

```yaml
roadmap:
  output_dir: arkhe/roadmap
  context_dir: .arkhe/roadmap
  status_file: docs/PROJECT-STATUS.md
```

### Priority 2: Rich Context

If `{context_dir}` exists, read all `.md` files — especially `documents.md` for the document map and `architecture.md` for module structure.

### Priority 3: Project Identity

Read `CLAUDE.md` and `README.md` to understand project scope and conventions.

### Priority 4: Documentation Scan

Glob for documentation, planning, and status files:

```
docs/**/*.md, plan/**/*.md, specs/**/*.md, arkhe/specs/*/spec.md
```

### Priority 5: Codebase Scan

Detect tech stack from build files, then scan for modules, routes, models, tests, and migrations.

## Arguments

Parse from `$ARGUMENTS`:

| Mode | Description |
|------|-------------|
| `status` | Overall dashboard — modules, phases, completion |
| `gaps` | Gap analysis status — open/closed/in-progress |
| `next` | Prioritized next actions |
| `delta` | What changed since last assessment |
| `blockers` | Blocking chain analysis |
| `risks` | Risk register with likelihood/impact |
| `update` | Write updated status document |
| `specs` | Spec pipeline status verification |
| _(none)_ | Full dashboard (combines status + gaps + next) |

## Module Maturity Scale

Rate each module using this shared vocabulary:

| Level | Description |
|-------|-------------|
| **Stub** | Directory/package exists, maybe a placeholder |
| **Domain Started** | Entities/models/types defined |
| **Service Layer** | Business logic implemented |
| **API Ready** | Endpoints/routes exposed |
| **Tested** | Tests covering key paths |
| **Production Ready** | Fully tested, documented, monitoring-ready |

## Mode Execution

### `status`

Produce a status dashboard:

| Module | Backend | Frontend | Maturity |
|--------|---------|----------|----------|

Then detail: What's working, What's planned, What's missing.

### `gaps`

Cross-reference all gap analysis documents. For each gap: original report, current status (Open/In Progress/Closed), evidence of closure.

### `next`

Prioritized recommendations combining: unclosed gaps, unstarted specs, module maturity imbalances, frontend-backend parity gaps.

### `delta`

Compare the status document against current codebase state. Highlight: new files/modules, closed gaps, new issues, migration count changes.

### `blockers`

Trace blocking chains. For each blocker: what it blocks, who owns it, what's needed to unblock.

### `risks`

Risk register:

| Risk | Likelihood | Impact | Score | Mitigation |
|------|-----------|--------|-------|------------|

### `update`

Generate an updated status document. Show the user a diff preview and ask for confirmation before writing to `{status_file}` (default: `docs/PROJECT-STATUS.md`). Preserve existing format but update all data points.

### `specs`

Spec pipeline verification:

| Spec | Title | Status | Evidence |
|------|-------|--------|----------|

Verify status against codebase, not just what the spec says.

## Output Rules

- **Evidence-based** — every claim backed by a file path, migration, or component
- **Tabular** — use tables for at-a-glance status; prose for analysis
- **Actionable** — always end with recommended next actions
- **Honest** — distinguish between "verified working" and "files exist but untested"
- `update` writes files after user confirmation; all other modes output to chat

## Lane Discipline

- Do NOT produce user stories or requirements — that's the PM's domain.
- Do NOT produce architecture documents or ADRs — that's the architect's domain.
- Do NOT write source code, tests, or config files.
- Don't confuse planning documents with implementation — a design doc is NOT a built feature.

## References

- [WORKFLOW.md](WORKFLOW.md) — Detailed discovery and mode workflows
- [EXAMPLES.md](EXAMPLES.md) — Usage examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
