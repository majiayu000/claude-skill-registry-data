---
name: unikit-mcp-audit
description: >-
  Curate .unikit/MCP-RECHECK-NOTES.md — the project's log of findings about the
  configured engine MCP server. Four jobs: re-stamp (the server moved, so every
  entry is suspect), replay (reproduce a `replay: safe` finding inside a
  disposable sandbox to see whether it still holds), retire (offer to drop what was
  fixed or went upstream), and upstream (print a ready diff for the packaged
  INDEX.md). Use for "audit the MCP notes", "are these findings still true",
  "recheck the MCP traps", "clean up MCP-RECHECK-NOTES", "the server was updated —
  revisit the notes". Replaying mutates a live editor, so it starts by telling you
  how to prepare it — save your scene, open an empty one — and asks once before
  touching anything. Everything it creates lives under a single UNIKIT_AUDIT_<runid>
  prefix, is deleted in one action, and the scene is never saved. To record a NEW
  finding use /unikit-mcp-trap instead.
argument-hint: "[optional: a note id such as R2, or `stamp` | `replay` | `retire` | `upstream`]  (mutates a live editor — asks first)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(date *)
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: tools
---

# MCP Audit — curate the recheck notes

`.unikit/MCP-RECHECK-NOTES.md` accumulates. Findings get fixed upstream, calls disappear,
servers move. Left alone the file drifts from a protection into a superstition — every
row costing a call, none of them still true.

This skill is the pass that keeps it honest. It is a **project** tool, not a release
tool: it curates what this project observed, and it never edits the packaged rules tree
(`.unikit/system/engine-mcp/` is rewritten by every `init` / `update`, so an edit there
is lost, and lost silently).

