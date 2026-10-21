---
name: project-docs-optimize
description: Audit and restructure the `.issueops` operating-document tree so its folders, root indexes, and records match the current issueops layout without losing constraints, breaking code-read paths, or duplicating normative ownership. Use when asked to optimize, split, reorganize, re-folder, or validate `.issueops` documentation, ADRs, cautions, conventions, operations, testing, or architecture docs, or when the checker reports nested records, undeclared directories, undeclared root documents, broken links, or oversized documents.
---

# Project Docs Optimize

## Goal

Keep `.issueops` a navigable, single-owner documentation tree whose layout
matches what the issueops code writes and reads today, while preserving every
actionable constraint and every required project-doc entrypoint.

## Lifecycle Position

```
create                  refresh during work      restructure
project-docs-bootstrap  ->  project-docs-update  ->  project-docs-optimize
```

This skill owns the restructure stage: layout, placement, and modular split.
Route new cautions, ADRs, and stale sections to `project-docs-update`, and
missing-document setup to `project-docs-bootstrap`. Triggers:

- `--mode report` shows one or more violations;
- a root document exceeds its manifest budget;
- the user asks to reorganize, split, re-folder, or restructure.

## Layout Contract

The checker enforces this layout. Resolve script paths relative to this skill.

| Location | Owner | Rule |
|---|---|---|
| `.issueops/<ROOT>.md` | standard project docs, family roots, `single_owner_topics` owners, manifest `root_documents` | Any other root `.md` is `undeclared_root_document`. |
| family `module_dir` | `manifest.families` | Dated records (`YYYY-MM-DD-slug.md`) sit directly in the module dir, because `project_docs_append` writes them there. A dated record in a subfolder is `nested_record`. |
| beside a nested module dir (`operations/*.md` next to `operations/guides/`) | manifest `fixed_documents` | Only documents code reads at that exact path; anything else is `undeclared_document`. |
| `issues/`, `gates/`, `verified-execution/`, `state/`, `evidence/`, `tmp/` | issueops runtime | Never move or rename a file the runtime wrote. Per-issue reports found elsewhere move into `issues/<n>/`. |
| `documentation/` | this skill | `manifest.json`, `README.md`, audits. |
| any other top-level dir | manifest `directories` (`path: purpose`) | Undeclared ones are `undeclared_directory`. |

Git-ignored files are not checked; a tree git ignores entirely is
`docs_tree_ignored`. Manifest entries that point at missing paths are
`missing_declared_path`.

## Where a stray document goes

| Document | Destination |
|---|---|
| Procedure an operator follows today | the family module (`operations/guides/`, `testing/`, ...) |
| Report, plan, or PR body for issue `<n>` | `issues/<n>/`, named `verified-execution-report.md`, `pr-body.md`, `plan-archive.md`, or another descriptive name. Never use `plan.md`, `intent.md`, `spec.md`, or `plan-review.md`: the runtime rewrites those for an active cycle. |
| Plan without an issue number | `plans/` |
| Evaluation, benchmark, scorecard, dogfood or research result | `research/` (a subfolder per topic) |
| Snapshot that no longer describes the system but is still cited | `archive/` |

## Hard rules

1. Required root filenames remain canonical entrypoints. Never replace them
   with compatibility copies or redirects.
2. Move detail; do not summarize away commands, constraints, decisions,
   failure modes, or evidence. Keep the repo's terminology and language.
3. Give every topic one normative owner; other documents link to it. For
   standard engineering topics, the project-docs-bootstrap skill's
   `references/engineering-standards.md` map is the ownership reference.
4. Before moving a file, `git grep` its path in Go code, tests, goldens,
   skills, and configs. A path read by code stays where it is and goes into
   `fixed_documents` when it sits beside a nested module.
5. Move with `git mv` so history follows; edit content with the host's file
   edit tool. Do not delete a historical record to clear a violation:
   declare its directory or move it into its family.
6. In historical records (dated ADR and caution records, `issues/`, `plans/`,
   `research/`, `archive/`), rewrite only Markdown link targets. Recorded
   commands, gate CHECK lines, evidence, and "Create:"/"Source:" paths stay as
   written; a blanket string replace turns them into claims that never ran.
7. Never weaken the manifest to hide a violation. A new `directories` entry
   needs a real purpose and a consumer.

## Workflow

### Audit

```bash
uv run --directory skills/project-docs-optimize python -m scripts.check \
  --root "$PWD" --mode report --json
```

Classify every violating path and every top-level directory: family module,
runtime artifact, historical record still cited, orphan, or misplaced. Record
the inventory and before counts in the ADR that records the restructure.

### Design

Update `.issueops/documentation/manifest.json` (families, `directories`,
`root_documents`) and `.issueops/documentation/README.md` before moving
content, so the target layout is written down first.

### Restructure

Work one family or directory at a time:

| Violation | Fix |
|---|---|
| `nested_record` | `git mv` the record into its module dir; on a name collision keep both and rename the older one with a suffix. |
| `undeclared_directory` | Route each document with the table above, or declare the directory in `directories` with its purpose. |
| `undeclared_document` | Move it into the nested module, or list it in `fixed_documents` if code reads its path. |
| `missing_declared_path` | Remove the stale manifest entry or restore the path. |
| `undeclared_root_document` | Move it into a family module, or declare it as a single-owner topic or in `root_documents`. |
| `line_budget_exceeded` | Split detail into focused modules and keep the root as an index. |
| `broken_link` / `module_dir_unlinked` | Rewrite relative links after every move; the root links into its module dir. |

After each move, recompute every relative link that resolved to the old path,
including links inside the moved file. In living documents (root indexes,
evergreen modules, `AGENTS.md`, skills, README files) also update plain-text
path mentions. Then rerun the checker.
Keep prose cleanup out of the move.

### Verify

In any repository:

```bash
uv run --directory skills/project-docs-optimize python -m scripts.check \
  --root "$PWD" --mode check --json
git diff --check
```

In the issueops repository itself, also run:

```bash
python3 scripts/validate-skill.py skills/project-docs-optimize
go test ./internal/adapter/projectdocs/... ./internal/domain/projectdoc/... ./internal/domain/docs/... -count=1
go test ./cmd/issueops/issueopsapp -run TestResponseContractsGolden
```

Moving or editing `.issueops` module documents does not change the golden. It
fails when a skill description, the required-doc set, or a path listed in
`inspect.docs` (AGENTS.md, CLAUDE.md, root documents) changes; then regenerate it
with `-update` and confirm the diff contains nothing else.

## Completion evidence

Report:

- before and after violation counts by code;
- the directory map: each top-level directory and its owner or purpose;
- moved paths and rewritten inbound links;
- checker output with zero violations and test exit codes;
- any retained exception and its reason.
