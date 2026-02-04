---
name: fvtt-version-compat
description: This skill should be used when importing Foundry classes, registering sheets, loading templates, enriching HTML, or using any Foundry API that has moved to namespaces. Covers compat wrappers, deferred sheet registration, and the modern-first fallback pattern.
---

# Foundry VTT Version Compatibility (V12/V13/V15+)

Use compatibility wrappers to avoid deprecation warnings when APIs move from globals to namespaces across Foundry versions.

## When to Use This Skill

Invoke this skill when:

### ✅ Use Compat Wrappers For:

- **Importing Foundry classes** - ActorSheet, ItemSheet, TextEditor
- **Registering sheets** - Actor sheets, item sheets, document sheets
- **Loading templates** - Handlebars template loading
- **Enriching HTML** - TextEditor.enrichHTML for journal content
- **Generating IDs** - randomID() for unique identifiers
- **Any Foundry API** - That has moved or will move to namespaces

### ❌ Don't Use Compat Wrappers For:

- **Stable globals** - `game`, `ui`, `CONFIG`, `Hooks`
- **Project-specific code** - Your own classes and functions
- **One-off migrations** - If only targeting a single Foundry version
- **Styling/layout** - CSS and templates (not API drift)

## The Problem: API Migration Across Versions

### What Changed Across Foundry Versions

**Foundry V11/V12 (Legacy):**
```javascript
// APIs available as globals
ActorSheet
ItemSheet
TextEditor.enrichHTML()
loadTemplates()
renderTemplate()
randomID()
Actors.registerSheet()
```

**Foundry V13+ (Namespaced):**
```javascript
// APIs moved to namespaces
foundry.appv1.sheets.ActorSheet
foundry.appv1.sheets.ItemSheet
foundry.applications.ux.TextEditor.implementation.enrichHTML()
foundry.applications.handlebars.loadTemplates()
foundry.applications.handlebars.renderTemplate()
foundry.utils.randomID()
foundry.applications.api.DocumentSheetConfig.registerSheet()
```

**Foundry V15+ (Legacy Removed):**
```
Globals will be REMOVED entirely
  ↓
Direct global access will break
  ↓
Must use namespaced APIs only
```

### Why This Breaks Code

```javascript
// ❌ This worked in V11/V12, will BREAK in V15+
import { ActorSheet } from "somewhere";  // No longer a global!

class MySheet extends ActorSheet {
  // ...
}

// ❌ This throws deprecation warnings in V13
TextEditor.enrichHTML(content, options);

// ❌ This will stop working in V15
Actors.registerSheet("my-module", MySheet, { makeDefault: true });
```

## Solution: Compatibility Wrappers

### Three Core Patterns

1. **Try modern first, fallback to legacy** - Nullish coalescing (`??`)
2. **Cache resolved classes** - Avoid repeated lookups
3. **Throw clear errors** - Don't silently fail if neither exists

## Step-by-Step Implementation

### Step 1: Create Compatibility Module

**File:** `scripts/compat.js`

```javascript
/**
 * Compatibility helpers for Foundry V12/V13/V15+
 * Prefer modern namespaced APIs, fallback to legacy globals
 */

/**
 * Get ActorSheet class (modern or legacy)
 * @returns {class} ActorSheet constructor
 */
export function getActorSheetClass() {
  // Try V13+ namespace first
  const modern = foundry?.appv1?.sheets?.ActorSheet;
  if (modern) return modern;

  // Fallback to V11/V12 global
  if (typeof ActorSheet !== 'undefined') return ActorSheet;

  throw new Error("Unable to resolve ActorSheet class");
}

/**
 * Get ItemSheet class (modern or legacy)
 * @returns {class} ItemSheet constructor
 */
export function getItemSheetClass() {
  return foundry?.appv1?.sheets?.ItemSheet ?? ItemSheet;
}

/**
 * Enrich HTML content (journal entries, descriptions)
 * @param {string} content - Raw HTML/markdown content
 * @param {object} options - Enrichment options
 * @returns {Promise<string>} Enriched HTML
 */
export function enrichHTML(content, options = {}) {
  // Try V13+ namespace
  const textEditor = foundry?.applications?.ux?.TextEditor?.implementation;

  if (textEditor?.enrichHTML) {
    return textEditor.enrichHTML(content, options);
  }

  // Fallback to V11/V12 global
  if (typeof TextEditor !== 'undefined' && TextEditor.enrichHTML) {
    return TextEditor.enrichHTML(content, options);
  }

  throw new Error("Unable to resolve TextEditor.enrichHTML");
}

/**
 * Generate random ID
 * @returns {string} Random ID
 */
export function generateRandomId() {
  const randomIdFn = foundry?.utils?.randomID ?? randomID;

  if (!randomIdFn) {
    throw new Error("Unable to resolve randomID generator");
  }

  return randomIdFn();
}
```

