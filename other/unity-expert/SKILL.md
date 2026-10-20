---
name: unity-expert
description: Complete Unity Mobile Endless Runner Architecture & Technical Art Pipeline - Master suite covering AI 3D asset ingestion, FSM game architecture, zero-GC object pooling, URP CurvedWorld shaders, camera juicing, mobile audio/haptics, responsive UI, and live verification.
user-invocable: true
---

# Unity Expert - Mobile Endless Runner Master Architecture & Technical Art Pipeline

This skill provides a standardized, production-grade architecture and technical art framework for *Cardiv* (and modern 3D mobile endless runners). It encapsulates 7 deep-research master documents into modular execution sub-commands.

---

## ⚡ QUICK COMMAND REFERENCE

| Command | Focus Module | Primary Reference Document |
|---|---|---|
| `/unity-expert-asset` | AI 3D Asset Normalization & FBX Pipeline | [`ai_3d_asset_ingestion_and_normalization.md`](researches/ai_3d_asset_ingestion_and_normalization.md) |
| `/unity-expert-arch` | FSM State Machine & Solvable Lane Generator | [`endless_runner_state_and_generation_systems.md`](researches/endless_runner_state_and_generation_systems.md) |
| `/unity-expert-pool` | Zero-GC Object Pooling & Dynamic Hazards | [`mobile_performance_zero_gc_architecture.md`](researches/mobile_performance_zero_gc_architecture.md) |
| `/unity-expert-render` | URP CurvedWorld Shader & Lighting Mastery | [`urp_curved_world_and_lighting_mastery.md`](researches/urp_curved_world_and_lighting_mastery.md) |
| `/unity-expert-juice` | Camera Juicing, Dynamic FOV & Screenshake | [`camera_juicing_and_screen_shake.md`](researches/camera_juicing_and_screen_shake.md) |
| `/unity-expert-audio` | Engine Audio Pitch & Haptic Feedback | [`mobile_audio_and_haptics.md`](researches/mobile_audio_and_haptics.md) |
| `/unity-expert-ui` | Responsive UI, Safe Area Notch & Canvas Splitting | [`ui_and_hud_responsive_layout.md`](researches/ui_and_hud_responsive_layout.md) |
| `/unity-expert-verify` | Live Verification, Diagnostics & Capture | Unity Editor Playmode & Screenshot Audit Tools |

---

## 🔗 MCP TOOL & ARCHITECTURE COORDINATION MATRIX

```
                                [User Request / Action]
                                           │
       ┌───────────────────┬───────────────┼───────────────┬───────────────────┐
       ▼                   ▼               ▼               ▼                   ▼
/unity-expert-asset /unity-expert-arch /unity-expert-pool /unity-expert-render /unity-expert-juice
(ModelImporter FBX) (FSM Game State)  (Zero-GC Pool)   (CurvedWorldLit)    (Dynamic FOV/Shake)
```

---

## 1. /unity-expert-asset - AI 3D Model Ingestion & Normalization Pipeline

Automates raw AI mesh ingestion (Meshy AI, Tripo AI, Rodin) into game-ready prefabs with zero manual tweaking.

### Mandatory Asset Standards:
1. **Scale Baking & Category Real-World Auto-Scaling**:
   - FBX models force `globalScale = 1.0f`, `bakeAxisConversion = true`, and `useFileScale = false`.
   - Calculate scale dynamically based on Category Real-World Length/Height:
     $$\text{scaleFactor} = \frac{L_{\text{target}}}{L_{\text{FBXnative}}}$$
     - **Vehicles**: Cars = `4.5m`, SUVs/Vans = `5.2m`, Semi-Trucks = `14.0m`, Trains = `22.0m`.
     - **Environment Props**: Overpass Bridges = `6.5m` clearance height (18m span), Buildings = `12m - 25m` height, Trees = `4m - 8m` height.
   - **Pivot & Automated Y-Grounding**:
     - Vehicles: Geometric bounds center pivot + automated `-minY` grounding.
     - Environmental Props (Trees, Buildings, Bridges): Bottom Base Pivot (`min_z` in Blender) for zero-effort `Y = 0` ground placement.
     - **CRITICAL SPAWNER Y-OFFSET RETENTION RULE**: Spawners, pool managers, and placement logic MUST NEVER reset or overwrite `childModel.localPosition.y` to `0f` upon spawning. Root GameObjects sit at road surface level ($Y = 0$), while `childModel.localPosition.y` retains the prefab's ground height offset so vehicle wheels sit flush on top of the asphalt road without sinking into the ground.
   - **CurvedWorld Bounds Expansion**: Apply `CurvedWorldBoundsExpander.cs` to all large environmental props (Bridges, Buildings) to prevent SRP frustum culling when meshes curve on horizon.
