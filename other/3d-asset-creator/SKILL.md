---
name: 3d-asset-creator
description: Complete AI 3D Asset Creation and Integration toolkit - generate reference concepts, trigger Meshy AI MCP generation, split and process models in Blender, wire custom PBR CurvedWorld materials in Unity, and visual test.
user-invocable: true
---

# 3D Asset Creator - AI Mesh Generation & Technical Art Pipeline

This skill provides a standardized, high-fidelity pipeline for generating 3D assets via Meshy AI, processing their geometries/wheels in Blender, and integrating them with custom URP CurvedWorld PBR materials in Unity.

---

## ⚡ QUICK COMMAND REFERENCE

| Command | Purpose | Subcommands / Tools |
|---|---|---|
| `/3d-asset-concept` | Reference Image Generation | `generate_image` |
| `/3d-asset-generate` | Meshy AI Generation Loop | `meshy-ai/create_text_to_3d_task`, `meshy-ai/retrieve_text_to_3d_task` |
| `/3d-asset-polish` | Blender Split, Symmetrize & Scale | `blender/execute_blender_code` |
| `/3d-asset-sync` | Unity Textures & PBR Materials | `unity-mcp/Unity_RunCommand` (BmwM5Mat & CurvedWorldLit) |
| `/3d-asset-auto` | Zero-Code Data-Driven Asset Import | `GenericVehicleAssetImporter` (Auto-creates `VehicleDataSO`, registers in `VehicleRegistry`) |
| `/3d-asset-verify` | Visual Inspection & Play Mode | `unity-mcp/Unity_ManageEditor`, `unity-mcp/Unity_Camera_Capture` |

---

## 🔗 MCP TOOL COORDINATION MATRIX

For automated execution, map slash commands directly to these MCP server tools:

```
[User Request]
      │
      ├──> /3d-asset-concept   ──> [generate_image] (2D Reference Art)
      │
      ├──> /3d-asset-generate  ──> [meshy-ai] (Text-to-3D Preview & Refine Tasks)
      │
      ├──> /3d-asset-polish    ──> [blender / execute_blender_code] (Wheel split, centering, scale)
      │
      ├──> /3d-asset-sync      ──> [unity-mcp / Unity_RunCommand] (Textures, NormalMap, PBR Material)
      │
      └──> /3d-asset-verify    ──> [unity-mcp / Unity_ManageEditor] (Viewport screenshots)
```

---

## 1. /3d-asset-concept - Reference Concept Art
Generate a 2D reference concept image using `generate_image` to establish proportions, silhouette, and colors before spawning the 3D model.
*Prompt Template:* `A beautiful low-poly stylized [asset_name], isometric view, vibrant colors, game asset, 3d render, studio lighting, solid color background, clean background, 3d low poly game art style`

---

## 2. /3d-asset-generate - Meshy AI Generation Loop

Generate high-quality 3D assets using the `meshy-ai` MCP server wrapper.

### A. Preview Generation (Draft Mesh)
Call `create_text_to_3d_task` with:
- `prompt`: `"low poly stylized [asset_name], vibrant colors, game ready asset, clean topology"`
- `mode`: `"preview"`
- `ai_model`: `"latest"`
- `art_style`: `"realistic"`
- `topology`: `"triangle"`
- `symmetry_mode`: `"auto"`

### B. Polling & Monitoring
Call `retrieve_text_to_3d_task` with the `task_id` returned from Step A. Wait until `status` is `"SUCCEEDED"`.

### C. Refinement & Texturing (High-Fidelity)
Call `create_text_to_3d_task` with:
- `mode`: `"refine"`
- `preview_task_id`: `<task_id_from_preview>`

Wait until the task succeeds. Extract the download URLs for:
- FBX/GLB model file.
- Textures (Diffuse/Albedo, Normal Map, Metallic, Roughness, Emission).

Place the down## 3. /3d-asset-polish - Blender Processing Script
Process the generated Meshy model in Blender to separate wheels, ground/center coordinates, and scale them to match realistic game scales.

Write a python script `process_model.py` and run it via Blender (`blender --background --python process_model.py`):

