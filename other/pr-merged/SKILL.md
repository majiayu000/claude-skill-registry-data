---
name: pr-merged
description: "The closing phase of one sub-task: once its pull request has merged, record the completion and work out which pending sub-tasks that releases. Verifies the merge by asking GitHub rather than trusting the claim, writes a completion record stamped verified: github, recomputes the released set, and hands that set back to its caller. Iteration belongs to /advance, not to this phase. Use when: the loop closes a sub-task, or a person says /pr-merged, 'PR 40 is merged', 'these PRs merged, continue', or returns after merging work outside a running loop. Reads a contract handoff plan and writes the result and state stores."
user_invocable: true
---

# /pr-merged — record a finished sub-task and release what it was blocking

A contract decomposes into sub-tasks. A sub-task often waits for another one to land in the
default branch. Nothing watches for that landing. When the merge happens outside the session,
the waiting sub-tasks stay waiting until a person remembers them.

This skill is how you tell the session a merge happened. It confirms the merge really
happened, records the finished sub-task, works out what that unblocks, and continues.

```
/pr-merged 40 41
   verify merged (ask GitHub)  ->  map to sub-task  ->  write completion record
   ->  recompute released sub-tasks  ->  continue
```

## The logic lives in a script — this file is the human front door

### Finding the script, under either install mode

The script ships with the plugin **and** with a vendored copy, but it sits at a different
place in each. Resolve it once, then use the result:

```bash
PRM=
S=.claude/scripts/pr_merged.py
if [ -f "$S" ]; then PRM=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then PRM=$CLAUDE_PLUGIN_ROOT/$S
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
  PRM=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$PRM" --contract <slug|path> --status --json   # read-only
```

A vendored project finds its own copy first. A plugin install finds the running version through `$CLAUDE_PLUGIN_ROOT`, then the install `installed_plugins.json` records, then the newest cache folder by version number. **If `PRM` comes
back empty, stop and say so** — the loop's every rule lives in that file, and a skill that
cannot find it can only guess at what it says.



**One implementation, two front doors.** A skill is instructions for a model, and the
caller may be a program rather than a session, and a program cannot invoke a skill. Both call the same
script instead, and both therefore behave identically. Two implementations of these rules
would drift the moment either changed.

When a run that names a contract applies, read `references/contract-completion.md` in full before continuing. If it cannot be read, stop and report the missing file; do not continue from memory.

When a writing run returns `flipped` and memory capture is enabled, that reference's step 5a asks one separate capture question and records the receipts in the linked brief. It reads `../design-first/references/central-memory.md` for the ground rules shared with `/design-first` Step 1.5. Step 5a is never built from a dry run, never joins the records confirmation, and no outcome of it blocks the records pull request.

```bash
py -3 "$PRM" --contract <slug|path> --pr <n|link> [--pr <n|link> ...] --json
py -3 "$PRM" --contract <slug|path> --status --json   # read-only
```

`--pr` takes either a bare number, in this repository, or an `https://` link, which may name
**another** repository — the sibling plugin, for instance. A link is resolved by `gh` per call,
never through a process-wide `--repo` flag or a `GH_REPO` environment variable.

**The records step: `/pr-merged --records <contract-slug> [--discard-differing <path>]`.** Records
that `/pr-merged` wrote stay in the starting tree until they are pushed to the stable records branch
and the copy is swept. The Next Command names this step whenever `records_unpushed` or
`records_stranded` of `--status --json` is not empty. It runs the procedure "The records pull
request" in `references/contract-completion.md` and nothing else: no pull request is verified and no
record is written. "Nothing to do" applies only when `records_reading` is `ok` and both lists are empty.
`--discard-differing <path>` is the owner's exit for a copy that differs from origin; run it only when
the owner names the path.

```bash
py -3 "$PRM" --contract <slug> --sweep-records --from "$START" [--removed <records worktree>] [--discard-differing <path>] --json
```

`--sweep-records` deletes a starting-tree copy only when it is identical to a copy on
`origin/<default>`, or to the stable branch's tip while a pull request holds it; keeps and names every
other copy; and prints one Tree-clean line per `--from` and `--removed` tree as its last lines
(`tree_lines`). It reads `records_reading` first: `unverifiable` exits 10 and deletes nothing.
`--local-evidence-only` skips deleting and pushing for this run (`records_action:
skipped-by-owner`). It never changes the evidence, never lifts a hold and never unblocks `/advance`'s
dispatch, which stays refused (exit 12) until a persistent read failure's named cause is fixed.

**An older `pr_merged.py` halts these steps.** When a `--status --json` or `--sweep-records` report has
no `records_reading` key, or any call exits 2 with `unrecognized arguments:` naming `--sweep-records`,
`--from`, `--removed`, `--discard-differing` or `--local-evidence-only`, stop and say: "this
`pr_merged.py` predates 0.14.0: sync the vendored copy (`tools/sync-plugin.cmd`)". An absent key never
reads as "nothing pending". `--record-subtask`, `--preconditions`, `--locate-parent`, the dispatch
packet and every JSON refusal carry no such keys and are never judged this way. Any other exit 2
without a JSON `error` is printed verbatim and halts.

