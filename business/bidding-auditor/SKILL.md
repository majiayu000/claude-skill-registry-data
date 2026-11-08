---
name: bidding-auditor
description: >
  Audit bid strategy, target validation, learning state, portfolio health, CPC trends,
  bid adjustments, and conversion value rules across 26 diagnostics in 7 modules.
  Scores 0-100 per module, never mutates the account.
  AUTO-ACTIVATE for: "bidding audit", "bid strategy audit", "tCPA audit", "tROAS audit",
  "smart bidding audit", "bid target review", "portfolio strategy review",
  "bid simulator opportunities".
argument-hint: "[module] [period]"
---

# Bidding Auditor

Diagnose-only skill that scores account-wide bid strategy and target health across 26 diagnostics organized into 7 modules. Read-only — never modifies the account.

**Scores 0-100** weighted across:
1. Target Validation (25 pts)
2. Strategy Selection (20 pts)
3. Learning Phase (15 pts)
4. Portfolio Health (15 pts)
5. CPC & Cost Health (10 pts)
6. Conversion Value Rules (10 pts)
7. Bid Adjustments (5 pts)

**Diagnostic ≠ recommendation.** Phase 1.5 walks the constraint cascade **Measurement → Business → Volume → Efficiency → Conversion → Budget → Competitive → Structural → Traffic** before any action is written. Pausing campaigns, switching strategies, or moving targets are all last-resort actions — see `reference/synthesis-playbook.md`.

**Handoff:** Findings route through `reference/handoff-matrix.md`. Two layers are blocking: Measurement (`/tracking-specialist`) and Business (`/strategy-audit --execute unit-economics`). The optimizer hard-refuses any mutation while a blocking layer is active.

---

## Command Routing

```
/bidding-auditor                              → Full audit (all 7 modules)
/bidding-auditor strategy                     → Module 1 only (BID-D01–D04)
/bidding-auditor targets                      → Module 2 only (BID-D05–D09)
/bidding-auditor learning                     → Module 3 only (BID-D10–D13)
/bidding-auditor portfolio                    → Module 4 only (BID-D14–D17)
/bidding-auditor adjustments                  → Module 5 only (BID-D18–D21)
/bidding-auditor cpc                          → Module 6 only (BID-D22–D24)
/bidding-auditor value-rules                  → Module 7 only (BID-D25–D26)
/bidding-auditor opportunities                → Cross-cutting opportunity-only report
/bidding-auditor learning-state               → Learning state table only
/bidding-auditor reconfirm                    → Re-run Phase 0 interview
/bidding-auditor {30|60|90}                   → Custom audit window
/bidding-auditor {module} {period}            → Module + period combination
/bidding-auditor experiments                  → Include Experiment campaigns (skips Phase 0 ask)
```

Default evaluation period: **30 days**. Options: 30, 60, 90.

**Scope filters (always-on):** Removed and paused campaigns are excluded at the GAQL layer (`campaign.status = 'ENABLED'`) — no data is pulled for them.

**Experiment campaigns:** excluded by default. Pass `experiments` (or set `biddingAudit.includeExperiments: true` in `config/ads-context.config.json`) to include drafts/experiments/A-B test variants. The filter is `campaign.experiment_type = 'BASE'`, so ended/promoted/graduated experiment campaigns — which carry an `EXPERIMENT` type and typically end up `REMOVED` — are doubly excluded by default. The `experiments` token can be combined with any other arg (e.g. `targets 60 experiments`).

---

## Phase 0: Prerequisites & Data Collection

### Phase 0.0: Business Context Resolution

**Read:** `config/ads-context.config.json → biddingAudit`. See `reference/configuration.md` for the schema.

**Branch A — Cached values fresh** (`lastConfirmed` exists, `businessMdHash` matches current `business.md` hash, <60 days old):

> CPA mode: "Using cached bidding context: primary KPI **CPA**, break-even **${breakEvenCPA}**, posture **${posture}** (PAR target ${parTarget}), last confirmed ${lastConfirmed}. Proceed? (y / update)"
>
> ROAS mode: "Using cached bidding context: primary KPI **ROAS**, break-even **${breakEvenROAS}**, posture **${posture}** (PAR target ${parTarget}), last confirmed ${lastConfirmed}. Proceed? (y / update)"

