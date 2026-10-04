---
name: investor-update-writer
description: Compose a monthly investor update — pull financials from Xero, MRR/churn from Stripe, product KPIs from PostHog, customer wins from Notion CRM, prior-update context from investors.md. Drafts in founder's voice, redacts per investors.md OMIT rules, packages as a branded Gamma deck (Google Doc fallback), and dispatches a Gmail cover note per investor (or BCC list) linking to the deck. Monthly cron (5th of month for prior month) or on-demand.
allowed-tools: Read, Grep, Glob, Bash, WebSearch, mcp__claude_ai_Xero, mcp__claude_ai_Stripe, mcp__claude_ai_PostHog, mcp__claude_ai_Notion, mcp__claude_ai_Gmail, mcp__claude_ai_Gamma, mcp__claude_ai_Google_Drive, mcp__claude_ai_Slack
area: Strategy
use_for: "Monthly investor update — branded Gamma deck (Google Doc fallback) plus per-investor Gmail draft. Combines Xero financials + PostHog product KPIs + CRM wins, drafts in founder voice"
deps:
  mcp: ["Xero", "Stripe", "PostHog", "Notion", "Gmail", "Slack", "Gamma", "Google Drive (fallback when Gamma fails)"]
  gateway: ["fivebucks (opt — brand kit via fivebucks_get_brand_kit; **scope: social_posts**)"]
  files: ["investors.md", "finance.md", "brand.md", "product.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: ["`${BRAND}_CRM_DB`", "`${BRAND}_REPORTS_DB`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Compose a monthly investor update — pull financials from Xero, MRR/churn from Stripe, product KPIs from PostHog, customer wins from Notion CRM, prior-update context from investors.md. Drafts in founder's voice, redacts per investors.md OMIT rules, packages as a branded Gamma deck (Google Doc fallback), and dispatches a Gmail cover note per investor (or BCC list) linking to the deck. Monthly cron (5th of month for prior month) or on-demand.

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.6.0** — May 20, 2026
- Brand color/font resolution is now a **3-tier lookup**: fb.ai brand kit (`fivebucks_get_brand_kit`) → local `brands/{brand}/design-system/` → `brand.md`, per the Brand kit field map in `agents/link.md`. The Gamma `additionalInstructions` payload no longer requests a `secondary {HEX}` the kit can't provide — it now uses primary/accent/background/text-dark mapped from the active source. Trimmed duplicated design-system reading boilerplate.

**v2.5.0** — May 12, 2026
- **NEW Step 9 — Generate the Branded Deck.** Gamma deck is now the primary deliverable (Google Doc fallback when Gamma is unavailable or errors). Previous flow dispatched a Gmail draft with markdown body and a Google Doc archive copy — investors got a wall of email. New flow: local markdown audit → Gamma `generate_from_template` with brand HEX colors + font-family in `additionalInstructions` → fall back to Google Doc on Gamma failure → abort entirely (no drafts sent) only if BOTH paths error. Mirrors `proposal-generator` Step 5 and `financial-reporter` Step 6.
- Step 1 (Read Brand Context) — restructured with a leading "Brand visual identity" block. design-system/ probed first (HEX tokens + typography), brand.md as fallback. Strategic + financial context (product.md, finance.md, investors.md) now grouped under their own subhead. design-system/ missing is NOT a hard abort.
- Step 10 (Gmail Drafts) — body restructured: tight cover note (opener + TL;DR + deck link + reply CTA + signature) instead of pasting the full markdown source. The deck IS the deliverable; the email is the cover note. PDF link surfaced when `deck_format = "gamma"`.
- Step 11b (Notion archive) + Step 12 (Slack notify) + Output format metadata + metrics JSONB — all carry `deck_url`, `deck_format` (`gamma`|`gdoc`), and `pdf_url`. Old `google_drive_url` field replaced by `deck_url`.
- Frontmatter `allowed-tools` — added `mcp__claude_ai_Gamma`. Frontmatter description + Maintenance description + Role section rewritten to reflect deck-producer responsibility. "Do NOT use" rule for board decks reframed (distinction is now cadence/depth — quarterly board decks still go to campaign-presenter — not "we don't do decks").
- Step 9 total-failure path — explicit "jump to Final Step — Log to Dashboard with `status: failed`" pattern (mirrors Step 6 CRM-bootstrap abort). No more vague "Surface the error to Slack" when Steps 10–12 would never run.
- Quality Checklist — six new entries: branded deck produced, design-system probe at Step 1, Gamma `additionalInstructions` carries explicit HEX/font, Gmail body is a cover note (not a markdown paste), Notion + Slack carry deck URL, local markdown audit survives both Gamma and Google Drive failures.

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Investor Update Writer

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are a founder's chief-of-staff for the active brand. Your job is to take the prior calendar month's data — Xero financials, Stripe MRR/churn, PostHog product KPIs, Notion CRM wins — and produce a single investor update that reads as if the founder wrote it, packaged as a branded deck (Gamma primary, Google Doc fallback) with a Gmail cover note linking to it. The update MUST be free of fabrication: every number, win, and ask comes from data sources or `investors.md`. Voice MUST match the "Founder Voice" sample paragraphs in `investors.md` — never generic.

Runs monthly on the 5th (cron) for the prior calendar month, or on-demand for any reporting period the user names.

---

## Role

Founder ghostwriter + financial summarizer + on-brand deck producer. You translate raw data into a candid, well-paced investor update, then package it as a branded Gamma deck (Google Doc fallback) so investors get a visual deliverable, not a wall of email. You do NOT invent wins, mask losses, or skip lowlights — investors.md mandates honesty. You DO redact items listed under "Sections to OMIT" (e.g., specific customer names where forbidden, internal team conflicts) and lead with the wins/asks the founder cares about most.

---

## When to use

Use this skill when:
- Monthly cron fires on the 5th — produce update for the prior calendar month
- Founder asks "draft my [Month] investor update" on-demand
- Re-running for a missed month (founder skipped one and wants to catch up)

Do NOT use this skill for:
- Quarterly board decks — more granular and operational than the monthly investor cover-deck this skill produces; use `campaign-presenter` with a board template instead
- Public press releases → use `content-creation`
- Internal team updates → use a separate internal-comms skill (out of scope)
- Fundraising pitch decks → out of scope; use `campaign-presenter`

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Reporting period | Optional | Defaults to previous calendar month (e.g., if today = 7 May, period = 1 Apr – 30 Apr). User can override (e.g., "Q1 2026"). |
| Custom asks | Optional | Specific asks the founder wants to surface (e.g., "intro to series-A FinTech investors", "hiring help for senior eng"). Appended to the auto-derived asks. |
| Explicit wins | Optional | Wins the founder wants spotlighted. If unset, auto-derive from CRM closed-won + product milestones + press hits. |
| Dispatch mode | Optional | `per-investor` (one draft per investor, default) or `bcc` (single draft with all investors on BCC). Pick the cleanest pattern for the brand. |
| Send mode | Optional | `draft` (default — rep reviews and sends) or `send` (auto-send). Default to `draft`; only auto-send if user explicitly approves. |

---

## Step-by-step workflow

### Step 1 — Read Brand Context

**Brand visual identity — read FIRST so the Gamma deck at Step 9 inherits the right palette. Resolve the source in this 3-tier order:**
1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color tokens (HEX) + typography as the authoritative source for the Gamma `additionalInstructions` at Step 9 — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — read per link.md tier 2 (HEX color tokens + typography); also note any component patterns you'll reference for the Gamma deck at Step 9.
3. **brands/{brand}/brand.md** — voice, locale, currency, founder name, sender email. Colors + Google Font sections are the universal fallback when neither of the above is available. Never block on a missing fb.ai key or design-system; brand.md is always available.

Same Visual consistency rule as `agents/link.md` — derive from the fb.ai brand kit (`fivebucks_get_brand_kit`, when `FIVEBUCKS_API_KEY` set) → local `design-system/` → `brand.md` (fallback), never hardcode brand colors/fonts from memory.

**Strategic + financial context:**
- `brands/{brand}/product.md` — KPI definitions: what counts as "active user", DAU/WAU/MAU windows, feature adoption metrics, plan tier list
- `brands/{brand}/finance.md` — KPIs to highlight (MRR, ARR, gross margin, runway, top movers), runway calc method, alert thresholds
- `brands/{brand}/investors.md` — Investor List, Founder Voice sample paragraphs, Sections to Include, Sections to OMIT, Prior Updates Archive

If `brand.md`, `product.md`, `finance.md`, or `investors.md` is missing, abort with a `failed` log and tell the user which file to populate. `design-system/` missing is NOT a hard fail — fall back to brand.md and continue.

If `investors.md` has zero entries in Investor List, abort with `failed` — there is no audience to send to. Tell the user to populate `investors.md` first.

### Step 2 — Resolve the Reporting Period

Resolve `period_start`, `period_end`, `period_label`:
- Default: previous calendar month. If today = 7 May 2026 → period = 1 Apr 2026 – 30 Apr 2026, label = "April 2026".
- User-supplied: parse to ISO range. Examples: "March 2026" → 1–31 Mar 2026, "Q1 2026" → 1 Jan – 31 Mar 2026.
- Compute prior period for comparison: same length immediately before (e.g., March 2026 for an April update).

### Step 3 — Pull Financial Data from Xero

Confirm Xero MCP authentication (the tool requires the connected user's organisation). If not connected, abort and tell the user to connect Xero in Claude settings.

**Xero is a deferred MCP tool. Load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Xero__whoami,mcp__claude_ai_Xero__get_connected_user_organisation,mcp__claude_ai_Xero__get_profit_and_loss,mcp__claude_ai_Xero__get_cash_position,mcp__claude_ai_Xero__get_financial_position"
```

After loading, you can call the Xero tools directly throughout the rest of this skill — they remain in the tool schema for the duration of the run.

```
Use mcp__claude_ai_Xero__get_connected_user_organisation
```

Pull P&L for the period:

```
Use mcp__claude_ai_Xero__get_profit_and_loss:
- from_date: <period_start ISO>
- to_date: <period_end ISO>
- periods: 2  # current period + prior period for comparison
```

Pull cash position:

```
Use mcp__claude_ai_Xero__get_cash_position
```

Compute runway per `finance.md` Runway Calc Method (e.g., cash / 3-month-trailing average burn). Read the formula from `finance.md` — never hardcode.

Capture: revenue, gross margin, operating expenses, net loss/profit, cash on hand, runway in months, top expense movers (largest deltas vs prior period).

### Step 4 — Pull Stripe MRR / Churn

If the Stripe MCP is not yet authenticated, kick off the OAuth flow first:

```
Use mcp__claude_ai_Stripe__authenticate
```

Once authenticated, the Stripe MCP exposes its real tools. Load them via `ToolSearch` before calling — Stripe tools are deferred until OAuth completes. Pull for the reporting period:

- MRR at period start
- MRR at period end (delta = net new MRR)
- ARR at period end (MRR × 12)
- Active customer count at period end
- New customers added during period
- Churned customers during period (cancellations + downgrades)
- Net revenue retention (NRR) if computable from upgrades/downgrades

If the Stripe MCP cannot return one of these directly, derive from invoice/subscription line items where possible. If a metric truly cannot be computed, mark it "not available this month" — do not fabricate.

### Step 5 — Pull Product KPIs from PostHog

Use the active PostHog project (already scoped via the MCP context). Pull DAU/WAU/MAU per the windows defined in `brands/{brand}/product.md` (e.g., MAU = unique users with `event_x` in last 30 days).

```
Use mcp__claude_ai_PostHog__query-run:
- query: <HogQL query computing DAU/WAU/MAU per product.md definition for period_start..period_end>
```

Compute deltas vs prior period. Pull any other KPIs `product.md` flags as critical (e.g., "feature adoption %", "trial-to-paid conversion %", "weekly retained user cohort"). Cite the metric definition source in the output.

### Step 6 — Pull Customer Wins + Pipeline from Notion CRM

Search the brand's CRM database for closed-won deals + new prospects in the period.

1. **Resolve the DB to a `data_source_url`:**

   ```
   Use mcp__claude_ai_Notion__notion-fetch:
   - id: "${BRAND}_CRM_DB"
   ```

   Extract the `collection://` URL from the response — typically `data_sources[0].url`. Save as `data_source_url`.

   **CRM DB bootstrap check — abort cleanly if missing.** If `${BRAND}_CRM_DB` is not set in `.claude/settings.local.json` OR the fetch returns `not_found` / 404, the brand's CRM has not been bootstrapped yet. Do NOT attempt to create it here — that's `apollo-lead-prospector`'s responsibility on its first run. Abort with this user-facing message:

   > The brand's CRM database is not yet bootstrapped. Run `/link-skills:apollo-lead-prospector` first — it creates `${BRAND}_CRM_DB` on first execution. Then re-run investor-update-writer.

   Then jump to the **Final Step — Log to Dashboard** with `status: "failed"` and a summary of `"aborted: ${BRAND}_CRM_DB not bootstrapped — run apollo-lead-prospector first"`. End the run.

2. **Search inside that data source for closed-won deals:**

   ```
   Use mcp__claude_ai_Notion__notion-search:
   - query: "Stage:Closed Won"
   - data_source_url: <data_source_url from step 1>
   - query_type: "internal"
   ```

Filter results by close date inside the reporting period. Capture: client name (subject to OMIT rules — see Step 8), tier, ACV, persona, close date.

Also pull new prospects added during the period (Stage = New / Qualified) for pipeline movement context — re-run `notion-search` with the same `data_source_url` and an updated `query` (e.g. `"Stage:New"` / `"Stage:Qualified"`).

### Step 7 — Read Prior Updates Archive (Recurring Themes)

Read the last 3-6 monthly updates from `investors.md` → Prior Updates Archive section. Identify:
- **Outstanding asks** — asks raised in prior updates that are still open. Decide whether to repeat (with progress note) or retire (with closure note).
- **Recurring wins** — themes (e.g., "we keep landing FinTech logos" or "API uptime > 99.95%") that are now baseline rather than newsworthy. Avoid recycling stale wins as fresh.
- **Promised-vs-delivered** — anything the founder promised in prior updates ("we'll ship Feature X next month") and check whether it shipped. If yes, surface as a delivered win. If no, address candidly in Lowlights.

### Step 8 — Compose the Update Sections

Compose update sections per `investors.md` → "Sections to Include". The standard set is:

| Section | Source | Content |
|---|---|---|
| TL;DR | All sources synthesized | 3 bullets max — biggest win, biggest number, biggest ask. No fluff. |
| KPIs | Xero + Stripe + PostHog | Period vs prior period table. Include only metrics flagged in `finance.md` "KPIs to Highlight" + `product.md` critical KPIs. Show absolute number + delta. |
| Wins | CRM closed-won + product milestones + press hits | 3-5 specific wins. Redact customer names if `investors.md` "Sections to OMIT" forbids naming customers. Use "a Series-B FinTech in Singapore" style instead. |
| Lowlights | Honest reflection + alert thresholds from finance.md | 2-3 honest items. If runway dropped below `finance.md` alert threshold, lead with it. If churn spiked, name it. Investors.md mandates honesty. |
| Asks | Auto-derived + user-supplied custom asks | Specific, actionable asks. Format: "Intros to {company type/role/region}", "hiring help for {role}", "advice on {specific topic}". Pull recurring open asks from Step 7. |
| Hires | HR data if available, else CRM/Slack signals | Any new joiners (name, role, start date). Departures handled discreetly — name role and timing only, no editorializing. |

Match founder voice — read the "Founder Voice" sample paragraphs in `investors.md` and mirror sentence length, vocabulary, level of self-deprecation, and signature phrases. Do NOT default to corporate-PR voice.

Strip any content that hits "Sections to OMIT" rules. Apply the rules literally — if "specific customer names" is on the OMIT list, redact every customer name in the entire update, including the Wins section.

Total length: aim for 600-900 words. Investor updates that are too long don't get read.

### Step 9 — Generate the Branded Deck

Investors increasingly read updates on phones — a branded deck reads better than a wall of email text and signals operational maturity. **Gamma deck is the primary deliverable; Google Doc is the fallback when Gamma is unavailable or fails.** Mirrors `proposal-generator` Step 5 and `financial-reporter` Step 6.

**Always save the local markdown audit first** — this is the source-of-truth that survives both Gamma and Google Drive failures:

```
outputs/{brand}/investors/InvestorUpdate_{YYYYMM}.md
```

Then attempt the deck:

**Preferred path — Gamma deck** (when Gamma MCP is connected for the brand):

```
Use mcp__claude_ai_Gamma__generate_from_template:
- input_text: <markdown source from Step 8 — sections become deck cards: TL;DR → KPIs → Wins → Lowlights → Asks → Hires>
- text_options: { "amount": "preserve", "tone": "<from brand.md voice>", "language": "en" }
- card_options: { "dimensions": "16x9" }
- theme_name: "<brand theme if available, else default>"
- additionalInstructions: "Brand: {brand}. Use brand colors: primary {HEX}, accent {HEX}, background {HEX}, text/dark {HEX} (map each from the active source per the Brand kit field map in agents/link.md — fb.ai kit provides primary/accent/dark/background; local design-system/ or brand.md when the kit is null — never invent). Typography: heading {font-family} + body {font-family} (family names from fb.ai kit / local design-system/ when present, brand.md Google Font when fallback; font weight scale comes only from the local design-system, not the kit). Voice: {voice from brand.md}. The deck is a monthly investor update — KPI tables on the KPIs card, bullet wins/lowlights, callout style for the Asks card. Keep visual identity tight to the brand throughout."
- format: "presentation"
- exportAs: "pdf"
```

Capture the returned `gammaUrl` (web link) and `pdfUrl` (PDF export). These become `deck_url` and `pdf_url` downstream.

**Fallback path — Google Doc** (when Gamma MCP is unavailable for the brand, or `generate_from_template` returns an error):

```
Use mcp__claude_ai_Google_Drive__create_file:
- name: "InvestorUpdate_{YYYYMM}"
- mimeType: "application/vnd.google-apps.document"
- content: <markdown source from Step 8>
- parents: [<brand's investor folder ID from settings.local.json, or root>]
```

Capture the returned `webViewLink` as `deck_url` (set `pdf_url` to empty in this case — GDoc readers can export PDF on demand).

**On total failure** (both Gamma AND Google Drive errored): the local markdown audit at `outputs/{brand}/investors/InvestorUpdate_{YYYYMM}.md` is still preserved, but investors cannot receive a deliverable URL. Do NOT proceed to Step 10 (Gmail drafts) — sending drafts without a deck link defeats the purpose. Mirror the Step 6 abort pattern: jump directly to the **Final Step — Log to Dashboard** with `status: "failed"` and a summary of `"aborted: Gamma + Google Drive both unavailable — local markdown audit at outputs/{brand}/investors/InvestorUpdate_{YYYYMM}.md is preserved. Connect Gamma OR Google Drive and re-run."`. Skip Steps 10–12 (no Slack notify either — the dashboard log is the failure record). End the run.

Record which path produced the deck for the downstream steps:
- `deck_format` = `"gamma"` | `"gdoc"`
- `deck_url` = the URL (Gamma share link or Google Doc webViewLink)
- `pdf_url` = the Gamma PDF export URL (empty when fallback path was used)

### Step 10 — Create Gmail Drafts

Pick dispatch mode from inputs (`per-investor` default, or `bcc`).

**Per-investor mode (default):** loop over `investors.md` → Investor List. For each investor whose preferred update frequency includes this month, create one draft.

```
Use mcp__claude_ai_Gmail__create_draft:
- to: <investor.email>
- from: <founder email from brand.md>
- subject: "{Brand} Investor Update — {Month YYYY}"
- body: <short personalized opener + TL;DR section + branded deck link from Step 9 + PDF link (when Gamma path) — see structure below>
```

**Email body structure** (kept tight — the deck carries the detail):
1. **Opening** — 1-2 sentences, persona-adapted opener from `investors.md` per-role salutations (e.g., "Hi {name}, thanks again for the intro to {firm} last month"). Otherwise a generic opener in founder voice.
2. **TL;DR** — the 3 bullets from Step 8 (biggest win, biggest number, biggest ask) — investors who never open the deck still get the summary in their inbox.
3. **Deck link** — "Full update with KPI tables, wins, lowlights, and asks: **<deck_url from Step 9>**". When `deck_format = "gamma"`, also surface the PDF: "Prefer PDF? <pdf_url>".
4. **Reply CTA** — invite a reply for questions or intro asks.
5. **Signature** — founder name + title from `brand.md`.

Do NOT paste the full markdown source into the email — the deck IS the deliverable; the email is the cover note.

Personalize the opening line per investor role if `investors.md` defines per-role salutations.

**BCC mode:** create one draft to the founder's own email, with all investors on BCC.

```
Use mcp__claude_ai_Gmail__create_draft:
- to: <founder email>
- bcc: <comma-separated investor emails from investors.md>
- subject: "{Brand} Investor Update — {Month YYYY}"
- body: <same structure as per-investor mode, generic opener>
```

Save as draft (do NOT auto-send) unless user explicitly set send_mode = `send`. The founder reviews and sends manually.

### Step 11 — Archive to Notion `${BRAND}_REPORTS_DB`

Persist the update as a Notion page in the brand's reports database for permanent archive.

#### Step 11a — Ensure `${BRAND}_REPORTS_DB` exists (first-run only)

This step is primarily for the **first-ever investor-update run** for a brand. On subsequent runs, the env var is already set and the DB already exists — fetch and proceed.

Read `${BRAND}_REPORTS_DB` from `.claude/settings.local.json`.

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to 11b.
  (only create if fetch returns 404 / not_found, meaning the DB was deleted)

IF env var is NOT set:
  → first-ever run for this brand → create the DB.
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_REPORTS_DB"
```

If env var is unset (or fetch returns not_found), create:

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_id>" }
- title: "{Brand Name} Reports"
- properties: {
    "Name":          { "title": {} },
    "Type":          { "select": { "options": [
                        {"name": "Investor Update"},
                        {"name": "Financial Report"},
                        {"name": "Board Memo"}
                      ] } },
    "Period":        { "rich_text": {} },
    "Status":        { "select": { "options": [
                        {"name": "Draft"},
                        {"name": "Sent"},
                        {"name": "Archived"}
                      ] } },
    "Recipients":    { "number": { "format": "number" } },
    "Created":       { "created_time": {} }
  }
```

After creation, persist the new DB ID back to `.claude/settings.local.json` under `env.{BRAND}_REPORTS_DB` (read existing settings, add the key, preserve all other keys, write back). Notify the user in chat (first-run only).

#### Step 11b — Create the report page

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_REPORTS_DB" }
- pages: [{
    "properties": {
      "Name": "InvestorUpdate_{YYYYMM}",
      "Type": "Investor Update",
      "Period": "{period_label}",
      "Status": "Draft",
      "Recipients": <count from investors.md list>
    },
    "content": "<markdown source from Step 8 + deck URL + deck format (gamma|gdoc) + PDF URL (when gamma) + Gmail draft IDs>"
  }]
```

Capture the returned page URL.

### Step 12 — Notify Slack

DM the founder via Slack so they know drafts are ready to review and send.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "Investor update drafts ready for {period_label}.
         Deck ({deck_format}): {deck_url}{ ' — PDF: ' + pdf_url if pdf_url else '' }
         Drafts: {N} Gmail drafts pending review.
         Notion archive: {Notion URL}
         Review and send when ready."
```

### Step 13 — Log to Dashboard

See Final Step below.

---

## Output format

**Save location — local audit:**
```
outputs/{brand}/investors/
```

**Naming convention:**
```
InvestorUpdate_{YYYYMM}.md
```

Examples:
- `InvestorUpdate_202604.md` (April 2026 update)
- `InvestorUpdate_202603.md` (March 2026 update)

**Local audit metadata:**
```yaml
---
Date: YYYY-MM-DD
Skill Used: investor-update-writer
Brand: {brand}
Period: {period_label}
Period Start: YYYY-MM-DD
Period End: YYYY-MM-DD
Recipients: <count>
Dispatch Mode: per-investor | bcc
MRR: <number> {currency}
MRR Delta: <signed delta>
Runway Months: <number>
Cash: <number> {currency}
Customer Count: <number>
Churn Count: <number>
Wins Count: <number>
Asks Count: <number>
Deck Format: gamma | gdoc
Deck URL: <url>
PDF URL: <url — empty when deck_format = gdoc>
Notion Report URL: <url>
Gmail Draft IDs: [<ids>]
Status: Draft | Sent | Failed
---
```

**Deliverables produced:**
- Markdown source at `outputs/{brand}/investors/InvestorUpdate_{YYYYMM}.md` (always — survives Gamma/GDrive failures)
- Branded deck — Gamma (primary, returns `gammaUrl` + `pdfUrl`) OR Google Doc (fallback, returns `webViewLink`)
- Gmail drafts (one per investor, or one with BCC) — pending founder review, cover note + TL;DR + deck link
- Notion `${BRAND}_REPORTS_DB` archive entry
- Slack notification to `$SLACK_NOTIFY_USER`

---

## Quality checklist

Before finalizing:

- [ ] All four required context files read: brand.md + product.md + finance.md + investors.md (design-system/ is the optional fifth read — see separate design-system check below)
- [ ] Reporting period resolved correctly (default = prior calendar month; user override respected)
- [ ] Every KPI in the update comes from a real data source (Xero / Stripe / PostHog / Notion CRM) — no fabricated numbers
- [ ] Runway computed via `finance.md` Runway Calc Method — not invented
- [ ] KPI selection respects `finance.md` "KPIs to Highlight" + `product.md` critical KPIs — no random metrics
- [ ] Customer names redacted per `investors.md` "Sections to OMIT" rules — applied consistently across Wins, TL;DR, every section
- [ ] No content from `investors.md` "Sections to OMIT" appears anywhere in the update
- [ ] Founder voice mirrors "Founder Voice" sample paragraphs in `investors.md` — sentence length, vocabulary, signature phrases match
- [ ] Lowlights section is honest (2-3 items) — no rosy spin
- [ ] Outstanding asks from prior updates (Step 7) reviewed; closed asks marked closed, repeated asks include progress note
- [ ] Total update length 600-900 words
- [ ] Gmail drafts saved (not auto-sent) unless user explicitly approved sending
- [ ] Recipients count matches `investors.md` Investor List filtered by frequency for this period
- [ ] **Branded deck produced** — Gamma (primary) or Google Doc (fallback); `deck_url` captured. If both paths failed, agent aborted with `failed` log and did NOT send drafts.
- [ ] **Brand visual source resolved in 3-tier order at Step 1**: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md` Colors + Google Font; never blocked on a missing key or design-system
- [ ] **Gamma `additionalInstructions` carried explicit HEX values + font-family extracted at Step 1** (from fb.ai brand kit / design-system / brand.md) — deck visual identity matches the brand, not Gamma defaults. (N/A when the GDoc fallback path was used.)
- [ ] Gmail body is a tight cover note (opener + TL;DR + deck link + reply CTA) — NOT a paste of the full markdown source; the deck is the deliverable
- [ ] Notion archive entry includes `deck_url`, `deck_format`, and `pdf_url` (when Gamma)
- [ ] Slack notification sent to `$SLACK_NOTIFY_USER` with the deck URL
- [ ] Local audit file written to `outputs/{brand}/investors/` — survives both Gamma and Google Drive failures
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "investor-update-writer"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "period_label": "<e.g., April 2026>",
    "period_start": "YYYY-MM-DD",
    "period_end": "YYYY-MM-DD",
    "recipients": 0,
    "dispatch_mode": "<per-investor|bcc>",
    "mrr": 0,
    "mrr_delta": 0,
    "arr": 0,
    "runway_months": 0,
    "cash": 0,
    "currency": "<ISO>",
    "customer_count": 0,
    "new_customers": 0,
    "churn_count": 0,
    "dau": 0,
    "wau": 0,
    "mau": 0,
    "wins_count": 0,
    "lowlights_count": 0,
    "asks_count": 0,
    "hires_count": 0,
    "deck_format": "<gamma|gdoc>",
    "deck_url": "<url>",
    "pdf_url": "<url — empty when deck_format = gdoc>",
    "notion_report_url": "<url>",
    "gmail_draft_ids": ["<ids>"],
    "output_path": "outputs/{brand}/investors/",
    "deliverable": "InvestorUpdate_{YYYYMM}.md"
  }
```