**The scope gate.** The script takes the records reading only where it can work: when the working
directory is a git tree root (it has a `.git` entry of its own) that has an `origin` remote. This gate
exists for in-process callers written before 0.14.0, which call `main()` from a folder with no repository
metadata or with a process runner that refuses, and which behave exactly as they did. It never looks at
where the contract file sits: a path-form `--contract` that points at another tree's concepts folder still
carries the `records_*` keys, and `--dispatch` still exits 12 on unpushed records.

This follows the pattern already used here: `/ship` shells out to `verify_issue_link.py`, and
`/design-first` to `derive_area.py`. The script owns the rules. This file explains the result
to a person and offers what to do next.

**The script is covered by tests** at `.claude/scripts/tests/test_pr_merged.py` — 760 cases over
identity, parsing, block classification, verdicts, records, releases, conflict detection, the
Hand-Resolved Summary (including the unread-commit count and its single-fetch walk), the
cross-repository pull-request path, the `GH_REPO` refusal, the Next Command and the Sub-Task
Cycle, plus the records leftover sweep, the evidence rule and the re-run guard. Measured by running
`py -3 .claude/scripts/tests/test_pr_merged.py` and reading its own
`unittest` summary line: `Ran 760 tests ... OK` (exit code 0). They were mutation-probed: disabling the
verification check, reading a missing dependency line as none, and counting scope notes as
sub-tasks each turn the suite red.

**Read the script's output rather than re-deriving it.** Everything below describes what the
script does and how to act on what it returns. Where this file and the script disagree, the
script is what runs, and the disagreement is a defect in this file.

## Where this sits — a phase, not a loop

**This skill does not iterate. It closes one sub-task and hands back.**

Three levels run this project's work, and each owns exactly one thing:

| Level | Owner | Owns |
|---|---|---|
| Outer chain | `/flow` | One work item, from intake through to shipped |
| Inner loop | `/advance` | Iterating the pending sub-tasks, one step per merge |
| Sub-task phase | **this skill** | Closing out one sub-task once its work has merged |

A sub-task's life runs: implement, test, review, verify, commit, open a pull request, merge.
**This skill is what happens after that merge.** It records the completion, works out what the
completion releases, and returns that set to whoever called it. Choosing what runs next, and
starting it, belongs to the loop.

Background and history: `references/background.md`. It holds no rules, so reading it is optional.

### Two ways it is invoked

Both are triggered by a session, not by a background process. Nothing calls this phase on its
own, because nothing watches for a merge. The difference is who is driving.

**`/flow` is driving.** It is carrying a work item and a merge just landed. The phase verifies,
records, recomputes and returns the released set. It asks nothing, because `/flow` already
holds the authority the operator gave it, and it continues with `/advance`.

**A person is driving.** They merged something, possibly after resolving a conflict, and came
back to say so. The phase does exactly the same four things. The only difference is the ending:
it reports the released set and points at `/advance` rather than continuing by itself.

**The work in between is identical.** Verification, the record and the release computation do
not care who called them. Only the handoff differs.

**Neither path iterates.** This phase closes one sub-task. `/advance` starts the next. A person
merging is what joins them, which is why a merge-gated contract cannot run unattended.

## The rule that governs the whole skill

**A claim that a pull request merged is a request to check, never a fact.**

The user may be misremembering. A pull request may be closed without merging. It may have
merged into something other than the default branch. Writing a completion record on an
unverified claim releases dependent work that has nothing to build on.

Nothing here acts until GitHub has said it merged. This is the same discipline the
closing-link check in `/ship` uses, and for the same reason.

## Step 0: Parse the invocation

**Called by the loop,** the input is a contract identifier, a sub-task identifier and a pull
request. Skip the discovery below; the caller already knows which sub-task this is.

**Called by a person,** accept any mix of these, separated by spaces or commas:

| Form | Meaning |
|---|---|
| `40`, `#40` | Pull request in the current repository |
| `https://github.com/<owner>/<repo>/pull/40` | May be another repository; respect the owner and name in the link |
| *(nothing)* | Discover candidates and let the user pick |

**Pass a link to the script exactly as given, as its own `--pr` argument** — never split into a
bare number, never routed through a process-wide `--repo` flag or a `GH_REPO` environment
variable. `gh` resolves the owner and name in the link per call; the script decides for itself
whether that repository is this one or another (Step 1 below).

With no argument:

```bash
gh pr list --state merged --author @me --limit 20 --json number,title,mergedAt,headRefName
```

Present the list. Never act on all of it unprompted.

## Step 1: Verify each pull request really merged

```bash
gh pr view <number> --json number,state,mergedAt,mergeCommit,headRefName,baseRefName,url,closingIssuesReferences
```

