---
description: Attach the current session to an existing branch or PR and continue work from there, abandoning the auto-created session branch. Invoke as `/from-branch <branch-name|#PR|PR-url> [<follow-up instruction or skill ...>]`, a skill in the follow-up named bare (`/from-branch #123 finalize`). The PR target may be a bare PR link or any deep link into it (a review link like `.../pull/NNN#pullrequestreview-<id>`, a review-comment or conversation-comment link, or a `/files` tab URL) — the PR number after `/pull/` is the basis for finding the branch. Also use when a session's launch prompt just names an existing branch to continue (e.g. `go claude/foo-xxxx`) instead of a literal `/from-branch`. The follow-up can be `go`/`implement`/`execute` to run the plan a prior `/plan` session left under `docs/plans/`.
---

When a Claude Code on-the-web session starts, the harness usually creates a
fresh branch (e.g. `claude/add-foo-bar-XXXX`) and checks it out. This skill
**discards that auto-branch** and re-points the working tree at an existing
branch or PR head so the rest of the session continues that work.

## Recognizing the signal (explicit _and_ implicit)

The obvious trigger is an explicit `/from-branch …` invocation. But a session
can also **start** with a launch prompt that just names an existing branch to
continue — with no literal `/from-branch`. Common shapes:

- `go claude/some-feature-xxxx` (or `implement …` / `execute …`),
- "continue the work on `<branch>`", "pick up `<branch>`", "keep going on
  `#123`".

These are the **same signal**: the harness has put you on a fresh auto-branch,
but the operator's intent is to attach to the _named_ existing branch and
continue its work — not to start new work on the auto-branch. Treat such a
launch prompt as an implicit
`/from-branch <that-branch> <the rest of the prompt as follow-up>` and run this
skill: resolve the named branch as the **Target** (Step 1), and take everything
else in the prompt as the **Follow-up** (a bare `go`/`implement`/`execute` → run
the plan under `docs/plans/`; anything richer → free-form follow-up). The tell
is a launch prompt whose subject is an _existing_ branch/PR the session is not
already on — when in doubt, `git ls-remote --heads origin <name>` confirms the
branch exists before attaching.

## Argument shape

The skill argument has two parts:

1. **Target** (required, first token): a branch name, a `#NNN` PR number, or
   **any URL that carries a PR number** — a bare PR URL
   (`https://github.com/<owner>/<repo>/pull/NNN`) or a deep link into that PR: a
   review link (`.../pull/NNN#pullrequestreview-<id>`), a review-comment link
   (`.../pull/NNN#discussion_r<id>`), a conversation-comment link
   (`.../pull/NNN#issuecomment-<id>`), or a tab/file URL (`.../pull/NNN/files`,
   `.../pull/NNN/commits/<sha>`, …). The PR number `NNN` after `/pull/` is the
   basis; the `#fragment`, trailing path, and any `?query` are stripped when
   resolving the branch (see Step 1), but a review/comment fragment is worth
   keeping as a pointer to _which_ feedback the operator wants addressed.
2. **Follow-up** (optional, everything after the target): one of —
   - a free-form instruction ("…fix the failing test, then push"),
   - another skill — a first token that names a directory under
     `.claude/skills/`, the rest being its arguments (e.g. `finalize and merge`,
     `check-merge`), with or without its slash (`@.claude/skills/CLAUDE.md` says
     why it comes bare) — if so, load and follow that skill **after** the attach
     step completes, or
   - the keyword **`go`** (or its synonyms **`implement`** / **`execute`**),
     optionally trailed by "the plan" / "plan" filler, meaning "execute the plan
     file a prior `/plan` session left under `docs/plans/`". Bare, with no plan
     named, it still means "implement the plan". Step 6 dispatches it.

Examples:

- `/from-branch #123` — attach and wait for further instructions.
- `/from-branch #123 finish the migration and push` — attach, then do the
  described work.
