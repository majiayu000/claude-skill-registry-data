---
name: Report Writer
version: 1.0.0
description: Generates professional reports from research and data
category: writing
tools:
  - document_generation
  - formatting
input_schema:
  title:
    type: string
    description: Report title
  content:
    type: string
    description: Main content/findings
  style:
    type: string
    enum: [technical, business, academic]
    default: business
  include_toc:
    type: boolean
    default: true
output_format: markdown
estimated_tokens: 3000
author: SkillsFlow
tags:
  - writing
  - reporting
  - documentation
---

# Report Writer Skill

## Purpose
Transform research, analysis, and data into polished, professional reports in multiple formats.

## Supported Styles

### Technical
For technical audiences - includes diagrams, code samples, specifications

### Business
For business executives - focuses on ROI, metrics, recommendations

### Academic
For academic contexts - includes citations, methodology, peer review readiness

## How It Works
1. Parse title, content, and style parameters
2. Structure content with appropriate sections
3. Add table of contents if requested
4. Format according to style guide
5. Return complete report markdown

## Example Usage

```
Title: "Q4 2025 Performance Report"
Content: "Company achieved 150% growth in sales..."
Style: business
Include TOC: true
```

## Output Includes
- Professional header
- Table of contents (optional)
- Well-organized sections
- Executive summary
- Recommendations/conclusions
- Appendices if needed

## Constraints
- Maximum 50,000 characters input
- 20-second generation timeout
- Output is markdown formatted
- Ready for PDF conversion

## Report Quality
✓ Professional formatting
✓ Clear section hierarchy
✓ Appropriate for stakeholders
✓ Publication-ready
