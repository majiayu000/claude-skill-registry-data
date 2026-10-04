---
model_tier: medium
name: git-workflow
description: "Use when working with Git — branch naming, commit messages, PR creation, rebasing, or the code review process — even when the user says 'push this' or 'merge the branch' without naming Git."
domain: process
scope:
  write: []
  verification_reason: "execution.handler is internal, so this skill spawns no subprocess — writes happen through the agent's declared allowed_tools. No command can prove a scope the skill never executes."
execution:
  type: assisted
  handler: internal
  allowed_tools: ["Bash(git:*)", "Bash(gh:*)"]
workspaces:
  - engineering
packs:
  - engineering-base
---

# git-workflow

## When to use

Use when preparing PRs, finishing branches, or following the team's Git workflow.

Do NOT use when:
- Code writing or review (use `php-coder` or `code-review` skill)
- CI/CD pipeline changes (use `github-ci` skill)

## Live remote state first — never from memory

```
BEFORE ANY MERGE / PUSH / PR / BRANCH ACTION — OR ANY CLAIM OR QUESTION
ABOUT THEIR STATE — QUERY THE LIVE REMOTE. NEVER FROM MEMORY OR
CONVERSATION HISTORY. A PR MAY ALREADY BE MERGED OR CLOSED REMOTELY.
ASKING WHAT `gh pr view` ANSWERS IS A CHEAP QUESTION — CHECK, DON'T ASK.
```

The local branch view and the conversation's memory both go stale the moment
anyone else — a maintainer, a parallel agent, an auto-merge rule — acts on the
remote. Acting or asking on stale state is the recurring failure this section
kills (canonical: asking "shall I merge these 4 PRs?" when all four were already
merged remotely). Run first, **every time**:

```bash
git fetch origin --quiet
gh pr view <number> --json number,state,mergeStateStatus,mergedAt,baseRefName
# state: OPEN | MERGED | CLOSED — act only on the live value
```

- **A state question is self-answering** — never ask the user "is it merged?",
  "is it mergeable?", "did it get pushed?", "is it still open?". `gh pr view` /
  `git fetch` answers it. Asking is a cheap question (per `no-cheap-questions`).
- **`MERGED` / `CLOSED`** → there is nothing to merge or push; report the live
  state and stop — do not attempt the action.
- **Before merging** → re-fetch and re-read `state` + `mergeStateStatus` in the
  **same turn**; never merge on a status seen earlier in the conversation.
- **"Based on main" / "current"** → prove it with
  `npx tsx node_modules/@event4u/agent-config/src/scripts/check_branch_freshness.ts`;
  exit `1` ⇒ the branch is behind and is **not** current — merge the base in,
  regenerate the derived files, then open the PR (see
  [`/create-pr`](../../commands/pr/create.md) § 1b). Exit `0` means only that
  the gate did **not refuse**: read the line. `branch is current` is the pass;
  `NOT VERIFIED` means the base could not be reached and freshness is
  **unknown** — the gate exits `0` there on purpose so an offline push is not
  blocked, which makes reporting it as "current" the one misread it cannot
  catch. Exit `0` also covers the paths with nothing to check — a no-op in CI, a
  detached HEAD, standing on the base itself — and under `--quiet` a genuine
  pass prints nothing, so run it without the flag when you need a verdict to
  read.
  Prefer it over `git rev-list --count HEAD..origin/main`, which is wrong twice
  over: it pins `main` as the base for a branch whose PR may target something
  else, and it reads the local tracking ref — a fetch from earlier in the
  session, which is memory rather than a check. The gate asks the remote and
  resolves the base from the open PR.

## Conventions

→ See guideline `docs/guidelines/php/git.md` for branch naming, commit messages, PR conventions.
→ See `commit-conventions` rule for commit format, types, and scope rules.
→ Use `conventional-commits-writing` skill for generating/reviewing commit messages.

## Procedure: Before opening a PR

1. Quality pipeline + tests — only when `quality.local_auto_run: true` (see [`quality-tools` § Execution policy](../quality-tools/SKILL.md)): type-checker → auto-fixer → linter → type-checker, then the project's test command (detect from manifest: `php artisan test` / `vendor/bin/phpunit` (PHP), `npm test` / `pnpm test` / `vitest` / `jest` (JS-TS), `pytest` (Python), `cargo test` (Rust), `go test ./...` (Go)). Under the default (`false` / missing) skip both — remote CI on the PR is the gate; say so instead of claiming they passed.
2. Rebase onto `main`.
3. Fill in PR template completely.

