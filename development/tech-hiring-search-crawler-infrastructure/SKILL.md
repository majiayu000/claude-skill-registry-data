---
name: "tech-hiring-search-crawler-infrastructure"
description: "Search and crawler infrastructure engineers build systems that discover, index, rank, and serve information at scale. This includes web crawlers (HTTP fetching, politeness, de-duplication), search index construction and ranking, information"
---

# Search & Crawler Infrastructure — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Search & Crawler Infrastructure

### What This Role Does
Search and crawler infrastructure engineers build systems that discover, index, rank, and serve information at scale. This includes web crawlers (HTTP fetching, politeness, de-duplication), search index construction and ranking, information retrieval algorithms, and query processing pipelines. This discipline is central to SEO tooling companies (Ahrefs, Semrush, Moz), search engines, e-commerce search, and enterprise knowledge management. Highly specialised — small talent pool, high competition.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Software Engineer (Search), Search Engineer, Crawler Engineer |
| Mid | Search Engineer, IR Engineer, Crawler Infrastructure Engineer |
| Senior | Senior Search Engineer, Senior IR Engineer, Search Platform Engineer |
| Staff+ | Staff Search Engineer, Principal Search Engineer, Search Architect |
| Research track | Search Relevance Scientist, Information Retrieval Researcher |

### Skill Tiers

**Tier 1 — Must-have:**
- Systems programming: C++, Go, Rust, Java, or OCaml — search infrastructure is performance-critical, scripting languages alone are insufficient
- Distributed systems fundamentals: consensus, partitioning, replication, fault tolerance
- Large-scale data processing: comfort with petabyte-scale systems
- Search fundamentals: inverted indexes, BM25/TF-IDF, document ranking

**Tier 2 — Differentiator:**
- Elasticsearch, Apache Solr, or Lucene — internals, not just API usage
- Web crawling: Scrapy, Nutch, or custom crawler development; URL frontier management, politeness protocols (robots.txt), deduplication (Simhash, MinHash)
- Vector search / dense retrieval: ANN algorithms (HNSW, IVF), FAISS, Weaviate, Qdrant
- ClickHouse for analytics at scale (critical for SEO tooling)
- Query parsing, query understanding, spelling correction, synonyms
- Link graph algorithms: PageRank, HITS, trustrank

**Tier 3 — Bonus:**
- OCaml (language of choice at Ahrefs — rare, extremely high signal)
- Custom storage engine development
- Neural information retrieval (learned sparse models, ColBERT, DPR)
- Experience with trillion-link or billion-page scale systems
- Research publications in IR, SIGIR, ECIR, WWW

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("search engineer" OR "information retrieval" OR "crawler engineer" OR "search infrastructure") (Elasticsearch OR Lucene OR Solr OR "web crawler" OR "inverted index") -recruiter -talent

# Research/academia crossover
site:linkedin.com/in/ ("information retrieval" OR "IR" OR "search relevance") (SIGIR OR "web crawling" OR "ranking" OR Lucene) -recruiter

# arXiv — find IR researchers
site:arxiv.org "web crawling" OR "information retrieval" 2024 OR 2025
site:arxiv.org "dense retrieval" OR "learned sparse" "BEIR" 2025

# GitHub — search systems engineers
language:rust followers:>30 pushed:>2025-01-01
language:ocaml followers:>15 pushed:>2025-01-01
site:github.com "joined on" (Elasticsearch OR "inverted index" OR "web crawler" OR ClickHouse) followers:>25

# OCaml community (Ahrefs-specific)
site:github.com "joined on" OCaml (search OR crawler OR indexing) followers:>10
 ``

### Seniority Signals

- **Junior → Mid:** Can implement a standard ranking algorithm from a paper; debugs relevance issues systematically
- **Mid → Senior:** Designs crawl systems that handle anti-bot measures, politeness, and URL deduplication at billion-URL scale; measures relevance quality with systematic evaluation frameworks
- **Senior → Staff:** Defines the architecture for a next-generation index; manages the tradeoffs between freshness, coverage, and cost at petabyte scale
- **OCaml signal:** Very few engineers work in OCaml professionally. Anyone with production OCaml experience at scale (Ahrefs, Jane Street, Meta's Hack tooling history) is an exceptionally rare profile.

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| Systems fundamentals | Distributed systems questions, data structures | Depth in CS fundamentals |
| Coding | Implement a simplified inverted index or BM25 scorer | IR understanding in code |
| System design | Design a web crawler for [scale] OR design a search index for [workload] | Scale thinking, crawl politeness, freshness vs. coverage |
| Domain depth | Discuss their most complex search or crawler system | Real ownership, failure modes they've encountered |
| Behavioural | STAR — high-scale incident, algorithm choice tradeoffs | Production maturity |

**Best system design question:** "Design a system to crawl 10 billion URLs and keep them fresh within 30 days. What's your frontier management strategy? How do you handle anti-bot measures?" The best candidates immediately discuss crawl budget, politeness delays, prioritisation (high-value domains crawled more frequently), and distributed coordination.

### Red Flags
- "I've used Elasticsearch" without understanding what it's doing internally
- No understanding of crawl politeness or robots.txt — a red flag for anyone building production crawlers
- Conflates search with recommendation (related but different problem spaces)
- Can't explain what an inverted index is at a technical level
- No experience with large-scale distributed systems (search doesn't work on a single machine at any interesting scale)

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $110k – $150k |
| Mid | $155k – $200k |
| Senior | $185k – $260k |
| Staff | $240k – $320k |
| Principal | $290k – $400k+ |

*Search infrastructure commands a significant premium — the talent pool is small and the domain knowledge is rare. Expect competition from Elastic, Solr/Lucene contributors, and the major search engines.*
