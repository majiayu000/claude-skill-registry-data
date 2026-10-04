---
name: ralphmode
description: Configure Claude Code, Codex CLI, and Gemini CLI for Ralph-style automation with fewer approval prompts while keeping project boundaries, secret denylists, and sandbox-first safety rules intact.
license: CC-BY-4.0
compatibility: Claude Code, Codex CLI, and Gemini CLI. Requires bash, git, and a repo-scoped workspace. Treat full bypass as sandbox-only. Codex guidance in this skill reflects the official sandbox/approval model current on 2026-03-06; legacy permissions.allow or deny examples are compatibility notes only.
metadata:
  version: 0.3.0
  author: supercent-io
  keyword: ralphmode
  platforms: Claude Code, Codex CLI, Gemini CLI
  tags: ralph, permissions, automation, claude-code, codex-cli, gemini-cli, sandbox, trusted-folders, bypass
allowed-tools: Read Write Bash Grep Glob
---

# Ralphmode

Ralphmode is a cross-platform permission profile for long-running `ralph` or `jeo` workflows.
It reduces approval friction, but it is not "allow everything everywhere."
The core rule is simple: widen automation only inside a bounded project or disposable sandbox, and keep secrets plus destructive commands explicitly blocked.

---

## 0. Agent Execution Protocol (execute immediately upon `ralphmode` keyword detection)

> The following steps are commands, not descriptions. Execute them in order immediately when `ralphmode` is invoked. Do not skip steps.

### STEP 0: Detect mode from user's message

Parse the user's invocation:
- If the user says **"sandbox"**, **"yolo"**, **"bypass all"**, **"skip all"**, **"disposable"** → `MODE=sandbox`
- Otherwise → `MODE=repo` (default, safer)

### STEP 1: Run the setup script

The setup script auto-detects your git root, applies the preset to `.claude/settings.json`, and creates the safety hook.

```bash
# Find the script (checks installed locations)
_RALPHMODE_SCRIPT=""
for _candidate in \
  "$(git rev-parse --show-toplevel 2>/dev/null)/.agent-skills/ralphmode/scripts/apply-ralphmode.sh" \
  "$HOME/.agent-skills/ralphmode/scripts/apply-ralphmode.sh" \
  "$HOME/.claude/skills/ralphmode/scripts/apply-ralphmode.sh" \
  "$(pwd)/.agent-skills/ralphmode/scripts/apply-ralphmode.sh"; do
  if [[ -f "$_candidate" ]]; then
    _RALPHMODE_SCRIPT="$_candidate"
    break
  fi
done

if [[ -n "$_RALPHMODE_SCRIPT" ]]; then
  bash "$_RALPHMODE_SCRIPT" --mode "$MODE"
else
  echo "⚠️  apply-ralphmode.sh not found — applying inline (Claude Code only)"
fi
```

If the script is not found, fall through to STEP 2 (inline application for Claude Code).

### STEP 2: Inline application (Claude Code — fallback when script is missing)

Only run this if the script from STEP 1 was not found.

**Repo preset** (default — for normal development):

```python
python3 - <<'EOF'
import json, os, subprocess

try:
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
        stderr=subprocess.DEVNULL, text=True).strip()
except Exception:
    root = os.getcwd()

target = os.path.join(root, '.claude', 'settings.json')
os.makedirs(os.path.dirname(target), exist_ok=True)

try:
    existing = json.loads(open(target).read()) if os.path.exists(target) else {}
except Exception:
    existing = {}

existing['_ralphmode_previous_permissions'] = existing.get('permissions')
existing['permissions'] = {
    'defaultMode': 'acceptEdits',
    'allow': [
        'Bash(npm *)', 'Bash(pnpm *)', 'Bash(bun *)', 'Bash(yarn *)',
        'Bash(python3 *)', 'Bash(pytest *)',
        'Bash(git status)', 'Bash(git diff)', 'Bash(git add *)',
        'Bash(git commit *)', 'Bash(git log *)', 'Bash(git push)',
        'Read(*)', 'Edit(*)', 'Write(*)'
    ],
    'deny': [
        'Read(.env*)', 'Read(./secrets/**)',
        'Bash(rm -rf *)', 'Bash(sudo *)',
        'Bash(git push --force*)', 'Bash(git reset --hard*)'
    ]
}

with open(target, 'w') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print(f'✓ Repo preset applied to {target}')
EOF
```

