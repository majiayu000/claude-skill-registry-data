---
name: review-ready
description: Use when the lead wants tasks vetted before juniors start them — "vet these before I hand them out", "are these tasks still a good idea", "is this safe for a junior", "review the fill-ready shortlist", "check the junior queue", or a bare "/review-ready". The gate between fill-ready (which ranks and promotes) and standup (which hands work out); covers both unassigned pools, developer and genealogist, with `--developer-only` to narrow it. Fans out one read-only task-reviewer agent per candidate issue, in parallel, each in fresh context — every agent reads the issue's cited code, the matching docs/architecture.md "If you're asked to…" block, the board's what-nothing-checks issues, and the relevant ADRs, then returns a verdict, the exact body text to add, and any decision only the lead can make. Collates the verdicts and writes each open question into its issue for `/make-decisions` to answer; applies the rest only when approved. Do NOT use to choose what the team works on, to rank the Backlog, or to move anything on the board — that is fill-ready, which calls this skill on its shortlist. Never starts the work.
allowed-tools:
  - Agent
  - Bash
  - Read
  - Grep
  - Glob
---

# Review tasks before juniors start them

`fill-ready` decides what the team starts. This decides whether those issues are
**safe to hand to a junior working with Claude Code**, whose failure mode is a
green, plausible, wrong PR rather than a stalled one.

Rationale, contracts, measurements and rejected alternatives:
`docs/specs/task-review-spec.md`. Read it before changing this skill or the
agent; do not re-derive what it settles.

**You propose, then apply what is approved — with one exception.** A
`## Decision needed` block and its `needs-decision` and `reviewed` labels go in on
your own authority; recording a question is not a decision, and a question nobody
wrote down is one nobody answers. Everything else waits. No branches, no PRs, no
code edits, no eval runs, and no board moves — promotion and demotion belong to
`fill-ready`.

## 0. Board facts

Repo `PioneerAIAcademy/cowork-genealogy`, project **1**.

```sh
gh project item-list 1 --owner PioneerAIAcademy --format json --limit 2000
```

## 1. Pick the candidates

**The normal case is `fill-ready`'s shortlist, before it promotes.** Its verdicts
feed that decision: a `needs-a-decision` item never enters the unassigned pool,
so it is never promoted and then swapped back out. A `senior` item does enter it
— it ranks in its lane's pool like anything else. Reviewing after promotion costs
the same issue two deep reads — see the spec, §2.

Other entry points:

- **Issue numbers as arguments** (`/review-ready 945 1031 1094`) — review exactly
  those, in any column. This is also how a re-review is asked for.
- **Bare `/review-ready`** — the standing pool: unassigned items in Ready, **both
  pools**, `developer` and `genealogist`. A first run, or a run after a gap.
- **`--developer-only`** — the old default, kept for a cheap pass when you know
  the genealogist half was gated this week. Halves the token cost and halves the
  coverage.

**`feedback`-labeled items are never in scope**, in any mode. They carry
`genealogist`, so they would otherwise land in the fan-out, but they are raw user
submissions sitting untriaged in the Feedback column — every question the three
passes ask is answered by working the case, not by reading the issue. Reviewing
one costs ~110k tokens to learn nothing. `/triage-feedback` owns them.

**A triaged one has already lost the label**, and is in scope exactly like any
other Backlog item: triage retitles it, writes the instructions and the
`**Touches:**` line, and drops `feedback` on the way to Backlog. So the filter
below needs no special case — if you are seeing the label, it has not been
triaged yet.

**Why both pools, since this was developer-only until 2026-08-19.** A stale
premise is not a developer-shaped defect. The run that changed it gated six
developer issues and zero genealogist ones, and four of the six came back
not-pickable — two carrying checks that would have shipped green and inert. The
genealogist half went to Ready on one reader's judgment. And a bad genealogist
premise is the more expensive one to discover: it surfaces in a paid
`make eval-skill` run, not in CI. The cost is real — roughly double, ~110k tokens
per issue — and is the point of the `--developer-only` escape, not a reason to
default to it.

### Review on entry, not daily

**Skip an item that already carries the `reviewed` label.** The board read in §0
answers this for every candidate at once — this is the whole standing-pool query:

```sh
# BOTH pools. A bare run covers `developer` and `genealogist` — the paragraph
# above is why. `--developer-only` is what narrows this back to one lane; do not
# bake that filter in here, which silently reverted the both-pools change once.
# `feedback` items are never in scope, in either lane — most carry `genealogist`
# and are raw untriaged bundles, and reviewing one costs ~110k tokens to learn
# nothing. `/triage-feedback` drops the label on the way to Backlog, so anything
# still carrying it has not been triaged and this filter is the whole guard.
gh project item-list 1 --owner PioneerAIAcademy --format json --limit 2000 | jq -r '
  .items[]
  | select(.status == "Ready" and (.assignees | length) == 0
           and ((.labels | index("developer")) or (.labels | index("genealogist")))
           and ((.labels | index("feedback")) | not)
           and ((.labels | index("reviewed")) | not))
  | .content.number'
```

