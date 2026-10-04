---
description: Bring an existing brand's setup up to date with the latest plugin version — detects gaps since the user last ran brand-setup and fills them interactively.
area: Setup
use_for: "Bring an existing brand's setup up to date with the latest plugin version — detects gaps since last brand-setup run and fills only what's missing (idempotent)"
deps:
  mcp: ["all (this is the audit skill — it probes everything)"]
  gateway: ["fivebucks (opt — brand kit / template / media probes + fivebucks_whoami key-scope check; **scope: social_posts**)"]
  files: []
  env: []
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.1 | July 13, 2026 |

**Description:** Bring an existing brand's setup up to date with the latest plugin version — detects gaps since the user last ran brand-setup and fills them interactively

### Change Log

**v2.20.1** — July 13, 2026
- **Corrected the fb.ai tool count referenced in the key-scope check messaging (98 → 100), matching the same correction made across the other v2.20.0 skills.**

**v2.20.0** — July 12, 2026
- **fb.ai key scope check for existing brands.** Repointed the stale api-keys links to `/dashboard/api-keys` and added a `fivebucks_whoami` probe: keys generated before scoping are **legacy full-access keys and keep working** (empty `scopes` — no action needed), but a regenerated key missing `social_posts` will silently break the fb.ai-dependent skills. Reports the granted scopes + quota snapshot and surfaces `auth/key-expired`.

**v2.19.0** — July 03, 2026
- **Corrected Zernio ad-account discovery tool name (fixes the v2.18.0 migration bug).** v2.18.0 assumed Zernio just drops the `late_` prefix, but Zernio's tools are resource-prefixed. Step 2/Step 3 ad-account resolution now calls **`ads_list_ad_accounts`** (was `list_ad_accounts`). `profiles_list` / `accounts_list` were already correct.

**v2.18.0** — July 01, 2026
- **Migration support for the Zernio + DataforSEO gateway split-off (gateway v1.7.4/v1.7.5) and Argil retirement.** Step 1e adds Zernio (`profiles_list` — success = authorized) and DataforSEO (`keywords_data_google_ads_search_volume`, optional) connector probes. Step 3f renames every `${BRAND}_LATE_*` env var → `${BRAND}_ZERNIO_*`, removes the now-defunct `LATE_API_KEY` (Zernio is OAuth — no key), and updates the auto-discover tool names (`profiles_list` / `accounts_list` / `list_ad_accounts`, no longer gateway-routed). Step 3g adds a **Zernio (required, OAuth)** connector walkthrough and a **DataforSEO (optional, Basic Auth)** connector walkthrough. Step 3k adds a brand-action row mapping this release — reconnect Zernio + DataforSEO as their own custom connectors and re-run account discovery, since Zernio's own API may return different SocialAccount `_id`s than the old gateway-proxied Late API.

**v2.17.0** — June 21, 2026
- **Migration support for the Inbound Gig Engine completion (v2.17.0 Sales skills `gig-proposal-writer` / `n8n-workflow-builder` / `vsl-demo-producer`).** Step 1e adds an **n8n Cloud MCP** probe (`get_workflow_best_practices`) — optional, only needed by `n8n-workflow-builder`. Step 3g adds the n8n Cloud connect-walkthrough prompt. Step 3k maps the new `Inbound Gig Engine completed` changelog entry to its optional brand action (connect n8n Cloud + optional `${BRAND}_N8N_PROJECT`). The three skills are auto-detected from the shipped `skills-manifest.json` (Step 1 registry read); no per-brand context file is required beyond what `gig-prospector` already needs.

# Plugin Update — Catch Existing Brands Up to Latest Plugin Version

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are the upgrade agent for the Link marketing plugin. The user has already run `brand-setup` at some earlier plugin version, and the plugin has since added new requirements (mandatory files, env vars, MCPs, CLAUDE.md sections, etc.). Your job is to **detect what's missing** in the current brand setup and walk the user through filling **only those gaps** — never re-run steps that are already complete.

This skill is **idempotent**. Running it twice in a row should produce a clean "nothing to do" report on the second pass.

## When to invoke

- After upgrading to a new plugin version (e.g. `git pull` in the marketplace folder)
- When a brand was set up months ago and skills are throwing "missing file / missing env var" errors
- User says "update", "upgrade", "catch up", "what's missing", "plugin-update"

## How this differs from brand-setup

| Aspect | brand-setup | plugin-update |
|---|---|---|
| When | First time, new brand | Existing brand, after plugin upgrade |
| Greenfield | Yes — writes everything | No — only fills gaps |
| Order | Linear, all 10 steps | Skips anything already complete |
| Re-asks for known data | Yes | No — reuses what's on disk |

If `brands/{brand}/` does not exist at all, this skill exits and tells the user to run `/link-skills:brand-setup` first.

## What this skill does

When you upgrade the plugin (e.g. `git pull` in the marketplace folder), some skills will have new requirements — new brand context files, new env vars, new MCP integrations, new sections in `brand.md`. Plugin-update is the **idempotent catch-up runner**: it inspects every brand asset, env var, MCP probe, and `CLAUDE.md` setting against the current plugin's expectations, then walks you through filling **only the gaps**. It never re-asks for data that's already on disk.

**Estimated time:** 5–30 minutes for a typical run. A clean brand (no gaps) finishes in ~5 minutes (mostly automated inspection). A heavily-outdated brand (e.g. last set up 6 months ago, missing the v2.4.0 sales/finance/customer-success files) can take 30–60 minutes if you choose to fill all the new context files in this session.

**The 6 steps:**

| # | Step | Purpose | Time |
|---|---|---|---|
| 0 | Determine version gap | Read current plugin version + brand's last-applied version; build the changeset that needs catching up | ~30 sec (auto) |
| 1 | Detect current state | Inspect every brand file, env var, MCP connector, CLAUDE.md section — no user prompts, just look | 1–2 min (auto) |
| 2 | Show the gap report | Compact summary of what's present / missing / optional, grouped by category. One question: "want to fill these now?" | 1 min |
| 3 | Fill the gaps interactively | Walk through each missing item in order. Each fill delegates to the matching brand-setup sub-step | 2–60 min (variable) |
| 4 | Re-validate | Test only the integrations touched in Step 3 to confirm fixes worked | 1–2 min |
| 5 | Record version + email + Slack | Write current plugin version to `brand.md`, send completion email, DM Slack | 30 sec |

