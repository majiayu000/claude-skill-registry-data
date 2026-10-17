---
name: image-generation
description: Generate images from a text prompt, either locally via ComfyUI + FLUX.1 or through a hosted image API. Use whenever a task needs a hero image, social card, illustration, or any other generated visual.
---

# Skill: Image generation

Generate images with a local ComfyUI backend (free, private, slow) or a hosted
API (fast, paid, better with text inside the image).

## Trigger patterns

- Someone asks for an image, visual, or graphic
- A draft or post needs a hero image or social card
- "Generate an image of...", "Make a visual for...", "Create artwork for..."

## Choosing a backend

| | ComfyUI + FLUX.1 (local) | Hosted API |
|---|---|---|
| **Speed** | minutes, roughly 11 on consumer hardware | seconds |
| **Cost** | free after the hardware | per image, billed |
| **Privacy** | nothing leaves the machine | prompt and output transit a third party |
| **Text in images** | unreliable | good |
| **Best for** | background and batch work | quick turnarounds, iteration, text overlays |

Default to the local backend for anything not time-sensitive. Reach for the
hosted one when the request is urgent, when you are iterating on a design and
need the feedback loop tight, or when the image has to contain readable text.

If the request says "quick", "fast", or "now", use the hosted backend.

**Both backends cost something.** The local one costs wall-clock time and a
large chunk of memory - it will evict other models. The hosted one costs money
per call. Do not generate speculatively.

## Prerequisites

**Local (ComfyUI):**

- ComfyUI reachable at `comfyui_url`, running the workflow graph at `comfyui_workflow_path`
- FLUX.1 weights plus the T5 XXL, CLIP-L and VAE files in ComfyUI's models directory
- `comfyui_output_dir` set to ComfyUI's own output directory and readable from here

**Hosted:**

- `OPENAI_API_KEY` present in the environment, from the chassis secret store. The script reads the process environment only and never opens a credentials file.

## Workflow

### Step 1 - write the prompt

Both backends respond to descriptive, visual prompts. Cover:

- **Subject:** what is in the image
- **Style:** photography, illustration, watercolor, minimal, cinematic
- **Lighting:** natural light, golden hour, studio, neon
- **Composition:** close-up, wide angle, overhead, symmetrical
- **Mood:** warm, energetic, calm, professional

Good:

> A bright coworking space with exposed brick walls, developers at laptops, warm afternoon light through tall windows, photography style, shallow depth of field

Bad:

> coworking space

### Step 2 - generate

```bash
# Configured default backend
bash "$IMAGEGEN_SCRIPT" "your prompt here"

# Force local
bash "$IMAGEGEN_SCRIPT" --comfyui "your prompt here"

# Force hosted
bash "$IMAGEGEN_SCRIPT" --openai "your prompt here"

# Explicit output path (works with either backend)
bash "$IMAGEGEN_SCRIPT" --openai "your prompt here" /path/to/my-image.png
```

The script prints the output path on stdout and progress on stderr, so
`IMG=$(bash "$IMAGEGEN_SCRIPT" "...")` captures the path cleanly.

Default output is `<output_dir>/generated-<timestamp>.png`.

### Step 3 - look at it

Read the generated file and inspect it. If it is wrong, adjust the prompt with
more specific descriptors or different style keywords. Iteration is cheap on the
hosted backend and expensive on the local one, so be more deliberate about
prompt changes when running locally.

### Step 4 - use it

Attach it to the reply, or reference the path from whatever draft needed it.

## Limitations

- The local backend takes minutes and a large amount of memory. Other local models will be swapped out while it runs.
- The hosted backend costs money per image and needs a working internet connection.
- Neither backend is reliable at rendering a specific string of text, though the hosted one is markedly better.
- Generated images land in the configured output directory. Nothing is cleaned up automatically - that is the install's business.

## Prompt tips by use case

| Use case | Style keywords |
|---|---|
| Article hero | cinematic, wide angle, vibrant, professional photography |
| Social card | minimal, clean background, centered subject, bold colors |
| Event promo | energetic, crowd, warm lighting, urban setting |
| Technical post | clean desk setup, code on screen, minimal, soft lighting |

## Swapping the workflow graph

The shipped graph is FLUX.1 Dev in API format. To use a different one, point
`comfyui_workflow_path` at your own export and set `comfyui_prompt_node`,
`comfyui_seed_node` and `comfyui_output_node` to the matching node ids. Those
three ids are the entire contract between this script and the graph: prompt in,
seed in, filename out.
