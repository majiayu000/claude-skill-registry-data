---
name: event-modeling
em-version: 1.22.0
description: >-
  Use when the user runs `/em:event-modeling` (with or without a phase name), or wants to resume an
  event-modeling session without specifying which part of the process applies. Reads the model's
  `.event-modeling.md` state (or the given phase name) and routes to the right focused skill —
  em:discover, em:design, em:implement, em:conform,
  or em:review — or, for building a planned set of ready slices through scoped
  sub-agents to one PR per slice against main (an `em engagement`), em:engagement. If you already
  know which of those applies — starting a new model, extracting from existing code,
  slicing/writing specs, implementing a ratified slice, leading an engagement, checking drift, or
  running a live/stakeholder view — invoke that skill directly instead of this one.
---
<!-- GENERATED FILE from .claude/skills/event-modeling/SKILL.md by scripts/build-plugin.ts — do not hand-edit; run npm run docs:generate -->

# Event Modeling with `em` — resume / route

`em` drives Event Modeling through ten phases — `discover, extract, model, slice, implement,
conform, watch, review, validate, engagement` — split across six focused skills, one per stage of
the process. This router skill is the single entry point for `/em:event-modeling`: it figures out
which phase applies and hands off, so you never need to remember which of the six skills a given
phase lives in.

| These phases... | ...live in this skill |
|---|---|
| `discover`, `extract` | `em:discover` — starting a new model, or extracting a current-state model from an existing codebase |
| `model`, `slice` | `em:design` — structuring the model into swimlanes/patterns, writing deep slice specs |
| `implement` | `em:implement` — building one ratified slice into merged, tested code |
| `conform`, `validate` | `em:conform` — drift-checking a model against its codebase, walking validation diagnostics |
| `watch`, `review` | `em:review` — the live browser viewer, facilitated stakeholder walkthroughs |
| `engagement` | `em:engagement` — build a planned set of ready slices through scoped sub-agents to one PR per slice, each against main |

## Routing logic

1. Check the tool: `em --version`. If missing, tell the user to run `npm i -g @milehimikey/em`
   and stop until installed. Then check this vendored bundle's own currency against it — see
   `${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md`'s Preconditions step 2: a bundle
   even one minor version behind the installed em is a STOP, not a warning — only a patch-only
   gap proceeds normally.
2. Parse `$ARGUMENTS` for a phase name.
   - **A recognized phase name** (`discover`, `extract`, `model`, `slice`, `implement`,
     `conform`, `validate`, `watch`, `review`, `engagement`): look it up in the table above and invoke that
     skill directly (via the `Skill` tool), passing the phase name along so it knows exactly
     where to start. Don't re-derive state first — the target skill's own preconditions handle
     that.
   - **No argument:** locate the model (an `.event-modeling.md`/`*.em` pair in the working
     directory, or one level down under `models/<slug>/` for a multi-model project — see
     `${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md`). If found, run
     `em state read <dir>` and read its `phase` field as JSON — don't parse the state file's
     bullets by hand. Map that phase through the table above and invoke the matching skill,
     telling it to resume at the recorded `step` too. If no model exists yet, ask the user
     whether this is a new model (`em:discover`, `discover`) or an existing system to
     extract from (`em:discover`, `extract`), then invoke that skill.
   - **An unrecognized argument:** treat it as free-text intent and pick the best-matching skill
     from the table's description, same as you would if the user had asked in plain language.
3. **Steer late work to `em:review` (MIL-236).** When the phase resolves to `slice`
   (recorded or requested), run `em status <model>.em --json` before handing off. Recommend
   `em:review` to the user instead of `em:design` when either holds:
   - no slice doc is left to write or deepen: `slices.byStatus.draft === 0`,
     `slices.byStatus.noDoc === 0`, and `slices.byStatus.reviewed +
     slices.byStatus.readyToImplement > 0`;
   - the state file's `## Open questions / parking lot` section has an unchecked `- [ ]` item.
   Say why: closing open questions and walking slices to the review gate is the review skill's
   job, not broad consistency work. Invoke `em:review` when the user agrees;
   otherwise hand off to `em:design` as the table says.
