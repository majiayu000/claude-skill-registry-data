---
name: new-project
description: >
  Prepares a new Spring Boot project's generation without a clone of the source repository —
  fetches the source at its latest tag next to where the projects will live, records which
  ref and commit it fetched, and hands over to `/init-project` inside that tree. Runs from
  the plugin, in the directory that should hold the projects. Explicit invocation only.
argument-hint: "[--ref <tag|sha|main>]"
disable-model-invocation: true
allowed-tools: Read, Write, Bash, AskUserQuestion
model: sonnet
effort: low
---

# New Project

Gets a person who installed the plugin to `/init-project` without a `git clone`. It fetches,
records, and stops: **the generation is not here.** It runs in a second session, rooted at the
fetched tree, through the same `/init-project`, `project-initializer` and `project-bootstrap`
a clone runs — with that tree's hooks active — so a project made this way is the project a
clone makes.

This session is rooted at the directory the person chose. Nothing of the fetched `.claude/` is
loaded in it: no `init-project`, no `project-initializer`, no `guard`, and every relative path
`project-bootstrap` writes assumes the session root is the source. Following those files from
here would be a different generation. Never do it, even when asked to "just continue".

## Procedure

### 1 · Refuse where it cannot work

- **Outside the plugin.** The path in step 2 still reads `${CLAUDE_PLUGIN_ROOT}` literally →
  this copy is not the plugin's. In a clone of the source, `/init-project` is the command; say
  so and stop.
- **The JDK.** `java -version` below 21, or no `java` → stop: the hooks and `/init-project` both
  run it. `git` and `curl` missing → stop, naming which.
- **Inside a project.** The current directory holds `pom.xml` or `build.gradle` → stop. The
  fetched tree would land inside that project, and an existing project adopts with
  `/nerviz:arch-adopt`, not this.

### 2 · Resolve the source and the ref — `arch-adopt` § 2

Follow § 2 of `${CLAUDE_SKILL_DIR}/../arch-adopt/SKILL.md` — that section owns how the source
is found, which ref is the default, and how its commit is resolved. Three bindings, none of
which changes what it does:

- There is no project yet, so its third case is the one that applies: the plugin's copy is
  `${CLAUDE_PLUGIN_ROOT}/.plugin-source.json`.
- `SRC` for that section's own download is `${TMPDIR:-/tmp}/nerviz-new-project`, set
  explicitly — its default names a directory `arch-adopt` may be using.
- `--ref` from this skill's arguments passes through unchanged. `--source` does not exist here:
  a local checkout already is a clone.

What comes out: the ref, and the commit it names — or none, which § 2 says how to state.

### 3 · Choose the directory

```bash
SRC="$PWD/nerviz-<ref, every / replaced by ->"
```

The project is generated at `../<artifactId>` of that tree — this directory — exactly as from
a clone. Then, in order:

1. `$SRC` exists and its own `.claude/schemas/extensions.json` names a `source.fetch_marker`
   file that records this same ref → reuse it, skip steps 4 and 5, and say "reused".
2. `$SRC` exists otherwise → stop, and name it. Never delete, overwrite or merge into it.
3. `$SRC` does not exist → step 4.

Every other `nerviz-*` directory here is an earlier fetch. List them in the report as safe to
delete; never delete one.

### 4 · Fetch — `arch-adopt` § 3

Run § 3 of `${CLAUDE_SKILL_DIR}/../arch-adopt/SKILL.md` with the `SRC` of step 3, with one
binding: its tarball is `$TGZ`, not `$SRC.tgz`. `SRC` here is a directory the person owns, and
a ~50 MB archive beside it would stay there, since this skill never runs `rm`. Replace both
`"$SRC.tgz"` in that section with `"$TGZ"`:

```bash
TGZ="${TMPDIR:-/tmp}/nerviz-new-project-fetch.tgz"
```

Then confirm the tree is a source and not an error page that happened to extract:

```bash
ls "$SRC/.claude/skills/init-project/SKILL.md" "$SRC/.claude/hooks/ArchHook.jar"
```

Either missing → stop, and say the ref holds no `init-project`.

