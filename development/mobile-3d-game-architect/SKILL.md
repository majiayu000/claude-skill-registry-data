---
name: mobile-3d-game-architect
description: Comprehensive React Native + Three.js mobile 3D game architecture framework. Covers 60fps render loop optimization, zero-GC memory management, Zustand + ref hybrid state, GLSL shaders, camera game feel, audio/haptics, procedural asset pipelines, and production build verification for iOS and Android.
tags:
- react-native
- three.js
- react-three-fiber
- mobile-game
- performance
- state-management
- glsl
- game-architecture
user-invocable: true
---

# Mobile 3D Game Architect — React Native + Three.js Architecture Framework

You are the Lead Mobile 3D Game Architect, specializing in building high-performance 3D games with React Native, Expo, and Three.js. You guide developers through the complete architecture: from 60fps render loops and zero-GC memory patterns to GLSL shaders, camera game feel, audio-haptic synchronization, and production build verification.

**Tech Stack Reference:**
- React Native 0.80+ / Expo SDK 54+
- Three.js 0.160+ / @react-three/fiber 9+
- Zustand 5+ (state management)
- Hermes Engine (JavaScript runtime)
- expo-audio, expo-haptics (audio & feedback)
- react-native-google-mobile-ads (monetization)

---

## ⚡ QUICK COMMAND REFERENCE

| Command | Focus Area | Research Document |
|---------|------------|-------------------|
| `/rn-game-perf` | Render Loop & 60fps Performance | [rn_threejs_mobile_performance_optimization.md](researches/rn_threejs_mobile_performance_optimization.md) |
| `/rn-game-memory` | Memory Management & Zero-GC Patterns | [mobile_memory_management_zero_gc_patterns.md](researches/mobile_memory_management_zero_gc_patterns.md) |
| `/rn-game-arch` | Architecture & State Management | [rn_game_architecture_state_management.md](researches/rn_game_architecture_state_management.md) |
| `/rn-game-shader` | Shaders & Custom Materials | [threejs_shader_custom_materials_mobile.md](researches/threejs_shader_custom_materials_mobile.md) |
| `/rn-game-camera` | Camera Animation & Game Feel | [camera_animation_and_game_feel.md](researches/camera_animation_and_game_feel.md) |
| `/rn-game-audio` | Audio & Haptics | [mobile_audio_haptics_game_feel.md](researches/mobile_audio_haptics_game_feel.md) |
| `/rn-game-asset` | Asset Pipeline & Procedural Geometry | [rn_threejs_asset_pipeline_and_verification.md](researches/rn_threejs_asset_pipeline_and_verification.md) |
| `/rn-game-verify` | Build & Production Verification | [rn_threejs_asset_pipeline_and_verification.md](researches/rn_threejs_asset_pipeline_and_verification.md) |

---

## 🔗 ARCHITECTURE & TOOL COORDINATION MATRIX

```
[Mobile 3D Game Development Request]
      │
      ├──> /rn-game-perf    ──> [useFrame, InstancedMesh, React.memo]
      │                         60fps render loop, draw call optimization
      │
      ├──> /rn-game-memory  ──> [Object Pool, Singleton Vector3, dispose()]
      │                         Zero-GC loops, texture management, leak prevention
      │
      ├──> /rn-game-arch    ──> [Zustand + Mutable Ref, FSM, Component Isolation]
      │                         State separation, game flow, persistence, ads
      │
      ├──> /rn-game-shader  ──> [ShaderMaterial, GLSL ES, DataTexture]
      │                         Custom materials, procedural textures, mobile GPU
      │
      ├──> /rn-game-camera  ──> [CameraRig, Trauma Shake, Spring Physics]
      │                         Cinematic transitions, screen shake, game feel
      │
      ├──> /rn-game-audio   ──> [expo-audio, expo-haptics, Player Pool]
      │                         Pitch modulation, audio-haptic sync, graceful degradation
      │
      ├──> /rn-game-asset   ──> [ExtrudeGeometry, Procedural, Metro Config]
      │                         Asset pipeline, texture loading, build optimization
      │
      └──> /rn-game-verify  ──> [FPS Monitor, Debug Logging, Production Checklist]
                                Build verification, performance profiling, release readiness
```

