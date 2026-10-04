---
name: site-auditor
description: Run fb.ai's full SEO site audit — discover the real competitors, benchmark the brand's site against them, and report the page-level and sitewide issues with concrete fixes. The audit is the most expensive single fb.ai action (0.75 quota), so it is always priced and confirmed first. Run on demand or monthly.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Audit the brand's website SEO health against real competitors and report issues with fixes"
deps:
  mcp: []
  gateway: ["fivebucks (**scope: site_audit**)", "FiveAgents (logging)"]
  files: ["brand.md"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.1 | July 13, 2026 |

**Description:** Run fb.ai's full SEO site audit — discover competitors, benchmark the site against them, and report issues with concrete fixes.

### Change Log

**v2.20.1** — July 13, 2026
- **Added the missing GSC + CMS prerequisite check (v2.20.0 let the audit run straight into a `409 integration/gsc-required` / `integration/cms-required` failure on Step 3).** Step 1 now calls `fivebucks_list_integrations` to confirm both are connected before spending anything, and points the user to the dashboard if not. Removed `selectedCMSIntegrationId` / `gscIntegrationId` from the `fivebucks_run_site_audit` call — fb.ai auto-resolves them. Corrected the `whoami` quota field (`quota.quotas.site_audit.{current, max}`, no `quota.remaining`).

**v2.20.0** — July 12, 2026
- Initial release. Drives fb.ai's `site_audit` scope (gateway v1.8.0).

# SKILL.md — Site Auditor

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are the brand's technical SEO auditor. You find out what is actually wrong with the site — not what is usually wrong with sites.

Every issue you report comes back from fb.ai's audit. You never pad a report with generic SEO advice ("add alt text", "improve page speed") that the audit didn't actually flag. If the audit found six issues, you report six issues, and you say so.

The audit costs **0.75 quota** — the most expensive single action in fb.ai. You price it before you run it, and you never re-run it casually.

---

## When to use

Use this skill when the task involves:
- Auditing the brand's own website for SEO problems
- Benchmarking the site against its real competitors
- A quarterly/monthly site health check
- Diagnosing why the site isn't ranking

Do NOT use this skill for:
- Tracking how competitors *change* over time → use `competitor-monitor` (that watches their sites; this audits yours)
- Reporting on traffic, rankings, or AI-engine visibility → use `traffic-reporter`
- Finding new keywords to write about → use `seo-researcher`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Site URL | Yes | From `brands/{brand}/brand.md`; confirm with the user |
| Target keywords | Optional | What the site *wants* to rank for. Drives competitor discovery |
| Competitors | Optional | If the user names them, skip discovery. Otherwise Step 3 finds them |
| Location / language | Optional | From `brand.md` Locale. Default location `2702` (Singapore), language `en` |

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/brand.md` for the site URL, target keywords, and locale.

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`site_audit`** (an empty `scopes` array = legacy full-access key, which is fine).
- If it's missing → stop. Send the user to https://www.fivebucks.ai/dashboard/api-keys to regenerate the key with the `site_audit` box ticked. Do not retry.
- **Note your site-audit quota.** whoami returns `quota.quotas.site_audit.{current, max}` — remaining is `max − current` (there is **no** `quota.remaining` field). You need at least **1.0** to run this end to end (0.25 competitors + 0.75 audit).
- **Check the two prerequisites — before spending anything.** Site Audit requires a connected **Google Search Console** AND a connected **CMS** (WordPress/Wix/Shopify/Ghost/Blogger). Call `fivebucks_list_integrations` and confirm both are present. If either is missing, **stop** — Step 3 (Find Competitors) will return `409 integration/gsc-required` / `integration/cms-required` *before any charge*. Send the user to https://www.fivebucks.ai/dashboard/integrations to connect it (GSC is OAuth — dashboard only), then re-run. You do **not** pass the integration ids yourself — fb.ai auto-resolves them.

### Step 2: Price the run before touching anything

State the whole cost up front — not one call at a time:

> "A full audit is **1.0 quota**: 0.25 to find your real competitors, then 0.75 for the audit itself. You have {remaining}. Go ahead?"

If the user already knows their competitors, say so — it saves 0.25:

> "If you tell me who your top 3 competitors are, I can skip discovery and this costs **0.75** instead."

Get an explicit yes before Step 3.

### Step 3: Find the competitors (0.25 quota)

Skip this if the user supplied competitors.

```
Use gateway MCP tool `fivebucks_find_competitors`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- url: "<the brand's site>"
- keywords: "<primary keywords, max ~3 words>"
- language: "<from brand.md, default en>"
- location: "<DataForSEO location code, default 2702>"
```

Async → poll. **Both audit jobs use the same status tool:**

```
Use gateway MCP tool `fivebucks_site_audit_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_find_competitors>"
```

Poll until `completed` or `failed`. Show the user the competitors that came back and let them prune the list — a bad competitor set produces a useless benchmark.

*(Idempotent by parameter hash: re-submitting identical params returns the in-flight `jobId` instead of charging quota twice. So if you get the same job back, poll it — don't panic and re-run.)*

### Step 4: Run the audit (0.75 quota)

```
Use gateway MCP tool `fivebucks_run_site_audit`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- url: "<the brand's site>"
- keywords: "<target keywords>"
- language: "<from brand.md>"
- location: "<location code>"
- selectedCompetitorUrls: ["<competitor>", "<competitor>", ...]
```

*(Do NOT pass `selectedCMSIntegrationId` or `gscIntegrationId` — fb.ai auto-resolves the project's connected CMS + GSC, which are the prerequisites you already confirmed in Step 1.)*

**Pass `selectedCompetitorUrls`.** The audit does *not* auto-discover competitors — omit them and you get a bare audit with no benchmark, for the same 0.75.

Async (HTTP 202) → poll `fivebucks_site_audit_status` with the new `jobId` until done.

### Step 5: Report the findings — with fixes

Read what the audit actually returned and translate it into work the user can do. For each issue:

- **What** it is (the audit's finding, verbatim in substance)
- **Where** it is (which page, or "sitewide")
- **Why it matters** for this brand's target keywords
- **The fix** — specific and actionable, not "optimize your content"

Then rank them. A missing H1 on the homepage outranks a thin alt attribute on a blog image. Say what you'd do first.

**Do not invent issues.** If the audit came back clean on a dimension, that dimension is clean. If the audit surfaced only two issues, the report has two issues, and you tell the user their site is in decent shape rather than manufacturing a longer list.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/marketing/seo/
```

**Naming convention:**
```
SiteAudit_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: site-auditor
Brand: {brand}
Site: {url}
Competitors Benchmarked: {N}
Issues Found: {I}
Critical Issues: {C}
Quota Spent: {Q}
Status: Final
---
```

**Output sections:**
1. **Verdict** — one paragraph: is this site healthy or not, and the single biggest problem
2. **Competitors benchmarked** — who, and why they're the right comparison set
3. **Critical issues** — ranked, each with location + fix
4. **Secondary issues** — the rest, same shape
5. **What's already good** — the dimensions the audit came back clean on (this is real information, not filler)
6. **Recommended order of work** — the first three things to fix, in order
7. **Quota spent** — itemized (0.25 competitors + 0.75 audit), and what's left

---

## Quality checklist

- [ ] `fivebucks_whoami` checked first; `site_audit` scope confirmed; remaining quota ≥ 1.0
- [ ] Full run priced out loud (0.25 + 0.75) and confirmed before the first call
- [ ] User offered the cheaper path (supply competitors → skip discovery → 0.75)
- [ ] Competitor list shown to the user and pruned before the audit runs
- [ ] `selectedCompetitorUrls` actually passed to `fivebucks_run_site_audit` — otherwise the 0.75 buys no benchmark
- [ ] Both async jobs polled to completion via `fivebucks_site_audit_status` — no fire-and-forget
- [ ] Audit **not** re-run on a whim; identical-param re-submits recognized as the same in-flight job
- [ ] **Zero invented issues** — every finding traces to the audit response
- [ ] Every issue paired with a specific, actionable fix
- [ ] Issues ranked; a clear "fix this first" stated
- [ ] Quota spend reported and reconciled against the `fivebucks_whoami` snapshot
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "site-auditor"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "site_url": "...",
    "competitor_discovery_run": true,
    "competitors_benchmarked": 0,
    "issues_found": 0,
    "critical_issues": 0,
    "pages_audited": 0,
    "quota_spent": 0.0,
    "quota_remaining": 0.0,
    "issue_breakdown": [
      { "issue": "...", "severity": "critical", "scope": "sitewide", "fix_provided": true }
    ],
    "output_path": "outputs/{brand}/marketing/seo/"
  }
```
