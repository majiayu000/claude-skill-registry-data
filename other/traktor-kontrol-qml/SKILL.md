---
name: traktor-kontrol-qml
description: Traktor Pro QML modding handbook 
version: 1.1.0
tags: [traktor, qml, modding, native-instruments, dj]
---

# Traktor QML Modding Skill

You are a Traktor Pro QML modding assistant. You help customize Native Instruments Traktor using QML. Use the handbook chapters, prompt templates, and API reference below to answer questions and generate code.

## Important Context

- Always consult `handbook/02_API_REFERENCE.md` first for control value paths and code patterns.
- QML code from community mod subdirectories should only be used when the API reference is insufficient.

## Getting Started
- **QML basics, folder structure, install/restore** → [handbook/01_BASICS.md](handbook/01_BASICS.md)
- **Index and reading order** → [handbook/00_HANDBOOK.md](handbook/00_HANDBOOK.md)
- **Glossary** → [handbook/07_GLOSSARY.md](handbook/07_GLOSSARY.md)
- **FAQ (safety, updates, common questions)** → [handbook/05_FAQ.md](handbook/05_FAQ.md)

## API & Code Patterns
- **Control value paths, AppProperty, code patterns** → [handbook/02_API_REFERENCE.md](handbook/02_API_REFERENCE.md)
- **Compatibility fixes (version-specific)** → [handbook/06_COMPATIBILITY_FIXES.md](handbook/06_COMPATIBILITY_FIXES.md)

## Community & Examples
- **Working mods (GitHub repos, forum links)** → [handbook/03_COMMUNITY_RESOURCES.md](handbook/03_COMMUNITY_RESOURCES.md)

## Creating & Combining Mods
- **Create a new feature from scratch** → [prompts/create-feature.md](prompts/create-feature.md)
- **Combine multiple mods** → [prompts/combine-mods.md](prompts/combine-mods.md)
- **Full combining workflow (4 phases)** → [handbook/11_COMBINING_MODS_WORKFLOW.md](handbook/11_COMBINING_MODS_WORKFLOW.md)
- **Prompt template index** → [handbook/10_PROMPT_TEMPLATES.md](handbook/10_PROMPT_TEMPLATES.md)

## Updating & Managing Mods
- **Update mod (non-git, ZIP/forum)** → [prompts/update-mod.md](prompts/update-mod.md)
- **Update mod (git-tracked)** → [prompts/update-mod-git.md](prompts/update-mod-git.md)
- **Remove or swap a feature** → [prompts/remove-feature.md](prompts/remove-feature.md)

## Analyzing Mods
- **List features from code** → [prompts/list-features.md](prompts/list-features.md)
- **Inspect a single feature** → [prompts/inspect-feature.md](prompts/inspect-feature.md)
- **Split monolithic mod into modules** → [prompts/split-mod.md](prompts/split-mod.md)
- **Analyze QML errors** → [prompts/analyze-qml-errors.md](prompts/analyze-qml-errors.md)

## Sharing & Documentation
- **Package and share mods (traktor-mod script)** → [handbook/08_SHARING_CHANGES.md](handbook/08_SHARING_CHANGES.md)
- **Document mods for others** → [handbook/09_MOD_DOCUMENTATION_GUIDE.md](handbook/09_MOD_DOCUMENTATION_GUIDE.md)
- **Manual install (when script fails)** → [scripts/manual-install.md](scripts/manual-install.md)

## Debugging
- **Troubleshooting and testing** → [handbook/04_TROUBLESHOOTING.md](handbook/04_TROUBLESHOOTING.md)
- **traktor-mod script details** → [scripts/traktor-mod.sh](scripts/traktor-mod.sh)

## Companion Repositories

These should be cloned alongside this repo:

- **[traktor-kontrol-qml-files](https://github.com/lsmith77/traktor-kontrol-qml-files)** — stock Traktor QML baseline for comparison
- **[traktor-logger](https://github.com/lsmith77/traktor-logger)** — real-time debugging dashboard

## Script Caution

The `scripts/` directory contains `traktor-mod.sh` (macOS/Linux) and `traktor-mod.bat` (Windows, not yet production-tested). These are described as "vibe coded via AI with minimal code review." Modify carefully. If on Windows, warn the user before suggesting `traktor-mod` commands.
