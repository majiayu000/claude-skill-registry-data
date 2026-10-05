---
name: jarvis-reset
description: Deletes the jarvis watch's local state (.jarvis/baseline·args·status·stopped) for a full reset, and — after a confirmation — the plan/checklist (.jarvis/plan.md·checklist.md). The next /loop /jarvis starts from a first boot (banner, plan opt-in, strength question). This does not stop the loop itself — it is an independent command that just clears the accrued tracking and saved settings. Use on requests like "reset jarvis", "jarvis reset", "clear the watch state", "start over".
---

# jarvis-reset

**Resets the local state** of the `jarvis` watch. It deletes the state files in `.jarvis/` (`baseline`·`args`) to **discard all accrued change tracking and the saved settings**, and — only after you confirm — the **plan/checklist** (`plan.md`·`checklist.md`). The next time you launch `/loop /jarvis`, it starts fresh as if on a first boot (start banner + plan opt-in + strength question).

> ⚠️ **This is not a command to stop the loop.** To stop a running watch, interrupt the `/loop` itself (Esc). `jarvis-reset` is **independent** of that and only clears *state*. Use it when you want a clean restart after stopping.

## Why an independent command

`/loop /jarvis` continues from `.jarvis/baseline`·`args` if they are present (that is what "resume" means). So when you want "fresh from scratch," you must explicitly clear that state — which is this skill's job. Loop termination (Esc) has no teardown hook, so a reset only ever happens via this **separate command**.

## Procedure

1. **Delete the watch state files in bulk** (per-tick, safe to always remove):

   ```bash
   rm -f .jarvis/baseline .jarvis/args .jarvis/status .jarvis/stopped .jarvis/paused
   ```

   - `.jarvis/status` is the liveness state file; deleting it clears the statusline immediately (shows watch not running).
   - `.jarvis/stopped` is the event stopped-flag dropped by the Stop hook; delete it too (harmless if absent).
   - `.jarvis/paused` may be a leftover from an older version; delete it too (harmless if absent).
   - The `.jarvis/` directory itself may be left in place (there may be other caches). Even if empty, there is no need to delete it.

2. **Plan & checklist — confirm before deleting.** Unlike the one-line state files, `.jarvis/plan.md` and `.jarvis/checklist.md` are **durable work** the human authored/approved. If either exists, **ask first** (`AskUserQuestion` or a plain confirm): *"Also delete the plan and checklist? This can't be undone."*
   - **Yes** → `rm -f .jarvis/plan.md .jarvis/checklist.md` (next start re-asks the plan opt-in).
   - **No** → leave them; the next `/loop /jarvis` resumes plan mode against the existing checklist (baseline was cleared, so it re-measures from scratch, but the plan/checklist stay).
   - If neither file exists, skip this step silently.

3. **Report** (one line): `🧹 Jarvis state reset. To turn it back on, /loop /jarvis (starts fresh from the banner, plan opt-in, and strength question).`

## Natural-language triggers

Handle reset intents like "reset jarvis", "jarvis reset", "clear the watch state", "start over" with this skill. If the nuance is only *stopping* ("just stop", "pause for a bit"), tell the user to interrupt the loop (Esc) — leaving the state in place lets `/loop /jarvis` resume from where it left off.

## What it does not do

- Does not directly stop a running `/loop` (that's Esc's job).
- Does not touch code/changes in the user's working tree — it only deletes the `.jarvis/` control files.

## References
- Watch core: `.claude/skills/jarvis/SKILL.md` ("control state files" table, start-time resume & self-correction)
