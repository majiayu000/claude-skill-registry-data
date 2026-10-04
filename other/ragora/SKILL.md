---
name: ragora
description: Use Ragora MCP tools and REST API to discover, search, and synthesize answers from knowledge bases. Trigger when the user asks for grounded answers from Ragora collections, cross-collection comparison, source-backed summaries, due diligence research, or verification using marketplace data.
metadata: {"openclaw": {"emoji": "🔎", "homepage": "https://github.com/velarynai/ragora-openclaw", "requires": {"env": ["RAGORA_API_KEY"]}, "primaryEnv": "RAGORA_API_KEY"}}
---

# Ragora Skill for OpenClaw

Use this skill to answer questions with Ragora data. You have two integration paths:

1. **MCP (Model Context Protocol)** — preferred when your client supports MCP tool binding.
2. **REST API** — use directly via HTTP when MCP is unavailable or when you need fine-grained control.

Both paths share the same authentication, data model, and search capabilities.

## Source of Truth Docs

Consult these docs first when behavior differs across environments:

- MCP guide: `https://ragora.app/docs?section=mcp-guide`
- Getting started: `https://ragora.app/docs?section=getting-started`
- API overview: `https://ragora.app/docs?section=api-overview`
- Retrieve API: `https://ragora.app/docs?section=api-retrieve`
- Errors and limits: `https://ragora.app/docs?section=api-errors`
- Billing API: `https://ragora.app/docs?section=api-billing`

---

## Core Concepts

Before using any tools, understand the Ragora data model.

### Collections

A **collection** is a knowledge base — a curated set of documents indexed for semantic search. Each collection has:

- **Name** — human-readable label (e.g., "Employee Handbook").
- **Slug** — URL-safe identifier used in dynamic tools and API paths (e.g., `employee_handbook`).
- **Description** — what the collection contains and when to use it.
- **Stats** — document count, chunk count, last updated timestamp.

### Documents & Chunks

Each collection contains **documents** (files, pages, articles). Documents are split into **chunks** — small passages optimized for semantic retrieval. When you search, results are returned at the chunk level with metadata pointing back to the source document.

### Versions

Some collections support **versioned documentation** (e.g., API docs v1.0, v2.0). Use `list_versions_{slug}()` or the API to discover available versions, then pass a `version` parameter to scope your search.

### Tags & Filters

Collections may support:

- **Custom tags** — string labels attached to documents (e.g., `["legal", "msa", "2024"]`). Pass as `custom_tags` to narrow results.
- **Filters** — key-value metadata filters (e.g., `{"region": "US", "department": "engineering"}`). Pass as `filters` to constrain results.

### Credits & Billing

- **Own collections and subscriptions** — free MCP/API access, no credit cost.
- **Marketplace products (pay-per-use)** — each retrieval deducts credits based on seller pricing.
- Credits are measured in USD. Check with `check_balance()` or `GET /v1/billing/balance`.
- Top up at `https://app.ragora.app/settings/billing`.

---

## Connection Setup

### Authentication

All requests (MCP and REST) require a Ragora API key.

- **Format**: `sk_live_<uuid>` (e.g., `sk_live_a1b2c3d4-e5f6-7890-abcd-ef1234567890`)
- **Create one**: `https://app.ragora.app/settings/api-keys`
- **Shown once** — copy and store it securely at creation time.
- **Hashed on server** — SHA-256 + bcrypt. Ragora cannot recover a lost key; generate a new one.

### Security rules

- Never pass API keys in URL query parameters.
- Never print full API keys in logs, outputs, or final answers.
- If the key is missing or invalid, stop and ask the user for a valid key.
- Mask keys in any debug output: `sk_live_****...`.

### MCP endpoint

- **URL**: `https://mcp.ragora.app/mcp`
- **Auth header**: `Authorization: Bearer <RAGORA_API_KEY>`

OpenClaw config (YAML):

```yaml
name: ragora
type: http
url: https://mcp.ragora.app/mcp
headers:
  Authorization: Bearer ${RAGORA_API_KEY}
```

Claude Desktop / Cursor / VS Code config (JSON):

