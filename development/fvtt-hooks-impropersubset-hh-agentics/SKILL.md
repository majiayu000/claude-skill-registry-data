---
name: fvtt-hooks
description: This skill should be used when registering hooks, creating custom hooks for module APIs, debugging hook execution, handling async in hooks, or preventing memory leaks from unclean hook removal. Covers Hooks.on/once/call/callAll, lifecycle order, and common pitfalls.
---

# Foundry VTT Hooks

**Domain:** Foundry VTT Module/System Development
**Status:** Production-Ready
**Last Updated:** 2026-01-04

## Overview

Foundry VTT uses an event-driven architecture where hooks allow modules to intercept and respond to VTT workflows. Understanding hooks is fundamental to all Foundry development.

### When to Use This Skill

- Registering event handlers for document changes
- Creating module APIs that other packages can consume
- Debugging hook execution order
- Preventing memory leaks from orphaned hooks
- Understanding async limitations in hooks

### Core Concepts

| Method | Purpose | Cancellable | Persists |
|--------|---------|-------------|----------|
| `Hooks.on(name, fn)` | Register persistent listener | N/A | Yes |
| `Hooks.once(name, fn)` | Register one-time listener | N/A | No |
| `Hooks.call(name, ...args)` | Trigger hook (stoppable) | Yes | N/A |
| `Hooks.callAll(name, ...args)` | Trigger hook (all run) | No | N/A |
| `Hooks.off(name, id)` | Unregister by ID | N/A | N/A |

## Lifecycle Hooks (Execution Order)

These fire once per client connection, in this order:

```
init → i18nInit → setup → ready
```

| Hook | When | Use For |
|------|------|---------|
| `init` | Foundry initializing | Register sheets, settings, CONFIG |
| `i18nInit` | Translations loaded | Localization-dependent setup |
| `setup` | Before Documents/UI/Canvas | Pre-game state setup |
| `ready` | Game fully ready | World initialization, game data access |

```javascript
// Correct registration order
Hooks.once("init", () => {
  // Register settings
  game.settings.register("my-module", "mySetting", { /* ... */ });

  // Register document sheets
  DocumentSheetConfig.registerSheet(Actor, "my-module", MyActorSheet, {
    makeDefault: true
  });
});

Hooks.once("ready", () => {
  // Safe to access game.actors, game.users, etc.
  console.log(`${game.actors.size} actors in world`);
});
```

## Document Hooks

All document types follow this pattern:

| Hook | Trigger Method | Can Cancel |
|------|---------------|------------|
| `preCreate{Doc}` | `Hooks.call` | Yes |
| `create{Doc}` | `Hooks.callAll` | No |
| `preUpdate{Doc}` | `Hooks.call` | Yes |
| `update{Doc}` | `Hooks.callAll` | No |
| `preDelete{Doc}` | `Hooks.call` | Yes |
| `delete{Doc}` | `Hooks.callAll` | No |

```javascript
// Prevent update if condition met
Hooks.on("preUpdateActor", (actor, change, options, userId) => {
  if (change.system?.hp?.value < 0) {
    ui.notifications.warn("HP cannot be negative");
    return false; // Cancels the update
  }
});

// React after update
Hooks.on("updateActor", (actor, change, options, userId) => {
  if (change.system?.hp?.value === 0) {
    ChatMessage.create({ content: `${actor.name} has fallen!` });
  }
});
```

## Render Hooks

Render hooks fire for the entire inheritance chain:

```javascript
// renderActorSheet → renderDocumentSheet → renderFormApplication → renderApplication

// ApplicationV1 signature
Hooks.on("renderActorSheet", (app, html, data) => {
  html.find(".header").append("<button>Custom</button>");
});

// ApplicationV2 signature (V12+)
Hooks.on("renderActorSheetV2", (app, html, context, options) => {
  // html is the rendered element
});
```

## Common Pitfalls

### 1. Async Functions Cannot Cancel Hooks

**CRITICAL:** Hooks never await callbacks. Async functions return a Promise, not `false`.

```javascript
// WRONG - Won't prevent the update!
Hooks.on("preUpdateActor", async (actor, change, options, userId) => {
  const allowed = await someAsyncCheck();
  if (!allowed) return false; // Returns Promise, not false!
});

// CORRECT - Synchronous check for cancellation
Hooks.on("preUpdateActor", (actor, change, options, userId) => {
  if (!someCondition) return false; // Actually prevents update
});
```

### 2. Memory Leaks from Orphaned Hooks

Hooks keep references to callbacks, preventing garbage collection:

```javascript
// BAD - Hook persists after app closes
class MyApp extends Application {
  constructor() {
    super();
    Hooks.on("updateActor", this._onUpdate.bind(this));
  }
}

// GOOD - Store ID and clean up
class MyApp extends Application {
  constructor() {
    super();
    this._hookId = Hooks.on("updateActor", this._onUpdate.bind(this));
  }

  close(options) {
    Hooks.off("updateActor", this._hookId);
    return super.close(options);
  }
}
```

### 3. Object Mutation vs Re-assignment

