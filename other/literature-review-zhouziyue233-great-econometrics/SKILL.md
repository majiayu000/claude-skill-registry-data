---
name: literature-review
description: Search, summarize, and synthesize economics literature. find research gaps, position your contribution.
---

# Literature-Review

## Purpose

This skill helps economists conduct rigorous literature reviews: actively searching academic databases, building reference list, summarizing individual papers, synthesizing views and evidence across the literature, identifying research gaps, and positioning the user's contribution.

## When to Use

- Finish phase 1 of the workflow (Research Question Scoping) and handoff to phase 2
- Start a literature review for a new project
- Draft the Related Literature section of a paper
- Find prior work to cite in an introduction
- Respond to a referee's request to engage more with the literature

---

## Step 0: OpenAlex API Key Setup

**Before starting any search, Claude must run this check every time the skill is invoked.**

### 0.1 Read the Config File

Read the file `[plugin_root]/.env`.

The file should contain:
```
OPENALEX_API_KEY=your-api-key-here
```

### 0.2 Decision Tree

**If the key is absent / still a placeholder:**

Use AskUserQuestion to prompt the user:

> *"请按以下步骤获取 OpenAlex API Key，然后粘贴到这里：*
> *① 访问 [https://openalex.org/settings/api](https://openalex.org/settings/api) → 注册 / 登录账号*
> *② 在账户设置页面生成 API Key → Copy*
> *③ 将 API Key 粘贴至此"*

- **If the user provides a key:** Append `OPENALEX_API_KEY=<value>` to `[plugin_root]/.env` (standard `KEY=VALUE` format, one entry per line — **not JSON**). If the key already exists in the file, replace that line in place. Confirm: *"✅ API Key 已保存，下次不再询问。"* Then proceed.
- **If the user skips:** Warn — *"⚠️ 未配置 API Key，OpenAlex 请求将受到严格限速，文献检索结果可能不完整。"* — then continue (omit `&api_key=...` from all URLs).

**If the key is already a valid non-placeholder string:** proceed silently — no prompt needed.

---

## Step 1: Confirm the Research Question

This skill is **Phase 2** of the empirical research workflow. The confirmed research question from Phase 1 is the essential input. Claude must follow this decision tree:

### 1.1 Check for a Confirmed Research Question

Scan your working directory to find the research-question.md document produced by the `question` skill:

```
研究问题：…
研究对象：…
识别层级：Level [A/B/C]
数据来源（初步）：…
研究假设：H₀ / H₁ / 预期方向
```

Then ask **only the two supplementary questions**:

> *"文献搜索还需要以下信息：*
> *① 文献时间范围：全部年份 / 2000年后 / 最近十年？*
> *② 有没有 2–3 篇奠基性论文（作者 + 标题或 DOI）可作为搜索锚点？没有也可以直接跳过。"*

Once the user answers (or skips ②), proceed directly to **Step 2**.

### 1.2 Back to /question command

**If no research-question.md document is found** (user jumped directly to literature review without going through Phase 1):

Run the `/question` command immediately:

> *"在开展文献检索之前，需要先明确研究问题。我将运行 /question 命令帮助你完成这一步。"*

Run the full `/question` workflow. After the user confirms the research question, return to this skill at **Step 1.1** (the block will now be present) and continue.

---

## Step 2: Generate a Comprehensive Keyword Matrix

Before searching, expand the user's topic into a **full keyword matrix**. Do not rely on a single phrase.

### 2.1 Generate Three Layers × Multiple Synonyms

| Layer | Primary terms | Synonyms / variants |
|-------|--------------|---------------------|
| **Core concept** | e.g. "minimum wage" | "wage floor", "wage policy", "statutory wage" |
| **Outcome** | e.g. "employment" | "jobs", "labor demand", "hours worked", "unemployment" |
| **Method** | e.g. "difference-in-differences" | "DiD", "diff-in-diff", "natural experiment", "quasi-experiment" |
| **Context** | e.g. "United States" | "US", "OECD", "developing countries", "low-income countries" |

### 2.2 Generate JEL Code Candidates

Map the research question to **3–6 relevant JEL codes** (e.g., J31 = Wage Level and Structure; J23 = Labor Demand; C21 = Cross-Sectional Models). These could be used in EconLit and NBER searches.

### 2.3 Construct Boolean Query Variants

Generate **at least 5 distinct query strings** covering different angles:

```
Query 1 (main):      ("minimum wage" OR "wage floor") AND (employment OR "labor demand")
Query 2 (method):    ("minimum wage") AND ("difference-in-differences" OR "DiD" OR "natural experiment")
Query 3 (mechanism): ("minimum wage") AND (prices OR "profit margins" OR "labor productivity")
Query 4 (subgroup):  ("minimum wage") AND ("low-skilled" OR "teen employment" OR "small business")
Query 5 (recent):    ("minimum wage") AND (employment) after:2018
```

---

## Step 3: Execute Multi-Round Active Search

Claude must **actively execute these searches** autonomously.

Primary search engine: OpenAlex API via WebFetch.

Supplementary & optional sources: Semantic Scholar, NBER, SSRN and arXiv.

Search rules:

1. Use primary search engine for all rounds.
2. Use supplementary sources only for following purposes:
   - More Coverage: OpenAlex results are clearly thin or missing a literature branch
   - Cross-validation: Use Semantic Scholar to verify that key metadata (title, authors, year, citation count, DOI) returned by OpenAlex is accurate and not erroneous
   - Working paper capture: recent NBER / SSRN papers are likely relevant

3. Semantic Scholar cross-validation is **mandatory** for all Core-tier papers — even when OpenAlex coverage is strong.
4. For Background / Methodological papers, cross-validation may be skipped if OpenAlex data looks internally consistent.

### **OpenAlex API**

All OpenAlex requests follow the base URL `https://api.openalex.org`. Append `&api_key=YOUR_KEY` (from `.env`) to every request. Without a key, requests are very limited but still functional for moderate searches.

#### ⚠️ 网络受限处理规则（Cowork 沙箱 WebFetch 被封锁时）

**在发出第一个 OpenAlex WebFetch 请求后，若收到网络错误（连接超时、403、域名无法解析等），必须严格遵循以下顺序，禁止直接跳转到网络搜索兜底：**

**Step A — 立即生成本地运行脚本，并提示用户在自己的电脑上执行**

向用户说明：

> *"Cowork 沙箱无法访问 OpenAlex API（网络受限）。请在您的本地终端运行以下 Python 脚本获取文献数据，然后将输出结果粘贴到这里或保存为文件后上传。*
>
> **运行方式：**
> ```bash
> pip install requests
> python fetch_openalex.py
> ```"*

随后生成完整的本地脚本 `fetch_openalex.py`（写入工作区）：

```python
"""
OpenAlex 文献获取脚本 — 在本地终端运行
生成文件：openalex_results.json
"""
import requests, json, time

API_KEY = "YOUR_OPENALEX_API_KEY"   # 替换为你的 API Key（或留空）
BASE    = "https://api.openalex.org"
HEADERS = {"User-Agent": "mailto:your@email.com"}

def fetch(url):
    if API_KEY:
        url += f"&api_key={API_KEY}" if "?" in url else f"?api_key={API_KEY}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    time.sleep(0.5)   # 避免触发速率限制
    return r.json()

queries = [
    # ── 根据研究问题自动填充的查询（Claude 在生成脚本时替换占位符）──
    f"{BASE}/works?search=KEYWORD_1&filter=type:article&sort=cited_by_count:desc&per_page=25",
    f"{BASE}/works?search=KEYWORD_2&filter=type:article&sort=cited_by_count:desc&per_page=25",
    f"{BASE}/works?search=KEYWORD_3&filter=type:article,publication_year:>2018&sort=cited_by_count:desc&per_page=25",
]

results = {}
for i, url in enumerate(queries, 1):
    print(f"查询 {i}/{len(queries)}: {url[:80]}...")
    try:
        data = fetch(url)
        results[f"query_{i}"] = data.get("results", [])
        print(f"  → 获取 {len(results[f'query_{i}'])} 篇")
    except Exception as e:
        print(f"  ✗ 失败：{e}")
        results[f"query_{i}"] = []

with open("openalex_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n✅ 结果已保存至 openalex_results.json")
print(f"   总计获取：{sum(len(v) for v in results.values())} 篇文献条目")
```

> **脚本中的占位符 `KEYWORD_1/2/3` 由 Claude 在生成时替换为 Step 2 生成的实际关键词查询字符串。**

**Step B — 等待用户上传 / 粘贴结果**

等待用户执行后返回结果。接受以下任意格式：
- 上传 `openalex_results.json` 文件
- 粘贴 JSON 文本到对话中
- 粘贴终端输出的纯文本

收到数据后，正常解析并继续 Round 1 的候选文献筛选流程。

**Step C — 仅当用户明确表示无法在本地运行时，才启用兜底方案**

若用户回复"无法运行"或"没有 Python 环境"，**此时**才可使用以下兜底（按优先级）：

1. 通过 `WebSearch` 搜索 Google Scholar / 学术搜索（降级，覆盖度有限）
2. 提示用户在浏览器手动访问 `https://openalex.org/works?search=...` 并将页面内容粘贴

**⛔ 严禁行为：** 在未提示用户尝试本地运行之前，直接切换到网络搜索兜底。

**Important — Two-step author lookup:** Never filter by author *name* directly (names are ambiguous). Always first search for the author's OpenAlex ID, then filter works by that ID.

**Pattern 1 — Works keyword search**

```
https://api.openalex.org/works?search=minimum+wage+employment+difference-in-differences&filter=type:article&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY
```

Key `filter` modifiers (combine with comma = AND):
- `type:article` — journal articles only
- `publication_year:2015-2024` — year range
- `publication_year:>2018` — after a year
- `is_oa:true` — open access only
- `topics.id:T10325` — by OpenAlex topic ID
- `authorships.institutions.country_code:US` — by country

Key `sort` options:
- `cited_by_count:desc` — most cited first
- `publication_year:desc` — most recent first
- `relevance_score:desc` — best text match first (default when `search=` used)

**Pattern 2 — Author ID lookup (step 1 of 2)**

```
https://api.openalex.org/authors?search=David+Card&per_page=5&api_key=YOUR_KEY
```
Parse the response: pick the top result's `id` field (e.g., `https://openalex.org/A5023888391`). Extract the short ID: `A5023888391`.

**Pattern 3 — Works by a specific author (step 2 of 2)**

```
https://api.openalex.org/works?filter=authorships.author.id:A5023888391&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY
```

**Pattern 4 — Retrieve a single work by DOI or OpenAlex ID**

```
https://api.openalex.org/works/doi:10.2307/2118030?api_key=YOUR_KEY
https://api.openalex.org/works/W2170494700?api_key=YOUR_KEY
```

**Pattern 5 — Forward citations (papers that cite a given work)**

```
https://api.openalex.org/works?filter=cites:W2170494700&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY
```

**Pattern 6 — Backward references (papers cited by a given work)**

Retrieve the work directly (Pattern 4) and read its `referenced_works` array. Then batch-fetch metadata:
```
https://api.openalex.org/works?filter=openalex_id:W111|W222|W333&per_page=50&api_key=YOUR_KEY
```
(Use pipe `|` to OR up to 100 IDs in one request.)

**Pattern 7 — Search with Boolean operators**

```
https://api.openalex.org/works?search=(minimum+wage+OR+wage+floor)+AND+(employment+OR+labor+demand)&filter=type:article,publication_year:2000-2024&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY
```
Use `AND`, `OR`, `NOT` (uppercase).

---

### **Round 1: Broad Sweep (Target: 25+ candidate papers)**

#### Primay Source — OpenAlex API

Run **at least 4–5 distinct queries**. For each query variant:

1. **Keyword search** (Pattern 1) with `sort=cited_by_count:desc` → capture top 25 results
2. **Author lookup** (Patterns 2+3) for 2–3 key authors identified in results → capture their top works
3. **Combined filter** adding `publication_year:>2018` → capture recent papers

Example sequence:
```
# Query 1: Main search
https://api.openalex.org/works?search=minimum+wage+employment&filter=type:article&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY

# Query 2: Method-focused
https://api.openalex.org/works?search=minimum+wage+"difference-in-differences"&filter=type:article&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY

# Query 3: Mechanism
https://api.openalex.org/works?search=minimum+wage+price+pass-through+profit+mechanism&filter=type:article&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY

# Query 4: Recent papers
https://api.openalex.org/works?search=minimum+wage+employment&filter=type:article,publication_year:>2018&sort=cited_by_count:desc&per_page=25&api_key=YOUR_KEY

# Query 5: Author lookup → Card
https://api.openalex.org/authors?search=David+Card&per_page=3&api_key=YOUR_KEY
# → get author ID, then:
https://api.openalex.org/works?filter=authorships.author.id:AUTHOR_ID&sort=cited_by_count:desc&per_page=20&api_key=YOUR_KEY
```

#### Supplementary Sources

**Semantic Scholar (for more coverage + cross-validation of OpenAlex data)**

**API Key Check (one-time per session):**

Read `.env` and look for `SEMANTIC_SCHOLAR_API_KEY`.

- **If the key is absent or still a placeholder:** Use `AskUserQuestion` to prompt:

  > *"Semantic Scholar 可作为 OpenAlex 的补充来源（捕获遗漏文献或作交叉检验）。配置 API Key 可获得更高请求速率：*
  > *① 访问 [https://www.semanticscholar.org/product/api](https://www.semanticscholar.org/product/api)  → 申请 API Key (建议直接闲鱼搜索Semantic Scholar API 购买)*
  > *② 将 Key 粘贴至此；若暂无 Key，直接回车跳过（将使用公共接口，速率受限）。"*

  - If user provides key: append `SEMANTIC_SCHOLAR_API_KEY=<value>` to `.env` (standard `KEY=VALUE` format — **not JSON**; replace existing line if present). Set flag `SS_AUTH = True`. Confirm: *"✅ Semantic Scholar API Key 已保存。"*
  - If user skips: set flag `SS_AUTH = False`. Note: *"⚠️ 将使用 Semantic Scholar 公共接口，调用速率受限。"*

- **If a valid key already exists in `.env`:** Set `SS_AUTH = True`, proceed silently.

**Branch A — With API Key (`SS_AUTH = True`): use Python via Bash**

Authentication is via HTTP header `x-api-key`, which WebFetch cannot set. Use `requests` in a Bash script instead.

```python
import requests, json, time

SS_KEY = "YOUR_SEMANTIC_SCHOLAR_API_KEY"   # loaded from .env
headers = {"x-api-key": SS_KEY}
BASE    = "https://api.semanticscholar.org/graph/v1"
FIELDS  = "title,year,authors,abstract,citationCount,externalIds,openAccessPdf,venue,publicationTypes"

# --- Task 1: Keyword search (cross-validation & coverage) ---
params = {
    "query":  "minimum wage employment difference-in-differences",  # adapt to topic
    "fields": FIELDS,
    "year":   "2000-2024",
    "sort":   "citationCount",   # most-cited first; alternatives: publicationDate
    "limit":  100,               # max per call; use "token" field in response for pagination
}
r = requests.get(f"{BASE}/paper/search/bulk", headers=headers, params=params)
results = r.json()   # keys: "total", "data" (list), "token" (next page)
papers  = results.get("data", [])
# Pagination: if results["token"] exists and more papers needed:
# params["token"] = results["token"]; repeat the call

time.sleep(1)   # respect 1 req/sec rate limit with key

# --- Task 2: Cross-validate a specific paper by DOI ---
doi = "10.2307/2118030"   # replace with actual DOI from OpenAlex results
r2  = requests.get(
    f"{BASE}/paper/DOI:{doi}",
    headers=headers,
    params={"fields": FIELDS},
)
paper = r2.json()   # single paper object

time.sleep(1)

# --- Task 3: Cross-validate by Semantic Scholar paper ID ---
# paperId can be found in search results or via DOI lookup
ss_id = "paper_id_here"
r3 = requests.get(
    f"{BASE}/paper/{ss_id}",
    headers=headers,
    params={"fields": FIELDS},
)
```

**Key response fields:**

| Field | Description |
|-------|-------------|
| `paperId` | Semantic Scholar internal ID |
| `externalIds.DOI` | DOI — use to match against OpenAlex entries |
| `externalIds.ArXiv` | arXiv ID (if preprint available) |
| `citationCount` | Total citations in Semantic Scholar's index |
| `abstract` | Full abstract text (no reconstruction needed, unlike OpenAlex) |
| `venue` | Journal or conference name |
| `openAccessPdf.url` | Direct PDF link if open access |
| `publicationTypes` | e.g., `["JournalArticle"]`, `["Preprint"]` |

---

**Branch B — Without API Key (`SS_AUTH = False`): use WebFetch**

The public Semantic Scholar API works without authentication but shares a global rate limit. Use WebFetch for individual calls and space them out.

```
# Keyword search (rate-limited)
https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=minimum+wage+employment+difference-in-differences&fields=title,year,authors,abstract,citationCount,externalIds,venue&sort=citationCount

# Cross-validate a specific paper by DOI
https://api.semanticscholar.org/graph/v1/paper/DOI:10.2307/2118030?fields=title,year,authors,citationCount,abstract,externalIds,venue

# Cross-validate by arXiv ID
https://api.semanticscholar.org/graph/v1/paper/ARXIV:2301.05345?fields=title,year,authors,citationCount,abstract,externalIds
```

> ⚠️ **Rate limit discipline (no key):** Issue at most **5–8 WebFetch calls** to Semantic Scholar per round. Space calls at least 3–5 seconds apart. If a `429` status is returned, pause and retry after 30 seconds.

---

**What to do with Semantic Scholar results in Round 1:**

1. **Coverage gap check** — run 1–2 keyword searches using queries that diverged from OpenAlex (e.g., different phrasing). Flag any papers in the top 20 Semantic Scholar results that are *absent* from the OpenAlex candidate list with citation count > 20.
2. **Abstract retrieval** — if OpenAlex `abstract_inverted_index` is missing for a Core candidate, use Semantic Scholar to retrieve the full plain-text abstract directly.
3. **Cross-validation of OpenAlex metadata** — for each paper, look it up on Semantic Scholar by DOI or title and compare the following fields against the OpenAlex record:

   | Field | Check |
   |-------|-------|
   | Title | Exact match? Flag truncations or garbled characters |
   | Authors | Same author list and order? Flag missing/extra authors |
   | Year | Published year matches? |
   | Journal / Venue | Consistent journal name? |
   | DOI | DOI present and resolves to the same paper? |
   

**If a discrepancy is found:** note it in the paper entry with a `⚠️ Data discrepancy` tag and flag for manual verification. Do **not** silently carry forward potentially incorrect OpenAlex metadata into the final literature table.

**arXiv (for latest economics preprints and working papers)**

**What to do with arXiv results in Round 1:**

1. **Recency capture** — collect papers from the last 12 months not yet published in journals. These often represent the methodological frontier.
2. **Preprint–publication link** — for papers already in OpenAlex, check `externalIds.ArXiv` (via Semantic Scholar) or search arXiv ID to confirm if the working paper version has additional material.

**Search patterns:**

```
# Economics preprints — keyword search, sorted by newest first
https://export.arxiv.org/api/query?search_query=all:minimum+wage+employment&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending

# Restrict to econ.* categories (General Economics, Econometrics, Labour)
https://export.arxiv.org/api/query?search_query=cat:econ.*+AND+all:minimum+wage+employment&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending

# Retrieve most-relevant results (default relevance ranking)
https://export.arxiv.org/api/query?search_query=all:minimum+wage+"difference-in-differences"&start=0&max_results=25

# Fetch a specific paper by arXiv ID
https://export.arxiv.org/api/query?id_list=2301.05345
```

---

**NBER (for latest working papers)**

**What to do with NBER results in Round 1:**

- Recency capture, NBER working papers from last 12 months that are absent from OpenAlex.

NBER is the most authoritative working paper repository in economics. It does not have a structured public search API, so use a combination of **WebSearch** and **WebFetch** for individual paper pages.

**Step 1 — Discover via WebSearch:**

```
site:nber.org/papers "minimum wage" employment 2023 2024
site:nber.org/papers "minimum wage" inequality recent
```

**Step 2 — Fetch individual paper metadata via WebFetch:**

```
# NBER paper page (contains title, authors, abstract, publication date, JEL codes)
https://www.nber.org/papers/w31234

# NBER also exposes a JSON metadata endpoint — faster than HTML parsing:
https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_id/w31234
```

---

**SSRN (for latest working papers)**

**What to do with SSRN results in Round 1:**

- Recency capture, SSRN working papers from last 12 months that are absent from OpenAlex.
- Topics involves intersection of law and economics.

SSRN is a preprint repository especially strong in law, finance, and applied economics. It does not offer a structured public API; use **WebSearch** as the primary discovery method.

**Step 1 — Discover via WebSearch:**

```
site:papers.ssrn.com "minimum wage" employment effects 2023 2024
site:papers.ssrn.com "minimum wage" causal inference difference-in-differences
site:papers.ssrn.com "minimum wage" inequality labour market 2024
```

**Step 2 — Fetch individual paper metadata via WebFetch:**

```
# SSRN abstract page — contains title, authors, abstract, date, download count
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4567890
```

> ⚠️ SSRN pages can be slow or return partial content. If WebFetch returns incomplete HTML, limit to 2–3 SSRN fetches per round and rely on WebSearch snippets for basic metadata.

---

Record every returned paper in a running list: Author(s), Year, Title, Source, OpenAlex ID (if available), Citation Count.

---

### Round 2: Citation Network Expansion (Target: +5–10 papers)

All searches in this round use **OpenAlex only**.

#### Seed Paper Selection

Do **not** use citation count alone. Select 5 seed papers as follows:

- **Top 3** from the Round 1 candidate list ranked by `cited_by_count` — these are the seminal works whose citation network is most productive to explore.
- **Top 2** most recently published candidates from Round 1 — these anchor the frontier and surface newer work not yet highly cited.

If fewer than 5 papers exist in Round 1, use all of them.

For each seed paper, crawl their citation network using OpenAlex.

#### Forward Citations

For each seed paper, retrieve works that cite it, sorted by citation count:

```
https://api.openalex.org/works?filter=cites:SEED_OPENALEX_ID&sort=cited_by_count:desc&per_page=25&select=id,title,authorships,publication_year,cited_by_count,primary_location&api_key=YOUR_KEY
```

Collect the top 10 citing works per seed paper.

#### Backward References

```
# Step 1: retrieve the seed paper's reference list
https://api.openalex.org/works/SEED_OPENALEX_ID?select=id,referenced_works&api_key=YOUR_KEY

# Step 2: batch-fetch metadata for up to 50 references
https://api.openalex.org/works?filter=openalex_id:W111|W222|W333&select=id,title,authorships,publication_year,cited_by_count,primary_location&per_page=50&api_key=YOUR_KEY
```

#### Inclusion Threshold

Add a paper to the candidate list if it meets **at least one** of:

- `cited_by_count > 5`, **or**
- Published within the last 3 years, **or**

#### Deduplication and Stopping Rule

**Deduplication:** after each seed paper's expansion, remove any paper whose OpenAlex ID already appears in the Round 1 candidate list. Work only with net-new entries.

**Stopping rule:** if across any 3 consecutive seed papers, forward citation expansion yields fewer than 2 new papers meeting the inclusion threshold, stop early — further expansion has diminishing returns.

---

#### Update the Candidate List

Append all qualifying net-new papers to the running list using the same fields as Round 1:

`Author(s) | Year | Title | OpenAlex ID | Citation Count`

---

## Step 4: Triage and Organize Papers

### 4.1 Fetch Abstracts for Triage

For each candidate paper, retrieve the abstract if not already fetched.

**Via OpenAlex (preferred):**

```
https://api.openalex.org/works/W2170494700?select=id,title,abstract_inverted_index,authorships,publication_year,cited_by_count,primary_location&api_key=YOUR_KEY
```
Note: OpenAlex stores abstracts as `abstract_inverted_index` (a word→position map). Reconstruct the abstract by sorting positions and joining words. Example Python reconstruction:
```python
inv = work["abstract_inverted_index"]  # {"The": [0], "effect": [1], ...}
abstract = " ".join(w for w, _ in sorted(
    ((w, p) for w, positions in inv.items() for p in positions),
    key=lambda x: x[1]
))
```

**Via Semantic Scholar (fallback):**
```
https://api.semanticscholar.org/graph/v1/paper/[PAPER_ID]?fields=title,abstract,authors,year,citationCount,venue
```

Assign each paper to one category:
- **Core** (directly relevant, must cite and engage)
- **Background** (motivates the topic, cite briefly)
- **Methodological** (uses a technique you adopt)
- **Contradictory** (finds different results — must address)
- **Excluded** (off-topic, weak identification, or low-quality)

After triage, proceed to 4.2 for Core papers and 4.3 for all other retained categories.

---

### 4.2 Full-Text Acquisition for Core Papers

For papers classified as **Core**, go beyond the abstract and acquire the full PDF. Limit this to a maximum of **10 papers** to keep the review tractable.

#### Priority Order for PDF Sources

Work through these sources in order until a PDF is obtained:

**① OpenAlex open-access URL (fastest)**

Retrieve the paper's open-access status from OpenAlex:

```
https://api.openalex.org/works/OPENALEX_ID?select=id,title,open_access,primary_location,locations&api_key=YOUR_KEY
```

Check `open_access.is_oa`. If `true`, use `open_access.oa_url` as the direct PDF link.

**② Semantic Scholar open-access PDF**

If OpenAlex has no OA URL, check Semantic Scholar:

```
# With API key (SS_AUTH = True)
GET https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf,externalIds
Header: x-api-key: YOUR_SS_KEY

# Without API key (SS_AUTH = False) — WebFetch:
https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf,externalIds
```

Use `openAccessPdf.url` if present.

**③ Source-specific direct URLs**

If `externalIds` reveal a known working paper source, use the known URL pattern:

| Source | URL pattern |
|--------|-------------|
| arXiv | `https://arxiv.org/pdf/{arxiv_id}` |
| NBER | `https://www.nber.org/system/files/working_papers/w{NNNN}/w{NNNN}.pdf` |
| SSRN | Fetch abstract page → find download link in HTML |

**④ WebFetch the DOI landing page**

As a last open-access check, fetch the DOI resolver page and look for an OA download link:

```
https://doi.org/{doi}
```

Some journals (AEA, NBER, IZA) serve open-access PDFs directly from the DOI redirect.

#### Downloading and Reading the PDF

Once a PDF URL is identified, download it using Python via Bash and then read it with the `Read` tool:

```python
import requests, re, os

pdf_url = "https://arxiv.org/pdf/2301.05345"   # replace with actual URL
paper_slug = "card_krueger_1994"                # short identifier for filename

save_path = f"/sessions/lucid-nifty-goodall/{paper_slug}.pdf"
r = requests.get(pdf_url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})

if r.status_code == 200 and "pdf" in r.headers.get("Content-Type", ""):
    with open(save_path, "wb") as f:
        f.write(r.content)
    print(f"Saved: {save_path}")
else:
    print(f"Failed: HTTP {r.status_code}, Content-Type: {r.headers.get('Content-Type')}")
```

Then read with the `Read` tool. For these core papers, read each in sections — Introduction + Conclusion first, then Data, then Empirical Strategy, then Results.

#### When PDF Is Unavailable (Paywalled)

If no open-access version is found after all steps above:
1. Note `[PAYWALLED]` in the candidate list for this paper.
2. Proceed with the abstract-only summary template (Section 4.3B).
3. Flag the paper for the user with a note: *"Full text unavailable — please upload the PDF manually if you have institutional access."*

---

### 4.3 Paper Summary Templates

Use the appropriate template based on paper category and whether full text was obtained.

#### 4.3A Full-Text Summary — Core Papers

Use this template when the full PDF has been read. It is the most detailed version and forms the primary input to Step 5.

```markdown
## [Author(s)] ([Year])

**Title:** [Full title]
**Published in:** [Journal / Working Paper Series, Volume/Number]
**JEL Codes:** [e.g., J31, C21]
**Citation count:** [N]
**OpenAlex ID:** [W...]
**Full text read:** Yes / Abstract only (paywalled)

### Research Question
[One sentence stating the causal question.]

### Data
- **Source:** [Dataset name, e.g., CPS, NLSY, administrative records]
- **Period:** [Years covered]
- **Sample:** [N observations; unit of analysis, e.g., county-month, individual]
- **Geography:** [Country / region / states]
- **Key variables:** [Outcome, treatment, main controls — with exact names if possible]
- **Sample restrictions:** [Any non-obvious exclusions applied]

### Identification Strategy
- **Method:** [DiD / IV / RDD / RCT / Matching / OLS]
- **Source of variation:** [What drives the treatment? e.g., state-level minimum wage changes]
- **Key assumption:** [e.g., parallel trends, exclusion restriction, continuity at threshold]
- **Assumption test(s):** [What did the authors test? What did they find?]
- **First-stage / relevance:** [For IV: F-statistic; for RDD: bandwidth, density test result]

### Main Findings
1. [Key result with coefficient magnitude + units + statistical significance, e.g., "A $1 MW increase reduces teen employment by 0.7 pp (se=0.2), significant at 5%"]
2. [Second key result]
3. [Third key result or primary heterogeneity finding]

### Robustness Checks
| Check | Result | Location |
|-------|--------|----------|
| [e.g., Alternative control group] | [Consistent / Attenuated / Null] | [Table A1] |
| [e.g., Placebo test] | [...] | [...] |

### Limitations
- **External validity:** [Main concern about generalisability]
- **Internal validity:** [Main remaining threat, e.g., parallel trends not perfectly supported]
- **Data:** [Key measurement or coverage limitation]

### Relevance to Your Project
[2–3 sentences: How does this paper shape your identification strategy, data choices, or expected results?]
```

---

#### 4.3B Abstract-Only Summary — non-Core / Paywalled Core

Use this shorter template for non-Core papers or Core papers where full text is unavailable.

```markdown
## [Author(s)] ([Year])

**Title:** [Full title]
**Published in:** [Journal / Working Paper Series]
**Category:** Background / Methodological / Contradictory / Core (paywalled)
**Citation count:** [N] | **OpenAlex ID:** [W...]

**Research Question:** [One sentence]
**Method:** [DiD / IV / RDD / OLS / other]
**Key finding:** [One sentence with magnitude if available]
**Relevance:** [One sentence — why is this paper in the list?]
```

---

## Step 5: Narrative Synthesis

After summarizing relevant papers, write a synthesis, but **Do not just list papers.** Economics papers use narrative paragraphs. Follow this structure:

**Paragraph 1 — Establish the big picture:**

> "A large literature examines the effect of X on Y. Early work using OLS found [result], but identification concerns motivated subsequent quasi-experimental research (Author A, Year; Author B, Year). Taken together, this literature establishes that [broad conclusion]."

**Paragraph 2 — Highlight consensus:**
> "There is now broad agreement that [specific finding]. [Author A (Year)] shows [result] using [method] in [context]. [Author B (Year)] confirms this using [different method/data], finding [comparable result]."

**Paragraph 3 — Highlight disagreements (must engage, not ignore):**
> "[Author C (Year)], however, finds [contradictory result]. This discrepancy may reflect [methodological difference / data difference / context difference]. We return to this issue in Section X."

**Paragraph 4 — Identify gaps that motivate your paper:**

> "Despite this progress, two questions remain unanswered. First, [Gap 1]. Second, [Gap 2]. Our paper contributes by [your approach]."

Research Gaps Taxonomy
| Gap type | Example |
|----------|---------|
| **Geographic** | Existing evidence is US-only; no developing country evidence |
| **Temporal** | Studies focus on short-run effects; long-run unknown |
| **Subgroup** | Effects on high-skill workers unstudied |
| **Mechanism** | What drives the effect? (price, profit, productivity?) |
| **Methodological** | All existing papers use OLS; no credible IV evidence |
| **Data** | All use survey data; no administrative records |
| **Policy counterfactual** | Effects at lower/higher magnitudes unknown|

**Paragraph 5 — Position Your Contribution**

> "This paper makes [N] contributions to the literature on [topic]. First, we [contribution 1] — while [Author A (Year)] studies [X], our paper is the first to [Y]. Second, we use [data/method] which allows us to [identify/measure] [Z], addressing [limitation in prior work]. Third, our findings [extend/challenge/reconcile] the evidence from [Author B (Year)] by showing [how/why]."

---

## Step 6: Deliver a Full Reference List

After completing the search and synthesis, produce a full BibTeX reference list for all Core and Background papers cited.

Retrieve structured metadata via OpenAlex:
```
https://api.openalex.org/works/W2170494700?select=id,doi,title,authorships,publication_year,primary_location,biblio&api_key=YOUR_KEY
```

The `doi` field, `primary_location.source.display_name` (journal name), `biblio.volume`, `biblio.issue`, and `biblio.first_page` / `biblio.last_page` provide everything needed for BibTeX.

**BibTeX format:**

```bibtex
@article{CardKrueger1994,
  author  = {Card, David and Krueger, Alan B.},
  title   = {Minimum Wages and Employment: A Case Study of the Fast-Food
             Industry in New Jersey and Pennsylvania},
  journal = {American Economic Review},
  year    = {1994},
  volume  = {84},
  number  = {4},
  pages   = {772--793},
  doi     = {10.2307/2118030}
}
```

Use `@unpublished` for working papers not yet published in a journal.

---

## Final Output: literature-review-report.md

After finishing all steps above, write the final literature review report and save it as `literature-review-report.md` in the working directory.

**Mandatory post-delivery reminder:**

After presenting the report link to the user, you **must** append the following notice:

> ---
> ### ⚠️ 学术诚信提示：请用其他大模型交叉核验文献
>
> 本报告已通过 OpenAlex + Semantic Scholar 交叉检验文献的元数据（标题、作者、期刊、年份）。尽管如此，**AI 生成的文献列表仍可能存在幻觉**。
>
> **强烈建议**将文献列表粘贴至 **ChatGPT**、**Gemini** 或其他独立大模型，并询问：
> 
> > *"请逐条检验以下文献是否真实存在，标题、作者、期刊、年份是否准确无误。"*
> 

**Example format of literature review report:**

```markdown
# Literature Review Report
**Topic:** Effects of Minimum Wage on Employment
**Source:** OpenAlex(primary), Semantic Scholar/NBER/arXiv/SSRN(supplementary)
**Date Range:** 1990-2026
**Papers reviewed:** 52 total → 12 Core, 9 Background, 6 Methodological, 4 Contradictory, 21 Excluded

---

## Core Papers

### Card and Krueger (1994)

**Title:** Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania
**Published in:** *American Economic Review*, 84(4), 772–793
**JEL Codes:** J31, J38
**Citation count:** 8,214 (OpenAlex) | 9,102 (Semantic Scholar)
**OpenAlex ID:** W2133060252
**Full text read:** Yes (NBER PDF)

**Research Question:**

**Data**

**Identification Strategy**

**Main Findings**

**Limitations**

**Relevance to Your Project**

---

## Non-Core Papers

### Neumark and Wascher (2000)

**Title:** Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania: Comment
**Published in:** *American Economic Review*, 90(5), 1362–1396
**Category:** Contradictory
**Citation count:** 1,247 | **OpenAlex ID:** W2048872744
**Full text read:** Yes (user uploaded)

**Research Question:**
**Method:**
**Key finding:**
**Relevance:**

---

## Narrative Synthesis

A large empirical literature examines the effect of minimum wages on employment......

The modern quasi-experimental literature, launched by Card and Krueger (1994), challenged this consensus using a difference-in-differences design......

Despite this progress, three questions remain underexplored......

This paper makes [N] contributions to the literature on [topic]. First...

---

## References

Autor, D. H., Manning, A., & Smith, C. L. (2016). The contribution of the minimum wage to US wage inequality over three decades: A reassessment. *American Economic Journal: Applied Economics*, 8(1), 58–99. https://doi.org/10.1257/app.20140073
```

---

## Common Pitfalls

- ❌ Presenting a search framework instead of actually running searches
- ❌ Stopping after one round of search queries — always do three rounds
- ❌ Filtering by author name directly (use two-step ID lookup)
- ❌ Only citing papers that support your argument
- ❌ Ignoring contradictory findings
- ❌ Confusing correlation with causation when describing OLS results
- ❌ Citing papers you have not read (mischaracterizing findings)
- ❌ Vague gap identification ("more research is needed") — be specific
- ❌ **Skipping the post-delivery integrity reminder** — always tell the user to cross-check the final reference list with ChatGPT / Gemini or another independent LLM before citing. AI-generated reference lists carry hallucination risk even after API-based cross-validation; a second-model sanity check is the last line of defence for academic integrity.
