---
name: codex-orchestration
description: Authoritative reference for OpenAI Codex CLI's orchestration surface - skills discovery paths, agents/openai.yaml schema, hooks.json events and stdin JSON payload, notify config, and AGENTS.md precedence. Use when installing skills, wiring hooks, debugging why a skill or hook isn't firing, or explaining Codex-vs-Claude-Code differences. Do NOT use for general Codex usage tips, prompt engineering, or non-orchestration configuration like models/approvals.
---

# Codex Orchestration

How OpenAI Codex CLI discovers skills, fires hooks, and loads instructions. Use this skill instead of web-searching the docs each time.

Source of truth: `developers.openai.com/codex/{skills,hooks,config-advanced,config-reference,guides/agents-md}`. Verify against live docs if behavior seems off - orchestration features evolve.

## When to Activate

- Install a skill and need the correct target directory
- Wire a Codex hook and need the event name, matcher, or payload shape
- Debug why an implicit skill isn't triggering on a matching prompt
- Author or review `agents/openai.yaml` for a skill
- Explain to a teammate why format-on-edit hooks don't work in Codex
- Migrate hook or skill conventions from Claude Code to Codex
- Add a `notify` program for turn-complete events
- Write or update this repo's README/hooks documentation

## Discovery: Skills

Skills are folders containing `SKILL.md` (required) plus optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`. Codex scans these paths (earlier wins on activation; duplicate names do NOT merge - both appear in selector):

| Priority | Path | Scope |
| --- | --- | --- |
| 1 | `$CWD/.agents/skills` | Current folder |
| 2 | `$CWD/../.agents/skills` | Parent folder |
| 3 | `$REPO_ROOT/.agents/skills` | Repo root |
| 4 | `$HOME/.agents/skills` | User |
| 5 | `/etc/codex/skills` | Admin |
| 6 | Bundled | System |

Common mistake: copying skills to `~/.codex/skills/` - that path does nothing. Use `~/.agents/skills/`.

## SKILL.md Format

```markdown
---
name: kebab-case-name
description: What it does, when to use it, AND when NOT to use it. Codex matches this for implicit invocation.
---
```

The body loads only after the skill activates. Front-load triggers and scope boundaries in `description`.

## agents/openai.yaml (Optional)

Put it at `skills/<name>/agents/openai.yaml`:

```yaml
interface:
  display_name: "User-facing name"
  short_description: "User-facing description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt"

policy:
  allow_implicit_invocation: true

dependencies:
  tools:
    - type: "mcp"
      value: "serverName"
      description: "Required MCP server"
```

Set `allow_implicit_invocation: false` for skills that should only fire on explicit `/skills` or `$skillname` invocation.

## Activation Methods

| Method | How |
| --- | --- |
| Implicit | Codex auto-selects based on `description` matching the user prompt |
| Explicit (menu) | User runs `/skills` |
| Explicit (inline) | User types `$skillname` in a prompt |

## Hooks (Experimental)

Enable with:

```toml
# ~/.codex/config.toml
[features]
codex_hooks = true
```

Config lives at `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`.

### Events

| Event | Fires | Matcher matches |
| --- | --- | --- |
| `SessionStart` | Session start or resume | `"startup"` or `"resume"` |
| `PreToolUse` | Before tool execution | Tool name - **Bash only currently** |
| `PostToolUse` | After tool completion | Tool name - **Bash only currently** |
| `UserPromptSubmit` | User submits prompt | N/A - use `"*"` or omit |
| `Stop` | Turn concludes | N/A - use `"*"` or omit |

Critical limit: `PreToolUse`/`PostToolUse` match Bash only. **File-edit hooks (format-on-save) cannot fire through Codex hooks.** Use `pre-commit`, `husky`, or a `Makefile` target.

### hooks.json Schema

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "hooks/scripts/guard_force_push.sh",
            "statusMessage": "Checking force-push",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Stdin JSON Payload

Hook scripts receive JSON on **stdin**, not as `$1`. Common fields:

| Field | Meaning |
| --- | --- |
| `session_id` | UUID |
| `transcript_path` | Path to the session transcript |
| `cwd` | Working directory |
| `hook_event_name` | Matches the event |
| `model` | Model name |
| `turn_id` | Current turn UUID |
| `tool_input` | Tool-specific - for Bash, has `command` |

Parse with `jq`:

```bash
payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"
```

### Exit Codes

| Code | Meaning |
| --- | --- |
| `0` | Allow / continue |
| `2` | **Block** the tool call (PreToolUse) |
| Other non-zero | Error surfaced to operator |

For `SessionStart`, `UserPromptSubmit`, `Stop`, scripts can emit a JSON object on stdout with: `continue` (bool), `stopReason` (string), `systemMessage` (string), `suppressOutput` (bool).

## notify (Stable, simpler)

Separate from `hooks.json`. Lives in `config.toml`:

```toml
notify = ["python3", "/path/to/notify.py"]
```

Fires on `agent-turn-complete` only. Receives JSON as `argv[1]` (single string arg), NOT stdin. Fields: `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message`.

## AGENTS.md Precedence

Codex builds an instruction chain from AGENTS.md files:

1. `~/.codex/AGENTS.override.md` (if present, else `~/.codex/AGENTS.md`)
2. Repo root `AGENTS.md`
3. Subdirectory `AGENTS.md` files closer to `$CWD`

`@file` references inside AGENTS.md resolve and inline, so AGENTS.md can pull in skill bodies directly:

```markdown
## Domain Guidance
- Security audits: @.agents/skills/security/SKILL.md
```

## BAD / GOOD: Installing a Skill

BAD

```bash
cp -r my-skill ~/.codex/skills/     # wrong directory; Codex ignores this
```

GOOD

```bash
mkdir -p ~/.agents/skills
cp -r my-skill ~/.agents/skills/    # user-scope discovery
# or
mkdir -p ./.agents/skills
cp -r my-skill ./.agents/skills/    # repo-scope discovery
```

## BAD / GOOD: Writing a PreToolUse Hook

BAD

```bash
#!/usr/bin/env bash
# Assumes the command arrives as $1 - it doesn't.
if [[ "$1" == *"rm -rf"* ]]; then exit 2; fi
```

GOOD

```bash
#!/usr/bin/env bash
set -euo pipefail
payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"
if [[ "$cmd" == *"rm -rf /"* ]]; then
  echo "Blocking dangerous rm -rf /" >&2
  exit 2
