---
name: lp-optimizer
description: Optimize landing pages with actionable fix-it guidance. Reads lp-auditor output and examines issues via Chrome DevTools. Use to fix LPs, improve CVR, or get CRO recommendations.
argument-hint: "[action]"
---

# LP Optimizer Skill

Reads the lp-auditor's output, deep-dives into specific issues via Chrome DevTools, and produces actionable fix-it guidance reports. Each action focuses on one problem area.

**Not built by this skill (per de-duplication log):**
- New LP wireframes from scratch --> landing-page-builder (`/landing-page-builder`)
- New ecommerce page wireframes --> ecom-page-builder (`/ecom-page-builder`)
- LP scoring/auditing --> lp-auditor (`/lp-auditor`)
- Conversion tracking setup --> tracking-specialist (`/tracking-specialist`)
- Ad copy quality --> ad-copy-specialist
- Offer quality --> offer-auditor (`/offer-auditor`)

## Command Format

```
/lp-optimizer                       # Menu: show available actions based on last audit
/lp-optimizer audit                 # LP-E04: Full optimization guidance (reads audit report)
/lp-optimizer cart                  # LP-E05: Cart & checkout optimization guide
/lp-optimizer urls                  # LP-E06: Fix broken URLs (reads URL health results)
/lp-optimizer speed                 # LP-E07: Page speed improvement guide
/lp-optimizer mobile                # LP-E08: Mobile experience improvement guide
/lp-optimizer message-match         # LP-E09: Fix message match gaps
/lp-optimizer forms                 # LP-E10: Reduce form friction
/lp-optimizer elements              # LP-E11: Add missing conversion elements
/lp-optimizer ab-test               # LP-E12: A/B test plan
/lp-optimizer monitor               # LP-E13: Set up LP performance monitoring
/lp-optimizer tracking              # LP-E14: LP-specific conversion tracking guide
```

All subcommands accept an optional `--url=https://...` flag to pre-load a target URL.

**Examples:**
- `/lp-optimizer` -- Interactive menu, recommends actions based on audit findings
- `/lp-optimizer speed --url=https://example.com` -- Speed improvement guide for specific URL
- `/lp-optimizer audit` -- Full optimization guidance from audit report
- `/lp-optimizer message-match` -- Fix ad-to-LP alignment issues

---

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `context/analysis/lp-audit.md` | Strongly recommended | Auditor's scored findings — drives prioritization |
| `context/business.md` | Recommended | Vertical detection (lead gen / SaaS / ecommerce) |
| `context/google-ads/data/ads.csv` | For message-match, audit, urls | Ad headlines, descriptions, final URLs |
| `context/google-ads/data/keywords.csv` | For message-match | Keywords mapped to ad groups |
| `context/google-ads/data/device-performance.csv` | For mobile, audit | Device-level CVR comparison |
| `context/google-ads/data/assets.csv` | For urls | Sitelink URLs, asset URLs |
| `context/offer-angles.md` | For elements, message-match | Offer messaging angles |
| Chrome DevTools MCP server | For most actions | Page inspection, Lighthouse, screenshots, DOM analysis |
| `context/account-changelog.md` | For Phase 0.5 mutation-sensitivity | Recent peer mutations (read only if ≤ 7d old; never auto-pull) |
| Peer audit reports under `context/analysis/` | For Phase 0.5 pre-flight + report enrichment | See `reference/handoff-matrix.md` § 1 for the 10-peer table |

---

## Process

---

### Phase 0: Load Context & Route

**0.0 — Quality Score Auditor handoff check**

Before routing, check whether the user recently ran `/quality-score-auditor`:

1. Check `context/analysis/quality-score-audit.md` exists AND was modified in the last 7 days.
2. If yes, read the `## Handoff Queue — LP Experience (→ /lp-optimizer)` section. Table columns: `final_url | ad_groups | keywords_below_avg | impressions | class_mix | recommended_action`.
3. If the queue has rows, surface to the user:

   > "**QS Auditor handoff active.** {N} LP URLs flagged with Below-Avg LP Experience, affecting {M} keywords / {impressions} impressions. The QS auditor recommends: `{recommended_action}` (usually `message-match`, `speed`, `mobile`, or `elements`). Run `/lp-optimize {recommended_subcommand} --url={url}` to target the flagged URL directly."

