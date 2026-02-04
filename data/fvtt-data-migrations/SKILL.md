---
name: fvtt-data-migrations
description: This skill should be used when moving data between storage locations, changing data structures, renaming fields, or removing deprecated data. Covers schema versioning, safe migration methods, the Foundry unset operator, and idempotent migrations.
---

# Foundry VTT Data Migrations

Implement safe, version-controlled data migrations for Foundry VTT modules when changing data structures or storage locations.

## When to Use This Skill

Invoke this skill when implementing changes that require migrating existing user data:

### ✅ ALWAYS Create Migration For:

1. **Moving data between storage locations:**
   - `actor.system.field` → `actor.flags.myModule.field`
   - `actor.system.field` → embedded item
   - Flag namespace changes

2. **Changing data structures:**
   - Array → Object/Map
   - Object → Array
   - Flat structure → nested structure
   - Renaming properties

3. **Changing data types:**
   - String → Number
   - Boolean → String (enum)
   - Single value → Array
   - Null semantics changes

4. **Removing deprecated data:**
   - Cleaning up orphaned flags
   - Removing obsolete system fields
   - Purging invalid data

5. **Foundry version compatibility:**
   - API changes between Foundry versions
   - Deprecation of core fields

### ❌ NO Migration Needed For:

1. **Additive changes only:**
   - Adding NEW optional fields (with defaults)
   - Adding NEW features that don't touch existing data
   - UI-only changes (CSS, templates without data changes)

2. **Non-breaking changes:**
   - Adding new flags alongside existing ones
   - Extending data without modifying existing structure
   - Backwards-compatible additions

## Foundry Migration System Overview

### Schema Version Pattern

Foundry modules track data structure versions using a `schemaVersion` setting:

```javascript
// In settings.js - register the version tracker
game.settings.register("my-module", "schemaVersion", {
  name: "Schema Version",
  scope: "world",        // World-level (not per-client)
  config: false,         // Hidden from UI
  type: Number,
  default: 0,            // 0 = never migrated
});
```

**How it works:**
1. New worlds start at version 0
2. Each migration increments the version (1, 2, 3...)
3. Migration runs ONCE per world, on first `ready` hook
4. If `currentVersion >= targetVersion`, migration is skipped

### Migration Lifecycle

```
World Created (v0)
    ↓
First Load → ready hook
    ↓
Migration.migrate() called
    ↓
Check: currentVersion (0) < targetVersion (1)?
    ↓ YES
Run migration steps
    ↓
Set schemaVersion = 1
    ↓
Show completion notification
    ↓
Future loads: currentVersion (1) >= targetVersion (1) → SKIP
```

## Step-by-Step Migration Workflow

### Step 1: Identify the Breaking Change

**Ask yourself:**
- What data structure is changing?
- Where is the old data stored? (system field? flag? embedded doc?)
- Where will the new data be stored?
- What transformation is needed?

**Example scenarios:**

```javascript
// Scenario A: Moving system field to flag
OLD: actor.system["background-details"]
NEW: actor.flags["bitd-alternate-sheets"].background_details

// Scenario B: Changing structure
OLD: actor.flags.myModule["equipped-items"] = [{ id: "abc" }, { id: "def" }]
NEW: actor.flags.myModule["equipped-items"] = { "abc": {...}, "def": {...} }

// Scenario C: Cleaning up orphaned data
OLD: actor.flags.myModule.abilityProgress = { "Reflexes": 2, "abc123": 1 }
NEW: actor.flags.myModule.abilityProgress = { "abc123": 1 }  // Remove name-based keys
```

### Step 2: Increment Target Schema Version

**In `scripts/migration.js`:**

```javascript
export class Migration {
    static async migrate() {
        const currentVersion = game.settings.get(MODULE_ID, "schemaVersion") || 0;
        const targetVersion = 2;  // ← INCREMENT THIS (was 1, now 2)

        if (currentVersion < targetVersion) {
            // ... migration logic
        }
    }
}
```

**Version numbering:**
- Start: `targetVersion = 1` (first migration)
- Each new migration: increment by 1 (2, 3, 4...)
- Never skip numbers
- Never decrement

### Step 3: Create Migration Method

**Add a new static method to `Migration` class:**

```javascript
static async migrateFieldName(actor) {
    const oldValue = foundry.utils.getProperty(actor, "system.old-field");
    const newValue = actor.getFlag(MODULE_ID, "new_field");

    // Check if migration needed
    if (!oldValue) return;  // No old data to migrate
    if (newValue) {
        // New data already exists - just clean up old
        await actor.update({ "system.-=old-field": null });
        return;
    }

    // Perform migration
    const updates = {};
    updates[`flags.${MODULE_ID}.new_field`] = oldValue;
    updates["system.-=old-field"] = null;

    await actor.update(updates);
    console.log(`[MyModule] Migrated old-field for ${actor.name}`);
}
```

