---
name: event-modeling-design
em-version: 1.22.0
description: >-
  Use when structuring a draft event model into swimlanes and the four patterns (State Change,
  State View, Automation, Translation), evaluating a model's structural completeness, or writing
  implementation-ready deep slice documents (field tables, invariants, Given/When/Then scenarios,
  error flows) for a model that already has its happy-path spine. Drives `em`'s model and slice
  phases — the core modeling work between discovery and implementation.
---

# Event Modeling — model & slice

You are facilitating the core modeling work: turning a draft happy-path spine into a
structurally complete, validated model, and then a deep implementation-ready spec per slice.
Your job is to **extract an accurate model from the user through Socratic questioning** — never
to invent the domain. You drive the `em` CLI to render the model live, and you produce
implementation-ready slice docs.

Read `../event-modeling-shared/reference/operating-principles.md` (preconditions, project
layout, the Socratic/validation discipline every phase follows) and
`../event-modeling-shared/reference/methodology.md` (the 7 steps + 4 patterns) before doing real
work — they are the source of truth. Run the preconditions there first: this phase expects a
draft model already exists (from `event-modeling-discover`'s `discover` or `extract` phase).

## Write scope, evidence, versions (MIL-236) — read before any edit

Full rules: `../event-modeling-shared/reference/operating-principles.md` ("Write scope and
evidence"). In short:

- **Bound to this model's directory.** The session is bound to the model directory it started
  in (`dirname(<model>.em)`). Never write under another model's directory or to its contract
  file. Read a neighbour only through its public surface (`public: true` elements in
  `em export <neighbour>.em`, or its committed contract), read-only.
- **Seam change request, never a cross-model edit.** When an open question needs another
  model's `public` element changed, add one dated bullet to THIS model's `.event-modeling.md`
  `## Decisions log`:
  `- YYYY-MM-DD: seam change request → <producerKey>:<kind>.<slug> — <what> — <why>`.
  Keep the question open, `blocked on:` the producer's owners. Never edit the other side.
- **Out of scope during design — never write:** generated contract artifacts
  (`contracts/*.tsp`, any OpenAPI or JSON-schema output), SDD/spec artifacts (`specs/`,
  `.specify/` — read the constitution, never write it), implementation source (`src/`, the
  model's `Code roots:`), `plugin/`, and a draft slice doc's `version:`. Exception: after
  marking an element `public` or changing a field of a `public` element, run
  `em api generate <model>.em` and commit the regenerated contract with the model edit — the
  API-first gate (`em validate --slice-ready`) refuses a public-touching slice whose contract
  is missing or stale. Never hand-edit the contract.
- **Slice docs: edit authored sections only.** Never hand-edit a generated region
  (`<!-- GENERATED:em-slice-…:start -->` … `:end -->`: field tables, the Invariants list); after
  any model edit run `em slice sync <model>.em` (see **Generated vs authored sections** below).
- **Evidence rule.** The `.em` model and the slice docs are the evidence for modeling
  decisions. Never read implementation source, generated contracts or `specs/` to decide a
  modeling question — ask the user. Code is read only in `extract` and `conform`.
- **Version rule.** Never bump a draft's `version:` on edit. Before any `em slice revise`,
  run `em status <model>.em --json`: pre-release = the model's `modelVersion` entry has
  `design: null` **and** `slices.byStatus.shipped === 0`. Pre-release → never run
  `revise`; edit `draft`/`reviewed` docs in place. Released → the revision path in
  the `slice` phase below.
- **Pre-commit check.** Stage the session's files, run `em system scope --staged` (STOP on any
  `seam-crossing`), then `git diff --cached --name-only` (STOP on any path outside this model's
  directory, any out-of-scope path above, or a changed `version:` line on a draft doc).
  Unstage the offending path and tell the user why.

## Phase: `model` — steps 5-7

Goal: a structurally complete, **validated** model with correct patterns and swimlanes.

1. **Swimlanes & patterns (step 5).** **Name the storylines first**: the one main storyline (the
   end-to-end journey) and the secondary ones (retire a thing, extend an attribute, reorganize).
   Wrap each one's slices in a `storyline "Name" [source "url"] { slice … }` block (grammar and the
   optional `after "<storyline>"` timeline clause: `em-dsl.md`) so the diagram gets a band per
   story and `em render --storyline "Name"` can show one alone; slices keep their file order, and
   a model can adopt storylines incrementally (`slice-outside-storyline` is only an advisory
   warning) — but name them before you slice, not after. **Once the storylines are named, give
   each its own file** (GH #421): run `em storyline split <root>.em` so the root keeps the
   vocabulary and the storyline list with its flow (`storyline "Name" [after "Other"]`) and each
   story's slices live in `<slug>/<slug>.em` with its docs in `<slug>/slices/` — do this before any
   doc is wired, so nothing moves twice. **A storyline that reads another story's events declares
   `after` it** (`storyline-reads-without-after` flags the ones you miss); two stories that run in
   parallel read nothing from each other. Then group events into **contexts** (bounded contexts /
   aggregates) — ask which events share a consistency boundary and who owns them. Classify each
   slice as one of the 4 patterns. **Share the slice between every automation or translation and
   the command it triggers** (the reaction — processor/translation — together with the command
   and event it produces; the read model it watches, if any, stays in the slice before). A
   translation or automation is a reaction: it **triggers a command and never records an event
   directly**. Add `translation` slices for external inputs (externally triggered: external →
   translation → command → event, no slice before) and for the system reacting to its own state
   (internally triggered: read model in the slice before → translation → command → event).
2. **Storyline review — before any slice doc is scaffolded.** Read the timeline as a story, not a schema
   (`../event-modeling-shared/reference/methodology.md`, "The story, not the schema"; em repo
   `docs/storyline.md`). Name the **main storyline** (end-to-end happy path) and every
   **secondary storyline** (retire, extend, reorganize), and group the slices under them; one
   lifecycle block per entity (N × create/update/archive, one trailing view each) is the CRUD
   shape — reshape it with the "Reshaping an existing model" checklist. Then the **intent test**
   per command (would a business person say this name at this step in the story? an endpoint-shaped
   name fails), the **question test** per view (write the question it answers; no question, no
   read model; a child view only when its query needs what the parent view lacks), the
   **views-as-lookups check** per `from "E"` on a view (does E add, change or remove a row here? if
   it only fills a column, put the column on the event that creates the row and drop E — see
   `../event-modeling-shared/reference/methodology.md`, "Views as lookups"), then the
   **trigger / housekeeping split** on what is left (*which event is the reason this row appears?*
   that one stays in `from`; every event that only keeps a row current or removes it moves to
   `updates from` — the view still reads it, the diagram no longer draws it; a to-do list with more
   than one or two inbound arrows is missing this split), the **continuation check** per `view X
   again` (it names only the events that changed the view since the previous instance, never the
   first instance's list again), and the
   **conditional-invariant signal** (invariants or fields that apply only "if `<field>` is set"
   mean two intents in one command: split it). Read each story on its own render and on the canvas
   (`em render <root>.em --map`), not on the full timeline. The `timeline-entity-clustered`,
   `command-second-intent`, `automation-split-by-outcome`, `view-lookup-source`,
   `again-restates-sources` and `storyline-reads-without-after` lints are the
   mechanical half (the lookup one only catches the cross-context cases — do the check by eye too); the
   design exit gate is `em validate --shape`. Shape the model first, scaffold docs after: a rename,
   split or merge from the reshape would orphan docs already wired with `--wire`. The `slice` phase is unchanged (timeline order).
3. **Elaborate scenarios — first pass (step 6).** Scaffold every slice's doc now, one per
   slice, none skipped: `em slice new "<slice name>" --pattern <state-change|state-view|
   automation|translation> --swimlane "<Persona> → <Context>" --wire <model>.em` writes
   `slices/<slice-name>.md` at `status: draft` (into the slice's own storyline folder when the model
   is split — pass the ROOT model to `--wire`) (the same command, flags, and `--wire`
   note-binding the `slice` phase's step 2 below documents in full). A slice whose only element
   is a `view X again` instance is a **continuation** (MIL-208), not a slice to scaffold —
   `--wire` refuses it and names the originating slice holding `X`'s first declaration; its
   scenarios go into that doc instead. Then, for each freshly scaffolded doc, hold a first-pass
   Socratic pass and write the happy-path Given/When/Then into
   its `## Scenarios (Given / When / Then)` section (as `### Scenario:` blocks — see **Generated
   vs authored sections** in the `slice` phase below) and the obvious invariants known so far into
   its `## Invariants / Business Rules` section — **into the doc, never into the state file.**
   Keep this pass shallow (no field tables, alternate/error flows, or NFRs yet — that's the full
   deep-dive in the `slice` phase below); the docs are the home for everything collected from
   here on, not yet implementation-ready specs. Because every doc already exists by the time the
   `slice` phase begins, its own step 2 scaffolding call is then a no-op — that phase picks up
   at its step 1's deeper pass. For a purely exploratory/backbone-mapping model that only needs
   status coloring right now (not a full spec per slice yet), `em slice stub-all <model>.em` is
   the one-command fast path: a near-free stub per undocumented slice, wired, in slice order
   (MIL-184) — skip the per-slice `em slice new` calls above and deepen individual docs later
   when the team is ready.
4. **Evaluate completeness (step 7).** Walk the model: every slice is a **complete** pattern, not a
   half-slice — **every command has something that triggers it**, every command emits an event,
   **every event is read by a read model**, **every read model has a consumer**, every view has a
   source, every UI is reachable, every connection is
   one of the six legal pairs, and every automation **and** translation triggers a command (none
   wired straight to an event, none with no command at all). Run `em validate` and resolve all
   errors and warnings — it catches a reaction wired straight to an event too now (see
   `../event-modeling-shared/reference/em-dsl.md`), so a clean run covers this case.
   For an unread event, don't just bolt on a view to silence the warning: ask the user who looks at
   this fact and what they do with it. The honest answers are "here's the read model we missed" or
   "nobody — so why are we recording it", and both improve the model.
   **Per `view`, also ask who reads it (MIL-215):** a person or client reads it → draw the `ui`
   that reads it; another model/system reads it → mark it `public`; only an automation reads
   it → nothing, it's internal by design. No new keyword — reachability is already what `ui` and
   `public` mean.
   **Per `view`, also ask whether each of its sources earns its place (GH #398):** for every
   `from "E"` on the view, does E add, change or remove a row here — or only fill a column on a
   row some other event already created? The latter is the views-as-lookups smell (methodology
   reference, "Views as lookups"): drop E as a source and have the event that creates the row
   carry the field instead. `view-lookup-source` flags the cross-context instances of this
   mechanically; a lookup from the view's own context (no `@Context` mismatch to key on) only
   this by-eye check catches.
   **Per translation fed from another model, declare what it consumes (MIL-235):** write
   `translation Order Intake consumes checkout:event.order-submitted`. The ref is
   `<modelKey>:<kind>.<slug>`, where kind is `event` or `view` and the target is marked `public`
   in its own model. The consumer declares the seam; the producer never lists its consumers, and
   the ref carries no version and no slice. Only a `translation` may carry `consumes`. If a
   reaction reads another model, it is a translation. `em validate` checks only the ref's
   grammar. Run `em system` from the repository (or on its `system.yaml`) to resolve it, and fix
   any `consumes-unknown-model`/`consumes-unknown-element` error. Never edit the other model to
   make a ref resolve. Ask its owner to publish the element instead, and record that ask as a
   seam change request (see **Write scope** above).
   **When you mark an element `public` here**, run `em api generate <model>.em` in the same
   session and stage `contracts/<model key>.tsp` with the model edit — the one derived artifact
   a design session produces, always by the command, never by hand.

5. **Shape exit gate (GH #282).** The model phase ends on the shape lints, not on your judgement
   of the storyline: run `em validate <model>.em --shape` (add `--json` to read it; exit code is
   always 0, so read the output). Every finding is either **fixed** in the model, or **accepted**
   as one bullet in `.event-modeling.md` `## Decisions log`:
   `- YYYY-MM-DD: shape-accepted: <rule> <refs> — <reason>`
   The gate passes only when **every remaining finding, waived or not,** has such a bullet. A
   baseline passed as `--waive-file <path>` (lines `<rule-code> <slice-key>`) only silences the CLI
   count for an estate; it never replaces the bullet. Re-run until each remaining finding has its
   bullet. **Refuse to move to the slice phase otherwise** (`em state set-phase slice` waits): the
   same kind of exit gate as asserting the generated contract above. Do not accept a finding
   without asking the user for the reason. The gate runs after doc scaffolding, so update or retire
   wired docs for renamed, merged or split slices.

End of phase: render, update state (`em state set-phase slice` — the mechanical marker the state
machine expects), and stop. Every slice already has a draft doc ready to receive the deep spec,
but slicing is deliberate work the team starts when it's ready for it, not this phase's automatic
next step.

## Phase: `slice` — deep slice documents

Goal: implementation-ready specs. Go slice by slice **in timeline order, starting with the first
slice on the storyboard** — never ask the user which slice to spec first, and never propose
starting with whichever slice looks highest-risk or most uncertain instead. Ratification
proceeds in the same order: later slices' scenarios and invariants depend on earlier slices'
events already being settled, so working out of order means re-litigating an earlier slice's
contract mid-spec. Check `README.md`'s Slices table for what's already done (run `em slice index
<model-name>.em` first if it looks stale).

**Outcomes stay in the slice.** When the deep dive surfaces failure, retry or timeout, add the
outcome events (`Fulfilment Failed`, `Fulfilment Retry Scheduled`, ...) and their Given/When/Then
scenarios to the SAME slice, with retry policy and failure handling as invariants in its doc —
never a sibling slice per control-flow branch (1.18.0 adds the lint `automation-split-by-outcome`). A new slice
only when a different actor or a different trigger is involved. Canon: Dilger, "one business
action… two different possible outcomes" and "Linearize it!"; Dymitruk, "a few of these stories
to show how a command can and cannot succeed".

This is also where **branch / unhappy-path events** are discovered and added to the model — as a
slice's alternate/error flows surface (a rejection, removal, cancellation, decline, expiry), add
the outcome event to the same slice unless a different actor or trigger is involved, then re-render. The happy-path spine from earlier
phases is the starting point, not the finished event set. **Every new event needs its reader too**
— a rejection or cancellation that nothing projects will warn, and usually the missing piece is
real (someone has to see that the request was declined).

For each slice:
0. **Check for re-ratification first.** A `draft` or `reviewed` doc is never re-ratified: edit
   it in place and leave its `version:` alone. If `slices/<slice-name>.md` already exists with
   `status: implemented` (or is ratified and needs a change), run `em status <model>.em --json`
   first. **Pre-release** (the model's `modelVersion` entry has `design: null` and
   `slices.byStatus.shipped === 0`): never run `em slice revise`; a ratified doc holds a
   human sign-off, so STOP, park the change as an open question, and let the ratifier decide.
   **Released** (either condition false): a doc with `status: implemented` is a
   re-ratification, not fresh authoring: hold a Socratic
   deep-dive on what changed (same rigor as step 1, scoped to the delta), update whichever
   sections actually changed, then express the change as the `## Delta` section — fixed heading,
   `### Added`/`Modified`/`Removed`/`Renamed` Requirement blocks each carrying its own scenarios
   (see `../event-modeling-shared/templates/slice.md` and
   `../event-modeling-shared/reference/slice-doc-schema.md#delta-section-grammar-and-lifecycle`)
   — **overwriting** whatever the section held before, never appending to it. Then continue at
   step 2 to bump `version` and flip `status` back to `ready-to-implement`, leaving
   `implementedIn` naming the prior version's PR (intended drift signal, not a bug — see the
   schema doc). Otherwise, this is first-time authoring: continue at step 1.
1. Hold a Socratic deep-dive to fill every section of `../event-modeling-shared/templates/slice.md`:
   intent, trigger/actor,
   command fields (types & rules), event(s) + payload (mark immutable facts) — field names and
   types go into the `.em`, the doc's tables are generated from it — invariants
   (give each a stable ID — see **Invariants live in the model** below), Given/When/Then scenarios (happy path + rule boundaries + edge cases),
   alternate/error flows (retries, idempotency, compensations), non-functional requirements
   (security/authz, PII/compliance, performance/SLA), read models affected, open questions. Park
   anything unresolved rather than guessing. Before finalizing field names/types or invariants,
   check whether the shape is already defined in **this model** (`.em` and its slice docs) or in
   a neighbour's public surface (read-only) — don't guess a shape that's already defined there.
   Never Grep or Read implementation source, OpenAPI files, DB migrations or `specs/` to settle
   it (evidence rule): if the user says the existing code is the source of truth, ask them for
   the shape, or park the question for an `extract` or `conform` session. Before finalizing an
   invariant, also compare it with the slices in
   **this same model** — never another `.em` model — that make the same kind of change (other
   `Archive*` or `Create*` state changes on different entities, say). If one of them already
   states an analogous rule, either state the same rule here — written out in this doc under
   this slice's own `INV-<MNEMONIC>-n` ID, not by pointing at the sibling's — or record why this
   slice's case differs. If this slice has a rule those siblings lack, raise that with the user
   as an open question against each of them; a ratified sibling changes only through its own
   re-ratification, never as a side effect of this slice. Repeating a rule across slice docs is
   correct: each doc is a self-contained spec, and whether the code behind those rules is shared
   is the constitution's call, not this doc's.
   **Invariants live in the model.** Write every NEW invariant into the `.em` as a standalone
   `invariant INV-<MNEMONIC>-<n> "rule sentence"` line directly after the command (or event) it
   guards — always with the rule sentence — then cite that ID in the doc's Invariants section as a
   plain mention and elaborate there (`- INV-CHK-1 — why, edge cases, the error returned`); never
   restate it as a `**INV-CHK-1:**` rule (`em validate` flags that as
   `invariants/declared-in-both`). A `public` command needs at least one invariant
   (`invariants/public-command-without-invariants`). A doc that already declares its own
   invariants keeps working; migrate one only when you are editing that slice anyway — move the
   ID and rule into the model, keep the doc's elaboration. Run `em validate` after the edit:
   `invariants/malformed-id` and `invariants/duplicate-id` are errors.
   **Generated vs authored sections.** A doc `em slice new` wrote has two kinds of section. The
   GENERATED regions — each command's, event's and read model's field table and the Invariants
   list, between `<!-- GENERATED:em-slice-…:start -->` / `:end -->` markers — restate the model:
   **never hand-edit a generated region.** To change a field, a type, or an invariant, edit the
   `.em`, then **after any model edit run `em slice sync <model>.em`**, which rewrites every
   region in place and leaves everything else byte-for-byte (`em slice sync <model>.em --check`
   reports a stale doc without writing). That includes a ratified or shipped doc: `ratifiedHash`
   covers the authored text only (since em 1.19.0), so sync rewrites its regions, keeps the
   signature and says so — never `em slice revise` a doc just to sync it; revise only when an
   authored section has to change. **Edit authored sections only**: Intent, Trigger &
   Actor, `Triggered by`/`Read by`/`Consumed by`, the invariant elaborations below the generated
   list, Scenarios, Alternate & Error Flows, NFRs, Dependencies, Open Questions. Scenarios use the
   constrained shape `em` reads back: a `### Scenario: <title>` heading, then `- **Given:**`,
   `- **When:**`, `- **Then:**` bullets with nested `  - ` items — all three in every block
   (`em validate` flags a block missing one as `slice-doc/structured-section-malformed`, and
   `--slice-ready` refuses it). A doc written before em 1.14 has no markers; leave it as it is
   unless you are re-creating it (`em slice new … --wire --force`, carrying the prose across).
   A question this version will not answer is deferred with `em slice defer <model> <key> "<question>" --until v<n> --decision "<what this version does>"` — never left `- [ ]`, never deleted, never answered by guessing.
   When the question lives on the diagram as an `issue "..."` note rather than on the doc, use
   `em slice defer <model> <key> --from-issue "<text>" --until v<n> --decision "<what this version does>"`
   instead: it writes the deferred item into the doc's Open Questions and removes the note in one
   step. A question that is *answered* is an edit to the authored section plus deleting the note —
   never a deferral.
2. **First-time authoring:** scaffold the doc mechanically rather than hand-writing the
   frontmatter — `em slice new "<slice name>" --pattern <state-change|state-view|automation|
   translation> --swimlane "<Persona> → <Context>" --wire <model>.em` writes `slices/<slice-name>.md`
   (kebab-cased to match, via the same slugging `em` uses everywhere else) with the canonical
   `schemaVersion`/`pattern`/`swimlane`/`status: draft`/`version: 1` frontmatter — exactly the
   five keys `em export` and the readiness gate require, no more — and the `# Slice:` heading +
   diagram-image stub already in place. `--wire` also inserts the `note
   "slices/<slice-name>.md"` line straight into the `.em`, onto the slice's primary element (the
   command for State Change, the view for State View, the processor for Automation, the
   translation for Translation), matched by export key — see step 4 for when it refuses instead.
   A slice whose sole candidate view is a later `view X again` instance is a **continuation**
   (MIL-208): `--wire` refuses it and names the originating slice holding `X`'s first
   declaration — write this slice's scenarios into that doc instead of scaffolding a new one.
   Both `--pattern` and `--swimlane` are required; an invalid `--pattern` is refused with the
   valid choices listed. Never hand-type this block, and never fall back to a placeholder
   pattern/swimlane to dodge the flags. It also writes every template section: the generated
   regions already filled from the model (field tables, Invariants list), the authored sections
   as placeholders. Then fill in the authored sections from step 1 (Intent, Trigger & Actor,
   invariant elaborations, Scenarios, ...) — those stay hand-authored; the generated regions
   follow the model through `em slice sync`. Record the originating need (ticket/conversation
   link) in the Intent section when one exists. When this doc exists because of a split, merge, or rename, add the matching
   lineage key(s) by hand (`split-from`/`merged-from`/`superseded-by`, `<slice-key>@v<N>` grammar
   — see `../event-modeling-shared/reference/slice-doc-schema.md` for the full schema; `em validate` catches a malformed one
   after the fact, see the `lineage-*` rules below).
   **Revision (step 0) — released models only.** Confirm the model is released first
   (`em status <model>.em --json`: the `modelVersion` entry's `design` is not `null`, or
   `slices.byStatus.shipped > 0`); on a pre-release model never run `revise`. The doc
   already exists, so `em slice new` doesn't apply here
   (it refuses to overwrite an existing file without `--force`, and forcing would blow away the
   doc's authored body) — run `em slice revise <model>.em <slice-key>` instead (MIL-283): it
   opens the next version as a **`draft`** in the existing frontmatter — `version` bumped,
   `status: draft`, the prior version's review and sign-off cleared — while the shipped version
   stays shipped in the shipped record (`implementedIn:`/`shippedVersion:`, untouched). If a
   question was deferred to this version, `em slice mark-implemented` already opened the draft
   at merge and the question is back on the list; `revise` then refuses ("the next version is
   already open") and you simply edit. The same command revises a ratified doc that **never
   shipped** (`ready-to-implement` with `ratifiedBy` set — a gap answered mid-build): the
   ratification is withdrawn and the draft opens. Either way the new version is a new spec:
   write the delta into `## Delta`, walk it in a review session (`em slice review --by`), and
   only then does `em slice ratify --by <name>` sign it. **Commit before ratifying (MIL-284):**
   `em slice ratify` records the commit and body hash it signs and refuses a doc with uncommitted
   changes — finish the doc's edits (deferrals included: `em slice defer` rewrites a body line, so
   a deferral after sign-off trips `slice-ready-body-changed-since-ratification`), commit, then
   ratify. A `draft`/`reviewed` doc is simply edited, and its `version:` never moves.
   **Public-touching slices (MIL-238).** On a slice that owns a `public` command, event or view,
   `em slice ratify --by <name>` refuses without one of two flags (`revise` takes neither — the
   confirmation belongs to the new version's ratification): pass
   `--meaning-unchanged` when this version does not change what the public contract means, or
   `--contract-change "<why>"` when a consumer must read the change differently. Without
   either, both refuse with `slice "<key>" touches the public surface — pass
   --meaning-unchanged, or --contract-change "<why>" if a consumer must read this change
   differently`; passing both refuses too. Run
   `em api generate <model>.em` first, so `em validate --slice-ready` sees a current contract
   (otherwise it blocks with `slice-ready-contract-stale`).
   Which flag applies is the ratifier's call, not yours: ask, never pick one to make the
   command pass. Ratification itself stays a human gate outside this session; a review session
   never ratifies (see `event-modeling-review`).
3. Render the slice's own diagram: `em render <model>.em --slice "<slice name>" -o
   slices/<slice-name>.svg` (kebab-case, matching the doc's filename and the `![Diagram]` stub
   `em slice new` already wrote) — redraws just this slice in its own canonical pattern shape.
4. Confirm it's wired into the `.em`: `em slice new --wire` (step 2) already inserted the `note
   "slices/<slice-name>.md"` line onto the slice's primary element's own declaration line — it
   only ever edits that one line, and only when doing so is unambiguous, so it refuses (writing
   NEITHER the doc nor the `.em` edit) rather than guess when the slice has zero or more than one
   candidate element of the primary kind, or when that line already carries a `note` clause. On a
   refusal, re-run step 2 without `--wire` — it prints the exact line to add, paste it onto the
   slice's primary element by hand.
5. Run `em slice index <model-name>.em` to regenerate `README.md`'s Slices table — the one
   canonical slice index — from the model and the doc frontmatter you just wrote (status,
   `implementedIn` once shipped). Never hand-edit the table; it's a generated block.
6. Re-render, run `em slice sync <model-name>.em --check` (it must print `ok:` for every doc you
   touched), and `em validate`.
7. Before committing, stage the session's files and run the pre-commit check: `em system scope
   --staged`, then `git diff --cached --name-only`. STOP on any `seam-crossing`, any path outside
   this model's directory, any out-of-scope path (see **Write scope** above), or a changed
   `version:` line on a draft doc.

A finished draft doesn't become implementable here: it goes through the review gate and then the
ratification gate, both human, both outside this phase — see
`docs/process.md#the-slice-lifecycle-gates` for who runs which and in what order.

Before the project's first slice is implemented it also needs a ratified implementation
constitution (stack, code style, testing norms, NFR baselines, review norms) — the
`event-modeling-implement` skill elicits it, see its `reference/implement.md` §7.

End of phase: every slice that should exist has a doc — except a continuation slice (MIL-208, a
later `view X again` instance), which has none by design and is documented by the originating
slice instead — `README.md`'s Slices table is current, and the model validates clean. Suggest
`event-modeling-implement` for each ratified slice.
