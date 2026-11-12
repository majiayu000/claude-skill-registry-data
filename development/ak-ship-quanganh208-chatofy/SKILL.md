---
name: ak-ship
description: "Ship a completed branch via tests, review, commit, push and PR, with official/beta aliases, Kongming advice and reviewed merge plus CI convergence."
when_to_use: "Invoke when work is done and needs a PR."
category: workflow
keywords: [ship, PR, merge, push, release, advice, kongming, review-pr]
argument-hint: "[official|stable|main|beta|dev|next] [--both] [--advice] [--merge] [--skip-tests] [--skip-review] [--skip-journal] [--skip-docs] [--social] [--yes-post] [--yes-post-private] [--dry-run]"
license: Proprietary
metadata:
  author: agentkit
  version: "2.4.0"
---

# Ship: Unified Ship Pipeline

Single command to ship a feature branch. Continue through authorized repairs and verification; stop for evidenced external blockers or unresolved material decisions.

**Inspired by:** gstack `/ship` by Garry Tan. Adapted for framework-agnostic, multi-language support.

## Arguments

| Flag | Effect |
|------|--------|
| `official`, `stable`, `main` | Normalize to `official`; ship to the detected default branch (main/master). Full pipeline with docs + journal |
| `beta`, `dev`, `next` | Normalize to `beta`; ship to the detected development branch (dev/beta/develop). Lighter pipeline, skip docs update |
| (none) | Auto-detect: if base branch is main/master → official, else → beta |
| `--both` | Dual-target ship: beta stage first, then a gated stable stage (see Dual-target ship). Supersedes a positional mode token |
| `--advice` | Run the ship-to-PR path under advisory-only `kongming` supervision |
| `--merge` | After PR creation, activate `ak-review-pr <PR> --fix --reply --merge`; append `--advice` when both flags are present |
| `--skip-tests` | Skip test step (use when tests already passed) |
| `--skip-review` | Skip pre-landing review step |
| `--skip-journal` | Skip journal writing step (also honors `journal.auto=false` config preference) |
| `--skip-docs` | Skip docs update step |
| `--social` | Opt-in: after the PR is created, compose a build-in-public journal draft and publish it to social channels (see "Build-in-public publishing" below). Off by default — never fires on a plain `/ak-ship`. |
| `--yes-post` | Required alongside `--social` to actually publish. Without it, the social step runs in dry-run mode: renders and prints the per-channel posts, makes no API call, exits 0. |
| `--yes-post-private` | Required alongside `--social --yes-post` when the repo is private — an explicit second opt-in for posting about non-public work. |
| `--dry-run` | Show what would happen without executing |

## Ship Mode Detection

```
Normalize one positional mode token before side effects:
  - official | stable | main → official
  - beta | dev | next        → beta
  - multiple or unknown tokens, including unknown `--flags` → stop and ask; never guess
If mode = "official" → target = main/master (auto-detect default branch)
If mode = "beta"     → target = dev/beta/develop (auto-detect dev branch)
If no mode token      → infer from current branch naming:
  - feature/* hotfix/* bugfix/* → official (target main)
  - dev/* beta/* experiment/*  → beta (target dev/beta)
  - unclear                    → ask_user capability
```

Aliases select a canonical mode; they do not force a literal branch name.

## Dual-target ship (`--both`)

When `--both` is present, ship to both targets in sequence — the beta pipeline
first, then a gated stable stage. `--both` supersedes a positional mode token;
if one is also given, warn once and continue in dual-target mode. It composes
with `--advice`, `--merge`, and the skip flags. With `--dry-run`, it simulates
the beta stage only and reports the stable stage as not-simulated.

Load `references/dual-stage-workflow.md` for the stage sequencing, the stable
stage gate (beta PR exists; with `--merge`, beta CI green first), the
promotion-convention path with its unrelated-work stop, and the completion
contract. The stable stage never force-pushes, never bypasses branch
protection, and never merges a promotion PR that sweeps unrelated work without
asking.

## Advisory supervision (`--advice`)

When `--advice` is present, the workflow MUST spawn `kongming` to supervise
the local ship-to-PR path, because the flag's entire contract is that a
supervisor saw the change. Load `../ak-brainstorm/references/advisory-supervision.md`
for supervisor identity, host detection, and model routing (Claude
subscription → Fable 5; Codex → `gpt-6-astra` + low effort; Cursor →
`claude-fable-5-high`). Kongming returns counsel, never code; the main agent
remains responsible for every decision, edit, and gate.

Mandatory normal-path checkpoints:

- **After pre-flight, before mutation** — pass the resolved canonical mode,
  detected target, branch/diff summary, constraints, and ask for a go/no-go plus
  the highest risk to watch.
- **After tests and local review, before versioning/commit/push/PR writes** —
  pass test evidence, findings and fixes, intended PR scope, and ask whether the
  evidence supports proceeding.
