---
name: figma-capture-extension
description: Chrome extension that captures webpages into Figma's clipboard format with font fixes and DOM cleanup
triggers:
  - capture a webpage to Figma
  - install figma capture extension
  - fix CJK fonts when capturing to Figma
  - customize font mapping for Figma capture
  - debug Figma capture clipboard issues
  - configure figma-capture chrome extension
  - flatten DOM for Figma import
  - bypass CSP when capturing to Figma
---

# Figma Capture Extension

> Skill by [ara.so](https://ara.so) — Design Skills collection

This Chrome extension captures any webpage into Figma's clipboard format, adding post-processing to fix fonts (especially CJK), clean up DOM structure, and remove empty elements before pasting into Figma.

## What It Does

- **CJK Font Correction**: Detects Chinese/Japanese/Korean text and remaps to `PingFang SC` / `Noto Serif SC`
- **Font Mapping**: Remaps unavailable fonts via configurable `font-map.json`
- **Default Font Fallback**: Assigns `Noto Sans SC` to elements without explicit fonts
- **DOM Flattening**: Removes wrapper elements that don't contribute visually
- **Empty Frame Cleanup**: Strips zero-size elements and childless containers
- **Event Isolation**: Prevents toolbar clicks from affecting host page behavior

## Installation

### Step 1: Download Figma's Capture Script

```bash
make
```

This downloads `capture.js` from Figma's public endpoint. The Makefile does:

```makefile
capture.js:
	curl -o capture.js https://www.figma.com/community/plugin/1159123024924461424/capture.js
```

### Step 2: Configure Font Mapping

```bash
cp font-map.example.json font-map.json
```

Example `font-map.json` structure:

```json
{
  "Arial": "Inter",
  "Helvetica": "Inter",
  "SF Pro Display": "Google Sans Flex",
  "Roboto": "Noto Sans SC",
  "system-ui": "Inter"
}
```

### Step 3: Load Extension in Chrome

1. Navigate to `chrome://extensions`
2. Enable **Developer mode** (top right toggle)
3. Click **Load unpacked**
4. Select the `figma-capture` directory

## Usage

### Basic Capture Workflow

1. Navigate to the webpage you want to capture
2. Click the extension icon **or** press `Alt+Shift+F`
3. Use the toolbar to:
   - Capture entire page
   - Select specific element by clicking
4. Switch to Figma
5. Press `Ctrl+V` (Windows) or `Cmd+V` (Mac)

### Keyboard Shortcut

Default: `Alt+Shift+F`

To customize, go to `chrome://extensions/shortcuts`

## Configuration Files

### manifest.json

Key configuration sections:

```json
{
  "manifest_version": 3,
  "name": "Figma Capture",
  "version": "1.0.0",
  "permissions": [
    "activeTab",
    "clipboardWrite"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_start"
    }
  ],
  "action": {
    "default_icon": "icon.png"
  },
  "commands": {
    "_execute_action": {
      "suggested_key": {
        "default": "Alt+Shift+F"
      }
    }
  }
}
```

### Font Mapping Configuration

Edit `font-map.json` to add custom font substitutions:

```json
{
  "SegoeUI": "Inter",
  "San Francisco": "Google Sans Flex",
  "PingFang": "PingFang SC",
  "Microsoft YaHei": "Noto Sans SC",
  "Hiragino Sans": "Noto Sans JP"
}
```

**Font mapping logic** (applied in order):
1. CJK detection → `PingFang SC` / `Noto Serif SC`
2. Custom `font-map.json` mappings
3. Icon font detection → preserve original
4. No font specified → `Noto Sans SC`

## Architecture

### Component Flow

```
User clicks extension icon
    ↓
background.js activates content script
    ↓
content.js injects capture.js
    ↓
capture.js serializes DOM → clipboard payload
    ↓
Clipboard interceptor transforms payload:
  - Font correction
  - DOM cleanup
  - Wrapper flattening
    ↓
Modified payload written to clipboard
    ↓
User pastes into Figma
```

### Key Files

- **background.js**: Service worker, patches `attachShadow` for event isolation
- **content.js**: Injected script, intercepts clipboard API
- **capture.js**: Figma's official serializer (downloaded, not in repo)
- **font-map.json**: User-configurable font substitutions

## Code Examples

### Clipboard Interception Pattern

```javascript
// Override clipboard write to transform Figma payload
const originalWrite = navigator.clipboard.write;
navigator.clipboard.write = async function(data) {
  const items = await Promise.all(data.map(async item => {
    if (item.types.includes('text/html')) {
      const blob = await item.getType('text/html');
      const html = await blob.text();
      
      // Transform Figma's clipboard payload
      const transformed = transformFigmaPayload(html);
      
      return new ClipboardItem({
        'text/html': new Blob([transformed], { type: 'text/html' })
      });
    }
    return item;
  }));
  
  return originalWrite.call(this, items);
};
```

### Font Detection and Remapping

```javascript
function detectAndFixFont(element, computedStyle) {
  const text = element.textContent || '';
  const fontFamily = computedStyle.fontFamily;
  
  // CJK detection
  const cjkRegex = /[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF]/;
  if (cjkRegex.test(text)) {
    // Check if serif
    const isSerif = /serif/i.test(fontFamily);
    return isSerif ? 'Noto Serif SC' : 'PingFang SC';
  }
  
  // Load font map
  const fontMap = loadFontMap(); // from font-map.json
  
  // Check for mapped font
  for (const [original, replacement] of Object.entries(fontMap)) {
    if (fontFamily.includes(original)) {
      return replacement;
    }
  }
  
  // Icon font detection (preserve)
  if (/icon|symbol|awesome|material/i.test(fontFamily)) {
    return fontFamily;
  }
  
  // Default fallback
  return fontFamily || 'Noto Sans SC';
}
```

### DOM Cleanup: Wrapper Flattening

```javascript
function flattenWrappers(node) {
  // Skip if not a wrapper candidate
  if (node.children.length !== 1) return false;
  
  const parent = node;
  const child = node.children[0];
  
  // Check if parent is just a pass-through container
  const parentStyle = getComputedStyle(parent);
  const childStyle = getComputedStyle(child);
  
  const isPassThrough = 
    parentStyle.backgroundColor === 'transparent' &&
    parentStyle.border === 'none' &&
    parent.getBoundingClientRect().width === child.getBoundingClientRect().width &&
    parent.getBoundingClientRect().height === child.getBoundingClientRect().height;
  
  if (isPassThrough) {
    // Promote child to parent's position
    parent.replaceWith(child);
    return true;
  }
  
  return false;
}
```

### Event Isolation for Toolbar

```javascript
// In background.js - save closed shadow roots
const shadowRoots = new WeakMap();

const originalAttachShadow = Element.prototype.attachShadow;
Element.prototype.attachShadow = function(init) {
  const shadowRoot = originalAttachShadow.call(this, init);
  if (init.mode === 'closed') {
    shadowRoots.set(this, shadowRoot);
  }
  return shadowRoot;
};

// In content.js - intercept toolbar clicks
window.addEventListener('click', (event) => {
  const toolbar = document.querySelector('.figma-capture-toolbar');
  if (!toolbar) return;
  
  const toolbarHost = toolbar.host;
  const shadowRoot = shadowRoots.get(toolbarHost);
  
  if (shadowRoot) {
    event.stopPropagation();
    event.preventDefault();
    
    // Re-dispatch inside shadow DOM
    const point = shadowRoot.elementFromPoint(event.clientX, event.clientY);
    if (point) {
      point.dispatchEvent(new MouseEvent('click', event));
    }
  }
}, true); // Capture phase
```

## Common Patterns

### Handling Special Elements

```javascript
// Skip script/style/svg from processing
const SKIP_TAGS = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'LINK', 'META'];

function shouldProcessElement(element) {
  if (SKIP_TAGS.includes(element.tagName)) {
    return false;
  }
  
  // Skip hidden elements
  const style = getComputedStyle(element);
  if (style.display === 'none' || style.visibility === 'hidden') {
    return false;
  }
  
  // Skip zero-size elements
  const rect = element.getBoundingClientRect();
  if (rect.width === 0 && rect.height === 0) {
    return false;
  }
  
  return true;
}
```

### Custom Font Mapping for Specific Websites

```javascript
// Create site-specific font mappings
const siteSpecificMaps = {
  'github.com': {
    '-apple-system': 'Inter',
    'BlinkMacSystemFont': 'Inter',
    'Segoe UI': 'Inter'
  },
  'twitter.com': {
    'TwitterChirp': 'Google Sans Flex',
    'Helvetica Neue': 'Inter'
  }
};

function getFontMap() {
  const hostname = window.location.hostname;
  const baseMap = JSON.parse(localStorage.getItem('font-map.json') || '{}');
  const siteMap = siteSpecificMaps[hostname] || {};
  
  return { ...baseMap, ...siteMap };
}
```

## Troubleshooting

### Fonts Not Displaying Correctly in Figma

**Problem**: Pasted elements show default Times or incorrect fonts

**Solution**: Check if fonts are installed in Figma:

```javascript
// Add debug logging to see what fonts are being applied
console.log('Applied font:', appliedFont);
console.log('Original font:', originalFont);
console.log('Font map:', fontMap);
```

Update `font-map.json` to map problematic fonts to fonts you have in Figma:

```json
{
  "ProblematicFont": "Inter",
  "AnotherBadFont": "Roboto"
}
```

### Extension Not Activating

**Problem**: Clicking icon does nothing

**Solution**: Check console for errors:

1. Right-click extension icon → Inspect popup
2. Go to `chrome://extensions` → Find Figma Capture → Click "background page"
3. Check for errors in console

Verify `capture.js` exists:

```bash
ls -la capture.js
# If missing:
make
```

### Clipboard Payload Not Modified

**Problem**: Fonts/cleanup not being applied

**Solution**: Verify clipboard interceptor is loaded:

```javascript
// In browser console on target page:
console.log(navigator.clipboard.write.toString());
// Should show wrapped function, not native code
```

Reload extension:
1. `chrome://extensions`
2. Click reload icon for Figma Capture
3. Refresh target webpage

### Empty or Broken Capture

**Problem**: Pasting creates empty frame or errors

**Solution**: Some elements may be over-cleaned. Adjust cleanup logic:

```javascript
// Disable wrapper flattening temporarily
const ENABLE_FLATTENING = false;

if (ENABLE_FLATTENING) {
  flattenWrappers(node);
}
```

Check for CSP violations in console — some sites block extension scripts.

### CJK Text Not Detected

**Problem**: Chinese/Japanese/Korean text uses wrong font

**Solution**: Verify regex pattern matches your text:

```javascript
const text = "你好世界";
const cjkRegex = /[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF]/;
console.log(cjkRegex.test(text)); // Should be true
```

Manually set font in `font-map.json`:

```json
{
  "SimSun": "Noto Sans SC",
  "Microsoft YaHei": "PingFang SC"
}
```

## Advanced Configuration

### Modify Default Fallback Font

Edit `content.js`:

```javascript
const DEFAULT_FALLBACK_FONT = 'Inter'; // Change from 'Noto Sans SC'
```

### Add Custom Cleanup Rules

```javascript
function customCleanup(element) {
  // Remove all data attributes
  for (const attr of element.attributes) {
    if (attr.name.startsWith('data-')) {
      element.removeAttribute(attr.name);
    }
  }
  
  // Remove specific classes
  const REMOVE_CLASSES = ['ad', 'banner', 'cookie-notice'];
  element.classList.remove(...REMOVE_CLASSES);
}
```

### Debug Mode

Add to `content.js`:

```javascript
const DEBUG = true;

function debug(...args) {
  if (DEBUG) {
    console.log('[Figma Capture]', ...args);
  }
}

debug('Font applied:', fontFamily);
debug('Element cleaned:', element.tagName);
```

## Limitations

- **Figma Dependency**: Relies on Figma's undocumented clipboard format (may break)
- **Font Availability**: Target fonts must be installed in Figma
- **CSP Restrictions**: Some sites block extension script injection
- **Dynamic Content**: May not capture lazy-loaded or JavaScript-rendered elements
- **`capture.js` Updates**: Figma may change/remove the download endpoint

## Resources

- Figma HTML to Design Plugin: https://www.figma.com/community/plugin/1159123024924461424
- Chrome Extension Manifest V3: https://developer.chrome.com/docs/extensions/mv3/
- Clipboard API: https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API
