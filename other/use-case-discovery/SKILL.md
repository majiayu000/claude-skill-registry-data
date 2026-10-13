---
name: use-case-discovery
description: >
  Runs FlashFusion AI use-case discovery workshops with enterprise clients to
  produce a ranked, scored backlog of automation and AI opportunities. Use when
  facilitating a discovery call, running an AI ideation or strategy workshop,
  assessing a department for automation candidates, scoring a list of use cases,
  estimating ROI for AI initiatives, or building a prioritized AI backlog.
  Triggers on: use case workshop, AI opportunities, discovery session, discovery
  call, automation candidates, AI strategy session, feasibility scoring, impact
  estimation, WSJF, prioritize AI initiatives, AI opportunity assessment, where
  should we use AI, what can we automate, AI backlog.
allowed-tools: Read, Write
license: MIT
metadata:
  version: "2.0.0"
  track: flashfusion
  type: procedure
---

# Use Case Discovery

FlashFusion consultant-led workshop that turns a client's pain points into a
ranked backlog of 10–15 AI/automation use cases — each scored for feasibility,
estimated for impact, and prioritized by WSJF. You run this as the facilitator:
collect, score, estimate, rank, hand back a defensible backlog.

## Evals

**Should trigger:**
1. "We're meeting the ops team at Northwind next week to figure out where AI could help — can you help me run the session?"
2. "I've got a list of 12 things the service desk wants to automate. Help me rank them so we know what to build first."
3. "Run an AI opportunity assessment for a 40-person finance department."

**Should NOT trigger:**
1. "Write the proposal and statement of work for the Northwind engagement." → that's `scoping-ai-engagements` (proposal/PRD/phase plan), not discovery.
2. "Build the ticket-to-article KB automation we scoped." → that's `building-kb-pipelines` (implementation of one chosen use case), not opportunity discovery.

## Decision Tree

```
What does the client have?
  ├─ Nothing yet — "where could we use AI?" ──────── FULL WORKSHOP. Run all 5 steps (intake → ranked backlog).
  ├─ A vague pain area / one department ──────────── SCOPED WORKSHOP. Run steps 1–5 bounded to that department.
  ├─ An existing list of candidate use cases ─────── SCORE-ONLY. Skip step 2 collection; start at step 3 (feasibility) on their list.
  └─ One specific use case they've already chosen ── EXIT. They're past discovery → hand to scoping-ai-engagements.
```

If you cannot tell which: ask **"Are we discovering opportunities from scratch, or ranking a list you already have?"**

## Intake (Step 1)

Collect these before scoring anything. Do not proceed on blanks — ask.

| Field | Why it matters |
|---|---|
| Client / org name | Labels the backlog; sets tone |
| Industry / vertical | Calibrates feasibility (regulated data lowers data-availability scores) |
| Team / department size | Scales the hours-saved math |
| Top pain point (the one that triggered this) | Anchors the session; becomes use case #1 candidate |
| Workshop scope | Whole org, one department, or score-only |
| Data environment (optional) | Where the data lives, sensitivity, access — feeds feasibility |

Capture verbatim. The "top pain point" is the thread you pull — most other use cases surface as adjacent friction.

## Golden Path

1. **Intake** — collect the table above. Confirm scope via the decision tree.
2. **Pain Point Collection** — elicit 12–20 raw pains. Prompt by category: manual/repetitive work, slow handoffs, error-prone steps, knowledge that lives in one person's head, things that don't scale. One line each: *who* hits it, *how often*, *what it blocks*. Deduplicate into distinct candidate use cases.
3. **Feasibility Scoring** — score each candidate 1–5 on three axes (rubric below). Compute a feasibility composite.
4. **Impact Estimation** — for each candidate, estimate hours/week recovered and a revenue/cost delta (rubric below).
5. **WSJF Prioritization** — compute WSJF per candidate, sort descending, trim to the top 10–15. Produce the backlog in the output schema.

## Feasibility Scoring (Step 3)

Score each use case 1–5 on each axis. **5 is always the most favorable.**

| Axis | 1 (worst) | 3 | 5 (best) |
|---|---|---|---|
| **Data availability** | Data doesn't exist / inaccessible / highly sensitive with no clearance | Exists but messy, partial, or needs cleanup | Clean, accessible, already structured |
| **Implementation complexity** | Multi-system, custom integration, new infra | Moderate — one integration, known pattern | Off-the-shelf / prompt-level / single tool |
| **Stakeholder readiness** | No sponsor, change-resistant, no time | Interested but unproven, needs convincing | Named sponsor, eager, willing to pilot |

