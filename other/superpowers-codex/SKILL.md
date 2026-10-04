---
name: superpowers-codex
description: >
  OpenAI Codex CLI wrapper — three modes. Review: independent diff review with
  pass/fail gate. Challenge: adversarial mode that tries to break your code.
  Consult: ask Codex anything with session continuity. Use when asked to
  "get a second opinion", "run codex", "cross-model review", or "adversarial test".
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
---

> **DEPRECATED** — use `/codex` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Codex — Cross-Model Review & Challenge

**Purpose:** Invoke OpenAI Codex CLI for independent code review, adversarial
challenge, or consultation. Provides session continuity and structured output.

**Requires:** Codex CLI (`which codex`)

---

## Modes

| Mode | Command | Purpose |
|------|---------|---------|
| **Review** | `codex review --base <branch>` | Independent diff review with pass/fail gate |
| **Challenge** | `codex challenge` | Adversarial — find ways the code will fail |
| **Consult** | `codex consult` | Ask Codex anything with session continuity |

---

## Step 1: Detect Codex

```bash
which codex 2>/dev/null && echo "CODEX_AVAILABLE" || echo "CODEX_NOT_AVAILABLE"
```

If `CODEX_NOT_AVAILABLE`: AskUserQuestion:
> "Codex CLI is not installed. Options:
> - A) Open Codex setup instructions in browser
> - B) Use a Claude subagent for independent review instead
> - C) Cancel"

If A: `open https://docs.codex.dsp.net/`
If B: skip to Step 2B (Claude subagent fallback)

---

## Step 2A: Codex Review Mode

### Run review
```bash
BASE_BRANCH="${1:-main}"
TMPERR=$(mktemp /tmp/codex-review-XXXXXXXX)
TMPOUT=$(mktemp /tmp/codex-review-out-XXXXXXXX)
codex review --base "$BASE_BRANCH" 2>"$TMPERR" | tee "$TMPOUT"
```

### Parse results
Read `$TMPERR` for stderr (errors, auth issues).
Read `$TMPOUT` for review output.

### Pass/Fail Gate
Parse findings. Gate: **P1 issues = FAIL**, everything else = PASS.

```
CODEX REVIEW GATE
=================
P1 (Critical): N — {list}
P2 (High): N
P3 (Medium): N
P4 (Low): N
GATE: PASS / FAIL
```

If FAIL: ask via AskUserQuestion whether to fix P1 issues before proceeding.

### Cost estimation
From token counts in output (if available):
```bash
ESTIMATED_COST=$(cat "$TMPOUT" | grep -i "cost\|tokens" | head -3)
echo "Estimated cost: $ESTIMATED_COST"
```

---

## Step 2B: Codex Challenge Mode

### Prompt construction
Read the diff or target file:
```bash
git diff --stat
DIFF_SIZE=$(git diff --stat | tail -1)
echo "Diff size: $DIFF_SIZE"
```

### Run challenge
```bash
TMPERR=$(mktemp /tmp/codex-challenge-XXXXXXXX)
TMPOUT=$(mktemp /tmp/codex-challenge-out-XXXXXXXX)
codex exec "You are a brutal security researcher. Find ways this code will fail in production.
Focus on: race conditions, nil pointer dereference, SQL injection, auth bypass, data corruption,
memory leaks, denial of service, and subtle logical errors. Be specific — cite file and line.
DO NOT suggest style improvements. Find BREAKAGE." \
  -s read-only -c 'model_reasoning_effort="xhigh"' \
  --enable web_search_cached 2>"$TMPERR" | tee "$TMPOUT"
```

5-minute timeout. Read stderr after:
```bash
cat "$TMPERR" && rm -f "$TMPERR" "$TMPOUT"
```

### Present findings
```
CODEX CHALLENGE FINDINGS
========================
{full verbatim output}
```

### Error handling:
- Auth failure: "Codex auth failed. Run `codex login` to authenticate."
- Timeout: "Codex timed out after 5 minutes."
- Empty response: "Codex returned no response."

---

## Step 2C: Codex Consult Mode

### Session management
```bash
SESSION_FILE=~/.claude/.context/codex-session-id
if [ -f "$SESSION_FILE" ]; then
  SESSION_ID=$(cat "$SESSION_FILE")
  echo "Continuing session: $SESSION_ID"
else
  echo "Starting new session"
fi
```

### Run consult
```bash
TMPERR=$(mktemp /tmp/codex-consult-XXXXXXXX)
TMPOUT=$(mktemp /tmp/codex-consult-out-XXXXXXXX)
QUESTION="${1:-}"
codex exec "$QUESTION" \
  -s read-only -c 'model_reasoning_effort="xhigh"' \
  --enable web_search_cached 2>"$TMPERR" | tee "$TMPOUT"
```

### Save session ID
```bash
cat "$TMPOUT" | grep -i "session\|id" | head -1 > "$SESSION_FILE" 2>/dev/null || true
```

### Present output
```
CODEX SAYS
==========
{full verbatim output}
```

---

## Plan Review Mode (auto-detected)

If reviewing a plan file, prefix the prompt:
```
You are a brutally honest technical reviewer examining a development plan.
Your job is to find what it missed: logical gaps, unstated assumptions,
overcomplexity, feasibility risks, missing dependencies.
Be direct. Be terse. No compliments. Just the problems.
```

---

## Cross-Model Comparison (if Claude review exists)

If a Claude review has been done in this session, compare findings:

```
CROSS-MODEL ANALYSIS
=====================
Codex found: {list}
Claude found: {list}
Overlap: {shared findings}
Codex-only: {unique findings}
Claude-only: {unique findings}

TENSION POINTS:
{where models disagree}
```

For each substantive tension: offer to add to TODOs via AskUserQuestion.

---

## Review Log

```bash
mkdir -p ~/.claude/.context
echo '{"skill":"codex-review","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","status":"STATUS","mode":"'"$MODE"'","gate":"'"$GATE"'","findings":N,"findings_fixed":N}' >> ~/.claude/.context/reviews.jsonl
```

---

## Codex Auth Setup

If auth errors occur:
```bash
codex auth status 2>/dev/null || codex login
```

If login fails: direct user to `https://docs.codex.dsp.net/` for setup.

---

## Completion Status

- **DONE** — Review/challenge/consult complete, findings presented
- **DONE_WITH_CONCERNS** — Codex returned partial results or errors
- **BLOCKED** — Codex not available or auth failed
- **NEEDS_CONTEXT** — No diff or question provided
