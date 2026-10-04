---
name: api-data-sources
description: Discover, document, and produce an integration blueprint for all authoritative APIs and data sources relevant to a user-described project. Outputs a full research package with per-API docs, a data catalog, and a step-by-step integration guide for a React + Supabase + Vercel + AI Agents stack.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch
---

Research and document all authoritative APIs and data sources for: $ARGUMENTS

$ARGUMENTS should include:
- A description of the app, project, or feature to research
- The target domain / industry (e.g. real estate, fitness, publishing)
- Optionally: budget constraints or pricing tier preferences (free-only, paid OK, enterprise)
- Optionally: data freshness requirements (real-time, daily, weekly, static)
- Optionally: a project slug for the output directory name
- Optionally: a custom output directory (default: `_docs/api-sources/`)
- Empty — ask the user to describe their project and use case

## Purpose

This skill produces a **complete API and data-source research package** — a set of markdown files that fully document every authoritative data source available for a given project, how to access each one, what data it returns, what it costs, and exactly how to integrate it all into a React + Supabase + Vercel + AI Agents application.

**What it produces:**
- A project directory under `_docs/api-sources/[project-slug]/`
- `_OVERVIEW.md` — executive summary of all discovered sources
- `apis/[api-name].md` — one detailed file per API
- `data-sources/[source-name].md` — one file per non-API data source
- `_DATA_CATALOG.md` — human-readable inventory of all available data types
- `_INTEGRATION_BLUEPRINT.md` — step-by-step guide for React + Supabase + Vercel + AI integration

---

## Phase 1 — Elicitation & Scoping

Before researching anything, understand the project deeply enough to filter results.

If the user's description is brief or ambiguous, ask **up to 4 targeted questions**. Skip any that are already answered by the description.

1. **What does the app do?** — What is the core user-facing functionality? What problem does it solve?
2. **What data does the app need?** — What types of information must the app display, process, or act on? (e.g. property listings, workout plans, book metadata, weather data)
3. **What's the budget posture?** — Free-tier only? Willing to pay per-request? Enterprise contracts OK? This filters which APIs to recommend.
4. **What's the data freshness requirement?** — Does data need to be real-time (websockets, streaming), near-real-time (polling every few minutes), daily batch, or static/occasional?

After scoping, write a **Scoping Summary** (internal, not output) that captures:
- The core domain(s) to search
- The data types needed (entities, fields, relationships)
- Budget constraints
- Freshness requirements
- Any explicit user preferences for specific providers

---

## Phase 2 — API & Data Source Discovery

### 2.1 — Search Strategy

For each data type identified in the scoping summary, search systematically:

1. **Search for official/authoritative APIs** — Use web search with queries like:
   - `"[domain] API" site:rapidapi.com OR site:programmableweb.com`
   - `"[data type] API" developer documentation`
   - `"[domain] open data" API`
   - `"[domain] REST API" OR "[domain] GraphQL API"`
2. **Check major API aggregators** — RapidAPI, ProgrammableWeb, API List, Public APIs (github.com/public-apis/public-apis)
3. **Check government/institutional open data** — data.gov, EU Open Data Portal, World Bank, census.gov, etc.
4. **Check domain-specific authoritative sources** — Industry databases, professional associations, research institutions
5. **Identify non-API data sources** — RSS/Atom feeds, CSV/JSON open datasets, web scraping targets (with legality notes), file downloads, existing databases

### 2.2 — Source Classification

Categorize every discovered source into one of these types:

| Type | Description |
|------|-------------|
| **REST API** | Standard HTTP request/response API |
| **GraphQL API** | GraphQL endpoint |
| **WebSocket / Streaming** | Real-time data push |
| **Webhook** | Event-driven push notifications |
| **RSS / Atom Feed** | Syndication feed |
| **Open Dataset** | Downloadable CSV, JSON, XML, or database dump |
| **Web Scraping Target** | Structured data on a public page (note ToS/legality) |
| **Supabase / DB Source** | Existing data the user already has in Supabase or another DB |
| **File-Based** | PDFs, spreadsheets, documents containing structured data |
| **AI-Generated** | Data that would be synthesized or enriched by an AI agent |

