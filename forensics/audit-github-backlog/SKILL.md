---
description: Sweep the whole open GitHub backlog — every open issue and PR — judging each against today's code, and produce a reviewable close/refile/keep plan that also assigns a P0–P3 priority to everything it keeps. Fans out one analyst per bucket over locally-dumped threads, holds the cross-cutting sweeps centrally, and asserts coverage before reporting. Closes and comments on nothing. Use when the user says "audit the backlog", "triage the backlog", "sweep the issues", "prioritise the backlog", "/audit-github-backlog", or asks what in the backlog is still worth keeping.
---

# `/audit-github-backlog` — the whole-backlog sweep

Judge **every** open issue and PR against the code as it is today, and leave a
reviewable plan saying what to close, refile, or keep — with the evidence, and
with a priority on everything that survives.

This is a read-and-decide pass. It closes, comments on, relabels, and edits
**nothing** on GitHub.

**Writing the plan is part of this skill, not a handoff to a later one.** Step 5
runs `@.claude/skills/plan/SKILL.md` and the plan file is this skill's output —
there is one document, in the normal plan lifecycle, not an audit report some
later session turns into a plan. Only _execution_ is separate, through `/go`,
and that gate is the point: the output is a bulk close list, and the only thing
worse than an unreviewed backlog is an unreviewed automated purge of one.

## This is a living document

Everything here was distilled from a **single** run over a 213-issue backlog. It
is right about what that run hit and unproven about everything else, so treat it
as the current best account rather than a settled procedure.

**While running it, collect what it gets wrong** — a trap it does not warn
about, a step that misfires, a bucket heuristic that produces nonsense, guidance
that cost more than it saved — and put them to the operator at the end, as
concrete proposed amendments to this file. Analysts are asked for the same at
the end of their reports. Do not silently work around a defect in these
instructions: the working-around is exactly the knowledge the next run needs.

## End state

- `docs/plans/backlog-audit.draft.do-not-implement.md` — the plan, in the
  lifecycle `@.claude/skills/plan/SKILL.md` defines.
- `docs/plans/backlog-audit/` — one analyst report per bucket, plus the merged
  verdict table.
- Nothing on GitHub has changed.

The subdirectory is load-bearing: `/go` Step 1 does `ls docs/plans/*.md` and
expects exactly one match, so the evidence must stay nested rather than
flattened beside the plan. Before you start, check `docs/plans/` is otherwise
empty — a leftover plan file from an earlier session makes that glob ambiguous.
`/finalize` sweeps `docs/plans/` at squash, so none of it reaches the trunk; the
durable record is the reasons left on the closed issues themselves.

---

## Step 1 — Collect

Dump the whole backlog to `tmp/audit/` (gitignored) **before** judging anything,
so no analyst re-fetches it and no rerun re-derives it:

- `issues/<n>.md` — full thread per open issue: body, labels, dates, all
  comments
- `prs/<n>.md` — the same per open PR, plus its base and head refs
- `pr-history.json` — every PR ever, **with `base.ref`**
- `rot.json` / `rot.md` — per-PR rot: commits behind/ahead, files touched,
  overlap with the base, whether the head ref is gone, and a local merge verdict
- `buckets.md` — the proposed split into coherent themes, one analyst each

`gh api --paginate` is the collection primitive;
`@.claude/skills/override-gh/SKILL.md` is the reminder that `gh` and `GH_TOKEN`
are available here. Read § "Verified CLI traps" **before** writing any of it —
most of those entries are there because the obvious approach fails _silently_,
and a rot number derived from a broken `git merge-base` is plausible fiction
rather than an error.

**Mechanize this step once the backlog outgrows hand collection.** At a few
dozen items, `gh` calls driven from the skill are fine. At a couple of hundred
they are not: the collection is re-run on every abandoned attempt, the rot
matrix is per-PR git work, and Step 4's coverage check is the difference between
a complete sweep and one that quietly dropped two items. Write it as two scripts
under `scripts/` — collect and aggregate — and make both **hard-fail rather than
guess**, since every trap below is a case where guessing looks like an answer.

