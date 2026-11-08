---
name: health
description: "Use when something isn't working (panels or the daily greeting missing, a command does nothing), after installing, moving or updating the folder, or when the user asks \"is everything working\" or \"check my setup\". Read-only checkup of version, safety checks, panels and connections; offers fixes."
---

# /health

A read-only checkup. Nothing is changed while checking. At the end, offer fixes; make a change only after the user says yes to that specific fix.

## 1. Run the script

From the workspace folder:

- Mac, Linux, or Windows with Git Bash: `bash .claude/skills/health/scripts/health.sh` (add `codex` at the end when running in Codex).
- Windows: also run `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\health\scripts\health.ps1` (add `-App codex` in Codex). It has the Windows-only checks (Git Bash present, files Windows blocked as downloaded). If bash isn't available at all, run only this one.

The app may ask the user to allow the run; tell them that's expected and that the check only looks. Each line is `OK:`, `FIX:`, `NOTE:` (worth knowing, nothing broken) or `SKIP:` (not checked, and why). The last two lines are `summary:` and `most important:`.

If the script itself fails (an error instead of those lines, or it stops before `summary:`), say so plainly: the checkup script couldn't run, which usually means the app's own files are damaged or blocked. Quote the first error line, still do the checks in step 2, and treat it like "Safety check failed" in step 4. On Windows, try the PowerShell version if the bash one failed, and the other way round.

## 2. Checks only you can do

Add these to the results yourself:

- **Panels (Claude Code only).** Look at your own tool list for `interview_start` (it may be listed as a deferred tool you can load, which counts). Present: the panels are loaded. Missing: they didn't load. The usual reasons, most likely first: the folder isn't trusted (reopen it and click Trust), the Claude Code version is too old (the script's version line; the desktop app needs 2.1.286 or later, and its version shows when the user types `/status` in a Code tab session), or it's a WSL or VS Code chat session, where panels never show. Say plainly that everything still works in the chat without them. In Codex, skip this: Codex has no panels.
- **Gmail and Google Calendar.** Look at your tool list for Gmail tools (names containing `Gmail` or `gmail`) and Calendar tools (`Calendar` or `calendar`). Report each as connected or not connected. Not connected is fine; it only means `/sync-inbox`, Gmail drafts and adding interviews to the calendar aren't available. Never call these tools as part of the check.
- **Permission mode (Claude Code only).** The script can't see it. A hook (`.claude/hooks/mode-notice.sh`) already tells a Manual-mode session once, on its first message, how to switch; if that note appeared earlier in this session and you already passed it on, don't repeat the whole message here, just list it as a NOTE in one line. If your instructions say auto mode (or plan mode) is active, it's fine; don't mention it. Otherwise the session is probably in Manual mode (it asks before almost every edit and command; an older model, an admin setting, or a past choice in the desktop app's mode selector can cause it). Add it as a NOTE: "This session is set to ask before almost every step. To let me work without constant prompts, press Shift+Tab until it shows auto mode (in the desktop app, use the mode selector next to the prompt box). If auto mode isn't offered, your model or your organization doesn't allow it; /model can switch to a newer model." Changes to their master resume and preferences still ask in every mode, on purpose. In Codex, skip this.
- **Hooks in this session.** If you saw the session-start greeting text (today's date and the pipeline summary) at the start of this conversation, hooks ran in this session; that settles the "hooks running" line even if the script reported it old or "not confirmed". If you didn't see it, a "not confirmed" NOTE means the time stamp came from another session or the other app, so treat it as a FIX (hooks are probably off here); if the script says FIX, believe the FIX.

## 3. Report

Plain English, short, no file paths unless they help, no code:

1. One line: "Everything important is working" or "N things need fixing".
2. The FIX items as a short list, each with the plain fix. Then any NOTE items worth mentioning (skip notes the user can do nothing about). Don't list OK and SKIP lines unless the user asks; mention a SKIP only when it hides something they care about.
3. **The one most important fix**, in one sentence, and offer to help with it. Rank: the folder isn't the workspace root > a safety check failed, hooks are off, or Codex is too old for the safety checks > Git Bash missing (Claude Code on Windows; a Codex-only user doesn't need it, so it's only a note for them) or files blocked (Windows) > setup not done or starter files missing > Excel has the tracker open > app too old for panels > a routine stopped running > notes.
4. If the folder uses git and the git push check is off (a NOTE), offer once to turn it on: it's optional. Say why in one line: the built-in safety check only sees commands the assistant types, while this check also catches pushes made from scripts; it also keeps AI attribution lines out of commit messages.

## 4. Offering fixes (only after a yes)

- **Setup not done or starter files missing:** offer `/start`. It puts back only missing files and never overwrites theirs.
- **Git push check off:** with a yes, run `git config core.hooksPath .githooks` in the workspace, then run the health script again to confirm.
- **Blocked files (Windows):** with a yes, run `Get-ChildItem -Recurse | Unblock-File` in PowerShell in the workspace folder, then check again.
- **Excel lock:** ask the user to save and close the sheet in Excel; don't delete the `~$` file yourself (Excel removes it when it closes). No lock file doesn't prove the sheet is closed (Excel on a Mac often leaves none), so before changing the tracker still ask if it's open in Excel.
- **A routine stopped running:** follow the routines skill, "When a routine stops running", one step at a time. If the user paused or deleted it on purpose, log that there so it isn't flagged again (that log line is the only change; it needs no separate yes).
- **Hooks off, wrong folder, app too old, Git Bash missing, connectors:** these are steps the user takes in the app or on their computer. Give the steps from the script line, one at a time. Hooks switched off by "managed settings" can only be changed by whoever manages the computer (an employer or school IT); say so, and say not to connect Gmail in Claude Code until then.
- **Safety check failed, hook setup missing, files missing, script line endings:** don't try to repair product files by hand. Follow the script line: `/update` works only when the workspace has its VERSION file (and the user has a release zip or a download link); otherwise suggest downloading a fresh copy and moving their data over with `/my-data`. Until it's fixed, say not to connect Gmail.

Don't add a line to `history/activity.md` for a checkup; it changes nothing.
