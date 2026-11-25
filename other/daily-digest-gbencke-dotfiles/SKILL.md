---
name: daily-digest
description: Generate The Architect's Digest — a daily curated briefing of the most relevant stories in architecture, distributed systems, cloud, languages, tooling, AI agents, CS research, and new technical book releases (Apress, O'Reilly, Packt, Manning), sourced live from Hacker News, Lobsters, GitHub Trending, Hugging Face Papers, InfoQ, and top engineering blogs.
---

# The Architect's Digest Skill

This skill produces a daily curated digest for software architects. The output is a long-form briefing: substantive, deeply annotated entries across 9 sections, written for senior engineers who want context and architectural implications — not headlines.

## Tools to Use

- `tavily_search`: Primary research tool. Use `search_depth: 'advanced'` and `topic: 'news'` when freshness matters. Always include `time_range: 'week'`.
- `obscura_web_scrape`: Fetch full article text when a search snippet is too thin to annotate meaningfully. Use for InfoQ, engineering blogs, GitHub Trending, and book review sources.

## Output

Save the digest to:

```
__.DailyDigest/YYYY-MM-DD-architects-digest.md
```

Create the `__.DailyDigest/` directory if it does not exist.

---

## Workflow

### Step 1 — Gather raw signals (run all searches in parallel)

Collect at minimum **5 candidates per section** before writing anything. Run all searches simultaneously — do not wait for one batch to complete before starting the next.

#### Architecture & Distributed Systems
```
tavily_search("distributed systems architecture infoq 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("infoq.com architecture microservices distributed systems 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("database reliability engineering zero-downtime upgrade 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("site:news.ycombinator.com distributed systems architecture 2026", topic: 'news', time_range: 'week')
tavily_search("site:lobste.rs distributed systems architecture 2026", topic: 'news', time_range: 'week')
```

#### GitHub Trending & Lobste.rs
Scrape the following pages in parallel to collect at least 50 repositories/items before filtering:

```
obscura_web_scrape("https://github.com/trending?since=daily")
obscura_web_scrape("https://github.com/trending?since=weekly")
obscura_web_scrape("https://github.com/trending/python?since=daily")
obscura_web_scrape("https://github.com/trending/go?since=daily")
obscura_web_scrape("https://github.com/trending/rust?since=daily")
obscura_web_scrape("https://lobste.rs/")
obscura_web_scrape("https://lobste.rs/newest")
```

Extract from each page: repo name, star total, stars today/this week, language, description. Deduplicate across pages (keep the entry with the highest star velocity). You must collect **at least 50 distinct repositories** before scoring. Pick the 15–20 most architecturally relevant for the final digest.

#### Languages & Tooling
```
tavily_search("programming language release rust golang typescript c++ 2026", topic: 'news', time_range: 'week')
tavily_search("developer tooling IDE compiler announcement 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("site:lobste.rs programming language tooling compiler 2026", topic: 'news', time_range: 'week')
tavily_search("infoq.com developer tools platform engineering 2026", search_depth: 'advanced', time_range: 'week')
```

#### Cloud & Infrastructure
```
tavily_search("AWS GCP Azure kubernetes infrastructure announcement 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("data center network fabric AI infrastructure 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("cloud provider new service announcement infoq 2026", search_depth: 'advanced', time_range: 'week')
```

#### AI & Agents
```
tavily_search("AI agent architecture production multi-agent system 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("LLM agent orchestration workflow enterprise 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("MCP model context protocol security architecture 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("infoq.com AI agents agentic systems context management 2026", search_depth: 'advanced', time_range: 'week')
```

#### Hugging Face Papers
Scrape the Hugging Face daily papers pages in parallel to collect at least 30 candidate papers before filtering:

```
obscura_web_scrape("https://huggingface.co/papers", dump: 'text')
obscura_web_scrape("https://huggingface.co/papers/week", dump: 'text')
obscura_web_scrape("https://huggingface.co/papers/month", dump: 'text')
```

Extract from each page: paper title, arXiv ID, upvote count, and the one-line abstract. Deduplicate across pages (keep the entry with the highest upvotes). Also run:

```
tavily_search("huggingface.co/papers trending LLM agents 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("arxiv trending paper reasoning agents inference efficiency 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
```

For papers that make the shortlist, fetch the arXiv abstract page for detail:

```
obscura_web_scrape("https://arxiv.org/abs/{arxiv_id}", dump: 'text')
```

Prioritize papers with architectural significance: new model architectures, inference/serving efficiency, agent frameworks, evaluation methodology, context management, and training/inference systems work — over pure benchmark-chasing results.

