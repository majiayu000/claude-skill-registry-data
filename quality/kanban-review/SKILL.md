---
name: kanban-review
description: 'Review a kanban feature or bug against its approved scope, current testing evidence and layered review rules. Write PASS/FAIL/REJECT/REQUIREMENT_BUG for the current execution. Use in review.'
---

# Kanban Phase 5 — Review (Autonomous)

Argument: `<feature_name>`.

Stand on quality, not survivor. Load layered review rules, audit the changes, and write a report whose `status:` is the truth `kf` trusts.

**Invoked through `kf run`?** If your prompt starts with `kf-run:`, you are a worker for this stage only: skip the "move to stage" step below, never run `kf stage` / `kf approve` / `kf archive` / `kf run`, never edit approved contract artifacts, do not commit, and end your final message with two lines exactly: `STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` and `Summary: <one or two sentences>`. The main agent reads them and decides the transition.

---

## 1. Move to review

```bash
kf stage {feature_name} review
```

(Already there → skip. If the move is refused, run `kf validate --change {feature_name}` — a missing/stale or non-PASS testing report blocks this direction; loop back through kanban-test.)

## 2. Load review rules

- Resolve rules per filename in project → user → package order. Include general, security and performance plus the project's stack rule when available.
- Project: `{project_root}/.kf/review/rules/*.md`; user: `~/.kf/review/rules/*.md`; package: `kanban-flow/review/rules/*.md` beside the installed CLI's package.json. If no rule source is available, report the missing rules instead of silently skipping review.
- Stack packs (`node`, `go`, `rust`, `python`, `php`, `ruby`, `java`) are opt-in: if the project's stack has no `{stack}.md`, suggest `kf rules` (auto-detect) or `kf rules --stack <id>` to install it — they are not auto-loaded from `kanban-flow/review/stacks/`.

Review **only files actually changed**. Record findings with severity HIGH / MEDIUM / LOW. Reproduce plausible failures — don't infer.

**AI-assisted code risk lens** — hunt for the failure modes AI-generated code produces most:

- Phantom tests: tests that execute code but never assert the behavior the spec requires
- Catch-and-swallow: catches that hide errors instead of handling or rethrowing with context
- Generic helpers without a domain anchor: abstractions invented for one call site
- Scope drift: changes outside the approved contract and task list
- Unrelated broad rewrites: reformatting or refactoring files beyond the diff's purpose
- Polished comments/commits that describe the change but never explain intent or risk

Preserve decisions: do not reopen verified findings or silently undo user-chosen scope, libraries, or thresholds. Before applying a security finding, threat-model it — state what the code stores, protects, and exposes; a finding without a reachable attack path is LOW.

Use the `## Baseline` recorded at the top of `tasks.md` (starting HEAD + pre-existing working-tree changes) to include committed, staged, unstaged and new untracked feature files. Preserve unrelated pre-existing changes. Verify the testing report is PASS for the current execution id. After any implementation fix, loop through testing again before writing a new review result.

**Worktree items:** when `kf status` shows a `Worktree:`/`Domain:` block, the reviewed changes live on branch `kf/<feature>` in that worktree — review `git diff`/`git log` of that branch (from the main checkout or inside the worktree), not the main checkout's own dirty files. The worktree teardown on archive refuses while it is dirty, so uncommitted review-relevant changes must be called out as a finding.

## 3. Write review-report

For `kind: bug`, review against the bug report and existing feature behavior. Check reproduction evidence, regression tests and fix scope; do not demand feature planning artifacts. Record the verified root cause and whether related feature docs need an update. If no documentation changes are needed, say why.

A bug fix is reviewed adversarially, because a narrow fix is the most common way a bug comes back wearing different clothes. Two things go in every bug review report, and "none" is a valid answer only when you say what you looked at:

- **Reachable regressions.** Name what else calls the code you changed, and what a plausible caller passes that the fix did not consider. A guard added for one entry point rarely covers the others — list the sibling paths and say, for each, whether you checked it or not. Do not write "no regressions"; write what you reached for.
- **Claims you disproved.** State at least one thing the implementer asserted that you tried to break and could not — the root cause, the blast radius, a "this cannot happen" in a comment. Re-run the reproduction yourself rather than trusting the report, and if an explanation in a comment is load-bearing, verify it instead of reading it. Comments that justify a fix have been wrong in exactly the direction that made the fix look correct.

A test that passes proves the code does something; it does not prove the test would fail if the fix were removed. When a fix turns on one predicate, delete or invert it and confirm a test goes red. A test that stays green under that is not protecting anything, and should be reported as a finding.

```bash
kf instruct review-report --change {feature_name}
```

Fill `phase-5-review-report.md`, set frontmatter `status:` to exactly one of:

- `PASS` — no HIGH blockers; change is shippable
- `FAIL` — HIGH blockers / broken tests
- `REJECT` — does not meet DoD / acceptance criteria
- `REQUIREMENT_BUG` — the requirement itself is wrong vs. real product need

Set `execution:` to the current id from instruct and keep Review Status/Final Decision consistent with frontmatter. Assess MEDIUM findings against acceptance and DoD; do not declare PASS merely because there are no HIGH findings.

## 4. The directional gate decides

- `PASS` → load kanban-archive for the applicable feature/bug closure before running `kf archive`.
- `FAIL`/`REJECT` → **structural fix needed**: loop back, re-implement, then the feature must be **re-tested before review again** (kanban-test skill).

```bash
kf stage {feature_name} implementation
```

- `REQUIREMENT_BUG` → **STOP FEATURE.** Do not silently rewrite the requirement — report back to the user what the review found and ask how to proceed. `kf stage` blocks all movement here by design.

---

## Done

A decisive report written. Hand off:

```text
If PASS: load the kanban-archive skill.
If FAIL/REJECT: load kanban-implement (then kanban-test before returning here).
If REQUIREMENT_BUG: stop and report to the user.
```
