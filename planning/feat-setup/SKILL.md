---
name: feat-setup
description: >
  Use when the user wants the project instructions file generated or updated from the detected
  stack and conventions — 'gerar o arquivo de instruções do projeto', 'criar convenções do
  projeto', 'setup governance', 'gerar AGENTS'. Writes the shared instructions file read by
  Claude Code, Codex, Hermes and OpenCode. Do NOT use to analyze the codebase in depth
  (feat-map) or to initialize the workspace (feat-init).
metadata:
  version: 3.2.1
---

# Generate the project instructions file

Which files each runtime reads, and the write rules, are in `references/project-files.md` —
read it first. The canonical content comes from `templates/AGENTS.template.md`.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Check existing** — for each instructions file named in `references/project-files.md`,
   report whether it exists and show its first 20 lines. Existing content → ask: update (merge
   sections), replace, or skip. Never overwrite silently.
3. **Gather context** — `.planning/feat/codebase.md` and `.planning/feat/context/*.md` when
   present (suggest `feat-map` first when absent), otherwise a quick read-only
   `python3 "<plugin-root>/scripts/feat_map.py" --repo-root .`.
4. **Ask (1 round max)** only what cannot be detected: what the project is (1 sentence) and any
   specific rules ("use defaults" is fine).
5. **Write** the canonical file from the template with real values — commands from
   `context/testing.md`, conventions from `context/conventions.md`. Then make Claude Code load
   the same rules as `references/project-files.md` prescribes (a one-line import file when it
   does not exist yet).
6. **Present** the sections written (Identity, Stack, Architecture, Conventions, Commands,
   Quality, Security, Golden Rules), the files created or updated, and next:
   `feat-feature "description"`.

## Prohibitions

- Never overwrite an existing instructions file without asking.
- Never invent conventions — detect them or ask.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
