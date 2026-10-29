---
name: engram-frame
description: ORCHESTRATOR-run skill — the main session conducts this interactive guided interview with the owner BEFORE starting an engram-factory job; a child agent cannot hold the owner channel. Option-based questions (pick a letter or freeform), MoSCoW prioritization, strike-lists over blank-page questions. Captures problem, outcome measures, non-goals, and a decision ledger with explicit authority. Trigger on any wish that is not yet a spec ("I want X", "make X better", "fix X"), or before /engram-factory when intent, outcome, or decision authority is unclear.
---

# engram-frame

Turn a wish into a brief the factory can run on. YOU are the orchestrator
holding this skill — no child agent has the owner channel. You interview the
owner (a Product Engineer, technical or functional), capture intent, never
design. The brief is the human-to-factory contract: everything the analyzer
would otherwise guess.

The failure this skill exists to prevent: a factory job where consequential
choices are decided downstream with no recorded human decision, discovered by
the human only at the approval gate.

## Contract

1. Capture intent, not design — no solutioning in the brief.
2. **The brief is functional**: what the system must do, for whom, and why it
   matters — language a functional reader can verify. Implementation belongs
   to analysis and plan, even for technical owners.
3. The owner speaks in quotes; decisions are `[HUMAN-DECIDED]` only with an
   explicit selection or verbatim statement. Silence is never consent.
4. Every consequential choice lands in the decision ledger: decided by the
   human, or explicitly delegated with a boundary and a revisit trigger.
5. The ask is the owner's words, verbatim, any length.
6. Stop interviewing when a different answer would no longer change what
   analysis does.

## Question format (use everywhere)

Every question is easy to answer:

```
<short stem> — A) <option>  B) <option>  C) <option>  D) freeform
```

- Options are grounded in repo context and prior answers, never generic
  filler. **Options describe behavior and outcomes, not mechanisms.**
- **Translate-and-confirm technical answers**: when the owner answers with a
  mechanism ("add a queue"), restate the functional intent and confirm: "the
  behavior you want is X — is the mechanism fixed, or a suggestion?" Fixed →
  owner-fixed constraint; suggestion → non-binding suggestions.
- One-word answers are valid: "B", "B but capped at 500", "none — …".
- You may recommend: "I'd pick B because <reason> — pick or correct." Disclose
  the assumption behind any consequential option ("option A assumes <X> —
  correct me if not"), and record the owner's REJECTION verbatim — a refusal
  is intent, not noise.
- Never exceed four substantive questions per round ("anything else?" is a
  transition, not a question). Caps: two rounds per area, eight rounds total;
  past a cap the request is not ready — say so and stop.

## Workflow

### 1. Classify the ambiguity

Fast path when the request names a problem, a checkable outcome, a boundary,
and its decision owner. Full path when any is missing — signals: "better /
faster / modernize / fix", no measurable outcome, unknown boundary, unidentified decisions.

### 2. Fast path — one confirm-and-ratify turn

Restate problem and outcome in one sentence each; ask the owner to confirm
(zero clarifiers is valid). If a named ambiguity would change analysis, ask
it in the question format — at most two. The owner's confirmation of the
restatement doubles as the whole-brief ratification — one turn, no extra
ceremony. Fill the ledger, write the brief, done.

### 3. Full path — interactive interview

One area per round, in this order; ≤ 4 option-based questions per round;
each area closes with "anything else?" and moves on. Hesitation on any
choice → park it `[OPEN]` immediately; never push a third time.

1. **Problem** — offer candidate framings from context:
   "Which hurts most? A) … B) … C) several — rank them."
2. **Outcome** — offer candidate measures:
   "How do we know it worked? A) <metric> B) <signal> C) owner-judged pass/fail
   (tell me the signal) D) freeform."
3. **Scope by MoSCoW** — propose the buckets, owner edits:
   ```
   Must:    <items>      Should:  <items>
   Could:   <items>      Won't:   <items>
   ```
   "Keep as-is, or move items / strike lines." Must → outcome core;
   Should → in scope; Could → follow-ups; Won't → non-goals. One round, no
   item-by-item interrogation.
4. **Boundaries by strike-list** — never blank-page. Propose what you believe
   is OUT (from repo context): "Strike any that should stay IN; add what's
   missing." Same for constraints: propose the known standards, owner edits.
5. **Decisions as tradeoff pairs** — each consequential choice as a
   functional either/or, the tradeoff stated in behavior terms:
   "A) <reversible behavior> B) <faster but riskier behavior>
   C) delegate to analysis within <boundary> D) leave OPEN."
   The owner's pick — including C or D — is the ledger row. **C and D require
   an explicit selection**: never record DELEGATED because the owner hesitated
   or because you judged the choice mechanical. Without a pick: OPEN, which
   blocks analysis.

### 4. Write the brief

Fill the factory brief template
(`.agents/skills/engram-factory/assets/templates/brief.md`). The ask is the
owner's words verbatim, any length. Ledger rows record the selection
("owner picked B: <option text>") or the verbatim freeform, each traceable
to a retrievable owner message (channel + reference). Capture the owner's
ratification of the whole brief verbatim (actor, channel, message reference,
date) — the approval gate displays it back to the human as the forgery
control.

### 5. Hand off to the factory

Fail-closed provenance gate: every HUMAN-DECIDED row and the ratification
resolve to retained owner messages (quote, retrievable reference, option
context); the owner ratifies the finished brief whole — a fast-path
confirmation covers the complete brief. Missing evidence or material OPEN
rows = not ready; stop.

The brief's ask becomes the feature file. Give the orchestrator both paths:
`factory.py create --feature-file <ask> --brief-file <brief>`. The controller
registers the brief as an immutable, REQUIRED analysis input; analysis honors
its ledger. The interview is over; the factory asks questions now, not you.

## When it fails

- Owner unavailable → tag open decisions `[BLOCKED: owner needed]` and stop.
- Two owners disagree → record both verbatim under one open decision; never average.
- No checkable outcome and no owner signal → outcome stays OPEN; the brief is
  NOT factory-ready. Request changes mid-interview → restart that area only.
- More rounds than the caps allow → not ready; stop.

## Anti-patterns

- Blank-page questions ("what do you want?") — always offer grounded options.
- Solutioning in the brief — including an owner's own mechanism recorded as
  intent instead of translated to behavior or parked as a suggestion.
- Owner-fixed constraints without an external source — internal preferences
  are suggestions or delegations, never constraints.
- Recording DELEGATED on hesitation, or downgrading an OPEN row without a
  verbatim owner-approved deferral in the row.
- A technical owner turning the brief into a design doc: if a statement names
  how instead of what, it does not belong here.
- Interrogation drift: more than four questions a round, or a third push on a
  parked choice.
- Shortening or paraphrasing the ask — quoted owner text is never compressed.
- Inventing outcome measures, selections, or ratification quotes.
- Marking `[DELEGATED]` without a boundary and revisit trigger.
- Converting an `[OPEN]` row into a decision to make the brief look complete.

## Final check

- Did every question offer options or freeform — no blank-page prompts?
- Is every statement functional — behavior, outcome, boundary — with
  mechanisms only as owner-fixed constraints or parked suggestions?
- Does every ledger row carry real authority — a recorded pick/quote, or an
  explicit delegation with a boundary?
- Could the analyzer start tomorrow morning without guessing at intent?
- Is the ask still the owner's words, not yours?
