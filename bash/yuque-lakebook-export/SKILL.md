---
name: yuque-lakebook-export
description: Use when exporting Yuque or .lakebook content to local Markdown for Obsidian migration or cleanup.
license: MIT
---

# Yuque Lakebook Export

## Overview

Convert Yuque knowledge bases, Yuque documents, or `.lakebook` files into local Markdown folders prepared for Obsidian. The workflow supports single or batch exports and cleanup for common migration issues such as missing images, cropped image mismatches, broken internal links, wrong folder hierarchy, and Markdown table rendering problems.

## When to Use

Use this skill when the user asks for:

- Exporting one or more Yuque `.lakebook` files
- Converting a Yuque knowledge base into Markdown
- Migrating Yuque content into Obsidian
- Fixing Yuque export issues around images, cropped images, internal links, hierarchy, or tables

## Do not use

Do not use this skill for:

- Generic Markdown editing that does not involve Yuque or `.lakebook`
- Website scraping tasks
- Export tasks that already come from a non-Yuque format

## Instructions

1. Prefer non-interactive execution so the agent can run deterministically.
2. Before any non-interactive export, the agent must confirm the output root directory with the user. Do not choose an output directory on the user's behalf.
3. If the user has not provided an output directory, ask a concise question and wait for the user's answer before running the export command.
4. Prefer `uv` consistently. Do not create temporary `.venv` or similar task-local environments in the working directory.
5. Before running any `uv` command, first check whether `uv` is available in the environment.
6. If `uv` is not installed or not available in `PATH`, the agent must ask the user for confirmation before installing `uv`. Do not install it silently.
7. Before running `uv sync` or `uv run python scripts/cli.py ...`, the agent must first switch into the installed skill tool directory, meaning the directory that contains this `SKILL.md`, `pyproject.toml`, `uv.lock`, and `scripts/`. Do not run these commands directly from the `.lakebook` source directory, the output directory, or the user's current workspace root.
8. Use this entrypoint for agent execution:

```bash
uv run python scripts/cli.py
```

9. Sync dependencies before first use:

```bash
uv sync
```

10. Recommended command order:

```bash
cd /path/to/installed-skill-root
uv sync
uv run python scripts/cli.py ...
```

11. Standard single-file execution:

```bash
uv run python scripts/cli.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

12. Standard batch execution:

```bash
uv run python scripts/cli.py -l "/path/to/your_file_1.lakebook" "/path/to/your_file_2.lakebook" -o "/target/root"
```

13. Although `scripts/cli.py` still supports interactive terminal selection for manual human use, agents must not rely on interactive mode because they cannot reliably capture terminal interaction state. Always pass explicit `-l` and `-o` arguments.
14. Do not manually create temporary virtual environments in the current working directory, the user's download directory, or any task directory; dependencies should be managed by `uv` from the skill tool directory.
15. Some Yuque exports include `<!doctype lake>` at the start of the document body; older implementations could render this as a stray `lake##` prefix in Markdown. The current skill implementation already handles this case.
16. After export, verify:
- `.md` files exist
- sibling `.assets` folders exist
- internal links are relative Markdown paths
- images render in Obsidian
- exported documents do not start with an erroneous `lake##` prefix

17. If export fails, inspect the batch log written next to the input `.lakebook` files.

For detailed behavior, troubleshooting, and output rules, read `references/usage.md`.
