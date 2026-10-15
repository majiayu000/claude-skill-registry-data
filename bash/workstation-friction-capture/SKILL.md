---
name: workstation-friction-capture
description: >-
  Triage the workstation-tool frictions logged this session (failed `bun run convo|chips|secrets|lexicon|remind|review` or mcp__html-review__* calls) and report genuine structural defects as a chip or note. Only when the Stop hook blocks session end on a non-empty friction log. Never speculatively.
---

# Workstation Friction Capture

The workstation's own CLIs and MCP tools sometimes have structural bugs or
gaps that a session silently works around instead of reporting. A
`PostToolUse` hook (`workstation-friction-detect.mjs`) mechanically logs
every failed call to a workstation tool during the session, with zero
judgment; this skill applies the judgment, once, right before the session
actually stops. Full doctrine (triage criteria, dedup, 3-chip cap, audit-log
format): `/Users/elmabi/Desktop/my-projets/workstation/docs/workstation-friction-capture.md`.

## Step 1 — Read the friction log

The Stop hook's block message gives the exact path:
`~/.claude/friction/<session-id>.jsonl` — one JSON object per line
(`{ts, tool, commandTruncated, errorExcerpt, sessionId, cwd}`). `tool` is
`"Bash"` (a workstation CLI call) or an `mcp__html-review__*` tool name.

## Step 2 — Triage each entry

Classify transient/self-inflicted (typo'd flag, wrong argument, a retry
resolved it — skip) vs genuine structural defect (the tool's contract itself
is wrong or incomplete — report). Strict bar, ALL must hold: costs a FUTURE
session real time; reproducible in principle; not already known (Step 3).
Be stingy — a false positive costs a wasted chip; a missed one resurfaces
on its own next time. Full criteria and the counter-example: see the doc above.

## Step 3 — Dedup against open chips FIRST

`cd ~/Desktop/my-projets/workstation && bun run chips list --project workstation`
— skip anything already tracked (read with `bun run chips read <id>` if unsure).

## Step 4 — Report, capped at 3 chips per session

For each surviving candidate, in impact order, report as a suggested task:
`start_session` with `initiation: "own_initiative"`, title = imperative
phrase, prompt = self-contained (failing command, error excerpt, tool, and —
if known — where in the workstation codebase the behavior likely lives). Its
chip is filed under the session's project: when the session runs outside the
workstation, find it with `bun run chips list --project <session slug>` and
move it with `bun run chips update <id> --project workstation`. Or report a
note/reminder via the
hub when there's no clean fix yet (`bun run remind add "<texte>" --project
workstation`, or a `note`-kind item via `bun run convo create`). Hard cap:
3 per session — leave the rest for next time, the log line stays as evidence.

## Step 5 — Log the pass (mandatory, even at 0 candidates)

Run the deterministic logger exactly once:

```bash
node /Users/elmabi/Desktop/my-projets/workstation/.claude/skills/workstation-friction-capture/scripts/log-pass.mjs \
  --runtime claude --session <session-id> --found <N> --reported <M>
```

It appends `{ts, sessionId, found, reported}` to
`~/.claude/friction/capture-log.jsonl`, the journal the Stop hook reads.

`N` = total lines in the session's friction log. `M` = chips/notes actually
created in Step 4 (0 is a fully valid, expected outcome). Never silent.

**`found` is load-bearing, not bookkeeping.** The Stop hook re-blocks only when
the session log has GROWN past the `found` of the last logged pass — that line is
what tells it this pass happened and how much it covered. So count `N` as the
log's non-empty lines, NOT the entries you judged worth reporting: under-count it
and the hook nags again next turn about frictions you already triaged; over-count
it and a genuinely new friction later in the session goes unnoticed. Skip the log
entirely and the hook falls back on a coarse per-session time window — it stops
nagging either way, but you lose the precision.

## Step 6 — Stop normally

After Step 5 the pass is complete. End your turn normally — the Stop hook's
`stop_hook_active` guard prevents a second block this turn, and its progress
guard (the `found` you just logged) prevents one on later turns; no `.jsonl`
cleanup needed.
