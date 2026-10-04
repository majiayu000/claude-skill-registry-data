---
name: niagara-authoring
description: Create, modify, compile, and visually evaluate AAA-quality Niagara particle systems in the editor.
---
# Skill: Niagara VFX Authoring

This skill defines the workflows, architectural rules, and standard operating procedures (SOPs) for AI agents to create, modify, compile, parameterize, and visually evaluate AAA-quality Unreal Engine 5 Niagara particle systems.

---

## 1. Niagara Architecture & Stack Execution Flow

A Niagara System executes in hierarchical phases. Modules in each phase execute sequentially from top to bottom:

```
UNiagaraSystem
├── System Phases:
│   ├── SystemSpawn   (Initial system initialization)
│   └── SystemUpdate  (Per-frame system lifetime, system parameters)
└── UNiagaraEmitter (One or more emitters per system)
    ├── Emitter Phases:
    │   ├── EmitterSpawn   (Emitter lifetime, burst intervals)
    │   └── EmitterUpdate  (Spawn rate, burst triggers)
    ├── Particle Phases:
    │   ├── ParticleSpawn  (Initial particle attributes: Location, Velocity, Mass, Lifetime, Color, Size)
    │   ├── ParticleUpdate (Per-frame attribute mutation: Forces, Drag, Acceleration, Color Curves, Collision)
    │   └── ParticleEvent  (Event response: OnCollision, OnDeath, Location events)
    └── Renderers:
        └── SpriteRenderer / MeshRenderer / RibbonRenderer / LightRenderer / DecalRenderer
```

### Module Stack Ordering Rules
1. **Solvers Last in Update**: When using physics forces (`GravityForce`, `Drag`, `AccelerationForce`, `PointAttractor`), always ensure `SolveForcesAndVelocity` is placed **after** all force modules in `ParticleUpdate`.
2. **Age & Lifetime First**: `UpdateAge` must run in `ParticleUpdate` before size/color scale modules that sample particle normalized age (`Particles.NormalizedAge`).
3. **Spawn Position Before Velocity**: Place spawn shape/location modules (`SphereLocation`, `BoxLocation`, `CylinderLocation`) before `AddVelocity`.

---

## 2. Standard Tool Workflow

### Step 1: Asset Initialization
* **Create System**:
  ```json
  {
    "_tool_name": "create_niagara_system",
    "asset_path": "/Game/VFX/NS_Explosion"
  }
  ```
* **Create Effect Type (Scalability & LODs)**:
  ```json
  {
    "_tool_name": "create_niagara_effect_type",
    "asset_path": "/Game/VFX/NE_ExplosionScalability"
  }
  ```
* **Create Niagara Data Channel (High-Frequency Decoupled Events)**:
  ```json
  {
    "_tool_name": "create_niagara_data_channel",
    "asset_path": "/Game/VFX/NDC_Impacts"
  }
  ```

### Step 2: Add Emitters
Append clean template emitters or duplicate from existing systems using `add_niagara_emitter`.
* **Stock Templates**: `SpriteBurst`, `RibbonTrail`, `MeshDebris`, `GPUSimulation`, or any engine template path (e.g. `/Niagara/DefaultAssets/Templates/Emitters/SimpleSpriteBurst.SimpleSpriteBurst`).
* **From Existing System**: Pass `system_path` and `emitter_template` as the source system, with optional `source_emitter_name` to extract a specific emitter.
* *Note: The engine automatically duplicates the template into the system's private package, ensuring templates on disk are never contaminated.*

```json
{
  "_tool_name": "add_niagara_emitter",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_template": "SpriteBurst",
  "emitter_name": "CoreFlash"
}
```

### Step 3: Add Logic Modules (`add_niagara_module`)
Inject stock or custom modules into any execution phase (`SystemSpawn`, `SystemUpdate`, `EmitterSpawn`, `EmitterUpdate`, `ParticleSpawn`, `ParticleUpdate`, `ParticleEvent`):
* **Stock Module Names**: `AddVelocity`, `GravityForce`, `Drag`, `Collision`, `AccelerationForce`, `SpawnBurstInstantaneous`, `SpawnRate`, `ScaleSpriteSize`, `ScaleColor`, `SolveForcesAndVelocity`, `UpdateAge`, `SphereLocation`, `BoxLocation`, `PointLocation`.
* **Asset Path Lookup**: Pass full content paths (e.g. `/Niagara/Modules/Spawn/Location/SphereLocation.SphereLocation` or project scripts `/Game/VFX/Modules/M_CustomForce`).
* **Phase Rules**:
  * For `SystemSpawn` or `SystemUpdate`, omit `emitter_name`.
  * For emitter/particle phases, provide `emitter_name`.
  * Use `target_index` (0-based) to insert at a precise position in the stack.

