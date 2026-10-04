---
name: hytale-modding
description: >-
  Hytale server-side plugin development standards using the ECS architecture,
  CommandBuffer, Interactions, Components, and Asset system. Use when writing or
  reviewing Hytale mod code, creating spells, registering components, building
  interactions, spawning entities/projectiles, playing sounds/particles, or working
  with the Hytale API (com.hypixel.hytale.*). Also triggers on: manifest.json,
  EntityStore, CommandBuffer, Ref, JavaPlugin, BuilderCodec, AssetRegistry,
  InteractionContext, KnockbackComponent, TransformComponent, SoundUtil, ParticleUtil.
---

# Hytale Server-Side Modding

## Architecture Overview

Hytale uses a **server-first ECS (Entity Component System)** architecture. All game logic runs server-side as Java plugins. Clients never run mod code.

```
JavaPlugin (entrypoint)
├── setup()              → register everything
├── Components           → ECS data attached to entities
├── Interactions         → player action handlers
├── Commands             → chat/console commands
├── Assets (JSON)        → data-driven configs (spells, items)
└── Systems              → tick-based logic (optional)
```

## Plugin Lifecycle

### Entry Point: `JavaPlugin`

```java
public class MyPlugin extends JavaPlugin {
    public MyPlugin(JavaPluginInit init) {
        super(init);
        // Constructor: only store instance, log version
    }

    @Override
    protected void setup() {
        // Register everything HERE, in this order:
        // 1. Asset modules (spells, configs)
        // 2. Commands
        // 3. Components
        // 4. Systems
        // 5. Interactions
    }
}
```

**Rules:**
- ONE singleton instance pattern per plugin (`static instance` + `getInstance()`)
- `setup()` is the ONLY place to register assets, components, commands, interactions
- Use `HytaleLogger.forEnclosingClass()` — never `System.out.println()` in production

---

## Entity Component System (ECS)

### Core Concepts

| Concept | Class | Role |
|---------|-------|------|
| Entity reference | `Ref<EntityStore>` | Pointer to an entity (player, NPC, projectile) |
| Component | Custom class + `ComponentType` | Data attached to an entity |
| Command buffer | `CommandBuffer<EntityStore>` | Safe queue for state mutations |
| System | Registered via `EntityStoreRegistry` | Tick-based logic processor |

### CommandBuffer — The Golden Rule

**ALL entity state changes go through `CommandBuffer<EntityStore>`.**

```java
// ✅ CORRECT: read/write via CommandBuffer
TransformComponent transform = cmd.getComponent(ref, TransformComponent.getComponentType());
cmd.putComponent(ref, KnockbackComponent.getComponentType(), knockback);

// ❌ WRONG: direct entity mutation outside CommandBuffer
entity.setPosition(x, y, z);  // NEVER DO THIS
```

### Reading Components

```java
// Get component (may return null)
TransformComponent transform = cmd.getComponent(ref, TransformComponent.getComponentType());

// Get or create component (never null)
PlayerSpellData data = cmd.ensureAndGetComponent(ref, componentType);
```

### Registering Custom Components

```java
// In plugin setup()
ComponentType<EntityStore, MyComponent> myType = 
    getEntityStoreRegistry().registerComponent(
        MyComponent.class,
        "namespace:component_id",    // unique ID
        MyComponent.CODEC            // serialization codec
    );
```

**Component naming**: `"modid:component_name"` (e.g., `"wt:player_spell_data"`)

---

## Interactions

Interactions are the bridge between player input and server logic.

### SimpleInstantInteraction Pattern

```java
public class MyInteraction extends SimpleInstantInteraction {

    public static final BuilderCodec<MyInteraction> CODEC = BuilderCodec.builder(
        MyInteraction.class,
        MyInteraction::new,
        SimpleInstantInteraction.CODEC
    ).documentation("Description").build();

    @Override
    protected void firstRun(
        @Nonnull InteractionType type,
        @Nonnull InteractionContext context,
        @Nonnull CooldownHandler cooldownHandler
    ) {
        CommandBuffer<EntityStore> cmd = context.getCommandBuffer();
        Ref<EntityStore> ref = context.getEntity();           // the item/block entity
        Ref<EntityStore> owner = context.getOwningEntity();   // the player
        Ref<EntityStore> target = context.getTargetEntity();  // hit target (nullable)
        
        // ... logic here ...
        
        context.getState().state = InteractionState.Finished; // mark done
    }
}
```

### Registration

```java
// In plugin setup()
getCodecRegistry(Interaction.CODEC)
    .register("Unique_Interaction_Id", MyInteraction.class, MyInteraction.CODEC);
```

**The interaction ID must match the one referenced in your item/block JSON assets.**

### Interaction Context Cheat Sheet

