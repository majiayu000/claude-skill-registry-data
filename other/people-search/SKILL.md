---
name: people-search
metadata:
  version: 2.5.0
  tags: [people-search, b2b, enrichment, kol, recruiting, web-research]
description: >
  Search, qualify, and enrich people and companies. Use this skill whenever the
  user wants to find professionals, candidates, or KOLs by title, company,
  location, seniority, or audience; enrich known contacts with email, phone, or
  LinkedIn; research companies for industry, funding, tech stack, or hiring
  activity; look up someone's contact info; source candidates for recruiting;
  generate B2B lead lists; or perform background web research on people or
  organizations. Trigger this skill even when the user doesn't explicitly say
  "search" or "enrich" — any mention of finding contacts, sourcing, prospecting,
  looking up a person or company, or gathering business intelligence should
  activate it.
---

# Lessie — People Search & Enrichment

## Setup

Lessie supports two modes: **CLI** (default, recommended) and **MCP Server**.

### Mode A: CLI (default)

Install the Lessie CLI binary:

```bash
npm install -g @lessie/cli
```

Or use without installing:

```bash
npx @lessie/cli --version
```

First-time authorization:

```bash
lessie auth
```

This opens a browser for login/registration. Token is cached at `~/.lessie/oauth.json`.

Verify connection:

```bash
lessie status
```

### Mode B: MCP Server

Add to your MCP config (Claude Code `~/.claude.json`, Cursor `~/.cursor/mcp.json`, Codex `~/.codex/config.toml`, etc.):

```json
{
  "mcpServers": {
    "lessie": {
      "command": "npx",
      "args": ["-y", "@lessie/mcp-server"],
      "env": {
        "LESSIE_REMOTE_MCP_URL": "https://app.lessie.ai/mcp-server/mcp"
      }
    }
  }
}
```

### Uninstall

- **CLI:** `npm uninstall -g @lessie/cli && rm -rf ~/.lessie/`
- **MCP:** Remove the `"lessie"` entry from your `.json` and `rm -rf ~/.lessie/`

## Version check

Run these checks once at the start of each session, before mode detection. Both checks are non-blocking — if any command fails (network error, timeout), skip silently and proceed.

### Skill version

1. Read current local version from this file's metadata `version` field above.
2. Fetch remote version:
   ```bash
   curl -sf --max-time 5 https://raw.githubusercontent.com/LessieAI/lessie-skill/main/people-search/SKILL.md | head -5 | grep 'version:' | head -1 | awk '{print $2}'
   ```
3. If the remote version is newer than the local version → tell the user:
   > ⬆️ A newer version of people-search skill is available ({local} → {remote}). Run this command to update:
   > ```
   > npx skills add LessieAI/lessie-skill -y -g
   > ```
4. If versions match or check fails → skip, say nothing.

### CLI version

1. Get local CLI version:
   ```bash
   lessie --version 2>/dev/null || npx @lessie/cli --version 2>/dev/null
   ```
2. Get latest published version:
   ```bash
   npm view @lessie/cli version 2>/dev/null
   ```
3. If the remote version is newer → tell the user:
   > ⬆️ A newer version of Lessie CLI is available ({local} → {remote}). Run this command to update:
   > ```
   > npm install -g @lessie/cli
   > ```
4. If versions match or either command fails → skip, say nothing.

## Quick start

After setup, try saying to Claude:

- "Find Engineering Managers at Stripe in San Francisco"
- "Look up Sam Altman's contact info"
- "Research OpenAI — recent news and open job postings"

## Mode detection

Determine which mode to use at the start of each session:

1. Check if `lessie` CLI is available: run `lessie status`
2. If the command succeeds → use **CLI mode** (call tools via Bash)
3. If the command fails (not found) → attempt auto-install: `npm install -g @lessie/cli`
4. After install, run `lessie status` again to verify
5. If install succeeds → use **CLI mode**
6. If install fails (no npm, permission denied, network error, etc.) → check if MCP tools are available (`authorize`, `use_lessie`)
7. If MCP tools are available → use **MCP mode**
8. If neither → inform the user that installation failed and suggest manual install or MCP setup

## Credits & Pricing

Lessie is a credit-based service.

New accounts receive free trial credits. View your balance and purchase more at https://lessie.ai/pricing.

The agent will disambiguate company names before searching to avoid wasting credits on wrong results.

## Data & Privacy

- **Data sources:** Contact and company information is aggregated from publicly available sources (business directories, social profiles, corporate websites).
- **Query logging:** Search queries are logged for service improvement and abuse prevention. No query data is shared with third parties.
- **Data compliance:** Lessie follows applicable data protection regulations. Users are responsible for using retrieved contact data in compliance with local laws (GDPR, CAN-SPAM, etc.).
- **Privacy policy:** https://lessie.ai/privacy
- **Terms of service:** https://lessie.ai/terms-of-service

## Authorization

### CLI mode

1. Run `lessie status` to check token validity.
2. If `authorized: false` → run `lessie auth` to open browser for login.
3. After the user completes login, run `lessie status` again to confirm.

### MCP mode

