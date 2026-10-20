---
name: iru-knowledge-compact
description: Compact the `knowledge/` base built by `iru-knowledge-process-inbox` — sweep `knowledge/pending` and
  `knowledge/agreements` for (a) duplicate pending tasks, removing the duplicates that have no tracker issue
  assigned while folding any extra context they carried into the surviving task, and (b) agreements/pending tasks
  that are already done, determined from the state of the GitHub issue (or Jira ticket) recorded on them by
  `iru-knowledge-to-issue`/`iru-knowledge-to-jira` — deleting the pending file and checking off the matching
  numbered item in its `agreement-<timestamp>.md` for each one that's completed. Also fixes drift between the two
  directories (a pending file whose agreement item is already checked, an open item whose pending file is gone).
  Invoke as `/iru-knowledge-compact`. Always shows the full set of proposed deletions/edits for confirmation
  before touching anything, and never removes a duplicate that has an issue assigned, or one whose duplicate
  partner also has a different issue — those are reported for a human decision instead. Stops early if
  `knowledge/` doesn't exist yet (run `iru-knowledge-setup` and `iru-knowledge-process-inbox` first). Use
  whenever the knowledge base has accumulated repeated action items across meetings, or its agreements no longer
  reflect work that has actually shipped, instead of hand-auditing every pending file.
model: sonnet
---

# Knowledge Compact

Keep `knowledge/pending` and `knowledge/agreements` honest: one pending file per distinct piece of outstanding
work, and nothing still marked open once its tracked issue says it's done.

Run directly by a person as periodic housekeeping, and automatically by `iru-knowledge-process-inbox` as its
final step, once a batch of new meetings has been filed into the knowledge base.

This skill only ever *reduces* the knowledge base (removes duplicate/finished pending files, checks off finished
agreement items, merges context). It never creates new agreements or pending tasks — that's
`iru-knowledge-process-inbox`'s job — and it never files or closes an issue on the tracker.

Throughout, "task id" means the `<timestamp>-<n>` part of a `knowledge/pending/pending-<timestamp>-<n>.md`
filename, exactly as `iru-knowledge-process-inbox` (Step 9) writes it and `iru-knowledge-complete` consumes it.

## Step 1 — Confirm prerequisites

- **`knowledge/` exists and has content**: check for `knowledge/pending` and `knowledge/agreements`. If
  `knowledge/` doesn't exist at all, tell the user to run `iru-knowledge-setup` and then
  `iru-knowledge-process-inbox` first, and stop. If both directories exist but hold nothing beyond `.gitkeep`,
  report that there's nothing to compact and stop.
- **Tracker access** (needed for Step 4 only — never a hard stop):
  - **GitHub**: check the repository is hosted on GitHub (`git remote get-url origin`, matching `github.com` or a
    GitHub Enterprise Server domain) and that `gh` is available and authenticated (`gh auth status`).
  - **Jira**: search with `ToolSearch` for a connected Jira MCP tool (a query like "jira issue") — only relevant if
    Step 2 actually finds `- Jira ticket:` lines.

  If neither tracker is reachable, don't stop: say so plainly and continue with Steps 3, 5 and 6 (duplicate
  detection and drift repair still work without a tracker), skipping Step 4's completion checks entirely rather
  than guessing whether anything is done.

## Step 2 — Build the inventory

Read every file in `knowledge/pending` and every `knowledge/agreements/agreement-*.md`. For each **pending file**
record:

- its task id and path;
- the agreement item text it carries (verbatim);
- its `- Agreement:` reference (file + item number) and `- Meeting:` reference, if present — falling back, when
  they're missing, to deriving them from the task id itself the way `iru-knowledge-complete`'s Step 2 does
  (split off the trailing `-<n>`; the remainder is the meeting `<timestamp>`);
- any tracker line: `- GitHub issue: <url>` or `- Jira ticket: <key> (<url>)`;
- anything else the file holds that isn't in that standard shape — hand-added notes, links, extra detail. This is
  the "additional context" Step 3 has to preserve when it merges duplicates.

For each **agreement file** record every numbered item: its number, its text, whether its checkbox is `[ ]` or
`[x]`, and any trailing tracked-in note (e.g. `_(tracked in <url>)_`) that `iru-knowledge-to-issue`/
`iru-knowledge-to-jira` appended.

Then cross-reference the two: which agreement items have a live pending file, which pending files point at an
agreement item, and which point at nothing that exists.

## Step 3 — Find duplicate pending tasks

Group pending tasks that describe **the same piece of work**, not just the same words. Two tasks from different
meetings restating the same action item are duplicates; two tasks that touch the same component but ask for
different outcomes are not. Compare the task text plus whatever context Step 2 gathered, and when a match is
genuinely borderline, leave it out of the duplicate set and mention it in Step 7's report instead — a false merge
silently loses a real task, a missed merge costs nothing but a re-run.

For each duplicate group, pick the **survivor** and classify the group:

- **Exactly one member has a tracker issue** → that one survives; every other member of the group is removed. This
  is the case the skill exists for: the work is already tracked once, and the untracked restatements are noise.
- **No member has a tracker issue** → the **earliest** task id survives (the meeting where the item was first
  agreed; later ones are re-affirmations of it). The rest are removed.
- **More than one member has a tracker issue** → remove **nothing** from this group. Report it in Step 7 as
  needing a human decision, naming each task id and its issue, since collapsing it would orphan a tracked issue.

