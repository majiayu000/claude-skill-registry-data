---
name: kickoff
description: >-
  Start-of-session ritual — get oriented in the repo (branch, working tree, open
  PRs/issues) and compose a descriptive session name, emitting a
  copy-pasteable /rename command for the user. Use when a working session is
  starting and needs orientation before beginning work. Invoke as /kickoff
  [topic or issue #].
allowed-tools: Read, Glob, Grep, Bash(git status:*), Bash(git branch --show-current), Bash(task --list-all:*), Bash(task status:*), Bash(gh pr list:*), Bash(gh issue list:*), Bash(gh label list:*)
---

# Kickoff Session

Formerly `/orient`.

**Arguments:** $ARGUMENTS

Orient at the start of a working session and give it a descriptive name so it
is easy to identify later in the session picker and the Claude mobile app.

## 1. Get oriented

Prefer the repo's own status plumbing when it exists; fall back to raw
commands otherwise:

- If **both** targets exist — `task --list-all 2>/dev/null | grep -q 'status:git'`
  and the same check for `status:gh` — run `task status:git` and
  `task status:gh`. Caution: `task` executes the checked-out Taskfile; on an
  untrusted branch (e.g. reviewing a stranger's PR), use the raw fallback
  instead.
- Otherwise run `git status -sb`, `git log --oneline -5`,
  `gh pr list --limit 10`, and `gh issue list --limit 10`.

Separately, as a credential preflight, check
`task --list-all 2>/dev/null | grep -q 'status:creds'`. Where present, run
`task status:creds`. The same untrusted-branch caution applies — on an
untrusted branch, skip this probe rather than run it. There is no raw
fallback for it: if the target is absent, note "no creds probe available" in
the report and move on.

Keep all of this bounded — if `gh`, `task status:git`, `task status:gh`, or
`task status:creds` hangs or is unauthenticated, note it and move on rather
than blocking the session start. A missing or failed creds probe is a
**report item, never a kickoff blocker** — kickoff proceeds either way and the
summary says what couldn't be checked.

**Sweep for stale claims.** The claim `/claim` makes has no owner once its
session ends: `/integrate` stops before the merge, `/wrap` leaves an open PR
alone, and a personal-account board has no automation — so when the maintainer
merges later, the assignee, `claim:*` label, and card status all
survive with nobody left to clear them. Session start is where that gets
caught, because it is the one step that runs without depending on the session
that made the claim:

```sh
gh issue list --repo <owner/repo> --assignee @me --state all --limit 200 \
  --json number,title,state,labels,url
# ...and by marker, because a claim can outlive its assignee. `gh issue list
# --label` is exact-match (no prefix), so enumerate every live claim namespace
# label the repo actually carries — family-level, model-pinned, and legacy —
# and query each. This must be a CHECKED read: a bare `for lbl in $(gh label
# list ...)` runs zero iterations and falsely reports a clean sweep on an
# expired token or rate limit, hiding the marker-only claim this exists to find
# (gh-verification.md). On an org repo the event-driven release cannot recover
# such a claim once its assignee is gone UNLESS the timeline still proves a
# covering assignment interval for the claim comment (its trust gate needs
# the owner, or that proof — see claim-lifecycle.md's trust-gate note); a
# claim with no such interval ever recorded is exactly the gap this sweep
# backstops — do not skip it on a failed enumeration, surface it:
if ! claim_labels="$(gh label list --repo <owner/repo> --limit 1000 --json name -q \
    '.[].name | select(startswith("claim:") or startswith("agent:"))')"; then
  echo "warning: could not list claim labels — the marker-only sweep is INCOMPLETE; retry or check auth" >&2
fi
while IFS= read -r lbl; do
  [ -n "$lbl" ] || continue
  gh issue list --repo <owner/repo> --label "$lbl" --state all --limit 200 \
    --json number,title,state,assignees,url
done <<<"$claim_labels"
```

**Query both, and union the results.** `/wrap` runs its cleanup as separate
commands on purpose — a combined `gh issue edit` fails wholesale when the repo
lacks the label — so a partial cleanup that removes the assignee and then fails
on the label or `Status` is an expected outcome. An assignee-only
query can never see exactly that leftover, which is the case this sweep is
supposed to recover.

`--state all`, not `open`: the motivating case is a *closing* PR merged after
the session ended, which auto-closes the issue — so `--state open` filters out
exactly the stale claims this sweep exists to find. The explicit `--limit`
matters too; the default returns 30.

**Assignment alone is not a claim.** Plenty of people assign themselves planned
backlog work. Flag an issue only when a claim marker corroborates it — an
`claim:*` label (or a legacy `agent:*` one), a card at `In Progress`, or a
`/claim` claim comment — and then only if its work has finished or stalled.

**A claim comment is history, not state.** Comments are never deleted, so the
claim comment survives its own release — and where the issue was already
assigned to you, `/wrap` correctly leaves that assignment in place too. Both
markers then persist forever, and treating the comment alone as current would
make every future `/kickoff` re-report the same long-released claim. So the
comment counts only when it is the **latest trusted `Claiming —` comment after
the latest trusted `Claim released —` comment**. A newer trusted claim record
supersedes an earlier refresh record without releasing the active claim.
Prefer the live markers (`claim:*` label, card at `In Progress`); fall back to
that one current comment only after checking what follows it.

Report what survives that test as loose ends and point at `/wrap` for the
release commands. Do not clear anything here: this step orients, it does not
mutate.

## 2. Compose the session name

Kebab-case, at most ~40 characters, most-specific-first. Pick the source in
this priority order:

1. The topic or issue number given in the arguments.
2. The issue/PR implied by the current branch or conversation.
3. The branch name.
4. Ask the user.

Pattern: `<topic>` or `<topic>-<issue#>` — e.g. `dev-workflow-skills-138`.
No `done-` prefix and no date (the picker already shows recency).

## 3. Emit the rename

You cannot rename the session yourself — there is no tool or command for the
model to do it. Say so explicitly, and output the command for the user to
paste, on its own line in a fenced block:

```text
/rename dev-workflow-skills-138
```

## 4. Record the name

Restate the chosen name in prose — e.g. "Session name:
`dev-workflow-skills-138`" — so `/wrap` can recover it from conversation
context even after compaction.

## 5. Summarize

Finish with 3–5 orientation bullets: current branch, clean/dirty tree,
notable open PRs or issues, credential readiness, and the suggested next
step. If implementation work is coming, suggest `/claim` next — it
sanity-checks the issue and claims it, and `/implement` expects that claim to
already exist.

**Credential readiness bullet.** Summarize what `task status:creds` found:
what is logged in, what is missing or unknown, and the remedy the status
output itself named (e.g. `gh auth login`, `codex login`,
`claude auth login`). Preserve the probe's own distinctions rather than
flattening them — "credential stored (not validated)" is not the same as
authenticated, `n/a` (not configured, or the CLI is absent) is not the same
as missing, and `unknown` is not the same as logged out. Quote the remedy
from the status output, not from memory. If the probe was skipped (untrusted
branch) or unavailable (target absent) or it failed, say so in this bullet —
that is the report item. This covers whether a login exists,
not what it is permitted to do: no line here establishes a token's **scopes**.
Whether a specific issue needs permissions the CI credential lacks is
`/claim`'s per-issue preflight vetting, not this probe's.