### 2.3 — Evaluation Criteria

For each source, assess:

- **Authority** — Is this the canonical/official source for this data? (prefer first-party APIs)
- **Reliability** — How stable is the API? Is there an SLA? When was it last updated?
- **Coverage** — Does it provide all the fields/entities needed, or only a subset?
- **Cost** — Free tier limits? Per-request pricing? Monthly caps?
- **Developer Experience** — Quality of docs, SDKs, community support
- **Terms of Service** — Any restrictions on storage, display, commercial use, or redistribution?

Rank sources as: **Primary** (recommended), **Alternative** (viable backup), or **Supplementary** (fills a gap not covered by primary).

---

## Phase 3 — Per-Source Documentation

### 3.1 — API Documentation Template

For each API, create a file at `apis/[api-name].md` with this structure:

```markdown
# [API Name]

> [One-line description of what this API provides]

| Field | Value |
|-------|-------|
| **Provider** | [Company/org name] |
| **Type** | REST / GraphQL / WebSocket / etc. |
| **Base URL** | `https://api.example.com/v2` |
| **Auth Method** | API Key / OAuth 2.0 / Bearer Token / None |
| **Official Docs** | [link to official documentation] |
| **Status Page** | [link if available] |
| **Role** | Primary / Alternative / Supplementary |

## Pricing & Quotas

| Tier | Price | Rate Limit | Monthly Quota | Notes |
|------|-------|------------|---------------|-------|
| Free | $0 | X req/sec | Y req/month | [any restrictions] |
| Pro | $X/mo | ... | ... | ... |
| Enterprise | Contact | ... | ... | ... |

> **Cost estimate for this project:** Based on [estimated usage pattern], expect ~[X] requests/month → [tier] tier → $[Y]/month.

## Getting Started

### Step 1 — Create an Account
[Exact steps: go to [URL], click sign up, verify email]

### Step 2 — Get API Credentials
[Exact steps: navigate to developer dashboard, create app, copy API key]

### Step 3 — Make Your First Request

```bash
curl -X GET "https://api.example.com/v2/endpoint" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

```typescript
// TypeScript / fetch
const response = await fetch('https://api.example.com/v2/endpoint', {
  headers: {
    'Authorization': `Bearer ${process.env.API_KEY}`,
    'Content-Type': 'application/json',
  },
});
const data = await response.json();
```

### Step 4 — Verify the Response
[Expected response shape — actual JSON example if available]

## Key Endpoints

### [Endpoint Name]
- **Method**: GET / POST / etc.
- **Path**: `/v2/resource`
- **Description**: [what it returns]
- **Parameters**: [key params with types and descriptions]
- **Response Shape**:
```json
{
  "field": "type — description"
}
```

[Repeat for each relevant endpoint]

## Data Fields Available

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `"abc123"` |
| ... | ... | ... | ... |

## Rate Limits & Error Handling

- **Rate limit**: [X requests per second/minute]
- **Rate limit header**: `X-RateLimit-Remaining`
- **Retry strategy**: [exponential backoff recommended]
- **Common errors**:
  | Status | Meaning | Action |
  |--------|---------|--------|
  | 401 | Invalid/expired API key | Refresh credentials |
  | 429 | Rate limited | Back off, retry after `Retry-After` header |
  | 500 | Server error | Retry with backoff |

## Terms of Service Notes

- [Any restrictions on caching, storage, redistribution, attribution requirements]
- [Link to full ToS]

## SDK / Libraries

- **Official SDK**: [npm package name if available]
- **Community libraries**: [notable wrappers]
```

### 3.2 — Non-API Data Source Template

For each non-API source, create a file at `data-sources/[source-name].md`:

```markdown
# [Source Name]

> [One-line description]

| Field | Value |
|-------|-------|
| **Provider** | [Organization] |
| **Type** | Open Dataset / RSS Feed / Scraping Target / File |
| **URL** | [access URL] |
| **Format** | CSV / JSON / XML / HTML / PDF |
| **Update Frequency** | Real-time / Daily / Weekly / Monthly / Static |
| **License** | [license type — CC-BY, MIT, proprietary, etc.] |
| **Role** | Primary / Alternative / Supplementary |

## How to Access

[Step-by-step instructions — download, subscribe, or fetch]

## Data Fields Available

| Field | Type | Description |
|-------|------|-------------|
| ... | ... | ... |

## Ingestion Strategy

[How to get this data into Supabase — manual upload, scheduled cron, Edge Function, etc.]

## Legal & Attribution

[Any attribution requirements, usage restrictions, or licensing terms]
```

---

## Phase 4 — Data Catalog

Create `_DATA_CATALOG.md` — a **human-readable inventory** of all data types available across all sources, filtered to the user's use case.

Structure:

```markdown
# Data Catalog — [Project Name]

> All data types available for [use case description], organized by category.

## [Category 1 — e.g. "Properties" or "User Profiles"]

| Data Point | Type | Source(s) | Freshness | Notes |
|-----------|------|-----------|-----------|-------|
| [field name] | string/number/etc. | [API name(s)] | real-time/daily/etc. | [any notes] |
| ... | ... | ... | ... | ... |

## [Category 2 — e.g. "Market Data"]

| Data Point | Type | Source(s) | Freshness | Notes |
|-----------|------|-----------|-----------|-------|
| ... | ... | ... | ... | ... |

[Repeat for each logical category of data]

## Coverage Matrix

Shows which sources provide which data categories:

| Source | [Cat 1] | [Cat 2] | [Cat 3] | ... |
|--------|---------|---------|---------|-----|
| [API 1] | ✅ | ✅ | ❌ | ... |
| [API 2] | ❌ | ✅ | ✅ | ... |
| [Dataset 1] | ✅ | ❌ | ❌ | ... |

## Gaps & Recommendations

[Any data the user needs that isn't available from discovered sources, with suggestions for alternatives — AI generation, user-submitted data, manual entry, etc.]
```

**Rules for the data catalog:**
- Only include data types that are relevant to the stated use case — don't list every field an API returns
- Group by user-facing category, not by source
- Use plain language — a non-technical stakeholder should be able to read this and understand what data is available
- Call out gaps explicitly — if a needed data type isn't available from any source, say so

---

## Phase 5 — Integration Blueprint

Create `_INTEGRATION_BLUEPRINT.md` — a **step-by-step integration guide** for wiring all sources into a React + Supabase + Vercel + AI Agents application.

Structure:

```markdown
# Integration Blueprint — [Project Name]

> Step-by-step guide to integrate [N] APIs and [M] data sources into a React + Supabase + Vercel + AI Agents stack.

## Architecture Overview

[High-level description of how data flows through the stack]

```
[ASCII or Mermaid diagram showing]:
External APIs → Supabase Edge Functions → Supabase DB → React Client
                                        ↕
                                   AI Agents (OpenAI)
```

## Step 1 — Supabase Setup

### 1.1 — Database Schema

```sql
-- Tables derived from the data catalog
CREATE TABLE [entity] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- fields mapped from API responses
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

[One CREATE TABLE per major entity, with comments explaining field origins]

### 1.2 — Row Level Security

```sql
-- RLS policies for each table
ALTER TABLE [entity] ENABLE ROW LEVEL SECURITY;

CREATE POLICY "..." ON [entity]
  FOR SELECT USING (auth.uid() = user_id);
```

### 1.3 — Environment Variables

```bash
# .env.local
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key

# API keys for each external source
[API_NAME]_API_KEY=your-key
OPENAI_API_KEY=your-key
```

## Step 2 — API Integration Layer

### 2.1 — Supabase Edge Functions

For each external API, create a Supabase Edge Function that:
1. Accepts a request from the client
2. Adds the API key server-side (never expose keys to the client)
3. Calls the external API
4. Transforms the response to match the DB schema
5. Optionally caches in Supabase

```typescript
// supabase/functions/[api-name]/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // [Implementation specific to each API]
})
```

[One code block per Edge Function with full implementation]

### 2.2 — Data Transformation

