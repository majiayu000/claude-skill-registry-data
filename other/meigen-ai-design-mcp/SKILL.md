---
name: meigen-ai-design-mcp
description: Generate images and videos with AI using MeiGen MCP server for Claude Code, Cursor, and other AI coding tools
triggers:
  - generate an image
  - create a logo design
  - make a product photo
  - animate this into a video
  - find design inspiration
  - enhance my image prompt
  - switch AI image models
  - setup image generation
---

# MeiGen AI Design MCP

> Skill by [ara.so](https://ara.so) — Design Skills collection.

MeiGen AI Design MCP turns AI coding tools into professional design assistants. It provides 8 MCP tools for generating images and videos, searching 1,446 curated prompts, enhancing prompts with AI, and managing design workflows. Works with Claude Code, Cursor, Windsurf, Roo Code, OpenClaw, and any MCP-compatible host.

**Backend options:**
- **MeiGen Cloud** — 9 models (GPT Image 2, Nanobanana 2, Midjourney V8.1, Flux 2 Klein, Seedream 5.0, Seedance 2.0, Happyhorse 1.0, Veo 3.1)
- **OpenAI-compatible API** — bring your own key and endpoint
- **Local ComfyUI** — run on your own GPU, full control over workflows

## Installation

### Claude Code Plugin (Recommended)

```bash
# Add marketplace and install
/plugin marketplace add jau123/MeiGen-AI-Design-MCP
/plugin install meigen@meigen-marketplace
```

**Restart Claude Code** after installation. Then run the setup wizard:

```bash
/meigen:setup
```

### Cursor / VS Code / Windsurf / Roo Code

```bash
# One command auto-configures for your tool
npx meigen init cursor      # Cursor
npx meigen init vscode      # VS Code / GitHub Copilot
npx meigen init windsurf    # Windsurf
npx meigen init roo         # Roo Code
npx meigen init claude      # Claude Code (project-level)
```

### OpenClaw

```bash
# Full plugin (commands + skills + MCP server)
openclaw bundles install clawhub:meigen-ai-design

# Or skill only
npx clawhub@latest install creative-toolkit
```

### Manual MCP Configuration

Add to your MCP config file (`.mcp.json`, `claude_desktop_config.json`, etc.):

```json
{
  "mcpServers": {
    "meigen": {
      "command": "npx",
      "args": ["-y", "meigen@1.3.1"],
      "env": {
        "MEIGEN_API_TOKEN": "meigen_sk_..."
      }
    }
  }
}
```

### CLI Mode (No MCP Host Required)

```bash
# Set token once
export MEIGEN_API_TOKEN=meigen_sk_...

# Generate
npx meigen gen --prompt "a calico cat in a sunlit kitchen"
npx meigen gen -p "tech logo" -m midjourney-v8.1 -r 1:1
npx meigen gen -p "product shot" --ref ~/Desktop/bottle.jpg
```

## Configuration

### Environment Variables

```bash
# MeiGen Cloud API token (get at https://www.meigen.ai → Settings → API Keys)
MEIGEN_API_TOKEN=meigen_sk_...

# OpenAI-compatible API (optional)
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1

# ComfyUI (optional)
COMFYUI_URL=http://localhost:8188

# Output directories (optional)
MEIGEN_OUTPUT_DIR=~/Pictures/meigen
MEIGEN_VIDEO_OUTPUT_DIR=~/Movies/meigen
```

### Project-Level Config

Create `.meigen.json` in your project root:

```json
{
  "provider": "meigen",
  "meigenApiToken": "${MEIGEN_API_TOKEN}",
  "defaultModel": "nanobanana-2",
  "defaultAspectRatio": "16:9",
  "comfyuiUrl": "http://localhost:8188",
  "comfyuiDefaultWorkflow": "txt2img",
  "openaiApiKey": "${OPENAI_API_KEY}",
  "openaiBaseUrl": "https://api.openai.com/v1"
}
```

## MCP Tools

### search_gallery

Search 1,446 curated prompts with visual previews. Free, no API key required.

```typescript
// AI agent will call this when user says:
// "find inspiration for product photography"
// "search for logo designs"
// "show me nature landscape prompts"

{
  "keywords": "product photography",
  "style": "commercial",
  "limit": 10
}
```

### get_inspiration

Get full prompt, all images, and metadata for a gallery entry. Free.

```typescript
// After search_gallery, get full details
{
  "id": "12345"
}
```

### enhance_prompt

Transform a brief idea into a professional image prompt. Free.

```typescript
// User says: "a coffee cup"
// AI calls enhance_prompt to expand into:
// "A ceramic coffee cup on a wooden table, warm morning light streaming through window, shallow depth of field, product photography style, commercial quality, 4K detail"

{
  "userPrompt": "a coffee cup",
  "style": "commercial",
  "aspectRatio": "16:9"
}
```

### list_models

List available models across all configured providers. Free.

```typescript
// Returns models from MeiGen Cloud, OpenAI, and local ComfyUI
{} // No parameters
```

### generate_image

Generate an image. Requires API key. Routes to best available provider automatically.

```typescript
// Basic generation
{
  "prompt": "a calico cat in a sunlit kitchen, photorealistic, 4K detail",
  "model": "nanobanana-2",
  "aspectRatio": "16:9"
}

// With reference image (local file auto-uploaded)
{
  "prompt": "product hero shot, professional lighting",
  "model": "gpt-image-2",
  "aspectRatio": "1:1",
  "referenceImagePath": "/Users/you/Desktop/bottle.jpg"
}

// With specific provider
{
  "prompt": "logo design, minimal, tech startup",
  "provider": "comfyui",
  "workflowName": "txt2img",
  "aspectRatio": "1:1"
}
```

### generate_video

Generate a video via MeiGen platform. Requires API key. Saves MP4 to `~/Movies/meigen/`.

```typescript
// Text-to-video
{
  "prompt": "a cat walking through a garden, cinematic",
  "model": "seedance-2.0-fast",
  "duration": 5
}

// Image-to-video (first frame)
{
  "prompt": "camera slowly zooms in",
  "model": "happyhorse-1.0",
  "duration": 5,
  "firstFramePath": "/Users/you/Desktop/scene.jpg"
}

// Veo 3.1 (longest duration)
{
  "prompt": "product rotation, studio lighting",
  "model": "veo-3.1",
  "duration": 10
}
```

**Video models:**
- `seedance-2.0-fast` — 5s, fastest
- `seedance-2.0-pro` — 5s, higher quality
- `happyhorse-1.0` — 5s, cinematic
- `veo-3.1` — up to 10s, best quality

### comfyui_workflow

Manage ComfyUI workflow templates. Free.

```typescript
// List workflows
{
  "action": "list"
}

// View workflow details
{
  "action": "view",
  "name": "txt2img"
}

// Import new workflow (from ComfyUI API format JSON)
{
  "action": "import",
  "name": "my-flux-workflow",
  "workflow": { /* ComfyUI API format workflow */ }
}

// Delete workflow
{
  "action": "delete",
  "name": "old-workflow"
}
```

### manage_preferences

Remember user's preferred style, aspect ratio, model, and favorite prompts. Free.

```typescript
// Set preferences
{
  "action": "set",
  "preferences": {
    "defaultModel": "midjourney-v8.1",
    "defaultAspectRatio": "1:1",
    "favoriteStyle": "minimal modern",
    "favoritePrompts": ["tech logo", "product photography"]
  }
}

// Get preferences
{
  "action": "get"
}
```

## Slash Commands

```bash
# Quick generate — skip conversation
/meigen:gen a calico cat in sunlit kitchen

# Search prompts
/meigen:find product photography

# Browse models
/meigen:models

# Setup wizard
/meigen:setup
```

## CLI Usage

### Basic Generation

```bash
# Simple prompt
npx meigen gen --prompt "a calico cat in a sunlit kitchen"

# Specific model + aspect ratio
npx meigen gen -p "tech logo" -m midjourney-v8.1 -r 1:1

# With reference image
npx meigen gen -p "product hero shot" --ref ~/Desktop/bottle.jpg

# Specific provider
npx meigen gen -p "portrait" --provider openai -m gpt-image-2

# ComfyUI workflow
npx meigen gen -p "landscape" --provider comfyui --workflow flux-dev
```

### Advanced Options

```bash
# Submit only (no polling) — good for CI
npx meigen gen -p "..." --no-wait

# Machine-readable JSON output
npx meigen gen -p "..." --json | jq -r '.imageUrls[0]'

# Custom output directory
MEIGEN_OUTPUT_DIR=/tmp/images npx meigen gen -p "..."

# Video generation (MeiGen Cloud only)
npx meigen gen -p "cat walking" --video -m seedance-2.0-fast --duration 5

# Video from first frame
npx meigen gen -p "zoom in" --video --first-frame scene.jpg
```

### All CLI Flags

```
-p, --prompt <text>          Image description (required)
-m, --model <name>           AI model (default: nanobanana-2)
-r, --aspect-ratio <ratio>   Aspect ratio: 1:1, 16:9, 9:16, etc. (default: 16:9)
--ref, --reference <path>    Reference image (local file, auto-uploaded)
--provider <name>            Force provider: meigen, openai, or comfyui
--workflow <name>            ComfyUI workflow name (when provider=comfyui)
--video                      Generate video instead of image
--duration <seconds>         Video duration: 5 or 10 (default: 5)
--first-frame <path>         First frame image for video (local file)
--no-wait                    Submit only, don't poll for completion
--json                       Machine-readable JSON output
```

## Common Patterns

### Parallel Batch Generation

When a user asks for multiple variations, MeiGen uses specialized sub-agents to generate in parallel:

```typescript
// User says: "Create 4 product images for this perfume"
// AI will:
// 1. Call enhance_prompt 4 times to craft distinct prompts
// 2. Spawn image-generator sub-agents to run generate_image in parallel
// 3. Return all 4 images in ~2 minutes

// No special code needed — MeiGen handles orchestration automatically
```

### Reference Image Upload

Local images are auto-compressed and uploaded:

```typescript
// User drops ~/Desktop/bottle.jpg into chat and says:
// "Make this look more professional"

// AI calls:
{
  "prompt": "professional product photography, studio lighting, white background",
  "model": "gpt-image-2",
  "aspectRatio": "1:1",
  "referenceImagePath": "/Users/you/Desktop/bottle.jpg"
}

// MeiGen auto-compresses to <10MB and uploads to MeiGen Cloud
```

### ComfyUI Workflow Import

```typescript
// 1. Export workflow from ComfyUI UI (Save API Format)
// 2. Import to MeiGen
{
  "action": "import",
  "name": "flux-dev-txt2img",
  "workflow": {
    "3": {
      "inputs": {
        "seed": 42,
        "steps": 20,
        "cfg": 7,
        "sampler_name": "euler",
        "scheduler": "normal",
        "denoise": 1,
        "model": ["4", 0],
        "positive": ["6", 0],
        "negative": ["7", 0],
        "latent_image": ["5", 0]
      },
      "class_type": "KSampler"
    },
    // ... rest of workflow
  }
}

// 3. Use in generate_image
{
  "prompt": "a cat",
  "provider": "comfyui",
  "workflowName": "flux-dev-txt2img"
}
```

### Prompt Enhancement Pipeline

```typescript
// User gives minimal prompt: "a logo"
// AI automatically enhances before generating:

// Step 1: enhance_prompt
{
  "userPrompt": "a logo",
  "style": "minimal modern"
}
// Returns: "Minimal modern logo design, geometric shapes, bold typography, monochrome color palette, vector art style, professional brand identity, clean lines, scalable, white background"

// Step 2: generate_image with enhanced prompt
{
  "prompt": "Minimal modern logo design, geometric shapes...",
  "model": "midjourney-v8.1",
  "aspectRatio": "1:1"
}
```

### Multi-Model Workflow

```typescript
// User: "Generate a logo with 3 different AI models"

// AI calls list_models to see what's available
{} // Returns: nanobanana-2, midjourney-v8.1, gpt-image-2, flux-2-klein, etc.

// Then generates with different models in parallel:
const models = ["nanobanana-2", "midjourney-v8.1", "flux-2-klein"];
for (const model of models) {
  generate_image({
    prompt: "Minimal tech startup logo, blue and white",
    model,
    aspectRatio: "1:1"
  });
}
```

## Troubleshooting

### "Provider not configured"

Run the setup wizard:

```bash
/meigen:setup
```

Or manually set environment variables:

```bash
export MEIGEN_API_TOKEN=meigen_sk_...
# OR
export OPENAI_API_KEY=sk-...
# OR
export COMFYUI_URL=http://localhost:8188
```

### ComfyUI connection failed

1. Check ComfyUI is running: `curl http://localhost:8188/history`
2. Verify URL in config: `"comfyuiUrl": "http://localhost:8188"`
3. Test workflow exists: call `comfyui_workflow` with `{"action": "list"}`

### Image generation times out

Video generation can take 5-10 minutes. If using Hermes Agent, increase timeout:

```yaml
mcp_servers:
  meigen:
    timeout: 600          # 10 minutes
    connect_timeout: 120  # 2 minutes
```

For Claude Code / Cursor, timeouts are handled automatically.

### "Invalid aspect ratio"

Supported ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, `9:21`

Model-specific limits:
- GPT Image 2: `1:1`, `16:9`, `9:16`
- Nanobanana 2: all ratios
- Midjourney V8.1: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`

### CLI: "Command not found: meigen"

Use `npx` to run without global install:

```bash
npx meigen gen -p "..."
```

Or install globally:

```bash
npm install -g meigen
meigen gen -p "..."
```

### Video: "Model does not support video"

Video generation is MeiGen Cloud only. Supported models:
- `seedance-2.0-fast`
- `seedance-2.0-pro`
- `happyhorse-1.0`
- `veo-3.1`

OpenAI and ComfyUI providers don't support video.

## Code Examples

### TypeScript: Generate Logo Variations

```typescript
// In an AI coding agent's context, this is what happens when user says:
// "Create 3 logo variations for a tech startup"

import { spawn } from 'child_process';

const prompt = "Minimal tech startup logo, geometric, blue and white, modern";
const models = ["nanobanana-2", "midjourney-v8.1", "flux-2-klein"];

async function generateLogoVariations() {
  const jobs = models.map(model => {
    return new Promise((resolve, reject) => {
      const proc = spawn('npx', [
        'meigen', 'gen',
        '--prompt', prompt,
        '--model', model,
        '--aspect-ratio', '1:1',
        '--json'
      ]);

      let output = '';
      proc.stdout.on('data', (data) => { output += data; });
      proc.on('close', (code) => {
        if (code === 0) {
          resolve(JSON.parse(output));
        } else {
          reject(new Error(`Model ${model} failed`));
        }
      });
    });
  });

  const results = await Promise.all(jobs);
  results.forEach((result, i) => {
    console.log(`${models[i]}: ${result.imageUrls[0]}`);
  });
}

generateLogoVariations();
```

### TypeScript: ComfyUI Workflow Execution

```typescript
// Generate with custom ComfyUI workflow
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function generateWithComfyUI() {
  const { stdout } = await execAsync(
    'npx meigen gen ' +
    '--prompt "portrait, cinematic lighting" ' +
    '--provider comfyui ' +
    '--workflow flux-dev-portrait ' +
    '--aspect-ratio 2:3 ' +
    '--json'
  );

  const result = JSON.parse(stdout);
  console.log('Image saved to:', result.localPath);
  return result.localPath;
}
```

### Bash: Batch Product Photos

```bash
#!/bin/bash
# Generate product photos from a reference image

REFERENCE="product.jpg"
PROMPTS=(
  "luxury still life, dramatic lighting"
  "minimal white background, studio lighting"
  "nature setting, botanical elements"
  "lifestyle shot with model"
)

for prompt in "${PROMPTS[@]}"; do
  npx meigen gen \
    --prompt "$prompt" \
    --ref "$REFERENCE" \
    --model gpt-image-2 \
    --aspect-ratio 4:3 \
    --json | jq -r '.localPath'
done
```

### Python: Video Generation Pipeline

```python
#!/usr/bin/env python3
import subprocess
import json
import os

def generate_video(prompt, first_frame=None, duration=5):
    cmd = [
        'npx', 'meigen', 'gen',
        '--prompt', prompt,
        '--video',
        '--model', 'seedance-2.0-fast',
        '--duration', str(duration),
        '--json'
    ]
    
    if first_frame:
        cmd.extend(['--first-frame', first_frame])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    print(f"Video saved to: {data['localPath']}")
    return data['videoUrls'][0]

# Text-to-video
generate_video("a cat walking through a garden, cinematic")

# Image-to-video
generate_video("camera zooms in slowly", first_frame="scene.jpg", duration=5)
```

### JavaScript: CI Pipeline Image Generation

```javascript
// ci-generate-assets.js
// Run in CI to generate marketing assets

const { execSync } = require('child_process');
const fs = require('fs');

const prompts = JSON.parse(fs.readFileSync('prompts.json', 'utf8'));

prompts.forEach((item) => {
  const cmd = `npx meigen gen --prompt "${item.prompt}" --model ${item.model} --aspect-ratio ${item.ratio} --no-wait --json`;
  
  try {
    const output = execSync(cmd, { encoding: 'utf8' });
    const result = JSON.parse(output);
    console.log(`Submitted: ${item.name} (ID: ${result.generationId})`);
  } catch (error) {
    console.error(`Failed: ${item.name}`, error.message);
    process.exit(1);
  }
});

console.log('All assets submitted. Check MeiGen dashboard for completion.');
```

## Provider-Specific Notes

### MeiGen Cloud

- **Free tier:** 10 images/day, search & enhance unlimited
- **Get API token:** https://www.meigen.ai → Settings → API Keys
- **Models:** nanobanana-2, gpt-image-2, midjourney-v8.1, flux-2-klein, seedream-5.0, seedance-2.0-fast, seedance-2.0-pro, happyhorse-1.0, veo-3.1
- **Video:** MeiGen Cloud only (OpenAI/ComfyUI don't support video)

### OpenAI-Compatible

- Works with OpenAI, Azure OpenAI, or any compatible API
- Set `OPENAI_API_KEY` and optionally `OPENAI_BASE_URL`
- Models: `gpt-image-2` (or whatever your endpoint provides)
- No video support

### Local ComfyUI

- Full control over models, samplers, workflows
- Import any ComfyUI API-format workflow
- Auto-detects KSampler, CLIPTextEncode, EmptyLatentImage, LoadImage nodes
- No cloud dependency, images never leave your machine
- No video support (use MeiGen Cloud for video)

## Advanced Configuration

### Custom Workflow Node Mapping

If MeiGen doesn't auto-detect your ComfyUI workflow nodes, manually specify IDs in workflow JSON:

```json
{
  "3": { "class_type": "KSampler", "_meigen_role": "sampler" },
  "6": { "class_type": "CLIPTextEncode", "_meigen_role": "positive_prompt" },
  "7": { "class_type": "CLIPTextEncode", "_meigen_role": "negative_prompt" },
  "5": { "class_type": "EmptyLatentImage", "_meigen_role": "latent" }
}
```

### Multi-Provider Fallback

Set up multiple providers for automatic fallback:

```json
{
  "provider": "comfyui",
  "comfyuiUrl": "http://localhost:8188",
  "meigenApiToken": "${MEIGEN_API_TOKEN}",
  "openaiApiKey": "${OPENAI_API_KEY}"
}
```

If ComfyUI is offline, MeiGen auto-falls back to cloud (MeiGen or OpenAI).

### Output Customization

```bash
# Custom output directories
export MEIGEN_OUTPUT_DIR=~/Desktop/ai-images
export MEIGEN_VIDEO_OUTPUT_DIR=~/Desktop/ai-videos

# Auto-open behavior (macOS only)
export MEIGEN_NO_AUTO_OPEN=1  # Disable auto-opening in Preview
```

## Resources

- **Homepage:** https://meigen.ai
- **GitHub:** https://github.com/jau123/MeiGen-AI-Design-MCP
- **Prompt Library:** https://github.com/jau123/nanobanana-trending-prompts
- **Discord:** https://discord.gg/uX6rnersUx
- **Video Demo:** https://youtu.be/JQ3DZ1DXqvs