Judge each against this table. The set is closed, and the first match wins.

| What GitHub reports | Verdict | Do |
|---|---|---|
| Merged, with a timestamp and a merge commit | `merged` | Continue with this one |
| State open | `not-merged` | Skip it, and say so. Write nothing |
| Closed, no merge timestamp | `closed-unmerged` | **Not a skip.** The sub-task could not be delivered — see the failure section below |
| Merged, base is not in the declared base set | `merged-elsewhere` | **Halt this one and ask.** It landed on a branch nobody declared, so dependents may still have nothing to build on |
| No such pull request | `not-found` | Skip it, and report the number |
| GitHub client missing or unauthenticated | `unverifiable` | **Halt the whole skill** |

**The declared base set** is the repository default branch plus every sub-task's own declared
base already on record in the state store. Under this contract's topology, every task pull
request merges into a parent branch rather than the default branch, so a merge landing there is
`merged`, not `merged-elsewhere` — the measured PR #173 defect this rule exists to close.
`merged-elsewhere` stays reachable for a base that is genuinely undeclared: nobody said the
dependents could build on that branch.

**A link naming another repository is checked differently.** The script asks GitHub for that
repository's own identity and compares it against the checkout's own — never against this
repository's declared base set. Its accepted base is that OTHER repository's own default branch
alone; landing anywhere else is still `merged-elsewhere`, a halt. Its sub-issue is still closed
**here**, in this checkout's own repository — `close_sub_issue` never takes `--repo`, and the
sub-issue number comes from this checkout's own state store, never from the other repository. A
link naming THIS repository is checked exactly like a bare number.

**On `unverifiable`, stop everything.** Without GitHub there is no way to tell a merged pull
request from a closed one, and guessing writes a lie into the completion store. Tell the user:

```
winget install --id GitHub.cli
gh auth login
```

Do not install it yourself. Do not reach the GitHub interface with a token taken from the
environment.

## Step 1.5: Flag hand-resolved files in the pull request's history

A file resolved by hand during a merge was never tested in the form that landed. With no
continuous integration, it is the highest-risk content in the pull request. Find it and say so.

**Look at the history, not the merge commit.** GitHub refuses to merge a conflicted pull
request, so the pull request's own merge commit is clean by construction. The resolution
happened earlier, when somebody merged the default branch into their own to clear it.

Verified on this repository: pull request #126's merge commit reports no resolved files, while
a merge commit inside its branch reports fourteen.

```bash
gh pr view <number> --json commits --jq '.commits[].oid'
# then, for each commit that has two parents:
git show --cc --name-only --format="" <sha>
```

The combined diff lists only files whose content differs from **both** parents. A clean
automatic merge lists nothing. Anything listed was either a hand-resolved conflict, or a
change introduced during the merge that existed in neither side. Treat both the same way:
they entered the codebase without ever being reviewed as a normal diff.

**Report them, do not block on them.** Name the pull request, the merge commit and the files.
Releasing dependents on top is the caller's decision, and it should be an informed one.

**Where this does not work.** A squash or rebase merge produces no merge commit, so nothing is
detectable. Say that plainly rather than reporting a clean result. This repository merges with
merge commits, so the check applies here.

**A commit that could not be read is never rendered clean.** When `git show --cc` itself fails
on a merge commit, or `git rev-list` cannot read a commit at all, that commit's own contents are
unknown — not a clean merge, and not the same as "no merge commit was found". The script counts
these separately as **unread commits**, and a summary with one or more unread commits never
reads `clean`, whatever its file list says: it reads `not detectable (unread commits: N)`
instead, with the file list's own suffix when files were also found. When the commit is simply
absent from this clone (never fetched here), the script tries **one** fetch, aimed at that
commit's own pull-request ref, before giving up and counting it unread — so a single absent
commit costs at most one fetch per run, never one per commit.

**What conflicts here in practice.** The files that collide most are the append-heavy shared
ones — the registries, the journal, and agent memories — not source code. A conflict in those
usually means a lost entry rather than broken behaviour, which is worth saying in the report so
the reader calibrates.

**A cross-repository pull request is never walked at all.** None of its commits exist in this
clone, so the script never spends a read (or a fetch) on any of them — every one of its reported
commits is counted unread, without exception, and its Hand-Resolved Summary reads accordingly.

## Step 2: Map each merged pull request to a sub-task

**First, load the sub-tasks.** Take them from whichever source exists, in this order:

1. A generated `task-map.yaml` for this contract, when one exists.
2. **The contract's `## Implementation Handoff` blocks.** Each `###` block is one sub-task.
   Its heading names it, such as Backend, Frontend or Data pipeline. Its
   `**Files to touch:**` list is its scope. This is the normal source today.

**Sub-task identity is derived from the block, never stored twice.** It is
`t<ordinal>-<slug of the name>`, so `### 2. Backend (…)` is `t2-backend`. One identity names
three things: the branch `task/<contract-slug>/<id>`, the completion record
`<id>.yaml`, and the sub-task named in the pull request title.

