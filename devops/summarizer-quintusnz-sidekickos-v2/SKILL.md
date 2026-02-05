---
name: Summarizer
version: 1.0.0
description: Summarizes large text content into concise summaries
category: analysis
tools:
  - text_analysis
  - nlp
input_schema:
  content:
    type: string
    description: Text content to summarize
  style:
    type: string
    enum: [bullet-points, paragraphs, executive-summary]
    default: bullet-points
  max_length:
    type: number
    description: Maximum length in words
    default: 500
output_format: markdown
estimated_tokens: 1000
author: SkillsFlow
tags:
  - summarization
  - analysis
  - content-processing
---

# Summarizer Skill

## Purpose
Convert large blocks of text into concise, well-organized summaries while preserving key information.

## How It Works
1. Analyze the input text for key themes
2. Identify main points and supporting details
3. Remove redundancy and unnecessary information
4. Organize summary in requested format
5. Return formatted summary

## Supported Styles

### Bullet Points
Quick overview with key facts as bullets

### Paragraphs
Narrative summary in paragraph form

### Executive Summary
Professional summary with key takeaways

## Example Usage

```
Input: "Long research paper about climate change..."
Style: executive-summary
Max Length: 300 words
Output: Professional summary of findings
```

## Constraints
- Maximum 30,000 character input
- Output respects max_length parameter
- Preserves factual accuracy
- 15-second timeout

## Quality Metrics
✓ Captures 80%+ of original meaning
✓ Reduces length by 60-80%
✓ Well-structured output
✓ No information loss on key points

## Use Cases
- Research paper summarization
- Meeting notes compression
- Document review
- Content curation
