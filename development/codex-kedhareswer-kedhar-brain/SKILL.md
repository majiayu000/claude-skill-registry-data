---
name: codex
description: >
  Enables Claude Code to invoke the Codex CLI (`codex exec` and session resumes) for automated
  code analysis, refactoring, and editing workflows. Triggers on any request to use Codex —
  "use Codex to...", "run Codex on...", "analyze with Codex", "have Codex look at...",
  "let Codex handle...", "Codex review...", "send this to Codex", etc.
---

# Codex Integration

Delegates code analysis, refactoring, and editing tasks to the Codex CLI from within Claude Code.

## Prerequisites

Verify both Codex and its version are usable:

```bash
codex --version 2>&1 || echo "CODEX_NOT_FOUND"
```

- If `CODEX_NOT_FOUND` → tell the user to install Codex CLI and add it to PATH.
- Store the version string for later reference (flag compatibility).

## Workflow

### 1. Discover Current Model

Parse the configured model — don't just dump the file:

```bash
grep -E '^model\s*=' ~/.codex/config.toml 2>/dev/null | head -1 | sed 's/.*"\(.*\)"/\1/'
```

- If the file is missing or the grep returns nothing → tell the user: "No Codex config found. Run `codex` once to generate `~/.codex/config.toml`, or tell me which model to use."
- Never hardcode model names. Models change with each Codex update.

### 2. Ask the User via AskUserQuestion

Use the `AskUserQuestion` tool **twice in sequence** (one question per call):

**Call 1 — Model selection:**
- Title: "Which model should Codex use?"
- Option 1: `{discovered_model} (current)` — "Your configured default"
- Option 2: any alternative model found in config history
- Always include **Other** so the user can type a custom model name

**Call 2 — Reasoning effort:**
- Title: "What reasoning effort?"
- Option 1: `medium` — "Balanced (default)"
- Option 2: `low` — "Quick, surface-level"
- Option 3: `high` — "Deep, thorough — slower but more detailed"

Wait for both answers before proceeding.

### 3. Determine Sandbox Mode

Use this explicit mapping — do NOT guess:

| Task keywords | Sandbox | Confirm? |
|---|---|---|
| analyze, review, check, audit, explain, read, inspect, compare | `read-only` | No |
| refactor, edit, write, fix, update, rename, move, add, create | `workspace-write` | No |
| install, deploy, run, execute, delete, rm, drop, full access | `danger-full-access` | **Always confirm** |

If ambiguous, default to `read-only` and tell the user: "I'm using read-only sandbox. Say 'allow writes' if Codex needs to modify files."

### 4. Build the Command

```bash
codex exec \
  -m {model} \
  -c model_reasoning_effort={effort} \
  -s {sandbox} \
  "{prompt}"
```

**Prompt enrichment** — Before passing the user's raw request, prepend project context:

```
Project: {repo_name} ({git_branch})
Working directory: {cwd}
---
{user's original request}
```

This gives Codex awareness of where it's operating.

### 5. Execute and Handle Output

Run via Bash **with stderr captured** (not suppressed):

```bash
codex exec -m {model} -c model_reasoning_effort={effort} -s {sandbox} "{prompt}" 2>&1
```

**Error handling — check exit code:**
- Exit 0 → relay output verbatim to user
- Exit non-zero → show the error and diagnose:

| Error pattern | Diagnosis |
|---|---|
| `command not found` | Codex CLI not installed or not on PATH |
| `auth` / `token` / `401` / `403` | Run `codex login` to re-authenticate |
| `unknown model` / `invalid model` | Model name is wrong — re-check config or ask user |
| `permission` / `sandbox` | Sandbox too restrictive — offer to escalate |
| `timeout` | Codex took too long — suggest reducing scope or lowering effort |

**Output size guard:**
- If output exceeds ~4000 characters, summarize the key findings in 5–10 bullet points
- Offer: "Full output is long. Want me to save it to a file?"

### 6. Post-Execution (Feedback Loop)

After relaying Codex output, **don't just stop**. Offer next steps:

- If Codex found issues → "Want me to fix these?"
- If Codex suggested changes → "Should I apply these edits?" (re-invoke with `workspace-write`)
- If analysis was broad → "Want me to dig deeper into any specific finding?"
- If Codex refactored code → "Want me to run your tests to verify?"

This turns a one-shot delegation into an iterative workflow.

### 7. Session Resumption

```bash
codex exec resume --last
# or by session ID:
codex exec resume {session-id}
```

Trigger on: "continue", "resume", "follow up", "pick up where Codex left off", "last session".

## Common Issues

| Problem | Fix |
|---------|-----|
| `command not found: codex` | Install Codex CLI, add to PATH |
| Auth error / expired token | Run `codex login` |
| Unknown model | Re-read `~/.codex/config.toml` — model names change across versions |
| Sandbox permission denied | Escalate: `read-only` → `workspace-write` → `danger-full-access` (confirm) |
| No config.toml found | Run `codex` once to generate it, or specify model manually |
| Output is empty | Check stderr — likely a silent failure. Re-run with `2>&1` |
| Codex hangs / times out | Reduce scope of the prompt or lower reasoning effort |
