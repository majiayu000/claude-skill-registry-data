---
name: ui-check
description: Use Playwright MCP to check UI styles and usability. Automatically used for requests like "check UI", "verify appearance", "take screenshot", "UI review", "screenshot analysis".
context: fork
agent: Explore
allowed-tools:
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - Bash
  - Read
---

# UI Check Skill

Use Playwright MCP to verify UI styles and usability.

## Usage

### 1. Launch Browser
```
Navigate to target URL with mcp__playwright__browser_navigate
```

### 2. Take Screenshot
```
Take screenshot with mcp__playwright__browser_screenshot
```

### 3. Resize Image (Required)

Always resize screenshots with ImageMagick before analyzing in Claude Code.

```bash
# Resize to 1024px width
magick screenshot.png -resize 1024x .claude/tmp/screenshots/resized.png
```

### 4. UI Analysis

Load resized image and analyze:
- Layout verification
- Style verification
- Accessibility verification
- Usability verification

## Check Perspectives

### Layout
- Is element placement appropriate?
- Is responsive design appropriate?
- Are margins/spacing consistent?

### Style
- Is color usage appropriate?
- Are fonts readable?
- Are icons appropriate?

### Accessibility
- Is contrast ratio sufficient?
- Are focus states clear?
- Is text size appropriate?

### Usability
- Is operation intuitive?
- Is feedback clear?
- Are error states understandable?

## Output

```markdown
# UI Check Result

## Screenshot
[Image path]

## Results

### Good Points
- ...

### Improvement Suggestions
- ...

## Recommended Actions
- ...
```

## Notes
- Save screenshots to `.claude/tmp/screenshots/`
- Always resize with `magick` command before analysis
- Using large images directly may cause crashes
