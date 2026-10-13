---
name: codex-2nd
description: "Get a second opinion from OpenAI Codex CLI on a plan or approach. Use when: (1) During planning phase of /x-as-pr or /x-wt-teams to validate the approach, (2) User says 'codex 2nd', 'second opinion', or 'codex opinion', (3) Wanting an alternative perspective before committing to a plan. Sends context and plan to codex, returns feedback. Called automatically by /x-as-pr and /x-wt-teams during planning."
allowed-tools:
  - Bash(bash $HOME/.claude/scripts/codex-guard.sh *)
  - Bash(node *)
  - Bash(timeout *)
  - Bash(gtimeout *)
---

# Codex 2nd Opinion

Get a second opinion from the codex plugin companion script on a plan, approach, or codebase exploration. Codex reads workspace files and does web research to provide an independent perspective.

## Codex Plugin Companion Script

The codex plugin provides a companion script for running tasks. Resolve it dynamically:

```bash
CODEX_PLUGIN_ROOT=$(command ls -d "$HOME/.claude/plugins/cache/openai-codex/codex"/*/ 2>/dev/null | sort -V | tail -1)
CODEX_COMPANION="${CODEX_PLUGIN_ROOT}scripts/codex-companion.mjs"
```

If the file does not exist, report "Codex plugin not installed — skipping second opinion" and continue without it.

Usage for second opinion tasks:

```bash
node "$CODEX_COMPANION" task -- "<prompt>"
```

**The `--` is load-bearing — do not remove it.** `codex-companion.mjs` shell-splits the prompt back into tokens when it is the *only* argument (`normalizeArgv`), and then reads any token starting with `-` as an option: a prompt merely *mentioning* `-m` sets `--model` to the next word and drops both from the text the model sees. `--` stops option parsing and keeps the prompt one argument.

The `task` command runs Codex in read-only mode by default (no `--write` flag).

## Process

### Step 0: Pre-flight Rate Limit Check

Before doing anything, check if Codex is currently rate-limited:

```bash
RATE_CHECK=$(node $HOME/.claude/scripts/codex-rate-limit.js check 2>&1)
RATE_EXIT=$?
```

If `RATE_EXIT` is non-zero (rate-limited), **silently fall back to Opus** (see Step 5 Fallback). Do NOT report the rate limit to the user or pause the workflow.

### Step 1: Build Context Prompt

Construct a prompt that includes:

- The current plan or approach being considered
- Key files or areas of the codebase involved
- Specific questions or concerns to address

```
You are reviewing a development plan. Provide a second opinion.

## Context
<what the project is, what repo we're in>

## Current Plan
<the plan or approach being considered>

## Questions
1. Are there any risks, edge cases, or issues with this approach?
2. Is there a simpler or better alternative?
3. Are there any files or areas of the codebase that should be considered but aren't mentioned?
4. Any other suggestions or concerns?

Be concise and practical. Focus on actionable feedback. If the plan looks solid, say so briefly — don't invent problems.
```

### Step 2: Run Codex

> **MUST run in the background.** Call the Bash tool with `run_in_background: true`.
> The Bash tool's foreground timeout is capped at **600000 ms (10 minutes)** — a larger
> `timeout` argument is silently clamped, so a foreground run is SIGKILLed at 10 minutes
> no matter what `gtimeout` is set to, leaving a 0-byte output file and an orphaned
> `codex-companion.mjs` process. Backgrounded commands are not subject to that cap.
>
> After launching, wait for the task-completion notification (or poll the output file),
> then continue at Step 3. If a foreground run was started by mistake and got killed,
> clean up the orphan before retrying:
> `pkill -f 'codex-companion.mjs'`