The skill is **idempotent** by design — running it twice in a row should produce a clean "nothing to do" report on the second pass. You can pause anywhere (e.g. say "skip" to a gap you don't want to fill now) and re-run later to pick up where you left off.

---

## Step 0 — Determine version gap

First the agent figures out **what changed** between the version your brand was set up at and the version you have installed now. It reads `version.ts` for the current installed version, looks at `brands/{brand}/brand.md` for the brand's last-applied version stamp, and reads every skill's maintenance section to build a per-skill version delta. The output is a list of what's new since the brand was last configured — the input that drives Step 3's brand-action mapping.

**Expect ~30 seconds.** Fully automated. Only asks you a question if the brand's last-applied version is missing from `brand.md` (in which case it asks you to recall when the brand was last set up).

### 0a. Read current plugin version

Open `plugins/link-skills/versions/version.ts` and read `DEFAULT_VERSION` (e.g. `v2.2.15`). This is the version the user has installed right now.

### 0b. Read last-applied version for this brand

Open `brands/{brand}/brand.md` and look for a `## Plugin Version` section:
- If present → `last_applied = that version string`
- If missing → ask the user: "What version were you on when you last ran brand-setup or plugin-update? (Run `git log --oneline -5` in this folder if unsure.)"
- If unknown → treat `last_applied = v2.0.0` (full audit)

### 0c. Read skill and agent maintenance sections

For each of the following files, read the `## Maintenance` block and extract the `Version` value from the table:

| File | Extract |
|---|---|
| `plugins/link-skills/agents/link.md` | Version |
| `plugins/link-skills/skills/brand-setup/SKILL.md` | Version |
| `plugins/link-skills/skills/content-generator/SKILL.md` | Version |
| `plugins/link-skills/skills/creative-designer/SKILL.md` | Version |
| `plugins/link-skills/skills/content-creation/SKILL.md` | Version |
| `plugins/link-skills/skills/social-calendar/SKILL.md` | Version |
| `plugins/link-skills/skills/digital-marketing-analyst/SKILL.md` | Version |
| `plugins/link-skills/skills/data-analysis/SKILL.md` | Version |
| `plugins/link-skills/skills/social-publisher/SKILL.md` | Version |
| `plugins/link-skills/skills/research-strategy/SKILL.md` | Version |
| `plugins/link-skills/skills/campaign-presenter/SKILL.md` | Version |
| `plugins/link-skills/skills/background-generator/SKILL.md` | Version |
| `plugins/link-skills/skills/plugin-update/SKILL.md` | Version |

### 0d. Build the version delta

Flag each skill/agent whose maintenance `Version` is **newer than `last_applied`**. These are the files that changed since the user's brand was last configured. Also flag any skill/agent that is **new** (did not exist at `last_applied` — compare the file list on disk against what version.ts history shows was introduced).

---

## Step 1 — Detect current state

Now the agent does a **read-only inspection sweep** of everything related to this brand — folder contents, brand.md sections, env vars, MCP connectors, CLAUDE.md, Notion DBs, template uploads, skill versions. No questions yet, no fixes — just look. Each sub-step (1a–1j) checks one category and tags items as present / missing / drift. The output of this step is the gap report you'll see in Step 2.

**Expect 1–2 minutes.** Mostly automated; a few MCP probes will hit external services (e.g. Notion, Apollo, Xero) which can be slow if connections are flaky.

Read everything that exists for the active brand. Do **not** prompt the user yet — just inspect.

### 1a. Brand folder contents

Check existence of each path under `brands/{brand}/`. Mark present/missing:

| Path | Required since | Status |
|---|---|---|
| `brand.md` | v2.0 | present / missing |
| `product.md` | v2.0 | present / missing |
| `audience.md` | v2.0 | present / missing |
| `competitors.md` | v2.0 | present / missing |
| `funnel.md` | v2.1.0 | present / missing |
| `avatars.md` | v2.1.0 | present / missing |
| `logo.png` | v2.0 | present / missing |
| `backgrounds/` | v2.0 (now empty by design) | present / missing |
| `design-system/` | v2.2.10 (optional — brand.md fallback since v2.2.15) | present / missing |
| `sales.md` | v2.4.0 | present / missing |
| `customer-success.md` | v2.4.0 | present / missing |
| `finance.md` | v2.4.0 | present / missing |
| `investors.md` | v2.4.0 (optional — only required if brand has raised external capital) | present / missing |
| `operations.md` | v2.4.0 (optional — meeting-analyzer falls back gracefully) | present / missing |

**Inline schema check — sales.md Booking URL.** If `sales.md` is present, open it and verify the `## Sender Persona` block contains a non-empty `Booking URL:` line. If missing → flag as ⚠ schema gap and route to `brand-setup` Step 5g Step A backfill (single-question fix — only the Booking URL is asked, no need to re-walk the rest of the sub-step). The `outreach-sequencer` standing-link fallback, the `customer-onboarder` kickoff fallback, and the `{link}` placeholder in Reply Routing all depend on this field; brands set up before it was introduced will silently use empty CTAs until backfilled.

**Inline schema check — sales.md Inbound Job Filters (v2.16.0).** If `sales.md` is present, check for a `## Inbound Job Filters` section. If missing → flag as ⏭ optional schema gap and route to the Step 3a targeted backfill (`brand-setup` Step 5g Step H — markets, platforms + account status, product.md-derived search keywords, budget/exclusions/cap). This section powers `gig-prospector`; without it that one skill can't run, but no existing skill breaks — so it's optional, not a required gap. Skip silently for brands that don't pursue freelance/marketplace work.

### 1b. brand.md sections

Read `brands/{brand}/brand.md` and check for these section headers (added in different versions):

| Section | Required since | Status |
|---|---|---|
| `## Tagline` | v2.0 | present / missing |
| `## Voice & Tone` | v2.0 | present / missing |
| `## Colors (HEX codes)` | v2.0 | present / missing |
| `## Locale` (Currency / Timezone / Meta USD exchange rate) | v2.2.0 | present / missing |
| `## Approved Phrases` | v2.0 | present / missing |
| `## Do NOT Say` | v2.0 | present / missing |
| `## Social Publishing` (Zernio profile + connected platforms) | v2.2.1 | present / missing |
| `## Content Strategy` (Primary channel + distribution platforms + cadence) | v2.14.0 | present / missing |

### 1c. funnel.md schema

Open `brands/{brand}/funnel.md` if present. Confirm it has:
- `## Stages (Google Ads)` table with GA4 event mappings
- `## Stages (Meta Ads)` table
- `## Cost Benchmarks` table
- No remaining `TBD` event names (if any → flag for re-mapping)

### 1d. Env vars in `.claude/settings.local.json`

Read `.claude/settings.local.json` (search up from cwd). Check the `env` block:

**Required:**
| Env var | Required since |
|---|---|
| `FIVEAGENTS_API_KEY` | v2.0 |
| `GEMINI_API_KEY` | v2.0 |
| `SLACK_NOTIFY_USER` | v2.0 |
| `REPORT_EMAIL` | v2.0 |
| `{BRAND}_ZERNIO_FB` / `_IG` / `_LI` | v2.2.1 |
| `{BRAND}_ZERNIO_TT` / `_TW` (TikTok / Twitter-X organic — `video-repurposer`, YouTube-First) | v2.14.0 |
| `{BRAND}_NOTION_DB` | v2.2.10 (social-calendar bootstraps if missing) |

> **Note:** Zernio (formerly Late) moved to its own OAuth MCP in gateway v1.7.4 — there is no longer a `LATE_API_KEY` env var. Authorization is handled by connecting the Zernio custom connector (Step 3g), not by saving a key.

**Optional:**
| Env var | Notes |
|---|---|
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | Keyword research |
| `DEFAULT_BRAND` | Workspace default brand |
| `{BRAND}_ZERNIO_GOOGLE_ADS` (Zernio SocialAccount `_id`) + `{BRAND}_ZERNIO_GOOGLE_ADS_CID` (Google Ads customer ID, 10-digit) | Both required for the Windsor.ai fallback in digital-marketing-analyst / data-analysis. Zernio's Google Ads tools take `account_id` AND `ad_account_id` — passing only the SocialAccount ID returns empty results. |
| `{BRAND}_ZERNIO_META_ADS_ACCOUNT_ID` | Meta Ads account ID for Windsor.ai fallback in digital-marketing-analyst / data-analysis (v2.5.0) |
| `{BRAND}_ZERNIO_LINKEDIN_ADS` (Zernio SocialAccount `_id`) + `{BRAND}_ZERNIO_LINKEDIN_ADS_CID` (LinkedIn sponsored account ID, numeric) | Both required for the LinkedIn Ads Windsor.ai fallback in digital-marketing-analyst / data-analysis. Same two-ID pattern as Google Ads — passing only the SocialAccount ID returns empty results. Optional: skip if the brand does not run LinkedIn Ads. |

**Auto-bootstrapped (no user action required at setup; created on first run of the relevant skill):**
| Env var | Bootstrapped by | Required since |
|---|---|---|
| `${BRAND}_CRM_DB` | apollo-lead-prospector / outreach-sequencer / proposal-generator | v2.4.0 |
| `${BRAND}_CUSTOMER_DB` | customer-onboarder / churn-predictor | v2.4.0 |
| `${BRAND}_INVOICE_TRACKER_DB` | invoice-collector | v2.4.0 |
| `${BRAND}_REPORTS_DB` | financial-reporter / investor-update-writer | v2.4.0 |
| `${BRAND}_COMPETITOR_DB` | competitor-monitor | v2.4.0 |
| `${BRAND}_MEETINGS_DB` | meeting-analyzer | v2.4.0 |
| `${BRAND}_ACTIONS_DB` | meeting-analyzer | v2.4.0 |
| `${BRAND}_PERFORMANCE_DB` | content-performance-analyst | v2.13.0 |
| `${BRAND}_TREND_DB` | trend-radar | v2.13.0 |
| `${BRAND}_GIGS_DB` | gig-prospector | v2.16.0 |

For each: if present + the matching DB exists in Notion → ✅ skip. If missing → not flagged as a gap (the skill will create on first run). The audit reports presence informationally only.

For each missing key, mark whether it's required or optional.

### 1e. MCP connectors

You cannot directly probe what the user has connected in Claude settings. Instead, **lazily test** each one with a low-cost call and treat connection errors as "not connected":

| MCP | Probe | Required since |
|---|---|---|
| Five Agents (gateway) | `fiveagents_log_run` (test entry) | v2.0 |
| Zernio (own MCP, OAuth) | `profiles_list` (success = authorized) | v2.18.0 (formerly Late, gateway-routed; split to its own custom connector in gateway v1.7.4 — `https://mcp.zernio.com/mcp`) |
| DataforSEO (own MCP, Basic Auth) | `keywords_data_google_ads_search_volume` with a trivial keyword (optional) | v2.18.0 (formerly gateway-routed; split to its own custom connector in gateway v1.7.5 — `https://mcp.dataforseo.com/mcp`; only needed for keyword research — never flag as a required gap) |
| Notion | `notion-search` query="ping" | v2.0 |
| Slack | `slack_search_users` query="me" | v2.0 |
| Gmail | `list_labels` | v2.0 |
| Google Calendar | `list_calendars` | v2.0 |
| Windsor.ai | `get_connectors` | v2.1.0 |
| Canva | `list-brand-kits` | v2.1.0 |
| Playwright | check `claude mcp list` (Bash) | v2.1.4 (website analysis in brand-setup Step 4 — template rendering now uses gateway) |
| Apollo.io | `apollo_users_api_profile` | v2.4.0 |
| Calendly | OAuth status check (Calendly MCP gates real tools behind authenticate) | v2.4.0 |
| Stripe | OAuth status check (Stripe MCP gates real tools behind authenticate) | v2.4.0 |
| Xero | `whoami` | v2.4.0 |
| PostHog | `user-get` | v2.4.0 (used by `churn-predictor`; `data-analysis` may already validate it — reuse if so) |
| Gamma | `get_themes` | v2.4.0 (used by `investor-update-writer`; `campaign-presenter` may already validate it — reuse if so) |
| n8n Cloud | `get_workflow_best_practices` (technique="list") | v2.17.0 (optional — used by `n8n-workflow-builder` for inbound-gig proof workflows; never flag as a required gap — only relevant if the brand pursues marketplace work) |
| Meta Ads MCP *(optional enhancement — limited rollout)* | attempt any `ads_*` tool call (e.g. `ads_get_ad_accounts`); 401 / not-found → not connected | v2.2.13 (Windsor.ai already covers Meta data fully when this isn't connected — never flag as a required gap) |

### 1f. Workspace CLAUDE.md

Check `CLAUDE.md` at the workspace root (alongside `brands/`).

| Item | Required since |
|---|---|
| File exists | v2.2.7 |
| Contains `## Agent Identity` block | v2.2.7 |
| `link.md` path is **absolute** (`os.path.isabs == True`) | **v2.2.10** |
| `link.md` path is correct (file exists at that location) | v2.2.7 |
| Contains `## Credential Loading` block with `load_credentials()` snippet | v2.2.7 |
| `## Active Brand` section names the current brand | v2.2.7 |
| Version stamp `<!-- link.md version: ... -->` present inside BEGIN/END markers | v2.3.0 |
| Version stamp matches current `agents/link.md` Maintenance version (will be refreshed in Step 3g regardless) | v2.3.0 |

### 1g. Claude Code settings

Read `.claude/settings.local.json` and `~/.claude/settings.json` for:

| Setting | Required since |
|---|---|
| Bypass permissions mode (`Allow bypass permissions mode`) | v2.2.3 |
| Domain Allowlist set to **All Domains** | v2.2.4 |
| Project Permission set to **Act without asking** | v2.2.5 |

These are UI settings — surface them to the user as a manual checklist if you can't read them programmatically.

### 1h. fb.ai social templates

Social templates live on fb.ai (brand-setup Step 4c), **not on disk** — there is no local folder, version hash, or gateway upload to reconcile. Detect which exist for this brand:

```
Use gateway MCP tool fivebucks_list_templates:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Record which of the four `type`s are present: `meta-carousel`, `meta-story`, `linkedin-post`, `meta-post`. If `FIVEBUCKS_API_KEY` isn't set (no fb.ai plan), skip this step — the brand uses the Gemini + Pillow fallback for all formats. Missing types are an install opportunity, not a failure (see Step 3c).

### 1i. fb.ai media library

Check whether the brand has any media uploaded via `fivebucks_list_media_folders`. If `FIVEBUCKS_API_KEY` isn't set, skip — record as N/A.

```
Use gateway MCP tool fivebucks_list_media_folders:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Result is non-empty → ✅ media library populated.
- Result is empty → ⏭ no brand photos uploaded (offer to set up in Step 3d; skills fall back to Gemini image generation when empty).

### 1j. Notion DB for social calendar

If `{BRAND}_NOTION_DB` is set:
- `notion-fetch` it. If success and the returned object is a database with `Name` (title) property → OK.
- If the fetch returns `not_found` or the object is not a database → mark for re-bootstrap.

If `{BRAND}_NOTION_DB` is unset → mark as missing (social-calendar will bootstrap on first run, but we offer to do it now).

### 1k. Skill and agent version audit

Using the data collected in Step 0, build a version table. **Read actual versions from disk — do not use the example below as current data.**

*(Example format only — versions shown here are illustrative, not current):*

| File | Installed version | Changed since {last_applied}? |
|---|---|---|
| agents/link.md | v2.3.0 | ✅ yes |
| brand-setup | v2.2.15 | ✅ yes |
| content-generator | v2.2.15 | ✅ yes |
| creative-designer | v2.2.15 | ✅ yes |
| content-creation | v2.2.15 | ✅ yes |
| social-calendar | v2.2.15 | ✅ yes |
| background-generator | v2.2.15 | ✅ yes |
| digital-marketing-analyst | v2.3.0 | ✅ yes |
| data-analysis | v2.3.0 | ✅ yes |
| social-publisher | v2.2.5 | — no |
| research-strategy | v2.2.5 | — no |
| campaign-presenter | v2.2.5 | — no |
| plugin-update | v2.3.0 | ✅ yes (new) |
| `apollo-lead-prospector` | v2.4.0 | ✅ yes (new) |
| `outreach-sequencer` | v2.4.0 | ✅ yes (new) |
| `proposal-generator` | v2.4.0 | ✅ yes (new) |
| `customer-onboarder` | v2.4.0 | ✅ yes (new) |
| `churn-predictor` | v2.4.0 | ✅ yes (new) |
| `invoice-collector` | v2.4.0 | ✅ yes (new) |
| `financial-reporter` | v2.4.0 | ✅ yes (new) |
| `competitor-monitor` | v2.4.0 | ✅ yes (new) |
| `investor-update-writer` | v2.4.0 | ✅ yes (new) |
| `meeting-analyzer` | v2.4.0 | ✅ yes (new) |

Flag any skill that is entirely **new** (folder exists on disk but `last_applied` predates its introduction). For each changed/new skill, extract the relevant changelog bullets from its `### Change Log` section — these drive Step 3k.

**Registry source.** Read the plugin's `skills-manifest.json` — it ships **pre-generated** from each skill's frontmatter, and its sync is enforced at release time by `commit-to-git` Step 4f. plugin-update runs in the user's Cowork project and does **not** regenerate or `--check` it (that's a maintainer/CI step) — it just reads the shipped manifest for each skill's `area` / `deps`. Reading the manifest needs no tooling; it's plain JSON.

---

## Step 2 — Show the gap report

The agent shows you a **single compact summary** of every category checked in Step 1 — what's present (✅), what's missing required (❌), what's missing optional (⏭). You see the whole picture before any fix work starts, so you can scan it and decide whether to walk through the gaps now or come back later. Optional gaps (e.g. design-system, social templates, investors.md if you haven't raised) are clearly marked so you don't feel pressured to fill them.