Steady state is then the three to five items `fill-ready` shortlisted that
morning, not the pool. Getting this wrong costs ~110k tokens per needlessly
re-reviewed issue.

Also skip, and say why: a body that is empty or a single line. That is a
`fill-ready` rewrite verdict, not a review.

**Cap the fan-out at 20 per run** — one full standing pool. The cap binds only on
a first run or after a gap; the steady-state delta never approaches it. When it
does bind, take the unreviewed ones oldest first, and **say in the report exactly
which candidates you did not review** — a silent cap reads as "everything is
clear" when it is not.

## 2. Fan out — one agent per issue, all in one message

Launch every `task-reviewer` **in a single message with multiple tool uses** so
they run concurrently. One agent per issue, never one agent for several: fresh
context per issue is what stops issue 7's reasoning contaminating issue 8's.

Each agent gets only:

```
Review issue #<N> in PioneerAIAcademy/cowork-genealogy for handoff to a junior
developer working with Claude Code. Follow your instructions exactly and return
your report in the specified format.
```

Do **not** pass your own opinion of the issue, its board rank, or another
agent's findings. An agent told what to expect finds it.

Do not review the issues yourself while the agents run. Wait.

## 3. Collate

Read every report. Then, in your own voice:

- **Group by verdict**, most consequential first: `close` and `stale-rewrite`
  (the board is wrong), then `senior` and `needs-a-decision` (the routing is
  wrong), then `ready-after-edit`, then `ready`.
- **Cross-check the agents against each other.** They ran blind, so two agents
  proposing edits to the same file, or naming the same open PR, is a collision
  neither could see. Say so.
- **Do not re-argue a verdict you have not checked.** If one looks wrong, spend
  the two minutes to verify it and say what you found — do not soften it.
- **Count the routing damage, split by remedy.** How many unassigned `developer`
  items in Ready turned out to be `senior`, and how many `needs-a-decision`? That
  pair is the report's headline: it is how much of the junior pool was not
  actually pickable, and the split says whether the fix is people or answers. A
  pool that is mostly `needs-a-decision` is cheap to unblock and is the strongest
  thing you can put in front of the lead.

## 4. Write the decisions down

**Never ask them.** Whoever runs this skill is not necessarily the person who
answers, and the answer arrives on its own schedule. `/make-decisions` presents
these and records the ruling.

Each agent returns its decisions already shaped — header, question, options with
the consequence that decides each, recommended first. **Pass them through
verbatim.** Do not rewrite an option's description into your own words: the agent
read the spec, the ADRs and the code, and you did not.

Then do the three things it could not, because it saw one issue. **All three
happen before any body write** — a fork shared by two issues written twice is a
question answered twice:

- **Merge identical forks.** When two issues ask the same question, write it once
  as policy and have the second point at the first — one answer, two issues
  unblocked.
- **Rank across issues**, not within one. It sets the order they are met in.
- **Drop what the answer would not change.** A choice with a conventional default
  is not a question — state the default you are assuming and move on.

Settle the smaller forks yourself and write each one into its issue body as a
stated assumption. An assumption that lives only in your report is invisible to
the junior who picks the issue up.

**Gate every surviving question on the agent's four-way test before you write a
block.** A fork is the lead's only if one live option spends money the card does
not budget, sets doctrine or precedent, adds hard-to-reverse surface, or touches
a prior ruling. If none applies, the agent should have decided it; write its
recommendation into the body as `**Decided (review-ready, <date>): A, <the
consequence>.** B considered: <one line>.` and treat the verdict as `ready`. A
fork whose every live option is $0, reversible, precedent-free and clear of any
prior ruling is never a question for him.