4. **BRANDED-class rows are flagged separately** — these are usually message-match or wrong-URL issues on branded traffic. Open those first (`/lp-optimize message-match`) even if other queue rows look higher-volume; the downside of a broken branded LP is much larger.
5. If the user invokes `/lp-optimize` with no subcommand, use the queue rows to pre-rank the interactive menu (QS-flagged URLs appear at top with an annotation).

If no QS audit exists, skip silently.

**0.1 — Parse subcommand and flags**

1. **Parse subcommand and flags:**
   - `audit` --> LP-E04 (full optimization guidance)
   - `cart` --> LP-E05 (cart & checkout)
   - `urls` --> LP-E06 (fix broken URLs)
   - `speed` --> LP-E07 (page speed)
   - `mobile` --> LP-E08 (mobile experience)
   - `message-match` --> LP-E09 (message match fix)
   - `forms` --> LP-E10 (form friction)
   - `elements` --> LP-E11 (missing conversion elements)
   - `ab-test` --> LP-E12 (A/B test plan)
   - `monitor` --> LP-E13 (performance monitoring)
   - `tracking` --> LP-E14 (LP-specific tracking)
   - No subcommand --> show interactive menu

2. **Check for audit report:**
   - Read `context/analysis/lp-audit.md`
   - If exists: extract relevant findings for the requested action, display summary
   - If missing: inform user they'll get better results by running `/lp-auditor` first, but proceed with standalone analysis

3. **Read `context/business.md`** for vertical context (lead gen / SaaS / ecommerce)

4. **Resolve target URL:**
   - If `--url=` flag provided: use that URL
   - If audit report exists: extract URL(s) from report
   - If neither: ASK user for target URL (except for `urls`, `monitor`, `ab-test` which can work from data only)

5. **If no subcommand, show interactive menu (two-step):**

**Step 1 — Pick a category** using AskUserQuestion:

If audit report exists, include a one-line findings summary in the question text:
`"Audit found: {count} FAIL, {count} WARN across {module names}"`

Options:
- **Fix Issues** — Address audit findings: speed, mobile, forms, broken elements
- **Content Alignment** — Message match with ads, conversion elements, trust signals
- **Testing & Planning** — A/B test plan, monitoring setup
- **Full Optimization** (Recommended when audit exists) — Prioritized fix-it guidance across all findings

**Step 2 — Pick a specific action** using AskUserQuestion:

Present the relevant actions based on the category selected in Step 1:

| Category | Options (pick up to 4) |
|----------|----------------------|
| Fix Issues | Page Speed (LP-E07), Mobile Experience (LP-E08), Form Friction (LP-E10), Fix Broken URLs* |
| Content Alignment | Message Match (LP-E09), Conversion Elements (LP-E11), Cart & Checkout*, Tracking Guide |
| Testing & Planning | A/B Test Plan (LP-E12), Monitoring Setup, Cart & Checkout*, Tracking Guide |
| Full Optimization | Skip Step 2 — proceed directly to LP-E04 |

`*` Conditional options:
- `Cart & Checkout` — only when vertical = ecommerce
- `Fix Broken URLs` — only when URL health issues found in audit
- When a conditional option does not apply, omit it (do not show greyed-out options)
- If fewer than 4 options remain after filtering, that is fine — AskUserQuestion requires minimum 2

Display configuration after selection:
```
LP Optimizer Configuration:
  Vertical: {vertical}
  Action: {action name} (LP-E{XX})
  Target URL: {url or "from audit report" or "data-only mode"}
  Audit Report: {found / not found}
```

---

### Phase 0.5: Peer Pre-flight (cross-skill gate + context)

LP-optimizer is a guidance skill — it doesn't mutate the account directly, but its recommendations shape the implementer's actions. Before producing any recommendation, run the cross-skill peer-lookup to (1) hard-block when upstream M/B layers are dirty and (2) capture peer context to enrich the report.

**Reference:** `reference/handoff-matrix.md` defines the freshness table, the universal hard-block, the mutation-sensitivity matrix, and the cross-skill context block format. Read it once at the start of this phase.

**0.5.1 — Walk the 10-peer freshness table**

