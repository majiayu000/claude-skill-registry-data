---
name: internet-search
description: "Web research with structured APIs and source hierarchy. Use for documentation lookup and technical answers."
context: fork
globs: ["**/*.md"]
alwaysApply: false
---

# Internet Search Skill

## When to Use

Use this skill when:
- Looking up library documentation, API references, or framework best practices
- Finding answers to technical problems (Stack Overflow, GitHub Issues, forums)
- Checking community consensus on architectural or tooling decisions
- Searching for scientific papers or technical literature
- Finding GitHub repos, issues, PRs, or community solutions
- Checking the latest version or changelog of a dependency
- Validating an approach against external real-world references
- Fetching real-world data (LULC product specs, sensor band definitions, etc.)

---

## 1. Tool: `web/fetch`

VS Code agents use `web/fetch` to retrieve web pages. It returns content as plain text (HTML stripped or Markdown).

```
web/fetch(url)    → returns page text
```

**Always prefer structured APIs** (JSON/XML responses) over raw HTML scraping — faster, more reliable, no parsing fragility.

**When you must fetch raw HTML** (forums, blog posts): extract only the relevant section, ignore navigation and ads.

### Jina Reader — free URL-to-Markdown converter (no API key required)

Prefix any URL with `https://r.jina.ai/` to get back clean, LLM-readable Markdown — no HTML parsing, no ads, no navigation noise. Works on any public page.

```
# Convert any URL to clean markdown
https://r.jina.ai/{FULL_URL}

# Examples:
https://r.jina.ai/https://docs.sqlalchemy.org/en/20/orm/session_basics.html
https://r.jina.ai/https://stackoverflow.com/questions/12345678/
https://r.jina.ai/https://fastapi.tiangolo.com/tutorial/dependencies/
```

> Use Jina Reader whenever a direct `web/fetch` on a page returns messy HTML. It is completely free, requires no key, and is ideal for documentation pages, blog posts, and forum threads.

---

## 2. Source Trust Hierarchy

Always escalate from the highest trust tier before falling back:

| Tier | Sources | Use for |
|------|---------|---------|
| **Tier 1 — Authoritative** | Official vendor docs, RFC/specs, peer-reviewed papers, GitHub repo READMEs | Definitive answers, API contracts, algorithm correctness |
| **Tier 2 — High-signal community** | Stack Overflow (accepted/high-vote answers), GitHub Issues/Discussions, official changelogs, MDN | Real-world implementation patterns, known bugs, version-specific behaviours |
| **Tier 3 — Useful but verify** | Hacker News, Reddit (engineering subreddits), Dev.to, well-cited blog posts (e.g. Martin Fowler, Netlify blog, AWS blog) | Current opinions, ecosystem trends, practical tips |
| **Tier 4 — Last resort** | General blog posts, tutorials, Medium articles | Background context only — always cross-check with Tier 1/2 |

> **Rule**: Never cite Tier 3/4 as the sole source for a technical decision. Always pair with a Tier 1 primary source.

---

## 3. Search Strategies by Category

### 3.1 General Web — Structured APIs

No Google/Bing API in VS Code agents. Use these reliable structured alternatives:

```yaml
# DuckDuckGo Instant Answers — fast text summaries, entity cards
ddg_instant:  "https://api.duckduckgo.com/?q={QUERY}&format=json&no_html=1&skip_disambig=1"

# Wikipedia — encyclopaedic summaries and definitions
wikipedia:    "https://en.wikipedia.org/api/rest_v1/page/summary/{TOPIC}"

# Wikipedia full search (returns list of matching articles)
wikipedia_search: "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={QUERY}&format=json&srlimit=5"

# Wikidata — structured facts (entity properties, identifiers)
wikidata:     "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={QUERY}&language=en&format=json"
```

### 3.2 Technology Q&A — Tier 2 Sources

**Stack Overflow** (most reliable for programming questions):

```yaml
# Search questions — sorted by votes, accepted answers only
so_search:    "https://api.stackexchange.com/2.3/search/advanced?q={QUERY}&site=stackoverflow&order=desc&sort=votes&accepted=True&pagesize=5"

# Get answers for a specific question ID
so_answers:   "https://api.stackexchange.com/2.3/questions/{ID}/answers?site=stackoverflow&order=desc&sort=votes&filter=withbody"

# Search across all Stack Exchange sites (ServerFault, SuperUser, etc.)
se_all:       "https://api.stackexchange.com/2.3/search/advanced?q={QUERY}&order=desc&sort=votes&site={SITE}"
```

