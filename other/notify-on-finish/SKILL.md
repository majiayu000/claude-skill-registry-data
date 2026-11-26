---
name: notify-on-finish
version: 0.1.1
allowed-tools:
  - Bash(${CLAUDE_SKILL_DIR}/scripts/notify-on-finish *)
  - Bash(notify-on-finish *)
description: Native desktop notifications for long-running work - runs a command detached, captures exit code and duration, then plays a sound and fires a notification (notify-send/D-Bus, osascript, log-only fallback). Use when a command will take more than a minute, when asked to leave something in the background and tell me when it finishes, or when waiting on a build, test suite, migration, benchmark or download.
---

# Notify On Finish

One command, detached, notifies when it ends. The skill exists so the agent never improvises `sleep 5 && notify-send …` inside a tool call: that blocks the turn, loses the exit code, and dies when the harness reaps the process group.

`scripts/notify-on-finish` is the whole implementation. Backend matrix, sounds and troubleshooting live in [NOTIFY.md](scripts/NOTIFY.md).

## 1. When to use it

| Situation | Do |
|---|---|
| Command likely to take **> 60 s** (build, full test suite, migration, install, benchmark, big download) | `notify-on-finish --label "<what>" -- <command>` |
| The user says "leave it running", "tell me when it's done", "in background" | same |
| Short command (< 60 s) | just run it; a notification is noise |
| The user wants the output in this turn | run it normally, no notification |

Announce it in one line when you launch - the label, and how to check:

```bash
${CLAUDE_SKILL_DIR}/scripts/notify-on-finish --label "go test ./..." -- go test ./...
# → 20261117T131539-1715152   (id on stdout)
```

Claude Code substitutes `${CLAUDE_SKILL_DIR}` here and in the `allowed-tools` rule, and the match is what lets the script run without a prompt. Other clients do not expand it: use the skill's own path (`<skill dir>/scripts/notify-on-finish`) or put the script on `PATH`.

Then tell the user: *"Running in the background; I'll check with `notify-on-finish --status`."* Do **not** follow it with `sleep 120` - that defeats the point.

## 2. Command contract

```bash
notify-on-finish --label "<label>" [--quiet] [--silent] [--no-notify] -- <command...>
notify-on-finish --label "<label>" --wait -- <command...>   # foreground, same exit code
notify-on-finish --status [--json]      # state, code, duration, label, log
notify-on-finish --clean                # drop finished runs
notify-on-finish --doctor               # which backends exist on this machine
```

- **Always pass `--`** before the command. Without it a flag in the command is parsed as one of ours.
- **Label** is the notification title: what a human would want to read at 3 a.m. Put the *intent*, not the raw argv (`"nightly test suite"`, not `"./gradlew test --no-daemon -x …"`).
- **Permissions.** The frontmatter's `allowed-tools` pre-approves both invocation forms for the turn in Claude Code, so the script runs without a prompt. Other clients have no such field: add the rule once with `rsk tools allow 'Bash(*notify-on-finish*)'` (Claude, persistent) or by hand in the client's config.
- Detached runs exit the turn immediately; stdout of the wrapper is the run **id**.
- `--wait` is for the case where the next step depends on the result *and* the notification is for a human away from the keyboard. It blocks; use it rarely.
- Exit status of `--wait` is the command's own. Detached runs report it in `--status` / the notification.

## 3. Reading the result back

```bash
notify-on-finish --status          # TSV: STATE  CODE  DURATION  LABEL  LOG
notify-on-finish --status --json   # same, for scripts
```

`STATE` is `running`, `done`, `failed` (exit 1-127) or `killed` (signal, code ≥ 128). The log path is in the last column: read the tail of it, never the whole file, when reporting a failure.

Report back as: outcome, duration, the one line that matters (last error line on failure), and the log path. Nothing else.

## 4. Rules

- **One wrapper, not a pipeline of your own.** No `&`, no `nohup`, no `disown` by hand, no `&& notify-send` after the command. The wrapper detaches with `setsid`, so it survives the tool call returning.
- **Sound and notification are independent.** A failing sound device must never suppress the notification; the wrapper already treats each backend as best-effort.
- **The exit code comes from the command**, never from `notify-send`. Verify with `--status`, not with `$?` of the launcher.
- **No daemon, no polling loop.** State lives in `$XDG_STATE_HOME/notify-on-finish/` (`<id>.meta`, `<id>.log`); a `--status` call is enough.
- **Headless / SSH / CI**: pass `--silent` (log only) or `--no-notify`. Never let a missing notification daemon turn into a failed task.
- **Do not retry a notification.** If `--doctor` shows no daemon, say so once and continue.
- **Never wrap a command that needs a TTY or reads stdin** (`ssh` prompts, `read`, `kubectl edit`): stdin is `/dev/null` by design.
- Keep labels under ~60 characters; long ones are truncated by the notification daemon, not by us.

## 5. Anti-patterns

```bash
# BAD - blocks the turn, loses `code`, dies with the process group, and the
# notification only fires if the sound device works.
sleep 5 && pw-play complete.oga && notify-send "Prueba" "Terminó"

# GOOD
notify-on-finish --label "prueba: sleep 5" -- sleep 5
```

```bash
# BAD - backgrounding by hand inside a tool call.
( ./long-build.sh & ) ; notify-send "started"

# GOOD
notify-on-finish --label "long build" -- ./long-build.sh
```

## 6. Non-Linux and missing pieces

`--doctor` prints what exists: `notify-send`, `dunstify`, `makoctl`, `swaync-client`, `gdbus`, `osascript`, `canberra-gtk-play`, `pw-play`, `paplay`, `afplay`, `setsid`, the freedesktop sound theme, and whether a notification daemon answers. On macOS the same script uses `osascript` + `afplay`; inside WSL or a container without a session bus, run `--silent` and read the log. Details and per-environment fixes: [NOTIFY.md](scripts/NOTIFY.md).
