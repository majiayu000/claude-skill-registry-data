---
name: preflight
description: Use BEFORE implementing code in a project set up with this kit — loads the language rules for detected manifests, the project's CLAUDE.md, and the active task's prior handoff annotations. Replaces the heavy context that would otherwise be re-injected on every prompt. Trigger when the user says "preflight", "load the rules", "ground yourself", or before starting a fresh implementation session.
---

# Preflight — load rules and grounding context

You are preparing to implement code. Load the project's rules and grounding context so you have the right constraints in mind. This replaces the heavy context that would otherwise be injected on every prompt.

## 1. Detect active languages and load rules

Check for project manifests and load the corresponding rule files:

| Manifest | Language | Rule file |
|----------|----------|-----------|
| `package.json` | JavaScript (+ React if a dep) | `.claude/rules/languages/javascript.md` (+ `javascript-react.md`) |
| `tsconfig.json` | TypeScript (+ React if a dep) | `.claude/rules/languages/typescript.md` (+ `typescript-react.md`) |
| `pyproject.toml` / `requirements.txt` | Python | `.claude/rules/languages/python.md` |

Only read rule files for languages actually detected in this project. `shell.md` has no manifest to detect — load it when editing shell scripts (`*.sh`).

Also read `.claude/rules/quality.md` and `.claude/rules/rigor.md` — these apply regardless of language.

## 2. Read project-specific and task context

Read `CLAUDE.md` if present, for project-specific conventions.

Read the active task's prior handoff annotations so a resuming agent picks up where the last one left off:

```bash
task project:<repo> +ACTIVE list
task <id> information
```

## 3. Scan project tree

Build spatial awareness of the project (max depth 3, max 50 entries):

```bash
ls -R --max-depth=3 | head -50
```

## 4. Check dependency versions

Read the primary manifest file (e.g., `package.json`, `pyproject.toml`) to ground yourself on actual dependency versions. Do not guess versions.

## 5. Print summary

Print a brief summary of what was loaded:

```
Preflight loaded:
  - Language rules: TypeScript, TypeScript-React
  - Quality and rigor rules
  - CLAUDE.md read
  - Active task handoff read
  - Project tree scanned (N entries)
  - Dependencies: package.json (N deps)
```

You are now grounded. Proceed with implementation.