For each peer in `handoff-matrix.md` § 1, stat the report file and read the header `**Date:**`. Apply the **freshness rule:** header date is canonical; mtime is tiebreaker only; surface contradictions; never auto-defer.

Build a small peer summary table for internal reasoning:

| Peer | Status | Findings overlapping target URL/campaigns |
|---|---|---|
| /tracking-specialist | fresh / stale / missing | {flagged or clean} |
| /strategy-specialist | fresh / stale / missing | {KPI+breakEven resolved? yes/no} |
| /quality-score-auditor | … | … |
| … | … | … |

**0.5.2 — Universal hard-block check (M and B layers)**

Per `handoff-matrix.md` § 2:

- **M (Measurement):** If `/tracking-specialist` audit is fresh AND has FAIL findings overlapping the campaigns the LP serves — **hard-block**. Surface the hard-block message and stop. If audit is missing entirely AND lp-optimizer has never run on this account, **hard-block** with "Conversion tracking has not been audited. LP recommendations are uncalibrated when CVR cannot be trusted."
- **B (Business):** If `/strategy-specialist` audit is fresh AND `primaryKPI` or `breakEven` is unresolved/placeholder — **hard-block**. If audit is missing entirely, same treatment as M.

When hard-blocked:

> **Pre-flight hard-block — {M or B}.**
> {one-line reason}.
>
> Run `{recommended_handoff}` first, then re-run `/lp-optimize {subcommand}`.
>
> Override (rare): re-run with `--override-measurement --override-reason="..."` or `--override-business --override-reason="..."` if you accept that recommendations will not be measurable / not be calibrated to unit economics.

Stop here unless the user re-invokes with the override flag.

**0.5.3 — Mutation-sensitivity check (soft-warn)**

Read `context/account-changelog.md` if it exists and is ≤ 7 days old. Do **not** auto-pull the changelog — lp-optimizer is a guidance skill, not a mutator. If changelog is missing/stale, log "changelog not consulted — {reason}" and skip this sub-phase.

For each entry, apply the Mutation Sensitivity Matrix in `handoff-matrix.md` § 3. Soft-warn cases:

- Recent ad-copy edits (≤ 7d) on overlapping ad groups → "RSA mid-test, LP+ad-copy signal will be entangled"
- Active QS optimization (≤ 7d) on overlapping ad groups → "QS still moving, LP fix lands on shifting baseline"
- Campaign restructure (≤ 14d) on overlapping campaigns → "traffic mix is shifting, current LP findings reflect pre-restructure traffic"

For each soft-warn, surface inline:

> ⚠ **Recent peer mutation detected.** {one-line warn from the matrix}.
>
> Proceed with LP recommendations? (yes / abort)

User "yes" continues the run; the warns are preserved into Phase 2's Cross-skill Context block. User "abort" stops the run.

**0.5.4 — Capture peer findings for enrichment**