```typescript
// lib/transformers/[api-name].ts
// Maps external API response shapes to internal DB schema
export function transform[Entity](apiResponse: ExternalType): InternalType {
  return {
    // field mappings
  }
}
```

### 2.3 — Caching Strategy

| Source | Cache Duration | Strategy | Rationale |
|--------|---------------|----------|-----------|
| [API 1] | 1 hour | Supabase table + stale-while-revalidate | [why] |
| [API 2] | No cache | Direct passthrough | [why — e.g. real-time pricing] |
| [Dataset] | 24 hours | Full table refresh via cron | [why] |

## Step 3 — React Client Integration

### 3.1 — Supabase Client Setup

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

### 3.2 — Data Hooks

```typescript
// hooks/use[Entity].ts
import { useQuery } from '@tanstack/react-query' // or SWR, or Supabase realtime

export function use[Entity](params: Params) {
  return useQuery({
    queryKey: ['entity', params],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('entity')
        .select('*')
        .match(params)
      if (error) throw error
      return data
    },
  })
}
```

[One hook per major data entity]

### 3.3 — Edge Function Calls (for fresh external data)

```typescript
// lib/api/[api-name].ts
export async function fetch[Data](params: Params) {
  const { data, error } = await supabase.functions.invoke('[api-name]', {
    body: params,
  })
  if (error) throw error
  return data
}
```

## Step 4 — AI Agent Integration

### 4.1 — Agent Architecture

[Describe how AI agents fit into the data flow]:
- Which data gets sent to the AI agent as context
- What the agent produces (summaries, recommendations, transformations, etc.)
- Whether the agent runs on-demand (user-triggered) or in the background (automated)

### 4.2 — OpenAI Integration

```typescript
// lib/ai/agent.ts
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function run[Agent](context: ContextType) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: `[System prompt specific to this use case]` },
      { role: 'user', content: JSON.stringify(context) },
    ],
  })
  return completion.choices[0].message.content
}
```

### 4.3 — Agent as Supabase Edge Function

```typescript
// supabase/functions/ai-[task]/index.ts
// Wraps the AI call in an Edge Function so the API key stays server-side
```

### 4.4 — Cost Estimation

| Model | Input Cost | Output Cost | Est. Tokens/Request | Est. Monthly Cost |
|-------|-----------|-------------|--------------------|--------------------|
| gpt-4o | $2.50/1M | $10/1M | [estimate] | $[estimate] |
| gpt-4o-mini | $0.15/1M | $0.60/1M | [estimate] | $[estimate] |

> **Recommendation**: [Which model to use and why, based on the use case complexity vs. cost]

## Step 5 — Vercel Deployment

### 5.1 — Environment Variables

Set these in the Vercel dashboard under Project → Settings → Environment Variables:

| Variable | Where to Get It |
|----------|----------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Dashboard → Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Same |
| `[API_NAME]_API_KEY` | [Provider dashboard URL] |
| `OPENAI_API_KEY` | platform.openai.com |

### 5.2 — API Routes (if using Next.js API routes instead of / in addition to Edge Functions)

```typescript
// app/api/[endpoint]/route.ts
```

### 5.3 — Cron Jobs (if needed)

```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/cron/refresh-[data]",
      "schedule": "0 */6 * * *"
    }
  ]
}
```

### 5.4 — Deployment Checklist

- [ ] All environment variables set in Vercel
- [ ] Supabase Edge Functions deployed (`supabase functions deploy`)
- [ ] Database migrations applied (`supabase db push`)
- [ ] RLS policies verified
- [ ] API rate limits tested under expected load
- [ ] AI agent costs estimated and budget alerts set
- [ ] Error monitoring configured (Sentry / Vercel Analytics)

## Cost Summary

