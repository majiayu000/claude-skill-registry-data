---
name: running
description: "Use when launching the Electron app for manual verification or UI smoke testing. This project uses the Unix launcher script for local development and requires explicit user approval before starting the app."
---

# Running the application

Use this skill when a change needs a manual startup check or when the user wants to confirm runtime behavior in the real Electron app.

## Operating system check

Check the current operating system at the start of every session, no later than before the first runtime command is executed.

- On macOS or Linux, the current instructions and launcher commands are valid.
- On Windows, do not assume the repo is already configured for that platform. Ask the user before using `run.ps1` or expanding the skill set for Windows.
- The current project guidance is intentionally Unix-oriented; do not silently mix Unix and Windows assumptions.

## When to run the app

You may start the application to verify behavior when the user asks for a manual check or when automated tests are insufficient for the user-visible behavior.

Use the app for smoke checks such as:

- opening a markdown file
- verifying startup with the default file
- checking relative links, images, and local media
- testing reload-on-save behavior
- checking search, TOC, or navigation flows
- validating theme and settings behavior

## Startup commands

This repository's Unix development launcher is:

```sh
./run.sh
```

This is intentionally Unix-only in this repo. Ignore `run.ps1` and all Windows-specific startup guidance unless a later skill is explicitly added for that platform after the user approves the extension.

If the user later works on Windows again, ask them to let the runtime and testing skills be extended for that environment before using any Windows-specific commands.

## What the launcher does

The actual behavior is implemented in the repo, and the current code confirms the following:

- `run.sh` is a thin wrapper that executes `node scripts/run.js -- $*`
- `scripts/run.js` runs `npm start -- ...`
- it waits for the app to write to `logs/main.log`
- it streams the log file in a `tail -f`-like way with colorized output
- when the main process reports `Main process stopped`, the wrapper exits

That means the script is primarily a development convenience wrapper, not a replacement for the real Electron startup path.

## Default file and file selection

Without arguments, the application opens the default file `README.md`.

The current CLI parsing logic confirms this default:

- `app/lib/cliMain.js` sets `defaults.filePath` to `README.md` relative to the repo root
- `filePath` is the last positional argument when one is provided
- for a direct app launch without a path, it falls back to the project README

The rendering test document `test/documents/default.md` is a good candidate for rendering regressions when a bug needs a reproducible markdown example. Consider extending that file when a fix is not yet captured there.

## Required process before launch

Before starting the real app, always ask for confirmation and briefly explain:

1. what action will be performed;
2. why it is being run;
3. what the user should watch in the console or UI; and
4. which file or scenario is being checked.

In practice, the user should be told what output to expect and which steps are needed to reproduce it, because the app is being observed through its console logs and window behavior.

## Bootstrap process and startup caveats

The app uses a starter/server bootstrap pattern in `app/main.js`:

- a lightweight starter process checks whether a server instance is already running
- if a server is already active, the starter forwards the requested file path and exits
- if no server is active, it starts the server process, passes the file to open, and exits
- the server process owns the actual Electron window lifecycle and browser windows

This should be treated as non-trivial startup behavior and must not be changed casually. It is easy to regress when adjusting app startup, IPC, or window-opening logic.

## Validation and reporting

- Do not start the app without user approval.
- Report the exact command used.
- Explain the user-visible scenario being verified.
- Summarize the relevant console output and whether the app launched cleanly.
- If the command exits with an error or the app stalls, report the problem and include the failure signals.
- When a change affects visible behavior, provide a short smoke-test sequence for the user if needed.
