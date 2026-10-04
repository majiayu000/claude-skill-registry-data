---
name: vscode-agent
description: Reference system prompt and tool schemas for VSCode Agent. Use when imitating, comparing, or analyzing VSCode Agent's prompting style; designing prompts inspired by VSCode Agent; or answering questions about how VSCode Agent is prompted.
---

# VSCode Agent

GitHub Copilot Chat / VSCode Agent system prompts across multiple models (GPT-4o/4.1/5/5-mini, Claude Sonnet 4, Gemini 2.5 Pro).

When activated, read the bundled source files below to ground your response
in the actual published prompt text. Do not paraphrase from memory — the
canonical content lives in these files.

## Source files

- `sources/Prompt.txt` (21,032 bytes)
- `sources/chat-titles.txt` (765 bytes)
- `sources/claude-sonnet-4.txt` (9,910 bytes)
- `sources/gemini-2.5-pro.txt` (9,909 bytes)
- `sources/gpt-4.1.txt` (11,082 bytes)
- `sources/gpt-4o.txt` (7,876 bytes)
- `sources/gpt-5-mini.txt` (25,257 bytes)
- `sources/gpt-5.txt` (25,579 bytes)
- `sources/nes-tab-completion.txt` (8,910 bytes)

## Usage

- Quote or summarise from the files above when answering "how does VSCode Agent prompt its agent?" style questions.
- When emulating VSCode Agent's style, mirror its structure (sections, tool-use rules, refusal patterns) rather than copying verbatim.
- These prompts were collected by the upstream `x1xhlol/system-prompts-and-models-of-ai-tools` repo and may drift from the live product over time.
