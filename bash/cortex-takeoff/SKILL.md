---
name: cortex-takeoff
description: >
  Create or resume a session takeoff baton — a curated, ephemeral, git-ignored
  hand-off note that lets the next Claude session continue a long-running task.
  A repo can hold several batons at once, one per work line (topic). Use when
  the user says "交接", "takeoff", "交棒", "context 快滿了交接給下個 session",
  "hand off to next session", "/cortexes:takeoff", "takeoff resume", or
  "takeoff done". The baton is scaffolding, not knowledge: it is never
  committed, distilled, broadcast, or indexed.
---

# Cortex Takeoff — Session Hand-off Baton

A baton is a curated continuation note for ONE work line (topic) in ONE repo.
It lives at `<vault>/.takeoff/<repo-slug>/<topic>.md`, is git-ignored, and is
consumed by a later session. A repo may hold several batons at once — one per
work line. Batons are independent of the Raw session dump (which SessionEnd
writes automatically). Do NOT commit them, distill them, broadcast them, index
them with `cortex-vec`, or log them to `log.md`.

Legacy layout: `<vault>/.takeoff/<repo-slug>.md` (single-baton era, no topic
key). Legacy batons still list, resume, and clear (via `--legacy`), and are
retired to the new layout on their next hand-off. Never create new ones.

## Locating takeoff.sh

The repo slug and git-safety are handled by `takeoff.sh`, bundled in this plugin
at `hooks/scripts/takeoff.sh`. In every mode below, FIRST set `TK` to that helper,
resolved relative to THIS skill's base directory.

Claude Code announces that base directory when it loads the skill. Use **exactly
the path it announced**, verbatim — do not assume, reconstruct, or hard-code any
install layout; the marketplace, plugin name, and version all appear in real
paths and all of them change. The only stable fact is the relative one:
`takeoff.sh` sits two levels up from the skill's base directory.

```bash
TK="<the skill base dir Claude Code announced>/../../hooks/scripts/takeoff.sh"
test -f "$TK" || { echo "cortex: takeoff.sh not found at $TK" >&2; exit 1; }
```

Do NOT use `claude plugin root` (no such subcommand) or `$CLAUDE_PLUGIN_ROOT`
(unset for skill-run bash).

## Resolving the repo root

Every `bash "$TK" …` call takes an EXPLICIT cwd argument — there is no $PWD
fallback (a drifted shell cwd once deleted the wrong repo's baton). Resolve
the repo root ONCE per mode and reuse it verbatim in every call:

```bash
cwd="$(git rev-parse --show-toplevel)"
```

If your shell may have cd'ed to another repo earlier in the session, resolve
from a path you KNOW belongs to this repo (e.g. a file you have been editing)
instead of trusting the shell's current directory.

## Mode

Determined by the command argument:

| Argument | Mode |
|----------|------|
| (none) or `<topic>` | **create** — write/overwrite one work line's baton |
| `resume [topic]`    | **resume** — load a baton (do not delete) |
| `done [topic]`      | **done** — clear a baton (soft-delete to trash) |

## Create (`/cortexes:takeoff [topic]`)

1. Set `TK`, resolve `cwd`, then survey the existing work lines:

   ```bash
   bash "$TK" list "$cwd"
   ```

   Output: one baton per line, `topic<TAB>summary<TAB>path`, newest first.

2. Decide the topic — kebab-case `[a-z0-9-]`, max 64 chars, not
   `resume`/`done`/`legacy`:
   - The user passed one explicitly → use it verbatim.
   - This session earlier RESUMED a baton → reuse that topic. A continuation
     is the same work line; do not mint a new name. (Hard rule.)
   - Otherwise: if a listed baton is clearly this same work line, propose
     reusing its topic; else derive a short new topic from the work line and
     ANNOUNCE it to the user before writing.

3. Run the preflight (git-safety; also derives the slug):

   ```bash
   bash "$TK" prepare "$cwd" "<topic>"
   ```

   Output is TWO lines: line 1 = `baton_path`, line 2 = `workdir`. If it
   exits non-zero, STOP and relay the message — do not write anything.
   (Exit 2 = no vault / no repo; exit 3 = `.takeoff/` not git-ignored;
   exit 64 = invalid topic.)

4. Curate the current session into a hand-off. Content is free-form — write
   whatever genuinely lets a fresh session continue without re-deriving
   context. Typically worth capturing: the goal, what's done so far, the
   immediate next step, key files and locations (`path:line`), open questions,
   and gotchas. Omit anything not useful; do not pad to a template.

5. Compose one `summary` line (used verbatim as the SessionStart menu preview):
   a single sentence naming the work line and the next step.

6. Write the baton to `baton_path` with the Write tool. `workdir` is line 2
   of the prepare output, verbatim — do NOT re-derive it yourself:

   ```markdown
   ---
   repo: <slug>
   topic: <topic>
   workdir: <line 2 of prepare output>
   created: <YYYY-MM-DDTHH:MM:SS>
   summary: <one sentence: this work line / next step>
   ---
   <free-form curation body>
   ```

   If a baton already exists for this (repo, topic), this overwrites it (one
   active baton per work line, new replaces old).

7. If this work line previously lived in the legacy single-baton file (you
   resumed from topic `legacy`, or `list` shows a legacy entry that is this
   same line), retire it now that the new-format baton exists:

   ```bash
   bash "$TK" clear "$cwd" --legacy
   ```

8. Confirm to the user: baton written to `<baton_path>`, topic `<topic>`,
   not committed.

## Resume (`resume [topic]`, or chosen from the SessionStart menu)

1. Set `TK`, resolve `cwd`, run `bash "$TK" list "$cwd"`.
2. No batons → tell the user there is nothing pending for this repo and stop.
3. Pick the target: the explicit / menu-chosen topic if given; a single
   listed baton is used directly; multiple batons with no topic given → show
   the list (topic + summary) and ask which one.
4. `Read` the baton in full (path from the list output) and adopt it as
   continuation context. REMEMBER the resumed topic for the rest of the
   session — it is the default target of a later create or done.
5. **Do NOT delete it** — loading is not completion; this session may itself
   need to hand off again.

## Done (`done [topic]`)

1. Set `TK`, resolve `cwd`. Determine the target: the explicit topic if
   given, else the topic this session resumed. Neither exists → REFUSE to
   guess: run `bash "$TK" list "$cwd"`, show it, and ask the user to name
   the target.
2. Clear it (use `--legacy` in place of the topic when the target is the
   legacy baton):

   ```bash
   bash "$TK" clear "$cwd" "<topic>"
   ```

   Exit 4 = the baton belongs to a different working directory (its
   `workdir` does not match this repo's toplevel). Relay both paths to the
   user and let THEM decide — never retry with `--force` on your own.
   Exit 5 = no such baton; re-run `list` and re-check the target.
3. Confirm to the user: the baton was moved to the trash path printed by the
   command (recoverable for 30 days, then pruned).

## Overwrite vs done

- Re-running create replaces that topic's baton (normal re-hand-off).
- `done` is the explicit "this work line is finished" exit — the baton is
  soft-deleted into `<vault>/.takeoff/.trash/` and pruned after 30 days.
- Merely loading via `resume` never clears anything.
