---
name: aiwf-gradio-coding
description: Use for Gradio Blocks, Interface, events, queueing, FastAPI mounting, auth, and local UI smoke validation.
---

# AIWF Gradio Coding

## Core Rule

Treat Gradio as both Python callback code and a live UI contract. Inspect Gradio version, `Blocks` or `Interface` structure, queueing, state, FastAPI mounting, auth, launch settings, and model/runtime cost before changing callbacks or components.

## Workflow

1. Inspect imports, app entrypoint, `Blocks`/`Interface` layout, event chains, state objects, queue settings, launch/mount code, tests, and deployment scripts.
2. Confirm whether the app is standalone Gradio, mounted into FastAPI, embedded in AIWF Studio, or a Hugging Face Space.
3. Patch callback signatures and component inputs/outputs together. Keep return shapes aligned with component expectations.
4. Avoid VRAM-heavy generation, large downloads, or public sharing links unless Shawn explicitly asks.
5. Validate with import/compile checks, callback unit tests when possible, and local UI smoke or screenshot for visible changes.

## Gradio Guardrails

- Prefer `Blocks` for multi-step apps, tabs, state, or custom layouts. Keep `Interface` for simple single-function demos.
- Keep queueing, concurrency, cancellation, and progress behavior explicit for model calls.
- When mounted in FastAPI, verify `root_path`, auth dependencies, static paths, and route conflicts.
- Do not treat Gradio auth as a full production security boundary without additional review. Add `aiwf-security-guardrails` for exposed apps.
- Add `aiwf-avoid-ai-design` for default Gradio styling, AI-looking layout, teal-heavy palettes, or public-facing visual polish.
- Preserve accessibility labels and visible error states.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
python -m compileall <package-or-file>
python -m pytest
python -c "import gradio as gr; print(gr.__version__)"
```

When launching, bind locally by default and stop the server before finalizing:

```powershell
python <app-entrypoint>
```

## Primary Source Anchors

- Gradio Blocks documentation: https://www.gradio.app/docs/gradio/blocks
- Gradio Interface documentation: https://www.gradio.app/docs/gradio/interface
- Gradio FastAPI mounting: https://www.gradio.app/docs/gradio/mount_gradio_app

Verify the installed Gradio version before using newer component, event, queue, or mount behavior.