- **When stuck or before a high-stakes decision** — pass approaches tried, the
  exact blocker or irreversible choice, and ask for a legitimate next step.

Empty/error counsel is recorded as a non-fatal advisory failure; authoritative
ship gates still decide whether to proceed. If `--advice` is present and no
delegation call occurs, the workflow is incomplete.

When `--merge` is also present, forward `--advice` to `ak-review-pr`. That skill
exclusively owns PR-level advisory checkpoints, review/fix/reply, merge
readiness, and post-merge CI. Do not duplicate those steps here.

`--advice` never bypasses tests, review blockers, branch protection, security
policy, or the downstream merge-readiness gate.

## Batch-landing repositories

Some repositories land pull requests through their own batch-landing owner (a
merge train, landing bot, or scheduled routine) rather than per-PR CI and
author merges. Treat a repository as batch-landing only when its own
instructions (`CLAUDE.md`, `AGENTS.md`, or its contributing or workflow docs)
declare that owner; never infer it from branch names or missing CI. When they
do:

- Run the local verification those instructions require, and put the evidence
  they name (for example a verification receipt line) in the PR body.
- Create the PR ready for review. Keep it draft only when that evidence is
  missing.
- Stop after Step 12b, even with `--merge`: skip Step 13, and do not enable
  auto-merge, update the branch, merge, or wait for PR checks. Report
  `Merge=delegated` with the landing owner and `CI=n/a`.
- Social publishing (Step 14) waits for the landing owner's merge; report it
  as not yet eligible.

## When to Stop (blocking)

- On target branch already → abort
- Merge conflicts that can't be auto-resolved → stop, show conflicts
- Test failures outside repair authority, unavailable dependencies/credentials, or repeated unresolved failure → report exact evidence and remaining work
- Critical issues requiring a scope/product decision → ask_user capability; repair ordinary branch-caused issues within scope
- Major/minor version bump needed → ask_user capability

## When NOT to Stop

- Uncommitted changes → include only files owned by this task and intended for this ship; preserve unrelated dirty files
- Patch version bump → auto-decide
- Changelog content → auto-generate
- Commit message → auto-compose
- No version file → skip version step silently
- No changelog → skip changelog step silently

## Pipeline

```
Step 1:  Pre-flight      → Branch check, mode detection, status, diff analysis
Step 2:  Link Issues      → Find/create related GitHub issues
Step 3:  Merge target     → Fetch + merge origin/<target-branch>
Step 4:  Run tests        → Auto-detect test runner, run, check results
Step 5:  Review           → Two-pass checklist review (critical + informational)
Step 6:  Version bump     → Auto-detect version file, bump patch/minor
Step 7:  Changelog        → Auto-generate from commits + diff
Step 8:  Journal          → Write technical journal via /ak-journal (see the shared "Journal step — opt-out" contract: --skip-journal flag or journal.auto config skips)
Step 9:  Docs update      → Update project docs via /ak-docs update (official only)
Step 9b: Finalize plan    → ak plan update --status completed (plan-backed; foreground, staged by Step 10)
Step 10: Commit           → Conventional commit with version/changelog
Step 11: Push             → git push -u origin <branch>
Step 12: Create PR        → gh pr create with structured body + linked issues
Step 12b: Link plan↔PR    → ak plan update --linked-pr <n> (plan-backed; no close until merge)
Step 13: Review + merge   → if --merge: ak-review-pr <PR> --fix --reply --merge [--advice] (skipped in batch-landing repositories)
Step 14: Social publish   → if --social: after Step 13 terminal-green when merging; otherwise after the existing green-PR-check gate
```

**Detailed steps:** Load `references/ship-workflow.md`
**Auto-detection:** Load `references/auto-detect.md`
**PR template:** Load `references/pr-template.md`
**Writing language:** Load `kits/engineer/skills/ak-review-pr/references/writing-language.md`
**PR body contract:** Load `kits/engineer/skills/ak-review-pr/references/pr-body-contract.md`

## Writing language + PR body (#1195)

Before Step 12, resolve language with
`WL_BIN=.claude/hooks/lib/writing-language.cjs
test -f "$WL_BIN" || WL_BIN=kits/core/hooks/lib/writing-language.cjs
node "$WL_BIN" --json` and author the PR body in
that language. Titles stay English conventional commits. The body must include
the seven evidence sections (plus Linked Issues / Ship Mode). Prefer honest
`None` / `Not run` / `Unavailable` over invented narrative.

## Build-in-public publishing (`--social`)