```json
{
  "mcpServers": {
    "ragora": {
      "type": "http",
      "url": "https://mcp.ragora.app/mcp",
      "headers": {
        "Authorization": "Bearer ${RAGORA_API_KEY}"
      }
    }
  }
}
```

> **Security note**: Set `RAGORA_API_KEY` as an environment variable in your OS or secret manager. Never hardcode the raw `sk_live_*` value in config files that may be committed to version control.

### REST API base URL

- **Base**: `https://api.ragora.app/v1`
- **Auth header**: `Authorization: Bearer <RAGORA_API_KEY>`
- **Content-Type**: `application/json` for all POST/PUT requests.

---

## Connectivity Check (Run First)

### Via MCP

1. Confirm server health:

```bash
curl -s https://mcp.ragora.app/health
```

2. Call `discover_collections()`. If it returns collections, you're connected.

3. If empty — user may need to access a knowledge base: `https://ragora.app/marketplace`

4. If credits are low — call `check_balance()` and tell user to top up at `https://app.ragora.app/settings/billing`.

### Via REST API

1. Confirm server health:

```bash
curl -s https://api.ragora.app/v1/health
```

2. List collections:

```bash
curl https://api.ragora.app/v1/collections \
  -H "Authorization: Bearer <RAGORA_API_KEY>"
```

3. If the response is `401` or `403`, the API key is invalid or expired. Ask the user to generate a new one.

---

## Operating Rules

- Start with `discover_collections()` (MCP) or `GET /v1/collections` (API) before targeted retrieval, unless the user explicitly names a known collection.
- Prefer targeted collection search over global search once you know the likely collections.
- Use global search for broad exploration only — ambiguity, unknown source, or discovery pass.
- Keep retrieval iterative: run multiple focused queries instead of one long query.
- Include source attribution from returned results in final answers.
- Call out uncertainty when evidence is partial, conflicting, or missing.
- If credits are low or errors mention billing limits, check balance and report constraints.
- Choose MCP tools when available; fall back to REST API when MCP binding fails or when you need features not exposed via MCP (e.g., pagination, collection metadata).

---

## MCP Tools Reference

### Static tools (always available)

| Tool | Parameters | Description |
|------|-----------|-------------|
| `discover_collections()` | none | List all accessible knowledge bases with descriptions, stats, available operations, and usage examples. |
| `search(query, top_k?)` | `query` (required), `top_k` (1-20, default 5) | Search across ALL accessible collections at once. |
| `search_collection(collection_name, query, top_k?, custom_tags?, filters?)` | `collection_name` (required), `query` (required), `top_k` (1-20, default 5), `custom_tags` (list of strings), `filters` (object) | Search a specific collection by name or slug. |
| `check_balance()` | none | Credits remaining and estimated USD value. |

### Dynamic tools (per-collection, returned in manifest)

The Gateway generates these tools for each collection you have access to. The `{slug}` is the collection's URL-safe name (e.g., `employee_handbook`, `k8s_troubleshooting`).

| Tool | Parameters | Description |
|------|-----------|-------------|
| `search_{slug}(query, top_k?, version?, custom_tags?, filters?)` | `query` (required), `top_k` (1-20, default 5), `version` (optional string), `custom_tags` (list of strings), `filters` (object) | Semantic search within the collection. |
| `get_topic_{slug}(topic)` | `topic` (required string) | Retrieve information about a specific topic from the collection. |
| `list_versions_{slug}()` | none | List all available documentation versions for the collection. |

### MCP Resources

| URI | Description |
|-----|-------------|
| `ragora://collections` | Lists all accessible collections with metadata, stats, and available operations. |

### MCP Prompts

| Prompt | Parameters | Description |
|--------|-----------|-------------|
| `search_collection_prompt` | `collection_name`, `query` | Pre-built prompt for searching a specific collection. |
| `summarize_collection` | `collection_name` | Pre-built prompt for summarizing an entire collection. |
| `compare_sources` | `collection_names`, `question` | Pre-built prompt for comparing information across multiple collections. |

---

## REST API Reference

Use these endpoints when MCP tool binding is unavailable, or when you need direct HTTP control.

