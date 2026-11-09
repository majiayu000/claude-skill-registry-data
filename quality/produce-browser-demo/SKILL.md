---
name: produce-browser-demo
description: Create a polished, verifiable demo video from local browser captures and an explicit choreography manifest. Use when a product walkthrough, interaction proof, or visual handoff needs controlled cursor, framing, timing, and media verification without recording private desktop content.
engines: [AGNOSTIC]
---

# Produce Browser Demo

## When to use

- Turning approved screenshots into a browser-style walkthrough.
- Re-rendering a demo with deterministic timing and framing.
- Producing review media without using a native screen recorder.

## Workflow

1. Collect local source frames and a manifest describing order, duration, pointer position, click cues, and optional framing changes.
2. Validate that every source path stays inside the intended input directory.
3. Render with `commands/render-browser-demo.sh`; require an existing media encoder rather than installing one.
4. Keep cursor motion deliberate, readable, and subordinate to the product behavior.
5. Inspect representative frames and verify output duration, dimensions, frame rate, and decode health.
6. Report source manifest and verification evidence.

## Output

- A local video file and resolved render manifest.
- Media-probe results and representative frame checks.
- Known limitations such as missing live input or audio.

## Guardrails

- Do not record microphones, cameras, native windows, notifications, or unrelated desktop content.
- Do not download remote media during rendering.
- Do not claim an assembled demo proves live application behavior.
