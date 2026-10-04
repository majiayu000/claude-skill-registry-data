---
name: autoloop
description: Run a long multi-round task that survives Claude usage limits — set up a shared state file + stop marker, then launch the local autoloop watchdog that resumes the session automatically after every limit window. Use when the user wants an unattended loop ("รัน loop ยาว", "ทำต่อเองหลังติดลิมิต", "run overnight", "keep going after usage limit") on a LOCAL project.
argument-hint: "what long-running task should the loop work on?"
---

# autoloop — drive a Claude Code session across usage limits

You are setting up an **unattended local loop**: a watchdog (`autoloop`) repeatedly resumes ONE Claude Code session headlessly, round by round. When the subscription usage limit hits, the watchdog parses the real reset time from Claude's own output, sleeps past it (fallback: +5h), and resumes — until a **stop marker** appears in a shared state file.

The engine lives where this skill was installed — find the repo root (the folder containing `bin/autoloop.mjs`). If the user installed via `npx skills add`, ask them where they cloned/keep it, or check common locations (`F:\claude-autoloop`, `~/claude-autoloop`).

## Contracts (explain these to the user)

1. **Work state file** (e.g. `docs/BUILD-STATE.md`) — the plan/checklist. The *working session* updates it every round. The watchdog only reads it, looking for the stop marker.
2. **Stop marker** (default `AUTOLOOP: COMPLETE`) — when the work is done, the working session must write this exact string into the state file (and/or say it in its reply). That is the ONLY clean finish signal.
3. **Runtime sidecar** `<state-file>.autoloop.json` — written by the watchdog automatically (pid, cycles, limitedAt, resumeAt, status). Never edit; safe to delete when not running.
4. **One driver per session** — while autoloop runs, nobody may manually resume that same session (no interactive chat, no second autoloop).

## Setup steps

1. **Prepare the state file** — if none exists, create one WITH the user: a markdown checklist of work units + a line documenting the agreed stop marker. The plan must instruct: *work 1–2 units per round → verify → commit → update this file → end the turn; when everything is checked, append the stop-marker line.*
2. **Identify the target session** — run `node <root>/bin/autoloop.mjs list`. ⚠️ Always pass `--session <id>` explicitly: `--continue` grabs the newest session in the cwd, which is often the wrong chat (e.g. the one you're in right now).
3. **Write the round prompt to a file** (`--prompt-file`) so the user can hot-edit it mid-run. Template:

   ```
   Recover first: git status — if a previous round died mid-work, finish it (verify + commit) before anything new.
   Then continue per <PLAN_FILE> from the state in <STATE_FILE>: do 1-2 work units, verify (typecheck/tests/e2e as the plan says), commit locally (do NOT push unless the plan says so), update <STATE_FILE>, then END YOUR TURN.
   If every item through the final gate is checked, append the line "AUTOLOOP: COMPLETE" to <STATE_FILE> and reply only: AUTOLOOP: COMPLETE
   ```

4. **Launch detached** (Bash tool):

   ```
   node <root>/bin/autoloop.mjs start \
     --cwd "<project dir>" \
     --session <session-id> \
     --state-file "<state file>" \
     --prompt-file "<prompt file>" \
     --permission-mode acceptEdits \
     --max-cycles 20 --max-waits 10 \
     --fallback-wait-min 300
   ```

   Permission notes: headless runs can't answer permission prompts. `acceptEdits` + the project's existing `.claude/settings.local.json` allowlist usually suffices. **Never** suggest `--dangerously-skip-permissions`. Recommend a first test with `--max-cycles 1`, then check the log for denied tools.

4b. **Notifications (optional but recommended for overnight runs)** — if `<root>/autoloop.secrets.json` exists (or TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID env), autoloop notifies on: start, limit-hit (with wake time), resumed, done, error, stopped. Verify with `node <root>/bin/autoloop.mjs notify-test` before a long run. Never read or echo the secrets file contents.

5. **Tell the user how to watch/stop:**
   - `node <root>/bin/autoloop.mjs status --state-file "<state file>"`
   - `node <root>/bin/autoloop.mjs stop   --state-file "<state file>"`
   - log: `<state-file>.autoloop.log`

## Failure modes to warn about

- Round died mid-work → next round's "recover first" line handles it (that's why it must stay in the prompt).
- Claude exits with a non-limit error → autoloop stops on purpose (never blind-loops); user reads the log tail from `status`.
- maxCycles reached before the marker → not an error; user restarts with a higher cap after reviewing progress.