If "y" → continue to Phase 0.1. Otherwise → Branch B.

**Branch B — First run, stale, or `reconfirm` requested:**

1. **Read `context/business.md`.** Form a draft for each field below. If a concept isn't present, leave the draft blank.

2. **HARD BLOCK — early exit if unit economics are missing/placeholder.**

   > "Bidding audit requires unit economics in `business.md`. Run `/strategy-audit --execute unit-economics` first to populate, then return here."

   Stop. Do NOT fall back, do NOT continue. This is the single biggest difference vs. budget-auditor — bidding without break-even is meaningless because half the diagnostics depend on it.

3. **Determine the primary KPI.** Read `searchTermAnalysis.biddingStrategy` if present. Otherwise infer from dominant strategy types across campaigns (TARGET_CPA / MAXIMIZE_CONVERSIONS → "cpa"; TARGET_ROAS / MAXIMIZE_CONVERSION_VALUE → "roas"). Confirm with user.

4. **Present draft → user interview:**

   > "Confirming bidding context for the audit:
   > **1. Primary KPI:** ${draft_kpi}
   > **2. Break-even ${kpi}:** ${draft_break_even} — Source: "${quoted_snippet}"
   > **3. Conversion action values:**
   >    - ${action_1}: ${value_1} (primary? y/n)
   >    - ${action_2}: ${value_2} (primary? y/n)
   > **4. Growth-efficiency posture:** growth (PAR 1.2) / balanced (PAR 1.5) / efficiency (PAR 2.0)?
   > **5. tCPA safety margin:** default 0.7 — accept or override?
   >
   > Reply field-by-field or paste corrected values. I'll save to ads-context.config.json."

5. **Action name alignment:** values written to `conversionActionValues` must exactly match strings in `googleAds.conversionActions` (case-sensitive). Note alignment to user before saving.

6. **Write to `biddingAudit` block:** primaryKPI, breakEvenCPA or breakEvenROAS, conversionActionValues, primaryConversionAction, growthEfficiencyPosture, parTarget (derived from posture), tCpaSafetyMargin, lastConfirmed=today, businessMdHash. Static defaults stay untouched unless user overrides.

### Phase 0.1: Config Validation

Verify required fields exist:
- `primaryKPI` ∈ {"cpa", "roas"}
- The matching break-even (`breakEvenCPA` for cpa, `breakEvenROAS` for roas)
- `conversionActionValues`, `primaryConversionAction`
- `growthEfficiencyPosture`, `parTarget`

If any missing → re-run Phase 0.0 Branch B.

### Phase 0.2: Data Freshness

Two checks:
1. **gads-context** (24h max age) — same pattern as keyword-auditor.
2. **`context/account-changelog.md`** — read the file's mtime + the date in its header.
   - Auditor: max 24h old → if stale, prompt "Account changelog is {N}d old. Refresh first via /account-changelog? (y/skip)".
   - Optimizer: 1h hard requirement, mandatory auto-pull (handled by the optimizer skill).

### Phase 0.2.5: Experiment Scope

Default scope is **enabled base campaigns only** — removed/paused campaigns are filtered at the GAQL layer, and experiment campaigns (`experiment_type ≠ 'BASE'`) are excluded so ended/promoted/graduated tests don't pollute strategy, learning, or CPC analysis.

If the user did NOT pass `experiments` AND `biddingAudit.includeExperiments` is not `true` in `config/ads-context.config.json`, ask once:

> "Include Experiment campaigns (drafts/experiments/A-B variants) in the bidding audit? Default: no — only enabled base campaigns. Ended experiments are always excluded because they're already REMOVED in the account."

Skip the ask when either signal is already present. Track the resolved value as `includeExperiments` and pass `--include-experiments` to `pull-all.js` when true.

### Phase 0.3: Module-Scope Determination

Parse the subcommand to decide which queries to pull:

| Subcommand | Queries |
|---|---|
| (full)      | all 6 |
| strategy    | bidding-strategies + campaigns-bidding-perf |
| targets     | campaigns-bidding-perf + campaigns-bidding-daily |
| learning    | bidding-strategies + campaigns-bidding-perf + data-exclusions + account-changelog |
| portfolio   | bidding-strategies + campaigns-bidding-perf |
| adjustments | campaigns-criteria |
| cpc         | campaigns-bidding-daily |
| value-rules | conversion-value-rules |

