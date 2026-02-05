---
name: fvtt-sockets
description: This skill should be used when implementing multiplayer synchronization, using game.socket.emit/on, creating executeAsGM patterns for privileged operations, broadcasting events between clients, or avoiding common pitfalls like race conditions and duplicate execution.
---

# Foundry VTT Sockets & Multiplayer

**Domain:** Foundry VTT Module/System Development
**Status:** Production-Ready
**Last Updated:** 2026-01-04

## Overview

Foundry VTT uses Socket.io for real-time communication between server and clients. Understanding socket patterns is essential for multiplayer-safe code.

### When to Use This Skill

- Broadcasting events to other connected clients
- Implementing GM-delegated operations for players
- Synchronizing non-document state across clients
- Creating animations/effects visible to all players
- Avoiding duplicate execution in hooks

## Socket Setup

### Manifest Configuration

Request socket access in your manifest:

```json
{
  "id": "my-module",
  "socket": true
}
```

### Event Naming

Each package gets ONE event namespace:
- **Modules:** `module.{module-id}`
- **Systems:** `system.{system-id}`

Multiplex event types with structured data:

```javascript
const SOCKET_NAME = "module.my-module";

game.socket.emit(SOCKET_NAME, {
  type: "playAnimation",
  payload: { tokenId: "abc123", effect: "fire" }
});
```

### Registration Timing

Register listeners after `game.socket` is available:

```javascript
Hooks.once("init", () => {
  game.socket.on("module.my-module", handleSocketMessage);
});

function handleSocketMessage(data) {
  switch (data.type) {
    case "playAnimation":
      playTokenAnimation(data.payload);
      break;
    case "syncState":
      updateLocalState(data.payload);
      break;
  }
}
```

## Basic Socket Patterns

### Emit to All Other Clients

```javascript
function broadcastAnimation(tokenId, effect) {
  game.socket.emit("module.my-module", {
    type: "playAnimation",
    tokenId,
    effect
  });
}
```

**Critical:** Emitting client does NOT receive its own broadcast.

### Self-Invoke Pattern

Always call handler locally when emitting:

```javascript
function triggerEffect(tokenId, effect) {
  const data = { type: "effect", tokenId, effect };

  // Execute locally
  handleEffect(data);

  // Broadcast to others
  game.socket.emit("module.my-module", data);
}

function handleEffect(data) {
  const token = canvas.tokens.get(data.tokenId);
  token?.animate({ alpha: 0.5 }, { duration: 500 });
}

// Socket listener (for other clients)
Hooks.once("init", () => {
  game.socket.on("module.my-module", (data) => {
    if (data.type === "effect") handleEffect(data);
  });
});
```

## ExecuteAsGM Pattern

Players often need GM-authorized operations (damage enemies, modify world data).

### Native Socket Approach

```javascript
const SOCKET_NAME = "module.my-module";

Hooks.once("init", () => {
  game.socket.on(SOCKET_NAME, async (data) => {
    // Only active GM handles this
    if (game.user !== game.users.activeGM) return;

    if (data.type === "damageActor") {
      const actor = game.actors.get(data.actorId);
      if (actor) {
        const newHp = actor.system.hp.value - data.damage;
        await actor.update({ "system.hp.value": Math.max(0, newHp) });
      }
    }
  });
});

// Player calls this
function requestDamage(actorId, damage) {
  game.socket.emit(SOCKET_NAME, {
    type: "damageActor",
    actorId,
    damage
  });
}
```

**Limitations:**
- No return value
- Manual GM check required
- Fails silently if no GM connected

### Socketlib Approach (Recommended)

Socketlib handles multiple GMs, return values, and error cases.

**Dependency (module.json):**
```json
{
  "relationships": {
    "requires": [{
      "id": "socketlib",
      "type": "module"
    }]
  }
}
```

