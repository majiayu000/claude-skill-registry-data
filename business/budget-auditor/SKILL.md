---
name: budget-auditor
description: >
  Audit budget limitation, sufficiency, monthly pacing, allocation, and shared-budget
  health across 19 diagnostics in 5 modules. Scores 0-100 per module, never mutates
  the account.
  AUTO-ACTIVATE for: "budget audit", "budget review", "budget health", "monthly pacing",
  "budget limited campaigns", "budget allocation review", "shared budget audit",
  "budget pacing audit".
argument-hint: "[module] [period] [base-only]"
---

# Budget Auditor

Diagnose-only skill that scores account-wide budget health across 19 diagnostics organized into 5 modules. Read-only — never modifies the account.

**Scores 0-100** weighted across:
1. Allocation (30 pts)
2. Limitation (25 pts)
3. Pacing (15 pts)
4. Sufficiency (15 pts)
5. Shared Budgets (15 pts)

**Diagnostic ≠ recommendation.** Phase 1.5 walks the constraint cascade **Measurement → Business → Bidding → Efficiency → Conversion → Competitive → Structural → Traffic** before any action is written. Raising budget is the most-gated action in the entire skill set; the auditor must form a root-cause hypothesis first — see `reference/synthesis-playbook.md`.

**Handoff:** Findings route through `reference/handoff-matrix.md`. Two layers are blocking — Measurement (`/tracking-specialist`) and Business (`/strategy-specialist`). The optimizer hard-refuses any raise while a blocking layer is active.

**Peer with bidding-specialist.** Budget and bid moves are co-equal levers; this skill owns the budget side only. Target CPA/ROAS adjustments stay with `/bidding-specialist`.

---

## Command Routing

```
/budget-auditor                              → Full audit (all 5 modules) + opportunities
/budget-auditor limitation                   → Module 1 only (BUD-D01–D04)
/budget-auditor sufficiency                  → Module 2 only (BUD-D05–D08)
/budget-auditor pacing                       → Module 3 only (BUD-D09–D12, lighter pull)
/budget-auditor allocation                   → Module 4 only (BUD-D13–D16)
/budget-auditor shared                       → Module 5 only (BUD-D17–D19)
/budget-auditor opportunities                → Cross-cutting opportunity-only report
/budget-auditor reconfirm                    → Re-run Phase 0 interview
/budget-auditor {30|60|90}                   → Custom audit window
/budget-auditor {module} {period}            → Module + period combination
/budget-auditor base-only                    → Exclude active experiment variants (rare; structural audits only)
```

Default evaluation period: **30 days**. Options: 30, 60, 90.

**Scope filters (always-on):** Removed and paused campaigns are excluded at the GAQL layer (`campaign.status = 'ENABLED'` and `campaign.serving_status = 'SERVING'`). No data is pulled for them.

**Experiment campaigns:** **INCLUDED by default** because active experiment variants consume real daily budget — excluding them would under-count spend and break Allocation, Pacing, IS Lost (Budget), and exhaustion-timing math. This inverts bidding-auditor's default.

Pass `base-only` (or set `budgetAudit.includeExperiments: false`) to drop experiment-type rows. Removed/paused campaigns are always excluded regardless. The `base-only` token composes with any other arg (e.g. `/budget-auditor allocation 60 base-only`).

---

## Phase 0: Prerequisites & Data Collection

### Phase 0.0: Business Context Resolution

**Read:** `config/ads-context.config.json → budgetAudit` and top-level `accountCurrency`. See `reference/configuration.md` for the schema.

**Branch A — Cached values fresh** (`lastConfirmed` exists, `businessMdHash` matches the current `business.md` hash, < 60 days old):

> "Using cached budget context: monthly target **${monthlyBudgetTotal} ${accountCurrency}**, ${N} per-campaign overrides, seasonality **${seasonalityProfile.mode}**. Last confirmed ${lastConfirmed}. Proceed? (y / update)"

If "y" → continue to Phase 0.1. Otherwise → Branch B.