**Pattern:**
```javascript
// Template for adding new compat functions
export function getAPIClass() {
  // 1. Try modern namespace
  const modern = foundry?.path?.to?.API;
  if (modern) return modern;

  // 2. Fallback to legacy global
  if (typeof LegacyGlobal !== 'undefined') return LegacyGlobal;

  // 3. Throw clear error
  throw new Error("Unable to resolve API");
}
```

### Step 2: Sheet Registration Compatibility

**File:** `scripts/compat-helpers.js`

```javascript
import { getActorSheetClass, getItemSheetClass } from "./compat.js";

// Cache DocumentSheetConfig to avoid repeated lookups
let cachedSheetConfig;

/**
 * Get DocumentSheetConfig (modern V13+) or null
 * @returns {object|null}
 */
function getSheetConfig() {
  if (cachedSheetConfig) return cachedSheetConfig;

  // Try multiple V13+ namespace locations
  const apiConfig =
    foundry?.applications?.apps?.DocumentSheetConfig ??
    foundry?.applications?.config?.DocumentSheetConfig ??
    foundry?.applications?.api?.DocumentSheetConfig;

  cachedSheetConfig = apiConfig ?? null;
  return cachedSheetConfig;
}

/**
 * Get legacy Actors collection (V11/V12)
 * @returns {object}
 */
function getActorsCollectionLegacy() {
  return foundry?.documents?.collections?.Actors ?? Actors;
}

/**
 * Get legacy Items collection (V11/V12)
 * @returns {object}
 */
function getItemsCollectionLegacy() {
  return foundry?.documents?.collections?.Items ?? Items;
}

/**
 * Register actor sheet (compatible across versions)
 * @param {string} namespace - Module ID
 * @param {class} sheetClass - Sheet constructor
 * @param {object} options - Registration options
 */
export function registerActorSheet(namespace, sheetClass, options = {}) {
  const sheetConfig = getSheetConfig();

  // Try V13+ API
  if (sheetConfig?.registerSheet) {
    return sheetConfig.registerSheet(
      CONFIG.Actor.documentClass,
      namespace,
      sheetClass,
      options
    );
  }

  // Fallback to V11/V12 API
  return getActorsCollectionLegacy()?.registerSheet?.(
    namespace,
    sheetClass,
    options
  );
}

/**
 * Unregister actor sheet (compatible across versions)
 */
export function unregisterActorSheet(namespace, sheetClass) {
  const sheetConfig = getSheetConfig();

  if (sheetConfig?.unregisterSheet) {
    return sheetConfig.unregisterSheet(
      CONFIG.Actor.documentClass,
      namespace,
      sheetClass
    );
  }

  return getActorsCollectionLegacy()?.unregisterSheet?.(namespace, sheetClass);
}

/**
 * Register item sheet (compatible across versions)
 */
export function registerItemSheet(namespace, sheetClass, options = {}) {
  const sheetConfig = getSheetConfig();

  if (sheetConfig?.registerSheet) {
    return sheetConfig.registerSheet(
      CONFIG.Item.documentClass,
      namespace,
      sheetClass,
      options
    );
  }

  return getItemsCollectionLegacy()?.registerSheet?.(
    namespace,
    sheetClass,
    options
  );
}

/**
 * Unregister item sheet (compatible across versions)
 */
export function unregisterItemSheet(namespace, sheetClass) {
  const sheetConfig = getSheetConfig();

  if (sheetConfig?.unregisterSheet) {
    return sheetConfig.unregisterSheet(
      CONFIG.Item.documentClass,
      namespace,
      sheetClass
    );
  }

  return getItemsCollectionLegacy()?.unregisterSheet?.(namespace, sheetClass);
}
```

