---
name: unreal-best-practices
description: >
  Comprehensive best practices guide for modern Unreal Engine 5.x development.
  Covers Epic's strategic direction toward modern systems (GAS, Enhanced Input, StateTree,
  MetaSounds, Niagara, PCG, CommonUI, World Partition, Game Feature Plugins, Gameplay Tags),
  the "research first" philosophy of always checking for newer UE systems before implementing,
  C++ vs Blueprint decision making, data-driven design, asset management, project organization,
  naming conventions, performance optimization, and debugging with Unreal Insights.
  Use when the user asks about UE best practices, modern UE5 workflows, which system to use,
  old vs new UE systems, recommended approaches, project setup, code organization, performance
  tips, Blueprint vs C++ decisions, naming conventions, or when starting a new feature and
  needing guidance on the right UE system to use. Also triggers when the user asks whether
  there is a newer/better way to do something in Unreal Engine, or when comparing legacy
  systems against modern replacements. Covers deprecated systems and their migration paths.
---

# Unreal Engine 5.x Best Practices Guide

## The "Research First" Principle

**Before implementing any gameplay system, always investigate whether Epic provides a newer, purpose-built system for it.** Epic Games continuously introduces modern frameworks that replace ad-hoc solutions. Using the latest recommended system yields better performance, easier networking, designer-friendly workflows, and future compatibility.

