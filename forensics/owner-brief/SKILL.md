---
name: owner-brief
layer: method
description: Shape every agent comment as a short typed brief the owner can triage in seconds — 🔴 issue · 💡 proposal · ✅ done · 🔀 choice · 🛠 action · 👀 review — with all the depth collapsed behind it. Enforced by the require-owner-brief hook. Use before posting ANY GitHub comment as an agent, or when asked to "make this shorter", "brief me", "just tell me what I need to do".
allowed-tools: Bash, Read, Grep
---

# The owner brief — one line they act on, everything else collapsed

The owner reads these on a phone, holding ~20 async threads. **The depth is not the problem
and is never cut** — the problem is that it arrives *as* the notification, so every ping costs
a full read.

So: **lead with a typed brief, collapse the rest.** Same comment, same content, different order.

## The six types

Pick exactly one. The last three are `ask-human`'s existing shapes — this is one vocabulary,
not a parallel system; reach for that skill's templates when the brief is a hold.

| | type | means | typical follow-up | may @mention? |
|---|---|---|---|---|
| 🔴 | **Issue** | something is broken or wrong | you decide whether it's worth fixing now | yes |
| 💡 | **Proposal** | a suggestion you can take or drop | yes / no / later | yes |
| ✅ | **Done** | landed and verified | nothing | **no** |
| 🔀 | **Choice** | a real fork, needs your pick | `A` / `B` | yes |
| 🛠 | **Action** | you must do something the agent can't | do it, then comment | yes |
| 👀 | **Review** | approve or reject a diff/preview | ✅ / `lgtm` / changes | yes |

If two apply, pick the one that describes **what you need back**, not what you did. A bug you
already fixed is ✅, not 🔴.

## The other half: don't spend a mention on nothing

**An @mention is a request for action.** Spending one on an FYI teaches the owner to ignore
mentions, which costs far more than the notification. The gate refuses a ✅ carrying a live
mention.

**Where the noise actually came from.** Over the last 100 comments, 29 would notify the owner
and **17 of those carried no ask at all** — their only mention was the mandatory provenance
disclaimer, `posted from @pmcp's account`. It sits in a blockquote, so a reader never sees it,
and GitHub notifies anyway. That was **59% of every ping**.

So the disclaimer now writes the handle in a **code span**:

```
> 🤖 **Claude Code** · interactive agent · posted from `@pmcp`'s account (not Maarten)
```

It renders identically and does not notify. Backticking it across the templates removes those
17 pings; the 12 that remain are genuine asks.

**GitHub notifies for a mention inside a blockquote and inside `<details>`.** Code spans and
fenced blocks are the only places it doesn't. So "hide it in the collapsed section" does *not*
make a mention silent — backtick it, or don't write it.

## The shape

Visible part **≤700 chars and ≤10 non-empty lines**:

```
🔴 **<one line: what happened>**
> 🤖 <provenance header — its own hook requires this>

**You:** <the single next action — or "nothing, FYI">
**Depth:** <link to the full comment / PR / run / report>

<details><summary>Findings / patch / evidence</summary>

…everything you were about to write, at any length…

</details>
```

**`**You:**` is the load-bearing line.** If you can't state one next action, you don't yet know
what you're asking for — work that out before posting.

## Say the visible part plainly (the word-choice layer)

Structure is only half. A brief that is the right shape and still full of repo jargon fails just
as hard — the owner said so, repeatedly: *"i have no idea what you said"*, *"thats unreadable"*,
*"this is gibberish to me"*. The rule is in `AGENTS.md` (*Plain language*); here is what it looks
like, from real messages this session:

| ❌ what was written | ✅ plain |
|---|---|
| "work the second group down — re-dispatch the tasks, verify/close the stale ones — so the filter converges to just the 8 that are genuinely yours" | "8 of these aren't really waiting for you — they got the wrong label. Want me to clean them up? **yes / no**" |
| "the sweep will tag the nine stranded PRs `status:needs-merge` for one-click merging" | "nine finished PRs will show up needing one tap to merge" |
| "#2095 keeps it that way going forward" | *(cut it — the owner doesn't run the plumbing)* |
| "re-dispatch the task to the pipeline" | "hand it back to run again" |

The pattern in every miss: naming the **mechanism** (the sweep, the filter, the label, the issue
number) instead of the **outcome** (what the owner sees or does). Read the visible part aloud as if
to someone who's never seen this repo; any phrase that needs a footnote gets rewritten.

## What doesn't count against the limits

Nothing inside `<details>`, a code fence, the provenance blockquote, an HTML comment marker, or
the generated-by footer. **Collapse it, don't cut it** — if the escape hatch weren't real,
agents would delete content instead of moving it, which is worse than the wall.

A comment with **no 🤖 header** (a human's) is untouched at any length.

## Two failure modes

**Burying the ask.** #2054 posted a patch-to-apply under a question heading, and the gate
announced *"asked you a question"* above 4,372 characters containing no question. The type
marker exists so this can't happen: it says what's wanted before anything else is read.

**Splitting the thread.** Don't post the brief and the depth as two comments — one comment,
brief in front, depth in `<details>`. Two comments doubles the notifications, which is the
problem, not the fix.

## Enforcement

`require-owner-brief` (PreToolUse on `add_issue_comment`) blocks a non-conforming agent
comment and prints the vocabulary + the collapse rule. The decision is
`scripts/owner-brief.mjs` — pure, unit-tested, and checked against the real comment corpus.

**Why the trigger is "is this an agent comment" and not "does it @mention the owner":** the
@mention rule was the obvious design and measuring killed it. Of the 29 owner-mentioning
comments in the last 100, **17 carry `@pmcp` only inside the mandatory provenance disclaimer**
— exactly the long reports being complained about. An @mention gate would have waved the
offenders through and constrained only the dozen that already used a standalone address.

**Why these limits:** across 93 agent comments the visible part runs 0 · 114 · 330 · 591 ·
25497 chars and 0 · 1 · 3 · 6 · 217 lines. The median is already 330 chars / 3 lines; 700c/10L
refuses the walls, not the norm. The line limit reuses the ~10 lines `ask-human` already
states rather than inventing a second number.

## Relationship to `ask-human`

`ask-human` covers the **blocking** subset (🔀 / 🛠 / 👀) in depth: the `Needs:` line, the
recommendation-first rule, the medium-selection table, `status:blocked`, push-before-you-block.
This skill is the wrapper that makes **every** comment — including the non-blocking 🔴 / 💡 / ✅
— arrive in the same scannable shape. When the brief is a hold, use `ask-human`'s template
inside it.