**Registration:**
```javascript
let socket;

Hooks.once("socketlib.ready", () => {
  socket = socketlib.registerModule("my-module");

  // Register callable functions
  socket.register("damageActor", damageActor);
  socket.register("getActorData", getActorData);
});

async function damageActor(actorId, damage) {
  const actor = game.actors.get(actorId);
  if (!actor) return { success: false, error: "Actor not found" };

  const newHp = Math.max(0, actor.system.hp.value - damage);
  await actor.update({ "system.hp.value": newHp });
  return { success: true, newHp };
}

function getActorData(actorId) {
  return game.actors.get(actorId)?.toObject() ?? null;
}
```

**Usage:**
```javascript
// Execute on GM client, get return value
async function applyDamage(actorId, damage) {
  try {
    const result = await socket.executeAsGM("damageActor", actorId, damage);
    if (result.success) {
      ui.notifications.info(`Damage applied. HP now: ${result.newHp}`);
    }
  } catch (error) {
    ui.notifications.error("No GM connected to process damage");
  }
}
```

## Socketlib Methods

| Method | Target | Awaitable | Use Case |
|--------|--------|-----------|----------|
| `executeAsGM(fn, ...args)` | One GM | Yes | Privileged operations |
| `executeAsUser(fn, userId, ...args)` | Specific user | Yes | Player-specific actions |
| `executeForEveryone(fn, ...args)` | All clients | No | Broadcast effects |
| `executeForOthers(fn, ...args)` | All except self | No | Sync without local call |
| `executeForAllGMs(fn, ...args)` | All GMs | No | GM notifications |
| `executeForUsers(fn, ids[], ...args)` | Listed users | No | Targeted messages |

### ExecuteForEveryone Example

```javascript
// Trigger animation on ALL clients
function playGlobalEffect(effectData) {
  socket.executeForEveryone("renderEffect", effectData);
}

// Registered function
function renderEffect(data) {
  canvas.effects.playEffect(data);
}
```

### ExecuteAsUser Example

```javascript
// Ask specific player for input
async function promptPlayer(userId, question) {
  try {
    return await socket.executeAsUser("showDialog", userId, question);
  } catch {
    return null; // Player disconnected
  }
}

// Registered function
async function showDialog(question) {
  return new Promise(resolve => {
    new Dialog({
      title: question,
      buttons: {
        yes: { label: "Yes", callback: () => resolve(true) },
        no: { label: "No", callback: () => resolve(false) }
      }
    }).render(true);
  });
}
```

## Data Synchronization

### Document Updates (Automatic)

Foundry syncs document updates automatically:

```javascript
// Syncs to all clients
await actor.update({ "system.hp.value": 50 });

// Does NOT sync (in-memory only)
actor.system.hp.value = 50;
```

### Non-Document State

Use sockets for custom state:

```javascript
let combatState = {};

Hooks.once("socketlib.ready", () => {
  socket.register("syncCombatState", (state) => {
    combatState = state;
    Hooks.callAll("combatStateChanged", state);
  });
});

function updateCombatState(newState) {
  combatState = newState;
  socket.executeForEveryone("syncCombatState", newState);
}
```

### Ownership Considerations

Only owners can update documents:

```javascript
// Player cannot update enemy
await enemyActor.update({ ... }); // Permission denied!

// Must delegate to GM
await socket.executeAsGM("updateEnemy", enemyId, changes);
```

## Common Pitfalls

### 1. Emitter Doesn't Receive Broadcast

```javascript
// WRONG - emitter never sees this
game.socket.on("module.my-module", playSound);
game.socket.emit("module.my-module", { sound: "bell.wav" });
// Sound plays for others, NOT for emitter!

// CORRECT - call locally AND emit
playSound({ sound: "bell.wav" });
game.socket.emit("module.my-module", { sound: "bell.wav" });
```

### 2. Duplicate Execution in Hooks

```javascript
// WRONG - runs on ALL clients
Hooks.on("deleteItem", (item) => {
  item.parent.update({ "system.count": item.parent.items.length });
});

// CORRECT - only owner executes
Hooks.on("deleteItem", (item) => {
  if (!item.parent?.isOwner) return;
  item.parent.update({ "system.count": item.parent.items.length });
});
```