Then match each merged pull request to a sub-task, stopping at the first hit:

1. The head branch is `task/<contract-slug>/<id>`. This is the normal case and it is exact.
2. The pull request title names the identity.
3. The state store records that branch against a sub-task.

All three are string matches against a derived identity. **There is no heuristic over file
lists,** because there no longer needs to be one — the branch carries the answer.

**A pull request that matches no sub-task is reported, never guessed at.** Say which number
could not be placed and carry on with the rest.

**A pull request that matches two sub-tasks** means an identifier is ambiguous. Halt that one
and show both rather than picking.

**If the contract has neither a generated plan nor handoff blocks,** say so and stop.
Do not invent a decomposition.

## Step 2.5: Close the sub-issue, once the merge is confirmed

**Only for a sub-task that carries a sub-issue.** Under this contract's topology a task pull
request merges into its parent branch, so GitHub's own keyword auto-close never fires for it —
the resolved link and the closing action are two different things. This step is what performs
the closing action `/ship` cannot: `/ship`'s own hard rule is *never* `gh issue close` by hand,
because for a pull request based on the default branch the resolved link is the honest closing
moment. That rule does not cover a task pull request based on a parent branch, and this step is
the scoped exception, gated on a GitHub-confirmed merge, never on a local belief.

**Read before you close (I-10). Never close on a local belief that a pull request merged.**

1. `gh pr view` must already have reported this pull request MERGED — Step 1's own verification,
   never re-derived here.
2. `gh issue view <sub> --json state` — read the sub-issue's own state first, and only then decide:
   - Already `CLOSED` → record `sub_issue_closed: already-closed` and do nothing further. This is
     what makes a re-run idempotent, and it is also what happens harmlessly if two runs race, or
     if GitHub ever does close the issue itself once the parent branch reaches the default branch.
   - `OPEN` → `gh issue close <sub> --reason completed --comment "<pull request url>"`, then
     re-read the state and record `closed` or `close-failed`.

**Never close a sub-issue without first reading its own state.** A close call issued on the
strength of "the pull request merged" alone, without the read in step 2, is exactly the anti-
pattern this step exists to prevent.

## Step 3: Write the completion record

For each merged pull request that mapped to a sub-task, write
`.claude/orchestrator/results/<contract-id>/<task-id>.yaml` in the shape above, with the merge
commit GitHub reported and `verified: github`. **The record's shape gains `sub_issue_closed`**,
carrying Step 2.5's outcome (`already-closed` | `closed` | `close-failed` | `unverifiable`). The
key is **omitted entirely** when no closure was attempted — a sub-task with no sub-issue, or a
merge that never reached Step 2.5 — exactly as `review_verdict` is omitted when nothing was read.

**A completion record is append-only in spirit.** A `completed` record replaces a `failed` one
only through the sweep's `update` state (a re-delivery). A differing `completed` record is never
overwritten: show both and ask, because the owner decides (`--discard-differing`). Two different
commits claiming to finish the same sub-task means either the work shipped twice or the mapping is
wrong, and both need a person. A re-run for a pull request the evidence already holds as `completed`
writes nothing and lists the sub-task under `already_recorded`.

Then update the state store to mark that sub-task completed, so the live position agrees with
the evidence. The script does this in the same run: a confirmed merge writes `status:
completed` plus `branch` (the head ref), `pull_request` (the link) and `base` (the base ref)
into the sub-task's state entry, and writes nothing for a pull request that maps to no sub-task.

**Commit what you just wrote.** Completion records and the brief's final status are written after the merge, so no earlier commit contains them. The state store is git-ignored and never staged. Stage exactly those files and commit them to the one stable records branch of the contract, `docs/<contract-slug>-records`. Do not use a `task/...` name: the loop maps a merged pull request to its sub-task by that exact branch pattern, and a records branch must not be mapped to one.

**One stable branch, added to and never re-cut.** Fetch `origin/docs/<contract-slug>-records` first.
- **It exists on origin:** check it out from that fetched ref, commit on top and push without force. Never re-cut it while it exists, because a re-cut drops the records already on it.
- **It is absent:** cut it from freshly fetched `origin/master`, push it and open a draft pull request.
- **It exists and no pull request has it as its head** (the last one merged or was closed): after the push, open a new draft pull request from the same branch.

When `/flow` is running this phase, pass the list of files to Step 8 of `/flow` instead of committing here, with the one exception below. Name the branch and the files in your report. The push itself asks nothing (Q1, answered 2026-11-02): it carries only docs files, goes to the one stable records branch, never forces, and merging stays with the person. The evidence confirmation before a flipping run (`references/contract-completion.md`, step 3) stays.