**Expect 1 minute.** Single question at the end: "Want me to walk through these gaps now?" If you say no, the skill exits cleanly and the gap report is logged to memory so you can revisit later.

Build a **compact gap table** and show it to the user before doing anything. Group by category. Mark each item as ✅ (present) / ❌ (missing required) / ⏭ (optional missing). Example:

```
[{brand}] Plugin Update — Gap Report
Plugin version: {last_applied} → {DEFAULT_VERSION}

Skills/agents updated since {last_applied}
  ✅ agents/link.md       v2.7.0  social templates → fb.ai (fivebucks_* tools)
  ✅ brand-setup          v2.2.15  Step 4c rewrite (EDITMODE contracts); design-system/ now optional
  ✅ content-generator    v2.7.0  render via fb.ai fivebucks_* (Step 4c-template)
  ✅ creative-designer    v2.2.15  template-path → gateway; design-system/ optional
  ✅ content-creation     v2.2.15  _copy.json output; naming convention split
  ✅ social-calendar      v2.2.15  Direction column added (11 columns)
  ✅ plugin-update        v2.3.0   new skill

Brand context files
  ✅ brand.md, product.md, audience.md, competitors.md, funnel.md, avatars.md, logo.png
  ❌ sales.md                             ← v2.4.0 (apollo-lead-prospector / outreach-sequencer / proposal-generator)
  ❌ customer-success.md                  ← v2.4.0 (customer-onboarder / churn-predictor)
  ❌ finance.md                           ← v2.4.0 (invoice-collector / financial-reporter)
  ⏭ investors.md                         ← v2.4.0 optional (only required if brand has raised external capital)
  ⏭ operations.md                        ← v2.4.0 optional (only required if user processes meeting transcripts)
  ⏭ design-system/                       ← optional (recommended; brand.md fallback if absent)

fb.ai social templates (Step 1h — needs FIVEBUCKS_API_KEY)
  ⏭ meta-carousel / meta-story / linkedin-post / meta-post — which exist on fb.ai? (install via Step 3c)

fb.ai media library (Step 1i — needs FIVEBUCKS_API_KEY)
  ⏭ no media folders found — upload brand photos via Step 3d

brand.md sections
  ✅ Tagline / Voice & Tone / Colors / Approved Phrases / Do NOT Say
  ❌ Locale (Currency / Timezone / Meta USD)        ← v2.2.0
  ❌ Social Publishing (Zernio profile + accounts)  ← v2.2.1

Env vars (.claude/settings.local.json)
  ✅ FIVEAGENTS_API_KEY, GEMINI_API_KEY, SLACK_NOTIFY_USER, REPORT_EMAIL
  ❌ {BRAND}_ZERNIO_FB, {BRAND}_ZERNIO_IG, {BRAND}_ZERNIO_LI
  ❌ {BRAND}_NOTION_DB                    ← will be created by social-calendar on first run, or bootstrap now

MCP connectors
  ✅ Five Agents, Notion, Slack, Gmail, Google Calendar
  ❌ Zernio (required for social-publisher — reconnect as its own OAuth connector; formerly gateway-routed)
  ❌ Windsor.ai (required for digital-marketing-analyst)
  ❌ Canva (required for campaign-presenter)
  ❌ Playwright (required for website analysis in brand-setup Step 4)
  ❌ Apollo.io (required for apollo-lead-prospector, outreach-sequencer)
  ❌ Calendly (required for customer-onboarder, meeting-analyzer)
  ❌ Stripe (required for invoice-collector, financial-reporter)
  ❌ Xero (required for invoice-collector, financial-reporter)
  ⏭ DataforSEO (optional — keyword research; reconnect as its own Basic Auth connector)
  ⏭ PostHog (optional — churn-predictor falls back to support-ticket + login signals)
  ⏭ Gamma (optional — investor-update-writer needs it; skip if you don't deliver investor decks)
  ⏭ Meta Ads MCP (optional enhancement — Windsor.ai already covers Meta Ads fully)

Workspace CLAUDE.md
  ❌ link.md path is RELATIVE — must be absolute (v2.2.10)
  ✅ Agent Identity block
  ✅ Credential Loading block

Settings
  Manual: confirm Bypass permissions ON, Domain Allowlist = All Domains, Project = Act without asking

→ {N} required gaps · {M} optional gaps · ready to walk through them?
```

Ask the user:
> Want me to walk through these gaps now? I'll skip anything you say "skip" to. Anything I miss won't break — just won't be set up.

If the user says no / not now, exit cleanly and offer to re-run later. Log the gap report to memory either way.

---

## Step 3 — Fill the gaps interactively

The agent walks through each missing item in order, **only prompting for items that came back ❌ or ⏭ in Step 2** — never re-asking for known-good state. For most fills, the agent delegates to the matching brand-setup sub-step (e.g. missing `sales.md` triggers `brand-setup` Step 5g, a Zernio connector not authorized triggers brand-setup Step 7a-ii Zernio OAuth authorize flow). You can say "skip" to any optional gap.

**Expect 2–60 minutes** depending on how many gaps you have. A brand with 3 missing context files + 2 missing env vars + a CLAUDE.md path fix takes ~10 min. A brand with 10+ gaps and lots of optional templates can stretch to an hour. The skill saves progress as it goes, so you can interrupt and resume.

Walk through each missing item in this order. **Skip any that came back ✅ in Step 2** — never re-prompt for known-good state.

### 3a. Brand context files (only if missing)

For each missing file in `brands/{brand}/`:

**Pre-fill rule — applies to every v2.4.0 file below (sales / customer-success / finance / investors / operations).** In a plugin-update context, the brand has been around for a while, so the v2.0 files (`brand.md`, `product.md`, `audience.md`, `competitors.md`, `funnel.md`) almost always already exist with rich content. **You MUST follow the "Read existing context first" mapping table at the top of each brand-setup sub-step (Step 5g intro, 5h intro, 5i intro, 5j intro, 5k intro) before asking the user anything.** Read those source files, draft answers from them, then ask "Confirm or edit?" per block — never ask from scratch what's already on disk. In a plugin-update context this rule is essentially mandatory because the source data is virtually guaranteed to exist; in a fresh brand-setup run it is best-effort because the source files are being built up in the same session.