> Available `{SITE}` values: `stackoverflow`, `serverfault`, `superuser`, `askubuntu`, `unix`, `datascience`, `gis`, `stats`

**Example — find top voted accepted answers on FastAPI async SQLAlchemy:**
```
web/fetch("https://api.stackexchange.com/2.3/search/advanced?q=FastAPI+async+SQLAlchemy+session&site=stackoverflow&order=desc&sort=votes&accepted=True&pagesize=5")
```

**GitHub Issues and Discussions** (authoritative for library bugs/patterns):

```yaml
github_issues: "https://api.github.com/search/issues?q={QUERY}+repo:{OWNER}/{REPO}+is:issue&sort=reactions&order=desc"
github_discussions: "https://api.github.com/search/discussions?q={QUERY}+repo:{OWNER}/{REPO}"
github_issues_open: "https://api.github.com/search/issues?q={QUERY}+state:open+label:bug&sort=reactions"
```

### 3.3 Tech Community & News — Tier 3 Sources

**Hacker News** (Algolia API — fast, reliable):

```yaml
# Search stories and comments
hn_search:    "https://hn.algolia.com/api/v1/search?query={QUERY}&tags=story&hitsPerPage=10"

# Search only Ask HN / Show HN posts
hn_ask:       "https://hn.algolia.com/api/v1/search?query={QUERY}&tags=ask_hn&hitsPerPage=5"

# Filter by date (recent posts only)
hn_recent:    "https://hn.algolia.com/api/v1/search_by_date?query={QUERY}&tags=story&hitsPerPage=10&numericFilters=created_at_i>1700000000"
```

**Dev.to** (practitioner articles, open source community):

```yaml
devto_search: "https://dev.to/api/articles?tag={TAG}&per_page=10&top=1"
devto_query:  "https://dev.to/search?q={QUERY}"
```

> Good tags: `python`, `fastapi`, `react`, `typescript`, `docker`, `postgresql`, `machinelearning`, `webdev`, `opensource`

**Reddit** (subreddit-scoped, useful for community picks and comparisons):

```yaml
# Search within a specific subreddit — returns JSON
reddit_sub:   "https://www.reddit.com/r/{SUBREDDIT}/search.json?q={QUERY}&restrict_sr=1&sort=top&t=year&limit=10"

# Cross-subreddit search
reddit_all:   "https://www.reddit.com/search.json?q={QUERY}&sort=top&t=year&limit=10"
```

> High-signal subreddits by domain:
>
> | Domain | Subreddit |
> |--------|-----------|
> | Python | `r/Python`, `r/learnpython` |
> | Web Dev | `r/webdev`, `r/reactjs`, `r/node` |
> | DevOps / Docker | `r/devops`, `r/docker` |
> | Machine Learning | `r/MachineLearning`, `r/learnmachinelearning` |
> | Data Science | `r/datascience`, `r/statistics` |
> | Remote Sensing / GIS | `r/gis`, `r/remotesensing` |
> | Databases | `r/PostgreSQL`, `r/SQL` |
> | Open Source | `r/opensource`, `r/programming` |

### 3.4 Official Vendor Documentation — Tier 1 Sources

**Always fetch official docs before any community source:**

```yaml
# Web platform (MDN — most authoritative for browser APIs, JS, CSS, HTML)
mdn_search:     "https://developer.mozilla.org/api/v1/search?q={QUERY}&locale=en-US"
mdn_page:       "https://developer.mozilla.org/en-US/docs/Web/{PATH}"

# Python standard library
python_docs:    "https://docs.python.org/3/library/{MODULE}.html"
python_search:  "https://docs.python.org/3/search.html?q={QUERY}"

# FastAPI
fastapi:        "https://fastapi.tiangolo.com/{PATH}"

# SQLAlchemy
sqlalchemy:     "https://docs.sqlalchemy.org/en/20/{PATH}"

# React
react_docs:     "https://react.dev/reference/react/{API}"

# TypeScript
typescript:     "https://www.typescriptlang.org/docs/handbook/{PATH}"

# Docker
docker_docs:    "https://docs.docker.com/reference/{PATH}"

# GitHub Actions
gha_docs:       "https://docs.github.com/en/actions/{PATH}"

# Traefik
traefik_docs:   "https://doc.traefik.io/traefik/{PATH}"
```

