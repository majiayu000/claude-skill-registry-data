---
name: help
description: "Side-route orientation skill. Use when the user asks 'what's next', 'where am I', or is returning to a repo mid-pipeline and wants to know which skill to run next. Reads repo state (branch, PRs, issues, research archive, milestones) and recommends one next step with a one-line reason. Not for executing work — only for routing."
---

# Help

Read the current repo state and recommend the next pipeline step. This skill does not do any work itself — it orients the user by pointing to the right next skill, citing the state it observed so the recommendation can be overruled.

This is the front door for users who are returning to a repo after a break, onboarding to Skill Kit for the first time, or stuck mid-pipeline and unsure which skill to invoke next.

## Invocation Position

This is a side-route skill. It reconnects to the main pipeline at whichever skill the diagnosis points to.

Use `/help` when:

- The user is starting a session in a repo that already uses Skill Kit and wants to know where they are in the pipeline
- The user has been away from a feature for a while and needs a refresher on what state the work is in
- A new team member is learning the pipeline and wants guidance rather than reading all of `references/SYSTEM-OVERVIEW.md`
- The user explicitly asks "what should I do next?" or "where am I?"

Do not use `/help`:

- To actually run the recommended skill — `/help` only recommends; the user runs the next skill themselves
- When the user already knows the next step and just wants to execute
- As a substitute for reading `references/SYSTEM-OVERVIEW.md` when the question is conceptual rather than state-specific
- For tasks unrelated to the feature pipeline (bug fixes with no upstream artifacts, one-off cleanups)

## Process

### 1. Gather repo state

Build a state snapshot in two phases: first detect the base branch sequentially (so downstream calls can reference it), then dispatch the read-only snapshot commands in parallel.

**Phase 1a — detect the base branch (run first, sequentially):**

```bash
# Prefer the remote's HEAD, fall back through common names
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's@^origin/@@')
if [ -z "$BASE_BRANCH" ]; then
  for candidate in main master prod develop trunk; do
    if git rev-parse --verify "$candidate" >/dev/null 2>&1; then BASE_BRANCH=$candidate; break; fi
  done
fi
# A name is not a ref. $BASE_BRANCH names the branch (for `--base`, `git switch`);
# $BASE_REF points at it, and is the only thing safe as a range endpoint.
if git rev-parse --verify "origin/$BASE_BRANCH" >/dev/null 2>&1; then
  BASE_REF="origin/$BASE_BRANCH"
else
  BASE_REF="$BASE_BRANCH"
  echo "note: origin/$BASE_BRANCH does not resolve — measuring against the local branch, which may be stale" >&2
fi
echo "base=$BASE_BRANCH ref=$BASE_REF"
```

