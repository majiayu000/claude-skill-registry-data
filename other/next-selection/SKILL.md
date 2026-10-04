---
name: next-selection
description: Choose what goes into the kajet-turbo project board's Next column — a balanced round of fixes, refactors and features drawn from the prioritized Backlog, respecting blocked-by chains and grouping into PRs, applied to the board only after the user approves. Use when the user asks what to work on next, wants to plan or refill Next ("przedyskutujmy priorytety na Next", "co bierzemy dalej"), or Next has run dry. Filing is issue-filing; assigning priorities is backlog-triage.
---

# Next selection: Backlog → Next

Selection is the third stage (`issue-filing` → `backlog-triage` → **selection**). It
reads the priorities triage assigned and does not reassign them. What it adds is the
shape of the next round: the mix of work, the dependency order, and the PRs it turns
into. Before starting, read [`../_shared/board.md`](../_shared/board.md).

## Sizing and mix (the user's standing preferences)

- **Size**: about 15 issues, **counting what is already In Progress**. Everything moves
  concurrently: other sessions put their issues In Progress while you plan.
- **Mix**: some fixes or hardening, some refactors, some features, every round. One
  category taking the whole round needs a stated reason.
- **Refactors**: prefer ones with a correctness or risk angle (a fail-open path, a
  limiter bypass) over cosmetic dedupe. Offer the cosmetic ones as an optional add-on,
  and only when they bundle cleanly into one PR.
- **Features**: prefer continuing the milestone currently being worked (its epic has
  recently ticked children) over opening a new front.

## 1. Collect

```bash
python3 .claude/skills/_shared/board.py stale
python3 .claude/skills/_shared/board.py list --status "In Progress" Next Backlog Blocked
git fetch -q origin main
```

If the stale report shows untriaged work (a large Inbox, or triaged issues without a
priority), say so. Selection from a half-triaged Backlog quietly skips issues that were
never weighed. Offer `backlog-triage` first, or proceed if the user prefers.

Read the full body of every candidate you have not read in this session. The
prioritized Backlog tells you what matters; the body tells you what the work is, what it
depends on, and whether it bundles with something else.

## 2. Build the round

1. **P0 and P1 go in by default.** Leaving one out needs a reason.
2. **Verify each candidate against `origin/main`** (Staleness table in `board.md`). An
   issue that is obsolete, already fixed, or absorbed by a PR is not a candidate: it is a
   clean-up. The first selection found that a P1 issue had been obsolete for weeks,
   because an architecture change had removed the thing it asked to fix.
3. **Fill the mix from P2.** Pick per category, not strictly by P order.
4. **Chains**: a blocked-by chain (A → B → C) goes in as an ordered chain or not at all.
   Include the head, and include later links only if the round is long enough to reach
   them. Never select a link whose blocker is not in the round or already In Progress.
   `board.py stale` flags this as "In Next but blocked by an open issue" — that is fine
   for an ordered chain and wrong for anything else.
5. **Group into PRs.** Issues touching the same function or file ship together, even if
   only the first one is in Next. Name the PR count, because it is a truer size of the
   round than the issue count.

## 3. Propose

Send one table grouped by type (fix, refactor, feat, plus what is already In Progress),
with P and a reason of at most one line. Below it give:

- the proportions and the PR count;
- **deliberately left out**: the two or three nearest misses and why, so the user can
  swap them in without re-reading the Backlog;
- clean-ups found on the way (obsolete issues to close, labels, `Closes` lines).

Ask in one `AskUserQuestion`: accept, add more of one category, or make swaps. Add a
multi-select for the clean-ups.

## 4. Apply (after approval)

Re-run `board.py list --status Next "In Progress"` first, since another session may have
moved items in the meantime. Then:

```bash
python3 .claude/skills/_shared/board.py set 403 368 397 274 --status Next
python3 .claude/skills/_shared/board.py set 381 382 384 --status Next --priority P2  # unprioritized picks
```

Selected issues that had no priority get one; selection never leaves an unprioritized
item in Next. Don't touch In Progress items.

## 5. Verify and hand off

List Next and In Progress again and confirm the round matches the approved table,
including anything that changed underneath you. Close by naming the first PR to pick up
and why (usually the highest-P item, bundled with whatever it shares a function or file
with).
