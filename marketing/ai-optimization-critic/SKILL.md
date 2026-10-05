---
name: ai-optimization-critic
alias: /ai-optimization-critic
description: "Review content for Google AI Overview eligibility — RAG retrievability, E-E-A-T signal completeness, fan-out coverage, semantic HTML for agent parsability, schema markup quality."
version: 1.0.0
disallowedTools: Write, Edit
invokable: true
perspective_module: true
---

# AI Optimization Critic

## JTBD (Jobs To Be Done)

### Primary Job
When I have existing content and want to know whether it is eligible for Google AI Overviews,
I want an evidence-backed AIO readiness review,
so I can address the specific gaps before investing in Tier 2 content or Tier 3 platform work.

### Secondary Jobs
- When an `ai-optimization-planner` output needs independent validation before implementation, I want a critic review, so the plan is sound before resources are committed.
- When a broader copy review needs an AIO eligibility lens, I want a focused perspective module, so the final recommendation includes AIO concerns without overclaiming.

### This Skill Is For
- Reviewing existing content for AI Overview eligibility gaps before publishing or refreshing.
- Reviewing an `ai-optimization-planner` output before implementation begins.
- Adding an AIO perspective to a `copy-critic` review on high-investment content.
- Auditing pages after Tier 1 or Tier 2 implementation to verify AIO signal improvements.

### This Skill Is NOT For
- Writing or rewriting content — this skill is read-only.
- Structural SEO review (heading hierarchy, meta descriptions, internal linking, intent alignment) — use `seo-advisor`.
- Suggesting `llms.txt`, AI-specific markup, or keyword variants for AI modes — these are not AIO signals.
- Predicting traffic or rankings.

### Resolution Paths

| User Situation | What Happens | What They Leave With |
|---------------|-------------|----------------------|
| Content may be AIO-ineligible | Full 10-phase investigation | Verdict with CRITICAL/MAJOR/MINOR findings and actionable fixes |
| Plan needs validation before implementation | Critic reviews ai-optimization-planner output | ACCEPT or REVISE verdict with specific concerns |
| Broader review needs AIO lens | Perspective Module mode (abbreviated) | Compact AIO perspective for parent critic |
| Post-implementation check | Full review focused on implemented changes | Updated verdict confirming improvement or remaining gaps |

### When to Escalate
- If content quality (tone, clarity, brand voice) is the primary problem → `copy-critic`
- If structural SEO (headings, meta, internal links) is the primary problem → `seo-advisor`
- If content doesn't exist yet → `copy-planner` + `ai-optimization-planner`
- If REVISE verdict requires planning → `ai-optimization-planner`

---

## Purpose

This critic is the companion reviewer to `ai-optimization-planner`. Its primary function is independent verification of AIO eligibility signals — ensuring that:

1. AIO-specific findings are genuinely about AIO, not structural SEO issues rebranded
2. E-E-A-T gaps are rated correctly against YMYL vs non-YMYL thresholds
3. Schema markup findings cite specific properties, not vague assertions
4. Fan-out coverage gaps identify the most commercially important absent angles
5. Scope boundary between AIO issues and seo-advisor/copy-critic issues is clearly maintained

The `**Scope Boundary**` output section is unique to this critic — it makes the domain boundary machine-parseable and prevents teams from conflating structural SEO with AIO eligibility.

---

## What This Skill Does

- ✓ Predicts likely issues before investigation (pre-commitment, reducing confirmation bias)
- ✓ Verifies indexing status and snippet eligibility (RAG prerequisites)
- ✓ Assesses E-E-A-T across all four dimensions with documented severity calibration
- ✓ Generates and scores query fan-out coverage (5–7 related queries)
- ✓ Audits Schema.org markup with specific property-level evidence
- ✓ Reviews multimedia richness and commodity-content signals
- ✓ Applies Multi-Perspective Review (RAG system, AI consumer, agentic task, seo cross-check)
- ✓ Runs mandatory Self-Audit (confidence/refutability/flaw-vs-preference)
- ✓ Runs mandatory Realist Check (calibrate severity to documented impact)
- ✓ Reports structural SEO issues in a non-scoring `**Scope Boundary**` section
- ✓ Works as standalone full reviewer OR abbreviated perspective module

## What This Skill Does NOT Do

- ✗ Write or edit content (read-only; `disallowedTools: Write, Edit`)
- ✗ Score structural SEO findings (heading hierarchy, meta descriptions, internal links)
- ✗ Recommend `llms.txt` or AI-specific markup
- ✗ Predict rankings or traffic
- ✗ Claim Core Web Vitals are direct AIO signals

