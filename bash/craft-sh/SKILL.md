---
name: craft-sh
description: Crafting a shell script that reads like prose. One story in main, one job per function, early returns, and the ways a shell lies to you.
---

# Skill: Craft Sh

> "A script you must read top to bottom is a script nobody reads."

Shell is no excuse. What makes a class readable makes a script readable.

## The Shape

`main` at the top. `main "$@"` at the bottom. Everything between is detail.

```bash
main() {
    read_arguments "$@"
    locate_worktree
    refuse_main_checkout

    ensure_herd_serves
    ensure_database_answers
    point_env_at_site
    report
}
```

Seven lines, the whole story. The test: **can a stranger describe the script after reading only
`main`?** If not, a name is wrong or a step does two jobs.

## The Standard

1. **One job per function, and few lines.** If the name needs "and", split it.
   **Length is the signal.** When a function grows, the verbosity has already started — that is the
   moment another function is merited, not once it is unreadable. The test is the call site:
   `fetch_objects; check_out_ref; point_at_origin` reads as English. A body you have to assemble does
   not.
   **An embedded program is code.** An `awk` or `sed` inside a single-quoted string obeys every rule
   here — one job, named steps, early return. A string is not a reason to stop. Once it has more than
   one job, give it `-f` and a file of its own.

2. **Early return. Never `else`.** Guard, return, carry on. Zero `else` reads downward, not sideways.
   **An `else` is a function you have not named yet** — it holds a second job, which is why it needed
   a second branch. Extract it and the `else` disappears on its own. Same for `elif`, once per arm.
   In a loop, `continue` is the early return.
3. **A condition is a named predicate.** `herd_is_listening` beats `nc -z 127.0.0.1 443`. The name
   holds the meaning; the command is detail.
4. **Verbs act, `ensure_` guards.** `install_vendor` works. `ensure_site_is_secured` makes something
   true or stops. The prefix tells the reader which.
5. **Poll the oracle, not the report.** Tools print `ERROR` and succeed. Read the port, the file, a
   separate check.
   **And a pipe answers for its last stage.** `cmd | head` reports `head`, so `$?` is not the
   command's. The pipe you added to shorten the output is the one that hides the answer.
6. **Guard every flag value.** `--name` with no value leaves `shift 2` short and `$#` unchanged, so
   the loop never ends.
7. **Decide `set -e` in writing.** It is on, or the header says why not. Silence means you never
   decided.
8. **Comments are their own skill.** See `kernel:craft-comment` — what earns a line, the taper,
   and the space that means no comment was needed.
9. **`shellcheck` passes on the machine you write on.** Not optional there, and **nothing checks it
   here** — a gate reaching for it would stop working on a host that has POSIX and `git` and nothing
   else, which is the case every other rule about shipped code is written for.
   So it binds where the tool is, and the tree grades what an exit code can hold: `bin/shell.sh`
   takes rules 2 and 1's length half, and `taper` takes rule 8.
10. **One name, one meaning.** Every variable is global unless you say otherwise, so a name that
    means two things is a bug waiting for a refactor.
11. **A name says what it returns.** `unit_targets_file`, not `unit_targets` — the call-site should
    read as the thing it gets.
12. **One voice.** `step`, `note`, `fail` — never `echo` everywhere. One place to change how a script
    speaks.
13. **No bare `exit 1`.** Document the codes. A caller cannot branch on "it broke".

## Examples

One subject per file. Open the one the rule sent you to.

| | |
|---|---|
| [shape](shape.md) | predicates, guard clauses, `ensure_` |
| [oracles](oracles.md) | polling what a tool claims, guarding a flag value |
| [voice](voice.md) | one voice, traps |
| [comments](comments.md) | the taper, breathing |
| [portability](portability.md) | what is BSD-only, and what to write instead |