Do not hardcode `main` or `master` — not every repo uses them (Skill Kit's own repo uses `prod`, and many others use `develop`, `trunk`, or a team-specific name). If `origin/HEAD` is not set and none of the fallback candidates exist, ask the user for the base branch name before continuing.

**Residual:** `$BASE_REF` is only as fresh as the last `git fetch`, and on a triangular fork (or a remote not named `origin`) `origin/$BASE_BRANCH` may be absent or track your fork rather than upstream — the `else` branch then falls back to the local branch, which is the stale-ref behavior this guard exists to avoid. It says so on stderr rather than falling back silently, because a plausible wrong answer with no signal is what let this defect live for five months. If the counts look wrong, `git fetch` and re-run, or set `BASE_REF` by hand.

**Phase 1b — gather the snapshot (run in parallel, each call independent):**

```bash
# Current branch and commits ahead of the detected base branch
git branch --show-current
git log --oneline "$BASE_REF..HEAD"

# Open PR for the current branch, if any
gh pr list --head "$(git branch --show-current)" --state open --json number,title,url

# Research archive entries for this repo (durable, per-user, outside the repo)
REPO_SLUG=$(git config --get remote.origin.url | sed -E 's|.*[:/]([^/]+)/([^/.]+)(\.git)?$|\1-\2|')
ls -t "$HOME/.claude/research/$REPO_SLUG/" 2>/dev/null

# Open issues with PRD or slice labels, or in open milestones
gh issue list --state open --json number,title,labels,milestone --limit 50

# The frontier — which open issues are actually takeable right now.
# `state` is the GraphQL enum here: uppercase OPEN, not REST's lowercase.
# `totalCount` counts blockers in every state, which is what distinguishes
# "blockers all closed" from "never wired" (see the note below).
gh issue list --state open --limit 100 --json number,blockedBy,assignees \
  --jq '.[]
       | {number,
          open_blockers: [.blockedBy.nodes[] | select(.state == "OPEN") | .number],
          ever_wired: .blockedBy.totalCount,
          assignee: (.assignees[0].login // null)}' 2>/dev/null

# Open milestones with remaining feature issues
gh api "repos/{owner}/{repo}/milestones?state=open" --jq '.[] | {title, open_issues, closed_issues}' 2>/dev/null
```

The frontier call is independent of every other call in this batch and cannot fail on a guessed ref, so it belongs inside the parallel batch. Filtering nodes to `state == "OPEN"` means a slice whose blockers have all closed reports an empty `open_blockers` with no bookkeeping, so this value can be trusted as current without re-reading the blockers.

Repos whose slice issues predate native dependency wiring (see `/prd-to-issues` §7) will report an empty `open_blockers` for everything. `ever_wired` tells that apart from a genuinely flat graph without guessing: if any issue reports `ever_wired > 0`, the repo *is* wired and the empty lists are real. If every issue reports `ever_wired: 0` and the bodies contain prose `Blocked by #N` lines, no edge was ever written — fall back to the prose and say so in the recommendation rather than asserting the whole backlog is takeable.

**Parallel tool-use gotcha.** In Claude Code, when one bash call in a parallel batch errors, the harness cancels its in-flight siblings — one bad ref takes down the whole snapshot. This is why Phase 1a must run first (and alone): if base-branch detection fails, nothing in Phase 1b will try to reference `$BASE_BRANCH`. Do not chain `&&`/`||` against a guessed branch name inside a parallel batch to "save a round trip" — it will fail noisily on any repo that does not match your guess.

If `gh` is not authenticated or the repo is not a GitHub repo, note which signals you could not gather and work from the rest. A missing signal is not a failure — it just narrows the recommendation.

### 2. Classify the state

Walk through these checks in priority order. The first one that matches is the recommendation. Stop at the first match — do not try to give the user three options.

| # | Signal | Recommendation | One-line reason |
|---|---|---|---|
| 1 | Open PR on current branch | Merge the PR, then run `/compound` | "You have an open PR on `<branch>` — if review is done, merge it and capture lessons." |
| 2 | Current branch has commits ahead of base, no open PR | `/pre-merge` | "You have `<N>` commits ahead of `<base>` with no PR yet — `/pre-merge` creates it and runs the architectural review." |
| 3 | Open slice issues referencing a PRD, none closed | `/execute` on the highest-priority slice with an empty `open_blockers` | "You have `<N>` open slice issues under PRD #`<prd>` — `/execute` is the next step for the first unblocked one." |
| 4 | Open slice issues referencing a PRD, some closed | `/execute` on the next slice with an empty `open_blockers` | "You have `<N>` open and `<M>` closed slices under PRD #`<prd>` — `/execute` picks up the next unblocked slice." |
| 5 | Open PRD issue with no slice issues | `/prd-to-issues` on PRD #`<prd>` | "PRD #`<prd>` is shaped but not yet decomposed — `/prd-to-issues` breaks it into slices." |
| 6 | Recent research archive entry for this repo, no open PRD issue matching its feature | `/write-a-prd` | "A recent research file for `<feature>` is archived but there is no PRD issue — `/write-a-prd` turns it into a shaped pitch." |
| 7 | Planning milestone with a `research-ready` feature issue | `/research` on the `research-ready` feature | "Milestone `<name>` has a `research-ready` feature — run `/research` on it." |
| 8 | Planning milestone with only `roadmap bet` features | Promote one feature to `research-ready`, then `/research` | "Milestone `<name>` has only `roadmap bet` features — pick one, promote it, then `/research`." |
| 9 | Shipped work but no `docs/solutions/` entry since the last merge | `/compound` | "The last merge shipped work that has not yet been compounded — run `/compound`." |
| 10 | QA bugs open and no active feature work | `/execute` on the highest-priority QA bug | "You have `<N>` open QA bug issues — `/execute` to work through them." |
| 11 | None of the above — clean slate, no feature in flight | `/shape` (or ask the user what they are trying to do) | "No feature work is in flight — `/shape` is the normal starting point." |

"Unblocked" in signals #3 and #4 means an empty `open_blockers` from the Phase 1b frontier call — read it, do not infer it from `Blocked by` prose in the issue bodies. This is the same rule `/prd-to-issues` §9 and the Ralph loop prompt use, so all three selection sites agree by construction rather than by coincidence.

### 3. Present the recommendation

Present one recommendation, with the one-line reason and the state signals that triggered it. Use this format:

```
## Where you are

<one paragraph: the state signals you observed, stated as facts>

## Next step

**`/<recommended-skill>`** — <one-line reason>

## Why this skill

<one short paragraph: what the skill produces and how it connects to the observed state>

## If this is wrong

<2-3 alternative next steps for common cases where the heuristic might have missed>
```

Example output (for signal #6, a recent research archive entry with no matching PRD issue):

```
## Where you are

Current branch: main. No open PRs. Research archive has `~/.claude/research/owner-repo/nextjs-middleware-migration-2026-04-05.md`, dated 2026-04-05 and pointing at a Next.js 16 middleware migration. No open PRD issue matches it (I searched open issues for "middleware" and "Next.js" and found nothing). No open slice issues. No active milestone.

## Next step

**`/write-a-prd`** — a recent research file is present but there is no PRD issue for the work it covers.

## Why this skill

`/write-a-prd` takes a completed research document and turns it into a shaped PRD filed as a GitHub issue. It consults the archived research automatically, so the recommendations in the research will flow into the pitch without you re-summarizing them. Expect 10–15 minutes of interview, then a PRD issue ready for `/prd-to-issues`.

## If this is wrong

- If the archived research is stale and no longer matches what you intend to build, run `/correct-course` first to clean up before shaping again.
- If you want to rewrite the research for a different approach, run `/research` again (it will produce a new archive entry with today's date).
```

### 4. Stop

After presenting the recommendation, stop. Do not start the recommended skill automatically, and do not ask the user if they want you to run it — the user decides. If the user wants to run it, they will invoke it themselves.

If the user responds with "that's wrong, I'm actually doing X," do not re-run the full state gather. Just answer the corrected question directly — your recommendation was based on signals, not authority.

## Heuristic Rules

- **One recommendation, not three.** The user is asking for a next step, not a menu. Pick the best match and commit to it.
- **Cite the state.** Every recommendation must reference the specific signal that triggered it — a file path, an issue number, a branch name. Vague recommendations lose trust fast.
- **Prefer the earliest unblocked step.** If the user has both an open slice issue and an unrelated merged PR that was never compounded, recommend compounding first only if the slice work is paused. When in doubt, recommend what unblocks forward motion on the most recent work.
- **Never fabricate signals.** If you could not read open issues because `gh` is unauthenticated, say so. Do not guess.
- **Never auto-run the recommendation.** `/help` is advisory. The user runs the next skill.

## What This Skill is NOT

- **Not a task tracker.** GitHub issues and PRs are the task tracker. This skill reads that state, it does not replace it.
- **Not a replacement for the pipeline overview.** If the user is asking conceptual questions about how the pipeline works, pull the relevant sections from `references/SYSTEM-OVERVIEW.md` and `references/using-this-pack.md` (bundled alongside this skill) rather than improvising. For deeper reading, point the user at the repo originals: <https://github.com/chrislacey89/skills/blob/main/SYSTEM-OVERVIEW.md> and <https://github.com/chrislacey89/skills/blob/main/docs/using-this-pack.md>.
- **Not a wizard.** It does not walk the user through shaping, research, or planning. It tells them which skill to start and gets out of the way.

## Handoff

- **Expected input:** a question like "what should I do next?" or ambient uncertainty about pipeline position
- **Produces:** a single next-step recommendation with cited state signals and a one-line reason
- **Feeds into:** whichever pipeline skill the recommendation points at — `/shape`, `/research`, `/write-a-prd`, `/prd-to-issues`, `/execute`, `/pre-merge`, or `/compound`
- **What comes next:** the user runs the recommended skill themselves — `/help` does not invoke anything