1. Call `authorize` to check connection status.
2. **If already authorized** → proceed to use tools directly.
3. **If not authorized** → `authorize` returns an authorization URL. Tell the user you need to open a browser for Lessie login/registration, and open it using the appropriate system command:
   - macOS: `open "<url>"`
   - Linux: `xdg-open "<url>"`
   - Windows: `start "<url>"`
4. Tell the user the browser has been opened and they need to complete login/registration.
5. After the user confirms, call `authorize` again to verify the connection.
6. If authorization fails (timeout, denied, port conflict), follow the diagnostic hints returned by `authorize` and retry.

Always inform the user before opening the browser — never silently redirect.

## Agent behavior rules

### CRITICAL: Confirm before every credit-consuming action

Every Lessie tool call costs credits. Credit costs per tool:

| Tool | Cost |
|------|------|
| `find-people` | **20 credits** per search |
| `enrich-people` | 1 credit × number of people (only charged for successful matches) |
| `review-people` | 1 credit × number of people |
| `enrich-org` | 1 credit |
| `find-orgs` | 1 credit |
| `job-postings` | 1 credit |
| `company-news` | 1 credit |
| `web-search` | 1 credit |
| `web-fetch` | 1 credit |
| `unlock_emails` | **3 credits** per newly unlocked person (current rate; check `price_per_unlock` in the response for the live value). Already-unlocked persons (across any of your prior searches) are free. Failed lookups not charged |
| `unlock_email_by_handle` | **3 credits** per successful unlock (current rate; check `price_per_unlock` in the response for the live value). `not_found` and `failed` are free. **Not idempotent** — re-running on the same handle re-charges |
| `unlock_phones` | **8 credits** per newly unlocked person (current rate; check `price_per_unlock` in the response). Already-unlocked persons across any of your prior searches are free. `non_unlockable` / `failed` not charged. Same per-user idempotency contract as `unlock_emails` |
| `unlock_phone_by_handle` | **8 credits** per successful unlock (current rate). Only `platform="linkedin"` actually resolves — other platforms return `not_found` with `reason="unsupported_platform"` and are free. **Not idempotent** for the same `(linkedin, handle)` pair |

**Before executing any command**, you MUST:

1. Tell the user what you are about to do and the estimated cost (e.g., "I'll enrich 3 people — this costs ~3 credits").
2. **Wait for explicit confirmation** before executing.
3. Never batch multiple credit-consuming calls without confirming the full plan first.

**Exception — skip confirmation** if the user has explicitly said they don't want to be prompted (e.g., "don't ask me every time", "just do it", "skip confirmations"). In that case, proceed directly but still log what you executed and the credits spent after each call.

### CRITICAL: Report credit usage after every call

After each conversation turn that involved one or more Lessie tool calls, append a one-line summary of credits consumed. Format:

> Used `<tool-name>`, cost <N> credit(s).

If multiple tools were called in the same turn, combine them:

> Used `web-search` + `enrich-org`, cost 2 credits total.

### CRITICAL: Read references before first CLI call

**Before executing any `lessie` CLI command for the first time in a session**, you MUST read [references/cli-reference.md](references/cli-reference.md) to learn the exact parameter syntax. Each tool has its own flag set — `find-people` takes `--query` (NL), `enrich-people` takes `--people` (JSON), `unlock-emails` / `unlock-phones` take `--search-id` + `--person-ids`, `unlock-email-by-handle` / `unlock-phone-by-handle` take `--handles`, etc. Don't guess — read the section for the tool you're about to call.

### Search mode disambiguation (B2B vs KOL)

Lessie supports two search modes with different data sources and result types:

- **B2B mode**: Searches professional databases (LinkedIn-based). Best for finding people by job title, company, seniority, or industry. Returns work email, phone, employment history.
- **KOL mode**: Searches social media platforms (Instagram, YouTube, TikTok, Twitter/X). Best for finding influencers, content creators, or public figures by audience, follower count, or content topic. Returns social links, follower counts.

**When the user's intent is ambiguous** — i.e., the query could reasonably target either professionals on LinkedIn or creators on social media — you MUST ask the user to clarify before searching. Present both options concisely:

Example ambiguous query: *"Find individuals who have hands-on experience with brain-monitoring sleep devices to share their insights."*

This could mean:
1. **B2B**: Product managers, engineers, or researchers at sleep-tech companies (via LinkedIn)
2. **KOL**: Health/tech influencers who have reviewed or used such devices (via social media)

Ask: "This could be LinkedIn professionals (PMs, engineers at sleep-tech companies) or social media creators who review sleep devices. Which direction do you prefer — or both?"

**When intent is clear**, proceed directly:
- "Find CTOs at fintech startups" → B2B (obvious)
- "Find beauty influencers on Instagram with 100k+ followers" → KOL (obvious)

### Entity disambiguation

When a user mentions a company name that could refer to multiple entities (e.g., "Manus" could be Manus AI, Manus Bio, Manus Plus, etc.), disambiguate before searching:

1. **Ask the user** which company they mean, or present the top candidates and let them pick.
2. If context makes it unambiguous (e.g., user previously discussed AI agents), state your assumption and confirm: "Did you mean Manus AI (manus.im), the AI-agent company?"
3. **Never silently assume** one entity over another — wrong domain = wasted search credits and irrelevant results.

## Tools overview

### People

| Tool | CLI command | When to use |
|------|-------------|-------------|
| `find_people` | `lessie find-people` | Discover people via a **natural-language task**. Pass the user's request verbatim through `--query`. The agent picks sources (B2B / KOL / web), keywords, and stops automatically. **Hard cap: 3 tool calls + 60s budget per request.** If the response has `partial: true`, the agent hit the budget — results are what it gathered before timeout |
| `enrich_people` | `lessie enrich-people` | Enrich known people with full profiles. **Two paths**: B2B (via linkedin_url or name+domain → email, phone, work history) and KOL (via twitter/instagram/tiktok/youtube username → follower count, social links). Max 10 per call |
| `review_people` | `lessie review-people` | Deep-qualify **ambiguous** candidates via web research — skip for obvious matches/mismatches |

### Contact unlock

| Tool | CLI command | When to use |
|------|-------------|-------------|
| `unlock_emails` | `lessie unlock-emails` | Unlock email addresses for people from a previous `find_people` result. **Per-user idempotent**: people you've already unlocked (in any search) cost 0. Takes `search_id` + `person_ids` (1–50) |
| `unlock_email_by_handle` | `lessie unlock-email-by-handle` | Unlock email by an explicit `(platform, handle)`, **without a prior search**. Takes a list of `{platform, handle}` (1–10). **NOT idempotent** — repeat calls on the same handle re-charge. Use only when the handle isn't in any `find_people` you've run |
| `unlock_phones` | `lessie unlock-phones` | Unlock company phone numbers for people from a previous `find_people` result. Same per-user idempotency contract as `unlock_emails` — already-unlocked people cost 0. Takes `search_id` + `person_ids` (1–50) |
| `unlock_phone_by_handle` | `lessie unlock-phone-by-handle` | Unlock phone by an explicit `(platform, handle)`, **without a prior search**. **Only `linkedin` resolves** — other platforms return `not_found` with `reason="unsupported_platform"` and aren't charged. **NOT idempotent**. Takes a list of `{platform, handle}` (1–10) |

**Decision rules:**
- **email vs phone**: pick the contact channel the user actually needs. `unlock_emails` and `unlock_phones` are independent — calling both for the same person charges both rates. Don't unlock the phone if the user only wants email
- **search-anchored vs handle-anchored**: if the person came from your own `find_people` result → use `unlock_emails` / `unlock_phones` (re-unlocks are free). If you got the handle from outside lessie (a LinkedIn URL the user pasted, a manual mention, etc.) → use `unlock_email_by_handle` / `unlock_phone_by_handle`
- **phone Tier 2 is LinkedIn-only**: `unlock_phone_by_handle` with a Twitter / Instagram / TikTok / YouTube handle will return `not_found` (with `reason="unsupported_platform"`), free of charge. Tell the user up-front rather than appearing to "try and fail"

### Companies

| Tool | CLI command | When to use |
|------|-------------|-------------|
| `find_organizations` | `lessie find-orgs` | Discover companies by name, keyword, location, size, funding |
| `enrich_organization` | `lessie enrich-org` | Get full profile for known company domain(s) — industry, employees, funding, tech stack |
| `get_company_job_postings` | `lessie job-postings` | View active job openings (needs `organization_id` from enrich) |
| `search_company_news` | `lessie company-news` | Find recent news articles (needs `organization_id` from enrich) |

### Web research

| Tool | CLI command | When to use |
|------|-------------|-------------|
| `web_search` | `lessie web-search` | General web search; cached results make follow-up `web_fetch` free |
| `web_fetch` | `lessie web-fetch` | Extract specific info from a URL via AI summarization |

## Detailed references

- **CLI command examples & MCP calling**: See [references/cli-reference.md](references/cli-reference.md)
- **Workflow patterns** (domain resolution, company research, search+qualify): See [references/workflow-patterns.md](references/workflow-patterns.md)
- **Domain resolution decision tree**: See [references/domain-resolution.md](references/domain-resolution.md)

## Key constraints

- `enrich_people` / `enrich_organization`: max 10 per call; split larger lists into batches
- `find_people`: hard ceiling of **3 tool calls + 60s wall-clock budget** per request. `target_count` 1-100 (default 30). NOT paginated — if you need more, run a new call with a different query
- `find_organizations`: paginated — use `--page` for more results
- `web_search` caches page content; if a result has `has_content: true`, calling `web_fetch` on that URL is instant
- Useful keywords to include in a `find-people` query: seniority terms (`owner`, `founder`, `c_suite`, `partner`, `vp`, `head`, `director`, `manager`, `senior`, `entry`, `intern`) and `current` vs `past` to bias employment recency. The agent uses these directly as filters
- For people enrichment, providing `domain` (company domain) alongside name greatly improves match accuracy
- CLI output is JSON on stdout, status messages on stderr — parse stdout for data
