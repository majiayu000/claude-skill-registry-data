---
name: "tech-hiring-cpp-systems-engineering"
description: "C++ systems engineers build the performance-critical infrastructure that everything else runs on: search engines, web crawlers, columnar databases, and distributed storage. Two primary contexts: (1) search and crawler infrastructure — high-throughput HTTP fetching, URL scheduling, inverted indexing at petabyte scale; (2) database internals — columnar storage engines, query execution, Raft replication, MVCC, and SIMD-optimised analytics (ClickHouse, TiFlash)."
---

# C++ Systems Engineering — Hiring Guide

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

## C++ Systems Engineering

### What This Role Does

C++ systems engineering at this level means owning the lowest layers of the stack where performance is not optional. Two distinct but related contexts:

**Search & Crawler Infrastructure** — Building the systems that discover, fetch, parse, and index the web at scale: URL schedulers across billions of domains, high-throughput HTTP fetching with politeness enforcement, content parsing pipelines, inverted index construction, and the distributed coordination that holds it all together.

**Database Systems (ClickHouse / TiDB / TiFlash)** — Building the analytical database layer: columnar storage engines, vectorised query execution, MVCC for snapshot isolation, Raft-based replication, compression codecs (LZ4, ZSTD), and SIMD-optimised operators. ClickHouse is C++ throughout. TiFlash (TiDB's analytical engine) is C++ built on ClickHouse's columnar format with Raft Learner replication.

Both contexts demand expert C++17/20, deep Linux knowledge, performance obsession backed by profiling data, and the ability to own production systems for years.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Software Engineer (Systems), C++ Engineer, Systems Developer |
| Mid | C++ Engineer, Systems Engineer, Search Engineer, Database Engineer |
| Senior | Senior C++ Engineer, Senior Systems Engineer, Search Infrastructure Engineer, Database Systems Engineer |
| Staff+ | Staff Engineer, Principal Systems Engineer, Distributed Systems Architect |
| Research track | Systems Researcher, Search Relevance Engineer, Database Research Engineer |

### Skill Tiers

**Tier 1 — Must-have (dealbreaker if missing):**
- Expert C++17 or C++20: move semantics, RAII, smart pointers, templates, concurrency primitives (std::atomic, mutexes, lock-free structures) — not just syntax, they understand what the compiler generates
- Linux systems fundamentals: TCP/IP sockets, memory-mapped files, page cache behaviour, I/O scheduling, multi-threaded programming
- Performance engineering: profiling with perf or flamegraphs, CPU cache behaviour, memory bandwidth constraints, latency vs. throughput reasoning
- Distributed systems at scale: has shipped systems handling billions of events/day or petabytes of data
- Production debugging: diagnosed memory leaks, race conditions, and performance regressions in production C++ code

**Tier 2 — Differentiator:**
- **Search/Crawler context:** inverted index internals, URL frontier management, crawl politeness (robots.txt, crawl budget), distributed deduplication (SimHash, MinHash), BM25/TF-IDF, Elasticsearch or Lucene internals
- **Database context:** columnar storage formats, query execution pipelines, MVCC and snapshot isolation, Raft replication, columnar compression, B-tree and LSM-tree internals, SIMD vectorisation
- RocksDB or LevelDB internals — not just usage, understands compaction, bloom filters, write amplification
- ClickHouse internals: MergeTree storage engine, materialized views, query optimizer, data types
- Custom memory allocators, arena allocation, memory pool patterns for high-throughput systems

**Tier 3 — Rare Upside:**
- Prior ClickHouse or TiFlash internals contributions
- SIMD intrinsics (AVX2/AVX-512) for data-parallel query execution
- Custom storage engine from scratch
- Research publications in databases (VLDB, SIGMOD, ICDE) or information retrieval (SIGIR, ECIR)
- HFT or real-time trading systems background — same performance discipline, highly transferable

### Sourcing Strings

```bash
# LinkedIn X-Ray — C++ systems / infrastructure
site:linkedin.com/in/ ("C++ engineer" OR "systems engineer" OR "infrastructure engineer") (C++ OR "C plus plus") ("distributed systems" OR "search" OR "crawler" OR "database") -recruiter -talent

# Database internals specialists
site:linkedin.com/in/ (ClickHouse OR TiDB OR "TiFlash" OR "columnar" OR "OLAP") ("software engineer" OR "database engineer" OR "systems engineer") -recruiter

# Search infrastructure
site:linkedin.com/in/ ("search engineer" OR "search infrastructure" OR "crawler engineer") (C++ OR Rust OR Go) (Elasticsearch OR Lucene OR "inverted index" OR "web crawler") -recruiter

# GitHub — C++ systems engineers
language:cpp followers:>20 pushed:>2025-01-01

# GitHub — ClickHouse / database contributors
site:github.com "joined on" (ClickHouse OR TiFlash OR "columnar storage" OR "query engine") C++ followers:>15

# GitHub — search/crawler C++
site:github.com "joined on" (crawler OR "search engine" OR "inverted index") C++ followers:>15
```

### Seniority Signals

- **Junior → Mid:** Moves from implementing isolated components to owning a full subsystem; starts reasoning about failure modes and production correctness, not just functionality
- **Mid → Senior:** Diagnoses and fixes subtle concurrency bugs in production; owns performance regressions end-to-end; their code runs for years without intervention
- **Senior → Staff:** Redefines the architecture of a major subsystem; identifies cross-team performance constraints; their design decisions shape how the next 10x of scale is handled

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| Phone screen | Systems design discussion: "Walk me through how you'd build a distributed crawler for 1B URLs. How do you handle politeness? What fails first?" | Distributed systems thinking, production maturity |
| C++ deep dive | Real C++ problem — write a thread-safe lock-free logger, or debug a subtle race in provided code | Concurrency correctness, memory management, modern C++ |
| Systems design | Design a columnar storage engine OR a web index serving 100k QPS — breadth, trade-off reasoning | Scale thinking, storage knowledge, failure modes |
| Domain depth | "Walk me through the most performance-critical system you've owned. Show me a profiler output from it." | Real ownership, measurement discipline, production experience |
| Code review | Review a PR touching a storage or query component | Can they read unfamiliar C++? Do they find the right problems? |

**Best search design question:** "Design a system to crawl 10B URLs and keep them fresh within 30 days. What's your frontier strategy? How do you handle anti-bot? What breaks at 10x?" Best candidates immediately discuss crawl budget, politeness delays, prioritisation by domain authority, and distributed coordination.

**Best database design question:** "Design a columnar analytics engine that needs to handle 100B row inserts/day while serving sub-second queries. How do you structure writes? How do you handle compaction?" Best candidates discuss partitioning, MergeTree-style background compaction, and the write-read trade-off explicitly.

### Red Flags
- "I've used ClickHouse" without understanding what MergeTree is doing internally
- Strong algorithmic problem-solver with no experience shipping systems at scale
- Writes C++ but shaky on move semantics, RAII, or what happens with a dangling reference
- Dismisses profiling: "we'll optimise if it becomes a problem" — in C++ systems, performance IS the problem
- No experience debugging race conditions or memory issues in production
- Cannot explain crawl politeness or why a crawler without robots.txt compliance is unshippable

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $120k – $160k |
| Mid | $160k – $210k |
| Senior | $195k – $275k |
| Staff | $250k – $340k |
| Principal | $310k – $420k+ |

*C++ systems engineers specialising in search infrastructure or database internals command significant premiums. Expect competition from Elastic, Clickhouse Inc., PingCAP, Yandex/VK, and the major search engines. The talent pool with both C++ depth and domain-specific knowledge (crawler architecture or OLAP database internals) is very small.*