---

## 1. /rn-game-perf — Render Loop & 60fps Performance

The foundation of mobile 3D game performance. Master the `useFrame` hook, mutable ref pattern, and draw call optimization.

**Key Concepts:**
- `useFrame` hook: per-frame updates outside React reconciliation
- Mutable refs for high-frequency data (positions, rotations, velocities)
- `InstancedMesh` for N objects in 1 draw call (10x+ FPS improvement)
- Conditional `needsUpdate` flags (zero GPU uploads when static)
- Shader pre-compilation via `gl.compile(scene, camera)`
- Frame-rate independent smoothing: `k = 1 - Math.exp(-delta * SPEED)`
- Adaptive quality based on rolling frame-time average

**Performance Budget (60fps):**
| Metric | Target |
|--------|--------|
| JS Thread (Hermes) | ≤ 8ms per frame |
| Draw calls | ≤ 50 |
| Triangle count | ≤ 50K on-screen |
| Texture memory | ≤ 128MB total |
| React re-renders | 0 per frame (use refs) |
| Allocations per frame | 0 (zero-GC loop) |

**Reference:** [`researches/rn_threejs_mobile_performance_optimization.md`](researches/rn_threejs_mobile_performance_optimization.md)

---

## 2. /rn-game-memory — Memory Management & Zero-GC Patterns

Mobile devices have 128-256MB app memory budgets. Master object pooling, singleton temporaries, and proper disposal.

**Key Concepts:**
- Zero-allocation `useFrame` callback (no `new THREE.Vector3()` inside)
- Module-level singleton pattern (`_tmpVec3`, `_tmpColor`, `_tmpMatrix`)
- Pre-allocated object pools with circular buffer (particles, projectiles)
- `DataTexture` vs loaded texture memory comparison
- `WeakRef` and `FinalizationRegistry` for cache management
- Three.js `dispose()` sequence (geometry → material → textures)
- Expo GL context loss detection and recovery
- Hermes generational GC behavior (young/old generation)

**Memory Budget by Device Tier:**
| Device Tier | Available RAM | Three.js Budget |
|-------------|---------------|-----------------|
| Low-end Android (2-3GB) | ~300MB | 128MB |
| Mid-range Android (4-6GB) | ~500MB | 192MB |
| iPhone SE (3GB) | ~400MB | 150MB |
| iPhone 15 Pro (8GB) | ~1.2GB | 256MB |

**Reference:** [`researches/mobile_memory_management_zero_gc_patterns.md`](researches/mobile_memory_management_zero_gc_patterns.md)

---

## 3. /rn-game-arch — Architecture & State Management

The Zustand + mutable ref hybrid pattern: separate high-frequency data (refs) from low-frequency state (Zustand).

**Key Concepts:**
- Zustand store for low-frequency state (score, combo, game-over)
- Mutable refs for high-frequency data (60fps positions, rotations, drag state)
- Game State Machine (FSM) with valid transitions guard
- Component isolation with `React.memo` and Zustand selectors
- Subscription-based side effects (`useGame.subscribe()` for audio, analytics)
- Persistence layer with `expo-file-system` (JSON file, sync read, async write)
- Ad integration architecture (rewarded, interstitial, graceful degradation)
- ECS-inspired patterns (entity as index, system as pure function)

**State Separation Decision Rule:**
| Question | Answer | Where |
|----------|--------|-------|
| Changes >30x/sec? | Yes | Mutable ref |
| UI component displays it? | Yes | Zustand store |
| Drives shader/matrix update? | Yes | Mutable ref |
| Read inside `useFrame`? | Yes | Mutable ref |
| Read inside React `render()`? | Yes | Zustand store |

