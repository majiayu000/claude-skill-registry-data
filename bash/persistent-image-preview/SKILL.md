---
name: persistent-image-preview
description: Use after generating, editing, exporting, or selecting an image when the user wants it opened or local workflow defaults require a persistent visible preview; preserves the image at a stable project path and launches a detached desktop viewer that survives the agent command.
---

# Persistent Image Preview

## Core Rule

When an image is generated or edited, a chat-rendered preview is not a persistent
local preview. Preserve the selected result at a stable project path and open it
in a detached desktop viewer before declaring the task complete.

Use this default sequence:

1. Keep the original generated file in place.
2. Copy the selected result to the requested output path. If none was given, use
   a descriptive path such as `artifacts/images/<name>.png` in the active
   project.
3. Verify that the destination exists, is non-empty, and has an image MIME type.
4. Inspect the result visually when correctness matters.
5. Launch the persistent viewer helper:

```bash
skills/persistent-image-preview/scripts/open_image_persistent.sh \
  artifacts/images/example.png
```

The helper uses `nohup` and `setsid`, records the last opened image, and keeps
the viewer independent of the invoking shell. Do not substitute a temporary
terminal-bound viewer process.

## Display Selection

The helper uses an explicit `--display` first. Without that flag it prefers the
current non-Xvfb desktop session and never falls back to a noVNC/Xvfb display.
This prevents a virtual-desktop image viewer from capturing later desktop file
opens through the shared D-Bus session. EOG is launched with a new instance for
the same reason. Pass an explicit display only when the preview is intentionally
part of a dedicated virtual desktop:

```bash
skills/persistent-image-preview/scripts/open_image_persistent.sh \
  --display :98 artifacts/images/example.png
```

Use `--viewer APP` only when a specific installed viewer is required. Otherwise
allow the helper to choose an available image viewer or `xdg-open`.

## Completion Evidence

Confirm all of the following:

- the stable project image exists and is non-empty;
- visual inspection shows the requested content;
- the helper exits successfully and records its state;
- the image remains open after the launch command returns.

If no graphical display or viewer is available, report that exact blocker. Do
not claim the image was opened merely because it appeared in chat.
