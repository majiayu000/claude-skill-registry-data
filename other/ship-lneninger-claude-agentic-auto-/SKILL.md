---
name: ship
description: "Turn a finished work item into a pull request that GitHub actually links back to its issue. Reads the Work Item Brief for the branch, worktree, contract and issue id, runs /verify-before-done, composes the PR title from the modules the diff really touches, pushes from the tree that holds the commits, opens the PR, then verifies the Closing Link with verify_issue_link.py and performs at most ONE repair. Writes pr:, issue_link: and status: shipped back into the brief. Use when: user says /ship, 'open the PR', 'ship it', 'raise a pull request', or after /verify-before-done passes on a completed item. This is the last stage of the delivery chain."
user_invocable: true
---

# /ship — Pull Request and Closing Link

The final stage of the delivery chain. `/task` opened the work item and `/design-first`,
`/tdd-first` and the reviewers delivered it; this skill turns those commits into a pull
request and proves the tracker learned about it.

**Chain position:**

```
/task → /design-first → /tdd-first → reviewers → /verify-before-done → /git-commit → /ship
                                                                                      ^^^^^
```

## Context — why this skill exists

Opening a pull request is the easy half. The half that silently fails is the link back to
the work item, and it fails in a way that looks exactly like success.

**A `Closes #N` line in a pull-request body is a REQUEST for a link, never proof of one.**
GitHub declines the request without saying so when the reference is cross-repository, or
when several numbers are comma-joined onto one keyword. A pull request whose base is not the
default branch sits in a third, unsettled case: whether the reference resolves there at all
has not been shown either way, but merging into that base does not close the issue even when
the reference did resolve -- resolving a reference and closing an issue are two different
things, and this file used to conflate them. The body still reads `Closes #12`, the pull
request still merges, and the issue may still be open afterward regardless of which reading
turns out to be true. `.claude/work-item-conventions.json` states the cross-repository and
comma-joined cases as `resolvesToClosingLink: false`, and `verify_issue_link.py` exists
because of a measurement: five of the last twelve merged pull requests in the originating
repository carried no resolved link at all.

So this skill's real job is not "open a pull request." It is: open one, then **ask GitHub
whether the link resolved**, and treat the answer as the deliverable. The only admissible
proof is the forge's own resolved reference, which `gh pr view --json
closingIssuesReferences` reports — and which populates on OPEN pull requests, so the repair
can happen before merge rather than being discovered after it.

**Hard rule that governs the whole skill: never report a link you have not seen resolved.**
Writing `issue_link: closes` because the body says `Closes #N` reintroduces the exact defect
this skill exists to prevent.

## Step 0: Find the Work Item Brief

The brief is the input. Everything else is read from it, never re-derived from the chat.

1. If the user named one, use it.
2. Otherwise match the current branch against the `branch:` field of every brief in
   `.claude/work-items/`. That is the reliable key — the branch is what carries the commits.
3. If nothing matches, list the briefs whose `status:` is not `shipped` and ask.

**No brief → halt.** Do not improvise one, and do not open a pull request without one. A
brief written after the fact records what you did, not what was asked, and the acceptance
criteria are the only thing that makes the PR body checkable. Send the user to `/task`.

Read and hold: `id`, `url`, `repo`, `title`, `type`, `branch`, `worktree`, `contract`,
`partial`, `issue_link`, `status`, `base`, and the recorded outcome of the issue offer,
`issue_offer` (with `issue_offer_reason` when it is `unavailable`). Their names and allowed
values are the `offerOutcomeField`, `offerOutcomes`, `offerReasonField` and `offerReasons` keys
in `work-item-conventions.json` → `issueLink`.

**The declared base.** The brief's `base:` field, when present, is the declared base this
whole skill measures against: what "commits ahead" is counted from, what the pull request is
opened against, and what the closing link is verified against. No brief, or a brief with no
`base:` field, means the declared base falls back to the repository's default branch (confirm
it with `git symbolic-ref refs/remotes/origin/HEAD` rather than assuming `main` or `master`).
An ordinary work item with no parent therefore reads exactly as it always has, because its
declared base *is* the default branch. Every `<base>` placeholder below this point means the
declared base, never a hardcoded default branch name.

