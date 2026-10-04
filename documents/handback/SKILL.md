---
name: handback
category: orchestration
description: |
  Terminal-message contract for an autonomous arc that has run out of
  agent-executable work and genuinely needs a human. Produces a WORK ORDER —
  asks first, each one an imperative addressed to the reader, carrying a default
  so silence is never fatal (the exception is narrow and must be named:
  irreversible, externally visible, or spends money) — followed by the unchanged
  nine-item receipt. Distinct from `handoff` (same arc, different reader: `handoff`
  writes `docs/handoffs/` for the NEXT AGENT; `handback` writes the chat
  message for the HUMAN AS DECISION-MAKER).
  Asking is the last resort, not the interface: no ask may exist until the
  seven-rung autonomy ladder has been climbed and recorded.
  Use when: (1) an autonomous arc is stopping and at least one ask is open,
  (2) the user asks "what do you need from me" / "what's blocking",
  (3) a lane has parked on a human dependency and the arc is notifying,
  (4) writing any message whose purpose is to obtain a decision.
  Triggers on "handback", "hand back", "what do you need from me", "what is
  blocking", "blocked on you", "what should I decide", "unblock", "your call".
---

# handback — end an arc with a work order, not a lab notebook

**Spec:** `broomva/workspace` → `docs/specs/2026-08-18-agent-handback-contract.html` (BRO-2179).

## Why this skill exists

Measured over 994 Claude Code transcripts (analysis set: 100 sessions of ≥6h
wall-clock and ≥150 assistant turns):

| | |
|---|---|
| Long arcs whose final message mentions a blocker at all | 31 / 100 |
| Long arcs **halting on a human** (terminal-stance phrasing) | **18 / 100** |
| …of those 18, containing a conforming ask block | **0 / 18** |
| …containing an imperative anywhere in the message | 3 / 18 |
| …containing any `?` at all | 13% |
| …with the question next to the blocker it describes | 6% |
| Stating a default if the human stays silent | 5% of all 100 |
| Ever emitting a push notification | **0 / 100** |
| Blockers knowable before the arc started | **81%** |

The two blocker rows differ on purpose. The broad count (31) includes messages
that merely *mention* being blocked — "the pre-commit hook blocked it", "#381
remains blocked by the hang". The narrow count (18) is the defensible one: a
terminal message that stops the arc **on a person**. The enforcement gate keys on
the narrow definition, because refusing a healthy receipt that happens to contain
the word "blocked" would fight the operator.