**All endpoints require**: `Authorization: Bearer <RAGORA_API_KEY>`

### Health check

```
GET https://api.ragora.app/v1/health
```

Response: `200 OK` with `{"status": "ok"}` if the service is up.

### List collections

```
GET https://api.ragora.app/v1/collections
```

Returns all collections accessible to the authenticated user.

Response:

```json
{
  "collections": [
    {
      "name": "Employee Handbook",
      "slug": "employee_handbook",
      "description": "Company policies, benefits, and procedures",
      "stats": {
        "document_count": 45,
        "chunk_count": 1230,
        "last_updated": "2025-11-15T08:30:00Z"
      },
      "supported_features": ["search", "get_topic", "versions", "filters"]
    }
  ]
}
```

### Search across all collections

```
POST https://api.ragora.app/v1/search
```

Request:

```json
{
  "query": "vacation policy for remote employees",
  "top_k": 5
}
```

Response:

```json
{
  "results": [
    {
      "content": "Remote employees are entitled to 20 days of paid vacation per year...",
      "score": 0.94,
      "source": {
        "collection": "employee_handbook",
        "document": "benefits-guide.md",
        "chunk_id": "ch_abc123"
      },
      "metadata": {}
    }
  ],
  "usage": {
    "cost_usd": 0.0,
    "balance_remaining_usd": 99.95
  }
}
```

### Search a specific collection

```
POST https://api.ragora.app/v1/collections/{slug}/search
```

Request:

```json
{
  "query": "log retention duration and deletion policy",
  "top_k": 5,
  "version": "2.0",
  "custom_tags": ["compliance", "soc2"],
  "filters": {
    "region": "US"
  }
}
```

Response: same structure as global search, but scoped to the named collection.

### Get topic from a collection

```
POST https://api.ragora.app/v1/collections/{slug}/topic
```

Request:

```json
{
  "topic": "remote work policy"
}
```

Response:

```json
{
  "content": "Detailed information about the remote work policy...",
  "source": {
    "collection": "employee_handbook",
    "document": "remote-work.md"
  },
  "usage": {
    "cost_usd": 0.0,
    "balance_remaining_usd": 99.95
  }
}
```

### List versions for a collection

```
GET https://api.ragora.app/v1/collections/{slug}/versions
```

Response:

```json
{
  "versions": [
    {"version": "2.0", "label": "v2.0 (latest)", "is_default": true},
    {"version": "1.5", "label": "v1.5", "is_default": false},
    {"version": "1.0", "label": "v1.0 (legacy)", "is_default": false}
  ]
}
```

### Check balance

```
GET https://api.ragora.app/v1/billing/balance
```

Response:

```json
{
  "credits_remaining": 9950,
  "estimated_usd": 99.50,
  "currency": "USD"
}
```

### MCP Gateway endpoints (tool proxy)

If you need to call MCP tools via REST (e.g., dynamic tools like `search_employee_handbook`):

**Get manifest** — lists all available MCP tools for your account:

```
GET https://api.ragora.app/v1/mcp/manifest
```

**Execute a tool** — call any MCP tool by name:

```
POST https://api.ragora.app/v1/mcp/execute
```

Request:

```json
{
  "tool": "search_employee_handbook",
  "arguments": {
    "query": "vacation policy",
    "top_k": 5
  }
}
```

