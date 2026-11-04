---
name: codex-imagegen
description: Personal-only bridge that delegates raster image generation to Codex's built-in $imagegen via codex exec.
---

# Codex ImageGen Bridge

Personal profiles only. Work profiles should use their OpenAI API key image
path instead.

Use the bundled script relative to this skill directory:

```bash
./scripts/codex-imagegen.sh "prompt describing the image" [output-dir]
```

Default output directory: `output/imagegen`.
The command prints the final generated image path on success.

## Notes

- This delegates to `codex exec 'Use $imagegen ...'`, so Codex must be
  installed and logged in.
- The script refuses obvious `work*` Pi profiles.
- Do not copy Codex's `~/.codex/skills/.system/imagegen` skill into Pi; that
  skill depends on a Codex-only built-in tool.