**Branch B — First run, stale, or `reconfirm` requested:**

1. **Read `context/business.md`.** Form drafts:
   - `monthlyBudgetTotal` if mentioned
   - currency hint (`USD`, `EUR`, etc.) for the top-level `accountCurrency`
   - any seasonality language ("Black Friday", "Q4 push", "summer slowdown")

2. **Read currently-enabled campaigns** from `context/google-ads/data/`. Compute current monthly run-rate for the read-back baseline.

3. **Show baseline:**
   > "I see ${N} enabled campaigns currently running ~${currentMonthly} ${currency}/month. Account-level monthly target?"

4. **Offer business.md write-back:** if the user provides a number not currently in business.md, ask:
   > "Want me to add this monthly target to business.md so it's the source of truth?"

5. **Optional per-campaign targets:**
   > "Want to set per-campaign targets for the campaigns you actively manage budgets for? (y / skip — defaults to even allocation across the total)"

   When yes, ask for `{ "campaign name": { "monthly": N, "priority": "protect"|"scale"|"hold" } }` for each one.

6. **Seasonality interview:**
   > "Does your business have seasonality? (y / n)"

   If yes:
   > "Which months matter? (e.g., May, November, December)"

   Stored as `seasonalityProfile.mode = "highlight_months"` with a lowercased month list.

7. **Confirm thresholds.** Present the static defaults inline; only override when the user explicitly does. Include `dailyBudgetToCpaRatio`, `overspendAlertPp`, `underspendAlertPp`, `isLostBudgetThreshold`, `maxSingleMutationMultiplier`.

8. **Currency:** If top-level `accountCurrency` is missing, ask:
   > "Account currency? (default USD)"

   Write to top-level config.

9. **Fallback escape hatch:** If the user can't supply `monthlyBudgetTotal`:
   > "No monthly target available — should I run in fallback mode? (Pacing module will be skipped; allocation/limitation/sufficiency/shared still run.) (y / n)"

   On yes, set `targetFallbackMode = "no_monthly_target"`.

10. **Write `budgetAudit` block** + `businessMdHash = sha256(business.md).slice(0,16)` + `lastConfirmed = today`. Static defaults stay untouched unless the user overrode any.

### Phase 0.1: Config Validation

Verify required fields:
- top-level `accountCurrency` (default to "USD" with a one-line warning if missing)
- either `budgetAudit.monthlyBudgetTotal` is set OR `budgetAudit.targetFallbackMode === "no_monthly_target"`

If validation fails → re-run Phase 0.0 Branch B.

### Phase 0.2: Data Freshness

Two checks:

1. **gads-context** — same pattern as keyword-auditor and bidding-auditor. If stale (>24h), prompt to refresh via `/gads-context`.

2. **`context/account-changelog.md`** — read mtime + the date in the file's header.
   - If file missing OR >24h old, prompt:
     > "Account changelog is {N}d old. Refresh first via /account-changelog? (y / skip)"
   - On the FIRST stale prompt of the session, also offer:
     > "Want me to auto-refresh account-changelog whenever it's stale during this session? (y / no, ask each time)"

     If yes, set `budgetAudit.accountChangelogConsentForSession = today` (in-memory; not persisted across sessions).
   - On skip → banner the report: "Change history may be stale — recent budget edits not reflected in diagnostics."

The optimizer enforces a stricter 1-hour freshness on the changelog and auto-refreshes; the auditor's threshold is 24h.

### Phase 0.2.5: Experiment Scope

**Default:** all currently SERVING campaigns — base AND active experiment variants. Inverse of bidding-auditor. Active experiments share/split the daily budget with their base, so excluding them would break spend, IS, and pacing math.

**Filter resolution:**
1. CLI flag `base-only` (or `--include-experiments=false`) → exclude experiment variants.
2. `budgetAudit.includeExperiments === false` → exclude experiment variants.
3. Otherwise → include.

