---
name: "doc-gap-analyzer"
description: "Automated documentation coverage analysis and gap detection for the Documentation department. Scans codebase for undocumented APIs, stale docs, missing examples, and knowledge graph gaps. Produces prioritized documentation targets. Use when auditing doc coverage, finding undocumented code, planning doc sprints, or running the documentation UAOP pipeline."
risk: low
tags: [documentation, quality, coverage, analysis]
created: 2026-03-23
updated: 2026-03-23
---

# Doc Gap Analyzer — Documentation Department Intelligence Engine

Find what's undocumented, what's stale, and what users can't find. UAOP Stage 1 + Stage 5 for Documentation.

## When to use

- Before releases — "is everything documented?"
- After new features — "what docs need updating?"
- Quarterly doc health review
- Onboarding review — "can a new person get started?"

## Pipeline

### Step 1: Coverage Scan
- Compare public API endpoints against doc pages (every endpoint needs a doc)
- Compare Python public functions against docstrings
- Check CLAUDE.md / README age vs last code change
- Verify all skills have SKILL.md files
- Check knowledge graph freshness (memory MCP entities)

### Step 2: Staleness Detection
- Docs modified > 90 days ago while code changed → flag as stale
- Code examples that reference deprecated APIs → flag as broken
- Links that return 404 → flag for fix

### Step 3: Gap Classification
| Gap Type | Priority |
|----------|----------|
| Public API with no docs | P0 |
| Stale docs (code changed, docs didn't) | P1 |
| No onboarding guide | P1 |
| Missing code examples | P2 |
| Broken internal links | P2 |
| Knowledge graph gaps (orphan entities) | P3 |

### Step 4: Produce Gap Report
- Coverage metrics (% of APIs documented, % of functions with docstrings)
- Top 10 gaps by priority
- Staleness report (docs that need refresh)
- Trend: improving or regressing?

### Step 5: Self-Improvement Loop
- Track doc-to-code sync ratio over time
- Measure onboarding time (proxy for doc quality)
- Auto-generated docs that need zero editing → template as standard

## Cadence
```
WEEKLY:   Staleness scan + broken link check
MONTHLY:  Full coverage report
QUARTERLY: Onboarding review + doc strategy update
```

## Agents
| Agent | Role |
|-------|------|
| repo-index (L0) | Scans codebase structure |
| knowledge-graph-guide (L0) | Checks knowledge graph completeness |
| documenter (L6) | Writes docs targeting gaps |
| technical-writer (L6) | Reviews doc quality |
