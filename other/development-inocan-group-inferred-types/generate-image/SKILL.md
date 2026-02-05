---
name: generate-image
description: Generate game asset images from text descriptions using Replicate's nano-banana-pro model. Use this skill when the user asks to create or generate 2D images, sprites, textures, or visual assets for the game.
---

# Generate Image Skill

## Purpose
Generate game asset images using Replicate's nano-banana-pro model. This skill handles prompt optimization, API calls, and file management through a standalone executable script.

## Inputs
- `description` (required): Text description of the asset (e.g., 'racing car', 'obstacle cube')
- `assetType` (optional): Type of asset ('vehicle', 'obstacle', 'prop', 'general')
- `baseImagePath` (optional): Path to existing image for image-to-image editing

## Invocation

Run the standalone script with JSON arguments:

```bash
npx tsx /Users/tomek/projects/kata-workshop-cc/.claude/skills/generate-image/scripts/generate.ts '{
  "description": "red cube obstacle",
  "assetType": "obstacle"
}'
```

For image-to-image editing:

```bash
npx tsx /Users/tomek/projects/kata-workshop-cc/.claude/skills/generate-image/scripts/generate.ts '{
  "description": "red sports car with racing stripes",
  "assetType": "vehicle",
  "baseImagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_red_sports_car_20251203_153045.png"
}'
```

## Output

The script outputs JSON to stdout:

```json
{
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_red_cube_obstacle_20251203_153045.png",
  "prompt": "red cube obstacle, geometric, stackable, destructible appearance, 1:1 aspect ratio, white background, isometric view, game asset, suitable for 3D conversion, 1024px, clean edges, simple design, high quality render"
}
```

Progress messages are sent to stderr, so you can see them in the console but they won't interfere with JSON parsing.

## How It Works

The script internally:
1. **Optimizes the prompt** using best practices for game assets:
   - Adds technical requirements: '1:1 aspect ratio, white background, isometric view'
   - Adds context: 'game asset, suitable for 3D conversion'
   - Adds quality directives: '1024px, clean edges, simple design'
   - Adds type-specific hints based on `assetType`:
     - **vehicle**: 'side view, wheels visible, streamlined design'
     - **obstacle**: 'geometric, stackable, destructible appearance'
     - **prop**: 'detailed, recognizable silhouette'

2. **Calls Replicate API** with the optimized prompt
   - Model: `google/nano-banana-pro`
   - Aspect ratio: 1:1
   - Output format: PNG
   - Safety tolerance: 5

3. **Saves the image** to `/public/images/generated/`
   - Filename format: `image_{sanitizedDescription}_{timestamp}.png`
   - Example: `image_red_cube_obstacle_20251203_153045.png`
   - Timestamps prevent overwrites

## Error Handling

If an error occurs, the script:
- Exits with code 1
- Outputs JSON error to stderr: `{"error": "error message"}`

Common errors:
- **`REPLICATE_API_TOKEN not set`**: User needs to add API key to [.env](.env)
  - Guide them to: https://replicate.com/account/api-tokens
- **`description is required`**: Missing required field in JSON input
- **`Replicate API error`**: API call failed (check network, API key, quotas)

## Tools Required
- Bash: For executing the TypeScript script via `npx tsx`
- Read: For verifying the generated file (optional)

## Success Criteria
- Script exits with code 0
- Valid JSON output with `imagePath` and `prompt`
- Image file exists at the returned path
- File is a valid PNG
- File size is reasonable (< 5MB)
- Image matches the description

## Example Usage

### Simple Generation
```bash
npx tsx .claude/skills/generate-image/scripts/generate.ts '{
  "description": "blue racing car",
  "assetType": "vehicle"
}'
```

**Expected output:**
```json
{
  "imagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_blue_racing_car_20251203_154530.png",
  "prompt": "blue racing car, side view, wheels visible, streamlined design, 1:1 aspect ratio, white background, isometric view, game asset, suitable for 3D conversion, 1024px, clean edges, simple design, high quality render"
}
```

### Image Editing
```bash
npx tsx .claude/skills/generate-image/scripts/generate.ts '{
  "description": "blue racing car with yellow racing stripes",
  "assetType": "vehicle",
  "baseImagePath": "/Users/tomek/projects/kata-workshop-cc/public/images/generated/image_blue_racing_car_20251203_154530.png"
}'
```

This will use the existing image as a base and apply the modifications.

## Implementation Details

The script is located at:
[.claude/skills/generate-image/scripts/generate.ts](.claude/skills/generate-image/scripts/generate.ts)

It imports shared utilities from:
- `scripts/api/replicate.ts` - Replicate API client
- `scripts/utils/prompt-optimizer.ts` - Prompt enhancement logic

This architecture ensures:
- **Testability**: Script can be tested independently
- **Reusability**: Same script works from any context
- **Maintainability**: Logic is centralized, not duplicated
- **Version control**: Clear tracking in git