The ask usually exists. It is placed last, written in the indicative ("Not
merged — auto-merge correctly blocked"), and carries no default, so the arc
dies on it — median 2.4h of stalled arc-time behind such a message, 25 of them
overnight-length.

## Rule zero — asking is the last resort, not the interface

**No ask may exist until every rung below has been tried and recorded.** A row
with an empty `exhausted` list is a defect, not a question.

| Rung | Try this | |
|---|---|---|
| 1 · Read | Is the answer already on disk — ticket history, prior conversations, the knowledge graph, the handoff doc, the code? | Most "decisions" are recoverable, not new |
| 2 · Standing grant | Has this exact question been answered before? Check `.control/preauth.yaml` | Re-asking a settled question is the cheapest failure to eliminate |
| 3 · Delegate | Can a fresh agent resolve it — a reader, a researcher, an adversarial reviewer with different context? | Chain agents instead of chaining to the human |
| 4 · Reroute | Can another lane, worktree, fan-out, or approach go around it? | The blocker is often a path, not a wall |
| 5 · Loop | Can iteration resolve it — retry under a changed assumption, let a persist loop converge? | Slow beats blocked when nobody is awake |
| 6 · Default | Is the choice reversible? **Take it, log it, tell the human afterwards. Do not ask.** — "log it" means an entry in the ledger's `decisions:`, and "tell the human" means the 🔀 block below | Reversible decisions are not the human's to make in real time |
| 7 · Ask | Only now. Record which rungs were tried and why each failed. | |

**Rung 6 is where most asks should die.** A choice that can be undone with one
commit does not warrant stopping an arc; it warrants a line in the receipt.
Only actions that are **irreversible**, **externally visible**, or **spend
money** may reach rung 7 without a default — and the ask must say which.

## Rule minus-one — never stop the arc while an unblocked lane remains

Blocked is a **lane** state, not an **arc** state. When an ask fires: park the
lanes it gates, emit the ask (push it if outside the waking window), and
continue on the next unblocked lane. Run `handback` only when the unblocked set
is empty. An arc that halts with runnable work left is the failure this skill
exists to prevent.

## The shape — six blocks, always in this order

*"Always in this order" constrains **order**, never presence.* A block with no
content is omitted, not rendered empty — an empty 🔀 block would assert that
nothing was decided, and an empty ⛔ block would assert that nothing is blocked.
Only the receipt is unconditional.

```
## ⛔ Blocked on you — N items, ~M min
   table: # | ask (imperative, addressed to "you") | unblocks | if you say nothing
   a decision row lists options A/B/C, one marked suggested, each with its cost
   plain language only; hard cap 7 rows, ranked by what each unblocks

## ▶ Running meanwhile
   what is still executing, or what ran with zero input from you

## ✅ Shipped
   PR table. One line each. No narrative.

## 🔀 Decided for you — N choices, least-confident first
   table: # | what I decided | why it was mine to take | undo
   rendered from the ledger's `decisions:` list, never free prose
   every row carries its one-line reversal — that is what made it safe not to ask
   hard cap 7, same as the ask block; overflow counted in the header

## 📋 Receipt — the nine items, unchanged
   1 dep chain · 2 plan vs done · 3 parallel streams · 4 files changed · 5 PRs
   6 deploys · 7 validation · 8 merge result · 9 follow-ups

## 📎 Detail → docs/handoffs/<arc>.md
   the NARRATIVE lives there: what happened and why, the review sagas, the
   corrections. That prose is what this contract displaces.
```

## The ten rules

Each is derived from a measured failure, not a style preference.

1. **The ask block is first.** Not a "Your call" section at 80% depth.
   *Measured: the ask lands around p80 of the message.*
2. **Every row is an imperative addressed to "you"** — a command to run, a link
   to click, a value to paste, or a one-line answer to a closed question.
   *Measured: 0 of the 18 halting messages contained a conforming ask block.*
3. **A decision row offers options, not an open question.** Two or three
   concrete choices, each with its consequence in one line, one marked as the
   recommendation. Never "what should we do about X?" — always "A, B, or C; I
   suggest B because …".
4. **Plain language, no internal vocabulary.** No primitive numbers, no gate
   names, no acronyms, no ticket ID standing in for the question. If a term
   needs the spec to understand, it does not belong in an ask.
5. **Every row carries a default.** "If you say nothing, I do X." A row with no
   safe default must say so explicitly and name what it costs.
   *Measured: 5% stated a default. Silence is otherwise fatal.*
6. **Every row is self-contained.** Answerable without opening a ticket. The
   ticket ID is a reference for later, never the carrier of the question.
   *Measured: 58% used a ticket as the carrier; median 1 ticket, up to 13.*
7. **Rows are ranked by what they unblock**, stated in the row — "unblocks 9 of
   18 rows", "unblocks 1 lane". A tired person answering one thing should be
   answering the right one.
8. **Hard cap: 7 rows.** More than seven means the arc should have asked
   earlier. Overflow goes to the ledger, with the total stated in the header
   ("3 of 11 shown").
9. **The nine-item receipt stays, underneath the asks.** It is structured and
   proves the work. What this contract displaces is the **free-form narrative**
   — that moves to `docs/handoffs/`.
10. **The ask block ends with the reply already drafted — one line per row,
   numbered to match.** A copy-pasteable
   skeleton, one line per row, recommendation pre-filled — so answering is an
   *edit*, not a composition. Rules 2–6 fix what a row **says**; none of them
   lowers the cost of **replying**, and a perfectly-formed ask still stalls if
   answering it means composing prose at 1am. Reacting beats imagining: hand
   the reader something to strike through, not a blank box. The skeleton is
   generated *from the rows*: if it has four lines and the table has five, the
   fifth ask is one the reader is never prompted to answer — a silent drop
   dressed as a convenience.

## The 🔀 block — what rung 6 owes the human

Rung 6 is where most asks are supposed to die: *take the reversible default, log
it, tell the human afterwards.* For as long as this contract defined five blocks,
there was nowhere for that last clause to land — the ladder told the arc to decide
and say so, and the message shape had no room for it. Every silent-but-correct
decision therefore looked identical to no decision at all, while the user still
inherited it.

The 🔀 block is that room. It is **not** an ask block: nothing in it is a
question, and the arc did not wait for any of it.

| Property | Why |
|---|---|
| Rendered by `ask_ledger.py decisions --render-handback`, not written free-hand | The rules below — ordering, the undo, the cap, the overflow header — are executable there and tested. Stated only in prose they are four things an agent forgets one at a time |
| An **irreversible** choice may not appear here as a settled default | Rung 6 licenses reversible choices only. Recording an irreversible one is still right, but the schema forces it to carry `verdict: needs-user` and name the ask that took it to the human |
| A `needs-user` row is **excluded** from this block | It reached the human, so it belongs in ⛔ keyed by its `ask`. Rendering it in both would print one item twice under contradictory headings — "decided for you" and "blocked on you" — which this workspace's own arc ledger did before the renderer excluded them |
| **Least-confident first** | Confidence ranks; verdict groups. The reader's attention is finite and should land on the choice most likely to be wrong, not the one that happened to be made first |
| Every row shows its **undo** | The reversal is the entire justification for not having asked. A row that cannot state one is a row that should have been an ask |
| Hard cap 7, overflow counted | Same discipline as the ask block. More than seven means the plan was foggy — the clustering *is* the signal, and the fix is upstream in the spec, not a longer table |

**Where each verdict surfaces**, so nothing is duplicated and nothing is dropped:

| Verdict | Block | Why |
|---|---|---|
| `sound` | 🔀 | Decided and settled. The user owns it now |
| `unsound` | 🔀, with its corrected decision | Decided, and known to need redoing |
| `needs-user` | **⛔ only**, via its `ask` | It was not decided for them — it was asked |

Consequence worth stating plainly: because the schema forces an irreversible
choice to be `needs-user`, no valid ledger can render one in 🔀 at all. The
renderer keeps a defensive branch for a ledger nobody validated — an empty undo
column would read as "no undo needed", the opposite of the truth — but on a valid
ledger that branch is unreachable.

**`sound` is not skippable.** The temptation is to list only the shaky calls, but
a confident decision the user never made is still architecture the user now owns.
Trivial discretion — internal naming, cosmetic calls — compresses to a one-line
count; everything load-bearing gets a row.

## Anti-patterns

| Rationalization | Why it fails |
|---|---|
| "I'll describe the blocker; they'll know what to do" | A statement about the world transfers no obligation. Zero of 31 measured messages contained a request addressed to a person. |
| "The ticket explains it" | The reader has no context loaded and may be on a phone. The ticket was written by an agent for an agent. |
| "It's a big decision, I shouldn't presume a default" | Defaults are for **reversible** choices, and most are. Reserve no-default for irreversible / externally visible / money-spending. |
| "I'll list everything so they have full context" | Seven rows maximum. More means the ladder was not climbed or the hour-zero batch was skipped. |
| "I'll ask now and keep working after they answer" | Wrong order. Park the gated lanes and keep working *now*; the answer arrives whenever it arrives. |
| "Asking is safer than assuming" | Asking is expensive — median 2.4h of stalled arc-time, 25 overnight stalls in the measured corpus. Rung 6 exists for this. |
| "I'll write the narrative first so they understand the ask" | That ordering is the measured defect. Narrative goes to the handoff doc; the ask goes first. |
| "I took a reversible default, so there is nothing to report" | Rung 6 is a licence to **not ask**, not a licence to **not tell**. The whole clause is "take it, log it, tell the human afterwards." A decision with no record is one the user inherits without ever seeing. |
| "The 🔀 rows are really questions — I'll move them into the ask block" | Then the ladder was not climbed. If it still needs the human it never reached rung 6; if it reached rung 6 it is settled and reversible. Rows do not belong in both. |
| "I'll list only the decisions I'm unsure about" | `sound` is not skippable. A confident call the user never made is still architecture they now own — the point is disclosure, not confession. |
| "They can just tell me what they want in their own words" | That is the blank box rule 10 exists to remove. An answer that requires composing prose costs more than one that requires striking a line through, and the measured stall is hours, not minutes. |

## Composition

- **`handoff`** — same arc, different reader. `handoff` writes
  `docs/handoffs/YYYY-MM-DD-<arc>.md` for the next *agent*; `handback` writes
  the chat message for the *human*. A stopping arc usually produces both, and
  the handback's Detail block links to the handoff.
- **`autonomous`** — supplies the nine-item receipt that block 4 renders, and
  owns the pre-flight that builds the ask ledger.
- **`persist` / `governed-autonomy-loop`** — a parked lane is a lane the next
  iteration's `PROMPT.md` omits; `handback` fires only when none remain.

## References

- `references/template.md` — copy-paste skeleton with a worked example.
