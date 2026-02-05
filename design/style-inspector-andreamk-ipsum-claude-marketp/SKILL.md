---
name: Style Inspector
description: Use when needing to extract CSS styles from a DOM element, inspect computed styles, check font-size/color/margin of elements, or analyze visual styling of a web page. Requires a CSS selector to target the element.
version: 1.0.0
---

# Style Inspector

Extract CSS styles (inline or computed) from DOM elements on a web page.

## Overview

This skill retrieves CSS styles from elements after the page has fully rendered. It can return either inline styles directly on the element or computed styles (the final calculated values after all CSS rules are applied).

## When to Use

- Check the actual font-size, color, or spacing of an element
- Debug CSS styling issues on a live page
- Extract styling information for replication or analysis
- Verify computed values differ from inline/stylesheet values

## Parameters

- **url** (required): The URL of the page
- **selector** (required): CSS selector to target the element
- **properties** (optional): Comma-separated list of CSS properties to return (e.g., `font-size,color,margin`). If omitted with `--computed`, returns all computed styles.
- **--computed** (optional flag): Return computed styles instead of inline styles

## Implementation

Use the `style-inspector.js` script with Puppeteer to extract styles. The script is in the plugin's shared `scripts/` directory.

### Pre-execution Check

Before running the script, check if `node_modules` exists in the plugin's scripts directory. If not, install dependencies:

```bash
# Check and install if needed (run from plugin root)
[ -d "scripts/node_modules" ] || (cd scripts && npm install)
```

### Basic Usage

Run from plugin root directory:

Get inline styles of an element:
```bash
node scripts/style-inspector.js "https://example.com" "h1"
```

Get specific computed styles:
```bash
node scripts/style-inspector.js "https://example.com" "h1" "font-size,color,margin" --computed
```

Get all computed styles (warning: long output):
```bash
node scripts/style-inspector.js "https://example.com" "h1" --computed
```

### Script Location

The script is located at `scripts/style-inspector.js` in the plugin root directory (shared across skills).

## Output

Returns JSON with the requested styles:

```json
{
  "selector": "h1",
  "styles": {
    "font-size": "32px",
    "color": "rgb(0, 0, 0)",
    "margin": "0px"
  }
}
```

## Error Handling

- Invalid URL: Report the URL format error
- Selector not found: Report that the selector matched no elements
- Page load timeout: Report timeout and suggest retrying
- Missing dependencies: Run pre-execution check to install
