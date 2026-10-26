---
name: aiview
description: "Use whenever a document is produced for the user to read and react to while it evolves: a brainstorm board, a plan, a design language, a prototype, a PR analysis, a review report, a live PDF. Also when a document must be registered, opened, listed, moved or retired, or a prototype's bindings checked. Not for code, tests or configuration, or any file nobody opens in a browser."
---

# aiview: the contract

**aiview** is the local viewer and index for the documents an agent writes for a person to read. The tool is `<skill-dir>/aiview.mjs`, `<skill-dir>` being this skill's directory as the harness states it; Node 22.5 or later. **`$A --help` lists every verb with its flags; every verb takes `--json`, preferred when parsing.**

## The checkout and the data home

| Root | Holds |
|---|---|
| The checkout, `<skill-dir>` | code, `dist/`, `dist-cli/`; rebuildable |
| The data home, `$SWARMSTORM_HOME` or `swarmstorm_appdata` in the OS home directory | `aiview.sqlite`, the server's pid and port files, every document under `docs/<project>/` |

- **Every document lives in the data home, outside any project repository.**
- **On a fresh clone, a new machine, or when a verb prints a build command**: `references/setup.md`.

## Where a document goes

**Ask the tool for the path**: a hand-built one is wrong on the next OS, the next machine, or in PowerShell.

```sh
A="node <skill-dir>/aiview.mjs"
$A status --json          # cwdProject: the project this working directory belongs to
$A use <slug>             # only if cwdProject differs from the active project
F=$($A path 2026-08-24-topic.brainstorm.md)   # the absolute path, joined for this OS
# write the document at $F
$A open "$F" --tag <topic>
```

- **`open` is the standard gesture**, on creation: it registers the file, starts a detached server if none runs, and prints the URL to tell the user.
- **A project is a folder of the data home, `docs/<slug>/`**; refiling is `move <ref> --project <slug>`, and `status --json` says which project claims a working directory.
- **The date in the name is when the work started.**
- **A location the user states explicitly wins.**
- **A tag names a topic, never the project**: the project is the folder and the viewer's scope already. Reuse a spelling `list` already shows before inventing one.
- **To declare a project, or when `status --json` reports no `cwdProject`**: `references/projects.md`.

## Registering a document

- **File name `YYYY-MM-DD-<topic>.<kind>.md`**, flat in the project's folder.
- **Kind is mandatory**, from the filename or `--kind`: `brainstorm`, `plan`, `task`, `module`, `reference`, `prototype`, `workbench`, `pr-analysis`, `report`, `pdf`, `roadmap` (one per project). A kind is a type of document; a topic is a tag.
- **One `--group <slug>` per piece of work**, titled once with `--group-title`, at most one group per document.
- **A plan takes its own group, `<topic>-plan`**, shared with its task documents and nothing else.
- **`--started <ISO>` when the discussion began before the file existed.**
- **One document per subject**: iterate the file, never a v2. A rejected variant is removed from the index.
- **Fix metadata with `update`.** `aiview.sqlite` is the tool's to write, and scratch files stay unregistered.
- **Prototypes are self-contained HTML**, per the `design-prototype` skill.
- **A workbench is one HTML page, its data optionally in a sidecar `<stem>/` beside it, read only through the frame's bridge, per the `create-workbench` skill**; a trace is a workbench. `move` carries the sidecar with the page.
- **The project's board is aiview's `/board` page, never a document**: `swarm open` adds the run's repository to it with `aiview board --repo <path>`, and `aiview board` alone prints its link. aiview draws it through swarm's `client/reader.ts`, a client of swarm's board server, and never opens swarm's store. `/board#run=<id>` opens one run's tab.

## Publishing before the work is done

**`pending add` puts a card at the head of the document for each unit of work still running; `pending done` removes it when the section is written.** On a fan-out, one card per subagent as it is dispatched, closed when its result lands, on the failure paths too. The properties and the wording: `references/pending.md`.

## Pointing at a prototype

**`show <file|#id> --component <Name>... [--variant <v>]` moves every open tab to the prototype and lights those components**, dimming the rest, until the next `show`, until `show --done` sends every tab back to what the person was reading, or until the person stops it themselves. `components <file|#id>` lists every name on the page and its variants, and `show` refuses any other, listing the ones it has. It prints the link that does the same in a tab opened later, and says how many tabs heard it. When to point and how to word the question: the `point-at` skill.

## Contract for calling skills

**A skill that produces documents says "through the `aiview` skill"**, then states only its document's metadata: kind, tags, group, and a start time that predates the file. Command syntax and directories stay here.

**A document opens on a part written for a person who was not there** (a brainstorm board, and any kind that adopts it): `references/human-part.md`.

**To describe the viewer, a mode or a toolbar to the person**: `references/viewer.md`.

## Red flags

| Thought | Reality |
|---|---|
| "I'll show it as a claude.ai artifact instead" | Documents stay local and offline, in the data home. |
| "I'll run serve in a background task and watch it" | `open` and `serve --detach` daemonise; `status` finds the server. |
| "I'll add `--path` pointing at where the documents are" | `paths` are working directories. Documents live in `docs/<slug>/`. |