### Phase 0.4: Data Pull

Run scoped batch pull:

```bash
node .claude/skills/bidding-auditor/scripts/pull-all.js \
  --period={evaluationPeriod} --lag={conversionLagDays} --module={moduleScope} \
  [--include-experiments]
```

Append `--include-experiments` only when the user opted in (Phase 0.2.5).

The script writes CSVs to `context/google-ads/data/`. It prints `__RESULTS_JSON__` on the last line — parse to report totals.

Tell the user: "Pulled {N} campaigns ({M} portfolios, {V} value rules). Running analysis..."

---

## Phase 1: Run Diagnostics

Read each module's diagnostic-rules file:
- `reference/diagnostic-rules-strategy.md` (Module 1)
- `reference/diagnostic-rules-targets.md` (Module 2)
- `reference/diagnostic-rules-learning.md` (Module 3)
- `reference/diagnostic-rules-portfolio.md` (Module 4)
- `reference/diagnostic-rules-adjustments.md` (Module 5)
- `reference/diagnostic-rules-cpc.md` (Module 6)
- `reference/diagnostic-rules-value-rules.md` (Module 7)

Dispatch to engines based on module scope:

```bash
# Modules 1+2 (also writes opportunities for BID-D09)
node .claude/skills/bidding-auditor/scripts/analyze-strategy-targets.js \
  --period={period}

# Modules 3+6 (also writes opportunities for BID-D24, learning-state.csv)
node .claude/skills/bidding-auditor/scripts/analyze-temporal.js \
  --period={period}

# Modules 4+7
node .claude/skills/bidding-auditor/scripts/analyze-portfolio.js

# Module 5
node .claude/skills/bidding-auditor/scripts/analyze-adjustments.js
```

Each engine writes `findings-{engine}.json` plus optional opportunities and CSVs to `context/analysis/bidding/` and `context/google-ads/data/`.

**Read the findings JSONs**, then assign verdicts:

| Verdict | Meaning |
|---|---|
| PASS | full points retained |
| WARN | 40% deduction |
| FAIL | 100% deduction |
| SKIP | excluded from scoring (denominator reduced) |
| INFO | no points at stake |

---

## Phase 1.5: Synthesis & Constraint Cascade (MANDATORY)

**Read `reference/synthesis-playbook.md` in full before writing any recommendation.** Skipping this phase produces mechanically-correct but strategically-wrong reports (e.g., "lower the tCPA on every flagged campaign" when the real issue is broken tracking).

Output: a ranked hypothesis list, each with:
- layer (M / B / Vol / Eff / Conv / Bud / Comp / Struct / T)
- evidence (which diagnostics)
- confidence (low/medium/high)
- whether it blocks downstream actions

### Required checks

1. **M layer** — BID-D26 fires; tracking-specialist has unresolved findings on flagged campaigns. Active → blocks all target/strategy mutations.
2. **B layer** — break-even missing/placeholder; primary KPI undefined. Active → blocks target validation.
3. **Vol layer** — BID-D03 fires. Trigger sub-cascade with options menu.
4. **Eff layer** — search-term waste, low QS, weak RSAs depressing CVR.
5. **Conv layer** — LP/offer driving low CVR.
6. **Bud layer** — budget-lost IS > 30% on flagged campaigns; or BID-D17 conflict.
7. **Comp layer** — BID-D22 / BID-D23 fire.
8. **Struct layer** — BID-D11 / BID-D14 fire.
9. **T layer** — pure bidding action only after all higher layers cleared or explicitly overridden.

### Anti-patterns

- Never recommend a target change while M or B is blocking. Replace with the handoff.
- Never recommend stacking strategy + target changes on the same campaign in one session.
- Never recommend a target step >20% (or >30% with `--aggressive`).
- Never write a flat actions table that mixes a tracking handoff with a tCPA tweak — segment by cascade state.

---

## Phase 2: Score & Report

Read `reference/scoring-model.md` for the model. Compute:
- module sub-scores (after deductions)
- N/A redistribution if any module SKIPs entirely (no portfolios, no value rules, all-smart-bidding accounts)
- weighted total

