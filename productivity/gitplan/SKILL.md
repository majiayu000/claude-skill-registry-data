---
name: gitplan
description: Plan and execute coherent Conventional Commit groupings for tangled working tree changes — multiple intertwined logical edits that need to be split into separate, reviewable commits.
metadata:
  website: "https://photostructure.com/coding/clean-commits/#gitplan"
---

**Applicability is about how tangled the changes are, not how many files they touch.** Invoke this skill when the working tree mixes multiple intertwined logical changes that need untangling into separate commits — even if that's only a handful of files. Skip it when the changes are trivial or superficial, no matter how many files they touch: formatter runs, lint autofixes, typo/grammar fixes, or edits that obviously belong in a single commit.

# Review and plan git commits

> More on these workflows: [photostructure.com/coding](https://photostructure.com/coding/)

## User direction

User instructions take precedence over this skill's grouping, review, and
approval defaults. If the user says "commit" or "approved, commit" for an
understood scope, use [stage](../stage/SKILL.md) to verify and commit that scope.
Unless the user also requests review first, do not restart planning, invoke
review skills, wait for a second opinion, or ask for approval again. This rule
also applies when the instruction arrives during the workflow below.
When project instructions require review before every commit, a commit
instruction for changes that review has not finished on since they last
changed runs the review first, and only an explicit instruction to skip review
skips it.

Propose focused, coherent, reviewable commits. Honor grouping the user has
already specified or approved.

If the repository has a layered structure (e.g. shared utilities → core → feature packages → app), work through it from the lowest-level layer upward so dependencies are committed before their consumers.

## Workflow

### Phase 1: Identify Themes

1. Scan all current changes with `git status` and `git diff --stat`. When
   subagents are available and the diff is large, use them to preserve context
   and summarize distinct areas.
2. For complex diffs, use `git diff -U150` but limit JSON/lockfiles to the first ~50 lines.
3. Identify logical themes/groupings. Each theme must have a **single coherent purpose** — a unifying "why" that explains every file in the group. If you can't state the purpose in one sentence without using "and", split the theme. **Never create catch-all buckets** like "housekeeping", "misc", "cleanup", or "various fixes". Every file belongs in a theme because of what it _does_, not because it's small or doesn't fit elsewhere. Orphan files that truly don't relate to any theme get their own single-file commit.
4. **Bundle related docs/plans with their code changes.** If a planning doc, design note, or task file corresponds to a theme, commit it alongside the code it describes — never lump it into a separate "docs" commit. Docs that don't correspond to any code change can go in a docs-only commit.
5. Present the themes to the user as a numbered list with brief descriptions. Order by increasing complexity/risk.
6. Ask: "Which theme should we focus on first?"

### Phase 2: Stage, Review, and Commit (per theme)

1. Stage only files belonging to the selected theme using `git add <files>`, including any related docs/plans decided in Phase 1.
2. **Kick off the second-opinion reviewers on the staged diff, in the background if the host supports it** — steps 2-3 of [`../second-opinion/SKILL.md`](../second-opinion/SKILL.md). Start them first so they run while you review. The reviewers have no staged-only scope, so name the staged file list in the prompt: "review these staged files: `<list>`. The other uncommitted changes belong to later commits; read them where they interact with the staged code. Report any defect the staged diff causes, including in callers or dependencies outside it."
3. Review the staged changes yourself using the `review-staged` skill. Use a capable model — reviews are important.
4. Collect the second opinions, then vet every finding from every review against ground truth and report the result — steps 4-7 of the gate. Accept and veto only with evidence.
5. If issues are accepted:
   - Present them clearly with priority, problem, and proposed fix.
   - Apply fixes incrementally, re-staging as needed.
   - Re-review until clean.
6. Present the gate's report, including its per-batch pass counts and model verdicts, with the proposed commit message, and ask for approval if commit authorization is still missing. When the user approves, commit immediately — no new review or second confirmation.
   - **Commit messages drive the changelog.** The body should describe user-facing behavior changes (what users will see/experience), not just implementation details. Lead with the "what changed for users" — implementation notes are secondary.

Skip the second opinion when the user directs you to commit, asks to skip
review, or the theme is purely mechanical (formatter run, lockfile bump). When
project instructions require review before every commit, skip it only when the
user explicitly asks to skip review.
Honor an explicit "review, then commit" sequence. Report review status briefly;
do not turn a skipped review into another permission request.

### Phase 3: Repeat

1. Check `git status` for remaining changes.
2. If more changes exist, return to Phase 1 and pick the next theme.
3. Continue until all changes are committed or the user stops.

## Review Guidelines

The per-theme review in Phase 2 is the `review-staged` workflow. Its method
and finding format live in
[`../review/references/single-pass.md`](../review/references/single-pass.md);
don't restate them here.

This skill owns only the grouping decision: whether each theme is a single
coherent commit, and how to split it if not.