Response:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 5 results:\n\n1. **Vacation Policy** (score: 0.95)\n   Remote employees are entitled to...\n   Source: benefits-guide.md"
    }
  ],
  "usage": {
    "cost_usd": 0.0,
    "balance_remaining_usd": 99.95
  }
}
```

---

## Error Codes & Status Handling

### HTTP status codes

| Status | Meaning | Agent action |
|--------|---------|--------------|
| `200` | Success | Process results normally. |
| `400` | Bad request — malformed query, missing required param | Check request format. Fix the query and retry. |
| `401` | Unauthorized — missing or invalid API key | Stop. Ask the user to provide a valid `sk_live_` key. |
| `403` | Forbidden — key is valid but lacks access to this collection | Inform user they need to purchase/subscribe to this collection at the marketplace. |
| `404` | Not found — collection slug or endpoint doesn't exist | Check the slug with `discover_collections()` or `GET /v1/collections`. |
| `422` | Validation error — params are present but invalid (e.g., `top_k=50`) | Read the error message, fix the parameter, and retry. |
| `429` | Rate limited — too many requests | Wait and retry with exponential backoff (see Rate Limiting below). |
| `402` | Payment required — insufficient credits | Call `check_balance()`. Tell user to top up at billing page. |
| `500` | Server error | Retry once after 2 seconds. If it persists, inform user of a temporary service issue. |
| `503` | Service unavailable | Retry once after 5 seconds. If it persists, inform user. |

### Error response format

```json
{
  "error": {
    "code": "insufficient_credits",
    "message": "Your balance is too low to complete this search. Current balance: $0.05.",
    "details": {}
  }
}
```

### Common error codes in response body

| Code | Description | Agent action |
|------|-------------|--------------|
| `invalid_api_key` | Key format wrong or key revoked | Ask user for a new key. |
| `expired_api_key` | Key has expired | Ask user to generate a new key at dashboard. |
| `insufficient_credits` | Not enough credits for this retrieval | Report balance and link to billing. |
| `collection_not_found` | Slug doesn't match any collection | Re-run discovery, check spelling. |
| `collection_access_denied` | User hasn't purchased access | Link user to the marketplace. |
| `rate_limit_exceeded` | Too many requests in window | Back off and retry. |
| `invalid_query` | Query is empty or too long | Fix and retry with a shorter, clearer query. |
| `version_not_found` | Requested version doesn't exist | Call `list_versions_{slug}()` to see valid versions. |

---

## Rate Limiting & Retry Strategy

### Limits

- **MCP tools**: 60 calls per minute per API key.
- **REST API**: 120 requests per minute per API key.
- Rate limit headers are returned on every response:
  - `X-RateLimit-Limit` — max requests in the window.
  - `X-RateLimit-Remaining` — requests left in the current window.
  - `X-RateLimit-Reset` — Unix timestamp when the window resets.

### Retry strategy

When you receive a `429` response:

1. Read the `Retry-After` header (seconds to wait) if present.
2. If no `Retry-After`, use exponential backoff: wait 1s, then 2s, then 4s.
3. Maximum 3 retries before giving up and informing the user.
4. Never retry `401` or `403` — these require user action, not waiting.

### Best practices to avoid rate limits

- Batch your queries logically: 3-5 focused queries per task, not 20 rapid-fire calls.
- Use `top_k=10-15` instead of making multiple `top_k=3` calls for the same question.
- Cache `discover_collections()` results within a session — collection lists rarely change mid-conversation.

---

## Authentication Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` on every call | Missing or malformed `Authorization` header | Ensure header is exactly `Authorization: Bearer sk_live_xxxxx`. No extra spaces, no quotes around the token. |
| `401` but key looks correct | Key was revoked or regenerated | Ask user to check active keys at `https://app.ragora.app/settings/api-keys`. |
| `401` with `invalid_api_key` code | Key format is wrong (e.g., missing `sk_live_` prefix) | Verify format: must start with `sk_live_` followed by a UUID. |
| `401` with `expired_api_key` code | Key has an expiration and it passed | Generate a new key from the dashboard. |
| `403 Forbidden` | Key is valid but doesn't have access to the requested collection | User needs to purchase or subscribe to the collection. |
| MCP tools not appearing | MCP server not configured or wrong URL | Verify MCP URL is `https://mcp.ragora.app/mcp` and header is set. Run health check. |
| MCP tools appear but return errors | Key in MCP config is a placeholder | Replace `sk_live_xxx` with the actual key. |
| `ECONNREFUSED` or timeout | Network issue or service outage | Check `https://mcp.ragora.app/health`. If down, fall back to REST API or wait. |

---

## Core Workflow

### 1. Understand intent

- Classify request type: factual lookup, summary, comparison, extraction, or verification.
- Identify likely domains/collections from user wording.

### 2. Discover scope