| Method | Returns | Notes |
|--------|---------|-------|
| `getCommandBuffer()` | `CommandBuffer<EntityStore>` | Can be null — always check |
| `getEntity()` | `Ref<EntityStore>` | The entity triggering the interaction |
| `getOwningEntity()` | `Ref<EntityStore>` | The player holding/using the item |
| `getTargetEntity()` | `Ref<EntityStore>` | Entity being targeted (nullable) |
| `getState()` | `InteractionStateHolder` | Set `.state = InteractionState.Finished` when done |

---

## Asset System (Data-Driven Configs)

### How It Works

1. Define a Java class with a `BuilderCodec` for deserialization
2. Create JSON files in `src/main/resources/Server/<AssetFolder>/`
3. Register an `HytaleAssetStore` in `setup()` that loads them

### Creating a New Asset Type

```java
// 1. Abstract base class
public abstract class Spell implements JsonAssetWithMap<String, DefaultAssetMap<String, Spell>> {
    
    public static final AssetCodecMapCodec<String, Spell> CODEC = new AssetCodecMapCodec<>(
        Codec.STRING,
        (spell, key) -> spell.id = key,
        spell -> spell.id,
        (spell, data) -> spell.data = data,
        spell -> spell.data
    );
    
    // Use BuilderCodec for fields
    public static final BuilderCodec<Spell> ABSTRACT_CODEC = BuilderCodec.abstractBuilder(Spell.class)
        .appendInherited(new KeyedCodec<>("JsonKey", Codec.TYPE), setter, getter, parentCopier)
        .add()
        .build();
}

// 2. Concrete subclass
public class MovementSpell extends Spell {
    public static final BuilderCodec<MovementSpell> CODEC = BuilderCodec.builder(
        MovementSpell.class, MovementSpell::new, Spell.ABSTRACT_CODEC
    )
    .appendInherited(new KeyedCodec<>("HeightJump", Codec.FLOAT), ...)
    .add()
    .build();
}
```

### Register Asset Store

```java
HytaleAssetStore<String, Spell, DefaultAssetMap<String, Spell>> store = 
    HytaleAssetStore.builder(Spell.class, new DefaultAssetMap<>())
        .setPath("Spells")                    // → Server/Spells/*.json
        .setCodec(Spell.CODEC)
        .setKeyFunction(Spell::getId)
        .loadsAfter(Item.class, BlockType.class)  // dependency ordering
        .build();

AssetRegistry.register(store);
```

### Register Subtypes (Polymorphic Dispatch)

```java
// In static initializer of the base class
static {
    CODEC.register("Movement", MovementSpell.class, MovementSpell.CODEC);
    CODEC.register("Projectile", ProjectileSpell.class, ProjectileSpell.CODEC);
}
```

**The `"Movement"` string must match the `"Type"` field in the JSON file.**

### JSON Config Example

```json
{
  "Type": "Movement",
  "Name": "Ascendio",
  "HeightJump": 10,
  "SpellDuration": 1.0,
  "Speed": 15.0,
  "activationSoundEventId": "SFX_Staff_Fire_Shoot",
  "Cooldown": 5.0,
  "ManaCost": 30.0
}
```

**Rules for JSON configs:**
- File name = asset ID (e.g., `Ascendio.json` → spell ID `"Ascendio"`)
- `"Type"` field drives polymorphic deserialization
- Sound event IDs must reference existing game sound events
- Place in `src/main/resources/Server/<AssetPath>/`

---

## Sound & Particles

### Playing Sounds

```java
// Resolve sound index (do this ONCE, e.g., in processConfig())
int soundIdx = SoundEvent.getAssetMap().getIndex("SFX_Staff_Fire_Shoot");

// Play at position
TransformComponent transform = cmd.getComponent(ref, TransformComponent.getComponentType());
if (transform != null) {
    Vector3d pos = transform.getPosition();
    SoundUtil.playSoundEvent3d(
        soundIdx,
        SoundCategory.SFX,
        pos.x, pos.y, pos.z,
        1.0f,   // volume
        1.0f,   // pitch
        cmd
    );
}
```

### Spawning Particles

```java
TransformComponent transform = cmd.getComponent(ref, TransformComponent.getComponentType());
if (transform != null) {
    Vector3d spawnPos = new Vector3d(transform.getPosition());
    spawnPos.y += 0.5d;  // offset above entity
    ParticleUtil.spawnParticleEffect("ParticleEffectId", spawnPos, cmd);
}
```

**Always wrap sound/particle calls in try-catch — missing asset IDs can throw.**

---

## Movement & Physics

### Applying Velocity (Knockback Pattern)

```java
KnockbackComponent knockback = new KnockbackComponent();
knockback.setVelocity(velocity);                          // Vector3d
knockback.setVelocityType(ChangeVelocityType.Set);        // Set = replace, Add = additive
knockback.setVelocityConfig(new VelocityConfig());
knockback.setDuration(0.5f);                              // seconds

cmd.putComponent(ref, KnockbackComponent.getComponentType(), knockback);
```

