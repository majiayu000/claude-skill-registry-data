---
name: CRO / Chief Revenue Officer
slug: cro
version: 1.0.1
homepage: https://clawic.com/skills/cro
description: Optimize conversion rates with funnel analysis, A/B testing, statistical significance, and compliance-safe experiments.
changelog: Added Core Rules structure with statistical rigor and compliance guidelines.
metadata: {"clawdbot":{"emoji":"📈","os":["linux","darwin","win32"]}}
---

## When to Use

User wants to improve conversion rates for websites, landing pages, SaaS products, or eCommerce. Agent runs funnel audits, designs A/B tests, interprets statistical results, and implements winning variants while maintaining legal compliance.

## Quick Reference

| Topic | File |
|-------|------|
| A/B testing methodology | `testing.md` |
| Conversion audits | `audits.md` |
| Legal compliance | `legal.md` |
| Tools and integrations | `tools.md` |

## Core Rules

### 1. Statistical Rigor First
- 95% confidence minimum before calling any test
- Calculate sample size before starting — underpowered tests waste time
- Run tests to full duration — early peeking inflates false positives
- Document hypothesis before running — post-hoc rationalization is not science

### 2. Funnel Analysis Before Optimization
- Map entire journey: awareness, consideration, decision, retention
- Quantify drop-off at each step with specific numbers
- Revenue impact per improvement — prioritize by dollars, not percentages
- Segment by traffic source, device, user type — aggregates hide insights

### 3. One Variable Per Test
- Isolate changes to attribute results correctly
- Multivariate testing requires massive traffic most don't have
- If you change two things and conversion improves, you learned nothing

### 4. Mobile-First Testing
- Test mobile variants explicitly — desktop assumptions fail on phones
- Majority of traffic is mobile, often worst conversion
- Touch targets, page speed, form friction all differ

### 5. Legal Compliance Non-Negotiable
- Cookie consent required in EU before tracking
- GDPR: personal data in experiments needs legal basis
- Dark patterns are illegal — fake urgency, confirm-shaming, hidden costs
- Accessibility (WCAG) is both legal requirement and conversion opportunity

### 6. Document Everything
- Hypothesis, variants, results, learnings in permanent record
- Losing tests are learning — document why hypothesis was wrong
- Share results across teams — wins in one funnel inform others

### 7. Revenue Connection
- Revenue targets tie to conversion targets — make the math explicit
- Signups mean nothing if they never convert to revenue
- Prioritize by ICE: Impact, Confidence, Ease

## Common Traps

- Calling tests early because results look good — false positives waste resources
- "We changed everything and revenue went up" — no control group proves nothing
- Copy-pasting competitor tactics without context — what works for them may fail for you
- Optimizing for vanity metrics — engagement without revenue is vanity
- Testing without proper tracking setup — retroactive data is unreliable

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `ceo` — strategic leadership
- `cfo` — financial planning
- `cmo` — marketing strategy
- `analytics` — data analysis

## Feedback

- If useful: `clawhub star cro`
- Stay updated: `clawhub sync`
