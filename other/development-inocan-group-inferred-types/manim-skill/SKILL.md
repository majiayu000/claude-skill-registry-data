---
name: manim-skill
description: Render Manim scenes to still frames and review them to diagnose animation/layout issues. Use when debugging scenes, verifying visual correctness, or inspecting frame-by-frame output.
---

# Manim Frame Review

Render a Manim scene to PNG frames, inspect them visually, and iterate quickly.

## Workflow

### 1. Render frames

Use the helper script to clear stale frames and re-render in one step:

```bash
python3 scripts/refresh_frames.py [--fps FPS] [--contact-sheet] <file.py> <SceneName>
```

- `--fps FPS`: Frames per second (default: 2). Increase for fast-paced animations.
- `--contact-sheet`: Generate a contact sheet (4x4 grid with evenly sampled frames) after rendering.

Or render manually:

```bash
manim -ql --fps 2 --format=png --silent <file>.py <SceneName> | tail -n 5
```

Frames are written to `media/images/<file>/`.

### 2. Inspect frames

For a quick overview, use `--contact-sheet` when rendering, producing `/media/images/<file>/<SceneName>_sheet.png`. **Always read the contact sheet first** to get an overview of the animation progression. Then **read at least one full-size frame** (e.g., the first, middle, or a frame showing a key transition) to verify details at full resolution. To regenerate a contact sheet without re-rendering:

```bash
python3 scripts/make_contact_sheet.py <frames_directory> --scene-name <SceneName>
```

Alternatively, read frame images directly for visual inspection. Check early, middle, and late frames plus key transitions to catch overlaps, cropping, or timing issues.

For fast-paced and detailed animations, it may be necessary to increase `--fps` to capture more frames, for example `--fps 4` or `--fps 8`. For example, if you were previously inspecting frames 0005 and 0006 at fps 2 and need to know what happens in-between, at fps 4 you would inspect frames 0010 and 0012 instead and have a new frame 0011 in between.

### 3. Iterate

Fix issues in the scene code, then repeat steps 1-2 until correct.

### 4. Render video

When the user wants the full video:

```bash
manim -ql <file>.py <SceneName>
```

Key render options:
- `-q [l|m|h|p|k]`: Quality (l: 854x480@15fps, m: 1280x720@30fps, h: 1920x1080@60fps)
- `--format [png|gif|mp4|webm|mov]`: Output format (default: mp4)
- `-r W,H`: Custom resolution
- `--enable_gui`: Enable GUI interaction (use when explicitly requested)

## References

Search `references/manim-docs/` recursively for Manim documentation (tutorials, guides, reference, FAQ).