```python
import bpy
import math
import mathutils

# 1. Reset scene & import model
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath="<input_path>") # or glb

# 2. Join all elements temporarily to find the absolute geometric center
all_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for obj in all_meshes:
    obj.select_set(True)
bpy.context.view_layer.objects.active = all_meshes[0]
bpy.ops.object.join()
joined = bpy.context.active_object

# 3. Center and apply location
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
joined.location = (0, 0, 0)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 1. Rotate main object by +90 deg around Z FIRST so car front faces +Y in Blender (+Z Forward in Unity, matching BMW M5 1:1)
main_obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = main_obj
main_obj.select_set(True)
main_obj.rotation_euler.z += math.radians(90)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 2. Separate loose parts (relative wheel positions are locked 100% inside wheel wells!)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

all_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

# 3. Robust Wheel Partitioning (Matches low-poly 30-80 vCount as well as high-poly 15k vCount Meshy models)
wheels = []
body_parts = []
for obj in all_meshes:
    v_count = len(obj.data.vertices)
    bbox = obj.bound_box
    xs = [v[0] for v in bbox]
    ys = [v[1] for v in bbox]
    zs = [v[2] for v in bbox]
    dx, dy, dz = max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)
    
    # Cylindrical wheel shape check (0.12m - 0.20m diameter)
    if (0.12 <= dy <= 0.20 and 0.12 <= dz <= 0.20 and 0.05 <= dx <= 0.25) or "wheel" in obj.name.lower():
        wheels.append(obj)
    else:
        body_parts.append(obj)

# 4. Handle Environmental Props (Trees, Buildings, Bridges) vs Vehicles
if len(wheels) == 0:
    # Static Prop (No Wheels): Join all parts and set origin to ABSOLUTE BOTTOM BASE (min Z)
    bpy.ops.object.select_all(action='DESELECT')
    for p in all_meshes:
        p.select_set(True)
    bpy.context.view_layer.objects.active = all_meshes[0]
    bpy.ops.object.join()
    prop = all_meshes[0]
    prop.name = "prop_body"
    
    # Set pivot to bottom base for instant Y=0 ground placement in Unity
    bbox = prop.bound_box
    min_z = min(v[2] for v in bbox)
    bpy.context.scene.cursor.location = (0.0, 0.0, min_z)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
else:
    # Vehicle (With Wheels): Join body parts and center wheel origins
    bpy.ops.object.select_all(action='DESELECT')
    if body_parts:
        for p in body_parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = body_parts[0]
        bpy.ops.object.join()
        body = body_parts[0]
        body.name = "body"

    for w in wheels:
        bpy.ops.object.select_all(action='DESELECT')
        w.select_set(True)
        bpy.context.view_layer.objects.active = w
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        loc = w.location
        x_side = 'right' if loc.x >= 0 else 'left'
        y_pos = 'front' if loc.y >= 0 else 'back'
        w.name = f'wheel-{y_pos}-{x_side}'

# 5. Export clean FBX
bpy.ops.export_scene.fbx(
    filepath="Assets/Cardiv/Models/asset_processed.fbx",
    use_selection=False,
    axis_forward='-Z',
    axis_up='Y',
    bake_space_transform=True,
    apply_scale_options='FBX_SCALE_ALL',
    object_types={'MESH'}
)
```

---

## 4. /3d-asset-sync - Unity Materials & PBR Integration

Copy textures to `Assets/Cardiv/Textures/` and dynamically assign them to CurvedWorld Lit materials.

### A. Texture Settings
Ensure the normal map is imported correctly in C# Editor scripts:
```csharp
string normalPath = $"{importFolder}/meshy_normal.png";
TextureImporter importer = AssetImporter.GetAtPath(normalPath) as TextureImporter;
if (importer != null && importer.textureType != TextureImporterType.NormalMap)
{
    importer.textureType = TextureImporterType.NormalMap;
    importer.SaveAndReimport();
}
```

### B. Material Setup with Custom/CurvedWorldLit Shader
Assign maps directly to the custom shader properties (Do NOT use URP Lit property names like `_MetallicGlossMap`):
- `_BaseMap` = `meshy_basecolor.png`
- `_BumpMap` = `meshy_normal.png` (Enable `_NORMALMAP`)
- `_MetallicMap` = `meshy_metallic_smoothness.png` (Set `_Metallic` = 0.35, `_Smoothness` = 0.55)
- `_EmissionMap` = `meshy_emission.png` (Enable `_EMISSION` and set `_EmissionColor = Color.white`)

### C. Invisible Trigger Colliders & No Primitive Renderer Rule
- **CRITICAL:** NEVER leave primitive `MeshFilter` or `MeshRenderer` components (e.g. `PrimitiveType.Cube`) attached to trigger sub-objects, ramps, or auxiliary colliders.
- Auxiliary triggers (such as ramp jump triggers or pickup areas) MUST be created as plain GameObjects with `BoxCollider` (`isTrigger = true`) **WITHOUT `MeshFilter` or `MeshRenderer`**.
- This guarantees that interactive triggers remain 100% invisible in gameplay, while the real 3D mesh renders cleanly.

### D. Mandatory Unity Editor Execution Rule (`Unity_ManageMenuItem`)
- Writing or modifying a C# Editor script with `[MenuItem("Cardiv/...")]` does NOT update `.prefab` assets on disk automatically.
- After creating or modifying any setup script, you MUST explicitly execute `Unity_ManageMenuItem` with `MenuPath: "Cardiv/<MenuItemName>"` to run the script inside Unity Editor and save updated `.prefab` assets to disk.

