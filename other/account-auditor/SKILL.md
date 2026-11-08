---
name: account-auditor
description: Audit account structure, naming, settings, ad groups, and defaults across 24 diagnostics in 5 modules. Scores 0-100 per module. Use for account audits, health checks, and structure reviews.
argument-hint: "[module]"
---

# Account Auditor Skill

Audits account structural health across 5 modules (24 diagnostics). DIAGNOSE-ONLY — findings route to specialist skills for execution.

| Module | IDs | Checks |
|--------|-----|--------|
| **Structure** | D01-D08 | Campaign type separation, brand/non-brand, business alignment, count efficiency, budget fragmentation, targeting overlap, zero-conversion, zero-impression |
| **Naming** | D09-D10 | Campaign naming convention, ad group naming consistency |
| **Settings** | D11-D19 | Display Network, Search Partners, location targeting/exclusion, language, ad rotation, ad schedule, tracking template, URL expansion |
| **Ad Groups** | D20-D23 | Thematic tightness, ads per ad group, impression distribution, SKAG detection |
| **Defaults** | D24 | Account-level setting defaults |

**Not checked by this skill (per de-duplication log):**
- Bid strategy health → bidding-specialist
- Auto-apply/recommendations → automation-specialist
- Feed health → feed-specialist
- Conversion tracking → tracking-specialist
- Ad copy quality → ad-copy-specialist

## Command Format

```
/account-auditor                    # Default: runs all 5 modules sequentially
/account-auditor structure          # D01-D08 only
/account-auditor naming             # D09-D10 only
/account-auditor settings           # D11-D19 only
/account-auditor adgroups           # D20-D23 only
/account-auditor defaults           # D24 only
```

**Examples:**
- `/account-auditor` — Full audit across all modules
- `/account-auditor structure` — Quick structural health check
- `/account-auditor settings` — Settings hygiene audit
- `/account-auditor adgroups` — Ad group quality check

---

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `context/google-ads/data/campaigns.csv` | Yes (from gads-context) | Campaign performance data for D01-D08 |
| `context/google-ads/data/campaigns-settings.csv` | Yes (pulled fresh) | Campaign settings for D11-D19 |
| `context/google-ads/data/adgroups.csv` | Yes (from gads-context) | Ad group data for D20-D23 |
| `context/google-ads/data/keywords.csv` | Yes (from gads-context) | Keyword data for D02, D06, D20, D23 |
| `context/google-ads/data/ads.csv` | Yes (from gads-context) | Ad data for D21 |
| `context/business.md` | Recommended | Brand name, vertical, goals |
| `config/ads-context.config.json` | Yes | Customer IDs |
| `context/google-ads/data/conversion-goal-config.csv` | Optional (for D24) | Conversion goal configuration |

---

## Process

---

### Phase 0: Prerequisites & Route

1. **Parse subcommand:**
   - `structure` → D01-D08 only
   - `naming` → D09-D10 only
   - `settings` → D11-D19 only
   - `adgroups` → D20-D23 only
   - `defaults` → D24 only
   - No subcommand (default) → run all modules sequentially

2. **Load config** — read `config/ads-context.config.json`, extract:
   - `googleAds.customerId` and `googleAds.loginCustomerId`

3. **Load business.md** — extract:
   - Vertical (ecommerce / lead gen / SaaS)
   - Brand name (needed for D02)
   - Business goals (needed for D03)
   - If business.md is missing: WARN but continue (structure/settings checks still work without it)

4. **Display configuration:**
   ```
   Account Audit Configuration:
     Account: {customerId}
     Vertical: {vertical}
     Brand: {brand_name}
     Mode: {structure / naming / settings / adgroups / defaults / full}
   ```

---

### Phase 0.5: Data Pull

**Pull fresh campaign settings data. Use existing gads-context data for performance files.**

```bash
# Campaign settings (no date range — structural data)
node .claude/skills/gads-context/scripts/query.js \
  --customer-id={customer_id} \
  --login-customer-id={login_customer_id} \
  --query-file=.claude/skills/account-auditor/reference/campaigns-settings-audit.gaql \
  --no-date-range \
  --allow-empty \
  --output=context/google-ads/data/campaigns-settings.csv

# All keywords (no date range — structural data, includes zero-impression keywords)
node .claude/skills/gads-context/scripts/query.js \
  --customer-id={customer_id} \
  --login-customer-id={login_customer_id} \
  --query-file=.claude/skills/account-auditor/reference/keywords-all.gaql \
  --no-date-range \
  --allow-empty \
  --output=context/google-ads/data/keywords-all.csv
```

**Why keywords-all.csv?** The standard `keywords.csv` from gads-context uses `keyword_view` with a date range and `metrics.impressions > 0`, so it only contains keywords that received impressions. For structural checks (D02 brand separation, D06 overlap, D20 thematic tightness, D23 SKAG detection), we need ALL keywords regardless of performance.