### Bands

| Score | Grade |
|---|---|
| 90–100 | Excellent |
| 75–89  | Good |
| 60–74  | Needs Attention |
| <60    | Critical |

### Write report to `context/analysis/bidding-audit.md`

Read `reference/report-template.md` for the structure. The report is hypothesis-organized, not diagnostic-organized:

1. **Diagnosis** — one paragraph naming the cascade layer + root cause.
2. **Top hypothesis** — name, layer, evidence, confidence.
3. **Module scores** — 7-row table.
4. **Risks — segmented:** 🔍 Investigate first / 🔧 Structural fix / 🔄 Recover efficiency / ✅ Act now / ⚠️ Hold (in learning).
5. **Opportunities** — cross-cutting list (always present, even on healthy accounts).
6. **Learning State** — permanent fixture table.
7. **Module details** — full per-diagnostic breakdown.

### Append to `context/analysis/bidding-audit-log.md`:

```markdown
## {date} — Score: {score}/100 ({grade})
- Period: {period}d | Campaigns: {n}
- Top hypothesis: {layer} — {name}
- Active blocking: {list or "none"}
- Top finding: {1-line}
```

---

## Phase 3: Opportunities Pass (unconditional)

Always run, even on zero-risk accounts. Cross-cutting opportunities surfaced by `analyze-strategy-targets` (BID-D09 starvation recovery, BID-D24 budget-lost recovery) and `analyze-temporal` (BID-D24 simulator gap heuristic) get merged into a single ranked list.

Each opportunity entry includes: type, campaign, projected impact (e.g. "+12 conv/30d at $X CPA"), and recommended action (which optimizer subcommand or peer skill).

---

## Phase 3.5: Peer Report Lookup (MANDATORY before handoff)

**Don't send the user from one door to the other.** Before recommending any peer-skill handoff in Phase 4, check whether that peer has already produced a fresh report — and if so, *read it and use its findings* instead of asking the user to re-run.

For each peer skill that the cascade would otherwise hand off to, follow this lookup:

| Peer skill | Report file | Fresh window |
|---|---|---|
| `/quality-score-auditor` | `context/analysis/quality-score-audit.md` | ≤ 7 days |
| `/search-term-auditor` | `context/analysis/search-term-audit.md` | ≤ 7 days |
| `/keyword-auditor` | `context/analysis/keyword-audit.md` | ≤ 7 days |
| `/competitive-analyst` | `context/analysis/competitive-audit.md` | ≤ 14 days |
| `/lp-auditor` | `context/analysis/lp-audit.md` | ≤ 14 days |
| `/offer-auditor` | `context/analysis/offer-audit.md` | ≤ 30 days |
| `/budget-auditor` | `context/analysis/budget-audit.md` | ≤ 7 days |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days |
| `/strategy-audit` | `context/analysis/strategy-audit.md` | ≤ 30 days |
| `/account-auditor` | `context/analysis/account-audit.md` | ≤ 30 days |

**Procedure for each relevant peer:**

1. Check if the file exists. If not → keep the handoff as "run `/peer-skill`".
2. If it exists, check mtime against the fresh window above.
3. **If fresh:** read the report's executive read / top hypothesis / module scores. Pull out the 1–3 findings that overlap with the bidding-auditor's flagged campaigns or hypotheses. Use them to:
   - Enrich the **Executive read** at the top of `bidding-audit.md` (quote the score and the headline finding, with date).
   - Replace "run `/peer-skill`" in the Phase 4 handoff with **"review the existing {date} report at {path} — top finding was: {one-liner}. Re-run only if you want fresh data."**
4. **If stale:** mention "a previous {peer} report exists from {date} but is {N} days old — recommend re-running before relying on it" and keep the handoff as a re-run.
5. **If missing:** standard "run `/peer-skill`" handoff.

The goal is that a user re-running `/bidding-auditor` after already having run `/quality-score-auditor` last week sees the QS findings *integrated into this report*, not a redundant "go run QS" instruction.

When the relevant peer report is fresh and contradicts or contextualizes a bidding hypothesis (e.g., bidding-auditor sees high rank-lost IS and the fresh QS report already explains why), say so explicitly in the Executive read — that's the whole point of cross-skill awareness.

