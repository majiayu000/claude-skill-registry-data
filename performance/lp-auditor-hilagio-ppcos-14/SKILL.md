---
name: lp-auditor
description: Audit landing pages across 40 diagnostics in 6 modules (structural, message match, technical, performance, URL health, ecom). Scores 0-100 per module. Use for LP audits and health checks.
argument-hint: "[module]"
---

# LP Auditor Skill

Audits landing page quality across 6 modules (40 diagnostics). DIAGNOSE-ONLY — findings route to lp-optimizer, landing-page-builder, or ecom-page-builder for execution.

| Module | IDs | Checks |
|--------|-----|--------|
| **Structural** | D01-D12 | Offer completeness, hero clarity, CTA quality, benefits, trust, social proof, objections, guarantee, section hierarchy |
| **Message Match** | D13-D16 | Ad-to-LP headline match, offer match, keyword relevance, visual consistency |
| **Technical** | D17-D24 | Page speed, Core Web Vitals, mobile responsiveness, mobile CVR gap, forms, SSL, images |
| **Performance** | D25-D31 | CVR vs benchmark, per-LP CPA, device splits, traffic source match |
| **URL Health** | D32-D37 | HTTP status codes, redirect chains, DSA URLs, keyword URLs, asset URLs, URL expansion |
| **Ecommerce** | D38-D40 | Product page elements, cart/checkout flow, category page quality |

**Not checked by this skill (per de-duplication log):**
- Conversion tracking setup → tracking-specialist
- Ad copy quality → ad-copy-specialist
- Offer quality → offer-auditor
- Account structure → account-auditor

## Command Format

```
/lp-auditor                          # Default: entry gate selector (choose module or full)
/lp-auditor structural               # D01-D12 only
/lp-auditor message-match            # D13-D16 only
/lp-auditor technical                # D17-D24 only
/lp-auditor performance              # D25-D31 only
/lp-auditor urls                     # D32-D37 only
/lp-auditor ecommerce                # D38-D40 only
```

All subcommands accept an optional `--url=https://...` flag to pre-load a target URL.

**Examples:**
- `/lp-auditor` — Interactive selector, then full or module-specific audit
- `/lp-auditor structural --url=https://example.com` — Structural audit of specific URL
- `/lp-auditor urls` — Batch URL health check across all active final URLs
- `/lp-auditor performance` — Per-LP performance analysis from Google Ads data

---

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `context/business.md` | Recommended | Vertical detection (lead gen / SaaS / ecommerce) |
| `context/google-ads/data/ads.csv` | Yes (message-match, urls, performance) | Ad headlines, descriptions, final URLs |
| `context/google-ads/data/keywords.csv` | Yes (message-match) | Keywords mapped to ad groups |
| `context/google-ads/data/device-performance.csv` | Yes (technical D20) | Device-level CVR comparison |
| `context/google-ads/data/assets.csv` | Optional (urls D36) | Sitelink URLs, asset URLs |
| Chrome DevTools MCP server | Yes (structural, technical, ecommerce) | Page inspection, Lighthouse, screenshots |
| `scripts/url-health-check.js` | Yes (urls) | Batch HTTP status + redirect chain checks |
| `scripts/page-content-extractor.js` | Yes (message-match) | Batch page content extraction (H1, hero, CTAs) |

---

## Process

---

### Phase 0: Entry Gate & Route

**Always starts with a selector question** (unless subcommand was passed via `/lp-auditor {module}`).

Present using AskUserQuestion with these 4 selectable options (fits within tool limits):

```
What type of landing page audit would you like to run?

1. Full Audit — All 6 modules, comprehensive score (D01-D40)
2. Page Quality — Structural + Message Match + Technical (D01-D24, needs a URL)
3. Ads Data — Performance + URL Health from Google Ads data (D25-D37, no URL needed)
4. Ecommerce — Product page, cart, category checks (D38-D40, needs URL)
```

For individual modules, users can bypass the selector with subcommands:
`/lp-auditor structural`, `/lp-auditor message-match`, `/lp-auditor technical`, `/lp-auditor performance`, `/lp-auditor urls`, `/lp-auditor ecommerce`

**After selection, conditionally ask for inputs based on what's needed:**

