---
name: slide-gen-content
description: "AI-powered content drafting, quality analysis, and optimization for presentation slides. Generates titles, bullets, speaker notes, and graphics descriptions."
version: "2.0.0"
author: "davistroy"
---

# Content Generation Skill

Generates and optimizes presentation content using Claude API with quality analysis.

## Capabilities

- **Content Drafting**: Generate titles, bullets, speaker notes, graphics descriptions
- **Quality Analysis**: 5-dimension scoring (readability, tone, structure, redundancy, citations)
- **Content Optimization**: Automated improvement with before/after tracking
- **Graphics Validation**: Ensure descriptions are specific enough for image generation

## Usage

### Draft Content
```bash
python -m plugin.cli draft-content outline.md --output content.md
```

### Analyze Quality

```bash
python -m plugin.cli analyze-quality content.md
```

### Optimize Content

```bash
python -m plugin.cli optimize-content content.md --output optimized.md
```

## Quality Dimensions

| Dimension   | Weight | Description                               |
|-------------|--------|-------------------------------------------|
| Readability | 25%    | Flesch-Kincaid score, sentence complexity |
| Tone        | 20%    | Consistency, audience appropriateness     |
| Structure   | 20%    | Parallel construction, logical flow       |
| Redundancy  | 15%    | Duplicate content detection               |
| Citations   | 20%    | Source attribution, evidence support      |

## Output Format

Content is output as Markdown with frontmatter:

```markdown
---
title: "Presentation Title"
author: "Generated"
date: "2026-01-04"
template: "stratfield"
quality_score: 8.5
---

# Slide 1: Introduction

## Title
Welcome to AI in Healthcare

## Bullets
- Point one with supporting detail
- Point two with evidence
- Point three with citation [1]

## Speaker Notes
Detailed notes for the presenter...

## Graphics Description
A modern hospital lobby with digital displays showing patient data dashboards...
```
