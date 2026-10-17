---
name: design-md-chrome-extractor
description: Chrome extension that extracts design systems from websites and generates DESIGN.md or SKILL.md files for AI coding agents using TypeUI format
triggers:
  - "extract design system from this website"
  - "generate a DESIGN.md file from webpage styles"
  - "create design skills from site CSS"
  - "build a TypeUI design markdown file"
  - "extract colors, typography, and spacing from this page"
  - "generate design tokens from website"
  - "create SKILL.md from design system"
  - "pull design foundations from active site"
---

# design-md-chrome-extractor

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

The TypeUI DESIGN.md Extractor is a Chrome extension that analyzes any website and extracts its design system (typography, colors, spacing, radius, shadows, motion) to generate standardized `DESIGN.md` or `SKILL.md` files. These files follow the open-source [TypeUI](https://www.typeui.sh/design-md) format and can be used with AI coding tools like Claude Code, Google Stitch, Codex, and Cursor to replicate design systems.

**Key capabilities:**
- Auto-extract design tokens from any webpage
- Generate DESIGN.md (design system documentation)
- Generate SKILL.md (AI agent-ready skills)
- Download extracted files for immediate use
- Refresh extraction on page state changes

## Installation

### From Chrome Web Store

Install directly from: https://chromewebstore.google.com/detail/designmd-style-extractor/ogpdnchdjiibhobphelbbkemnnemkfma

### Local Development Installation

1. Clone the repository:
```bash
git clone https://github.com/bergside/design-md-chrome.git
cd design-md-chrome
```

2. Load in Chrome:
   - Open `chrome://extensions`
   - Enable **Developer mode** (toggle in top-right)
   - Click **Load unpacked**
   - Select the `design-md-chrome` project folder

3. Verify installation:
   - Extension icon should appear in Chrome toolbar
   - Pin it for easy access

## Usage Patterns

### Basic Extraction Workflow

1. **Navigate** to target website (e.g., `https://stripe.com`)
2. **Click** the extension icon in toolbar
3. **Click** "Auto-extract" button
4. **Review** extracted design tokens in popup
5. **Generate** DESIGN.md or SKILL.md
6. **Download** the file

### Programmatic Extraction (Content Script)

The extension injects `content.js` which performs extraction:

```javascript
// Core extraction happens via message passing
chrome.runtime.sendMessage({
  action: 'extract',
  url: window.location.href
}, (response) => {
  console.log('Extracted tokens:', response.tokens);
});
```

### Style Token Structure

Extracted tokens follow this structure:

```javascript
{
  typography: {
    fontFamilies: ['Inter', 'system-ui', 'sans-serif'],
    fontSizes: ['12px', '14px', '16px', '20px', '24px', '32px'],
    fontWeights: ['400', '500', '600', '700'],
    lineHeights: ['1.2', '1.5', '1.6']
  },
  colors: {
    primary: ['#635BFF', '#0A2540'],
    neutral: ['#FFFFFF', '#F6F9FC', '#E3E8EE'],
    semantic: {
      success: '#00D924',
      error: '#DF1B41',
      warning: '#FFC043'
    }
  },
  spacing: ['4px', '8px', '12px', '16px', '24px', '32px', '48px', '64px'],
  radius: ['0px', '4px', '8px', '12px', '16px', '9999px'],
  shadows: [
    '0 1px 3px rgba(0,0,0,0.1)',
    '0 4px 6px rgba(0,0,0,0.1)',
    '0 10px 40px rgba(0,0,0,0.15)'
  ],
  motion: {
    durations: ['150ms', '200ms', '300ms', '500ms'],
    easings: ['ease', 'ease-in-out', 'cubic-bezier(0.4,0,0.2,1)']
  }
}
```

## Generated File Structure

### DESIGN.md Format

```markdown
# [Site Name] Design System

## Mission
Define and maintain consistent visual language for [product].

## Brand
- **URL**: https://example.com
- **Audience**: [Developers/Designers/General]
- **Surface**: Web application

## Style Foundations

### Typography
- Font families: Inter, system-ui
- Sizes: 12px, 14px, 16px, 20px, 24px, 32px
- Weights: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- Line heights: 1.2 (tight), 1.5 (base), 1.6 (relaxed)

### Colors
**Primary**
- `#635BFF` - Brand primary
- `#0A2540` - Dark navy

**Neutral**
- `#FFFFFF` - White
- `#F6F9FC` - Light gray
- `#E3E8EE` - Medium gray

### Spacing
Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px

### Radius
Values: 0px, 4px, 8px, 12px, 16px, 9999px (pill)

## Accessibility
- WCAG 2.2 AA compliance required
- Minimum contrast ratio 4.5:1 for text
- Focus indicators required on all interactive elements
```

### SKILL.md Format

Similar structure but optimized for AI agent consumption with additional sections:

- **Component Rule Expectations**: State, interaction, accessibility requirements
- **Quality Gates**: Testable validation criteria
- **Guideline Authoring Workflow**: Step-by-step implementation process

## Extension Architecture

### Manifest (manifest.json)

```json
{
  "manifest_version": 3,
  "name": "DESIGN.MD Style Extractor",
  "version": "1.0.0",
  "permissions": ["activeTab", "scripting"],
  "action": {
    "default_popup": "popup.html"
  },
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["content.js"]
  }]
}
```

### Message Passing Pattern

**Popup → Content Script:**
```javascript
// popup.js
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  chrome.tabs.sendMessage(tabs[0].id, {
    action: 'extractStyles'
  }, (response) => {
    displayTokens(response.tokens);
  });
});
```

**Content Script → Background:**
```javascript
// content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractStyles') {
    const tokens = extractDesignTokens();
    sendResponse({tokens});
  }
});
```

## API Reference

### Extension Actions

| Action | Description | Response |
|--------|-------------|----------|
| `extractStyles` | Scan page for design tokens | `{tokens: Object}` |
| `generateDesignMD` | Create DESIGN.md content | `{markdown: String}` |
| `generateSkillMD` | Create SKILL.md content | `{markdown: String}` |
| `refresh` | Re-run extraction | `{tokens: Object}` |
| `download` | Trigger file download | `{success: Boolean}` |

### Core Extraction Functions

```javascript
// Extract all computed styles from page
function extractDesignTokens() {
  const allElements = document.querySelectorAll('*');
  const tokens = {
    typography: new Set(),
    colors: new Set(),
    spacing: new Set(),
    radius: new Set(),
    shadows: new Set()
  };
  
  allElements.forEach(el => {
    const computed = window.getComputedStyle(el);
    
    // Extract typography
    tokens.typography.add(computed.fontFamily);
    tokens.typography.add(computed.fontSize);
    tokens.typography.add(computed.fontWeight);
    
    // Extract colors
    if (computed.color !== 'rgba(0, 0, 0, 0)') {
      tokens.colors.add(computed.color);
    }
    if (computed.backgroundColor !== 'rgba(0, 0, 0, 0)') {
      tokens.colors.add(computed.backgroundColor);
    }
    
    // Extract spacing
    ['margin', 'padding'].forEach(prop => {
      ['Top', 'Right', 'Bottom', 'Left'].forEach(side => {
        const value = computed[prop + side];
        if (value !== '0px') tokens.spacing.add(value);
      });
    });
    
    // Extract border radius
    if (computed.borderRadius !== '0px') {
      tokens.radius.add(computed.borderRadius);
    }
    
    // Extract box shadows
    if (computed.boxShadow !== 'none') {
      tokens.shadows.add(computed.boxShadow);
    }
  });
  
  return normalizeTokens(tokens);
}