**Read `buckets.md` and override the split freely.** The proposal is a
convenience; what matters is the coverage assertion behind it. Merge two small
buckets, split a 47-item one, move an item that landed under the wrong theme.
Coherent buckets are the whole point — one analyst seeing a cluster whole spots
the duplicates and the shared root cause that ten analysts each holding one item
cannot. Keep every item in exactly one bucket; that invariant is what Step 4
re-checks.

## Step 2 — Fan out one analyst per bucket

**First, write this run's repo context to `tmp/audit/analyst-context.md`** —
what shipped, what was retired and what replaced it, what the live architecture
is — composed from `CLAUDE.md` and whatever decision docs the project keeps.
Every analyst reads it, and it is the baseline the whole question "is this still
relevant?" rests on: without it a retired-subsystem bucket is unjudgeable. Don't
skimp it. It is written per run rather than kept in this skill because a copy
here would drift from the repo it describes, and an analyst judging against
stale context is the failure this pass exists to prevent.

Then one `general-purpose` agent per bucket, in a single message so they run
concurrently. **The rules are a file, not prompt text** — `analyst-rules.md`
beside this one — so each prompt stays short and every analyst provably reads
the same standard rather than N hand-copies of it:

```
You are a backlog analyst on a whole-backlog audit sweep.

Read .claude/skills/audit-github-backlog/analyst-rules.md in full and follow it
exactly, including tmp/audit/analyst-context.md, which it tells you to read first.

Your bucket: <BUCKET KEY> — <BUCKET REMIT from buckets.md>
Your items: <ITEM NUMBERS>
Write your report to: docs/plans/backlog-audit/<NN>-<bucket-key>.md
```

Analysts need `general-purpose` because they write their own report file. They
do not need — and must not use — any GitHub write access; the rules file says
so, and that is what makes running ten agents over a live backlog safe.

**Never read an analyst's transcript output file.** It will overflow your
context. Use the completion notification, then read the report file it wrote.

**Scale effort to age.** For items touched in the last fortnight the useful
output is "confirm still live, and find the exceptions" — not a deep dive each.
Say so in the bucket remits.

## Step 3 — Hold the cross-cutting sweeps yourself

These span every bucket, so no analyst can do them. Run them while the analysts
work.

1. **Open issues already closed by a merged PR.** Scan `pr-history.json` for
   merged PRs referencing an open issue number. **Filter on `base.ref`** — a PR
   merged to an `epic/*` branch has not landed on the trunk, and reading it as
   landed is how two issues got reported as done when they weren't. A merged PR
   referencing an issue is not proof the issue is finished either: watch for
   "schema only", "slice 1", "split from".
2. **Why superseded PRs were closed.** The closing comment on a closed PR often
   explains a whole cluster of open issues at once — one "Superseded by #1518"
   explained ten. Read the comments, not just the state.
3. **Label and process traps** — see § "Recurring failure modes", which is a
   re-check list, not a one-off.

**Feed findings back down.** When a sweep turns up evidence a running analyst
needs, `SendMessage` it to that agent rather than letting them rediscover the
fact or miss it.

## Step 4 — Aggregate, and assert coverage

Merge every report's final `## Summary` table into one verdict table, and
**refuse to proceed** on inexact coverage — an item judged by nobody, judged
twice, or carrying a verdict outside the taxonomy. Name the file to fix in each
case, fix the reports, and re-merge until it passes. Do not hand-reconcile
around it: this check is why the mechanical half is worth scripting at all,
since a hand-merged run silently dropped 2 of 213 items and the output looked
complete.