Objects are passed by reference - mutation works, re-assignment doesn't:

```javascript
// WORKS - Mutation affects original
Hooks.on("preUpdateActor", (actor, change, options, userId) => {
  change.name = "Modified"; // Changes the actual update
});

// DOESN'T WORK - Re-assignment breaks reference
Hooks.on("preUpdateActor", (actor, change, options, userId) => {
  change = { name: "New" }; // Local variable only!
});
```

### 4. Hooks Fire Per-Client

Each client runs hooks independently. Check userId to avoid duplicate actions:

```javascript
// BAD - All clients try to create the item
Hooks.on("createActor", (actor, options, userId) => {
  actor.createEmbeddedDocuments("Item", [itemData]);
});

// GOOD - Only triggering client acts
Hooks.on("createActor", (actor, options, userId) => {
  if (userId !== game.user.id) return;
  actor.createEmbeddedDocuments("Item", [itemData]);
});
```

### 5. Hook Context (this) Issues

```javascript
// WRONG - Can't unregister by function reference
Hooks.on("updateActor", this.onUpdate);
Hooks.off("updateActor", this.onUpdate); // Fails!

// WRONG - bind() creates new function each time
Hooks.on("updateActor", this.onUpdate.bind(this));
Hooks.off("updateActor", this.onUpdate.bind(this)); // Different function!

// CORRECT - Use hook ID
this._hookId = Hooks.on("updateActor", this.onUpdate.bind(this));
Hooks.off("updateActor", this._hookId); // Works
```

## Creating Custom Hooks for Module APIs

### Basic Pattern

```javascript
// my-module.js
Hooks.once("init", () => {
  const api = {
    registerExtension: (config) => { /* ... */ },
    doAction: (data) => { /* ... */ }
  };

  // Expose API
  game.modules.get("my-module").api = api;

  // Announce readiness
  Hooks.callAll("myModuleReady", api);
});

// Other modules consume it
Hooks.once("myModuleReady", (api) => {
  api.registerExtension({ name: "My Extension" });
});
```

### Allowing Cancellation

```javascript
class MySystem {
  static performAction(data) {
    // Allow other modules to prevent action
    const allowed = Hooks.call("myModule.beforeAction", data);
    if (allowed === false) return null;

    const result = this._doWork(data);

    // Notify completion (cannot be cancelled)
    Hooks.callAll("myModule.afterAction", result);

    return result;
  }
}
```

### Naming Convention

Use namespaced names: `moduleName.eventName`
- `combatTracker.turnChanged`
- `tokenMagic.effectApplied`
- `myModule.ready`

## Debugging Hooks

### Enable Debug Mode

```javascript
// In browser console
CONFIG.debug.hooks = true;

// Toggle macro
CONFIG.debug.hooks = !CONFIG.debug.hooks;
console.warn("Hook debugging:", CONFIG.debug.hooks);
```

### Debug Specific Hook

```javascript
// Log arguments for a specific hook once
Hooks.once("updateActor", (...args) => console.log("updateActor args:", args));
```

### Developer Mode Module

Use the [Developer Mode](https://foundryvtt.com/packages/lib-dev-mode/) module for persistent debug flag management without shipping debug code.

## Implementation Checklist

- [ ] Use `Hooks.once` for init/setup/ready (not `Hooks.on`)
- [ ] Store hook IDs for any persistent hooks
- [ ] Clean up hooks in `close()` or destruction methods
- [ ] Check `userId === game.user.id` before document operations
- [ ] Never use async for `pre*` hooks that need cancellation
- [ ] Mutate objects, don't re-assign them
- [ ] Use namespaced names for custom hooks
- [ ] Use `Hooks.call` for cancellable events, `Hooks.callAll` for notifications

## Quick Reference: Common Hook Signatures

```javascript
// Document hooks
Hooks.on("preCreateActor", (document, data, options, userId) => {});
Hooks.on("createActor", (document, options, userId) => {});
Hooks.on("preUpdateActor", (document, change, options, userId) => {});
Hooks.on("updateActor", (document, change, options, userId) => {});
Hooks.on("preDeleteActor", (document, options, userId) => {});
Hooks.on("deleteActor", (document, options, userId) => {});

// Render hooks (V1)
Hooks.on("renderActorSheet", (app, html, data) => {});

// Render hooks (V2)
Hooks.on("renderActorSheetV2", (app, html, context, options) => {});

// Canvas hooks
Hooks.on("canvasReady", (canvas) => {});
Hooks.on("canvasPan", (canvas, position) => {});
```

## References

- [Hooks API Documentation](https://foundryvtt.com/api/classes/foundry.helpers.Hooks.html)
- [Hook Events Reference](https://foundryvtt.com/api/modules/hookEvents.html)
- [Community Wiki: Hooks](https://foundryvtt.wiki/en/development/api/hooks)
- [Community Wiki: Hooks Listening & Calling](https://foundryvtt.wiki/en/development/guides/Hooks_Listening_Calling)

---

**Last Updated:** 2026-01-04
**Status:** Production-Ready
**Maintainer:** ImproperSubset