**Grep the comments for `Ruling` and `Decision` first.** A question already
ruled in a comment gets the ruling applied, not a block and a label, unless a
fact it rested on has since changed (`CLAUDE.md`, "A ruling binds only while its
premises hold"). Then write the block, naming the change.

**`needs-decision` routes to the lead and nobody else.** To reach a senior
reviewer on a PR question, @-mention them on the issue. Do not use the label.

Write each surviving question into the issue **body**, above the reviewed marker:

```
## Decision needed — <header>

<question, one sentence>

- **A — <label>** — <consequence that decides it>  *(recommended)*
- **B — <label>** — <consequence>

<details><summary>Body text if A</summary>

<the issue-body text option A produces>

</details>

<details><summary>Body text if B</summary>

<the issue-body text option B produces>

</details>

*Prepared by review-ready YYYY-MM-DD.*
```

**Carry every option's pre-written body text, not just the recommended one.** The
agent wrote one block per option precisely so that applying the answer is a
mechanical splice by someone who did not do the reading. Drop them and the
splice becomes a rewrite, and `/fill-ready` skips its gate on text nobody vetted.

**Apply `needs-decision` in the same write.** A block without the label is
invisible to every query in the loop. `reviewed` goes on after, once the block
has landed.

**This write is not gated on approval** — recording a question is not a decision,
and a question nobody wrote down is a question nobody answers. Body, not a
comment: a finding in a comment thread is a finding that evaporates.

## 5. Write the verdicts

**Every verdict has a write** — a verdict you cannot act on silently does
nothing. The `## Decision needed` block and the `needs-decision` label go in on
your own authority. Every other write waits for approval — and `reviewed` goes on
only after every write that verdict needs has landed, so a `ready-after-edit` or
`stale-rewrite` item is not labelled until its approved body edit is in.

```sh
# needs-a-decision — the fixed-format `## Decision needed` block, ungated.
# ready-after-edit / stale-rewrite — the agent's replacement text, once approved.
gh issue view <N> --repo PioneerAIAcademy/cowork-genealogy --json body -q .body > body.md
# edit body.md, then:
gh issue edit <N> --repo PioneerAIAcademy/cowork-genealogy --body-file body.md

# senior — hard regardless of any open question. Label only, no assignee: work
# is handed out at standup, not here. Keep the developer/genealogist label on it
# — that is what picks the lane, and CODEOWNERS routes the review the same way.
gh issue edit <N> --repo PioneerAIAcademy/cowork-genealogy --add-label senior

# needs-a-decision — NOT senior. One answer unblocks it, and the work behind it
# is frequently junior. Labelling this `senior` is the common mistake: it sends a
# sentence looking for a scarce person. The `## Decision needed` block must
# already be in the body — `/make-decisions` has nothing to present without it.
gh issue edit <N> --repo PioneerAIAcademy/cowork-genealogy --add-label needs-decision

# close
gh issue close <N> --repo PioneerAIAcademy/cowork-genealogy \
  --reason "not planned" --comment "<why>"

# every verdict except close, last — this is what §1 skips on next run
gh issue edit <N> --repo PioneerAIAcademy/cowork-genealogy --add-label reviewed
```

**Add the `reviewed` label last**, after the body write lands. Labelling first and
failing on the body leaves an issue that looks vetted and is not.

One-time, if the label does not exist yet:

```sh
gh label create reviewed --repo PioneerAIAcademy/cowork-genealogy \
  --description "Vetted by task-reviewer before junior handoff" --color 0E8A16
```

Rules on the writes:

- **Edit the body, not a comment.** The junior reads the body. A finding in a
  comment thread is a finding that evaporates.
- **Prepend, never replace — except `stale-rewrite`.** Keep the original text
  below your addition under an `## Original issue` heading. A `stale-rewrite`
  replaces the ask, because the premise moved and the ask is now wrong; it keeps
  the original under the same heading.
- **Open the body with the marker**, for the junior who picks it up:

  ```
  > **Reviewed <YYYY-MM-DD> before junior handoff.** <one clause: decision
  > recorded below / no decision needed / premise was false>; the original body
  > follows under "Original issue".
  ```

  This is prose for a reader, not state. The `reviewed` **label** is the state,
  here and in `/fill-ready`. `/make-decisions` refreshes the clause when it
  records a ruling.
- **Carry the rationale to the destination the agent named** — a spec section, a
  comment at the constraining site. It is part of the task, not a nicety;
  `CLAUDE.md` keeps settled tradeoffs out of issue bodies for a reason.
- **Board moves are `fill-ready`'s.** On the normal path a `senior` or
  `needs-a-decision` verdict comes back before promotion, so there is nothing to
  move — you label it and it stays in Backlog, out of the junior pool. On a
  standing-pool run the item is already in Ready; report it for the swap.
- **Never answer a fork yourself, and never record one as answered.** Every
  surviving question gets written down and labelled `needs-decision`.
  `/make-decisions` is the only place a ruling is taken and applied.
- **`senior` and `needs-decision` are orthogonal — apply both when both are
  true.** They answer different questions (`fill-ready` §6): `senior` says *who*
  does the work once it is startable, `needs-decision` says *what* is blocking it
  now. An item can be hard **and** waiting on one answer; label it both, and it
  stays out of the ranking until the answer lands, then goes to a senior.
  What you must not do is reach for `senior` on an item that is merely
  undecided — that sends a sentence looking for a scarce person.

Deleting an issue needs the lead to say so for that specific issue. Never batch
a delete under a general approval.

## Output shape

1. **Headline** — how many candidates, how many came back not-pickable
   (`senior` + `needs-a-decision`), and how many you did not get to.
2. **Not-pickable** — the `senior` and `needs-a-decision` items, each with the
   one-line reason and where it should go instead.
3. **Wrong on the board** — `close` and `stale-rewrite`, with the evidence.
4. **Body edits** — a table: issue, verdict, whether it landed or awaits approval, the one-clause reason, and
   what the edit adds (missing sites / the instrument / the hidden cost / the
   inoculating sentence). Full text below the table, not in it.
5. **Clean** — the `ready` items, one line each including the one thing each
   agent would still improve.
6. **Cross-issue** — collisions the individual agents could not see, and any open
   PR touching the same files.
7. **Questions written down** — one line each, with the issue they landed on.

Then stop. The `## Decision needed` writes and their labels go in regardless;
everything else waits for approval.
