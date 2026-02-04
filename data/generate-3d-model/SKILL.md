---
name: generate-3d-model
description: Convert 2D images to 3D GLB models using Fal.ai's sam-3/3d-objects model. Use this skill when the user asks to create 3D models from images, convert images to GLB format, or generate 3D game assets from 2D sources.
---

# Generate 3D Model Skill

## Purpose
Convert 2D images to 3D GLB models using Fal.ai's sam-3/3d-objects model. This skill handles image validation, upload, 3D generation, and provides React Three Fiber integration examples through a standalone executable script.

## Inputs
- `imagePath` (required): Absolute path to the source image
- `description` (required): Original text description - **used as segmentation prompt for Fal.ai**
- `prompt` (optional): Additional guidance for 3D generation (defaults to description)

**Important**: The `description` is used to guide SAM's auto-segmentation. It should clearly describe
the object in the image (e.g., "blue cube", "red donut", "sports car"). This tells SAM what to extract
from the image. Without a clear prompt, segmentation will fail.

## Invocation

Run the standalone script with JSON arguments:

```bash
npx tsx /Users/tomek/projects/kata-workshop-cc/.claude/skills/generate-3d-model/scripts/generate.ts '{
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_red_cube_obstacle_20251203_153045.png",
  "description": "red cube obstacle"
}'
```

With optional prompt guidance:

```bash
npx tsx /Users/tomek/projects/kata-workshop-cc/.claude/skills/generate-3d-model/scripts/generate.ts '{
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_racing_car_20251203_154530.png",
  "description": "blue racing car",
  "prompt": "racing car with detailed wheels and aerodynamic body"
}'
```

## Output

The script outputs JSON to stdout:

```json
{
  "modelPath": "/Users/tomek/projects/kata-workshop-cc/public/3d/generated/model_red_cube_obstacle_20251203_153102.glb",
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_red_cube_obstacle_20251203_153045.png",
  "description": "red cube obstacle"
}
```

The model is automatically downloaded and saved to the local filesystem. The `modelPath` is an absolute path ready to use.

Progress messages are sent to stderr (e.g., "Generating 3D model (this will take 30-60 seconds)...", "Downloading GLB model...").

## How It Works

The script internally:
1. **Validates the image** file exists and is readable
2. **Converts image to base64 data URL** for Fal.ai API
3. **Calls Fal.ai API** to generate the 3D model
   - Model: `fal-ai/sam-3/3d-objects`
   - Takes 30-60 seconds to complete
   - Shows progress in console
4. **Downloads the model automatically** with retry logic
5. **Saves to local filesystem** and validates GLB format
6. **Returns the local file path**

## Loading in React Three Fiber

Once the GLB model is saved, provide this example to the user:

```typescript
import { useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

function RedCubeObstacle() {
  const gltf = useLoader(
    GLTFLoader,
    '/3d/generated/model_red_cube_obstacle_20251203_153102.glb'
  )

  return (
    <primitive
      object={gltf.scene}
      position={[0, 0, 0]}
      scale={1}
    />
  )
}
```

With physics (Rapier):

```typescript
import { RigidBody } from '@react-three/rapier'
import { useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

function PhysicsRedCubeObstacle() {
  const gltf = useLoader(
    GLTFLoader,
    '/3d/generated/model_red_cube_obstacle_20251203_153102.glb'
  )

  return (
    <RigidBody type="dynamic" colliders="hull">
      <primitive object={gltf.scene} />
    </RigidBody>
  )
}
```

## Error Handling

If an error occurs, the script:
- Exits with code 1
- Outputs JSON error to stderr: `{"error": "error message"}`

Common errors:
- **`FAL_KEY not set`**: User needs to add API key to [.env](.env)
  - Guide them to: https://fal.ai/dashboard/keys
- **`imagePath is required`**: Missing required field in JSON input
- **`description is required`**: Missing required field
- **`Image not found or invalid`**: Image file doesn't exist at specified path
- **`Fal.ai API error`**: API call failed (check network, API key, quotas)

## Tools Required
- Bash: For executing the TypeScript script via `npx tsx`
- Read: For verifying the generated file (optional)

## Success Criteria
- Script exits with code 0
- Valid JSON output with `modelPath`, `imagePath`, and `description`
- Model URL is accessible
- Downloaded GLB file is valid (magic number 'glTF')
- Model can be loaded in Three.js

## Tips for Best Results

For better 3D conversion quality, the source image should:
- Have clear object boundaries
- Be on white/transparent background
- Show the object from a good angle (isometric or side view works well)
- Have good lighting and contrast
- Be at least 512px (1024px is optimal)

If the 3D model quality is poor, suggest to the user:
- Regenerate the image with more emphasis on 'clean edges'
- Try a different camera angle in the prompt
- Ensure the background is truly white
- Simplify complex designs

## Example Usage

### Simple 3D Generation
```bash
# Step 1: Generate the 3D model (get URL)
npx tsx .claude/skills/generate-3d-model/scripts/generate.ts '{
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_blue_racing_car_20251203_154530.png",
  "description": "blue racing car"
}'
```

**Expected output:**
```json
{
  "modelPath": "https://fal.run/files/abc123/model.glb",
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_blue_racing_car_20251203_154530.png",
  "description": "blue racing car"
}
```

### With Prompt Guidance
```bash
npx tsx .claude/skills/generate-3d-model/scripts/generate.ts '{
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_racing_car_20251203_154530.png",
  "description": "racing car",
  "prompt": "sports car with visible wheels and aerodynamic design"
}'
```

## Implementation Details

The script is located at:
[.claude/skills/generate-3d-model/scripts/generate.ts](.claude/skills/generate-3d-model/scripts/generate.ts)

It imports shared utilities from:
- `scripts/api/fal.ts` - Fal.ai API client
- `scripts/utils/file-manager.ts` - Image validation

This architecture ensures:
- **Testability**: Script can be tested independently
- **Reusability**: Same script works from any context
- **Maintainability**: Logic is centralized, not duplicated
- **Version control**: Clear tracking in git