When `EXPERIMENT`-type campaigns are pulled, banner the report:
> "ℹ️ Audit includes ${N} active experiment campaign(s). Spend, IS, and pacing reflect base + experiment serving share."

Module 4 (Allocation) groups experiment rows under their base so a base+experiment pair counts as ONE budget consumer.
Module 5 (Shared Budgets) flags experiment-variant in shared pool as a configuration risk inside BUD-D17.

### Phase 0.3: Module-Scope Determination

Parse the subcommand → choose which queries to pull:

| Subcommand | Queries pulled |
|---|---|
| (full)        | all 5 |
| limitation    | campaign-budgets + campaigns-budget-perf |
| sufficiency   | campaign-budgets + campaigns-budget-perf + campaigns-pacing-daily + bidding-strategies |
| pacing        | campaign-budgets + campaigns-pacing-daily + campaigns-budget-perf + account-budget |
| allocation    | campaign-budgets + campaigns-budget-perf |
| shared        | campaign-budgets + campaigns-budget-perf + bidding-strategies |
| opportunities | campaign-budgets + campaigns-budget-perf + campaigns-pacing-daily |

### Phase 0.4: Data Pull

Run scoped batch pull (default INCLUDES experiments):

```bash
node .claude/skills/budget-auditor/scripts/pull-all.js \
  --period={evaluationPeriod} --lag={conversionLagDays} --module={moduleScope} \
  [--base-only]
```

The script writes CSVs to `context/google-ads/data/`. It prints `__RESULTS_JSON__` on the last line — parse to confirm row counts and the resolved experiment scope.

Tell the user: "Pulled {N} campaigns, {M} budgets, {S} portfolios. Experiments: {INCLUDED|excluded}. Running analysis…"

---

## Phase 1: Run Diagnostics

Read each module's diagnostic-rules file:
- `reference/diagnostic-rules-limitation.md` (Module 1)
- `reference/diagnostic-rules-sufficiency.md` (Module 2)
- `reference/diagnostic-rules-pacing.md` (Module 3)
- `reference/diagnostic-rules-allocation.md` (Module 4)
- `reference/diagnostic-rules-shared.md` (Module 5)

Dispatch to engines based on module scope:

```bash
# Modules 1, 2, 4, 5 — produces findings-health.json + opportunities-health.json
node .claude/skills/budget-auditor/scripts/analyze-budget-health.js \
  --period={evaluationPeriod}

# Module 3 — produces findings-pacing.json + opportunities-pacing.json + pacing-projection.csv
node .claude/skills/budget-auditor/scripts/analyze-pacing.js
```

Each engine writes to `context/analysis/budget/`.

**Read the findings JSONs**, then assign verdicts per `reference/scoring-model.md`:

| Verdict | Effect |
|---|---|
| PASS | full points retained |
| WARN | 40% deduction |
| FAIL | 100% deduction |
| INFO | informational, no points at stake |
| SKIP | excluded; denominator reduced |

---

## Phase 1.5: Synthesis & Constraint Cascade (MANDATORY)

**Read `reference/synthesis-playbook.md` in full before writing any recommendation.** The whole point of the cascade is that "raise the budget" is almost always the wrong first move when an upstream layer is dirty.

Output: a ranked hypothesis list, each with:
- layer (M / B / Bid / Eff / Conv / Comp / Struct / T)
- evidence (which diagnostics)
- confidence (low / medium / high)
- whether it blocks downstream raise actions

Required checks (every audit):
1. **M layer** — tracking-specialist findings on flagged campaigns? Active → blocks all raise mutations.
2. **B layer** — break-even or primary KPI missing? Active → blocks profitability-dependent diagnostics (BUD-D03/D04/D13/D14/D15) and any raise.
3. **Bid layer** — BUD-D05, BUD-D08, BUD-D19 fire? Sequence `/bidding-specialist` before any budget mutation on the affected campaigns.
4. **Eff layer** — fresh search-term/keyword/QS audits show waste on flagged campaigns? Recover efficiency before raise.
5. **Conv layer** — CVR is the bottleneck on a budget-limited profitable campaign? `/lp-auditor`, `/offer-auditor` first.
6. **Comp layer** — IS Lost (Rank) > IS Lost (Budget) on flagged campaign? Decompose via `/competitive-analyst`.
7. **Struct layer** — zero-spend or daypart exhaustion? `/account-auditor`, `/geo-schedule-auditor`, `/account-changelog`.
8. **T layer** — pure budget action (raise/reduce/reallocate/share-fix) — only after the cascade clears.

