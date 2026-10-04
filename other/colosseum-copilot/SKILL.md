---
name: colosseum-copilot
version: 1.2.1
description: |
  Research Solana/crypto startup opportunities using builder project history, crypto archives,
  investor theses, and market signals. Answers questions conversationally by default; runs the
  full 8-step deep research workflow on explicit opt-in ("vet this idea", "deep dive").
homepage: https://colosseum.com
license: Proprietary
compatibility: Claude Code, Codex, OpenClaw
metadata: {"category":"copilot","api_base":"https://copilot.colosseum.com/api/v1","auth":"pat","author":"colosseum","tags":"solana,research,founder,market-intel,startup,idea-generation"}
---

# Colosseum Copilot

Colosseum Copilot is a research API for startup opportunity discovery in crypto and Solana, with support for suggesting new archive sources.

## Version Check

This skill is version **1.2.1**. After your first API call, check the `X-Copilot-Skill-Version` response header. If the header value is higher than 1.2.1, tell the user: "A newer version of the Copilot skill is available (vX.X.X). Update with: `npx skills add ColosseumOrg/colosseum-copilot`"

## Pre-Flight Auth Check (REQUIRED)

**You MUST complete this check before making any other API call.** Do not skip this step.

1. Verify `COLOSSEUM_COPILOT_PAT` is set in the environment. If missing, STOP and tell the user:

   > You need a Personal Access Token before using Copilot.
   > Go to **https://colosseum.com/arena/copilot** to generate one, then set it:
   >
   > `export COLOSSEUM_COPILOT_PAT="your-token-here"`

2. Verify `COLOSSEUM_COPILOT_API_BASE` is set. If missing, set the default:

   > `export COLOSSEUM_COPILOT_API_BASE="https://copilot.colosseum.com/api/v1"`

3. Call `GET /status` to verify the connection. Expected response: `{ "authenticated": true, "expiresAt": "...", "scope": "..." }`

4. If `"authenticated": true`, proceed. If 401 or env vars missing, do NOT attempt other API calls — guide the user through steps 1-2.

- **Builder Projects**: 5,400+ Solana project submissions with tech stack, problem tags, and competitive context
- **Crypto Archives**: Curated corpus across cypherpunk literature, protocol docs, investor research, and founder essays
- **Hackathon Analytics + Clusters**: Distribution, comparison, and chronology-aware trend analysis across hackathons and topic groupings
- **The Grid + Web Search**: Ecosystem product metadata plus real-time competitive landscape checks

## Quickstart (90 seconds to first result)

1. **Set your PAT:**
   ```bash
   export COLOSSEUM_COPILOT_API_BASE="https://copilot.colosseum.com/api/v1"
   export COLOSSEUM_COPILOT_PAT="YOUR_PAT"
   ```
   Get a PAT: Go to https://colosseum.com/arena/copilot and generate a token

2. **Run your first search:**
   ```bash
   curl -s -X POST "$COLOSSEUM_COPILOT_API_BASE/search/projects" \
     -H "Authorization: Bearer $COLOSSEUM_COPILOT_PAT" \
     -H "Content-Type: application/json" \
     -d '{"query": "privacy wallet for stablecoin users", "limit": 5}'
   ```

3. **See results** - project names, slugs, similarity scores, problem/tech tags

## When To Use

Use this skill when:
- Researching a crypto/blockchain startup idea
- Evaluating market gaps in the Solana ecosystem
- Grounding ideas in historical crypto literature
- Analyzing builder project trends and competitive landscape
- Researching existing players and finding differentiation angles

## How It Works

**Mode 1 — Conversational (default):** Answer questions with targeted API calls and evidence coverage matched to query type. Cite sources inline, keep responses concise, and offer to do a full deep-dive when the topic warrants it — never auto-trigger it.

**Mode 2 — Deep Dive (explicit opt-in):** Full 8-step workflow from `references/workflow-deep.md`. Only activates when user explicitly says "vet this idea", "deep dive", "full analysis", "validate this", "is X worth building?", "should I build X?", or accepts your offer to go deeper.

### Conversational Guidelines