2. **Tangent & Normal Calculation**: Recalculate smooth normals at $60^\circ$ and calculate MikkTSpace tangents (`importTangents = ModelImporterTangents.CalculateMikk`).
3. **Automated Orientation Scoring & Forward Alignment**:
   - Evaluate rotation matrices to find the bounding box size where $Z_{\text{length}} > X_{\text{width}} > Y_{\text{height}}$.
   - **World Space Pre-Multiplication Rule**: To flip model forward direction without inverting pitch/roll (preventing roof-on-ground flips), ALWAYS pre-multiply in world space:
     `bestRot = Quaternion.Euler(0f, 180f, 0f) * bestRot;`
4. **Geometric Wheel Detection & Pivot Centering Standard**:
   - For auto-split AI models (e.g. Meshy AI `model_part0`...`model_part20`), compute wheel positions in root space using submesh geometric bounds centers:
     `Vector3 posInRoot = root.transform.InverseTransformPoint(mf.transform.TransformPoint(mf.sharedMesh.bounds.center));`
   - Classify 4 wheels standardly based on `posInRoot.x >= 0` ("right" vs "left") and `posInRoot.z >= 0` ("front" vs "rear") into `wheel-front-left`, `wheel-front-right`, `wheel-rear-left`, `wheel-rear-right`.
   - **Local Pivot Normalization**: Center wheel mesh vertices around origin (`verts[i] -= center`) and offset local transform (`mf.transform.localPosition += center`) so wheels rotate smoothly around their own axle without orbital wobbling.
5. **Safe Tag & Layer Assignment Rule for Editor Setup Scripts**:
   - Editor automation and asset setup scripts MUST NEVER assign `gameObject.tag` or `gameObject.layer` directly without bounds checking.
   - Always check `int layer = LayerMask.NameToLayer("LayerName"); if (layer >= 0 && layer <= 31) gameObject.layer = layer;` to prevent out-of-bounds layer errors.
   - Always wrap tag assignment in `try { gameObject.tag = "TagName"; } catch (UnityException) {}` to handle uncreated tags gracefully without crashing Editor execution.
6. **PBR Texture Mapping & Material Pipeline**:
   - Automatically configure Texture Importers: `meshy_normal.png` as `TextureImporterType.NormalMap`.
   - Map PBR texture maps to `Custom/CurvedWorldLit` using exact shader property names:
     - `_BaseMap` = `meshy_basecolor.png`
     - `_BumpMap` = `meshy_normal.png` (`_NORMALMAP` keyword)
     - `_MetallicMap` = `meshy_metallic_smoothness.png` (Set `_Metallic` = 0.35, `_Smoothness` = 0.55)
     - `_EmissionMap` = `meshy_emission.png` (`_EMISSION` keyword, `_EmissionColor = Color.white`)
7. **Invisible Trigger Colliders & Prefab Execution Rules**:
   - **No Primitive Mesh Renderers**: Auxiliary triggers (ramps, checkpoints, event zones) MUST be plain GameObjects with `BoxCollider` (`isTrigger = true`) **WITHOUT `MeshFilter` or `MeshRenderer`**.
   - **Mandatory Editor Execution**: After writing/modifying any `[MenuItem("Cardiv/...")]` setup script, ALWAYS execute `Unity_ManageMenuItem` with `MenuPath` to rebuild `.prefab` assets directly inside Unity Editor.
