---
name: oss-agent-prompts
description: Reference system prompt and tool schemas for Open Source Agents. Use when imitating, comparing, or analyzing Open Source Agents's prompting style; designing prompts inspired by Open Source Agents; or answering questions about how Open Source Agents is prompted.
---

# Open Source Agents

System prompts for open-source coding agents: Cline, Bolt, RooCode, Codex CLI, Gemini CLI, Lumo.

When activated, read the bundled source files below to ground your response
in the actual published prompt text. Do not paraphrase from memory — the
canonical content lives in these files.

## Source files

- `sources/Bolt/Prompt.txt` (21,945 bytes)
- `sources/Cline/Prompt.txt` (47,083 bytes)
- `sources/Codex CLI/Prompt.txt` (4,848 bytes)
- `sources/Codex CLI/openai-codex-cli-system-prompt-20250820.txt` (23,864 bytes)
- `sources/Gemini CLI/google-gemini-cli-system-prompt.txt` (18,976 bytes)
- `sources/Lumo/Prompt.txt` (8,253 bytes)
- `sources/RooCode/Prompt.txt` (43,961 bytes)

## Usage

- Quote or summarise from the files above when answering "how does Open Source Agents prompt its agent?" style questions.
- When emulating Open Source Agents's style, mirror its structure (sections, tool-use rules, refusal patterns) rather than copying verbatim.
- These prompts were collected by the upstream `x1xhlol/system-prompts-and-models-of-ai-tools` repo and may drift from the live product over time.