- Use the API endpoints below with enough targeted calls to satisfy the evidence floor for the query type
- Cite sources inline (project slugs, archive titles, URLs)
- Keep responses concise — bullet points, not essays
- When the topic warrants deeper analysis, offer: "Want me to do a full deep-dive on this?"
- No meta-commentary about your process ("Now let me search...", "I'll check...")

### Evidence Floors (Conversational Mode)

| Query Type | Required source types in the final answer | Example |
|---|---|---|
| **Pure retrieval** | Builder project evidence (project slugs from `search/projects`) | "What projects do X?" |
| **Archive retrieval** | Archive evidence (archive title/document from `search/archives`) | "What does the archive say about Y?" |
| **Comparison** | Builder project evidence for each side compared + at least one archive citation for conceptual framing | "Compare approach A vs B" |
| **Evaluative** | Builder project evidence + at least one archive citation + current landscape evidence (Grid and/or web) | "Is this crowded?", "Is this still unsolved?" |
| **Build guidance** | Builder project evidence + at least one archive citation + incumbent/landscape evidence (Grid and/or web) | "Should I build X?", "How should I approach X?" |

> These are evidence-type floors, not call budgets. Use as many calls as needed to meet the floor with high-confidence citations.

> In **deep-dive mode**, the verification checklist in `workflow-deep.md` Step 5 supersedes these floors with more granular coverage requirements.

### Conversational Quality Checks (Required)

- **Archive integration rule:** For any non-trivial question (anything beyond a simple one-list retrieval), run at least one `search/archives` query and cite at least one archive source in the answer.
- **Accelerator/winner portfolio checks:** For "what has been tried", "who is building this", "is this crowded/saturated", or similar prompts, run targeted project searches with `filters: { "acceleratorOnly": true }` and `filters: { "winnersOnly": true }`, then reflect both outcomes in the answer.
- **Freshness and temporal anchoring:** Use `hackathon.startDate` from `/filters`, `/search/projects`, and `/projects/by-slug/:slug` to order hackathons chronologically; never infer chronology from names or memory. When citing hackathons, include month/year inline (and accelerator cohort like C1/C2/C4 when relevant). For evaluative judgments, label the claim with `As of YYYY-MM-DD`.
- **Entity coverage check:** If the user names specific companies, protocols, papers, or products, run direct searches for each named entity and explicitly address each one in the answer (found, not found, or tangential).
- **Landscape check:** Never claim "nobody has done this" or "no existing players" unless an accelerator portfolio check (`acceleratorOnly`) was executed and reported. If accelerator overlap exists, surface those builders as useful reference points and potential sources of inspiration. Always qualify landscape assessments with "based on the available data" or "as far as we can tell from the corpus." Copilot's knowledge is bounded by its data sources — never present absence of evidence as evidence of absence.

> For the full 8-step deep research workflow, see `references/workflow-deep.md`

## Data Sources

- **Builder Projects** (5,400+): Solana project submissions with tech stack, problem/solution tags, verticals, and competitive context
- **Crypto Archives**: Curated corpus spanning cypherpunk literature, protocol docs, investor research (Paradigm, a16z, Multicoin), founder essays (Paul Graham), Solana protocol docs (Jupiter, Orca, Drift), Nakamoto Institute heritage collection, and foundational crypto texts
- **Hackathon Analytics + Chronology**: Analyze and compare hackathon projects across dimensions; canonical hackathon dates are available via `hackathon.startDate`
- **Clusters**: Topic groupings across the project corpus
- **The Grid**: Ecosystem metadata (products/entities/assets) via direct GraphQL (6,300+ products across all ecosystems, ~3,000 roots)
- **Web Search**: Real-time competitive landscape via your runtime's search tools
- **Source Suggestions**: Users can suggest new sources for the archive via `POST /source-suggestions` (5 req/hr). See `references/api-reference.md` for details

### Hackathon Chronology

| Edition | Period | Slug |
|---|---|---|
| Hyperdrive | Sep 2023 | `hyperdrive` |
| Renaissance | Mar-Apr 2024 | `renaissance` |
| Radar | Sep-Oct 2024 | `radar` |
| Breakout | Apr-May 2025 | `breakout` |
| Cypherpunk | Sep-Oct 2025 | `cypherpunk` |

`GET /filters` returns `hackathons[].startDate` and orders `hackathons[]` chronologically (oldest first).