8. **Hierarchy Isolation & Data-Driven Registry Rule**:
   - All vehicle metadata, materials, scale factors, and Y-offsets are stored in `VehicleDataSO` ScriptableObjects registered in `VehicleRegistry.asset`.
   - `PlayerVisualRig` and `MainMenuScreen` query `VehicleRegistry` dynamically. **0 C# code modifications required when adding 100+ vehicles.**
   ```text
   [Entity Root] (Scale = 1,1,1) -> Rigidbody, BoxCollider, IPoolable, Scripts
     └── [Visual Pivot Node] (Scale = 1,1,1) -> Local Y-Ground Offset & Rotation
           └── [Model FBX Instance]
                 ├── body (Car Body Mesh)
                 ├── wheel-front-left (Centered Pivot)
                 ├── wheel-front-right (Centered Pivot)
                 ├── wheel-rear-left (Centered Pivot)
                 └── wheel-rear-right (Centered Pivot)
   ```

*Reference Code & Guide:* [`ai_3d_asset_ingestion_and_normalization.md`](researches/ai_3d_asset_ingestion_and_normalization.md)

---

## 2. /unity-expert-arch - FSM State Machine & Solvable Traffic Generation

Implements clean, interface-driven game flow and solvable procedural spawning.

### Key Architectural Components:
1. **State Machine (`IGameState` & `GameContext`)**:
   - `IntroState`: Pool prewarm, camera countdown flyby.
   - `GameplayState`: Player control, velocity scoring, near-miss monitoring.
   - `BulletTimeState`: Matrix slow-motion curve (`Time.timeScale = 0.35f`).
   - `CrashState`: Impact freeze frame, vehicle crumple, ragdoll.
   - `ReviveState`: 50m hazard clearing sweep, 3s invincibility shield.
2. **Solvable Traffic Solver (`TrafficSpawnValidator`)**:
   Enforces mathematical solvability prior to committing batch spawns:
   $$T_{\text{arrive}} = \frac{\Delta Z}{V_{\text{player}} - V_{\text{traffic}}}, \quad T_{\text{switch}} < T_{\text{arrive}} - \epsilon_{\text{reflex}}$$
3. **Floating Origin Reset (`FloatingOriginHandler`)**:
   When player $Z > 1000\text{m}$, broadcast transform shift $(\Delta Z = -1000\text{m})$ to eliminate float32 vertex jitter and camera stutter.

*Reference Code & Guide:* [`endless_runner_state_and_generation_systems.md`](researches/endless_runner_state_and_generation_systems.md)

---

## 3. /unity-expert-pool - Zero-GC Object Pooling & Dynamic Event System

Eliminates runtime heap allocations and handles dynamic kinetic environmental hazards.

### Pooling & Event Rules:
1. **Zero-GC Contracts**: Implement `IPoolable` (`OnSpawn`, `OnDespawn`). Pre-cache `IPoolable[]` and `Rigidbody[]` arrays on prefab initialization.
2. **Payload Decoupling Rule**:
   When a truck payload drops (e.g. `FallingContainerEvent`), **do NOT unparent the truck's child mesh**. Hide the truck's child mesh (`SetActive(false)`) and spawn a separate pooled `FallenContainer` obstacle prefab onto the road.
3. **No Dynamic Component Churn**: Never call `DestroyImmediate` or `AddComponent` during gameplay spawning.
4. **Time.timeScale Physics Sync**: Always update `Time.fixedDeltaTime = 0.02f * Time.timeScale` during slow-motion.

*Reference Code & Guide:* [`mobile_performance_zero_gc_architecture.md`](researches/mobile_performance_zero_gc_architecture.md)

---

## 4. /unity-expert-render - URP CurvedWorld Shader & Mobile Lighting Pipeline

Renders stylized curved horizon visuals with 100% dynamic shadow accuracy.

### Shader & Lighting Standards:
1. **2-Axis Curvature HLSL Formula**:
   $$\Delta Y = -K_z \cdot (Z_{\text{vertex}} - Z_{\text{camera}})^2, \quad \Delta X = K_x \cdot (Z_{\text{vertex}} - Z_{\text{camera}})^2$$
