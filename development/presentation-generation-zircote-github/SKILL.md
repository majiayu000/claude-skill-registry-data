---
name: presentation-generation
description: Generate slide deck presentations from prompts. Triggers on "create presentation", "generate slides", "build deck", "presentation about"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Task
---

# Presentation Generation Skill

Generate professional slide deck presentations from prompts, with support for research, project analysis, and multiple output formats.

## Trigger Phrases

- "create presentation about..."
- "generate slides for..."
- "build a deck on..."
- "presentation for [audience]..."
- "slides covering..."
- "pitch deck for..."

## Workflow Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   1. RESEARCH   │────▶│   2. OUTLINE    │────▶│   3. CONTENT    │
│   (Optional)    │     │   Generation    │     │   Expansion     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
┌─────────────────┐     ┌─────────────────┐            │
│   5. OUTPUT     │◀────│   4. DESIGN     │◀───────────┘
│   Generation    │     │   Application   │
└─────────────────┘     └─────────────────┘
```

## Directory Structure

```
docs/presentations/
├── templates/
│   ├── systematic-velocity.py      # Dark, data-focused style
│   ├── clean-minimal.py            # Light, professional style
│   ├── technical-blueprint.py      # Diagram-heavy style
│   └── marketing-bold.py           # High-contrast CTA style
├── output/
│   ├── [presentation-name].pdf
│   ├── [presentation-name].pptx
│   └── [presentation-name]/        # HTML reveal.js
│       ├── index.html
│       └── assets/
├── drafts/
│   └── [presentation-name].md      # Markdown source
└── assets/
    ├── fonts/
    ├── images/
    └── brand/
```

## Presentation Markdown Format

```markdown
---
title: "Presentation Title"
subtitle: "Optional Subtitle"
author: "Author Name"
date: 2025-12-29
style: systematic-velocity
format:
  - pdf
  - html
  - pptx
---

# Section Title
<!-- New section marker -->

---
<!-- Slide separator -->

## Slide Title

- Bullet point 1
- Bullet point 2
- Bullet point 3

::: notes
Speaker notes go here. Not visible on slides.
:::

---

## Slide with Metrics

<!-- metric: value="3,504%" label="Year 1 ROI" -->
<!-- metric: value="95%" label="Time Saved" -->
<!-- metric: value="2 weeks" label="Payback Period" -->

---

## Slide with Code

```python
# Code blocks are syntax highlighted
def example():
    return "Hello, World!"
```

---

## Slide with Image

![Alt text](assets/diagram.png)

---

## Slide with Columns

::: columns
:::: column
Left column content
::::
:::: column
Right column content
::::
:::

---

# Thank You

<!-- cta: text="Get Started" url="https://github.com/zircote/github" -->
```

## Research Phase

### Web Search Research
```bash
# Triggered when research sources include "Web Search"
# Uses WebSearch tool for latest information

Topics to research:
- [Topic 1 from prompt]
- [Topic 2 from prompt]
- Latest developments in [field]
```

### GitHub Repository Analysis
```bash
# Analyze repository structure
gh repo view owner/repo --json name,description,stargazerCount,forkCount

# Get recent activity
gh api repos/owner/repo/stats/commit_activity

# List recent releases
gh release list --repo owner/repo --limit 5

# Analyze issues/PRs
gh issue list --repo owner/repo --state all --limit 20 --json title,state,labels
gh pr list --repo owner/repo --state all --limit 20 --json title,state,labels
```

### Project Documentation Analysis
```bash
# Read key files
cat README.md
cat docs/COMPREHENSIVE_GUIDE.md
find . -name "*.md" -path "./docs/*" | head -20
```

## Design Styles

### Systematic Velocity (Default)
- **Background**: Deep charcoal (#1A1A1A)
- **Accent**: Coral (#DA7756)
- **Text**: Off-white (#EBEBEB)
- **Typography**: Inter (body), JetBrains Mono (code/metrics)
- **Elements**: Geometric grids, node clusters, metric blocks

### Clean Minimal
- **Background**: White (#FFFFFF)
- **Accent**: Blue (#2563EB)
- **Text**: Charcoal (#1F2937)
- **Typography**: Inter (all)
- **Elements**: Generous whitespace, subtle shadows

### Technical Blueprint
- **Background**: Dark blue (#0F172A)
- **Accent**: Cyan (#06B6D4)
- **Text**: Light gray (#E2E8F0)
- **Typography**: Fira Code (all)
- **Elements**: Grid lines, connection diagrams, code blocks

### Marketing Bold
- **Background**: White (#FFFFFF)
- **Accent**: Vibrant gradient (purple→pink)
- **Text**: Dark (#111827)
- **Typography**: Poppins (bold headings), Inter (body)
- **Elements**: Large CTAs, high contrast, testimonials

## Generation Commands

### Generate from Markdown
```bash
# PDF output
uv run --with reportlab,Pillow python docs/presentations/generate.py \
  --input docs/presentations/drafts/my-presentation.md \
  --output docs/presentations/output/my-presentation.pdf \
  --format pdf \
  --style systematic-velocity