### Step 3: Template Loading Compatibility

```javascript
/**
 * Load Handlebars templates (compatible across versions)
 * @param {Array<string>} paths - Template paths
 * @returns {Promise}
 */
export function loadHandlebarsTemplates(paths) {
  // Try V13+ namespace
  const loader = foundry?.applications?.handlebars?.loadTemplates;

  if (loader) {
    return loader(paths);
  }

  // Fallback to V11/V12 global
  if (typeof loadTemplates !== 'undefined') {
    return loadTemplates(paths);
  }

  throw new Error("Unable to resolve Handlebars template loader");
}

/**
 * Render Handlebars template (compatible across versions)
 * @param {string} path - Template path
 * @param {object} data - Template data
 * @returns {Promise<string>}
 */
export function renderHandlebarsTemplate(path, data) {
  // Try V13+ namespace
  const renderer = foundry?.applications?.handlebars?.renderTemplate;

  if (renderer) {
    return renderer(path, data);
  }

  // Fallback to V11/V12 global
  if (typeof renderTemplate !== 'undefined') {
    return renderTemplate(path, data);
  }

  throw new Error("Unable to resolve Handlebars template renderer");
}
```

### Step 4: Use Compat Wrappers in Your Code

**File:** `scripts/module.js` (Entry point)

```javascript
import { registerActorSheet, registerItemSheet } from "./compat-helpers.js";
import { loadHandlebarsTemplates } from "./compat-helpers.js";
import { BladesAlternateActorSheet } from "./blades-alternate-actor-sheet.js";
import { BladesAlternateItemSheet } from "./blades-alternate-item-sheet.js";

const MODULE_ID = "my-module";

Hooks.once("init", async function() {
  console.log("My Module | Initializing");

  // Load templates (compat)
  await loadHandlebarsTemplates([
    "modules/my-module/templates/actor-sheet.html",
    "modules/my-module/templates/item-sheet.html",
  ]);
});

Hooks.once("ready", async function() {
  // Register sheets (compat)
  // Why ready hook? V13+ requires DocumentSheetConfig to be available
  // which isn't ready during init

  registerActorSheet(
    MODULE_ID,
    BladesAlternateActorSheet,
    {
      types: ["character"],
      makeDefault: true,
      label: "Alternate Character Sheet"
    }
  );

  registerItemSheet(
    MODULE_ID,
    BladesAlternateItemSheet,
    {
      types: ["item"],
      makeDefault: false,
      label: "Alternate Item Sheet"
    }
  );
});
```

**File:** `scripts/blades-alternate-actor-sheet.js`

```javascript
import { getActorSheetClass } from "./compat.js";
import { enrichHTML } from "./compat.js";

// Get base class via compat wrapper
const ActorSheet = getActorSheetClass();

export class BladesAlternateActorSheet extends ActorSheet {
  static get defaultOptions() {
    return foundry.utils.mergeObject(super.defaultOptions, {
      classes: ["bitd-alt", "sheet", "actor"],
      template: "modules/my-module/templates/actor-sheet.html",
      width: 900,
      height: 800,
    });
  }

  async getData() {
    const data = await super.getData();

    // Enrich description (compat)
    if (data.actor.system.description) {
      data.enrichedDescription = await enrichHTML(
        data.actor.system.description,
        { secrets: data.editable }
      );
    }

    return data;
  }
}
```

## Compatibility Patterns

### Pattern 1: Simple Class Resolution

```javascript
// Get class, throw if not found
export function getAPIClass() {
  const api = foundry?.new?.path?.API ?? LegacyGlobalAPI;

  if (!api) {
    throw new Error("Unable to resolve API");
  }

  return api;
}
```

### Pattern 2: Cached Resolution

