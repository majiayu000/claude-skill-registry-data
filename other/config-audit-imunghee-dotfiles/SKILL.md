---
name: config-audit
description: "Audit ~/.config/{ai,claude,codex}/ and the deployed tool home (~/.claude or ~/.codex) for 3-tier structure compliance: layout, prefix convention, AGENTS.manifest sync, deploy-model integrity, generated-file protection. Use after creating, editing, or moving files there. Skip project-local .claude/ config and unrelated dotfiles."
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

Audit `~/.config/{ai,claude,codex}/` structure for compliance with the 3-tier layout rules.

## Checks (tool-agnostic)

### 1. Tier violation
- A file in `claude/` whose body has NO Claude-specific dependency (no slash commands, no `Agent(subagent_type=...)`, no `EnterPlanMode`/`EnterWorktree`, no `~/.claude/`-only paths, no Claude hooks/extensions, no settings.json permissions) → suggest moving to `ai/`.
- A file in `codex/` whose body has NO Codex-specific dependency (no sandbox modes, no `codex exec`, no `~/.agents/skills/`, no `config.toml [mcp_servers.*]`-only refs) → suggest moving to `ai/`.
- A file in `ai/` whose body uses tool-only tokens or systems → split the tool-specific portion into the tool's directory. Exception: naming both tools side by side, where the file depends on neither — `ai/README.md`'s deploy tables, `PERSONAL.md` giving each tool its own phrasing of one instruction, a memory note recording that a hook exists on one tool and not the other. **The test: delete one tool from the file.** If the advice still stands for the tool that remains, the mention is descriptive and belongs in `ai/`; if it collapses, it is a dependency and belongs in that tool's directory.
- A file in `ai/` containing a literal `~/.claude/` or `~/.codex/` path (instead of the `{{TOOL_HOME}}` token) → FAIL (a literal tool path silently breaks the other tool). Exceptions: `ai/README.md`, `ai/skills/config-audit/SKILL.md`, and `ai/memory/feedback_ai_config_structure.md` — these describe the deploy model itself and must name both tools' literal targets. The rule targets *operational* paths (command/ls/script targets), not prose that documents deploy structure.

### 2. Prefix violation
- File or skill directory directly under `claude/{rules,memory,skills}/` without `claude-` prefix → FAIL (move with rename).
- File or skill directory directly under `codex/{rules,memory,skills}/` without `codex-` prefix → FAIL.
- Any file under `ai/` with `claude-` or `codex-` prefix → FAIL (prefix is for tool-specific tiers only).
- For tool-specific skills, the directory name is the ownership boundary and MUST keep the native prefix. The `SKILL.md` frontmatter `name:` is the user-facing invocation/display name and MAY omit the native prefix when the shorter name is clear and unique in that tool's deployed skill scope.
- Duplicate `SKILL.md` frontmatter `name:` values within one deployed skill scope → FAIL (Claude scope: `ai/skills`, `ai/skills/private`, `claude/skills`; Codex scope: `ai/skills`, `ai/skills/private`, `codex/skills`).

### 3. AGENTS.manifest drift
- A file in `ai/` (excluding `ai/skills/`, `ai/scripts/`, `ai/lib/`, `ai/.gitignore`, `ai/AGENTS.manifest` itself, `ai/README.md`) NOT listed in `ai/AGENTS.manifest` → WARN (Codex will not see this file). Same as `ai/scripts/sync-back.sh --strict` would catch.
- A line in `ai/AGENTS.manifest` whose target file does not exist → FAIL.
- `feedback_ai_config_structure.md` not the first memory entry in the manifest memory section → FAIL (Codex must see token rules before any token-using file).