2. **Pass Parity**: Apply identical vertex displacement math in both `ForwardLit` and `ShadowCaster` passes.
3. **CPU Frustum Culling Expansion**: Expand `renderer.localBounds` via `CurvedWorldBoundsExpander.cs` to prevent CPU static AABB culling from clipping bent meshes.
4. **Forward+ Lighting**: Use URP Forward+ for vehicle spotlights to keep SRP Batcher compatibility intact across mobile GPUs (ARM Mali, Qualcomm Adreno, Apple Silicon).

*Reference Code & Guide:* [`urp_curved_world_and_lighting_mastery.md`](researches/urp_curved_world_and_lighting_mastery.md)

---

## 5. /unity-expert-juice - Camera Juicing, Dynamic FOV & Screenshake

Delivers visceral player feedback and cinematic speed sensation.

### Juicing Mechanics:
1. **Speed FOV Stretch**: $FOV = \text{Lerp}(FOV_{\text{min}}, FOV_{\text{max}}, \text{InverseLerp}(V_{\text{min}}, V_{\text{max}}, V_{\text{player}}))$ with smooth damping.
2. **Trauma-Based Screenshake**: $Intensity = \text{Trauma}^2$. Perlin noise for rumble, harmonic damped sine wave for hard impacts.
3. **Impact Hitstop**: Micro pause ($0.03\text{s} - 0.08\text{s}$) using unscaled time for impact weight.
4. **Lane Switch Roll Banking**: Dynamic roll banking ($\theta_{\text{roll}} = -k \cdot v_x$) during quick evasive turns.

*Reference Code & Guide:* [`camera_juicing_and_screen_shake.md`](researches/camera_juicing_and_screen_shake.md)

---

## 6. /unity-expert-audio - Mobile Engine Audio & Haptics Pipeline

Produces realistic engine acoustics and cross-platform tactile feel.

### Audio & Haptic Standards:
1. **Engine Pitch Modulation**: $Pitch = P_{\text{min}} + (P_{\text{max}} - P_{\text{min}}) \cdot \frac{V}{V_{\text{max}}}$ with RPM gear curves and `Mathf.SmoothDamp`.
2. **3D Spatial Audio & Doppler**: 3D spatial blend (1.0), custom distance attenuation curves, and Doppler level tuning for passing traffic.
3. **Audio Mixer Ducking**: Low-pass filter sweeps ($22000\text{Hz} \rightarrow 800\text{Hz}$) during bullet-time and crash sequences.
4. **Cross-Platform Haptics**: iOS `UIImpactFeedbackGenerator` & Android `VibrationEffect` via `MobileHapticBridge.cs`.

*Reference Code & Guide:* [`mobile_audio_and_haptics.md`](researches/mobile_audio_and_haptics.md)

---

## 7. /unity-expert-ui - Responsive UI Layout & UGUI Performance

Optimizes mobile HUD elements across all display ratios and notches.

### UI Standards:
1. **Device Safe Area**: Auto-fit `RectTransform` anchors using `Screen.safeArea` for notches and punch-holes (`SafeAreaHandler.cs`).
2. **Canvas Splitting**: Separate Static HUD canvas from Dynamic Score/Speedometer canvases to prevent full-canvas VBO re-batching.
3. **Zero-GC Text Updates**: Use `TMP_Text.SetText()` overloads and shared material presets.
4. **Aspect Ratio Adapters**: Dynamic scaling for 16:9, 19.5:9, 21:9, and tablet 4:3 screens.

*Reference Code & Guide:* [`ui_and_hud_responsive_layout.md`](researches/ui_and_hud_responsive_layout.md)

---

## 8. /unity-expert-verify - Automated Quality Audit & Verification Workflow

1. Force asset database synchronization (`AssetDatabase.Refresh()`).
2. Run Unity Playmode test loop (`Unity_ManageEditor`).
3. Capture high-resolution viewport screenshots (`Unity_Camera_Capture`).
4. Validate zero console errors, zero runtime GC allocations, and clean 60 FPS performance.