---

## Use_When

- Content draft is ready and team wants AIO eligibility review before publishing
- High-investment content (original research, case study, product page) needs AIO validation
- Reviewing `ai-optimization-planner` output before Tier 1/2/3 implementation begins
- Post-implementation verification (was schema markup added correctly? did E-E-A-T improve?)
- Adding AIO perspective to a `copy-critic` review on strategic content

## Do_Not_Use_When

- Need structural SEO review (heading hierarchy, meta, internal links) → use `seo-advisor`
- Need content quality review (tone, clarity, brand voice) → use `copy-critic`
- Content doesn't exist yet → use `copy-planner` and `ai-optimization-planner`
- You want to know if content "will rank" → not deterministic; no tool can answer this

---

## Modes

### Standalone Mode

When invoked with `/ai-optimization-critic [content or URL]`:

1. Run Phase 1: Pre-Commitment Predictions
2. Run Phase 2: RAG Retrievability Investigation
3. Run Phase 3: E-E-A-T Signal Audit
4. Run Phase 4: Query Fan-Out Coverage Assessment
5. Run Phase 5: Semantic HTML and Schema Markup Audit
6. Run Phase 6: Multimedia Richness and Non-Commodity Content
7. Run Phase 7: Multi-Perspective Review
8. Run Phase 8: Self-Audit (mandatory)
9. Run Phase 9: Realist Check (mandatory)
10. Run Phase 10: Synthesis
11. Output full format contract (see below)

### Perspective Module Mode

When invoked by `copy-critic`, `seo-advisor`, or another skill with `perspective: ai-optimization-critic`:

Run abbreviated review (Phases 2–3, top 2 fan-out findings, top schema gap):

Output only:
```
**AIO Perspective:**
- RAG eligibility: [CONFIRMED/ASSUMED/BLOCKED] — [1 sentence]
- E-E-A-T: [STRONG/PARTIAL/WEAK] — [top gap if any, 1 sentence]
- Fan-out coverage: [X/Y angles] — [most important absent angle]
- Schema: [key type present or the most critical missing type]
- Key recommendation: [single most impactful AIO improvement]
```

---

## Output Format Contract

These headings are **load-bearing** — eval harness and downstream parsers depend on exact names:

```
**VERDICT: [REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT]**
**Overall Assessment**
**Pre-commitment Predictions**
**Critical Findings**
**Major Findings**
**Minor Findings**
**Scope Boundary**
**What's Missing**
**Multi-Perspective Notes**
**Verdict Justification**
**Open Questions (unscored)**
```

The `**Scope Boundary**` section is unique to this critic. It lists structural SEO issues or content quality issues found during review — acknowledged but explicitly not scored as AIO findings. This section maintains the domain boundary with `seo-advisor` and `copy-critic`.

### Verdict Scale

- **REJECT**: One or more CRITICAL findings (blocks AIO retrieval OR YMYL E-E-A-T absent), or YMYL content with multiple MAJOR findings
- **REVISE**: One or more MAJOR findings without CRITICAL; improvements are specific and actionable
- **ACCEPT-WITH-RESERVATIONS**: Only MINOR findings; no MAJOR or CRITICAL; notable items in What's Missing
- **ACCEPT**: No MAJOR or CRITICAL findings; a clean AIO eligibility review

---

## Severity Scale

- **CRITICAL**: Demonstrably blocks AIO retrieval (`nosnippet` directive, content not indexed with strong evidence) OR YMYL content with total absence of any E-E-A-T dimension
- **MAJOR**: Documented AIO signal gap that is addressable — missing schema on content with an obvious schema type, pure commodity content with ABSENT Experience signals, primary fan-out angle entirely absent, `<main>` landmark absent on a substantial site
- **MINOR**: May improve AIO inclusion but not clearly deterministic — additional schema fields, PARTIAL fan-out coverage, original images recommended, dates in text but not `<time datetime>`
- **ENHANCEMENT**: Best practice improvement with no documented AIO impact

---

## Companion_Skills

- **ai-optimization-planner**: Companion planner — invoke when REVISE or REJECT to redesign the improvement plan
- **seo-advisor**: When `**Scope Boundary**` section indicates structural SEO needs dedicated review
- **copy-critic**: When REVISE verdict or `**Scope Boundary**` indicates content quality needs improvement
- **copy-planner**: When REVISE verdict includes MAJOR E-E-A-T content gaps requiring original writing

---

**Version:** 1.0.0
**Last Updated:** 2026-05-19
**Perspective Module Compatible:** Yes
**Standalone Ready:** Yes
