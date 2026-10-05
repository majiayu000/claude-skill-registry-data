---
name: code-review
description: |
  Review **the change you are currently making** — working-tree diff, or a branch's diff vs
  its base — for correctness bugs AND reuse / simplification / efficiency cleanups, fanning
  the review out across parallel sub-agents, then **apply the fixes** (`--fix`) or post them
  as inline PR comments (`--comment`). Use when asked to "code review", "review my diff",
  "review this change", or as the review stage of a ship pipeline. For reviewing someone
  else's PR, prefer your harness's PR-review skill. This is the portable, bundled reviewer —
  if your harness ships a richer native code-review skill, prefer that one.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "[--fix] [--comment]"
---

# Code Review — diff in, findings (and fixes) out

Review the change for two classes of issue and report them with evidence:

1. **Correctness bugs** — logic errors, broken edge cases, race conditions, silent
   failures / swallowed errors, security holes, resource leaks, wrong types, off-by-ones.
2. **Quality cleanups** — reuse (an existing helper already does this), simplification
   (dead code, needless indirection, over-abstraction), and efficiency (obvious N², a
   query in a loop, redundant work).

> **Portability note.** Needs only a shell (`git`), file reading, and editing. It *uses*
> sub-agents when your harness has them (for breadth — see below) but never *requires* them:
> with no sub-agent support it runs the same passes sequentially. If your harness provides a
> richer native review (e.g. Claude Code's built-in `code-review` with an `ultra` cloud
> mode), a ship orchestrator should call *that* instead and treat this skill as the fallback.

## Flags (parse from the arguments)

| Flag | Effect |
|------|--------|
| `--fix` | After reporting, **apply** the high-confidence findings to the working tree |
| `--comment` | Post findings as inline review comments on the open PR (needs `gh`) |

There is no effort/depth knob: thoroughness comes from **fanning the review out across
parallel sub-agents** (below), scaled to the size of the change — not from a reasoning dial.

## Sub-agents — fan the review out, then verify

Where your agent can spawn sub-agents — Claude Code `Agent`/Task, Codex `worker` / custom
agents, Grok parallel sub-agents, Hermes `delegate_task`, OpenClaw `sessions_spawn` — use
them; the review is embarrassingly parallel. If your agent can't, run the same passes
sequentially yourself: the result is identical, just slower.

1. **Fan out reviewers.** Spawn one sub-agent per review dimension, scaled to the diff — a
   tiny change needs one or two, a large one warrants the full set:
   - **correctness** — logic, edge cases, races, error handling, types
   - **security** — injection, authz, secrets, unsafe input
   - **performance** — N², query-in-loop, needless allocation / IO
   - **reuse & simplification** — an existing helper does this; dead code; over-abstraction

   For a large diff, split each dimension by area/file too. Give each sub-agent the diff, the
   files it must read, and instructions to return findings as `{file:line, severity,
   description, fix}` — reading the real code, not just the patch.

   > **Stacked PRs — pin the base explicitly.** If the branch's base is not the repo default,
   > the change is stacked on a parent branch. Say so in *every* sub-agent prompt — e.g.
   > `Base: origin/<baseRefName> (stacked on PR #N, NOT main)` — and pass both the merge-base
   > SHA (`git merge-base origin/<baseRefName> HEAD`) and the head SHA. Sub-agents that
   > default to comparing against the default branch produce confused analysis and flag
   > changes that belong to the parent PR.
2. **Collect + dedupe.** Merge the findings; drop duplicates (same file:line + issue).
3. **Verify adversarially.** For each surviving finding, spawn an independent verifier
   sub-agent whose job is to **refute** it: open the cited `file:line`, run the check, and
   default to "not a real issue" unless the evidence holds. Keep only findings that survive.
   This is what lets the fan-out be wide without drowning the report in false positives.

## Workflow

1. **Scope the diff.** Default: uncommitted changes — `git diff` (and `git diff --cached`).
   Reviewing a branch/PR: the full diff vs base — `git diff <base>...HEAD`.
2. **Review.** Run the fan-out + adversarial verification above (or, with no sub-agents, do
   each dimension and each verification as a sequential pass yourself).
3. **Report.** Group surviving findings by file. For each: `file:line`, severity
   (🔴 bug / 🟡 should-fix / 🟢 nice-to-have), one-line description, and the fix. Keep it
   scannable. If the change is clean, say so plainly — never invent findings to look busy.
4. **Apply (`--fix` only).** Apply the 🔴 and 🟡 findings as minimal, surgical edits that
   match surrounding style. Leave 🟢 nice-to-haves unless trivial. Never change behavior
   beyond the finding. Re-read each edit to confirm it's correct.
5. **Comment (`--comment` only).** Post each finding as an inline comment on the PR via
   `gh` (see below). Batch them into one review where the harness supports it.

## Posting inline comments (`--comment`)

Needs the `gh` CLI authenticated against a GitHub remote. Resolve the PR for the current
branch, then comment per finding:

```bash
PR=$(gh pr view --json number -q .number)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
# one inline comment on the PR's head commit:
gh api "repos/$REPO/pulls/$PR/comments" --method POST \
  -f body="🟡 <finding>. <suggested fix>" \
  -f commit_id="$(gh pr view "$PR" --json headRefOid -q .headRefOid)" \
  -f path="<file>" -F line=<line> -f side=RIGHT
```

If `gh` is absent or the change isn't a PR, fall back to printing the findings and say so
(fail loud — never silently skip the requested `--comment`).

## Rules

- **Evidence over vibes.** Every finding cites `file:line` and a concrete reason.
- **Quality and correctness are both in scope**, but a real bug always outranks a cleanup.
- **Surgical fixes only.** Don't refactor untouched code or restyle the file.
- **Don't fabricate.** "No issues found" is a valid, honest result.
