---
name: create-prd
description: Generate comprehensive Product Requirements Documents for web and mobile apps using lean startup methodology. Perfect for solo entrepreneurs and new product concepts. Creates hypothesis-driven PRDs with MVP focus, user stories, and technical specifications. Exports to multiple formats including Markdown, HTML, and DOCX. Use when planning new products, defining MVPs, or documenting product vision for AI coding assistants.
---

# Create PRD - Lean Product Requirements Document Generator

This skill helps you create comprehensive, lean Product Requirements Documents (PRDs) optimized for solo entrepreneurs and rapid product development. It follows lean startup principles to help you document your product vision, validate assumptions, and communicate requirements clearly to AI coding assistants or future collaborators.

## Quick Start

To create a new PRD, run:
```bash
python scripts/init_prd.py
```

This will guide you through an interactive process to define your product and generate a complete PRD.

## Core Workflow

### 1. Initialize Your PRD
Start with the interactive script that asks targeted questions:
```bash
python scripts/init_prd.py --type [consumer-app|b2b-saas|marketplace|custom]
```

### 2. Generate Lean Canvas (Optional)
Create a one-page business model:
```bash
python scripts/generate_lean_canvas.py
```

### 3. Create User Stories
Transform features into INVEST-compliant user stories:
```bash
python scripts/create_user_stories.py
```

### 4. Export Your PRD
Generate multiple output formats:
```bash
python scripts/export_prd.py --format [md|html|docx|all]
```

## PRD Structure

Your PRD will include these essential sections:

### Essential Sections (Always Included)
1. **Executive Summary** - Problem, solution, and value proposition
2. **Target Users** - Primary persona and jobs to be done  
3. **MVP Scope** - Core features and success criteria
4. **User Stories** - INVEST-compliant stories with acceptance criteria
5. **Technical Overview** - Platform, stack, and integration requirements

### Optional Sections (Based on Your Needs)
- Competitive Analysis
- Revenue Model
- Marketing Strategy
- Detailed User Flows
- Design Requirements

## Templates Available

- `lean_prd_template.md` - Default lean startup template
- `consumer_app_template.md` - Optimized for B2C mobile/web apps
- `b2b_saas_template.md` - Enterprise-focused features
- `marketplace_template.md` - Two-sided marketplace dynamics

## Key Features

### For Solo Founders
- **Question-driven process** - Extracts the right information through targeted questions
- **Hypothesis tracking** - Document and validate assumptions
- **MVP-focused** - Emphasizes core features over feature creep
- **Pivot-friendly** - Easy to update when changing direction

### For AI Coding
- **AI-optimized format** - Works seamlessly with Claude Code, Cursor, Windsurf
- **Clear specifications** - Unambiguous requirements for AI interpretation
- **Technical clarity** - Explicit about integrations and dependencies

## Using the Interactive PRD Builder

The `init_prd.py` script will guide you through:

1. **Problem Definition**
   - What problem are you solving?
   - Who experiences this problem?
   - What evidence do you have?

2. **Solution Approach**
   - Core value proposition
   - Key differentiators
   - Solution hypothesis

3. **User Definition**
   - Primary user persona
   - Early adopter characteristics
   - User goals and needs

4. **MVP Features**
   - 3-5 core features maximum
   - Priority ranking
   - Success metrics

5. **Technical Requirements**
   - Platform selection (web/mobile/both)
   - Key technical constraints
   - Required integrations

## Best Practices

### Keep It Lean
- Start with the problem, not the solution
- Focus on learning over perfection
- Document hypotheses explicitly
- Define clear success metrics

### Write for Clarity
- Use simple, direct language
- Avoid jargon and ambiguity
- Include concrete examples
- Specify acceptance criteria

### Think MVP
- Maximum 5 core features for v1
- Each feature must serve the core value prop
- Defer "nice to have" features
- Define "done" clearly

## Export Formats

### Markdown (Default)
- Perfect for GitHub repositories
- Easy to version control
- Universal compatibility

### HTML
- Shareable via browser
- Includes formatting and styling
- Good for stakeholder review

### DOCX
- Compatible with Google Docs
- Easy to edit and comment
- Professional presentation

### Raw Outputs
All exports are saved to `/outputs/` directory for easy upload to any platform.

## Workflow Tips

### For New Products
1. Start with `init_prd.py` using the `--type` flag
2. Answer all questions (use "TBD" if unsure)
3. Review generated PRD
4. Iterate based on feedback
5. Export when ready

### For AI Coding Sessions
1. Generate PRD with clear technical specs
2. Export as Markdown
3. Provide to AI coding assistant
4. Reference specific sections during development

### For Validation
1. Create initial PRD with hypotheses
2. Build MVP based on PRD
3. Gather user feedback
4. Update PRD with learnings
5. Plan next iteration

## Command Reference

```bash
# Start new PRD
python scripts/init_prd.py

# With specific template
python scripts/init_prd.py --type marketplace

# Generate lean canvas
python scripts/generate_lean_canvas.py

# Create user stories from features
python scripts/create_user_stories.py --input features.txt

# Export to all formats
python scripts/export_prd.py --format all

# Export to specific format
python scripts/export_prd.py --format md --output my-product-prd.md
```

## Need More Detail?

For specific aspects of PRD creation, see the reference guides:
- `references/lean_methodology.md` - Lean startup principles
- `references/mvp_planning.md` - Defining your MVP
- `references/user_story_guide.md` - Writing effective user stories
- `references/tech_stack_selector.md` - Choosing your technology
- `references/api_integration_guide.md` - Documenting integrations
