---
name: merge-recent-issues
description: Use when the lead wants the last couple of days' new issues checked against the open pool for merges — "merge recent issues", "did we file any duplicates", "check the new issues against the backlog", "anything filed today that belongs on an existing issue", or a bare "/merge-recent-issues". Takes an optional day count (`/merge-recent-issues 5`); defaults to 2 days. Reads every issue filed in the window and asks one question each — does this belong on an issue that already exists? Compares only against Backlog, unassigned Ready, and icebox, so it never steals a card someone has started. Run it daily, right after /triage-standup files the day's inflow. Verdicts and merge doctrine come from /merge-issues, which owns them; this is the cheap daily catcher, not a second opinion. Proposes first and applies only what the lead approves; never starts the work, and never writes the project board.
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Merge recent issues

`/merge-issues` **owns merge doctrine**. This skill owns *selection and cadence*:
it looks only at what was filed in the last couple of days, while the reason for
each filing is still recoverable and before a duplicate gets ranked, promoted and
assigned.

**Run this daily; do not run `/merge-issues` daily instead.** A new issue landing
on top of an existing one is the case that decays fastest and the cheapest to
check. N *old* issues queued on one eval slot is what `/merge-issues` is for, and
obsolescence, clusters and board hygiene are `/audit-board`'s.

**Read `.claude/skills/merge-issues/SKILL.md` before proposing anything, and use
its verdicts verbatim.** Do not invent a verdict here and do not restate its
rules in your own words. If this file and that one ever disagree, that one wins
and the disagreement is a finding to report.

**You propose, then apply what is approved.** No branches, no PRs, no code edits.
You have no `Edit` or `Write` tool on purpose.

**Never write the project board.** Closing an issue auto-moves its card to Not
planned; nothing else here needs a column change. A `gh` token without the
`project` scope fails a board write while appearing to succeed.

## 0. The window

Default **2 days**. The lead may pass a day count: `/merge-recent-issues 5`.

```sh
d=$(date -v-2d +%Y-%m-%dT%H:%M:%SZ)   # or -v-<N>d
gh issue list --repo PioneerAIAcademy/cowork-genealogy --state open \
  --limit 300 --json number,title,body,createdAt,labels,assignees \
  --jq "[.[] | select(.createdAt > \"$d\")] | sort_by(.createdAt)"
```

**The window overlaps on purpose — do not tile it.** Two days re-reads roughly
one day of already-checked issues every run, which costs one skim each and finds
nothing. The opposite error is permanent: an issue filed Friday afternoon, with a
24-hour window run Monday morning, is never seen by this skill again. Overlap is
cheap; a gap is forever.

If the lead asks for exactly one day, do it — but say in the report which issues
fell outside the window that a 2-day run would have caught.

## 1. What to compare against

**Backlog, unassigned Ready, and `icebox`.** Nothing else.

```sh
gh project item-list 1 --owner PioneerAIAcademy --limit 2000 --format json
```

The board list truncates silently at `--limit`; the project has well over 600
items, so a limit that equals the row count means you lost rows. Check the length
against the number you asked for before trusting it.

**Do not merge into In Progress, Review, or assigned Ready.** Someone is holding
that card. If a new issue genuinely duplicates active work the verdict is
**close as duplicate of active work** — close the *new* one, comment pointing at
the active card, and say so in the report so the lead can tell the holder. That
is a different action from a merge and should never be reported as one.

## 2. The verdicts

Read `/merge-issues` and use its four verdicts — duplicate, absorb, batch, and
the lane split — plus the close-as-duplicate-of-active-work above. Everything it
says about **which** verdict applies binds here unchanged; do not re-derive it
from this file.

Three of its rules decide most of what this pass sees:

- **Search by fix site, not by topic.** Read the `**Touches:**` line first.
  Issues that collide almost never share a title — they want different lines in
  one file. A body with no such line is not "touches nothing"; read it by hand.
- **Never replace N issues with one issue holding N rows.** No trackers, no
  umbrellas, no index issues.
