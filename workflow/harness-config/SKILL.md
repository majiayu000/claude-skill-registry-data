---
name: harness-config
description: Keep agent configuration — instructions, skills, commands, agents, MCP registrations, hooks, permissions, and reusable prompts — aligned across more than one agent harness (e.g. Claude Code + Codex) from a single canonical config repo. Use when changing personal or repository agent configuration, migrating a workflow between harnesses, diagnosing configuration drift, or asking whether a capability will propagate from one harness to another.
---

# Harness Configuration

One canonical tree, projected into each harness. Your config repo — a personal,
versioned repository checked out at a stable path, written `<config>` below — is
the behavioural source of truth. Each harness consumes a *projection* of it: a
symlink, a generated file, or a native discovery path. Preserve native host
configuration where formats or capabilities genuinely differ.

## Resolving `<config>`

Before anything else, locate the canonical tree: check a conventional location
such as `~/.agents`, or an env var like `$AGENTS_CONFIG`. If neither resolves,
ask the user once and record the answer. If no config repo exists yet, offer
to create one — a fresh versioned repository at a stable path — before
proceeding.

## The tooling contract

Two tools you implement once, whatever you name them:

- **sync** — projects the canonical tree into each host's directories
  (symlinks where the format matches, generated files where it does not).
  Idempotent; run it after every edit.
- **doctor** — validates the projections: every shared surface reaches every
  harness, no orphaned or hand-edited projections, no credentials or session
  state in the shared tree. Non-zero exit on any failure.

## Classify the change

| Surface | Canonical source | Projection |
| --- | --- | --- |
| Personal instructions | `<config>/AGENTS.md` | Linked as `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` |
| Personal skills | `<config>/skills/<name>/SKILL.md` | The skills directory is linked into each harness's discovery folder (e.g. `~/.claude/skills`, `~/.codex/skills`) |
| Repository instructions and skills | Repo `AGENTS.md`, `.agents/skills/` | `CLAUDE.md` and `.claude/` compatibility links |
| Repository commands | `.agents/commands/` | Generated per-harness command skills |
| Repository agents | `.agents/agents/*.md` | Generated host-native agent definitions (e.g. Codex `.toml`) |
| MCP registrations | Repo `.mcp.json` | Generated host config (e.g. Codex `config.toml`), plus per-repo overrides under `<config>/hosts/<harness>/` |
| Reusable prompts | `<config>/prompts/` | Each harness's prompt/command mechanism (e.g. slash-command files) |
| Hooks, permissions, UI | Native host settings | Keep behaviour equivalent; do not force identical syntax |

The Codex entries illustrate one projection scheme, not stock Codex behaviour.
Note one scoping mismatch: `.mcp.json` is per-repo while Codex registers MCP
servers globally — your sync tool must decide how to bridge it (namespacing
generated entries, or per-repo overrides).

## Process

0. If no sync or doctor tooling exists yet, offer to scaffold both from the
   classification table before proceeding: sync as a script projecting each
   canonical path to its per-harness location, doctor as a script verifying
   the projections match canon and that no host directory contains hand edits.
1. Read both current projections before changing a host-specific surface.
2. Edit the canonical source when the surface is shared — never the projection.
3. Keep shared prose model- and harness-neutral. Quarantine unavoidable
   differences under `<config>/hosts/<harness>/` or a repository override file.
4. Run your sync tool.
5. Run your doctor check, then commit and push. Commit promptly — an
   uncommitted edit is the only copy that exists and can be lost to a parallel
   session overwriting the same files. Commit only after the doctor passes, so
   a broken state is never the tip.
6. Report what now propagates automatically and any genuine host limitation.

## Rules

- Never copy a shared skill into a host directory.
- Never edit a generated projection (command skills, agent definitions, host
  config) — change the canonical source and re-run sync.
- Translate host primitives instead of forking a shared file for syntax:
  `Agent(...)` or `Task(...)` means the current harness's native sub-agent
  mechanism; `Skill(...)` means its native skill loader.
- Never copy credentials, authentication state, sessions, history, caches, or
  tokens into the shared tree.
- Preserve host-specific capabilities (e.g. two harnesses whose hooks fire on
  the same events but are configured with different syntax). Match information
  and workflow, not syntax.
