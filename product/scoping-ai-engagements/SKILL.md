---
name: scoping-ai-engagements
description: >
  Scopes, proposes, and phases AI enablement engagements for FlashFusion client
  organizations. Use when running a discovery conversation, writing a client
  PRD, scoring a WSJF backlog, building a domain-unlock or capability rollout,
  drafting a stakeholder brief, or turning discovery answers into a phased plan.
  Triggers on: AI enablement engagement, client PRD, WSJF backlog, domain unlock,
  rollout proposal, stakeholder 1-pager, leadership brief, AI adoption roadmap,
  make the case, get buy-in, FlashFusion engagement, enablement scope, phase
  plan, discovery conversation, scope this engagement.
license: MIT
allowed-tools: Read, Write
compatible-with: claude-code, codex, openclaw
metadata:
  version: "2.0.0"
  track: flashfusion
  type: procedure
---

# Scoping AI Engagements

FlashFusion methodology for scoping, proposing, and phasing AI enablement at
client organizations. Run a structured discovery conversation, score initiatives
with WSJF, and translate the answers into a phased plan with gates, kill
criteria, and measurable outcomes — targeted at one reader who can say yes.

## Evals

**Should trigger:**
1. "A client wants an AI adoption roadmap. Walk me through the discovery and write the proposal."
2. "Help me score these five AI initiatives with WSJF and turn the top two into a phased rollout."
3. "Draft a one-pager for the VP of Ops making the case for the support-automation initiative."

**Should NOT trigger:**
1. "Where could this client use AI? Help me run the opportunity workshop." → that's `use-case-discovery` (find + rank raw opportunities); this skill scopes a chosen direction into a proposal.
2. "Pull our internal AI platform adoption numbers." → that's `analyzing-loxihart-platform-data`.
3. "Now build the thing." → technical implementation, hand to `enabling-ai-solutions`.

## Principles (keep)

1. **Audit before proposal.** Benchmark Zero first — current state, cost, who is affected. Never propose on an unknown baseline.
2. **One reader per brief.** Every deliverable targets one stakeholder, one ask.
3. **WSJF before roadmap.** No initiative enters a plan without a score.
4. **Phase gates required.** Written kill criterion per phase.
5. **Measurable outcomes only.** ≥ 1 concrete metric per initiative.
6. **No placeholders.** Ask for missing data; mark `[FILL: …]` rather than invent.

## Decision Tree — pick the deliverable, then route

```
What does the client need?
  ├─ Brief for one exec ─────────── templates/stakeholder-1pager.md
  ├─ Full initiative proposal ───── templates/prd.md
  ├─ Prioritize an initiative list ─ workflows/wsjf-scoring.md
  ├─ Phase a capability rollout ──── workflows/rollout-plan.md
  └─ Don't know the reader yet ───── ASK: "Who is the primary reader, and what
                                      action do you need from them?"  Then route.
```

Stakeholder framing per archetype: `references/stakeholder-archetypes.md`.

## Discovery Conversation — question order

Run these in order. Each answer feeds a later step; don't skip ahead. Capture
verbatim. Where the client can't answer, mark `[FILL: …]` and keep going.

1. **Baseline (Benchmark Zero):** "How is this handled today, start to finish? How long does it take and how often?" → establishes current state and cost.
2. **Who is affected:** "Who does this work, and who feels it when it's slow or wrong?" → identifies the reader/sponsor and the people the change touches.
3. **Pain & cost:** "What does the status quo cost — in hours, errors, money, or risk?" → the case for change.
4. **Desired outcome:** "If this worked perfectly in 90 days, what's different, and how would you measure it?" → the measurable outcome (one concrete metric).
5. **Constraints:** "What can't move — data access, compliance, budget, timeline, tools?" → bounds feasibility and phase length.
6. **Readiness & sponsor:** "Who owns the yes? Who will pilot it? How much change appetite is there?" → confirms there's a sponsor before you propose.

Stop and confirm the **reader** and the **one ask** before writing anything.

## Golden Path — discovery answers → phased plan

1. **Run the discovery conversation** (six questions above). Record answers.
2. **Name the initiative(s)** — short, outcome-oriented (e.g., "Tier-1 Ticket Auto-Triage"), not tool names.
3. **Score each with WSJF** — `(Business Value + Time Criticality + Risk Reduction) / Job Size`, Fibonacci 1-2-3-5-8-13-20. Archive anything < 2.0. Detail: `workflows/wsjf-scoring.md`.
4. **Set the measurable outcome** — pull the metric from discovery Q4. One concrete number with a baseline and a target.
5. **Phase the rollout** — break the top initiative(s) into gated phases. Each phase gets an entry gate, a written kill criterion, and what it proves. Pattern: `workflows/rollout-plan.md`.
6. **Write to one reader** — frame for the chosen archetype (`references/stakeholder-archetypes.md`), pick the deliverable from the decision tree, assemble the schema below.

## Phase Plan — required fields

Every phased plan MUST contain, per initiative:

- **Initiative name** — outcome-oriented, one line.
- **WSJF score** — the four inputs shown, not just the quotient.
- **Measurable outcome** — one metric, with baseline → target and the measurement window.
- **Phases** — a table. Each phase row requires:

  | Phase | Goal (what it proves) | Entry gate | Kill criterion | Duration |
  |---|---|---|---|---|

  A phase with no written kill criterion is not done — go back and write one.

## Output Schema

Deliver one document, framed for the single reader:

1. **Header** — client, initiative name(s), reader/archetype, the one ask, date.
2. **Benchmark Zero** — current-state cost and who's affected. Figures `[SOURCED]`/`[GENERATED]`.
3. **The Case** — 2–3 sentences in the reader's frame (revenue / hours / triage / toil per archetype).
4. **WSJF** — table of initiatives with all four inputs and the score, sorted descending.
5. **Phase Plan** — the required-fields table above for the top initiative(s).
6. **Measurable Outcomes** — the metric(s), baseline → target, window.
7. **Open Items** — every `[FILL: …]` in one list.

## Self-Verification Checklist

Before returning:
1. Benchmark Zero present — no proposal on an unknown baseline (Principle 1).
2. Exactly one reader and one ask identified (Principle 2).
3. Every initiative has a WSJF score with all four inputs shown (Principle 3).
4. Every gated phase has a written kill criterion (Principle 4).
5. Every initiative has ≥ 1 concrete measurable outcome with baseline + target (Principle 5).
6. No invented client facts or figures; gaps carry `[FILL: …]` (Principle 6).
7. Deliverable matches the archetype framing for the chosen reader.
8. SKILL.md routed to template/workflow files rather than restating them in full.

## CLAIMS

- WSJF `(BV + TC + RR) / Job Size` on a Fibonacci scale is an established SAFe method; the < 2.0 archive cutoff is a FlashFusion convention. [SOURCED — SAFe; GENERATED — cutoff]
- The six-question discovery order is a FlashFusion convention defined in this skill. [GENERATED]
- Stakeholder archetype framings (CEO/VP Ops/IT Manager/Eng lead) are carried from the original skill. [SOURCED — prior skill version]

## COUNTEREXAMPLE

- Do NOT use to discover/rank raw opportunities (→ `use-case-discovery`) or to build the solution (→ `enabling-ai-solutions`).
- A roadmap with no per-phase kill criterion violates Principle 4 even if every initiative is WSJF-scored.

## CONTRADICTIONS

- ! "Measurable outcomes only" vs. early discovery where the client can't yet quantify the metric — resolve by capturing `[FILL: baseline metric]` and treating quantification as a Phase 0 deliverable, not a reason to ship an unmeasurable plan.
