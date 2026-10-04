---
name: thalarch-media3
description: >
  Specialist reliability workflow for AndroidX Media3 playback, MediaSession/MediaLibrarySession,
  MediaLibraryService, Android Auto browsing, queue/timeline identity, caching, preload/recovery,
  audio/video track selection, and audio-processing pipelines. Use when Media3 behavior, APIs,
  deprecations, playback lifecycle, controller contracts, or automotive media browsing are material.
---

# Thalarch Media3

Media3 work is state-machine and lifecycle work. A local symptom is not permission to redesign the
playback architecture.

## 1. Ground the real Media3 contract

Before changing version-sensitive code:

- inspect the project's actual Media3 artifacts and versions;
- inspect the concrete session/service/player classes in use;
- identify current controller/session commands and compatibility requirements;
- use current official AndroidX Media3 documentation for exact signatures or deprecation replacements;
- route uncertain API facts through `thalarch-source-grounding`.

A remembered Media3 signature is a hypothesis until it matches the project's version.

## 2. Build an ownership map before mutation

Trace who owns and mutates:

- Player / ExoPlayer;
- `MediaSession` / `MediaLibrarySession`;
- `MediaSessionService` / `MediaLibraryService`;
- queue/timeline state;
- playback intent;
- media identity and metadata;
- cache and preload state;
- audio/video track selection;
- audio processors and output routing;
- lifecycle/cancellation/recovery jobs.

Never change playback architecture to fix a local bug until the existing ownership, lifecycle,
timeline, and Media3 contract have been traced.

## 3. Session and controller invariants

When changing connection callbacks or command exposure, preserve deliberately:

- accepted/rejected controller policy;
- player commands;
- session/custom commands;
- connection hints/extras when used;
- notification/controller behavior;
- Android Auto and external controller compatibility.

For deprecated APIs, use the supported replacement for the exact installed version. Do not hide a
migration behind deprecation suppression when a compatible modern API exists.

## 4. Queue, timeline, and identity

Treat queue identity as a contract, not a display detail.

Check:

- stable media IDs across refresh/rebinding;
- duplicate tracks and repeated queue entries;
- current-item preservation across recovery;
- next/previous semantics;
- shuffle/repeat interaction;
- metadata refresh without accidental identity replacement;
- stale progress/duration state when the media ID changes.

A metadata-equivalent item is not automatically the same queue entry.

## 5. Playback intent and transitional state

Distinguish user intent from transient player state.

Examples:

- `playWhenReady` can represent intent while buffering makes `isPlaying == false`;
- a reconnect/resync event can carry stale position;
- a track change can require resetting UI position before new timeline values arrive.

Do not infer pause intent from buffering or other transient states without tracing the actual contract.

## 6. Audio-only, video, and track selection

Verify the requested mode explicitly.

For audio-only playback, inspect whether an unnecessary video track/decoder remains selected and
whether changing selection preserves fallback behavior. For video mode, do not degrade video
capability as a side effect of an audio optimization.

Test transitions between audio-only and video-capable paths when the application supports both.

## 7. Cache, preload, and recovery

Before changing cache behavior, combine with `thalarch-no-regression` and `thalarch-performance`.

Audit first for evidence of:

- periodic full-cache enumeration;
- repeated key scans;
- unnecessary database/cache reconciliation loops;
- duplicated preload work;
- unbounded recovery loops;
- stale cache identity;
- cancellation leaks.

If the suspected inefficiency is not demonstrated, preserve the working cache and report the audit
result instead of performing a speculative rewrite.

Recovery must preserve the intended current item, position, play/pause intent, and queue unless the
product contract explicitly says otherwise.

## 8. Audio processing

When Media3 `AudioProcessor` or `DefaultAudioSink` behavior is involved:

- map processor order;
- identify format assumptions and bypass rules;
- preserve latency/headroom/clipping invariants;
- distinguish DSP UI changes from DSP algorithm changes;
- test enable/disable and live parameter changes;
- avoid stacking two processors/equalizers that unintentionally multiply effects.

A settings redesign is not permission to rewrite a functioning DSP pipeline.

## 9. Android Auto and media browsing

For `MediaLibrarySession` browsing, propagate `page` / `pageSize` through the real data boundary when
collections can be large. Do not load an entire large library merely to call `.take(pageSize)`.

Preserve:

- parent/child IDs;
- ordering;
- browsable/playable flags;
- search behavior;
- root/home virtual folders;
- current queue behavior.

Use `thalarch-android`'s Room pagination reference when Room or another queryable local store backs
the library.

## 10. Proof

Compilation proves signatures and types only.

Depending on the changed contract, use the cheapest adequate evidence:

- targeted unit/state tests;
- Media3 component/integration tests;
- service/controller tests;
- emulator/device interaction;
- Android Auto/desktop-head-unit browsing where available;
- `adb`/logs/profiling for runtime lifecycle or memory claims.

Report runtime behavior `UNVERIFIED` when the required runtime boundary could not be exercised.
