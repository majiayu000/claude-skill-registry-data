---
name: response-state-visualizer
description: Stream safe, staged previews of answers in CLI output. Use when you need to show how a response forms or changes state without exposing chain-of-thought.
---

# Response State Visualizer

Use this skill to show intent, plan signals, and draft previews while the answer is forming.

## Workflow

1) Enable the preview stream with `GPIA_RESPONSE_PREVIEW=1`.
2) Emit stages like Intent, Keywords, Skills, Draft, Final.
3) Keep previews short and safe (no hidden reasoning traces).

## Script

- Run: python skills/dialogue/response-state-visualizer/scripts/demo_preview.py