**An `id:` reading of `UNKNOWN` or `unknown` halts here.** Those are the
`unresolvedIdTokens` in `work-item-conventions.json` → `issueLink`, and they mean nobody
filled the field in — which is not the same as "this work has no issue" and must never be
treated as one. Ask the user for the issue number, or for permission to set `id: none`.

## Step 1: Pre-flight

Four checks, in order. Each has produced a wasted pull request at least once.

### 1a. Stand in the tree that holds the commits

If the brief's `worktree:` field names a path, **the commits are there, not here.** Either
enter it (`EnterWorktree` with `path:`) or run every git command in this skill with
`git -C <worktree>`. Pushing from the parent tree pushes a branch with none of the work on
it, and the pull request opens empty.

Confirm before continuing:

```bash
git -C <tree> rev-parse --abbrev-ref HEAD     # must equal the brief's branch:
git -C <tree> status --short                  # uncommitted work is not shipped
```

**Also halt in the main checkout:** if `py -3 .claude/scripts/flat_worktree.py --describe` reports `current_tree: main-checkout`, stop and say "run `/task`, or `EnterWorktree` into a worktree, then `/ship`". A detached HEAD is otherwise a halt, with one exception: the detached flat worktree `/advance` makes when the parent branch is held by the main checkout, where the branch to ship is the brief's `branch:`.

### 1b. The branch must actually differ from the base

```bash
git -C <tree> fetch origin
git -C <tree> log --oneline origin/<base>..HEAD
```

**If the declared base names a branch absent from `origin`, this fetch or log step fails
outright.** Halt and say so plainly — that is a readable reason, and reporting it as an empty
commit list would be a worse, misleading halt.

An empty list means the implementation happened somewhere else — the classic outcome of a
contract implemented in the parent tree while the branch lived in a worktree. Halt and say
so; do not open an empty pull request.

### 1c. Never ship from the default branch

If `HEAD` is `master` or `main`, halt. `/ship` opens pull requests; it does not push to the
default branch, force-push, or merge. Those three are the user's, always. The one merge this
tooling performs is a completed contract's parent pull request, and `land_contract.py` owns it,
never this skill: `/ship` opens drafts and runs before any merge it could confirm.

### 1d. Run the verification gauntlet

Invoke `/verify-before-done`. **A failure halts the ship.** This is the last gate before the
work becomes visible to other people, and "the tests were already red before I started" is
not a reason to open the pull request — it is a reason to say so and stop.

## Step 2: Compose the pull-request title

**Issue titles carry ONE effort tag; pull-request titles carry EVERY touched module.** The
two conventions are different on purpose and both live in
`.claude/work-item-conventions.json`. Read them from there. Do not restate the tag lists in
this file — that file is the single source of truth, and duplicating it is how `/task` and
`/ship` drift apart.

```
[<MODULE>]...[<MODULE>] <Title>
```

The `<Title>` is the brief's `title:` field, which `/task` already stripped of its
`[EFFORT]` prefix. **Do not re-add the effort tag.** A pull request is described by what it
touches, not by why it was raised.

### Deriving the modules

From the diff, never from memory. **Run the script; do not apply the rules by hand.**
`land_contract.py --module-tags` reads the diff and the `prTitle` block and returns the tags,
the unmapped paths and the ready-made prefix:

```bash
LANDER=
S=.claude/scripts/land_contract.py
if [ -f "$S" ]; then LANDER=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then LANDER=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  LANDER=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$LANDER" --module-tags --base origin/<base> --json
```

Read `tags` (already ordered), `unmapped` and `prefix`. Exit 0 means the tags were read. Exit 9
means the `--base` ref cannot be read: fetch origin and pass a ref that exists, then run it again. An
unmapped path is listed in `unmapped` and tagged with nothing; the script never asks, so the
ask-then-add rule under "When a path matches nothing" below still applies. If `LANDER` comes
back empty (an older install), derive the tags by hand from the changed paths:

```bash
git -C <tree> diff --name-only origin/<base>...HEAD
```

Then, for each path, walk `prTitle.map` and collect every tag whose globs match. Emit them
in `prTitle.order`, never in discovery order.

Three traps, all of which have fired before:

- **`ignore.globs` first.** Those paths contribute no tag and must not trigger the unmapped
  prompt. They are not shippable source.