### Anti-patterns

- Never recommend a raise while M or B is blocking. Replace with the handoff.
- Never recommend a raise on a campaign with `state = unprofitable` — that's a reduce candidate.
- Never recommend stacking a raise + reduce on the same campaign in one session.
- Never propose a single-mutation jump > `maxSingleMutationMultiplier` (default 1.3×) without explicit `--aggressive`.
- Never write a flat actions table that mixes a tracking handoff with a raise — segment by cascade state per the report template.

---

## Phase 2: Score & Report

Read `reference/scoring-model.md`. Compute:
- module sub-scores (after deductions)
- N/A redistribution if any module SKIPs entirely (no shared budgets, fallback-mode pacing, all-PMax-no-tCPA Sufficiency split)
- weighted total

### Bands

| Score | Grade |
|---|---|
| 90–100 | Excellent |
| 75–89 | Good |
| 60–74 | Needs Attention |
| <60 | Critical |

### Write report to `context/analysis/budget-audit.md`

Read `reference/report-template.md`. Section order:

1. Executive read (prose, 2–4 paragraphs)
2. Score, grade, window, run timestamp, banners (experiments, fallback mode, stale changelog)
3. Top hypothesis row
4. Module score table (5 rows)
5. Risks segmented: 🔍 Investigate first / 🔧 Bidding-side fix / 🔄 Recover efficiency / ⚖️ Allocation / ✅ Act now / ⚠️ Hold
6. Opportunities (always present)
7. Pacing snapshot (if module ran)
8. Sequenced handoffs
9. Per-diagnostic appendix

### Append to `context/analysis/budget-audit-log.md`:

```markdown
## {date} — Score: {score}/100 ({grade})
- Period: {period}d | Campaigns: {n} | Consumers: {m}
- Top hypothesis: {layer} — {label}
- Active blocking: {comma list or "none"}
- Top finding: {1-line}
```

---

## Phase 3: Opportunities Pass (unconditional)

Always run, even when zero risk findings. Cross-cutting opportunities surfaced by the engines:

- **profitable_limited_recovery** — IS-lost-budget recovery on a profitable campaign. Includes projected incremental conversions, cost, and CPA/ROAS at the projected unit cost.
- **winner_underfunded** — profitable campaign capturing < 15% spend share with material IS Lost (Budget).
- **seasonality_ramp** — next month is a designated highlight month and budgets haven't been raised.
- **underspend_redeploy** — pacing projects underspend; surface unspent dollars for reallocation.

Each entry: type, scope, $-projection, recommended optimizer subcommand. Currency rounding is to the nearest dollar (transparency over tidy numbers).

---

## Phase 3.5: Peer Report Lookup (MANDATORY before handoff)

**Don't send the user from one door to the other.** Before recommending any peer-skill handoff in Phase 4, check whether that peer has *already* produced a fresh report — and if so, **read it and integrate its findings into THIS report** instead of asking the user to re-run.

The whole point of cross-skill awareness is that a user who runs `/quality-score-auditor` last week and then runs `/budget-auditor` this week sees the QS findings *quoted inside the budget report*, not a redundant "go run QS" instruction. Re-running an auditor that already produced a fresh answer wastes the user's time and obscures the budget-side action.

### Freshness windows

