---
name: codebase-audit
description: Audit and map a codebase to understand structure, dependencies, and risks. Use when the user asks to audit a repo, understand architecture, or assess codebase quality or health.
---

# Codebase Audit

## Overview
Create a fast, evidence-based map of the repo and highlight risk and quality hotspots.

## Inventory
1. List top-level structure (use `ls`, `tree -L 3`, `rg --files`).
2. Identify entry points (search for `main`, CLI, or service starts).
3. Capture dependency manifests (pyproject, package.json, requirements, go.mod).

## Required Tool Pass (must run all tools)
Run every tool below and log its output. If any tool is missing, invoke action-gate to install it and block the audit until the full tool pass is complete.
- Use OS-appropriate installers via action-gate (apt/dnf/yum/pacman/brew/choco/scoop) and retry.
- `rg` for search and inventory.
- `tree -L 3` for structure.
- `tokei` (or `scc` or `cloc`) for LOC; choose one and run it.
- `ctags` or a tree-sitter indexer for symbol maps; choose one and run it.
- `git log --stat` for hotspots (if repo has history).
- `repomap` for a scoped module summary (install if missing).
- `repomix` for a full-repo map with ignores applied (install if missing).
- Jina embeddings tooling for semantic clustering or duplication hints (install/configure if missing). If API key is required, stop and request it.

## Repomap Scope Rules (required)
- Do not run repomap on the full repo if it times out; run it on scoped code folders (`scripts/`, `skills/`, and other non-JS/JSX code dirs).
- If repomap throws tree-sitter query errors for JS/JSX, skip those folders and rely on `ctags` for symbol mapping.
- If a target folder lacks `.gitignore`, create a minimal `.gitignore` in that folder before running repomap.

## Repomix Rules (required)
- Use repomix for the full-repo map and ensure `node_modules/` and large data dirs are ignored.
- Prefer a local `repomix.config.json` or `.repomixignore` if present; otherwise, generate one (`repomix --init`) and add ignore patterns.
- Record the output file path and style used (markdown/json/plain).

## Long-Run Handling
- If a tool is slow, use `timeout` or run under `tmux`/`nohup` to avoid session loss. Do not treat this as a fix for tool errors.

## Risk and Quality Checks
- Large files, high churn areas, and untested modules.
- Security and PII paths, data flow, and external integrations.
- Configuration, environment assumptions, and hidden dependencies.

## Output
- Module map, key flows, and hotspots.
- Findings with severity and suggested next steps.
- Open questions to confirm architecture or intent.
- Note which tools were run vs unavailable.

## Acceptance Criteria
- Full tool pass completed with outputs captured.
- Any missing tool is reported and blocks the audit until resolved.
- Environment-specific install commands are documented when blockers occur.
- Repomap outputs are produced for scoped folders, and repomix output is produced for the full repo.
