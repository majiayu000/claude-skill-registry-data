---
name: backgrounding-commands
description: Detaches commands with bgrun and streams their logs with bgfind. Use for backgrounded, long-running, or nohup-style jobs.
allowed-tools: Bash(bgrun *), Bash(bgfind --list), Bash(bgfind --preview *), Bash(cat ~/.local/state/bg/*), Bash(tail ~/.local/state/bg/*)
---

# Backgrounding commands

`bgrun` starts a detached script into a session directory; `bgfind` is an fzf picker over
those directories. They share nothing but an on-disk layout, so either works alone.

Both live in `~/dotfiles/bin`, symlinked to `~/.local/bin`. Linux only (`setsid` is
util-linux). Full rationale is in each script's header: `bgrun -h`, `bgfind -h`.

## The layout (the whole interface)

```
$BG_DIR (default ~/.local/state/bg)/<slug>-<YYYYmmdd-HHMMSS>/
    cmd.sh   the script that ran, verbatim
    out      its stdout      meta     key: value — name, started, host, cwd, src, cmd, pgid, ended
    err      its stderr      status   exit code, written ONLY on exit
```

`meta` and `status` are reserved; every other file is opaque payload, `cmd.sh` included — it
lists and streams like any other file, which is what you want when the question is "what did
this session actually run". **No `status` file means still running** — that is the liveness
check, not a `ps` lookup.

## Starting a job

bgrun takes bash's two forms and nothing else:

```bash
bgrun ~/simtest/run.sh "job name"     # like `bash FILE args`: args arrive as $1...
bgrun -n simtest -c 'a | b && c'      # like `bash -c STR`: one short line
```

**There is no argv form.** `bgrun -- trainer --lr 1e-4` fails with `no such file: trainer`;
write `bgrun -c 'trainer --lr 1e-4'`, or point it at a two-line script. Neither form can
launch a binary or honour a `#!/usr/bin/env python3` shebang, for the same reason
`bash ./trainer` cannot — the file is read as shell source.

Whichever form, bgrun copies the job into `cmd.sh` inside the session and runs *that copy*.
Editing or deleting the original mid-run cannot reach the job, a `/tmp` sweep does not turn
the session into a dead reference, and re-running is `bash "$d/cmd.sh" <args>`.

Stdout is the session dir and nothing else, so capture it: `d=$(bgrun ...)`. Returns in ~20 ms
regardless of job length. Chatter goes to stderr.

`bash -n` runs over the job before the session directory exists, so a missing file or a syntax
error fails in the caller's terminal with exit 1 and leaves nothing behind.

## Where a long command should live

Anything with a heredoc, a `&&` chain, or quoting worth thinking about belongs in a file
rather than on a command line — that is what the file form is for:

```bash
f=$(mktemp -t job.XXXXXX.sh)   # -t puts it in /tmp; without it, the cwd
cat > "$f" <<'EOF'
...                            # EOF must be at column 0
EOF
d=$(bgrun -n task "$f")        # the session keeps its own copy
```

For a string already sitting in a variable — the opaque case — `-c "$cmd"` is safe: the quotes
wrap a bare parameter expansion, and an expansion's result is never re-scanned, so `&&`, `|`
and `$( )` inside it reach the inner shell untouched. Quotes around text *typed at the prompt*
are the dangerous case, because there the outer shell expands your `$(...)` before bgrun runs.

The user's own route to these commands is readline's `edit-and-execute-command`: `set -o vi`
lives in `~/.bash_vars`, so `Esc` then `v` at the prompt opens nvim on the pending line, the
LuaSnip snippets in `~/dotfiles/nvim/luasnippets/sh.lua` (`simtest`, `bce`, `repriori`) expand
there, and `:wq` hands the file back to bash to run. Nothing is pasted, so no rendered-code
indentation and no re-quoting — which is why a snippet can safely contain `<<'EOF'`.

## Driving it as an agent

**Never launch bare `bgfind`** — it is a full-screen fzf app and there is no tty. Use:

```bash
bgfind --list                 # one line per session: name, state, size, cmd
bgfind --preview <name>       # meta + file table + tail of the newest file
cat "$d/status"; tail -50 "$d/err"
```

**Follow `err`, not just `out`.** Bazel, glog and most Python tooling write everything to
stderr, so a `submit_unified_job` session has an empty `out` and the job link in `err`;
`tail -f "$d/out"` on one looks hung forever.

Prefer the Bash tool's own `run_in_background` when the job only needs to outlive the current
turn — the harness then re-invokes on exit, which is cheaper than polling. Reach for `bgrun`
when the job must outlive the **session** (terminal closes, Claude exits) or when the user
wants to find it later in the picker.

To wait for a job, use the Monitor tool with an until-loop on `test -f "$d/status"`. Do not
foreground-`sleep` in a poll loop; it is blocked.

## Teaching the user the picker

```
bgfind                # newest activity first
bgfind -p             # print the chosen session dir instead of streaming
bgfind -d /some/dir   # any directory-of-directories works
```

| Key | Does |
|---|---|
| `enter` | stream the session's most recently written file |
| `ctrl-f` | choose which file to stream |
| `ctrl-o` | open the session dir in `$EDITOR` |
| `ctrl-r` | redraw the preview (it does not auto-follow) |

Streaming is `less +F`, which follows the file and shows `Waiting for data... (interrupt to
abort)` at the bottom. In follow mode the *first* keypress only drops out of following into a
normal pager -- so `q` once stops following and `q` again quits, and `Ctrl-C` then `q` does the
same; `F` resumes. Quitting leaves a stray line of the pager's screen in the scrollback, which
is a remnant, not an error message.

## Gotchas

- **bgrun's exit code is not the job's.** It reports whether the spawn succeeded, so success
  and liveness both come from `status`; `$?` only ever means "did bgrun get as far as
  forking". Pre-flight closes the loud half of this — a missing file or a syntax error exits 1
  before forking, so `bgrun foo && next` stops — but a job that starts and *then* fails still
  leaves bgrun reporting 0 with the real code in `$d/status`.
- **It wraps one command, not a paste.** bgrun is in the `nohup`/`setsid`/`time` family: it
  sees a single command and cannot look past a `&&`, a `;`, or a newline. Prefixed to a
  multi-line block it backgrounds the first fragment and leaves the rest running in the
  terminal. The caller's shell also expands `$(...)` first, so `bgrun req=$(mktemp)` hands it
  the one word `req=/tmp/tmp.XYZ` — a loud `no such file` now, but still not the job intended.
- **Heredocs want a file, not `-c`.** In a single-quoted `-c` string the outer shell eats the
  quotes of `<<'EOF'`, silently leaving `<<EOF`, so the body gets expanded; write `<<\EOF`,
  whose backslash survives single quotes. And the terminator must be at column 0 — an indented
  `  EOF` (easy to get from copying a rendered code block) never closes the heredoc, so the
  rest of the script becomes payload, `cat` succeeds, and the session exits **0** having run
  nothing. `bash -n` prints a warning for exactly this at launch but exits 0, so it is a hint,
  not a guard.
- **`pipefail` is off inside the job**, as in any fresh `bash`: `false | true` succeeds, so a
  pipeline whose producer dies still reports 0. Start scripts with `set -euo pipefail`.
- **No tty, and stdin is `/dev/null`.** `[ -t 1 ]` is false, so colors and progress bars
  vanish; anything that prompts — `sudo`, `gcloud auth login`, an ssh passphrase, a bare
  `read` — fails instantly rather than hanging.
- **Killing:** `kill -- -$(sed -n 's/^pgid: *//p' "$d/meta")` takes down the job and every
  child. The supervisor traps TERM/INT and records 143/130, so the session still gets a
  `status`. `kill -9` is untrappable and leaves the session reading as "running" forever.
- **`meta` identifies a session; it does not re-run it.** `cmd` is the script's basename plus
  arguments, or the `-c` string, `%q`-escaped onto one line so it stays greppable and fits the
  picker's column. `src` records where `cmd.sh` was copied from, which is the only trace left
  once a temp file is swept. To re-run, use `cmd.sh`.
- Session names are unique by construction, so nothing ever clobbers a previous run's log.
  Old sessions accumulate; `rm -rf` directories under `$BG_DIR` freely, no index to update.