```json
{
  "_tool_name": "add_niagara_module",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "ParticleUpdate",
  "module_type": "Drag",
  "target_index": 1
}
```

### Step 4: Configure Pins, Direct Data Interfaces & Reset Pins
* **Flexible Input Modes**: Provide either:
  * Literal `value` (e.g. `"1.5"`, `"(X=0,Y=0,Z=-980)"`, `"(R=1,G=0.5,B=0,A=1)"`)
  * `link_parameter` (e.g. `"User.PrimaryColor"`, `"Particles.NormalizedAge"`)
  * **Direct Data Interface / Asset Input**: Provide `asset_path`, `interface_class`, and/or `properties` directly to configure the pin's internal Data Interface without needing an intermediate User parameter (ideal when the asset/channel does not need runtime gameplay rebinding).
* **Targeting Multiple Modules**: When an emitter contains multiple modules of the same type, use `module_index` (0-based) or `node_guid` to target the exact instance.

```json
// Example 1: Linking to an existing parameter
{
  "_tool_name": "set_niagara_module_pin",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "ParticleUpdate",
  "module_type": "ScaleColor",
  "pin_name": "ScaleAlpha",
  "link_parameter": "Particles.NormalizedAge"
}

// Example 2: Direct Data Interface configuration on module input
{
  "_tool_name": "set_niagara_module_pin",
  "system_path": "/Game/VFX/NS_ImpactListener",
  "emitter_name": "ListenerEmitter",
  "phase": "ParticleUpdate",
  "module_type": "ReadFromDataChannel",
  "pin_name": "DataChannel",
  "interface_class": "NiagaraDataInterfaceDataChannelRead",
  "asset_path": "/Game/VFX/NDC_Impacts"
}
```

* **Direct Curve Module Input (`set_niagara_module_pin` with `curve_keys`)**:
  To configure an inline curve data interface (e.g. `ScaleSpriteSize.Uniform Curve Sprite Scale` or `ScaleColor.ScaleAlpha`) directly on a module input pin:
```json
{
  "_tool_name": "set_niagara_module_pin",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "ParticleUpdate",
  "module_type": "ScaleSpriteSize",
  "pin_name": "Uniform Curve Sprite Scale",
  "curve_keys": [
    { "time": 0.0, "value": 1.0 },
    { "time": 1.0, "value": 0.0 }
  ]
}
```
For multi-channel curves (e.g. `NiagaraDataInterfaceColorCurve` or vector curves), pass an object keyed by channel name:
```json
{
  "_tool_name": "set_niagara_module_pin",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "ParticleUpdate",
  "module_type": "ScaleColor",
  "pin_name": "Linear Color Curve",
  "curve_keys": {
    "Red": [{ "time": 0.0, "value": 1.0 }, { "time": 1.0, "value": 0.2 }],
    "Green": [{ "time": 0.0, "value": 0.8 }, { "time": 1.0, "value": 0.0 }],
    "Blue": [{ "time": 0.0, "value": 0.1 }, { "time": 1.0, "value": 0.0 }]
  }
}
```
*Note: Multi-channel curves also accept channel abbreviations (`"R"`, `"G"`, `"B"`, `"A"`, `"X"`, `"Y"`, `"Z"`), or a flat array `[{"time": 0.0, "value": 1.0}, ...]` to apply uniformly across all channels. Ensure the module's mode switch (e.g. ScaleColor's `Color Scale Mode = RGBA Linear Color Curve`) is set so the curve pin is active.*
Inspect existing curve keys on any curve DI module input using `list_niagara_parameters` with scope `"ModuleInput"`, `"GraphInput"`, or `"all"`.

* **Resetting Module Pins (`reset_niagara_module_pin`)**:
  To remove an input override, restore autogenerated default values on static switches, and clean up upstream exclusive or orphaned input nodes:
```json
{
  "_tool_name": "reset_niagara_module_pin",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "ParticleUpdate",
  "module_type": "ScaleColor",
  "pin_name": "ScaleAlpha",
  "clean_orphaned_nodes": true
}
```

* **Dynamic Input Scripts on Module Pins (`dynamic_input`)**:
  To attach a dynamic calculation script (e.g. `Multiply_Int`, `Multiply_Float`, `Divide_Float`) to a module pin instead of a literal constant:
```json
{
  "_tool_name": "set_niagara_module_pin",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "EmitterUpdate",
  "module_type": "SpawnBurstInstantaneous",
  "pin_name": "Spawn Count",
  "dynamic_input": "Multiply_Int"
}
```

