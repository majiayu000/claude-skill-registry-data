---
name: explain
description: >-
  Explain a plan, a shape, a shipped change, code, or the last message so it's impossible to misunderstand —
  an ASCII drawing of how it works, then plain words, facts kept verbatim. Like SQL's EXPLAIN for a
  query plan. Use when someone says "explain simply", "use ascii to explain", "explain the
  plan to me", "that didn't land", "too dense", "I don't get it", "walk me through what we shipped",
  or needs to understand and defend a system to their team.
---

# Explain

SQL's `EXPLAIN` shows how a query will actually run. This does the same for work: how the thing actually runs, drawn and said so plainly it can't be misread. The goal is that the developer can stand at a whiteboard and explain it — and defend it — without line-level knowledge.

## What to explain

- **`/explain` with no argument, or "that didn't land" / "too dense" / "I don't get it"** → your most recent assistant message. Re-explain it only: no tools, no new information, no answering a new question. If there's no previous message, say there's nothing to explain yet.
- **A file** (`thoughts/shapes/…`, `thoughts/plans/…`) → read it and explain what it will build and how.
- **A shipped change** (branch, PR, "what we just built") → read the diff, the touched code, and the git log. Plans go stale, so explain what the code does now; where it differs from the plan, say so.
- **Anything else** (a module, a flow, an error, a concept) → read what's needed and explain it the same way. The four questions below apply only if it's customer-facing.

## How

**1. Draw it first.** Open with an ASCII drawing of the mechanism — boxes and arrows showing how data and control move: in through I/O, through the logic (Function), into and out of storage (State). Reuse the plan's layer map when there is one. Keep it under ~20 lines. Label arrows with what travels on them.

```
 browser ──POST /invoices/sync──► API ──► syncInvoices() ──► Stripe
                                              │
                                              ▼ upsert by stripe id
                                        invoices table ──► GET /invoices ──► Billing page
```

**2. Then say it plainly.** Talk like you're explaining it to a smart friend over a beer.
- Simple words, short sentences. A technical term stays only if it's the real name of something; gloss it in a clause the first time.
- No childish analogies — no lemonade stands or toy trains. Just the thing itself, said simply.
- Casual and direct: "ok so…", "basically…", "the point is…". A bit of personality is fine; it's not a meme.
- Simpler isn't shorter. Take the space clarity needs; cut preamble, hedging, and consultant-speak.
- Flatten structure: no headers, no tables. Sentences, and a short list only when there really are separate parts.

**3. Keep facts verbatim.** Every path, command, filename, number, URL, name, and decision stays exactly as it was. Simplify the explanation around the facts, never the facts.

**4. Customer-facing work: the four questions.** When the target reaches customers (shape `Stakes: customer-facing`, a plan with a Whiteboard Defense section, or a shipped change on a user-facing path), finish with the four things a lead will ask — same plain voice:
- **Why this and not the other way?** The decisions that matter and what was passed over.
- **What if someone's trying to break it?** A malicious or misbehaving actor, and what stops them.
- **What does the data look like, and why that shape?**
- **Where does it fail?** What breaks, what the user sees, how anyone would notice.

Answer from the artifact and the code. If the answer isn't there, say so plainly — "the plan never says what happens when Stripe is down" — instead of inventing one. Those gaps are the most useful part.

## Output

```
[ASCII drawing]

[plain-words explanation]

[customer-facing only: the four questions, answered or flagged as gaps]
```

No signature block, no summary of the summary.

## Handoffs

- Gaps found in a plan → `/dev-skills:write-plan` to close them before executing.
- Want to present it to the team → `/tap-skills:render-doc` then `/tap-skills:dossier-publish`.