**Sandbox preset** (only for disposable environments):

```python
python3 - <<'EOF'
import json, os, subprocess

try:
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
        stderr=subprocess.DEVNULL, text=True).strip()
except Exception:
    root = os.getcwd()

target = os.path.join(root, '.claude', 'settings.json')
os.makedirs(os.path.dirname(target), exist_ok=True)

try:
    existing = json.loads(open(target).read()) if os.path.exists(target) else {}
except Exception:
    existing = {}

existing['_ralphmode_previous_permissions'] = existing.get('permissions')
existing['permissions'] = {'defaultMode': 'bypassPermissions'}

with open(target, 'w') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print(f'✓ Sandbox preset applied to {target}')
EOF
```

### STEP 3: Ensure safety hook exists

```bash
HOOK="$HOME/.claude/hooks/ralph-safety-check.sh"
if [[ ! -f "$HOOK" ]]; then
  mkdir -p "$(dirname "$HOOK")"
  cat > "$HOOK" << 'HOOKEOF'
#!/usr/bin/env bash
CMD=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('command',''))" 2>/dev/null)
TIER1='(rm[[:space:]]+-rf|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+push.*--force|DROP[[:space:]]+TABLE|[[:space:]]sudo[[:space:]]|chmod[[:space:]]+777|\.env|secrets/)'
if echo "$CMD" | grep -qE "$TIER1"; then
  echo "BLOCKED: Tier 1 dangerous command detected." >&2
  echo "Command: $CMD" >&2
  exit 2
fi
HOOKEOF
  chmod +x "$HOOK"
  echo "✓ Safety hook created: $HOOK"
else
  echo "✓ Safety hook exists: $HOOK"
fi
```

### STEP 4: Report to the user

After applying, tell the user:
1. Which preset was applied (`repo` or `sandbox`)
2. Which file was written (`.claude/settings.json` path)
3. What the allow/deny list contains
4. How to revert: `rm .claude/settings.json` (project-local) or restore `~/.claude/settings.json` (global)
5. **Restart Claude Code** to activate permission changes

---

## When to use this skill

- You want `ralph` to iterate without repeated approval popups.
- You are setting up the same repo for Claude Code, Codex CLI, and Gemini CLI.
- You need a shared safety model: repo-only writes, no secrets reads, no destructive shell by default.
- You want a stronger separation between day-to-day automation and true YOLO mode.

## Instructions

### Step 1: Define the automation boundary first

Before changing any permission mode:

- Pick one project root and keep automation scoped there.
- List files and commands that must stay blocked: `.env*`, `secrets/**`, production credentials, `rm -rf`, `sudo`, unchecked `curl | sh`.
- Decide whether this is a normal repo or a disposable sandbox.

If the answer is "disposable sandbox," you may use the platform's highest-autonomy mode.
If not, use the repo-scoped preset instead.

### Step 2: Choose one preset per platform

Use only the section that matches the current tool:

- Claude Code: everyday preset first, `bypassPermissions` only for isolated sandboxes.
- Codex CLI: use the current official approval and sandbox model first; treat older `permissions.allow` and `permissions.deny` snippets as compatibility-only.
- Gemini CLI: trust only the project root; there is no true global YOLO mode.

Detailed templates live in [references/permission-profiles.md](./references/permission-profiles.md).

### Step 3: Apply the profile locally, not globally, unless the workspace is disposable

Prefer project-local configuration over user-global defaults.

- Claude Code: start with project `.claude/settings.json`.
- Codex CLI: start with project config and repo instructions or rules files.
- Gemini CLI: trust the current folder, not `~/` or broad parent directories.

If you must use a user-global default, pair it with a stricter denylist and a sandbox boundary.

### Step 4: Run Ralph with an explicit verification loop

After permissions are configured:

1. Confirm the task and acceptance criteria.
2. Run `ralph` or the `jeo` plan-execute-verify loop.
3. Verify outputs before claiming completion.
4. If the automation profile was temporary, revert it after the run.

Recommended execution contract:

```text
boundary check -> permission profile -> ralph run -> verify -> cleanup or revert
```

### Step 5: Keep "skip" and "safe" separate

