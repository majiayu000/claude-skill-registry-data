---
name: choose-edit-mode
description: "Decide how to change a document that already exists: ALTER, describe → edit → CREATE OR MODIFY, or a new document. The answer depends on who owns the document (your MDL scripts or Studio Pro). Use before editing anything in an existing app, before editing a project script that has no `mdl 1;` header, before re-executing DESCRIBE output, and before touching a Studio Pro-authored microflow or nanoflow."
---

# Choose the Edit Mode by Who Owns the Document

MDL has two ways to change a document, and each is safe in a different situation.

| | Declarative | Patch |
|---|---|---|
| Statement | `create or modify <type> X ( … ) { … }`, the whole definition | `alter <type> X …`, only the change |
| Source of truth | your `.mdl` scripts | the stored model |
| Use for | new apps and modules; documents your scripts created and nobody has edited since | documents made or edited in Studio Pro; marketplace modules |
| Risk | drops whatever the statement does not say, including content MDL cannot express | none for what it does not mention |

## The rule

1. **New app, new module, new document: write declarative MDL.** There is nothing to
   read and nothing to preserve.
2. **Existing Studio Pro document: change it with `alter`.** An `alter` leaves every
   element it does not name untouched. Measured: `alter page … set Caption` changed
   one string and byte-preserved every other translation on the page.
3. **describe → edit → `create or modify` only for documents mxcli created** and whose
   stored state is still what your script produced (nobody has changed them in Studio
   Pro since). On a Studio Pro-authored document this path is lossy even when you
   change nothing. On real projects it has flipped association storage from table to
   column, dropped page translations, dropped nanoflow annotation links, changed export
   levels, and dropped a snippet's type. `mxcli diff` runs the script on a scratch
   copy and lists every unit it would write, so run it first and expect "exec would
   write nothing" for a document you did not mean to change.
4. **Never `drop` and re-create an existing document to change it.** The new document
   gets new identities. For an entity, the runtime then drops its table and its rows.

Not sure who owns it? Treat it as Studio Pro-owned.

## Scripts are `mdl 1` — upgrade a headerless file before you edit it

Every script you write starts with `mdl 1;`. A project script **without** that
header is `mdl 0`, the alpha language: some statements mean something else there
(`limit 1`, a reassignment without `set`, a backslash in a string) and some
spellings `mdl 1` refuses. So **never mix dialects in one file.** Adding `mdl 1`
statements to a headerless file runs them under `mdl 0` rules, and typing the
header in by hand changes the meaning of the lines already there.

Before you edit a headerless project script, upgrade that file:

```bash
./mxcli fmt --upgrade --header -p app.mpr -w script.mdl   # rewrite to mdl 1 and add the header
./mxcli check script.mdl -p app.mpr                       # reports what exec would refuse
```

`fmt` rewrites every spelling and construct whose meaning the header changes, and
declines the header for the file when a construct has no mechanical rewrite or
when `exec` would then refuse a statement — it names each one. Fix those by hand,
or leave that file at `mdl 0` and put the new work in a new file that starts with
`mdl 1;`.

Then edit, `exec`, and **`exec` the same script a second time**: the second run
must write nothing — every statement reported unchanged, or "already in sync". That
needs re-runnable statements: `create or modify`, or `create … if not exists`, not
a bare `create`, which refuses an existing document. A write on the second run
means the script and the stored model disagree — find out why before you hand the
change over.

## Which document types have `alter`

`./bin/mxcli syntax` is authoritative. At the time of writing:

| Document | Patch statement |
|---|---|
| Entity, attribute, index | `alter entity` (add / rename / modify / drop attribute, set …) |
| Association | `alter association … set …` |
| Enumeration | `alter enumeration` (add / rename / modify / drop value) |
| Page, snippet, layout | `alter page` / `alter snippet` / `alter layout` { set / insert / drop / replace } |
| Workflow | `alter workflow` { set / insert before / after / into / drop / replace } — activities by name or 'caption' |
| Settings, security | `alter settings`, `alter app security`, `grant` / `revoke` |
| Many pages at once | `update widgets … where …` (see `bulk-widget-updates`) |
| **Microflow, nanoflow** | **none yet** |
| Menu, navigation profile, Java action | none (`alter navigation` replaces the whole profile) |

## Types with no `alter`: microflows, nanoflows, menus, Java actions

The only way to change one is to re-emit the whole document with `create or modify`.
On a Studio Pro-authored microflow that rebuild renumbers element IDs, removes merges
and resets connector curves, even for a one-line change. So:

- **Prefer adding over editing.** Put new logic in a new sub-microflow that you create
  declaratively, and limit the change to the existing flow to the one call that
  reaches it.
- **Keep the change minimal.** Start from fresh `describe` output, change only the
  lines you must, and do not reformat, reorder or tidy anything else.
- **Review the result before you hand it over.** Commit (or copy the `.mpr`) first.
  After `exec`, `describe` the document again and diff it against the original output.
  On an MPR v2 project, also check that `git status mprcontents/` lists only the units
  you meant to change (`mxcli diff-local` shows them as MDL). Anything else that
  changed is a loss, not your edit.
- If the flow is large or the change is broad, tell the user and suggest making the
  change in Studio Pro.
