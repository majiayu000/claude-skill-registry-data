---
description: Switch this project's pi dispatch mode (off / soft / strict)
disable-model-invocation: true
---

The user wants to set the pi-delegate mode to: $ARGUMENTS

If `$ARGUMENTS` is empty, just show the current mode and policy — do nothing else:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-mode"
```

For `off` and `soft`, set it directly and report the result:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-mode" <mode>
```

What the three modes do:
- `off` — no intervention at all. Suitable for a project pi should never touch.
- `soft` — nudges when existing product code is touched (default).
- `strict` — **blocks** edits to existing product code, requiring `pi_dispatch` instead.

The mode is recorded against the **project root** and applied by the project root of the
file being edited — not by wherever the session happens to be sitting. A strict project
therefore stays strict when edited from another project's session, or from one of its own
subdirectories. Report the path the command prints, so the user can see which project the
mode actually landed on.

## Setting `strict`: survey the project first

`strict` is the mode with teeth, so it needs to know what to protect. Without a policy it
falls back to a built-in heuristic that only fits one shape — a `src/` directory holding
`.ts/.tsx/.js/.jsx/.mjs/.svelte/.py`. On a Go, Rust, Elixir, or `<pkg>/`-layout Python
tree that heuristic protects **nothing**, and says nothing about it: strict looks switched
on and is not. So work out this project's real answer.

**1. Look at the project.** Read the manifest (`go.mod`, `Cargo.toml`, `pyproject.toml`,
`package.json`, `mix.exs`, …) and list the top-level directories. You are answering one
question: *which paths hold product source that should be written by pi rather than by
hand?*

Typical answers, as a starting point and not a lookup table — the repo in front of you
wins over any of them:

| Layout | Usually protect |
|---|---|
| Node / TS | `src/**` |
| Go | `internal/**`, `cmd/**`, `pkg/**` |
| Rust | `src/**/*.rs` |
| Python (`<pkg>/`) | `<pkg>/**/*.py` |
| Elixir | `lib/**` |

**Test files are NOT an exception. Do not put them in `allow`.** They are the single
biggest block of characters in most repos, and dispatching them is the plugin's whole
premise — the skill's rule is structural, not about judgment: *is this a character that
gets committed? then pi writes it*, implementation and tests alike. Exempting tests looks
reasonable ("the test is the spec, so I should write it") and quietly hands the largest
share of the work straight back to hand-typing. That is the exact leak strict exists to
close: with a written rule in place and no enforcement, roughly 80% of committed characters
were still typed by the main model.

If you want to fix the contract before pi implements it, the contract belongs **in the task
book** — prose you write, not a file that gets committed. And an acceptance test you run
yourself to judge the result is fine too, because it is a throwaway you never commit. What
must not happen is `src/**/*.test.ts` landing in the repo from your own keyboard.

`allow` is for things that are **not hand-written source at all**: generated code
(`*.pb.go`, `*_pb2.py`, `src/generated/**`, snapshots) and framework shells that are
config in disguise (`src/app.d.ts`, `src/app.html`, a vitest setup file). Getting *these*
wrong is what makes someone switch strict off entirely rather than live with it.

Paths that are simply outside the protected globs — docs, config, migrations you hand-write
by policy, fixtures, scripts — need no `allow` entry at all; they were never protected.

**2. Show the user what you propose, and why.** List the `protect` globs and the `allow`
globs, each with a one-line reason, and name anything you were unsure about. Patterns are
relative to the project root; `**` crosses directories, `*` stays inside one segment, and
a trailing `/` means "everything under here".

**3. Wait for their answer.** Do not write the policy until they approve it. They may edit
the lists — use what they say, not what you proposed. This confirmation step is the whole
reason this is safe: otherwise the model editing the files is also the model deciding
which files it may edit.

**4. Then write it:**

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-mode" strict \
  --protect "internal/**,cmd/**/*.go" \
  --allow "**/*.pb.go"
```

Note what is and is not in that `--allow`: generated protobuf output, yes; `**/*_test.go`,
no. Tests are dispatched like everything else.

`--allow` is optional — a policy with no exceptions at all is the common case, and the
better default. Omit it unless the repo actually contains generated or shell files inside
the protected globs.

The command prints back the mode, the project root, and the stored policy. Show that
output — it is the user's confirmation that what landed is what they agreed to.

To go back to the built-in heuristic, `--clear-policy` removes the stored lists. The policy
survives a switch to `soft` and back, so nobody has to redo the survey to toggle the mode.

**Correcting a policy already in place**: re-run the command with the full lists you want.
`--protect` and `--allow` replace what is stored, they do not merge — so to drop an
exception, simply re-issue the policy without it (`--allow ""` clears the exceptions while
keeping the protected globs).

## What strict can and cannot do

Be straight with the user about the limits, at least the first time they enable it:

- Only `Write` and `Edit` are intercepted. The same edit made through `Bash` (`sed -i`, a
  heredoc, `python - <<EOF`) is never seen. This is a discipline rail against your own
  habit, not a security boundary.
- Brand-new files are always allowed, whatever the policy says — writing a file from
  scratch is the shape pi is best at.
- `/pi-delegate:probe` grants a one-time bypass for a deliberate hand-edit.
- The policy lives in `~/.claude/pi-delegate/modes.json`, outside any project, so it is not
  protected by the guard it configures.
