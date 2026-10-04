---
name: unreal-gas
description: >
  Expert guide for Unreal Engine 5.x Gameplay Ability System (GAS) C++ development.
  Covers AbilitySystemComponent, GameplayAbilities, GameplayEffects, Attributes/AttributeSets,
  GameplayTags, GameplayCues, AbilityTasks, prediction/replication, and common patterns.
  Use when the user asks about GAS, gameplay abilities, gameplay effects, attribute sets,
  ability system component, gameplay tags in the context of GAS, gameplay cues,
  ability tasks, or any UAbilitySystemComponent / UGameplayAbility / UGameplayEffect /
  UAttributeSet related C++ code. Also triggers for questions about ability prediction,
  ability replication, combo systems using GAS, cooldowns, costs, stacking, or
  damage/healing pipelines built on GAS.
---

# Unreal Engine Gameplay Ability System (GAS) -- C++ Guide

## Official Documentation (always consult for latest details)

These are the authoritative sources. Reference them for up-to-date API details, as GAS evolves across engine versions:

| Source | URL |
|--------|-----|
| **Epic GAS Landing Page** | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine |
| **Understanding GAS (Overview)** | https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-unreal-engine-gameplay-ability-system |
| **ASC & Attributes** | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-component-and-gameplay-attributes-in-unreal-engine |
| **Gameplay Abilities** | https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-abilities-in-unreal-engine |
| **Attributes & Attribute Sets** | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-attributes-and-attribute-sets-for-the-gameplay-ability-system-in-unreal-engine |
| **Gameplay Effects** | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine |
| **Ability Tasks** | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-tasks-in-unreal-engine |
| **Community GAS Docs (tranek)** | https://github.com/tranek/GASDocumentation |

The community docs by tranek are the most comprehensive single resource for GAS. They cover advanced topics (prediction internals, optimization, replication modes, pitfalls) that Epic's official docs do not. Always check them for edge cases and production patterns.

The **Lyra Sample Project** is Epic's recommended working reference implementation for GAS.

## Plugin Setup

1. Enable **Gameplay Abilities** plugin in the editor
2. Add to `Build.cs`:
   ```cpp
   PublicDependencyModuleNames.AddRange(new string[] {
       "GameplayAbilities", "GameplayTags", "GameplayTasks"
   });
   ```
3. UE 5.2 and earlier: call `UAbilitySystemGlobals::Get().InitGlobalData()` in your AssetManager or GameInstance. UE 5.3+ does this automatically.

## Core Architecture

See [references/core-classes.md](references/core-classes.md) for the full class reference, setup patterns, and C++ code snippets.

**System overview:**
```
Actor
  +-- UAbilitySystemComponent (ASC) --- manages everything below
        +-- UGameplayAbility instances (granted abilities)
        |     +-- UAbilityTask instances (async execution)
        +-- UAttributeSet instances (numeric data)
        +-- Active UGameplayEffect specs (modifiers)
        +-- FGameplayTag container (status/state)
        +-- GameplayCue triggers (cosmetic FX)
```

**Key relationships:**
- ASC is the central hub; one per Actor (place on Pawn or PlayerState)
- Abilities create/apply Effects to modify Attributes and Tags on targets
- Effects auto-trigger Cues when their tags match `GameplayCue.*` tags
- Tags control ability activation, blocking, and cancellation systemically
- AbilityTasks handle async work (montages, delays, targeting) within abilities

## Gameplay Effects Quick Reference

See [references/effects-and-attributes.md](references/effects-and-attributes.md) for detailed GE patterns, modifier math, stacking, cooldowns, and attribute handling.

**Duration types:**
- **Instant** -- modifies BaseValue permanently, never tracked as active
- **Duration** -- modifies CurrentValue, auto-reverts on expiry
- **Infinite** -- persists until explicitly removed

**Modifier aggregation:** `((Base + Additive) * Multiplicative) / Division`
- Multiply/Divide uses `1 + Sum(Mods - 1)` -- two +50% multipliers = +100%, not +125%

## Ability Lifecycle

```
GiveAbility() -> TryActivateAbility() -> CanActivateAbility()
  -> ActivateAbility() [override this] -> CommitAbility() [apply cost/cooldown]
  -> ... do work (AbilityTasks) ... -> EndAbility()
```

**Four activation methods:** explicit handle, GameplayEvent, GameplayEffect tags, Input codes.

**Instancing policies:**
- `InstancedPerActor` -- recommended default; one instance reused per actor
- `InstancedPerExecution` -- new instance each activation; simplest but heaviest
- `NonInstanced` -- uses CDO; best performance, C++ only, no state/delegates/RPCs

## Networking & Prediction

See [references/networking.md](references/networking.md) for replication modes, prediction details, and multiplayer patterns.

**Net Execution Policies:** LocalPredicted, LocalOnly, ServerOnly, ServerInitiated.

**Key rules:**
- ASC replicates Attributes and Tags to all clients, but NOT abilities/effects (bandwidth optimization)
- Non-instant GEs support prediction rollback; instant GEs (damage) do NOT
- Cues use unreliable replication -- cosmetic only, never gameplay logic
- ASC's owning Actor must be locally controlled for remote activation to work
- For PlayerState-based ASC: use Mixed replication for players, Minimal for AI

## Common Patterns & Pitfalls

See [references/patterns-and-pitfalls.md](references/patterns-and-pitfalls.md) for implementation recipes and known issues.

**Critical pitfalls:**
- `PreAttributeChange` clamping does NOT permanently change modifiers -- clamp BaseValue in `PostGameplayEffectExecute` instead
- `Server Respects Remote Ability Cancellation` causes more trouble than it's worth -- disable it
- `Replication Policy` on GameplayAbility is misleadingly named -- do not use it
- PlayerState `NetUpdateFrequency` defaults too low -- increase it or enable Adaptive Network Update Frequency
- Removing AttributeSets at runtime can crash clients
- Animation montages must use `PlayMontageAndWait` AbilityTask, not direct `PlayMontage`, for replication