| Service | Tier | Monthly Cost | Notes |
|---------|------|-------------|-------|
| Supabase | [Free/Pro] | $[X] | [what's included] |
| [API 1] | [Tier] | $[X] | [based on estimated usage] |
| [API 2] | [Tier] | $[X] | ... |
| OpenAI | Pay-as-you-go | $[X] | [based on model + est. usage] |
| Vercel | [Hobby/Pro] | $[X] | [based on traffic estimate] |
| **Total** | | **$[X]/mo** | |
```

---

## Execution Steps

### Step 1 — Scope the Project
Read `$ARGUMENTS`. If insufficient, ask the 4 elicitation questions. Produce an internal scoping summary.

### Step 2 — Research APIs & Data Sources
Use web search extensively. For each domain/data-type identified in scoping, search for authoritative APIs. Visit official documentation pages to verify endpoints, pricing, and auth methods. Check API aggregators for alternatives.

### Step 3 — Create the Output Directory
Create `_docs/api-sources/[project-slug]/`, `apis/`, and `data-sources/` subdirectories.

### Step 4 — Write _OVERVIEW.md
Summarize all discovered sources, their roles (primary/alternative/supplementary), and the overall data strategy.

### Step 5 — Write Individual API Files
One file per API in `apis/`. Follow the API documentation template exactly. **Include working code examples** — don't leave placeholders. If you cannot verify an endpoint, note it as "unverified."

### Step 6 — Write Individual Data Source Files
One file per non-API source in `data-sources/`. Follow the data source template.

### Step 7 — Write _DATA_CATALOG.md
Compile the full data inventory. Organize by user-facing category. Include the coverage matrix. Call out gaps.

### Step 8 — Write _INTEGRATION_BLUEPRINT.md
Produce the full integration guide. Every code block should be as close to production-ready as possible. Include actual SQL schemas, actual TypeScript types, actual Edge Function boilerplate.

### Step 9 — Report
Summarize what was created using the output format below.

---

## Output Format

After generating all files, output:

```
## API & Data Source Research: [Project Name]

### Sources Discovered
- **APIs**: [count] ([count] primary, [count] alternative, [count] supplementary)
- **Data Sources**: [count]
- **Data Types Cataloged**: [count] across [count] categories

### Files Created
- `_docs/api-sources/[slug]/_OVERVIEW.md` — Executive summary
- `_docs/api-sources/[slug]/apis/[name].md` — [one-line desc]
- ...
- `_docs/api-sources/[slug]/data-sources/[name].md` — [one-line desc]
- ...
- `_docs/api-sources/[slug]/_DATA_CATALOG.md` — Full data inventory
- `_docs/api-sources/[slug]/_INTEGRATION_BLUEPRINT.md` — React + Supabase + Vercel + AI guide

### Estimated Monthly Cost
| Service | Cost |
|---------|------|
| [itemized] | $X |
| **Total** | **$X/mo** |

### Coverage Gaps
- [Any data the user needs that no source provides]

### Next Steps
1. Review `_OVERVIEW.md` for the recommended source selection
2. Sign up for API keys (links in each API file)
3. Follow `_INTEGRATION_BLUEPRINT.md` step by step
4. Start with the primary APIs; add alternatives if you hit rate limits or need more coverage
```

---

## Anti-Patterns

- **Don't recommend APIs you haven't verified.** If you can't confirm an API exists and has current documentation, don't include it. Note any uncertainty explicitly.
- **Don't skip pricing.** Every API file must include pricing information. If pricing isn't publicly available, say "Contact sales — pricing not public" rather than guessing.
- **Don't recommend scraping when an API exists.** Always prefer official APIs over scraping. Only suggest scraping as a last resort, and always note ToS implications.
- **Don't write placeholder code.** Code examples should be as close to copy-paste-ready as possible. Use realistic variable names, proper error handling, and TypeScript types.
- **Don't conflate data types with API endpoints.** The data catalog should be organized by what the user *sees* (entities, fields), not by which API returns them.
- **Don't ignore free tiers.** Many projects can run entirely on free tiers. Always document the free tier first, then paid upgrades.
- **Don't ignore rate limits.** Rate limits are a production concern. Always document them and include retry/backoff strategies.
- **Don't be vague about auth.** "Uses API key" is not enough. Document exactly where to put the key (header, query param, bearer token) with a working example.
- **Don't forget AI cost estimation.** AI agents can be the most expensive part of the stack. Always include token/cost estimates for the specific use case.
