---
name: academic-writing
description: |
  学术论文写作技能。辅助撰写论文各个章节，包括摘要、引言、方法、
  结果、讨论等。支持多种写作风格和输出格式。
triggers:
  - 写论文
  - write paper
  - 论文写作
  - 撰写论文
  - draft paper
  - academic writing
domain: academic_writing
version: "1.0"
---

# Academic Writing Skill

## Overview
Assists researchers in writing academic papers with proper structure, style, and citations.

## Trigger Conditions
- User requests to write or draft a paper
- Section-specific writing (abstract, introduction, etc.)
- Paper revision and editing tasks

## Workflow

### Step 1: Outline Generation
Create structured outline based on:
- Research topic and findings
- Target journal/venue
- Paper type (research, review, case study)

### Step 2: Section Composition
Write each section following academic conventions:

**Script**: `scripts/compose_section.py`

#### Section Templates
- Abstract (structured: background, methods, results, conclusion)
- Introduction (context, gap, contribution)
- Methods (reproducible description)
- Results (clear presentation)
- Discussion (interpretation, limitations, future work)
- Conclusion (summary, implications)

### Step 3: Citation Integration
- Insert citations at appropriate points
- Format according to target style (APA, IEEE, etc.)
- Generate bibliography

## Output Format
```json
{
  "section": "introduction",
  "content": "Markdown formatted text...",
  "citations": ["[1]", "[2]"],
  "word_count": 500
}
```

## Best Practices
1. Start with clear research question
2. Support claims with evidence
3. Maintain consistent terminology
4. Use active voice where appropriate
5. Avoid jargon when possible
