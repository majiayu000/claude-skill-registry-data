---
name: marp-image-generator
description: Generate optimized images for Marp slides using Playwright MCP with theme-matching color palettes and guideline-compliant sizes
---

# Marp Image Generator Skill

## Overview

This skill generates images optimized for Marp presentations (16:9 format) using Playwright MCP. It creates HTML-based diagrams with theme-matching color palettes (canyon-custom or github-dark) and converts them to PNG screenshots at guideline-compliant sizes.

## When to Use

- User needs to create diagrams, charts, or visual content for Marp slides
- User wants images that match the presentation theme (canyon-custom or github-dark)
- User requires specific sizes following the Marp image size guideline
- User needs comparison charts, info panels, or process diagrams

## Workflow

### Step 1: Determine Image Specifications

**Image Size Reference** (from `docs/spec/marp/image-size-guideline.md`):

| Use Case | Recommended Size | Aspect Ratio |
|----------|-----------------|--------------|
| Full-size image | 1216px × 582px | 2.09:1 |
| Safe area (recommended) | 1100px × 550px | 2:1 |
| 16:9 image | 1034px × 582px | 16:9 |
| Two-column (per image) | 550px × 400px | 1.375:1 |
| imageCenter | 900px × 600px | 3:2 |
| imageFull | 1280px × 720px | 16:9 |
| Retina (2x) | 2200px × 1100px | 2:1 |

**Most Common Use Cases:**
- **General diagrams**: 1100px × 550px (safe area)
- **Comparison layouts**: 550px × 400px (two-column)
- **Full-screen impact**: 1280px × 720px (imageFull)

### Step 2: Select Color Theme

**Canyon-Custom Theme Colors:**
- Primary: `#d4ed00` (yellow-green)
- Secondary: `#333333` (dark gray)
- Accent: `#00bcd4` (cyan)
- Background: `#ffffff` (white)
- Box colors:
  - Blue box: `#d4ed00` border on `#f0f7d8` background
  - Green box: `#01ad09` border on `#dbecdc` background
  - Yellow box: `#b47800` border on `#f5f0c6` background
  - Red box: `#ad0140` border on `#f0dce3` background

**GitHub-Dark Theme Colors:**
- Primary BG: `#0d1117`
- Secondary BG: `#161b22`
- Tertiary BG: `#21262d`
- Text Primary: `#f0f6fc`
- Text Secondary: `#7d8590`
- Border: `#30363d`
- Accent: `#1f6feb` (blue)
- Success: `#238636` (green)
- Danger: `#da3633` (red)
- Warning: `#9e6a03` (yellow)

**Design Principle**: **NO GRADIENTS** - Use solid colors and subtle color variations only

### Step 3: Create HTML Diagram

HTML files should be saved to `application/marp/src/html/` with this template:

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagram Title</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        'sans': ['"Hiragino Sans"', '"ヒラギノ角ゴシック"', '"Yu Gothic"', '"游ゴシック"', '"Noto Sans JP"', 'sans-serif']
                    },
                    colors: {
                        // Canyon-Custom theme colors
                        'canyon-primary': '#d4ed00',
                        'canyon-secondary': '#333333',
                        'canyon-accent': '#00bcd4',
                        'canyon-bg': '#ffffff',
                        'canyon-box-blue': '#f0f7d8',
                        'canyon-box-green': '#dbecdc',
                        'canyon-box-yellow': '#f5f0c6',
                        'canyon-box-red': '#f0dce3',

                        // GitHub-Dark theme colors
                        'gh-bg-primary': '#0d1117',
                        'gh-bg-secondary': '#161b22',
                        'gh-bg-tertiary': '#21262d',
                        'gh-text-primary': '#f0f6fc',
                        'gh-text-secondary': '#7d8590',
                        'gh-border': '#30363d',
                        'gh-accent': '#1f6feb',
                        'gh-success': '#238636',
                        'gh-danger': '#da3633',
                        'gh-warning': '#9e6a03',
                    }
                }
            }
        }
    </script>
    <style>
        body {
            width: 1100px;  /* Adjust based on target size */
            height: 550px;
        }
    </style>
</head>
<body class="bg-white font-sans flex items-center justify-center p-10">
    <!-- Canyon-Custom example -->
    <!-- For GitHub-Dark: change class to "bg-gh-bg-primary text-gh-text-primary" -->

    <div class="w-full h-full">
        <!-- Diagram content here -->
    </div>
