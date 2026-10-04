---
name: workflow
description: Orchestrate the repo workflow from brief through draft PR using skills and thin role wrappers.
---

# Workflow

## Objective

Coordinate the standard delivery flow:

`brief -> spec -> tdd -> code -> review -> draft-pr`

This is a skill entry point, not a command wrapper. Keep the orchestration light and route work into the stage skills instead of duplicating their guidance here.

## Instructions

1. Ask for the feature or change name and which stage range to run (`full`, partial like `spec -> code`, or resume from an existing artifact).
2. Check which stage artifacts already exist before asking the user to recreate them:
   - `docs/briefs/`
   - `docs/specs/`
   - `docs/qa/reports/`
3. For each selected stage, invoke the matching skill (`brief`, `spec`, `tdd`, `code`, `review`, `draft-pr`). Each skill self-routes via its own `Invocation` preface: `brief`, `spec`, `tdd`, `code`, and `test` run inline in the current chat under the appropriate persona, while `review`, `draft-pr`, and `pr-description` default to delegating to their owning subagent.
4. After each stage, summarize:
   - what was produced
   - which paths changed or were created
   - open decisions or blockers
   - the next recommended skill
5. Keep context compact. Prefer referencing existing artifact paths over restating full document contents.
6. Do not create workflow state files or command-era JSON checkpoint files in Phase 1.

## PR validation (before `draft-pr`)

- Prefer targeted checks while iterating; do not rerun full verification on every tiny commit by default.
- **Before opening or updating a PR**: run a full verification pass from the repo root. Include builds when the change touches app/runtime code, config, dependencies, or anything that could affect shipped output.
- **Docs-only** edits (markdown with no runtime effect): a full build is not required; still run linting when the diff touches linted paths.
- On follow-up pushes to an open PR, rerun checks when the changeset meaningfully affects verified code.

## Stage Outputs

- `brief` -> `docs/briefs/{feature}.md`
- `spec` -> `docs/specs/{feature}.md`
- `tdd` -> failing or newly added unit tests
- `code` -> implementation and verification results
- `review` -> `docs/qa/reports/{date}-{branch-or-pr}.md`
- `draft-pr` -> branch, commit, and draft PR output
