---
name: aetherbrowser-huggingface-nav
description: "Navigate Hugging Face models, datasets, and spaces through AetherBrowser for research, validation, and publishing workflows. Use when inspecting repo cards, files, docs, and leaderboard surfaces in browser mode."
---

# AetherBrowser Hugging Face Nav

## Workflow

1. Route to CLI-side research lane.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain huggingface.co --task navigate --engine playwriter`

2. Open target repository.
- User: `https://huggingface.co/<user>`
- Model: `https://huggingface.co/<user>/<model>`
- Dataset: `https://huggingface.co/datasets/<user>/<dataset>`
- Space: `https://huggingface.co/spaces/<user>/<space>`

3. Verify and capture context.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title`
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot`

4. Hand off to CLI/API as needed.
- Use `hf` CLI for uploads/downloads after browser discovery.

## Rules

- Use browser flow for discovery and validation.
- Use API/CLI flow for repeatable state changes.
- Preserve evidence in lane logs for reproducibility.
