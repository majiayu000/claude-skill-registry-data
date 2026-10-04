---
name: agent-instructions
description: >
  Use whenever creating OR editing CLAUDE.md, AGENTS.md, GEMINI.md, a SKILL.md, or any
  other file whose job is to instruct an AI coding agent, at any scope level (user/global,
  project root, parent folder, subdirectory, or a skill/runbook in a plugin repo). Covers
  scope diagnosis, content taxonomy, multi-tool compatibility for Claude Code, Codex, Gemini
  CLI, and OpenCode, cookbook templates for Python, TypeScript, monorepo, agent/MCP, and
  minimal projects, and the RED-GREEN editing discipline for revising instructions/skills/
  runbooks that already exist. Invoke when the user asks to "create a CLAUDE.md", "set up
  Claude for this project", "what should go in my AGENTS.md", "write agent instructions",
  "help me set up my global Claude configuration", "edit this skill", "update this runbook",
  "add a rule to AGENTS.md", or any similar request — even without explicit mention of
  CLAUDE.md or AGENTS.md. If the user is starting a new project or onboarding into an
  existing one and no instruction file exists, proactively suggest creating one.
metadata:
  last_updated: "2026-08-23"
---

# Agent Instructions Builder

A builder skill for creating and editing `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `SKILL.md`,
and related AI coding assistant instruction files at any scope level, for any tool.

## When to Use

Invoke this skill when the user:

- Asks to create or write a `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, or similar file
- Says "set up Claude for this project" or "add agent instructions"
- Asks "what should go in my CLAUDE.md?" or "what belongs in AGENTS.md?"
- Wants a global/user-level configuration file (`~/.claude/CLAUDE.md`)
- Is starting a new project and wants instruction files from scratch
- Needs multi-tool support (Claude Code + Codex + Gemini + OpenCode reading the same repo)
- Is working in a monorepo and needs parent/child scoping
- Is **editing** an existing `CLAUDE.md`/`AGENTS.md`, `SKILL.md`, or runbook — adding a
  rule, correcting one, or moving content between files

## Quick Reference

| Scope | File(s) | Reference |
| --- | --- | --- |
| User/global | `~/.claude/CLAUDE.md` | `references/scope-hierarchy.md`, `references/cookbook/user-global.md` |
| Project root | `CLAUDE.md` or `AGENTS.md` | `references/scope-hierarchy.md`, project cookbook |
| Personal (gitignored) | `CLAUDE.local.md` | `references/scope-hierarchy.md` |
| Subdirectory / path-scoped | `.claude/rules/*.md` | `references/scope-hierarchy.md`, `references/cookbook/monorepo.md` |
| Multi-tool project | CLAUDE.md + AGENTS.md + GEMINI.md | `references/multi-tool-compat.md` |
| **Editing** an existing instruction file, skill, or runbook | `references/editing-discipline.md` |

## Workflow

### Step 1: Diagnose Scope

Ask — or infer from the codebase and conversation context:

- **Which level?** User-global, project root, monorepo parent/child, or a combination?
- **Which tool(s)?** Claude Code only, or also Codex, Gemini CLI, OpenCode?

Use the **Scope Decision Guide** below if unsure.

### Step 2: Gather Context

For **project-level** files, read the codebase first. Check `package.json`, `pyproject.toml`,
`Makefile`, `README.md` — don't ask for things you can discover. Then determine:

- Project type (Python library? TypeScript API? monorepo? agent/plugin?)
- Key commands: build, test, lint, dev server
- Async stance (async-first, sync-first, or mixed)
- Non-obvious constraints or conventions the AI would need to know
- Team or solo? (If solo, personal preferences can go here; if team, use `CLAUDE.local.md`
  for personal preferences)

For **user-global** files, ask the user about:

- Role and primary languages/frameworks
- Communication preferences (verbosity, code vs. prose, etc.)
- Recurring tools and workflows that apply across all projects

### Step 3: Select Cookbook Template

Read the relevant file from `references/cookbook/` and adapt it to the actual project.
Remove sections that don't apply; add project-specific content.