### Direction Vectors (JOML)

```java
// Look direction from entity
Transform look = TargetUtil.getLook(ref, cmd);
Vector3d direction = new Vector3d(look.getDirection());

// Scale to speed
direction.mul(speed);  // .mul() = scalar multiply each component

// Pure vertical vector
Vector3d upward = new Vector3d(0, intensity, 0);
```

### Checking Movement State

```java
MovementStatesComponent mc = cmd.getComponent(ref, MovementStatesComponent.getComponentType());
if (mc != null) {
    MovementStates states = mc.getMovementStates();
    boolean isFlying  = states.flying;
    boolean isFalling = states.falling;
}
```

---

## Player Messaging

### Translation-Based Messages

```java
PlayerRef playerRef = cmd.getComponent(ref, PlayerRef.getComponentType());

// Simple message
Message msg = Message.translation("server.spells.noSpellSelected");

// With parameters
Message msg = Message.translation("server.spells.onCooldown").param("seconds", 3.5f);
```

Translation keys defined in `src/main/resources/Server/Languages/en-US/server.lang`.

---

## Commands

Register in `setup()`:

```java
getCommandRegistry().registerCommand(new MyCommand());
```

---

## Entity Stats (Mana/Stamina)

```java
EntityStatMap statMap = cmd.ensureAndGetComponent(ref, EntityStatsModule.get().getEntityStatMapComponentType());
int staminaIdx = DefaultEntityStatTypes.getStamina();

// Read
EntityStatValue current = statMap.get(staminaIdx);
float value = (current != null) ? current.get() : 0f;

// Write (must be inside world.execute for thread safety)
EntityStore store = cmd.getExternalData();
World world = store.getWorld();
world.execute(() -> {
    statMap.subtractStatValue(staminaIdx, cost);
});
```

---

## Common Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `System.out.println()` | `LOGGER.atInfo().log(...)` |
| Mutate entity state directly | Use `CommandBuffer` |
| Ignore null `CommandBuffer` | Always null-check `context.getCommandBuffer()` |
| Silent `catch (Exception e) {}` | Log the error: `LOGGER.atWarning().log(...)` |
| Hardcode sound event strings at call site | Resolve index once in `processConfig()` |
| Store `Ref<EntityStore>` long-term | Refs may become invalid between ticks |
| Skip `InteractionState.Finished` | Always mark interaction complete |
| Use `new Vector3d(0,1,0).mul(x)` | Use `new Vector3d(0, x, 0)` directly |
| Mutate stats outside `world.execute()` | Always defer stat changes to world thread |

---

## Project Structure

```
src/main/java/com/magistere/wizardingtales/
├── WizardingTales.java          # Plugin entrypoint (JavaPlugin)
├── Commands/                    # Chat commands
├── Components/                  # Custom ECS components
├── Effects/                     # Status effects, world services
├── Interactions/                # Player action handlers
├── Spells/                      # (future) spell-specific logic
├── asset/
│   ├── SpellModule.java         # Asset store registration
│   └── config/
│       ├── Spell.java           # Abstract base (polymorphic codec)
│       ├── SpellType.java       # Enum: PROJECTILE, MOVEMENT, etc.
│       ├── ProjectileSpell.java # Concrete spell type
│       └── MovementSpell.java   # Concrete spell type
├── casting/
│   ├── SpellCaster.java         # Executor dispatcher
│   ├── SpellCastContext.java    # Cast context DTO
│   ├── SpellCastResult.java     # Result wrapper
│   ├── executor/
│   │   ├── SpellExecutor.java   # Interface
│   │   ├── ProjectileExecutor.java
│   │   └── MovementExecutor.java
│   └── projectile/              # Projectile tracking
└── ui/                          # Custom UI pages

src/main/resources/
├── manifest.json                # Plugin manifest (templated)
├── Server/
│   ├── Spells/                  # Spell JSON configs
│   └── Languages/en-US/         # Translation strings
└── Common/                      # Shared client/server assets
```

## Adding a New Spell Type — Checklist

1. Create `NewTypeSpell extends Spell` with its `BuilderCodec`
2. Add enum value to `SpellType`
3. Register in `Spell` static block: `CODEC.register("NewType", ...)`
4. Create `NewTypeExecutor implements SpellExecutor`
5. Register executor in `SpellCaster.registerExecutors()`
6. Add JSON file in `Server/Spells/YourSpell.json`
7. Add translation keys in `server.lang`
8. Test with `/selectspell` and `/learnspell` commands

## Verification

```bash
./gradlew build        # compilation check
./gradlew runServer    # runtime test with game server
```