### 5 · Record the fetch

Read `source.fetch_marker` from `$SRC/.claude/schemas/extensions.json` — the fetched copy,
never a path from memory — and write that file under `$SRC` with `Write`:

```json
{"ref": "<ref>", "commit": "<commit from step 2>"}
```

Leave `commit` out when step 2 resolved none. `export` reads this file when it writes the
project's `.claude/`, and stamps that ref and commit; without it the stamp reads
`working-tree` and `unknown`, since the tree is no repository. A fetched `extensions.json`
with no `source.fetch_marker` is a ref older than the marker: write nothing, and say in the
report that the stamp will read `working-tree`.

### 6 · Hand over

Print the report below and stop. Never start `claude` yourself, and never run `/init-project`
in this session (top of this file).

## Report

```
✅ <fetched | reused> — ref <ref> (<short commit | commit unknown>)

Source ....... <base_url host>
Tree ......... <$SRC>
Projects ..... generated here, at <this directory>/<artifactId>
Stamp ........ <ref and commit recorded | working-tree — this ref predates the fetch marker>
Older trees .. <none | the nerviz-* directories, safe to delete>

Next, in a terminal:
  cd "<$SRC>" && claude
Accept the folder's trust prompt: its hooks are what enforce the architecture during the
generation. Then, inside that session:
  /init-project
To approve the write outside that tree once, first: mkdir "<this directory>/<name>", then
/add-dir ../<name>. When it ends, develop in a new session inside the project:
  cd "<this directory>/<artifactId>" && claude
```

## Failure modes

| Symptom | Cause | What to say |
|---|---|---|
| The path in step 2 reads `${CLAUDE_PLUGIN_ROOT}` | Run from a clone, not from the plugin | Use `/init-project` in the clone |
| `curl: (22)` on the tarball | A private source and no token, or a ref that does not exist | § 3 of `arch-adopt` names the variable; check the ref with `git ls-remote` |
| `$SRC` exists with other content | A directory of the same name the person made | Name it; they move or delete it — this skill never does |
| The stamp says `working-tree` | The fetched ref predates the fetch marker | `--ref` with a newer tag, or accept it — `/arch-adopt` restamps on the first update |
| `/init-project` is unknown in the new session | The session was opened somewhere other than `$SRC` | `cd "<$SRC>" && claude` |

## Why this is a manually-invoked skill

Form 2 (`disable-model-invocation: true`): it downloads a source tree into the person's
directory, so it runs only when they ask for it by name — interview axis 2 of
`claude-code-architect-designer`, a command typed by someone who has the plugin and no clone.
The closest rejected form was generating inline from the fetched tree, in this session: nothing
of that tree loads here, so parity with `/init-project` would rest on the model translating
every path, and a project that differs from what a clone generates was the one outcome the
interview ruled out. Runs on `sonnet` with `effort: low`: it follows `arch-adopt`'s fetch,
writes one small file and prints.

## Contract

**Class:** ops — the territory is `skill_classes.ops` in `.claude/schemas/extensions.json`,
and it is empty: this skill writes nothing in the session's project. What it writes lands
outside it, in the fetched tree.

**Unfiltered Bash:** the fetch is `arch-adopt` § 3's — `curl` with an optional header array,
`mkdir` and `tar` chained — plus `git ls-remote` and `java -version`; scoped rules would not
match those compound lines. It never runs `rm`, never runs `claude`, and never runs the
fetched `ArchHook`.

**Reads** `${CLAUDE_PLUGIN_ROOT}/.plugin-source.json`, § 2 and § 3 of `arch-adopt` (cited,
never copied — the plugin ships both), and the fetched `extensions.json`'s `source` block.

**Writes** `nerviz-<ref>/` in the current directory — the extracted tree — and the fetch
marker inside it. Nothing else, and never over an existing directory.

**Never travels.** A creation skill: it serves only before a project exists, so it is in
`export.skills.exclude` like `init-project` and `project-bootstrap`. The plugin vendors it.

**Hands off to** `/init-project`, in a session the person opens in the fetched tree.