**The format is not owned here.** `/unikit-mcp-trap` owns
`references/notes-format.md`; this skill reads it as the interface and curates against
it.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md` and
apply it to all output (fall back to English if it is missing). Ids, `area` keywords, and
the observation protocol stay **English** — other skills grep them. Do not announce the
language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Bootstrap

Silently load — do not narrate:

1. **`{{skills_dir}}/unikit-mcp-trap/references/notes-format.md`** — the format
   specification: header fields, the two sections, ids, the genre rejections, and the
   `replay: safe` definition. Mandatory; without it, curate nothing.
2. **`.unikit/system/dev-principles.md`** — the evidence contract (A1/A2), the failure
   classes (A3), the area vocabulary (A8), and `no rules ≠ no rights` (A9). Read it
   whole — the part below its `LAZY-READ BOUNDARY` marker too: this skill touches editor
   state, so it is a first Editor task by definition.
3. **`.unikit/system/engine-mcp/INDEX.md`** — the delivery stamp (`server:`) and the
   base section, including **how a project-relative asset path is written for this
   engine** (see "The asset root is a contract" below). File absent →
   there are no known exceptions; that restricts nothing and switches nothing to
   `⏸️ MANUAL`.
4. **`.unikit/MCP-RECHECK-NOTES.md`** — the file being curated. Absent → say so and
   stop; there is nothing to audit and nothing to create.

Then pick the run id: `<runid>` is a short token unique to this run (a timestamp is
enough). Every object, asset, and file this skill creates carries it.

## The asset root is a contract, not a path

When a replay needs an asset, it goes under a **project-relative audit folder**:

```
<the project's asset root>/UNIKIT_AUDIT_<runid>/
```

**The literal form of that root is engine-specific and must not appear in this file.**
Take it from `.unikit/system/engine-mcp/INDEX.md` → the access/base section, which states
how project-relative paths are written for the configured engine. Not stated there → ask
the user once, and record the answer for this run only.

This is not pedantry about portability. A hard-coded root passes every guard in the
repository and then makes the sandbox contract **unsatisfiable on any other engine** —
silently, because the path simply resolves somewhere else. The whole safety of a replay
rests on "everything I created is under one prefix I can delete in one action". The same
split is why `unikit-gd-recon/SKILL.md` stays engine-agnostic and puts the per-engine
matrix into `references/code-recon.md`.

## Job 1 — stamp

Compare the notes header (`server:`) against the delivery stamp.

Different → print one line and continue:

```
WARN [mcp-audit] server in notes header ≠ configured (<notes> ≠ <configured>)
```

A mismatch makes every entry **suspect**, not void. Suspect entries stay in force: a
stale check costs one call and fails safe, while dropping checks because the server
underneath them changed throws away the protection they were written for. What the
mismatch changes is the **priority** of the replay pass — these are the rows most worth
replaying, and they are offered first.

The installer renames this file on every completed server switch, so a mismatch is not
the ordinary case: it means a switch was interrupted, or the file arrived by hand. That
is still information and not an error — and it is not a re-stamp instruction either, see
"What this skill never does".

## Job 2 — replay

Only rows marked `replay: safe` are ever replayed. `replay: manual` rows are **shown,
never executed** — see Step 2.

Replaying executes an arbitrary call taken from a note's `evidence` field against a live
editor. That is a mutating operation and this skill is granted accordingly; the
restraint lives in the **behaviour below**, not in the tool perimeter, and it is
compensated by the structural rollback in SWEEP and CONFIRM.

### The six-step safety envelope

The order is load-bearing. It is "gates with no edits between them" — the whole run is
described and confirmed before anything is created, and nothing is executed before that
confirmation.

**There are no pre-flight measurements. The user's confirmation is the only gate.**

That is a deliberate inversion of what stood here, and the reason is measurement, not
taste. The gate used to refuse on `dirty` — and a **fresh empty untitled scene, the one
safe place to run this, is `dirty=True` by default** (`mcp_status` → `scene=New Scene
dirty=True`). The gate therefore rejected the only correct state *structurally, every
time*, while a configured saved production scene reads `dirty=False` and sailed through.
The check was not merely weak; it was pointing the wrong way. Nor is such a check
portable: of the servers surveyed, one reports no scene-dirty state at all, one does not
document editor state, and one runs an engine where "compiling" is not a concept. The
status blob is not even atomic — four calls in one minute named three different ports.

**1 — INSTRUCT, then ASK.** Say what this run does and what the editor has to look like
for it, then ask once. **Nothing is created and nothing is mutated before the answer.**
The one thing read from the server beforehand is the optional courtesy line in item 3 —
it names the open scene, it is allowed to fail, and no decision depends on it.

The message carries, in this order:

1. **What the audit does to the open scene:** it creates objects there and it **never
   saves**. Whatever is in the scene when you say yes is what it will be worked on top of.
2. **What the user is asked to do:** (a) save the scene you care about, (b) create a new
   empty scene, (c) make sure nothing is compiling and Play Mode is off.
3. **A courtesy line naming the currently open scene** — see "The scene line is a
   courtesy" below.
4. **Everything that will be created:** the sandbox root `UNIKIT_AUDIT_<runid>`, the asset
   folder if one is needed, the filename prefix — plus which rows will be replayed and
   which will only be shown.
5. **The question:** `Editor ready? [y/N]`.

Anything other than an explicit yes ends the run. Nothing has been touched at this point,
so there is nothing to undo.

**2 — FILTER.** Drop `replay: manual` rows from execution and simply display them, with
the reason they cannot be replayed automatically. `manual` is also the **default** for
any row whose `replay` field is missing or unreadable.

**3 — MARK.** Place a console marker. Everything after it is the delta this run is
answerable for.

This is the **first call this skill is required to make** — worth knowing when reading a
transport error here. Only one call can precede it, the optional courtesy read in Step 1,
and it is allowed to have failed or been skipped, so its success is not something you can
lean on: treat a failure at MARK as the first evidence about the connection, not the
second.

**4 — REPLAY.** Execute strictly inside the sandbox:

```
UNIKIT_AUDIT_<runid>                     the single root object in the scene
<asset root>/UNIKIT_AUDIT_<runid>/       only if an asset is genuinely required
UNIKIT_AUDIT_<runid>_<name>              any file outside the project, baselines included
```

One root object, one folder, one filename prefix. Nothing is created outside them. If a
row cannot be reproduced inside the sandbox, it is not `safe` — record that and treat
the row as `manual` from here on.

Each replayed row yields a verdict on its own claim: does the trap still reproduce? Read
the state back — the response is not the answer, per A1.

**A row that failed to replay because the editor was unstable is not silently demoted.**
See "A failed replay is not automatically a demotion" below: the rule above turns "did not
reproduce in the sandbox" into `manual`, and applied blindly it would corrupt a perfectly
good `safe` row whose replay happened to land during a compile.

**5 — SWEEP.** Delete the sandbox root in one action. One root, one deletion; that is
what the naming was for.

**6 — CONFIRM.** Search by the `<runid>` prefix and **do not save the scene**.

Step 6 is the structural guarantee: the scene was never saved, so even a sweep that
fails leaves nothing on disk. That is why the scene must not be saved even when
everything looks clean — saving would convert a recoverable mess into a committed one.

### The scene line is a courtesy, not a check

Step 1 prints the name of the currently open scene. That line is **shown, and nothing
else**: it is not compared against anything, no value of it changes the run, and if the
call that produces it fails, the line is simply absent and the run continues to the
question.

Three words, so it is not turned back into a gate later: **shown, not checked.**

**Name the scene, never characterise it.** Print what it is called and stop there — not
"clean", not "empty", not "safe to use". This skill no longer measures scene state, so any
such word is invented; and even when it was measured, "clean" said far more than the
measurement supported. That was the original complaint: `dirty=False` on a fully configured
production scene got reported as a clean scene, which is a `false success` (A3) on the
reporting side. Where an unsaved-changes state genuinely has to be described anywhere in
this pipeline, the words are **"no unsaved changes"**, which is what was actually read.

What it is for is the original complaint. A user reads "create a new empty scene", says
yes, and has in fact forgotten — with the name in front of them they see their production
scene sitting there and answer no. It solves that by informing a human, which is the only
place the judgement belongs now.

### A failed replay is not automatically a demotion

A `safe` row whose replay does not reproduce is a **retirement candidate** (Job 3) — the
server was fixed, or the call is gone. A `safe` row whose replay fails while the editor is
unstable is **neither**: it is a run that produced no evidence.

So when there is reason to suspect instability — a compile started mid-run, the transport
answered inconsistently, the console shows unrelated errors after the marker — **do not
write `manual` into the row**. Report the failure with the reason and offer the demotion
to the user as a choice.

Without this, the REPLAY rule ("could not be reproduced in the sandbox → not `safe`")
quietly downgrades a correct row because a domain reload happened to land in the middle of
it, and the note is degraded for good on evidence that never existed.

### The sweep is proved, not announced

```
CLAIM:    the sandbox is gone
EVIDENCE: search for UNIKIT_AUDIT_<runid> → 0 objects, 0 assets
          console delta from the marker → no new errors