---

## Phase 4: Sequenced Handoff Offer

Read `reference/handoff-matrix.md`. Always sequence by cascade priority — **never** present as a flat menu. Apply the Phase 3.5 lookup results to each handoff line: if a fresh peer report exists, the line becomes "review existing report" not "run new audit".

Template when an upstream hypothesis is active:

> **Top hypothesis:** {layer} — {name} (explains ~{pct}% of flagged risk)
>
> Before any target or strategy change, here's what I'd run in order:
>
> 1. **{blocking M handoff}** — {why} → `/{skill}`
> 2. **{B handoff}** — {why} → `/{skill}`
> 3. **{Eff layer}** — search-term/keyword/QS first → `/search-term-auditor`, `/quality-score-auditor`
> 4. **{Conv layer}** — LP/offer recovery → `/lp-auditor`, `/offer-auditor`
> 5. **{Bud peer}** — `/budget-auditor`
> 6. **{T layer — bidding actions only after the above}**
>    - {N} target adjustments → `/bidding-optimizer adjust-targets`
>    - {M} migrations → Manual: Google Ads UI → Drafts & Experiments (50/50, 14–30d, promote on KPI win)
>    - structural fixes → `/bidding-optimizer fix-shared-portfolio`, `/bidding-optimizer cpc-cap`

When all higher layers are clear:

> "Cascade clears 1–8 are green. Ordered by priority:
>
> - **Always-safe structural:** `/bidding-optimizer fix-shared-portfolio`, `/bidding-optimizer remove-adjustments`
> - **Target adjustments (within 20% step cap):** `/bidding-optimizer adjust-targets`
> - **Migrations (experiment-based):** Manual via Google Ads UI → Drafts & Experiments (50/50, 14–30d, promote on KPI win)
> - **Scale (paired with budget):** `/bidding-optimizer scale` + `/budget-optimizer raise`"

Only show subcommands with findings to act on.

---

## Phase 5: Report Generation

Already written in Phase 2. Phase 5 is the user-facing presentation. Lead with the **Executive read** (the plain-English section at the top of the report), then the structured artifacts. The goal is a reply the user can act on without opening the full report:

1. **Executive read** (2–4 short paragraphs, prose). What the score actually means, the 1–3 things to do this week with the *why*, what is NOT a problem and why red findings can be ignored (zombies, deliberate Manual CPC, N/A modules), and one line on how to read the rest. No bullet lists in this opening — flowing prose. Match `report-template.md` Executive read guidance.
2. Score, grade, window, run timestamp.
3. Top hypothesis row (one line).
4. 7-row module scores.
5. Sequenced handoff offer (Phase 4 template).
6. Note location of full report: `context/analysis/bidding-audit.md`.

The Executive read should already exist as the first section of the written report from Phase 2 — if it's missing, write it before printing.

---

## Edge Cases

| Scenario | Handling |
|---|---|
| No portfolios in account | Module 4 marked SKIP entirely; 15 pts redistribute proportionally. |
| No mCPC campaigns | Module 5 SKIP; 5 pts redistribute (small effect). |
| No conversion value rules | Module 7 SKIP; 10 pts redistribute. |
| All-smart-bidding accounts | Modules 5+7 both N/A → 15 pts redistribute. |
| Single-campaign account | Cross-portfolio checks SKIP; note in report. |
| account-changelog missing or >24h | Surface to user; learning-state findings degrade to INFO until refreshed. |
| business.md missing unit economics | Phase 0 hard-blocks. No fallback. |
| Campaign in learning (<14d since change) | BID-D11/D13 fire WARN; optimizer hard-refuses any mutation. |
| Portfolio strategy with no inline target | Auditor resolves via bidding-strategies.csv; finding meta carries `target_source: portfolio`. |
| Conversion lag > evaluation window | Re-run with longer window — surface as M3 hypothesis. |
| Currency other than USD | All money columns formatted via top-level `accountCurrency` if set; otherwise USD default. |
| API rate limit | pull-all.js delegates to query.js which already retries; surfaces error, exits 1. |
| Recently created campaign (<14d) | Engines mark INFO with "new — monitoring" note. |
