---
name: amp
description: Reference system prompt and tool schemas for Amp. Use when imitating, comparing, or analyzing Amp's prompting style; designing prompts inspired by Amp; or answering questions about how Amp is prompted.
---

# Amp

Sourcegraph Amp coding agent.

When activated, read the bundled source files below to ground your response
in the actual published prompt text. Do not paraphrase from memory — the
canonical content lives in these files.

## Source files

- `sources/README.md` (614 bytes)
- `sources/claude-4-sonnet.yaml` (66,230 bytes)
- `sources/gpt-5.yaml` (62,239 bytes)

## Usage

- Quote or summarise from the files above when answering "how does Amp prompt its agent?" style questions.
- When emulating Amp's style, mirror its structure (sections, tool-use rules, refusal patterns) rather than copying verbatim.
- These prompts were collected by the upstream `x1xhlol/system-prompts-and-models-of-ai-tools` repo and may drift from the live product over time.
