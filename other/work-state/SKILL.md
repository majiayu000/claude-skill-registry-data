---
name: work-state
description: |
  Report whether work is committed, pushed, tidy and installed, do the safe clean-up and install,
  and ask the rest once. Ends the message with one honest status line.
---

# Work state

After finished work the question is not only "is it landed" but "is it committed, pushed, tidied away and installed". This skill runs `scripts/work-state.py`, does what is safe, asks about the rest once, and ends the message with the script's status line; the script measures, this skill only acts on what it printed.

Invoke with: `/superpowers-gstack:work-state`

## Run

Locate the script relative to this skill (it usually runs in the user's project, where `scripts/` does not exist). It needs Python 3.11 or newer; macOS's `/usr/bin/python3` is 3.9, so pick an interpreter first:

```bash
WS="<this skill's base directory>/../../scripts/work-state.py"
PY=""
for p in python3 python3.14 python3.13 python3.12 python3.11 /opt/homebrew/bin/python3; do
  if command -v "$p" >/dev/null 2>&1 && "$p" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then PY=$p; break; fi
done
if [ -z "$PY" ]; then
  echo "work-state: no Python 3.11+ found (macOS /usr/bin/python3 is 3.9) — install one, e.g. brew install python" >&2
  false   # stop here: non-zero, and the script is not run
else
  "$PY" "$WS" report --repo "$PWD"
fi
```

`report` changes nothing except one `git fetch --quiet origin` (15 s limit). Run with an older Python anyway, the script stops with code 70.

## Read the result

On exit 0 and 1 the last line of stdout is a JSON object, also when the report itself failed (then it holds `line` and `error`). Exits 2, 64 and 70 print only a reason on stderr and no JSON: show that reason and stop. Its keys: `line`, `committed`, `pushed`, `tidy`, `installable` (each with `status`, `detail`, `items`), `safe_actions` and `ask`. Exit code 0 means nothing is open, unknown or stale; 1 means something is; 2 means `--repo` is not a git repository; 64 is a usage error; 70 is Python older than 3.11.

`line` is what ends your message, copied as printed. The line never says ✓ while something is left: it names what remains (`mapper ryddet ✗ (1 kan ryddes, 2 må avgjøres)`), and `?` means unmeasured, not fine. Never rewrite a ✗ or ? into a ✓ and never drop a part of the line.

## Do what is safe

`safe_actions` is a list of argument lists the script judged safe: a push of a branch that has an upstream, removal of a clean worktree whose branch is an ancestor of `origin/main`, `git branch -d` of such a branch, a leftover folder that holds only cache moved to the Trash, and the `install` call for a `macos-app` that is `stale`.

- Run `safe_actions` as printed: one entry at a time, from the main folder (the first entry of `git worktree list`), in the order given. Do not add flags, reorder, merge or "improve" an entry. The only permitted addition is the `--quit-path <bundle recorded in verify-and-land Phase 5>` that the user's Phase 6 yes covered, appended to the `install` entry (the path is one argv element, no quote characters).
- Each entry is an argv list (a JSON array of separate arguments). Execute it directly as separate arguments (for example `subprocess.run(argv)`), never joined into a shell string and never re-quoted: paths contain spaces, and the Trash entry carries an AppleScript fragment. The `install` entry starts with the absolute path of a Python 3.11+ interpreter, so it needs no substitution.
- Stop at the first entry that fails and show its output; do not try the later ones.
- An `install` entry can take minutes (it builds). Run it in the background and wait for the session's notification that it finished before the second `report`; a `report` while it runs would show the old state.
- Re-run `report` once at the end, and end the message with that second `line`. Never loop more than twice: report, act, report.
- `committed` has no safe action. Commit only files you changed yourself in this task; anything else goes to `ask`.

## Ask once

Collect everything in `ask`, plus any stop code from `install` that needs the user (4, 5, 6 below), into one `AskUserQuestion` in one message. Make one question per item, in plain words, with concrete options; with more than four items, put them in one numbered list in the question text and ask the user to answer by number. If the user does not answer, do nothing about those items; the line stays honest and shows them as open. After `install` has stopped on a question, its answer is stored in `<git dir>/gstack-install-result.json`, so each `report` puts the question in `ask` again until a run succeeds (the same stop may therefore repeat; ask it once per message): ask it only if the session is not in the middle of another task.

## Install codes

`install` prints a last stdout line `{"status", "code", "reason", "commit"}`, and every run that holds the install lock also stores it in `<git dir>/gstack-install-result.json`. A `status` of `current` means the stamp already proves `origin/main` is installed.

| Code | Meaning | The agent does |
|---|---|---|
| 0 | Installed, or already current | Re-run `report`; the line ends the message. |
| 2 | The `Installable:` line is not `macos-app`, or is missing, or `--repo` is not a git repository | Say so. Nothing to install here; `/superpowers-gstack:adapt` writes the line. |
| 3 | The main folder is not on `main`, is not clean, `pull --ff-only` failed, or `main` differs from `origin/main` | Show the named files or the reason. The user decides; do not stash or reset. |
| 4 | The app is running | Ask the user. Only after their yes in this session, re-run `install` with `--quit-running` (asks the app to quit itself), or with `--quit-path APP` to quit just that bundle. The script never kills. |
| 5 | The span since the stamp may change data on disk, or cannot be measured | Show the reason and ask. Only after the user's yes in this session, re-run with `--accept-migration`. |
| 6 | A copy without a stamp is in the way | Ask whether it may be replaced. Only after the user's yes in this session, re-run with `--replace-unstamped`. |
| 7 | Another app, or one that cannot be identified, has the name | Tell the user to tidy by hand: no flag helps. Name the app the reason names. |
| 8 | The build failed; nothing was touched | Show the log path from the reason (`<git dir>/gstack-install-build.log`). |
| 9 | The check failed; the old copy is untouched (a temporary copy was removed, or the swap was rolled back) | Report the reason and stop. Nothing is stamped. |
| 10 | The applications folder is missing or not writable, or macOS refused the swap | Report and stop. Never `sudo`. |
| 11 | `main` moved during the build; nothing swapped or stamped | Report and stop. The user may run `/superpowers-gstack:work-state` again. |
| 12 | Another install holds the lock, or `land` held its lock longer than 60 s | Wait, then run `report` again. |
| 64 | Usage error (bad flags, scheme or settings not usable) | Show the state as printed. Do not guess. |
| 70 | Unexpected error, interrupted ("avbrutt"), or Python older than 3.11 | Show the printed state. Do not guess. |

`/superpowers-gstack:verify-and-land` has already opened the branch build in Phase 5; when the user says yes to "make this the current version and install it in /Applications", it passes `--quit-path <the bundle from Phase 5>` to `install` (the argument is the literal absolute path as ONE argv element, without quote characters), so the commonest path does not stop at code 4. Without that yes, the flag is not passed.

## Never

- never `git branch -D` (a refused `-d` is the guard working), never force push, never `sudo`, never kill a process; an app is quit with `--quit-running` or `--quit-path` only.
- Never pass `--quit-running`, `--quit-path`, `--accept-migration` or `--replace-unstamped` without the user's yes in this session. A yes from an earlier session or from a stored result does not count.
- Never edit, shorten or reword the script's output: not `line`, not an entry of `safe_actions`, not a `reason`. The only permitted addition is the `--quit-path <bundle recorded in verify-and-land Phase 5>` that the user's Phase 6 yes covered, appended to the `install` entry (the path is one argv element, no quote characters).
- Never stash, reset, or remove a worktree the session stands in or one that `report` marked as in use.