- **`**` crosses a directory separator; a single `*` does not.** `src/*` means the direct
  children of `src` and never a nested file. **Python's `fnmatch` disagrees** — there `*`
  crosses `/` — so a matcher built on it over-matches and tags modules the diff never
  touched. This is a verified failure mode, recorded in the conventions file itself. Use
  `pathlib.PurePath.match` or an explicit segment-wise matcher.
- **`atLeastOne: true`.** A title with no module tag is invalid.

A map entry may also carry `coveredBy`, a list of tags that cover it. Drop the entry's tag
when the diff also carries a tag named in its `coveredBy`; keep it when the diff does not. It
is data on the map entry in the conventions file, so a repository states its own covering
pairs and the template ships none.

### When a path matches nothing

`prTitle.map` ships as an **empty template** — its `order` and `map` arrays name a project's
own source layout, and nothing else in the generic asset set does. So in a repository that
has not populated it, *every* path is unmapped.

Do not invent a tag. Ask the user via `AskUserQuestion`, quoting the unmapped paths and
proposing tags derived from the top-level directories, then **write the accepted answer back
into `prTitle.map` and `prTitle.order`** in the same turn. That is the extension seam: the
map is meant to grow the first time each module is shipped, so the second pull request
touching that module needs no prompt.

## Step 3: Compose the pull-request body

Built from the brief, so the reviewer reads what was asked rather than what you remember:

```markdown
## What this delivers
<the brief's problem statement, one paragraph>

## Acceptance criteria
- [x] <each criterion from the brief, ticked only if genuinely met>

## Out of scope
<verbatim from the brief, so a reviewer does not ask for it>

## Design
Contract: <the brief's contract: path, or "none — <size> item, routed direct">

## Verification
<the actual /verify-before-done output: what ran, what passed, what failed and why
 that failure is acceptable. Never "all tests pass" without the numbers.>

## North-star alignment
<the brief's grade, verbatim>

## Notes
<anything a reviewer should not have to discover on their own — see the declared-base
 rule below for one thing that belongs here. When the brief has no issue, add one line:
 "No issue: declined by the user", or "No issue: could not be opened (<reason>)" using the
 brief's `issue_offer_reason:`, which at this point is `create-failed` or
 `no-problem-statement`, the two reasons that stay valid at ship time>

Closes #<id>
```

Rules for the closing line:

- **One keyword per line** (`oneKeywordPerLine: true`). Comma-joining numbers onto one
  keyword is one of the ways GitHub silently declines the link.
- Same repository: `Closes #<n>`. Cross-repository: `Closes <owner>/<repo>#<n>`.
- **`partial: true` in the brief means `Refs #<n>`, not `Closes`.** The item is deliberately
  not completed by this pull request, and a closing keyword would shut a live work item.
- **`id: none` means no line at all.** That is a success path, not a defect — see Step 3.5.

**If the declared base is not the default branch**, write into the Notes section that the
closing reference will not fire the issue closed on this merge, and that `/pr-merged`
performs the close afterward — see Step 4d's `deferred-close` row for the mechanism. Draft
this now: Step 0 already knows the declared base before this step starts, so there is no
need to wait for Step 4d's verdict and edit the body back in afterward.

An unticked acceptance criterion is not a blocker to shipping, but it **must** be visible in
the body with a one-line reason. Silently ticking everything is how an item is reported
delivered and reopened a week later.

## Step 3.5: Offer to open an issue when there is none

**Gate — all four must hold:** the brief's id reading is `absent` (the `absentIdTokens` list
in `work-item-conventions.json` → `issueLink`, whose values are not restated here) **and**
`gh` is available and authenticated **and** the brief's `parent_issue:` reading is `none` or
the key is absent **and** the brief's `issue_offer:` outcome is not already a final answer.
The final answers are `declined`, and `unavailable` with the reason `no-problem-statement`
(there is still nothing honest to put in an issue body). Every other reading fires the gate:
`pending`, a missing `issue_offer:` line, `unavailable` with a `gh-missing` or
`gh-unauthenticated` reason (stale, because `gh` works now), and `unavailable` with
`create-failed`. Gate on the **id**, never on the `source:` string — that field is free
prose in practice. A resolved `parent_issue:` means this brief belongs to a Sub-Task Work
Item whose own sub-issue was already created at intake time — this offer never fires for one,
because offering to create a second issue for work that already has one is how duplicates get
made. This skill has no parent-aware mode of its own; this gate is the one place it needs to
tell the two cases apart, and it does so on the normalized reading, never on free prose.

