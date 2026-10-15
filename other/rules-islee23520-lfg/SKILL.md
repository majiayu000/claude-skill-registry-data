---
name: rules
description: Use when the user asks about lfg/GrokBuild rules injection, project rules files, matching, or environment configuration.
---

# GrokBuild Rules (lfg)

Rules injection is automatic once the lfg Grok plugin is enabled. It injects:

- static project instructions on `SessionStart` and `UserPromptSubmit` (native rules hook + config loader)
- matching file-specific rules after edit-like tools via PostToolUse (rules-injector glue)

Dynamic PostToolUse output is injected as additional context when the host attaches hook output. If hook context is not visible, read matching rule files from disk directly.

Supported project sources:

- `CONTEXT.md`
- `.omo/rules/**/*.md`
- `.claude/rules/**/*.md`
- `.cursor/rules/**/*.md`
- `.github/instructions/**/*.md`
- `.github/copilot-instructions.md`
- Root / nested `AGENTS.md` (fail-closed project awareness)

## Environment (lfg / Grok)

Prefer lfg/Grok-owned knobs when present. Codex-only `CODEX_RULES_*` names may appear in upstream OMO docs as historical reference; on GrokBuild do not require `CODEX_HOME` or Codex plugin layout.

## Cross-host note

Upstream may brand this as "Codex Rules". On GrokBuild the owner is **lfg native rules** (`lfg-native-rules.mjs` + `src/core/omo/rules-engine`).