</body>
</html>
```

**Naming Convention**: Use snake_case (e.g., `comparison_chart.html`, `workflow_diagram.html`)

### Step 4: Open in Browser and Resize

Use Playwright MCP:

```
Navigate to: file:///home/node/workspace/application/marp/src/html/[filename].html
```

**Browser Resize** (set body width/height to match target dimensions):
- For 1100×550: body width=1100px, height=550px
- For 1280×720: body width=1280px, height=720px
- Browser viewport can be larger (e.g., 1920×1080)

### Step 5: Take Screenshot

Use `mcp__playwright__browser_take_screenshot`:
- `filename`: `application/marp/src/assets/[diagram-name].png`
- `type`: `png`
- `fullPage`: `false` (capture viewport only for exact size)

**IMPORTANT - Move to Correct Location**:
After taking screenshot, ALWAYS move from Playwright MCP directory to assets directory:
```bash
mv /home/node/workspace/.playwright-mcp/application/marp/src/assets/[diagram-name].png /home/node/workspace/application/marp/src/assets/[diagram-name].png
```

### Step 6: Use in Marp Slides

```markdown
![Diagram Title](src/assets/diagram-name.png)
```

## Design Templates

### Template 1: Two-Column Comparison (Canyon-Custom)

**Target Size**: 1100px × 550px
**Use Case**: Before/After, Pros/Cons

```html
<body class="bg-white text-canyon-secondary font-sans flex items-center justify-center p-10">
    <div class="w-full h-full flex gap-10">
        <div class="flex-1 border-3 border-canyon-primary bg-canyon-box-blue p-8 flex flex-col rounded-lg">
            <h2 class="text-canyon-primary text-3xl font-bold mb-5 border-b-2 border-canyon-primary pb-2">
                Before
            </h2>
            <ul class="list-none text-xl leading-relaxed space-y-2">
                <li class="flex items-start">
                    <span class="text-canyon-primary mr-3">●</span>
                    <span>Item 1</span>
                </li>
                <li class="flex items-start">
                    <span class="text-canyon-primary mr-3">●</span>
                    <span>Item 2</span>
                </li>
                <li class="flex items-start">
                    <span class="text-canyon-primary mr-3">●</span>
                    <span>Item 3</span>
                </li>
            </ul>
        </div>
        <div class="flex-1 border-3 border-canyon-primary bg-canyon-box-blue p-8 flex flex-col rounded-lg">
            <h2 class="text-canyon-primary text-3xl font-bold mb-5 border-b-2 border-canyon-primary pb-2">
                After
            </h2>
            <ul class="list-none text-xl leading-relaxed space-y-2">
                <li class="flex items-start">
                    <span class="text-canyon-primary mr-3">●</span>
                    <span>Item 1</span>
                </li>
                <li class="flex items-start">
                    <span class="text-canyon-primary mr-3">●</span>
                    <span>Item 2</span>
                </li>
                <li class="flex items-start">
                    <span class="text-canyon-primary mr-3">●</span>
                    <span>Item 3</span>
                </li>
            </ul>
        </div>
    </div>
</body>
```

### Template 2: Info Panel (GitHub-Dark)

**Target Size**: 1100px × 550px
**Use Case**: Feature highlights, key points

```html
<body class="bg-gh-bg-primary text-gh-text-primary font-sans flex items-center justify-center p-10">
    <div class="w-full h-full flex items-center justify-center">
        <div class="bg-gh-bg-secondary border-2 border-gh-accent border-l-8 p-10 rounded-lg max-w-4xl">
            <h1 class="text-gh-accent text-5xl font-bold mb-8">
                Key Features
            </h1>
            <ul class="list-none text-3xl leading-loose space-y-4">
                <li class="flex items-start">
                    <span class="text-gh-success text-4xl mr-4">✓</span>
                    <span>Feature 1</span>
                </li>
                <li class="flex items-start">
                    <span class="text-gh-success text-4xl mr-4">✓</span>
                    <span>Feature 2</span>
                </li>
                <li class="flex items-start">
                    <span class="text-gh-success text-4xl mr-4">✓</span>
                    <span>Feature 3</span>
                </li>
            </ul>
        </div>
    </div>
</body>
```

### Template 3: Process Steps (Canyon-Custom)

**Target Size**: 1100px × 550px
**Use Case**: Workflow, step-by-step guide

```html
<body class="bg-white text-canyon-secondary font-sans flex items-center justify-center p-10">
    <div class="w-full h-full flex items-center justify-between px-5">
        <div class="flex-1 text-center p-5">
            <div class="w-20 h-20 bg-canyon-primary text-canyon-secondary rounded-full flex items-center justify-center text-4xl font-bold mx-auto mb-5">
                1
            </div>
            <div class="text-2xl font-bold mb-2">Plan</div>
            <div class="text-lg text-gray-600">Define requirements</div>
        </div>

        <div class="text-6xl text-canyon-accent">→</div>

        <div class="flex-1 text-center p-5">
            <div class="w-20 h-20 bg-canyon-primary text-canyon-secondary rounded-full flex items-center justify-center text-4xl font-bold mx-auto mb-5">
                2
            </div>
            <div class="text-2xl font-bold mb-2">Build</div>
            <div class="text-lg text-gray-600">Implement features</div>
        </div>

        <div class="text-6xl text-canyon-accent">→</div>

        <div class="flex-1 text-center p-5">
            <div class="w-20 h-20 bg-canyon-primary text-canyon-secondary rounded-full flex items-center justify-center text-4xl font-bold mx-auto mb-5">
                3
            </div>
            <div class="text-2xl font-bold mb-2">Test</div>
            <div class="text-lg text-gray-600">Verify quality</div>
        </div>
    </div>
