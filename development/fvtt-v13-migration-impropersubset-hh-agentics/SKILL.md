---
name: fvtt-v13-migration
description: This skill should be used when the user asks to "migrate to V13", "upgrade to Foundry V13", "update module for V13", "fix V13 compatibility", "convert to ESM", "use DataModel", or mentions V13-specific patterns like hook signature changes, actor.system vs actor.data.data, or Application V2. Provides comprehensive Foundry VTT V13 development patterns and migration guidance.
---

# Foundry VTT V13 Development Guide

**Domain:** Foundry VTT Module/System Development
**Status:** Production-Ready
**Last Updated:** 2026-01-05

## Overview

This guide covers V13-specific patterns and migration from earlier versions. For modules targeting V13, follow these guidelines.

### When to Use This Skill

- Migrating a module/system from V12 or earlier to V13
- Converting CommonJS (`require`) to ESM (`import`/`export`)
- Implementing DataModel for structured data
- Updating deprecated patterns (`actor.data.data` to `actor.system`)
- Fixing hook signature changes after V13 upgrade
- Setting up V13-compatible manifest configuration

## Core Architecture Principles

### Use DataModel for Structured Data
**ALWAYS** use `foundry.abstract.DataModel` for defining data structures instead of plain JavaScript objects. DataModels provide:
- Built-in validation and type coercion
- Schema definition with `DataSchema`
- Automatic data preparation lifecycle
- Integration with Foundry's document system

Example:
```javascript
class MyModuleData extends foundry.abstract.DataModel {
  static defineSchema() {
    const fields = foundry.data.fields;
    return {
      name: new fields.StringField({ required: true, blank: false }),
      value: new fields.NumberField({ initial: 0, min: 0 }),
      enabled: new fields.BooleanField({ initial: true })
    };
  }
}
```

### ESM Modules Only
Foundry V13 uses **ECMAScript Modules (ESM)** exclusively. Your code must:
- Use `import` and `export` statements (NO `require()`)
- Declare `"esmodules"` in your manifest (NOT `"scripts"`)
- Use `.js` extensions in import paths when importing relative files

Example manifest entry:
```json
{
  "esmodules": ["scripts/module.js"],
  "scripts": []
}
```

### Internationalization (i18n)
**ALWAYS** use `game.i18n.localize()` or `game.i18n.format()` for user-facing text. Never hardcode English strings.

```javascript
// BAD
ui.notifications.info("Item created successfully");

// GOOD
ui.notifications.info(game.i18n.localize("MYMODULE.Notifications.ItemCreated"));

// For dynamic values
const message = game.i18n.format("MYMODULE.Notifications.ItemCreatedWithName", {
  name: itemName
});
```

Localization files go in `lang/en.json`:
```json
{
  "MYMODULE.Notifications.ItemCreated": "Item created successfully",
  "MYMODULE.Notifications.ItemCreatedWithName": "Item {name} created successfully"
}
```

## Common V13 Pitfalls

### Hook Arguments Have Changed
Many hooks in V13 have different argument signatures than V12. Always check the current API documentation.

**Example: `createToken` Hook**
```javascript
// V12 (OLD - WRONG in V13)
Hooks.on("createToken", (scene, tokenData, options, userId) => { });

// V13 (CORRECT)
Hooks.on("createToken", (tokenDocument, options, userId) => { });
```

### Document vs Data
V13 distinguishes between Document classes (e.g., `Actor`, `Item`) and their data models:
- Access document properties directly: `actor.name`, `item.system`
- Use `actor.system` to access system-specific data defined in your DataModel
- Avoid accessing `actor.data.data` (deprecated pattern from V10)

```javascript
// BAD (V10 pattern)
const hp = actor.data.data.attributes.hp.value;

// GOOD (V13 pattern)
const hp = actor.system.attributes.hp.value;
```

### Active Effects Structure
Active Effects in V13 use a cleaner structure:
- Effects are stored in `document.effects` (EffectCollection)
- Use `await actor.createEmbeddedDocuments("ActiveEffect", [effectData])`
- Effect changes use `key` (path to property) and `mode` (add, multiply, override, etc.)

```javascript
const effectData = {
  name: game.i18n.localize("MYMODULE.Effects.Blessed"),
  icon: "icons/magic/light/beam-rays-yellow.webp",
  changes: [{
    key: "system.attributes.ac.bonus",
    mode: CONST.ACTIVE_EFFECT_MODES.ADD,
    value: "2"
  }],
  duration: { rounds: 10 }
};

await actor.createEmbeddedDocuments("ActiveEffect", [effectData]);
```

