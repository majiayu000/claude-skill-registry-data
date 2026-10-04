---
name: thalarch-android
description: >
  Coordinates Android/Kotlin/Jetpack Compose/Gradle/Media3 work. Use for Android UI, playback,
  services, device behavior, build/toolchain, R8, Room/data access, testing, edge-to-edge, adaptive
  layout, localization, performance, or runtime debugging. Prefer official Google Android skills/CLI
  when installed and use device or emulator evidence for runtime-specific acceptance.
---

# Thalarch Android

## Android lens

Prefer official current Android skills/tooling available in the environment for version-sensitive
platform facts. Thalarch supplies scope control, regression safety, causal reasoning, routing, and
proof discipline around them.

## Preflight

Inspect:

- module graph;
- Gradle/AGP/Kotlin/version catalog;
- manifests;
- Compose/navigation/state patterns;
- Media3/session/service/player ownership when playback is involved;
- Room/repository/data-source boundaries when persistence is involved;
- locale/resource structure when user-facing text changes;
- CI build tasks;
- device/runtime requirements.

Do not upgrade toolchain or libraries unless the task requires it.

## Specialist routing

Use the smallest relevant stack rather than loading every Android skill.

- Media3, ExoPlayer, `MediaSession`, `MediaLibrarySession`, Android Auto, queue/timeline, audio/video
  track selection, cache/preload/recovery, or audio-processing pipeline → `thalarch-media3`;
- Compose redesign/product UI/settings/media surfaces → `thalarch-compose-ui`, plus
  `thalarch-design-system` when visual direction needs extraction or re-articulation;
- fuzzy title/artist/catalog/provider identity resolution → `thalarch-entity-matching`;
- user-facing strings, locale resources, RTL, placeholder parity, translation completeness →
  `thalarch-localization`;
- a working subsystem where a narrow change could break adjacent behavior → `thalarch-no-regression`;
- measured/suspected CPU, allocation, memory, cache, build, or hot-path cost → `thalarch-performance`;
- Room/SQL query-shape and persistence work → `thalarch-data-sql` as needed;
- version-sensitive deprecations/API migrations → `thalarch-source-grounding` plus the Android
  deprecation playbook below.

## No-Regression Contract

For playback, cache, persistence, sync, migration, concurrency, or other high-blast-radius surfaces,
use `thalarch-no-regression` before mutation.

Capture the local must-preserve behaviors, the suspected problem, evidence state, intended action
(`AUDIT ONLY` vs targeted mutation), and the verification needed.

A similar fix in another application is evidence to investigate, not evidence that this repository
has the same defect.

## Compose

Check:

- state ownership/stability;
- effects/lifecycle;
- recomposition-sensitive work;
- lazy keys;
- edge-to-edge/insets;
- adaptive behavior;
- touch targets/semantics;
- theme consistency;
- localization/truncation;
- RTL/AutoMirrored directional icons;
- font scaling;
- rendered behavior on the actual supported device classes.

For substantial Compose work, use `thalarch-compose-ui` rather than treating source review as visual
proof.

## Media/runtime

For Media3/playback/services inspect:

- lifecycle/session ownership;
- cancellation;
- buffering/retry;
- cache;
- queue/timeline invariants;
- audio focus;
- service process/state;
- resolver/network fallback ordering;
- audio-only vs video-capable selection;
- preload/recovery loops;
- DSP/audio-processor ordering when relevant.

Route substantial Media3 work to `thalarch-media3`.

Do not cure state bugs with arbitrary delays without evidence.

## Performance and cache

When the task touches memory, cache, hot paths, playback churn, jank, or repeated work, read:

- `references/android-performance.md`

Audit for concrete work such as repeated regex compilation, collection scans, Room N+1 queries,
full-cache enumeration, polling loops, listener/job leaks, oversized artwork, recomposition-heavy
work, native/media allocation churn, or unnecessary video decoding during audio-only playback.

For a cache that currently works, combine `thalarch-performance` with `thalarch-no-regression` and
presume its current semantics must be preserved until a defect/inefficiency is demonstrated.

## Room and pagination

When a caller exposes paging (`page` / `pageSize`) and the backing collection can be large, trace the
paging contract all the way to the data source. Read:

- `references/room-pagination.md`

Do not claim real pagination when the implementation loads the full dataset and truncates it after
the fact. Preserve ordering, identity, filtering, and browsing semantics; test empty, partial,
>1000-row, duplicate/ordering, and adjacent-page boundaries where relevant.

## Deprecation migration

For compiler deprecations or override-signature warnings, read:

- `references/deprecation-migration.md`

Ground the exact installed dependency version, prove the official replacement, migrate minimally,
and preserve runtime semantics. Do not use suppression as a substitute for a valid supported
migration.

## Localization

When new or changed user-facing text is introduced, use `thalarch-localization` to verify locale
inventory, key and placeholder parity, natural domain terminology, layout expansion, and RTL.

A default-locale build does not prove translation completeness or unclipped UI.

## Proof hierarchy

Compilation proves compilation only.

For runtime/UI behavior use, where available:

- targeted unit/integration tests;
- instrumentation;
- emulator/device interaction;
- Android Auto/head-unit/controller interaction when relevant;
- `adb`/log evidence;
- screenshots/recordings for visual claims;
- profiling/trace evidence for performance claims.

Keep unavailable runtime/device evidence explicitly `UNVERIFIED` rather than upgrading a source-only
inference into PASS.