A brief whose id is `unresolved` never reaches this offer; Step 0 already halted on it.
Offering to *create* an issue for work that may already have one is how duplicates get made.

**This point, `/task` Step 2.5 point 6 and `/design-first` Step 3.6 share their wording — one
mechanism, three call sites.** `/task` asks at intake and `/design-first` asks when a run
starts there; this is the last ask, at the moment the work becomes visible. One
`AskUserQuestion`, asked once, quoting the exact title and body. Write the body (the problem
statement, then the acceptance criteria) to a file first and pass the file, never the text
inline — Git Bash can mangle free text that starts an argument:

```bash
gh issue create --title "[<TYPE>] <bare title>" --body-file <path to the body file>
```

Record the answer in the brief's `issue_offer:` line. Never write `declined` unless the user
answered this question in this run. An assumed answer writes `pending` and never `declined`.

- On accept, write `id:`, `url:` and `repo:` back into the brief **before** Step 4 composes
  the body, so the closing line can reference it, and set `issue_offer: opened`. If the create
  command fails, write `issue_offer: unavailable` and `issue_offer_reason: create-failed`.
- On decline, write `issue_offer: declined`. `id: none` stays and the body carries no closing
  line. With the recorded-offer requirement on, Step 4d's verdict is `offer-declined`; with it
  off, the verdict is `not-applicable`. Both resolve to `issue_link: none` and are a
  **success**, not a warning.
- If `issue_offer: opened` is recorded but the id is absent, the issue has probably already been created and only the id was lost. First look for it: search the repository's issues by its exact title, and if one is found, write its id back into the brief (`id:`, `url:`, `repo:`). Only offer to create an issue when none is found.
- If `gh` is not available here, write `issue_offer: unavailable` with the matching
  `issue_offer_reason:`. That is not a final answer. Without `gh`, Step 4d halts earlier still,
  with `unverifiable` and the cause `gh-missing` (or `gh-unauthenticated`), until `gh` works
  again.

**Invent nothing.** If the brief's problem statement is empty, the offer does not fire; write
`issue_offer: unavailable` with `issue_offer_reason: no-problem-statement`.

## Step 4: Push and open the pull request

### 4a. Push from the right tree

```bash
git -C <tree> push -u origin <branch>
```

