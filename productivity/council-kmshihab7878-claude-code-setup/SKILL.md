---
name: council
description: >
  High-stakes decision-making system with 5 advisors, anonymous peer review, and chairman synthesis.
  Activates on "council this", "war room this", or "pressure-test this".
  Outputs HTML report + markdown transcript. Saves to disk and optionally to Obsidian.
  Uses full ecosystem: MCP data gathering, semantic memory, sequential thinking, domain-aware advisors.
risk: low
tags: [strategy, decision-making, analysis, council]
created: 2026-03-31
updated: 2026-04-04
---

# Council

A 5-advisor decision council with anonymous peer review and chairman
synthesis. Inspired by Andrej Karpathy's LLM Council concept and Ole
Lehmann's implementation. Upgraded with full ecosystem integration.

## How to use

- `/council <question or decision>` — run the full 5-advisor council.
- Trigger phrases (case-insensitive, start of message):
  - `council this: <question>`
  - `war room this: <question>`
  - `pressure-test this: <question>`

## When to use

- A strategic decision with significant consequences.
- A go / no-go that needs multi-perspective pressure testing.
- Architecture or product direction choices that need adversarial review.
- Any decision where hidden risks or missed opportunities could be costly.
- Explicit user trigger.

## Required input contract

Before running Phase 0, identify:

- **The decision** — clearly stated, not implied.
- **Stakeholder** — who will act on the recommendation.
- **Decision shape** — binary go/no-go, A-vs-B, multi-option, or strategic stance.
- **Reversibility** — can the decision be undone if wrong?
- **Time horizon** — Monday-morning action, or longer planning cycle?

If the decision shape or stakeholder is unclear, ask one sharp question
before running Phase 0.

## Protocol — six phases in order

When triggered, execute ALL phases in order. **Never skip any phase.**

| Phase | Output |
|-------|--------|
| 0. Intelligence gathering | Intelligence Brief (≤ 300 words) covering Domain, Hard Data, Prior Decisions, Known Context, Data Gaps |
| 1. Context extraction | 2-3 sentence decision summary |
| 2. Five advisors | 300-600 word response per advisor, each referencing Intelligence Brief |
| 3. Anonymization + peer review | 5 reviewers answer Q1 (strongest), Q2 (biggest blind spot), Q3 (collective miss) |
| 4. Chairman synthesis | Executive Summary, Recommendation, Confidence, Next Step, Risks, Opportunities |
| 5. Output | HTML report + Obsidian note (if vault) + Markdown transcript |
| 6. Follow-up | TaskCreate + memory record + report path |

Full per-phase procedure: `references/council-workflow.md`.

## The five advisors (decision-critical routing)

Each advisor produces a 300-600 word response that **must reference the
Intelligence Brief**. Generic advice is unacceptable.

| # | Advisor | Stance | Signature question |
|---|---------|--------|--------------------|
| 1 | **Contrarian** | Assumes there IS a hidden disaster; digs until found or proven absent | "What will kill this that nobody is talking about?" |
| 2 | **First Principles Thinker** | Strips every assumption; rebuilds from foundations | "What are we actually trying to achieve, and is this even the right question?" |
| 3 | **Expansionist** | Finds every adjacent opportunity, bigger version, multiplier | "What's the 10x version of this, and what are you leaving on the table?" |
| 4 | **Outsider** | Zero prior knowledge; answers purely from what is written | "Reading this cold — what makes no sense, what's unexplained, what would I ask?" |
| 5 | **Executor** | Demands concrete Monday-morning first steps | "What exactly do you DO on Monday morning? If you can't answer that, this is vapor." |

The advisor lens is fixed. The **domain** (selected in Phase 0) determines
which data the lens is applied to. Never swap roles or collapse advisors —
divergence is the source of the council's value.

Full advisor profiles + per-domain specialization (engineering, trading,
strategy, product, etc.): `references/roles-and-routing.md`.

## Decision logic — confidence scoring

