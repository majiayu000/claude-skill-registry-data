---
name: pr-review
description: Reviews a pull request or the current branch before merge ("review my PR", "review this branch", "is this ready to merge?") against a catalog of review concerns (a built-in starter set plus the project's own, mined from its past reviews) in two agent stages, map-and-review per slice of the diff and a separate validation, and reports only validated bugs, issues, and nits, each quoting its added line, with an advisory ship verdict. Also builds or refreshes the project's concern catalog from past review comments. Unlike a general code review, it checks the project's own recurring concerns and prints how much of the catalog it covered. Use when asked to review, audit, or check a branch or pull request for correctness or readiness to merge, or to build a review catalog.
argument-hint: "[base-branch | pull-request] | mine"
disable-model-invocation: true
---

# PR review

Slice the diff; for each slice, one agent maps the catalog onto its added lines and reviews every concern it mapped; a separate skeptic validates every finding. The report is compiled mechanically from validated findings only. Every agent runs on the model of the session that invoked the skill. It launches a multi-agent run, so it runs only when the user invokes it.

## Modes

- **Review** (default): the current branch against its base, or the named base branch or pull request.
- **Mine** (argument `mine`): build or refresh the project's concern catalog, per [references/mining.md](references/mining.md).

## Inputs

- **Settings first**: Read `.claude/shipyard/pr-review.md` in the project root, if it exists, before anything else. It sets the base branch, review paths, security-sensitive paths, slice size, agent cap, findings cap, and CI-enforced rules with their suppression markers; shape in [references/overlay-example.md](references/overlay-example.md).
- **The catalog**: every `references/catalog-*.md` (format in [references/catalog.md](references/catalog.md)) plus the project's `.claude/shipyard/pr-review/concerns.md`, which wins on id collisions.
- **The diff**, scoped once by `scope.sh` in this skill's folder and shared with every agent.

## Pipeline

```
scope.sh ──> full.diff + diff.txt ("path:line: code", added lines only)
   │         slices: one if ≤ 10 files and ≤ 400 added lines; else ~400 lines each,
   ▼         by top-level directory, security paths alone, at most 6 (slices grow past it)
1 Map and review   concern-reviewer per slice, in parallel, whole catalog each:
   │               MAP concerns to its lines, then REVIEW each: finding or cleared
   ▼
check (no model)   drop findings whose evidence_line isn't at location; flag unreviewed ids
   ▼
2 Validate         review-verifier, one agent over every slice's findings:
   │               confirmed | false-positive | pre-existing | duplicate
   ▼
report from confirmed findings only: Bugs / Issues / Nits / Summary + coverage
```

Contracts, schemas, the slicing rule, and the report template: [references/stages.md](references/stages.md). The runnable script: [references/workflow.js](references/workflow.js).

## Rules

- **Evidence line is mandatory.** Every finding cites `location` and `evidence_line` verbatim from `diff.txt`; the mechanical check drops any whose line isn't there.
- **Added lines only.** Pre-existing defects are tagged and dropped, not reported.
- **Severity**: `bug` wrong behavior, data loss, or a security hole; `issue` a design defect a reviewer would block on; `nit` a minor preference with a reason. Mark design-level findings as possibly intentional.
- **Findings cap** from settings (default 10), highest severity first; say how many were cut.
- **Don't re-flag what CI enforces**, except an added line that suppresses a rule.
- **Read-only end to end**: no agent edits files or commits. Posting findings as PR comments is a separate step and a **HUMAN TRIGGER**: only on the user's approval.
- **The coverage line reports what ran**: counts from agent outputs and the check, `n/a` for any not computed, never an estimate; unreviewed concerns are listed, never hidden. The verdict is advisory.

## Steps (review mode)

```
- [ ] 1 Read settings and resolve the base
- [ ] 2 Scope the diff
- [ ] 3 Run the two stages
- [ ] 4 Print the report
- [ ] 5 Offer rejected findings on request
```

1. **Read settings and resolve the base**: the settings' base branch, else the default branch; for a pull request, fetch its head into a worktree.
2. **Scope the diff**: `bash <skill>/scope.sh <worktree> <base> <scratch> [review paths, :!skips]`, or `--diff <file>` when you were handed a diff. It prints `files=N added=M`; on `added=0` report "No changes to review." and stop. Without a shell, build `diff.txt` from the diff yourself.
3. **Run the two stages**. With a workflow runner, run `references/workflow.js` with args `worktree`, `base`, `scratch`, `skillDir`, `diff` (the contents of `diff.txt`), `title`, `focus` (plus `cap`, `ciRules`, `securityPaths`, `sliceLines`, `maxAgents` from settings) and print its `report` verbatim. Without one, follow "Running without a workflow runner" in [references/stages.md](references/stages.md): `concern-reviewer` per slice (namespaced, e.g. `shipyard-delivery:concern-reviewer`) in parallel, the check, then `review-verifier`, each a direct child of this session.
4. **Print the report**: Bugs, Issues, Nits (each says `none` when empty, never omitted), then the Summary with the verdict and the coverage line.
5. **Offer rejected findings on request**: only if the user asks; they're the audit trail of what the check and validation killed.

## Handoff

`next:` fixes go back to the implement stage; a clean review goes to the describe stage.
