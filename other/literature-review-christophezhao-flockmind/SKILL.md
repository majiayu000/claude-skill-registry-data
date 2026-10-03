---
name: literature-review
description: |
  科研文献综述技能。当用户提到"综述"、"survey"、"find papers"、
  "文献调研"、"文献检索"时自动触发。支持多数据源检索和结果综合。
triggers:
  - 综述
  - survey
  - find papers
  - 文献调研
  - 文献检索
  - review papers
  - 调研
domain: academic_writing
version: "1.0"
---

# Literature Review Skill

## Overview
This skill helps researchers conduct comprehensive literature reviews by searching multiple academic databases and synthesizing findings.

## Trigger Conditions
- User mentions "文献综述", "综述", "survey"
- Tasks involving academic paper search and analysis
- Requests for research background investigation

## Workflow

### Step 1: Query Understanding
Analyze the user's research topic and extract key concepts:
- Main research area
- Specific focus or questions
- Time range preferences
- Language preferences

### Step 2: Multi-Source Search
Execute searches across multiple databases:
- ArXiv (preprints, latest research)
- Semantic Scholar (comprehensive coverage)

**Script**: `scripts/search_papers.py`

### Step 3: Result Synthesis
Aggregate and analyze search results:
- Deduplicate papers across sources
- Rank by relevance and citations
- Identify key themes and gaps

See: `SEARCH_STRATEGIES.md` for advanced techniques
See: `SYNTHESIS_GUIDE.md` for synthesis methodology

## Output Format
```json
{
  "query": "original search query",
  "papers": [
    {
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "year": 2024,
      "summary": "Brief abstract",
      "url": "https://...",
      "relevance": "high"
    }
  ],
  "synthesis": {
    "themes": ["Theme 1", "Theme 2"],
    "gaps": ["Gap 1"],
    "recommendations": ["Recommendation 1"]
  }
}
```

## Best Practices
1. Start with broad searches, then narrow down
2. Cross-reference findings across sources
3. Prioritize recent, highly-cited papers
4. Look for review articles first for overview