## Procedure: Finish a branch

When implementation is complete and all tests pass:

```
Work complete. What would you like to do?

1. Push and create a Pull Request
2. Keep the branch as-is (I'll handle it later)
3. Discard this work
```

### Option 1: Push and create PR

1. Run quality pipeline + tests (only when `quality.local_auto_run: true`; default `false` → skip, remote CI is the gate).
2. **The push-ready sequence** — fetch → integrate the base SET → regenerate →
   verify → re-check freshness (this repo wires it as a `push-ready` task target;
   a consumer wires its own). Not optional housekeeping: see § A push closes its
   own loop. A stale push is refused, so skipping this buys the refusal.
3. `git push -u origin <branch>`.
4. `gh pr create` using PR template.
5. **Settle it** — the turn is not over at step 4:
   `npx tsx node_modules/@event4u/agent-config/src/scripts/ci_settle.ts <pr>`

## A push closes its own loop

```
A PUSH IS NOT A DELIVERY. THE EVIDENCE FOR A PUSH IS THE CI VERDICT,
NEVER THE PUSH'S OWN EXIT CODE.
BEHIND THE BASE → INTEGRATE BEFORE PUSHING, NEVER AFTER THE PR IS RED.
RED AFTER PUSHING → FIX IT IN THE SAME TURN, OR SAY PLAINLY THAT YOU DID NOT.
NEVER HAND THE USER A RED PR WITH ITS CAUSE NAMED AND UNFIXED.
```

Two halves, failing differently, over the 30 sessions and 50 PRs before
2026-09-04. **Stale base**: 25 of 50 PRs carried a `Merge branch 'main' into …`
commit (52 in total), and the three most-failing workflows are the base-relative
ones — a branch pushed behind its base was verified against a base it no longer
merges into. **Unsettled push**: 22 of 30 sessions ran `gh run view
--log-failed`, and 20 of 50 PRs carried a follow-up `fix(ci|gates|budget)`
commit. Only 19 of 50 landed with neither. Each half now has a deterministic
carrier — the pre-push hook refuses a verified-behind branch and points at the
push-ready sequence; the `push-settle` PostToolUse concern fires the moment git
reports a ref advanced. Neither replaces the discipline: the hook is skippable
with `AGENT_CONFIG_SKIP_PREPUSH_FRESHNESS=1` for a genuine WIP push, and the
settle reminder is advisory, because leaving a push deliberately unsettled is
legitimate — **ending the turn silently on one is not**.

`ci_settle` non-zero → read only the failing part
(`gh run view --job <id> --log-failed | grep -E '×|FAIL|Error'`), fix, push
again; the author of the red is irrelevant (`fix-what-you-see`). Three failed
attempts on one target → stop and surface them (`autonomous-execution` N=3).
Exit `2` is **not** a verdict — the wait timed out or the API could not be read.
Counts, carrier limits and the honest cost:
[`references/push-closes-its-loop.md`](references/push-closes-its-loop.md).

## PR template

The project uses `.github/pull_request_template.md`:
1. Jira ticket link (badge)
2. Description — what and why
3. Type of change
4. Checklist (docs, rebase, quality, review, tests, QA)
5. Links + screenshots

## Default branch

- `main` is default/production branch.
- Merge strategy: merge commits (not squash).

## Procedure: Safe squash-after-push

Use ONLY when the user explicitly authorized a squash on a branch that
is already on origin. The whole sequence runs in **one turn** — never
end the session between rewrite and push.

Trigger context: `git-history-discipline` rule routed here.

### 1. Snapshot before touching anything

```bash
BRANCH=$(git branch --show-current)
DATE=$(date +%F)
git fetch origin
git tag "safe-squash-pre/${BRANCH}/${DATE}" HEAD
git tag "safe-squash-origin/${BRANCH}/${DATE}" "@{u}"
```

Two tags = two recoveries (local tip + origin tip). Do not skip the
tags — `git reflog` is TTL-bounded and unreliable across sessions.

### 2. Verify aligned starting state

```bash
git rev-list --left-right --count HEAD...@{u}
```

- `0  0` → aligned, proceed.
- `N  0` (local ahead) → unpushed work, proceed.
- `0  N` (origin ahead) → `git pull --ff-only` first, then re-check.
- `M  N` (both non-zero) → **divergent**. Abandon the squash and run
  § Divergent-State Recovery below.

### 3. Perform the squash

Default — soft-reset path (single token-cheap rewrite):

```bash
git reset --soft "$(git merge-base HEAD <base>)"
git commit -m "<conventional commit message>"
```