- `brand.md` / `audience.md` missing → run `brand-setup` Step 4 (Website Analysis) for this brand only. Re-extract from the website.
- `product.md` / `competitors.md` missing → run `/link-skills:research-strategy` to regenerate.
- `funnel.md` missing → run `brand-setup` Step 5 funnel block (ask user about funnel + GA4 events).
- `avatars.md` missing → run `brand-setup` Step 5 avatars block.
- `logo.png` missing → ask the user for the file path, copy into `brands/{brand}/logo.png`.
- `backgrounds/` missing → just `mkdir`. No content needed (Gemini generates fresh per post since v2.2.9).
- `sales.md` missing → run `brand-setup` Step 5g (Sales context). **Apply the Read-first pre-fill table at the top of Step 5g** — Sender Persona drafts from brand.md (founder name/title), ICP filters draft per persona from audience.md, disqualification blocklist drafts from competitors.md URLs, default tier per persona drafts from product.md Pricing. Only ask the user from scratch for fields that have no source.
- `sales.md` present but Sender Persona is missing `Booking URL:` (flagged by Step 1a inline schema check) → ask only the single question: "What's your public Calendly scheduling link (e.g. `https://calendly.com/you/intro-call`)?" Append `- Booking URL: {url}` to the Sender Persona block of `brands/{brand}/sales.md`. Do NOT re-run the full Step 5g — Sender Persona Name/Title/Signature/Photo are already populated; this is a targeted backfill only.
- `sales.md` present but missing `## Inbound Job Filters` (flagged by Step 1a inline schema check) → ask first: "Does this brand pursue freelance/marketplace work (Upwork, Freelancer.com, etc.)?" If no → skip (not a gap; `gig-prospector` simply won't run). If yes → run `brand-setup` Step 5g **Step H** only: confirm Markets, Platforms + account status, **draft Search Keywords from `product.md`** (never hardcode), then Budget Floor / Exclusions / Daily Cap. Append the `## Inbound Job Filters` section to `brands/{brand}/sales.md` — do NOT re-walk the rest of Step 5g. `${BRAND}_GIGS_DB` auto-bootstraps on `gig-prospector`'s first run.
- `customer-success.md` missing → run `brand-setup` Step 5h. **Apply the Read-first pre-fill table at the top of Step 5h** — Plan Tiers drafts from product.md Pricing, Onboarding Milestone trigger events draft from funnel.md GA4 events, Intervention Playbook copy drafts from brand.md voice. Only ask the user from scratch for fields that have no source.
- `finance.md` missing → run `brand-setup` Step 5i. **Apply the Read-first pre-fill table at the top of Step 5i** — Escalation Tone Ladder copy drafts from brand.md voice, currency / Alert Threshold formatting from brand.md `## Locale`, KPIs to Highlight defaults to MRR/ARR if product.md Pricing implies subscription else project margin / cash collected. Only ask the user from scratch for fields that have no source.
- `investors.md` missing → ask first: "Have you raised external capital?" If no → skip (not flagged as gap). If yes → run `brand-setup` Step 5j. **Apply the Read-first pre-fill table at the top of Step 5j** — Sections to Include KPIs draft from finance.md (if present), drafting tone falls back to brand.md voice if user pastes <2 prior updates, sender attribution drafts from sales.md Sender Persona. Only ask the user from scratch for the investor list and prior-updates archive (those have no other source).
- `operations.md` missing → ask first: "Do you run regular meetings (1:1s, standups, client calls) and want Claude to process transcripts?" If no → skip (not flagged as gap; meeting-analyzer falls back). If yes → run `brand-setup` Step 5k. **Apply the Read-first pre-fill table at the top of Step 5k** — Sales tasks owner drafts from sales.md Sender Persona, Customer issues owner drafts from customer-success.md CSM mentions, Finance tasks owner drafts from finance.md alert recipient. Only ask the user from scratch for owners that have no other-file source.
- `competitors.md` extension missing (existing file present but lacks `monitor_urls` / `track_pages` / `exec_team` per competitor) → run `brand-setup` Step 5l. Prompts user to add the new fields per existing competitor entry.

### 3b. design-system/ (optional — recommended)

**fb.ai context — show this before any fivebucks.ai link.** fivebucks.ai (fb.ai) is a **paid** product. Never give the user a `fivebucks.ai` URL or ask them to upload there (the optional upload below, plus Steps 3c and 3d all do) without first explaining what it is:
> **About fb.ai (fivebucks.ai):** it's an optional **paid subscription** that stores your **design system and social templates** in the cloud, so Claude can **automate your branded social posting** — generating and publishing fully on-brand Carousels, Stories, and IG / FB / LinkedIn posts for you. Your design system also lives locally for **free**, so you can start without paying; the fb.ai plan adds the hosted social templates and lets posts render in your exact brand colors and fonts. You can skip fb.ai entirely — Claude falls back to the colors and fonts in `brand.md` plus Gemini rendering, which stays fully supported.

If `brands/{brand}/design-system/` is missing, offer installation but accept "skip" — the brand.md colors and fonts are a fully functional fallback:

> Your brand doesn't have a Claude Design system installed. It's optional — skills fall back to the colors and fonts in `brand.md`. Installing it gives tighter visual consistency across all outputs. Want to set it up now?

If yes, walk the user through `brand-setup` Step 4b:
1. Open https://claude.ai/design → go to **Design System** → click **Create**
2. On the **"Set up your design system"** page, fill the attach form — **Company name and blurb**; optionally attach a GitHub repo / local code / a **.fig** file / **fonts, logos and assets**; and paste the colors, fonts, and voice already in `brands/{brand}/brand.md` into **Any other notes** — then click **Continue to generation**
3. On the generation prompt, paste a website-aware prompt so Claude validates against the live site. Substitute the brand's website URL (ask the user if it isn't already known, or pull it from `brand.md`):
   ```
   This is my website: {WEBSITE_URL} — please read it and use it to validate and fill in my colors, typography, components, spacing, and overall visual style.
   Confirm and refine against the site: colors (primary / secondary / accent), heading + body fonts, and brand voice from brand.md.
   Build a complete, reusable design system: color tokens, a type scale, buttons, cards, headers / nav, and spacing.
   ```
   Iterate until it feels on-brand.
4. Share → Download Project as .zip → unzip (leave it wherever it is — e.g. `~/Downloads/Acme Design System`; no need to move it)
5. Ask the user for the path to the unzipped folder, then request access to *that exact path* before reading it — the user approves it in a one-time prompt:
   ```
   mcp__cowork__request_cowork_directory(path="<the path the user gave>")
   ```
   Required in the Cowork harness (filesystem access is sandboxed to approved directories); request the folder the user named, not a guessed default. In local Claude Code this tool is absent and the filesystem is already accessible — skip the request. If the user declines, ask them to move the folder inside the project mount, then copy from there.
6. Once access is approved, copy the folder into `brands/{brand}/design-system/` (Python `shutil.copytree`, handling the single-inner-folder nested-zip case — see brand-setup Step 4b-C).

Verify `brands/{brand}/design-system/` exists and is non-empty before marking complete. If the user skips, mark as ⏭ — not a gap that blocks any skill.