| Project type | Template |
| --- | --- |
| Python (FastAPI, library, data) | `references/cookbook/python-project.md` |
| TypeScript (Next.js, API, CLI, agent) | `references/cookbook/typescript-project.md` |
| Monorepo (any language) | `references/cookbook/monorepo.md` |
| Agent, MCP server, or plugin | `references/cookbook/agent-mcp-project.md` |
| Side project / minimal | `references/cookbook/minimal-project.md` |
| User global (`~/.claude/CLAUDE.md`) | `references/cookbook/user-global.md` |

### Step 4: Generate and Write

Quality targets:

| Scope | Target length | Key principle |
| --- | --- | --- |
| User-global | 100–200 lines | Comprehensive personal preferences |
| Project-level | 20–80 lines | Concrete facts about this codebase |
| Subdirectory rule | 5–20 lines | Path-scoped, laser-focused |

Every line costs context on every session. Trim ruthlessly — if removing a line wouldn't
confuse a new contributor, remove it.

If multiple tools are in use, read `references/multi-tool-compat.md` before generating.

Write the file(s) to disk at the correct paths, then tell the user where each one lives.

### Editing an Existing Instruction File, Skill, or Runbook

Creating from scratch and revising something that already exists are different jobs.
Before adding, correcting, or moving a rule in a `CLAUDE.md`/`AGENTS.md`, a `SKILL.md`,
or a `references/*.md` runbook, read
[`references/editing-discipline.md`](references/editing-discipline.md) — the RED-GREEN
discipline for doc edits (a check that the guidance is actually missing before writing
it, one incident citation per rule, and where a fix belongs: local file vs. the global
instruction files loaded into every session). For creating a genuinely new skill from
nothing, use `superpowers:writing-skills` instead — its pressure-scenario testing is
the heavier tool for guidance that doesn't exist yet.

---

## Scope Decision Guide

```
Need agent instructions for...
├── Every project on this machine → ~/.claude/CLAUDE.md  (user-global)
├── This specific project only
│   ├── Solo project                → CLAUDE.md at project root
│   ├── Team project (checked in)  → CLAUDE.md or AGENTS.md at project root
│   └── Personal prefs on a team   → CLAUDE.local.md  (add to .gitignore)
├── Monorepo with distinct sub-packages
│   ├── Spans all packages          → root CLAUDE.md
│   └── Package-specific rules      → CLAUDE.md in that package dir, or
│                                      .claude/rules/<name>.md with paths: frontmatter
└── Multi-tool (2+ AI assistants)
    └── See references/multi-tool-compat.md
```

---

## Anti-Patterns

Avoid these — they make instruction files worse over time:

| Anti-pattern | Why it fails | Alternative |
| --- | --- | --- |
| Multi-step procedures ("to deploy, step 1...") | Bloats every session; hard to maintain | Move to a skill or a runbook |
| Large reference material | Expensive on every session | `@import` or a skill with `references/` |
| "Always use X" with no context | Gets ignored; no reasoning to generalize from | Explain the why: "Use X because Y" |
| Git history or incident notes | Stale fast; belongs in commits | Commit message or ADR |
| Duplicate content across scope levels | Diverges silently | Use `@import` to share a single source |
| Instructions for hypothetical scenarios | Not active constraints | Only write what shapes daily work |
| Personal preferences in a team file | Pollutes shared instructions | Put personal prefs in `CLAUDE.local.md` |

---

## Multi-Tool Quick Guide

For projects used with more than one AI coding tool, read `references/multi-tool-compat.md`
for the full decision matrix. Quick summary:

- **Claude Code only** → write everything in `CLAUDE.md`, use `@import` freely
- **Codex only** → write everything in `AGENTS.md` (plain Markdown, no imports)
- **Claude Code + Codex** → write in `AGENTS.md`; `CLAUDE.md` = single line `@AGENTS.md`
- **+ Gemini / OpenCode** → same as above; make `GEMINI.md` a **symlink** to `AGENTS.md`
  (`ln -sf AGENTS.md GEMINI.md` — Gemini has no imports, and a symlink means zero sync drift).
  OpenCode reads `AGENTS.md` directly.
- **Claude-only tool wiring** (which skill/hook to invoke) → keep it in a separate
  `claude-extras.md`, and set `CLAUDE.md` = `@AGENTS.md` + `@claude-extras.md` so the shared
  `AGENTS.md` stays universal. Prefer symlinks from a canonical source over copies; see
  `references/multi-tool-compat.md`.