### 3. Race Conditions with Multiple GMs

```javascript
// RISKY - activeGM can change during async
game.socket.on(name, async (data) => {
  if (game.user !== game.users.activeGM) return;
  await actor.update({ ... }); // Another GM might be active now!
});

// SAFE - socketlib guarantees atomic execution
await socket.executeAsGM("updateActor", actorId, data);
```

### 4. No Permission Check on Handlers

```javascript
// VULNERABLE - any player can trigger
game.socket.on(name, (data) => {
  game.actors.get(data.id).update({ "system.hp": 9999 });
});

// SAFE - validate permissions
game.socket.on(name, (data) => {
  const actor = game.actors.get(data.id);
  if (!actor?.isOwner && !game.user.isGM) return;
  actor.update({ "system.hp": data.hp });
});
```

### 5. No GM Connected

```javascript
// WRONG - silent failure
socket.executeAsGM("doThing", data);

// CORRECT - handle error
try {
  await socket.executeAsGM("doThing", data);
} catch {
  ui.notifications.warn("A GM must be connected for this action");
}
```

### 6. Update Storms

```javascript
// WRONG - N clients = N updates
Hooks.on("updateActor", (actor, changes) => {
  actor.update({ "system.modified": Date.now() });
});

// CORRECT - only owner updates
Hooks.on("updateActor", (actor, changes) => {
  if (!actor.isOwner) return;
  if (changes.system?.modified) return; // Prevent loop
  actor.update({ "system.modified": Date.now() });
});
```

## Best Practices

### 1. Use Structured Events

```javascript
// Good - clear, maintainable
game.socket.emit(SOCKET_NAME, {
  type: "applyEffect",
  targetId: token.id,
  effectType: "fire",
  duration: 3000
});
```

### 2. Batch Updates

```javascript
// Bad - 3 updates
await actor.update({ "system.hp": 10 });
await actor.update({ "system.mp": 5 });
await actor.update({ "system.status": "hurt" });

// Good - 1 update
await actor.update({
  "system.hp": 10,
  "system.mp": 5,
  "system.status": "hurt"
});
```

### 3. Skip No-Op Updates

```javascript
const newHp = calculateHp(actor);
if (actor.system.hp.value === newHp) return;
await actor.update({ "system.hp.value": newHp });
```

### 4. Document Socket Messages

```javascript
/**
 * Socket: module.my-module
 *
 * @event applyDamage
 * @param {string} actorId - Target actor
 * @param {number} damage - Damage amount
 * @param {string} type - Damage type (fire, cold, etc.)
 */
```

### 5. Prefer Socketlib for Complex Operations

Native sockets for simple broadcasts. Socketlib when you need:
- Return values
- Multiple GM handling
- Permission-based execution
- Error handling

## Implementation Checklist

- [ ] Add `"socket": true` to manifest
- [ ] Use correct namespace (`module.X` or `system.X`)
- [ ] Register listeners in `init` hook
- [ ] Use structured event data with `type` field
- [ ] Call handler locally when emitting (self-invoke pattern)
- [ ] Check ownership in document operation hooks
- [ ] Use socketlib for GM-delegated operations
- [ ] Handle "no GM connected" errors
- [ ] Batch related updates
- [ ] Skip no-op updates
- [ ] Test with multiple connected clients

## References

- [Sockets Wiki](https://foundryvtt.wiki/en/development/api/sockets)
- [Game.socket API](https://foundryvtt.com/api/classes/foundry.Game.html)
- [Socketlib Package](https://foundryvtt.com/packages/socketlib)
- [Socketlib GitHub](https://github.com/manuelVo/foundryvtt-socketlib)

---

**Last Updated:** 2026-01-04
**Status:** Production-Ready
**Maintainer:** ImproperSubset
