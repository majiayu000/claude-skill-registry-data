---
name: scratch-status
description: "Report what is still open across .scratch/: every effort's open tickets and decisions, what blocks it, how stale it is, and the next skill to run. Read-only — never files research, removes anything, or touches disk. Companion to scratch-cleanup, which does those."
disable-model-invocation: true
argument-hint: "An effort slug to check just one (omit for every effort)"
model: sonnet
effort: low
---

# Scratch Status

A quick answer to "what's left to do in `.scratch/`", with nothing written or removed. For
the full sweep (filing research, removing done efforts, judging contradictions), that is
`scratch-cleanup`; this skill only ever reports.

`$ARGUMENTS` is an effort slug to scope to `.scratch/<slug>/` alone; empty means every effort.

In Claude Code with the leek-skills plugin, `/scratch [slug]` shows steps 1–2 live in a pane without a turn; point the user at it for a quick look. You cannot read that board, so always run the steps below: they add the commit-ancestry checks and the per-artifact report the board lacks.

## 1. Inventory

Read the tracker layout from `.agents/issue-tracker.md` (fallback `docs/agents/issue-tracker.md`,
then `setup/issue-tracker.md` in this collection) and the status vocabulary from the matching
`triage-labels.md`. Then walk `.scratch/` (or just `.scratch/<slug>/` when scoped) and find every
**effort**: a directory holding a map, spec, decisions, tickets, or triage request files. Older
efforts may use an `issues/` folder instead of `tickets/`; treat it as tickets. Skip `research/`
and any unclassified file: this skill reports on efforts, not the whole inbox.

For each effort, note its last change date: `git log -1 --format=%cs -- <path>` for tracked
files, the file mtime otherwise.

Done when every effort under scope is found, with a date.

## 2. Read each effort

For every file in an effort (map, every decision ticket, the spec, every build ticket), read its
status in either dialect: the YAML frontmatter `status:` field, or a legacy `**Status:**` /
`Status:` line near the top of the body. Also read:

- **Info for the report**: every file's `title`; the map's `## Destination` as one line; the
  spec's `## Problem Statement` as one line and the count of lines under `## Open questions`
  (zero when the section is absent); each closed decision's `## Resolution` (or `## Closed`
  reason) as one line.
- **Blockers**: any `Blocked by` line or explicit dependency reference to another ticket's id.
- **Claimed-by**: whether the ticket is claimed, and by whom.
- **Commit references**: a 7–40 character hex SHA in the status line, `## Resolution`, or
  `## Comments`; check `git merge-base --is-ancestor <sha> <default-branch>` (default branch:
  `git symbolic-ref --short refs/remotes/origin/HEAD` without the remote prefix, else `main`).
  A squash-merged or rebased commit is not missing. Before counting one as off the branch,
  check, in order: a merged PR contains it (`gh api repos/{owner}/{repo}/commits/<sha>/pulls`),
  `git cherry <default-branch> <sha> <sha>~1` prints it with `-`, or a default-branch commit
  has the same subject. Only a commit that fails all three is missing.

Classify the effort exactly as `scratch-cleanup` does:

- **done**: every file's status is closed or the wontfix role string, every cited commit is on
  the default branch, and nothing contradicts (a spec still `ready-for-agent` while every ticket
  is closed is a contradiction, so is a closed ticket whose commit is missing).
- **mismatched**: fails the contradiction check, or has a file with no readable status.
- **open**: has any open file. Note the single most-blocked chain if one ticket blocks several
  others.

An open effort is **stale** when its newest file is older than 30 days, the same default
`scratch-cleanup` uses.

These rules are the source of truth; the `/scratch` board's `hooks/mods/scratch-scan.ts` must
change with them, so a drift shows as the board and this report disagreeing.

Done when every effort in scope is labelled done, mismatched, or open (with stale marked), and
every open ticket has its blockers and claim state noted.

## 3. Report

One block per effort in scope, most urgent first (unblocked open work, then blocked open work,
then stale, then mismatched, then done). A **done** effort collapses to one line:
`` `.scratch/<slug>/` — done, last change <date>. Next: `/scratch-cleanup` ``. Every other
effort gets the full block:

```markdown
### `.scratch/<slug>/`: <open | ⚠️ mismatched> · last change <date><, ⚠️ stale>

**Map**: <title>, <status>. Destination: <one line>.
**Spec**: <title>, <status>. <problem, one line>. <n> open questions.

**Decisions**: <n> open of <n>
| # | Decision | Status | Resolution or blocker |
|---|---|---|---|
| 01 | <title> | closed | <resolution, one line> |
| 02 | <title> | blocked | by 01 |

**Tickets**: <n> open of <n>
| # | Ticket | Status | Detail |
|---|---|---|---|
| 01 | <title> | ready | |
| 02 | <title> | blocked | by 01 |
| 03 | <title> | in progress | claimed by <claimant> |
| 04 | <title> | closed | <short SHA>, on <default-branch> |

**Next**: `<command>`: <why, one line>.
<Also: up to two alternatives, one line each, only when they exist.>
```

Section rules:

- An absent artifact gets one line, so its absence is visible: `**Map**: none.`,
  `**Spec**: none.`, `**Decisions**: none.`, `**Tickets**: none.` Older efforts' `issues/`
  folder reports as Tickets; a loose triage request file gets its own line,
  `**Request** <file>: <title>, <status>.`
- List every decision and ticket, closed ones too, in number order.
- **Status** is one word, derived, never the raw field: `closed` (status closed or wontfix;
  say `wontfix` in Detail), `in progress` (claimed, or status `in-progress`), `blocked` (any
  `blocked-by` entry not closed), `ready` (open, unblocked, unclaimed), or `⚠️ unreadable`.
- **Detail** for a ticket: the open blockers (`by 01, 03`), the claimant, or for a closed
  ticket its cited commit and whether it is on the default branch (`⚠️ <sha> missing` when it
  failed all three checks). Empty when there is nothing to say. A decision's last column is its
  one-line resolution once closed, its blockers or claimant while open.
- Mark nothing else with ⚠️: only stale, mismatched, unreadable, and missing commits.

**Next** names the one command that moves the effort forward, then says why in plain words:

| Situation | Next |
|---|---|
| An open, unblocked, unclaimed decision | `/grill-me <decision path>`, the lowest number |
| A map with no decisions yet | `/wayfinder <map path>` |
| Every decision closed, no spec | `/to-spec` |
| A spec with open questions and no tickets started | settle them first: `/grill-me <spec path>` |
| A spec with no tickets | `/to-tickets <spec path>` |
| An unclaimed, unblocked build ticket | `/implement <ticket path>`, the ready ticket that unblocks the most others (lowest number on a tie) |
| Only the delivery ticket left, at `ready-for-human` | after deploy: `/implement <delivery ticket path>` |
| Only claimed or blocked work left | who to wait on, or which blocker to clear |
| Mismatched | ⚠️ the contradiction in one line, and what to change to settle it |

The **Also** line gives real alternatives, not repeats: with two or more ready build tickets,
`/implement-spec <spec path>` builds the frontier in parallel; with several ready decisions,
`/wayfinder <map path> all` resolves them in one run; the other ready ticket ids by number.

After the last block, one line naming any effort with no readable status file at all, then a
one-line total: `<n> open, <n> stale, <n> mismatched, <n> done`. Stop there: no plan, no
questions, no approval prompt.
