---
name: research-agent
description: >
  Systematic deep research methodology using multiple sources. USE when: researching
  SOTA techniques, comparing libraries/frameworks, finding best practices, verifying
  claims, investigating bugs via GitHub issues, technical due diligence, literature review.
  Trigger: "research X", "find the best way to Y", "what's the SOTA for Z", "compare A vs B",
  "is X still maintained". Combines web, GitHub, docs and codebase sources.
metadata:
  version: "1.0.0"
  category: "Research"
  sources: ["Karpathy research methodology", "auto-research.instructions.md"]
---

# Skill: Research Agent

## Research Protocol

### Step 1: Decompose the query
```
Query: "best free LLM for code generation 2026"

Decompose into:
- What: free LLMs (no cost inference)
- Domain: code generation (function, debug, complete)
- Constraint: 2026 (recent, not outdated)
- Implicit: API vs local, speed vs quality
```

### Step 2: Source hierarchy (search in parallel)

| Priority | Source | Tool | What to look for |
|----------|--------|------|-----------------|
| 1 | Codebase | semantic_search, grep | Existing patterns, prior art |
| 2 | Official docs | fetch_webpage | Latest API, breaking changes |
| 3 | GitHub | fetch_webpage issues/discussions | Known bugs, community solutions |
| 4 | Community | fetch_webpage (SO, Reddit, Discord) | Real-world experiences |
| 5 | Registries | npm/PyPI/crates.io | Popularity, maintenance status |

### Step 3: Validate findings

Validation checklist:
- [ ] Date check: is this < 6 months old? If not, verify still valid
- [ ] Version check: compatible with project's pinned versions?
- [ ] Cross-reference: confirmed by ≥ 2 independent sources?
- [ ] Author credibility: official docs > known experts > anonymous posts

### Step 4: Synthesize

```
Structure output as:
1. TL;DR (1 sentence answer)
2. Recommendation (with rationale)
3. Key findings (3-5 bullet points)
4. Trade-offs (pros/cons table)
5. Sources (cited with date)
6. Next steps (actionable)
```

## Research Templates

### Technology comparison
```
Compare [A] vs [B] for [use case]:

| Criteria | A | B |
|----------|---|---|
| Performance | | |
| Cost | | |
| Community | | |
| Maintenance | | |
| License | | |
| Learning curve | | |

Recommendation: [A/B] because [reason]
```

### SOTA research
```
SOTA for [topic] as of [date]:

State of the art:
- Best approach: [name] — [why]
- Performance benchmark: [metric] = [value]
- Key paper: [authors, venue, year]
- Production-ready implementation: [repo/package]

Recent game changers:
- [paper/technique]: changes [what] by [how much]

What's still open:
- [challenge 1]
- [challenge 2]
```

### GitHub issue investigation
```
Bug: [description]

Search: GitHub issues → repo/issues?q=[keywords]

Findings:
- Issue #[N]: [title] — Status: [open/closed/PR merged]
- Fix: [commit/PR link]
- Workaround: [if applicable]

Root cause: [explanation]
Solution: [steps]
```

## Query Optimization for AI Research

Use these search patterns for better results:

```bash
# Web search — specific and recent
"[technology] [problem] site:github.com 2025"
"[library] best practices [year]"
"[error message] fix [language]"

# GitHub issues
"repo:[owner/repo] [keyword] is:issue"
"[error] in:title is:closed"

# Docs
"[library] [version] [feature] docs"
```

## Anti-Patterns in Research
- ❌ Trust first result only → ✅ Cross-reference 3+ sources
- ❌ Use outdated tutorials (2020-2022 for fast-moving domains) → ✅ Check dates
- ❌ Skip official docs → ✅ Official docs first for API accuracy
- ❌ Research without codebase check → ✅ Check existing patterns first
- ❌ Deep research for simple facts → ✅ Match depth to complexity

## ZeroClaw Integration
```bash
# Trigger deep research SOP
zeroclaw agent -m "hint:smart research: what's the best free embedding model for RAG in 2026?"

# Research + store in memory
zeroclaw agent -m "research zeroclaw provider rotation patterns and save findings to memory"
```