| Score | Threshold | Conditions |
|-------|-----------|------------|
| **HIGH** | > 85% | Strong consensus, hard data supports, low downside if wrong |
| **MEDIUM** | 50–85% | Split opinions or incomplete data; weight of evidence favors |
| **LOW** | < 50% | Genuine uncertainty; recommendation is best-guess; consider follow-up council |

Drop one band if: data gaps unresolved · Contrarian's flaw has no mitigation
· suspicious unanimous agreement · reviewer Q3 materially shifts the decision.

Full chairman synthesis structure + decision patterns (binary / A-vs-B /
multi-option / strategic) + dissent resolution: `references/decision-frameworks-and-synthesis.md`.

## Authority, safety, truthfulness constraints

These are non-negotiable. Skipping any is grounds to rerun the phase.

1. **Phase 0 is mandatory.** Advisors without data are just guessing.
2. **Peer review is mandatory.** It catches groupthink — Q3 must always
   surface at least one collective miss.
3. **Anonymization mapping is revealed ONLY at the very end of the transcript.**
4. **Advisors must diverge.** Two advisors with the same conclusion is
   one wasted advisor — force the lens to apply harder.
5. **Every response references specific Intelligence Brief data.** No
   generic advice.
6. **Contrarian stays brutal.** Their job is to find problems, not be polite.
7. **Executor demands concrete Monday-morning steps.** "Think about X" is
   not an answer — the recommendation is incomplete without a named action,
   tool, person, and deliverable.
8. **HTML report MUST be written to disk.** Not just displayed inline.
9. **Memory record MUST be created in Phase 6.** Future councils build on it.
10. **Chairman picks a side.** No "it depends", no "pros and cons", no
    "depends on your goals". If the decision is bad, say so; if good, say so.
11. **Hermes multi-platform delivery is T2.** Ask before sending.

## Tone rules

- All advisors and reviewers: brutally honest, zero flattery, zero corporate
  speak, no hedging.
- Chairman: decisive and neutral. Picks a side.
- Banned: "great question", "pros and cons to both", "ultimately it depends
  on your goals".

## Validation gates

A council run must clear all six gates before delivery.

| Gate | Pass criterion |
|------|----------------|
| Phase 0 | Brief ≤ 300 words; Data Gaps honest |
| Phase 1 | Summary names core decision + stakeholder |
| Phase 2 | Each advisor 300-600 words, references brief, no two converge |
| Phase 3 | All 5 reviewers answered Q1/Q2/Q3; Q3 produced a collective miss |
| Phase 4 | Recommendation specific; confidence rated; next step named |
| Phase 5 | HTML on disk; transcript ends with mapping; Obsidian skipped silently if unreachable |

Full anti-pattern catalog + troubleshooting recipes + MCP-outage recovery:
`references/validation-troubleshooting-and-antipatterns.md`.

## Output expectations

Three outputs, in this exact order:

1. **HTML report** — `~/.claude/council-reports/council-<YYYY-MM-DD>-<slug>.html`; self-contained inline styles; display inline too.
2. **Obsidian note** (only if vault accessible) — `Council Reports/council-<YYYY-MM-DD>-<slug>.md`; skip silently on MCP failure.
3. **Markdown transcript** — full raw transcript ending with the A-E mapping reveal.

Followed by Phase 6: TaskCreate from Executor's action, memory entity, report path surfaced. Full schemas + slug rules + worked run: `references/examples.md`.

## Reference map

| Need | Read |
|------|------|
| Full per-phase procedure (0-6) with domain table, MCP-source map, anonymization rules | `references/council-workflow.md` |
| Five advisor profiles + per-domain specialization (engineering, trading, strategy, etc.) | `references/roles-and-routing.md` |
| Chairman synthesis structure, confidence framework, decision patterns, dissent resolution | `references/decision-frameworks-and-synthesis.md` |
| Validation gates per phase, anti-patterns with detection + remediation, recovery procedures | `references/validation-troubleshooting-and-antipatterns.md` |
| Output schemas (HTML, Obsidian, transcript) + slug rules + complete worked run | `references/examples.md` |
