---
name: researching
description: Comprehensive research with cited sources. Use for complex research that should be verified and persist.
---

# Researching

Produce well-sourced research artifacts with verified citations.

## When to Use

- Complex research requiring multiple sub-queries
- Need documented research that persists beyond conversation
- Topic requires source verification and confidence calibration
- High-stakes decisions that need cited evidence

**Don't use for**: Quick lookups. Just search directly.

## Artifact Requirements

- **Minimum 3 independent evidence bundles** per research topic
- Each bundle must cite primary sources with URLs
- Source diversity required: official docs, peer-reviewed, reputable secondary
- Academic citations must be validated with `bibval`

## Quality Rubric

| Criterion | Requirement |
|-----------|-------------|
| **Citations** | Every claim has inline citation with URL |
| **Coverage** | Key perspectives included (not just first result) |
| **Recency** | Sources current (≤2 years for APIs/tech, flexible for fundamentals) |
| **Confidence** | Calibrated honestly; uncertainties stated explicitly |
| **Conflicts** | Disagreements between sources noted, not hidden |

## Source Credibility Hierarchy

Weight findings by source authority:

1. **Official documentation** - canonical, highest weight
2. **Peer-reviewed papers** - validated, high weight
3. **Reputable blogs/talks** - expert authors, medium weight
4. **Stack Overflow (accepted)** - community validated, medium weight
5. **Forums/unverified** - low weight, note uncertainty

## Output Schema

```json
{
  "topic": "string",
  "status": "COMPLETE | PARTIAL",
  "confidence": "HIGH | MEDIUM | LOW",
  "findings": [
    {
      "subtopic": "string",
      "content": "string with inline citations",
      "sources": ["url1", "url2"]
    }
  ],
  "sources": [
    {
      "url": "string",
      "title": "string",
      "authority": "official | peer-reviewed | blog | forum"
    }
  ],
  "gaps": ["string"]
}
```

## Constraints

- Prefer primary sources over secondary
- Cross-reference claims across multiple sources
- Flag single-source claims as lower confidence
- Run `bibval` on academic citations before including

## Recording Findings

Post research artifacts to jwz for persistence and discovery:

```bash
jwz post "research:<topic>" --role alice \
  -m "[alice] SYNTHESIS: <topic>
Status: COMPLETE | PARTIAL
Confidence: HIGH | MEDIUM | LOW
Findings:
- <finding 1>
- <finding 2>
Sources: <url1>, <url2>"
```

## Discovery

```bash
jwz search "SYNTHESIS:"
jwz search "FINDING:"
jwz read "research:<topic>"
```
