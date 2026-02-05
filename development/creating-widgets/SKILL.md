---
name: creating-widgets
description: Creating new StickerNest widgets from scratch. Use when the user asks to create a widget, build a widget, add a new widget, make a widget component, or implement widget functionality. Covers manifest creation, HTML templates, TypeScript module structure, Protocol v3.0 communication, and widget registration.
---

# Creating StickerNest Widgets

This skill guides you through creating new widgets for StickerNest v2. Widgets are self-contained HTML/JS applications that run in sandboxed iframes and communicate via the postMessage API (Protocol v3.0).

## Widget Types

StickerNest supports two widget implementation approaches:

### 1. Inline HTML Widgets (Most Common)
TypeScript module that exports `manifest` + `html` string. Located in `src/widgets/builtin/`.

### 2. React Component Widgets (Advanced)
TypeScript/React component with separate manifest JSON. Located in `src/widgets/` subdirectories.

---

## Quick Start: Creating an Inline Widget

### Step 1: Create the Widget File

Create `src/widgets/builtin/MyWidget.ts`:

```typescript
import type { WidgetManifest } from '../../types/manifest';
import type { BuiltinWidget } from './index';

export const MyWidgetManifest: WidgetManifest = {
  id: 'stickernest.my-widget',        // MUST be lowercase with hyphens
  name: 'My Widget',
  version: '1.0.0',
  kind: 'display',                     // See widget kinds below
  entry: 'index.html',
  description: 'Brief description for AI context',
  author: 'StickerNest',
  tags: ['category', 'feature'],
  inputs: {
    // Input ports - see connecting-widget-pipelines skill
  },
  outputs: {
    // Output ports - see connecting-widget-pipelines skill
  },
  capabilities: {
    draggable: true,
    resizable: true,
    rotatable: true,
  },
  io: {
    inputs: ['trigger.activate'],      // AI wiring hints
    outputs: ['data.result'],
  },
  size: {
    width: 200,
    height: 150,
    minWidth: 100,
    minHeight: 80,
    scaleMode: 'scale',
  },
};

export const MyWidgetHTML = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .container {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--sn-bg-primary, #0f0f19);
      color: var(--sn-text-primary, #e2e8f0);
      padding: 12px;
    }
  </style>
</head>
<body>
  <div class="container" id="container">
    <!-- Widget content here -->
  </div>
  <script>
    (function() {
      const API = window.WidgetAPI;

      // State
      let state = {};

      // Initialize from saved state
      API.onMount(function(context) {
        state = context.state || {};
        // Initialize UI
        API.log('MyWidget mounted');
      });

      // Handle inputs
      API.onInput('trigger.activate', function(value) {
        // Handle trigger
      });

      // Handle state changes
      API.onStateChange(function(newState) {
        state = { ...state, ...newState };
        // Update UI
      });

      // Cleanup
      API.onDestroy(function() {
        API.log('MyWidget destroyed');
      });
    })();
  </script>
</body>
</html>
`;

export const MyWidget: BuiltinWidget = {
  manifest: MyWidgetManifest,
  html: MyWidgetHTML,
};
```

### Step 2: Register the Widget

Add to `src/widgets/builtin/index.ts`:

```typescript
import { MyWidget } from './MyWidget';

export const BUILTIN_WIDGETS: Record<string, BuiltinWidget> = {
  // ... existing widgets
  'stickernest.my-widget': MyWidget,
};