**Optional fb.ai upload:** after the local copy is in place, ask whether the user also wants to upload the design system to fb.ai (only useful with a paid fb.ai plan — lets fb.ai social templates render with the brand's colors/fonts). If yes:
1. Go to https://www.fivebucks.ai/dashboard/api-keys — generate API Key if not done yet *(skip if already generated)*
2. Go to https://www.fivebucks.ai/dashboard/social-posts/brand-kit — click **Upload Design System Zip** and upload the ZIP.

The fb.ai upload is optional — the local `design-system/` already works everywhere. Skip is fine.

### 3c. Optional fb.ai social templates (offer, don't force)

From Step 1h you know which of the four `type`s exist on fb.ai. For any **missing** type the brand would benefit from, offer to set it up — but accept "skip":

> Want to set up any optional social templates? Pick any of the four: Meta Carousel (IG/FB carousel), Meta Story (IG/FB 9:16), LinkedIn Post (LinkedIn single-image), Meta Post (IG/FB single-image). They make published content more polished and need a paid fb.ai plan. Skip any channel you don't publish on — it falls back to Gemini + Pillow.

If yes, walk through the matching brand-setup sub-step (each = author in Claude Design → generate API Key at https://www.fivebucks.ai/dashboard/api-keys if not done yet → upload ZIP at https://www.fivebucks.ai/dashboard/social-posts/templates → verify via `fivebucks_list_templates`):
- Meta Carousel → `brand-setup` Step 4c-i
- Meta Story → `brand-setup` Step 4c-ii
- LinkedIn Post → `brand-setup` Step 4c-iii
- Meta Post → `brand-setup` Step 4c-iv

There is **no** local copy, version hash, or gateway-upload step to reconcile — templates live on fb.ai and are detected live. If `FIVEBUCKS_API_KEY` isn't set, skip this step (the brand uses the Gemini + Pillow fallback).

### 3d. Optional fb.ai media library (offer, don't force)

Check whether the brand has any media folders via `fivebucks_list_media_folders`. If the media library is empty and the user wants on-brand photos in generated posts, offer to set it up:

> The fb.ai media library is empty. Uploading brand photos lets skills pick on-brand visuals automatically. Want to add some now? You can always skip and upload later.

If yes:
> 1. Go to https://www.fivebucks.ai/dashboard/api-keys — generate API Key if not done yet *(skip if already generated)*
> 2. Go to https://www.fivebucks.ai/dashboard/social-posts/media
> 3. Create one folder per template type, named **exactly** as follows — `content-generator` matches photos to templates using these names:
>    - **LinkedIn Post** — photos for LinkedIn single-image posts
>    - **Meta Story** — photos for Instagram / Facebook Stories
>    - **Meta Carousel** — photos for Instagram / Facebook Carousels
>    - **Meta Post** — photos for Instagram / Facebook single-image posts
>
>    Only create folders for template types that exist on fb.ai. Then click **Upload Media** inside each folder to add your photos.

If the user skips, mark as ⏭ — skills fall back to Gemini image generation. If `FIVEBUCKS_API_KEY` isn't set, skip this step entirely.

### 3e. brand.md sections (only the missing ones)

For each missing section header in `brand.md`, append it without rewriting existing content:

- **Locale missing** — extract Currency / Timezone / Meta USD exchange rate from the website (re-use Step 4 logic). Append a `## Locale` section to `brand.md`.
- **Social Publishing missing** — re-run `brand-setup` Step 7b Step D (auto-discover Zernio profile + connected accounts via the Zernio MCP tools `profiles_list` + `accounts_list`). Append a `## Social Publishing` section.
- **Content Strategy missing** — run `brand-setup` Step 4a. Ask the user: (1) Primary channel: `youtube` or `static`? (2) If `youtube`: which platforms for distribution, which are currently connected, clips per video. Write the `## Content Strategy` section to `brand.md`. This section is read by `social-calendar` at runtime to select planning mode — without it, `social-calendar` defaults to static mode.

### 3f. Env vars (only the missing ones)

For each missing required env var, ask the user for the value and append/update `.claude/settings.local.json` under `env`. Preserve all existing keys — never overwrite the file wholesale.

For missing `{BRAND}_ZERNIO_FB/IG/LI/TT/TW`: re-run the Zernio MCP tools `profiles_list` + `accounts_list` to auto-discover. (`_TT` = TikTok, `_TW` = Twitter/X — organic publishing IDs needed by `video-repurposer` for YouTube-First clip publishing; skip any platform not connected to Zernio.)

**Legacy `${BRAND}_LATE_*` → `${BRAND}_ZERNIO_*` rename.** Brands set up before gateway v1.7.4 have their Zernio account IDs stored under the old `${BRAND}_LATE_*` prefix (and a now-defunct `LATE_API_KEY`). For every `${BRAND}_LATE_*` key in the `env` block (`_FB` / `_IG` / `_LI` / `_TT` / `_TW` / `_GOOGLE_ADS` / `_GOOGLE_ADS_CID` / `_META_ADS_ACCOUNT_ID` / `_LINKEDIN_ADS` / `_LINKEDIN_ADS_CID`), copy the value to the matching `${BRAND}_ZERNIO_*` key and delete the old key. Also delete `LATE_API_KEY` if present — Zernio is now an OAuth connector with no API key.

For missing `{BRAND}_NOTION_DB`: ask the user if they want to bootstrap now (calls `notion-create-database` per `social-calendar` Step 3a) or defer to first social-calendar run.

For missing `{BRAND}_ZERNIO_GOOGLE_ADS`, `{BRAND}_ZERNIO_GOOGLE_ADS_CID`, `{BRAND}_ZERNIO_META_ADS_ACCOUNT_ID`, `{BRAND}_ZERNIO_LINKEDIN_ADS`, or `{BRAND}_ZERNIO_LINKEDIN_ADS_CID`: auto-discover via the Zernio MCP. SocialAccount IDs need no user input; customer / sponsored-account IDs fall back to a prompt only when Zernio rate-limits or returns nothing.

```
Step 1 — Zernio SocialAccount IDs (no user input):
Use Zernio MCP tool `accounts_list`:
→ Find entry where platform is "googleads" or "google" → save _id as ${BRAND}_ZERNIO_GOOGLE_ADS
→ Find entry where platform is "metaads" or "facebook" → save _id as ${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID
→ Find entry where platform is "linkedinads" or "linkedin_ads" (NOT plain "linkedin", which is the
   organic LinkedIn page saved as ${BRAND}_ZERNIO_LI) → save _id as ${BRAND}_ZERNIO_LINKEDIN_ADS

Step 2 — Google Ads customer ID (only if ${BRAND}_ZERNIO_GOOGLE_ADS_CID is missing):
Use Zernio MCP tool `ads_list_ad_accounts`:
- account_id: ${BRAND}_ZERNIO_GOOGLE_ADS

2a. Accounts returned → take the customer ID (numeric) from the first entry and save as
    ${BRAND}_ZERNIO_GOOGLE_ADS_CID.
2b. Empty response OR 429 rate-limit → ask the user:
    > "What is your Google Ads customer ID? You can find it in the top-right corner
    > of your Google Ads account (format: XXX-XXX-XXXX)."
    Strip dashes before saving.

Step 3 — LinkedIn sponsored account ID (only if ${BRAND}_ZERNIO_LINKEDIN_ADS is set
        and ${BRAND}_ZERNIO_LINKEDIN_ADS_CID is missing):
Use Zernio MCP tool `ads_list_ad_accounts`:
- account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS

3a. Accounts returned → take the numeric sponsored account ID from the first entry and save as
    ${BRAND}_ZERNIO_LINKEDIN_ADS_CID.
3b. Empty response OR 429 rate-limit → ask the user:
    > "What is your LinkedIn sponsored account ID? Open Campaign Manager → look at the URL or
    > top-left account picker — it's a numeric ID (e.g. 517258773)."
    Save the digits only.

Step 4 — Legacy rename (handle before Step 1):
If ${BRAND}_ZERNIO_GOOGLE_ADS_ACCOUNT_ID or legacy ${BRAND}_LATE_GOOGLE_ADS exists but
${BRAND}_ZERNIO_GOOGLE_ADS does not, copy the value across, delete the old key, then run
Step 2 to populate _CID. (See also the blanket `${BRAND}_LATE_*` → `${BRAND}_ZERNIO_*`
rename above — apply that first.)
```

`${BRAND}_ZERNIO_GOOGLE_ADS`, `${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID`, and `${BRAND}_ZERNIO_LINKEDIN_ADS` are SocialAccount IDs (Zernio-side `_id`s); `${BRAND}_ZERNIO_GOOGLE_ADS_CID` and `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are the actual platform-side account IDs (Google Ads customer ID, LinkedIn sponsored account ID). Zernio's Google Ads and LinkedIn Ads tools require **both** the SocialAccount ID AND the platform-side ID — passing only the SocialAccount ID returns empty results. Only save the vars for platforms that are returned. If the Zernio connector is not authorized, skip silently and note: "Windsor.ai fallback ads account IDs not set — connect Zernio first." If LinkedIn Ads is not in `accounts_list`, skip Step 3 — most brands do not run LinkedIn Ads and the analyst skills tolerate the gap.

After updating `.claude/settings.local.json`, also store the remaining vaultable API keys (`GEMINI_API_KEY`, `FIVEBUCKS_API_KEY`) in the gateway vault via `fiveagents_store_credential` (mapping per `brand-setup` Step 7b vault table). Zernio (OAuth) and DataforSEO (own Basic-Auth connector) are **not** gateway-vaulted — no `fiveagents_store_credential` for them.

#### fb.ai key — check its scopes (new in v2.20.0)

fb.ai API keys are now **project-scoped with 10 capabilities**, and can carry an expiry. Existing keys generated before this change are **legacy keys with full access — they keep working, no action needed**. But it's worth confirming, because a key regenerated with boxes unticked will silently break skills.

If `FIVEBUCKS_API_KEY` is set, probe it:

```
Use gateway MCP tool fivebucks_whoami:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Read the response and report:

- **`scopes: []` (empty)** → a legacy full-access key. ✅ Everything works. No action.
- **`scopes` lists capabilities** → a scoped key. Check `social_posts` is present — without it, `content-generator`, `creative-designer`, `social-publisher`, `social-calendar` and the other fb.ai-dependent skills will fail with `auth/insufficient-scope`. If it's missing, tell the user to regenerate at https://www.fivebucks.ai/dashboard/api-keys with the box ticked, then re-store it via `fiveagents_store_credential` (service `fivebucks`).
- **`auth/key-expired` (401)** → the key expired. Regenerate and re-store.
- Also surface the returned `quota` snapshot so the user knows what they have left.

Mention what the key now unlocks beyond social templates — SEO research, article generation, publishing, site audits, traffic monitoring, and cold-email lead gen (100 tools). A brand that only ticked Social Posts is leaving the rest on the table.

For the auto-bootstrapped DB env vars (`${BRAND}_CRM_DB`, `${BRAND}_CUSTOMER_DB`, `${BRAND}_INVOICE_TRACKER_DB`, `${BRAND}_REPORTS_DB`, `${BRAND}_COMPETITOR_DB`, `${BRAND}_MEETINGS_DB`, `${BRAND}_ACTIONS_DB`, `${BRAND}_PERFORMANCE_DB`, `${BRAND}_TREND_DB`):

- If env var is missing → no action. The skill that depends on it will create the Notion DB on first run and persist the ID to `.claude/settings.local.json` (same pattern as `${BRAND}_NOTION_DB` for social-calendar).
- If env var is present but the Notion DB has been deleted → ask the user: "Re-bootstrap now or defer to first run?" Both paths work; bootstrap-now avoids a confusing error on next skill run.

Surface this informationally in the gap report — do not flag as a required gap.

### 3g. MCP connectors

**For every MCP flagged ❌ or ⏭ in Step 1e, walk the user through the specific connector flow below — do not just list them in the gap report and move on.** The user's brand-setup run is the only place these prompts appear in full; if plugin-update silently skips them, the user will end up with skills that error on first use because their MCP isn't connected.

Iterate through the missing MCPs in this order. For each one, post the prompt verbatim, wait for the user to confirm (or say "skip"), then re-probe. Mark complete only when the probe call succeeds.

**Connected Apps (OAuth via Settings → Connected Apps):**

- **Notion not connected** (required — content calendar, briefs, auto-bootstrapped DBs):
  > Notion isn't connected — used for the content calendar, strategy briefs, and the auto-bootstrapped CRM / customer / invoice / report / competitor / meeting / actions / performance / trend / gigs DBs. Go to **Settings → Connected Apps → Notion → Authorize**, then tell me when done.

- **Slack not connected** (required — skill-run notifications):
  > Slack isn't connected — used for "skill done" DMs after each run. Go to **Settings → Connected Apps → Slack → Authorize**, then tell me when done.

- **Gmail not connected** (required — email reading + report delivery):
  > Gmail isn't connected — used for reading inbound replies and delivering reports. Go to **Settings → Connected Apps → Gmail → Authorize**, then tell me when done.

- **Google Calendar not connected** (required — scheduling content drops & meetings):
  > Google Calendar isn't connected — used for scheduling content drops and meetings. Go to **Settings → Connected Apps → Google Calendar → Authorize**, then tell me when done.

- **Windsor.ai not connected** (mandatory — Google Ads + GA4 + Meta Ads): walk all 3 steps, do not collapse to one prompt:
  > Windsor.ai isn't connected — this is the universal source for Google Ads + GA4 + Meta Ads (Facebook + Instagram).
  > 1. If you don't have an account yet, sign up free at https://windsor.ai/register
  > 2. In your Windsor dashboard, connect **all three**: Google Ads, GA4, and Meta Ads (Facebook Ads). All three are required — Meta Ads in Windsor is mandatory regardless of whether the optional Meta Ads MCP is added.
  > 3. Then in Claude: **Settings → Connected Apps → Windsor.ai → Authorize**.
  > Tell me when done.

  After the user confirms, re-run `get_connectors` and verify the result includes Google Ads, GA4, **and** Facebook. If any of the three is missing, ask the user to connect the missing one in their Windsor dashboard before marking complete.

- **Canva not connected** (used by `campaign-presenter`):
  > Canva isn't connected — used for campaign decks and pitch presentations. Go to **Settings → Connected Apps → Canva → Authorize**, then tell me when done. (Skip if you don't deliver Canva decks — `campaign-presenter` will be unconfigurable for this brand.)

**Business-operations MCPs (added in v2.4.0):**

- **Apollo.io not connected** (used by `apollo-lead-prospector`, `outreach-sequencer`):
  > Apollo.io isn't connected — used for lead enrichment, contact search, and email-sequence injection. Go to **Settings → Connected Apps → Apollo.io → Authorize**, then tell me when done. (Skip if you don't run outbound — those two skills will be unconfigurable for this brand.)

