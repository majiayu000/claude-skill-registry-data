---
name: cf-init
version: 1.2.0
author: Ashay Kubal @ Qball Inc.
description: Initialize the CLEAR framework in the current project. Use when a user wants to set up CLEAR for the first time, reinitialize an existing project (destructive), or refresh meta files (CLAUDE.md + rules.md) from the latest CLEAR templates (non-destructive).
user-invocable: true
argument-hint: "[--reinit-clean | --refresh-config | --force]"
allowed-tools:
  - Bash
  - Write
  - Read
  - Glob
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Initialize CLEAR Framework

Set up CLEAR (Context Layered Engineering for Agentic Resources) in the current project. This skill runs a single CLI command that creates the `.clear/` directory structure, generates a project manifest, initializes Session 0, configures hooks, configures the statusline, and returns a structured JSON result. Claude then adds session resume instructions to CLAUDE.md.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`. This matters most for `/cf-init`, which a consumer always runs *before* any restart.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op.

---

## When to Use This Skill

| Trigger Pattern | Example User Request | Flag |
|-----------------|---------------------|------|
| First-time CLEAR setup | "Initialize CLEAR in this project" | (none) |
| Reinitialize from scratch (DESTRUCTIVE) | "Reset CLEAR — start fresh", "Reinitialize CLEAR" | `--reinit-clean` |
| Refresh meta files only (non-destructive) | "Refresh my CLAUDE.md from the latest CLEAR template", "Update CLEAR rules.md" | `--refresh-config` |
| Set up framework tracking | "Set up CLEAR so my sessions are tracked" | (none) |

**Destructiveness matrix:**

| Flag | What it does | What it preserves |
|------|--------------|-------------------|
| (none) | First-time init — refuses if `.clear/` already exists | n/a |
| `--reinit-clean` | Creates a `.clear.backup.<ts>/` then DELETES `.clear/` (knowledge, workpackages, sessions, audit). Re-initializes Session 0. | Nothing inside `.clear/`. Backup directory only. |
| `--refresh-config` | Rewrites ONLY `CLAUDE.md` + `.claude/rules/rules.md` from latest CLEAR templates. Idempotent. | All of `.clear/`. All sessions/knowledge/workpackages untouched. |
| `--force` | **DEPRECATED** alias for `--reinit-clean`. Will be removed in CLEAR vNEXT. Emits stderr warning. | Same as `--reinit-clean`. |

**DO NOT use for:**
- Checking CLEAR status after initialization (use `/cf-status` instead)
- Reloading configuration without reinitializing (use `/cf-reload` instead)

**Recommendation logic (BINDING):**

If the user asks to "refresh", "update", "re-sync", or "reload" CLEAR meta files (CLAUDE.md or rules.md) and their stated goal is NOT to wipe existing knowledge/sessions/workpackages, recommend `--refresh-config` and explicitly warn against `--reinit-clean`/`--force`. The destructive flags wipe ALL `.clear/` state with no shipped restore CLI in Phase A — recovery requires manual copy from the timestamped backup directory.

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. Execute in order. No skipping.**

- [ ] Pre-flight check completed (determine initialization state)
- [ ] Init CLI executed (creates .clear/ structure, manifest, config, session 0, env vars, statusline)
- [ ] CLI output parsed and verified (success / partial / error)
- [ ] Session resume instructions added to project CLAUDE.md
- [ ] Success output displayed with project ID, session ID, and next steps

---

## Command Reference

Init CLI at `$CLEAR_PLUGIN_ROOT/build/infrastructure/init/cli/`.

> **Pre-init note on the plugin root:** `$CLEAR_PLUGIN_ROOT` is persisted into the
> project's `.claude/settings.json` by the SessionStart hook on the first session *after*
> initialization. On a brand-new project it is therefore **empty until cf-init has run and
> Claude Code has been restarted** — so on the very first `/cf-init`, `$CLEAR_PLUGIN_ROOT`
> may be blank. When it is, use Claude Code's native per-plugin variable `$CLAUDE_PLUGIN_ROOT`
> as the `--plugin-root` value (and in the CLI path) instead. After the first post-init
> restart, `$CLEAR_PLUGIN_ROOT` is set and the table commands below work as written.

| Action | CLI Command |
|--------|-------------|
| Initialize CLEAR | `init-cli --cwd=. --plugin-root=$CLEAR_PLUGIN_ROOT` |
| Reinitialize from scratch (DESTRUCTIVE) | `init-cli --cwd=. --plugin-root=$CLEAR_PLUGIN_ROOT --reinit-clean` |
| Refresh meta files only (non-destructive) | `init-cli --cwd=. --plugin-root=$CLEAR_PLUGIN_ROOT --refresh-config` |
| Reinitialize (legacy alias) | `init-cli --cwd=. --plugin-root=$CLEAR_PLUGIN_ROOT --force`  ← DEPRECATED |

---

## Usage

```
/cf-init [--reinit-clean | --refresh-config | --force]
```

**Arguments:**

- `--reinit-clean` — **DESTRUCTIVE.** Creates a timestamped backup at `.clear.backup.<ts>/`, then DELETES the existing `.clear/` directory (knowledge, workpackages, sessions, audit). Re-initializes a fresh `.clear/` with Session 0. Use when intentionally starting over.
- `--refresh-config` — **Non-destructive.** Rewrites ONLY `CLAUDE.md` and `.claude/rules/rules.md` from the latest CLEAR templates. Leaves `.clear/` entirely untouched. Idempotent — re-running on an up-to-date project is a no-op. Use when you only want to pick up new CLEAR governance text.
- `--force` — **DEPRECATED** alias for `--reinit-clean`. Same destructive behavior; emits a stderr deprecation warning. Will be removed in CLEAR vNEXT.

Current arguments: $ARGUMENTS

---

## Instructions

### Pre-flight Check

Before any initialization, determine the current state and intent:

```bash
ls -la .clear/config/clear-manifest.yaml 2>/dev/null && echo "ALREADY_INITIALIZED" || echo "NOT_INITIALIZED"
```

**Branch on result:**

- **ALREADY_INITIALIZED + no flag:** Display a message explaining the project is already initialized. Surface the three options to the user:
  - `--refresh-config` to rewrite only CLAUDE.md + rules.md from latest templates (non-destructive).
  - `--reinit-clean` to wipe `.clear/` and start over (DESTRUCTIVE — creates a backup but deletes all knowledge/sessions/workpackages).
  - Do nothing if neither matches their intent.
  STOP here.
- **`.clear/` exists but no manifest:** Display an error explaining this is an unknown state that cannot be safely initialized. STOP here.
- **NOT_INITIALIZED:** Proceed with the init CLI below (no destructive-flag prompt needed).
- **ALREADY_INITIALIZED + `--reinit-clean` or `--force`:** Execute the **Destructiveness Confirmation Prompt** below BEFORE running the CLI.
- **ALREADY_INITIALIZED + `--refresh-config`:** Proceed directly to the init CLI (non-destructive path; no confirmation needed).

---

### Destructiveness Confirmation Prompt (BINDING — `--reinit-clean` / `--force` only)

If the user invoked `/cf-init --reinit-clean` or `/cf-init --force` against an already-initialized project, emit the following warning to the user BEFORE running the CLI and pause for explicit confirmation:

> **WARNING — `--reinit-clean` is destructive.**
>
> Running this will create a backup at `.clear.backup.<ts>/`, then DELETE the existing `.clear/` directory. You will lose:
> - All knowledge entries
> - All workpackages
> - All session handoffs
> - The audit log
>
> Phase A of WP-PS1 does not yet ship a restore CLI. Recovery requires manually copying files back from the backup directory.
>
> **If your goal is to refresh `CLAUDE.md` or `.claude/rules/rules.md` only**, use `/cf-init --refresh-config` instead — it leaves `.clear/` entirely untouched.
>
> Confirm: do you want to proceed with the destructive reinit? (yes/no)

- If the user answers **yes**: proceed to the init CLI.
- If the user answers **no** (or anything other than yes): STOP. Do not run the CLI. Suggest `--refresh-config` if their goal is meta-refresh.

If the user invoked `--force`, ALSO mention that `--force` is deprecated and `--reinit-clean` is the new name.

---

### Run Init CLI

Execute the init CLI to perform `.clear/` setup. The argument list depends on which flag the user passed:

```bash
# Determine the flag arg to pass through
FLAG_ARG=""
case "$ARGUMENTS" in
  --reinit-clean) FLAG_ARG="--reinit-clean" ;;
  --refresh-config) FLAG_ARG="--refresh-config" ;;
  --force) FLAG_ARG="--force" ;;