// Also add to re-exports at bottom
export { MyWidget };
```

---

## Widget Manifest Reference

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID: lowercase, alphanumeric, hyphens. Format: `stickernest.widget-name` |
| `name` | string | Display name for UI |
| `version` | string | Semantic version (X.Y.Z) |
| `kind` | WidgetKind | Widget category (see below) |
| `entry` | string | Entry file, usually `index.html` |
| `inputs` | Record | Input port definitions |
| `outputs` | Record | Output port definitions |
| `capabilities` | object | `{ draggable, resizable, rotatable }` |

### Widget Kinds

| Kind | Use Case |
|------|----------|
| `display` | Text, images, static content |
| `interactive` | Buttons, forms, user input |
| `container` | Groups other widgets |
| `2d` | 2D graphics, canvas |
| `3d` | Three.js, 3D content |
| `audio` | Audio players, visualizers |
| `video` | Video players |
| `hybrid` | Multiple content types |

### Optional Fields

```typescript
{
  description?: string;           // For AI context
  tags?: string[];                // Search/categorization
  author?: string;                // Creator info
  io?: WidgetCapabilityDeclaration; // AI wiring hints
  size?: WidgetSizeConfig;        // Default dimensions
  events?: { emits?: string[]; listens?: string[] }; // Broadcast events
  skin?: WidgetSkinManifest;      // Theming support
}
```

### Size Configuration

```typescript
size: {
  width: 200,           // Default width
  height: 150,          // Default height
  minWidth: 100,        // Minimum width
  minHeight: 80,        // Minimum height
  maxWidth?: 800,       // Maximum width
  maxHeight?: 600,      // Maximum height
  aspectRatio?: 16/9,   // Lock aspect ratio
  lockAspectRatio?: true,
  scaleMode: 'scale' | 'crop' | 'stretch' | 'contain',
}
```

---

## WidgetAPI Reference

The `window.WidgetAPI` object provides the interface for widget communication:

### Lifecycle

```javascript
API.onMount(callback)      // Called when widget loads, receives context with state
API.onDestroy(callback)    // Called before widget unloads
```

### State Management

```javascript
API.setState({ key: value })           // Save persistent state
API.onStateChange(callback)            // Listen for external state changes
```

### Input/Output (Pipelines)

```javascript
API.onInput('portId', callback)        // Listen for pipeline inputs
API.emitOutput('portId', data)         // Emit to pipeline outputs
```

### Events (Broadcast)

```javascript
API.emit('eventName', payload)         // Emit broadcast event
API.on('eventName', callback)          // Listen for broadcast events
```

### Utilities

```javascript
API.log(message)                       // Debug logging
API.getAssetUrl(path)                  // Resolve asset URLs
```

---

## Theme Tokens

Use StickerNest CSS variables for consistent theming:

```css
/* Backgrounds */
--sn-bg-primary: #0f0f19;
--sn-bg-secondary: #1a1a2e;
--sn-bg-tertiary: #252538;

/* Text */
--sn-text-primary: #e2e8f0;
--sn-text-secondary: #94a3b8;

/* Accents */
--sn-accent-primary: #8b5cf6;
--sn-success: #22c55e;
--sn-error: #ef4444;
--sn-warning: #f59e0b;

/* Borders */
--sn-border-primary: rgba(139, 92, 246, 0.2);
--sn-radius-sm: 4px;
--sn-radius-md: 6px;
--sn-radius-lg: 8px;
```

---

## Common Patterns

### Editable Content

```javascript
API.onInput('content.set', function(value) {
  state.content = value;
  updateDisplay();
  API.setState({ content: value });
  API.emitOutput('content.changed', value);
});
```

### Click Handling

```javascript
element.addEventListener('click', function() {
  API.emit('clicked', { timestamp: Date.now() });
  API.emitOutput('ui.clicked', {});
});
```

### Loading External Data

```javascript
API.onMount(async function(context) {
  try {
    const response = await fetch(API.getAssetUrl('data.json'));
    const data = await response.json();
    // Use data
  } catch (err) {
    API.log('Failed to load data: ' + err.message);
  }
});
```

---

## Validation Checklist

Before registering a new widget:

- [ ] `id` is lowercase with hyphens only (e.g., `stickernest.my-widget`)
- [ ] `version` follows semver (X.Y.Z)
- [ ] All required manifest fields present
- [ ] Input/output port IDs match between manifest and code
- [ ] Uses `window.WidgetAPI` for communication
- [ ] Has `onMount` and `onDestroy` lifecycle handlers
- [ ] Uses CSS variables for theming
- [ ] Added to `BUILTIN_WIDGETS` registry
- [ ] Added to re-exports

---

## Reference Files

- **Manifest types**: `src/types/manifest.ts`
- **Widget registry**: `src/widgets/builtin/index.ts`
- **Example widget**: `src/widgets/builtin/BasicTextWidget.ts`
- **Protocol docs**: `Docs/WIDGET-DEVELOPMENT.md`
- **Full spec**: `Docs/WIDGET-PROTOCOL-SPEC.md`