```bash
LOGDIR=$(node $HOME/.claude/scripts/get-logdir.js)
mkdir -p "$LOGDIR"
DATETIME=$(date +%Y%m%d_%H%M%S)

# Resolve codex companion script
CODEX_PLUGIN_ROOT=$(command ls -d "$HOME/.claude/plugins/cache/openai-codex/codex"/*/ 2>/dev/null | sort -V | tail -1)
CODEX_COMPANION="${CODEX_PLUGIN_ROOT}scripts/codex-companion.mjs"

# Detect timeout command (gtimeout on macOS via coreutils, timeout on Linux/WSL)
if command -v gtimeout &>/dev/null; then
  TIMEOUT_CMD="gtimeout"
elif command -v timeout &>/dev/null; then
  TIMEOUT_CMD="timeout"
else
  TIMEOUT_CMD=""
  echo "WARNING: neither gtimeout nor timeout found. Running without timeout."
fi

bash $HOME/.claude/scripts/codex-guard.sh --wait 300 -- \
  ${TIMEOUT_CMD:+$TIMEOUT_CMD} ${TIMEOUT_CMD:+1800} node "$CODEX_COMPANION" task -- \
  "<prompt>" \
  > "$LOGDIR/${DATETIME}-codex-2nd.md" \
  2>"$LOGDIR/${DATETIME}-codex-2nd-stderr.log"
```

Long prompts: write the prompt to a file first and pass it as
`PROMPT=$(cat <prompt-file>)` … `task -- "$PROMPT"`, rather than inlining a multi-hundred-line
heredoc into the command.

**Timeout: 30 minutes (1800s), enforced by `gtimeout`/`timeout` inside a backgrounded
Bash call.**

### Step 3: Collect Results

1. Check for rate limiting in output files:

   ```bash
   node $HOME/.claude/scripts/codex-rate-limit.js check-output \
     "$LOGDIR/${DATETIME}-codex-2nd.md" \
     "$LOGDIR/${DATETIME}-codex-2nd-stderr.log"
   ```

   If rate limit detected, jump to **Step 5 Fallback** (Opus second opinion).

2. Read the output file
3. If empty or missing, check stderr log for errors
4. If codex timed out or failed, jump to **Step 5 Fallback**

### Step 4: Return Feedback

Return the codex feedback to the caller. The caller decides whether to incorporate it into the plan.

### Step 5: Fallback — Opus second opinion

If codex was rate-limited, timed out, or produced no usable output, **silently fall back to Opus**. Spawn one general-purpose subagent with `model: opus` to give the same second opinion the codex prompt would have produced. The caller still gets advisory feedback — no quota-loud failure mode, no missing second opinion.

```
Agent tool:
  description: "Opus 2nd opinion (codex fallback)"
  subagent_type: "general-purpose"
  model: "opus"
  prompt: <same second-opinion prompt that would have gone to codex — plan/context + the standard questions>
```

Return the subagent's feedback to the caller exactly as if it came from codex. Do NOT mention the fallback to the user — silent means silent.

## Timeout Policy

- **Timeout**: 30 minutes (1800s), via `gtimeout`/`timeout`
- **MUST be backgrounded** (Bash `run_in_background: true`). The Bash tool clamps foreground `timeout` to 600000 ms, so any foreground run dies at 10 minutes with a 0-byte output file and an orphaned `codex-companion.mjs`
- **If codex times out**: Silently fall back to Opus (Step 5)
- **Fallback agent**: general-purpose subagent at `model: opus` — the caller always gets a second opinion, just from Opus instead of codex when codex is down. Opus is the designated Claude-side stand-in for codex throughout these skills

## When Called by /x-as-pr or /x-wt-teams

These skills call `/codex-2nd` during their planning phase:

1. After understanding the task and forming an initial plan
2. Send the plan to codex for feedback
3. If useful feedback is returned, update the plan
4. Optionally re-run `/codex-2nd` with the updated plan (up to 3 iterations total)
5. Finalize the plan and proceed with implementation

## Important Notes

- Codex reads workspace files for context — no need to paste file contents into the prompt
- All file writing done by Claude Code, never by codex
- This is advisory — never block the workflow if codex is unresponsive
- **Silent fallback policy**: If codex is rate-limited, timed out, or unavailable, silently fall back to an Opus general-purpose subagent (Step 5). NEVER pause the workflow, NEVER report the rate limit, NEVER ask what to do. The caller still gets a second opinion — just from Opus instead of codex
- NEVER use `~` in paths — use `$HOME`
