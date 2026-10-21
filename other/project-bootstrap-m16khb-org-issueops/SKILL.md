---
name: project-bootstrap
description: "Orchestrate first-time issueops project setup for a repository: AGENTS.md routing block, repo profile metadata, and the .issueops document family through the project-docs-bootstrap sub-skill, plus lifecycle routing to project-docs-update and project-docs-optimize. Use when asked to bootstrap a repo for issueops, set up project docs, or initialize agent guidance for a repository. Each sub-skill is also usable standalone."
---

# Project Bootstrap (Orchestration)

Orchestrate first-time repo setup and own the project-docs lifecycle routing.
This skill never replaces its sub-skills' own contracts; it sequences them and
owns the pieces that are not docs-specific.

## Sub-skill Contract

Load the matching sub-skill, resolved relative to this skill's directory:

- `../project-docs-bootstrap/SKILL.md` — creation and template refresh of the
  `.issueops` family and `AGENTS.md` routing block (static CLI pass +
  evidence-bound enrichment pass via its `PROMPT.md`).
- `../project-docs-update/SKILL.md` — incremental refresh during ongoing work
  (`project_docs_append` for cautions/ADRs by default,
  `project_docs_revise` for one-document replacement).
- `../project-docs-optimize/SKILL.md` — structural modularization of oversized
  docs under the manifest contract.

Their safety rules, workflows, and verification steps apply in full. Where
this skill adds obligations, the stricter rule wins.

## What This Orchestrator Owns Directly

- Repo profile metadata and lifecycle state initialization (the CLI writes
  these alongside the docs pass).
- Never overwrite an existing `AGENTS.md` wholesale. The harness may prepend
  the behavioral top block when missing and manages only the `ISSUEOPS`
  marker block after that.
- Treat generated docs as evidence-backed drafts. If the project already has
  stronger local docs, preserve and reference them.
- Lifecycle routing decisions (below).

## Lifecycle

```
create              refresh during work            restructure
project-docs-bootstrap  ->  project-docs-update  ->  project-docs-optimize
```

| Signal | Route to |
|---|---|
| No `.issueops` docs, or explicit template refresh request | `project-docs-bootstrap` |
| Completed work produced a caution, ADR, or stale section | `project-docs-update` |
| Root docs over line budget, duplicated ownership, checker violations > 0, or explicit reorganization ask | `project-docs-optimize` |

`project-docs-update` and `project-docs-optimize` route back here (or to
`project-docs-bootstrap`) when required docs are missing.

## Workflow

1. Run the dry-run plan first:

   ```bash
   issueops project bootstrap --repo . --dry-run --json
   ```

   MCP alternative: `project_docs_bootstrap_plan`.

2. Inspect `signals.files`, `signals.languages`, `signals.test_commands`,
   `signals.profile`, and each planned `files[].action`.

3. Write files and repo profile metadata when the plan is acceptable:

   ```bash
   issueops project bootstrap --repo . --json
   ```

   `--sync` refreshes existing generated docs — only on explicit request.

4. Run the enrichment pass from `../project-docs-bootstrap/PROMPT.md`: repo
   evidence in, no invented facts, updates through the MCP contract
   (`project_docs_route` → `project_docs_read` → `project_docs_revise` /
   `project_docs_append`).

5. For later task routing, prefer the route over injecting every doc:

   ```bash
   issueops project route-docs --repo . --task "commit" --json
   issueops project route-docs --repo . --task "test" --json
   issueops project route-docs --repo . --task "architecture" --json
   ```

6. When solved problems or decisions become durable knowledge, append them:

   ```bash
   issueops project append --repo . --kind caution --title "<problem>" --summary "<what happened>" --resolution "<fix>" --json
   issueops project append --repo . --kind adr --title "<decision>" --summary "<why>" --decision "<choice>" --json
   ```

   For full-document revisions use the MCP contract through
   `project-docs-update`, not the CLI.

## Verify

- `AGENTS.md` contains the behavioral top block and only the managed marker
  block changed.
- `.issueops/*.md` exist with evidence/confidence language where facts
  were inferred.
- MCP maintenance works: `project_docs_route`, `project_docs_read`,
  `project_docs_revise`, `project_docs_append`.
- The target repo's smallest relevant validation command passes when docs
  make workflow claims.

## Completion Evidence

Report: plan summary, files created/preserved/synced, enrichment updates with
evidence, lifecycle routing decisions made, verification results, and
remaining unknowns.
