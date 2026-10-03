---
name: framecrawler
description: Build, run, troubleshoot, or extend FrameCrawler, including the local prompt UI, Codex plugin, SceneSpec generator, macOS menu-bar inspector, and Blender add-on handoff flow. Use when Codex needs to turn prompts into Blender-ready SceneSpec output or refine the editable blockout workflow.
---

# FrameCrawler

Use this skill when the user wants to work on the FrameCrawler prompt-to-Blender workflow rather than a generic text-to-JSON script.

## Quick Start

1. Keep one shared `scene_spec.json` path across Codex, the local UI, the menu-bar app, and Blender.
2. Prefer writing into the exact watched file Blender is already using.
3. Mention the next physical Blender step every time: `Load SceneSpec` once, or keep `Start Watching` enabled.
4. If the scene does not visibly change, check path alignment before changing the generation logic.

## What FrameCrawler Includes

- `index.html`, `app.js`, and `styles.css` for the local prompt UI
- `plugins/framecrawler/` for the repo-local Codex plugin
- `plugins/framecrawler/scripts/generate_scenespec.js` for CLI generation
- `FrameCrawlerBarApp/` for the native macOS menu-bar inspector
- Blender add-on files under the Tinyfish Blender workspace

## Workflow

### Generate SceneSpec

- Use the plugin or CLI to turn a cinematic prompt into watcher-friendly SceneSpec JSON.
- If the user wants Blender to visibly update, write into the exact `scene_spec.json` Blender is watching.
- Preserve the run archive under `.framecrawler/runs/<timestamp-project>/` so the latest prompt, JSON, and metadata stay inspectable.

### Guide The User

- Be explicit about the watch flow, not just the JSON output.
- Tell the user whether they should press `Load SceneSpec`, `Start Watching`, or reload the Blender add-on.
- If the menu-bar app is available, suggest it for quick prompting, Blender launch, and archive inspection.

### Improve The Product

- Prioritize concrete user-visible wins over broad rewrites.
- Strong next moves include:
  - clearer menu-bar actions
  - stronger plugin prompting guidance
  - better SceneSpec normalization for hard scene types
  - richer Blender-side controls that still preserve the watched-file workflow

## Reference Commands

Generate JSON:

```bash
node plugins/framecrawler/scripts/generate_scenespec.js \
  --prompt "A courier runs through a neon alley at dusk"
```

Write directly into Blender's watched file:

```bash
node plugins/framecrawler/scripts/generate_scenespec.js \
  --prompt "A courier runs through a neon alley at dusk" \
  --output /absolute/path/to/scene_spec.json
```

Perplexity-enriched generation:

```bash
PERPLEXITY_API_KEY=your_key_here \
node plugins/framecrawler/scripts/generate_scenespec.js \
  --prompt "A courier runs through a neon alley at dusk" \
  --research
```

## Resources

- `skills/framecrawler/agents/openai.yaml`: install-time metadata and default invocation prompt.
- `skills/framecrawler/assets/`: icons for catalog and README listings.
