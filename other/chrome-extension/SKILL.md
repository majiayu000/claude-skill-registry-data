---
name: chrome-extension
description: Chrome extension structure, Manifest V3, the popup, content scripts, service workers, and storage. Use when creating an extension, editing manifest.json, adding a permission, building the popup UI, injecting a content script, or wiring message passing. Triggers on manifest.json with manifest_version, chrome.tabs, chrome.scripting, chrome.storage, chrome.runtime.onMessage, service-worker.js, popup.html, and loading an unpacked extension.
user-invocable: false
---

# Chrome Extension

**Manifest V3, a popup styled in Catppuccin Mocha, and the minimum permissions the extension actually needs.**

Manifest V2 is removed from Chrome, so V3 is the only target. This assumes unpacked or sideloaded distribution; a Web Store listing adds review requirements and a signing key that change the packaging step.

## Layout

```
extension-root/
├── manifest.json           # required
├── Makefile                # builds the distributable zip
├── README.md
├── .github/
│   ├── assets/logo.png
│   └── workflows/release.yaml
├── icons/
│   ├── icon16.png          # toolbar
│   ├── icon32.png          # Windows taskbar
│   ├── icon48.png          # the extensions page
│   └── icon128.png         # install dialog and store listing
├── popup/
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
├── content/
│   └── content.js          # runs inside web pages
├── background/
│   └── service-worker.js
└── lib/                    # optional shared code
    └── utils.js
```

Popup, content, and background code stay in separate directories because they run in three different contexts with three different sets of available APIs, and a flat layout invites calling `chrome.tabs` from a content script where it does not exist.

## Manifest

```json
{
  "manifest_version": 3,
  "name": "[EXTENSION_NAME]",
  "version": "1.0.0",
  "description": "[Brief description of what the extension does]",

  "icons": {
    "16": "icons/icon16.png",
    "32": "icons/icon32.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },

  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "32": "icons/icon32.png"
    }
  },

  "permissions": ["activeTab", "storage", "scripting"],

  "background": {
    "service_worker": "background/service-worker.js"
  },

  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content/content.js"],
      "run_at": "document_idle"
    }
  ]
}
```

Unused sections are deleted rather than left empty. A declared content script that does nothing still runs on every page the user visits.

`version` here is what the browser installs against and what the Makefile reads, so it is the single place a release number is bumped.

## Permissions

Request the minimum that works. Every permission is shown to the user at install time, and a broad one on a small extension is the most common reason someone declines it.

| Permission | Grants |
|---|---|
| `activeTab` | access to the current tab only when the user clicks the extension |
| `storage` | `chrome.storage` for settings |
| `scripting` | programmatic script injection |
| `tabs` | tab URLs and metadata for every tab, at all times |
| `cookies` | reading and writing cookies, with host permissions |
| `webRequest` | observing network requests |

`activeTab` is preferred over `tabs` wherever it suffices, since it grants access to one tab at the moment of a user gesture rather than standing access to all of them.

`host_permissions` names specific domains when the extension only works on specific domains. `<all_urls>` asks for every site a person will ever visit.

## Popup

The popup is a normal page in an extension context: it has the `chrome.*` APIs and no access to the page it was opened over, which is what content scripts and `chrome.scripting` are for.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[EXTENSION_NAME]</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <header class="header">
      <h1>[EXTENSION_NAME]</h1>
      <p class="subtitle">Brief tagline here</p>
    </header>

    <main class="content">
      <div class="section">
        <label for="input-field">Label</label>
        <input type="text" id="input-field" placeholder="Enter value...">
      </div>
      <div class="actions">
        <button id="action-btn" class="primary">Primary Action</button>
      </div>
    </main>

    <footer class="footer">
      <div id="status" class="status"></div>
    </footer>
  </div>

  <script src="popup.js"></script>
