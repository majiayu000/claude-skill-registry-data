---
name: generate-assets
description: Generates 3D models and audio assets via AI APIs (Meshy, ElevenLabs) and imports them into Unreal Engine.
argument-hint: "What you want to generate (e.g. '3D model of a rusty barrel', 'Audio of a villain laughing')"
---

# Generative AI Workflow

You have access to a Python utility script `generative_utils.py` located inside the plugin's ExternalServer directory. This script securely interfaces with third-party generative AI services to create assets for the Unreal Engine project.

## Requirements

The user MUST provide the required API keys in a `.env` file located at the root of the project.
- For 3D Models (Meshy): `MESHY_API_KEY`
- For Audio (ElevenLabs): `ELEVENLABS_API_KEY`

If the script fails due to a missing key, kindly ask the user to add the key to the `.env` file in the project workspace.

## Step 1: Generate the Asset

To generate an asset, you will run the Python script using a local terminal. The script will poll the API, download the asset, and save it.

Resolve the path to `generative_utils.py` dynamically:
- Script location: `{AGENT_PLUGIN_DIR}/ExternalServer/src/generative_utils.py`
- If `{AGENT_PLUGIN_DIR}` is not in your environment, use `.agents/plugins/UnrealEngine/ExternalServer/src/generative_utils.py` relative to the project root.

**For 3D Models:**
```bash
python "{AGENT_PLUGIN_DIR}/ExternalServer/src/generative_utils.py" --project-root "{PROJECT_ROOT}" meshy --prompt "Your detailed prompt here"
```
*Note: This will download an .fbx file and its associated PBR texture maps (.png).*

**For Audio / Text-to-Speech:**
```bash
python "{AGENT_PLUGIN_DIR}/ExternalServer/src/generative_utils.py" --project-root "{PROJECT_ROOT}" elevenlabs --prompt "Text to speak"
```
*Note: This will download a proper RIFF/WAV file.*

## Step 2: Import into Unreal Engine

Once the Python script succeeds, it will print the absolute paths of the downloaded files. You MUST import these files into the Unreal Editor immediately.

**For 3D Models:**
1. Use the `import_mesh` MCP tool for the `.fbx` model.
2. Use the `import_assets_batch` MCP tool for the texture `.png` files (`base_color`, `normal`, `roughness`, `metallic`, `ao`).
3. Destination paths: `/Game/GenAI/Meshes/` for models, `/Game/GenAI/Textures/` for texture maps.

**For Audio (.wav):**
1. Use the `import_assets_batch` MCP tool.
2. Destination path: `/Game/GenAI/Audio/`.

## Step 3: One-Shot PBR Material Setup (3D Models Only)

After importing the mesh and texture maps, build and assign the material using the native one-shot PBR material action:

1. **Create PBR Material Graph**: Use `create_pbr_material_from_textures` to instantiate texture samples and wire `BaseColor`, `Normal`, `Roughness`, `Metallic`, and `AO` pins in a single atomic tool call:
   ```json
   {
     "MaterialPath": "/Game/GenAI/Materials/M_GenAI_{Name}",
     "BaseColorTexturePath": "/Game/GenAI/Textures/T_{Name}_BaseColor",
     "NormalTexturePath": "/Game/GenAI/Textures/T_{Name}_Normal",
     "RoughnessTexturePath": "/Game/GenAI/Textures/T_{Name}_Roughness",
     "MetallicTexturePath": "/Game/GenAI/Textures/T_{Name}_Metallic",
     "BlendMode": "Opaque",
     "ShadingModel": "DefaultLit"
   }
   ```
2. **Assign Material**: Use `configure_static_mesh` or `set_component_properties` to assign `/Game/GenAI/Materials/M_GenAI_{Name}` to the static mesh material slot.

## Step 4: Sound Wave & Cue Setup (Audio Assets Only)

After importing raw `.wav` audio files into `/Game/GenAI/Audio/`:

1. **Configure Sound Wave & Sound Cue**: Use `configure_sound_wave_cue` to set playback parameters (`bLooping`, `VolumeMultiplier`, `PitchMultiplier`) and optionally generate a `USoundCue` asset with 3D spatial attenuation:
   ```json
   {
     "SoundWaveAsset": "/Game/GenAI/Audio/SW_GenAI_{Name}",
     "CueAssetPath": "/Game/GenAI/Audio/SC_GenAI_{Name}",
     "bLooping": false,
     "VolumeMultiplier": 1.0,
     "PitchMultiplier": 1.0,
     "AttenuationAssetPath": "/Game/Audio/ATT_Default3D"
   }
   ```