When an operator decision changes verdicts wholesale — as "never close a parent
with an open sub-issue" does — write it into
`docs/plans/backlog-audit/00-overrides.md` and re-merge. Overrides are applied
last and win. Recording the decision once and regenerating beats hand-editing it
into every report it touches. An override row takes the analyst's
`| Item | Verdict | Priority | Reason |` shape (`analyst-rules.md` §
"Reporting"); one that drops the priority column silently unprioritizes what it
touches.

## Step 5 — Write the plan (this skill's output)

Follow `@.claude/skills/plan/SKILL.md` — the plan cycle happens **here**, in
this run, rather than being left for a later session. Write
`docs/plans/backlog-audit.draft.do-not-implement.md`, carrying the counts, the
themes and process findings worth a decision, the guard list of items **not** to
close and why, and a pointer to the merged verdict table for the per-item
detail. Do not restate the taxonomy or the guards — they live here.

The plan's execution section is a close list _and_ a relabel list, so it must
say **how** each item closes and **what** each survivor becomes: carry the
`state_reason` from each verdict (see the taxonomy below), the `duplicate_of`
target for every `CLOSE_DUPLICATE`, and for every `KEEP` and `REFILE` the
priority label to apply and the stale priority label to remove. Carry a
priority-by-bucket table alongside the verdict counts, and name the `P0`s and
`P1`s in the plan body — at a backlog's worth of surviving items those two tiers
are the part an operator will actually read, and burying them in the appendix
wastes the sweep's most useful output.

Require one thing of the PR that eventually executes the plan: **its body lists
every issue and PR the sweep touches**, as a bullet list of `#<n> — <title>`
grouped by verdict — the `KEEP` and `REFILE` groups subgrouped by priority —
wrapped in a `<details>` block. Each `#<n>` becomes a GitHub-native mention, so
an item carries a link back to the sweep that judged it, and the operator can
read what is about to close without opening the plan. Numbers and titles only —
no per-item descriptions; at ~200 items that list is already most of the body,
which is why it is folded.

Delegate rather than reimplement: `@.claude/skills/propose-issue/SKILL.md` for
every new or refiled issue, `@.claude/skills/go/SKILL.md` for execution.

End the run by putting your proposed amendments to this skill to the operator —
yours and the ones analysts flagged. See § "This is a living document".

---

## The verdict taxonomy

Every verdict carries a one-line reason naming the commit, PR, or verified
absence behind it.

- `CLOSE_DONE` — the work described is done. Closes as `completed`; no priority.
- `CLOSE_NOT_PLANNED` — obsolete or abandoned — real once, nobody will do it
  now. Closes as `not_planned`; no priority.
- `CLOSE_DUPLICATE` — another issue covers it; the reason names it as `#<n>`.
  Closes as `duplicate`; no priority.
- `REFILE` — close **and** open a fresh re-framed issue. Closes as `duplicate`;
  priority required.
- `KEEP` — still reads true against today's code. Not closed; priority required.
- `UNSURE` — needs a human. Say precisely what you could not establish. Not
  closed; no priority.

**A close carries its modality.** GitHub's close reason is an enum —
`completed`, `not_planned`, `duplicate` — and `mcp__github__issue_write` takes
it as `state_reason` (plus `duplicate_of` for the canonical issue number).
Closing everything as a bare "closed" throws away the distinction between _this
shipped_ and _we decided against this_, which is most of what a reader of a
closed issue wants to know. That is why the taxonomy splits the close verdicts
rather than leaving the modality to the reason prose: the verdict is the only
field parsed mechanically, so anything outside it is a suggestion the executing
agent can drop — and in the first run, did.

**The enum is issues-only, so a PR's modality lives in prose.** A pull request
accepts no close reason — it reads back `state_reason: null` however it was
closed, including the ones closed deliberately with written rationales. For the
PRs in a sweep, the verdict's mapped reason is what the **closing comment** has
to say, and there is no `duplicate_of` link to be had — name the issue inline
instead. Don't let a plan instruct `state_reason` on a PR; it silently does
nothing.