| Peer skill | Report file | Fresh window |
|---|---|---|
| `/quality-score-auditor` | `context/analysis/quality-score-audit.md` | ≤ 7 days |
| `/search-term-auditor` | `context/analysis/search-term-audit.md` | ≤ 7 days |
| `/keyword-auditor` | `context/analysis/keyword-audit.md` | ≤ 7 days |
| `/competitive-analyst` | `context/analysis/competitive-audit.md` | ≤ 14 days |
| `/lp-auditor` | `context/analysis/lp-audit.md` | ≤ 14 days |
| `/offer-auditor` | `context/analysis/offer-audit.md` | ≤ 30 days |
| `/bidding-auditor` | `context/analysis/bidding-audit.md` | ≤ 7 days |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days |
| `/strategy-specialist` | `context/analysis/strategy-audit.md` | ≤ 30 days |
| `/account-auditor` | `context/analysis/account-audit.md` | ≤ 30 days |

### Procedure for each peer that the cascade would otherwise hand off to

1. **Check if the file exists.** If not → keep the handoff as a plain "run `/peer-skill`" line.
2. **If it exists, check mtime AND the date in the report header against the freshness window.**
3. **If fresh:** open the report and read its **executive read / top hypothesis / module scores / risks**. Pull out the 1–3 findings that overlap with this audit's flagged campaigns or hypotheses. Use them to:
   - **Enrich the Executive read at the top of `budget-audit.md`** — quote the peer's score, the headline finding, and the date inline.
   - **Replace** the Phase 4 line "run `/peer-skill`" with: **"Review the existing {date} {peer} report at {path} — top finding: '{one-liner}'. Re-run only if you want fresher data."**
   - In the Risks section, when an Eff/Conv handoff is the top hypothesis, quote the peer's specific finding (campaign names, page URLs, search-term n-grams, etc.) so the user can act without leaving the budget report.
4. **If stale:** mention "a previous {peer} report exists from {date} but is {N} days old — recommend re-running before relying on it" and keep the handoff as a re-run.
5. **If missing:** standard "run `/peer-skill`" handoff.

### When a fresh peer report contradicts a budget hypothesis

Say so explicitly in the Executive read. Example: budget-auditor flags `BUD-D03` (profitable + IS Lost (Budget) 22% on Branded Search) and would normally route to `/budget-optimizer raise` — but the fresh QS report shows the same campaign has rank-lost IS at 90% driven by LP issues. Loosening the budget won't recover that lost traffic; LP fixes will. **The budget report must say this, not silently propose the raise.**

That cross-skill validation is the entire reason this phase exists. A budget audit that ignores a fresh QS or LP audit is worse than no budget audit, because it produces a confidently-wrong recommendation.

---

## Phase 4: Sequenced Handoff Offer

Apply Phase 3.5 lookup results, then render per `reference/handoff-matrix.md`. Always sequence by cascade priority — never present as a flat menu.

When upstream is dirty:

> **Top hypothesis:** {layer} — {label}
>
> Before any budget change, run in order:
> 1. **{M handoff if active}** → `/{skill}`
> 2. **{B handoff if active}** → `/{skill}`
> 3. **{Bid peer (if Bid layer firing)}** → `/bidding-specialist`
> 4. **{Eff layer}** → `/search-term-auditor`, `/quality-score-auditor`, etc.
> 5. **{Conv layer}** → `/lp-auditor`, `/offer-auditor`
> 6. **{Comp / Struct (informational)}** → `/competitive-analyst`, `/account-auditor`
> 7. **{T — `/budget-optimizer` only after the above clear}**
>    - {N} reallocations → `/budget-optimizer reallocate`
>    - {M} reductions → `/budget-optimizer reduce`
>    - {K} raises (gated) → `/budget-optimizer raise`

When all clear:

> Cascade clears 1–7 are green. Ordered by priority:
> - Always-safe: `/budget-optimizer fix-shared`, `/budget-optimizer pacing-adjust`
> - Reallocate: `/budget-optimizer reallocate`
> - Reduce: `/budget-optimizer reduce`
> - Raise (gated): `/budget-optimizer raise`

Only show subcommands with findings to act on.

---

## Phase 5: Report Generation

