---
name: github-copilot-instructions
description: >-
  Use for creating, splitting, reviewing, or debugging GitHub Copilot custom instructions in Visual Studio Code, including .github/copilot-instructions.md, .github/instructions/*.instructions.md, and AGENTS.md. Do not use for slash commands, Agent Skills, custom agents, hooks, or ordinary project documentation.
argument-hint: "[repository rules, target paths, and existing instruction files]"
---

# GitHub Copilot instructions

Encode stable repository facts and conventions at the narrowest automatic
scope. Instructions affect chat requests, not inline suggestions.

## Workflow

1. Inspect existing instruction files, project configuration, build/test entry
   points, nested repositories, and the active VS Code settings.
2. Separate rules that apply to nearly every task from language, framework, or
   directory-specific rules.
3. Put broad rules in `.github/copilot-instructions.md`. Put conditional rules
   in `.github/instructions/<purpose>.instructions.md` with `applyTo` globs.
4. Use `AGENTS.md` only for durable cross-agent repository guidance. Treat
   nested discovery as host/setting dependent.
5. Rewrite every statement as fact, condition/action, prohibition, or exact
   verification command. Remove aspiration, task-specific prompts, and history.
6. Check overlaps. Applicable files can be combined without guaranteed order;
   eliminate contradictions rather than declaring a winner.

## Rules

- Keep always-on context short, self-contained, and broadly applicable.
- Ground commands in files that exist and commands that were actually tested.
- Use forward-slash repository-relative `applyTo` patterns. Test positive and
  negative paths; do not assume `*.py` recursively matches the repository.
- Link local context with relative Markdown links rather than copying it.
- Do not put secrets, mutable status, long API references, personas, or one-off
  workflow prompts in instructions.
- Do not use deprecated settings-based code/test-generation instructions for a
  new design. Inspect current host settings for review/commit/PR special cases.

Read [scope and glob contracts](references/artifact-contracts.md). Use
[instruction patterns](references/patterns.md) and finish with
[verification](references/verification.md).

## Completion

Every rule has a justified scope; YAML parses; globs select intended files and
exclude near misses; commands and paths exist; no instruction sets conflict;
and VS Code lists the applied instruction reference in a representative chat.