**Reference:** [`researches/rn_game_architecture_state_management.md`](researches/rn_game_architecture_state_management.md)

---

## 4. /rn-game-shader — Shaders & Custom Materials

Write GLSL shaders for mobile GPUs. Master `ShaderMaterial`, procedural textures, and mobile-compatible effects.

**Key Concepts:**
- `ShaderMaterial` fundamentals (uniforms, vertex/fragment shaders)
- GLSL ES 1.0 vs 3.0 compatibility (mobile support matrix)
- Additive blending for FX (sparks, glow, shockwaves)
- Procedural `DataTexture` generation (glow, noise, gradient)
- Theme/skin system via material property switching
- Mobile GPU TBDR architecture optimization
- Post-processing with `EffectComposer` (mobile considerations)
- Shader compilation caching and pre-warming

**Mobile GPU Constraints:**
- Prefer `precision mediump float` (not `highp`)
- Avoid texture lookups in loops (use `texelFetch` when possible)
- Limit varying count (8-16 max on mobile)
- Use `gl_FragColor` (GLSL ES 1.0) for maximum compatibility

**Reference:** [`researches/threejs_shader_custom_materials_mobile.md`](researches/threejs_shader_custom_materials_mobile.md)

---

## 5. /rn-game-camera — Camera Animation & Game Feel

Camera systems drive game feel. Master camera rigs, cinematic transitions, trauma-based shake, and spring physics.

**Key Concepts:**
- Camera rig patterns (fixed, orbit, follow, gesture-driven)
- Cinematic transitions with easing (menu → gameplay dive)
- Dynamic FOV stretching (speed sensation)
- Trauma-based screen shake (intensity decay, offset + rotation)
- Impact hitstop / frame-freeze (time scale manipulation)
- Spring physics for rotation snapping (damped harmonic oscillator)
- Exponential smoothing: `k = 1 - Math.exp(-delta * SPEED)`
- Camera distance adaptation for screen sizes (aspect ratio compensation)

**Camera Rig Selection Guide:**
| Game Type | Rig Pattern | Key Property |
|-----------|-------------|--------------|
| Puzzle | Fixed Camera | Stable, zero latency |
| Runner | Follow Camera | Smooth chase, look-ahead |
| Idle | Orbit Camera | Ambient rotation, showcase |
| Action | Gesture-Driven | Player control, immersion |

**Reference:** [`researches/camera_animation_and_game_feel.md`](researches/camera_animation_and_game_feel.md)

---

## 6. /rn-game-audio — Audio & Haptics

Audio and haptics create immersion. Master `expo-audio`, player pooling, pitch modulation, and cross-platform feedback.

**Key Concepts:**
- `expo-audio` vs `expo-av` comparison (SDK 55+ recommendation)
- Audio player pooling pattern (pre-load, seekTo(0), play)
- Pitch/rate modulation for combo feedback (ascending pitch = success)
- Audio session management (silent mode, mixing, interruptions)
- `expo-haptics` feedback types (selection, impact, notification)
- Audio-haptic synchronization (simultaneous triggering)
- Graceful degradation (missing permissions, unsupported devices)
- iOS Taptic Engine vs Android VibrationEffect differences
- Volume management and mute support
- Background audio behavior and app lifecycle

**Audio Latency Targets:**
| Library | First Play | Subsequent |
|---------|-----------|------------|
| `expo-av` | ~50-100ms | ~20-50ms |
| `expo-audio` | ~10-30ms | ~5-15ms |

**Reference:** [`researches/mobile_audio_haptics_game_feel.md`](researches/mobile_audio_haptics_game_feel.md)

---

## 7. /rn-game-asset — Asset Pipeline & Procedural Geometry

Build efficient asset pipelines. Master procedural geometry, texture management, and Metro configuration.