esac

node "$CLEAR_PLUGIN_ROOT/build/infrastructure/init/cli/init-cli.js" \
  --cwd="$PROJECT_DIR" \
  --plugin-root="$CLEAR_PLUGIN_ROOT" \
  $FLAG_ARG
```

**For `--refresh-config` (non-destructive path):** the CLI invokes ONLY `updateProjectClaudeMd` + `updateProjectRulesMd`. None of the directory/manifest/session/hook/statusline steps run. Output JSON will have `status: "success"` with no `init` block.

**For full init / `--reinit-clean` / `--force`:** the CLI performs:
1. (Force path only) Creates `.clear.backup.<ts>/` backup, deletes existing `.clear/`
2. Creates `.clear/` directory structure (7 subdirectories)
3. Creates manifest at `.clear/config/clear-manifest.yaml`
4. Creates configuration at `.clear/config/clear-config.yaml`
5. Initializes Session 0 (session.json, session-history.json, sync-state.json)
6. Configures environment variables (kill switches) in `.claude/settings.json`
7. Configures statusline for context window detection in `.claude/settings.json`

**Do NOT use Write or Edit on any `.clear/` file.** The CLI handles all `.clear/` mutations via `fs.writeFileSync`, which is invisible to the PreToolUse guard.

### Parse CLI Output

The CLI returns JSON:

```json
{
  "status": "success | partial | error",
  "init": {
    "success": true,
    "projectName": "...",
    "projectPath": "...",
    "projectId": "prj-xxxxxxxx",
    "sessionId": "init-xxxx-...",
    "steps": [{"step": "...", "success": true}],
    "checks": [{"name": "...", "passed": true, "message": "..."}]
  },
  "statusline": {
    "needsRestart": true,
    "originalStatusline": null
  },
  "error": "..." 
}
```

**Branch on status:**

- **`success` + `init` block present**: Full init succeeded. Proceed to Step 6.
- **`success` + NO `init` block**: `--refresh-config` path completed (non-destructive meta-file refresh). CLAUDE.md + `.claude/rules/rules.md` are now updated. Step 6 (session-resume append) is NOT needed — skip it. Report completion to the user and STOP.
- **`partial`**: Init succeeded but statusline configuration failed. Proceed to Step 6 with a warning about statusline.
- **`error`**: Initialization failed. Display the error message and the `init.steps` array showing which steps completed. Advise the user to run `/cf-init --reinit-clean` to retry. If the error is `CONFLICTING_FLAGS`, explain that `--refresh-config` cannot be combined with `--reinit-clean` or `--force`.

---

### Add Session Resume Instructions (Step 6)

**This is the only Write operation in the skill — it writes to `CLAUDE.md`, NOT to `.clear/`.**

Append session resume instructions to the project's `CLAUDE.md` file. These instructions tell Claude how to restore CLEAR context after `/clear` or compaction events. If `CLAUDE.md` does not exist, create it with the resume instructions.

---

### Error Recovery

If initialization fails partway through:

- Report which steps completed successfully (from `init.steps` array)
- Report which step failed and the reason
- Provide guidance:
  - First-time init failure → "Run `/cf-init` again to retry."
  - Reinit failure (partial wipe) → "Run `/cf-init --reinit-clean` to retry from scratch. A backup of the prior state was created at `.clear.backup.<ts>/`."
  - `CONFLICTING_FLAGS` error → "`--refresh-config` and `--reinit-clean`/`--force` are mutually exclusive. Pick one based on intent."

---

## Completion Checklist

**For first-time init or `--reinit-clean` / `--force`:**

- [ ] (If reinit) Destructiveness Confirmation Prompt presented to user and explicit "yes" received before running the CLI
- [ ] (If `--force`) User informed that `--force` is deprecated and `--reinit-clean` is the new name
- [ ] Init CLI executed successfully (or partially with statusline warning)
- [ ] `.clear/` directory contains all 7 subdirectories (verified by CLI steps)
- [ ] Configuration and manifest files exist (verified by CLI)
- [ ] Session 0 is active (verified by CLI)
- [ ] Environment variables configured (verified by CLI)
- [ ] Session resume instructions appended to CLAUDE.md
- [ ] Success output displayed: project ID, Session 0 ID, and next steps
- [ ] User informed of next steps: create a plan, define workpackages, run `/cf-status`
- [ ] If statusline was configured (`statusline.needsRestart` is true): "Please exit and restart Claude Code. After restarting, the CLEAR statusline appears at the bottom of the screen — that confirms it is working. If it is missing or you want to verify the install wiring, run `/cf-debug install`."
- [ ] Context advisory displayed: "CLEAR calculates context based on max usage, but it is advisable to start a new session after hitting 75%+ of operational context."

**For `--refresh-config`:**

- [ ] Init CLI executed successfully with `status: "success"` and no `init` block in output
- [ ] User informed: "CLAUDE.md and `.claude/rules/rules.md` refreshed from latest CLEAR templates. `.clear/` was not touched — all sessions, knowledge, and workpackages remain intact."
- [ ] Step 6 (session-resume append) intentionally SKIPPED — the CLI's update already handles meta-file content.