```javascript
// Cache expensive lookups
let cachedConfig;

function getConfig() {
  if (cachedConfig) return cachedConfig;

  const config =
    foundry?.new?.path?.Config ??
    foundry?.another?.path?.Config ??
    LegacyConfig;

  cachedConfig = config ?? null;
  return cachedConfig;
}
```

### Pattern 3: Method Delegation

```javascript
// Wrap methods that moved
export function someMethod(...args) {
  const api = foundry?.new?.path?.API?.implementation;

  if (api?.someMethod) {
    return api.someMethod(...args);
  }

  if (typeof LegacyAPI !== 'undefined' && LegacyAPI.someMethod) {
    return LegacyAPI.someMethod(...args);
  }

  throw new Error("Unable to resolve someMethod");
}
```

### Pattern 4: Optional Chaining for Safety

```javascript
// Use ?. to safely traverse nested paths
export function getDeepAPI() {
  return (
    foundry?.level1?.level2?.level3?.API ??
    OldGlobal?.level1?.API ??
    LegacyAPI
  );
}
```

## Why Defer Sheet Registration to `ready` Hook?

### The Problem

```javascript
// ❌ BAD: Registering in init hook
Hooks.once("init", function() {
  registerActorSheet(MODULE_ID, MySheet, { ... });
});

// Result in V13+:
// Error: DocumentSheetConfig is not available yet!
```

### The Solution

```javascript
// ✅ GOOD: Register in ready hook
Hooks.once("ready", function() {
  registerActorSheet(MODULE_ID, MySheet, { ... });
});
```

**Why?**
- V11/V12: Sheet registration works in `init` hook (globals available)
- V13+: `DocumentSheetConfig` isn't initialized until after `init`
- V15+: Legacy globals won't exist, must use `DocumentSheetConfig`

**Solution:** Always register sheets in `ready` hook for V13+ compatibility

## Common Use Cases

### Use Case 1: Extend Base Sheet Class

```javascript
import { getActorSheetClass } from "./compat.js";

const ActorSheet = getActorSheetClass();

export class MyActorSheet extends ActorSheet {
  // No deprecation warnings!
}
```

### Use Case 2: Enrich Journal Content

```javascript
import { enrichHTML } from "./compat.js";

async function displayJournalEntry(content) {
  const enriched = await enrichHTML(content, {
    secrets: game.user.isGM,
    documents: true,
    links: true,
  });

  return enriched;
}
```

### Use Case 3: Load Templates on Init

```javascript
import { loadHandlebarsTemplates } from "./compat-helpers.js";

Hooks.once("init", async function() {
  await loadHandlebarsTemplates([
    "modules/my-module/templates/actor-sheet.html",
    "modules/my-module/templates/parts/abilities.html",
    "modules/my-module/templates/parts/items.html",
  ]);
});
```

### Use Case 4: Generate Unique IDs

```javascript
import { generateRandomId } from "./compat.js";

function createNewItem() {
  const item = {
    _id: generateRandomId(),
    name: "New Item",
    type: "item",
  };

  return item;
}
```

## Adding New Compat Functions

### Recipe for New API

1. **Identify the move**
   - V11/V12 global: `OldAPI`
   - V13+ namespace: `foundry.new.path.NewAPI`

2. **Add compat function**
   ```javascript
   export function getNewAPI() {
     return foundry?.new?.path?.NewAPI ?? OldAPI;
   }
   ```

3. **Update imports**
   ```javascript
   // Before
   import { OldAPI } from "somewhere";

   // After
   import { getNewAPI } from "./compat.js";
   const OldAPI = getNewAPI();
   ```

4. **Test across versions**
   - V11: Should use legacy global
   - V13: Should use modern namespace
   - No deprecation warnings in either

## API Migration Checklist

Common APIs that have moved or will move:

- [ ] `ActorSheet` → `foundry.appv1.sheets.ActorSheet`
- [ ] `ItemSheet` → `foundry.appv1.sheets.ItemSheet`
- [ ] `TextEditor.enrichHTML` → `foundry.applications.ux.TextEditor.implementation.enrichHTML`
- [ ] `loadTemplates` → `foundry.applications.handlebars.loadTemplates`
- [ ] `renderTemplate` → `foundry.applications.handlebars.renderTemplate`
- [ ] `randomID` → `foundry.utils.randomID`
- [ ] `Actors.registerSheet` → `DocumentSheetConfig.registerSheet`
- [ ] `Items.registerSheet` → `DocumentSheetConfig.registerSheet`
- [ ] `Dialog` → `DialogV2` (see dialog-compat skill)

