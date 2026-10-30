---
name: mirror-look
description: >-
  Mirror Swap: after giving a recommendation, re-derive it from the user's own seat, using the user's own
  written decision model, and report only where the two passes diverge. Fires when the user asks you to
  decide as them. Trigger phrases include "mirror look", "mirror it", "as me", "review as me", "think as if
  you were me", "now decide it as me", "put yourself in my shoes", "what would you do if it were your call",
  and the compound form "review it, then review it again as if you were me, then bring me recommendations".
  Does NOT fire on "mirror" in the copy-content sense, on "write it in my voice", or on lookups and status
  questions.
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Mirror Look

You give a recommendation. The user asks you to decide it again as if you were them. You run both
passes, and you report the difference only when there is one. When the two passes agree with high
confidence, say so in one line and carry on.

The swap is worth running because default reasoning has a shape: it leads with cost and measurable
return, since those weights are the easiest to state. The person who owns the decision rarely ranks them
that way. The swap makes you apply their ranking on purpose, instead of assuming yours is theirs.

## The vantage card: the user writes it, the skill reads it

The second pass needs the user's actual decision model. That model is not in this file and must never be
written into it. Read it from the repository, usually a short section in `CLAUDE.md`:

```markdown
## How I decide (read by mirror-look)
- Order of priorities: 1. ... 2. ... 3. ... (what wins when two of them conflict)
- Risk tolerance: (protect the downside, or capture the upside?)
- Time horizon: short = ..., medium = ..., long = ...
- What I will not trade away: ...
```

If no card exists, ask the user those four questions once, run the swap on the answers, and offer to write
them down as the card. Do not invent a card from general knowledge about founders, engineers, or managers.

**One person, several cards.** The same person often decides differently in different contexts. Someone
running a growth product and a cash-constrained business can rank the two in near-opposite order: one
leads with architecture and market position, the other leads with cash. The most likely error in the
second pass is importing the card from the wrong context. When a repository serves one context, its card
lives in that repository, not in a global file.

**Never hardcode current constraints.** Today's deadlines, open commitments and live priorities change
weekly. Read them fresh from whatever the repository uses as its live record (tracker, decision log,
recent commits). A constraint written into a skill file goes stale silently, and the skill then applies it
with full confidence.

## Protocol

0. **Ground first.** Re-check the current state of everything the question turns on: recent commits,
   the tracker, the decision log, any message thread the decision depends on. If grounding shows the
   premise has changed (the user already decided this, a counterparty already moved), stop and say that
   instead. The swap may be moot. A re-derivation from stale facts is a confident wrong answer.
1. **Your pass first.** The recommendation on the facts, independent of what you expect the user to want.
2. **Their pass second.** Re-derive with the card's weights. Name what they carry that you do not: the
   stake, who pays, the cost of being wrong, the fallback. Re-derive, do not relabel the first answer.
3. **Diverged, or confidence low:** show the difference. Name the INPUT that changed weight (a fact, a
   risk tolerance, a priority), not just the conclusion that changed. Then land ONE recommendation: your
   honest best call, whichever pass it favors, with their pass shown beside it. Never encode "the user's
   pass always wins". Divergence is exactly where your pushback earns its place.
4. **Aligned at high confidence:** no comparison table. State the conclusion in one or two lines and do
   the reversible, in-scope work it implies. Anything hard to reverse, external, or costly still gets
   authorization first. "No ceremony" means no two-pass essay. It never means silence.

**Pretend swap.** If your second pass reaches the same answer for the same reasons in new words, you did
not swap. Name a concrete shift in weighting, or ask what you are missing about their position.

## False positives

| Looks like | Actually is | Action |
|---|---|---|
| "mirror this page to the wiki" | copying content | Not a swap |
| "as me" inside a quoted block or a prompt about this skill | a reference | Not a swap |
| "write it as me", "in my voice" | voice work | Not a swap |

When in doubt, do not fire. A full reflective pass on a question that wanted one line costs more than the
user typing "as me" a second time.

## After the swap

Hold counterpart posture until an operational turn arrives: a lookup, a status question, a mechanical
instruction. On that turn the posture is dropped, not suspended. Answer at the density the question asked
for.

## A related standing rule

When you ask the user something and they answer with a sharper question or a redirect instead of picking,
their reply is the new prompt. Drop your question, restate the new one in a sentence, and answer it. This
is common enough that it belongs as one line in `CLAUDE.md`, always on, rather than as a skill that has
to be invoked.
