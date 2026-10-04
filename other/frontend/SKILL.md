---
name: frontend
description: Frontend development context for the Megahub project. Use when working on the web-based IDE, Vite build system, Blockly visual programming, Web Bluetooth API integration, JavaScript frontend code, CSS/styles, UI components, or anything in the /frontend/ directory.
---

# Frontend Development — Megahub IDE

## Tech Stack

- **Vite** — build tool and dev server
- **Blockly 12.3.1** — visual programming editor; custom blocks in `/frontend/src/components/blockly/` — see `blockly` skill for block authoring, Lua generators, and BLOCKS.md generation
- **Vanilla JS** — no framework (intentionally lightweight for ESP32 flash size)
- **Web Bluetooth API** — browser BLE, Chrome/Edge/Opera only
- **Prism.js** — Lua syntax highlighting in the preview panel
- **Web Components** — all sidebar panels are custom elements with Shadow DOM

## Build Modes

| Mode | Description |
|------|-------------|
| `dev` | Hot reload, localStorage for persistence, no BLE |
| `bt` | Production BLE mode, deployed to GitHub Pages |
| `web` | WiFi/HTTP mode, served from firmware WebServer |

Mode is available at runtime as `import.meta.env.VITE_MODE`.

---

## File Structure

```
frontend/
  index.html                  Main entry point (HTML skeleton)
  src/
    index.js                  App controller, event wiring, all Application.* methods
    bleclient.js              BLE protocol client (fragmentation, streaming, events)
    theme.css                 CSS design tokens (all --vscode-* variables)
    styles.css                Global styles, layout grid, all UI component CSS
    components/
      blockly/                Blockly editor + custom block definitions
      files/                  Project manager dialog (list/create/delete/autostart)
      logger/                 Terminal-style log output (max 50 entries)
      luapreview/             Syntax-highlighted Lua code preview
      portstatus/             Real-time LEGO port status cards
      ui/                     show_value block output display
      btdevicelist/           Bluetooth Classic device list + discovery
      sidebar-toggle/         Mobile sidebar toggle button
```

---

## VS Code Dark Theme System

All design tokens are CSS custom properties defined in `theme.css`. **Always use these — never hardcode colors or sizes.**

### Key Color Tokens

```css
--vscode-bg-primary: #1e1e1e      /* Main background */
--vscode-bg-secondary: #252526    /* Panels, cards, sidebar */
--vscode-bg-elevated: #2d2d30     /* Hover states */
--vscode-bg-input: #3c3c3c        /* Form inputs */

--vscode-text-primary: #cccccc    /* Main text */
--vscode-text-secondary: #858585  /* Muted text, breadcrumb items */
--vscode-text-tertiary: #6a6a6a   /* Very muted (separators) */
--vscode-text-bright: #ffffff     /* Headings, active labels */

--vscode-accent-blue: #007acc     /* Focus borders */
--vscode-accent-blue-dark: #0078d4 /* Primary buttons, status bar */
--vscode-accent-blue-hover: #1177bb
--vscode-accent-teal: #4ec9b0     /* Success, connected state */
--vscode-accent-yellow: #dcdcaa   /* Warning, connecting state */

--color-success: #4ec9b0
--color-error: #f48771
--color-error-bg: #5a1d1d
--color-warning: #dcdcaa

--vscode-border-light: #3c3c3c
--vscode-border-medium: #3e3e42
```

### Key Spacing / Sizing Tokens

```css
--spacing-xs: 0.25rem   --spacing-sm: 0.5rem
--spacing-md: 0.75rem   --spacing-lg: 1rem
--spacing-xl: 1.25rem   --spacing-2xl: 1.5rem

--transition-fast: 0.15s ease
--transition-medium: 0.3s ease

--header-height: 3rem
--z-modal: 1100   --z-tooltip: 2000
```

---

## Application Mode System

Three modes, switched via `Application.setMode(mode)`:

| Mode | View shown |
|------|-----------|
| `btconnect` | Welcome screen + connect button |
| `management` | Project list (files component) |
| `editor` | Blockly editor + sidebar controls |

### Visibility Mechanism

**`dynamicvisibility` class** (all modes):
```javascript
// setMode() sets display:block/none on elements with class dynamicvisibility
// Elements also have class visible-{mode} to declare when they appear
// e.g. class="dynamicvisibility visible-editor visible-management"
```
⚠ `setMode()` always sets `display: block` — do NOT use `dynamicvisibility` for elements that need `display: flex` or `display: grid`.

**`body.dataset.mode`** (CSS-based, for flex/grid elements):
```javascript
// setMode() also sets document.body.dataset.mode = mode
// Use CSS selectors: body[data-mode="editor"] .my-element { display: flex }
// Used by: header breadcrumb, back button
```

---

## Layout Grid

```
┌──────────────────────────────────────┐  ← header (3rem)
│ [←] Megahub IDE / project  [toggle] │
├──────────────────┬───────────────────┤  ← 1fr
│                  │ sidebar buttons   │
│  Blockly /       │ ─────────────────│
│  Files /         │ accordion panels  │
│  Welcome         │  lua / ports /   │
│                  │  ui / btdevices  │
├──────────────────┴───────────────────┤  ← footer (8–12rem)
│  Logger (terminal output)            │
├──────────────────────────────────────┤  ← statusbar (20px)
│ ● Connected to Megahub IDE           │
└──────────────────────────────────────┘
```

