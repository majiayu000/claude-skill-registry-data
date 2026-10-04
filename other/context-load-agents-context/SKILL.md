---
name: context-load-agents-context
description: Load ancestor AGENTS.md context for a target file. Use when Codex, Claude, Copilot, or another agent needs local domain context before reading or editing source files.
allowed-tools:
  - Bash(.agents/skills/context-load-agents-context/scripts/load-agents-context.sh:*)
models:
  claude: haiku      # low-complexity; script-driven file traversal with no deep reasoning required
  copilot: gpt-5.4-mini  # mini equivalent for low-complexity Copilot tasks
  codex: gpt-5.4-mini
---

# Load AGENTS Context — Skill

## TL;DR

Agent-agnostic skill that emits `*AGENTS.md` context files from ancestor directories for a target source file; each file loads at most once per conversation session. Claude Code runs the script automatically as a `PostToolUse` hook. Codex, Copilot, and other agents invoke the same skill script explicitly.

## Non-Negotiables

- **Never load from auto-loaded dirs** — skip `.agents/rules/`, `.ai/rules/`, `.claude/rules/`, `.cursor/rules/`, `.github/instructions/`. Those are already in context via the AI tool's built-in loading mechanism.
- **Exit 0 always** — the hook must never return a non-zero exit code; it must not block the triggering tool. File-operation failures (tracker write, content read) are silently tolerated.
- **Read/Edit/Write or explicit skill invocation only** — skip unrelated hook tools (`Grep`, `Glob`, `Bash`). Trigger on actual file access for context, or on an explicit skill request.
- **Session dedup** — each `*AGENTS.md` file must be emitted at most once per conversation session. Paths are canonicalised (physical path) so symlinked access (`.claude/...` vs `.agents/...`) is treated as the same file.

## Design & Rationale

The sequence diagram, the six LADRs (PostToolUse choice, session-file dedup, git-root walk,
thin-wrapper script, superseded scope injection, skill-on-path injection), the detailed
Key Behaviors list, and the transfer checklist live in **[`references/design.md`](references/design.md)**.
Read that only when modifying the skill or its script — it is not needed to run the skill.

## Hook Registration

Add to `.agents/settings.json` (equivalently `.claude/settings.json` via symlink) under `hooks`:

```json
"PostToolUse": [
  {
    "matcher": "Read|Edit|Write",
    "hooks": [
      {
        "type": "command",
        "command": ".agents/hooks/load-agents-context.sh"
      }
    ]
  }
]
```

## Invocation

Use the skill as `/load-agents-context <path>` or run the script directly:

```bash
.agents/skills/context-load-agents-context/scripts/load-agents-context.sh --file path/to/source-file
```

Codex can pass its thread identifier for stable deduplication:

```bash
CODEX_SESSION_ID="${CODEX_SESSION_ID:-${CODEX_THREAD_ID:-codex-manual}}" \
  .agents/skills/context-load-agents-context/scripts/load-agents-context.sh --tool Codex --file path/to/source-file
```

Copilot can pass a stable prompt/session identifier:

```bash
.agents/skills/context-load-agents-context/scripts/load-agents-context.sh \
  --tool Copilot \
  --session-id copilot-vscode-session \
  --file path/to/source-file
```

## Transferring to Another Repo

See the checklist in [`references/design.md`](references/design.md#transferring-to-another-repo).

## Changelog

| Date | Change | Ref |
|:-----|:-------|:----|
| 2026-05-30 | Initial version. | |
| 2026-06-06 | Move mermaid/LADRs/Key Behaviors/transfer docs to `references/design.md`; fix stale `context/load-agents-context/` script paths to flat `context-load-agents-context/`. | |
