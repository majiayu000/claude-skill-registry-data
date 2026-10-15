---
name: internet-search
description: "Tool-agnostic search — query construction, tool selection, source trust hierarchy."
context: fork
globs: ["**/*.md"]
alwaysApply: false
---

# Internet Search Skill

## 1. Tool Selection

Three search tools are available. Choose by task type:

| Task | Primary Tool | Why | Fallback |
|------|-------------|-----|----------|
| Library/framework docs, API reference, version migration | `context7` | Official docs + code examples, version-aware | `webfetch` known docs URL |
| Broad web search, technical Q&A, current info, news | `websearch` | Semantic search across indexed web, live crawl option | `webfetch` specific result URLs |
| Known URL (docs page, GitHub issue, blog post, changelog) | `webfetch` | Direct fetch of a specific page, returns markdown | — |

**Parallel rule**: `context7` + `websearch` can run simultaneously — they are independent tools.

---

## 2. Query Construction

### 2.1 Be Specific

```
❌ "Python async"
✅ "FastAPI background tasks SQLAlchemy async session 2024"

❌ "Docker error"
✅ "Docker multi-stage build COPY --from permission denied non-root"
```

### 2.2 Include Version

Append the target version or year to scope results:

```
"SQLAlchemy 2.0 async session pattern"
"Next.js 15 server components migration"
"React 19 use() hook"
```

### 2.3 Use Domain-Specific Keywords

```
# Framework/library — include name + key concept
"FastAPI dependency injection lifespan"

# Bug/error — include exact error message + language/framework
"TypeError: 'NoneType' object is not callable FastAPI"

# Comparison — make explicit
"Redis vs Valkey 2025 performance comparison"
```

---

## 3. Source Trust Hierarchy

Always escalate from the highest trust tier before falling back:

| Tier | Sources | Use for |
|------|---------|---------|
| **T1 — Authoritative** | Official vendor docs, RFC/specs, peer-reviewed papers, GitHub READMEs | Definitive answers, API contracts, algorithm correctness |
| **T2 — High-signal** | Stack Overflow (accepted/high-vote), GitHub Issues/Discussions, official changelogs | Real-world patterns, known bugs, version behaviors |
| **T3 — Useful, verify** | Hacker News, Reddit (engineering subs), well-cited blogs | Current opinions, ecosystem trends, practical tips |
| **T4 — Last resort** | Random tutorials, Medium articles, LLM-generated content | Background only — always cross-check with T1/T2 |

> Never cite T3/T4 as the sole source for a technical decision. Always pair with a T1 primary source.

---

## 4. Parallel Search Strategy

```
STEP 1 — PARALLEL (T1 sources):
  ├── context7 (library docs — structured, version-aware)
  └── websearch (broad web + community)

STEP 2 — webfetch (T1/T2 specific URLs):
  ├── Known docs page or GitHub README
  ├── Stack Overflow accepted answer
  └── GitHub issue / discussion

STEP 3 — ONLY IF NEEDED (T3):
  └── websearch with site:reddit.com or site:news.ycombinator.com

→ Synthesize after each step; stop when enough evidence gathered.
```

For known URLs, use `webfetch` directly. For search results that return URLs, `webfetch` the most promising ones for full content.

---

## 5. Result Format

Always return structured findings:

```markdown
## Research: {TOPIC}

**Answer**: [Direct answer, 1-2 sentences]

**Confidence**: High / Medium / Low
**Sources**:
| URL | Tier | Key Takeaway |
|-----|------|-------------|
| [official docs](url) | T1 | Confirms pattern X |
| [SO answer](url) | T2 | 342 votes — accepted fix |
| [GitHub issue #123](url) | T2 | Fixed in v2.1.0 |

**Caveats**: [Version-specific warnings, conflicting evidence, stale info]
```

---

## 6. Quality Checklist

Before finalizing, verify:

- [ ] **Recency** — info still valid? Flag anything >3 years old in fast-moving fields (JS/TS, LLMs, cloud infra).
- [ ] **Version alignment** — does the answer match the project's library/major version?
- [ ] **Primary over secondary** — prefer official docs over tutorials that re-explain them.
- [ ] **Confidence calibrated** — T3/T4 sources downgrade confidence. Single source = Low.
- [ ] **No hallucinated URLs** — only cite URLs from actual fetch results or officially documented patterns.
```