#### CS Research
```
tavily_search("site:queue.acm.org distributed systems database paper 2026", time_range: 'week')
tavily_search("arxiv.org cs.DC cs.DB distributed systems 2026", topic: 'news', time_range: 'week')
tavily_search("post-quantum cryptography migration security 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("observability tracing AI agent research 2026", search_depth: 'advanced', time_range: 'week')
```

#### Tech & Startup Book Reviews
Scrape and search the following sources in parallel. Focus on books published or reviewed in the past 90 days:

```
obscura_web_scrape("https://commoncog.com/blog/", dump: 'text')
obscura_web_scrape("https://fivebooks.com/category/technology/", dump: 'text')
obscura_web_scrape("https://fs.blog/category/reading/book-reviews/", dump: 'text')
obscura_web_scrape("https://www.oreilly.com/radar/", dump: 'text')
obscura_web_scrape("https://bookauthority.org/books/new-software-engineering-books", dump: 'text')
obscura_web_scrape("https://bookauthority.org/books/new-startup-founders-books", dump: 'text')
tavily_search("new technology startup book review 2026", topic: 'news', search_depth: 'advanced', time_range: 'week')
tavily_search("site:commoncog.com book review", search_depth: 'advanced', time_range: 'week')
tavily_search("site:fs.blog book summary 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("site:fivebooks.com technology startup 2026", search_depth: 'advanced', time_range: 'week')
tavily_search("software engineering architecture startup book published 2026", search_depth: 'advanced', time_range: 'week')
```

Prioritize sources in this order:
1. **commoncog.com** — practitioner-depth reviews; strong on business operations, mental models, and startup strategy
2. **fs.blog (Farnam Street)** — mental models, decision-making, and business strategy books
3. **fivebooks.com/category/technology** — expert-curated lists; good for surfacing consensus must-reads
4. **oreilly.com/radar** — new O'Reilly releases and practitioner-authored tech books
5. **bookauthority.org** — ranked lists for new startup and engineering books
6. **shortform.com/best-books/genre/best-technology-books** — summaries with critical context
7. **pragprog.com** — new Pragmatic Programmer releases; practitioner-written
8. **goodreads.com/shelf/show/software-business** — community signal on which titles are actually being read

For each candidate book, extract: title, author, publisher, publication date, reviewer/source, and a summary of the review's core argument.

**Book deduplication against previous digests.** Before selecting candidates, check the `__.DailyDigest/` directory for existing digests from the past 30 days. Read the `## Tech \& Startup Book Reviews` and `## Technical Books` sections of the 5 most recent files and extract every book title and author. Exclude any book that has already appeared in a previous digest. Do not repeat a book until at least 30 days have passed since its last appearance. If a book was covered recently, skip it regardless of whether a new review is available.

#### Technical Books (New Releases)
Scrape and search the publisher catalogs in parallel. Focus strictly on books **published within the past 90 days** — check the publication date on each book's page and drop anything older:

```
obscura_web_scrape("https://www.manning.com/catalog", dump: 'text')
obscura_web_scrape("https://www.apress.com/us/shop", dump: 'text')
obscura_web_scrape("https://www.packtpub.com/en-us/all-products", dump: 'text')
obscura_web_scrape("https://www.oreilly.com/search/?q=*&type=book&publishers=O%27Reilly%20Media%20Inc.&order_by=published_on", dump: 'text')
tavily_search("site:manning.com new book MEAP 2026", search_depth: 'advanced', time_range: 'month')
tavily_search("site:apress.com new book release software 2026", search_depth: 'advanced', time_range: 'month')
tavily_search("site:packtpub.com new book release 2026", search_depth: 'advanced', time_range: 'month')
tavily_search("site:oreilly.com new book published 2026", search_depth: 'advanced', time_range: 'month')
tavily_search("Apress OR Packt OR Manning OR O'Reilly new technical book release", topic: 'news', search_depth: 'advanced', time_range: 'month')
```

For each candidate book, extract: title, author(s), publisher, publication date, topics covered, and page count if available. If a catalog page or search result does not show the publication date, fetch the book's detail page:

```
obscura_web_scrape("{book detail page URL}", dump: 'text')
```

Prioritize books aimed at working architects and senior engineers: distributed systems, architecture, cloud infrastructure, data engineering, platform engineering, AI systems, and language/runtime internals. Skip beginner tutorials and certification-prep titles unless they cover a genuinely new platform or standard. The same 30-day deduplication rule from the Book Reviews section applies here.

---