### Canvas Rendering Layers
V13 has reorganized canvas layers. Use the correct layer references:
- `canvas.tokens` - TokenLayer
- `canvas.tiles` - TilesLayer
- `canvas.lighting` - LightingLayer
- `canvas.grid` - GridLayer

### Dialog API Updates
Dialog construction now prefers Application V2 patterns in some contexts, but classic Dialogs still work:

```javascript
new Dialog({
  title: game.i18n.localize("MYMODULE.Dialog.Title"),
  content: `<p>${game.i18n.localize("MYMODULE.Dialog.Content")}</p>`,
  buttons: {
    yes: {
      icon: '<i class="fas fa-check"></i>',
      label: game.i18n.localize("MYMODULE.Dialog.Confirm"),
      callback: () => { /* action */ }
    },
    no: {
      icon: '<i class="fas fa-times"></i>',
      label: game.i18n.localize("MYMODULE.Dialog.Cancel")
    }
  },
  default: "yes"
}).render(true);
```

## Data Field Types Reference

When defining DataModel schemas, use these field types from `foundry.data.fields`:

- `StringField` - Text data
- `NumberField` - Numeric values (integers or floats)
- `BooleanField` - True/false values
- `ObjectField` - Nested objects
- `ArrayField` - Arrays of values
- `SchemaField` - Nested DataModel schema
- `HTMLField` - Sanitized HTML content
- `FilePathField` - File paths (images, sounds, etc.)
- `ColorField` - Color values (hex strings)
- `AngleField` - Angles in degrees
- `AlphaField` - Alpha transparency (0-1)

## Best Practices

1. **Always await async operations** - Most Foundry operations are async
2. **Check for user permissions** - Use `game.user.isGM` or document permission checks
3. **Use `fromUuidSync()` or `fromUuid()`** - For reliable document references
4. **Leverage Hooks** - Don't override core behavior, extend it via hooks
5. **Handle errors gracefully** - Wrap operations in try/catch and show user-friendly messages
6. **Test with multiple users** - Permission and rendering issues often appear in multi-user scenarios
7. **Follow Foundry's module conventions** - Use proper manifest structure, versioning, and compatibility flags

## Manifest Requirements

Your `module.json` or `system.json` must declare V13 compatibility:

```json
{
  "id": "my-module",
  "title": "My Module",
  "version": "1.0.0",
  "compatibility": {
    "minimum": "13",
    "verified": "13",
    "maximum": "13"
  },
  "esmodules": ["scripts/init.js"],
  "languages": [
    {
      "lang": "en",
      "name": "English",
      "path": "lang/en.json"
    }
  ]
}
```

## Development Workflow

1. Enable "Developer Mode" in Foundry settings for better error messages
2. Use browser DevTools Console for debugging
3. Use `console.log()` liberally, or set up proper logging with `CONFIG.debug`
4. Test in a fresh world to avoid conflicts with other modules
5. Use `CONFIG.debug.hooks = true` to see all hook executions

Remember: When in doubt, check the official Foundry VTT V13 API documentation at https://foundryvtt.com/api/

## Implementation Checklist

### Module Structure
- [ ] Manifest declares `"esmodules"` (not `"scripts"`)
- [ ] All imports use ESM syntax with `.js` extensions
- [ ] Compatibility set to minimum V13

### Data Patterns
- [ ] DataModel classes define schemas with `defineSchema()`
- [ ] Access system data via `document.system` (not `data.data`)
- [ ] Active Effects use correct change structure

### Code Quality
- [ ] All user-facing strings use `game.i18n.localize()`
- [ ] Hook callbacks use V13 argument signatures
- [ ] Async operations are properly awaited
- [ ] Permissions checked before privileged operations

### Testing
- [ ] Module loads without console errors
- [ ] DataModel validation works correctly
- [ ] Hooks fire with expected arguments
- [ ] Multi-user scenarios tested

## References

- [Foundry VTT V13 API](https://foundryvtt.com/api/)
- [DataModel API](https://foundryvtt.com/api/classes/foundry.abstract.DataModel.html)
- [Migration Guide](https://foundryvtt.wiki/en/development/guides/v13-migration)
- [ESM in Foundry](https://foundryvtt.wiki/en/development/guides/esm)

---

**Last Updated:** 2026-01-05
**Status:** Production-Ready
**Maintainer:** ImproperSubset