`REFILE` is the one with an ordering constraint: **open the replacement first,
then close the original as `duplicate` and name the replacement in the closing
comment.** A refile is a `duplicate` rather than a `not_planned` because the
work was not dropped — it moved, and a reader arriving at the old issue has to
be carried to the live one instead of reaching a dead end. Pass `duplicate_of`
too — it costs nothing and it is what sets `state_reason` — but the bolded
`#<n>` in the comment is the link a reader is actually guaranteed (see §
"Verified CLI traps"). Analysts are not told any of this: they judge that an
item needs re-framing, and the mechanism is execution's business.

Two rules do the heavy lifting, and both are rules rather than preferences:

- **Age is never a reason to close.** An issue that still reads true against
  today's code is `KEEP` however old. In the single run this method comes from
  that kept 119 of 213 issues alive — and several had got _worse_ while sitting,
  with duplicate counts growing 3→4, 13→15, 18→31, and one predicted drift
  actually happening.
- **`REFILE` is a framing mismatch, not a wish.** "Still a good idea, nobody did
  it" is `KEEP`. `REFILE` is for an item whose named paths, symbols, or
  architecture are gone.

## Every surviving item carries a priority

A sweep that only decides what survives hands back a backlog of the same size in
the same undifferentiated order — the thing that made it unreadable in the first
place. So `KEEP` and `REFILE` also carry a **`P0`–`P3`** tier: for a `REFILE`,
the tier its replacement is filed at. Closing verdicts and `UNSURE` carry none.

The tier definitions and the calibration rules that make independent analysts
comparable — priority is the consequence of _not_ doing it, `P0` is rare, a
uniform bucket is a failed judgement — live in `analyst-rules.md` § "Priority",
the file the analysts author against. Don't restate them here or in the plan.

The tier is required-or-forbidden per verdict rather than optional, and the Step
4 merge rejects a row that breaks either half: an optional column is one every
analyst fills differently, and an unprioritized `KEEP` is exactly the
undifferentiated backlog this exists to break up. Map each tier onto one of the
repo's existing priority labels rather than minting a parallel set beside them,
and record the mapping wherever the merged verdict table is written, so the plan
and its execution read the same one.

Two things follow for the plan and its execution:

- **A kept item is relabelled, not merely left alone.** Execution applies the
  mapped label and removes any priority label the item already carries — a
  backlog's existing priority labels are usually near-synonyms and barely used,
  so an item keeping a stale one alongside a fresh one is worse than either.
- **Priority is the operator's most likely override.** It is a judgement call in
  a way "does this file still exist" is not, so expect tier disagreements at
  review and take them through `00-overrides.md` like any other — the override
  row carries the priority column too.

## The evidence standard

Every verdict cites a path, a line, a grep result, or a commit SHA. **A verdict
without one is discarded.** Verifying means answering, concretely:

- do the named files still exist? do the named symbols?
- does the described duplication, bug, or gap **still** exist?
- was it already fixed — `git log --oneline --all --grep '#<n>'`,
  `git log -S'<symbol>'`?
- is a newer open issue already covering it?

## Recurring failure modes to re-check every run

The sweep is unusually well placed to catch these, and all three recurred:

1. **Label traps.** A label that both marks work as claimed _and_ excludes it
   from future selection is a one-way door: every item the routine ever touched
   leaves the candidate pool permanently, so it accumulates the backlog it
   exists to drain. One such label had done that to 36 issues. Check every
   automation label for whether anything ever removes it — and prefer expressing
   liveness (an open linked PR) over history (the label's presence).
2. **Unmerged output backlogs.** A routine that opens PRs faster than a human
   merges them converts backlog into a second, less visible backlog. 22
   finalized PRs sat ~46 days.
3. **Parent/child bookkeeping.** Auto-filed parents whose children are tracked
   separately, where nobody closes the parent; and merged PRs that never
   auto-closed their issue because they merged to a non-default branch.

## Guards

**Ordering** — violating these loses information that exists nowhere else:

- **File replacements before closing anything that holds them.** An umbrella may
  be the only record of live work: one held three items recorded nowhere else in
  213 issues.
- **Never close a parent with an unresolved sub-issue** — however finished the
  parent's own text looks. Check `/repos/<owner>/<repo>/issues/<n>/sub_issues`,
  not just the body: the sub-issue link is API-only, so a parent reads as
  complete right up until you query it. In the first run this cut one bulk close
  from 19 items to 11.
- **Harvest un-trackable prose before closing auto-filed reports.** Recurring
  readouts accumulate product signal in sections that are neither a tracked
  issue nor a marker.

**Never close:**

- **Unfinished security verification.** A closed-child count can overstate how
  closed a gate is — in one case the top finding had actively _regressed_.
- **Production data repairs that never ran.** Bad data does not age out.

**Mechanical:** renumber `TODO(#n)` comments before closing `#n`; carry
salvageable design out of a PR before closing it; every close carries a one-line
reason, so the sweep is a record rather than a purge.

## Verified CLI traps

Each of these was hit for real. **All but the first fail quietly.**

Each trap, then what to do about it:

- Shallow clone → `git merge-base` exits 1 with empty output, and downstream rot
  numbers are fiction — `git fetch --unshallow`, then assert; never proceed on
  the numbers it would otherwise print.
- `mergeable` / `mergeStateStatus` are `UNKNOWN` until GitHub computes them
  lazily — compute locally with `git merge-tree --write-tree`.
- `gh issue view/list --json stateReason` → `Unknown JSON field` — valid fields
  are `state`, `closed`, `closedAt`; read the reason from
  `gh api /repos/…/issues/<n>`.
- `gh pr view --json closingIssuesReferences` → `Unknown JSON field` — issue↔PR
  links are GraphQL-only: query
  `repository.pullRequests.closingIssuesReferences`.
- `duplicate_of` set `state_reason` but recorded no `MarkedAsDuplicateEvent` —
  neither the REST parameter nor GraphQL's `closeIssue(duplicateIssueId:)`
  rendered a link — name the canonical issue in the closing comment, in bold;
  treat the field as write-only.
- `gh pr list --search 'issue/1647'` does not index branch names —
  `gh api '/repos/<owner>/<repo>/pulls?head=<owner>:<branch>'`, or scan the
  paginated history.
- `gh pr list --limit 500` silently truncates — `gh api --paginate`.
- `gh api --paginate` emits one JSON array **per page**, concatenated — so a
  single `JSON.parse` reads page 1 and drops the rest — `--slurp` (gh ≥ 2.52)
  flattens them; below that, split the concatenated arrays yourself.
- Merged-PR-title → issue-number matching without `base.ref` reads epic-branch
  merges as landed — always filter on `base.ref`.
- Bash `cd` persists between tool calls, so later globs resolve against the
  wrong directory — absolute paths.
- A subagent's transcript output file will overflow the coordinator's context —
  never read it; use the completion notification.

## What a run costs, and how often it happens

Context, not a decision for you to make — you are invoked when the operator
invokes you.

**This is an expensive run.** Roughly 200k tokens per analyst and about the same
for the coordinator, so a ten-bucket sweep costs on the order of ten times a
normal planning session — which is what it is, at bottom. Nothing about it is
"cheap to just rerun". If you are tempted to restart the fan-out because a
couple of reports came back thin, re-run those buckets rather than all of them.

**It is on demand, roughly monthly, and deliberately not a cron.** The worst
cluster the first run found had accumulated in ~46 days, which is what makes
monthly the right order of magnitude. It is not scheduled because the output
needs a human decision, and analysis nobody reads is worse than no analysis —
also why the operator's own review is the gate before anything executes.