### Step 2 — Fetch full articles for top candidates

For any candidate where the search snippet is insufficient to write a substantive annotation, fetch the full article:

```
obscura_web_scrape("{article URL}", dump: 'text')
```

Do this for at least 6–8 of the best candidates across all sections. For book reviews, always fetch the full review text — summaries alone are too thin to annotate well.

---

### Step 3 — Score and select

For each candidate, score on three axes (1–3 each):

| Axis | Question |
|---|---|
| **Relevance** | Is this directly useful to a working architect or technical founder? |
| **Novelty** | Is this new information, not a rehash? |
| **Depth** | Is there enough substance to annotate at length? |

Keep only items scoring **7 or higher**. Target **130 total items** across all sections. If a section has fewer than 15 qualifying items, run additional targeted searches for that section before proceeding.

For the Book Reviews section specifically: prefer books that contain a concrete argument, a novel framework, or production-tested insight over books that are primarily narrative or motivational. For the Technical Books section: prefer books that teach a mechanism or a system over books that survey a topic superficially. Additionally, exclude any book that has appeared in a previous digest within the last 30 days — a repeated book fails the novelty criterion regardless of review quality.

---

### Step 4 — Write annotations

For each selected item, write a **comprehensive annotation of 350–600 words** covering:

1. **What it is** — state the thing plainly, with concrete specifics (numbers, names, versions).
2. **The architectural mechanism** — explain *how* it works, not just *that* it works.
3. **The architectural implication** — why does this matter to someone designing systems?
4. **Context and comparison** — connect it to something the reader already knows: a pattern, a prior art, a related incident, a competing approach.
5. **Tradeoffs and caveats** — what doesn't this solve? What are the risks or limitations?
6. **Actionability** — what should the reader do, evaluate, or watch next?

For **Book Review** and **Technical Books** annotations, replace "architectural mechanism" and "architectural implication" with:

2. **The book's central argument** — what claim does it make and what evidence does it provide?
3. **Who should read it** — which role (architect, founder, engineering manager, IC) gets the most from it, and at what career stage?

Use the tone of a senior engineer explaining something to a peer — direct, specific, no hype. Phrase caveats and limitations honestly. Let complexity stand; do not oversimplify.

Example tone target:
> Yelp's DBRE team did an in-place rolling upgrade across 1,000+ Cassandra nodes without interrupting production — no parallel cluster, no maintenance window. The strategy combined controlled batch upgrades, cluster repair between each step, and automated health checks throughout. Unlike blue-green approaches that spin up a parallel cluster, this was the harder path: it relies entirely on Cassandra's backward compatibility window and requires the cluster to remain coherent throughout the upgrade sequence. The architectural takeaway generalizes: stateful systems can be continuously upgraded if you treat the cluster as a rolling contract, not a monolith. Teams on Kafka, Elasticsearch, or any AP-model database have a concrete runbook to study here. The important caveat is that this approach requires deep automation investment upfront — attempting it manually at this scale would be unsafe.

---

### Step 5 — Select the lead story

The lead story is the single most architecturally significant item across all sections. It must:
- Represent a meaningful shift in the landscape
- Be something a senior engineer would immediately want to discuss with their team
- Have concrete evidence or production data backing it (not just an announcement)

Write a one-sentence lead blurb for the `> **Lead story:**` block.

---

### Step 6 — Assemble the digest

Use this exact template:

