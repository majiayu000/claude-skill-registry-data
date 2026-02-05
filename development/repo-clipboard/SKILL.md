---
name: repo-clipboard
description: Snapshot the current directory into pseudo-XML for LLM context. Use when you need to share a repo (or a sub-tree) with Codex/LLMs, especially for code review/debugging, generating an agent-friendly “repo snapshot”, or piping context into tools like `llm` (see skill $llm-cli). Supports `.gitignore`-aware file discovery, common ignore patterns, extension filtering, regex include/exclude, optional file-list printing, line-range snippets, and writes `/tmp/repo_clipboard.{stdout,stderr}` for reuse.
---

# repo-clipboard

## Quick start

- Snapshot the current directory to stdout (for piping), while writing `/tmp/repo_clipboard.stdout` and metadata to stderr:
  - `scripts/repo_clipboard --llm -e py,md,yml --print-files`
- Copy the snapshot to the Windows clipboard (WSL) and also write `/tmp/repo_clipboard.stdout`:
  - `scripts/repo_clipboard -e py,md,yml`

## Snippets (token-efficient context)

- Include only specific line ranges:
  - `scripts/repo_clipboard --llm -e md --snippet README.md:5-25 --snippets-only`

## Reference

- For full CLI usage, examples, and flag semantics, read `repo-clipboard/references/usage.md`.

## LLM review loop (with `llm`; see skill $llm-cli)

- Default intelligence picks:
  - `wbg:claude-opus-4.5`
  - `wbg:gpt-5.2-xhigh` (very slow; reserve for the hardest reviews)
- Large-context pick (when the repo snapshot is huge):
  - `wbg-gemini-3-pro-preview`