**Migration method naming:**
- `migrate{FeatureName}` - Descriptive of what's being migrated
- Examples: `migrateEquippedItems`, `migrateAbilityProgress`, `migrateLegacyFields`

### Step 4: Call Migration Method in migrate()

**Add to the migration sequence:**

```javascript
static async migrate() {
    const currentVersion = game.settings.get(MODULE_ID, "schemaVersion") || 0;
    const targetVersion = 2;

    if (currentVersion < targetVersion) {
        ui.notifications.info(
            "My Module: Migrating data, please wait..."
        );

        for (const actor of game.actors) {
            if (actor.type !== "character") continue;

            // Step 1: Existing migration
            await this.migrateEquippedItems(actor);

            // Step 2: NEW migration (add here)
            await this.migrateFieldName(actor);
        }

        await game.settings.set(MODULE_ID, "schemaVersion", targetVersion);
        ui.notifications.info("My Module: Migration complete.");
    }
}
```

**Order considerations:**
- Dependencies first (if migration B relies on migration A, run A first)
- Independent migrations can be in any order
- Comment the purpose of each step

### Step 5: Test Migration

**Testing checklist:**

1. **Create test world with OLD data structure:**
   - Use console to create old-format data: `game.actors.getName("Test").update({ "system.old-field": "test" })`
   - Verify old data exists

2. **Trigger migration:**
   - Reload world (triggers `ready` hook)
   - Watch console for migration logs
   - Check for errors

3. **Verify migration results:**
   - Check new data exists: `game.actors.getName("Test").getFlag("my-module", "new_field")`
   - Check old data removed: `game.actors.getName("Test").system["old-field"]` (should be undefined)
   - Verify notification appeared

4. **Verify migration runs ONCE:**
   - Reload world again
   - Check console - should NOT see migration logs (already at target version)

5. **Test with multiple actors:**
   - Create several test actors with old data
   - Verify all migrate correctly

## Safe Migration Patterns

### Pattern 1: System Field → Flag

```javascript
static async migrateLegacyFields(actor) {
    const updates = {};
    let changed = false;

    // Get old and new locations
    const oldValue = foundry.utils.getProperty(actor, "system.old-field");
    const newValue = actor.getFlag(MODULE_ID, "new_field");

    if (oldValue && !newValue) {
        // Old exists, new doesn't - migrate
        updates[`flags.${MODULE_ID}.new_field`] = oldValue;
        updates["system.-=old-field"] = null;
        changed = true;
    } else if (oldValue && newValue) {
        // Both exist - favor new, clean up old
        updates["system.-=old-field"] = null;
        changed = true;
    }

    if (changed) {
        await actor.update(updates);
        console.log(`[MyModule] Migrated old-field for ${actor.name}`);
    }
}
```

**Key points:**
- Check both old and new locations
- Handle case where both exist (favor new)
- Handle case where only old exists (migrate)
- Batch updates into single `actor.update()` call

### Pattern 2: Array → Object/Map

```javascript
static async migrateEquippedItems(actor) {
    const equipped = actor.getFlag(MODULE_ID, "equipped-items");

    // Check if still in old format (array)
    if (Array.isArray(equipped)) {
        const newMap = {};
        for (const item of equipped) {
            if (item && item.id) {
                newMap[item.id] = item;
            }
        }

        await actor.setFlag(MODULE_ID, "equipped-items", newMap);
        console.log(`[MyModule] Migrated equipped items for ${actor.name}`);
    }
}
```

**Key points:**
- Use `Array.isArray()` to detect old format
- Transform data structure
- Handle null/undefined items gracefully
- Use `setFlag()` to replace entire structure

### Pattern 3: Clean Up Orphaned Data

```javascript
static async migrateAbilityProgress(actor) {
    const progressMap = actor.getFlag(MODULE_ID, "abilityProgress") || {};
    if (foundry.utils.isEmpty(progressMap)) return;

    let changed = false;
    const updates = {};

    for (const [key, value] of Object.entries(progressMap)) {
        // Foundry IDs are always 16 characters
        if (key.length !== 16) {
            // This is likely a name-based key (orphaned) - remove it
            updates[`flags.${MODULE_ID}.abilityProgress.-=${key}`] = null;
            changed = true;
        }
    }

    if (changed) {
        await actor.update(updates);
        console.log(`[MyModule] Cleaned orphaned flags for ${actor.name}`);
    }
}
```

