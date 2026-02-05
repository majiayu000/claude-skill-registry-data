---
name: template-slide-deck
description: Generate professional slide decks using company-provided template presentations. Use this skill when the user wants to create a presentation based on their own branded PowerPoint template, company slide deck template, or organizational design standards. Triggers include requests like "create slides using our template", "make a presentation with our company format", "generate a deck from this template", or "build slides matching our brand". Also use when the user asks to create slides and has uploaded or mentioned a template .pptx file.
---

# Template-Based Slide Deck Generator

Generate professional presentations by applying content to company-provided PowerPoint templates. This skill ensures brand consistency by using the organization's established slide designs.

## Workflow Overview

1. **Prompt for template** (required) - Obtain the template .pptx file
2. **Prompt for content** (required unless context available) - Gather content to populate slides
3. **Delegate to pptx skill** - Use the template-based workflow from `/mnt/skills/public/pptx/SKILL.md`

## Step 1: Prompt for Template

**Always ask for the template first.** The template contains the company's slide layouts, colors, fonts, and design standards.

Prompt:
```
To create your presentation, I'll need your company's PowerPoint template file (.pptx) that contains your branded slide layouts.

Please upload the template slide deck. This should be a .pptx file containing example slides showing your organization's approved layouts (title slides, content slides, section dividers, etc.).
```

**If user provides a URL instead of a file:** Attempt to fetch it, but inform them that direct file upload is preferred for best results.

**If user says they don't have a template:** Offer to create a presentation from scratch without a template (this falls back to the standard pptx skill workflow).

## Step 2: Determine Content Source

Check for existing context before prompting. Use this decision tree:

### Scenario A: Rich context exists in conversation
If the conversation preceding this skill invocation contains substantial content that could populate a presentation (e.g., a document summary, meeting notes, research findings, project plan):

```
I see you've been working on [describe the content]. Would you like me to create a slide deck based on this content using your template?

If yes, please upload your company's PowerPoint template (.pptx).

If you'd like to provide different content for the slides, let me know.
```

### Scenario B: No substantial context
If the conversation is fresh or lacks content suitable for slides:

```
Now I need the content for your presentation. Please provide one of the following:

- **Text content**: Paste or describe what you want on each slide
- **Document**: Upload a document (Word, PDF, text) to extract content from  
- **Outline**: Provide bullet points or a structured outline
- **Topic**: Give me a topic and key points to develop into slides

What would you like your presentation to cover?
```

## Step 3: Execute Template-Based Creation

Once both template AND content are available:

1. **Read the pptx skill**: `view /mnt/skills/public/pptx/SKILL.md`
2. **Follow the "Creating a new PowerPoint presentation using a template" workflow** exactly
3. Key steps from that workflow:
   - Create thumbnail grids to analyze template
   - Build template inventory
   - Map content to appropriate template slides
   - Use rearrange.py to duplicate/order slides
   - Extract text inventory with inventory.py
   - Generate replacement JSON
   - Apply with replace.py
   - Validate output visually

## Content-to-Slide Mapping Guidelines

When mapping user content to template slides:

- **Title/Cover slide**: Use for presentation title and subtitle/date
- **Section dividers**: Use to separate major topics
- **Text-heavy layouts**: Match to detailed explanations or multiple bullet points
- **Two-column layouts**: Use for comparisons or paired concepts
- **Image + text layouts**: Only use when user provides actual images
- **Quote layouts**: Reserved for actual attributable quotes

**Content length considerations:**
- Count the user's key points before selecting layouts
- Don't force 4 items into a 3-column layout
- Split dense content across multiple slides rather than overcrowding

## Handling Edge Cases

**User uploads wrong file type:**
```
That file doesn't appear to be a PowerPoint template (.pptx). Please upload a .pptx file containing your company's slide layouts.
```

**Template has very few layouts:**
```
This template has [N] unique layouts. For your [M] content sections, I'll need to reuse some layouts. I'll select the most appropriate layout for each section.
```

**Content exceeds template capacity:**
```
Your content has more sections than distinct template layouts. I'll create additional slides by duplicating the most suitable layouts. The presentation will maintain visual consistency.
```

**User wants to modify template styling:**
Direct them to work with the template file first, or note that significant style changes would require editing the template itself rather than just populating it.