VERDICT:  CONFIRMED | NOT CONFIRMED
```

`NOT CONFIRMED` → a loud, `ERROR`-level report listing **by name** everything that
remains, and **no blind repeat of the deletion**. A second delete against an unknown
state is how a failed cleanup becomes a destructive one.

### Two hard limits on what may be touched

- This skill may delete **only what it created in this run**. No pre-existing name is
  ever a legitimate target for deletion or modification — not "it looks like leftovers",
  not "it is obviously temporary".
- Leftovers from an **aborted earlier run** are recognisable: a different `<runid>` under
  the same prefix. They are reported and offered for sweeping as a **separate action
  with its own confirmation** — never folded into this run's cleanup, and never swept
  because the prefix matched.

## Job 3 — retire

A row is a retirement candidate when:

- its replay no longer reproduces the trap — the server fixed it; or
- the replay fails because the call is gone — same outcome, no separate mechanism
  needed; or
- the packaged `INDEX.md` now carries the same check — the finding went upstream and the
  local row is a duplicate.

Offer each candidate with its evidence. **Removal is proposed, never automatic**: a
replay is one observation, and one observation is exactly the sample size the whole
"executors do not write these notes" rule exists to distrust.

Accepted → remove the row from **both** tables, leaving the id retired. Ids are never
reused: they are referenced from plans (`from: <plan>#<id>`), from upstream diffs, and
from earlier reports.

Then stamp the header: `audited: <today>`. This is the **only** field of the notes header
this skill writes, and the only place `audited:` ever moves — it is the cursor
`/unikit-mcp-trap` reads to decide which plans are new.

## Job 4 — upstream

A local row that would help every project using this server belongs in the packaged tree
instead. Print a **ready diff** for `mcp/<engine>/rules/<server>/INDEX.md` — the check
row in the packaged form (`id | area | confirm that`), with the observation kept beside
it as PR context.

Print it. Do not apply it: the packaged tree lives in the UniKit repository, is owned by
the maintainers, and is retired there by a conformance run plus a diff. After the PR
merges, the local row becomes a duplicate and the next audit retires it under Job 3.

## What this skill never does

- **Never saves the scene.** Not on success, not to "clean up". Step 6.
- **Never creates a scene of its own, and never re-opens the one that was there.** The
  dangerous half is the **return**, not the creation: opening the production scene back
  over a dirty scratch scene is a second `destructive default` call — a class this very
  server declares (`a scene is created over an unsaved one`) — and the editor's
  Save / Don't Save dialog is one an agent cannot answer. Preparing the editor is the
  user's step, in Step 1, and it stays there.
- **Never deletes or edits anything it did not create in this run.**
- **Never repeats a failed sweep blindly** — it reports what remains, by name.
- **Never edits the packaged rules tree**, and never edits a plan.
- **Never rewrites `server:`** in the notes header to make a mismatch go away. The
  mismatch is information: it is what makes rows suspect.
- **Never writes `⏸️ MANUAL`** because rules are missing, and never treats an
  unreachable editor as proof that a capability is absent — that is a stop-condition
  (A7), reported as a fact.

## See also

- `/unikit-mcp-trap` — record a new finding; owner of `references/notes-format.md`.
- `.unikit/system/dev-principles.md` — the evidence contract, the failure classes, and
  the degradation ladder this skill descends when a route is unavailable.