// Normalize and deduplicate tokens
function normalizeTokens(rawTokens) {
  return {
    typography: {
      fontFamilies: Array.from(rawTokens.typography).filter(isFontFamily),
      fontSizes: Array.from(rawTokens.typography).filter(isFontSize).sort(),
      fontWeights: Array.from(rawTokens.typography).filter(isFontWeight).sort()
    },
    colors: Array.from(rawTokens.colors).map(normalizeColor),
    spacing: Array.from(rawTokens.spacing).sort(numericalSort),
    radius: Array.from(rawTokens.radius).sort(numericalSort),
    shadows: Array.from(rawTokens.shadows)
  };
}
```

## Testing

Run the test suite:

```bash
node tests/run-tests.mjs
```

Test coverage includes:
- Token extraction accuracy
- Markdown generation validity
- Color normalization (rgb → hex)
- Spacing scale deduplication

## Common Patterns

### Extract and Save Workflow

```javascript
async function extractAndSave(format = 'DESIGN') {
  // 1. Extract tokens
  const tokens = await extractDesignTokens();
  
  // 2. Generate markdown
  const markdown = format === 'DESIGN' 
    ? generateDesignMD(tokens)
    : generateSkillMD(tokens);
  
  // 3. Download file
  const blob = new Blob([markdown], {type: 'text/markdown'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${format}.md`;
  a.click();
}
```

### Custom Token Filtering

```javascript
// Filter extracted colors by frequency
function filterFrequentColors(colors, minOccurrences = 5) {
  const colorMap = new Map();
  
  colors.forEach(color => {
    const normalized = normalizeColor(color);
    colorMap.set(normalized, (colorMap.get(normalized) || 0) + 1);
  });
  
  return Array.from(colorMap.entries())
    .filter(([_, count]) => count >= minOccurrences)
    .map(([color, _]) => color);
}
```

### Merge Multiple Extractions

```javascript
// Combine tokens from multiple pages
function mergeTokens(tokensArray) {
  return {
    typography: {
      fontFamilies: [...new Set(tokensArray.flatMap(t => t.typography.fontFamilies))],
      fontSizes: [...new Set(tokensArray.flatMap(t => t.typography.fontSizes))].sort(),
      fontWeights: [...new Set(tokensArray.flatMap(t => t.typography.fontWeights))].sort()
    },
    colors: [...new Set(tokensArray.flatMap(t => t.colors))],
    spacing: [...new Set(tokensArray.flatMap(t => t.spacing))].sort(numericalSort),
    radius: [...new Set(tokensArray.flatMap(t => t.radius))].sort(numericalSort),
    shadows: [...new Set(tokensArray.flatMap(t => t.shadows))]
  };
}
```

## Troubleshooting

### Extension Not Detecting Styles

**Issue**: Extracted tokens are empty or incomplete.

**Solutions**:
- Wait for page to fully load (including dynamic content)
- Refresh extraction after SPA navigation
- Check if styles are in Shadow DOM (requires additional traversal)
- Verify content script has injected: `chrome://extensions` → Inspect views

### Download Not Working

**Issue**: Generated file doesn't download.

**Solutions**:
```javascript
// Ensure proper blob MIME type
const blob = new Blob([content], {type: 'text/markdown;charset=utf-8'});

// Add fallback for different browsers
if (navigator.msSaveBlob) {
  navigator.msSaveBlob(blob, filename);
} else {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

### Duplicate Tokens

**Issue**: Multiple similar values extracted (e.g., `16px` and `16.5px`).

**Solution**:
```javascript
// Round to nearest whole pixel
function roundPixels(value) {
  const num = parseFloat(value);
  return Math.round(num) + 'px';
}

// Apply tolerance-based deduplication
function deduplicateWithTolerance(values, tolerance = 1) {
  return values.reduce((acc, val) => {
    const num = parseFloat(val);
    if (!acc.some(existing => Math.abs(parseFloat(existing) - num) < tolerance)) {
      acc.push(val);
    }
    return acc;
  }, []);
}
```

### Cross-Origin Restrictions

**Issue**: Cannot extract from iframe with different origin.

**Solution**: Extension permissions already include `<all_urls>`, but iframes require explicit traversal:

```javascript
function extractFromIframes() {
  const iframes = document.querySelectorAll('iframe');
  iframes.forEach(iframe => {
    try {
      const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
      // Extract from iframe document
      extractDesignTokens(iframeDoc);
    } catch (e) {
      console.warn('Cannot access iframe:', e);
    }
  });
}
```

## Integration with AI Coding Tools

### Using Extracted DESIGN.md with Claude Code

```bash
# Add to project context
cp DESIGN.md .claude/

# Reference in prompts
"Build a button component following DESIGN.md spacing and color tokens"
```

### Using with Cursor

```bash
# Add to .cursorrules
cp DESIGN.md .cursorrules/design-system.md

# Reference in code
// Uses spacing-4 (16px) from DESIGN.md
<div className="p-4">
```

### Using with Google Stitch

Upload `SKILL.md` as a custom skill to enable design-system-aware code generation.

## Resources

- **Chrome Web Store**: https://chromewebstore.google.com/detail/designmd-style-extractor/ogpdnchdjiibhobphelbbkemnnemkfma
- **TypeUI Format Spec**: https://www.typeui.sh/design-md
- **Curated Skills**: https://www.typeui.sh/design-skills
- **GitHub Repository**: https://github.com/bergside/design-md-chrome