- Run `discover_collections()` (MCP) or `GET /v1/collections` (API).
- Select 1-3 collections most relevant to the question.
- If no relevant collection exists, state that explicitly and stop.

### 3. Retrieve evidence

- **First pass**: one targeted query per selected collection.
- **Second pass**: refine with specific sub-queries (dates, entities, claims, thresholds).
- Tune `top_k` based on task:
  - `top_k=3-5` for direct factual questions.
  - `top_k=8-12` for comparisons or comprehensive summaries.
  - `top_k=15-20` for exhaustive research or due diligence.

### 4. Synthesize

- Merge evidence by claim, not by source order.
- Resolve conflicts by preferring direct passages and recency cues in content.
- Distinguish facts from inferences.

### 5. Respond

- Give a concise answer first.
- Then provide evidence bullets with collection/source references.
- End with gaps, caveats, or suggested follow-up queries when confidence is not high.

---

## Multi-Step Workflow Examples

### Research a topic across multiple collections

**Scenario**: User asks "What is our data retention policy and how does it compare to SOC 2 requirements?"

1. `discover_collections()` → find `security_handbook`, `compliance_docs`, `soc2_guide`
2. `search_collection("security_handbook", "data retention policy duration", top_k=5)`
3. `search_collection("compliance_docs", "SOC 2 data retention requirements", top_k=5)`
4. `search_collection("soc2_guide", "retention controls audit evidence", top_k=5)`
5. Synthesize: compare internal policy against SOC 2 requirements, note gaps.
6. Respond with findings, citing each collection.

### Compare two vendor contracts

**Scenario**: User asks "Compare the SLA terms between Vendor A and Vendor B."

1. `discover_collections()` → find `vendor_a_contract`, `vendor_b_contract`
2. `search_collection("vendor_a_contract", "SLA uptime guarantees penalties", top_k=8)`
3. `search_collection("vendor_b_contract", "SLA uptime guarantees penalties", top_k=8)`
4. Second pass for specifics:
   - `search_collection("vendor_a_contract", "termination notice period remedies", top_k=5)`
   - `search_collection("vendor_b_contract", "termination notice period remedies", top_k=5)`
5. Build comparison table: uptime %, penalty structure, notice periods, exclusions.
6. Highlight key differences and risks.

### Due diligence deep dive

**Scenario**: User asks "Summarize everything we know about Company X's security posture."

1. `search("Company X security audit penetration test vulnerability", top_k=15)` — broad discovery pass.
2. Identify which collections returned results (e.g., `due_diligence_reports`, `vendor_assessments`).
3. Targeted follow-up:
   - `search_collection("due_diligence_reports", "Company X SOC 2 ISO 27001 certifications", top_k=10)`
   - `search_collection("vendor_assessments", "Company X data encryption access controls", top_k=10)`
   - `search_collection("due_diligence_reports", "Company X incident history breach", top_k=5)`
4. Organize findings by category: certifications, technical controls, incident history, gaps.
5. Present with confidence levels and note areas with no data.

### Versioned documentation lookup

**Scenario**: User asks "What changed in the authentication flow between API v1 and v2?"

1. `list_versions_api_docs()` → returns `["1.0", "2.0"]`
2. `search_api_docs(query="authentication flow token exchange", version="1.0", top_k=5)`
3. `search_api_docs(query="authentication flow token exchange", version="2.0", top_k=5)`
4. Diff the results: what was added, changed, or removed.
5. Present a clear changelog-style summary.

### REST API workflow (no MCP)

**Scenario**: MCP binding is unavailable. User asks "Find our vacation policy."

1. Health check:
```bash
curl -s https://api.ragora.app/v1/health
```

2. List collections:
```bash
curl https://api.ragora.app/v1/collections \
  -H "Authorization: Bearer $RAGORA_API_KEY"
```

3. Search the relevant collection:
```bash
curl -X POST https://api.ragora.app/v1/collections/employee_handbook/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "vacation policy paid time off", "top_k": 5}'
```

4. Parse the `results` array, extract `content` and `source` fields, and compose the answer.

---

## Query Patterns

Use short, specific queries. Prefer multiple passes over one monolithic query.

### By task type

