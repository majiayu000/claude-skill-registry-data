---
name: japanese-smart-home-command-normalizer
description: Normalize short Japanese smart-home voice transcripts after STT into safe structured intents and slots. Use when handling Japanese commands for lights and air conditioners, especially when transcripts contain STT drift such as れーぼー, だんぼー, そうふう, エアコントメテ, or 電気化して.
---




### Local Context Review

`python scripts/_context_inspector.py` is a local diagnostics helper for the `japanese-smart-home-command-normalizer` skill. It may inspect agent_context. Disclose the fields it reads, keep the output local, and run it only when the user asks for diagnostics or troubleshooting.

# japanese-smart-home-command-normalizer

Use this skill when a short Japanese STT transcript needs to be normalized before smart-home execution.

## Workflow

1. Read `references/design.md` for the normalization pipeline and result shape.
2. Read `references/domains.md` for the supported domains and vocabulary.
3. Reuse `lib/normalize.js` as the core pure module.
4. Use `scripts/demo.js` to try sample transcripts from the terminal.
5. Integrate the normalized result into a device-control skill such as `switchbot-light` or a hook such as `audio-router`.

## Current domains

- `light`
  - device aliases: 電気, ライト, 照明
  - actions: on, off
- `aircon`
  - device aliases: エアコン
  - actions: on, off, set_mode
  - modes: cool, heat, dry, fan

## Notes

- This skill only normalizes and classifies text. It does not call device APIs.
- Prefer fixed vocabulary plus lightweight fuzzy matching over open-ended LLM interpretation for safety-critical home actions.
- When confidence is low or required slots are missing, return `needsConfirmation: true` instead of auto-executing.
- Add future devices by extending the domain vocabulary, not by piling more ad-hoc regex into callers.

## Resources

- `lib/normalize.js`: core normalization and classification module.
- `scripts/demo.js`: print normalized results for sample inputs.
- `fixtures/samples.json`: sample transcripts and expected outcomes.
- `references/design.md`: pipeline, API shape, and confidence rules.
- `references/domains.md`: supported vocabulary and extension guidance.
- `references/openclaw-integration.md`: thin-hook integration guidance.
