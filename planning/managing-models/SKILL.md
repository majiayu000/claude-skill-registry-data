---
name: managing-models
description: Sanctioned model download path. Reads policies/model_sources.yaml, downloads via huggingface_hub or direct URL with sha256 verification, places the file under the correct ComfyUI models folder. DEFERRED-ACTIVATION — gated behind user setting `allow_model_download` (default false). Never auto-invoked by the planner.
v1_2_match:
  kinds: [model_download]
  capability: managing-models
v1_2_output: model_handle
deferred_activation: true
gate_setting: allow_model_download
---

# managing-models

Planning-category skill (v1.2 slots 6.7 + 8.9). Scripts:

- `scripts/download.py` — stdin `{"capability": str, "file": str, "repo": str, "sha256": str}`,
  stdout a `ModelHandle` JSON when the download succeeds + verifies, else a
  structured error envelope.

## Activation gate

This Skill is **dormant by default**. The planner may emit a
`model_download` sub-goal but the executor refuses to dispatch unless
the user has set `allow_model_download = true` in their host settings.
This is per the iron-law clause in CLAUDE.md: model weight downloads
are a halt point, not a silent action.

## CLAUDE.md compliance

- §12 #3 — every download is keyed to a `model_sources.yaml` entry.
  No "guess the URL" path.
- §12 #8 — sha256 mismatch raises a loud error envelope; never silently
  proceeds.
- Iron-law — never installs software on the user's machine without
  explicit gate.
