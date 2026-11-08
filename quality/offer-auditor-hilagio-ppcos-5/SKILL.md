---
name: offer-auditor
description: Audit offer quality across 16 diagnostics (value, urgency, trust, positioning). Scores 0-100. Use for offer quality checks, health reviews, and assessments.
argument-hint: "[--module value|urgency|trust|positioning]"
---

# Offer Auditor Skill

Audits offer quality across 1 module (16 diagnostics). Scores the offer's foundation and identifies gaps.

**CRITICAL: All questions to the user MUST use the `AskUserQuestion` tool with selectable options.** Never ask questions as plain text in the terminal. For every question, provide 2-4 concrete answer options the user can select from. When asking for specific data (e.g., D02 dream outcome fix), provide example answers as selectable options plus the "Other" escape hatch for custom input. Use `multiSelect: true` when multiple answers apply.

**DIAGNOSE (audit):**

| Module | IDs | Method |
|--------|-----|--------|
| **Offer Quality** | D01-D16 | business.md + brand.md validation + user interview |

## Command Format

```
/offer-auditor                        # All 16 diagnostics
/offer-auditor --module value         # D01-D06 (Value + Uniqueness)
/offer-auditor --module urgency       # D07-D08 (Urgency)
/offer-auditor --module trust         # D09-D13 (Risk + Proof + Credibility)
/offer-auditor --module positioning   # D14-D16 (Audience + Audit Score + Competitor)
```

**Examples:**
- `/offer-auditor` — Full offer quality audit
- `/offer-auditor --module value` — Check value prop and differentiation only
- `/offer-auditor --module trust` — Check risk removal, social proof, credibility

---

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `context/business.md` | Yes | Core input — vertical, offer description, pricing, guarantees |
| `context/brand.md` | Yes | Brand context — value prop, USPs, trust signals, target audience |
| `context/offer-angles.md` | For D15 angles | If exists, validate angle quality |
| `context/competitor-ads/*.csv` | For D16 | Competitor offer comparison |
| `context/account-changelog.md` | Recommended | Recent changes |

---

## Process

---

### Phase 0: Prerequisites & Route

1. **Parse subcommand:**
   - `--module value` → D01-D06 only
   - `--module urgency` → D07-D08 only
   - `--module trust` → D09-D13 only
   - `--module positioning` → D14-D16 only
   - No subcommand (default) → run all 16 diagnostics

2. **Load business.md** — extract and display:
   - Vertical (ecommerce / lead gen / SaaS)
   - Offer-related sections
   - Last Updated date
   - If business.md is missing, STOP: tell user to run `/business-context-gatherer` first

3. **Load brand.md** — extract:
   - Value proposition, USPs, trust signals, guarantees, pricing
   - Target audience
   - If brand.md is missing, STOP: tell user to run `/ads-context-gatherer [URL]` first

4. **Check account-changelog.md** — scan for recent offer, pricing, or landing page changes.

Display configuration:
```
Offer Audit Configuration:
  Account: {client name}
  Vertical: {vertical}
  Module: {value / urgency / trust / positioning / full}
  business.md Last Updated: {date} ({X} days ago)
  brand.md: {present / missing}
```

---

### Phase 1: Vertical Detection

Determine vertical from business.md. All 16 diagnostics run for all verticals — unlike strategy-specialist, offer quality is universal.

However, some diagnostics have vertical-specific evaluation criteria. Read `reference/diagnostic-rules-offer-quality.md` for per-diagnostic vertical notes.

---

### Phase 2: Run Diagnostics

**Read `reference/diagnostic-rules-offer-quality.md`.**

For each diagnostic in the requested module:

1. Check if the required data exists in business.md and/or brand.md
2. If data exists → evaluate against criteria → assign PASS / WARN / FAIL
3. If data is missing → assign ASK status
4. Record details for the report

**For D15 (Offer Audit Checklist Score):**
- Read `reference/offer-audit-checklist.md`
- Run the 15-check audit internally against available data
- Score: 12+ = PASS, 8-11 = WARN, <8 = FAIL

**For D16 (Competitor Offer Comparison):**
- Check if `context/competitor-ads/*.csv` exists
- If yes: extract competitor offers and compare across 4 pillars
- If no: ASK — suggest running `/competitor-scraper [domain]` first

After running all diagnostics in a module, display results table:

```
Offer Quality Results:
| ID | Diagnostic | Status | Pts | Details |
|----|-----------|--------|-----|---------|
| D01 | Value proposition clarity | PASS | 10/10 | Clear and specific |
| D02 | Dream outcome specificity | WARN | 5/10 | Present but not quantified |
...

Module score: X/Y (Z%) — {grade}
```

---

### Phase 2.5: Interview Gate

After initial diagnostic pass, if any diagnostics have ASK status:

1. **Present the batch using AskUserQuestion:** Ask "I found {X} items that need your input — want to provide the data now?" with options: "Yes, let's fill them in" / "Skip for now".

2. **If user chooses to provide data:** For each ASK item, use AskUserQuestion with:
   - A clear question (what you need to know)
   - 2-4 example answers as selectable options based on the vertical and context you've seen (e.g., for D02 dream outcome: "20-slide deck in 2 minutes", "80% less time on slides", "Create presentations 10x faster")
   - The user can always pick "Other" for custom input

3. **If user provides data:**
   - Re-run affected diagnostics with new data
   - Ask: "Want me to update business.md with this data?"
   - If yes, update the relevant section

3. **If user skips:**
   - Mark as SKIP, exclude from scoring denominator

---

### Phase 3: Score & Log

**Scoring:**

| Severity | Points |
|----------|--------|
| Critical | 10 |
| High | 10 |
| Medium | 5 |

SKIP and ASK (unresolved) diagnostics are excluded from the scoring denominator.

**Grade scale:**
- 90-100%: Excellent
- 70-89%: Good
- 50-69%: Needs Attention
- 0-49%: Critical

**Append to log:** Write entry to `context/analysis/offer-audit-log.md` using format from `reference/report-template.md`.

---

### Phase 3.5: Peer Report Lookup (MANDATORY before writing the report)

**Don't send the user from one door to the other.** Before recommending any peer-skill handoff in Phase 4, check whether that peer has already produced a fresh report — and if so, **read it and integrate its findings into THIS report** instead of asking the user to re-run.

The whole point of cross-skill awareness is that a user who runs `/lp-audit` last week and then runs `/offer-audit` this week sees the LP findings *quoted inside the offer report*, not a redundant "go run LP audit" instruction. Re-running an auditor that already produced a fresh answer wastes time and obscures the offer-side action. Offer quality and LP quality overlap heavily (the offer lives on the LP), so peer integration with `/lp-auditor` should be especially tight — quote concrete LP findings (missing guarantee placement, weak hero value prop, generic CTA copy) inline rather than handing off blindly.

#### Freshness windows

| Peer skill | Report file | Fresh window |
|---|---|---|
| `/quality-score-auditor` | `context/analysis/quality-score-audit.md` | ≤ 7 days |
| `/search-term-auditor` | `context/analysis/search-term-audit.md` | ≤ 7 days |
| `/keyword-auditor` | `context/analysis/keyword-audit.md` | ≤ 7 days |
| `/budget-auditor` | `context/analysis/budget-audit.md` | ≤ 7 days |
| `/bidding-auditor` | `context/analysis/bidding-audit.md` | ≤ 7 days |
| `/competitive-analyst` | `context/analysis/competitive-audit.md` | ≤ 14 days |
| `/lp-auditor` | `context/analysis/lp-audit.md` | ≤ 14 days |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days |
| `/strategy-specialist` | `context/analysis/strategy-audit.md` | ≤ 30 days |
| `/account-auditor` | `context/analysis/account-audit.md` | ≤ 30 days |

#### Procedure for each peer that the routing would otherwise hand off to

1. **Check if the file exists.** If not → keep the handoff as a plain "run `/peer-skill`" line.
2. **If it exists, check the date in the report header against the freshness window.** The report header date is canonical. mtime is a sanity check — if mtime is *older* than the header date, warn the user that something is off.
3. **If fresh:** open the report and read its **executive read / top findings / module scores**. Pull out the 1–3 findings that overlap with this audit's offer hypotheses (value prop, guarantee, urgency, social proof, audience clarity, CTA quality, message match). Use them to:
   - **Enrich the Executive read at the top of `offer-audit.md`** — quote the peer's score, the headline finding, and the date inline.
   - **Replace** the routing line "run `/peer-skill`" with: **"Review the existing {date} {peer} report at {path} — top finding: '{one-liner}'. Re-run only if you want fresher data."**
   - In Critical Issues / Recommendations / Next Steps, when a peer handoff is the recommended action, quote the peer's specific finding so the user can act without leaving this report.