### 4. Undefined tokens
- Any `{{[A-Z_]+}}` in `ai/` source files whose name is NOT in the defined token set ({{TOOL_HOME}}, {{TOOL_NAME}}, {{TOOL_NAME_LC}}, {{INSTRUCTIONS_FILE}}, {{CONFIG_FILE}}, {{PLAN_DIR}}, {{STATE_DIR}}) → FAIL. Either add to the token set + bootstrap expand functions, or replace with literal value.
- `{{PLAN_DIR}}` must resolve to `.agents/plans`, `{{STATE_DIR}}` to `.agents/state`. `.agents/skills` is for Codex skill discovery only; `.agents/plans`, `.agents/state`, and `.agents/tasks/` (per-task backlog/closed/links/memory) must stay sibling entries (never inside `.agents/skills`).

### 5. Generated-file integrity
- `~/.claude/MEMORY.md` missing the `AUTO-GENERATED` header → FAIL (file was hand-edited or bootstrap is broken).
- `~/.codex/AGENTS.md` missing the `AUTO-GENERATED` header → FAIL.
- `~/.codex/AGENTS.md` missing `<!-- codex/DEVGUARD.md -->` when `codex/DEVGUARD.md` exists → FAIL (Codex-only addendum is not deployed).
- Bytes of `~/.codex/AGENTS.md` exceeding `project_doc_max_bytes` (read from `codex/config.toml.template`) → FAIL.

## Checks (tool-specific, run only when current tool matches)

### Claude
- `~/.claude/settings.json` hook entries reference scripts that exist under `claude/hooks/` → if a referenced script is missing, FAIL (dangling hook reference).
- `~/.claude/MEMORY.md` index entries reference files that exist under `~/.claude/memory/` (or its `private/` subdir) → FAIL on missing entry target, WARN on file-without-entry.
- Plain files under `~/.claude/memory/` that are not generated, not symlinks to `ai/memory/` or `claude/memory/`, and not indexed by `~/.claude/MEMORY.md` → WARN (runtime-only memory drift).
- `~/.claude/skills/<name>` symlinks resolve to a real directory under `ai/skills/` or `claude/skills/` → FAIL on broken symlink.

### Codex
- `~/.codex/config.toml` parses as valid TOML → FAIL on parse error.
- `[mcp_servers.<name>]` blocks have `command` (stdio) or `url` (HTTP) → WARN if neither.
- `project_doc_max_bytes` is set ≥ current AGENTS.md size → FAIL otherwise.
- `codex/config.toml.template` `UserPromptSubmit` hooks missing `codex/hooks/inject-context.sh`, or its timeout is not exactly 30 seconds → FAIL (session binding must resolve within the prompt turn).
- Either inject-context adapter does not parse the exact `session_id`, pass its strict tool
  namespace to `ensure-session`, or preserve the 30-second bound → FAIL. A `default`/PPID
  binding key or an `ensure-current` prompt path is also a FAIL.
- An unbound main adapter payload contains any plan id/title/path/branch/base/recovery
  field, or does not state that main current is launcher-only → FAIL.
- Either inject-context adapter omits the exact canonical continuation guard from every
  branch without a validated draft/active session binding (normal unbound/empty,
  `legacy_unmapped`, `internal_error`, malformed `ok`, or unexpected status), or emits it
  for a validated draft/active `ok` binding → FAIL.
- `~/.agents/.codex/state/current.txt` exists and is non-empty → WARN (legacy tool-specific state pointer; current shared state is repo-local `.agents/state/current.txt`).
- Any legacy `~/.agents/.codex/plans/*.md` frontmatter has `status: draft` or `status: active` → WARN (old Codex plan namespace may conflict with shared plan/state expectations).
- `~/.agents/skills/<name>` symlinks resolve under `ai/skills/` or `codex/skills/` → FAIL on broken.

## Output

Report each FAIL/WARN with:
- File path (and line number when applicable)
- Rule violated
- Suggested fix (one line)

Group by Check 1–5 then tool-specific. End with a one-line summary: `N FAIL, M WARN, K PASS`.

## Rules

- Read-only — never modify files. Surface findings only.
- A check that does not apply (no relevant files exist) → report `— (n/a)`, not PASS.
- For Check 3, do not auto-update the manifest; that is the user's call.
