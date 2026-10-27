---
name: chrome-extension
description: Expert knowledge in developing Chrome extensions covering all aspects from basic architecture to advanced features. Covers Manifest V3, service workers, content scripts, Chrome APIs, popup and options pages, security, performance, testing, debugging, and publishing. Use when developing Chrome extensions or migrating from Manifest V2 to V3. For HTML, CSS, and JavaScript best practices and modern web APIs, use the modern-web-dev skill.
metadata:
  version: 1.0.0
---

# Chrome Extensions Development Skills

This skill set provides expertise in developing Chrome extensions, covering all aspects from basic architecture to advanced features.

## Prerequisites and Related Skills

**Modern Web Development Foundation**: Chrome extensions are built using HTML, CSS, and JavaScript. For guidance on modern web APIs, browser features, and JavaScript best practices, see [modern-web-dev](../modern-web-development/SKILL.md). This skill focuses on Chrome extension-specific architecture, APIs, and patterns.

When building extension UI (popups, options pages, content scripts), see [modern-web-dev](../modern-web-development/SKILL.md) for:
- HTML/CSS/JavaScript best practices
- Modern browser APIs (fetch, async/await, etc.)
- Browser support and compatibility
- Performance optimization techniques
- Accessibility guidelines

## Overview

Chrome Extensions extend the functionality of the Chrome browser, allowing developers to customize the browsing experience, add new features, and integrate with web pages. This skill covers modern extension development using Manifest V3.

## Core Competencies

- **Extension Architecture**: Understanding Manifest V3 structure and components
- **Background Service Workers**: Managing extension lifecycle
- **Content Scripts**: Interacting with web pages
- **Popup and Options Pages**: Creating user interfaces
- **Chrome APIs**: Using browser-specific APIs
- **Security**: Implementing secure extensions
- **Performance**: Optimizing extension performance
- **Testing and Debugging**: Testing extensions effectively
- **Publishing**: Distributing extensions via Chrome Web Store

## Extension Components

### Manifest File (manifest.json)
The manifest file defines the extension's structure, permissions, and resources.

**Key Manifest V3 Features**:
- Service workers instead of background pages
- Declarative network request API
- Improved security model
- Host permissions separate from API permissions

**Required Fields**:
```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0",
  "description": "Extension description"
}
```

### Service Workers
Background scripts that handle extension lifecycle and respond to browser events.

**Common Uses**:
- Event listeners
- Extension state management
- Message handling
- Alarm scheduling
- Network request interception

**Best Practices**:
- Keep service workers lightweight
- Store persistent data in chrome.storage
- Handle service worker lifecycle (may stop and restart)
- Use alarms for recurring tasks

### Content Scripts
JavaScript that runs in the context of web pages.

**Capabilities**:
- Read and modify DOM
- Listen to DOM events
- Send messages to service worker
- Access limited Chrome APIs

**Limitations**:
- Isolated JavaScript environment
- No access to page's JavaScript variables
- Cannot use all Chrome APIs

**Injection Methods**:
- Static (via manifest)
- Dynamic (programmatically)
- CSS injection

### Popup and Options Pages
HTML pages that provide user interface.

**Popup**:
- Small window from extension icon
- Temporary UI for quick actions
- Closes when focus is lost

**Options Page**:
- Full page for extension settings
- Can be embedded or full page
- Persistent settings via chrome.storage

**Implementation Note**: When building these UI components, follow modern HTML/CSS/JavaScript practices from [modern-web-dev](../modern-web-development/SKILL.md). Use modern APIs like `fetch()`, `async/await`, and contemporary DOM manipulation techniques rather than legacy patterns.

### Chrome APIs

**Essential APIs**:
- `chrome.runtime`: Extension lifecycle and messaging
- `chrome.storage`: Store and retrieve data
- `chrome.tabs`: Interact with browser tabs
- `chrome.scripting`: Execute scripts dynamically
- `chrome.action`: Control extension icon and popup
- `chrome.alarms`: Schedule code to run periodically
- `chrome.declarativeNetRequest`: Modify network requests
- `chrome.cookies`: Manage cookies
- `chrome.webRequest`: Observe and analyze traffic (MV2 legacy)

**Permissions Required**:
- Request only necessary permissions
- Explain permission usage to users
- Use optional permissions when possible

## Security Best Practices

1. **Content Security Policy (CSP)**
   - No inline scripts in extension pages
   - Use external JavaScript files
   - Restrict sources of scripts and styles