- **Calendly not connected** (used by `customer-onboarder`, `meeting-analyzer`):
  > Calendly isn't connected — used for kickoff scheduling and meeting metadata pulls. Go to **Settings → Connected Apps → Calendly → Authorize**, then tell me when done. (Skip if you don't use Calendly — `customer-onboarder` falls back to manual scheduling and `meeting-analyzer` reads transcripts directly.)

- **Stripe not connected** (used by `invoice-collector`, `financial-reporter`):
  > Stripe isn't connected — used for invoice status and payment data. Go to **Settings → Connected Apps → Stripe → Authorize**, then complete the OAuth flow it gates the real tools behind. Tell me when both `authenticate` and `complete_authentication` have succeeded. (Skip if you bill outside Stripe — `invoice-collector` and `financial-reporter` will be unconfigurable for this brand.)

- **Xero not connected** (used by `invoice-collector` for invoice sync, `financial-reporter` for P&L):
  > Xero isn't connected — used for invoice status sync and pulling the P&L. Go to **Settings → Connected Apps → Xero → Authorize**, then tell me when done. (Skip if you don't use Xero — `financial-reporter` will fall back to Stripe-only data.)

- **PostHog not connected** (used by `churn-predictor` for product-usage signals):
  > PostHog isn't connected — used by `churn-predictor` for product-usage signals (login frequency, feature engagement). Go to **Settings → Connected Apps → PostHog → Authorize**, then tell me when done. (Skip if you don't use PostHog — `churn-predictor` falls back to support-ticket + login-frequency signals only.)

- **Gamma not connected** (used by `investor-update-writer` for investor decks):
  > Gamma isn't connected — used by `investor-update-writer` for monthly investor decks. Go to **Settings → Connected Apps → Gamma → Authorize**, then tell me when done. (Skip if you don't deliver investor updates — `investor-update-writer` will be unconfigurable for this brand.)

- **n8n Cloud not connected** *(optional — used by `n8n-workflow-builder` for inbound-gig proof workflows):*
  > n8n Cloud isn't connected — used by `n8n-workflow-builder` (the Prove phase of the Inbound Gig Engine) to build the proof-of-concept automation that backs a freelance bid. Go to **Settings → Connected Apps → n8n Cloud → Authorize**, then tell me when done. (Skip if you don't pursue marketplace work or don't demo automations — `n8n-workflow-builder` will be unconfigurable, but `gig-prospector` and `gig-proposal-writer` still run.) Optionally, to send these workflows to a specific n8n project, give me the project ID and I'll save it as `${BRAND}_N8N_PROJECT`; otherwise they go to your default project.

**Custom connectors (Settings → Connectors → Add custom connector):**

- **Zernio not connected / not authorized** (required — social publishing + ads account discovery; formerly gateway-routed as "Late", split to its own MCP in gateway v1.7.4):
  > Zernio (formerly Late) is now its own connector — it's used to publish social posts and to discover your ad-account IDs. Go to **Settings → Connectors → Add custom connector**, name `Zernio`, URL `https://mcp.zernio.com/mcp`, then sign in with your Zernio account (OAuth). Tell me when done. (If you set this brand up before this change, you can also delete the old `LATE_API_KEY` from `.claude/settings.local.json` after authorizing — Zernio no longer uses an API key.)

  After the user confirms, re-run the Step 1e probe (`profiles_list`); mark complete only when it succeeds. If a `LATE_API_KEY` still exists in the `env` block, delete it (Zernio is OAuth-only now).

- **DataforSEO not connected** *(optional — keyword research only; formerly gateway-routed, split to its own MCP in gateway v1.7.5):*
  > (Optional) DataforSEO is now its own connector — used only for keyword research (search volume, suggestions). If you do keyword research: **Settings → Connectors → Add custom connector**, name `DataforSEO`, URL `https://mcp.dataforseo.com/mcp`, then authenticate with **Basic Auth** using your `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` credentials. Skip if you don't do keyword research — nothing else depends on it. Tell me whether you added it or skipped. (No env rename needed — the login/password env vars are unchanged.)

- **Meta Ads MCP not connected** (optional enhancement — limited rollout):
  > (Optional) Meta has an official MCP server that gives skills slightly more direct Marketing API access than Windsor.ai. If you want to try it: **Settings → Connectors → Add custom connector**, name `Meta Ads`, URL `https://mcp.facebook.com/ads`, sign in with the Facebook/Meta Business account that owns the brand's ad accounts. If "Add custom connector" isn't visible or sign-in fails — no problem, your Windsor.ai connection already covers Meta Ads fully. Tell me whether you added it or skipped.

  - If the user added it successfully → save `META_ADS_SOURCE=meta_ads_mcp` to `.claude/settings.local.json` `env` block.
  - If the user skipped or couldn't add it → leave `META_ADS_SOURCE` unset. Downstream skills default to Windsor for Meta data. **Do not flag as a required gap** — this is purely an enhancement.

**CLI-installed MCPs:**

- **Playwright not connected** (required for website analysis in `brand-setup` Step 4):
  ```bash
  claude mcp add playwright -- npx @playwright/mcp@latest
  ```
  Then ask the user to restart Claude Code and confirm `/mcp` shows `playwright`.

After every walkthrough, re-run the corresponding probe from Step 1e and only mark the gap closed when the probe succeeds. If the user said "skip", record it as ⏭ in the final summary so they can revisit later.

### 3h. CLAUDE.md (re-run brand-setup Step 9)

