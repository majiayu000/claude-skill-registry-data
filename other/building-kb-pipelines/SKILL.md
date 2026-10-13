---
name: building-kb-pipelines
description: >
  Designs and operates FlashFusion's Zero-Admin KB Generation pipeline —
  automated ticket-to-article for MSP/ITSM environments. Use when scoping a KB
  automation engagement, designing the ticket-to-article pipeline, configuring
  article quality gates or draft review, choosing the deployment stack, or
  producing the phase plan. Triggers on: KB automation, KB pipeline,
  ticket-to-article, zero-admin KB, article automation, IT knowledge management,
  documentation pipeline, KB scoping session, KB phase plan, draft-mode review,
  article quality gate.
license: MIT
allowed-tools: Read, Write
compatible-with: claude-code, codex, openclaw
metadata:
  version: "2.0.0"
  track: flashfusion
  type: procedure
---

# Building KB Pipelines

FlashFusion's Zero-Admin KB Generation service: ITSM tickets in, draft KB
articles out, human reviews before publish. Reference deployment — Loxihart MSP,
~90-second generation, ~$1–5/month on AWS Lambda + Bedrock. Architecture is
stack-agnostic. This SKILL.md drives the session; deep content lives in the
reference files it routes to.

## Evals

**Should trigger:**
1. "A client wants their resolved tickets to auto-generate KB articles. Help me scope it."
2. "Design the ticket-to-article pipeline — what are the stages and where do the quality gates go?"
3. "Build the KB automation phase plan with the pilot gate and kill criteria."

**Should NOT trigger:**
1. "Write a KB article on resetting a VPN token." → single article on demand, use `generating-kb-articles`.
2. "Score and rank the client's AI opportunities." → that's `use-case-discovery`, not pipeline design.

## Principles (non-negotiable)

1. **Draft mode is non-negotiable.** All articles publish to Draft. A human reviews before it goes live.
2. **Router quality gate first.** Not every ticket becomes an article — the router decides.
3. **Benchmark Zero required.** Measure current KB state, volume, and cost before building.
4. **Five sections required.** Incomplete articles route to the KB GAP queue, never publish.
5. **PII redaction is Phase 0.** Strip PII before generation, always.

## Decision Tree — route to the right reference file

```
What's the task?
  ├─ "How does the pipeline work / what are the stages / router criteria?"
  │     → references/pipeline-architecture.md
  ├─ "What goes in an article / the five sections / validation rules?"
  │     → templates/article-schema.md
  ├─ "What's the rollout plan / phase gates / kill criteria?"
  │     → workflows/phase-plan.md
  ├─ "What stack / infra / cost / which LLM?"
  │     → references/stack-options.md
  └─ "Scope a new KB engagement end-to-end"
        → run the Golden Path below (touches all four)
```

Load only the reference file the current task needs. Do not dump all four.

## Intake — collect before scoping

Ask for these. Do not design on blanks; insert `[FILL: …]` and flag it.

| Field | Why it matters |
|---|---|
| ITSM platform | Webhook + API shape (e.g., Freshservice, ServiceNow, Jira SM). `[FILL: client ITSM platform]` |
| Ticket volume (resolved/month) | Sizes cost, router throughput, and pilot duration |
| Existing KB state | Benchmark Zero — article count, freshness, gaps |
| Article-worthy ticket types | Seeds the router's include criteria |
| PII / data sensitivity | Sets Phase 0 redaction scope and any compliance constraints |
| Cloud / stack preference | AWS, Azure, or other; drives `references/stack-options.md` |
| Reviewer + publish owner | Who clears the Draft queue, and how often |
| Definition of a "good" article | Calibrates the validator and pass-rate gate |

## Golden Path — scope a KB engagement

1. **Intake** — collect the table above. Capture the ITSM platform and ticket volume first; everything sizes off them.
2. **Benchmark Zero** — document current KB count, freshness, top recurring ticket themes, and the cost of the status quo (analyst time writing articles manually). No baseline, no build.
3. **Define the router gate** — from `references/pipeline-architecture.md`, set include/exclude criteria for which resolved tickets become article candidates.
4. **Lock the article schema** — confirm the five required sections and validation rules from `templates/article-schema.md`. Confirm Draft-only publishing.
5. **Set Phase 0 PII redaction** — define what gets stripped before any generation. `[FILL: client-specific PII fields / compliance regime]`.
6. **Choose the stack** — pick deployment from `references/stack-options.md` (reference: AWS Lambda + Bedrock). Estimate monthly cost from ticket volume.
7. **Build the phase plan** — instantiate `workflows/phase-plan.md` with this client's gate thresholds and kill criteria.
8. **Produce the scoping deliverable** — assemble the output template below and hand back.

## Scoping Output Template

Deliver one document with these named sections:

1. **Engagement Header** — client, ITSM platform, ticket volume, reviewer/owner, date.
2. **Benchmark Zero** — current KB state, monthly article-worthy volume, status-quo cost. Each figure `[SOURCED]` or `[GENERATED]`.
3. **Pipeline Design** — the stage diagram and the router include/exclude criteria (from pipeline-architecture).
4. **Article Schema** — the five sections + validation/quality gate; confirmation of Draft-only.
5. **PII & Compliance** — Phase 0 redaction scope; any regulatory constraint. `[FILL: …]` where unknown.
6. **Stack & Cost** — chosen stack, estimated monthly cost, scaling note.
7. **Phase Plan** — table of phases with duration, gate threshold, and kill/extend criteria.
8. **Open Items** — every `[FILL: …]` in one list.

## Self-Verification Checklist

Before returning the scope:
1. Intake table complete or every gap carries an explicit `[FILL: …]`.
2. Benchmark Zero present — no proposal on an unknown baseline.
3. Router gate has explicit include AND exclude criteria.
4. Article schema confirms five sections and Draft-only publishing.
5. Phase 0 PII redaction defined (or flagged `[FILL: …]`).
6. Phase plan includes a written kill criterion per gated phase.
7. Cost figures labeled `[SOURCED]` or `[GENERATED]`; no invented pricing.
8. SKILL.md routed to reference files rather than restating their full content.

## CLAIMS

- Reference deployment (Loxihart MSP, ~90s generation, ~$1–5/mo on AWS Lambda + Bedrock) is carried forward from the original skill. [SOURCED — prior skill version]
- Draft-mode-only publishing with mandatory human review is a FlashFusion service principle. [GENERATED]
- Exact router scoring thresholds, the specific Bedrock model, and PII redaction implementation are not specified here and must be supplied per client. [GENERATED — see [FILL] markers]

## COUNTEREXAMPLE

- Do NOT use for writing a single KB article (→ `generating-kb-articles`) or for opportunity ranking (→ `use-case-discovery`).
- Do NOT auto-publish: a pipeline that skips the Draft queue violates Principle 1 regardless of pass rate.

## CONTRADICTIONS

- ! "Stack-agnostic architecture" vs. a concrete AWS Lambda + Bedrock reference — resolve by treating AWS as the reference implementation in `references/stack-options.md`, not a requirement.
