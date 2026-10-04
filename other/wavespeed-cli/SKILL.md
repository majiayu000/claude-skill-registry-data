---
name: wavespeed-cli
description: "AI image generation, video generation, SVG/vector creation, and image editing powered by WaveSpeed AI CLI. Use when the user wants to generate images, create videos from text or images, edit/modify images with AI, create visual assets (hero images, thumbnails, placeholders, social media graphics), animate still images into video, batch-generate multiple assets, iterate on designs, generate SVG/vector logos or icons, restore old photos, relight images, colorize B&W photos, swap faces, or segment images. Also triggers for: 'make me an image', 'generate a thumbnail', 'create a placeholder', 'animate this', 'edit this photo', 'change the background', 'generate assets for my project', 'I need visuals', 'make me a logo', 'restore this old photo', 'relight this', 'which wavespeed model should I use', or any request involving AI-powered image/video creation or editing — even if the user doesn't mention WaveSpeed by name."
license: Apache-2.0
version: 0.3.0
---

# WaveSpeed CLI

Generate images, videos, SVGs, and edit images using 36+ WaveSpeed AI models from the command line.

## References

Load these files when needed — do not load all of them upfront:

- [references/model-guide.md](references/model-guide.md) — **decision tree for picking the right model.** Load this before any generation or editing task. It maps user intent ("I need a logo", "restore this old photo") to the best model.
- [references/cli.md](references/cli.md) — full CLI command reference. Load before running any `wavespeed` command.
- [references/models.md](references/models.md) — full model catalog (36+ models with IDs, types, speeds). Load only when the model-guide doesn't cover the use case or the user asks to browse all models.
- [references/installation.md](references/installation.md) — installation and API key setup. Load if `wavespeed` is not installed or `WAVESPEED_API_KEY` is not set.

## Environment Check

Before running any workflow, verify the CLI is available and authenticated:

```bash
wavespeed --help
echo $WAVESPEED_API_KEY
```

If `wavespeed` is not installed or the API key is missing, load [references/installation.md](references/installation.md) and stop until setup is complete.

## Workflow Routing

---

**`workflows/generate-asset.md`** — Creating something new
- "Generate an image / video / logo / icon for my project"
- "Create a hero image / thumbnail / placeholder / social graphic"
- "Text to image / text to video / text to SVG"
- "I need a visual asset for..."
- "Make me a logo" / "Generate an icon"
- Any single image, video, or SVG generation request

---

**`workflows/iterate-design.md`** — Changing something existing
- "Refine this image" / "Try a different style"
- "Change the background / colors / lighting of this image"
- "Edit this photo to..." / "Make it more [adjective]"
- "Relight this" / "Restore this old photo" / "Colorize this"
- "Face swap" / "Change the season" / "Blend these together"
- Any request to modify, improve, or transform an existing image

---

**`workflows/batch-generate.md`** — Creating many things at once
- "Generate images for all these pages / sections"
- "I need 5 variations of..." / "Batch generate thumbnails"
- "Make multiple versions with different styles"
- Any request involving multiple generations from a list of prompts

---

Once you identify the right workflow, load that file and follow its instructions.

If the user's intent matches more than one workflow, ask one clarifying question before routing. If it matches none, ask what they are trying to accomplish.

**Direct CLI operations** — these skip workflows entirely. Load [references/cli.md](references/cli.md) and run directly:

- Upload a file — `wavespeed upload <file>`
- List models — `wavespeed models`
- Check status — `wavespeed status <request-id>`
- Quick one-off where the user already specified all parameters
