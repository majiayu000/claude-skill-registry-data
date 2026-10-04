---
name: screenshot
description: Take screenshots of web pages for blog posts, documentation, and marketing. Capture full pages, specific elements, dark mode, and custom dimensions.
allowed-tools: Bash, Read, Write
env:
  - SCREENSHOT_OUTPUT_DIR
---

# Screenshot Skill

Take screenshots of web pages for use in blog posts, documentation, and marketing content.

## Quick Usage

```bash
bun .claude/skills/screenshot/scripts/screenshot.ts <url> <output-filename>
```

### Examples

```bash
# Screenshot a web page
bun .claude/skills/screenshot/scripts/screenshot.ts https://example.com page-screenshot.webp

# Screenshot with custom dimensions
bun .claude/skills/screenshot/scripts/screenshot.ts https://example.com wide-shot.webp --width=1400 --height=900

# Screenshot in dark mode
bun .claude/skills/screenshot/scripts/screenshot.ts https://example.com dark-mode.webp --dark

# Full page screenshot
bun .claude/skills/screenshot/scripts/screenshot.ts https://example.com full-page.webp --full

# Screenshot a specific element
bun .claude/skills/screenshot/scripts/screenshot.ts https://example.com header.webp --selector="header"
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--width` | 1200 | Viewport width in pixels |
| `--height` | 800 | Viewport height in pixels |
| `--dark` | false | Enable dark mode |
| `--wait` | 2000 | Wait time in ms after page load |
| `--full` | false | Capture full page (scrollable) |
| `--selector` | null | Screenshot specific element only |

## Dependencies

Install required packages before using:

```bash
bun add playwright sharp
npx playwright install chromium
```

## First-Time Setup

If playwright browsers aren't installed, run:

```bash
npx playwright install chromium
```

## Use Cases

1. **Feature Screenshots** - Show new UI features in blog posts
2. **Before/After** - Document improvements with visual comparisons
3. **Tutorial Steps** - Capture each step of a process
4. **Product Demos** - Showcase actual product in articles
5. **Social Cards** - Generate images for social media sharing

## Tips

- Use `--wait=3000` for pages with animations
- Use `--dark` to match dark mode screenshots
- Use `--selector` to focus on specific UI elements
- WebP format provides best quality/size ratio
