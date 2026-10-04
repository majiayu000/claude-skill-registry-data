---
name: nanobana-prompts
description: "Craft high-quality prompts for Google Nano Banana Pro image generation. Use when the user wants to write, improve, or refine an image generation prompt, needs help describing a visual concept for AI generation, wants to adapt a prompt to a different style (photorealistic, anime, 3D, etc.), wants to build a prompt from a reference image description, asks 'how do I prompt for...', 'write me a prompt', 'improve this prompt', 'make this more cinematic/anime/realistic', 'nanobana prompt', 'nano banana prompt', 'I want to make an image of...', 'help me with my image prompt', 'this image gen result looks bad', 'show me example prompts', or any request about prompt engineering for image generation — even if they don't mention Nano Banana by name."
license: Apache-2.0
version: 0.1.0
---

# Nano Banana Pro Prompt Crafting

Write excellent prompts for Nano Banana Pro (and compatible models) by applying proven structural patterns from 12,400+ community prompts.

## References

Load these files when needed — do not load all of them upfront:

- [references/prompt-structure.md](references/prompt-structure.md) — the universal 9-layer prompt structure (Subject → Outward). Load before crafting any prompt.
- [references/styles.md](references/styles.md) — style descriptors and keywords for 16 styles (photography, anime, 3D render, etc.). Load when the user picks a style or needs help choosing one.
- [references/technical-specs.md](references/technical-specs.md) — camera, lighting, composition, rendering, and resolution keywords. Load when adding technical polish to a prompt.
- [references/example-prompts.md](references/example-prompts.md) — complete example prompts organized by category. Load when the user wants to see examples or needs a starting point.

## Workflow Routing

---

**`workflows/craft-prompt.md`** — Creating a new prompt from scratch
- "Write me a prompt for..."
- "I need a prompt for a YouTube thumbnail / social post / character"
- "Help me describe [concept] for image generation"
- "Create a Nano Banana prompt for..."
- Any request to write a new image generation prompt from nothing

---

**`workflows/refine-prompt.md`** — Improving an existing prompt
- "Improve this prompt: [prompt text]"
- "This prompt isn't giving good results"
- "Make this prompt more detailed / specific / vivid"
- "What's wrong with this prompt?"
- "Add more detail to this prompt"
- Any request where the user already has prompt text and wants it better

---

**`workflows/adapt-style.md`** — Changing the style of a prompt
- "Convert this prompt to anime style"
- "Make this more cinematic / photorealistic / 3D"
- "I have a prompt for photography but I want it as an illustration"
- "Restyle this prompt for [target style]"
- Any request to keep the same subject/scene but change the visual style

---

**`workflows/describe-to-prompt.md`** — Building a prompt from a description or reference
- "I have this image, write a prompt that would recreate it"
- "Turn this description into an image prompt"
- "I want something that looks like [detailed description]"
- "Here's a reference — write a generation prompt based on it"
- Any request where the user provides a visual description or image to translate into prompt form

---

Once you identify the right workflow, load that file and follow its instructions.

If the user's intent matches more than one workflow, ask one clarifying question before routing. If it matches none, ask what they are trying to accomplish.

## Direct Operations

Some requests can be handled without a full workflow:

- **"Show me example prompts for [category]"** — Load [references/example-prompts.md](references/example-prompts.md) and present the relevant example.
- **"What styles are available?"** — Load [references/styles.md](references/styles.md) and list them with brief descriptions.
- **"What aspect ratio should I use for [platform]?"** — Load [references/technical-specs.md](references/technical-specs.md) and answer from the aspect ratio table.

## Integration with wavespeed-cli

This skill produces prompts. It does NOT run generation commands. After crafting a prompt, offer: "Want me to generate this with wavespeed-cli?" If the user says yes, hand off to the wavespeed-cli skill with the finished prompt.