**Key points:**
- Use heuristics to identify orphaned data (length, format, etc.)
- Use `-=` syntax to remove specific keys: `"flags.module.field.-=keyToRemove"`
- Log what was cleaned for debugging

### Pattern 4: Batch Multiple Field Migrations

```javascript
static async migrateLegacyFields(actor) {
    const updates = {};
    let changed = false;

    // Migration 1: background-details
    const oldDetails = foundry.utils.getProperty(actor, "system.background-details");
    const newDetails = actor.getFlag(MODULE_ID, "background_details");
    if (oldDetails && !newDetails) {
        updates[`flags.${MODULE_ID}.background_details`] = oldDetails;
        updates["system.-=background-details"] = null;
        changed = true;
    }

    // Migration 2: vice-purveyor
    const oldPurveyor = foundry.utils.getProperty(actor, "system.vice-purveyor");
    const newPurveyor = actor.getFlag(MODULE_ID, "vice_purveyor");
    if (oldPurveyor && !newPurveyor) {
        updates[`flags.${MODULE_ID}.vice_purveyor`] = oldPurveyor;
        updates["system.-=vice-purveyor"] = null;
        changed = true;
    }

    // Single batched update for all changes
    if (changed) {
        await actor.update(updates);
        console.log(`[MyModule] Migrated legacy fields for ${actor.name}`);
    }
}
```

**Key points:**
- Accumulate all updates in single `updates` object
- Single `actor.update()` call at the end
- More efficient than multiple sequential updates

## Foundry Document Update Syntax

### Setting Values

```javascript
updates["system.field"] = newValue;                 // Set system field
updates[`flags.${MODULE_ID}.field`] = newValue;     // Set flag
updates["system.nested.deep.field"] = newValue;     // Set nested field
```

### Removing Fields (Unset)

```javascript
updates["system.-=oldField"] = null;                // Remove system field
updates[`flags.${MODULE_ID}.-=oldFlag`] = null;     // Remove flag
updates["flags.module.map.-=keyName"] = null;       // Remove map key
```

**The `-=` syntax:**
- Foundry's special unset operator
- Completely removes the field from the document
- Different from setting to `null` or `undefined` (which leaves the key)

### Using foundry.utils.getProperty

```javascript
// Safe nested property access (returns undefined if any level missing)
const value = foundry.utils.getProperty(actor, "system.deep.nested.field");

// vs direct access (throws if intermediate property missing)
const value = actor.system.deep.nested.field;  // Error if 'deep' undefined!
```

## Actor Iteration Patterns

### By Actor Type

```javascript
for (const actor of game.actors) {
    if (actor.type !== "character") continue;  // Only migrate characters
    await this.migrateCharacterFields(actor);
}
```

### All Actor Types

```javascript
for (const actor of game.actors) {
    // Migrate all actors regardless of type
    await this.migrateCommonFields(actor);
}
```

### Specific Types Only

```javascript
for (const actor of game.actors) {
    if (actor.type === "character") {
        await this.migrateCharacterFields(actor);
    } else if (actor.type === "crew") {
        await this.migrateCrewFields(actor);
    }
}
```

## User Notifications

```javascript
// Start notification
ui.notifications.info("My Module: Migrating data, please wait...");

// After migration completes
ui.notifications.info("My Module: Migration complete.");

// Error notification (if migration fails)
ui.notifications.error("My Module: Migration failed. See console for details.");
```

**When to notify:**
- Always show start notification (sets user expectation)
- Always show completion notification
- Show error notification if any migration fails
- Keep messages concise and actionable

## Console Logging

```javascript
// Per-actor migration success
console.log(`[MyModule] Migrated equipped items for ${actor.name}`);

// Overall migration start
console.log("[MyModule] Starting migration to schema v2");

// Debug information
console.log(`[MyModule] Found ${Object.keys(progressMap).length} progress entries`);
```

**Logging best practices:**
- Use module prefix: `[MyModule]`
- Include actor name for per-actor logs
- Use `console.log` for success (not `console.error`)
- Log meaningful progress (not every check, just actions taken)

## Common Migration Scenarios

### Scenario: Renaming a Flag

```javascript
static async renameFlag(actor) {
    const oldValue = actor.getFlag(MODULE_ID, "oldName");
    const newValue = actor.getFlag(MODULE_ID, "newName");

    if (oldValue && !newValue) {
        await actor.setFlag(MODULE_ID, "newName", oldValue);
        await actor.unsetFlag(MODULE_ID, "oldName");
        console.log(`[MyModule] Renamed flag for ${actor.name}`);
    }
}
```

### Scenario: Combining Multiple Flags

