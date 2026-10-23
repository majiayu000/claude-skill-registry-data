---
name: gz-prd
description: Use to define or revise project-level intent as a PRD before ADR planning.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "0.3.1"
model: opus
---

# gz prd

## Overview


> **Self-Escalation (opus-tier).** The dialogue with the operator stays in the main session: a subagent cannot ask the operator a question or hear the answer, and what the operator adds is this skill's primary input. When the session model is below opus-tier, you may spawn an `Agent` with `model="opus"` for a bounded drafting or QC track that needs no operator input — pass the operator's words verbatim and the relevant context (ADR IDs, OBPI IDs, prior decisions), and treat what it returns as a draft you verify, not as the operator-facing result.

Scaffold a product requirements document, then fill it with the operator.
`gz prd <name>` (`prd` in `src/gzkit/commands/init_cmd.py`):

- requires an initialized project (`.gzkit.json`); otherwise it exits 1;
- canonicalizes `name` to `PRD-<SLUG>-<semver>`: a leading `PRD-` is dropped, a
  trailing `-X.Y.Z` becomes the semver (default `1.0.0`), and the rest is
  stripped to alphanumerics and upper-cased, so `my-product` becomes
  `PRD-MYPRODUCT-1.0.0` (GHI #186). A name with no alphanumeric character
  exits 1;
- renders the `prd` template (`src/gzkit/templates/prd.md`) with
  `status: Draft`, today's date, `--title` (default: the id) and the author
  prompts in `AUTHOR_PROMPTS["prd"]` (`src/gzkit/templates/author_prompts.py`)
  into `<paths.prd>/<id>.md`;
- appends one `prd_created` ledger event, which makes the id a node in the
  `gz state` graph.

The author prompts are questions, not content: Problem Statement, North Star,
Invariants and the Q&A Transcript stay unwritten until the operator answers
them. It does not check for an existing file: a name that canonicalizes to an
existing id overwrites that file and appends a second event. `--dry-run` prints
the path and event it would write, whether or not the file exists, and writes
nothing. `gz interview prd` is the interactive alternative: it asks the
questions in `PRD_QUESTIONS` (`src/gzkit/interview.py`) and writes the answers
into the same template.

## Workflow

1. Preview: `uv run gz prd <name> --dry-run`. If the printed path already
   exists, stop — that PRD is revised in place, not re-scaffolded.
2. Create it: `uv run gz prd <name> [--title "<title>"]`.
3. Interview the operator for each author prompt and replace it with their
   answer; record the exchange under Q&A Transcript. `required_headers` in
   `src/gzkit/schemas/prd.json` is the authority for the sections and the
   permitted `status` values.
4. Validate: `uv run gz validate --documents` checks the frontmatter and
   headers against that schema. Capture the output to a file and read `$?`
   straight after it.
5. Report the id, path and validation result. ADRs are then planned against the
   PRD with `gz-plan` (`uv run gz plan create`).

## Example

```bash
uv run gz prd my-product --dry-run
uv run gz prd my-product --title "My Product Requirements"
uv run gz validate --documents
```