```markdown
# The Architect's Digest
### {Day of week}, {Month} {Day}, {Year}

> **Lead story:** {one-sentence lead blurb}

---

## Index

- **Architecture & Systems**
  - [{Title}]({URL}) — {one-line summary}
  - [{Title}]({URL}) — {one-line summary}
- **GitHub Trending**
  - [{owner/repo}]({URL}) — {one-line summary}
  - [{owner/repo}]({URL}) — {one-line summary}
- **Language & Tooling**
  - [{Title}]({URL}) — {one-line summary}
  - [{Title}]({URL}) — {one-line summary}
- **Cloud & Infrastructure**
  - [{Title}]({URL}) — {one-line summary}
  - [{Title}]({URL}) — {one-line summary}
- **AI & Agents**
  - [{Title}]({URL}) — {one-line summary}
  - [{Title}]({URL}) — {one-line summary}
- **CS & Research**
  - [{Title}]({URL}) — {one-line summary}
  - [{Title}]({URL}) — {one-line summary}
- **Hugging Face Papers**
  - [{Title}]({URL}) — {one-line summary}
  - [{Title}]({URL}) — {one-line summary}
- **Tech & Startup Book Reviews**
  - [{Title} by {Author}]({URL}) — {one-line summary}
  - [{Title} by {Author}]({URL}) — {one-line summary}
- **Technical Books**
  - [{Title} by {Author}]({URL}) — {one-line summary}
  - [{Title} by {Author}]({URL}) — {one-line summary}

---

## Architecture & Systems

**[{Title}]({URL})**
*Source: {Source name} · {date or engagement metric if available}*

{annotation — 350–600 words}

`tags: {tag1} · {tag2} · {tag3} · {tag4}`

---

{repeat for each item in this section}

## GitHub Trending

**[{owner/repo} — ★{total} (+{today} today)]({URL})**
*Source: GitHub Trending · {language}*

{annotation — 350–600 words}

`tags: {tag1} · {tag2} · {tag3}`

---

{repeat for each item in this section}

## Language & Tooling

{same item format}

---

## Cloud & Infrastructure

{same item format}

---

## AI & Agents

{same item format}

---

## CS & Research

{same item format}

---

## Hugging Face Papers

**[{Title}]({arXiv URL})**
*Source: Hugging Face Papers · arXiv:{arxiv_id} · {upvotes if available} upvotes*

{annotation — 350–600 words}

`tags: {tag1} · {tag2} · {tag3}`

---

{repeat for each item in this section}

## Tech & Startup Book Reviews

**[{Title} by {Author}]({URL})**
*Source: {Review source} · Published: {publication date} · Publisher: {publisher}*

{annotation — 350–600 words covering: what the book argues, the central framework or evidence, who should read it, what it costs the reader in time vs. what it delivers, and one honest caveat}

`tags: {tag1} · {tag2} · {tag3}`

---

{repeat for each item in this section}

## Technical Books

**[{Title} by {Author}]({URL})**
*Source: {Publisher} · Published: {publication date} · {page count if available}*

{annotation — 350–600 words covering: what the book teaches, the mechanism or system at its core, who should read it and at what career stage, what it costs the reader in time vs. what it delivers, and one honest caveat}

`tags: {tag1} · {tag2} · {tag3}`

---

{repeat for each item in this section}
```

Assembly rules:
- Every item must have a working URL obtained from a search or scrape result. Never construct URLs by inference.
- Tags: lowercase, hyphen-separated, 3–6 per item.
- Source attribution: use the actual publication name (InfoQ, The New Stack, GitHub Trending, Commoncog, Farnam Street, etc.).
- Engagement metrics (HN points, GitHub star counts): include when found; omit when not — never estimate.
- Section order: Architecture & Systems → GitHub Trending → Language & Tooling → Cloud & Infrastructure → AI & Agents → CS & Research → Hugging Face Papers → Tech & Startup Book Reviews → Technical Books.
- If a section genuinely has no qualifying items on a given day, omit the section entirely rather than padding it.

---

### Step 7 — Save

Write the assembled digest to `__.DailyDigest/YYYY-MM-DD-architects-digest.md`. Print the full path when done.

---

## Execution Rules

- **Stay current.** All items must be from the past 7 days unless explicitly labelled as a resurface of a classic paper. Book reviews may cover books published within the past 90 days.
- **No hallucinated links.** Every URL must have been returned by a tool call. If uncertain, verify with a second `tavily_search` or `obscura_web_scrape` before including.
- **No padding.** Weak items with thin substance are worse than a shorter digest. Drop them.
- **Minimum word count: 10,000 words.** The digest should be substantive enough to serve as a complete weekly briefing. Annotations are the primary vehicle — invest in depth.
- **Tone.** Direct, senior-engineer-to-senior-engineer. No hype, no filler ("game-changing", "revolutionary", "exciting"). State what something does, what it costs, and what it doesn't solve.
- **Minimum items: 130.** Spread across all nine sections:
  - Architecture & Systems: at least 20 items
  - GitHub Trending: at least 15 items (from a candidate pool of 50+ repos)
  - AI & Agents: at least 15 items
  - Language & Tooling: at least 10 items
  - Cloud & Infrastructure: at least 10 items
  - CS & Research: at least 10 items
  - Hugging Face Papers: at least 10 items (from a candidate pool of 30+ papers)
  - Tech & Startup Book Reviews: at least 5 items
  - Technical Books: at least 5 items (all published within the past 90 days)
- Keep running additional searches until the 130-item target is met.
- **GitHub Trending pool.** You must scrape at least 50 distinct repos (deduplicated) before selecting the final 15–20 for the digest. Do not skip the language-specific trending pages — they surface repos that the polyglot feed misses.