**After a successful push, sweep.** Run `--sweep-records --from "$START" --removed <records worktree>` (and `--removed` for any other tree this run removed), then print `tree_lines` verbatim. The sweep deletes a copy only when its twin is on origin, so a failed or declined push deletes nothing. Report what it kept and why: a copy that differs is named with its two blob ids and the `--discard-differing` remedy. Never delete a starting-tree copy by hand.

**The completion hand-off push.** When this run leaves every sub-task with a completion record and the contract has a parent branch (the script's `next_command` for this run is `/advance <slug>`), commit and push the records draft BEFORE handing to `/advance`, even when `/flow` is running. Do not defer it to `/flow` Step 8. The landing reads records only from the remote, so a record that is still on this disk is invisible to it.

## Step 4: Recompute which sub-tasks are released

For every sub-task with no completion record, work out what it depends on.

**Dependencies are read, never derived.** Every sub-task block carries a `Depends on:` line
holding either `none` or the ordinals it waits for. Read it. Do not infer ordering from
anything else.

**Never derive dependencies from overlapping file lists.** That was an earlier rule here and it
was wrong. Overlapping files mean two writers could clobber each other. They say nothing about
one thing needing another to exist first. Backend and frontend touch entirely different files,
and the frontend still needs the endpoint before it can call it, so the rule gets the most
common case in this project exactly backwards.

**A sub-task with no `Depends on:` line is a defect in the contract, not a sub-task with no
dependencies.** Report it and leave the sub-task blocked. Guessing `none` releases work that
may have nothing to build on.

Then, for each dependency, look for a completion record carrying `verified: github`.

- **Every dependency has a verified record** → the sub-task is **released**.
- **Any dependency has no record** → it stays blocked. Name which dependency holds it.
- **A dependency names a sub-task not in the plan** → report it, and leave the sub-task
  blocked.

That last rule carries the weight. Treating an unresolvable dependency as satisfied is how a
gate stops gating while still looking like it works. That is the exact defect found in the
orchestrator's own gate, and this skill must not repeat it.

**Compute releases from completion records only.** Do not read the live state to decide a
release. State can be stale; a record is evidence.

## Step 5: Hand the released set back — do not iterate

This phase ends by returning three things: the sub-task it closed, the set that closing
released, and the set still blocked with what each is waiting for.

**What happens next depends on who called.**

**The loop called.** Return the sets and stop, except on the completion move described below. Do
not start a sub-task, do not ask the user anything, and do not decide an order. The loop owns iteration, and it already holds the
authority it was started under. A phase that starts work behind its caller's back produces two
things driving the same queue.

**A person called.** There is no loop to hand back to, so report and offer:

- **One or more released** → name them, and offer `/advance`, which takes the next step.
  Do not start a sub-task from here; `/advance` owns dispatch.

**When every sub-task has a completion record,** hand off using the script's own `next_command`
— printed verbatim, never re-derived here (Step 7 below). The command depends on whether the
contract was built on a parent branch, whoever called:

- **No parent branch:** `/verify-before-done`; `/ship` follows verification.
- **A parent branch:** `/advance <slug>`. This phase hands straight to `/advance`, which starts the
  background landing and asks nothing. This is the one case where this phase starts something, and
  it starts it by invoking `/advance`, never by launching the landing itself. Step 3's completion
  hand-off push comes first, so the landing finds every record on the remote.

Do not declare the contract finished from here. Completion of the last sub-task is a fact this
phase can report. Whether the contract is done is a verdict that belongs to the landing (parent
branch) or to verification (none).

For a contract with two or more mergeable sub-tasks, the end of the contract is also its
**parent** pull request, not any sub-task's own. The landing script enforces the rule that the
parent must not be merged while any child issue is still open (the topology contract's I-12): it
reads the children from the parent issue twice and halts `children-still-open`. Nothing in this
phase checks it, and the operator no longer has to.

## When a sub-task cannot be delivered

When a sub-task cannot be delivered (its pull request was closed unmerged, or its implementer halted) applies, read `references/undeliverable-sub-task.md` in full before continuing. If it cannot be read, stop and report the missing file; do not continue from memory.

## Step 6: Clean up, automatically, on every call

A delivered work item leaves worktrees and merged branches behind. **This step runs on every
call, after Steps 3 to 5 and after any records pull request, and it asks nothing.** The script
`cleanup_delivered.py` (Delivery cleanup) does the whole job and decides for itself whether
anything may go: it reads the contract and the records at `origin/<default>`, and until the
records pull request has merged it answers "not delivered yet" and removes nothing. The first
call after that merge removes everything it safely can, and a later call removes whatever a
standing session had held back.

Resolve the script as `CLN` (absolute, before the `cd`), then run it from the main root. The
lookup order is the plugin root, then the installed-plugin records and the newest cache folder,
then the current worktree's own copy. It never tries the main checkout's copy.

```bash
START="$PWD"
CLN=
S=.claude/scripts/cleanup_delivered.py
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then CLN=$CLAUDE_PLUGIN_ROOT/$S
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
  CLN=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
  if [ -z "$CLN" ] && [ -f "$PWD/.git" ] && [ -f "$PWD/$S" ]; then CLN=$PWD/$S; fi
fi
( cd "$(py -3 "$CLN" --print-main-root)" && py -3 "$CLN" --contract <slug> --from "$START" [--remove-remote] --json )
```

The `cd` runs in a subshell on purpose: the session's own shell stays in the folder it started in, so
the calls after this step still see the start tree, and a failed `cd` cannot be followed by a script
call from the wrong folder. The current folder's own copy is taken only in a linked worktree (its `.git` is a file), never
in the main checkout, whose copy may be stale. **If `CLN` comes back empty, stop this step, do
not run the line above, and say so in the report's Cleanup line** — nothing was removed,
and nothing else in this skill depends on it.

- **Exit 5 is normal.** It means "not delivered yet": nothing was touched, and the script's
  `line` says when it runs again. Exit 3 means some items were kept, each with its reason. Exit
  10 means the delivery could not be verified and nothing was touched. None of these is a failure
  of this skill.
- **`remove-remote` is a parameter of this skill**, for example `/pr-merged 40 remove-remote`.
  It is off by default. When it is given, pass `--remove-remote` to the script as shown, and
  nothing else; without it the script never changes a remote branch and lists the ones still
  present as `remote-kept`.
- The script prints one `line`. **Step 7's `- Cleanup:` entry is that `line`, verbatim.** When
  the line ends with `finish: <command>`, a session stood in a tree it had to remove: that tree
  was left untouched, and the next call from a shell outside it clears it. Print that one command and nothing more.
- Skip the step only when the run named no contract; there is no work item to clean up then.

## Step 7: Report

**Render every entry in the JSON report's `hand_resolved` list by printing its own `reading`
field verbatim — never collapse it, and never derive a reading yourself from `merge_commits`
and `files`.** `pr_merged.py`'s `_render_hand_resolved_reading` computes the reading once and
stamps it onto every entry — a seeded stored-record entry, a not-recorded placeholder, and an
entry measured this run alike — before either of its own output branches reads it. Re-deriving
the same reading here would be a second implementation of the same rule, which is exactly the
drift Alternatives Considered rejects; it also risks disagreeing with the script's own wording,
which is the overclaim the Hand-Resolved Summary exists to prevent.

For reference only, never as a decision rule to re-derive, `reading` is always one of five
shapes:

- `not-recorded` — a completion record written before the unread-commit count existed, a
  stored `hand_resolved` value with no `commits_unread` key at all (the record predates it and
  cannot tell "nothing was unread" apart from "nobody counted"), or a stored value the script
  could not read at all (hand-edited or partially-migrated)
- `not detectable (...)` — nothing was genuinely inspectable: zero, missing or otherwise
  malformed `merge_commits`; a `files` value the script could not read as a list of strings; a
  malformed unread-commit count; or one or more commits the script could not read even after its
  one fetch attempt — named as `not detectable (unread commits: N)`
- `clean` — at least one merge commit was inspected, none was conflicted, and every reported
  commit was read (a present, well-formed `commits_unread` of exactly zero)
- the comma-separated file list — files differing from both parents of an inspected merge
  commit, resolved by hand or changed during the merge; gains an ` (unread commits: N)` suffix
  when some other reported commit could not be read

Print each entry as `<sub-task>[ #<pr>]: <reading>` (`h.get("reading")`), naming the pull
request only when the entry carries one — a seeded or not-recorded entry does not.

**The closing line is the script's own `next_command`, printed verbatim — never composed
prose.** `report["next_command"]["commands"]`, joined by `", then "`, or, when that list is
empty, `"none — " + report["next_command"]["reason"]`.

```
### PR-MERGED REPORT
- Verified merged: <number -> sub-task, one line each>
- Skipped: <number — verdict, one line each>
- Unmapped: <numbers that matched no sub-task>
- Contract defects: <block id — reason (files-but-no-recognised-agent | no-files-but-names-an-agent), one line each | none>
- Hand-resolved: <sub-task[ #pr] — <entry's own `reading` field, printed verbatim>, one line each | none>
- Completion records written: <paths>
- Records left in starting tree: <the report's records_untracked paths, each with its state (unpushed | update | differs | unsafe) and reason, or "none"; "unverifiable — <records_reading_cause>" when records_reading is unverifiable>
- Trees: <the sweep's tree_lines, printed verbatim, one per tree touched: the starting tree and the records worktree>
- Review verdicts: <sub-task — pass | pass-with-findings | blocked | unreadable | unfetched | cross-repository, one line each | none read this run>
- Released: <sub-tasks now unblocked, and what released them>
- Still blocked: <sub-task — waiting on X>
- Failed: <sub-task — severity, one-line reason, and what it now blocks | none>
- Contract complete: <yes — the script's `next_command`, printed verbatim: `/verify-before-done` (no parent branch) or `/advance <slug>` (a parent branch: the landing script starts there and merges the parent pull request itself, after its children-closed gate) | no, N sub-tasks remain | blocked on architect re-entry>
- Cleanup: <the cleanup script's own `line`, printed verbatim — never composed prose | no contract named | script not found>
- Next command: <report["next_command"], rendered exactly as the rule above says>
```

**The three loop-owned review readings.** `unreadable` means the merge commit is in the local
clone but the declared artefact is absent, malformed or outside the closed set. `unfetched` means
the merge commit itself is not in the local clone, even after this run's one fetch of the pull
request's base branch. It is not a bad artefact; it is a commit the clone does not hold. To clear
it, fetch the commit or restore the network, then run `/pr-merged <pr>` again. The new run
overwrites the record. If the pull request's base branch has since been deleted, the loop's fetch
can never bring the commit down, and the reading will not clear on its own. The operator must bring
the commit into the local clone by hand before rerunning. No command for that case is verified
here, so none is suggested.

`cross-repository` means the merge commit lives in a **different** repository from this
checkout's own — the sub-task's pull request was a `Cross-Repository Pull Request`, resolved by
its `https://` link. Its own remedy is **not** a fetch: no fetch this clone can ever run reaches
another repository's merge commit, so telling the operator to fetch would send them at a remedy
that can never work. Instead, open the declared artefact in the pull request's **own**
repository, at its own merge commit, and read its `**Verdict:**` line there by hand. The
dependent stays withheld until that reading is brought over some other way; no command that
does this automatically is verified by this contract, so none is suggested here — see the
follow-up stub this contract cites for an automated read.

State what was skipped as plainly as what succeeded.

## Refusal: `GH_REPO` is set in the environment

When `GH_REPO` is set in the environment applies, read `references/gh-repo-refusal.md` in full before continuing. If it cannot be read, stop and report the missing file; do not continue from memory.

## The stores, and the design that defined them

This phase writes to `.claude/orchestrator/results/` and `state/`, and reads a plan. Those
paths come from an earlier subsystem that specified three stores and never filled any of them.

**That subsystem's scripts were removed on 2026-09-14.** Its planner never parsed a contract
and no session was ever launched, so the completion store was created, read in two places, and
never written to once. Both readers invented success when they found nothing.

The store names are kept because the design behind them was right: a plan of sub-tasks, one
durable record per finished sub-task, and a working position rebuilt from those records. This
phase is the producer that store never had.

**Do not model this phase's dependency check on the removed one.** That gate failed open: the
executor named a branch with a date appended, the lookup omitted the date, and on the miss it
released the child anyway. This phase computes releases from completion records, which carry
no naming convention to get wrong.

### Where the sub-tasks come from

Contracts written from the standard template carry an `## Implementation Handoff` section, with
one block per agent — implementer and review gate alike — and a `**Files to touch:**` list inside
each. **That list is what makes a block a sub-task, not who is assigned to it.** A review gate
declares its artefact and is waited on for a merge exactly as an implementer is. A block naming
an agent with no file list is a contract defect that halts the plan. That is the plan this phase
walks, and it needs no planner to produce it.

The removed planner looked for a `## Task Decomposition` heading instead, which no contract
ever wrote. That mismatch is the whole reason its plan store stayed empty.

## Anti-patterns (halt immediately)

- **Writing a completion record on the user's word alone.** Ask GitHub. Everything rests on
  this.
- **Writing `tests_passed: true` because a merge happened.** A merge is not a test run.
  Record what was observed, and `unknown` when nothing was.
- **Treating a closed pull request as delivered.** Closed without merging is the opposite.
- **Treating a closed pull request as a skip.** It is a failed sub-task and it escalates.
- **Treating a layout warning as a blocker, or as a failure to record.** `--status --json` carries
  `layout_warnings` in three forms plus two key states: absent for a contract that is not judged, `[]`
  when judged and nothing is to be reported (it clears once no sub-task remains), and entries
  `single-branch-delivery` (work already on the default branch, while sub-tasks remain), `held` (a Records
  pull request is open: merge it first) and `unverifiable` (an input could not be read: give its re-read
  remedy, for example `git fetch origin <default>`). A warning blocks nothing, and a record is written as
  GitHub reports it. Show the warning's remedy to the owner, and keep recording.
- **Releasing dependents of a failed sub-task.** They would build on work that does not exist.
- **Deleting a failure record when the architect supersedes it.** A second failure on the same
  sub-task should be visible as a pattern.
- **Treating an unresolvable dependency as satisfied.** That is the orchestrator's own defect.
- **Computing a release from the live state instead of completion records.** State goes stale.
- **Overwriting an existing completion record silently.** Two commits for one sub-task needs a
  person. A differing `completed` record is never overwritten; only the sweep's `update` (a
  `completed` record over a `failed` one) is pushed over an existing record.
- **Inventing a sub-task graph** when the contract has no decomposition. Report it instead.
- **Deriving a dependency from overlapping file lists.** Overlap means two writers could
  clash. It does not mean one needs the other first.
- **Reading a missing `Depends on:` line as `none`.** It is a contract defect. Report it.
- **Guessing which sub-task a pull request belongs to.** Report the unmapped number.
- **Starting several released sub-tasks without asking,** on the person-called path. Each is
  a full run.
- **Starting anything at all when the loop called you.** Return the sets and stop. Two
  things driving one queue will disagree the moment either changes. The one exception is the
  completion move of a contract with a parent branch, which hands to `/advance`.
- **Declaring the contract finished** because the last sub-task closed. That verdict belongs
  to the landing (parent branch) or to `/verify-before-done` (none).
- **Handing to `/advance` on the completion move before the records draft is pushed.** The landing
  reads records from the remote only, so an unpushed record reads as `not-complete`.
- **Re-cutting `docs/<contract-slug>-records` while it exists on origin.** Fetch it, commit on top
  and push without force. Cut it from `origin/master` only when it is absent. A `-2` or `-3` suffix
  names the records worktree folder only, never the branch.
- **Asking before a records push to the stable branch, or pushing anywhere else without asking.** Every
  records push to `docs/<contract-slug>-records` runs without a prompt (Q1). Only the evidence
  confirmation before a flipping run stays, and a push to any other branch still confirms.
- **Deleting a starting-tree record copy by hand, or sweeping before the push succeeded.** The sweep
  deletes only a copy whose twin is on origin; a copy that differs is kept for the owner.
- **Launching the landing from this phase.** `/advance` starts it, in the background.
- **Hand-running `git branch -d` or `git branch -D`,** or removing a worktree with a manual line.
  The cleanup script checks that the tip is in `origin/<default>` before it deletes anything.
- **Running a global tidy of worktree metadata** (git's `prune` for worktrees). It would also
  remove other work items' stale entries. The script never does it, and neither does this skill.
- **Composing the cleanup line as prose.** Step 7 prints the script's `line` verbatim.
- **Deleting a remote branch without `remove-remote`.** A remote deletion is outward-facing; it
  happens only when the caller passed the parameter.
- **Closing a sub-issue on a local belief that a pull request merged.** Step 1's GitHub
  verification must already have confirmed the merge before Step 2.5 runs.
- **Closing a sub-issue without first reading the issue's own state.** I-10's read-before-close
  ordering is what makes a re-run idempotent; skipping it risks a redundant mutation and a
  comment posted twice.
- **Rendering a zero `merge_commits` count as "none detected" or "clean".** It means nothing
  was inspectable, not that nothing was found — the exact overclaim the Hand-Resolved Summary's
  four-field shape exists to prevent.
- **Collapsing the five hand-resolved readings into a bare file list.** An empty list from a
  genuinely clean merge and an empty list from an uninspectable one are different claims; render
  both distinctly.
- **Rendering `clean` for any pull request that reported an unread commit.** A genuinely clean
  merge inspected beside a commit the script could never read is still not detectable as a whole
  — the unread count withholds `clean` whatever the file list says.
- **Sending the operator to fetch for a `cross-repository` review verdict.** No fetch this clone
  runs can ever reach another repository's merge commit; that remedy belongs to `unfetched` alone.
- **Setting `GH_REPO` to read a pull request in another repository.** Pass its link instead —
  `GH_REPO` retargets every `gh` call the script makes, including the sub-issue close, and the
  script refuses outright (exit 8) rather than risk it.
- **Composing the closing "next command" line as prose.** Print `report["next_command"]`
  verbatim — a second implementation of a rule the script owns is how the two drift.

## When NOT to use this skill

- A pull request you are about to open. That is `/ship`.
- A whole work item with no sub-tasks, which you want to resume. Invoke `/flow` with the brief.
- Checking what is in flight with nothing merged. That is `/list-contracts`.

## Skill integrations

- **Reads** the plan store, and **writes** the completion and state stores.
- **Is a phase of** the orchestrator's loop, which owns iteration over a contract's
  sub-tasks. This skill closes one sub-task and returns; it never iterates.
- **Sits inside** `/flow`, which owns the outer chain for one whole work item.
- **Offers released sub-tasks to** `/tdd-first` on the person-called path only, with the
  contract as the authority.
- **Hands a finished contract on** with the script's printed `next_command`: `/verify-before-done`
  when it has no parent branch (`/ship` follows verification), and `/advance` when it has one.
  `/advance` starts the background landing, and `.claude/scripts/land_contract.py` merges the parent
  pull request. The topology contract's I-12 children-still-open gate is enforced there (phases P4
  and P12). Contract: `.claude/concepts/2026-10-05-contract-completion-lands-on-master.md`.
- **Complements** `/ship`, which opens pull requests. This skill handles what happens after
  one merges.
- **Implemented by** `.claude/scripts/pr_merged.py`, which the loop calls directly.
- **Does not depend on** the removed orchestrator scripts; its design record is at
  `.claude/orchestrator/`.
