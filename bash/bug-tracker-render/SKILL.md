---
name: bug-tracker-render
description: Internal helper invoked only by other skills in this plugin (bug-submit, bug-fix) to (re)generate the repo-wide bugs/bugs-tracker.html from the plugin's tracker template plus the current filesystem state. Runs scripts/render_bug_tracker.py, which scans bugs/ (open) and bugs/archive/ (closed), renders each bug as an expandable Issues card with relative-path screenshots, and writes the tracker wholesale. Holds no state of its own. Never touches bug folders or report .md files. Not user-invocable.
user-invocable: false
allowed-tools: Bash(python3 *), Bash(find *), Bash(test *)
---

# bug-tracker-render

Invoked as a sub-step of another skill in this plugin (`bug-submit` Step 8, `bug-fix` Step 9c) whenever the set of bugs on disk changes. All rendering lives in `scripts/render_bug_tracker.py`: this skill locates the script, runs it, and relays its one output line.

The tracker is a **generated artefact**: it carries no state of its own, so the script rebuilds it wholesale every call. That makes "create" and "update" the same operation, and open-vs-closed is always re-derived from folder location — never stored.

## Step 1 — Locate the script

The script ships with this plugin at `scripts/render_bug_tracker.py`.

- **Try the running plugin's own copy first** — this skill's base directory was announced when it was invoked (`…/dev-skills/<version>/skills/bug-tracker-render`), so the script sits at `<base>/../../scripts/render_bug_tracker.py`. If that file exists, use it: it matches the running plugin version and no search is needed.
- Otherwise search: `find ~ -path "*dev-skills*/scripts/render_bug_tracker.py" 2>/dev/null` (the pattern must tolerate the `<version>` segment installed plugins carry under `plugins/cache/<marketplace>/dev-skills/<version>/`). Exactly one match → use it. Several → prefer one under a `plugins/cache/` path at the **highest** version over a working clone. None → output `bug-tracker-render: skipped — script not found` and stop; never reimplement the rendering here.

## Step 2 — Run it

The script is stdlib-only and runs with the system interpreter, not a project environment. It finds the repo root by walking up from the current directory and uses the template that ships next to it.

```bash
python3 "<script>"
```

## Step 3 — Relay

Relay the script's single output line verbatim to the caller:

```
bug-tracker-render: bugs/bugs-tracker.html updated — <O> open, <C> closed
```

or `bug-tracker-render: skipped — <reason>` (not in a git work tree, template or script missing, unreadable template). A skip is a note, not an error: never abort the calling skill over it, and never substitute a hand-written tracker.

## Constraints (non-negotiable)

- **Never touch bug folders or report `.md` files.** The only write is `bugs/bugs-tracker.html`. Creating, moving and closing bugs is the caller's job.
- **Always regenerate wholesale.** Never patch a card in place or hand-edit the tracker — the script rebuilds it from template + filesystem so it can never drift from reality.
- **Status is derived, never stored.** Open = a folder in `bugs/`; closed = a folder in `bugs/archive/`.
- **Relative image paths only.** The tracker and its images ship together under `bugs/`; the script never embeds remote URLs or absolute paths.
- **Degrade, don't fail.** Any problem is one skip line, never an error to the caller.