**Use existing data from gads-context (do NOT re-pull unless stale):**
- `context/google-ads/data/campaigns.csv` — performance data (D01-D08)
- `context/google-ads/data/adgroups.csv` — ad group data (D20-D22)
- `context/google-ads/data/ads.csv` — ad data (D21)

If any required file doesn't exist, tell the user to run `/gads-context` first or pull individually.

Display data pull summary:
```
Data Sources:
| File                      | Rows | Status          |
|---------------------------|------|-----------------|
| campaigns-settings.csv    | {n}  | Pulled fresh    |
| keywords-all.csv          | {n}  | Pulled fresh    |
| campaigns.csv             | {n}  | OK (existing)   |
| adgroups.csv              | {n}  | OK (existing)   |
| ads.csv                   | {n}  | OK (existing)   |
```

If campaigns.csv has zero enabled campaigns, STOP and tell user: "No enabled campaigns found in this account."

**Exclude ended experiment campaigns:**
After loading data, filter out campaigns where `experiment_type = EXPERIMENT` AND `serving_status = ENDED` from both `campaigns-settings.csv` and `campaigns.csv`. These are completed experiments that should not be audited alongside live campaigns. Running experiments (`serving_status != ENDED`) are kept in the audit.

If any ended experiments are excluded, note them in the data pull summary:
```
Excluded {n} ended experiment campaign(s): {campaign names}
```

---

### Phase 1: Run Diagnostics

**Read `reference/diagnostic-rules-shared.md` first** (scoring model, severity definitions, CSV column mapping).

**Then read ONLY the module-specific rules for the requested subcommand:**

| Subcommand | Reference files to load |
|---|---|
| `structure` | `diagnostic-rules-structure.md` |
| `naming` | `diagnostic-rules-naming.md` |
| `settings` | `diagnostic-rules-settings.md` |
| `adgroups` | `diagnostic-rules-adgroups.md` |
| `defaults` | `diagnostic-rules-defaults.md` |
| Default (all) | Run modules sequentially. Load and release each module's references before loading the next. |

**Important:** When running all modules (default), do NOT load all reference files at once. Run structure first, then naming, then settings, etc. — loading each module's references fresh for that phase.

Read CSV data files into working memory.

Run each diagnostic in order per the module-specific rules. For each, produce a structured result:

```
ID: AUD-DXX
Name: {diagnostic name}
Status: PASS | WARN | FAIL | SKIP
Severity: Critical | High | Medium | Low
Points: {earned} / {possible}
Details: {what was found — list specific campaigns/ad groups/settings}
Recommendation: {if WARN or FAIL, what to fix}
Routing: {specialist skill that handles the fix, if applicable}
```

**After each module, display results table:**

```
{Module Name} Diagnostic Results:
| ID      | Diagnostic                 | Status | Pts   | Detail                              |
|---------|---------------------------|--------|-------|-------------------------------------|
| AUD-D01 | Campaign type separation   | PASS   | 10/10 | All campaign types properly separated |
| AUD-D02 | Brand/non-brand separation | FAIL   | 0/10  | Brand keywords found in "Non-Brand Search" |
| ...     | ...                       | ...    | ...   | ...                                 |
```

---

### Phase 2: Score & Log

**Calculate scores:**

1. Tally points earned vs points possible (exclude SKIP diagnostics from denominator)
2. Calculate module scores:
   - Structure: D01-D08 (max 75 pts)
   - Naming: D09-D10 (max 10 pts — 5 Medium + 3 Low [mapped to 5])
   - Settings: D11-D19 (max 65 pts)
   - Ad Groups: D20-D23 (max 35 pts — adjusted for actual point values: 5+10+5+5=25)
   - Defaults: D24 (max 5 pts)
   - Overall: total earned / total possible as percentage

3. Assign grade:
   - 90-100%: Excellent
   - 70-89%: Good
   - 50-69%: Needs Attention
   - < 50%: Critical

**Append to log:** `context/analysis/account-audit-log.md`

If file doesn't exist, create it with header `# Account Audit Log`.

Append a timestamped entry using the log template from `reference/report-template.md`.

---

### Phase 2.5: Peer Report Lookup (MANDATORY before writing the report)

**Don't send the user from one door to the other.** Before recommending any peer-skill handoff in Phase 3, check whether that peer has already produced a fresh report — and if so, **read it and integrate its findings into THIS report** instead of asking the user to re-run.

The whole point of cross-skill awareness is that a user who runs `/quality-score-auditor` last week and then runs `/account-audit` this week sees the QS findings *quoted inside the account report*, not a redundant "go run QS" instruction. Re-running an auditor that already produced a fresh answer wastes time and obscures the account-side action (naming, ad-group split, settings fix).

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
| `/offer-auditor` | `context/analysis/offer-audit.md` | ≤ 30 days |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days |
| `/strategy-specialist` | `context/analysis/strategy-audit.md` | ≤ 30 days |