### E. Bounds Expansion & Dynamic Scaling Standard
Never hardcode arbitrary scale multipliers. Auto-scale models by matching native FBX bounds length to category real-world meters:

| Category | Examples | Target Real-World Dimension | Key Placement Standard |
|---|---|---|---|
| **Sedan / Sports / Police** | Dodge, BMW, Police Car, Hypercar | Length `4.5m`, Width `1.9m` | Geometric bounds center pivot |
| **SUV / Van / Pickup** | SUV, Delivery Van | Length `5.2m`, Width `2.1m` | Geometric bounds center pivot |
| **Semi-Truck / Tanker** | Flatbed Truck, Fuel Tanker, Car Carrier | Length `14.0m`, Width `2.6m` | Geometric bounds center pivot |
| **Train / Locomotive** | Freight Train, Train Wagons | Length `22.0m`, Height `4.2m` | Track center pivot |
| **Overpass Bridge / Arch** | Highway Bridge, Arch Overhead | Clearance Height `6.5m`, Width `18.0m` | Spans 3 lanes + shoulders |
| **Buildings / Storefronts** | City Buildings, Gas Station | Height `12.0m - 25.0m` | Bottom Base Pivot (`Y=0` foundation) |
| **Trees / Vegetation** | Palm Trees, Bushes, Pine Trees | Height `4.0m - 8.0m` | Bottom Base Pivot (`Y=0` root) |
| **Small Obstacles** | Traffic Cone, Barrier, Shield | Height `0.8m - 1.2m` | Ground base pivot |

**Dynamic Scaling Formula:**
```csharp
// 1. Measure native unscaled FBX length (Z dimension)
float nativeLength = unscaledBounds.size.z;
float targetLength = GetCategoryTargetLength(vehicleType); // e.g. 4.5m for Car, 14.0m for Semi-Truck, 22.0m for Train
float scaleFactor = targetLength / nativeLength;
fbxInstance.transform.localScale = Vector3.one * scaleFactor;

// 2. Automated Y-Grounding: Calculate combined bounds min Y and set localPosition.y to -minY
Renderer[] renderers = fbxInstance.GetComponentsInChildren<Renderer>(true);
Bounds combinedBounds = new Bounds(fbxInstance.transform.position, Vector3.zero);
bool boundsInit = false;
foreach (var r in renderers)
{
    if (!boundsInit) { combinedBounds = r.bounds; boundsInit = true; }
    else { combinedBounds.Encapsulate(r.bounds); }
}
fbxInstance.transform.localPosition = new Vector3(0f, -combinedBounds.min.y, 0f); // Zero Y-clipping ground contact across ALL asset types!
```

---

## 4.5. Zero-Code Data-Driven Vehicle Pipeline (`GenericVehicleAssetImporter`)

When importing new vehicles into Cardiv, **do NOT write custom C# Editor scripts or modify `PlayerVisualRig.cs` / `MainMenuScreen.cs`**. The system uses a 100% Data-Driven architecture:

1. **Unity Menu:** Open `Cardiv -> Generic Vehicle Asset Importer Window` (or call `GenericVehicleAssetImporter.ProcessAndImportVehicle()`).
2. **Inputs:** Provide `importFolderPath` (e.g. `Assets/MeshyImports/NewCarFolder`), `vehicleId` (e.g. `AudiR8`), and `category` (e.g. `Sportscar`).
3. **Automated Pipeline:**
   - Auto-configures textures (`meshy_normal.png` as NormalMap).
   - Runs Blender CLI to rotate +90° Z, partition 4 wheels, and export `Assets/Cardiv/Models/[vehicleId]Car/[vehicleId]_processed.fbx`.
   - Creates URP `Custom/CurvedWorldLit` material at `Assets/Cardiv/Materials/[vehicleId]CarMat.mat`.
   - Computes combined bounds to calculate Y-ground offset (`groundOffsetY = -combinedBounds.min.y`).
   - Automatically builds/updates `VehicleDataSO` at `Assets/Cardiv/Data/Vehicles/[vehicleId]Data.asset` and registers it in `VehicleRegistry.asset`.
   - Attaches `Model_[vehicleId]` container to `PlayerCar.prefab`.
4. **Zero Code Changes Needed:** `PlayerVisualRig` and `MainMenuScreen` query `VehicleRegistry` dynamically at runtime. Adding 100+ vehicles requires **0 C# code modifications**.

---

## 5. /3d-asset-verify - Visual Inspection & Verification
1. Force asset recognition using `AssetDatabase.Refresh()`.
2. Instantiate prefabs using `Cardiv/Setup Prototype Scene` menu item.
3. Toggle `Play` mode using `Unity_ManageEditor`.
4. Run `FrameSelected` on `PlayerCar` Scene view and capture screenshot.
