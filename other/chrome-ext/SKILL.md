---
name: chrome-ext
description: Scaffold a Chrome extension from a description. Generates manifest v3, content scripts, popup, and styles with minimal permissions. Use when building a new browser extension.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: [extension-description]
---

# Chrome Extension Scaffolder

Generate a complete Chrome extension skeleton from a plain-English description.

**Argument**: `$ARGUMENTS` is a description of what the extension should do (e.g., "highlight all links on the page and copy them to clipboard"). If not provided, ask.

## Process

### 1. Parse the description

Determine from the description:
- **Injection type**: Does it need a content script (modifies pages), popup (standalone UI), or both?
- **Target sites**: All sites, or specific domains (e.g., YouTube, GitHub)?
- **Permissions needed**: What's the minimum set? See permission guide below.
- **Extension name**: Derive a short name from the description.

### 2. Choose the output directory

Ask the user where to create it. Suggest a dedicated `chrome-extensions/[Extension Name]/` folder alongside their other projects.

### 3. Generate the extension

Create these files:

#### manifest.json
```json
{
  "manifest_version": 3,
  "name": "[Extension Name]",
  "version": "1.0.0",
  "description": "[One-line description]",
  "permissions": ["activeTab"],
  "icons": {},
  "action": {}
}
```

**Permission guide** — use the minimum required:
- `activeTab` — almost always sufficient for reading/modifying the current tab
- `scripting` — only if popup needs to inject code into pages via `chrome.scripting.executeScript()`
- `clipboardWrite` — only if writing to clipboard
- `storage` — only if persisting settings/data
- `host_permissions` — only if targeting specific domains (e.g., `"*://*.youtube.com/*"`)

**Do NOT add** `tabs`, `<all_urls>`, or broad permissions unless absolutely necessary.

#### content.js (if content script needed)
```javascript
// [Extension Name] — Content Script
// Runs on: [target pages]

(function() {
  'use strict';

  // ===== CONFIG =====
  const CONFIG = {
    // Extension-specific settings
  };

  // ===== MAIN =====
  function init() {
    // Wait for page to be ready
    // Set up observers if SPA (e.g., YouTube)
  }

  // ===== UI INJECTION =====
  function injectUI() {
    const container = document.createElement('div');
    container.id = '[extension-name]-container';
    // Build UI elements
    // Use inline styles for critical positioning
    // Use styles.css for polish
    document.body.appendChild(container);
  }

  // ===== CORE LOGIC =====
  // [Main functionality here]

  // ===== SPA NAVIGATION (if needed) =====
  // For sites like YouTube that use client-side routing:
  // const observer = new MutationObserver(() => { ... });
  // observer.observe(document.body, { childList: true, subtree: true });

  // ===== INIT =====
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

#### popup.html (if popup needed)
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      width: 320px;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 14px;
      color: #1a1a1a;
    }
    h1 {
      font-size: 16px;
      margin: 0 0 12px;
    }
    button {
      width: 100%;
      padding: 10px 16px;
      background: #0d9488;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.15s;
    }
    button:hover { background: #0f766e; }
    button:active { background: #115e59; }
    .status {
      margin-top: 8px;
      font-size: 13px;
      color: #6b7280;
    }
  </style>
</head>
<body>
  <h1>[Extension Name]</h1>
  <button id="action-btn">[Action Label]</button>
  <div class="status" id="status"></div>
  <script src="popup.js"></script>
</body>
</html>
```

#### popup.js (if popup needed)
```javascript
document.getElementById('action-btn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const status = document.getElementById('status');

  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        // [Core logic that runs on the page]
      }
    });

    status.textContent = 'Done!';
    status.style.color = '#059669';
  } catch (err) {
    status.textContent = 'Error: ' + err.message;
    status.style.color = '#dc2626';
  }
});
```

#### styles.css (if content script injects UI)
```css
/* [Extension Name] styles */

#[extension-name]-container {
  position: fixed;
  z-index: 99999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Match page theme if needed */
/* YouTube dark mode: html[dark] */
/* Generic dark mode: @media (prefers-color-scheme: dark) */
```

### 4. Fill in the logic

Replace all placeholder comments with actual implementation based on the user's description. The generated extension should be functional, not just a skeleton.

### 5. Create a simple icon

Generate a minimal SVG icon (128x128) with:
- A colored rounded rectangle background
- A single letter or simple symbol in white
- Save as `icons/icon-128.svg`

Then render PNGs:
```bash
mkdir -p icons
# Create 16, 48, 128 px versions
qlmanage -t -s 128 -o icons/ icons/icon-128.svg 2>/dev/null
cp icons/icon-128.svg.png icons/icon-128.png
sips -z 48 48 icons/icon-128.png --out icons/icon-48.png
sips -z 16 16 icons/icon-128.png --out icons/icon-16.png
rm icons/icon-128.svg.png
```

Update manifest.json icons:
```json
"icons": {
  "16": "icons/icon-16.png",
  "48": "icons/icon-48.png",
  "128": "icons/icon-128.png"
}
```

### 6. Test instructions

After generating, tell the user:
1. Open `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the extension folder
5. Test on a relevant page

## Rules
- Minimal permissions: `activeTab` unless the description needs more
- Must load and work via "Load unpacked" with no build step