Interactive rebase only when the user wants per-commit control — it
replays derived files (`dist/agent-src/`, router projections)
per commit and conflicts on every replay.

### 4. Re-push in the SAME turn

```bash
FETCHED_SHA=$(git rev-parse "@{u}")
git push --force-with-lease="${BRANCH}:${FETCHED_SHA}" origin "${BRANCH}"
git fetch origin
[ "$(git rev-parse HEAD)" = "$(git rev-parse @{u})" ] \
  && echo "OK: origin matches HEAD" \
  || echo "MISMATCH — do not end session"
```

If the push fails (pre-push hook, network, token budget):
- Fix the underlying cause **now**.
- Re-push immediately.
- Do not commit new work on top of the squashed-but-unpushed tip.
- Do not end the session until `HEAD == @{u}`.

### 5. Hand off only with verified parity

Report exactly:
- pre-squash tip SHA (from step 1)
- pre-squash tag name (for recovery)
- post-squash tip SHA == origin SHA (verified in step 4)
- PR number, if any, and confirm it picked up the new tip

## Procedure: Divergent-State Recovery

Fires when `git rev-list --left-right --count HEAD...@{u}` shows
**both** sides non-zero on the current branch.

### 1. Stop. Do not pull.

A blind `git pull --rebase` here replays remote commits on top of a
local history that may already represent the same work in a different
shape — guaranteed conflict storm in derived files, possible
double-application of the same change. This is the documented failure
mode behind `git-history-discipline`.

### 2. Tag both sides immediately

```bash
TS=$(date +%FT%H%M)
git tag "diverged-local/${TS}" HEAD
git tag "diverged-origin/${TS}" "@{u}"
```

### 3. Diagnose: which side is the correct future?

```bash
git log --oneline @{u}..HEAD   # local-only commits
git log --oneline HEAD..@{u}   # origin-only commits
git diff @{u}..HEAD --stat     # shape of local-ahead work
```

Decision matrix:

| Pattern | Future | Action |
|---|---|---|
| Local has the same logical work as origin, just reshaped (squash/rebase) | **Local** | After PR-review check (step 4), `git push --force-with-lease=<branch>:<origin-sha>` |
| Origin has commits local does not reflect (another contributor pushed) | **Origin** | Tag any local-ahead work for cherry-pick, then `git reset --hard @{u}` |
| Both sides have genuine independent work | **ask user** | Never decide silently — surface the two commit lists and let the user pick |

### 4. PR review-comment check (mandatory before any force-push)

If a PR is open on this branch:
```bash
gh pr view --json reviews,comments
# or via GitHub API: /repos/<owner>/<repo>/pulls/<num>/{reviews,comments}
```

If review comments are anchored to commits that the force-push will
erase → STOP, ask the user how to preserve them. A force-push that
destroys live review feedback is unrecoverable from the agent side.

### 5. Recover or proceed

Use the tags from step 2 to restore either side if step 4 surfaces a
problem. After resolution, verify `HEAD == @{u}` and report both
SHAs plus the tags created.

## Hard prohibitions on a pushed branch

- No `git pull --rebase` after detecting divergent state.
- No `git push --force` without `--force-with-lease=<branch>:<sha>`.
- No squash-then-end-session — the push must complete in the same turn.
- No reflog-only recovery — always tag the state explicitly first.

## Shared-branch & inherited commits — ask-before-drop protocol

Depth for the [`git-history-discipline`](../../rules/git-history-discipline.md)
Iron Law on inherited & shared-branch commits (migrated here per P4 of
`road-to-kernel-and-router.md`).

The user often works in parallel with the agent, and multiple agents may
share one PR branch. A commit that looks "unrelated" or "stray" may be
deliberate in-flight work the user expects to keep. Reseating a branch onto a
different base, `git reset --hard`-ing away inherited commits, force-pushing
over a branch you did not create, or branching from a base with unexpected
commits and then "cleaning" them out all **silently discard work** — the exact
failure that law prevents.

Before ANY of these, STOP and ask (one numbered-options prompt per
[`user-interaction`](../../rules/user-interaction.md)):

- reseating a branch's base (`git rebase --onto`, `git reset --hard <other-base>`)
  in a way that drops commits already on the branch;
- excluding / not-carrying-forward commits that were on the branch when you
  started this session;
- force-pushing (or `push <local>:<remote>`-replacing) a branch that carries
  commits you did not author;
- branching from a base with unexpected commits, then resetting them away.