fi
exit 0
```

## BAD / GOOD: Format-on-edit

BAD

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit", "hooks": [{ "type": "command", "command": "prettier --write" }] }
    ]
  }
}
```

`Edit` is not a matchable tool name for `PostToolUse` today. The hook never fires.

GOOD

Move it to `pre-commit`:

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks: [{ id: prettier }]
```

Or expose it via `make fmt` and document it in `AGENTS.md` under `## Environment Setup`.

## Codex vs Claude Code Differences

| Concern | Codex | Claude Code |
| --- | --- | --- |
| Skill install dir | `.agents/skills/` | `.claude/skills/` or plugin packs |
| Skill frontmatter | `name`, `description` | `name`, `description`, `allowed-tools`, etc. |
| Hooks config | `hooks.json` (experimental) | `settings.json` `hooks` block (GA) |
| Pre/PostToolUse matchers | Bash only | All tools including `Edit`, `Write`, etc. |
| Hook input | stdin JSON | stdin JSON |
| Turn-complete hook | `notify` in config.toml | `Stop` hook |
| Instructions file | `AGENTS.md` | `CLAUDE.md` |

## Debugging Checklist

When a skill or hook isn't firing:

- Confirm the skill folder lives under one of the six `.agents/skills` paths. Duplicate names surface in the selector, they don't merge.
- Check `description` for triggering vocabulary. A vague description will miss implicit activation.
- For explicit invocation, run `/skills` and verify the skill is listed.
- For hooks, verify `[features] codex_hooks = true` is set and `hooks.json` parses as valid JSON.
- For `PreToolUse`/`PostToolUse`, confirm the matcher is `Bash` - Edit/Write tools won't fire it.
- Add a trace line to the hook script: `echo "fired: $(date)" >> /tmp/codex-hook.log`. If nothing appears, Codex is not invoking the hook.
- Tail the transcript path from the hook payload if you need to see what Codex saw.

## Checklist

- [ ] Skills install under `.agents/skills/` (not `.codex/skills/`)
- [ ] Every `SKILL.md` description declares scope boundary ("do NOT use for ...")
- [ ] `agents/openai.yaml` added when a skill needs implicit-invocation policy or MCP dependencies
- [ ] `hooks.json` lives at `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`
- [ ] Hook scripts parse JSON from stdin, not `$1`
- [ ] PreToolUse hooks use matcher `"Bash"` (no other tools supported yet)
- [ ] Format-on-edit is routed through `pre-commit` or `make`, not `hooks.json`
- [ ] `[features] codex_hooks = true` set in `config.toml` before expecting hooks to fire
- [ ] `notify` is used only for `agent-turn-complete`; payload arrives via `argv[1]`
- [ ] AGENTS.md uses `@file` imports to pull skill bodies into long-lived context when needed