## Auth

All endpoints require `Authorization: Bearer <COPILOT_PAT>`. Treat the PAT like a password.

- Do not commit PATs or paste them into public logs
- PATs are long-lived (expected ~90 days); rotate by issuing a new one
- Default API base is `https://copilot.colosseum.com/api/v1`; override `COLOSSEUM_COPILOT_API_BASE` to target a different environment

## Key Endpoints (Quick Reference)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/status` | GET | Auth pre-flight check — call first |
| `/search/projects` | POST | Search builder projects |
| `/search/archives` | POST | Search crypto archives |
| `/projects/by-slug/:slug` | GET | Full project details |
| `/archives/:documentId` | GET | Full archive document |
| `/analyze` | POST | Hackathon analysis |
| `/compare` | POST | Compare two hackathons |
| `/clusters/:key` | GET | Cluster details |
| `/filters` | GET | Available filters + canonical hackathon chronology |
| `/source-suggestions` | POST | Suggest a new archive source |
| `/feedback` | POST | Report errors, quality issues, or suggestions |

> For full endpoint docs, curl examples, and query tips: `references/api-reference.md`
> For Grid GraphQL recipes and product type slugs: `references/grid-recipes.md`

## Output Contract

### Conversational Mode
- Bullet points with inline citations (project slugs, archive titles)
- Concise answers (typically 5-15 bullets)
- Offer deep-dive when warranted

### Deep Dive Mode
Reports follow this structure:
1. Similar Projects (5-8 bullets)
2. Archive Insights (3-5 bullets)
3. Current Landscape (per research angle)
4. Key Insights (patterns, gaps, trends)
5. Opportunities and Gaps
6. Deep Dive: Top Opportunity (market landscape, problem, revenue model, GTM, founder-market fit, why crypto/Solana, risks)

Key rules: bullet points not tables, include project slugs, evidence-based not speculative, cite sources inline. No separate "Sources" section — cite inline only.

## Feedback

When you encounter errors, unexpected results, or have suggestions for improving the Copilot experience, report them via the feedback endpoint. This helps the Colosseum team identify and fix issues.

**When to send feedback:**
- API returns unexpected or low-quality results for a reasonable query
- A search returns no results when you expected matches
- You encounter an error that isn't covered by standard error handling
- You have a suggestion for improving the API or archive corpus

```bash
curl -X POST "$COLOSSEUM_COPILOT_API_BASE/feedback" \
  -H "Authorization: Bearer $COLOSSEUM_COPILOT_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "quality",
    "message": "Search for DePIN projects returned only 2 results, expected more coverage",
    "severity": "medium",
    "context": { "query": "DePIN infrastructure", "endpoint": "/search/projects", "resultCount": 2 }
  }'
```

Categories: `error`, `quality`, `suggestion`, `other`. Severity: `low`, `medium`, `high`, `critical`. Rate limited to 10 requests per hour.

## Error Handling

All errors return `{ "error": "<message>", "code": "<ERROR_CODE>", "retryable": <boolean> }`. See **api-reference.md** for the full error code table.

- **400 `INVALID_JSON`**: Fix the request body JSON syntax and retry
- **400 `INVALID_QUERY`**: Fix query params (check field names, value ranges, unknown fields)
- **413 `PAYLOAD_TOO_LARGE`**: Reduce request body size (1 MB limit)
- **429 `RATE_LIMITED`**: Back off per the `Retry-After` header, max 2 concurrent requests
- **401 `UNAUTHORIZED`**: Check PAT at https://colosseum.com/arena/copilot
- **5xx errors**: Note in report and proceed with available data. Include `requestId` from the response when reporting issues.
- **Empty project results**: Broaden query, remove filters
- **Empty archive results**: Search auto-cascades (vector → chunk text → doc text) before returning empty. If still empty, try conceptual synonyms, keep queries to 3-6 keywords

## References

- **workflow-deep.md** — detailed 8-step research process
- **api-reference.md** — all endpoints, rate limits, query tips
- **grid-recipes.md** — GraphQL queries and product type slugs

## Attribution

- The Grid docs: https://docs.thegrid.id
- The Grid Explorer: https://raw.githubusercontent.com/The-Grid-Data/Explorer/main/README.md