### Step 5: Configure & Manage Renderers
Add visual renderers (`add_niagara_renderer`), update existing renderers (`edit_niagara_renderer`), or remove unwanted/default renderers (`remove_niagara_renderer`):
* **Add Renderer**:
```json
{
  "_tool_name": "add_niagara_renderer",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "renderer_type": "Light",
  "properties": {
    "RadiusScale": 250.0,
    "bCastShadows": false
  }
}
```
* **Edit Renderer** (modify properties or enable/disable):
```json
{
  "_tool_name": "edit_niagara_renderer",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "renderer_name_or_type": "SpriteRenderer",
  "b_is_enabled": false,
  "properties": {
    "Material": "/Game/Materials/M_ParticleGlow"
  }
}
```
* **Remove Renderer**:
```json
{
  "_tool_name": "remove_niagara_renderer",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "renderer_name_or_type": "SpriteRenderer"
}
```

### Removing Modules & Emitters
* **Remove Module (`remove_niagara_module`)**:
```json
{
  "_tool_name": "remove_niagara_module",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash",
  "phase": "ParticleUpdate",
  "module_name": "Drag"
}
```
* **Remove Emitter (`remove_niagara_emitter`)**:
```json
{
  "_tool_name": "remove_niagara_emitter",
  "system_path": "/Game/VFX/NS_Explosion",
  "emitter_name": "CoreFlash"
}
```

### Step 6: Expose Parameters, Bind Data Interfaces & Inspect
* **Parameter Store Scope Rules**:
  * `set_niagara_parameter` and `set_niagara_data_interface` configure the UNiagaraSystem asset's parameter store (`User.` scope).
  * `Emitter.` and `System.` scopes are internal to execution graphs and cannot be written directly to the asset parameter store. To configure emitter/system-level inputs, use `set_niagara_module_pin` directly or expose a `User.` parameter and link it.
* **User Parameters (`set_niagara_parameter`)**: Expose parameters for Blueprints, C++, or material overrides:
  ```json
  {
    "_tool_name": "set_niagara_parameter",
    "system_path": "/Game/VFX/NS_Explosion",
    "parameter_name": "User.PrimaryColor",
    "data_type": "LinearColor",
    "value": "(R=1.0,G=0.4,B=0.05,A=1.0)"
  }
  ```
* **User Data Interfaces (`set_niagara_data_interface`)**:
  When gameplay code or Blueprints need to dynamically assign or modify data interfaces at runtime:
  1. Bind the external data interface to a `User.` parameter via `set_niagara_data_interface`:
     ```json
     {
       "_tool_name": "set_niagara_data_interface",
       "system_path": "/Game/VFX/NS_ImpactListener",
       "parameter_name": "User.NDCReader",
       "interface_class": "NiagaraDataInterfaceDataChannelRead",
       "asset_path": "/Game/VFX/NDC_Impacts",
       "asset_property_name": "DataChannelAsset"
     }
     ```
  2. Link the module pin to that `User.` parameter via `set_niagara_module_pin`:
     ```json
     {
       "_tool_name": "set_niagara_module_pin",
       "system_path": "/Game/VFX/NS_ImpactListener",
       "emitter_name": "ListenerEmitter",
       "phase": "ParticleUpdate",
       "module_type": "ReadFromDataChannel",
       "pin_name": "DataChannel",
       "link_parameter": "User.NDCReader"
     }
     ```
* **Multi-Scope Parameter Inspection (`list_niagara_parameters`)**:
  Inspect parameters across any scope (`all`, `User`, `System`, `Emitter`, `ModuleInput`, `GraphInput`), including bound assets, DI classes, module input overrides, and detection of orphaned graph input nodes:
  ```json
  {
    "_tool_name": "list_niagara_parameters",
    "system_path": "/Game/VFX/NS_Explosion",
    "scope": "all",
    "include_module_inputs": true,
    "include_orphaned_nodes": true
  }
  ```
* **Parameter Cleanup (`remove_niagara_parameter`)**:
  Remove obsolete, misspelled, or orphaned parameters from the system parameter store:
  ```json
  {
    "_tool_name": "remove_niagara_parameter",
    "system_path": "/Game/VFX/NS_Explosion",
    "parameter_name": "User.ObsoleteParam"
  }
  ```

### Step 7: Synchronous Compilation Verification
Call `compile_niagara_system` to build bytecode and verify zero compilation errors across all system, emitter, and event scripts:
```json
{
  "_tool_name": "compile_niagara_system",
  "system_path": "/Game/VFX/NS_Explosion"
}
```

### Step 8: Temporal Vision Capture Loop
Call `capture_niagara_system_isolated` to render a 2x2 keyframe grid (10%, 30%, 60%, 90% simulation window):
```json
{
  "_tool_name": "capture_niagara_system_isolated",
  "system_path": "/Game/VFX/NS_Explosion",
  "duration_seconds": 1.5,
  "max_dimension": 512
}
```
* Inspect the returned image artifact:
  * Check quadrant 1 (10%): Initial burst shape, core flash intensity.
  * Check quadrant 2 (30%): Expansion velocity, debris dispersal.
  * Check quadrant 3 (60%): Drag deceleration, smoke volume buildup.
  * Check quadrant 4 (90%): Alpha fade, scale dissipation, zero hard pop artifacts.
  * Inspect the bottom-left 1-meter white scale indicator bar to verify physical world sizing.

