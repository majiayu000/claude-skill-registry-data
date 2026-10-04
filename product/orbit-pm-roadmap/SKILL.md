---
name: orbit-pm-roadmap
description: Extract a quarterly roadmap from a WordPress plugin codebase + audits + feedback — proposes a quarter-by-quarter plan based on RICE backlog, technical debt findings, competitor gaps, and user feedback. Use when the user says "draft roadmap", "Q3 plan", "what should we ship next quarter", "roadmap from audits".
---

# 🪐 orbit-pm-roadmap — Quarterly roadmap drafter

Pulls signals from every Orbit audit + user feedback + competitor analysis and proposes a 4-quarter plan. PM-friendly artefact, not a final commitment.

---

## Quick start

```bash
claude "/orbit-pm-roadmap Draft a 4-quarter roadmap for my-plugin from the latest gauntlet + feedback mining + competitor compare."
```

Output: `reports/roadmap-<timestamp>.md`.

---

## What it does

### 1. Reads inputs
- `reports/rice-backlog-*.md` — `/orbit-pm-rice` output (priorities)
- `reports/feedback-mining-*.md` — `/orbit-pm-feedback-mining` themes
- `reports/competitor-*.md` — `/orbit-competitor-compare` gaps
- `reports/qa-report-*.md` — gauntlet findings (tech debt, security)
- `SKILL-ROADMAP.md` — pending items if relevant

### 2. Themes the next 4 quarters

| Quarter | Theme | Why |
|---|---|---|
| Q1 | 🛡 Security & Compliance | Audit found 3 high-severity findings + we're approaching GDPR review |
| Q2 | ⚡ Performance Sprint | Lighthouse score gap vs competitors, slow editor on big posts |
| Q3 | 🎨 UX Refresh | RICE backlog top 5 are all UX, supports retention KPI |
| Q4 | 🆕 Block Bindings + Interactivity API | Modernise to WP 6.5+ APIs before WP 7.0 |

### 3. Per-quarter detail
```
## Q1 — Security & Compliance

Goals
- Resolve 3 High-severity findings from /orbit-wp-security
- Achieve plugin-check 100% pass
- Register GDPR export + erase hooks
- Patch the AJAX nonce-refresh bug (#1 in RICE)

Out of scope
- New features (intentionally — security focus)

Risk
- Compliance team review may surface late requirements
- Mitigation: book review meeting Week 4
```

### 4. North-star metric mapping
Each quarter's work tied to a measurable outcome:
- Security quarter → `gauntlet --mode release` exit 0 every release
- Perf quarter → Lighthouse ≥ 90 on every visual URL
- UX quarter → guidance score ≥ 8 + complaint themes drop 50%

### 5. Trade-offs surfaced
The roadmap notes what you're NOT doing. "Q1 we are not adding features" lets you say no with rationale.

---

## Output

```markdown
# Roadmap — my-plugin · 2026-04-29 → 2027-04-29

## Themes
- Q1 (May–Jul 2026): Security & Compliance
- Q2 (Aug–Oct 2026): Performance Sprint
- Q3 (Nov 2026–Jan 2027): UX Refresh
- Q4 (Feb–Apr 2027): Block Bindings + Interactivity API

## North-star metric per quarter
- Q1: 0 Critical/High in `/orbit-gauntlet --mode release`
- Q2: Lighthouse ≥ 90 on Settings, Editor, Dashboard
- Q3: Guidance score ≥ 8/10
- Q4: 100% blocks on apiVersion 3 + Interactivity API for dynamic blocks

## Q1 detail
[goals, scope, out-of-scope, risk]

## Carry-forward (not yet scoped)
- Multilingual deep audit (WPML + Polylang)
- Multisite cross-tenant test pass
- iOS app integration

## Sign-off
Draft prepared by /orbit-pm-roadmap on 2026-04-29.
Reviewed by: <PM> on <date>
Approved by: <Founder> on <date>
```

---

## Pair with

- `/orbit-pm-rice` — feed RICE scores into quarter sequencing
- `/orbit-pm-feedback-mining` — anchor themes to user pain
- `/orbit-pm-competitor-pulse` — competitive gaps go into specific quarters

---

## Sources & Evergreen References

### Canonical docs
- [Lenny's Newsletter — Roadmaps](https://www.lennysnewsletter.com/p/roadmaps) — modern PM thinking
- [Marty Cagan — Inspired](https://svpg.com/inspired-how-to-create-products-customers-love/) — product-discovery context
- [North Star Framework](https://amplitude.com/blog/north-star-metric) — outcome-oriented planning

### Last reviewed
- 2026-04-29
