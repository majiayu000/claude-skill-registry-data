---
name: project-docs-update
description: "Evidence-bound incremental refresh of existing .issueops project documents during ongoing work through the project_docs MCP contract: route, read with SHA-256, then append cautions or ADRs via project_docs_append, or revise one document at a time via project_docs_revise. Use when a completed change, solved failure, new command, or durable decision should be reflected in project docs. For initial creation use project-docs-bootstrap; for structural modularization use project-docs-optimize."
---

# Project Docs Update

## Goal

Keep existing `.issueops` documents current while work happens, without
losing user consensus and without restructuring. Knowledge lands as
append-only records by default; full-document replacement is the exception.

## Lifecycle Position

`project-docs-bootstrap` (create) → **this skill** (incremental refresh) →
`project-docs-optimize` (restructure). If `.issueops` documents are
missing, route to `project-docs-bootstrap` first. If documents are oversized
or ownership is duplicated, route to `project-docs-optimize`; do not
restructure here.

## IssueOps publication gate

An IssueOps cycle reaches this skill through its `project_docs_review` gate:
publication is blocked until the cycle records whether the change left anything
for the operating docs. Update the documents here **first**, then record the
verdict from `issueops-implement` — the gate seals the change fingerprint, and a
document edited after the record makes that seal stale. `--verdict updated`
requires the doc path to be in the change set, so an unedited file cannot pass,
and `--verdict no-change` requires at least one `--reviewed-doc` path that
exists under `.issueops/` (or the root `AGENTS.md`), so an unread catalog cannot
pass either. When the change was appended during implementation, the docs
stage (`issueops-docs`) re-checks it against the final diff and owns the reseal.

## When to Trigger

Route the current task first to avoid injecting every doc into context:

```bash
issueops project route-docs --repo . --task "<task kind>" --json
```

| Work outcome | Action |
|---|---|
| Solved false case, recurring failure, operational risk | `project_docs_append(kind=caution)` |
| Durable decision with rationale or rejected alternatives | `project_docs_append(kind=adr)` |
| Changed command, convention, architecture fact, or stale doc section | `project_docs_revise` on that one document |
| Only needs doc context for the task | route/read only; no write |

In a modular repository (`documentation/manifest.json` present),
`project_docs_append` writes one dated record file under the family module
directory (`adr/2026-08-20-slug.md`, `cautions/...`), adds a
`- [<title>](<file>)` line to that family's `overview.md` when the overview
exists, and never touches the root index — read/revise on record files is
allowed. When the overview is missing, the result carries a warning and the
record must be linked by hand from the family index. There is no flat-layout
fallback: every repository gets the same record-file routing, and a repo
whose family roots do not exist yet is flagged by the checker and repaired
by `project-docs-bootstrap`.

`project_docs_route` also returns up to five dated `cautions/` and `adr/`
records whose title, summary, or `Source:` line shares at least two terms with
the task (Korean task words such as 배포·빌드·이미지 map to their English
terms). Put the files and the operation you are about to touch in the task text
so past lessons about them surface.

Trigger this skill when a completed unit of work produced one of the left-side
outcomes. Do not batch updates speculatively for hypothetical future work.

## Decision Table: append vs revise

| | `project_docs_append` (default) | `project_docs_revise` (exception) |
|---|---|---|
| Shape | Append-only dated record in CAUTIONS/ADR | Full document replacement |
| Use when | New knowledge is a discrete event/decision | An existing section is stale or wrong |
| Consensus risk | None (additive) | Requires preserving stronger existing guidance |
| Locking | Not required | `expected_sha256` from `project_docs_read` |
| Confirm | Not required | `confirm=true` only after the replacement preserves stronger guidance |

One document per update. Never rewrite multiple documents in one pass.

## MCP Contract

1. `project_docs_route` — map the task to the owning documents.
2. `project_docs_read` — read the target document, keep its `sha256`.
3. `project_docs_revise` with `expected_sha256`, `summary` (why), `evidence`
   (user instruction, files, commands), `confirm=true` — or
   `project_docs_append(kind=caution|adr)` for append-only knowledge.

CLI fallback: `issueops project append --kind caution|adr` covers
records. There is no CLI for full-document revision; when MCP is unavailable,
edit the file directly with the same evidence discipline and state that MCP
was bypassed in the report.

## Safety Rules

1. Every statement written must be backed by a file, command output, or
   explicit user instruction. Mark anything else `Unknown / not confirmed`.
2. Preserve user consensus: `project_docs_revise` replacements must keep all
   stronger existing guidance; when in doubt, append rather than replace.
3. Never edit `AGENTS.md` outside the behavioral top block and managed marker
   block unless explicitly requested.
4. Never restructure documents (moving sections, splitting files) — that
   belongs to `project-docs-optimize` and its checker contract.
5. Do not update CAUTIONS or ADR for hypothetical issues; only concrete
   solved cases and real decisions.
6. Honor `expected_sha256` failures: re-read, reconcile the intervening
   change, then retry — never force an overwrite.

## Verify

- Re-read the updated document and confirm the change and only the intended
  change landed.
- Run the smallest relevant repo check when the update claims workflow or
  command facts.
- Report revised/appended documents, evidence, commands run, and remaining
  unknowns.

## Completion Evidence

List: documents revised or entries appended, the evidence for each, the
route/read/update sequence used, verification results, and anything left as
`Unknown / not confirmed`.
