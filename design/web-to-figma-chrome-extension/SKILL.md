---
name: web-to-figma-chrome-extension
description: Chrome extension that captures webpages and converts them into editable Figma-compatible JSON files with support for full-page and element capture
triggers:
  - capture webpage to figma format
  - convert html to figma json
  - export website design to figma
  - create figma file from webpage
  - capture web elements for figma
  - build chrome extension for web capture
  - parse webpage into figma data structure
  - extract design tokens from website
---

# Web to Figma Chrome Extension

> Skill by [ara.so](https://ara.so) — Design Skills collection

## Overview

Web to Figma is a Chrome extension that captures any webpage and exports it as a Figma-compatible JSON file. It provides an in-page floating toolbar for one-click capture, supports cross-origin image proxy fetching to handle CORS issues, and offers configurable concurrency settings for image downloads.

**Key capabilities:**
- Full-page capture of DOM elements, styles, and layout
- Element-specific capture for targeted design extraction
- Cross-origin image proxy mode to avoid missing images
- Configurable image fetch concurrency (4/6/8/10/12/16/20/infinite)
- Export as `.json` for Figma workflows

## Installation

### Developer Mode (Local)

1. Clone the repository:
```bash
git clone https://github.com/Paidax01/web-to-figma.git
cd web-to-figma
```

2. Open Chrome and navigate to `chrome://extensions/`

3. Enable **Developer mode** (toggle in top-right)

4. Click **Load unpacked**

5. Select the `web-to-figma` directory

The extension icon should now appear in your Chrome toolbar.

## Project Architecture

```
web-to-figma/
├── manifest.json          # Extension configuration
├── background.js          # Service worker for proxy and coordination
├── capture.js             # Core capture logic (DOM traversal, style extraction)
├── runner.js              # Orchestrates capture process
├── inpage-toolbar.js      # Floating UI toolbar on webpage
├── popup.html/css/js      # Extension popup UI
└── logo/                  # Extension icons
```

### Key Components

- **`capture.js`**: Main capture engine that traverses the DOM, extracts computed styles, handles images, text nodes, and layout information
- **`background.js`**: Background service worker that proxies cross-origin image requests
- **`runner.js`**: Coordinates the capture flow and message passing between components
- **`inpage-toolbar.js`**: Injects floating toolbar UI into webpages for quick access

## Core Capture Flow

### 1. Extension Popup Configuration

The popup (`popup.html`) provides settings:

```javascript
// Example popup.js structure
document.getElementById('startCapture').addEventListener('click', async () => {
  const useProxy = document.getElementById('proxyMode').checked;
  const concurrency = document.getElementById('concurrency').value;
  
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'startCapture',
    config: {
      useProxy: useProxy,
      imageConcurrency: parseInt(concurrency)
    }
  });
});
```

### 2. Triggering Capture

From the in-page toolbar or popup:

```javascript
// inpage-toolbar.js pattern
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'startCapture') {
    const config = message.config || {};
    
    // Start capture process
    captureWebpage(config).then(result => {
      // Generate download
      downloadJSON(result, `figma-capture-${Date.now()}.json`);
    });
  }
});
```

### 3. DOM Traversal and Data Extraction

The capture engine recursively walks the DOM:

```javascript
// capture.js core pattern
function captureElement(element, config) {
  const computedStyle = window.getComputedStyle(element);
  const rect = element.getBoundingClientRect();
  
  const nodeData = {
    type: element.tagName.toLowerCase(),
    id: element.id || null,
    className: element.className || null,
    position: {
      x: rect.left + window.scrollX,
      y: rect.top + window.scrollY,
      width: rect.width,
      height: rect.height
    },
    styles: extractStyles(computedStyle),
    text: extractText(element),
    children: []
  };
  
  // Handle images
  if (element.tagName === 'IMG') {
    nodeData.src = element.src;
    if (config.useProxy) {
      nodeData.proxyUrl = await fetchImageViaProxy(element.src, config);
    }
  }
  
  // Recursively capture children
  for (const child of element.children) {
    if (shouldCaptureElement(child)) {
      nodeData.children.push(captureElement(child, config));
    }
  }
  
  return nodeData;
}

function extractStyles(computedStyle) {
  return {
    color: computedStyle.color,
    backgroundColor: computedStyle.backgroundColor,
    fontSize: computedStyle.fontSize,
    fontFamily: computedStyle.fontFamily,
    fontWeight: computedStyle.fontWeight,
    lineHeight: computedStyle.lineHeight,
    padding: {
      top: computedStyle.paddingTop,
      right: computedStyle.paddingRight,
      bottom: computedStyle.paddingBottom,
      left: computedStyle.paddingLeft
    },
    margin: {
      top: computedStyle.marginTop,
      right: computedStyle.marginRight,
      bottom: computedStyle.marginBottom,
      left: computedStyle.marginLeft
    },
    border: {
      width: computedStyle.borderWidth,
      style: computedStyle.borderStyle,
      color: computedStyle.borderColor,
      radius: computedStyle.borderRadius
    },
    display: computedStyle.display,
    position: computedStyle.position,
    zIndex: computedStyle.zIndex
  };
}
```

### 4. Cross-Origin Image Handling

Background proxy pattern:

```javascript
// background.js proxy implementation
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'fetchImage') {
    fetch(message.url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit'
    })
    .then(response => response.blob())
    .then(blob => {
      const reader = new FileReader();
      reader.onloadend = () => {
        sendResponse({
          success: true,
          dataUrl: reader.result
        });
      };
      reader.readAsDataURL(blob);
    })
    .catch(error => {
      sendResponse({
        success: false,
        error: error.message
      });
    });
    
    return true; // Async response
  }
});

// capture.js usage
async function fetchImageViaProxy(url, config) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage({
      action: 'fetchImage',
      url: url
    }, response => {
      if (response.success) {
        resolve(response.dataUrl);
      } else {
        reject(new Error(response.error));
      }
    });
  });
}
```

### 5. Concurrency Control

Managing parallel image fetches:

```javascript
// Concurrency limiter pattern
class ConcurrencyQueue {
  constructor(limit) {
    this.limit = limit === 'infinite' ? Infinity : limit;
    this.running = 0;
    this.queue = [];
  }
  
  async add(fn) {
    while (this.running >= this.limit) {
      await new Promise(resolve => this.queue.push(resolve));
    }
    
    this.running++;
    try {
      return await fn();
    } finally {
      this.running--;
      const resolve = this.queue.shift();
      if (resolve) resolve();
    }
  }
}

// Usage in capture
async function captureImagesWithConcurrency(images, config) {
  const queue = new ConcurrencyQueue(config.imageConcurrency || 4);
  
  return Promise.all(
    images.map(img => 
      queue.add(() => fetchImageViaProxy(img.src, config))
    )
  );
}
```

## Configuration

### manifest.json

```json
{
  "manifest_version": 3,
  "name": "Web to Figma",
  "version": "1.0.0",
  "description": "Convert any webpage into an editable Figma file",
  "permissions": [
    "activeTab",
    "storage",
    "downloads"
  ],
  "host_permissions": [
    "<all_urls>"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["inpage-toolbar.js", "capture.js", "runner.js"],
      "run_at": "document_idle"
    }
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "logo/icon16.png",
      "48": "logo/icon48.png",
      "128": "logo/icon128.png"
    }
  }
}
```

### Runtime Configuration

Pass config object to capture functions:

```javascript
const captureConfig = {
  useProxy: true,              // Enable cross-origin image proxy
  imageConcurrency: 8,         // Parallel image fetches (4/6/8/10/12/16/20/'infinite')
  fullPage: true,              // Capture entire page vs. viewport
  includeHidden: false,        // Capture elements with display:none
  maxDepth: 50,                // Maximum DOM traversal depth
  captureIframes: false,       // Whether to capture iframe content
  captureBackgrounds: true,    // Include CSS background images
  minimumSize: { width: 1, height: 1 } // Skip tiny elements
};
```

## Common Patterns

### Full-Page Capture

```javascript
async function captureFullPage() {
  const config = {
    useProxy: true,
    imageConcurrency: 8,
    fullPage: true
  };
  
  // Scroll to top
  window.scrollTo(0, 0);
  
  // Capture from root
  const rootElement = document.body;
  const captureData = await captureElement(rootElement, config);
  
  // Add metadata
  const result = {
    version: '1.0',
    timestamp: new Date().toISOString(),
    url: window.location.href,
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight
    },
    document: {
      width: document.documentElement.scrollWidth,
      height: document.documentElement.scrollHeight
    },
    tree: captureData
  };
  
  return result;
}
```

### Element-Specific Capture

```javascript
function captureSpecificElement(selector) {
  const element = document.querySelector(selector);
  
  if (!element) {
    throw new Error(`Element not found: ${selector}`);
  }
  
  const config = {
    useProxy: true,
    imageConcurrency: 6,
    fullPage: false
  };
  
  return captureElement(element, config);
}

// Usage
const headerData = await captureSpecificElement('header.main-header');
```

### Download JSON Result

```javascript
function downloadJSON(data, filename) {
  const jsonString = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonString], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  
  // Cleanup
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

### Handling SVGs

```javascript
function captureSVG(svgElement) {
  const serializer = new XMLSerializer();
  const svgString = serializer.serializeToString(svgElement);
  const svgDataUrl = `data:image/svg+xml;base64,${btoa(svgString)}`;
  
  return {
    type: 'svg',
    content: svgString,
    dataUrl: svgDataUrl,
    viewBox: svgElement.getAttribute('viewBox'),
    width: svgElement.width.baseVal.value,
    height: svgElement.height.baseVal.value
  };
}
```

### Canvas Capture

```javascript
function captureCanvas(canvasElement) {
  try {
    const dataUrl = canvasElement.toDataURL('image/png');
    return {
      type: 'canvas',
      dataUrl: dataUrl,
      width: canvasElement.width,
      height: canvasElement.height
    };
  } catch (error) {
    // Canvas may be tainted by cross-origin content
    return {
      type: 'canvas',
      error: 'Tainted canvas - cross-origin content',
      width: canvasElement.width,
      height: canvasElement.height
    };
  }
}
```

## Advanced Usage

### Custom Style Extraction

```javascript
function extractCustomProperties(element) {
  const styles = window.getComputedStyle(element);
  const customProps = {};
  
  // Extract CSS custom properties (variables)
  for (let i = 0; i < styles.length; i++) {
    const prop = styles[i];
    if (prop.startsWith('--')) {
      customProps[prop] = styles.getPropertyValue(prop);
    }
  }
  
  return customProps;
}
```

### Text Node Extraction

```javascript
function extractTextNodes(element) {
  const textNodes = [];
  const walker = document.createTreeWalker(
    element,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  
  let node;
  while (node = walker.nextNode()) {
    const text = node.textContent.trim();
    if (text) {
      const range = document.createRange();
      range.selectNode(node);
      const rect = range.getBoundingClientRect();
      
      textNodes.push({
        text: text,
        position: {
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY,
          width: rect.width,
          height: rect.height
        }
      });
    }
  }
  
  return textNodes;
}
```

### Background Image Extraction

```javascript
function extractBackgroundImages(element) {
  const style = window.getComputedStyle(element);
  const bgImage = style.backgroundImage;
  
  if (bgImage && bgImage !== 'none') {
    const urlMatch = bgImage.match(/url\(['"]?(.*?)['"]?\)/);
    if (urlMatch && urlMatch[1]) {
      return {
        url: urlMatch[1],
        size: style.backgroundSize,
        position: style.backgroundPosition,
        repeat: style.backgroundRepeat
      };
    }
  }
  
  return null;
}
```

### Progressive Capture with Progress Callback

```javascript
async function captureWithProgress(element, config, onProgress) {
  const totalElements = element.querySelectorAll('*').length;
  let processedElements = 0;
  
  async function captureWithCallback(el) {
    processedElements++;
    if (onProgress) {
      onProgress({
        processed: processedElements,
        total: totalElements,
        percentage: (processedElements / totalElements * 100).toFixed(2)
      });
    }
    return captureElement(el, config);
  }
  
  return await captureWithCallback(element);
}

// Usage
const result = await captureWithProgress(
  document.body,
  { useProxy: true, imageConcurrency: 8 },
  (progress) => {
    console.log(`Capturing: ${progress.percentage}%`);
  }
);
```

## Troubleshooting

### Images Not Capturing

**Problem:** Images appear as broken or missing in exported JSON.

**Solutions:**

1. Enable cross-origin proxy mode:
```javascript
const config = { useProxy: true, imageConcurrency: 8 };
```

2. Verify background.js has proper permissions in manifest.json:
```json
{
  "host_permissions": ["<all_urls>"]
}
```

3. Check if images are lazy-loaded:
```javascript
// Scroll through page to trigger lazy loading
async function scrollToLoadImages() {
  const scrollStep = window.innerHeight;
  const scrollMax = document.body.scrollHeight;
  
  for (let y = 0; y < scrollMax; y += scrollStep) {
    window.scrollTo(0, y);
    await new Promise(resolve => setTimeout(resolve, 200));
  }
  
  window.scrollTo(0, 0);
}

await scrollToLoadImages();
const result = await captureFullPage();
```

### Capture Timeout or Slow Performance

**Problem:** Capture takes too long or times out.

**Solutions:**

1. Reduce image concurrency:
```javascript
const config = { imageConcurrency: 4 }; // Lower value
```

2. Skip hidden elements:
```javascript
function shouldCaptureElement(element) {
  const style = window.getComputedStyle(element);
  return style.display !== 'none' && 
         style.visibility !== 'hidden' &&
         style.opacity !== '0';
}
```

3. Limit DOM depth:
```javascript
function captureElementWithDepth(element, config, currentDepth = 0) {
  if (currentDepth > config.maxDepth) {
    return null;
  }
  // ... capture logic
}
```

### Extension Not Injecting

**Problem:** Toolbar or capture functionality not appearing on page.

**Solutions:**

1. Check content script injection in manifest.json:
```json
{
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["inpage-toolbar.js", "capture.js", "runner.js"],
    "run_at": "document_idle"
  }]
}
```

2. Verify no CSP (Content Security Policy) blocks:
```javascript
// Check console for CSP errors
// May need to adjust for strict CSP pages
```

3. Reload extension after code changes:
```bash
# In chrome://extensions/, click reload icon
```

### Memory Issues with Large Pages

**Problem:** Browser crashes or slows down on large/complex pages.

**Solutions:**

1. Capture in chunks:
```javascript
async function captureInChunks(rootElement, chunkSize = 100) {
  const allElements = Array.from(rootElement.querySelectorAll('*'));
  const chunks = [];
  
  for (let i = 0; i < allElements.length; i += chunkSize) {
    const chunk = allElements.slice(i, i + chunkSize);
    chunks.push(await Promise.all(
      chunk.map(el => captureElement(el, config))
    ));
    
    // Allow event loop to process
    await new Promise(resolve => setTimeout(resolve, 0));
  }
  
  return chunks.flat();
}
```

2. Exclude large elements:
```javascript
const config = {
  minimumSize: { width: 10, height: 10 },
  excludeSelectors: ['.ad-container', '.comments-section']
};
```

### JSON Export Too Large

**Problem:** Generated JSON file is too large to download or process.

**Solutions:**

1. Compress data:
```javascript
function compressStyles(styles) {
  // Only include non-default values
  const compressed = {};
  const defaults = {
    color: 'rgb(0, 0, 0)',
    backgroundColor: 'rgba(0, 0, 0, 0)',
    // ... other defaults
  };
  
  for (const [key, value] of Object.entries(styles)) {
    if (value !== defaults[key]) {
      compressed[key] = value;
    }
  }
  
  return compressed;
}
```

2. Paginate output:
```javascript
function exportInPages(captureData, elementsPerFile = 500) {
  const files = [];
  const elements = flattenTree(captureData);
  
  for (let i = 0; i < elements.length; i += elementsPerFile) {
    const chunk = elements.slice(i, i + elementsPerFile);
    files.push({
      filename: `figma-capture-page-${Math.floor(i / elementsPerFile) + 1}.json`,
      data: { elements: chunk }
    });
  }
  
  return files;
}
```

## Packaging for Distribution

### Create Distribution Build

```bash
# Remove development files
zip -r web-to-figma-extension.zip . \
  -x "*.DS_Store" \
  -x ".git/*" \
  -x "node_modules/*" \
  -x "*.md" \
  -x "tests/*"
```

### Version Management

Update version in manifest.json:

```json
{
  "version": "1.0.1",
  "version_name": "1.0.1 Beta"
}
```

## Integration with Figma API

While this extension exports JSON, you can process it for Figma import:

```javascript
// Example post-processing for Figma plugin
function convertToFigmaNodes(captureData) {
  return {
    name: captureData.type || 'Frame',
    type: mapToFigmaType(captureData.type),
    x: captureData.position.x,
    y: captureData.position.y,
    width: captureData.position.width,
    height: captureData.position.height,
    fills: convertFills(captureData.styles.backgroundColor),
    strokes: convertStrokes(captureData.styles.border),
    children: captureData.children.map(convertToFigmaNodes)
  };
}

function mapToFigmaType(htmlType) {
  const typeMap = {
    'div': 'FRAME',
    'span': 'TEXT',
    'img': 'RECTANGLE', // With image fill
    'svg': 'VECTOR'
  };
  return typeMap[htmlType] || 'FRAME';
}
```

## Best Practices

1. **Always test on sample pages first** before capturing production sites
2. **Use proxy mode for public websites** with image CDNs
3. **Adjust concurrency based on network speed** (slower connection = lower concurrency)
4. **Clear browser cache** if getting stale captures
5. **Respect robots.txt and terms of service** when capturing third-party sites
6. **Handle errors gracefully** - not all pages will capture perfectly
7. **Version your capture format** for backward compatibility

## Legal and Ethical Considerations

- Only capture content you have permission to use
- Respect copyright and intellectual property rights
- Follow website terms of service
- Do not capture sensitive or personal information without consent
- Comply with GDPR, CCPA, and other privacy regulations
- Use for learning, research, or authorized design workflows only
