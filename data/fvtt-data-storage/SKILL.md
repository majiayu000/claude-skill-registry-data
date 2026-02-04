---
name: fvtt-data-storage
description: This skill should be used when choosing between flags, settings, or files for data storage, implementing document flags, registering module settings, handling file uploads, or migrating data between storage types. Covers namespacing, scope types, and performance optimization.
---

# Foundry VTT Data Storage

**Domain:** Foundry VTT Module/System Development
**Status:** Production-Ready
**Last Updated:** 2026-01-04

## Overview

Foundry VTT provides three primary storage mechanisms: Flags (document-attached), Settings (global config), and Files (external storage). Choosing the wrong method is a common source of bugs and performance issues.

### When to Use This Skill

- Deciding where to store module/system data
- Implementing document-specific custom properties
- Creating module configuration options
- Handling large datasets that impact performance
- Migrating data between storage types

### Quick Decision Matrix

| Need | Use | Why |
|------|-----|-----|
| Data on specific document | **Flags** | Travels with document, respects permissions |
| Global module config | **Settings** (world) | Synced to all clients, GM-controlled |
| Per-device preference | **Settings** (client) | localStorage, user-specific |
| Large datasets | **Files** | No performance impact on documents |
| Export/import data | **Files** | Portable, shareable |

## Flags

Flags attach key-value data to Documents (Actors, Items, Scenes, etc.).

### Basic Usage

```javascript
// Set a flag
await actor.setFlag('my-module', 'customProperty', { value: 42 });

// Get a flag
const data = actor.getFlag('my-module', 'customProperty');
// data === { value: 42 }

// Delete a flag
await actor.unsetFlag('my-module', 'customProperty');

// Direct access (read-only)
const value = actor.flags['my-module']?.customProperty;
```

### Namespacing

Always use your module ID as the scope:

```javascript
// CORRECT - Uses module ID
await doc.setFlag('my-module-id', 'flagName', value);

// WRONG - Generic scope causes collisions
await doc.setFlag('world', 'flagName', value);
```

### Batch Updates

```javascript
// BAD - Three database writes
await actor.setFlag('myModule', 'flag1', value1);
await actor.setFlag('myModule', 'flag2', value2);
await actor.setFlag('myModule', 'flag3', value3);

// GOOD - Single database write
await actor.update({
  'flags.myModule.flag1': value1,
  'flags.myModule.flag2': value2,
  'flags.myModule.flag3': value3
});
```

### Nested Flag Operations

```javascript
// Delete nested key (V10+)
await doc.unsetFlag('myModule', 'todos.completedItem');

// Alternative: Foundry deletion syntax
await doc.setFlag('myModule', 'todos', { '-=completedItem': null });
```

### Pitfalls

**1. Periods in Object Keys Break getFlag:**

```javascript
// BROKEN - Period in key causes issues
await doc.setFlag('myModule', 'data', { 'some.key': 'value' });
const result = doc.getFlag('myModule', 'data');
// result !== { 'some.key': 'value' } - Data corrupted!

// WORKAROUND - Use class instance (treated as complex object)
class MyData {
  constructor(data) { Object.assign(this, data); }
}
await doc.setFlag('myModule', 'data', new MyData({ 'some.key': 'value' }));
```

**2. Inactive Module Throws Error:**

```javascript
// UNSAFE - Throws if module not installed
const value = doc.getFlag('optional-module', 'flag');

// SAFE - Handle missing module
const value = doc.flags['optional-module']?.flag ?? defaultValue;
```

## Settings

Settings store global configuration with different scopes.

### Scope Types

| Scope | Storage | Editable By | Synced | Use For |
|-------|---------|-------------|--------|---------|
| `client` | localStorage | Any user | No | UI prefs, device settings |
| `world` | Database | GM only | Yes | Module config, rules |
| `user` (V13+) | Database | That user | Yes | Per-user cross-device |

### Registration

```javascript
Hooks.once('init', () => {
  // Client setting - per-device
  game.settings.register('myModule', 'theme', {
    name: 'UI Theme',
    hint: 'Select your preferred theme',
    scope: 'client',
    config: true,
    type: String,
    choices: {
      light: 'Light',
      dark: 'Dark'
    },
    default: 'light',
    onChange: value => applyTheme(value)
  });

  // World setting - shared, GM-only
  game.settings.register('myModule', 'enableFeature', {
    name: 'Enable Feature',
    hint: 'Turns on the special feature for all users',
    scope: 'world',
    config: true,
    type: Boolean,
    default: false,
    requiresReload: true  // V10+ prompts user to reload
  });
});
```

### Hidden Settings with Menus

For complex config, hide the setting and use a FormApplication:

```javascript
// 1. Register menu button
game.settings.registerMenu('myModule', 'configMenu', {
  name: 'Advanced Configuration',
  label: 'Configure',
  icon: 'fas fa-cog',
  type: MyConfigApp,
  restricted: true  // GM only
});

// 2. Register hidden backing setting
game.settings.register('myModule', 'config', {
  scope: 'world',
  config: false,  // Hidden from settings UI
  type: Object,
  default: { option1: true, threshold: 10 }
});

// 3. Access in FormApplication
class MyConfigApp extends FormApplication {
  getData() {
    return game.settings.get('myModule', 'config');
  }

  async _updateObject(event, formData) {
    await game.settings.set('myModule', 'config',
      foundry.utils.expandObject(formData)
    );
  }
}
```

### Setting Types