| Selection | Modules run | Needs URL? | Needs Google Ads data? | Needs Chrome DevTools? | Needs scripts? |
|-----------|------------|-----------|----------------------|----------------------|----------------|
| Full Audit | All 6 | No — auto-discovers all URLs from ads data | Yes (all) | Yes (all, per URL) | Yes (both scripts) |
| Page Quality | Structural + Message Match + Technical | YES — ask for URL | Yes (ads.csv, keywords.csv, device-performance.csv) | Yes (screenshot, DOM, Lighthouse, mobile) | Yes (page-content-extractor.js) |
| Ads Data | Performance + URL Health | No — auto-discovers from ads data | Yes (ads.csv, keywords.csv, assets.csv) | No | Yes (url-health-check.js) |
| Ecommerce | Ecommerce only | YES — ask for URL(s) | No | Yes (page content) | No |

Individual subcommand requirements:

| Subcommand | Needs URL? | Needs Google Ads data? | Needs Chrome DevTools? | Needs scripts? |
|------------|-----------|----------------------|----------------------|----------------|
| structural | YES | No | Yes | No |
| message-match | YES | Yes (ads.csv, keywords.csv) | No | Yes (page-content-extractor.js) |
| technical | YES | Yes (device-performance.csv) | Yes | No |
| performance | No — auto-discovers | Yes (ads.csv) | No | No |
| urls | No — auto-discovers | Yes (ads.csv, keywords.csv, assets.csv) | No | Yes (url-health-check.js) |
| ecommerce | YES | No | Yes | No |

**Routing steps:**
1. Present selector (or parse subcommand)
2. Read `context/business.md` → extract vertical (lead gen / SaaS / ecommerce)
3. Based on selection, determine which inputs are needed and ask only the relevant questions
4. If ecommerce module selected but vertical is NOT ecommerce: SKIP ecommerce module, inform user
5. Load `reference/diagnostic-rules-shared.md` for scoring system and result format
6. Proceed to data collection for only the selected modules

**Display configuration:**
```
LP Audit Configuration:
  Vertical: {vertical}
  Mode: {full / structural / message-match / technical / performance / urls / ecommerce}
  Target URL: {url or "auto-discover from ads data"}
```

---

### Phase 1: Data Collection (only for selected modules)

**Google Ads data (only if Performance, Message Match, URL Health, or Full selected):**
- Read `context/google-ads/data/ads.csv` → ad headlines, descriptions, final URLs
- Read `context/google-ads/data/keywords.csv` → keywords mapped to ad groups
- Read `context/google-ads/data/device-performance.csv` → device-level CVR (Technical + Full only)
- Extract all unique final URLs from ads, keywords, sitelinks, DSA targets

If any required file doesn't exist, tell the user to run `/gads-context` first.

**Script execution (only if Message Match, URL Health, or Full selected):**
- Dedupe all collected URLs into a single list
- For Message Match: run `scripts/page-content-extractor.js` (extracts H1, hero, offer, CTAs per URL)
- For URL Health: run `scripts/url-health-check.js` (HEAD requests, status codes, redirect chains)

**Chrome DevTools (only if Structural, Technical, Ecommerce, or Full selected):**
- Navigate to target URL(s)
- Take full-page screenshot
- Extract page DOM structure (headings, sections, CTAs, forms, images)
- Run Lighthouse audit for Core Web Vitals (Technical + Full only)
- Emulate mobile viewport (Technical + Full only)
- Monitor network requests for image sizes (Technical + Full only)

Display data summary:
```
Data Sources:
| Source                    | Status          | Detail               |
|---------------------------|-----------------|----------------------|
| business.md              | OK              | Vertical: {vertical} |
| ads.csv                  | OK ({n} ads)    | {n} unique URLs      |
| keywords.csv             | OK ({n} KWs)    | {n} ad groups        |
| device-performance.csv   | OK              | {n} campaigns        |
| page-content-extractor   | Ran ({n} URLs)  | Content extracted     |
| url-health-check         | Ran ({n} URLs)  | Status codes checked  |
| Chrome DevTools          | Connected       | {url}                |
```

---

### Phase 2: Run Diagnostics

**Read `reference/diagnostic-rules-shared.md` first** (scoring model, severity definitions).

**Then read ONLY the module-specific rules for the requested modules:**

| Module | Reference file to load |
|---|---|
| Structural | `diagnostic-rules-structural.md` |
| Message Match | `diagnostic-rules-message-match.md` |
| Technical | `diagnostic-rules-technical.md` |
| Performance | `diagnostic-rules-performance.md` |
| URL Health | `diagnostic-rules-url-health.md` |
| Ecommerce | `diagnostic-rules-ecommerce.md` |
| Full (all) | Run modules sequentially. Load and release each module's references before loading the next. |