**Preserve-first is necessary but not sufficient.** Even when you keep the
commits reachable (a save-branch / tag), you still **ask before** the branch
the user sees loses them — "I preserved them locally" is not a substitute for
the question, because the user may be mid-edit on the shared branch and a
force-push would clobber their in-flight work regardless of your local backup.

## Two protective stops (for the protocol phase)

1. **Pre-rewrite stop.** Before any squash / amend / rebase on a branch that is on origin: `git fetch && git rev-list --left-right --count HEAD...@{u}`. If **either** side is non-zero — STOP and run § Divergent-State Recovery. A blind `git pull --rebase` in this state is the documented failure mode. (§ Safe squash-after-push steps 1–2 implement this stop.)

2. **Post-rewrite stop.** After the rewrite, push in the **same turn** with `--force-with-lease=<branch>:<fetched-sha>` and verify `git rev-parse origin/<branch>` equals `git rev-parse HEAD`. If the push fails (hook, network, token budget) — fix the cause and re-push **before** ending the session, committing new work, or handing off. (§ Safe squash-after-push step 4 implements this stop.)

If either stop fires and resolution is not immediate → tag the state (`git tag local-rewritten-tip-<ISO-date>`) and hand control back to the user. Do not let a new session inherit a dirty divergence.

## Equivalents that are also forbidden by default

- `git rebase -i` (interactive)
- `git rebase --autosquash`
- `git commit --fixup` / `--squash` (helpers that feed autosquash)
- `git commit --amend` on already-pushed commits
- `git push --force` / `--force-with-lease` (unless paired with the protocol)
- `git reset --hard` past unpushed work the user might want
- Squash-merge of a PR via API or CLI when the user has not picked the merge strategy
- Cherry-pick rewriting that drops or reorders commits

`--amend` on the *current local* commit before the first push is the narrow exception (treated as continuing to compose the commit, not rewriting history).

## Amend-after-hook-failure trap (data-loss)

When a **pre-commit hook fails, the commit did NOT happen** — no new commit
object was created. A reflexive `git commit --amend` at that point does not
"retry the commit"; it rewrites the **previous, already-good** commit,
destroying that work. This is the one place the narrow `--amend` exception
above turns into data loss.

Recovery — never amend after a hook failure:

1. Read the hook output and **fix the cause** (the lint/test/format failure).
2. **Re-stage** the fix (`git add`).
3. Create a **NEW commit** (`git commit`, not `--amend`) — the prior commit was
   never overwritten and must stay intact.

(Migrated here from `git-history-discipline` — recovery now lives next to the
mechanism it protects.)

## Why history discipline exists

Interactive rebase + fixup loops generate disproportionate token cost on every iteration: re-running CI per replayed commit, resolving the same content conflict in two derived files (`dist/router.json`, `.windsurfrules`), losing the working tree to a stash that silently re-introduces older state. A single conflict can burn the budget of an entire feature.

A previous session squashed a pushed branch, the push hook failed at the token boundary, the session ended — and the next session saw local and origin pointing at different SHAs for the same logical work. A blind `git pull --rebase` cascaded into conflicts across every derived file. Recovery required forensic SHA-archaeology. The pre/post-rewrite stops make that sequence structurally impossible.

## When you'd be tempted

- "I want commit 3 to come before commit 2 because the topic flows better." → don't. Reviewers read the PR diff.
- "There are two `chore: regenerate` commits, ugly." → don't. They are honest checkpoints.
- "A linter caught an issue in commit 2 — let me fold the fix in." → don't. Add `fix(scope): …` on top.
- "I want to drop the WIP commit before pushing." → ask the user first.
- "Squash-merge when I open the PR will clean it anyway." → also true, also irrelevant — let the merge strategy do that work, not you.
- "My branch inherited some unrelated commits — I'll reseat it on `origin/main` so my PR is clean." → **don't, ask first.** They may be the user's parallel work or another agent's. Preserve them and ask which base the user wants.
- "The remote branch has commits I didn't author and no PR — I'll just force-push over it." → don't. No-PR is not no-owner; ask before replacing a branch you did not create.

## Output format

1. Commits following conventional commit format
2. PR description with structured sections (if creating PR)

## Gotcha

- Never commit/push/merge without explicit user permission.
- Keep subject line under 72 chars.
- Don't rebase shared branches.
- `git stash` can lose work — prefer WIP commits.

## Do NOT

- Do NOT commit directly to `main`.
- Do NOT push without running quality tools first.
- Do NOT force-push to shared branches.

## Auto-trigger keywords

- Git workflow
- branch naming
- commit message
- PR convention