</body>
```

### Template 4: Centered Message (GitHub-Dark)

**Target Size**: 1280px × 720px (imageFull)
**Use Case**: Section divider, key message

```html
<style>
    body {
        width: 1280px;
        height: 720px;
    }
</style>
</head>
<body class="bg-gh-bg-primary text-gh-text-primary font-sans flex items-center justify-center">
    <div class="h-full flex flex-col items-center justify-center text-center">
        <h1 class="text-7xl font-bold mb-8 text-gh-text-primary">
            Main Message
        </h1>
        <div class="w-52 h-1.5 bg-gh-accent my-8"></div>
        <p class="text-4xl text-gh-text-secondary max-w-4xl">
            Supporting description goes here
        </p>
    </div>
</body>
```

## Design Guidelines

### Color Usage Rules

**Canyon-Custom Theme:**
- Primary accent: `#d4ed00` (use for borders, headings, icons)
- Secondary accent: `#00bcd4` (use for highlights, links)
- Background: `#ffffff` or light tints (`#f0f7d8`, `#dbecdc`)
- Text: `#333333` (dark gray, never pure black)

**GitHub-Dark Theme:**
- Primary accent: `#1f6feb` (use for borders, headings, links)
- Success/positive: `#238636` (use for checkmarks, success states)
- Warning: `#9e6a03` (use for caution, alerts)
- Danger: `#da3633` (use for errors, critical info)
- Background: Layer with `#0d1117`, `#161b22`, `#21262d`
- Text: `#f0f6fc` (primary), `#7d8590` (secondary)

### Typography

- **Heading sizes**: 32px - 72px
- **Body text**: 18px - 28px
- **Small text**: 14px - 16px
- **Font weight**: Normal (400) or Bold (600-700)

### Spacing

- **Padding**: 20px - 40px
- **Gaps**: 20px - 40px
- **Margins**: 10px - 30px
- **Border width**: 2px - 8px

### No Gradient Policy

**Avoid:**
- ❌ `linear-gradient()`
- ❌ `radial-gradient()`
- ❌ Multiple color stops

**Use Instead:**
- ✅ Solid colors
- ✅ Layered backgrounds with different opacity
- ✅ Adjacent color blocks

## User Request Templates

### Template: Create Diagram

```
Create a Marp image diagram using the marp-image-generator skill.

**Content**:
- Type: [comparison / info-panel / process / message]
- Title: [Title]
- Elements:
  - [Element 1]
  - [Element 2]
  - [Element 3]

**Theme**: [canyon-custom / github-dark]

**Size**: [1100x550 / 1280x720 / 550x400]

**Reference**: @docs/spec/marp/image-size-guideline.md

**Output**:
- HTML: application/marp/src/html/[filename].html
- PNG: application/marp/src/assets/[filename].png
```

## Troubleshooting

### Issue 1: Colors Don't Match Theme

**Cause**: Using incorrect color codes

**Solution**:
- Refer to theme CSS files:
  - Canyon-Custom: `application/marp/theme/canyon-custom.css`
  - GitHub-Dark: `application/marp/theme/github-dark.css`
- Use exact hex codes from color palette

### Issue 2: Image Size Incorrect

**Cause**: Body dimensions not matching target size

**Solution**:
- Set `body { width: XXXpx; height: YYYpx; }` to exact target dimensions
- Use `fullPage: false` when taking screenshot

### Issue 3: Text Too Small/Large

**Cause**: Font sizes not optimized for target dimensions

**Solution**:
- For 1100×550: Use 24-36px for headings, 18-24px for body
- For 1280×720: Use 48-72px for headings, 28-36px for body
- Test and adjust based on visual balance

### Issue 4: Gradients Detected

**Cause**: Using `linear-gradient()` or `radial-gradient()`

**Solution**:
- Replace with solid colors
- Use layered `<div>` elements with different background colors
- Use border colors for visual separation

## Best Practices

1. **Use Tailwind CSS**: Leverage Tailwind utility classes for faster development
2. **Custom Theme Colors**: Use the extended color palette (canyon-*, gh-*) for theme consistency
3. **Keep It Simple**: One diagram = one concept
4. **Color Consistency**: Stick to theme palette
5. **Size Accuracy**: Match exact dimensions from guideline (1100×550 default)
6. **No Gradients**: Use solid colors and borders only
7. **Move to Correct Location**: Always move (not copy) from `.playwright-mcp/` to `application/marp/src/assets/` to keep directories clean
8. **Test on Slide**: Verify the image looks good in actual Marp presentation

## Related Resources

- **Image Size Guideline**: `docs/spec/marp/image-size-guideline.md`
- **Marp Implementation Guide**: `application/marp/CLAUDE.md`
- **Theme Files**: `application/marp/theme/`
- **Existing HTML Examples**: `application/marp/src/html/`
- **Playwright MCP Setup**: `docs/features/tool-playwright-mcp-setup/`

## Permissions Required

This skill requires Playwright MCP configured in `.mcp.json`:

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