Treat these as different modes:

- Repo automation: minimal prompts inside a bounded workspace.
- Sandbox YOLO: promptless execution in a disposable environment only.

Do not collapse them into one shared team default.

### Step 6: Configure Mid-Execution Approval Checkpoints

Static permission profiles (Steps 2–3) reduce friction before a run starts, but they do not stop dangerous operations that arise during execution. Add dynamic checkpoints so that Tier 1 actions are blocked or flagged at the moment they are attempted.

#### Dangerous operation tiers

| Tier | Action | Platform response |
|------|--------|------------------|
| **Tier 1** (always block) | `rm -rf`, `git reset --hard`, `git push --force`, `DROP TABLE`, `sudo`, `.env*`/`secrets/**` access, production environment changes | Block immediately, require explicit user approval |
| **Tier 2** (warn) | `npm publish`, `docker push`, `git push` (non-force), DB migrations | Output warning, continue only with confirmation |
| **Tier 3** (allow) | File reads/edits, tests, local builds, lint | Allow automatically |

#### Platform checkpoint mechanisms

| Platform | Hook | Blocking | Recommended pattern |
|----------|------|----------|-------------------|
| Claude Code | `PreToolUse` (Bash) | Yes — exit 2 | Shell script pattern-matches command; blocks Tier 1 |
| Gemini CLI | `BeforeTool` | Yes — non-zero exit | Shell script blocks tool; stderr fed to next turn |
| Codex CLI | `notify` (post-turn) | No | `approval_policy="unless-allow-listed"` + prompt contract |
| OpenCode | None | No | Prompt contract in `opencode.json` instructions |

**Principle**: Combine static profiles (Steps 2–3) with dynamic checkpoints (this step).
- Platforms with pre-tool hooks (Claude Code, Gemini): use the hook script.
- Platforms without (Codex, OpenCode): rely on `approval_policy` and explicit prompt contracts that instruct the agent to output `CHECKPOINT_NEEDED: <reason>` and wait before proceeding with Tier 1 actions.

See [references/permission-profiles.md](./references/permission-profiles.md) for full hook script templates per platform.

## Examples

### Example 1: Claude Code sandbox run

Use the Claude sandbox preset from [references/permission-profiles.md](./references/permission-profiles.md), then run Ralph only inside that isolated repo:

```bash
/ralph "fix all failing tests" --max-iterations=10
```

### Example 2: Codex CLI sandbox Ralph run

For sandbox ralph runs, use the CLI flags directly:

```bash
codex -c model_reasoning_effort="high" --dangerously-bypass-approvals-and-sandbox -c model_reasoning_summary="detailed" -c model_supports_reasoning_summaries=true
```

For repo-scoped (non-sandbox) runs, use the config file approach from [references/permission-profiles.md](./references/permission-profiles.md):

```toml
approval_policy = "never"
sandbox_mode = "workspace-write"
```

Place this in `~/.codex/config.toml` (or a project-local override) and restart Codex before running Ralph.

### Example 3: Gemini CLI sandbox or trust-only setup

For sandbox ralph runs, use `--yolo` mode:

```bash
gemini --yolo
```

For normal repo automation, trust the current project folder with explicit file selection and run the Ralph workflow for that repo only. See [references/permission-profiles.md](./references/permission-profiles.md) for details.

## Best practices

- Default to the least-permissive preset that still lets Ralph finish end-to-end.
- Keep secret denylists and destructive command denylists even when approvals are reduced.
- Use full bypass only in disposable environments with a clear project boundary.
- Record which preset was applied so teammates can reproduce or revert it.
- Re-check platform docs when upgrading CLI versions because permission models change faster than skill content.

## References

- [What are Agent Skills?](https://agentskills.io/what-are-skills)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Permission Profiles](./references/permission-profiles.md)
- [Claude Code permissions](https://docs.anthropic.com/en/docs/claude-code/iam#permission-modes)
- [Codex configuration and rules](https://developers.openai.com/codex/cli/config)
- [ChatGPT Codex sandbox and approval modes](https://help.openai.com/en/articles/11997270-codex-in-chatgpt)
- [Gemini CLI trusted folders](https://github.com/google-gemini/gemini-cli/blob/main/docs/trusted-folders.md)