Desktop (≥1512px): 75/25 content/sidebar split. Mobile: sidebar is a slide-in overlay.

---

## Existing UI Patterns (use these, don't reinvent)

### Notifications (Toast)
```javascript
showNotification('success' | 'error' | 'warning' | 'info', title, message, durationMs)
// duration 0 = no auto-dismiss
// Returns the notification element (for manual dismissal)
```

### Confirmation Dialog
```javascript
const confirmed = await showConfirmDialog(title, message, {
  confirmText: 'Delete',   // default: 'Confirm'
  cancelText: 'Cancel',
  destructive: true        // red confirm button (default: true)
});
```

### Top Progress Bar
```javascript
Progress.show()   // indeterminate shimmer sweep
Progress.hide()
// Used for: project list load, file open, file save
```

### BLE Connection Modal
```javascript
ConnectionModal.show()              // resets all steps to pending
ConnectionModal.setStep(stepId)     // marks previous steps done, current active
ConnectionModal.setAllDone()        // all checkmarks
ConnectionModal.setError(stepId, message)  // marks step red, shows error text
ConnectionModal.hide()
// stepIds: 'requesting' | 'connecting' | 'services' | 'notifications' | 'mtu' | 'ready'
```

### VS Code Status Bar
```javascript
StatusBar.setConnecting()
StatusBar.setConnected(deviceName)
StatusBar.setDisconnected()
StatusBar.setMessage(text)   // right-side info text
StatusBar.clearMessage()
```

### Sidebar Icon Buttons
```css
.sidebar-icon-btn                   /* base */
.sidebar-icon-btn-primary           /* blue background (Execute) */
.sidebar-icon-btn-danger            /* red background (Stop) */
.sidebar-icon-btn-save              /* neutral, turns blue on hover */
.sidebar-icon-btn-toggle            /* teal when aria-pressed="true" */
.sidebar-icon-btn.btn-loading       /* spins the SVG icon */
```

---

## BLE Client Architecture (`bleclient.js`)

### Connection Flow
```
connect(onProgress?)
  → navigator.bluetooth.requestDevice()  [requires user gesture]
  → _setupGattConnection(onProgress?)
      → gatt.connect()
      → getPrimaryService()
      → getCharacteristic() × 4
      → startNotifications() × 3
      → sleep(200)  ← CRITICAL: BLE stack propagation delay
      → waitForMTU(2000)
      → testControlChannel()
  → emits onProgress callbacks at each step
```

### Message Protocol
- **5-byte fragment header**: type, messageId, fragmentNum(2), flags
- **MTU**: default 23 bytes, negotiated up to 517 bytes
- **Fragmentation**: automatic for all requests/responses
- **Streaming protocol**: for large file uploads (chunks + ACK window)

### Event System
```javascript
bleClient.addEventListener(APP_EVENT_TYPE_*, callback)
bleClient.removeAllEventListeners()
// Event types: LOG, PORTSTATUS, COMMAND, BTCLASSICDEVICES
```

### File Upload
```javascript
await bleClient.uploadFileStreaming(projectId, filename, content, onProgress?)
// Sliding window: 8 chunks in flight, waits for ACK before advancing
```

---

## Animation Principles

**All animations must be purposeful — each one communicates meaning:**

| Use case | Animation | Timing |
|----------|-----------|--------|
| State transitions | CSS `transition` | `var(--transition-fast)` = 0.15s ease |
| Indeterminate loading | Shimmer sweep (progress bar) | 1.4s linear infinite |
| Spinner (waiting) | Rotate 360° | 0.8s linear infinite |
| Step completion | Scale 0→1 + opacity | 0.15s ease-out (one-shot) |
| Status dot state change | Color transition | 0.3s ease |
| Connecting pulse | Opacity 1→0.3→1 | 1s ease-in-out infinite |

**Always wrap looping animations in:**
```css
@media (prefers-reduced-motion: reduce) {
  /* replace animation with instant state */
}
```

---

## Component Pattern (Web Components)

All sidebar panels are custom elements with Shadow DOM:
```javascript
class MyComponent extends HTMLElement {
  connectedCallback() {
    const shadow = this.attachShadow({ mode: 'open' });
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(styleSheet);   // import from style.css
    shadow.adoptedStyleSheets = [sheet];
    shadow.innerHTML = template;     // import from component.html
  }
}
customElements.define('custom-my-component', MyComponent);
```

Accordion behavior: dispatch `accordion-expand` / `accordion-collapse` custom events. Parent (`initSidebarAccordion()` in `index.js`) collapses all others on expand.

---

## Important Constraints

- **Bundle size**: Keep JS small — it's embedded in 4MB ESP32 flash
- **No framework**: No React/Vue/Angular — intentional
- **Shadow DOM**: Component styles are isolated; `theme.css` variables are inherited through the shadow boundary
- **Web Bluetooth**: User gesture required for `requestDevice()` — never call without a click handler
- **Supported browsers**: Chrome, Edge, Opera only — Firefox/Safari don't support Web Bluetooth