## Testing Across Versions

### Manual Testing

```
1. Test in Foundry V11 (if supporting)
   - Check console for errors
   - Verify sheets register correctly
   - Confirm templates load

2. Test in Foundry V12
   - Same checks as V11
   - Look for deprecation warnings

3. Test in Foundry V13+
   - No deprecation warnings
   - All features work
   - Modern APIs used (check network/console)
```

### Console Verification

```javascript
// In browser console, verify which API is being used

// V11/V12 - Should use globals
console.log(typeof ActorSheet !== 'undefined');  // true

// V13+ - Should use namespaces
console.log(foundry?.appv1?.sheets?.ActorSheet);  // class ActorSheet
```

## Common Pitfalls

### ❌ Pitfall 1: Using Globals Directly

```javascript
// BAD: Will throw deprecation warnings in V13, break in V15
class MySheet extends ActorSheet {
  // ...
}
```

**Fix:** Use compat wrapper

```javascript
// GOOD
import { getActorSheetClass } from "./compat.js";
const ActorSheet = getActorSheetClass();

class MySheet extends ActorSheet {
  // ...
}
```

### ❌ Pitfall 2: Registering Sheets in Init Hook

```javascript
// BAD: Breaks in V13+
Hooks.once("init", function() {
  Actors.registerSheet(MODULE_ID, MySheet, { ... });
});
```

**Fix:** Use ready hook + compat wrapper

```javascript
// GOOD
import { registerActorSheet } from "./compat-helpers.js";

Hooks.once("ready", function() {
  registerActorSheet(MODULE_ID, MySheet, { ... });
});
```

### ❌ Pitfall 3: Not Handling Multiple Namespace Locations

```javascript
// BAD: Assumes single namespace location
export function getConfig() {
  return foundry?.applications?.api?.Config ?? LegacyConfig;
}

// Problem: Config might be in different namespace!
```

**Fix:** Check multiple locations

```javascript
// GOOD
export function getConfig() {
  return (
    foundry?.applications?.api?.Config ??
    foundry?.applications?.apps?.Config ??
    foundry?.applications?.config?.Config ??
    LegacyConfig
  );
}
```

### ❌ Pitfall 4: Silent Fallback Failures

```javascript
// BAD: Returns undefined if both fail
export function getAPI() {
  return foundry?.new?.API ?? OldAPI;
}

// Calling code will crash with cryptic error later
```

**Fix:** Throw clear error

```javascript
// GOOD
export function getAPI() {
  const api = foundry?.new?.API ?? OldAPI;

  if (!api) {
    throw new Error("Unable to resolve API - unsupported Foundry version?");
  }

  return api;
}
```

## Quick Checklist

Before using Foundry APIs:

- [ ] Identified if API has moved to namespace
- [ ] Created compat wrapper function
- [ ] Used compat wrapper instead of direct global
- [ ] Moved sheet registration to `ready` hook
- [ ] Cached expensive lookups (configs, classes)
- [ ] Threw clear errors if API not found
- [ ] Tested in V12 and V13+ (if targeting both)
- [ ] No deprecation warnings in console

## References

- Implementation: `scripts/compat.js` - Core compatibility wrappers
- Helpers: `scripts/compat-helpers.js` - Sheet registration, template loading
- Guide: `docs/compat-helpers-guide.md` - Usage examples
- Foundry API Docs: [Application V1 Migration](https://foundryvtt.com/article/v11-api-migration/)

For BitD Alternate Sheets:
- All sheet classes extend via `getActorSheetClass()` / `getItemSheetClass()`
- Sheet registration happens in `ready` hook via `registerActorSheet()`
- Template loading uses `loadHandlebarsTemplates()` in `init` hook
- HTML enrichment uses `enrichHTML()` wrapper
- Supports Foundry V12 minimum, tested through V13
- Prepared for V15+ when legacy globals are removed