Already written in Phase 2; Phase 5 is the user-facing presentation. The reader should be able to act on the **Executive read alone** — that's the bar. Everything else is reference material for when they want detail.

Lead with the **Executive read** (prose, ~300 words, no bullet lists). It must:
- State what the score actually means in plain language (not just the band).
- Name the 1–3 things that matter this week, ranked, each with the *why*.
- Name what is NOT a problem so red text below doesn't waste attention.
- **Quote inline any fresh peer-report findings** discovered in Phase 3.5 (date, score, one-line top finding) — this is the most valuable line in the report.
- End with one line on how to read the rest.

Then in this order:

1. Diagnosis paragraph (technical restatement of the cascade hypothesis).
2. Top hypothesis row.
3. Module score table (5 rows; mark N/A modules clearly).
4. Risks segmented by cascade state (🔍 Investigate first / 🔧 Bidding-side fix / 🔄 Recover efficiency / ⚖️ Allocation / ✅ Act now / ⚠️ Hold / ℹ️ Confirm intent). Each line that hands off to a peer skill **integrates the fresh peer's specific finding when one exists** — never a bare "go run X".
5. Opportunities table (always present, even on healthy accounts).
6. Pacing snapshot (when Module 3 ran).
7. Sequenced handoffs (numbered protocol — see Phase 4 template).
8. Module details appendix.
9. Configuration snapshot.
10. One-line: "Full report saved to `context/analysis/budget-audit.md`."

Read `reference/report-template.md` for the full template + style guidelines (prose first, quote-don't-link, sequence-don't-menu, name-reality-not-just-verdict).

The Executive read is the contract: a user who only reads the first paragraph should still leave with the right next action.

---

## Edge Cases

| Scenario | Handling |
|---|---|
| No shared budgets in account | Module 5 SKIP entirely; 15 pts redistribute. |
| `targetFallbackMode = "no_monthly_target"` | Module 3 SKIP; 15 pts redistribute. Banner the report. |
| `monthlyBudgetTotal = null` AND no fallback | Phase 0.1 fails; re-run interview. |
| `primaryKPI` / break-even missing | BUD-D03/D04/D13/D14/D15 return INFO with `blocking: ['business']`; route to `/strategy-specialist`. Other diagnostics still run. |
| Single-campaign account | Allocation diagnostics SKIP; report notes the structural gap. |
| account-changelog missing or >24h | Prompt the user; cache consent for the session if they say "auto-refresh from now on". |
| Account-budget query fails (non-invoicing) | Soft-fail, don't error the whole run. Logged as SKIP. |
| New campaigns (<14d old) | Marked INFO with "new — monitoring" note inside findings; no raise recommendation. |
| All-PMax account with no tCPA | BUD-D05 SKIPs (single-diagnostic); module remains scored on BUD-D08. |
| Currency other than USD | All money columns formatted via top-level `accountCurrency`. |
| API rate limit | pull-all.js delegates to query.js which retries; surfaces error and exits 1. |
| Conversion lag > evaluation window | Re-run with longer window — surface as M2 hypothesis. |
| Recently raised budget (<14d) | Findings annotate "in learning"; optimizer hard-refuses any raise on the same campaign for 14d. |

---

## Known Gaps (v1)

- **BUD-E08 monitoring alerts** — deferred to v1.1; will write `monitoring/budget-alerts.json` for the future `/daily-monitor` orchestrator.
- **Performance Planner integration** — opportunity projection uses the `is_lost_budget` heuristic; v1.1 swaps in CampaignBidSimulatorService and Performance Planner forecasts.
- **Hourly segmentation for BUD-D06** — daily 95% threshold is the v1 stand-in; v1.1 adds hourly when row-count tradeoff is acceptable.
- **Per-channel scoring weights** — single set of module weights for v1; v1.1 will diverge if Search/PMax/Shopping accounts diverge enough in practice.
- **`bid-budget-reviewer` orchestrator** — v1.1; for now the report sequences bidding-specialist + budget-optimizer handoffs explicitly.