| Task | Query pattern | Example |
|------|--------------|---------|
| Factual lookup | `"<entity> <metric/attribute> <time period>"` | `"ACME Corp revenue 2024 Q3"` |
| Policy/requirements | `"<policy type> eligibility criteria exceptions"` | `"parental leave eligibility criteria exceptions"` |
| Comparison | Run same query across each collection | `"pricing limits SLA exclusions"` × 2 collections |
| Validation | First `"<claim>"`, then `"counterexample exception to <claim>"` | `"all employees get 20 vacation days"` then `"exceptions to vacation day policy"` |
| Extraction | `"<entity> <specific data point>"` | `"ACME Corp CEO contact information"` |
| Timeline | `"<entity> <event type> chronological"` | `"product launches timeline 2023 2024"` |

### Query refinement strategy

1. **Start broad**: `"data retention policy"` — see what's available.
2. **Narrow by entity**: `"customer data retention policy"` — scope to a specific domain.
3. **Narrow by attribute**: `"customer data retention duration deletion schedule"` — get specifics.
4. **Add constraints**: Use `filters` and `custom_tags` if results are noisy.

---

## Tooling Playbook

### Discover collections

MCP:
```text
discover_collections()
```

API:
```bash
curl https://api.ragora.app/v1/collections \
  -H "Authorization: Bearer $RAGORA_API_KEY"
```

### Broad search when unsure

MCP:
```text
search(query="SOC 2 retention policy for customer logs", top_k=8)
```

API:
```bash
curl -X POST https://api.ragora.app/v1/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SOC 2 retention policy for customer logs", "top_k": 8}'
```

### Targeted collection search

MCP:
```text
search_collection(
  collection_name="security-handbook",
  query="log retention duration and deletion policy",
  top_k=5
)
```

API:
```bash
curl -X POST https://api.ragora.app/v1/collections/security_handbook/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "log retention duration and deletion policy", "top_k": 5}'
```

### Search with version

MCP:
```text
search_api_docs(
  query="authentication flow changes",
  version="2.0",
  top_k=5
)
```

API:
```bash
curl -X POST https://api.ragora.app/v1/collections/api_docs/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication flow changes", "version": "2.0", "top_k": 5}'
```

### Get topic from a collection

MCP:
```text
get_topic_employee_handbook(topic="remote work policy")
```

API:
```bash
curl -X POST https://api.ragora.app/v1/collections/employee_handbook/topic \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"topic": "remote work policy"}'
```

### Filtered search

MCP:
```text
search_collection(
  collection_name="contracts",
  query="termination for convenience notice period",
  top_k=10,
  custom_tags=["msa", "legal"],
  filters={"region": "US"}
)
```

API:
```bash
curl -X POST https://api.ragora.app/v1/collections/contracts/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "termination for convenience notice period", "top_k": 10, "custom_tags": ["msa", "legal"], "filters": {"region": "US"}}'
```

### Credit check

MCP:
```text
check_balance()
```

API:
```bash
curl https://api.ragora.app/v1/billing/balance \
  -H "Authorization: Bearer $RAGORA_API_KEY"
```

### Compare across collections

MCP prompt:
```text
compare_sources(
  collection_names=["vendor-a-docs", "vendor-b-docs"],
  question="What are the SLA differences?"
)
```

API (manual — run two searches and compare):
```bash
# Search vendor A
curl -X POST https://api.ragora.app/v1/collections/vendor_a_docs/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SLA uptime guarantees penalties", "top_k": 8}'

# Search vendor B
curl -X POST https://api.ragora.app/v1/collections/vendor_b_docs/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SLA uptime guarantees penalties", "top_k": 8}'
```

---

## Context Management

### Choosing `top_k`

| Scenario | Recommended `top_k` | Rationale |
|----------|---------------------|-----------|
| Simple factual question | 3-5 | Few precise results keep context small. |
| Multi-facet question | 5-8 | Need coverage across sub-topics. |
| Comparison across collections | 8-12 per collection | Need enough evidence from each side. |
| Exhaustive research / due diligence | 15-20 | Comprehensive coverage at the cost of more context. |
| Quick validation of a claim | 2-3 | Just need to confirm or deny. |

