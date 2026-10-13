---
name: okr-engineering-alignment
description: Write engineering OKRs that connect team work to business outcomes, avoid output-vs-outcome confusion, and use DORA and product metrics as key results. Covers OKR fundamentals, why engineering OKRs fail, connecting team OKRs to company OKRs, leading vs. lagging indicators, quarterly cadence, scoring, and common pitfalls.
triggers:
  - "write OKRs"
  - "OKR"
  - "quarterly goals"
  - "engineering goals"
  - "key results"
  - "align team to company goals"
  - "team objectives"
  - "what should we measure"
  - "how do we track progress"
audience:
  - manager
---

# OKR Engineering Alignment

OKRs (Objectives and Key Results) are one of the most misused frameworks in engineering. Used well, they focus a team on meaningful outcomes and connect engineering effort to business value. Used badly, they become a bureaucratic checklist of tasks dressed up as goals.

**The core distinction**: an Objective is inspiring and directional; a Key Result is measurable and verifiable. If your KR can't be scored on a number, it's not a KR — it's a task.

> For writing the strategy that OKRs flow from, use the `technical-strategy` skill.  
> For reviewing team health metrics, use the `engineering-metrics` skill.

---

## OKR Fundamentals

### Objectives
- **Directional and inspiring** — they answer "what are we trying to achieve and why does it matter?"
- **Qualitative** — not a number, a direction
- **Achievable in a quarter** (for team OKRs) or a year (for company OKRs)
- **Connected upward** — every team OKR should trace to a company or department OKR

Good Objective: *"Make our deployment process a competitive advantage, not a bottleneck"*  
Bad Objective: *"Improve CI/CD"* (too vague) | *"Ship the new deploy pipeline"* (a project, not an objective)

### Key Results
- **Measurable** — a number, a percentage, a date with a binary outcome
- **Outcome-oriented** — measures change in the world, not completion of tasks
- **2–4 per Objective** — more dilutes focus
- **Ambitious but achievable** — 70% attainment is the OKR standard (not 100%)

Good KR: *"Reduce mean time to restore (MTTR) from 45 min to < 15 min"*  
Bad KR: *"Complete the observability project"* (output) | *"Improve MTTR"* (not measurable)

### Initiatives
Initiatives are the *work* you'll do to achieve the Key Results. They are not KRs.

```
Objective → Key Results (what success looks like)
               ↓
           Initiatives (how you'll get there)
```

This distinction is the most common OKR failure point. Don't skip it.

---

## Why Engineering OKRs Often Fail

| Failure mode | Example | Why it's wrong | Fix |
|---|---|---|---|
| **Output confusion** | KR: "Ship feature X" | Shipping ≠ value delivered | KR: "Feature X increases user activation by 10pp" |
| **Task list** | KR: "Complete migration to K8s" | A task, not an outcome | KR: "Reduce deployment time from 20 min to < 5 min" |
| **Health metric as KR** | KR: "Maintain 99.9% uptime" | You're already doing this; not a stretch | Upgrade to 99.95%, or use as a guardrail |
| **Too many OKRs** | 4 Objectives, 12 KRs | Nothing is truly prioritized | 1–3 Objectives; 2–4 KRs each |
| **Sandbagging** | KR: "Reduce p50 latency by 5%" | Too easy; no real stretch | 70% attainment at 100% effort is right |
| **No business connection** | KR: "Reduce build times" | Build times in isolation aren't business value | Frame: "Reduce build times to enable 2x deploy frequency, supporting product team velocity" |
| **Not updated** | KRs written in January, checked in December | OKRs need weekly pulse and quarterly review | Weekly 15-min check-in; monthly full review |

---

## Connecting Team OKRs to Company OKRs

Every team OKR should have a clear line to a company or department OKR. If it doesn't, question whether it should be a priority.

### Cascade Pattern

```
Company OKR
  Objective: "Become the reliability leader in our market segment"
  KR: "Achieve and publicize 99.95% uptime for all Tier-1 services"

  ↓ cascades to ↓

Engineering Team OKR
  Objective: "Build observability that makes us proactively reliable"
  KR 1: "Reduce MTTR from 45 min to < 15 min"
  KR 2: "Alert before customers notice issues: 80% of incidents detected internally first"
  KR 3: "100% of Tier-1 services have SLOs defined and tracked"
```

**How to cascade**:
1. Start with company OKRs. What would engineering need to be true for those to succeed?
2. Write the engineering Objective that expresses that contribution
3. Write KRs that are engineering-measurable but business-meaningful
4. Don't copy company KRs verbatim — translate them into engineering outcomes

---

## Writing Good Engineering Key Results

### Output vs. Outcome Conversion Table

| Output KR (bad) | Outcome KR (good) | Why better |
|---|---|---|
| "Complete the data pipeline migration" | "P95 data latency reduced from 4 hours to < 15 minutes" | Measures the improvement, not the work |
| "Ship the new onboarding flow" | "New user activation rate increases from 34% to 45%" | Measures user behavior, not shipping |
| "Implement distributed tracing" | "Mean time to diagnose production issues < 30 min (from baseline of 2 hours)" | Measures the value of the tooling |
| "Reduce technical debt" | "Team velocity increases 20% as measured by story points/sprint, sustained for 6 weeks" | Connects debt to delivery speed |
| "Hire 3 engineers" | "New hire time-to-first-PR ≤ 7 days; 90-day retention 100%" | Measures onboarding quality, not headcount |

---

### DORA Metrics as Engineering Key Results

DORA metrics (from *Accelerate*) are some of the best engineering KRs because they measure outcomes (delivery capability), not outputs (tasks completed).

