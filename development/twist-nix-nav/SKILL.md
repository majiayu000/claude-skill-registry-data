---
name: twist-nix-nav
description: Navigate a local emacs-twist/twist.nix checkout and point to relevant files for questions about twist.nix configuration, flake outputs, library functions, Home Manager integration, package build flow, or tests. Use when a user asks where something is defined or how twist.nix is wired and the answer should reference code rather than reproduce it. Ask for the repo path if it is not available.
---

# Twist Nix Navigation

## Overview

Provide file-level guidance for twist.nix questions and direct the user to inspect code. Keep outputs short, avoid copying code or long excerpts, and ask for the local repo path when needed.

## Workflow

1. Locate the local checkout. Ask the user for the twist.nix repo path if unknown.
2. Map the question to files using `references/twist-nix-nav.md`.
3. Open the relevant files and point to identifiers or sections by name.
4. Summarize at a high level and tell the user to read the code for details.
5. If the user asks for code reproduction or distribution, remind them that twist.nix is GPLv3 and avoid copying unless they accept GPL terms.

## Answer Style

- Use absolute or workspace-relative paths when referencing files.
- Prefer navigation cues over quoted code.
- Suggest `rg -n "identifier" <repo>` to locate definitions.

## References

Read `references/twist-nix-nav.md` for the file map and common entry points.