```javascript
// Choices dropdown
game.settings.register('myModule', 'mode', {
  type: String,
  choices: { a: 'Option A', b: 'Option B' },
  default: 'a'
});

// Number with range slider
game.settings.register('myModule', 'volume', {
  type: Number,
  range: { min: 0, max: 100, step: 5 },
  default: 50
});

// File picker
game.settings.register('myModule', 'backgroundImage', {
  type: String,
  filePicker: 'image',  // 'audio', 'video', 'any'
  default: ''
});

// DataModel for validation (recommended)
game.settings.register('myModule', 'validated', {
  type: MyDataModel,
  default: {}
});
```

### onChange Behavior

```javascript
// Client scope: fires only on this client
game.settings.register('myModule', 'clientSetting', {
  scope: 'client',
  onChange: value => {
    // Only runs locally
  }
});

// World scope: fires on ALL clients
game.settings.register('myModule', 'worldSetting', {
  scope: 'world',
  onChange: value => {
    // Runs everywhere when GM changes it
    // Re-fetch to ensure consistency
    const current = game.settings.get('myModule', 'worldSetting');
  }
});
```

## Files

Use file storage for large datasets or exportable data.

### When to Use Files

- Data > 100KB that would slow document operations
- Export/import functionality
- Asset management (images, audio)
- Sharing data between worlds

### FilePicker Upload

```javascript
// Upload a file
const file = new File(
  [JSON.stringify(data, null, 2)],
  'export.json',
  { type: 'application/json' }
);

await FilePicker.upload(
  'data',           // source: 'data', 'public', 's3'
  'myModule/data',  // target directory
  file,
  {},
  { notify: true }
);
```

### Reading Files

```javascript
// Fetch and parse JSON
async function loadData(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to load ${path}`);
  return response.json();
}

const data = await loadData('modules/myModule/data/config.json');
```

### Lazy Loading Pattern

Store file reference in flag, load on demand:

```javascript
// Store reference
await actor.setFlag('myModule', 'dataFile', 'myModule/data/actor-123.json');

// Load when needed
async function getActorData(actor) {
  const path = actor.getFlag('myModule', 'dataFile');
  if (!path) return null;
  return loadData(path);
}
```

## Common Mistakes

### Wrong: Flags for Module Config

```javascript
// BAD - Config doesn't belong on a random document
await game.user.setFlag('myModule', 'globalConfig', config);

// GOOD - Use world setting
game.settings.register('myModule', 'globalConfig', {
  scope: 'world',
  config: false,
  type: Object
});
```

### Wrong: Large Data in Flags

```javascript
// BAD - Slows every actor update
await actor.setFlag('myModule', 'history', arrayWith10000Entries);

// GOOD - Store in file, reference in flag
const file = new File([JSON.stringify(history)], `${actor.id}-history.json`);
await FilePicker.upload('data', 'myModule/history', file);
await actor.setFlag('myModule', 'historyFile', `myModule/history/${actor.id}-history.json`);
```

### Wrong: Client Setting for Shared State

```javascript
// BAD - Each user sees different value
game.settings.register('myModule', 'gameRule', {
  scope: 'client',  // Wrong scope!
  type: Boolean
});

// GOOD - World scope for shared rules
game.settings.register('myModule', 'gameRule', {
  scope: 'world',
  type: Boolean
});
```

## Migration Between Storage Types

### Flag to Setting

```javascript
Hooks.once('ready', async () => {
  const version = game.settings.get('myModule', 'schemaVersion') ?? 0;

  if (version < 2) {
    // Collect data from actor flags
    const migrated = {};
    for (const actor of game.actors) {
      const old = actor.getFlag('myModule', 'oldData');
      if (old) {
        migrated[actor.id] = old;
        await actor.unsetFlag('myModule', 'oldData');
      }
    }

    // Store in setting
    await game.settings.set('myModule', 'migratedData', migrated);
    await game.settings.set('myModule', 'schemaVersion', 2);

    ui.notifications.info('MyModule: Migration complete');
  }
});
```

### Setting to File (Large Data)

```javascript
async function migrateToFile() {
  const largeData = game.settings.get('myModule', 'bigSetting');

  // Export to file
  const file = new File(
    [JSON.stringify(largeData, null, 2)],
    'migrated-data.json',
    { type: 'application/json' }
  );
  await FilePicker.upload('data', 'myModule', file);

  // Update setting to path reference
  await game.settings.set('myModule', 'dataPath', 'myModule/migrated-data.json');
  await game.settings.set('myModule', 'bigSetting', null);
}
```

## Implementation Checklist

- [ ] Use module ID as flag scope (never 'world' or generic names)
- [ ] Register settings in `init` hook
- [ ] Use `scope: 'world'` for shared config, `scope: 'client'` for preferences
- [ ] Batch flag updates with `document.update()` when setting multiple
- [ ] Use files for data > 100KB
- [ ] Handle missing flags/settings with defaults
- [ ] Add `requiresReload: true` for settings that need refresh (V10+)
- [ ] Use DataModel for setting validation when possible

## References

- [Flags API](https://foundryvtt.wiki/en/development/api/flags)
- [Settings API](https://foundryvtt.wiki/en/development/api/settings)
- [Handling Data Guide](https://foundryvtt.wiki/en/development/guides/handling-data)
- [FilePicker API](https://foundryvtt.com/api/classes/foundry.applications.apps.FilePicker.html)

---

**Last Updated:** 2026-01-04
**Status:** Production-Ready
**Maintainer:** ImproperSubset
