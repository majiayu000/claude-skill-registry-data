---
name: harness-setup
description: "Initializes and configures Harness in a project — CI, memory, duo workflow, Codex. Use when setting up a new project or adding Harness configuration."
when_to_use: "initialize project, setup harness, configure CI, setup memory, duo workflow, gitignore"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
argument-hint: "[init|codex|opencode|duo|cleanup|gitignore]"
effort: medium
model: sonnet
---

# Harness Setup

## Quick Reference

| User Input | Subcommand | Behavior |
|------------|------------|----------|
| `harness-setup` (no args) | `init` | Runs `gitignore` → project initialization (CLAUDE.md + plans.json + settings.json) |
| `harness-setup init` | `init` | New project initialization: gitignore → CLAUDE.md + plans.json + settings.json |
| `harness-setup gitignore` | `gitignore` | Merge harness-managed block into .gitignore (runs `scripts/merge-gitignore.sh`) |
| `harness-setup cleanup` | `cleanup` | Periodic maintenance: delete old logs, archive completed phases (`harness plan-cli archive`), trim traces |
| `harness-setup codex` | `codex` | Set up Codex CLI: copy config, rules, and skills to project `.codex/` |
| `harness-setup opencode` | `opencode` | Set up OpenCode: copy config, commands, and skills to project `.opencode/` |
| `harness-setup duo` | `duo` | Set up both Codex and OpenCode in one step |

## Subcommand Details

### init — Project Initialization

Introduce Harness to a new project.

**Generated files** (user's project):
```
project/
├── CLAUDE.md            # Project configuration
├── .gitignore           # Standard ignore rules (harness-managed block appended)
└── .claude/
    ├── settings.json    # Claude Code permissions/sandbox/env
    ├── harness/plans.json  # Task tracking (auto-created by harness plan-cli)
    ├── memory/          # Trace archive + schemas (archive/, schemas/)
    ├── output-styles/   # Custom output styles (if any)
    ├── rules/           # Custom rules (if any)
    ├── scripts/         # Custom scripts (if any)
    └── skills/          # Custom skills (if any)
    └── settings.local.json # Local custom settings (gitignored) for user overrides
```

> **Note**: Neither `hooks/` nor `harness.toml` is generated into a user's project.
> - Hooks ship inside the installed plugin (`.claude-plugin/hooks.json`) — Claude Code
>   loads them from there automatically.
> - `harness.toml` + `harness sync` is a *plugin-author* workflow for regenerating
>   `.claude-plugin/*` files from a single TOML SSOT. User projects have no
>   `.claude-plugin/` to regenerate, so the TOML would be an orphaned file. Users who
>   want unified TOML authoring for their own `.claude/settings.json` can opt in later
>   via a dedicated subcommand (future work).

**Flow**:
1. Run the `gitignore` subcommand (idempotent — calls `scripts/merge-gitignore.sh`)
2. Detect project type (Node.js/Python/Go/Rust/Other)
3. Generate minimal CLAUDE.md
4. Create `.claude/harness/` directory (plans.json is auto-created on first `harness plan-cli add-phase` call)
5. Generate `.claude/settings.json` (permissions/sandbox/env — safe defaults)

### gitignore — Harness .gitignore Block

Merges the harness-managed block into the project's `.gitignore`. Safe to run multiple times — skips if the marker is already present.

Implementation: [`scripts/merge-gitignore.sh`](${CLAUDE_SKILL_DIR}/scripts/merge-gitignore.sh)

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/merge-gitignore.sh"
# Or with an explicit target path:
bash "${CLAUDE_SKILL_DIR}/scripts/merge-gitignore.sh path/to/.gitignore"
```

The block ignores `.claude/sessions/`, `logs/`, `settings.local.json`, and `states/`,
while force-tracking `.claude/memory/`, `.claude/output-styles/`, `.claude/rules/`,
`.claude/scripts/`, `.claude/skills/`, and `.claude/settings.json`.

### codex — Codex CLI Setup

Sets up the project for Codex CLI by copying Harness config templates and skills.
See [Codex CLI Setup Reference](${CLAUDE_SKILL_DIR}/references/codex.md) for full file layout and troubleshooting.

**Prerequisites**: Codex CLI installed (`npm install -g @openai/codex`)

**What it does**:
1. Checks that `codex` is installed; prints install instructions if not
2. Copies `templates/codex/*` → `.codex/` (config.toml, rules/harness.rules, .codexignore)
3. Copies `AGENTS.md` to the project root
4. Copies all skills from plugin `skills/` → `.codex/skills/` with `disable-model-invocation: true` patched into each SKILL.md frontmatter
5. Overlays `templates/codex-skills/` → `.codex/skills/` (codex-native variants of breezing and harness-work override the generic copies)

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/setup-codex.sh"
```

> **Note**: Excluded from the no-args `init` run — requires an external `@openai/codex` install that should be explicit opt-in.

### opencode — OpenCode Setup

Sets up the project for OpenCode by copying Harness config templates, commands, and skills.

**Prerequisites**: OpenCode installed (see https://opencode.ai/)

**What it does**:
1. Checks that `opencode` is installed; prints install instructions if not
2. Copies `templates/opencode/opencode.json` → `.opencode/opencode.json`
3. Copies `templates/opencode/commands/` → `.opencode/commands/`
4. Copies `AGENTS.md` to the project root
5. Copies all skills from plugin `skills/` → `.opencode/skills/` as-is (opencode ignores unknown frontmatter fields)

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/setup-opencode.sh"
```

> **Note**: Excluded from the no-args `init` run — requires OpenCode to be installed explicitly.

### duo — Codex + OpenCode Setup

Runs both `codex` and `opencode` setup subcommands in sequence.

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/setup-codex.sh"
bash "${CLAUDE_SKILL_DIR}/scripts/setup-opencode.sh"
```

### Cleanup

Periodic maintenance tasks:

| Task | Command |
|------|---------|
| Delete old logs | `find .claude/logs -mtime +30 -delete` |
| Archive completed phases | `harness plan-cli archive` |
| Delete old traces | `tail -1000 .claude/state/agent-trace.jsonl > /tmp/trace && mv /tmp/trace .claude/state/agent-trace.jsonl` |

## Related Skills

- `harness-plan` — Create project plans after setup
- `harness-work` — Execute tasks after setup
- `harness-review` — Review setup configuration
