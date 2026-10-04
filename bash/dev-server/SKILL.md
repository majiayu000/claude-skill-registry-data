---
name: dev-server
description: "Start the project's dev server in the background and set up a persistent log monitor. Use this whenever the user asks to start, run, or boot the dev server, or says 'run the server', 'start it up', 'keep an eye on errors', or similar. Works for any framework — Node/npm, Python, Make, or custom scripts."
---

# Dev Server + Monitor

Start the project's dev server in the background and attach a persistent Monitor so you're notified automatically on any error or warning — without polling.

---

## Step 1 — Detect the start command

Inspect the project root (current working directory) in this priority order:

1. **`package.json`** — use `npm run dev` if a `"dev"` script exists, otherwise `npm start` if `"start"` exists, otherwise `npm run serve` if `"serve"` exists.
2. **`pyproject.toml` / `setup.py`** — look for a `[project.scripts]` entry or a common entrypoint. If the project uses `uv`, prefer `uv run <entrypoint>`. If it uses plain Python, use `python -m <module>` or the script name.
3. **`Makefile`** — use `make dev` if the target exists, otherwise `make run` or `make serve`.
4. **`Procfile`** — parse the `web:` line and use that command.
5. **`docker-compose.yml` / `compose.yml`** — use `docker compose up` only if no lighter-weight option was found above.

If nothing is found, tell the user and ask them to specify the command. Do not guess.

Once you have the command, tell the user: "Detected start command: `<command>`" before proceeding.

---

## Step 2 — Kill any existing instance

Kill any running process that matches the detected command so the new instance starts clean. Use `pkill -f` with a distinctive substring from the command (e.g., `pkill -f navidrome-feed`, `pkill -f 'npm run dev'`). Follow with `sleep 1` to let the port release. Suppress errors from pkill with `2>/dev/null`.

---

## Step 3 — Start the server in the background

Run the server with output redirected to `/tmp/dev-server.log` (truncate first so old logs don't accumulate):

```bash
truncate -s 0 /tmp/dev-server.log
<start-command> >> /tmp/dev-server.log 2>&1
```

Use `run_in_background: true` so the Bash tool doesn't block.

Wait 4–5 seconds, then tail the last 15 lines of `/tmp/dev-server.log` and confirm the server started cleanly (look for a "started", "listening", "running", or "Application started" line). If you see an immediate crash or import error, report it and fix it before continuing.

---

## Step 4 — Monitor only if issues were found

**Do not start a Monitor unconditionally.** Instead:

1. Check the startup tail from Step 3 for any ERROR, WARNING, Traceback, or Exception lines.
2. **If the startup log is clean** — tell the user "Server is running cleanly. No monitor started — I'll only look at logs if you report a problem." Stop here.
3. **If the startup log contains errors or warnings** — start exactly one Monitor (persistent):

```bash
tail -f /tmp/dev-server.log | grep --line-buffered -E "ERROR|WARNING|Error|Traceback|Exception|CRITICAL|failed|❌"
```

Set `persistent: true`. Tell the user what error was found and that the monitor is now active.

---

## Notes

- Log file is always `/tmp/dev-server.log` so it's easy to `tail` manually too.
- If the server needs env vars (`.env` file), make sure the shell inherits them — `uv run` and `npm run` pick up `.env` automatically; for raw Python you may need `dotenv run` or to source `.env` first.
- Only start one Monitor per session. If one is already running (check if you've already spawned it this session), skip Step 4.