| DORA Metric | Description | Example KR |
|---|---|---|
| **Deployment frequency** | How often does production deploy? | "Deploy frequency increases from 2x/week to daily" |
| **Lead time for changes** | Time from commit to production | "Lead time from commit to prod < 1 hour (from 3 days)" |
| **Change failure rate** | % of deployments causing incidents | "Change failure rate < 5% (from current 15%)" |
| **Mean time to restore (MTTR)** | Time to recover from incidents | "MTTR < 30 min for P1 incidents (from 90 min)" |

DORA elite benchmarks for reference:
- Deployment frequency: multiple times per day
- Lead time: < 1 hour
- Change failure rate: 0–15%
- MTTR: < 1 hour

---

### Leading vs. Lagging Indicators

A good OKR set includes both:

| Type | Definition | Example | Risk |
|---|---|---|---|
| **Lagging** | Measures outcome after the fact | "MTTR < 15 min by end of quarter" | You find out at the end if you failed |
| **Leading** | Predicts whether you'll hit the lagging metric | "100% of services have runbooks by week 6" | May not actually predict the lagging metric |

Best practice: pair one lagging KR (the goal) with one leading KR (the early signal). If you only have lagging, you have no warning system.

---

## OKR Writing Template

```markdown
## [Team Name] OKRs — Q[N] [Year]

### Connecting to Company Strategy
[Which company OKRs does this team directly contribute to?
1–2 sentences tracing the connection.]

---

### Objective 1: [Inspiring, directional statement]
*Connects to: [Company OKR it supports]*

**Key Results:**
| KR | Baseline | Target | Confidence | Owner |
|---|---|---|---|---|
| [Measurable outcome] | [Current state] | [End state] | [H/M/L] | [Name] |
| [Measurable outcome] | | | | |

**Initiatives** (how we'll get there — not KRs):
- [ ] [Initiative 1]
- [ ] [Initiative 2]

**Guardrails** (what we won't sacrifice to hit these KRs):
- [e.g., "We will not reduce oncall quality to improve deployment frequency"]

---

### Objective 2: [...]
[Repeat structure]

---

### What We're Not Doing This Quarter
[Explicit list of plausible work that is deprioritized — shows real trade-offs]

### Key Assumptions
[What must be true for these OKRs to be achievable? What would cause us to revise?]
```

---

## Quarterly OKR Review Template

Use at the end of each quarter:

```markdown
## Q[N] OKR Review — [Team] — [Date]

### Scoring
| KR | Target | Actual | Score (0.0–1.0) | Notes |
|---|---|---|---|---|
| [KR 1] | [target] | [actual] | [score] | [what happened] |
| [KR 2] | | | | |

### Scoring guide:
- 0.0–0.3: Didn't make real progress
- 0.4–0.6: Made progress but fell short
- 0.7–1.0: Target achieved (0.7 is the OKR sweet spot)
- > 1.0: Target was too easy (set a harder one next time)

### Retrospective
**What drove our best results?**

**What got in the way?**

**What did we learn about our estimates / assumptions?**

**What should change in how we set OKRs next quarter?**

### Carryover to Q[N+1]
| Item | Status | Carry over? | Rationale |
|---|---|---|---|
| [KR or initiative] | [in progress / dropped] | [yes/no] | |
```

---

## OKR Cadence

| Cadence | Activity | Duration |
|---|---|---|
| **Annual** | Set company OKRs; team OKRs cascade | 1–2 planning days |
| **Quarterly** | Set team OKRs; review previous quarter | 2–4 hours |
| **Monthly** | Full OKR review: score, blockers, adjustments | 1 hour |
| **Weekly** | Pulse check: are KRs on track? Any blockers? | 15 min |

**Weekly pulse check format** (async-friendly):
> "OKR pulse for KR [X]: Last week we were at [Y%]. This week [progress update]. On track / at risk because [reason]. Need help with: [specific blocker or nothing]."

---

## Scoring and Calibration

**OKRs are not performance reviews.** A 0.7 on a well-set OKR is excellent. A 1.0 consistently means targets are too easy. Use OKR scores to calibrate the ambition of future goal-setting, not to judge people.

**What to do with low scores:**
- 0.4–0.6: Investigate whether the KR was achievable or whether execution failed
- < 0.4: Either the goal was too ambitious, blockers were not escalated early enough, or priorities changed — identify which

**Common score manipulation to avoid:**
- Retroactively changing the target when you're going to miss it
- Counting partially completed initiatives as KR progress
- Scoring on effort rather than outcome

---

## Output Format

When applying this skill, the agent should:
- Ask for the company's top OKRs or strategic priorities before writing team OKRs
- Ask for current baselines (e.g., current MTTR, current deploy frequency) to write meaningful KRs
- Convert any output-framed KRs into outcome-framed KRs
- Flag if an OKR set has too many objectives or too many KRs per objective
- Produce the full OKR set using the template above
- Suggest 1–2 DORA metrics that would be appropriate KRs for the team's context
- Identify any KRs that are actually health metrics (maintain, not improve) and suggest they be moved to guardrails instead

---

## References
- John Doerr: *Measure What Matters* — The canonical OKR reference; includes Google origin story
- Nicole Forsgren, Jez Humble, Gene Kim: *Accelerate* — Source of DORA metrics as engineering outcomes
- Will Larson: [Goal-setting and OKRs for engineering teams](https://lethain.com) — Practical engineering framing
- LeadDev: [Engineering metrics that matter](https://leaddev.com/engineering-metrics)
- Christina Wodtke: *Radical Focus* — OKR implementation story; highly practical