**First — always re-embed the full `agents/link.md` body between the BEGIN/END markers, regardless of any other CLAUDE.md gaps. Refreshing the stamp comment alone is wrong — after a `git pull` that adds new skills (e.g. v2.4.0's 10 business-ops skills), the stamp will read "v2.4.0" while the embedded body still describes v2.3.x as a "marketing agent" with no Apollo / Stripe / Xero / etc. mentions. Always replace the body too.**

```python
import glob, os, re, datetime

# Locate agents/link.md (same search order as brand-setup Step 9a)
config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
patterns = []
if config_dir:
    patterns.append(os.path.join(config_dir, "**/agents/link.md"))
patterns.extend([
    os.path.expanduser("~/.claude/**/agents/link.md"),
    os.path.expandvars(r"%APPDATA%\Claude\**\agents\link.md"),
    os.path.expanduser("~/Library/Application Support/Claude/**/agents/link.md"),
])
found = [f for p in patterns for f in glob.glob(p, recursive=True)]
link_md_path = os.path.abspath(os.path.realpath(found[0])) if found else None
if not link_md_path:
    raise RuntimeError("Could not locate agents/link.md — ask user for the full path.")

# Read current link.md from disk + strip YAML frontmatter (same as brand-setup Step 9a)
link_md_content = open(link_md_path, encoding='utf-8').read()
link_md_body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', link_md_content, count=1, flags=re.DOTALL).lstrip()

# Extract version from the Maintenance table
version_match = re.search(r'\|\s*Link\s*\|\s*(v[\S]+)\s*\|\s*([^|\n]+)\s*\|', link_md_content)
link_version = version_match.group(1).strip() if version_match else "unknown"
link_version_date = version_match.group(2).strip() if version_match else "unknown"
embed_date = datetime.date.today().isoformat()

# Build the full replacement block (stamp + body), wrapped in the existing BEGIN/END markers
new_block = (
    f"<!-- BEGIN agents/link.md (embedded by brand-setup) -->\n"
    f"<!-- link.md version: {link_version} | Last Changed: {link_version_date} | Embedded: {embed_date} -->\n"
    f"\n"
    f"{link_md_body}\n"
    f"\n"
    f"<!-- END agents/link.md -->"
)

# Replace EVERYTHING between (and including) the markers — body and stamp together
claude_md = open("CLAUDE.md", encoding='utf-8').read()
if "<!-- BEGIN agents/link.md (embedded by brand-setup) -->" in claude_md and "<!-- END agents/link.md -->" in claude_md:
    claude_md_new = re.sub(
        r'<!-- BEGIN agents/link\.md \(embedded by brand-setup\) -->.*?<!-- END agents/link\.md -->',
        lambda m: new_block,  # lambda avoids re.sub's backslash interpretation in link_md_body
        claude_md,
        count=1,
        flags=re.DOTALL,
    )
else:
    # Markers absent — fall through to the "Missing entirely" branch below; do not partial-write here.
    claude_md_new = claude_md

if claude_md_new != claude_md:
    # Show the diff to the user before writing (per the rule at the bottom of this step)
    open("CLAUDE.md", "w", encoding='utf-8').write(claude_md_new)
```

This runs unconditionally every time plugin-update executes — it is the equivalent of what brand-setup Step 9b does on first install. After a `git pull`, both the version stamp **and** the embedded `link.md` body are refreshed, so CLAUDE.md always reflects the currently installed version's full content (skills table, MCP list, context-file rows, etc.).

**Verification after re-embed** — confirm the stamp matches `agents/link.md`'s current Maintenance version AND that a string unique to the new version appears in the embedded body. Example: after upgrading to v2.4.0, grep CLAUDE.md for `apollo-lead-prospector` (one of the 10 new skills); if absent, the body did not get re-embedded and you should retry the regex with the full text re-read.

**Then patch any remaining CLAUDE.md gaps** — only the affected lines:

- **Missing entirely** → create from scratch (full brand-setup Step 9 flow, including version stamp).
- **Relative path** → resolve absolute path (Step 9a) and replace the line in place. Validate `os.path.isabs` before writing. Do not rewrite the rest of the file.
- **Missing Credential Loading block** → append it under the existing Agent Identity block.
- **Active Brand mismatch** → update the brand line; if multi-brand, append rather than replace.

Show a unified diff to the user before writing any changes to CLAUDE.md.

**Finally — refresh the `## Visual System` block in `CLAUDE.md` (equivalent of brand-setup Step 9c).** This runs unconditionally every time plugin-update executes — it brings stale or missing Visual System blocks up to date (e.g. brands set up before Step 9c was introduced, or before the media library row was added in v2.8.0).

Detection (best-effort — skip any call that requires `FIVEBUCKS_API_KEY` when the key is unset):

```python
from pathlib import Path

brand_root = Path("brands") / brand  # `brand` is the active brand slug

def folder_status(name):
    p = brand_root / name
    return "installed" if (p.is_dir() and any(p.iterdir())) else "not installed"

design_system_status = folder_status("design-system")   # local — the crucial baseline

# Optional fb.ai mirror — call fivebucks_get_brand_kit (skip if FIVEBUCKS_API_KEY unset).
# design_system_fbai = "uploaded" if result is non-null, else "not uploaded"

# Social templates — call fivebucks_list_templates; collect each returned `type` (skip if no key).
fb_template_types = []   # e.g. ["meta-carousel", "linkedin-post"], or [] if none / no fb.ai key

# Media library — call fivebucks_list_media_folders (skip if no key).
# media_status = "installed" if any folders exist, else "not installed"
```

Build the block using the same template as brand-setup Step 9c (substituting `{design_system_status}`, `{design_system_fbai}`, `{fb_template_types}`, `{media_status}`), then inject idempotently:
- If `CLAUDE.md` already contains `<!-- BEGIN visual-system (managed by brand-setup Step 9c) -->` and `<!-- END visual-system (managed by brand-setup Step 9c) -->` markers, replace everything between (and including) those markers with the freshly built block.
- Otherwise, append the new block to the end of `CLAUDE.md` preceded by a blank line.

Show the user a concise status line:
> ✅ `CLAUDE.md` Visual System section refreshed:
> - design-system (local): **{design_system_status}** · fb.ai mirror: **{design_system_fbai}**
> - fb.ai social templates: {fb_template_types or "none"}
> - media library: **{media_status}**

### 3i. Settings (manual)

For UI-only settings, show a checklist and ask the user to confirm each one:

> Please confirm in Claude settings:
> - [ ] Settings → Claude Code → Allow bypass permissions mode = ON
> - [ ] Settings → Capabilities → Domain Allowlist = All Domains
> - [ ] Project → Permission = Act without asking
> Reply "all set" when done.

### 3j. Funnel TBD events

If `funnel.md` had `TBD` entries in Step 1c and Windsor.ai is now connected, re-run the GA4 event-discovery flow from `brand-setup` Step 8 #16 and patch in the confirmed event names.

### 3k. Version-specific brand actions

For each skill/agent flagged as changed in Step 1k, read its `### Change Log` bullets and map them to required brand configuration actions. Use this decision table:

| Changelog entry | Brand action required |
|---|---|
| Direction column added (content-generator / social-calendar v2.2.15) | ✅ Check Notion Social Calendar DB has a `Direction` select column at position 10; add it if missing |
| Social templates migrated to fb.ai — `fivebucks_*` tools (v2.7.0) | ✅ Run Step 1h (`fivebucks_list_templates`) to see which `type`s exist on fb.ai; offer missing ones via Step 3c. The old local `social-meta-*-template/` folders, `template_upload`/`template_list`, and version hashes no longer apply. |
| design-system/ MANDATORY → OPTIONAL (brand-setup v2.2.15) | ❌ No action — constraint relaxed |
| _copy.json output added (content-generator / content-creation v2.2.15) | ❌ No action — additive output format |
| Naming convention split: social vs non-social (content-creation v2.2.15) | ❌ No action — future outputs only |
| Meta Ads framing reversed — Windsor.ai MANDATORY (brand-setup v2.2.13) | ✅ Confirm Windsor.ai has Meta Ads (Facebook) connected; if not → Step 3f |
| DEFAULT_BRAND + {BRAND}_NOTION_DB env vars (brand-setup v2.2.12) | ✅ Check env block for both; add if missing |
| CLAUDE.md embeds agents/link.md (brand-setup v2.2.11) | ✅ Check CLAUDE.md for embedded link.md content (BEGIN/END markers); if absent → Step 3h |
| date_preset → last_30dT (digital-marketing-analyst v2.2.8) | ❌ No action — runtime parameter, no brand config |
| `apollo-lead-prospector introduced (link-skills v2.4.0)` | ✅ Check `brands/{brand}/sales.md` exists. If not → run brand-setup Step 5g sales sub-step |
| `outreach-sequencer introduced (link-skills v2.4.0)` | ✅ Same as apollo-lead-prospector — sales.md must exist |
| `proposal-generator introduced (link-skills v2.4.0)` | ✅ Same as apollo-lead-prospector — sales.md must exist |
| `customer-onboarder introduced (link-skills v2.4.0)` | ✅ Check `brands/{brand}/customer-success.md` exists. If not → run brand-setup Step 5h |
| `churn-predictor introduced (link-skills v2.4.0)` | ✅ Same as customer-onboarder — customer-success.md must exist |
| `invoice-collector introduced (link-skills v2.4.0)` | ✅ Check `brands/{brand}/finance.md` exists. If not → run brand-setup Step 5i |
| `financial-reporter introduced (link-skills v2.4.0)` | ✅ Same as invoice-collector — finance.md must exist |
| `investor-update-writer introduced (link-skills v2.4.0)` | ✅ Check `brands/{brand}/investors.md` exists. If not → ask if brand has raised external capital; if yes → run brand-setup Step 5j |
| `competitor-monitor introduced (link-skills v2.4.0)` | ✅ Check `brands/{brand}/competitors.md` has the new `monitor_urls`/`track_pages`/`exec_team` fields per competitor. If not → run brand-setup Step 5l (extension) |
| `meeting-analyzer introduced (link-skills v2.4.0)` | ⏭ Optional — ask user if they want operations.md set up. If yes → brand-setup Step 5k |
| `digital-marketing-analyst v2.3.0 / data-analysis v2.3.0 — Windsor.ai fallback via Zernio (v2.5.0–v2.5.1)` | ✅ Check `${BRAND}_ZERNIO_GOOGLE_ADS` (Zernio SocialAccount `_id`) + `${BRAND}_ZERNIO_GOOGLE_ADS_CID` (Google Ads customer ID) + `${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID` + `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` in env. Both Google vars and both LinkedIn vars are required pairs for Zernio ads calls. LinkedIn vars are optional — skip if the brand doesn't run LinkedIn Ads. If missing → run Step 3f auto-discover (also handles the legacy `${BRAND}_LATE_*` → `${BRAND}_ZERNIO_*` rename, including `${BRAND}_ZERNIO_GOOGLE_ADS_ACCOUNT_ID`/legacy `${BRAND}_LATE_GOOGLE_ADS` → `${BRAND}_ZERNIO_GOOGLE_ADS`) |
| `social-calendar YouTube-First Mode added (v2.14.0)` | ✅ Check `brands/{brand}/brand.md` has `## Content Strategy` section. If missing → run brand-setup Step 4a to define primary channel. Without it, social-calendar defaults to static mode regardless of the brand's actual publishing workflow. |
| `trend-radar synthesis requirement added (v2.14.0)` | ✅ No brand file action required — the skill now synthesizes competitor research + web research before writing to Trend DB. Existing `competitors.md` already serves as the competitor input. |
| `gig-prospector introduced (link-skills v2.16.0)` | ⏭ Optional — ask if the brand pursues freelance/marketplace work. If yes → check `brands/{brand}/sales.md` has a `## Inbound Job Filters` section; if missing → run `brand-setup` Step 5g Step H (markets, platforms + account status, product.md-derived keywords, budget/exclusions/cap). `${BRAND}_GIGS_DB` auto-bootstraps on first run; `FREELANCER_OAUTH_TOKEN` is an optional env var that enables the Freelancer.com API source. No existing skill breaks if skipped. |
| `Inbound Gig Engine completed (link-skills v2.17.0)` | ⏭ Optional — only for brands pursuing marketplace work (those with `## Inbound Job Filters`). `gig-proposal-writer` and `vsl-demo-producer` need no new connector (Notion + Slack + Claude in Chrome, already covered). `n8n-workflow-builder` needs the **n8n Cloud** MCP — if the brand wants to demo automations, run the Step 3g n8n Cloud walkthrough; optionally set `${BRAND}_N8N_PROJECT`. No env var auto-bootstraps beyond `${BRAND}_GIGS_DB` (already created by `gig-prospector`). No existing skill breaks if skipped. |
| Zernio + DataforSEO split off the gateway; Argil retired (link-skills v2.18.0) | ✅ **Zernio (required):** reconnect as its own MCP — Settings → Connectors → Add custom connector → `https://mcp.zernio.com/mcp` → sign in with your Zernio account (OAuth). Then rename existing `${BRAND}_LATE_*` env vars → `${BRAND}_ZERNIO_*` (Step 3f) and delete the now-unused `LATE_API_KEY`. Re-run account discovery (`profiles_list` / `accounts_list`) — Zernio's own API may return different SocialAccount `_id`s than the old gateway-proxied Late API, so don't assume they carry over. **DataforSEO (optional):** if the brand uses keyword research, reconnect as its own MCP — Add custom connector → `https://mcp.dataforseo.com/mcp` → Basic Auth with `DATAFORSEO_LOGIN`/`DATAFORSEO_PASSWORD` (no env rename needed). **Gemini image model:** no brand action — runtime default changed to `gemini-3.1-flash-image`, no env/file impact. Argil (avatar video) retired with no replacement — no action. |

For changelog entries not in this table, apply judgment: if the change touches a per-brand configuration file (`brand.md`, `funnel.md`, `.claude/settings.local.json`, `CLAUDE.md`) → flag for review. If it is a skill-internal logic change → no brand action needed.

Show the user only the rows where brand action is required:

```
Version-specific actions ({N} required)
  ✅ Direction column — checking Notion DB...
  ✅ Template upload check — reading brand.md Social Templates...
  ✅ Windsor.ai Meta Ads — re-probing connector...
```

---

## Step 4 — Re-validate

After you've filled the selected gaps, the agent runs a **focused validation pass** — only re-testing the integrations that were touched in Step 3 (not re-running the full Step 1 inspection). The output is a summary table of what was fixed, what was skipped, and what passed validation. If any fix failed validation (e.g. you re-authorized Windsor.ai but the probe still 401s), the agent flags it for retry.

**Expect 1–2 minutes.** No questions unless a validation fails.

After all selected gaps are filled, run a focused validation pass — only test integrations that were touched in Step 3. Reuse the test calls from `brand-setup` Step 8.

### 4a. Show what was fixed

| Gap | Action taken | Status |
|---|---|---|
| design-system/ missing | Installed via Claude Design | ✅ |
| Locale section in brand.md | Extracted from site, appended | ✅ |
| Zernio connector not authorized | User authorized OAuth connector (no key saved/vaulted) | ✅ |
| Windsor.ai not connected | User authorized, probe passed | ✅ |
| CLAUDE.md link.md path relative | Replaced with absolute path | ✅ |
| meta-carousel template (fb.ai) | User chose to skip | ⏭ |
| ... | ... | ... |

This is the **diagnostic** view — useful for "what changed?" but not what the user actually wants to know.

### 4b. Agent Readiness Summary (business-friendly)

The "what was fixed" table answers a technical question. The owner wants the business answer: *which agents will run on my brand starting today, which still need a fix, and which did I skip?* Step 4b produces that answer.

**Build the readiness matrix using the exact spec in `brand-setup` Step 8d** (translation table, status rules, display format, JSON schema, and the 8d-iv rule for deriving `connected_tools[]` from the generated `skills-manifest.json`). The only difference is where the inputs come from:

| Input | brand-setup Step 8d source | plugin-update Step 4b source |
|---|---|---|
| MCP connection state | Step 8a–8c-bis probe results | Step 1e probe results, **updated** by any Step 3f re-probes |
| Brand context file presence | Step 5/6 generation outcomes | Step 1a inspection, **updated** by any Step 3a fills |
| Env vars / Notion DBs | Step 7b save + Step 8d validation | Step 1d inspection, **updated** by any Step 3e fills |

In other words: take the Step 1 audit, overlay every successful fix from Step 3, and compute the matrix from the post-fix state. Skills the user explicitly skipped during Step 3 (e.g. "skip Apollo, I don't run outbound") map to ⏭ in the matrix; skills that had a missing dep neither fixed nor skipped map to ❌.

Print the matrix to chat in the same exact format documented in `brand-setup` Step 8d-iii. Save the structured `agent_readiness[]` + `readiness_summary` object — Step 5b reads it directly into the email payload.

**Do not proceed to Step 5 until the readiness matrix has been printed to chat and saved.**

---

## Step 5 — Record version + completion email + Slack

Final step — wrap up. The agent writes the **current plugin version** into `brands/{brand}/brand.md` `## Plugin Version` section so future `plugin-update` runs know where to start their delta from. It then sends a completion email and Slack DM summarizing what was fixed, what was skipped, and any gaps that remain. After this step, the brand is fully caught up to the current plugin version.

**Expect 30 seconds.** No questions.

### 5a. Write plugin version to brand.md

Append or update the `## Plugin Version` section in `brands/{brand}/brand.md`:

```markdown
## Plugin Version
Last applied: {DEFAULT_VERSION} — {today's date}
```

If the section already exists, replace the `Last applied:` line in place — do not rewrite anything else. This is the anchor that future `plugin-update` runs use in Step 0b to determine the delta.

### 5b. Send completion email and Slack DM

Send completion email and Slack DM. Reuse the `brand-setup.ts` server-side template via `tag: "brand-setup"` — the same template handles upgrades.

```
Use gateway MCP tool `fiveagents_send_email`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- to: ${REPORT_EMAIL}
- subject: "🔧 Plugin update complete — {brand}"
- html_body: JSON.stringify(payload)
- tag: "brand-setup"
```

JSON payload mirrors the `brand-setup` Step 10 schema:
- **`agent_readiness[]` + `readiness_summary`** — primary block; reuse the structured object saved in Step 4b verbatim. Same schema as brand-setup. The server-side template renders this as the headline section.
- **`files[]` and `connections[]`** — secondary diagnostic blocks; only contain items that were touched in Step 3 (not the full inventory).
- Add a top-level `mode: "update"` field so the template (or downstream telemetry) can distinguish a fresh setup from an upgrade.
- Add a top-level `brand_name` field — the properly cased brand display name (e.g. `"Five Agents"`), NOT the slug. Read it from the first `# ` heading in `brands/{brand}/brand.md` before building the payload (same approach as brand-setup Step 10):

  ```python
  import re
  brand_md = open(f"brands/{brand}/brand.md", encoding="utf-8").read()
  m = re.search(r'^#\s+(.+?)\s*$', brand_md, re.MULTILINE)
  brand_name = m.group(1).strip() if m else brand
  ```

  The template renders `brand_name` in the email title; `brand` (the slug) stays as a separate field for filesystem references.

Slack DM (lead with readiness, integration deltas as secondary diagnostic):
```
🔧 [{brand}] Plugin update applied

Agent Readiness (20 total):
  ✅ {N_ready} ready · ⚠️ {N_degraded} works with limitations · ❌ {N_not_ready} need fixing · ⏭ {N_skipped} skipped

{If N_not_ready > 0:}
Top fixes to unlock more agents:
  • {Agent name 1} — {one-line fix from agent_readiness[].fix}
  • {Agent name 2} — {one-line fix}
  (full list in the email)

This update: {N} gaps fixed · {M} skipped
Detail in email
```

Cap the "top fixes" list at 3. If `N_not_ready == 0`, omit the Top fixes block; lead with "🎉 Every connected agent is configured and ready to run."

---

## Quality Checklist

- [ ] Step 0 read `version.ts` DEFAULT_VERSION and brand.md `## Plugin Version` before doing anything
- [ ] Step 0 read every skill/agent maintenance section and built the version delta table
- [ ] Step 1 ran a full inspection without prompting the user
- [ ] Step 1a checked all 5 new brand-context files (sales.md, customer-success.md, finance.md, investors.md, operations.md) with optional annotations applied to investors.md and operations.md
- [ ] Step 1d checked the 10 auto-bootstrapped DB env vars (incl. v2.13.0 `${BRAND}_PERFORMANCE_DB`, `${BRAND}_TREND_DB` and v2.16.0 `${BRAND}_GIGS_DB`) without flagging missing ones as required gaps
- [ ] Step 1a inline schema check for sales.md `## Inbound Job Filters` ran; missing section offered as an optional Step 3a backfill (gig-prospector) — not flagged as a required gap
- [ ] Step 1e probed all v2.4.0 / v2.2.13 / v2.17.0 / v2.18.0 MCP rows (Apollo.io, Calendly, Stripe, Xero, PostHog, Gamma, optional n8n Cloud, optional Meta Ads MCP, Zernio, optional DataforSEO)
- [ ] Step 3f walked the user through any ❌ or missing env vars, renamed any legacy `{BRAND}_LATE_*` → `{BRAND}_ZERNIO_*` (and deleted `LATE_API_KEY`), and ran auto-discover for `{BRAND}_ZERNIO_*` vars where applicable
- [ ] Step 3g walked the user through every ❌/⏭ MCP with the explicit per-MCP prompt — never silently skipped a missing connector
- [ ] Step 1i probed `fivebucks_list_media_folders` (when `FIVEBUCKS_API_KEY` set) and recorded media library state
- [ ] Step 1k produced a version table showing which skills/agents changed since `last_applied`
- [ ] Step 2 gap report opened with the version delta block (updated skills listed with changelog summaries)
- [ ] Step 3 only walked through items marked ❌ or offered ⏭ — never re-asked for known-good state
- [ ] Step 3a fill handlers ran the matching brand-setup Step 5g–5l sub-step for any missing brand context file
- [ ] Step 3k mapped changelog entries to brand actions and only surfaced rows requiring action
- [ ] Step 3k changelog → brand-action mapping covered all changelog→action rows
- [ ] All file writes were patches (preserve existing content), not full rewrites
- [ ] Step 3h refreshed the `<!-- link.md version: ... -->` stamp in CLAUDE.md unconditionally
- [ ] Step 3h refreshed the `## Visual System` block in CLAUDE.md (brand-setup Step 9c equivalent) — probed design-system/, fivebucks_get_brand_kit, fivebucks_list_templates, fivebucks_list_media_folders and injected/replaced the markers
- [ ] CLAUDE.md `link.md` path is absolute (`os.path.isabs == True`) after the run
- [ ] `.claude/settings.local.json` retained all pre-existing keys
- [ ] Re-validation in Step 4 only tested touched integrations
- [ ] Idempotent — a second immediate run produces zero gaps and `last_applied == DEFAULT_VERSION`
- [ ] `fivebucks_list_templates` called in Step 1h (when `FIVEBUCKS_API_KEY` set) to detect which template types exist on fb.ai
- [ ] Missing template types offered via Step 3c (author in Claude Design → fb.ai dashboard upload); skips accepted
- [ ] Step 5a wrote `## Plugin Version` to brand.md with the current DEFAULT_VERSION
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "plugin-update"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars — e.g. 'Filled 5 gaps; design-system installed; Windsor.ai connected'>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "plugin_version": "<from versions/version.ts DEFAULT_VERSION>",
    "gaps_detected": 0,
    "gaps_fixed": 0,
    "gaps_skipped": 0,
    "fixes": [
      { "category": "files", "item": "design-system/", "action": "installed", "status": "ok" },
      { "category": "mcp", "item": "Zernio", "action": "authorized", "status": "ok" },
      { "category": "mcp", "item": "Windsor.ai", "action": "user_connected", "status": "ok" },
      { "category": "claude_md", "item": "link.md path", "action": "replaced_with_absolute", "status": "ok" }
    ]
  }
```

**Status values:** `success` (all required gaps fixed), `partial` (some required gaps still missing — user skipped), `failed` (skill errored).
