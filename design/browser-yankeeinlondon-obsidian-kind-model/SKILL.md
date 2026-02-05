---
name: browser
description: Expert knowledge for modern browser technologies including HTML5, CSS (Grid, Flexbox, Container Queries, Scroll-Driven Animations, Anchor Positioning), Progressive Web Apps (PWA, Service Workers, Web Push, File System Access), and Browser APIs (Canvas, Geolocation, Web Storage, Web Share, Drag and Drop). Use when working with web standards, client-side features, responsive design, offline capabilities, or native-like web experiences.
last_updated: 2025-12-21T14:30:00Z
hash: d46d7bb644d9e28f
---

# Browser Technologies

Modern browser technologies have evolved into a comprehensive platform for building native-quality web applications. This skill covers HTML5, CSS (2025 standards), Progressive Web Apps, and Browser APIs.

## Core Principles

- **Progressive Enhancement**: Build baseline experiences that work everywhere, then layer advanced features
- **Feature Detection Over Browser Sniffing**: Use `'feature' in navigator` or `@supports` queries
- **Secure Contexts**: Most powerful features require HTTPS (or localhost for development)
- **User Consent**: Hardware and location APIs require explicit permission prompts
- **Performance First**: Use compositor-thread features (CSS animations, scroll-driven animations) over main-thread JavaScript
- **Accessibility by Default**: Semantic HTML + ARIA only when needed; never replace native elements
- **Container Queries for Components**: Use media queries for page layout, container queries for component responsiveness
- **CSS Custom Properties as Bridges**: Share state between JS and CSS via `--custom-properties`
- **Offline-First for PWAs**: Design for network failure; use Service Workers for resilient experiences
- **Sandbox vs. System**: OPFS for hidden app data, File System Access API for user files

## Quick Reference

### HTML5 Essentials

```html
<!-- Popover API (native top-layer management) -->
<button popovertarget="menu">Open</button>
<div id="menu" popover>Content</div>

<!-- Dialog (modal & non-modal) -->
<dialog id="modal">
  <button onclick="this.closest('dialog').close()">Close</button>
</dialog>
<script>document.getElementById('modal').showModal()</script>

<!-- Native details/summary (accordion) -->
<details>
  <summary>Click to expand</summary>
  <p>Hidden content</p>
</details>
```

### CSS Modern Layout

```css
/* Container Queries (component-aware) */
.wrapper {
  container-type: inline-size;
  container-name: card-container;
}

@container card-container (min-width: 400px) {
  .card { flex-direction: row; }
}

/* Grid with auto-responsive columns */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* Scroll-Driven Animation */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.element {
  animation: fade-in linear;
  animation-timeline: scroll();
}
```

### Progressive Web Apps

```javascript
// Service Worker Registration
if ('serviceWorker' in navigator) {
  await navigator.serviceWorker.register('/sw.js');
}

// Install Prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
});

// Web Push Notifications
const permission = await Notification.requestPermission();
const registration = await navigator.serviceWorker.ready;
const subscription = await registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
});
```

## Topics

### Core Technologies

- [HTML Standards](./html.md) - Semantic elements, ARIA, forms, media, Popover API
- [CSS Modern Features](./css.md) - Grid, Flexbox, Container Queries, Animations, Cascade Layers
- [Progressive Web Apps](./pwa.md) - Service Workers, Manifest, Installation, Offline capabilities

### Browser APIs

- [Web Storage](./web-storage.md) - localStorage, sessionStorage, IndexedDB strategy
- [File System Access](./file-system.md) - OPFS vs. device-level access, security model
- [Canvas & Graphics](./canvas.md) - 2D context, WebGL, OffscreenCanvas
- [Geolocation](./geolocation.md) - getCurrentPosition, watchPosition, accuracy handling
- [Web Share](./web-share.md) - Native share dialog integration
- [Drag and Drop](./drag-drop.md) - DataTransfer API, accessibility considerations

### Integration Patterns

- [HTML-JavaScript Interaction](./html-js-interaction.md) - DOM manipulation, event handling
- [CSS-JavaScript Interaction](./css-js-interaction.md) - Custom properties, View Transitions, Houdini

## Common Patterns

### Feature Detection Wrapper

```javascript
const BrowserFeatures = {
  // Check for API support
  has(feature) {
    const checks = {
      serviceWorker: 'serviceWorker' in navigator,
      geolocation: 'geolocation' in navigator,
      fileSystemAccess: 'showOpenFilePicker' in window,
      webShare: 'share' in navigator,
      containerQueries: CSS.supports('container-type: inline-size'),
      viewTransitions: 'startViewTransition' in document
    };
    return checks[feature] ?? false;
  },

  // Graceful degradation
  async fileOperation(content) {
    if (this.has('fileSystemAccess')) {
      // Chromium: Direct file access
      const handle = await window.showSaveFilePicker();
      const writable = await handle.createWritable();
      await writable.write(content);
      await writable.close();
    } else {
      // Fallback: Blob download
      const blob = new Blob([content], {type: 'text/plain'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'file.txt';
      a.click();
    }
  }
};
```

### Responsive Component (Container Query)

```css
/* Define container */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Mobile-first base */
.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Container-based breakpoints */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}

@container card (min-width: 600px) {
  .card {
    padding: 2cqi; /* Container query units */
  }
}
```

## Browser Support Strategy

### Baseline Features (98%+ support - 2025)
- Service Workers, Web App Manifest, Web Push
- CSS Grid, Flexbox, Custom Properties
- Container Queries (size-based)
- localStorage, sessionStorage
- Canvas 2D, Geolocation
- Popover API, Dialog element

### Chromium-Exclusive (Chrome/Edge only)
- File System Access API (device-level)
- Web Bluetooth, Web USB, Web Serial
- Multi-Screen Window Placement
- Protocol Handlers (full integration)

### Progressive Enhancement Pattern

```javascript
// Always provide fallback
if (BrowserFeatures.has('webShare')) {
  button.onclick = async () => {
    await navigator.share({ title, text, url });
  };
} else {
  button.onclick = () => {
    navigator.clipboard.writeText(url);
    showToast('Link copied!');
  };
}
```

## Resources

- [WHATWG HTML Living Standard](https://html.spec.whatwg.org/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web)
- [Can I Use](https://caniuse.com/)
- [W3C WAI-ARIA](https://www.w3.org/WAI/standards-guidelines/aria/)
- [Web.dev](https://web.dev/)
- [Chrome Platform Status](https://chromestatus.com/)
