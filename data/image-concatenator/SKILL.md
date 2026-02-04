---
name: image_concatenator
description: A utility skill to vertically concatenate multiple images into a single file.
---

# Image Concatenator

This skill provides a tool to vertically merge images.

### Capabilities

- **Concatenate**: Merges list of images into one.

### How to use

Use the `run_bash` tool to run the skill’s script.

Provide the output path first, followed by one or more input image paths. Resolve the
script path from the skill root before invoking the tool. The script lives at
`scripts/concatenate_images.py`.

**Example:**
If the user asks to merge `a.png` and `b.png` into `result.png`, run the `run_bash`
tool with `scripts/concatenate_images.py result.png a.png b.png` as the command.