**Feasibility composite** = average of the three axes (1.0–5.0). Anything scoring **data availability ≤ 2** is flagged `DATA-BLOCKED` and noted regardless of impact — it cannot start until data is sorted.

## Impact Estimation (Step 4)

For each use case estimate two things. Show your assumptions inline.

- **Hours/week recovered** = (people affected) × (times performed/week) × (minutes each ÷ 60) × (automatable fraction). State each factor.
- **Revenue/cost delta** = annualized money effect. Pick the dominant lever and label it:
  - *Cost-out*: hours/week × 52 × loaded hourly rate → annual labor recovered. `[FILL: client loaded hourly rate]` if unknown.
  - *Revenue-enabling*: faster cycle time → throughput or conversion lift. Estimate conservatively; label `[GENERATED]`.
  - *Risk/error reduction*: cost of current error rate × reduction. Use only if the client can quantify the error cost.

Never invent precise dollar figures. If an input is missing, insert `[FILL: …]` and carry the use case with hours-only impact.

## WSJF Prioritization (Step 5)

Cost of Delay over Job Size — consistent with `scoping-ai-engagements`.

```
WSJF = (Impact Value + Time Criticality + Risk Reduction) / Job Size
```

- **Impact Value** — map the impact estimate to Fibonacci 1-2-3-5-8-13-20 (bigger hours/$ → higher).
- **Time Criticality** — Fibonacci. How much does delaying erode the value? (seasonal, contractual, competitive).
- **Risk Reduction** — Fibonacci. Does it de-risk compliance, key-person dependency, or error exposure?
- **Job Size** — Fibonacci, derived from feasibility: Job Size ≈ `6 − round(feasibility composite)` (high feasibility → small job). Floor at 1.

Sort descending. Trim to top 10–15. Anything WSJF **< 2.0** drops to a "parking lot" note, not the backlog.

## Output Schema

Return a single document with these named sections:

1. **Header** — Client, industry, team size, workshop scope, date, facilitator.
2. **Discovery Summary** — 2–3 sentences: the top pain point and the headline opportunity.
3. **Ranked Backlog** — a table, sorted by WSJF descending, 10–15 rows. Required columns:

   | # | Use Case | Pain Addressed | Feasibility (avg) | Hours/wk | Revenue/Cost Δ | WSJF | Flags |
   |---|---|---|---|---|---|---|---|

   `Flags` carries `DATA-BLOCKED`, `[FILL: …]`, or `parking-lot`. Each $ figure labeled `[SOURCED]` or `[GENERATED]`.
4. **Top 3 Recommendations** — for the highest-WSJF items: one paragraph each on why it's first, what's needed to start, and the obvious quick win.
5. **Parking Lot** — use cases scored but below the WSJF cut, with the one-line reason.
6. **Open Data Needs** — every `[FILL: …]` collected in one list so the client knows exactly what to provide.

Optional fields (include when known): per-use-case sponsor name, target start phase, dependency on another use case.

## Self-Verification Checklist

Before returning the backlog:
1. Every use case scored on all three feasibility axes (no blanks).
2. Every use case has hours/week AND a revenue/cost line (or an explicit `[FILL: …]`).
3. Every WSJF has all four inputs shown — no bare final numbers.
4. Backlog is sorted by WSJF descending and trimmed to 10–15.
5. Every dollar figure labeled `[SOURCED]` or `[GENERATED]`.
6. `DATA-BLOCKED` flag applied wherever data availability ≤ 2.
7. Open Data Needs lists every `[FILL: …]` in the document.
8. No invented client facts, rates, or benchmarks presented as known.

## CLAIMS

- WSJF (Cost of Delay ÷ Job Size, Fibonacci) is an established SAFe prioritization method. [SOURCED — Scaled Agile Framework]
- The 1–5 three-axis feasibility rubric (data / complexity / readiness) is a FlashFusion convention defined in this skill. [GENERATED]
- Deriving Job Size from the feasibility composite (`6 − round(composite)`) is a convenience mapping defined here, not an external standard. [GENERATED]

## COUNTEREXAMPLE

- Do NOT use for scoping/proposing a chosen engagement (→ `scoping-ai-engagements`) or implementing one use case (→ `building-kb-pipelines`).
- A high-WSJF use case that is `DATA-BLOCKED` should not be recommended as "start now" — sequence the data work first.

## CONTRADICTIONS

- ! Impact Estimation wants precise ROI, but the no-fabrication rule forbids inventing rates — resolve by carrying `[FILL: …]` and reporting hours-only until the client supplies the figure.