#### Procedure for each peer that the routing would otherwise hand off to

1. **Check if the file exists.** If not → keep the handoff as a plain "run `/peer-skill`" line.
2. **If it exists, check the date in the report header against the freshness window.** The report header date is canonical. mtime is a sanity check — if mtime is *older* than the header date, warn the user that something is off.
3. **If fresh:** open the report and read its **executive read / top findings / module scores**. Pull out the 1–3 findings that overlap with this audit's flagged campaigns, ad groups, or settings. Use them to:
   - **Enrich the Executive read at the top of `account-audit.md`** — quote the peer's score, the headline finding, and the date inline.
   - **Replace** the routing line "run `/peer-skill`" with: **"Review the existing {date} {peer} report at {path} — top finding: '{one-liner}'. Re-run only if you want fresher data."**
   - In Critical Issues / Routing, when a peer handoff is the recommended action, quote the peer's specific finding so the user can act without leaving this report.
4. **If stale:** mention "a previous {peer} report exists from {date} but is {N} days old — recommend re-running before relying on it" and keep the handoff as a re-run.
5. **If missing:** standard "run `/peer-skill`" handoff.

#### When a fresh peer report contradicts an account-audit hypothesis

Say so explicitly in the Executive read — never auto-defer or auto-override. Example: account-auditor flags D02 (brand/non-brand separation) because brand keywords appear in a "Non-Brand" campaign — but the fresh keyword-audit shows those tokens are actually competitor terms misclassified as brand. The D02 finding is then unreliable; the structure fix would do harm. **The account report must say this, not silently propose a campaign rebuild.**

That cross-skill validation is the entire reason this phase exists. An account audit that ignores a fresh QS, keyword, or tracking audit produces a confidently-wrong recommendation.

---

### Phase 3: Write Report

Write `context/analysis/account-audit.md` using `reference/report-template.md`.

This report is regenerated on each run (overwrites previous). The log (Phase 2) preserves history.

**Lead with the Executive read** — the 6-slot prose contract defined in `reference/report-template.md`. Apply Phase 2.5 lookup results to slot 4 (inline-quoted fresh peer findings) and to every line in Routing Recommendations that points to a peer skill.

Fill in all sections in this order:
1. **Executive read** (prose, ≤300 words, no bullets) — score meaning, 1–3 priorities w/ why, what's NOT a problem, fresh peer findings inline, how-to-read, score trend.
2. Overall score + grade
3. Module scores breakdown
4. Critical issues (FAIL diagnostics, sorted by severity) — with peer findings integrated when fresh
5. All diagnostic results per module
6. Routing recommendations — apply Phase 2.5 results: every line says either "run /peer" (missing/stale) or "review existing {date} report at {path}" (fresh, with the one-liner finding)
7. Data freshness

---

### Phase 4: Summary & Next Steps

Already written in Phase 3; Phase 4 is the user-facing presentation. The reader should be able to act from the **Executive read alone** — that's the bar. Everything else is reference material.

Print to user in this order:

1. **Executive read** (the prose section from the report — quote it verbatim, don't re-summarize). It already covers score-meaning, this-week priorities w/ why, what's-NOT-a-problem, fresh peer findings inline, how-to-read, score trend.
2. Score, grade, mode, run timestamp.
3. Module score table.
4. Top 3 issues — sorted by severity, with specific fix actions.
5. **Routing recommendations** — apply Phase 2.5 lookup results to every line. Each peer handoff says either "review existing {date} report at {path} (top finding: ...)" or "run `/peer-skill`":
   - If D01/D02 FAIL: "Brand/structure issues found. Campaign restructuring needed."
   - If D06 FAIL: "Keyword overlap detected. Run keyword audit to resolve duplicates."
   - If D07/D08 FAIL: "Non-serving campaigns found. Review and pause or fix."
   - If D11 FAIL: "Display Network enabled on Search campaigns. Fix in campaign settings immediately."
   - If D13/D14 FAIL: "Location targeting misconfigured. Fix in campaign settings."
   - If D21 FAIL: "Ad groups without ads. Create RSAs for active ad groups."
   - If all PASS: "Account structure is solid. Consider running specialist audits next."
6. Note location of full report: `context/analysis/account-audit.md`.

**Log to memory:** Write entry to `context/memory/YYYY-MM-DD.md` per memory-logging rules:

```markdown
## Account Audit Completed
- Mode: {mode}
- Score: {score}% ({grade})
- Key findings: {list of FAIL/WARN items}
- Routing: {list of specialist skills recommended}
- Report: context/analysis/account-audit.md
```

---

### Phase 5: Report Offer

After presenting the summary and logging to memory, offer the user a professional report:

> "Want me to generate a branded HTML report of this audit? I can create a professional client-ready document you can export to PDF. Just say yes or run `/report-generator`."

- If user accepts: run the `/report-generator` skill, passing the current client context
- If user declines: end the skill normally