4. **Never do the phase work here.** Recommend the focused skill by name and hand off. Never run
   a cross-cutting "make everything consistent" pass from this skill: no sweeping edits across
   slice docs, no regenerating or hand-editing derived artifacts, no reading implementation code
   to settle a modeling question. The design-session write scope below applies to anything
   started from here.
5. Once you've handed off, this skill's job is done for the session — the target skill owns the
   conversation from there, including re-invoking `em:event-modeling` (this skill) itself at the end
   if the user wants to stop and resume later.

## Design-session write scope (MIL-236)

These rules bind every `discover`/`model`/`slice` session, whichever skill runs it. The full
text is in `${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md` ("Write scope and
evidence").

- **Bound to one model directory.** The session is bound to the model directory it started in
  (`dirname(<model>.em)`). Never write under another model's directory or to its contract file.
  A question that needs another model's `public` element changed becomes a **seam change
  request**: a dated Decisions-log bullet in THIS model's `.event-modeling.md`, and the question
  stays open as blocked-on-upstream.
- **Out of scope during design — never write:** generated contract artifacts
  (`contracts/*.tsp`, any OpenAPI or JSON-schema output); SDD/spec artifacts (`specs/`,
  `.specify/` — the constitution may be read, never written); implementation source (`src/`,
  the model's `Code roots:`); `plugin/`; a draft slice doc's `version:`.
- **Evidence rule.** The `.em` model and the slice docs are the evidence for modeling
  decisions. Code is consulted only in `extract` (`em:discover`) and `conform`
  (`em:conform`).

## Shared reference material

Every phase skill (and this one) points back to the same shared resources rather than
duplicating them — read them once, they apply everywhere:

- `${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md` — the Socratic/validation discipline
  every phase follows, the preconditions above in full, and the project layout these skills
  create (including multi-model projects).
- `${CLAUDE_PLUGIN_ROOT}/shared/reference/methodology.md` — the 7 steps and 4 patterns (Event Modeling
  methodology).
- `${CLAUDE_PLUGIN_ROOT}/shared/reference/em-dsl.md` — `em`'s DSL grammar, CLI reference, and the full
  `em validate` rule catalog.
- `${CLAUDE_PLUGIN_ROOT}/shared/templates/*.md` — the slice/state/model-readme/conformance-report
  templates every phase scaffolds from.

## em command reference (quick)

<!-- GENERATED:cli-quick:start -- run `npm run docs:generate` to refresh, do not hand-edit -->
```bash
em --version
em init <name>.em                          # optional starter scaffold
em scaffold <name>                         # full project: <slug>/<slug>.em, README.md, .event-modeling.md
em validate <name>.em                      # check rules; exit 0 if clean/warnings only
em render <name>.em -o <name>.svg          # render (svg/png/pdf by extension)
em render <name>.em --emit-dot             # inspect generated Graphviz DOT
em render <name>.em --slice "<slice-name>" -o slices/<slug>.svg   # this slice's own diagram
em watch <name>.em -o <name>.svg           # re-render on save (run in background)
em watch <name>.em -o <name>.svg --serve   # + the live browser viewer: instant push-reload, pan/zoom (--port N)
                                            #   click "Review mode" for a slice-by-slice storyboard walkthrough
```
<!-- GENERATED:cli-quick:end -->

Always finish a working session by: re-rendering, running `em validate`, and updating
`.event-modeling.md` — `em state set-phase <phase> [--step <n>]` for the current phase/step,
decisions and open questions by hand, and `em state log-usage <model>.em --phases <phases>` for
the Usage log entry. Before committing a design session, stage the files and run the pre-commit
check in `${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md` ("Write scope and
evidence"): `em system scope --staged` plus `git diff --cached --name-only`; STOP on any finding.
