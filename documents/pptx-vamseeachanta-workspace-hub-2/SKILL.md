---
name: pptx
description: PowerPoint presentation toolkit for creating new presentations, editing
  existing ones, and using templates. Supports HTML-to-PPTX conversion, slide manipulation,
  and professional design. Use when building presentations, slide decks, or visual
  reports.
type: reference
version: 1.1.0
last_updated: 2026-01-02
category: data
related_skills:
- docx
- pdf
- xlsx
capabilities: []
requires: []
tags: []
---

# Pptx

## Overview

This skill provides three primary workflows for PowerPoint manipulation: creating from scratch, editing existing presentations, and using templates.

## Quick Start

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Add title slide
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title_slide.shapes.title.text = "My Presentation"
title_slide.placeholders[1].text = "By Claude"

prs.save("presentation.pptx")
```

## When to Use

- Creating automated presentation reports
- Building slide decks from data
- Generating pitch presentations
- Converting HTML content to slides
- Adding charts and tables to presentations
- Batch processing multiple presentations
- Updating existing presentations programmatically
- Creating consistent branded presentations from templates

## Version History

- **1.1.0** (2026-01-02): Added Quick Start, When to Use, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with python-pptx, templates, OOXML editing

## Sub-Skills

- [Execution Checklist](execution-checklist/SKILL.md)
- [Error Handling](error-handling/SKILL.md)
- [Metrics](metrics/SKILL.md)
- [Quick Reference](quick-reference/SKILL.md)
- [Dependencies](dependencies/SKILL.md)

## Sub-Skills

- [Basic Creation with python-pptx (+3)](basic-creation-with-python-pptx/SKILL.md)
- [Before Writing Code (+1)](before-writing-code/SKILL.md)
- [Read and Modify (+2)](read-and-modify/SKILL.md)
- [Apply Template](apply-template/SKILL.md)
- [Unpack Presentation (+2)](unpack-presentation/SKILL.md)