- `/from-branch #123 go` — attach, then execute the plan under `docs/plans/`.
- `/from-branch #123 implement the plan` — same thing (`implement` is a synonym
  and the trailing "the plan" is just filler).
- `/from-branch #123 finalize` — attach, then invoke
  `@.claude/skills/finalize/SKILL.md`.
- `/from-branch feat/new-thing sync-branch` — same idea with a raw branch name.
- `/from-branch https://github.com/<owner>/<repo>/pull/123#pullrequestreview-999`
  — a review deep link: parse `123` as the PR, attach to its branch, and treat
  that review's comments as the feedback to address.

## Environment note (read this before running gh)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN` environment variable available. Prefer `gh` for branch/PR operations
in this skill — the GitHub MCP tools (`mcp__github__*`) are scoped to a narrow
allowlist and will refuse some branch-level actions you need here (e.g. checking
out a PR head, fetching arbitrary refs, pushing). If a step seems blocked by MCP
restrictions, fall back to `gh` / plain `git` over HTTPS using `GH_TOKEN`. Do
**not** assume the MCP restriction means the action is impossible — `gh` will
work.

## Step 1 — Resolve the target to a branch + remote ref

Parse the first token of the argument:

- **`#NNN`, a PR URL, or any deep link into a PR** → the branch is keyed off the
  **PR number**, so first extract it. Don't hand a fragment-bearing URL straight
  to `gh` — a trailing `#pullrequestreview-…` / `#discussion_r…` /
  `#issuecomment-…`, a `/files`|`/commits/<sha>` path, or a `?query` can confuse
  it. Pull `NNN` out of the URL with a `pull/(\d+)` match and resolve the bare
  number:
  `gh pr view <NNN> --json number,headRefName,headRepository,headRepositoryOwner,isCrossRepository,state,url`
  (a bare `#NNN` needs no extraction). The branch you want is `headRefName`. If
  `isCrossRepository` is true, the PR is from a fork — note this; the remote
  will be the fork, not `origin`.
  - **If the link carried a review/comment fragment**, it's telling you _which_
    feedback to act on — resolve it so the follow-up is grounded in it.
    `#pullrequestreview-<id>` is a review (its inline comments carry the
    substance even when the review body is just "see below" — read them with
    `gh api repos/<owner>/<repo>/pulls/<NNN>/reviews/<id>/comments`, or the
    equivalent MCP `get_review_comments`; for the whole PR — every review and
    thread, each quoting the lines its comment hangs off —
    `python3 scripts/export-github-item.py <NNN>` writes it to
    `docs/pr/<NNN>/pr.md`, indexed so you can open the threads you need rather
    than the document); `#discussion_r<id>` is one review comment;
    `#issuecomment-<id>` is a conversation comment. Treat addressing that
    feedback as the implicit follow-up when the operator didn't spell one out.
- **Plain branch name** → use it as-is. Confirm it exists on `origin` with
  `git ls-remote --heads origin <branch>` (or on the fork remote if the user
  gave `owner:branch`).