```javascript
static async combineFlags(actor) {
    const flag1 = actor.getFlag(MODULE_ID, "flag1");
    const flag2 = actor.getFlag(MODULE_ID, "flag2");
    const combined = actor.getFlag(MODULE_ID, "combined");

    if ((flag1 || flag2) && !combined) {
        const newValue = {
            part1: flag1 || {},
            part2: flag2 || {}
        };

        const updates = {};
        updates[`flags.${MODULE_ID}.combined`] = newValue;
        updates[`flags.${MODULE_ID}.-=flag1`] = null;
        updates[`flags.${MODULE_ID}.-=flag2`] = null;

        await actor.update(updates);
        console.log(`[MyModule] Combined flags for ${actor.name}`);
    }
}
```

### Scenario: Migrating Embedded Documents

```javascript
static async migrateItemData(actor) {
    const updates = [];

    for (const item of actor.items) {
        if (item.type === "ability") {
            const oldField = item.system.oldField;
            if (oldField) {
                updates.push({
                    _id: item.id,
                    "system.newField": oldField,
                    "system.-=oldField": null
                });
            }
        }
    }

    if (updates.length > 0) {
        await actor.updateEmbeddedDocuments("Item", updates);
        console.log(`[MyModule] Migrated ${updates.length} items for ${actor.name}`);
    }
}
```

## Error Handling

```javascript
static async migrate() {
    const currentVersion = game.settings.get(MODULE_ID, "schemaVersion") || 0;
    const targetVersion = 2;

    if (currentVersion < targetVersion) {
        ui.notifications.info("My Module: Migrating data, please wait...");

        try {
            for (const actor of game.actors) {
                if (actor.type !== "character") continue;

                // Wrap each migration in try-catch to prevent one failure from blocking others
                try {
                    await this.migrateEquippedItems(actor);
                    await this.migrateAbilityProgress(actor);
                } catch (err) {
                    console.error(`[MyModule] Migration failed for ${actor.name}:`, err);
                    ui.notifications.warn(`Migration failed for ${actor.name} - see console`);
                }
            }

            // Update version even if some actors failed
            await game.settings.set(MODULE_ID, "schemaVersion", targetVersion);
            ui.notifications.info("My Module: Migration complete.");

        } catch (err) {
            console.error("[MyModule] Critical migration error:", err);
            ui.notifications.error("My Module: Migration failed. See console for details.");
        }
    }
}
```

**Error handling strategies:**
- Wrap entire migration in try-catch
- Optionally wrap per-actor migrations to continue on individual failures
- Always log errors with context (actor name, migration step)
- Set schemaVersion even if some migrations fail (prevents infinite retry loop)

## Testing Migration with Console

### Create Test Data (Old Format)

```javascript
// In browser console
const actor = game.actors.getName("Test Character");

// Set old system field
await actor.update({ "system.old-field": "test value" });

// Set old array-based flag
await actor.setFlag("my-module", "equipped-items", [{ id: "abc123" }]);

// Verify old data
console.log(actor.system["old-field"]);  // "test value"
console.log(actor.getFlag("my-module", "equipped-items"));  // [{ id: "abc123" }]
```

### Trigger Migration Manually

```javascript
// Force schemaVersion back to 0
await game.settings.set("my-module", "schemaVersion", 0);

// Run migration
await Migration.migrate();

// Check results
const actor = game.actors.getName("Test Character");
console.log(actor.getFlag("my-module", "new_field"));  // "test value"
console.log(actor.system["old-field"]);  // undefined (removed)
```

## Quick Checklist

Before committing migration code:

- [ ] Incremented `targetVersion` in `migrate()` method
- [ ] Created migration method with descriptive name (`migrate{FeatureName}`)
- [ ] Checked both old and new data locations (handle both-exist case)
- [ ] Batched updates into single `actor.update()` call
- [ ] Used `-=` syntax to remove old fields
- [ ] Added console logging with module prefix and actor name
- [ ] Called migration method in `migrate()` sequence
- [ ] Added user notifications (start + complete)
- [ ] Tested migration with test world containing old data
- [ ] Verified migration runs ONCE (doesn't re-run on reload)
- [ ] Tested with multiple actors
- [ ] Documented migration in PR description

## References

- Migration implementation: `scripts/migration.js`
- Schema version registration: `scripts/settings.js`
- Migration trigger: `scripts/module.js` (ready hook)
- Testing guidelines: `CONTRIBUTING.md` line 56

For BitD Alternate Sheets module:
- Schema version registered in `scripts/settings.js` line 59
- Migration triggered in `scripts/module.js` line 43 (ready hook)
- Current target version: Check `scripts/migration.js` line 6
- Typical actor types: `character`, `crew`, `npc`
