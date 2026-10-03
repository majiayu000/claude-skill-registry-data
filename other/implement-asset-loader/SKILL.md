---
name: implement-asset-loader
description: "Use when generating a type-safe asset loading/streaming system with reference counting, platform-aware load strategies, and ECS asset component integration."
---

## 1. Core Pattern

1. **Platform & Language Detection**: Scan project config for target platform/language; resolve hardware constraints.
2. **Type & Strategy Generation**: Generate `AssetType` enums, `LoadStrategy` enums (AOT/On-Demand/DLC), `AssetBundle`, `AssetRef`.
3. **Reference Counting**: Implement `Acquire`/`Release` mechanics, main loading function (all strategies), error handling for missing/invalid assets.
4. **Asset Pool**: Generate `AssetPool` for high-frequency assets to reduce GC pressure; implement progress callback interfaces.
5. **ECS Asset Components (MANDATORY)**: Generate components referencing loaded assets by string ID (not direct object refs):
   - `SpriteComponent` — sprite/texture by ID, UV coords, scale, flip flags
   - `AnimationComponent` — animation asset (sprite sequence), current frame, speed, loop flag
   - `AudioComponent` — audio asset by ID, volume, play state, loop flag
   - Place in same location as other ECS components (e.g., `src/core/ecs/components.ts`)
6. **Renderer Integration (MANDATORY)**: Replace color-based rendering with sprite/texture drawing from `SpriteComponent` data; fallback to colored rectangle when asset unavailable; TODO comments if no asset system exists.
7. **Export**: Write implementation to language-appropriate files (`.ts`/`.rs`/`.cs`).

## 2. Interaction Protocol

* Platform unclear → ask, default to most constrained target.
* Strategy contradicts platform (e.g., massive AOT on mobile) → warn, suggest On-Demand/DLC.

## 3. Red Flags

Monolithic loader causing frame drops · Missing `Acquire`/`Release` cleanup · Desktop-centric AOT bundles on mobile

## 4. Integrity Audit

* [ ] `Acquire`/`Release` for all asset types
* [ ] Error handling for missing/invalid assets (no crash)
* [ ] Platform-specific strategies applied
* [ ] ECS components generated (`SpriteComponent`/`AnimationComponent`/`AudioComponent`)
* [ ] Renderer uses loaded assets (not just placeholder colors)
* [ ] Components store string IDs, not object references
* [ ] `AssetPool` implemented for high-frequency assets to reduce GC pressure
* [ ] Progress callback interfaces available for async load operations

## 5. Execution Command

Command: `/implement-asset-loader`
