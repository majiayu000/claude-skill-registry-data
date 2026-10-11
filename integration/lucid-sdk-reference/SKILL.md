---
name: lucid-sdk-reference
description: Lucid SDK documentation and patterns for extension development. Use when working with EditorClient, BlockProxy, LineProxy, PageProxy, panels, modals, menus, data connectors, shape libraries, or any Lucid SDK features.
allowed-tools: Read, WebFetch, Grep, Glob
---

# Lucid SDK Reference

This skill provides comprehensive guidance for developing Lucid extensions, specifically tailored for the Quodsi project.

## Quick Links

- **Official Documentation**: https://developer.lucid.co/docs/
- **Extension API**: https://developer.lucid.co/extension-api/
- **Custom Shapes**: https://developer.lucid.co/custom-shapes/
- **Local Reference**: See [lucid-reference.md](lucid-reference.md)

## SDK Architecture Overview

The Lucid Extension SDK uses a **proxy-based architecture** for interacting with documents:

```
EditorClient (entry point)
    ├── DocumentProxy (document-level operations)
    │   ├── PageProxy (page management)
    │   │   ├── BlockProxy (shapes)
    │   │   ├── LineProxy (connectors)
    │   │   └── GroupProxy (grouped items)
    │   └── properties (document data)
    ├── Viewport (view state, selection)
    ├── Menu (dropdown/context menus)
    ├── Modal (dialog windows)
    └── Panel (docked UI panels)
```

## Key Classes Used in Quodsi

| Class | Purpose | Quodsi Usage |
|-------|---------|--------------|
| `EditorClient` | Main SDK entry point | Extension initialization, actions |
| `DocumentProxy` | Document access | Storing model data |
| `PageProxy` | Page operations | Getting blocks/lines, creating shapes |
| `BlockProxy` | Shape manipulation | Simulation objects (Activity, Resource) |
| `LineProxy` | Connector manipulation | Connectors between activities |
| `CustomBlockProxy` | Custom shape handling | Quodsi shape library shapes |
| `Panel` | Right dock UI | React app integration |
| `Viewport` | Selection, view state | Tracking user selection |

## Extension Scopes

Extensions declare capabilities in `manifest.json`:

| Scope | Description |
|-------|-------------|
| `READ` | Read document elements and data |
| `WRITE` | Modify document elements and data |
| `SHOW_MODAL` | Display modal dialogs |
| `CUSTOM_UI` | Create panels in right dock |
| `DOWNLOAD` | Enable file downloads |
| `NETWORK` | Direct XHR API access |
| `OAUTH_TOKEN` | Access user OAuth tokens |
| `USER_INFO` | Access user information |

## Common Patterns

### Getting Current Selection
```typescript
const client = new EditorClient();
const viewport = new Viewport(client);
const selectedItems = viewport.getSelectedItems();
```

### Iterating Blocks on a Page
```typescript
const document = new DocumentProxy(client);
for (const [pageId, page] of document.pages) {
    for (const [blockId, block] of page.allBlocks) {
        // Process each block
    }
}
```

### Checking Custom Shape Type
```typescript
if (block instanceof CustomBlockProxy) {
    if (block.isFromStencil('quodsi_shape_library', 'Activity')) {
        // Handle Activity shape
    }
}
```

### Panel Communication (Extension → React)
```typescript
// In Panel subclass
this.sendMessage({ type: 'DATA_UPDATE', payload: data });

// In React app
window.addEventListener('message', (e) => {
    const { type, payload } = e.data;
});
```

### Panel Communication (React → Extension)
```typescript
// In React app
parent.postMessage({ type: 'SAVE_REQUEST', data }, '*');

// In Panel subclass
protected messageFromFrame(message: JsonSerializable): void {
    if (message.type === 'SAVE_REQUEST') {
        // Handle save
    }
}
```

## Quodsi-Specific Implementation

### Shape Library Location
`/shapelibraries/quodsi_shape_library/`

### Extension Entry Point
`/editorextensions/quodsi_editor_extension/src/extension.ts`

### Key Services
- `ModelManager`: Central coordinator for model state
- `StorageAdapter`: Handles LucidChart storage persistence
- `MessageRouter`: Routes messages between extension and panels

### Data Storage Pattern
```typescript
// Store model data on document
client.document.setData('modelDefinition', JSON.stringify(model));

// Retrieve model data
const data = client.document.getData('modelDefinition');
const model = JSON.parse(data);
```

## Troubleshooting

1. **Panel not receiving messages**: Ensure panel is ready before sending (handle `REACT_APP_READY`)
2. **Block class not found**: Call `client.loadBlockClasses(['ClassName'])` first
3. **Shape data not persisting**: Use `properties.set()` for shape-level data
4. **Custom shapes not recognized**: Verify library/shape names match folder structure

## Full API Reference

See [lucid-reference.md](lucid-reference.md) for complete API documentation including:
- All proxy class methods and properties
- Event handling
- Data import/sync
- OAuth integration
- Shape library development