For every peer that is **fresh + dirty + overlaps** the target URL/campaigns, extract 1–3 key findings (with the peer's report date) into a working buffer. These will be rendered into the report's Cross-skill Context block in Phase 2.

If `/quality-score-auditor` flagged LPE on the URL being optimised (which is also the trigger for Phase 0.0's handoff queue), **always** include a chain row: "applying these LP fixes targets QS Auditor's LPE flag — re-run `/quality-score-auditor` 14 days post-implementation to verify recovery."

If no peer is fresh + dirty + overlapping, the working buffer is empty and the Cross-skill Context block will be omitted in Phase 2.

---

### Phase 1: Deep Investigation

Each action loads its specific reference file from `reference/` and uses Chrome DevTools to examine the problem area in depth.

**Important:** The auditor *scored* the issue. The optimizer *diagnoses root causes and provides specific fixes*.

**Load the reference file for the selected action:**

| Action | Reference file |
|--------|---------------|
| LP-E04: Full Optimization | `reference/optimize-methodology.md` |
| LP-E05: Cart & Checkout | `reference/action-cart-checkout.md` |
| LP-E06: Fix URLs | No reference needed -- reads audit URL health data |
| LP-E07: Speed | `reference/action-speed.md` |
| LP-E08: Mobile | `reference/action-mobile.md` |
| LP-E09: Message Match | `reference/action-message-match.md` |
| LP-E10: Forms | `reference/action-forms.md` |
| LP-E11: Elements | `reference/action-elements.md` |
| LP-E12: A/B Test | `reference/action-ab-test.md` |
| LP-E13: Monitoring | `reference/action-monitoring.md` |
| LP-E14: Tracking | No reference needed -- bridges to tracking-specialist |

**Then execute the action-specific investigation per the reference file instructions.**

For actions that use Chrome DevTools (speed, mobile, message-match, forms, elements, cart, full audit):
1. Navigate to target URL
2. Take screenshots of relevant page areas
3. Extract DOM elements relevant to the issue
4. Run Lighthouse if needed (speed, mobile)
5. Emulate mobile if needed (mobile)
6. Analyze findings against the reference file patterns

For data-only actions (urls, monitor, ab-test, tracking):
1. Read relevant Google Ads data files
2. Read audit report findings
3. Cross-reference with reference file methodology

---

### Phase 2: Generate Guidance Report

Each action produces a markdown report following the template in `reference/report-template.md`.

Every report includes these sections:

1. **Cross-skill Context** (NEW — render only when Phase 0.5.4 buffer is non-empty) — Fresh peer findings overlapping the target URL/campaigns + any soft-warns from the mutation-sensitivity matrix. Format per `reference/handoff-matrix.md` § 4. Render this block **immediately after the report header, above Issue Summary** so the implementer sees the cross-skill picture first. When `/quality-score-auditor` flagged LPE on this URL, the block must include the explicit chain row tying the LP fixes to QS recovery.
2. **Issue Summary** -- What's wrong, quantified where possible
3. **Root Cause Analysis** -- Why it's happening (not just symptoms)
4. **Fix Recommendations** -- Specific, actionable, prioritized as:
   - P1 (Quick wins): High impact, low effort -- do immediately
   - P2 (Strategic fixes): High impact, high effort -- schedule next
   - P3 (Optimizations): Lower impact -- batch with other changes
5. **Implementation Notes** -- Who needs to do what (developer, designer, marketer, account manager)
6. **Expected Impact** -- What improvement to expect
7. **Screenshots** -- Before state captured from Chrome DevTools (when applicable)
8. **Next Steps** -- Bridge to other skills/commands. Always include the QS re-audit chain (`re-run /quality-score-auditor 14d after implementation`) when LPE was flagged in the Cross-skill Context block.

**Output file:** `context/analysis/lp-optimize-{action}.md`

Where `{action}` maps to:
- `audit` --> `lp-optimize-audit.md`
- `cart` --> `lp-optimize-cart.md`
- `urls` --> `lp-optimize-urls.md`
- `speed` --> `lp-optimize-speed.md`
- `mobile` --> `lp-optimize-mobile.md`
- `message-match` --> `lp-optimize-message-match.md`
- `forms` --> `lp-optimize-forms.md`
- `elements` --> `lp-optimize-elements.md`
- `ab-test` --> `lp-optimize-ab-test.md`
- `monitor` --> `lp-optimize-monitor.md`
- `tracking` --> `lp-optimize-tracking.md`

---

### Phase 3: Summary & Next Steps

Present to user:

1. **Top recommendations** -- the 3 highest-impact fixes from the report
2. **Implementation priority** -- P1 items with specific instructions
3. **Bridges to other skills:**
   - If rebuild recommended (score < 40%): "Run `/landing-page-builder` to build a new lead gen LP" or "Run `/ecom-page-builder` to build a new product page"
   - If re-audit needed after fixes: "After implementing fixes, run `/lp-auditor` to re-score"
   - If tracking issues found: "Run `/tracking-specialist` to check conversion tracking"
   - If offer is the real problem: "Run `/offer-auditor` to evaluate your offer quality"
   - If ad copy needs alignment: "Run `/rsa-maker` to generate new ad copy matching LP messaging"
4. **Report location** -- `context/analysis/lp-optimize-{action}.md`

**Log to memory:** Write entry to `context/memory/YYYY-MM-DD.md` per memory-logging rules:

```markdown
## LP Optimization Guidance Generated
- Action: {action} (LP-E{XX})
- URL: {url}
- Audit report used: {yes/no, score if yes}
- Top findings: {list of key issues}
- P1 fixes: {count} quick wins identified
- Report: context/analysis/lp-optimize-{action}.md
```