### 3.5 Package Registries & Changelogs

```yaml
# PyPI — version, dependencies, homepage, release date
pypi:           "https://pypi.org/pypi/{PACKAGE}/json"
pypi_releases:  "https://pypi.org/pypi/{PACKAGE}/json"   # releases key in response

# npm
npm:            "https://registry.npmjs.org/{PACKAGE}"
npm_latest:     "https://registry.npmjs.org/{PACKAGE}/latest"

# Conda (conda-forge)
conda:          "https://api.anaconda.org/package/conda-forge/{PACKAGE}"

# crates.io (Rust, if needed)
crates:         "https://crates.io/api/v1/crates/{CRATE}"
```

### 3.6 GitHub — Code, Repos, Issues

```yaml
# Search repositories
github_repos:   "https://api.github.com/search/repositories?q={QUERY}&sort=stars&order=desc&per_page=5"

# Search code (find implementations in the wild)
github_code:    "https://api.github.com/search/code?q={QUERY}+language:python&per_page=5"

# Search issues (bugs, questions, workarounds)
github_issues:  "https://api.github.com/search/issues?q={QUERY}&sort=reactions&order=desc&per_page=5"

# Get README
github_readme:  "https://raw.githubusercontent.com/{OWNER}/{REPO}/main/README.md"

# Get specific file
github_file:    "https://raw.githubusercontent.com/{OWNER}/{REPO}/main/{PATH}"

# List releases / changelog
github_releases: "https://api.github.com/repos/{OWNER}/{REPO}/releases?per_page=5"
```

### 3.7 Academic / Scientific Literature

```yaml
# Semantic Scholar — papers, abstracts, citations (no key required)
s2_search:      "https://api.semanticscholar.org/graph/v1/paper/search?query={TERM}&fields=title,authors,year,abstract,citationCount,openAccessPdf&limit=10"
s2_paper:       "https://api.semanticscholar.org/graph/v1/paper/{PAPER_ID}?fields=title,authors,year,abstract,references"

# CrossRef — DOI resolution, journal/date filters
crossref:       "https://api.crossref.org/works?query={TERM}&filter=type:journal-article,from-pub-date:2020&rows=10&sort=relevance&mailto=researcher@example.com"

# arXiv — preprints (cs.*, eess.*, physics.*, q-bio.*)
arxiv:          "https://export.arxiv.org/api/query?search_query=all:{TERM}&start=0&max_results=10&sortBy=relevance"

# EarthArXiv — geoscience and remote sensing preprints
eartharxiv:     "https://eartharxiv.org/repository/search/?q={TERM}"

# MDPI Remote Sensing (open access, peer-reviewed)
mdpi_rs:        "https://www.mdpi.com/search?q={TERM}&journal=remotesensing&article_type=research-article"

# MDPI broad search
mdpi:           "https://www.mdpi.com/search?q={TERM}&article_type=research-article"

# PubMed (biology, environment, health)
pubmed:         "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={TERM}&retmax=10&retmode=json"
```

**Example — fetch top papers with citation count:**
```
web/fetch("https://api.semanticscholar.org/graph/v1/paper/search?query=change+detection+SAR+deep+learning&fields=title,authors,year,abstract,citationCount,openAccessPdf&limit=5")
```

### 3.8 Remote Sensing & Geospatial Sources

```yaml
# Google Earth Engine dataset catalog
gee_catalog:    "https://developers.google.com/earth-engine/datasets/catalog/{DATASET_ID}"

# STAC — spatiotemporal asset catalog
stac_planetary: "https://planetarycomputer.microsoft.com/api/stac/v1/search"
stac_element84: "https://earth-search.aws.element84.com/v1/collections"

# USGS Landsat
usgs_landsat:   "https://www.usgs.gov/landsat-missions/landsat-collection-2"

# Copernicus / ESA Sentinel
sentinel_docs:  "https://sentinel.esa.int/web/sentinel/technical-guides"

# MapBiomas
mapbiomas:      "https://mapbiomas.org/en/colecoes-mapbiomas-1"

# OpenStreetMap Nominatim (geocoding)
nominatim:      "https://nominatim.openstreetmap.org/search?q={QUERY}&format=json&limit=5"
```