**Important:** When running all modules (full), do NOT load all reference files at once. Run structural first, then message match, then technical, etc. — loading each module's references fresh for that phase.

Run each diagnostic in order per the module-specific rules. For each, produce a structured result:

```
ID: LP-DXX
Name: {diagnostic name}
Status: PASS | WARN | FAIL | SKIP
Severity: Critical | High | Medium | Low
Points: {earned} / {possible}
Details: {what was found — specific elements, URLs, screenshots}
Recommendation: {if WARN or FAIL, what to fix}
Routing: {skill that handles the fix: lp-optimizer, landing-page-builder, ecom-page-builder}
```

**After each module, display results table:**

```
{Module Name} Results:
| ID     | Diagnostic              | Status | Pts   | Detail                                    |
|--------|-------------------------|--------|-------|-------------------------------------------|
| LP-D01 | Offer section complete  | PASS   | 10/10 | All 5 components present                  |
| LP-D02 | Hero 5-second test      | WARN   | 5/10  | H1 is 14 words — too long                |
| ...    | ...                     | ...    | ...   | ...                                       |
```

### Phase 2.5: Interview Gate

After running all selected diagnostics, batch any that have ASK status (diagnostics that need user input to evaluate).

Present all ASK questions together via AskUserQuestion with selectable options where possible. Resolve answers back into PASS/WARN/FAIL.

Common ASK scenarios:
- D16: "Do you run Display or Video campaigns to this LP?"
- D22: "May I test the form submission? (will fill test data)"
- D39: "What is the cart page URL?"
- D40: "What is the category page URL?"

---

### Phase 3: Score & Log

**Calculate scores:**

1. Tally points earned vs points possible (exclude SKIP diagnostics from denominator)
2. Calculate module scores using weights:

| Module | Weight (lead gen/SaaS) | Weight (ecommerce) |
|--------|----------------------|-------------------|
| Structural (D01-D12) | 35% | 30% |
| Message Match (D13-D16) | 20% | 20% |
| Technical (D17-D24) | 20% | 20% |
| Performance (D25-D31) | 15% | 15% |
| URL Health (D32-D37) | 10% | 10% |
| Ecommerce (D38-D40) | N/A — excluded | 5% |

For lead gen/SaaS: ecommerce module is excluded, weights for other modules sum to 100%.
For ecommerce: all modules included.

3. Overall score: weighted average across enabled modules
4. Assign grade:
   - 90-100%: Excellent
   - 70-89%: Good
   - 50-69%: Needs Attention
   - < 50%: Critical

**Append to log:** `context/analysis/lp-audit-log.md`

If file doesn't exist, create it with header `# LP Audit Log`.

Append a timestamped entry using the log template from `reference/report-template.md`.

---

### Phase 3.5: Peer Report Lookup (MANDATORY before writing the report)

**Don't send the user from one door to the other.** Before recommending any peer-skill handoff in Phase 4, check whether that peer has already produced a fresh report — and if so, **read it and integrate its findings into THIS report** instead of asking the user to re-run.

The whole point of cross-skill awareness is that a user who runs `/quality-score-auditor` last week and then runs `/lp-audit` this week sees the QS findings *quoted inside the LP report*, not a redundant "go run QS" instruction. Re-running an auditor that already produced a fresh answer wastes time and obscures the LP-side action.

#### Freshness windows

| Peer skill | Report file | Fresh window |
|---|---|---|
| `/quality-score-auditor` | `context/analysis/quality-score-audit.md` | ≤ 7 days |
| `/search-term-auditor` | `context/analysis/search-term-audit.md` | ≤ 7 days |
| `/keyword-auditor` | `context/analysis/keyword-audit.md` | ≤ 7 days |
| `/budget-auditor` | `context/analysis/budget-audit.md` | ≤ 7 days |
| `/bidding-auditor` | `context/analysis/bidding-audit.md` | ≤ 7 days |
| `/competitive-analyst` | `context/analysis/competitive-audit.md` | ≤ 14 days |
| `/offer-auditor` | `context/analysis/offer-audit.md` | ≤ 30 days |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days |
| `/strategy-specialist` | `context/analysis/strategy-audit.md` | ≤ 30 days |
| `/account-auditor` | `context/analysis/account-audit.md` | ≤ 30 days |

#### Procedure for each peer that the routing would otherwise hand off to

