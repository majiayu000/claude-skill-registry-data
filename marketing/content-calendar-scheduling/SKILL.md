---
name: content-calendar-scheduling
description: Schedule a completed OpenNolan project on the local Content Calendar, optionally researching and remembering a niche-specific posting time.
---

# Content Calendar Scheduling

Use this skill only after the project has a final render at `renders/final.mp4`.
Scheduling creates a local calendar plan; it does not publish or connect to any
social platform.

## Workflow

1. Confirm which of TikTok, Instagram, and YouTube the user wants. Multiple
   channels belong in one `schedule_content` call.
2. If the user gave a date and time, pass it as `scheduled_at`. The tool checks
   the existing calendar and moves a colliding slot to the same time on the next
   open day; always tell the user the returned time.
3. If no time was given, provide a short stable `niche` label. The tool first
   checks its writable per-niche cache and otherwise uses the built-in weekday
   lunch/early-afternoon pattern from the daily-tech-carousel skill.
4. Optionally use WebSearch to research a better posting time for the niche.
   Prefer current primary studies or first-party platform guidance. Convert the
   result to the host's local `HH:MM` time and pass it as
   `learned_local_time`; the tool writes it into the runtime copy of this skill.
5. Call `schedule_content` once and report its returned date, time, and channels.

A project holds ONE slot. Calling the tool again for the same project MOVES that
slot instead of adding a second one, so a correction is just another call — and
the user sees the new time when they open Schedule in Mission Control.

The writable cache lives beside project data at
`.content-calendar/content-calendar-scheduling/SKILL.md`. A cached niche skips
the research step on later calls. Never place research prose, user content, or
account data in the cache—only the normalized niche key, local time, source, and
update timestamp.
