---
name: market-audit
description: Full marketing audit orchestrator launching 5 parallel subagents and aggregating into a unified client-ready report.
---

# Marketing Audit Orchestrator

Marketing audit engine for `/market audit <url>`. Orchestrate a comprehensive
analysis by launching 5 specialist subagents in parallel, then synthesize
their findings into a single client-ready report. This is the most complex
marketing skill — it produces the highest-value deliverable.

## When this skill is invoked

The user runs `/market audit <url>`. Fetch the target URL, classify the
business, launch 5 specialist subagents in parallel, aggregate findings into a
unified report saved to `MARKETING-AUDIT.md`, and display a terminal summary.

## Required input contract

Before launching subagents:

- **Target URL** — must be reachable; if not, report and ask to verify.
- **Auth state** — if pages are gated, note what is accessible and flag
  gated content for manual review; do not invent the missing analysis.
- **Cross-skill inputs** — if `COMPETITOR-REPORT.md` or `BRAND-VOICE.md`
  exist in the current directory, load them.
- **Site size** — for single-page sites, adapt the analysis and flag the
  limited scope in the executive summary.

## Compliance, claims, and audit-integrity constraints

- **No fabricated competitive data.** Competitor scores, named results, and
  comparison entries must come from real observation of competitor URLs or
  be explicitly marked illustrative.
- **Revenue impact estimates are scenarios, not promises.** Always use
  conservative / moderate / aggressive ranges with confidence labels
  (High / Medium / Low). Never imply guaranteed outcomes.
- **Industry benchmarks must be cited or labeled as estimates.** "Industry
  benchmark CR is 2–4%" needs a source or a 🟡 estimate tag.
- **No dark patterns** in recommendations (hidden costs revealed late,
  manipulative opt-outs, forced continuity, "Yes / No-thanks" guilt copy) —
  FTC-banned and damaging long-term.
- **WCAG 2.2 AA accessibility is non-negotiable** — contrast ≥ 4.5:1 body /
  ≥ 3:1 large text, ≥ 16px body, keyboard nav, alt text, focus indicators.
- **Privacy compliance (GDPR / CCPA)** — explicit opt-in for marketing,
  no pre-checked boxes, privacy policy near forms, no PII targeting in copy.
- **Subagent independence.** Each subagent works from the same brief but
  produces its own findings — do not let one subagent's output bias another.
  Synthesize at Phase 3.
- **Handle partial data gracefully.** If a subagent fails or a page is gated,
  note the gap — never fabricate.
- **Mobile-first.** Recommendations must work on the 60%+ of traffic that is mobile.

## Three-phase workflow

### Phase 1 — Discovery

1. `WebFetch` homepage + up to 5 key interior pages (pricing, about,
   product/features, blog, contact).
2. Classify business type (SaaS / E-commerce / Agency / Local / Creator /
   Marketplace) — classification shapes every subagent's analysis focus.
3. Build the page map (homepage, landing pages, pricing, product, about,
   blog, contact, legal). Store for all subagents.

Full detection-signal table per business type + page map detail:
`references/audit-workflow.md`.

### Phase 2 — Parallel subagents

Launch **all 5 subagents simultaneously** with the business type, page map,
and fetched content.

| # | Subagent | Score produced |
|---|----------|----------------|
| 1 | `market-content` | Content & Messaging (0–100) |
| 2 | `market-conversion` | Conversion Optimization (0–100) |
| 3 | `market-competitive` | Competitive Positioning (0–100) |
| 4 | `market-technical` | SEO & Discoverability (0–100) |
| 5 | `market-strategy` | Brand & Trust (0–100) + Growth & Strategy (0–100) |

Full per-subagent evaluation checklists + cross-subagent funnel view:
`references/channel-and-funnel-audits.md`.

### Phase 3 — Synthesis

Aggregate subagent outputs into a unified report.

## Scoring (decision logic)