1. **Check if the file exists.** If not → keep the handoff as a plain "run `/peer-skill`" line.
2. **If it exists, check the date in the report header against the freshness window.** The report header date is canonical. mtime is a sanity check — if mtime is *older* than the header date, warn the user that something is off.
3. **If fresh:** open the report and read its **executive read / top findings / module scores**. Pull out the 1–3 findings that overlap with this audit's flagged URLs, ad groups, or campaigns. Use them to:
   - **Enrich the Executive read at the top of `lp-audit.md`** — quote the peer's score, the headline finding, and the date inline.
   - **Replace** the routing line "run `/peer-skill`" with: **"Review the existing {date} {peer} report at {path} — top finding: '{one-liner}'. Re-run only if you want fresher data."**
   - In Priority Fixes / Routing, when a peer handoff is the recommended action, quote the peer's specific finding so the user can act without leaving this report.
4. **If stale:** mention "a previous {peer} report exists from {date} but is {N} days old — recommend re-running before relying on it" and keep the handoff as a re-run.
5. **If missing:** standard "run `/peer-skill`" handoff.

#### When a fresh peer report contradicts an LP hypothesis

Say so explicitly in the Executive read. Example: lp-auditor flags Module 4 (Performance) for low CVR on Campaign X — but the fresh tracking-audit shows the conversion event for that campaign is misfiring. The CVR finding is then unreliable; LP fixes won't help if the conversion isn't being recorded. **The LP report must say this, not silently propose LP changes.**

That cross-skill validation is the entire reason this phase exists. An LP audit that ignores a fresh tracking or QS audit produces a confidently-wrong recommendation.

---

### Phase 4: Write Report

Write `context/analysis/lp-audit.md` using `reference/report-template.md`.

This report is regenerated on each run (overwrites previous). The log (Phase 3) preserves history.

**Lead with the Executive read** — the 6-slot prose contract defined in `reference/report-template.md`. Apply Phase 3.5 lookup results to slot 4 (inline-quoted fresh peer findings) and to every line in Routing Recommendations that points to a peer skill.

Fill in all sections in this order:
1. **Executive read** (prose, ≤300 words, no bullets) — score meaning, 1–3 priorities w/ why, what's NOT a problem, fresh peer findings inline, how-to-read, score trend.
2. Overall score + grade
3. Module scores breakdown
4. Priority fixes (sorted by impact) — with peer findings integrated when fresh
5. All diagnostic results per module
6. Routing recommendations — apply Phase 3.5 results: every line says either "run /peer" (missing/stale) or "review existing {date} report at {path}" (fresh, with the one-liner finding)
7. Data freshness

---

### Phase 5: Summary & Next Steps

Already written in Phase 4; Phase 5 is the user-facing presentation. The reader should be able to act from the **Executive read alone** — that's the bar. Everything else is reference material.

Print to user in this order:

1. **Executive read** (the prose section from the report — quote it verbatim, don't re-summarize). It already covers score-meaning, this-week priorities w/ why, what's-NOT-a-problem, fresh peer findings inline, how-to-read, score trend.
2. Score, grade, mode, run timestamp.
3. Module score table.
4. Top 3 issues — sorted by severity, with specific fix actions.
5. **Routing recommendations** — apply Phase 3.5 lookup results to every line. Each peer handoff says either "review existing {date} report at {path} (top finding: ...)" or "run `/peer-skill`".
   - If structural FAILs: "Run `/lp-optimize elements` to get fix guidance for missing elements"
   - If message match FAILs: "Run `/lp-optimize message-match` to fix ad-to-LP alignment"
   - If technical FAILs: "Run `/lp-optimize speed` or `/lp-optimize mobile` for technical fixes"
   - If performance FAILs: "Run `/lp-optimize audit` for full optimization guidance"
   - If URL health FAILs: "Run `/lp-optimize urls` to fix broken URLs"
   - If score < 40%: "Consider rebuilding: run `/landing-page` or `/ecom-page`"
   - If all PASS: "Page is solid. Monitor with `/lp-optimize monitor`"
6. Note location of full report: `context/analysis/lp-audit.md`.

**Log to memory:** Write entry to `context/memory/YYYY-MM-DD.md` per memory-logging rules:

```markdown
## LP Audit Completed
- Mode: {mode}
- URL: {url or "auto-discovered {n} URLs"}
- Score: {score}% ({grade})
- Key findings: {list of FAIL/WARN items}
- Routing: {list of skills/commands recommended}
- Report: context/analysis/lp-audit.md
```
