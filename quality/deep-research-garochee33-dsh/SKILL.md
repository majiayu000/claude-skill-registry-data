---
name: deep-research
version: "2.0"
description: Deep multi-source research synthesis — web, academic, patent, and internal KB cross-referencing
trigger: deep research, research synthesis, literature review, patent search, competitive analysis, intelligence gathering
---

# Deep Research Skill v2.0

## Purpose
Conduct thorough multi-source research across web, academic databases, patent systems, and internal Trinity KB, then synthesize findings into actionable intelligence.

## Capabilities
- Multi-source parallel search (Tavily, arXiv, PubMed, Semantic Scholar, Wikipedia, OEIS)
- Patent landscape analysis
- Competitive intelligence gathering
- Academic literature review and citation mapping
- Internal KB cross-referencing for existing knowledge
- Executive summary generation with confidence scores

## Research Protocol
1. **Scope**: Define research question, constraints, and target depth
2. **Search**: Fan out to 3+ sources in parallel
3. **Filter**: Rank by relevance, recency, and authority
4. **Synthesize**: Cross-reference findings, identify patterns and contradictions
5. **Report**: Structured output with citations, confidence levels, and knowledge gaps

## Agents
- **Researcher** (primary): Deep web and academic search
- **Oracle**: Internal KB and data intelligence
- **Prophet**: Strategic pattern recognition

## Tools
- `deep_web_search` (Tavily), `research_topic`
- `patent_search`, `arxiv_search`, `pubmed_search`, `semantic_scholar_search`
- `wikipedia_lookup`, `wolfram_alpha_query`
- `search_vault` (internal KB)

## Quality Gates
- Minimum 3 independent sources for any factual claim
- All citations must include URL/DOI
- Confidence scoring: HIGH (3+ corroborating sources), MEDIUM (2), LOW (1)
- Research reports must include "Knowledge Gaps" section

## Protocol

1. **Assess** — Understand the specific requirement and context
2. **Plan** — Determine the approach based on the guidance above
3. **Execute** — Apply the deep research methodology
4. **Verify** — Validate the output against expected standards
5. **Report** — Document results and any issues encountered

## Integration

This skill is available via:
- `invoke_skill("deep-research")` in the agent kernel
- `POST /api/skills/invoke` with `skillId: "deep-research"`
- Semantic search via `GET /api/skills/search?q=deep+research`
