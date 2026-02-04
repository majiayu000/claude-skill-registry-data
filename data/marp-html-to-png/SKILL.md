---
name: marp-html-to-png
description: Create HTML diagrams for Marp slides and capture them as PNG screenshots using Playwright MCP
---

# Marp HTML to PNG Skill

## Overview

This skill helps create interactive HTML diagrams for Marp presentations and converts them to PNG screenshots using Playwright MCP. HTML files are created in `application/marp/src/html/` and screenshots are saved to `application/marp/src/assets/`.

## When to Use

- User needs to create visual diagrams for Marp slides
- User wants to convert HTML/CSS diagrams to static images
- User requests comparison charts, flowcharts, or interactive visualizations for presentations
- User needs to update existing HTML diagrams and regenerate screenshots

## Workflow

### Step 1: Create HTML Diagram

HTML files should be saved to `application/marp/src/html/` with the following template structure:

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>図解タイトル</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        'sans': ['"Noto Sans JP"', 'sans-serif']
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 min-h-screen flex items-center justify-center font-sans overflow-hidden">
    <!-- Diagram content -->
    <!-- IMPORTANT: DO NOT include diagram title in HTML - Marp slides will add titles -->
</body>
</html>
```

**Naming Convention**: Use snake_case for HTML files (e.g., `fullscreen_comparison.html`, `pdca_cycle.html`)

**IMPORTANT - No Titles in Diagrams**:
- Do NOT include diagram titles (h1, h2, etc.) in the HTML content
- Marp slides will add titles separately
- Focus only on the visual content/diagram itself

### Step 2: Open HTML File in Browser

Use Playwright MCP to navigate to the local HTML file:

```
file:///home/node/workspace/application/marp/src/html/[filename].html
```

**Browser Resize** (IMPORTANT - Follow Marp Image Size Guideline):
- **Default**: Width: 1100px, Height: 550px (Safe area size - recommended)
- Alternative: Width: 1216px, Height: 582px (Full content area)
- Reference: `docs/spec/marp/image-size-guideline.md`

### Step 3: Take Screenshot

Use the `mcp__playwright__browser_take_screenshot` tool with:
- `filename`: `application/marp/src/assets/[diagram-name].png`
- `type`: `png`
- **IMPORTANT**: After taking screenshot, ALWAYS move from `.playwright-mcp/application/marp/src/assets/` to `application/marp/src/assets/` using:
  ```bash
  mv /home/node/workspace/.playwright-mcp/application/marp/src/assets/[diagram-name].png /home/node/workspace/application/marp/src/assets/[diagram-name].png
  ```

### Step 4: Use in Marp Slides

Reference the screenshot in Marp markdown:

```markdown
![図解タイトル](src/assets/diagram-name.png)
```

## Design Guidelines

### Recommended Sizes (Follow Marp Image Size Guideline)

**IMPORTANT**: All HTML diagrams should be designed to fit within Marp's safe area size.

- **Recommended (Default)**: 1100px × 550px (Safe area size)
  - Use this for most diagrams
  - Set HTML `body` to: `width: 1100px; height: 550px;`
  - Browser viewport: `1100px × 550px`

- **Full Content Area**: 1216px × 582px
  - Use only when you need maximum space
  - Set HTML `body` to: `width: 1216px; height: 582px;`
  - Browser viewport: `1216px × 582px`

- **Reference**: `docs/spec/marp/image-size-guideline.md`

### Background Styles

**Light Background**:
```html
<body class="bg-white min-h-screen p-8">
```

**Dark Gradient Background**:
```html
<body class="bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 min-h-screen flex items-center justify-center">
```

### Font Sizes
- **Title**: `text-6xl` (60px)
- **Subtitle**: `text-4xl` (36px)
- **Body**: `text-2xl` (24px)
- **Small**: `text-xl` (20px)

### Color Palette
- **Success/Positive**: `green-500`, `green-300`
- **Warning/Negative**: `red-500`, `red-300`
- **Info**: `blue-500`, `blue-300`
- **Highlight**: `yellow-400`, `orange-500`

## Examples

### Example 1: Comparison Diagram

**Existing Reference**: `application/marp/src/html/fullscreen_comparison.html`

Features:
- 2-column layout (Before vs After)
- Dark gradient background
- Icons with bullet points
- Circular progress meters

### Example 2: PDCA Cycle

**Existing Reference**: `application/marp/src/html/pdca_cycle.html`

Features:
- White background
- Center-aligned layout
- SVG circular arrows
- 4-card layout (Plan, Do, Check, Action)

## User Request Templates

### Template 1: Create HTML Diagram

```
Create an HTML diagram for a Marp slide.

**Content**:
- Title: [Title]
- Elements:
  - [Element 1]
  - [Element 2]
  - [Element 3]

**Design**:
- Layout: [2-column / centered / grid]
- Background: [light / dark gradient]
- Color scheme: [success=green / warning=red]

**Reference**: @application/marp/src/html/fullscreen_comparison.html

**Save to**: application/marp/src/html/[filename].html
```

### Template 2: Take Screenshot

```
Open the HTML diagram and take a screenshot:

**HTML File**:
file:///home/node/workspace/application/marp/src/html/[filename].html

**Browser Size** (Follow Marp Image Size Guideline):
- Width: 1100px
- Height: 550px

**Screenshot Options**:
- Save to: application/marp/src/assets/[diagram-name].png
- Type: PNG

**Post-Screenshot**:
Move file from Playwright MCP directory to assets directory:
```bash
mv /home/node/workspace/.playwright-mcp/application/marp/src/assets/[diagram-name].png /home/node/workspace/application/marp/src/assets/[diagram-name].png
```
```

## Troubleshooting

### Issue 1: HTML File Not Displaying

**Cause**: Incorrect file path

**Solution**:
- Use `file://` protocol
- Absolute path: `/home/node/workspace/application/marp/src/html/[filename].html`

### Issue 2: Screenshot Size Not Matching Guidelines

**Cause**: Browser viewport not following Marp image size guideline

**Solution**:
- Use `mcp__playwright__browser_resize` tool
- **Default**: width=1100, height=550 (Safe area size - recommended)
- Alternative: width=1216, height=582 (Full content area)
- Reference: `docs/spec/marp/image-size-guideline.md`

### Issue 3: Fonts Not Rendering

**Cause**: Japanese fonts not loaded

**Solution**:
- Ensure Tailwind config includes font family (see template)
- Use system fonts: Hiragino Sans, Yu Gothic

### Issue 4: Colors Not Matching

**Cause**: Incorrect Tailwind class names

**Solution**:
- Check Tailwind docs for correct color classes
- Use prefixes: `bg-`, `text-`, `border-`

## Best Practices

1. **Follow Size Guidelines**: Always use 1100px × 550px (default) or 1216px × 582px (full area)
2. **Keep It Simple**: One diagram = one concept
3. **Reusability**: Template similar layouts
4. **Accessibility**: Ensure sufficient contrast (minimum 4.5:1)
5. **Performance**: Use emojis instead of external images
6. **Consistency**: Follow existing HTML diagram patterns
7. **Move to Correct Location**: Always move (not copy) screenshot from `.playwright-mcp/` to `application/marp/src/assets/` to keep directories clean

## Permissions Required

This skill requires Playwright MCP to be configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headless", "--isolated"]
    }
  }
}
```

## Related Resources

- **Existing HTML Diagrams**: `application/marp/src/html/`
- **Marp Implementation Guide**: `application/marp/CLAUDE.md`
- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **Playwright MCP Setup**: `docs/features/tool-playwright-mcp-setup/`
