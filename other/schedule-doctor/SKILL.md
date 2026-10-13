---
name: schedule-doctor
description: "Use when the user is about to schedule a Claude task, or asks why a scheduled task, /loop, cron job or routine did not run, ran late, or stopped partway (for example 'will this scheduled task actually run?', 'why didn't my 7am task fire?', 'check this before I schedule it')."
---

# Schedule Doctor

## Overview

Scheduled Claude tasks fail quietly: a run halts on a tool nobody pre-approved, a run is skipped because the computer slept (closing the lid still sleeps it), or one late catch-up run acts on stale data. This skill checks a task before it is scheduled, and explains afterwards why a run did not fire. Scripts do the checking and the classifying; the agent fetches task state through the scheduling tools, shows what the scripts found, and never names a cause the scripts did not.

## The scripts

In this skill's `scripts/` directory (use the base directory shown when the skill loads). Python 3 and the standard library only; use `python3`, or `python` / `py -3` if that is what works. All three are read-only.

- `preflight.py --prompt-file FILE [--guard-hours N] [--json]` lints a task prompt: the tools it likely needs (each marked `pre-approve` or `approve once with Run now`), whether it has a time guard (and a paste-ready one if not), and phrases like "today" or "latest" that a late run would read against the wrong date.
- `power_check.py [--json]` reads the OS sleep timeout and lid-close action (`powercfg` on Windows, `pmset` on macOS) and says whether the machine keeps awake unattended: yes, no or unknown.
- `diagnose.py --record FILE [--late-minutes N] [--json]` classifies one run record (shape below) into one verdict.

## Before a task is scheduled (pre-flight)

1. Get the prompt: from the user, or by reading the task through the surface's tool (table below). Save it to a scratch file outside the repo.
2. Run `preflight.py --prompt-file FILE --json`. Show the tool list as "likely needs", never "will need", and when it says none were detected, ask the user what the task touches instead of treating that as an all-clear. Offer to pre-approve the `pre-approve` tools in the user's permission settings; for `approve once with Run now` tools (git push, deleting, sending, deploying) say they should be approved once by running the task with Run now, not left permanently allowed.
3. A found guard is only a regex match: read it back to the user and confirm it really checks the time. If `time_guard.present` is false, ask the user how many hours of lateness is acceptable, rerun with `--guard-hours`, and show the snippet. Adding it is a prompt edit: show the diff and wait for an explicit yes in this conversation first.
4. Mention the staleness hints: those phrases are where a late run goes wrong even with a guard.
5. Run `power_check.py`. It reads the sleep timeout, the hibernate timeout and the lid-close action (including settings Windows hides). If `keeps_awake` is `no` or `unknown`, say what the findings show; `unknown` on a laptop usually means the lid setting could not be read. Then ask the user to confirm Claude Desktop's Keep computer awake setting, which the script cannot see.

## After a run did not fire (post-mortem)

1. Fetch the task and its latest run through the surface's tools (table below) and write the record to a scratch file outside the repo:

   ```json
   {
     "surface": "desktop | code-cron | routine",
     "scheduled_for": "ISO-8601",
     "started_at": "ISO-8601 or null",
     "ended_at": "ISO-8601 or null",
     "status": "string or null",
     "last_event": "string or null",
     "error_text": "string or null",
     "permission_denied_tool": "string or null",
     "machine_events": [{"kind": "sleep | hibernate | lid-close | wake", "at": "ISO-8601"}]
   }
   ```

   Leave a field `null` when the surface does not give it. Never invent a value. Only diagnose a run whose scheduled time has already passed. Write the file as UTF-8 (a Windows PowerShell `>` redirect writes UTF-16; the script reads that too, but prefer UTF-8).

   How the script reads the record:
   - `status`: `completed`, `succeeded`, `success`, `ok`, `done` or `finished` is a finished run; `failed`, `error`, `errored`, `timed-out`, `timeout` or `aborted` is a failure; anything else (`running`, `cancelled`, `stopped`, an unfamiliar word) is not treated as finished. Use the surface's own word, not your paraphrase.
   - `last_event` and `status` containing `permission`, `denied`, `approval` or `approve` (any case, `_` or `-`) count as a permission halt. Use the surface's own wording.
   - `machine_events[].kind` must be one of `sleep`, `hibernate`, `lid-close`, `wake` (any case); any other kind is an error, so map the source's events onto these.
   - A `wake` with no earlier sleep in the window is not sleep evidence.
2. For `machine_events`, ask the user, or with their consent read sleep history around the scheduled time: on Windows the System log's Kernel-Power events: 42 (entering sleep) and 107 (resume from sleep), and on laptops with Modern Standby 506 (entering) and 507 (exiting), which is how most recent laptops sleep; on macOS `pmset -g log`. Show the command before running it.
3. Run `diagnose.py --record FILE --json` and report the verdict, the `why` and the evidence verbatim.
4. Act on the verdict:
   - `permission-halt`: name the tool, then use the pre-flight advice for it.
   - `slept-through`: run `power_check.py`, and point to the Keep computer awake setting and the lid-close action.
   - `late-catchup`: add or tighten the time guard, using pre-flight steps 3 and 4.
   - `failed-unknown`: show the error text; it is not a scheduling problem the skill can classify.
   - `unfinished-unknown`: the run started on time but nothing shows it finished (still running, cancelled, stopped, or an unfamiliar status). Show the status and ask the user whether it is still going; do not call it healthy.
   - `never-ran-unknown`: say there is not enough data. Suggest the user check the machine was on and the app open at that time. Do not guess a cause.
   - `healthy`: say the run looks fine and ask what they saw.

## Fetching task state per surface

| Surface | `surface` value | Prompt and schedule | Last run |
| --- | --- | --- | --- |
| Claude Desktop scheduled task | `desktop` | the scheduled-tasks tools in this session (names contain `scheduled_task`) | the same tools' run details |
| Claude Code session cron (`/loop`, `CronCreate`) | `code-cron` | `CronList` | the session transcript and the cron's own output |
| Cloud routine (`/schedule`) | `routine` | the `schedule` skill's listing | its run history |

If this session has no tool for a surface, say so and ask the user to paste the prompt, the scheduled time, the start and end times, and any error. Do not read an app's files from disk to get task state: the layout is not stable.

## Rules

- Scripts decide. Never name a cause yourself; `never-ran-unknown` stays unknown.
- Never edit a scheduled task or its prompt before showing the diff and getting an explicit yes in this conversation.
- Never print or paraphrase prompt or transcript content beyond the short snippets the scripts print.
- Do time comparisons only through the scripts. A timestamp without an offset is read as UTC: say so if the user's times are local.
- The Desktop app changes quickly; a release may fix some of these failures. If a verdict contradicts what the user sees, show the evidence and say the app may have changed.

## Common mistakes

- Calling the tool list a guarantee. It is a heuristic over the prompt text.
- Reporting `slept-through` without sleep evidence. Without it the verdict is `never-ran-unknown`.
- Treating a run the user started by hand before its time as late. Negative delay is healthy.
- Forgetting the Keep computer awake toggle: `power_check.py` cannot see it.