For every group where something is removed, work out what the removed members add that the survivor doesn't
already say — a deadline, a named owner, a narrowed scope, an extra meeting that re-raised it, a link. That
becomes the merge text Step 6 appends to the survivor.

## Step 4 — Determine what's already completed

Skip whatever this step can't reach, per Step 1's tracker findings.

For every pending task and every still-open (`[ ]`) agreement item that carries a tracker reference — from the
pending file's `- GitHub issue:`/`- Jira ticket:` line or the agreement item's trailing tracked-in note — look up
the issue's current state:

- **GitHub**: `gh issue view <number-or-url> --json number,title,state,stateReason,closedAt` (add `--repo <owner>/<repo>`
  when the URL points at a repository other than this one).
- **Jira**: the connected MCP tool's issue-read call, reading the ticket's status and resolution.

Classify each:

- **Closed as completed** (GitHub `state: CLOSED` with `stateReason: COMPLETED`; Jira in a Done/Resolved status
  with a resolution that means the work landed) → **completed**.
- **Closed as not planned / won't do / duplicate** (GitHub `stateReason: NOT_PLANNED`; Jira resolved as Won't
  Do/Duplicate) → **not completed**. The work was dropped, not done — never check its box off as if it shipped.
  List these in Step 5's plan as a separate group and let the user decide (drop the task, or leave it open).
- **Still open** → leave entirely alone.
- **Issue not found, deleted, or inaccessible** (bad URL, wrong repo, no permission) → leave alone and report it;
  a lookup failure is not evidence of completion.

Items with no tracker reference at all are simply out of scope for this step — this skill has no way to judge
whether they're done, and won't guess.

## Step 5 — Add drift repairs, then confirm the whole plan

Two inconsistencies between the two directories are worth folding into the same pass, both found in Step 2's
cross-reference:

- **Pending file whose agreement item is already `[x]`** → the completion was recorded but the pending file
  outlived it; delete the pending file.
- **Open (`[ ]`) agreement item with no pending file and no tracker reference** → don't recreate anything and
  don't check it off; just list it in Step 7's report so the user knows it's untracked.

Now present the complete plan to the user via `AskUserQuestion` before anything is written or deleted — grouped as
**duplicates to remove** (with the survivor for each), **completed items to close out**, **closed-as-not-planned
items** and **drift repairs**, each entry naming the task id, its agreement item, and the one-line reason. Offer:

- **Apply everything** (recommended when the plan reads correctly).
- **Apply only some of it** — take the user's selection and apply just those entries.
- **Cancel** — change nothing, and go straight to Step 7's report.

Never skip this confirmation: every action below deletes a file or edits a tracked agreement, and the duplicate
judgement in Step 3 is the skill's own reading of the text, not something the files state outright.

## Step 6 — Apply the approved plan

In this order, so a partially applied run always leaves consistent files behind:

1. **Merge context into survivors.** For each duplicate group, append Step 3's merge text to the surviving pending
   file — as extra lines below its existing `Agreement:`/`Meeting:`/tracker lines, keeping the original task text
   verbatim — and note the task ids it absorbed, e.g. `- Supersedes: <task-id>, <task-id>`. Do this *before*
   deleting anything, so an interruption can't lose the context.
2. **Remove duplicate pending files.** Delete each removed member's pending file, then annotate its agreement item
   so the agreement file doesn't end up with an open item nothing tracks: leave the checkbox `[ ]` and append a
   short note — `_(superseded by task <survivor-id>)_`. Don't check it off: a duplicate is still outstanding work,
   just tracked elsewhere.
3. **Close out completed items.** For each item Step 4 found completed:
   - **A pending file exists** → run `Skill({skill: "iru-knowledge-complete", args: "<task-id>"})`, which deletes
     the pending file and checks off the matching agreement item. If it stops on an inconsistency (missing
     agreement file, item not found, item already checked), don't work around it by hand — record its message and
     carry it into Step 7's report.
   - **No pending file, only an open agreement item** → change that item's `[ ]` to `[x]` directly, leaving its
     text, its tracked-in note, and every other item untouched.
4. **Apply the approved drift repairs** from Step 5.
5. **Handle approved closed-as-not-planned items** exactly as the user decided in Step 5 — if they chose to drop
   one, delete its pending file and annotate its agreement item `_(not planned — <issue url>)_` with the checkbox
   left `[ ]`, since the work was abandoned rather than delivered.

Never edit `knowledge/meetings` or `knowledge/people` — a meeting record is history and stays as written, however
its agreements end up resolved. Never close, reopen, or comment on a tracker issue: this skill reads issue state,
it doesn't drive it.

## Step 7 — Report

Summarize, grouped:

- **Duplicates**: each group collapsed — the survivor's task id, the ids removed, why that survivor was chosen,
  and what context was merged into it. Then the groups deliberately left alone (more than one tracked issue), and
  any borderline pairs Step 3 declined to merge, so the user can judge those themselves.
- **Completed**: each task id/agreement item closed out, with the issue that proved it, and whether the pending
  file was removed, the checkbox checked, or both.
- **Closed as not planned**: each one and what was done with it.
- **Drift repairs** applied, and untracked open agreement items found.
- **Skipped**: anything the tracker couldn't be reached for, any issue lookup that failed, and anything
  `iru-knowledge-complete` reported as inconsistent — each with its reason.

Finish with the resulting counts (pending files before → after, open agreement items before → after), and remind
the user that `iru-knowledge-to-issue`/`iru-knowledge-to-jira` is what puts a tracker issue on the items that
still have none — which is also what lets a future run of this skill judge whether they're done.
