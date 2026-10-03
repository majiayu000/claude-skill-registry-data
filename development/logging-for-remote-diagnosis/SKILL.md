---
name: logging-for-remote-diagnosis
description: Use when building any mechanic that could fail on a machine out of reach - a shipped product, a CLI a user runs, a server.
---

## The rule

Add the logs as you build the mechanic, not after. The test to hold yourself to: a user on another machine hits a bug, turns on verbose logging, and sends you one dump. From that dump alone, with no chance to add a log and ask them to try again, can you tell which path ran, what got skipped, and why? If not, the logging isn't done yet.

## Fires when

While writing any branch, early return, skip, or async/deferred step in code that runs somewhere you can't attach a debugger. At build time, not at bug time.

## How to apply

Log the entry of each path, every branch and skip with the deciding condition, key values and counts, and the chosen outcome. Use a greppable tag prefix (e.g. `[Dispatch]`, `[Sync]`) so the dump is filterable.

Key values means ids, sizes, counts, and reasons — not payloads. Credentials and tokens never go in a log line, and personal data is payload too: log the user id, not the email. The dump you're designing for gets read on screens you don't control and forwarded around.

For async or deferred work, log at schedule time and at execution time. They're different moments and either can be the bug.

Before calling it done, reread each branch and ask: "from the verbose dump alone, could I tell this branch was taken and why?"

## Absence is not proof

A missing log line does not prove the code didn't run. The log level may have been off. If you grep a dump and find zero hits for a tag, "verbose was disabled" is at least as likely as "the branch didn't execute" — say that out loud and rule it out first. When chasing a live bug, either confirm the user's verbose level is actually on, or temporarily log the key decision at a level that always shows.

## Worked example

A file-sync tool skips some files and a user reports "it just ignored half my folder." With no instrumentation you're guessing. With it, their dump reads: `[Sync] scanning 412 files`, `[Sync] skip report.tmp reason=matched-ignore-glob`, `[Sync] skip photo.HEIC reason=unsupported-ext`, `[Sync] uploaded 198`. Now you know the skips were two real rules firing, not a bug, and exactly which rule hit which file. You answered a remote bug report correctly from one dump, without ever touching their machine.

## Red flags

| Thought | Reality |
|---|---|
| "I'll add logs if it turns out to be buggy" | You get one shot at a stranger's log. Add them now. |
| "No log line for that path, so it didn't run" | Or the level was off. Verify emission, don't infer from silence. |
| "This branch is obvious, it doesn't need a log" | Obvious to you, invisible in a dump from someone else. |
| "The email makes the log easier to read" | It also makes the dump a PII leak. Log the id, look the rest up. |
