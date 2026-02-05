---
name: research-and-synthesis
description: Fetch and summarize authoritative external sources into actionable guidance. EXCLUSIVE to researcher agent.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---
# Research and Synthesis

**Exclusive to:** `researcher` agent

## Instructions

1. Understand project stack from `docs/project-overview-pdr.md`
2. Define the research question clearly
3. Fetch 1-3 authoritative sources
4. Verify with multiple sources
5. Summarize actionable findings

## Source Evaluation

| Criteria | ✅ Good | ❌ Bad |
|----------|---------|--------|
| Recency | < 1 year | > 2 years |
| Authority | Official docs | Random blogs |
| Relevance | Same stack | Different framework |

## Research Process

1. Define the question clearly
2. Fetch 1-3 authoritative sources
3. Verify with multiple sources
4. Summarize actionable findings

## Package Evaluation

| Factor | Check |
|--------|-------|
| Maintenance | Last commit < 6 months |
| Compatibility | Works with Laravel 12 / React 19 |
| Documentation | Clear docs, examples |
| Security | No known vulnerabilities |

## Comparison Matrix

```markdown
| Criteria | Option A | Option B |
|----------|----------|----------|
| Implementation | ⭐⭐⭐ | ⭐⭐ |
| Performance | ⭐⭐ | ⭐⭐⭐ |
| Security | ⭐⭐⭐ | ⭐⭐ |
```

## Output Template

```markdown
## Summary
[2-3 sentences]

## Key Findings
- Finding 1
- Finding 2

## Recommendation
[Which option and why]

## References
- [Source](url)
```

## Examples
- "Confirm best practice for Laravel validation"
- "Compare package A vs package B"
