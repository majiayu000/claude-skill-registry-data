---
name: update-readme
description: Keep all README files aligned with the current codebase by rewriting setup steps, removing outdated content, and syncing documentation to the latest repository state whenever asked to update, refresh, or sync READMEs.
---

# Update README

## Goals

- Keep every README in the repo accurate for the current codebase.
- Ensure README explains the nix directory layout for common packages/settings and host-specific configuration placement.
- Remove outdated or no-longer-true statements.
- Write in concise English.

## Workflow

1) Discover README targets

- List README files with `rg --files -g 'README*'` from the repo root.
- Only the top-level `README.md` is permitted; subdirectory READMEs are not allowed.
- If any subdirectory README files exist, remove them and consolidate their content into the top-level README.

2) Determine scope for the README

- The top-level `README.md` must be the only README in the repo.
- Use the filesystem to confirm what exists before writing.

3) Rewrite the README

- Keep content minimal; include `## Setup` and `## Nix layout`.
- `## Setup`
  - Describe the exact setup steps required now.
  - Include copy-pasteable commands in Markdown code blocks so the setup can be executed directly.
  - Remove deprecated steps or tooling references.
- `## Nix layout`
  - Explain where common packages/settings live and where host-specific configuration lives inside `nix/`.
  - Use short sentences or bullets; avoid excessive detail.

4) Remove obsolete content

- Delete any badges, deprecated sections, or instructions that are no longer true.
- If a section cannot be substantiated from current files, remove it.

## Output expectations

- English only.
- No extra sections beyond the required two.
- For the root README, never mention deprecated folders (like `init/`) or non-active folders unless instructed.
- Only `README.md` at repo root may exist; delete any others.

## Notes

- This repo treats `git/`, `nvim/`, `wezterm/`, and `zsh/` as the active configuration roots.
- If a README claims to manage files or scripts that no longer exist, remove those claims.
