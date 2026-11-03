---
name: no-comments
description: "Spawn Comment Sicko, or a swarm of them over the whole repo, fix accepted findings, and offer encodings for claimed constraints."
disable-model-invocation: true
---

# No comments

Spawn Comment Sicko. Act on accepted findings.

Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, `dev` (`master` when the branch is `dev`), including the working tree.

The whole repo (`/no-comments all`, "the repo", "everything") or a directory runs as a swarm.

## Swarm

N Comment Sickos in parallel, one slice each, drained into one report and one plan. Open a todolist with one entry per phase before launching anything: Frame, Fan out, Aggregate, Plan.

### Frame

1. Done means every file in scope has an accepted sicko result or is reported as a gap. The artifact is the Plan below.
2. List the files with `git ls-files` over the scope, code only: `*.ts`, `*.tsx`, `*.js`, `*.mjs`, `*.yml`, `*.sh`, `*.ps1`. Count each file's comment lines.
3. The files in scope must have no uncommitted changes (`git status --short -- <files>`), so the swarm's deletions can be reviewed and reverted on their own. Otherwise ask to commit or stash first.
4. Slice by file, about 150 comment lines a slice. Never split a file: one sicko owns it. A file past that size is a slice alone. N is the number of slices, at most 8; past that, grow the slices.

### Fan out

Spawn all N in one message: the Agent tool, `subagent_type: "comment-sicko"`. Every brief stands alone: its exact files, that other sickos own every other file and it touches only its own, and that its report ends `PASS` (nothing to flag), `ISSUES` (flags), or `BLOCKED` with the reason. Do not restate its rules.

If a sicko drops out, go on with the rest and note it.

### Aggregate

Wait for every sicko. Run Step 2 on each slice: its report and `git diff -- <its files>`. A rejected slice is reverted (`git restore -- <its files>`) and given once to a fresh sicko with the failure named. A second rejection or a dropout is a gap. A gap never counts as a pass. Do not paste raw reports.

### Plan

Report before Step 3:

- A table: slice, files, comments deleted, `MUST KILL`s, restored, status.
- **Deleted:** the comments already gone, counted by file. They sit in the working tree to review.
- **Quick fixes:** accepted `MUST KILL`s Step 3 fixes directly (a dead path, a dropped parameter, the real API), one line each.
- **Refactors:** the ones that need a shape, grouped where one change answers several, a one-line sketch each.
- Constraint comments for Step 5, gaps and dropouts.

Then ask via AskUserQuestion: carry out quick fixes and refactors, quick fixes only, or none yet. Steps 3 to 6 run on what is approved, one change at a time, the gates after each.

## Steps

1. Spawn the Agent tool with `subagent_type: "comment-sicko"`. Pass the scope. Do not restate its rules. A swarm's Fan out is this step, and its Aggregate runs Step 2.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, read their symbol, its callers and its history (`git log -S`, `git blame`) to learn how it works and why it is there. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `/no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, sketch it once for the accepted set and surrounding code: the files, the types, the moves, no code. Stop at the sketch. The sketch shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. Fixing root causes and redesigning from first principles guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards. After any code change, run CLAUDE.md's gates: `claude plugin validate .`, `claude plugin test .`, `tsc -p .` (`npx -y -p typescript tsc -p .` without a global `tsc`).
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval via AskUserQuestion. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, sketch, fixes, encoding offers, encodings, unenforced constraints, gate results, and other open work. Commit nothing: the `commit` skill does.

Adapted from pstack's no-comments and swarm by Lauren Tan, MIT: see `LICENSE` beside this file.
