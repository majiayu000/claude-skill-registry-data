---
name: backlog-triage
description: Triage the kajet-turbo project board's Inbox into Backlog — read every Inbox issue, check it against origin/main for obsolete premises, propose a P0–P3 priority per issue grouped by theme, and apply it to the board only after the user approves. Also picks up triaged issues that still lack a priority. Use when the user asks to triage, prioritize, or clear the Inbox ("nadajmy priorytety", "przenieśmy inboxy do backlogu"), or when board.py stale reports untriaged work. Filing issues is issue-filing; choosing what goes into Next is next-selection.
---

# Backlog triage: Inbox → Backlog

Triage is the second stage (`issue-filing` → **triage** → `next-selection`). Its output is
a `Priority` on every triaged issue and Status `Backlog`. That priority is the contract
`next-selection` reads, so it has to reflect the issue as it stands **today**, not as it
stood when it was filed. Before starting, read [`../_shared/board.md`](../_shared/board.md)
for the priority scale, the blocking rules, and the staleness checklist.

The user decides and you propose. Triage is a conversation: nothing on the board changes
until the user has seen the whole table.

## 1. Collect

```bash
python3 .claude/skills/_shared/board.py stale                # mechanical staleness
python3 .claude/skills/_shared/board.py list --status Inbox  # the work
git fetch -q origin main
```

Include issues from the stale report's "Triaged issue without a priority" section in the
same round. They are untriaged work that bypassed the Inbox.

Dump every issue body to the scratchpad (`gh issue view N --json number,title,labels,milestone,body`)
and **read them all, in full**. The `## Impact` section is the main signal. Titles lie by
omission: "risk:" can mean anything from a latent footgun to an unpinned audit invariant.
With more than about 40 issues you may split the reading across subagents, but you
assign the priorities yourself.

## 2. Verify against `origin/main`

Code-review spin-offs age fast: the refactor that the review was part of keeps moving
code. For each issue, grep its cited symbols and paths on `origin/main` and classify it
with the Staleness table in `board.md`: valid, valid but the code moved, already fixed,
premise gone, or implemented by an open PR. This is the step that catches what the
mechanical report can't. In the first triage it found one issue already fixed by a
merged PR, one whose premise a refactor had deleted, and one being implemented by an open
PR that had no `Closes` line.

## 3. Propose

Send one message, grouped by **theme**, not a flat list of 40 rows. Useful themes are
the ones that later become PRs: security and PII, DB and ops, the follow-ups from one
refactor, one milestone's chain, frontend, dev loop. For each row give the issue number,
the proposed P, and a reason of at most one line taken from the issue's own Impact.

Calibration, beyond the scale in `board.md`:

- **Observed in production and violating a stated project rule** (PII in logs,
  anonymization) → P0 or P1. Say that it was observed; don't just assert severity.
- **Dev-loop pain** that hits every session (tests hanging in worktrees, a broken check)
  → P1. Every Claude session runs in a worktree, so every session pays for it.
- **Confirmed user-visible bug class** → P1, even if only one instance has been proven.
- **A milestone's chain**: the next unblocked step is P1, the middle of the chain is P2,
  and the closing tail (dashboards, validation) is P3. The epic itself gets no P.
- **Latent risk with no incident**, or a real feature gap → P2.
- **The issue's own Impact says "cosmetic" / "not a problem today"** → P3. If you think it
  is worth more, say why explicitly. Never upgrade silently.
- Note **bundling** where you see it (two issues touching the same function, one PR), so
  `next-selection` can use it.

Keep a separate section listing what does **not** go to Backlog: close candidates
(already fixed, premise gone), absorbed-by-PR items, and epics with closed children still
unticked. Then ask the binary decisions in one `AskUserQuestion`: the overall table
accepted or corrected, which clean-ups to do, and any close-an-epic question.

## 4. Apply (after approval)

```bash
python3 .claude/skills/_shared/board.py set 403 --status Backlog --priority P0
python3 .claude/skills/_shared/board.py set 368 260 397 --status Backlog --priority P1
python3 .claude/skills/_shared/board.py set 304 394 --status Backlog   # epics: no priority
python3 .claude/skills/_shared/board.py tick-epic 392 --apply
```

Closures and `Closes #N` edits go through `gh`, with English comments that name the PR
or commit. Epics are closed only on an explicit yes.

## 5. Verify

Re-run `board.py list --status Inbox` (it should come back empty) and `board.py stale`.
Compare the Backlog priority counts with the approved table, then report the outcome:
counts per P, what was closed, what was deferred, and anything the stale report still
shows that is out of this round's scope.