2. **Permission Management**
   - Follow principle of least privilege
   - Use activeTab when possible
   - Request host permissions at runtime

3. **Input Validation**
   - Sanitize all user input
   - Validate messages from content scripts
   - Use DOMPurify for HTML sanitization

4. **Data Security**
   - Never store sensitive data in sync storage
   - Use encryption for sensitive data
   - Clear data on uninstall

5. **Communication Security**
   - Validate message senders
   - Use externally_connectable carefully
   - Implement message authentication

## Common Patterns

**Note**: The examples below use modern JavaScript patterns (async/await, arrow functions, etc.). For comprehensive guidance on modern web APIs and JavaScript best practices, see [modern-web-dev](../modern-web-development/SKILL.md).

### Messaging Between Components

**One-time messages**:
```javascript
// From content script to service worker
chrome.runtime.sendMessage({type: 'action', data: value});

// From service worker to content script
chrome.tabs.sendMessage(tabId, {type: 'action', data: value});
```

**Long-lived connections**:
```javascript
// Create port connection
const port = chrome.runtime.connect({name: 'channel'});
port.postMessage({data: value});
port.onMessage.addListener((msg) => {});
```

### Storage Management

```javascript
// Save data
await chrome.storage.sync.set({key: value});

// Retrieve data
const result = await chrome.storage.sync.get(['key']);

// Listen for changes
chrome.storage.onChanged.addListener((changes, namespace) => {});
```

### Dynamic Script Injection

```javascript
// Inject script into tab
await chrome.scripting.executeScript({
  target: {tabId: tabId},
  files: ['content.js']
});

// Inject CSS
await chrome.scripting.insertCSS({
  target: {tabId: tabId},
  files: ['styles.css']
});
```

## Development Workflow

1. **Setup**
   - Create manifest.json
   - Organize file structure
   - Load unpacked extension for testing

2. **Development**
   - Use TypeScript for type safety
   - Implement hot reload for development
   - Use modern build tools (Webpack, Vite, Rollup)
   - Follow [modern-web-dev](../modern-web-development/SKILL.md) for JavaScript/HTML/CSS coding standards and modern API usage

3. **Testing**
   - Unit test business logic
   - Integration test Chrome API usage
   - Manual testing in browser
   - Test across Chrome versions

4. **Debugging**
   - Use Chrome DevTools
   - Check service worker console
   - Inspect popup and options pages
   - Use chrome://extensions page

5. **Publishing**
   - Create Chrome Web Store account
   - Prepare store listing (icons, screenshots, description)
   - Submit for review
   - Monitor reviews and crash reports

## Performance Optimization

1. **Minimize Permissions**
   - Reduces security warnings
   - Faster review process

2. **Optimize Content Scripts**
   - Inject only when needed
   - Use run_at: "document_idle" when possible
   - Minimize DOM operations

3. **Efficient Service Workers**
   - Respond to events quickly
   - Use alarms for periodic tasks
   - Cache frequently used data

4. **Bundle Size**
   - Minimize dependencies
   - Tree shake unused code
   - Use code splitting

## Common Use Cases

- **Productivity**: Tab management, note-taking, task tracking
- **Content Modification**: Ad blocking, dark mode, custom styles
- **Data Collection**: Web scraping, analytics, monitoring
- **Integration**: Third-party service integration
- **Security**: Password managers, privacy tools
- **Development Tools**: Debugging, testing, profiling

## Migration from Manifest V2 to V3

**Key Changes**:
- Background pages → Service workers
- webRequest API → declarativeNetRequest API
- Browser action/Page action → Action API
- executeScript/insertCSS → scripting API
- Remotely hosted code not allowed
- Enhanced security requirements

## Resources and Tools

- Chrome Extension Documentation
- Extension samples on GitHub
- Chrome Web Store developer dashboard
- Extension development frameworks (WXT, Plasmo)
- Testing tools (Puppeteer, Playwright)

## Best Practices Summary

✅ Use Manifest V3
✅ Request minimal permissions
✅ Implement proper error handling
✅ Validate all inputs
✅ Use chrome.storage for persistence
✅ Test across different scenarios
✅ Follow Chrome Web Store policies
✅ Provide clear privacy policy
✅ Keep extension updated
✅ Monitor user feedback
✅ See [modern-web-dev](../modern-web-development/SKILL.md) for HTML/CSS/JavaScript best practices and modern browser APIs