</body>
</html>
```

```javascript
document.addEventListener('DOMContentLoaded', async () => {
  const actionBtn = document.getElementById('action-btn');
  const status = document.getElementById('status');

  const showStatus = (message, type = 'info') => {
    status.textContent = message;
    status.className = `status ${type}`;
  };

  actionBtn.addEventListener('click', async () => {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => document.title, // this body runs in the page, not the extension
      });
      showStatus(`Page title: ${results[0].result}`, 'success');
    } catch (error) {
      showStatus(`Error: ${error.message}`, 'error');
    }
  });
});
```

The function passed to `executeScript` is serialized and evaluated in the page, so it closes over nothing from the popup. A variable referenced from the surrounding scope is `undefined` there rather than an error at the call site.

Every `chrome.*` call is wrapped in a `try`/`catch`, because a permission the user revoked and a tab that closed both reject rather than returning an error value.

## Theme

Catppuccin Mocha is the default for a new extension. An extension that already has a palette keeps it.

```css
:root {
  --rosewater: #f5e0dc; --flamingo: #f2cdcd; --pink: #f5c2e7;
  --mauve: #cba6f7; --red: #f38ba8; --maroon: #eba0ac;
  --peach: #fab387; --yellow: #f9e2af; --green: #a6e3a1;
  --teal: #94e2d5; --sky: #89dceb; --sapphire: #74c7ec;
  --blue: #89b4fa; --lavender: #b4befe; --text: #cdd6f4;
  --subtext1: #bac2de; --subtext0: #a6adc8; --overlay2: #9399b2;
  --overlay1: #7f849c; --overlay0: #6c7086; --surface2: #585b70;
  --surface1: #45475a; --surface0: #313244; --base: #1e1e2e;
  --mantle: #181825; --crust: #11111b;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  background-color: var(--crust);
  color: var(--subtext0);
  min-width: 320px;
  max-width: 400px;
}

.container { padding: 16px; }
.header { margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--surface1); }
.footer { padding-top: 12px; border-top: 1px solid var(--surface1); }
.actions { display: flex; gap: 8px; margin-top: 16px; }

input, textarea {
  width: 100%;
  padding: 8px 12px;
  background-color: var(--surface0);
  color: var(--text);
  border: 1px solid var(--surface1);
  border-radius: 6px;
}
input:focus, textarea:focus { outline: none; border-color: var(--blue); }

button {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  background-color: var(--surface0);
  color: var(--text);
  border: 1px solid var(--surface1);
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}
button:hover { background-color: var(--surface1); }
button.primary { background-color: var(--blue); color: var(--crust); border: none; flex: 1; }
button.primary:hover { background-color: var(--sapphire); }
button:disabled { opacity: 0.5; cursor: not-allowed; }

.status { font-size: 12px; padding: 8px; border-radius: 6px; text-align: center; }
.status:empty { display: none; }
.status.success { color: var(--green);  background-color: rgba(166, 227, 161, 0.1); }
.status.error   { color: var(--red);    background-color: rgba(243, 139, 168, 0.1); }
.status.warning { color: var(--yellow); background-color: rgba(249, 226, 175, 0.1); }
.status.info    { color: var(--blue);   background-color: rgba(137, 180, 250, 0.1); }
```

The popup has a `min-width` and a `max-width` because Chrome sizes it from its content, and an unconstrained popup jumps in width as its status text changes.

`.status:empty { display: none; }` keeps an empty status area from reserving space before anything has happened.

## Content Scripts

A content script runs in the page's DOM but in an isolated JavaScript world, so it sees the page's elements and not its variables.

```javascript
(function () {
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getData') {
      sendResponse({
        success: true,
        data: { title: document.title, url: window.location.href },
      });
    }
    return true;
  });
})();
```

`return true` keeps the message channel open for an asynchronous `sendResponse`. Without it the channel closes when the listener returns and the reply is dropped.

The IIFE wrapper keeps declarations out of the shared script scope, since several content scripts can run in one page.

## Service Worker

The background service worker is event-driven and Chrome terminates it when idle, so nothing may be held in a module-level variable across events. State lives in `chrome.storage`.

```javascript
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ settings: { enabled: true } });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'someAction') {
    handleAction(message.data)
      .then((result) => sendResponse({ success: true, result }))
      .catch((error) => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

async function handleAction(data) {
  return { processed: true };
}
```

`onInstalled` seeds defaults once, so the first run has settings before any UI reads them.

## Storage

```javascript
async function loadSettings() {
  const { settings } = await chrome.storage.local.get('settings');
  return settings ?? { enabled: true };
}

async function saveSettings(settings) {
  await chrome.storage.local.set({ settings });
}

chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'local' && changes.settings) {
    applySettings(changes.settings.newValue);
  }
});
```

`chrome.storage.local` is used rather than `localStorage`, because the service worker has no `localStorage` and the two contexts would otherwise disagree about the same setting.

The `onChanged` listener is what keeps an open popup in step with a change made elsewhere, rather than each context caching its own copy.

## Icons

| Size | Shown in |
|---|---|
| 16x16 | the browser toolbar |
| 32x32 | the Windows taskbar |
| 48x48 | `chrome://extensions` |
| 128x128 | the install dialog and store listing |

All four are the same design scaled, in PNG with transparency, drawn from the Catppuccin palette so they read against both light and dark browser chrome. A design that only works at 128 pixels is unrecognizable at 16, which is the size a user actually looks at.
