---
name: codex-collab
version: 2.0.0
description: |
  Background dual-agent collaboration with Codex CLI. Sends tasks to Codex
  via `codex exec` in the background, captures JSONL output, and integrates
  results without blocking Claude Code. No tmux, no Terminal windows.
  Use when asked to "codex collab", "dual agent", "pair with codex", "codex tmux",
  "collaborate with codex", "let codex help", or "spiral coding".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# /codex-collab — Claude + Codex Background Collaboration

You are running the `/codex-collab` skill. This sends tasks to Codex CLI
via `codex exec --full-auto --json` in the **background**, captures structured
JSONL output, and integrates results — all without blocking Claude Code or
opening any extra windows.

This is NOT the same as `codex:codex-rescue` (which uses the shared Codex
runtime). This skill runs a standalone Codex process per task.

---

## Architecture

```
 Claude Code (foreground)              Codex (background process)
 ┌──────────────────────┐              ┌──────────────────────┐
 │                      │   Bash bg    │                      │
 │  Send task ──────────────────────►  │  codex exec          │
 │                      │              │  --full-auto --json  │
 │  Continue working    │              │  > output.jsonl      │
 │  on other things     │              │                      │
 │                      │   Read file  │  Writes JSONL events │
 │  Read results  ◄────────────────── │  to output file      │
 │                      │              │                      │
 │  Integrate & iterate │              └──────────────────────┘
 └──────────────────────┘
```

Key advantages over v1 (tmux-based):
- **No Terminal windows opened** — zero visual clutter
- **Non-blocking** — Claude Code continues while Codex works
- **Structured output** — JSONL events, no TUI scraping
- **Reliable** — no Ink TUI quirks, no tmux send-keys timing issues

---

## Step 0: Preflight

Check that codex is available:

```bash
CODEX_BIN=$(which codex 2>/dev/null || echo "")
echo "codex: ${CODEX_BIN:-NOT_FOUND}"
codex --version 2>/dev/null || true
```

If codex is `NOT_FOUND`, stop and tell the user:
- codex: `npm install -g @openai/codex` or `bun install -g @openai/codex`

---

## Step 1: Determine Working Directory

Use the current working directory or the git repository root:

```bash
WORK_DIR=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
echo "WORK_DIR: $WORK_DIR"
```

**Important**: `codex exec` requires being inside a git repository. If the
working directory is not a git repo, warn the user.

---

## Step 2: Create Session Directory

Each collaboration session gets a directory under `/tmp/codex-collab/`:

```bash
SESSION_ID=$(date +%s)
SESSION_DIR="/tmp/codex-collab/$SESSION_ID"
mkdir -p "$SESSION_DIR"
echo "SESSION_DIR: $SESSION_DIR"
```

---

## Step 3: Send a Task to Codex (Background)

To send a task to Codex, use the Bash tool with `run_in_background: true`.
This is the key difference from v1 — Claude Code is NOT blocked.

The command pattern:

```bash
TASK_ID=1  # increment for each task in the session
echo '<prompt_text>' | codex exec \
  --full-auto \
  --json \
  --ephemeral \
  -C "$WORK_DIR" \
  > "$SESSION_DIR/task_${TASK_ID}.jsonl" \
  2> "$SESSION_DIR/task_${TASK_ID}.err"
echo "CODEX_EXIT=$?" >> "$SESSION_DIR/task_${TASK_ID}.status"
```

**Critical rules for the prompt:**
- Use single quotes around the prompt text in the echo to avoid shell expansion
- For prompts containing single quotes, use a heredoc instead:
  ```bash
  codex exec --full-auto --json --ephemeral -C "$WORK_DIR" \
    > "$SESSION_DIR/task_${TASK_ID}.jsonl" \
    2> "$SESSION_DIR/task_${TASK_ID}.err" \
    << 'PROMPT'
  Your prompt text here, can contain any characters
  PROMPT
  echo "CODEX_EXIT=$?" >> "$SESSION_DIR/task_${TASK_ID}.status"
  ```

**Always use `run_in_background: true`** for the Bash tool call so Claude Code
can continue working while Codex processes the task.

Tell the user:

> Codex 任务 #N 已在后台启动，你可以继续其他工作。稍后我会检查结果。

---

## Step 4: Check Task Status

When you need the result (or are notified the background task completed),
read the output files:

```bash
# Check if task is done
cat "$SESSION_DIR/task_${TASK_ID}.status" 2>/dev/null || echo "STILL_RUNNING"
```