```
Marketing Score = (
    Content_Score      × 0.25 +
    Conversion_Score   × 0.20 +
    SEO_Score          × 0.20 +
    Competitive_Score  × 0.15 +
    Brand_Score        × 0.10 +
    Growth_Score       × 0.10
)
```

| Score | Grade | Meaning |
|-------|-------|---------|
| 85–100 | A | Excellent — minor optimizations only |
| 70–84 | B | Good — clear opportunities for improvement |
| 55–69 | C | Average — significant gaps to address |
| 40–54 | D | Below average — major overhaul needed |
| 0–39 | F | Critical — fundamental marketing issues |

Per-grade aggregator emphasis + diagnostic heuristics for low category scores:
`references/scoring-and-diagnostics.md`.

## Recommendation classification

| Tier | Timeline | Effort | Impact |
|------|----------|--------|--------|
| Quick Wins | < 1 week | Low | High |
| Strategic Recommendations | 1–4 weeks | Medium | High |
| Long-Term Initiatives | 1–3 months | High | Transformative |

Example recommendations per tier: `references/scoring-and-diagnostics.md`.

## Revenue impact

```
Revenue Impact = Monthly Traffic × Conversion Rate Improvement × Avg Deal Value
e.g. 10,000 visitors × 0.5% conv lift × $99 ARPU = $4,950 / mo
```

| Impact | Monthly lift | Confidence |
|--------|--------------|------------|
| High | > $5,000/mo or > 20% | Based on clear audit evidence |
| Medium | $1,000–$5,000/mo or 5–20% | Based on industry benchmarks |
| Low | < $1,000/mo or < 5% | Incremental optimization |

Always provide conservative / moderate / aggressive ranges. Full framework +
reporting templates: `references/remediation-and-reporting.md`.

## Validation gates

Before delivering the report:

- [ ] All 5 subagents executed (or failures noted with explicit gaps).
- [ ] Composite score calculated with correct weights; sum to 100%.
- [ ] Quick Wins (5–10), Strategic (3–7), Long-Term (2–5) classified.
- [ ] Every recommendation carries a Confidence tag (High / Medium / Low).
- [ ] No competitor data is fabricated or unmarked.
- [ ] Accessibility / privacy / dark-pattern compliance checked on every recommendation.
- [ ] Mobile-first explicitly considered for UX-affecting recommendations.
- [ ] Partial-data gaps disclosed in the executive summary.

## Output expectations

- **Report file**: write the unified audit to `MARKETING-AUDIT.md` in the
  current directory using the full template.
- **Terminal output**: render the score, breakdown bars, top 3 quick wins,
  top 3 strategic moves, and estimated revenue impact range.

Full `MARKETING-AUDIT.md` template + terminal output format:
`references/remediation-and-reporting.md`.
Competitor comparison table, executive summary, recommendation packaging
examples: `references/examples.md`.

## Error handling

- **URL unreachable** — report and suggest verifying the URL.
- **Subagent failure** — continue with remaining subagents and note the gap.
- **Authenticated content** — note what was accessible; recommend manual review.
- **Single-page or content-thin site** — adapt the analysis; flag limited scope.

## Cross-skill integration

- If `COMPETITOR-REPORT.md` exists, incorporate its findings.
- If `BRAND-VOICE.md` exists, use it to contextualize content analysis.
- Reference other available analyses in the executive summary.

## Reference map

| Need | Read |
|------|------|
| Phase 1 detection signals + page map; Phase 2 launch + partial-data handling | `references/audit-workflow.md` |
| Composite formula deep dive, grade interpretation, recommendation tiers, diagnostic heuristics | `references/scoring-and-diagnostics.md` |
| Per-subagent evaluation checklists + cross-subagent funnel view | `references/channel-and-funnel-audits.md` |
| Revenue impact framework, full `MARKETING-AUDIT.md` template, terminal output, reporting rules | `references/remediation-and-reporting.md` |
| Competitor comparison, executive summary, Quick/Strategic/Long-Term entry examples, partial-data disclosure | `references/examples.md` |