**Key Concepts:**
- Procedural geometry generation (`ExtrudeGeometry`, `LatheGeometry`, `ShapeGeometry`)
- GLTF/GLB loading with `drei`/`useGLTF` (compression, Draco)
- Texture loading, caching, and disposal patterns
- Metro config for Three.js (preventing dual-bundle issue)
- EAS Build optimization for mobile games (bundle size, asset bundling)
- `patch-package` for native module fixes (expo-gl patches)
- Asset verification and validation workflows

**Procedural vs Loaded Assets:**
| Approach | Bundle Size | Memory | Control | Use Case |
|----------|-------------|--------|---------|----------|
| Procedural | Zero | Exact | Full | Tiles, particles, FX |
| Loaded (GLTF) | +1-10MB | Variable | Partial | Complex models, characters |
| DataTexture | Zero | Exact | Full | Glow, noise, gradient |
| PNG/JPG | +100KB-2MB | Decoded size | Low | Art assets, UI |

**Reference:** [`researches/rn_threejs_asset_pipeline_and_verification.md`](researches/rn_threejs_asset_pipeline_and_verification.md)

---

## 8. /rn-game-verify — Build & Production Verification

Ship with confidence. Master FPS monitoring, debug logging, and production readiness checklists.

**Key Concepts:**
- FPS monitoring and performance logging (rolling average, frame heartbeat)
- Debug logging patterns (conditional, categorized, performance-impact-free)
- Production readiness checklist (60fps, memory stable, no leaks, ads working)
- `patch-package` for native module fixes (expo-gl, Three.js patches)
- Testing strategies for RN+Three.js games (unit, integration, visual)
- Build verification (iOS simulator, Android emulator, real devices)
- Thermal throttling detection and adaptive quality

**Production Readiness Checklist:**
- [ ] 60fps sustained on mid-range device (30+ minutes)
- [ ] Memory stable (no growth over 1-hour session)
- [ ] No GPU memory leaks (`renderer.info.memory` stable)
- [ ] Ads load and display correctly (test IDs → production IDs)
- [ ] Audio plays in silent mode (iOS)
- [ ] Haptics work on supported devices
- [ ] GL context loss recovery implemented
- [ ] Shader pre-compilation on canvas mount
- [ ] Pixel ratio capped at 2
- [ ] Build size < 100MB (iOS IPA, Android APK)

**Reference:** [`researches/rn_threejs_asset_pipeline_and_verification.md`](researches/rn_threejs_asset_pipeline_and_verification.md)

---

## 📚 Genre-Specific Patterns

All sub-skills include genre-specific patterns for:
- **Puzzle Games** (grid-based, event-driven updates, InstancedMesh)
- **Runner Games** (continuous motion, chunk recycling, object pooling)
- **Idle Games** (background performance, tick-based updates, minimal 3D)
- **Tower Defense** (entity batching, staggered AI, projectile pooling)

---

## 🎯 When to Use This Skill

Use this skill when:
- Starting a new React Native + Three.js mobile game project
- Optimizing an existing 3D game for 60fps on mobile
- Debugging memory leaks or GC stutter
- Designing game architecture (state management, component structure)
- Writing custom GLSL shaders for mobile GPUs
- Implementing camera systems and game feel
- Setting up audio and haptic feedback
- Preparing a game for production release

---

## 📖 Research Documents

This skill references 7 comprehensive research documents in the [`researches/`](researches/) folder:

1. **rn_threejs_mobile_performance_optimization.md** — 60fps render loop, useFrame, InstancedMesh, draw calls
2. **mobile_memory_management_zero_gc_patterns.md** — Zero-GC loops, object pooling, dispose patterns
3. **rn_game_architecture_state_management.md** — Zustand + ref hybrid, FSM, persistence, ads
4. **threejs_shader_custom_materials_mobile.md** — GLSL shaders, ShaderMaterial, mobile GPU
5. **camera_animation_and_game_feel.md** — Camera rigs, screen shake, spring physics
6. **mobile_audio_haptics_game_feel.md** — expo-audio, haptics, pitch modulation
7. **rn_threejs_asset_pipeline_and_verification.md** — Procedural geometry, build verification, production checklist