4. **If stale:** mention "a previous {peer} report exists from {date} but is {N} days old — recommend re-running before relying on it" and keep the handoff as a re-run.
5. **If missing:** standard "run `/peer-skill`" handoff.

#### When a fresh peer report contradicts an offer hypothesis

Say so explicitly in the Executive read. Example: offer-auditor flags weak social proof (D11/D12) — but the fresh `/lp-auditor` report shows the LP's testimonial section is buried below the fold. The offer content may be fine; the *placement* on the LP is the real lever. **The offer report must surface the contradiction, not silently propose offer rewrites.**

Another example: offer-auditor flags weak urgency (D07/D08) — but the fresh `/quality-score-auditor` report shows the campaigns are losing impression share to budget, not relevance. The urgency finding may not be what's costing conversions. Surface it; never auto-defer or auto-override.

That cross-skill validation is the entire reason this phase exists. An offer audit that ignores a fresh LP, QS, or tracking audit produces a confidently-wrong recommendation.

---

### Phase 4: Write Report

Write full report to `context/analysis/offer-audit.md` using template from `reference/report-template.md`.

This file is regenerated on each run (overwrites previous). The log file preserves history.

**Lead with the Executive read** — the 6-slot prose contract defined in `reference/report-template.md`. Apply Phase 3.5 lookup results to slot 4 (inline-quoted fresh peer findings) and to every Next Steps / Recommendations line that points to a peer skill.

Fill in sections in this order:
1. **Executive read** (prose, ≤300 words, no bullets) — score meaning, 1–3 priorities w/ why, what's NOT a problem, fresh peer findings inline, how-to-read, score trend.
2. Overall score + module breakdown
3. Offer Quality Results (full diagnostic table)
4. Critical Issues — quote peer findings inline when they overlap
5. Recommendations — apply Phase 3.5 results: every line says either "run /peer" (missing/stale) or "review existing {date} report at {path}" (fresh, with the one-liner finding)
6. Next Steps — same Phase 3.5 logic for any peer-skill handoffs
7. Data freshness

---

### Phase 5: Summary & Next Steps

Already written in Phase 4; Phase 5 is the user-facing presentation. The reader should be able to act from the **Executive read alone** — that's the bar. Everything else is reference material.

Print to user in this order:

1. **Executive read** (the prose section from the report — quote it verbatim, don't re-summarize). It already covers score-meaning, this-week priorities w/ why, what's-NOT-a-problem, fresh peer findings inline, how-to-read, score trend.
2. Overall score, grade, module, run timestamp
3. Top 3 issues (FAIL items first, then WARNs) with specific fix actions
4. Suggested next action via offer-maker commands AND peer-report references — apply Phase 3.5 lookup results to every peer line. Each peer handoff says either "review existing {date} report at {path} (top finding: ...)" or "run `/peer-skill`".
5. Note location of full report: `context/analysis/offer-audit.md`

**DIAGNOSE → offer-maker bridge:**

| DIAGNOSE Result | Suggested Action |
|----------------|------------------|
| D01-D06 FAIL (value/uniqueness weak) | "Run `/offer-maker create` to redesign your offer" |
| D07-D08 FAIL (no urgency) | "Run `/offer-maker create` and focus on the Urgency pillar" |
| D09-D13 FAIL (trust gaps) | "Run `/offer-maker create` and focus on the Trust pillar" |
| D14 FAIL (audience unclear) | "Run `/offer-maker angles` to sharpen audience targeting" |
| D15 FAIL (low audit score) | "Run `/offer-maker create` — offer needs fundamental work" |
| D16 FAIL (no competitor comparison) | "Run `/offer-maker competitor` to benchmark your offer" |
| All PASS | "Offer foundation is solid — run `/offer-maker angles` to extract message angles for RSAs" |

**Log to memory:** Append entry to `context/memory/YYYY-MM-DD.md` using format from `reference/report-template.md`.

---

## Integration Points

### Uses (reads from):
- `context/business.md` — Primary data source
- `context/brand.md` — Brand context and trust signals
- `context/offer-angles.md` — Angle quality check (if exists)
- `context/competitor-ads/*.csv` — Competitor comparison (D16)

### Produces (writes to):
- `context/analysis/offer-audit.md` — Full audit report
- `context/analysis/offer-audit-log.md` — Append-only log

### Downstream:
- `/offer-maker` — Suggested for fixing FAIL/WARN items

---

## Output Location

- Report: `context/analysis/offer-audit.md`
- Log: `context/analysis/offer-audit-log.md`
- Memory: `context/memory/YYYY-MM-DD.md`
