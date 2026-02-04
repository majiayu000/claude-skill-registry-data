---
name: ia-presenter
description: Generate markdown presentations compatible with IA Presenter. Use when the user requests to create an IA Presenter presentation, generate an IA Presenter document, or convert content into an IA Presenter markdown file. Also use when the user asks to create a presentation in markdown format without specifying a tool.
---

# IA Presenter

## Overview

This skill generates markdown files formatted for IA Presenter, a presentation tool with specific markdown syntax requirements. IA Presenter uses standard markdown with unique conventions for slide separation, content visibility, and layout control.

## Core Syntax Rules

### Slide Structure

Use heading levels to control slide hierarchy:
- `# Title` and `## Subtitle` on the first slide create the cover page
- `---` separates slides
- `### Heading` creates content slide titles (always visible)

### Content Visibility

Control what appears on slides using tab characters:
- Lines starting with a **tab character** appear on the slide
- Lines without tabs are speaker notes (invisible to audience)
- Headings always appear and don't need tabs

**Critical:** Use actual tab characters (`\t`), not the tab symbol or spaces.

### Layout Control

Create side-by-side layouts by separating tabbed content with a non-tabbed line:
```
	Left panel content

	Right panel content
```

Without the separator, content stacks vertically.

## Creating Presentations

### Standard Structure

Follow this typical flow:
1. Cover slide (# Title, ## Subtitle)
2. Executive summary or key message slide
3. Content slides with concise points
4. Conclusion or next steps slide

### Content Guidelines

Keep text minimal and impactful:
- Use bullets and short phrases over paragraphs
- Focus on keywords that reinforce spoken content
- Avoid long sentences that distract from the presenter
- Prioritize visuals (images, graphs) when available

### Gathering Information

Before generating, ask clarifying questions:
- Presentation topic and target audience
- Key messages or objectives
- Number of slides needed
- Whether images are available (and what they depict)
- Any specific content structure preferences

### Images

Handle images as follows:
- All image paths start with `/assets/`
- Example: `/assets/myimage.jpg`
- Use `size: contain` on the line after the image path to fit the full image
- If user provides images, ask what each depicts to place appropriately
- If no images provided, skip image syntax (user will add later)

### Formatting

Standard markdown works within IA Presenter:
- `**bold**` for bold text
- `*italic*` for italic text
- `[link text](url)` for hyperlinks
- Backtick code blocks with optional language: ` ```python `
- Ordered lists: `1.`, `2.`, etc.
- Unordered lists: `-` or `*`

## Output Format

Always create a `.md` file in `/mnt/user-data/outputs/` with the IA Presenter formatted content.

## Reference Example

See `references/Example_IA_Presenter_Deck.md` for a complete working example demonstrating all syntax features.

## Additional Resources

Full IA Presenter markdown documentation: https://ia.net/presenter/support/basics/markdown