**Workflow:**
1. Identify the problem domain (input, abilities, audio, particles, AI, UI, movement, etc.)
2. Check the [Modern Systems Quick Reference](#modern-systems-quick-reference) below
3. If uncertain, search Epic's documentation and the UE Public Roadmap for the latest system status
4. Prefer production-ready modern systems over legacy approaches
5. For experimental systems: evaluate maturity before committing -- use them in prototypes, not shipping builds

**Why this matters:** Epic signals their direction through actions, not just announcements. When they rebuild the First/Third Person templates to use GAS and Enhanced Input, or when Fortnite ships with Game Feature Plugins and CommonUI, that is the clearest indicator of where the ecosystem is heading.

## Official Documentation (always consult for latest details)

| Source | URL |
|--------|-----|
| **Epic Documentation Hub** | https://dev.epicgames.com/documentation/en-us/unreal-engine |
| **UE Public Roadmap** | https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap |
| **Lyra Sample Project** | https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine |
| **UE Release Notes** | https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-release-notes |
| **Epic Community Tutorials** | https://dev.epicgames.com/community/learning |
| **Experimental Features List** | https://dev.epicgames.com/documentation/en-us/unreal-engine/experimental-features |
| **Allar's UE5 Style Guide** | https://github.com/Allar/ue5-style-guide |
| **Tom Looman's UE5 Guides** | https://tomlooman.com |
| **X157 Dev Notes (Lyra)** | https://x157.github.io/UE5/ |

The **Lyra Starter Game** is Epic's canonical reference implementation for modern UE5 architecture. It demonstrates GAS, Enhanced Input, Game Feature Plugins, CommonUI, GameplayMessageSubsystem, Gameplay Tags, and modular gameplay patterns -- all derived from Fortnite's production codebase.

## Modern Systems Quick Reference

See [references/modern-systems.md](references/modern-systems.md) for detailed information on each system, migration paths, and documentation links.

**System status as of UE 5.7:**

| Domain | Legacy/Old System | Modern System | Status |
|--------|-------------------|---------------|--------|
| **Input** | BindAction/BindAxis | **Enhanced Input** | Production -- legacy deprecated since 5.1 |
| **Abilities** | Ad-hoc booleans/timers | **Gameplay Ability System (GAS)** | Production -- recommended for ability-driven games |
| **State/Classification** | Enums, booleans, strings | **Gameplay Tags** | Production -- foundation of modern UE |
| **AI Behavior** | Behavior Trees | **StateTree** | Production since 5.1 -- alternative, BTs still supported |
| **AI Interaction** | Manual scripting | **Smart Objects** | Production since 5.1 |
| **Particles/VFX** | Cascade | **Niagara** | Production -- Cascade deprecated since 5.0 |
| **Audio** | SoundCue | **MetaSounds** | Production (core) -- SoundCue not yet deprecated |
| **Audio Mixing** | Static config | **Audio Modulation** | Production |
| **Rendering (Geometry)** | Manual LODs | **Nanite** | Production since 5.0 |
| **Rendering (Lighting)** | Baked lightmaps | **Lumen** | Production since 5.0 |
| **Level Streaming** | World Composition / Level Streaming | **World Partition** | Production -- World Composition deprecated |
| **UI (Multiplatform)** | Raw UMG | **CommonUI + UMG** | Beta (used in Fortnite) |
| **Movement** | CharacterMovementComponent | **Mover 2.0** | Experimental -- CMC still recommended |
| **Procedural Content** | Manual/Blueprint scripting | **PCG Framework** | Production since 5.7 |
| **Architecture** | Monolithic modules | **Game Feature Plugins** | Production (Lyra/Fortnite) |
| **Messaging** | Direct delegates/casting | **GameplayMessageSubsystem** | Production (Lyra) |
| **Animation (Locomotion)** | State machines/blend trees | **Motion Matching (PoseSearch)** | Experimental |
| **Animation (Interaction)** | Manual montage sync | **Motion Warping** | Production-usable |
| **Animation (Rigging)** | External DCC only | **Control Rig** | Production (core) |
| **Asset Selection** | Hardcoded switch/if chains | **Chooser Tables** | Beta since 5.4 |
| **Networking (Large-scale)** | Default replication | **Iris** | Beta since 5.7 |
| **Dialogue** | Third-party plugins | **CommonConversation** | Experimental (not recommended) |

## C++ and Blueprint Best Practices

See [references/blueprint-and-cpp.md](references/blueprint-and-cpp.md) for detailed patterns, communication methods, and performance guidelines.

**The gold standard pattern: Abstract C++ base + Blueprint subclass.**

```
C++ (UCLASS(Abstract))                  Blueprint Subclass
+----------------------------------+    +---------------------------+
| Base class logic                 |    | Visual/gameplay config    |
| - Core systems & algorithms     |    | - Asset references        |
| - Networking & replication       |    | - Tuning values           |
| - Performance-critical code      |    | - Event responses         |
| - BlueprintImplementableEvent    |    | - Designer iteration      |
| - UPROPERTY(EditDefaultsOnly)   |    | - One-off behaviors       |
+----------------------------------+    +---------------------------+
```

**Decision matrix:**
- **C++**: Base classes, systems, performance-critical code, networking, editor tools
- **Blueprint**: Gameplay logic, configuration, prototyping, VFX triggers, UI layout
- **Both**: C++ defines the framework, Blueprint fills in the gameplay details

**Critical rules:**
- Avoid Event Tick -- use timers, events, and delegates instead (20-30% perf improvement)
- Use Blueprint Interfaces over casting for cross-Blueprint communication (avoids hard references)
- Use `TSoftObjectPtr<>` for assets not immediately needed (prevents memory bloat)
- Cache references instead of searching every frame
- Blueprint Nativization was removed in UE 5.0 -- manually convert hot paths to C++

## Data-Driven Design

See [references/data-driven-design.md](references/data-driven-design.md) for Data Tables, Data Assets, Primary Assets, Asset Manager, and Gameplay Tag patterns.

**Core principle: Separate data from logic.** Let designers configure without touching code.

| Asset Type | Best For | Key Trait |
|------------|----------|-----------|
| **Data Table** | Large homogeneous datasets (100+ items) | CSV/JSON import, FTableRowBase rows |
| **Data Asset** | Unique complex definitions (bosses, skill trees) | Full inheritance, UObject members |
| **Primary Data Asset** | Assets with lifecycle management | Asset Manager integration, async loading |
| **Gameplay Tags** | Hierarchical state/classification | Replaces enums, designer-creatable |

**Gameplay Tags are fundamental** -- use them for state management, ability classification, damage types, animation states, input binding, and cross-system communication. Always use `FGameplayTagContainer` over `TArray<FGameplayTag>`.

## Project Organization

See [references/project-organization.md](references/project-organization.md) for naming conventions, folder structure, and modular architecture patterns.

**Naming convention prefixes (standard):**

| Prefix | Type | Prefix | Type |
|--------|------|--------|------|
| `BP_` | Blueprint | `IA_` | Input Action |
| `WBP_` | Widget Blueprint | `IMC_` | Input Mapping Context |
| `DA_` | Data Asset | `GA_` | Gameplay Ability |
| `DT_` | Data Table | `GE_` | Gameplay Effect |
| `SM_` | Static Mesh | `NS_` | Niagara System |
| `SK_` | Skeletal Mesh | `AM_` | Animation Montage |
| `M_` | Material | `ABP_` | Animation Blueprint |
| `MI_` | Material Instance | `BS_` | Blend Space |
| `T_` | Texture | `S_` | Sound Wave |

**Folder structure: Feature-based, not asset-type-based.**

## Performance and Debugging

See [references/performance-and-debugging.md](references/performance-and-debugging.md) for tick optimization, object pooling, GC management, profiling, and Unreal Insights.

**Top performance rules:**
1. Disable tick on actors/components that don't need it (`bCanEverTick = false`)
2. Use timers and events instead of per-frame polling
3. Pool frequently spawned/destroyed actors (projectiles, particles)
4. Use Nanite for static geometry -- eliminates manual LOD creation
5. Profile with Unreal Insights (`-trace=cpu,gpu,frame,counters`), not guesswork
6. Use `COND_*` flags on replicated properties to minimize network bandwidth
7. Audit asset references with the Reference Viewer to prevent memory bloat

## Key Design Patterns from Lyra

Lyra establishes these patterns as Epic's recommended architecture:

1. **Game Feature Plugins**: Self-contained features that inject into the base game at runtime. One-way dependency -- core game never references features.
2. **Experience System**: Async-loading game mode configurations built on Game Feature Plugins. Superior to traditional GameMode subclassing.
3. **GameplayMessageSubsystem**: Tag-based publish-subscribe messaging. Eliminates tight coupling between gameplay systems.
4. **GAS + Gameplay Tags**: Abilities defined via data, activated via tags, with tag-based blocking/cancellation.
5. **Enhanced Input + Tag Binding**: Input Actions mapped to Gameplay Abilities via Gameplay Tags (not direct function calls).
6. **CommonUI**: Platform-aware UI with automatic input device switching and focus management.
7. **Primary Data Assets + Asset Manager**: Controlled async loading with bundle-based memory management.

## Version-Specific Breaking Changes

**Key changes affecting development practices:**
- **UE 5.0**: `FVector` → 3 doubles; `TObjectPtr<>` replaces raw pointers in UPROPERTY
- **UE 5.1**: Enhanced Input becomes default; legacy input deprecated
- **UE 5.3**: C++20 default for new projects; `BuildSettingsVersion.V5`
- **UE 5.5**: Legacy stat profiler deprecated → use Unreal Insights; Zen Loader production-ready; Path Tracer production-ready
- **UE 5.6**: Swarm Manager removed; `FString::Appendf` enforces `static constexpr` format strings; HWRT performance improved
- **UE 5.7**: PCG Framework production-ready; Substrate production-ready; `FindObject` uses `EFindObjectFlags`; `BuildSettingsVersion.V6`