If `STILL_RUNNING`, the background Bash command hasn't completed yet. You'll be
notified automatically when it finishes — do NOT poll or sleep.

---

## Step 5: Extract the Response

Once the task is complete, read the JSONL output:

```bash
cat "$SESSION_DIR/task_${TASK_ID}.jsonl"
```

Parse the JSONL events. The key event types:
- `{"type":"thread.started","thread_id":"..."}` — session started
- `{"type":"turn.started"}` — a turn began
- `{"type":"item.completed","item":{"type":"agent_message","text":"..."}}` — Codex's response text
- `{"type":"item.completed","item":{"type":"tool_call",...}}` — Codex executed a tool
- `{"type":"item.completed","item":{"type":"tool_output",...}}` — tool output
- `{"type":"turn.completed","usage":{...}}` — turn finished with token usage

Extract the `agent_message` text from `item.completed` events. That is
Codex's response.

If there are errors, check:

```bash
cat "$SESSION_DIR/task_${TASK_ID}.err"
```

Present the response to the user:

```
Codex 回复 (任务 #N):
────────────────────────────────────────
<extracted response>
────────────────────────────────────────
```

---

## Step 6: Spiral Collaboration Loop

After receiving Codex's response:

1. **Analyze**: Read and understand what Codex said
2. **Synthesize**: Combine Codex's insight with your own analysis
3. **Act or Iterate**:
   - If you and Codex agree -> execute the plan (edit files, run tests, etc.)
   - If you disagree -> explain the disagreement to the user, ask for direction
   - If more context needed -> send a follow-up task to Codex (new task ID)
   - If Codex found something you missed -> investigate it yourself first

**Collaboration patterns:**

- **Divide and conquer**: You handle file A, send Codex to review file B
- **Verify**: You implement, send Codex to review your changes
- **Brainstorm**: You propose approach A, ask Codex for alternatives
- **Debug**: You share error context, ask Codex for diagnosis
- **Challenge**: Ask Codex to find holes in your implementation

For each iteration, increment the task ID and go back to Step 3.

**Important**: Since each `codex exec` is a fresh process, you must include
sufficient context in each prompt. Codex does NOT remember previous tasks.
Include relevant file paths, previous decisions, and constraints.

---

## Step 7: Cleanup

When the collaboration is complete:

```bash
rm -rf "$SESSION_DIR"
```

Tell the user: "Codex 协作已完成，临时文件已清理。"

---

## Prompt Composition Guidelines

When sending prompts to Codex:

1. **Be an operator, not a collaborator.** Give Codex clear, scoped tasks.
2. **Provide context inline.** Tell Codex which files to look at by path.
3. **One task per message.** Don't bundle multiple unrelated questions.
4. **Be specific about output format.** Tell Codex what you want back:
   a diff, a list of issues, a yes/no verdict, etc.
5. **Include the working directory context.** Codex runs with `-C $WORK_DIR`
   so it can read files in the repo, but explicit paths help.

Example prompts:
- "Review src/auth.ts for security issues. Focus on token handling. List each issue with file:line and severity."
- "What's the simplest way to add rate limiting to the /api/chat endpoint? Return a concrete implementation plan."
- "Find all places where we catch errors but don't log them. Return file paths and line numbers."
- "Read the diff in CHANGES.md and write a changelog entry for it."

---

## Error Handling

- **Codex not in git repo**: Ensure `-C` points to a git repository
- **Codex exec fails**: Check the `.err` file for error details
- **Timeout**: `codex exec` has no built-in timeout. If a task seems stuck
  (background process not completing after 10+ minutes), inform the user
  and consider killing the process
- **Multiple concurrent tasks**: Each task gets its own files in `$SESSION_DIR`,
  so multiple background tasks can run simultaneously without conflict

---

## Important Rules

- **Non-blocking**: ALWAYS use `run_in_background: true` when sending tasks to Codex.
  Claude Code should NEVER block waiting for Codex.
- **No Terminal windows**: NEVER use `open -a Terminal`, `osascript`, or any
  command that opens GUI windows. Everything runs headlessly.
- **No tmux**: This skill does NOT use tmux. All interaction is through
  `codex exec` and file I/O.
- **Transparency**: Always show the user what you're sending to Codex and
  what Codex responded. No hidden conversations.
- **No blind trust**: Codex's suggestions should be verified. Don't apply
  changes without understanding them first.
- **Keep it focused**: Each Codex task should have a clear purpose.
  Don't send vague "what do you think?" messages.
- **Context per task**: Each `codex exec` is stateless. Include all
  necessary context in each prompt.