# HTML (Reveal.js) output
uv run --with jinja2 python docs/presentations/generate.py \
  --input docs/presentations/drafts/my-presentation.md \
  --output docs/presentations/output/my-presentation/ \
  --format html \
  --style systematic-velocity

# PowerPoint output
uv run --with python-pptx,Pillow python docs/presentations/generate.py \
  --input docs/presentations/drafts/my-presentation.md \
  --output docs/presentations/output/my-presentation.pptx \
  --format pptx \
  --style systematic-velocity

# All formats
uv run python docs/presentations/generate.py \
  --input docs/presentations/drafts/my-presentation.md \
  --output docs/presentations/output/ \
  --format all \
  --style systematic-velocity
```

## Slide Templates

### Title Slide
```markdown
---

# {title}

## {subtitle}

{author} | {date}

---
```

### Problem/Opportunity Slide
```markdown
---

## The Challenge

> "Quote highlighting the pain point"

- Problem statement 1
- Problem statement 2
- Problem statement 3

<!-- visual: icon="warning" -->

---
```

### Solution Slide
```markdown
---

## The Solution

**{Product/Feature Name}**

{One-line value proposition}

::: columns
:::: column
### Before
- Manual process
- Error-prone
- Time-consuming
::::
:::: column
### After
- Automated
- Reliable
- Fast
::::
:::

---
```

### Metrics/ROI Slide
```markdown
---

## Results

<!-- metric: value="95%" label="Time Saved" size="large" -->
<!-- metric: value="3,504%" label="ROI" size="large" -->
<!-- metric: value="$109K" label="Annual Value" size="large" -->

---
```

### Feature Grid Slide
```markdown
---

## Key Features

::: grid cols="3"
- **Feature 1**: Description
- **Feature 2**: Description
- **Feature 3**: Description
- **Feature 4**: Description
- **Feature 5**: Description
- **Feature 6**: Description
:::

---
```

### CTA Slide
```markdown
---

## Get Started Today

<!-- cta: text="Try It Free" url="https://..." primary="true" -->
<!-- cta: text="View Documentation" url="https://..." -->

**Contact**: email@example.com

---
```

## Validation Checklist

Before generating final output:

- [ ] Title slide has title, subtitle (optional), author, date
- [ ] Problem/opportunity clearly stated
- [ ] Solution directly addresses problem
- [ ] Features/benefits are specific (not generic)
- [ ] Metrics are accurate and sourced
- [ ] Visual hierarchy is clear (one main point per slide)
- [ ] Speaker notes included for complex slides
- [ ] CTA is clear and actionable
- [ ] Total slide count matches target
- [ ] All images have alt text
- [ ] Code samples are tested and correct
- [ ] Brand colors/fonts applied consistently

## Integration with GitHub Issues

When triggered from a GitHub issue:

1. Parse issue body for structured fields
2. Extract presentation requirements
3. Perform research based on selected sources
4. Generate outline and seek approval (comment on issue)
5. Generate full presentation
6. Attach outputs to issue or create PR
7. Close issue with summary

```bash
# Triggered by workflow on issue labeled "presentation"
gh issue view $ISSUE_NUMBER --json body,title | jq -r '.body' > request.json

# Process and generate
python docs/presentations/generate_from_issue.py --issue request.json

# Attach output
gh issue comment $ISSUE_NUMBER --body "Presentation generated! See attached files."
```

## Related Skills

- `content-pipeline` - For blog/social content extraction from presentations
- `template-creation` - For custom presentation templates
- `ai-tuning` - For optimizing AI-generated content
