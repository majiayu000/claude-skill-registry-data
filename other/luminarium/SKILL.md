---
name: luminarium
description: |
  Print the localhost URL for The Luminarium — moflo's daemon dashboard — for the current project.
  Use when the user asks for "the luminarium link", "the moflo dashboard", "the daemon UI", or anything synonymous.
  Each project gets a deterministic port in 33000–33999; the actual bound port is recorded in `.moflo/daemon.lock`.
---

# /luminarium — Project Dashboard Link

Surface the URL for The Luminarium (the moflo daemon's localhost UI) for the project that this session is running in. No prompts, no confirmations — print the link and stop.

## Procedure

1. **Find the project root.** Walk up from `process.cwd()` looking for a `.moflo/` directory. The session's cwd is almost always the project root, so check there first.

2. **Read `.moflo/daemon.lock`.** It's a JSON file written by the daemon at bind time. The dashboard port is the `port` field:

   ```json
   { "pid": 12345, "port": 33421, "startedAt": "...", ... }
   ```

   - If the file exists and `port` is a valid number → the daemon is running and bound. Use that port.
   - If the file is missing or `port` is absent/invalid → the daemon is not running. See step 4.

3. **Print the link** in a single line, with the path verbatim — Claude Code renders it as clickable:

   ```
   The Luminarium: http://localhost:<port>
   ```

   Nothing else. No banner, no follow-up question, no "what would you like to do?".

4. **If the daemon isn't running** (no lock file, or unparseable), say so in one line and offer the start command — don't run it:

   ```
   The moflo daemon isn't running for this project. Start it with: npx flo daemon start
   ```

## Why read the lock, not compute the port

The port is project-deterministic (sha256(projectRoot) mapped into 33000–33999), but if the deterministic port was already taken at bind time the daemon scans forward and binds an alternate. The lock file is the only source of truth for what's actually bound. Do not compute the hash yourself — read the file.

## Don't

- Don't fall back to any hardcoded port — there is no project-agnostic dashboard port; a literal would route to a foreign daemon on a multi-project machine. If the lock is missing, report "not running".
- Don't compute the deterministic port and report it as the link when the lock is missing — the daemon may be down, or bound to an alternate port. Report "not running" instead.
- Don't run `flo daemon start` automatically — the user asked for a link, not for daemon management. Leave starting to `/healer` or the user.
- Don't open a browser. Print the URL; let the user click.

## Output

A single line. Examples:

```
The Luminarium: http://localhost:33421
```

```
The moflo daemon isn't running for this project. Start it with: npx flo daemon start
```

## See Also

- `/healer` — diagnoses and (with `--fix`) starts the daemon if it's not running.
- `src/cli/services/daemon-port.ts` (and its JS twin `bin/lib/daemon-port.mjs`) — canonical port-resolution helpers; `resolveClientPort()` is what the rest of moflo uses.