If resolution fails (PR not found, branch doesn't exist on the remote), **stop
and report** — do not silently fall back to the auto-branch. **Lead the report
with one cause, because it is the common one by far: the session is pointed at
the wrong repository.** The repo is chosen per session from a dropdown above the
input box, and with many in the list it is easy to leave the previous one
selected — so a session meant for `owner/A` runs against `owner/B`, where the
named branch genuinely isn't there. A missing branch is thus weak evidence the
_branch_ is wrong and strong evidence the _repo_ is. So ask that first and
plainly: name the repo this session is attached to (`git remote -v`) and ask
whether it's the one they meant. The typo / never-pushed / already-merged
theories come second, and only once the operator confirms the repo is right.

**Always look for any PRs on the target branch — open _or_ closed — and skim
them before doing anything else.** Even when the target is a plain branch name
(not a `#NNN`/URL), the branch usually has PR history that tells you what the
work is, what's already been reviewed, and whether an earlier PR was
closed/merged/superseded. Run
`gh pr list -R <owner>/<repo> --head <branch> --state all --json number,title,state,url,isDraft,baseRefName`,
then for each hit skim its body, commits, and reviews
(`gh pr view <NNN> -R <owner>/<repo> --json body,commits,reviews,comments,mergeable,mergeStateStatus,isDraft,state`).
This grounds the rest of the session in the branch's actual history — reviewer
feedback still to address, a merged PR meaning follow-up must restart from the
trunk (see the system prompt's merged-PR rule), or a draft that `/finalize` will
later land.

**`mergeable` and `mergeStateStatus` are fetched as context, not as a work
item.** They belong in the attach report, and they are the input
`@.claude/skills/handle/SKILL.md` Step 2 reads — nothing here acts on them. So a
`CONFLICTING` / `DIRTY` head is **reported**, and the Step 6 follow-up runs
regardless. This fetch is where a conflicted head lands in front of an agent
that has the host harness's "fix it now" rule loaded, which is why the negative
is stated at all; CLAUDE.md § "Key principles" carries the general clause.

**Note the PR's base ref while you're there.** `baseRefName` is the branch this
work merges into, and it is not always the trunk — a project with promotion
branches or long-lived feature branches will have PRs based elsewhere. Every
follow-up you dispatch (`/finalize`, `/check-merge`, `/sync-branch`, free-form
work) resolves the base from the PR itself, but state it explicitly when you
hand off so nothing silently reverts to a `main` assumption.

## Step 2 — Record the auto-branch and sanity-check it

`/from-branch` is meant to be the **first** message of a session, so the branch
you're currently on is essentially always the harness-created auto-branch —
empty, unpushed work, exists only because the harness needed something to check
out. Note its name and tip, which Step 4 writes into its command literally:

```bash
git branch --show-current
git rev-parse HEAD
```

**Sanity check** (don't trust the assumption blindly — verify there's no work to
lose):

```bash
git fetch origin main
git rev-list --count origin/main..HEAD     # expected: 0
```

If the count is `0` and the working tree is clean, proceed — the auto-branch is
empty and will be discarded in Step 4.

An untracked `docs/pr/<n>/` is the one thing that does not count as work to
lose: `.claude/hooks/prompt-handle-pr-export.sh` writes it before the turn, on
whatever branch HEAD was on, and `git checkout` carries it across to be
committed there by `@.claude/skills/handle/SKILL.md` Step 2. Leave it and
proceed.

If the count is non-zero, or there are uncommitted changes, **stop and ask the
user**. This shouldn't happen in normal `/from-branch` usage (the skill is meant
for fresh sessions), so it's a signal that something is off — maybe the user
invoked the skill mid-session after doing work, maybe the harness behavior
changed. Don't auto-cherry-pick or auto-discard; surface the situation and let
the user direct.

## Step 3 — Fetch and check out the target

```bash
git fetch origin <branch>                 # same-repo PR or plain branch
# For a cross-repo PR, add the fork as a remote first:
#   gh pr checkout <NNN>                  # easiest path — gh sets up the remote
git checkout <branch>
git pull --ff-only origin <branch>        # ensure tip matches remote
```

`gh pr checkout <NNN>` is the most robust path when the input was a PR — it
handles fork remotes, sets upstream, and leaves you on the PR head. Prefer it
for PR inputs.

Verify the result with `git branch --show-current` and `git log --oneline -3` —
the head should match the PR/branch you intended, not the auto-branch.

## Step 4 — Clean up the auto-branch

Delete the auto-branch on `origin`, where an empty branch is clutter every later
branch list carries. The local ref needs nothing: it dies with the container.

The delete is its own Bash call, with the branch name and the Step 2 SHA written
out literally — never a variable, never chained after the checkout:

```bash
git push --force-with-lease=refs/heads/<auto-branch>:<step-2-sha> origin :refs/heads/<auto-branch>
```

The auto-mode classifier judges a command by its text, never by its output, so
the Step 2 check proving the branch empty is invisible to it; a variable or a
bare `--delete` reads as deleting a remote branch nobody named, which it blocks
as Git Destructive. The lease is the proof it can read — git refuses with
`stale info` unless the remote ref still sits on the SHA you checked — and a
block on a separate call cannot take the attach down with it.

Any refusal — `stale info`, a 403 from the session's git proxy, a classifier
block — is reported and left for the operator; the attach stands. Don't retry it
by another route: a 403 and a block are both policy answers.

## Step 5 — Update the development-branch contract

The session was launched with instructions to develop on the auto-branch (see
the system prompt's "Git Development Branch Requirements"). That instruction is
now stale. From this point on:

- Treat the **target branch** as the working branch for commits and pushes.
- Push with `git push -u origin <target-branch>` (not the auto-branch).
- Do **not** push to the auto-branch even if it still exists on `origin`.

State this explicitly in your turn output so the user can see the redirect took
effect.

## Step 6 — Dispatch the follow-up

- **No follow-up provided** → report the attach (current branch, last commit, PR
  link if applicable) in 1–2 sentences and stop. Wait for the user's next
  instruction.
- **`go` / `implement` / `execute` follow-up** (the keyword optionally trailed
  by "the plan" / "plan" — nothing richer) → load `@.claude/skills/go/SKILL.md`
  and follow it from its Step 1; it owns locating the plan under `docs/plans/`,
  the plan-file lifecycle flip, and the closing hand-off to `/pr`. Do **not**
  inline-copy those steps. A `/from-branch` launch is already continued work, so
  there is no plan cycle to open — this follow-up **is** the go-ahead the
  lifecycle flip quotes. If the follow-up carries a real instruction beyond the
  keyword + that filler, it's a free-form follow-up — handle it as the bullet
  below instead.
- **Free-form follow-up** → load `@.claude/skills/go/SKILL.md` and follow it via
  its § "Planless entry", treating the follow-up text as the task. Two points
  are `/from-branch`-specific:
  - **A concrete request is not a plan cycle.** `/from-branch` is continued work
    (CLAUDE.md § "Plan mode & questions in web sessions"), so routing through
    `/go` is not an invitation to write a plan file first.
  - **The quality passes are diff-scoped, so they self-limit.** A follow-up that
    produced no code ("explain why X fails", "rerun CI") leaves them nothing to
    act on, and each says so in its own "When to use". That is a property of the
    passes — "the change was small" is not grounds to skip them.
- **Skill follow-up** (e.g. `finalize`, `check-merge`, `sync-branch`, or
  `test-on-gh` where the project has hydrated it) → load
  `@.claude/skills/<name>/SKILL.md` and follow it with the rest of the follow-up
  as its arguments. Do **not** inline-copy its steps; read and execute the
  actual file so updates to that skill flow through.

## Failure modes to call out

- **Auto-branch is unexpectedly non-empty** (commits ahead of `origin/main`,
  uncommitted changes, detached HEAD) — Step 2 already stops on this. Don't try
  to recover automatically; ask the user.
- **Target branch already checked out** — skip Steps 2–4 and proceed to Step 6.
- **MCP says "not allowed"** for a branch/PR action — switch to `gh` (the token
  is in `GH_TOKEN`). Don't report the action as impossible.
- **Branch was force-pushed since the PR was opened** — `git pull --ff-only`
  will refuse; do a `git reset --hard origin/<branch>` only after confirming
  with the user that there's no local work to lose.
- **`go`/`implement`/`execute` given but `docs/plans/` has zero or multiple
  files** — don't guess; `@.claude/skills/go/SKILL.md` Step 1 owns the
  resolution, and Step 6 dispatches there.