---

## 4. Site-Scoped Search (when you know the target site)

When you know the domain but not the exact URL, use DuckDuckGo with `site:` operator embedded in the query:

```yaml
# Site-scoped via DuckDuckGo instant answers
ddg_site: "https://api.duckduckgo.com/?q=site:{DOMAIN}+{QUERY}&format=json&no_html=1"

# Examples:
"https://api.duckduckgo.com/?q=site:stackoverflow.com+FastAPI+async+context+manager&format=json&no_html=1"
"https://api.duckduckgo.com/?q=site:docs.python.org+asyncio+gather&format=json&no_html=1"
"https://api.duckduckgo.com/?q=site:github.com+rasterio+issue+band+count&format=json&no_html=1"
```

**Useful `site:` targets:**

| Target | Domain |
|--------|--------|
| Stack Overflow | `stackoverflow.com` |
| Python docs | `docs.python.org` |
| MDN | `developer.mozilla.org` |
| FastAPI docs | `fastapi.tiangolo.com` |
| SQLAlchemy docs | `docs.sqlalchemy.org` |
| GitHub Issues | `github.com` |
| Docker docs | `docs.docker.com` |
| AWS docs | `docs.aws.amazon.com` |
| Traefik docs | `doc.traefik.io` |
| Read the Docs | `readthedocs.io` |

---

## 5. Query Construction Best Practices

### 5.1 Be Specific

```
❌ Too broad:  "machine learning remote sensing"
✅ Specific:   "U-Net semantic segmentation Sentinel-2 deforestation 2022"

❌ Too broad:  "Python async"
✅ Specific:   "FastAPI background tasks SQLAlchemy async session 2024"

❌ Too broad:  "Docker error"
✅ Specific:   "Docker multi-stage build COPY --from permission denied non-root"
```

### 5.2 Boolean & Filter Operators

```
# Stack Overflow — keyword combinations
"FastAPI" AND "async" AND "SQLAlchemy" AND "session"

# GitHub Issues — filters
is:issue is:closed label:bug "NoneType" "async_session"

# CrossRef — date + type filter
&filter=type:journal-article,from-pub-date:2021

# arXiv — category filter  
search_query=cat:eess.IV+AND+all:sentinel+deforestation

# GitHub code — language filter
{QUERY}+language:python+extension:py
```

### 5.3 URL Encoding

Always encode spaces and special characters:

```python
import urllib.parse
query = urllib.parse.quote("change detection SAR backscatter temporal")
url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5"
```

---

## 6. Parallel Search Strategy

For any non-trivial research question, launch sources in parallel grouped by trust tier:

```
STEP 1 — PARALLEL (Tier 1 primary sources):
  ├── web/fetch(official docs)
  ├── web/fetch(PyPI or GitHub README)
  └── web/fetch(Semantic Scholar — if academic topic)

STEP 2 — PARALLEL (Tier 2 community sources):
  ├── web/fetch(Stack Overflow — top voted accepted answer)
  ├── web/fetch(GitHub Issues — known bugs on this topic)
  └── web/fetch(arXiv or CrossRef — alternate paper source)

STEP 3 — ONLY IF NEEDED (Tier 3):
  ├── web/fetch(Hacker News — community discussion)
  └── web/fetch(Reddit — engineering subreddit)

→ Synthesise after each step; stop when enough evidence gathered
→ Never cite Tier 3 as sole source for a technical decision
```

---

## 7. Result Synthesis Template

After fetching, always return structured findings:

```markdown
## Research Findings: {TOPIC}

### Summary
[2–3 sentence answer to the question based on findings]

### Key Papers / Specs
| Title | Source | Year | Trust | Key Point |
|-------|--------|------|-------|-----------|
| [Paper Title](url) | Semantic Scholar | 2023 | Tier 1 | ... |

### Community Evidence
| Source | Votes/Stars | Finding |
|--------|-------------|---------|
| [SO answer](url) | 342 votes ✓ accepted | Use `asyncio.gather` instead of `create_task` here |
| [GH issue #123](url) | 87 👍 | Fixed in v2.1.0 — upgrade required |

### Reference Implementations
| Repo | Stars | Relevant file |
|------|-------|---------------|
| [owner/repo](url) | 1.2k | `src/service.py` — async session pattern |

### Official Docs
- [Library Name — relevant section](url): key quote or note

### Recommendation
**Answer**: [Direct answer]
**Confidence**: High / Medium / Low  
**Caveat**: [Any version-specific or context-specific warnings]
**Sources**: [List citations with tier]
```