**In a detached advance worktree** publish with `git push origin HEAD:refs/heads/<parent>` (`<parent>` is the brief's `branch:`), with no force form and no `+` refspec. If refused, halt with: "the parent moved on origin; `git fetch` and `git merge --ff-only origin/<parent>` here, then retry".

### 4b. Open it

**Before the create, check the merge direction:** `py -3 .claude/scripts/merge_direction.py --head <branch> --base <declared base> --session-root <main_root from flat_worktree.py --describe>`. Any non-zero exit (11 refused, 10 unverifiable), a missing script or a timeout halts with the printed reason. Always pass `--head <branch>` as well as `--base` to `gh pr create`; in a detached advance worktree that is `--head <parent> --base <default branch>`.

Write the body to a file rather than passing it inline — a shell will mangle the backticks
and the checklist.

```bash
gh pr create --base <base> --head <branch> \
  --title "<composed title>" --body-file <path> --draft
```

`<base>` is Step 0's declared base — the brief's `base:` field, falling back to the
repository's default branch when the brief or the field is absent. For an ordinary work item
with no parent the declared base *is* the default branch, so this reads exactly as it always
has.

**Ordering matters, and no verdict below can catch a violation of it.** GitHub parses the
body's closing keywords against the base **at the moment the body is saved**, and does not
re-parse when the base changes afterwards. The command above already satisfies this — `--base`
and `--body-file` are one `gh pr create` call. If this pull request already exists and needs
retargeting, the retarget and the body **must** be written in the same `gh pr edit` call
(`gh pr edit --base <base> --body-file <path>`) — never a `--base` edit followed by a later,
separate body edit. The command looks correct either way; only the ordering decides whether
the link resolves.

Open as a **draft** unless the user asked otherwise, and say that you did. A draft is
reversible; a review request pinging five people is not.

**In a Claude Code cloud session GitHub's GraphQL endpoint is blocked (HTTP 403), but REST works.**
The scripts read through REST there. For the actions `gh` would send over GraphQL, use the CCR
routes on `api.github.com` named in the 403 text instead of `gh pr ready` / `gh pr merge --auto`:
`POST /repos/{owner}/{repo}/pulls/{n}/ccr/ready_for_review`, `POST .../ccr/convert_to_draft`,
`PUT` or `DELETE .../ccr/auto_merge`. A pull request's resolved closing issue links are
GraphQL-only, so Step 4d returns `unverifiable` with cause `graphql-unavailable` there: confirm the
link on github.com or from a local checkout, and never accept the body text as proof.

### 4c. Capture the number

```bash
gh pr view --json number,url,isDraft
```

### 4d. Verify the Closing Link — the step that earns the skill its name

Never conclude this from the body you just wrote. Ask the forge:

```bash
py -3 .claude/scripts/verify_issue_link.py --brief <brief path> --pr <n> --json
```

The script performs **no mutation** of any GitHub object; it only reads. It returns a
`verdict` from a closed set of nineteen. Branch on it:

| Verdict | Meaning | Action |
|---|---|---|
| `deferred-close` | The declared base is not the default branch — either GitHub resolved the closing reference or the body carries one GitHub has not resolved; either way this base will not fire it on merge | Proceed. `issue_link: deferred`. `/pr-merged` owns the close, after confirming the merge. |
| `linked` | GitHub reports a resolved closing reference | Success. `issue_link: closes` |
| `not-applicable` | No issue to link (`id: none`) and the recorded-offer requirement is off, or no conventions data file | Success. `issue_link: none` |
| `offer-declined` | No issue, and the brief records that the user declined the offer | Success. `issue_link: none` |
| `offer-unavailable` | No issue, and the brief records a reason the offer could not be made that still holds (`create-failed` or `no-problem-statement`) | Success. `issue_link: none` |
| `exempt-partial` | `Refs #N` on a deliberately partial item | Success. `issue_link: refs` |
| `absent-repairable` | No link, and the body can be repaired | **The one repairable row** — see below |
| `offer-unrecorded` | No issue, and the brief records no decision about opening one (or records a reason that no longer holds) | HALT. Ask the Step 3.5 question, record the answer in `issue_offer:`, then re-run Step 4d. Do not create the pull request again: it is already open. If `issue_offer` is `opened`, first look for the issue already created, searching by its exact title, write its id back into the brief, and only offer to create one when none is found. |
| `still-absent` | Repair was attempted and the link is still missing | HALT. `issue_link: unresolved` |
| everything else | `unverifiable` (including the cause `brief-path-unresolved`, which means pass the brief path as it exists from the current directory), `malformed-id`, `unresolved-id`, `issue-unreachable`, `issue-already-closed`, `pr-not-open`, `foreign-closing-ref`, `unexpected-closing-ref`, `undeclared-target`, `refs-without-partial` | HALT. Report the `reason` and `remediation` verbatim |

**Whether a closing reference resolves at all from a non-default base is unsettled** — do not
build a check on either reading of it. **What is settled: merging into a non-default base
does not close the issue, whether or not the reference resolved.** That is why `deferred-close`
fires either way: its two conditions (a resolved match, or a body carrying a reference GitHub
has not resolved) cover both readings, so a pull request against a declared, non-default base
reaches this verdict regardless of which reading turns out to be true. `/pr-merged` performs
the close after confirming the merge and reading the sub-issue's own state first — that
exception belongs to `/pr-merged`, never to this skill, which runs before the merge it would
need to confirm even exists.

**The repair loop runs at most ONCE** (`maxRepairAttempts: 1`). On `absent-repairable` the
result carries a `bodyDiff`. Apply it with a single `gh pr edit --body-file <path>`, then
re-invoke the script **with `--repair-attempted`** and take the second verdict as final:

```bash
gh pr edit <n> --body-file <repaired path>
py -3 .claude/scripts/verify_issue_link.py --brief <brief path> --pr <n> --repair-attempted --json
```

Do not loop further. A second failure is a real condition — usually a cross-repository
reference or a non-default base — and hammering `gh pr edit` will not change it.

**On any halting verdict the pull request stays open and the work is not lost.** Report the
verdict, the reason and the remediation, and say plainly that the tracker was not linked.
That is an honest partial delivery; a silent `status: shipped` is not.

## Step 5: Write the outcome back into the brief

Only from Step 4d's verdict, never from intent:

- `pr:` — the URL from Step 4c.
- `issue_link:` — `closes` | `refs` | `none` | `unresolved` | `deferred`, exactly as the
  verdict maps. `deferred` is written only by the `deferred-close` verdict — the declared base
  will not fire the closing keyword on merge, and `/pr-merged` owns the eventual close.
  **Never write `manual`.** That value exists in `linkStates` for a human who reconciled an
  issue by hand, and an agent writing it fakes a human action.
- `status:` — `shipped` only when Step 4d returned a non-halting verdict. On a halting
  verdict leave the previous status and record why.

Commit the brief update on the branch so the record travels with the work.

**`/ship` never flips the contract's `Status`.** The flip is automatic after the merge, by `/pr-merged` (see Step 6 of the design-first skill). A flip here would reach the default branch as `implemented`, and the script would then find the contract already implemented, with no checklist fill and no run log.

## Step 6: Worktree lifecycle, after the merge

Nothing to run here for a delivered work item. Its worktrees and merged branches are removed
automatically by Delivery cleanup (`cleanup_delivered.py`), which `/pr-merged` and `/advance`
run on every call once the contract reads `implemented` at the default branch. An abandoned
worktree that was never delivered is removed with `git worktree remove <path>` alone, never with
git's worktree `prune`, which would also remove other work items' stale entries.

Never `rm -rf` the directory — that leaves stale metadata and git keeps the branch reserved.
Do not remove a worktree the user entered by path for their own purposes.

## Anti-patterns (halt immediately)

- **Reporting a link because the body says `Closes #N`.** The body is a request. Only the
  forge's resolved reference is proof, and `resolvesToClosingLink: false` says so in the
  conventions file.
- **Treating an `UNKNOWN` id as "no issue".** Absent and unresolved mean opposite things.
  Folding them together is how an unresolved field ships unlinked and is reported as success.
- **Writing `issue_link: manual`.** Reserved for a human.
- **Looping the repair.** One attempt, by contract.
- **Pushing from the parent tree when the brief names a worktree.** The pull request opens
  with none of the work in it.
- **Guessing module tags instead of deriving them from the diff**, or building the matcher
  on `fnmatch`, where `*` crosses `/` and silently over-matches.
- **Re-adding the `[EFFORT]` tag to the pull-request title.** Effort tags belong to issues,
  module tags to pull requests.
- **Ticking every acceptance criterion to make the body look clean.**
- **Opening the pull request when `/verify-before-done` failed.**
- **Merging, force-pushing, or pushing to the default branch.** None of the three belong to
  this skill.

## When NOT to use this skill

- Mid-flight work that is not finished — `/ship` is a terminal stage, not a checkpoint.
- A change with no work item and no intent to create one; use `/git-commit` and stop.
- Repositories whose forge is not GitHub. The verification step is `gh`-only, and without it
  the link cannot be proven — which, by this skill's own rule, means it must not be claimed.

## Skill integrations

- **Fed by** `/task`, which writes the `id`, `url`, `repo`, `contract`, `branch`, `worktree`
  and `partial` fields this skill reads back.
- **Runs** `/verify-before-done` at Step 1d as a hard gate.
- **Drives** `.claude/scripts/verify_issue_link.py` at Step 4d — the only production caller.
- **Shares** `.claude/work-item-conventions.json` with `/task`: that file owns the effort
  tags, the module map and the `issueLink` keyword data, and neither skill restates them.
- **Shares its Step 3.5 wording** with `/task` Step 2.5 point 6 and `/design-first` Step 3.6 —
  one mechanism, three call sites, so a free-text item is offered an issue at intake (or at
  design time) and once more at ship time unless the user already answered.
- **Follows** `/git-commit`, which produces the commits this skill pushes.