---

## 3. General VFX Design Recipes

### Recipe A: Instantaneous Burst (Explosions, Impacts, Muzzle Flashes)
1. **Emitter**: Add `SpriteBurst` or clone `SimpleSpriteBurst`.
2. **EmitterUpdate**: Add `SpawnBurstInstantaneous`, set `SpawnCount` to desired particle count (e.g. 50–200).
3. **ParticleSpawn**:
   * Add `SphereLocation` (or `BoxLocation`) with radius ~20–50cm.
   * Add `AddVelocity` with radial velocity 500–1500 cm/s.
   * Set `Lifetime` range (e.g. Min: 0.3s, Max: 0.8s).
4. **ParticleUpdate**:
   * Add `Drag` (value: 2.0–5.0) to rapidly decelerate high-speed particles.
   * Add `ScaleSpriteSize` or `ScaleColor` linked to `Particles.NormalizedAge`.
   * Add `SolveForcesAndVelocity` at the end of `ParticleUpdate`.
5. **Renderer**: Add `LightRenderer` with `RadiusScale: 300.0` for dynamic flash.

### Recipe B: Continuous Ambient Stream (Fire, Smoke, Steam)
1. **Emitter**: Add `GPUSimulation` or `SpriteBurst` template.
2. **EmitterUpdate**: Add `SpawnRate` (e.g. 50–500 particles/sec).
3. **ParticleSpawn**:
   * Add `SphereLocation` or `PointLocation`.
   * Add `AddVelocity` with upward cone direction `(X=0, Y=0, Z=150)`.
   * Set `Lifetime` range (e.g. 1.5s–3.0s).
4. **ParticleUpdate**:
   * Add `AccelerationForce` pointing upwards `(X=0, Y=0, Z=100)`.
   * Add `ScaleSpriteSize` with a curve expanding size over lifetime.
   * Add `ScaleColor` fading alpha to 0.0 at `NormalizedAge: 1.0`.
   * Add `SolveForcesAndVelocity`.
5. **Renderer**: Ensure the assigned material uses `DepthFade` to prevent clipping against geometry.

### Recipe C: Physical Debris / Sparks
1. **Emitter**: Add `MeshDebris` or `SpriteBurst`.
2. **ParticleSpawn**:
   * Add `AddVelocity` with high random cone velocity.
   * Set `Mass` (e.g. 1.0–5.0).
3. **ParticleUpdate**:
   * Add `GravityForce` `(X=0, Y=0, Z=-980)`.
   * Add `Collision` module with `Restitution: 0.4` and `Friction: 0.2`.
   * Add `SolveForcesAndVelocity`.
4. **Renderer**: Add `MeshRenderer` and set `Meshes` property to a debris static mesh.

---

## 4. Advanced Architectural Patterns

### Niagara Data Channels (NDCs) for High-Frequency Events
* **Never use `SpawnSystemAtLocation` for high-frequency or overlapping events** (e.g. machine gun impacts, footsteps, shell casings, sparks). Spawning individual actor components for repetitive events creates heavy GC and draw call overhead.
* **Architecture**:
  1. Create a Data Channel asset (`create_niagara_data_channel`).
  2. Setup a persistent listener Niagara System with `set_niagara_data_interface` (`NiagaraDataInterfaceDataChannelRead`).
  3. Blueprints or C++ traces write compact hit matrices and material IDs directly to the channel.

### Scalability & Effect Types
* **Assign an `EffectType` to every production asset**: Distance culling, max instance budgets, and LOD culling prevent frame drops during intense gameplay.
* Culled at low scalability: dynamic light renderers, secondary sub-emitters, mesh debris.

---

## 5. Performance Optimization Checklist

- [ ] **GPU Simulation**: If particle count $\ge 1,000$, use GPU simulation target (`SimTarget = ENiagaraSimTarget::GPUSim`).
- [ ] **Fixed Bounds**: Always enable Fixed Bounds on finished assets to eliminate per-frame bounding box recalculations.
- [ ] **Translucency Softness**: For smoke/fire sprites, assign materials configured with `DepthFade` to prevent hard clipping against world geometry.
- [ ] **Scalability Assigned**: Ensure every asset is tied to a valid `EffectType` with distance culling enabled.
- [ ] **SolveForces Order**: Ensure `SolveForcesAndVelocity` is the last module in `ParticleUpdate` whenever forces or velocities are modified.