---

## 8. Source Quality Checklist

Before citing a source, verify:

- [ ] **Recency**: is the information still valid? Check date. Flag anything >3 years old in fast-moving fields (JS/TS, LLMs, cloud infra).
- [ ] **Votes / citations**: SO answers with <5 votes or papers with <10 citations are weak signal — note it.
- [ ] **Version alignment**: does the answer target the same version as the project? A SQLAlchemy 1.4 answer may not apply to SQLAlchemy 2.0.
- [ ] **Accepted/merged**: for GitHub issues, check if it's resolved. For SO, prefer accepted answers.
- [ ] **Open access**: for academic papers, prefer `openAccessPdf` in Semantic Scholar or arXiv preprint. Avoid citing paywalled abstracts as evidence.
- [ ] **Primary over secondary**: prefer the library's own docs over any tutorial or blog that re-explains them.
- [ ] **No hallucinated URLs**: only use URLs from actual fetch results or from the known stable patterns in this skill.

---

## 9. Rate Limits & Etiquette

| API | Limit | Notes |
|-----|-------|-------|
| **Jina Reader** (`r.jina.ai`) | No hard limit | Converts any URL to clean Markdown; no key needed |
| Semantic Scholar | 100 req/5 min | Pass `x-api-key` header for higher dedicated limit |
| CrossRef | ~50 req/s | Use `mailto=` param for polite pool (faster queue) |
| arXiv | ~3 req/s | Add 1s delay between batched calls |
| GitHub (unauthenticated) | 10 search req/min · 60 req/hr | Optionally pass `Authorization: token {TOKEN}` for 30 search req/min |
| Stack Exchange (unauthenticated) | 300 req/day | Free app key at stackapps.com raises limit to 10,000/day |
| DuckDuckGo Instant Answers | No official limit | Respectful crawl rate |
| Wikipedia / Wikidata | No hard limit | Add `User-Agent` header with contact info |
| Reddit | 10 req/min | Use `User-Agent: MyApp/1.0` header |
| Hacker News (Algolia) | No hard limit | Very permissive |
| PyPI / npm / conda | No hard limit | Very permissive |
| PubMed (NCBI) | 3 req/s | Free API key at NCBI raises limit to 10 req/s |

```yaml
# CrossRef polite pool — faster, prioritised queue
"https://api.crossref.org/works?query={TERM}&mailto=researcher@example.com"

# GitHub optional auth header (higher limits)
headers: { "Authorization": "token {GITHUB_TOKEN}" }

# Stack Exchange free app key (10k/day)
"https://api.stackexchange.com/2.3/search/advanced?q={QUERY}&site=stackoverflow&key={APP_KEY}"

## MCP Search Server Integration

### Why MCP for Search
MCP search servers provide AI-augmented, structured search results that are cleaner than raw web scraping. They understand the context of queries and return structured, relevant results.

### Available MCP Search Servers

| MCP Server | Source | Strengths | Use Case |
|------------|--------|-----------|----------|
| Brave Search | `@anthropic/brave-search` | Web + news + images, freshness | General web search, current events |
| Tavily | `tavily-mcp` | AI-optimized, ad-free | Developer research, technical queries |
| Exa | `exa-mcp` | Neural search, embeddings | Semantic search, academic papers |
| Perplexity | `perplexity-mcp` | Answer generation + citations | Complex research questions |

### Integration Pattern

```python
# MCP search tool registration
search_tools = await discover_mcp_tools(servers=[
    "brave-search",
    "tavily-mcp",
    "perplexity-mcp"
])

# Multi-provider search strategy
async def parallel_search(query: str) -> SearchResults:
    """Search across multiple MCP providers in parallel."""
    results = await asyncio.gather(
        brave_search(query),
        tavily_search(query), 
        perplexity_search(query),
        return_exceptions=True
    )
    return aggregate_and_deduplicate(results)
```

### Query Construction for MCP
- MCP search servers benefit from structured queries with context
- Include domain filters, date ranges, and result counts
- MCP tools return structured JSON (not raw HTML) — no parsing needed
```