- **The default is merge.** Same decision, same files, same paid eval run, same
  reviewer, or one is the class and the other its instance — all merge.
  "Cross-reference and note it", "schedule together" and "decide together but
  keep separate" are not verdicts. Splitting on *mechanism purity* — two tools,
  two matchers, two code paths — is an author's aesthetic, not a work boundary.

Two instructions this pass owes on top of that:

**Never report "different lanes" as the reason for an independent verdict.** A
lane difference is never on its own a reason to keep two issues apart. If it is
the only thing separating two issues on the same skill, they merge — and the paid
eval run they would otherwise each need is the reason.

**A one-way mechanical dependency is a body edit, not a merge.** When issue B
only needs to *apply* something issue A defines — a convention, a constant, a
helper — do not merge and do not cross-reference. **Edit B's body** so the
dependency reads as an instruction ("apply the convention issue #A defines")
rather than a coordination requirement.

## 3. Prove it before proposing

**Open the files both issues name.** Title and framing resemblance is the
dominant false positive here, and it is convincing — two issues both described as
"a prose lint with a file-and-line allow-list" routinely share no mechanism at
all, one comparing hashes across duplicated copies and the other matching a
banned phrase.

Three checks, every proposed merge:

1. **Same fix site?** Open the file. Quote the lines.
2. **Blocked or unblocked?** **Never merge an unblocked issue into a blocked
   one** — that parks ready-to-start work behind an adjudication it does not
   need. Check both bodies for a stated blocker and resolve it
   (`gh issue view <N> --json state`).
3. **Does it add a paid eval run?** If the absorbed issue's skill is already in
   the target's touch list, merging is free — say so. If it is not, the merge adds
   a `make eval-skill` run plus an annotation pass, which is a real cost the lead
   should see stated, not discovered later.

An issue body is **a claim written on a particular day**. Verify any factual
claim — a path, a line number, a measurement, a tool's behaviour — before
repeating it, and cite what you checked.

## 4. Applying an approved merge

Four steps. Skipping any one of them loses something.

1. **Fold the content into the target**, under a heading naming the source issue
   and the date. Carry the detail the absorbed issue adds — its evidence, its
   acceptance criteria, its sequencing gate, its extra `Touches:` paths. A merge
   that drops the loser's specifics is a close, and should have been reported as
   one.
2. **Retitle the target if its title no longer covers the merged scope.** A title
   that describes half the work is how the other half gets forgotten by the person
   who picks it up.
3. **Move the assignee and any label the target lacks.** An absorbed issue with an
   assignee has someone expecting to do it — `gh issue edit <target> --add-assignee
   <login>` — and say so in the report so the lead can correct it. A `nothing-checks`
   or `cluster:*` label on the loser must survive too.
4. **Close with the reasoning, not just a pointer.**

```sh
gh issue close <N> --repo PioneerAIAcademy/cowork-genealogy \
  --reason "not planned" \
  --comment "Merged into issue #<target>.

<why these are one piece of work — the shared decision, file, or run>"
```

Write the comment for someone who filed the issue and will wonder where it went.
"Duplicate of #N" is not enough; name what the two share.

If the target's body carries a banner or note asserting the two are separate,
**rewrite it in the same pass**. A stale "keep these apart" note outliving the
merge is worse than no note.

## 5. Output shape

1. **Merges** — one block each: the pair, the shared fix site with the lines you
   read, the verdict from `/merge-issues`, which issue survives and why, whether it
   costs an eval run, and any assignee being moved.
2. **Close as duplicate of active work** — separately, with who holds the card.
3. **Body edits** — one-way mechanical dependencies, with the exact replacement
   sentence.
4. **Independent** — one line per remaining issue. This is most of them on most
   runs, and it should read as a checklist. "Nothing merged today" is a good
   answer; do not manufacture a pair to justify the run.
5. **Anything you could not check**, and why — an unreadable file, an issue whose
   `Touches:` line is missing and whose fix site you could not infer.

Then stop and wait for approval. Apply only what he approves. Do not begin any of
the work the issues describe.