Opt-in only — without `--social`, ak-ship behavior is byte-identical to
today. When passed, after Step 12b and any requested Step 13 review/merge,
Step 14 composes
a build-in-public journal draft from the PR/issue/plan context (`Why this?`
/ `What changed` / `The tricky bit` / `What's next` / an optional thanks),
persists it via `ak journal create` (so every social post traces back to a
durable journal entry), then publishes to the channels tagged
`groups.build_in_public` in `.agentkit/journal.yaml` (falling back to all
configured channels if that group isn't defined).

Guardrails (never bypassed by any flag):
- **CI must be green.** If the PR's checks are failing, the step refuses to
  post and explains why — the ship itself still completed.
- **`--skip-journal` skips the whole social step**, not just the journal
  write — a social post always requires its journal record.
  `journal.auto = false` does **not** suppress this step: `--social` is an
  explicit user choice, distinct from the automatic per-ship journal (Step 8).
- **Collaborator-only signal.** Only PR review comments from
  `COLLABORATOR`/`MEMBER`/`OWNER` associations feed the draft's "The tricky
  bit" section — outside commenters are never quoted into a public post.
- **Dry-run by default.** Without `--yes-post`, the step renders every
  channel's post and stops — no API call. Re-run with `--social --yes-post`
  to actually publish.
- **Private-repo confirmation.** If the repository is private, `--social
  --yes-post` alone still refuses; add `--yes-post-private` too.

Full step-by-step commands: `references/release-and-social-workflow.md` (Step 14).

## Token Efficiency Rules

- Steps 4 (tests) and 5 (review): delegate to `tester` and `code-reviewer` subagents — don't inline
- Steps 8 (journal) and 9 (docs): run in **background** — don't block pipeline
- Step 2 (issues): use single `gh` command batch — avoid multiple API calls
- Skip steps early via flags to save tokens on unnecessary work
- Beta mode auto-skips: docs update (Step 9)
- Capture step outputs inline — don't re-read files already in context

## Quick Start

User says `/ak-ship` → run full pipeline → output PR URL.
User says `/ak-ship beta` → ship to dev branch with lighter pipeline.
User says `/ak-ship official` → ship to main with full docs + journal.
User says `/ak-ship stable` or `/ak-ship main` → normalize to official mode.
User says `/ak-ship dev` or `/ak-ship next` → normalize to beta mode.
User says `/ak-ship beta --advice --merge` → supervised ship, then reviewed merge and CI convergence.
User says `/ak-ship --both --merge` → beta PR, reviewed beta merge to green, then the gated stable stage.

## Output Format

```
✓ Pre-flight: branch feature/foo, 5 commits, +200/-50 lines (mode: official)
✓ Issues: linked #42, created #43
✓ Merged: origin/main (up to date)
✓ Tests: 42 passed, 0 failed
✓ Review: 0 critical, 2 informational
✓ Version: 1.2.3 → 1.2.4
✓ Changelog: updated
✓ Journal: written (background) / skipped (opt-out via --skip-journal or journal.auto)
✓ Docs: updated (background)
✓ Committed: feat(auth): add OAuth2 login flow
✓ Pushed: origin/feature/foo
✓ PR: https://github.com/org/repo/pull/123 (linked: #42, #43)
✓ Advice: 2 checkpoints completed / failed with reason / not requested
✓ Review: Approve / blocked(reason) / not requested
✓ Merge: merged / delegated(landing owner) / blocked(reason) / not requested
✓ CI: green / red / pending / n/a
```

## Important Rules

- **Tests gate the ship.** Run them unless valid same-revision evidence supports `--skip-tests`. Classify failures, fix authorized branch-caused defects and rerun affected checks; do not advance to publication with red evidence.
- **Never force-push.** Use a plain `git push`; a force push rewrites history other people have already pulled.
- **Ask only for unresolved expensive decisions:** scope-changing critical findings and major/minor version bumps. Repair in-scope defects and continue on established defaults.
- **Auto-detect everything.** Test runner, version file, changelog format, target branch — detect from project files.
- **Framework-agnostic.** Works for Node, Python, Rust, Go, Ruby, Java, or any project with a test command.
- **Subagent delegation.** Use `tester` for tests, `code-reviewer` for review, `journal-writer` for journal, `docs-manager` for docs. Don't inline.
- **Reviewed merge delegation.** `--merge` activates `ak-review-pr` with `--fix --reply --merge`; `--skip-review` skips only Step 5, so that the downstream review still runs.
- **Fail closed on downstream state.** When `--merge` is requested, social publishing and merged/green completion claims require terminal `Verdict=Approve`, `Merge=merged`, and `CI=green`; a blocked, red, pending, or unavailable tuple stops those actions. Without `--merge`, the existing Step 14 green-PR-check gate still owns social eligibility.
- **Dry-run has no delegation side effects.** `--dry-run` stops before `kongming`, `ak-review-pr`, or social publishing.
- **Background tasks.** Journal and docs run in background to not block the pipeline.

## Workflow Position

**Typically follows:** `/ak-code-review` (ship after review passes)
**Typically precedes:** `/ak-journal` (document after shipping)
**Related:** `/ak-code-review` (review before shipping), `/ak-test` (test before shipping)
