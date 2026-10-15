---
name: asg
description: Use this skill to convert asciinema/asciicast v3 terminal recordings into animated or static SVGs with ASG. Trigger it when a user wants to install or invoke ASG, render a .cast or .cast.zst file, create a README terminal demo, choose window, theme, timing, playback, font, or geometry options, validate generated SVG output, or troubleshoot ASG, npm/WASI, sharpness, font, and playback problems. Do not use it for recording terminal sessions or editing unrelated SVG files.
---

# Render Terminal SVGs with ASG

Use ASG for asciicast v3-to-SVG work. Preserve the recording unless the user explicitly asks to trim, resize, restyle, or replace an existing output.

## Workflow

### 1. Establish the input and output

- Accept a local `.cast`, zstd-compressed `.cast.zst`, stdin (`-`), HTTP(S) URL, or asciinema.org recording ID.
- Choose an explicit `.svg` output path unless the user requests stdout.
- Check before overwriting an unrelated existing file. Regenerating a named demo is an intentional overwrite.
- Let ASG validate the input instead of guessing from the extension. ASG accepts asciicast v3 only.

If ASG reports a v1 or v2 recording, migrate it first only with the user's approval:

```bash
asciinema convert old.cast recording-v3.cast
```

### 2. Choose one runner

Prefer an existing native installation after checking `asg --version`:

```bash
asg input.cast output.svg
```

If `asg` is unavailable and Node.js 22 or newer is available, use the npm/WASI package without installing it globally:

```bash
npx --yes @kingsword/asg@latest input.cast output.svg
```

For repeated use, install exactly one distribution:

```bash
npm install -g @kingsword/asg
# or
cargo install asg --locked
```

Use `@latest` for normal one-off work. Pin a package version only when the surrounding project requires reproducible tooling.

### 3. Render for the destination

Use window decorations for documentation and product demos:

```bash
asg input.cast output.svg --window
```

Render a static frame or a focused excerpt when the full recording is unnecessary:

```bash
asg input.cast still.svg --at 4.5 --window
asg input.cast excerpt.svg --from 3 --to 12 --window
```

Do not add `--from 0.1` automatically. Add it when a README or image proxy freezes on an intentionally blank first frame, then verify that no meaningful opening content was removed.

Read [the CLI reference](references/cli.md) before using non-default timing, playback, theme, font, padding, or geometry options, and when diagnosing a failed conversion.

### 4. Validate the result

1. Confirm the command exits successfully and note ASG's reported bytes, frame count, duration, and cell geometry.
2. Confirm the output exists, is non-empty, and parses as XML. Use `xmllint --noout output.svg` when available; otherwise use a structured XML parser from the environment.
3. Render or open the SVG at its intended display size. For animations, inspect the opening state and at least one later state.
4. For a README, reference the committed SVG by a relative path when possible:

   ```markdown
   ![Terminal demo](path/to/demo.svg)
   ```

5. Report the exact command, output path, conversion metrics, and validation performed.

## Guardrails

- Use `--window`, not `--windows`.
- Do not hand-edit generated SVG internals; change the command or source cast and regenerate.
- Do not claim pixel-identical text across devices. SVG text uses fonts available on the viewer's system.
- Keep the SVG's aspect ratio when embedding it. Avoid rasterizing it merely to resize it.
- If identical pixels on every device matter more than vector scaling, explain that a raster renderer such as `agg` is a better fit.
- If a host disables SVG CSS animation, provide a static frame with `--at` or use a host that serves the SVG as an image.
- Treat URLs and asciinema.org IDs as network operations and respect the environment's network policy.