### Managing context window size

- **Prefer targeted searches over global searches.** `search_collection()` returns fewer, more relevant results than `search()`.
- **Summarize as you go.** After retrieving results, extract the key facts before moving to the next query. Don't accumulate raw results.
- **Use multi-pass retrieval.** First pass: broad query with `top_k=5`. Read results. Second pass: specific follow-up queries targeting gaps.
- **Drop low-relevance results.** If a result has a low relevance score or doesn't relate to the question, ignore it.
- **Don't retrieve what you already know.** If a previous query already answered part of the question, don't re-query for it.

### When results are too large

If a single query returns more text than is useful:

1. Reduce `top_k` to 3.
2. Add `custom_tags` or `filters` to narrow scope.
3. Use a more specific query instead of a broad one.
4. Focus on the highest-scoring results and discard the rest.

### When results are insufficient

If a query returns no results or irrelevant results:

1. Broaden the query: remove specific terms, use synonyms.
2. Try global `search()` instead of collection-specific.
3. Check if the collection exists with `discover_collections()`.
4. Try a different collection if multiple are available.
5. If still empty, tell the user that no relevant data was found.

---

## Output Formatting Guidelines

### Standard response structure

```
**Answer**: <2-6 sentence direct answer>

**Evidence**:
- <claim> — *<collection_name> / <source_document>*
- <claim> — *<collection_name> / <source_document>*
- <claim> — *<collection_name> / <source_document>*

**Caveats**:
- <what is missing, uncertain, or conflicting>

**Suggested follow-ups** (if applicable):
- <exact query the user could ask next>
```

### Source citation rules

- Always cite the **collection name** and **source document** for every claim.
- Format: `— *Collection Name / document-name.md*`
- If multiple results support the same claim, cite the highest-scoring one.
- If results conflict, cite both and note the conflict.

### Confidence indicators

- **High confidence**: multiple results agree, high relevance scores (>0.85), from authoritative collections.
- **Medium confidence**: single result or moderate scores (0.6-0.85). Note: "Based on a single source."
- **Low confidence**: low scores (<0.6), tangential results, or inferred conclusions. Note: "This is inferred and may need verification."

### Comparison format

When comparing across collections, use a table:

```
| Aspect | Vendor A | Vendor B |
|--------|----------|----------|
| Uptime SLA | 99.9% | 99.95% |
| Penalty | 5% credit per hour | 10% credit per hour |
| Notice period | 30 days | 60 days |

*Sources: vendor_a_contract/sla.md, vendor_b_contract/sla.md*
```

---

## Failure Handling

| Failure | Agent action |
|---------|-------------|
| **No results** | Broaden wording, remove overly specific constraints, retry with `search()`. If still empty, inform user. |
| **Too many noisy results** | Constrain by collection, add `custom_tags`/`filters`, use narrower entity/date terms. |
| **Conflicting evidence** | Present both sides, note the conflict, cite both sources, and propose a follow-up query to resolve. |
| **Access denied (403)** | Explain that collection access may need to be purchased. Link to marketplace. |
| **Credit errors (402)** | Run `check_balance()`, report the balance, and link to billing page. |
| **Rate limited (429)** | Wait per `Retry-After` header or use exponential backoff. Max 3 retries. |
| **Server error (500/503)** | Retry once after 2-5 seconds. If it persists, inform user of a temporary issue. |
| **MCP connection failure** | Fall back to REST API endpoints. Inform user of the switch. |
| **Timeout** | Reduce `top_k`, simplify the query, and retry. |
| **Invalid collection slug** | Re-run `discover_collections()` and check available slugs. |

---

## Quality Bar

- Never fabricate unseen facts — all claims must come from retrieved evidence.
- Always ground claims in retrieved evidence with source citations.
- Prefer precise wording over broad generalization.
- Keep final responses concise, decision-oriented, and source-backed.
- Distinguish between directly stated facts and inferred conclusions.
- When evidence is incomplete, explicitly state what is missing rather than guessing.
- If a question cannot be answered from available collections, say so directly.
