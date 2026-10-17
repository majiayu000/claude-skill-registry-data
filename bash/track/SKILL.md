---
name: track
description: Console-native billable hours tracker. Routes /track:start, /track:stop, /track:pause, /track:resume, /track:status, /track:report to a bash dispatcher that maintains a git-versioned JSONL ledger under ~/.time-tracker/. Use whenever the user invokes one of those slash commands. The skill itself does no time arithmetic, file I/O, or git work — the dispatcher does all of that. The skill's job is to construct the correct Bash invocation — for /track:start, /track:stop, /track:pause, and /track:resume, split optional --at/--ago flags from the positional client name (start). For /track:stop the user's note must be piped through stdin rather than passed as an argument (so shell metacharacters in the note cannot be interpreted). /track:pause and /track:resume take no positional args.
version: 0.3.0
---

# track skill

This skill is the safe-invocation wrapper around `bin/track.sh`. Its sole job is to translate one of the `/track:*` slash commands into a `Bash` tool invocation that runs the dispatcher correctly. All ledger logic, locking, atomic writes, git commits, jq math, and error messages live in `bin/track.sh` — do not reimplement any of that here.

## Locating the dispatcher

The dispatcher lives at `${CLAUDE_PLUGIN_ROOT}/bin/track.sh`. If `$CLAUDE_PLUGIN_ROOT` is unset, fall back to the absolute path inferred from the SKILL.md location: `<plugin root>/bin/track.sh` where the plugin root is the parent of `skills/track/`. Either path resolves to the same script.

## Invocation patterns

For each subcommand, run the Bash tool with the exact command shape below. Do NOT add extra flags, do NOT pre-process arguments, do NOT interpret the output — print whatever the dispatcher prints, verbatim.

### /track:start

User invocation: `/track:start <client> [--at HH:MM | --ago <duration>]` (with `$ARGUMENTS` containing the client name and optional backdating flag)

Bash invocation:
```
bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" start $ARGUMENTS
```

The `<client>` argument is constrained by the dispatcher to alphanumeric + dash + underscore characters. The optional flags are also dispatcher-validated (`--at` requires `HH:MM`, `--ago` requires `<Nh><Nm><Ns>` like `30m`, `1h30m`, `90s`). Both are safe to pass positionally.

**Backdating flag-parsing rule:** if `$ARGUMENTS` contains `--at <VAL>` or `--ago <VAL>` tokens, they are flag-value pairs consumed by the dispatcher. They are only meaningful at the start of `$ARGUMENTS`, before the client name token. Order between `--at`/`--ago` and the client is flexible (either `start vytl --ago 30m` or `start --ago 30m vytl` works), but pass through `$ARGUMENTS` as the user typed it — let the dispatcher's flag loop handle the parsing.

### /track:stop

User invocation: `/track:stop [--at HH:MM | --ago <duration>] [note...]` (with `$ARGUMENTS` containing optional backdating flag(s) followed by an optional note)

**Critical: the note is piped through stdin, never passed as an argument.** This is a security boundary — the note is the only user-controlled input string in the system, and stdin-piping eliminates any possibility of shell metacharacter interpretation. Backdating flags go on argv (the dispatcher rejects any positional arg as ambiguous).

**Flag-parsing rule (getopt convention):** when splitting `$ARGUMENTS`, the dispatcher consumes `--at <VAL>` or `--ago <VAL>` **only when they appear at the start of `$ARGUMENTS`, before the first non-flag token.** After the first non-flag token, all remaining tokens are part of the note — including any literal `--at` or `--ago` strings inside it. This prevents a note like `"fixed bug --at line 47"` from being mis-parsed as a flag.

So when invoking:

- If `$ARGUMENTS` is empty (no flags, no note):
  ```
  bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" stop
  ```
- If `$ARGUMENTS` starts with `--at <VAL>` or `--ago <VAL>` (with no note after):
  ```
  bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" stop <FLAG> <VAL>
  ```
- If `$ARGUMENTS` contains only a note (no leading flags):
  ```
  printf '%s' "<NOTE>" | bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" stop
  ```
- If `$ARGUMENTS` starts with a flag AND has a note after:
  ```
  printf '%s' "<NOTE>" | bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" stop <FLAG> <VAL>
  ```

In every case `<NOTE>` is the literal text of the note portion (after any leading flag tokens are consumed), quoted as a shell string. Use `printf '%s'` rather than `echo` to avoid escape-sequence interpretation of the note content.

The dispatcher's `cmd_stop` parses argv flags first, then checks `[ ! -t 0 ]` and reads stdin for the note when present. It refuses end-before-start (the only validation on backdating), preserving the active timer for retry.

If the timer is currently paused and the user did not pass `--at`/`--ago`, the dispatcher uses the pause point as the end automatically — the user does not need to resume before stopping.

### /track:pause

User invocation: `/track:pause [--at HH:MM | --ago <duration>]` (with `$ARGUMENTS` containing the optional backdating flag)

Bash invocation:
```
bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" pause $ARGUMENTS
```

`/track:pause` takes no positional args (no client, no note). `--at`/`--ago` backdate the moment the pause began — useful if the user forgot to pause when they actually stepped away. The dispatcher refuses a pause timestamp before the timer's start, and refuses to pause if the timer is already paused or if no timer is running.

### /track:resume

User invocation: `/track:resume [--at HH:MM | --ago <duration>]` (with `$ARGUMENTS` containing the optional backdating flag)

Bash invocation:
```
bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" resume $ARGUMENTS
```

`/track:resume` takes no positional args. `--at`/`--ago` backdate the resume moment. The dispatcher refuses a resume timestamp before the pause point, and refuses to resume if no timer is running or the timer isn't currently paused.

### /track:status

User invocation: `/track:status` (no arguments)

Bash invocation:
```
bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" status
```

### /track:report

User invocation: `/track:report [--week | --month YYYY-MM] [--client <name>]` (with `$ARGUMENTS` containing the optional flags)

Bash invocation:
```
bash "${CLAUDE_PLUGIN_ROOT}/bin/track.sh" report $ARGUMENTS
```

Flag values are constrained by the dispatcher (regex check on `--month YYYY-MM` and the client name) and are safe to pass positionally.

## Output handling

Print the dispatcher's stdout and stderr verbatim. Do not summarize, do not reformat, do not add commentary. The dispatcher's output is designed to be the user-facing surface; wrapping it in chat prose adds noise.

If the dispatcher exits non-zero, surface that to the user — the error message is already user-facing and includes recovery instructions where applicable.
