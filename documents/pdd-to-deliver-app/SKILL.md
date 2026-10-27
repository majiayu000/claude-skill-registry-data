---
name: pdd-to-deliver-app
description: >
  Build the CommCare Deliver (service-delivery) app from an approved PDD via Nova. Needs an
  approved PDD.
disable-model-invocation: false
---

# PDD to Deliver App

Generate the Deliver (service delivery) app from the PDD using the Nova
plugin (`voidcraft-labs/nova-marketplace`, slash command
`/nova:autobuild`).

## Inputs

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `1-design/idea-to-pdd.md` | source PDD; archetype + Deliver App Specification + delivery unit drive the Nova brief |
| Run root | `runs/<run-id>/inputs-manifest.yaml` | the resolver from a PDD-named `[FIXED]` source instrument to the `file_id` of its published file in `inputs/`. Step 4k reads that file — the workbook/PDF itself, never the brief — to check every scoring constant against the source (ace#1527). `inputs[]` lists direct child FILES only, so when the published bundle is a SUBFOLDER of `inputs/` 4k walks the manifest's own recorded `subfolders_not_listed[].folder_id` one level to find it (ace#1648). No `[FIXED]` instrument → 4k skips and says so; a `[FIXED]` instrument whose source cannot be resolved → 4k **HALTS**, never skips. |

## Products

- `3-commcare/pdd-to-deliver-app_summary.md` — Deliver-app structure summary (forms, fields, `nova_app_id`), whose body ends with a `## Build notes` section for the build team's non-decision notes (Step 7)
- decision rows in the run's `decisions.yaml` (`phase: 3-commcare`, `skill: pdd-to-deliver-app`), one per latitude taken and per ambiguity hit — the run's review artifact (Step 7, § Decisions Log)

## Terminology — every string a worker sees

App name, menu (module) names, form names, question labels, hints, option labels, validation
messages and case-list column headers are reader-visible text, and
[`skills/_terminology.md`](../_terminology.md) binds them. In particular **US spelling, always**
(owner, 2026-10-20, no carve-out for worker-facing labels): "Enroll adults", "Adult Enrollment",
"program", "organization" — never "Enrol", "Enrolment", "programme", "organisation", even when the
PDD, the partner or the country uses UK English (connect-fi/20261018-1440 shipped "Enrol adults" /
"Adult Enrolment" on-device — ace#3232). Translations are the target language's own; the rule binds
the English source. **Never respell an identifier** — case types, case property names and question
ids (`days_to_enrolment`) keep their spelling, and the Nova prompt cue "CommCare Connect markers" is a
code-level phrase that stays as written.

## Process

1. **Read the PDD** from `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md` via Google Drive MCP.

2. **Extract the Deliver app spec** from the PDD. Pay special attention
   to the **delivery unit** — this is the most archetype-sensitive part
   of the spec and determines the form structure (see `## Archetypes`
   below).

3. **Compose a Nova brief** — a single natural-language description that
   `/nova:autobuild` consumes as its sole argument. Nova does not accept
   file paths or markdown attachments. The brief should:
   - Open with the delivery purpose and the verification artifact
     (1–2 sentences)
   - State the archetype framing explicitly (atomic-visit vs.
     focus-group session vs. multi-stage)
   - **Explicitly state this is a CommCare Connect Deliver app and
     that every form needs the appropriate `connect.deliver_unit`
     (or `task`) block per CommCare Connect's rules.** This is
     load-bearing language — without it, autobuild often skips the
     per-form Connect blocks even though its system prompt knows
     about them. The `app-connect-coverage` skill in Phase 3 Step 1.5
     is the safety net for cases where the brief was vague, but the
     more robust path is for this brief to be unambiguous up front.
     See `docs/learnings/2026-04-29-nova-connect-marker-bugs.md`
     § Bug 1 for the prompt-quality dependency.
   - **State the marker MECHANISM: a Deliver app must carry an APP-LEVEL
     Connect mode of `deliver` — set via
     `configure_connect({work_id, request_id, mode: "deliver", participants})` — AND
     every paid form must carry a `connect.deliver_unit` block.** The
     app-level mode is what makes Nova's compiler emit the
     `<learn:deliver>` marker into the released CCZ. **Leaving the app
     with no Connect mode ships a marker-less CCZ even when each form
     already has a `connect.deliver_unit` block** — Connect surfaces zero
     deliver units → Phase 4 cannot create a payment unit. Per form, set
     `connect.deliver_unit: {name, id, entity_id, entity_name}` — via the
     `participants[]` entry on `configure_connect`, or via
     `update_form({moduleUuid, formUuid, connect})` after build; the form
     stays `type: registration` — there is no special deliver form type.
     This mirrors the Learn app, which compiles its `learn_module` /
     `assessment` markers because its app-level mode is `learn`. Name
     `mode: "deliver"` explicitly in the brief so the architect sets it as
     part of the build, not as an afterthought.
     - **Do NOT** tell the architect the marker is "module-level" via
       `module_type` / `add_module`, and do NOT let the app land with no
       Connect mode. Live Nova `update_module` accepts only `name` (no
       `module_type`); there is no `add_module` tool (it is
       `create_module`, which has no Connect parameter). A brief that
       frames the marker as module-level leads the architect to leave the
       app-level mode unset and ship a marker-less CCZ — the root cause of
       the `malaria-rdt/20260603-1600` Phase 3 halt.
     - **`update_app` no longer carries `connect_type`** — it was removed
       in Nova's 2026-07-31 redeploy (dimagi-internal/ace#1133) and
       `update_app({work_id, request_id, name})` now sets the display name only.
       `configure_connect` is the ONLY path to the app-level mode, and it
       is **REPLACE-ALL**: every form omitted from `participants[]` has
       its Connect block CLEARED. See Step 4e.
     - **The `get_app` / `get_form` `[Connect enabled]` flag is a FALSE
       POSITIVE for compile** — it shows whenever a form carries a
       `connect.deliver_unit` block, even when `connect_type: ""` means the
       marker will NOT compile. Never treat `[Connect enabled]` as evidence
       the marker shipped; verify against the compiled CCZ
       (`connect_markers.deliver ≥ 1`, see Step 4e + `app-release-qa`).
     > For the mechanism rationale + the controlled malaria-rdt disproof,
     > see reference.md § Marker mechanism.
   - **REQUIRED — every form that needs its own paid deliver_unit
     MUST live in its own module.** Nova's `compile_app` emits the
     module slug as the `<learn:deliver id="...">` attribute for
     every form in the module, and Connect's HQ→Connect sync dedups
     deliver_units by `(app, slug)`. Two forms in one module produce
     ONE deliver_unit (named after the first form, second form
     silently unpaid in production). Architect each module with
     exactly one paid form. Insert this paragraph **verbatim** into
     the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Every form that needs its own paid deliver_unit
     > MUST live in its own module. Connect's HQ→Connect sync
     > dedups DeliverUnit records by `(app, slug)` and Nova's
     > `compile_app` reuses the module slug as the
     > `<learn:deliver id>` for every form in that module. The
     > result: two forms in one module collapse into ONE
     > deliver_unit with the first form's name, leaving the second
     > form's submissions silently unpaid because no payment_unit
     > can be wired to a non-existent deliver_unit. The default
     > Nova choice — group related forms into one module — does
     > not transfer to Deliver apps. Use exactly one paid form per
     > module.

     See `feedback_connect_deliver_unit_per_module` memory for the
     full mechanism + reproduction history.
   - Describe the delivery form's structure section by section
   - List the required Connectify fields (Deliver Unit, Entity ID)
   - Reference the relevant PDD section (Evidence Model, Output
     Specification, etc.)
   - **REQUIRED — Forbid angle-bracket placeholder notation in
     label/option/hint text.** Insert this paragraph **verbatim** into
     the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Do NOT use literal `<` or `>` characters in any form
     > label, option label, hint text, constraint message, or itext
     > value. Nova's XForm emitter does not entity-encode `<`/`>` in
     > label text, so a literal "<placeholder>" or "<expected format>"
     > becomes invalid XML when CCHQ parses the form during
     > `make_build` (CCHQ rejects with "Error parsing XML: StartTag:
     > invalid element name"). Use words ("placeholder text", "the
     > expected format") or backticks (`expected format`) for
     > placeholder syntax. `&` is NOT restricted: Nova entity-encodes
     > it to `&amp;` and HQ builds it, so keep a partner's published
     > name verbatim, `&` included (verified against a released build,
     > ace#2150). This applies to hint text and constraint messages too,
     > anywhere literal `<`/`>` would be tempting (e.g. format hints,
     > validator-message templates).

     Filed upstream as voidcraft-labs/nova-plugin issue #15
     ("XForm emitter does not entity-encode `<`/`>` in label text");
     this skill-side constraint is the workaround. Phase 3's
     `app-release` Step 4a surfaces a typed `BuildRejectedError` (with
     form name + line/col) and dispatches a Nova architect repair
     loop if the architect violates this constraint anyway, so the
     operator gets clean diagnostic + auto-recovery instead of "Cannot
     make new version" + a CCHQ UI peek. See
     `docs/learnings/2026-04-29-nova-connect-marker-bugs.md` § Bug 4.
   - **REQUIRED — Set `connect.deliver_unit.id` AND `connect.task.id`
     explicitly to short stable identifiers, separately from the human-
     readable `name`.** This is the load-bearing constraint; the ≤40-char
     name fallback below is just a safety net. Insert this paragraph
     **verbatim** into the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Every `connect.deliver_unit` and `connect.task` block
     > MUST include an explicit `id` field. The id is the Connect slug —
     > it MUST be short (8-20 chars), lowercase, snake_case, code-like,
     > and stable across renames of the human-readable name. Examples:
     > `shop_registration`, `sample_prep_initial`, `wohl_shipment`. Do
     > NOT rely on Nova's default derivation (which slugifies the module
     > name) — that conflates the Connect slug with the display name and
     > trips Connect's 50-char `DeliverUnit.slug` column on any name that
     > slugifies past ~40 chars. The `name` field is a separate, human-
     > readable string that can be any length and is what shows up in
     > the deliver-unit picker on Connect — terseness is preferred for
     > picker readability but not required for correctness once the id
     > is set explicitly. Vellum-authored apps (the human-driven
     > authoring path in HQ's form designer) separate these into two UI
     > fields ("Delivery Unit ID" / "Task ID" and "Name") and humans
     > naturally pick short identifiers; Nova's API exposes the same two
     > fields but the architect has to set both explicitly because there's
     > no UI to nudge the separation. See
     > `docs/learnings/2026-05-17-connect-slug-length-50-char-trap.md`
     > § Generalization (Vellum-as-source-of-truth) for the full mechanism
     > + source citations.

   - **REQUIRED — Keep deliver_unit/task names short enough that the
     derived slug fits Connect's 50-char column (FALLBACK).** This is
     the defense-in-depth fallback for cases where the explicit-id rule
     above is missed. Insert this paragraph **verbatim** into the brief,
     in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: If you have not set `connect.deliver_unit.id` /
     > `connect.task.id` explicitly per the rule above, the `name` field
     > MUST be ≤ 40 characters as a fallback — Nova's default slug
     > derivation overflows Connect's 50-char `DeliverUnit.slug` /
     > `TaskType.slug` column on longer names and triggers an opaque
     > HTTP 500 from `connect_create_opportunity`. Prefer the explicit-id
     > rule above (cleaner; lets `name` be any length); this clause
     > exists only because architects sometimes skip the id field.

     Reproducer + class-level preventer: see
     `pdd-to-learn-app/SKILL.md` § REQUIRED — Set id explicitly. The
     structural backstop is `app-release` Step 6's
     `projected_connect_state.oversized_slugs.deliver_units` /
     `oversized_slugs.task_units` gate. Removal criteria: (a) drop the
     ≤40-char fallback when the upstream commcare-connect PR widens
     `DeliverUnit.slug` to `max_length=255` (already `=100` since a prior
     fix) AND `TaskType.slug` to `max_length=255` (dimagi/commcare-connect#1195)
     and `SLUG_LENGTH_LIMIT` in `mcp/connect/backends/commcare.ts` is
     bumped in lock-step. (b) KEEP the explicit-id rule even after the
     column widens — it's a cleanliness invariant matching Vellum's
     slug-vs-name separation, not just a workaround for the column width.
   - **REQUIRED — `entity_id` is Connect's dedup / payment grain; make
     it a BUSINESS KEY built from form fields, NOT the system case id.**
     `entity_id` is the value Connect uses to group deliveries onto one
     CompletedWork row per real-world entity (it does NOT stop a repeat
     being paid — ace#2512). It
     must therefore be a human-meaningful key derived from the PDD's
     `duplicate-detection-key` (Evidence Model Layer A) — the natural
     identifiers that define one unique entity (e.g. beneficiary name +
     phone; outlet + brand + batch) — built from the form's own fields.

     **Do NOT use the raw case id.** Both forms of it are wrong:
       1. `/data/case/@case_id` is hard-rejected by Nova `validate_app`
          ("references `/data/case` which doesn't exist in this form") —
          the case block is a build-time-emitted XForm node, not a
          blueprint field the validator's reference oracle can resolve.
       2. `#case/case_id` compiles to a casedb-lookup XPath that breaks
          install on a CASE-CREATE form (`XPathTypeMismatchException`
          from `FormDef.initAllTriggerables`; "A part of your
          application is invalid" on device) — Connect populates
          `case_id_new_<type>_<n>` not `case_id`, and the case isn't in
          `casedb` yet.
       3. Even if the validator accepted it, a per-registration case
          UUID gives **zero cross-registration / cross-FLW dedup** — two
          FLWs registering the same entity get two case_ids → two paid
          entities → the PDD's duplicate-detection is defeated. The case
          id is the wrong *grain*, independent of the validator quirk.

     A single `/data/...` field path as `entity_id` is install-safe
     (form fields resolve at `xforms-ready`) and `validate_app`-clean
     (it's a real form reference).

     **No component of `entity_id` may be free `text` where the option set is
     enumerable.** The business key is only as good as the fields it
     concatenates: an editable free-text component means one typo mints a
     SECOND payable delivery for the same real-world event, and two distinct
     entities that share a name collapse into one. Every key component that
     names a place, facility, community, or roster member MUST be a
     lookup- or inline-backed select — see
     `_app-component-library.md § structured-capture` § option sources for the
     `get_lookup_tables` + `set_field_options_source` recipe. If a key
     component genuinely cannot be made a select this run, record it as a decision
     row (§ Decisions Log) naming the `entity_id` you shipped, with
     `review_ask: recommended-confirmation` + `confirm_reason`; do not ship
     it silently.
     (Reproducer: `spark-facilitator/20260731-0656` — free-text `village`
     forced a mid-run repoint of the key from `village + date_of_meeting` to
     `community_id`, which was ALSO free text, so only the name-collision mode
     closed. ace#1136.)

     > For the 6-app deployed-practice audit that grounds this rule, see reference.md § entity_id business key.

     Insert the matching paragraph(s) **verbatim** into the brief, in
     their own paragraph, prefixed `REQUIRED:`.

     **Case-CREATE deliver_units** (registration forms — the typical
     atomic-visit Deliver app):

     > REQUIRED: For any `connect.deliver_unit` block on a CASE-CREATE
     > form, set `entity_id` to a BUSINESS KEY built from the form's own
     > fields — NOT the case id. Create a hidden calculate field (e.g.
     > `entity_key`) whose `calculate` is a `concat(...)` of the
     > natural-identifier fields that define a unique entity per the
     > PDD's duplicate-detection key, then set
     > `entity_id` to reference that field and `entity_name` to the
     > human-readable label field. Both are expression STRINGS (live
     > schema 2026-09-28: `type: ["string","boolean"]`, *"#form/age reads
     > an answer; #case/age reads the current record"*): `entity_id:
     > "#form/entity_key"`, `entity_name: "#form/beneficiary_name"`. A bare
     > id (`entity_key`) is refused as an unknown reference. (`#case/…` has
     > no case to read on a CASE-CREATE form — case reads belong on
     > followup forms; see the case-UPDATE rule below.) The pre-2026-09-27
     > `{ parts: [...] }` object shape is gone (voidcraft-labs/commcare-nova#693).
     >
     > **It is raw XPath — nothing concatenates or quotes for you.** A
     > literal separator written between two references (`#form/a - #form/b`)
     > is the XPath **minus operator**; the key evaluates to `NaN` — the same
     > constant for every worker — so Connect collapses the whole programme
     > into ONE payable entity and everyone after the first goes unpaid.
     > Nova accepts it with no error and the app builds clean; the only
     > symptom is unpaid work (ace#1232, proven against a compiled CCZ).
     > **Any literal separator MUST be quoted inside a `concat(...)`:**
     > `concat(#user/username, ' - ', #form/visit_start_time)` — or,
     > better, use the hidden-`entity_key`-field shape below, which builds
     > the `concat(...)` in the field's own `calculate` and points
     > `entity_id` at that one field.
     >
     > **Mind the grain of every component.** A date-only component
     > (`#form/visit_date = today()`) makes the key **per worker per day** —
     > a day's submissions pay as ONE. That is only right when the PDD's
     > paid unit IS one per worker per day. For a per-submission key, use a
     > time-bearing timestamp written `format-date(now(), '%Y-%m-%d
     > %H:%M:%S')` — **never a bare `now()`**, which in a hidden field
     > renders date-only and collapses to the same per-day key with no
     > error anywhere (ace#2935; `_app-component-library.md §
     > section-timestamps`).
     >
     > Example for a malaria RDT outlet visit whose dedup key is
     > (outlet, brand, batch): `entity_key` =
     > `concat(/data/outlet_name, ' - ', /data/rdt_brand,
     > ' - ', /data/batch_number)`. **Build the composite inside
     > `concat(...)`, as shown — do NOT express it as alternating
     > reference and bare `" - "` text.** An earlier version of this
     > section offered that shape as an equivalent, on a since-disproven
     > claim that the expression joins its members for you; it
     > does not. (The two statements contradicted each other between
     > ace#1230 and ace#969; the live-derived rule above wins.) The
     > hidden `entity_key` calculate
     > field is preferred for a second reason too — persisting the key
     > as form data is what lets case-UPDATE forms read the same grain
     > back (see below). Do NOT use `/data/case/@case_id`
     > (rejected by `validate_app` — the case block is not a blueprint
     > field) or `#case/case_id` (compiles to a casedb lookup that breaks
     > create-form install, and is the wrong dedup grain anyway: a
     > per-registration UUID gives no cross-registration/cross-FLW
     > dedup). Form fields resolve at `xforms-ready`, so a `concat(...)`
     > of them is install-time resolvable and validator-clean.

     **Case-UPDATE / multi-form deliver_units** (visit-series and
     multi-stage apps where the SAME entity is referenced across forms):

     > REQUIRED: When a `connect.deliver_unit` spans multiple forms (a
     > registration form plus later visit forms for the same entity),
     > every form MUST emit the IDENTICAL `entity_id` grain. On a
     > followup form, **read the case with a `#case/<property>`
     > reference in a hidden field's `calculate`** — that is the
     > sanctioned case-read path, and it is how a `longitudinal-visits`
     > key reaches the entity's history (its current phase/step, its
     > per-step counter). Build the key in a hidden `entity_key`
     > calculate and point `entity_id` at ONE `field-ref` to it:
     >
     > ```
     > entity_key.calculate =
     >   concat(#case/case_id, '-', #case/<state property>, '-',
     >          #form/<capped counter>, '-', #form/<payability discriminator>)
     > ```
     >
     > (Nova renders `#case/` as `#<case_type>/` in its read-back; both
     > mean the current record.)
     >
     > **This path is verified against a released CCZ, not just the
     > blueprint.** `voidcraft-labs/commcare-nova#458` (a followup form's
     > `case-ref` to its OWN case type rejected by the canonical round
     > trip) closed COMPLETED 2026-08-15. On
     > `spark-facilitator/20260925-1536` the Deliver followup form was
     > briefed with `#case/` reads, the architect built them without a
     > rejection, and the released build `5c1eef4323224550b1c36a7da9521e71`
     > compiles them as LIVE `calculate` binds over the case database —
     > not as preload-dependent `setvalue`s:
     >
     > ```
     > <bind nodeset="/data/entity_key" calculate="concat(
     >   instance('casedb')/casedb/case[@case_id = instance('commcaresession')/session/data/case_id]/@case_id, '-',
     >   instance('casedb')/casedb/case[@case_id = …]/pilot_fcap_step, '-',
     >   /data/capped_index, '-', /data/meeting_kind)"/>
     > ```
     >
     > (dimagi-internal/ace#2199.) `#case/case_id` is correct HERE because
     > the case already exists on a followup form; it stays wrong on a
     > CASE-CREATE form (see the case-create rule above).
     >
     > **Two case-READ shapes that are still NOT a read:**
     >
     > - **`caseWrite` is write-only — it does not preload.** A hidden
     >   field carrying `caseWrite` plus a literal `default_value` looks
     >   like a preload and is not one: it holds the literal and then
     >   writes that literal back, wiping the case property (ace#1224).
     >   Step 4i below halts on this shape. Read with `#case/` in a
     >   `calculate` instead.
     > - **A visible case-bound field DOES preload (ace#2006).** The
     >   released Deliver CCZ of `spark-facilitator/20260828-0703`
     >   contains `<setvalue … value="instance('casedb')/…"
     >   event="xforms-ready"/>` for 35 of its 36 answerable questions.
     >   That is a pre-fill of the previous visit's ANSWER, not a read
     >   you can build a key on — see the derived-state rule below.
     >   *Enforced:* `lib/casedb-preload-audit.ts`, run by
     >   `app-release-qa` § Step 2.9.
     >
     > **Do NOT fall back to `concat(username, <date>)` for a
     > longitudinal design.** That is the `atomic-visit` grain: it drops
     > the entity's history out of the key, so a per-entity cap ("3 paid
     > per step") cannot be expressed and the design silently becomes
     > "any visit counts" (ace#1462). It remains a legitimate key only
     > for an `atomic-visit` followup where the worker IS the entity
     > referent and no history is priced.
     >
     > **When the FLW does NOT map 1:1 to the entity**, `#case/case_id`
     > already distinguishes the entities the worker serves — no re-asked
     > select is needed. If a key component genuinely cannot come from
     > the case or the form, record it as a decision row (§ Decisions
     > Log) naming the `entity_id` you shipped.
     >
     > Caveat that still applies: every literal separator and every
     > per-form suffix goes **inside** `concat(...)`, never as a bare
     > `{ kind: "text", text: " - <form_name>" }` part between two
     > references.

     > **Case-write DERIVED state only, never the raw answers
     > (dimagi-internal/ace#2006).** Nova emits a casedb read-back
     > `<setvalue event="xforms-ready">` for **every** property the form
     > case-writes — measured 1:1 on the `spark-facilitator/20260828-0703`
     > Deliver CCZ: 42 properties written, the same 42 read, zero
     > asymmetry. **There is no write-only case binding from the
     > authoring surface.** So case-writing a visible question is the
     > same act as preloading it on the next visit.
     >
     > That build case-wrote all 35 answerable questions plus 7 derived
     > summary fields, so a CBF returning to a community met the whole
     > previous meeting pre-filled — including `meeting_conducted` and
     > `meeting_type`, the two fields Connect reads to decide payment —
     > and could re-file it by tapping Next and taking one new photo.
     >
     > **The split is clean, so take it.** Only the DERIVED fields are
     > load-bearing downstream:
     >
     > - the case list renders `last_meeting_date` and `pilot_fcap_step`
     > - the payment key reads `meetings_on_current_step`
     > - rollups read `Total_Attendance` / `Total_Participation` /
     >   `Percentage_Participation` / `cumulative_savings`
     >
     > All seven are hidden calculated nodes, so preloading them is
     > harmless — nothing asks the worker to confirm them. The 35 raw
     > answers were persisted for nothing: **M&E reads form submissions,
     > not the case**, and the case detail never displayed them (the same
     > verdict separately complained that neither payability field was
     > reviewable after submit — they were on the case, just never shown).
     >
     > So: put `case_property_on` on the derived summary nodes and NOT on
     > the questions. If a raw answer genuinely must live on the case,
     > say why in a decision row (§ Decisions Log) and declare it as an allowed exception to
     > `app-release-qa`'s `casedb_preloads` gate, so the trade is visible
     > rather than accidental.

     > **To make an answer REVIEWABLE after submit, mirror it into a hidden
     > field — do not case-write the question (dimagi-internal/ace#2006).**
     > Dropping `case_property_on` from the questions costs the case detail
     > its record of what the worker filed, and a worker who mis-tapped a
     > payability field then has no way to notice before payday. That is a
     > real requirement, and it does NOT require re-binding the question.
     >
     > Mirror it instead: a **hidden** field whose `calculate` reads the
     > question, carrying the `case_property_on`. The mirror is case-written
     > (so the case list and detail can render it) and it preloads (so does
     > every hidden field) — and the preload is harmless precisely because
     > nothing asks the worker to confirm a hidden field.
     >
     > **This is not a new pattern — the app already ships one.** In the
     > `spark-facilitator/20260828-0703` Deliver CCZ:
     >
     > ```xml
     > <bind nodeset="/data/meeting_summary/last_meeting_date"
     >       calculate="/data/meeting_date/date_of_meeting"/>
     > ```
     >
     > hidden, mirroring the `date_of_meeting` question, case-written to
     > `village.last_meeting_date`, and rendered as the case list's "Last
     > meeting" column. `Total_Attendance` and `meetings_on_current_step`
     > are the same shape. Reuse it for any answer the design wants visible
     > after submit — a payability field is the obvious candidate, since the
     > worker cannot otherwise catch their own mis-tap.
     >
     > Name mirrors for what they are (`last_meeting_type`, not
     > `meeting_type`), so the case property that holds "what was last
     > recorded" is never confused with the question that asks "what
     > happened this time".

     **Payability-scoped keys** (any form where SOME submissions are not
     paid work):

     > REQUIRED: When the PDD marks a SUBSET of submissions to this form
     > **non-payable** — a did-not-happen branch, a screening-only
     > visit, an ineligible-household record, a committee meeting on a
     > form that also records community meetings — the **payability
     > discriminator MUST be a component of `entity_id`.**
     >
     > Derive the key from the PDD's **paid-unit definition**, not only
     > from its `duplicate-detection-key` identity fields. The key must
     > be unique per *payable* event, so that a non-payable submission
     > occupies a DIFFERENT key space and cannot consume the payable
     > one. An identity-only key on such a form means the FLW's
     > non-payable submission mints the key first, the real payable
     > visit dedups against it, and the worker is structurally blocked
     > from being paid for work they actually did — while the form's own
     > closing text often tells them to record both.
     >
     > Put the discriminator **inside** the `concat(...)`, never as an
     > extra `parts[]` entry (caveat (ii) above). A dedup key of
     > (community, date) on a form that records both committee and
     > community meetings becomes
     > `concat(/data/community_code, '-', /data/meeting_date, '-', /data/meeting_type)`.
     >
     > The discriminator is now a key component, so the "no free `text`
     > where the option set is enumerable" rule above applies to it: it
     > MUST be a select. On the CASE-UPDATE path the discriminator must
     > be answered on THIS form — an ordinary `field-ref` to the form's
     > own select. Do NOT reach for the entity's stored copy: a followup
     > form cannot read its own case (see the case-UPDATE rule above), so
     > a discriminator that "comes off the case" ships as a constant.
     >
     > If the PDD's non-payable set cannot be expressed as a form field
     > at all, do NOT ship the identity-only key silently — record as a
     > decision row (§ Decisions Log, with `review_ask:
     > recommended-confirmation` + `confirm_reason`) that non-payable
     > submissions share the payable key space, and name the field that
     > would fix it.
     >
     > Scope note: this closes the *slot-consumption* mode. A non-payable
     > record still mints a CompletedWork on its own key until Layer A
     > verification rejects it — the `deliver_unit` marker itself carries
     > no relevance condition, which is upstream of ACE. (ace#969.)

     > For the upstream-validator note + the history of why the case id was abandoned, see reference.md § entity_id business key.

   - **REQUIRED — Architect must verify-then-retry every `add_fields`
     call.** Nova's `add_fields` has a partial-persistence quirk: a
     single call with N items often persists only the first few; a
     skipped verification ships forms that look complete in the build
     summary but render with missing questions in the actual app.
     Insert this paragraph **verbatim** into the brief, in its
     own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Nova's `add_fields` has a partial-persistence quirk.
     > After EVERY `add_fields` call, count the entries in the result's
     > `fields` array (Nova returns one `{id, uuid}` per field it
     > persisted) against the number you sent. If fewer came back, or
     > the call errored, call `get_form` on that form, re-issue
     > `add_fields` for the missing fields, and re-verify. Repeat until counts match. For forms with >10
     > fields plan on 2–5 `add_fields` invocations. Do not move on to
     > the next form before counts match — silent partial persistence
     > on form N becomes invisible once you start working on form
     > N+1.

     The count comes from the `add_fields` result, not a `get_form` read:
     in a fresh single-agent kaduna-graduation build (ace#3078 arm A,
     2026-10-17) all 25 successful calls returned exactly as many
     `fields` entries as were sent, while the old "call `get_form` after
     every call" wording contradicted the app-test economy rule below and
     the architect dropped the check entirely (0 `get_form` calls,
     ace#3124). Step 4a's full `get_form` read-back after the build is
     still the backstop.

     > For the full failure analysis, see reference.md § add_fields partial persistence.

     Also insert this paragraph verbatim into the brief
     (dimagi-internal/ace#1181):

     > REQUIRED: a large `add_fields` call can fail with
     > `InputValidationError: could not be parsed as JSON`. This is a
     > HARNESS-side failure, not a Nova one, and not a size limit —
     > `voidcraft-labs/commcare-nova#459` was closed NOT_PLANNED on 2026-08-16 after
     > Nova's request logs showed zero malformed bodies and payloads up
     > to 23.4 KB returning 200. The error is Claude Code's own
     > client-side error, raised when the model's streamed tool-call
     > arguments fail `JSON.parse` locally, before any request is made;
     > the two known causes are a generation cut mid-call and a deferred
     > tool's schema dropping out of context after compaction. The
     > "cut mid-string" appearance is an artifact of the harness echoing
     > only the first ~200 chars.
     > So: do NOT pre-batch defensively, and do NOT debug the payload's
     > quoting. Send the natural batch. IF you see that error, shrink the
     > batch and retry — as RECOVERY, not as a planned cadence. Nova
     > commits each batch atomically (all-or-nothing), so a retry after
     > this error cannot double-write. The verify-then-retry rule above
     > still applies to every batch.

   - **REQUIRED — Deployability (fitness) components.** A faithful
     transcription of the PDD's field list is NOT a deployable
     instrument. `pdd-to-deliver-app-eval`'s fitness axis (55% weight)
     **hard-fails** the build on each gap below; the build must emit the
     applicable components so the instrument is field-reliable, not just
     structurally complete.

     The canonical, parameterized text for each component lives in
     **[`skills/_app-component-library.md`](../_app-component-library.md)** —
     the single source of truth, paired 1:1 with the eval dimension that
     hard-fails a build omitting it. For each Deliver component whose
     **Trigger** fires for this app, open the library and insert that
     component's **Brief paragraph** into the brief **verbatim**, in its
     own paragraph, prefixed `REQUIRED:`, substituting any `<PARAM>`
     placeholders from the PDD. Emit-checklist (see the library for full
     text + triggers):

     - `gps-accuracy-capture` — PDD Evidence Model states a GPS radius.
     - `init-safe-calculates` — always emit alongside any capture-later
       calculate (always pairs with `gps-accuracy-capture`).
     - `data-quality-constraints` — always, for any data-capture form.
     - `case-write-back` — any case-UPDATE / follow-up form that captures
       new observations.
     - `structured-capture` — any answer with an enumerable option set, **any
       field the PDD spells `select` / `lookup` / "choose from" / "from the
       registered X", and any field that feeds a Connect `entity_id`.** A
       PDD-declared select that ships as free `text` is a DEFECT, not a
       degradation: the architect must call `get_lookup_tables` and bind the
       option set with `set_field_options_source` (lookup- or inline-backed)
       rather than falling through to `kind: text`, and any degradation that
       does happen must be recorded as a decision row (§ Decisions Log).
       Verified ACE-direct by
       Step 4f (ace#1136).
       Table values can be read ONLY via choice-list binds and values saved
       at submit (case writes) — never inside a calculation or label (Nova
       refuses `lookup()` there); a build-time setting used mid-form becomes a
       constant with a hint and a decision row
       (`nova-integration.md § Where a table value can be READ`, ace#2974).
     - `section-timestamps` — PDD success metrics reference visit-time / a
       cost model.
     - `embedded-bc-script` — PDD specifies a verbatim behavior-change
       segment.
     - `app-language-layer` — PDD names a working language other than
       English (Deliver variant). The brief tells the architect to build
       the app in **English ONLY** and to call no language atom. **ACE
       owns the language layer**, ACE-direct, in Step 4l below — after
       every English-editing step has finished. That split is the fix
       for ace#1556: the architect's operating prompt forbids it saving
       self-generated target text, so a brief that asked it to author
       translations produced a silent no-op (207 units copied, 0
       translated, both targets, on `spark-facilitator/20260820-0817`).
       It also makes translate-LAST structural — the architect's turn is
       over before the language exists. Never stack languages inline.
       (Standing decision 2026-08-17, PR #1463, superseding
       ace#968/#1391; ownership split 2026-08-23, ace#1556 — see
       `_app-component-library.md § app-language-layer` for the proven
       contract and the ACE-direct recipe.) Graded by
       `language_conformance`.
     - `deliver-app-naming` — always. App name must contain "Deliver app".
     - `nova-authoring-rules` — always (Learn + Deliver). One paragraph of
       the nine refusals and lookups that recur across Nova builds (ace#3300);
       insert it verbatim, do not restate its clauses here.
     - `no-starter-module` — always (Learn + Deliver). Apps created before
       2026-09-27 were seeded with a placeholder module (top-level menu
       "Survey" → form "Survey" → one text field `question_1` labelled
       "Question 1"); since `voidcraft-labs/commcare-nova#693` a new app
       starts empty (`begin_work({new_app})`, no seed), so the component is
       now a guard for reused/older apps and a regression tripwire. Emit the component
       so the brief tells the architect to DELETE it, and to report whether it
       was present. Removal is currently architect discretion, and discretion
       is what varies run to run: on `bednet-check-2-visit/20260828-0629` the
       Deliver app shipped with the seed while the Learn app, briefed from the
       same template in the same phase, removed it unprompted. Enforced at
       release by `app-release-qa § Step 4` (ace#1787).
     - `live-photo-capture` — any image/photo capture question, but **do NOT
       put it in the Nova brief**. Nova's authoring surface has no appearance
       control: an `image` field's slots are `id` / `kind` / `label` / `hint` /
       `help` / `required` / `relevant` / `validate` / `calculate` /
       `default_value` / `caseWrite` / `optionsSource`, and none of them is
       `appearance` (`caseWrite.mode` saves a link to the attachment — a
       different thing). The component is real and enforced, just not here: it
       is applied POST-BUILD by `app-hq-settings` § Step 3, which fetches each
       Deliver form's draft XForm (`commcare_get_form_source`), injects
       `appearance="acquire"` onto every image `<upload>`, and patches it back
       (`commcare_patch_xform`) before `app-release`; `app-release-qa` then
       BLOCKER-gates it off the released CCZ form XML as
       `camera-only-appearance-missing`. Briefing it only makes the architect
       search for an atom that does not exist and report a spurious "unmet
       requirement" into the run's review record — the one place meant to
       carry REAL deviations (dimagi-internal/ace#1640; same defect as ace#1632, which
       hit `grid-menu-display` on bednet-check-2-visit/20260825-1310).
     - `no-section-module-language` — always. No user-facing "section" or
       "module" wording anywhere — including lookup-table rows, which render
       as choices or displayed text when a field is bound to the table
       (ace#2976).
     - `connect-supported-capabilities-only` — always. Use only capabilities
       that work WITHOUT an HQ feature flag; `commcare_connect` is the sole
       exception. **Most concretely: do NOT add case-search inputs** — a case
       LIST needs no flag, while a case SEARCH requires `search_claim` and
       fuzzy/advanced matching additionally requires `case_search_advanced`,
       and BOTH are `TAG_FROZEN` in HQ ("do not add new projects to this
       list"), so the build cannot ship as designed rather than merely waiting
       on provisioning (ace#1195).
     - `grid-menu-display` — always (Learn + Deliver), but **do NOT put it
       in the Nova brief**. Nova's authoring surface exposes no
       menu-display-format control at all: `update_app` sets only the display
       name, `create_module` / `update_module` carry no display-format field,
       `set_menu_media` sets icons and audio labels (Menu ICONS are a different thing and ACE does apply them — `app-media-coverage` at Phase 3 Step 1.7, via this same `set_menu_media`, using Nova's built-in topic/action icon slugs.), and `set_case_list_tile`
       lays out a case LIST, which is a different thing entirely. The
       component is real and enforced, just not here: it is applied
       POST-BUILD by `app-hq-settings` (Phase 3 Step 2.65) via
       `commcare_set_menu_display` + `commcare_set_app_menu_display`, and
       BLOCKER-gated by `app-release-qa` off the released app's raw doc.
       Briefing it made every architect build report a spurious "unmet
       requirement" into the run's review record — the one place meant to
       carry REAL deviations — and invited the architect to reach for an unrelated atom
       to satisfy the paragraph (dimagi-internal/ace#1632; live on
       bednet-check-2-visit/20260825-1310, where Step 2.65 then applied all
       three fields HQ-side on the first attempt).
     - `observable-before-derived` — any visit/encounter form with an
       outcome / disposition / status field. Ask observations in
       real-world order; COMPUTE the outcome. A user-facing outcome
       question placed before its own inputs is a defect (ace#979).
     - `constraint-locality` — always, for any form with constraints. A
       constraint must be fixable on the screen where it fires; it may
       reference only `.` or same-repeat siblings (ace#980). **Carve-out
       (ace#1560): a MINIMUM-rows gate must be bound OUTSIDE the repeat it
       counts.** A constraint on a node inside a repeat is evaluated per
       repeat INSTANCE, so at zero repetitions it never evaluates — the one
       case the gate exists to catch. `count(/data/roster[…]) >= 1` bound on
       a question INSIDE `/data/roster` is a same-repeat sibling reference,
       satisfies the sentence above exactly, and is dead. Put the minimum on
       a gate question immediately AFTER the repeat. A cap (`count(…) <= 10`)
       is the opposite case and correctly stays inside. Verified at Step 2.8
       by `app-release-qa` over the released binds.
     - `repeat-count-source` — any repeat with a fixed row count (Nova
       `count_bound`). The count must be known when the form OPENS (case
       property, session, lookup, constant) — never a question in the same
       form: Nova snapshots a root count once on `xforms-ready`, so a
       same-form "how many?" answer is still blank and the repeat renders
       ZERO rows (ace#2517 — all 5 on `spark-facilitator/20260926-1413`).
       "Worker states N, then fills N rows" → `user_controlled` repeat with
       the number derived as `count(<repeat>)`. Verified at Step 2.8 by
       `app-release-qa` (`dead-repeat-count`, `lib/repeat-count-audit.ts`).
     - `case-choice-attendance` — a form opened on a group-like case that
       records which of its existing members took part (attendance, a
       distribution, a screening). ONE `multi_select` whose choices are the
       group's own open member cases (`optionsSource: {kind: 'cases'}`), plus
       an unlabelled `query_bound` roster that updates each member the FINAL
       checklist ticks. Not one yes/no screen per member, which was the
       pre-2026-10-08 fallback (`voidcraft-labs/commcare-nova#728`), and never
       an update repeat driven by the checklist answer. Exact shapes:
       `lib/case-choice-attendance.ts`. If `scripts/probe-nova-case-choices.ts`
       exits non-zero, brief the yes/no fallback and record why under
       `## Build notes`.
     - `screen-grouping` — always, for any form that puts more than one
       question in a `group`. A group is a CommCare field-list, so its children
       share ONE scrollable screen. Multiple questions per screen is GOOD
       design — this is **not** a one-question-per-screen rule — but group by a
       shared rule (one recall period, one answer source), split when that rule
       changes, never nest a `repeat` inside a group, and keep a long read-aloud
       passage on the screen carrying the answer it governs. Verified ACE-direct
       by Step 4g.
     - `consent-script-floor` — **always-on for capture of identifiable
       people, on exactly the same condition as `live-photo-capture`: any
       image / photo / audio / video capture question of people fires this
       component ON ITS OWN.** No consent field, no read-aloud passage, and
       no mention of consent anywhere in the PDD is required — a PDD that is
       *silent* about consent fires it just as hard as one that describes
       consent being sought. A photo question that needs `acquire` is
       categorically also a photo question that needs the floor; evaluate the
       two off the same detection and emit both. (It also fires on the other
       clauses in the component: a read-aloud announcement to an assembled
       group, a verbal consent taught in the Learn app, or a photo-consent
       line inside a behavior-change script.) **Do not reason "the PDD
       doesn't mention consent, so the trigger doesn't fire"** — that is
       exactly the miss that shipped 0-of-6 elements on an app photographing
       8+ identifiable people into an AI verification layer plus a human
       audit sample (`spark-facilitator/20260812-1635`, ace#1223; the prior
       run of the same opp shipped 4/6, so this has now missed twice).
       All six floor elements — and check `confidential`, where the
       data goes (name any AI verification layer and human audit sample), and
       that participation does not guarantee selection **by name**, because
       those three are the ones builds actually omit (ace#983, ace#1137).
       This is a build-time authoring rule; `pdd-to-deliver-app-eval §
       consent_floor` is the backstop, not the place to discover it. When this
       fires alongside `embedded-bc-script` on the same read-aloud passage,
       BOTH are emitted and this one governs the content.
     - `threshold-coherence-flag` — PDD fixes ≥2 numbers constraining one
       physical quantity. Check the pairs and record the check in the
       summary's `## Build notes`; a conflict the build had to resolve is
       also a decision row (§ Decisions Log) (ace#984). Carry `program_parameters.duplicate_gps_rule` into the
       brief WHOLE — radius, accuracy condition and fallback — and classify
       the dedup pair with `lib/gps-dedup-coherence.ts`: an
       accuracy-conditioned radius is coherent, and no `[FIXED]` or
       author-attributed threshold is ever moved to resolve a conflict
       (ace#2373).
     - `fixed-instrument-transcription` — the app digitises a `[FIXED]`
       published instrument whose source file the run's
       `inputs-manifest.yaml` names. Transcribe every constant exactly;
       verified ACE-direct by Step 4k (ace#1527).
     - `payability-scoped-key` — the PDD marks a SUBSET of submissions to a form
       **non-payable** (a did-not-happen branch, a screening-only visit, an
       ineligible-entity record, a committee meeting on a form that also records
       community meetings). Mandates the payability discriminator in `entity_id`
       **AND in `entity_name`**. Both halves matter and only one of them is
       stated twice: the skill's own "Payability-scoped keys" paragraph above
       covers `entity_id`, so a brief composed from that paragraph alone ships a
       correct key with an ambiguous DISPLAY name — payable and non-payable
       entities rendering byte-identically on the worker's completed-work and
       invoice views, one approved and one rejected with nothing to tell them
       apart. That is ace#1958, whose fix landed in the component and was then
       unreachable because this checklist did not name it, so the defect
       recurred on the next build of the same opp (ace#2279).
     - `entity-state-taxonomy` — **always for `archetype:
       longitudinal-visits`**, and for any archetype whose PDD declares a
       phase / stage / status vocabulary the worker sees. Carry the PDD's
       `program_parameters.entity_state_taxonomy` into the brief
       **verbatim** — every state value with its label and its member
       activity/step range — and where that row names a source document,
       read THAT document out of the run's frozen `inputs/` (resolved via
       `inputs-manifest.yaml`) rather than enumerating from the PDD's
       summary table. Parse the row with `parseStateTaxonomy` from
       `lib/entity-state-taxonomy.ts` BEFORE composing the brief:
       `declared: false`, or a non-empty `problems`, is a **HALT** with a
       Phase-1 finding, never a licence to invent a vocabulary. Verified
       ACE-direct by Step 4l (ace#1564). `stateless: true` (row
       `stateless [source: …]`) is a declaration, not a gap: brief NO state
       field (ace#2774).

     Do NOT inline-paraphrase these — reference the library so the build
     and `pdd-to-deliver-app-eval` stay symmetric. Skip a component whose
     trigger doesn't fire.

   - **Followed-entity id on every paid form (ace#2889).** When the PDD's
     `program_parameters.followed_entity_case_type` names a case type
     (`parseFollowedEntityCaseType` from `lib/followed-entity-id.ts`), every
     paid form — every form carrying a Connect `deliver_unit` — that serves
     that entity must record its id in a **hidden** field at the form root
     named `followedEntityIdField(caseType)` (= `<case_type>_case_id`, e.g.
     `participant_case_id`), whose value is DERIVED from the case model, never
     worker-entered or hard-coded. Put this in the brief as a `REQUIRED:`
     line naming the field and, per paid form, its source:
     - a form that runs ON the followed case → the session case id
       (`#case/@case_id`, i.e. `instance('commcaresession')/session/data/case_id`);
     - a child-case form (a crop cycle, session or pregnancy under the
       followed entity) → the child case's PARENT id, read from casedb
       (`instance('casedb')/casedb/case[@case_id = instance('commcaresession')/session/data/case_id]/index/parent`);
     - a form that CREATES the followed entity → the new case block's
       `@case_id`.
     A paid form that genuinely serves no followed entity is recorded in the
     summary's `## Build notes` under `followed_entity_id.exempt` with its
     reason (the PDD's Deliver spec must say so) — `app-release-qa § Step 4.9`
     reads that map and fails every other paid form that lacks the field. On
     `smallholder-seasonal/20261012-1549` the paid Harvest visit updated the
     crop cycle and named nothing that identified the woman, so no reporting
     layer could attach the visit to her. `followed_entity_case_type: none
     (<reason>)` or an absent row (non-longitudinal, non-multi-stage) → skip.

   - **App-test economy (always).** Insert this paragraph **verbatim** into
     the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Keep app-test output small — every app-test result stays in
     > your context for the rest of the build. Batch each journey into as
     > few `continue_app_test` calls as possible: up to 8 `actions` per
     > call, each with an `expect` (screen / form / submitted) so a journey
     > that behaves costs one call and a wrong turn stops at the first
     > miss. Do not re-observe a screen you have already seen; to re-read
     > evidence, use `read_app_test` with a small `limit` (and `inspect`
     > only the step you need), not a fresh journey. Test each distinct
     > journey once per saved revision, then re-test only the journeys a
     > later edit touched. Do not call `get_form` on a form you just
     > authored to confirm it — the `add_fields` and save results already
     > say what was saved; `get_form` is for a count that came back short.

     Why: Nova has no compact/delta result mode (`continue_app_test` and
     `get_form` take no size control — voidcraft-labs/nova-plugin#71), and
     each `continue_app_test` result measured 35–108 KB, ~30 per build. On
     `kaduna-graduation/20261015-1411` the Deliver architect's context reached
     ~944k and hit the 250-turn cap before reporting. Batching cuts the call
     count, which is the half ACE can control. When #71 ships a compact
     mode, add it to this paragraph (`skills/nova-capability-adoption`).

4. **Invoke `/nova:autobuild "<brief>"`.** Capture from the response:
   - `app_id` — durable Nova handle, written to the summary as
     `nova_app_id`. Since nova plugin v2 the architect builds in private
     work and SAVES checkpoints; the app id is the one its `save_work`
     returned. **If the report names a `work_id` with pending changes (the
     build stopped before a final save), the build is INCOMPLETE** — the
     saved app lacks that work, and upload/compile never see it. Treat it
     as an unfinished build (re-dispatch or `/nova:edit` to finish), never
     record it as delivered.
   - Build summary
   - Any warnings

   **Every ACE-direct Nova edit in Steps 4a–4l runs in PRIVATE WORK
   (`voidcraft-labs/commcare-nova#693`, 2026-09-27).** Contract and observed
   behaviour: `playbook/integrations/nova-integration.md § The private-work authoring contract`. The rules this
   skill depends on:

   - Open work **after** `/nova:autobuild` has returned — never while an
     architect dispatch is in flight (its saves would make ACE's candidate
     `stale`, and a stale candidate can only be discarded):
     `begin_work({request_id, app_id})` → keep the `work_id`.
   - Every mutation below (`add_case_list_columns`, `configure_connect`,
     `update_form`, `set_field_options_source`, `edit_field`, `remove_field`,
     `update_case_list_column`, `add_fields`, `update_translations`, …) takes
     `work_id` + a fresh `request_id` and **no `app_id`**. It answers
     `saved: false`: the saved app is unchanged until
     `save_work({work_id, request_id, expected_revision})`, with
     `expected_revision` = the `revision` from the latest mutation (or
     `get_work`).
   - **Require `saved: true` on the save answer.** A stale or refused save
     comes back as DATA (`saved: false`, `kind: "stale-base"` …), not as an
     error. On `stale`, `discard_work` and redo the edit from current saved
     state. Scripted edits use `lib/nova-work.ts` (`NovaWork.begin` →
     `stage` → `save`), whose `save()` throws unless Nova saved.
   - **Save before every read-back that proves an edit**, and read back with
     `app_id` (saved state). A `work_id` read shows the candidate even when
     the save failed. Wherever a step below says "re-fetch" / "re-run
     `get_app`" after an edit, the save comes first.
   - A save must leave a buildable app — never empty a form.
   - Before Step 5, `get_work` must read `pending_changes: 0`. An unsaved
     edit raises no error anywhere; it is simply absent from what
     `app-deploy` uploads.

4a. **Post-build field-count verification — runnable recipe (skill-side safety net).**

    The architect-brief language above puts retry-then-verify
    discipline on the architect agent. This step is the skill-side
    safety net for cases where the architect finished short — including
    the case where the architect ran out of budget mid-form and
    silently persisted N-of-M expected fields with no error. (FGD
    Deliver apps are the highest-risk surface: the per-section summary
    form for focus-group archetypes is ~45-70 fields with 7 section
    groups — exactly the kind of long form where partial persistence is
    most likely.)

    **Always run this recipe before writing the success summary.** Not
    a prose contract — a numbered tool-call sequence the L0 LLM
    executes verbatim:

    1. **Build the expected field-count table** from the brief that was
       sent to `/nova:autobuild`. For each `(module, form)` pair the
       brief named, extract the field list. Persist as an in-memory
       map `expected[module][form] -> [field_id, ...]`. The brief is
       the source of truth — not the PDD prose, not the architect's
       return string.

    **Read the built app ONCE, from the snapshot (ace#3132).** This skill runs
    BEFORE Phase 3's Step 1.4 lint, so there is usually no snapshot yet. Get
    one with a single server-side call (none of the blueprint enters your
    context), or reuse the caller's:

    ```bash
    ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
    TSX="node $ACE_ROOT/node_modules/tsx/dist/cli.mjs"
    # caller passed nova_snapshot: it must be FRESH (exit 0), else take your own
    $TSX "$ACE_ROOT/scripts/nova-app-snapshot.ts" --snapshot <nova_snapshot> --app <nova_app_id> --check
    # no snapshot, or not FRESH:
    $TSX "$ACE_ROOT/scripts/nova-app-lint.ts" --app <nova_app_id> --type deliver \
      --snapshot-out "<scratch>/nova-app-snapshot_<app>.json"
    ```

    Ignore the lint's verdict here (Phase 3 Step 1.4 owns the gate) and use
    only the file it wrote. `FRESH`, or the file you just wrote → take the
    uuid map from `nova-app-snapshot.ts --snapshot <file> --outline` (it also
    prints the app's `connect` type) and each form from `--form <formUuid>`;
    **do not call `get_app` or `get_form`** for steps 2–3 below, nor for
    4e step 1–2. Any other result (exit 3/4, no file written) → read live as
    written below, never "close enough". **After ANY edit of this app, take a
    new snapshot with the same lint command** before re-reading — the old
    file predates the edit. Reads that verify this skill's OWN write stay live
    (`LIVE_READS`, `lib/nova-app-snapshot.ts`): the `get_form` inside each
    `/nova:edit` prompt, and the post-save `get_app` re-fetch in 4e step 3 (it stays live: it proves the save landed and that `configure_connect` cleared no form).

    2. **Read the built app** via one `get_app({app_id})` call. Compare
       module + form names against the expected map. **Halt** if any
       expected `(module, form)` is missing — that's a structural gap
       the field-count recipe can't fix.

       **This same call is the addressing map.** Nova is uuid-addressed
       (2026-07-31 migration — see
       `playbook/integrations/nova-integration.md § The 2026-07-31
       uuid-addressing migration`); there are no `moduleIndex` /
       `formIndex` parameters on any tool. `get_app`'s blueprint prints
       `[uuid <rfc-uuid>]` on every module, form, and field:

       ```
       - Module "CBF Registration" [uuid b60055c1-…] (case_type: cbf)
         - Form "CBF Registration" [uuid c3deb000-…] (registration, 12 fields)
           - community_id [uuid c3df54f7-…] (text)
       ```

       Build `uuids[module][form] -> {moduleUuid, formUuid}` (and the
       per-field uuids) from this ONE response and carry it through the
       rest of the recipe — Steps 4b–4h all address off this map. One
       lookup beats N. If you only hold a semantic name later,
       `search_blueprint({query, app_id})` resolves it — but prefer the
       map you already have.

    3. **For every form in the expected map**, call
       `get_form({app_id, moduleUuid, formUuid})` using the uuids from
       step 2 (one call per form, batchable in parallel across forms).
       Collect:
       - `persisted_ids`: the set of `field.id` values present in the
         response. Hidden / label / group / repeat fields all count.
       - `persisted_count`: `len(persisted_ids)`.

    4. **Compute the diff per form.** `missing = expected[m][f] -
       persisted_ids`. **Also** compute `referenced_missing`: any field
       referenced in another field's `calculate` / `relevant` /
       Connect-marker `user_score` / `entity_id` that isn't in
       `persisted_ids`. (`validate_app` flags this class as
       "X references Y which doesn't exist in this form" — same
       shortfall, different detection path. Catching it here means we
       don't ship to `validate_app` with a known gap.)

    5. **If `missing ∪ referenced_missing` is empty across every form,
       proceed to step 4b (one-form-per-module check).** No edit needed.

    6. **If non-empty for any form**, dispatch ONE `/nova:edit` call
       per affected form. Prompt template:

       ```
       /nova:edit <app_id> "Add the following missing fields to form
       <module-name> / <form-name>: <comma-separated field ids and
       their kind/calculate spec from the brief>. After each add_fields
       call, get_form and verify persistence. Do not return until every
       requested field is present."
       ```

       Re-run step 3 + step 4 after the edit returns, from a NEW snapshot
       (same lint command, `--snapshot-out`) — the old one predates the edit.
       The `get_form` inside the `/nova:edit` prompt is the editor's own
       read-back of its write and stays live.

    7. **Bounded loop, max 3 iterations.** If any form is still short
       after the third iteration, halt with a structured failure
       listing `<form-name>: <missing ids>` per offender, and do NOT
       write the success summary. The operator decides whether to
       /nova:edit manually, re-dispatch autobuild, or escalate.

    > For why this runs even though `validate_app` catches some shortfalls downstream, see reference.md § Step 4a safety net.

    Same shape as `app-connect-coverage` — verify+fix in a bounded
    loop, post-Nova.

4b. **Structural pre-flight: one form per module (deliver_unit slug
    uniqueness).** After field counts match, verify the module/form
    layout is what Connect's sync will consume cleanly. Cheap check;
    fires before any HQ upload.

    1. Call `get_app({app_id})` and enumerate
       modules + forms.
    2. Count forms tagged with `connect.deliver_unit` (or `connect.task`)
       across the app. Call this `intended_paid_form_count`.
    3. Count modules whose form set contains ≥ 1 paid form. Call this
       `paid_module_count`.
    4. **Assert** `paid_module_count === intended_paid_form_count`.
       If not, every multi-paid-form module will collapse to one
       deliver_unit at Connect's sync (Nova reuses the module slug as
       `<learn:deliver id>` per form; Connect dedups by slug). The
       collapsed-but-non-first forms reach production silently unpaid.

    On mismatch, dispatch:

    ```
    /nova:edit <app_id> "Split module <X> so that each of its paid
    forms (<form-Y>, <form-Z>) lives in its own module. Connect dedups
    deliver_units by slug and Nova currently emits the module slug as
    the <learn:deliver id> for every form in that module, so multi-form
    modules collapse to one deliver_unit at sync. After the edit, every
    form with connect.deliver_unit set must be the only form in its
    module."
    ```

    Re-fetch and re-assert. **Bounded loop, max 3 iterations.** If
    still mismatched after 3, surface a clear failure listing each
    offending module + the forms that need separating, and do not
    write the success summary.

    See `feedback_connect_deliver_unit_per_module` memory for the
    upstream Nova bug that necessitates this.

4c. **Case write-back verification (follow-up forms must persist
    observations).** The structural preventer for case-update forms that
    capture observations but write zero case properties (losing what they
    observed). `pdd-to-deliver-app-eval § case_persistence` hard-gates
    this at ≤2; this step catches it at build time. Cheap; runs on the
    already-fetched blueprint. Same bounded-loop shape as 4a/4b.

    1. From `get_app({app_id})`, identify each **case-UPDATE** form (a
       form Nova tagged as updating an existing case type rather than
       creating one — it carries `case_property_on` writes against a case
       type some other form creates).
    2. For each case-update form, list its **user-facing observation
       fields** (non-hidden, non-label questions the FLW answers).
    3. **Assert** that the form binds **≥1** of those observation fields
       to a case property via `case_property_on`. A case-update form
       that captures new observations and writes zero case properties
       fails this assertion.
    4. On failure, dispatch:

       ```
       /nova:edit <app_id> "Form <module>/<form> is a case-update form
       that captures observations (<list>) but writes no case
       properties. Bind the observation fields that represent durable
       state (<list>) to case properties on case type <type> via
       case_property_on, so the follow-up visit persists what it
       observed. After the edit, get_form and verify each binding."
       ```

       Re-fetch and re-assert. **Bounded loop, max 3 iterations.** If
       still failing after 3, surface a clear failure naming the form +
       its unpersisted observations, and do not write the success
       summary. (Single-form atomic-visit apps with no case-update form
       have nothing to check — skip cleanly.)

4d. **Case-list column heal — runs ACE-DIRECT (deterministic preventer
    for the autonomous-architect allowlist gap).** A case-CREATE module
    whose `caseListConfig.columns` is empty (`case_list_config: null`)
    fails Nova's `validate_app` with a single error against that module.
    The autonomous architect dispatched in Step 4 (`/nova:autobuild` →
    `Agent(nova:nova-architect-autonomous)`) **cannot clear this error
    on its own**: the case-list-config tool family
    (`add_case_list_columns`, `set_case_list_filter`,
    `update_case_list_column`, `remove_case_list_column`,
    `reorder_case_list_columns`, `set_case_search_display`,
    `set_case_search_advanced`, `add_search_inputs`, …) is **not present
    in the autonomous architect's tool allowlist**. It will try
    `generate_schema`, a fresh `create_module`, and promoting
    `case_name` to a visible field — none of which auto-seeds the
    default column — and report it cannot reach validate-clean.

    These case-list-config atoms ARE available to the ACE session
    Code session that executes this skill, so the heal is a
    deterministic L0 operation: run it here, after the autonomous build
    returns, rather than asking the architect to do something its tools
    can't.
    > For why this step lives ACE-direct (not the architect brief) + the upstream allowlist gap (jjackson/ace#632), see reference.md § Step 4d ACE-direct heal.

    Cheap; runs on the already-fetched blueprint. Same bounded-loop
    shape as 4a/4b/4c.

    Note: Nova's `validate_app` is architect-side only — it is NOT
    exposed at the L0/user tool surface (nova@nova-marketplace 1.1.0;
    jjackson/ace#821), so this recipe inspects the blueprint directly
    instead of asking the validator.

    1. From the already-fetched `get_app({app_id})` blueprint, identify
       every **case-CREATE** module, and for each one call
       `get_module({app_id, moduleUuid})` — the `moduleUuid` comes from
       the Step 4a step-2 addressing map — to confirm its case type and
       whether its case list is empty (`case_list_config: null` /
       missing `caseListConfig.columns`). If every case-create module
       already carries a non-empty case list — or the app has no
       case-create modules — skip the rest of this step; there is
       nothing to heal.
    2. For each offending module, call
       `add_case_list_columns({work_id, request_id, moduleUuid, ...})` to add ONE
       plain column over the case name field (the module's `case_name` /
       case-name field). A single default column is sufficient to clear
       the architect-side validate error; this is the same one-column
       heal an operator applies by hand.
    3. `save_work` (require `saved: true`), then re-fetch via
       `get_module({app_id, moduleUuid})` and re-assert
       the case list is now non-empty. **Bounded loop, max 3
       iterations** over steps 1–3. If any case-create module still has
       an empty `caseListConfig.columns` after the third iteration,
       surface a clear failure naming each module still missing its
       case-list column, and do NOT write the success summary.

    (Apps with no case-CREATE module, or whose case-create modules
    already carry a non-empty case list, skip cleanly at step 1.)

    **CAUTION — this heal can author a case list nobody can reach
    (dimagi-internal/ace#977).** On a REGISTRATION-ONLY module the entry's
    only session datum is `function="uuid()"`, so no entity-selection screen
    is ever pushed and the column set added here is dead configuration —
    satisfying `validate_app` while producing a list no worker can ever see.
    `app-release-qa` Step 4 blocks that shape (`case-list-unreachable`) —
    but only when the case type is unreachable **app-wide** (ace#1281). If a
    sibling module opens the same case type behind a real entity datum, the
    inert detail on the registration module is `[INFO]`, not a blocker, because
    Nova **refuses** to remove the last visible Results column from a module
    that declares a case type ("Every case list needs at least one visible
    Results field… Nothing was changed") — the shape is unavoidable and must
    not be healed here.

    So when a case-CREATE module has no case list, ask FIRST whether the
    module is genuinely registration-only **and whether any other module opens
    that case type**. If nothing does, the right resolution is to add the
    followup form the PDD implies — **not** to add a column to clear the
    validator. This is Jon's blueprint invariant from 2026-07-28: a module that
    declares a case type + case list should have some form that actually opens
    a case.

4e. **Deliver-marker compile pre-check (catch a missing app-level Connect
    type before deploy) — runs ACE-DIRECT.** Mirror of
    `pdd-to-learn-app` § 4b. The autonomous architect
    (`Agent(nova:nova-architect-autonomous)`) can land a Deliver app with
    **no app-level Connect mode** even though every form already carries
    its `connect.deliver_unit` block. The per-form `[Connect enabled]`
    flag is a **FALSE POSITIVE for compile**: with no app-level mode the
    released CCZ ships with ZERO `<learn:deliver>` markers, Connect
    surfaces zero deliver units, and Phase 4 fails at payment-unit
    creation. `app-release-qa` (Phase 3 Step 2.8) catches it
    post-release, but that is a full deploy→build→release cycle too late
    — assert it here, cheaply, on the already-built app.

    1. Read the app's Connect type and complete form list from the § 4a
       snapshot (`--outline`: `connect` + `forms[]` with uuids); no
       `get_app`. Live fallback only when 4a left no `FRESH` snapshot: call
       `get_app({app_id})` — its summary header prints the Connect type
       (e.g. `Connect type: deliver`; a standard app prints none) — and
       **keep that response** for its form list and `[uuid …]` markers.
    2. **Assert the header reads `Connect type: deliver`.** Do NOT rely
       on the per-form `[Connect enabled]` flag — it is a false positive
       for compile (see above, and Step 3's marker-mechanism bullet).
    3. On a miss, heal ACE-direct with **`configure_connect`**, which is
       available to the ACE session that executes this skill.
       `update_app` no longer carries `connect_type` — it was removed in
       Nova's 2026-07-31 redeploy (dimagi-internal/ace#1133);
       `configure_connect` replaced it and sets the app-level mode AND
       every form's Connect block in one atomic call.

       > **⚠ `configure_connect` is REPLACE-ALL, not a patch.** Upstream:
       > *"learn/deliver requires the complete nonempty UUID-addressed
       > participant set, and every unlisted form becomes auxiliary."*
       > **Every form you omit from `participants[]` has its existing
       > Connect block CLEARED.** A partial participant list turns this
       > marker-repair into a marker-deletion — strictly worse than the
       > problem you came to fix. This is the OPPOSITE of
       > `update_form({connect})`, which is per-form and additive.

       So: **enumerate the COMPLETE participating set from the step-1
       `get_app` response first**, then call once:

       ```
       configure_connect({
         work_id, request_id,
         mode: "deliver",
         participants: [
           // EVERY paid form in the app, addressed by formUuid.
           { formUuid: "<paid form uuid>",
             connect: { deliver_unit: { name, entity_id, entity_name } } },
           …
         ]
       })
       ```

       Note the **expression shape** — since voidcraft-labs/commcare-nova#693
       `entity_id` / `entity_name` (like `relevant`, `calculate`,
       `default_value`) are expression STRINGS that name answers as
       `#form/<path>`; a bare id is refused as an unknown reference.
       Omit each block's `id` and let Nova derive it.

       Then `save_work` (require `saved: true`), re-run `get_app({app_id})`
       and re-assert BOTH the header and that every
       form that carried a Connect block before still carries one.
       **This re-fetch stays live** (`LIVE_READS`): it verifies this
       step's own write, which the § 4a snapshot predates.
       **Bounded loop, max 3 iterations.** The per-form
       `connect.deliver_unit` blocks the architect already built stay
       intact, so the marker compiles on the next deploy with **no
       rebuild and no fresh app id**. If the header still does not read
       `Connect type: deliver` after the third attempt (or
       `configure_connect` is itself unavailable), halt with a clear
       `deliver-marker-wont-compile` failure and do NOT write the success
       summary.

    Use `update_form({moduleUuid, formUuid, connect})` **only** to refine
    one sub-config on a form that ALREADY participates — it cannot enable
    Connect, switch mode, or add a participant, and it refuses a
    whole-slot null. Full division of labour:
    `playbook/integrations/nova-integration.md § configure_connect
    replaced update_app({connect_type})`.

    Reproducer: `malaria-rdt/20260603-1600` — the Deliver app landed with
    no app-level Connect mode; both the original and a fresh
    re-upload+re-release produced `connect_markers.deliver = 0` (that
    session predated the L0 heal and fell back to a rebuild, blocked by a
    concurrent Nova `create_app` outage — a tool since removed, #693). See jjackson/ace#694. The L0
    heal in step 3 above was confirmed live on
    `bednet-spot-check/20260616-0618` — one call flipped the header from
    absent to `Connect type: deliver` with the per-form blocks intact, no
    rebuild. See jjackson/ace#792. (That heal was
    `update_app({connect_type: "deliver"})` at the time; the parameter was
    removed 2026-07-31 and `configure_connect` is now the only path —
    dimagi-internal/ace#1133.)

4f. **Option-source pre-check (PDD-declared selects must not ship as free
    text).** The structural preventer for ace#1136. `structured-capture` puts
    the rule in the architect brief; this step is the ACE-direct safety net for
    when the architect had no option list in front of it and fell through to
    `kind: text` anyway — the exact failure mode of
    `spark-facilitator/20260731-0656`, where four of five PDD-declared
    select/lookup fields shipped as free text and only the one with an
    inline-enumerable option set survived. Cheap; runs on the already-fetched
    blueprint. Same bounded-loop shape as 4a–4e.

    1. **Build the declared-select list from the PDD** (not from the brief and
       not from the architect's return string). Every field in the Deliver App
       Specification whose spec text contains `select`, `lookup`,
       `choose from`, `pick from`, or `from the registered …` goes on the list,
       plus every field named as a component of a `connect.deliver_unit`
       `entity_id`.
    2. **Resolve each one in the built app.** Nova is uuid-addressed — one
       `search_blueprint({query: '<field id>', app_id})` per field returns
       `{moduleUuid, formUuid, fieldUuid}` and the field's context; or read
       them off the `get_form` responses already fetched in Step 4a.
    3. **Assert** each declared-select field's `kind` is `single_select` or
       `multi_select`. Collect the offenders as
       `degraded[] = {field_id, declared_as, shipped_kind, feeds_entity_id}`.
    4. **If `degraded` is empty, run the whole-app lookup sweep in step 8 and
       then proceed to Step 5.** An empty `degraded` list means no field needs
       CONVERTING; it does not mean no field needs CHECKING (ace#2143).
    5. **For each offender, try to bind a real option source before accepting
       the degradation.** Call `get_lookup_tables({app_id})` ONCE — it lists
       this app Project's data tables and their columns with the stable ids
       `set_field_options_source` needs — then, per offender:
       - **A table holds the option set** → convert the field and bind it:
         `set_field_options_source({work_id, request_id, moduleUuid, formUuid,
         fieldUuid, source: {kind: 'lookup', tableId, valueColumnId, labelColumnId}})`.
         The call is an atomic REPLACE of the field's complete choice source
         (there is no retained inactive source), so send the whole thing.
         Convert a `text` field to a select first via
         `edit_field({work_id, request_id, moduleUuid, formUuid, fieldUuid, updates:
         {kind: 'single_select', optionsSource: {...}}})` — a kind conversion
         that would set saved case values aside returns `needsConfirmation`;
         on a fresh build there is nothing to set aside, so re-call with
         `confirmConversion: true`. **Every bind made here is a site for the
         step-8 sweep** — do not verify it ad hoc.
       - **No table, but the set is knowable** from the PDD / inputs / a source
         `.ccz` → bind it inline:
         `source: {kind: 'inline', options: [{value, label}, …]}` — `label`
         is plain text since voidcraft-labs/commcare-nova#693 (≥2 options).
       - **Neither** → ship a select over the values you DO have plus an
         explicit "Other" with a relevance-gated `_other` free-text follow-up.

         **Neither rung is available when the PDD names a partner register for
         this field (ace#1621).** Both invent vocabulary — the inline rung by
         enumerating a set the architect composed, the Other rung by shipping a
         partial set as if it were the register — and "knowable from the PDD /
         inputs / a source `.ccz`" is precisely the case where the real values
         exist and must be read rather than composed. Go to the register
         procedure in step 7, which now **builds and binds** the register
         rather than handing it to an operator (ace#1886).
    6. **`save_work` (require `saved: true`), then re-run steps 2–3 against
       the SAVED app (`app_id` reads). Bounded loop, max 3 iterations.**
    7. **Whatever survives is a NAMED gap, never a silent one.** Any field
       still on `degraded` after the third iteration MUST appear as a decision
       row (§ Decisions Log) and in the Step 7 summary's `option_source_gaps`
       list, with the field id, what the PDD declared, what shipped, and the
       exact table + value column + label column that needs to exist before
       go-live.

       **Do not decide halt-vs-record by reading the paragraphs below — call
       `classifyOptionSourceGap` in `lib/option-register.ts`, once per
       still-degraded field, and do what it returns** (ace#2857). It takes
       facts, not conclusions: `{feeds_entity_id, payable,
       non_enumerable_by_nature, candidate_values, declares_partner_register}`,
       where `candidate_values` is every legitimate member of the option set
       you actually FOUND in the PDD / frozen `inputs/` / a source `.ccz`.
       `outcome: 'halt'` halts; `outcome: 'record'` records the row and
       proceeds, carrying `exemption` and `reason` verbatim into it. The prose
       below is the rationale for what that function does, not a second,
       hand-applied copy of it.

       **Every recorded gap is `review_ask: required-before` +
       `needed_by: go-live`** — the ask the function returns, and never
       `recommended-confirmation`. An option-source gap IS a go-live
       prerequisite by definition, and `recommended-confirmation` is
       explicitly the ask that gates nothing (`lib/decisions-schema.ts`:
       *"`required-before` is the only one that gates anything"*), so the old
       wording asked for the non-blocking ask in the same sentence as "since
       it is a go-live prerequisite". `required-before` is an enforced release
       blocker (`assessRequiredBeforeAsks`, `lib/release-readiness.ts`), so the
       gap now gates the gate it belongs to.

       **Halt** — do not write the success summary — if any still-degraded
       field `feeds_entity_id` **on a PAYABLE deliver unit**: a free-text
       component of Connect's dedup / payment grain is a payment-correctness
       defect, not a data-quality one (one typo mints a second payable
       delivery; two same-named entities collapse into one). Everything else
       records and proceeds.

       **A SECOND halt class: a PDD-named partner register (ace#1621).**
       The halt above is scoped to payment correctness, so it is silent on the
       other way a degraded select does damage — shipping ACE's invented words
       as the PARTNER's taxonomy. When the PDD sources a field's options from a
       named register (`<field> from <tag> [source: …] [filtered by …]` in
       § Program Parameters), **an inline invented option list is a HALT**,
       whatever the field's `feeds_entity_id` / payability status, and it is
       never dischargeable as a named gap.

       Do not eyeball it and do not re-derive it — run
       `lib/option-register.ts`: `parseRegisterDeclaration` over the PDD row,
       then `diffOptionRegister({declaration, built, registerRows})` over the
       option source read back from the blueprint. Any finding halts; the
       `unbound-register` code is the one that fires here. `declared: false`
       while the field exists is a **Phase-1 gap** (the PDD owes the register),
       reported against Phase 1, not as an architect defect — the build was
       supposed to HALT rather than fill it.

       Source the rows from the partner's own `.ccz` fixture XML via
       `parseFixtureRegister` in preference to a prose structure document: a
       production CCZ carries the register's REAL value codes, which are what
       the app stores and what the partner's M&E joins on, whereas a
       human-readable guide usually carries only labels and forces the build to
       mint an identifier scheme the partner has never seen (the #1527
       "trust extraction first" rule, one layer over).

       **ACE now finishes the job — extract, create, populate, bind, and
       PROVE the bind (ace#1886).** Both former blockers are gone.
       `create_lookup_table` takes the columns AND the rows in one atomic
       write, and binding a select to that table was accepted and read back
       live on 2026-09-06 (`voidcraft-labs/commcare-nova#545` closed COMPLETED
       2026-09-02). There is no operator handoff and no CSV. The terminal
       behaviour is:

       1. Extract the register (`parseFixtureRegister` over the partner's
          `.ccz` fixture XML, per the paragraph above).
       2. `create_lookup_table({work_id, request_id, name, tag, columns, rows})`
          — one call, up to 5000 rows, returns durable table and column uuids
          in input order. Use the tag the PDD declares. **This write is NOT
          staged**: Project data commits at call time, is visible before any
          save, and is not undone by `discard_work` (the tag stays taken). Only
          the bind in step 3 is staged.
       3. Bind the field. On a field that is already a select,
          `set_field_options_source({work_id, request_id, moduleUuid, formUuid,
          fieldUuid, source: {kind:'lookup', tableId, valueColumnId, labelColumnId}})`.
          On a field that shipped as `text`, `edit_field` with
          `updates: {kind:'single_select', optionsSource: {...}}` converts and
          binds in one call. **`set_field_options_source` refuses a `text`
          field outright** (*"is not a single- or multiple-choice field"*), so
          convert first — observed live 2026-09-06.

          Then **`save_work` and require `saved: true`.** Until the save lands
          the bind exists only in the candidate: `upload_app_to_hq` would ship
          the unbound field with no error.
       4. **Verify by READ-BACK of the SAVED app, never by the write's
          response.** Call `get_field({app_id, moduleUuid, formUuid, fieldUuid})`
          for the field (with `app_id`, after step 3's save — a `work_id` read
          would show the candidate's bind even if the save was refused) AND
          `get_lookup_table_rows({app_id, tableId})` for the table, and pass
          BOTH to `verifyLookupBind` in `lib/option-register.ts`
          (`{requested, readBack: field.optionsSource, rows}`). This is not
          ceremony: `add_fields` answers a *correctly bound* lookup field with
          `"options": []` and no mention of the source, so its response can
          neither confirm nor deny a bind. A `verified: false` of any code is a
          HALT.

          **`rows` is REQUIRED, and page to the end (ace#2143).** A bind that
          lands on a table whose VALUE column repeats a code is refused by
          Nova's `upload_app_to_hq` preflight one skill later, in `app-deploy`
          — *"A lookup-powered choice list uses activity_id for its saved
          values, but malawi_activities repeats the same value in several rows.
          Make the values unique or choose another value column."* Uniqueness
          **within a filter partition is not enough**: on
          `spark-facilitator/20260906-2233` `malawi_activities` carried `other`
          on seven rows, one per FCAP step, which no worker ever sees twice at
          once, and Nova still refused the whole app. `get_lookup_table_rows`
          pages at 100 rows, so concatenate the pages and pass
          `complete: true`; a partial read is `verified: false`, because a
          duplicate on an unread page is invisible.

          **The value column must also be whitespace-free (ace#2984).** Nova's
          preflight has a second rule: *"…contain spaces or line breaks there.
          Saved values can't contain whitespace. Tidy those rows or choose
          another value column."* So a table ACE (or the architect) authors
          needs a **slug-shaped value column** — e.g. `code` with
          `svc_entry_1` — distinct from the display `name` it uses as the
          label; never bind the display name as the saved value. On
          `kaduna-graduation/20261015-1411` `kgrad_services` had only
          `area, service_type, name, location, contact`, three selects saved
          `name` (`"Placeholder: services directory entry 1 …"`), and the whole
          Deliver app was refused at upload. `verifyLookupBind` returns
          `whitespace-values` for this; the repair is to add the code column
          and rebind `valueColumnId` to it, not to strip the labels.

          **Repairing a duplicate is not just renaming the rows.** A shared
          `other` row usually exists once per partition *because* the select is
          filtered — one shared row would be excluded from every partition —
          and the follow-up field's `relevant` / `required` are written against
          the literal value (`activity = 'other'`). Renaming to `s1_other` …
          `s7_other` requires that predicate to change too (e.g.
          `ends-with(activity, 'other')`). Decide which of the two shapes you
          want before editing rows.
       5. Record the table id, the column ids, and the `verifyLookupBind`
          verdict in Step 7's summary (`option_register` frontmatter and
          `## Build notes`). That verdict is
          the run's evidence the register is live; without it the build is
          asserting a bind it never observed.

       **The halt is now scoped to the cases ACE genuinely cannot finish**, not
       to the binding. It fires when:

       - the PDD declares **no** register for a field whose options must come
         from one (`declared: false`) — a Phase-1 gap, reported against
         Phase 1; the build must never fill it;
       - the declared source cannot be read from the run's frozen `inputs/`
         (`source-unavailable`) — unverifiable is not the same as correct;
       - `diffOptionRegister` / `diffRegisterRows` return any finding; or
       - **`verifyLookupBind` does not verify.** Treat this as the regression
         it is: run `scripts/probe-nova-fixtures.ts` (via `$ACE_ROOT`), which
         exits 0 when the bind still works and 2 if it has regressed
         upstream — then `skills/upstream-regression-triage`. Contract and
         tripwire table in `playbook/integrations/nova-integration.md § The
         fixtures (Project data table) channel`.

       In every one of those cases, halt rather than degrade. A select
       carrying invented values is strictly worse than a halt because it has no
       downstream symptom — the app is complete and internally consistent with
       its own invention, and every structural gate passes it (ace#1564's
       rationale, same class). **An unverified bind is the same defect wearing
       a better disguise:** the select renders empty to a field worker while
       every ACE artifact says the register shipped.

       Why this is not covered by the payment halt: on
       `spark-facilitator/20260820-0817` the meeting-activity repeat shipped 11
       ACE-authored placeholders (`attendance_register`,
       `facilitated_discussion`, `savings_collection`, …) identical on all 24
       FCAP steps, while Spark's own 78-activity register sat in the run's
       frozen `inputs/`. The field does not feed `entity_id`, so 4f recorded a
       gap and proceeded exactly as written — and it took an operator reading
       the residual, days later, to stop the release.

    8. **Sweep EVERY lookup-backed select in the app — not just the ones this
       step bound (ace#2143).** This runs unconditionally, including when
       `degraded` was empty at step 4 and when no partner register is declared
       at all.

       Steps 1–7 only ever reach a field that FAILED an assertion: a
       PDD-declared select that shipped as free text, or a register field the
       PDD named. A field the architect already shipped as a correctly-shaped
       `single_select` bound to a table it authored itself passes step 3 and is
       never looked at again — and that is the field that broke
       `spark-facilitator/20260906-2233`. `malawi_activities` was created,
       populated and bound by the architect, recorded as clean by every ACE
       gate, and refused by Nova's `upload_app_to_hq` preflight in `app-deploy`
       because its value column repeated `other` on seven rows. Nova's preflight
       sweeps every lookup-powered choice list in the app, so the only ACE-side
       check that cannot be bypassed is one with the same scope.

       **One call does all of sub-steps 1–3:** `scripts/nova-app-lint.ts --app
       <nova_app_id> --type deliver` (invocation in `agents/commcare-setup.md §
       Step 1.4`) reads every bound table once, server-side, and runs
       `auditLookupBinds` over every lookup-backed select — plus the two value
       rules added since: **whitespace in the saved value** (`whitespace-values`,
       ace#2984 — Nova's preflight refuses "Saved values can't contain
       whitespace"; give an authored table a slug-shaped code column distinct
       from its display `name` and bind the value to that) and **blank values /
       labels and wiped rows** (`blank-values`, `blank-labels`,
       `lookup-wiped-rows` — ace#2978: `edit_lookup_rows` `update` REPLACES the
       row, so always send every cell). HALT on any `lookup-binds` blocker it
       prints. The manual sub-steps below are what it does, kept for when the
       script cannot run.

       1. Collect every field in the built app whose options source reads back
          `kind: 'lookup'`, whoever created it — walk the `get_form` responses
          already fetched in Step 4a and read each one's `optionsSource`. For
          any form Steps 4b–4f EDITED, re-read `get_form({app_id, …})` after
          its save; the Step 4a response predates those binds.
       2. For each distinct `tableId` in that set, read the rows:
          `get_lookup_table_rows({app_id, tableId})`, paging to the end (100
          rows/page) and passing the concatenated rows with `complete: true`.
          One read per table, not per field.
       3. Call `auditLookupBinds` in `lib/option-register.ts` with one
          `{field, requested, readBack, rows}` site per bound field. **HALT on
          `ok: false`**, quoting `describeLookupBindAudit(audit)`.

       The failures it names are all invisible to every other gate ACE runs:
       `duplicate-values` and `whitespace-values` (the upload preflight
       refuses the app),
       `empty-table` and `not-a-lookup-source` (the select renders EMPTY on the
       device), `no-rows-read-back` / `partial-rows-read-back` (the check did
       not actually run — not a pass). Fixing one here costs a row edit; the
       same fix after `app-deploy` costs the whole of Phase 3 again.

       **Three exemptions (ace#1295, ace#2857) — all returned by
       `classifyOptionSourceGap`, none applied by hand.** Each comes from the
       halt's own rationale: it is payment correctness, so it does not reach a
       case where payment cannot be affected, and the escape ladder in step 5
       has no rung that fits a set nobody can enumerate:

       - **The deliver unit is UNPAID.** A form the PDD declares not payable
         carries no payment unit (`app-connect-coverage § Step 2` decides
         payability by role — ace#1327), so neither failure mode exists.
         Record the gap in `option_source_gaps` and proceed.
       - **The component is non-enumerable BY NATURE** — a personal name, a
         free-text identifier, anything captured at the moment the entity
         first enters the system. On a registration form there is no roster to
         select from: no lookup table can exist, inline enumeration is
         impossible for an open-ended name, and "the values you DO have plus
         Other" is nonsense for a name field. `concat(username,
         hh_head_name, visit_date)` is the STANDARD registration-key shape,
         not a degradation.
       - **No candidate value exists anywhere (`no-candidate-values`,
         ace#2857).** Not one legitimate member of the set appears in the PDD,
         the frozen `inputs/`, or a source `.ccz`. Then every rung of the
         step-5 ladder is empty *by construction* — no table holds a set that
         does not exist, there is nothing to enumerate inline, and "the values
         you DO have plus Other" is just Other — and **any value shipped would
         be invented**, which is `CLAUDE.md § No inferred backstory` on the
         partner's own vocabulary.

         More to the point, **halting accomplishes nothing here**: re-running
         Phase 3 cannot produce the set, because it is the partner's to supply
         before go-live. So the protection moves to the gate the risk actually
         belongs to. Nothing is paid during Phases 3–8; the typo and the
         collapse both happen when real workers submit real deliveries. A
         `required-before` / `go-live` row is an enforced release blocker, so
         the set must arrive before anyone can be paid either way.

         **This is deliberately NOT the exemption ace#2857 proposed.** That one
         keyed on the PDD declaring free text as an "advisory mechanism" — but
         the PDD is AI-authored, so that lets Phase 1's own prose disarm
         Phase 3's payment gate, and the qualifying phrase was one run's house
         style. This one keys on a fact about the world, and the caller records
         the search it ran.

         Live false-halt: `turmeric-market-study-ghana/20261012-1749`, Deliver
         app `d3a23546`, `market` — a PDD-declared select, a component of the
         payable `turmeric_survey` entity key, with **no market named anywhere
         in any input** because the implementing organisation chooses them
         after the build (operator ruling `market-list-source-confirmed`).
         Phase 2's journeys passed on either shape. The build was correct and
         the phase halted; the agent overrode the halt and recorded the
         override, which is the right outcome by the wrong mechanism.

       Every exemption is **stated in the decision row with the reason**
       (§ Decisions Log) — pass `verdict.exemption` and `verdict.reason`
       through verbatim — and never taken silently. When the unit is payable
       and candidate values DO exist, a degraded component still halts. Second
       live false-halt: `bednet-check-2-visit/20260813-2313`, Deliver app
       `74a097c6`, where the first two exemptions applied at once.

    (Apps whose PDD declares no select/lookup fields skip cleanly at step 1.)

4g. **Screen-shape check (a group is a field-list — catch the wall BEFORE
    deploy).** The structural preventer for the `screen-grouping` component.
    A Nova `kind: group` compiles to a CommCare **field-list**, so every child
    renders on ONE scrollable screen. Grouping questions that belong together
    is correct and expected; the defect is a group that has become a wall, and
    until this step existed nothing in Phase 3 looked at screen composition at
    all. Cheap; runs on the already-fetched blueprint. Same bounded-loop shape
    as 4a–4f.

    **Position rationale — this MUST run before `app-deploy`.** On
    hh-poverty-targeting/20260812-2034 the shape (all ten PPI indicators plus
    the roster repeat on one screen) was not noticed until `app-test-cases`
    tried to author the smoke recipe against it — two steps later, with the app
    already uploaded. Fixing it there cost a re-upload, a fresh HQ app id and an
    orphan app to soft-delete. Had Phase 4 already run it would have cost a
    delete-and-recreate of the Connect opportunity
    (`connect_create_opportunity` writes HQ app ids at create time and
    Connect's edit form does not expose them). Here the same fix is free.

    1. From the `get_app` / `get_form` responses already fetched in Step 4a,
       build the form's field tree with each field's `id`, `kind`, flattened
       `label` text, and `children` for groups/repeats.
    2. Feed it to the pure helper — do NOT eyeball the counts:

       ```ts
       import { checkScreenShape, formatScreenShapeReport }
         from '../../lib/screen-shape';
       const report = checkScreenShape(fields);
       ```

    3. Branch on the findings:
       - `severity: 'violation'` on `oversized-screen` → **split that group**
         into sets that share a rule, via `add_fields` (new group containers)
         + `move_field`. **Create each new container carrying the SAME
         `relevant` the original group had, BEFORE moving any field into it** —
         a field moved out of a gated group to an ungated one silently loses
         its gating, which is a correctness defect far worse than the scroll
         length you came to fix.
       - `severity: 'violation'` on `repeat-in-field-list` → `move_field` the
         repeat to the form root, or into a group of its own.
       - `severity: 'warn'` → keep the grouping only if the questions are one
         coherent set, and say so in the summary's `## Build notes`;
         otherwise split.
    4. Re-fetch and re-run. **Bounded loop, max 3 iterations.** If a violation
       remains after the third, surface a clear failure naming each offending
       group and do NOT write the success summary.
    5. Record the final `formatScreenShapeReport(...)` line in the summary's
       `## Build notes`,
       plus one sentence per surviving `warn` justifying the grouping.

    (Forms with no multi-question group skip cleanly — `screensChecked: 0`.)

4h. **Taught-vs-collectable cross-check (dimagi-internal/ace#1259).** Runs
    ONLY when the Learn app for this run already exists (it is built first in
    Phase 3; if you are building Deliver standalone, skip and say so).

    Nothing in ACE cross-reads the two blueprints: `pdd-to-learn-app` and this
    skill each build from the PDD independently, and each `-eval` grades its
    own app against the PDD in isolation. So a curriculum can instruct a worker
    to perform a step this form cannot record, and every Phase 3 gate passes.
    Live on hh-poverty-targeting/20260813-1612: Learn M8's padlocked-dwelling
    worked example says "you still do all of this… take one photograph… record
    the outcome as vacant", while the only `dwelling_photo` sits in a group
    gated `relevant: consent = 'yes'` — never reached on a vacant visit. At
    their first padlocked dwelling the worker follows the training, takes the
    photo, and finds no screen to attach it to. A human found it by reading the
    two blueprints side by side.

    ```ts
    import { checkTaughtStepsCollectable, formatTaughtVsCollectableReport }
      from '../../lib/taught-vs-collectable';
    const report = checkTaughtStepsCollectable(learnBlueprint, deliverBlueprint);
    ```

    **Do NOT auto-fix.** Which artifact is wrong is a judgement — the Learn app
    may over-teach or this form may under-collect, and BOTH can be
    PDD-conformant at once (they were on that run: §5.1 listed the live
    photograph under "a payable visit requires all of", §5.2 gated the photo
    screen on Consent = yes). Surface each finding as a decision row (§ Decisions
    Log) with both sides quoted in `reasoning` and `review_ask:
    recommended-confirmation` + `confirm_reason`, and raise it at the Phase 3
    pause so a human decides which side moves. `report.status === 'unable'`
    means the check **did not run** — the curriculum states no unconditional
    evidence step, so there was nothing to cross-check. That is NOT "the two
    apps agree": record it in the summary's `## Build notes` with its `reason` (`formatTaughtVsCollectableReport` renders it), and
    if the curriculum visibly DOES teach one, the phrase matchers are the bug.

4i. **Fake-preload check (a hidden `caseWrite` field can never hold the case
    value) — runs ACE-DIRECT.** The structural preventer for ace#1224. Because
    a followup form cannot read its own case on this Nova instance (§ `entity_id`
    case-UPDATE rule), architects reach for a shape that *looks* like a preload
    and is not: a hidden field with `caseWrite` set whose value comes from a
    literal `default_value`. It holds the literal forever, and then writes that
    literal **to the case** — so it simultaneously collapses whatever it feeds
    and wipes the case property it names. Nothing fails at build, validate, or
    submit time; every symptom is post-hoc and silent. Cheap; runs on the
    already-fetched blueprint. Same bounded-loop shape as 4a–4g.

    1. From the `get_app` / `get_form` responses already fetched in Step 4a,
       enumerate every field where **all three** hold:
       - `kind == "hidden"`, AND
       - `caseWrite` is set (any case type / property), AND
       - its value comes from a literal `default_value` — i.e. there is no
         `calculate` referencing a real answered field on this form. A
         `default_value` of `''` (or any constant) with no such `calculate`
         is the defect shape.

       Collect them as
       `fake_preloads[] = {field_id, case_type, property, feeds_entity_id,
       guards_relevant[]}`.

    2. **HALT if any of them feeds a `connect.deliver_unit` `entity_id` or
       `entity_name`** — directly as a part, or transitively via a field
       whose `calculate` references it. That is a **payment-correctness**
       defect, not a data-quality one: the key evaluates to the same constant
       for every entity, so Connect folds every delivery a worker makes onto
       ONE CompletedWork row — the per-entity record, per-entity review and
       any per-entity cap are gone while every submission succeeds (and each
       repeat is still paid, ace#2512). Do not write the success summary; surface the
       field, the marker it feeds, and the case property it would wipe.

    3. **Also inspect every hidden field referenced by a `relevant`
       expression**, whether or not it feeds a marker. This is how the
       dead-advisory mode surfaces and it is invisible to an entity_id-only
       scan: an advisory gated on `x != ''` where `x` is always `''` can never
       fire, so the guardrail the PDD promised is inert while reading as
       present in the blueprint, the Work Order and the training materials.
       Treat a `relevant` guarding on a fake preload as a violation and fix it
       in the same pass.

    4. **Repair — add a new visible field, never convert in place.** `hidden`
       is a **TERMINAL kind in Nova**: `edit_field` categorically refuses
       hidden→visible, and `confirmConversion: true` does NOT unlock it (that
       flag only covers kind conversions that set saved case values aside).
       So the repair is: add a NEW visible field that captures the value the
       form actually needs (a select over the same option source the create
       form used, per Step 4f), repoint the `entity_id` / `entity_name` parts
       and any `relevant` at the new field, and **neutralise** the old one —
       drop its `caseWrite` so it stops overwriting the case property, or
       `remove_field` it outright if nothing else references it.

       ```
       /nova:edit <app_id> "Field <id> in <module>/<form> is hidden with a
       caseWrite to <case_type>/<property> and a literal default_value, so it
       can never hold the case value and overwrites that property with the
       literal. Add a new VISIBLE field capturing <value> (select over
       <option source>), repoint <entity_id|entity_name|relevant> at it, and
       remove the caseWrite from <id>. Do not attempt to convert <id> to
       visible — hidden is terminal. After the edit, get_form and verify."
       ```

    5. Re-fetch and re-assert. **Bounded loop, max 3 iterations.** Anything
       still on `fake_preloads` after the third iteration goes in a decision
       row (§ Decisions Log) and the Step 7 summary's `## Build notes` by field id, case property, and what it
       feeds — and if it feeds a marker, the step halts per step 2 rather
       than recording.

    (Apps with no hidden `caseWrite` fields skip cleanly at step 1.)

4j. **Payability-discriminator backstop (ace#1489) — runs ACE-DIRECT.** The
    `entity_id` payability rule lives in Step 3's Nova brief, which is
    *architect prose*: nothing downstream of the build re-checks that the key
    the architect actually shipped honours it. So an identity-only key on a
    form with a non-payable branch escapes Phase 3 silently and is caught a
    whole Nova build later by `app-release-qa` Step 2.8, which raises
    `no-entity-component` as a `[BLOCKER]` and hard-halts the phase. The
    resolution helper already exists and the EVAL side already runs it
    (`pdd-to-deliver-app-eval § Connectify wiring (b2)`); this step closes the
    build/eval asymmetry, exactly as 4g pairs with the eval's `checkScreenShape`.

    1. Read the PDD's Program Parameters `entity_id_grain` and whether the PDD
       marks any subset of submissions to this form non-payable (a did-not-happen
       branch, a screening-only visit, a committee-vs-community meeting type).

    2. Feed it to the pure helper — do NOT adjudicate this by reading the key:

       ```ts
       import { resolveEntityIdGrain } from '../../lib/entity-id-precedence';
       const grain = resolveEntityIdGrain({
         pinnedComponents,          // from the PDD's entity_id_grain
         payabilityDiscriminator,   // the built form field expressing payability, if any
         hasNonPayableBranch,
         sourcePinned,
       });
       ```

    3. Branch on the resolution:
       - `deviates: true` → the built key MUST ship `grain.components` in order,
         and a decision row (§ Decisions Log) MUST disclose it using
         `grain.discloseAs`. Edit the
         `entity_id` calculate via Nova if it does not match, then re-fetch.
       - `unresolvable: true` → a non-payable branch exists but **no field
         expresses payability**. Do NOT ship silently: record `grain.reason` verbatim
         in a decision row (§ Decisions Log, with `review_ask:
         recommended-confirmation` + `confirm_reason`) and name the field that
         would fix it. This is
         the case the helper exists to stop from passing quietly.
       - otherwise → the PDD-pinned grain stands; record the one-line reason.

    4. **Whenever the shipped key is payability-scoped, the residual list MUST
       name the Phase-4 verification predicate that rejects the non-payable
       value** (ace#1434). The scoped key stops a non-payable submission
       consuming the payable slot, but it also mints `<identity> - no` as its
       own countable entity — so without that predicate the daily cap decides,
       and a worker whose first follow-up was a refusal can still be blocked.
       A key shipped without the residual is the ace#969 failure one layer down.

    5. Re-fetch and re-assert. **Bounded loop, max 3 iterations.** If the key
       still disagrees with `grain.components` after the third, surface a clear
       failure naming the built key and the required one, and do NOT write the
       success summary — halting here costs one loop; letting it through costs
       a Nova build plus a Phase-3 halt.

    6. **Capped-index arithmetic — when the cap rides in the key (ace#2148).**
       A per-entity cap ("at most N paid meetings per FCAP step") puts a
       clamped counter in the key, fresh per payable encounter up to the cap and
       constant after it. **The key does not stop the over-cap payment** — with
       the `duplicate` flag off (always, on ACE opportunities) Connect resets a
       repeat key to `pending`, auto-approves it and pays it again (ace#2512;
       `playbook/integrations/connect-api.md § A repeated entity_id is PAID
       AGAIN`). So the form MUST ALSO compute a `payable_slot` field (`yes` only
       for an in-cap payable encounter) for Phase 4's `form_field_rules` row to
       gate on, and the build summary names it. If the PDD names no such field,
       build it anyway from the same counter the clamp reads (it is derivable:
       `yes` iff the encounter is payable AND the pre-submission count is below
       the cap) and list it as a Phase 4 residual — never ship a cap that rides
       only in the key. Keep non-payable record kinds on a form with no
       `deliver_unit` marker (they would otherwise consume `max_daily` /
       `max_total`). The clamp constant is still NOT the cap. **A `casedb` read is the
       state BEFORE this submission** — the case property is written on submit —
       so `min(<casedb count>, N)` admits `N + 1` distinct keys and the
       (N+1)-th mints an index that has never existed, which Connect pays. On
       `spark-facilitator/20260906-2233` that turned a cap of 3 into a cap of 4:
       28 payable events against a declared `total_cap_per_flw` of 21, with
       every build-time gate green and `is_payable` correctly 0 on the fourth
       meeting (Connect never reads it).

       Two correct spellings, sharing no constant — both have shipped from this
       path, five weeks apart:

       ```
       if(<casedb count> >= <cap>, <cap - 1>, <casedb count>)   # indices 0..cap-1
       min(<casedb count> + 1, <cap>)                            # indices 1..cap
       ```

       So do NOT adjudicate it by comparing the clamp to the cap. Read the
       built `capped_index` back with `get_field`, and either trace the first
       `cap + 1` payable submissions by hand — confirming the last lands on an
       index an earlier one already used — or run the same trace mechanically:

       ```ts
       import { checkBuiltClampCapacity } from '../../lib/payable-cap-arithmetic';
       // binds: every node the counter reads -> its calculate, from get_field
       // read-backs (Nova `#form/…` and case-type `#<case_type>/…` spellings accepted as-is).
       const r = checkBuiltClampCapacity(builtCalculate, binds, declaredCap);
       r.status === 'checked' && r.ok;  // must hold
       ```

       The helper resolves the counter's timing from the expression
       (`classifyCounterTiming`) — never assume one. `min(<casedb count> + 1,
       cap)` is `includes-current` and admits exactly `cap`; simulating it as
       pre-increment reads `cap + 1` and HALTs a correct build (ace#2515). A
       `status: 'unable'` (timing undecidable — usually a counter node missing
       from `binds`) is a halt too, not a default: supply the missing calculate
       or trace by hand.

       A mismatch is a **HALT**, repaired inside the same bounded loop as step 5.
       `app-release-qa § Step 4` runs `checkPayableCapArithmetic` over the
       RELEASED form as the backstop; reaching it means a Nova build and a
       Phase-3 halt were spent on arithmetic decidable here.

    (Forms with no non-payable branch skip cleanly — `deviates:false`, and the
    pinned grain stands.)

4k. **Fixed-instrument constant fidelity (ace#1527) — runs ACE-DIRECT.** When
    the PDD marks an instrument `[FIXED]`, its questions AND its arithmetic are
    fixed by a published document that ACE only *digitises*. Every other gate on
    this path is structurally blind to a constant's VALUE: `validate_app`
    checks expression structure and references, `pdd-to-deliver-app-eval` grades
    the build against the PDD — which describes the instrument narratively, so a
    wrong constant is PDD-conformant prose — and `app-release-qa` checks form
    counts, Connect markers and install-time behaviour. Step 3 hands the
    architect the point values as PROSE, so the architect transcribes from a
    model-authored brief, and **the brief is the thing under test**. On
    `hh-poverty-targeting/20260819-1435` that shipped 9 of 17 point values wrong
    and all 101 poverty-likelihood values invented. A wrong scorecard produces a
    complete, plausible, fully-verified dataset that ranks the wrong households,
    and no downstream check has a symptom to catch. (The PPI licence permits
    digitising a scorecard and its lookup tables only UNMODIFIED, so this is a
    compliance question as well as a quality one.)

    1. **Trigger — two conditions, two DIFFERENT outcomes (ace#1648).** The
       trigger used to AND "the PDD marks an instrument `[FIXED]`" with "the
       manifest carries a source file for it" into ONE silent skip, so
       *nothing to check* and *the thing I must check is unreachable* were
       indistinguishable and both reported green. **A skip that disables a
       correctness check is worse than one that degrades an output, because
       the run still says green.** Split them:

       - **No instrument is `[FIXED]`** → **skip cleanly** and say so in the
         summary's `## Build notes` (`instrument_constants: skipped —
         <reason>`). Legitimate.
       - **A `[FIXED]` instrument whose source resolves** (step 2) → run the
         check.
       - **A `[FIXED]` instrument whose source does NOT resolve** → **HALT.**
         Never a skip. Print the resolution detail, record a `[BLOCKER]`-grade
         residual naming the file that would close it (a Phase-1 gap), and do
         NOT write the success summary. Shipping a digitised scorecard that
         nothing ever compared against its published source — while reporting
         a clean phase — is exactly the ace#1527 failure this step exists to
         prevent.

       In every branch: do not substitute the PDD's prose restatement of the
       table or the Nova brief for the file, and **do not compose a path by
       name**.

    2. **Resolve from the MANIFEST — `inputs[]` and the folder ids the
       manifest itself records, ONE LEVEL (ace#1648) — publisher's file
       first (ace#2852) — then fetch the bytes.**
       Read `inputs-manifest.yaml` and match the entry for the instrument the
       PDD names. If no `inputs[]` entry matches, **or the match is a derived
       extraction** (`classifyInstrumentArtifact(entry) === 'derived'` — e.g.
       a `text/markdown` "extracted verbatim" file), walk the manifest's own
       recorded folder ids — each `subfolders_not_listed[].folder_id`, plus
       `source_folder_id` when present — with
       `drive_list_folder({folderId})`, **one level deep, never recursively**,
       and match there. The manifest's `inputs[]` is direct child FILES only
       (orchestrator Step 5c) — that is deliberate, since `inputs[]` is the
       frozen evidence set Phase 1 synthesizes from — so a vendor bundle
       published as a SUBFOLDER of `inputs/`, the natural shape for a vendor
       download, is never in `inputs[]`, and 4k took the skip branch every
       time it was.
       Walking an id the manifest ITSELF recorded is not guessing; composing a
       path from a name still is, and is still forbidden. Exactly one match →
       proceed; more than one → HALT rather than pick; zero → HALT per step 1.
       Pass BOTH the derived `inputs[]` entry and the walk's matches to the
       helper: it resolves the single publisher-class subfolder file over the
       extraction and names the passed-over entry in its memo; it keeps the
       extraction (with its ace#2110 caveat) only when the subfolders hold no
       published file. Before ace#2852 the `inputs[]` match ended the search,
       so on `smallholder-seasonal/20261012-1549` the strict path resolved the
       extracted `.md` while the publisher's `.xlsx` sat one level down in a
       manifest-recorded subfolder.

       Classify the outcome with the helper rather than by eye — it owns the
       skip-vs-halt split, so the branch cannot silently revert:

       ```ts
       import { resolveInstrumentSource } from '../../lib/instrument-constants';
       const resolution = resolveInstrumentSource({
         fixedInstrument,              // does the PDD mark an instrument [FIXED]?
         manifestEntry,                // matching inputs[] entry, or null
         subfolderCandidates,          // matches from the one-level walk
         manifestRecordsSubfolders,    // did the manifest record any folder ids?
         instrumentName,
       });
       // 'skipped' -> write resolution.memo into ## Build notes and move on
       // 'halt'    -> print resolution.detail and STOP (no success summary)
       // 'proceed' -> resolution.source.file_id is the source
       ```

       **`resolution.artifactClass` says WHAT you resolved, and it is not
       decoration (ace#2110).** This step's premise is that the artifact it
       diffs against is UPSTREAM of ACE — that is the whole force of "read the
       SOURCE, never the Nova brief and never the PDD's restatement". A third
       model-authored intermediate defeats it silently: an EXTRACTION of the
       workbook, published into `inputs/` as the instrument. `proceed` fires
       either way, the diff runs, and `mismatches: 0` is reported by a check
       that compared ACE to ACE. Live on `poverty-graduation/20260905-1345`,
       whose only instrument in `inputs[]` is a `text/markdown`
       "(official, extracted verbatim)" file while the publisher's workbook
       sits in a DIFFERENT opportunity's inputs.

       `artifactClass: 'derived'` does NOT halt — on that run it was the only
       instrument artifact in the frozen inputs, and halting would block a
       build over a file that is very likely correct. It changes what you may
       CLAIM. Carry `resolution.memo` verbatim (it already appends the caveat)
       into the summary's `## Build notes` AND a decision row (§ Decisions
       Log, with `review_ask: recommended-confirmation` + `confirm_reason`),
       and record the class in Step 7's frontmatter, because a derived check is
       real but **unfalsifiable**: an error in the extraction is reproduced
       faithfully by the build and the diff still reads clean. Name the
       publisher's file that would close it.

       Then fetch by `file_id`:

       ```ts
       drive_download_binary({ fileId, writeToPath: '<scratch>/<name>.xlsx' })
       ```

       `drive_read_file` returns a typed `unsupported_binary_mimetype` error for
       `.xlsx` / `.pdf` / `.docx` and points at `drive_download_binary` (see
       `docs/atom-schemas.md § drive_read_file`) — reach for the binary atom
       first rather than rediscovering that (ace#1527). **Read the SOURCE, never
       the Nova brief and never the PDD's restatement**: both are model-authored,
       and one of them is the artifact this step exists to test.

    3. **Trust the extraction BEFORE using it as an oracle — run this FIRST.**

       ```ts
       import {
         readXlsxColumn,
         assertExtractionTrusted,
       } from '../../lib/instrument-constants';
       const extracted = readXlsxColumn(bytes, {
         sheet, column, firstRow, lastRow,      // all declared by the SOURCE
       });
       const trust = assertExtractionTrusted(extracted.values, {
         expectedFirst, expectedLast, expectedRowCount,
         // 'none' for a scorecard POINTS column — it restarts at 0 for each
         // indicator, so it is never monotonic (ace#2932). Omit it for a
         // poverty-likelihood column, which is strictly monotonic.
         direction,
       });
       ```

       `trusted: false` → **HALT.** Print every `trust.failures` entry and every
       `extracted.problems` entry, then stop: do NOT diff, do NOT edit the app,
       and do NOT write the success summary. An unchecked extraction is a second
       way to ship a wrong instrument while reporting success — the first repair
       round's extraction produced `score 4 -> 79.0`, because an `.xlsx` cell
       carrying `t="s"` holds an INDEX into `xl/sharedStrings.xml` and an
       undecoded index is a perfectly plausible number. `readXlsxColumn` decodes
       through the shared-string table and returns an unresolved index as a
       STRING for exactly that reason, so a `non-numeric` failure is the
       header-leak signature, not a parser quirk. The three assertions
       (endpoints, strict monotonicity, row count) are independent and all run,
       so the printed list is every way the extraction is wrong, not the first.

    4. **Read the BUILT literals from Nova, then diff.** `get_field` over each
       scoring `calculate` and each lookup branch, addressed off the Step-4a
       `get_app` blueprint map — reuse it, do not re-fetch the app. Build a flat
       `key -> points` table plus an `indicator -> {option -> points}` table for
       each side, then:

       ```ts
       import {
         diffScoringConstants,
         compareMaxScore,
       } from '../../lib/instrument-constants';
       const diff = diffScoringConstants({ source: sourceConstants, built: builtConstants });
       const max  = compareMaxScore({ sourcePoints, builtPoints, clampAt });
       ```

       `clampAt` is the ceiling of the PDD's `min(<score>, N)` clamp. Judge
       nothing by eye: `diff.mismatches`, `diff.missingInBuild` and
       `diff.extraInBuild` are the finding set, and `max.clampDead` is the
       second-order one.

    5. **Any mismatch, or `clampDead: true`, is a HALT — this is not a warn.**
       Repair in a **bounded loop, max 3 iterations**: `edit_field` the offending
       literal → `save_work` (require `saved: true`) → re-fetch with `app_id` →
       re-diff. If anything still disagrees after the third,
       surface a structured failure naming every `{key, source, built}` plus
       `sourceMax` vs `builtMax`, and do NOT write the success summary.
       `clampDead: true` alongside `clampReachableInSource: true` means the built
       instrument cannot reach the ceiling its own clamp exists to enforce — the
       clamp is dead code and the overshoot the PDD wants observable can never
       fire, which is precisely how a wrong instrument stays internally
       consistent with its own wrong numbers. Fix the constants; never delete
       the clamp to make the check pass.

    6. **`## Build notes` records the CHECK, not just its verdict.** Write
       into the summary's `## Build notes` the source `file_id` and file name, **`resolution.artifactClass` — whether the diff
       was against the publisher's own file or against a derived extraction of
       it (ace#2110)** — the sheet / column / row range read, the number
       of rows checked, both endpoint values as extracted, `sourceMax` vs
       `builtMax` and whether the clamp is live, and the mismatch count (`0` on
       success). Add the licence note: the published instrument is reproduced
       UNMODIFIED — verbatim transcription of the scorecard and its lookup table
       is what the licence permits, and any "improvement", including a tidier
       rounding, is out of scope for this build.

    (No `[FIXED]` instrument → skip cleanly; `## Build notes` says so. A `[FIXED]`
    instrument whose source cannot be resolved — not in `inputs[]`, and not
    found by the one-level walk of the manifest's recorded folder ids — is a
    **HALT**, never a skip (ace#1648). A skip is a legitimate outcome only in
    the first case; a SILENT skip is never one.)

    **No added options on a `[FIXED]` instrument (ace#2366).** A "Declined",
    "Don't know" or "Refused" option on a `[FIXED]` instrument question is NOT
    `[ACE]` latitude unless the instrument itself carries that option — it is an
    added option on a verbatim-only tool, even when it scores 0. Record refusal
    at the visit level (the PDD's non-payable outcomes), never as an extra
    answer. `app-release-qa § Step 4.8` diffs the released form against the
    instrument file and blocks on it.

4k′. **Partner-instrument field provenance (ace#2197) — runs ACE-DIRECT,
    beside 4k.** When the PDD builds a form out of a partner's SHIPPED
    instrument that sits in `inputs/` (a partner CCZ / XForm named by
    `inputs-manifest.yaml` — `[FIXED]` or not), every field identifier the PDD
    names must say where it came from. On `spark-facilitator/20260907-1120`
    § 5.3 screen 8 listed `male_leader_attendence`, `female_leader_attendence`
    (verbatim from Spark's v1392 `forms-4.xml`, typo and all) beside
    `partner_staff_attendance`, which exists nowhere in that app — and the
    invented name read as the partner's own field in the build, the Work Order
    and the training materials. Resolve the instrument exactly as 4k step 2
    does (manifest only, never a composed path), unzip it, and run:

    ```ts
    import {
      checkInstrumentFieldProvenance,
      declaredNetNewIdentifiers,
    } from '../../lib/instrument-field-provenance';
    const prov = checkInstrumentFieldProvenance({
      fieldSpec,                                   // the PDD's field-spec table rows for this form
      instrumentForms,                             // the partner form XML(s) the PDD cites
      declaredNetNew: declaredNetNewIdentifiers(pddMarkdown), // its reused-vs-net-new split
    });
    ```

    Every identifier comes back `reused`, `net-new`, or
    `claimed-reused-but-absent` (absent from the instrument, yet listed beside a
    reused field or on a line that says "reused"/"verbatim", and not declared
    NET-NEW). Only the third is a finding, and it is **not** yours to resolve by
    guessing: build the field under the PDD's name, record it as NET-NEW in
    `## Build notes`, and write one decision row per finding (`evidence_basis:
    conflicting`, `review_ask: recommended-confirmation`) quoting
    `prov.findings[i].message` — the PDD must either name the instrument's real
    field or declare the identifier NET-NEW in its split. No partner instrument
    in `inputs/` → skip and say so in `## Build notes`. *Enforced:*
    `test/lib/instrument-field-provenance.test.ts` (the real v1392 form and the
    run's own PDD).

4l. **Entity state-taxonomy fidelity (ace#1564) — runs ACE-DIRECT.** When the
    followed entity carries states the app must NAME, those names are the
    partner's own process vocabulary and ACE only transcribes them. Step 3
    hands the architect the taxonomy as PROSE, and the architect needs the
    option set to build the phase-filtered step picker `longitudinal-visits`
    requires — so a thin or missing declaration is filled in with something
    plausible. On `spark-facilitator/20260820-0817` that shipped four invented
    phase labels and a different four-way partition of the 24 steps than
    Spark's own published guide (which sat in the run's `inputs/`). Every gate
    passed it: `validate_app` checks structure, the eval grades against a PDD
    that describes the lifecycle narratively, and `app-release-qa` checks counts
    and install-time behaviour — an app is internally consistent with its own
    invented vocabulary. The Learn app then teaches one mapping while Deliver
    offers another, and the invented labels reach real workers and, via the
    training deck, the partner.

    1. **Trigger.** Fires iff the app ships any state option set the worker
       sees — a phase / stage / status / round picker, case-list column, or
       filter. **Always fires for `archetype: longitudinal-visits`**, whose
       case-list requirement makes such a state mandatory. No such state
       anywhere → skip cleanly and say so in the summary's `## Build notes`
       (`entity_state_taxonomy: skipped — <reason>`).
       **Exception — a declared stateless entity (ace#2774).** When
       `parseStateTaxonomy` returns `stateless: true` (the PDD row reads
       `stateless [source: …]`), the PDD has positively declared that the
       followed entity has no states: brief NO state field, no phase picker
       and no state case-list column, and record
       `entity_state_taxonomy: stateless — 0 states declared` in the summary.
       The diff in step 3 still runs (declared `[]`), so any state option set
       the architect added anyway surfaces as `extraInBuild` — an invented
       state — and is repaired by removal.

    2. **Parse the DECLARED taxonomy — this is the only authority.**

       ```ts
       import { parseStateTaxonomy } from '../../lib/entity-state-taxonomy';
       const declared = parseStateTaxonomy(programParameters.entity_state_taxonomy);
       ```

       `declared: false` → **HALT.** The PDD declares no state vocabulary while
       the trigger fires: record a Phase-1 finding naming
       `program_parameters.entity_state_taxonomy` (and the § Entity Lifecycle
       prose it should be derived from), and do not build the picker.
       **Do not substitute a generic lifecycle vocabulary to keep the build
       moving** — an invented phase name is worse than a gap, because a gap is
       visible and a plausible wrong vocabulary is not. `problems` non-empty
       (overlapping step ranges, duplicate values, duplicate labels) → HALT the
       same way: the ambiguity is the PDD's to resolve, not this step's.

       When `declared.source` names a document, the brief must have been
       composed from THAT file out of the run's frozen `inputs/` (resolved via
       `inputs-manifest.yaml`), not from the PDD's summary table. If it was
       not, re-compose before diffing — the summary table is the artifact under
       test.

    3. **Read the BUILT option set from Nova, then diff.** `get_field` over each
       state-bearing select, addressed off the Step-4a `get_app` blueprint map
       (reuse it, do not re-fetch), plus the member activity/step list each
       state exposes. Then:

       ```ts
       import { diffStateTaxonomy, describeTaxonomyDiff } from '../../lib/entity-state-taxonomy';
       const diff = diffStateTaxonomy({ declared: declared.states, built });
       ```

       Judge nothing by eye: `diff.extraInBuild` (an invented state),
       `diff.missingInBuild`, `diff.relabelled` (the partner's words rewritten)
       and `diff.repartitioned` (the step partition moved) are the finding set,
       and `describeTaxonomyDiff` renders them.

    4. **Any finding is a HALT — this is not a warn.** Repair in a **bounded
       loop, max 3 iterations**: `edit_field` the offending option value / label
       / member list → `save_work` (require `saved: true`) → re-fetch with
       `app_id` → re-diff. If anything still disagrees after the
       third, surface a structured failure listing every finding line and do NOT
       write the success summary. Never "fix" the diff by editing the PDD's
       declared taxonomy to match what was built.

    5. **The Learn app is briefed from the SAME declared taxonomy**, so
       Learn/Deliver agreement is transitive — two builds that each match the
       PDD cannot contradict each other. If the Learn app was briefed from
       anything else, that is the same defect one app over: record it as a
       residual against `pdd-to-learn-app` rather than reconciling Deliver to
       Learn.

    6. **`## Build notes` records the CHECK, not just its verdict.** Write
       into the summary's `## Build notes` the declared
       state values with their labels and step ranges, the source document (or
       `none — declared inline in the PDD`), the number of states and steps
       compared, and the finding count (`0` on success).

    7. **Propagate the corrected taxonomy to the CASE-LIST ENUMS
       (dimagi-internal/ace#1688).** Steps 3–4 repair the FORM's option labels
       via `edit_field`. They do not touch the case-list columns — and this
       step's own trigger (step 1) names a *case-list column* as a surface the
       taxonomy reaches. That gap is the whole of ace#1688: on
       `spark-facilitator/20260820-0817` the Phase-3 correction landed on the
       form itemsets and never on the enums, so the `fcap_community` tile kept
       rendering the earlier INVENTED taxonomy while the form offered Spark's
       real one. Stored `1` read as `1. Introduction` before the visit and
       `1. Planning` during it.

       **ACE does not author these enums — the architect does.** The case-list
       tool family (`add_case_list_columns`, `update_case_list_column`,
       `configure_case_list`) carries a `kind: 'id-mapping'` column whose
       `mapping: [{value, label}]` is supplied by whoever calls it, and the
       autonomous architect calls it while building the picker. So the enum is
       composed from the architect's reading of the brief, independently of the
       itemset, and nothing reconciles the two. These atoms are available at
       **ACE-direct** (Step 4d already uses the family), which is why the
       reconciliation belongs here rather than in an upstream issue.

       1. For each state-bearing select repaired above, read the module's case
          list — `get_module({app_id, moduleUuid})` off the Step-4a addressing
          map — and select every column with `kind: 'id-mapping'` whose `field`
          is a case property that select writes.
       2. **Derive, do not compare-then-guess.** Build the mapping from the
          form's itemset: one `{value, label}` per option, using the option's
          own value and its repaired label. Keep the column's existing `field`,
          `header`, `sort` and visibility; replace only `mapping`. Where the
          tile deliberately shows a SUBSET of the options, keep that subset —
          the rule is subset, not equality — but every entry it does keep must
          come from the itemset.
       3. `update_case_list_column({work_id, request_id, moduleUuid, columnUuid,
          column})` with the full column body (the uuid carries over; never
          supply one).
       4. `save_work` (require `saved: true`), then re-fetch via
          `get_module({app_id, …})` and re-assert value-for-value against the
          itemset. **Bounded loop, max 3 iterations**, same shape as 3–4. Still
          disagreeing after the third → structured failure naming each column
          and the values that differ; do NOT write the success summary.
       5. Record in the summary's `## Build notes`: columns rewritten, values per column, and the
          form each was derived from.

       **Never reconcile the other way.** The itemset is the authority — it is
       what the worker picks from and what the stored value means. Editing the
       form's labels to match a stale enum re-introduces the invented
       vocabulary this step exists to remove.

    8. **Record every tile value no form writes BY DESIGN
       (dimagi-internal/ace#3220).** A state the PDD says is set OUTSIDE the
       forms — a Phase 10 close-out bulk case update, an HQ automatic case
       update, an integration — has a case-list label and no form writer, so
       the released-CCZ gate cannot tell it from a stale enum. For each such
       state, and ONLY where the PDD states it (the `entity_state_taxonomy`
       row, § Entity Lifecycle, or the build residual this step files for it —
       e.g. connect-fi's *"No form sets stage Handed over at close-out; every
       adult still in progress on 28 Feb 2027 needs a bulk case update"*), add
       an entry to the summary's `externally_written_case_values` frontmatter
       (Step 7): `property` (the case property the column renders), `values`
       (the stored values, exactly as the tile maps them), `writer` (what sets
       them, e.g. `Phase 10 close-out bulk case update on HQ`) and `source`
       (the PDD section, or the residual quoted verbatim). Keep the residual
       too — it is the human-facing ask that the out-of-form write actually
       happens; this entry is its machine-readable twin. **Never add an entry
       to clear a gate finding:** a tile value with no PDD statement behind it
       is an invented or stale enum, and the fix is to remove it (sub-step 7),
       not to declare it. No such state → `externally_written_case_values: []`.

       *Enforced downstream:* `app-release-qa § Step 4` check 3 runs
       `checkCczCaseListEnumFidelity` over the released CCZ and halts with
       `[BLOCKER]` `case-list-enum-drift` if any of this was missed — that gate
       is what makes this step falsifiable rather than aspirational
       (`lib/ccz-enum-fidelity.ts`, `test/lib/ccz-enum-fidelity.test.ts`).

4n. **Derived-chain guard check (a value computed from a subtree the visit
    never entered) — runs ACE-DIRECT (ace#1823).** Placed immediately before
    4m so every STRUCTURAL check still lands ahead of the language layer,
    which stays LAST. A repair here edits `relevant` / `calculate`
    expressions and never label text, so it cannot demote a translation.

    **The defect.** A form gates a group on consent and then computes derived
    values at form ROOT, where no `relevant` applies. On a vacant / refused /
    no-eligible-respondent visit the group is skipped, `count()` over the empty
    nodeset returns **0**, and the form submits a complete, confident, wrong
    record. Live on `hh-poverty-targeting` (HQ app
    `ce668763ad6c4b48ac5f4cd4502f3f8c`, released build), read straight out of
    `deliver-latest-release.ccz` → `modules-0/forms-0.xml`:

    ```
    /data/roster        relevant="/data/consent_screen/consent = 'yes'"   <- gated
    /data/member_count  = count(/data/roster/is_member[. = 'yes'])        <- NOT guarded
    /data/hh_size_band  = if(/data/member_count <= 3, 'le3', …)           <- NOT guarded
    /data/size_points   = if(/data/hh_size_band = 'le3', 31, …)           <- NOT guarded
    /data/ppi_score     = if(/data/visit_outcome = 'completed', <sum>, '') <- guarded
    ```

    So `member_count = 0`, `hh_size_band = 'le3'`, `size_points = 31` on every
    non-payable door. `ppi_score` is correctly blank, which is exactly why this
    survives: **nothing looks wrong at the score level.** The corruption is one
    layer down, in the band — and the band is the field a band-boundary fraud
    control groups on (PDD § Evidence Model, Layer C). On that run it is
    **1,072 non-payable doors of 3,794** (28%) landing in the 31-point band by
    construction. A worker with more vacant doors looks like a worker
    clustering at the boundary; the signal and the artefact are
    indistinguishable.

    Every gate is blind to it. A `calculate` over an empty nodeset is valid
    XForm, so `validate_app` passes, `app-release-qa` passes (it checks counts
    and install-time behaviour), the app installs, plays and submits, and the
    eval grades against a narrative PDD. Phase 7 blanked the chain in the
    synthetic fixture and declared the deviation — a fixture-side workaround.
    The app still ships this way, so a real deployment would too.

    ```ts
    import { checkDerivedChainGuards, formatDerivedChainReport }
      from '../../lib/derived-chain-guard';
    const report = checkDerivedChainGuards(rootFields);   // from Step 4a's get_form
    ```

    **Two guard shapes count, because the app that motivated this used the
    second:** the field carries its own `relevant`, OR its `calculate` is a
    conditional whose CONDITION reads a field outside the gated subtree (the
    `ppi_score` shape). A conditional whose condition reads only tainted fields
    is **not** a guard — `if(member_count <= 3, 'le3', …)` looks defensive and
    faithfully converts a phantom 0 into a phantom band. Taint therefore
    PROPAGATES: guarding the leaf is not enough and guarding the final score is
    not enough. Every node between the gated subtree and the submitted record
    has to be able to say what its value means on a visit that never happened.

    1. Run the check on the root field list already fetched in Step 4a.
    2. **For each finding, apply the SAME guard the payable path already
       uses** — normally the visit-outcome discriminator (`relevant:
       "/data/visit_outcome = 'completed'"`, or the inline `if(...)` shape if
       the chain already uses one). Re-run to confirm `findings.length === 0`.
       Bounded at 3 iterations like 4a–4g.
    3. **A finding may be CLEARED BY JUSTIFICATION instead**, and this is a
       real case, not an escape hatch: sometimes a zero over an empty nodeset
       is exactly right ("units delivered on a refused visit: 0"). The check
       does not claim otherwise. It claims the form has to SAY so — record each
       cleared finding as a decision row (§ Decisions Log) naming the field
       and why its value is meaningful on a skipped visit. Silence is not a
       justification.
    4. Record `formatDerivedChainReport(...)` in the summary's `## Build
       notes` either way.

    (Forms with no `relevant`-gated container skip cleanly — `gatedSources` is
    empty and there is nothing to find. *Enforced:*
    `test/lib/derived-chain-guard.test.ts` +
    `test/skills/deliver-l0-loop-integrity.test.ts`.)

4o. **Metric terms are SUBMITTED on the paid form (ace#2590) — runs
    ACE-DIRECT.** Placed after 4n and before 4m: a repair adds a hidden
    `calculate` field and never edits label text, so it cannot demote a
    translation. Step 4h checks that what is TAUGHT is collectable; nothing
    else checks that what is MEASURED is submitted.

    **The defect.** Connect receives the paid form as visits and nothing
    else, so a PDD § Success Metrics indicator is computable from visit data
    only if every numerator and denominator term rides on that form. A value
    held on the CASE (or captured on an unpaid form, such as enrolment) is
    invisible to Connect unless the paid form mirrors it as a hidden
    `calculate`. On `spark-facilitator/20261001-2208` PDD §8.2 S1 was
    "Households represented ÷ enrolled number_of_households"; the Community
    Meeting Record READ `#community/number_of_households` inside the validate
    of `hh_represented_at_the_meeting` (`. <= #community/number_of_households`)
    and never submitted it — none of its nine hidden case-write mirrors carried
    it. Phase 7's `semantic-registry-author` had to list S1 under "Not
    computable from visit data": the run completed and a partner-owned
    indicator vanished from every report. The 20260926-1800 build only had S1
    because it happened to submit `enrolled_households`.

    1. Enumerate, verbatim, every PDD § Success Metrics row the indicator
       layer will compute, and split each into its terms — `numerator` +
       `denominator` for a rate, `value` for a count or mean. Resolve EACH term
       to where its value lives — this is the judgement, made once, per term:
       `{kind:'field', fieldId}` (captured or calculated on the paid form),
       `{kind:'case', property, caseType}` (a case property, e.g. one written
       at enrolment), or `{kind:'external', reason}` (data visits cannot carry:
       a payment ledger, an external survey, a supervisor log). Do not resolve
       a term to `external` because mirroring it is inconvenient — `external`
       means no visit can carry it.
    2. Run the check against the PAID form's fields from Step 4a's `get_form`
       (the form whose submission Connect pays — the deliver-unit form):

       ```ts
       import { checkMetricTermsSubmitted, formatMetricTermsReport }
         from '../../lib/metric-terms-submitted';
       const report = checkMetricTermsSubmitted(terms, paidFormFields);
       ```

    3. **For each `case-not-mirrored` finding, add a hidden field whose
       `calculate` is the case reference** (e.g. `enrolled_households =
       #community/number_of_households`; a blank guard `if(#community/x = '',
       0, #community/x)` also counts) via `add_fields` in the open private work,
       `save_work`, re-read the form with `app_id`, and re-run until
       `findings.length === 0`. `readsAt` names where the form already READS
       the value — that is the proof the value is on the device at submit time.
       For `field-absent` / `field-not-a-value`, either the resolution in step 1
       was wrong (fix the mapping) or the PDD's captured field is missing (add
       it). Bounded at 3 iterations like 4a–4n.
    4. **Any term still unsubmitted after the loop, and every `external` term,
       is named in the summary as not computable, with the reason** —
       `report.notComputable` plus the residual findings, as one decision
       row per term (§ Decisions Log — `deliver-metric-not-computable-<slug>`,
       with `review_ask: recommended-confirmation` + `confirm_reason`, since
       a partner-owned indicator is going unmeasured) and in the
       `metric_terms` frontmatter block. A metric that
       silently stops being computable is the defect; a named one is a
       decision a reviewer can see and answer.
    5. `report.status === 'unable'` means the check **did not run** — no terms
       were enumerated, or the paid form read is empty. That is NOT a pass:
       record `formatMetricTermsReport(report)` with its reason in the
       summary's `## Build notes` and fix the input. Record the report in
       `## Build notes` either way.

    *Enforced:* `test/lib/metric-terms-submitted.test.ts` (the shipped S1 form
    as positive control; the same form with `enrolled_households` mirrored as
    the negative control) + `test/skills/deliver-l0-loop-integrity.test.ts`.

4m. **Language layer — runs ACE-DIRECT, LAST of the 4x steps (ace#1556).**
    Applies only when the PDD names a working language other than English;
    otherwise skip and say so in the summary.

    **Why ACE-direct and not the architect.** The architect's operating prompt
    (nova plugin `1.26.0`/`1.27.0`, `skills/autobuild/SKILL.md`) says *"Never
    treat your own language fluency as a substitute or bulk-translate
    self-generated text through `update_translations`. Only save target text
    supplied by the user."* An `/ace:run` supplies no human target strings, so
    the architect declines and the layer silently never lands — 207 units
    copied, 0 translated, in both targets on `spark-facilitator/20260820-0817`
    (ace#1556). ACE is the caller — the "user" in that sentence — so ACE
    supplies the target text through the same six atoms on its own Nova MCP
    surface. Running here also makes translate-LAST **structural**: every
    English-editing step (4a–4k) is already done, so nothing can demote a
    translation to `out-of-date` behind you.

    Execute `_app-component-library.md § app-language-layer` **ACE's ACE-direct
    recipe** verbatim — `get_languages` → `add_language(copyFrom: 'en')` →
    page `get_translatable_content` and author real values via
    `update_translations` (≤50 units/call, echoing each just-read
    `sourceFingerprint`) → `get_languages` again. Read the atoms' live schemas
    from Nova's `tools/list`; do not paraphrase them here.

    **Gate:** `out-of-date` and `missing` must both be 0 at hand-off. Record
    the final per-language coverage counts in the summary's `## Build notes`,
    plus one line
    stating the translations are ACE-authored (`origin: ai`) and carry
    `needs-review` until a speaker of the language reviews them. If the layer
    cannot be completed, halt loud with the counts — do NOT write a summary
    claiming a language layer the app does not carry. Partial coverage is the
    false affordance the issue was filed about: units left `origin: copied`
    are English strings wearing the language's name, and a worker cannot tell
    them apart from real translations.

5. **(Optional) Inspect the built app** via `/nova:show <app_id>` to
   cross-check structure against the PDD before writing the summary.

6. **Self-evaluate (LLM-as-Judge):**
   - Does the app structure match the PDD Deliver spec?
   - Is the delivery unit framed correctly for the archetype?
   - Are all Connectify fields configured (Deliver Unit, Entity ID)?
   - Are verification criteria encoded in form questions?
   - Did every field the PDD spelled `select` / `lookup` ship as a select
     with a real option source, and is every remaining gap named (Step 4f)?
   - Does every screen hold a set the worker can hold in view, with no group
     over the ceiling and no `repeat` nested in a field-list (Step 4g), and is
     each surviving `warn` justified in `## Build notes`?
   - Does every node feeding `entity_id` / `entity_name` actually vary per
     worker and per entity — no hidden `caseWrite` fake preload (Step 4h), no
     bare `text` separator between two parts (which compiles to subtraction),
     and no dependency on a followup form reading its own case?
   - If any consent is sought from the people whose data or images are
     captured — spoken or field-gated — does that script carry all six
     `consent-script-floor` elements, `confidential` and where-the-data-goes
     included?
   - Is every PDD § Success Metrics numerator / denominator term SUBMITTED
     on the paid form — captured, or mirrored from the case by a hidden
     `calculate` — and is every term that is not named as not computable,
     with the reason (Step 4o)?
   - If the PDD marks an instrument `[FIXED]`, was every scoring constant
     diffed against the SOURCE file from `inputs-manifest.yaml` (not the brief,
     not the PDD's restatement) on a `trusted` extraction, with zero mismatches
     and a clamp that can still fire (Step 4k)? If the step skipped, does
     `## Build notes` say why — and was the reason "no instrument is `[FIXED]`"? An
     unresolvable `[FIXED]` source is a HALT, not a skip (ace#1648).

6b. **Exit gate — `nova-app-lint` must exit 0 before you return.** Run
   `scripts/nova-app-lint.ts --app <nova_app_id> --type deliver` (invocation
   in `agents/commcare-setup.md § Step 1.4`) on the SAVED app. It checks in
   code the standing instructions this skill briefs (app name, the
   `section`/`module` terminology rule including bound lookup rows, lookup
   binds, case-list labels vs form labels, casedb preloads, Connect-marker
   floor, starter module). Fix every `[BLOCKER]` it names, save, re-run; do
   not edit for a `[WARN]` — record it in `## Build notes`. Quote its first
   line (`… PASS|WARN — N blocker(s) …`) in `## Build notes`. Phase 3 will
   not dispatch the eval while it fails, so returning with blockers only
   moves the same fix later.

7. **Write the summary** to
   `ACE/<opp-name>/runs/<run-id>/3-commcare/pdd-to-deliver-app_summary.md` with required
   frontmatter:

   ```yaml
   ---
   nova_app_id: <id-returned-by-autobuild>
   # `/build/`, NOT the legacy `/apps/` route, which 404s (ace#1431).
   # Built by `novaAppUrl()` in `lib/nova-url.ts` — the single source.
   nova_app_url: https://commcare.app/build/<id-returned-by-autobuild>
   archetype: <atomic-visit | longitudinal-visits | focus-group | multi-stage>
   delivery_unit: <one-line description matching the PDD>
   # Addressing map — Nova is uuid-addressed (2026-07-31, ace#1132).
   # COPIED VERBATIM from the get_app response § 4a step 2 already read
   # (the `[uuid …]` printed on each module/form/field) — NEVER typed
   # from a pattern, re-derived, or reconstructed from memory (ace#2144).
   # app-deploy Step 2.5 and app-connect-coverage address off this block
   # instead of calling get_app, so a wrong uuid here is trusted.
   nova_uuids:
     modules:
       - name: <module name>
         uuid: <moduleUuid>
         forms:
           - name: <form name>
             uuid: <formUuid>
             # Only the fields later steps address directly (entity_key,
             # payable marker, image uploads). Not every field.
             fields:
               entity_key: <fieldUuid>
   # Componentized runs ONLY (Phase 1 products.mode == componentized): the
   # Phase-1 component ids this Deliver app built forms for, verbatim.
   # app-deploy copies it into products.apps.deliver.components_built via
   # buildCommcareProducts (ace#2157). Omit on the synthesized path.
   components_built: [<component_id>, ...]
   externally_written_case_values: []  # Step 4l sub-step 8 (ace#3220).
                            # Tile values no form writes BY DESIGN, each
                            # {property, values, writer, source} — e.g.
                            # {property: stage, values: [handed_over],
                            #  writer: "Phase 10 close-out bulk case update
                            #  on HQ", source: "<PDD residual, verbatim>"}.
                            # app-release-qa check 3 passes ONLY these as
                            # [INFO]; empty list is the usual value.
   option_source_gaps: []   # Step 4f — one entry per PDD-declared select
                            # that still shipped as free text, with the
                            # table + value column + label column it needs.
                            # Empty list is the expected value.
   option_register:         # Step 4f. One entry per PDD-declared partner
                            # register. Omit the block ONLY when the PDD
                            # declares no register — an absent block on a
                            # triggered field is a BLOCKER at the eval, since
                            # "the check did not run" is indistinguishable from
                            # "it was skipped because it would have failed".
                            # `verified` (ace#1886) is the run's EVIDENCE the
                            # select is actually live: it comes from
                            # verifyLookupBind over a get_field read-back,
                            # never from the write's own response, which
                            # reports `options: []` on a correctly bound field.
     - field: <field id as the PDD names it>
       tag: <lookup table tag the PDD declared>
       table_id: <uuid returned by create_lookup_table>
       rows: <n>            # rows written, from the partner's own source
       findings: 0          # diffOptionRegister + diffRegisterRows; >0 HALTED
       verified: true       # verifyLookupBind code `ok`; anything else HALTED
   lookup_bind_audit:       # Step 4f step 8 (ace#2143). EVERY lookup-backed
                            # select in the app, whoever bound it — not just
                            # the ones this step bound. Required whenever the
                            # app has at least one; `sites: 0` is the value
                            # for an app with none. A missing block on an app
                            # that HAS one reads as "the sweep did not run".
     sites: <n>             # fields audited via auditLookupBinds
     failures: 0            # >0 HALTED; quote describeLookupBindAudit lines
   metric_terms:            # Step 4o (ace#2590). Always present when the PDD
                            # has a § Success Metrics table.
     submitted: <n>         # terms the paid form carries (report.submitted)
     not_computable:        # every external term + every residual finding;
                            # [] is the expected value
       - metric: <PDD id, e.g. S1>
         term: <the PDD's words>
         reason: <why visit data cannot carry it>
   instrument_constants:    # Step 4k (ace#1527). Omit the block ONLY when no
                            # instrument is [FIXED]. There is no other skip
                            # reason: an unresolvable [FIXED] source HALTS the
                            # step rather than recording a skip (ace#1648).
     source_file_id: <file_id from inputs-manifest.yaml>
     artifact_class: published | derived
                            # ace#2110. `resolution.artifactClass`. `published`
                            # = the publisher's own workbook/PDF. `derived` = an
                            # extraction of it, so the check is real but
                            # UNFALSIFIABLE (an error in the extraction is
                            # reproduced by the build and the diff reads clean).
                            # A reader must be able to tell the two apart
                            # without opening Drive.
     rows_checked: <n>      # rows actually diffed against the source
     mismatches: 0          # anything above 0 means Step 4k halted
   ---
   ```

   **`nova_uuids` is read back, not trusted.** Its module/form uuids come
   from the `get_app` response § 4a step 2 already read — a fresh
   `get_app({app_id})` if a later step added a module or form — copied
   character for character, never written from a pattern. On
   `spark-facilitator/20260906-2233` the Deliver map recorded
   `11110000-0000-4000-8000-000000000001` for a module the app holds as
   `11111111-0000-4000-8000-000000000001` (all four module/form uuids
   truncated the same way, field uuids correct), and `app-deploy`'s lint
   then failed `get_form` with "No module with UUID … is in this app"
   (ace#2144). After writing the summary, call
   `get_form({app_id, moduleUuid, formUuid})` on one pair from the block;
   if it does not resolve, rewrite the block from a fresh `get_app` before
   moving on.

   **Every latitude taken and every ambiguity hit is a decision row — the
   run's review artifact.** Append them with ONE `decisions_append_rows` call
   immediately after this write (§ Decisions Log): one row per place the build
   exercised latitude the PDD granted (`deliver-latitude-<slug>`), one per
   `[FIXED]` statement that could not be built exactly as written
   (`deliver-ambiguity-<slug>`, `OPEN` when unresolved), plus the rows Steps
   3–4o direct (stated exemptions, cleared derived-chain findings, metrics not
   computable from visit data, taught-vs-collectable findings). Cite the PDD
   section in `source` on every row. Each row carries `plain`, and `check_at` +
   `correct_looks_like` wherever the choice is visible in the app; an open
   question a person must settle carries `review_ask: recommended-confirmation`
   + `confirm_reason` (`skills/_decisions-review-fields.md`). `decisions.yaml`
   is what ace-web renders with a comment box and an answer editor on every
   row, and an answer there carries into the next run. On
   `poverty-graduation/20260908-0510` this summary listed four `[ACE]`
   latitudes in prose (screen shape, transfer-method capture, derived-chain
   guards, asset menu) and the run's 66 decision rows included none of them,
   so no reviewer could see or answer them (ace#2371, ace#2384). The Phase 3
   boundary now fails this skill if the summary exists and zero rows carry
   `phase: 3-commcare` + `skill: pdd-to-deliver-app`.

   **The body ends with a section headed exactly `## Build notes`** for the
   build team's notes that are not decisions: the screen-shape and
   derived-chain reports, the threshold-coherence checks, the case-read and
   GPS notes, the consent-floor checklist, the instrument-constants and
   state-taxonomy check records, the `verifyLookupBind` verdicts, the
   metric-terms report and the language-layer coverage counts. Write `None.`
   rather than dropping the heading. A note that records a CHOICE a reviewer
   could disagree with belongs in a decision row, not here.

   **State every app check at the scope it is keyed on** — in the decision
   row's `plain` and in `## Build notes` alike. A form constraint or a
   `casedb` read is keyed on the case the form is filled against, so describe
   it as "per community" / "per household", never as enforcing a per-worker
   limit. On `spark-facilitator/20260926-1800` the date check was called the
   "one-community-meeting-per-day check" and the threshold line read "daily cap
   1 vs the one-community-meeting-per-day date check — coherent", which Phase 4
   and the run's review record then read as the app enforcing the per-WORKER
   daily cap. It does not: one worker can record two communities on one day,
   and only Connect's payment unit `max_daily` stops the second being paid. Say
   which limit a per-worker rule relies on (Connect's), and what the app check
   adds at its own scope.

8. **Notify admin group** that Deliver app generation is complete.

## Archetypes

The Deliver app's structure depends on the PDD's `archetype:` field. The
"delivery unit" concept is the most archetype-sensitive part of ACE — get
this wrong and `connect-opp-setup` will configure the wrong verification
rules.

### `atomic-visit`
Delivery unit = **one FLW visit to one beneficiary**. The form is the
verification artifact: every required field, photo, GPS coordinate. Case
management follows the standard create → update → close pattern. The
form's fields map 1:1 to Layer A and Layer B of the PDD's Evidence Model.

### `longitudinal-visits`

Delivery unit = **one FLW visit to one followed entity**, and the entity
is a real case with a life longer than the visit. Structurally this is
CommCare case management as normal — case type, registration form,
follow-up form(s) against a case list — with three requirements the
`atomic-visit` branch does not carry:

1. **The case list must show which visit is due.** Put the entity's
   phase / last-activity / next-due state in the case-list columns (and
   in search inputs where the caseload is large). An FLW who has to open
   a case to discover the next activity will guess instead.
   **Those state names are the PARTNER's vocabulary, and this archetype
   is the reason they exist at all** — a case list showing state means
   the app must name every state, and the architect will invent the set
   if the brief does not carry it. Emit
   `_app-component-library.md § entity-state-taxonomy` (always, for this
   archetype), carry the PDD's declared taxonomy into the brief verbatim,
   and HALT rather than invent when the PDD declares none. Verified at
   ACE-direct by Step 4l (ace#1564).
2. **Follow-up forms preload the case state the predicate reads.** Any
   longitudinal fact Layer A depends on must be *on the submitted form*
   to be enforceable downstream — Connect's form-field rules see the
   form, not the case. Preloading is what makes the longitudinal
   predicate expressible at all.
3. **`entity_id` carries entity + sequence position**, per the PDD's
   `payment-unit-entity-id` decision — typically
   `concat(<case_id>, '-', <activity_code>)`. As elsewhere, `entity_id`
   is a **business key, not the case id**: the case id alone pays each
   entity exactly once, ever.

The failure mode to design against is a Deliver app that is
case-managed and a payment predicate that is not — the app tracks the
entity beautifully while Connect pays for any visit at all
(`spark-facilitator/20260813-2126`, ace#1462).

### `focus-group`

Delivery unit = **one completed FGD session, attested by a 5-field
CommCare form** submitted at session end. The Deliver app for
focus-group is intentionally minimal — it is the **payment trigger
only**, not the content-capture surface and not the artifact-upload
surface.

**FGD content lives in a Google Doc**, not in this app. **The gdoc is
written after the session ends — typically hours or days later — and
cannot be linked from the attestation form at submission time.** All
qualitative content (per-section themes, verbatim quotes, consensus
grading, post-FGD report, facilitator reflection) lives in the gdoc.
Audio recording (if captured) is out-of-band entirely — it does not
go through CommCare; the facilitator attaches audio to the gdoc as a
Drive attachment or shares it through a separate Drive folder. The
attestation form captures only session-happened evidence + consent
confirmation, and each submission is one payment unit. See
`docs/superpowers/specs/2026-05-15-focus-group-archetype-redefinition.md`.

**App shape (one module, one form):**

- **Module 1: Session Attestation** (case type: `fgd_session`).
- **Form: "Session Attestation"** (case-create, `connect.deliver_unit`
  set). One submission = one completed session = one payment trigger.

**Required fields on the attestation form (5 fields):**

| Field | Kind | Notes |
|---|---|---|
| `consent_all_participants` | single_select | Required attestation: did every participant consent to participate? Options: `yes` (consent obtained from all participants) / `no` (one or more declined / not obtained). Constraint: `. = 'yes'` — form cannot be submitted without affirmative consent, because there is no payment for an FGD held without consent. |
| `session_date` | date | When the session was held. Facilitator picks; usually today (submitted at session end) but can be one or two days back if writing it up later. |
| `venue` | text | Free-text venue description. Hint: include the village/community name + the specific space (e.g. "Kibera, community hall behind the primary school"). |
| `gps` | geopoint | Captured at the venue. Anchors location verification (Layer A). Captured at form-fill time on the FLW's device — implicitly proves the FLW was AT the venue when they attested. |
| `photo` | image | A single evidence photo. Hint: an attendance sheet (first names + role + consent marks, NO faces) or a venue photo. Faces only if every participant has actively consented to a face photo. |

That is the complete form. No audio, no participant count, no per-section
fields, no gdoc link, no reflection, no facilitator-name field
(captured implicitly via Connect's FLW identity). Auto-generated
`case_name` from `concat(#user/username, '-', #form/session_date)` keeps
the case list legible.

**Connect markers:**

- `connect.deliver_unit` set on the form.
- `connect.entity_id` defaults to `concat(#user/username, '-', today())` —
  one paid delivery per facilitator per day, the realistic case for
  60-90 min sessions + travel. This is already a business key (good — see
  the §`entity_id` REQUIRED rule). If any LLO schedules ≥2 sessions/day
  per facilitator, override to a finer-grained business key, e.g.
  `concat(#user/username, '-', /data/session_date, '-', /data/venue)` —
  NOT `#case/case_id` (`payment-unit-entity-id` Decisions Log row).

**Coordinator review flow (out-of-band):**

Layer A verification happens automatically against form contents
(GPS within an expected radius of the planned venue, photo attached,
consent attested, session_date within an expected fielding window).
Layer B verification is the coordinator reviewing the **facilitator's
gdoc**, matched to the attestation submission by `(FLW identity,
session_date, venue)` — there is no `gdoc_link` field, so matching is
operator-driven (coordinator sees the attestation in the FormRepeater
feed, expects a gdoc from that facilitator about that session,
follows up if it doesn't arrive within the gdoc submission window).

**Specifically not included:**

- **No audio upload through CommCare.** Audio recording (if captured)
  is out-of-band entirely. CommCare doesn't carry large audio files
  for FGDs — they live in Drive or wherever the LLO keeps audio.
- **No `gdoc_link` field.** The gdoc doesn't exist when the
  attestation is submitted. Linkage between attestation and gdoc is
  coordinator-driven, by `(FLW, session_date, venue)` match.
- **No per-section structured summary fields.** Qualitative content
  lives in the gdoc.
- **No participant-count / segment / start-end-time fields.** These
  go in the gdoc.
- **No facilitator-reflection field.** Goes in the gdoc.
- **No pre-checklist field.** The pre-session preparation is the LLO's
  responsibility; the consent attestation is the only check that needs
  to gate payment.
- **No pre-session + post-session + reviewer-verification form split.**
  One form, submitted at session end.
- **No case management beyond per-session.** No case lifecycle, no
  per-beneficiary cases, no per-participant follow-up.
- **No Learn-app-equivalent training surface.** `pdd-to-learn-app` is a
  no-op for focus-group archetype.

**Brief language for `/nova:autobuild`:** open with "this is a 5-field
session attestation form for an FGD opportunity. The mobile form
captures only proof-of-session-happened (consent, date, venue, GPS,
photo); it is NOT a content-capture form and NOT an artifact-upload
form. Qualitative content lives in a Google Doc written after the
session, out-of-band; audio (if captured) lives in Drive separately.
One submission = one completed session = one Connect deliver_unit
submission = one payment trigger."

### `multi-stage`
Generate one Deliver app per stage that has its own delivery work,
branching on each stage's archetype. The two Deliver apps may have
completely different structures (e.g., Stage 1 = focus-group session
form, Stage 2 = atomic household-visit form).

## MCP Tools Used

- **Google Drive MCP:** `drive_read_file`, `drive_create_file`
- **ACE decisions MCP:** `decisions_append_rows` (Step 7 — § Decisions Log)
- **Nova plugin slash commands:** `/nova:autobuild`, `/nova:show`,
  `/nova:list`, `/nova:edit`
- **Nova MCP tools ACE calls directly** (Steps 4a–4l): `get_app`,
  `get_module`, `get_form`, `search_blueprint` (semantic id → uuids in one
  call), `add_case_list_columns`, `edit_field`, `configure_connect`,
  `update_form`, `get_lookup_tables`, `set_field_options_source`,
  `create_lookup_table`, `update_case_list_column`, and the private-work
  lifecycle `begin_work` / `get_work` / `save_work` / `discard_work`
  (voidcraft-labs/commcare-nova#693, 2026-09-27). Every mutation is staged — `work_id` +
  `request_id`, no `app_id` — and lands only on a `save_work` answering
  `saved: true`; reads take `app_id` (saved) or `work_id` (candidate). See
  `playbook/integrations/nova-integration.md § The private-work authoring contract`. Nova is
  **uuid-addressed** since 2026-07-31 (dimagi-internal/ace#1132) —
  `moduleUuid` / `formUuid` / `fieldUuid`, never indexes; resolve the whole
  map with ONE `get_app({app_id})` at Step 4a and reuse it. The app-level
  Connect mode is set by `configure_connect({work_id, request_id, mode, participants})`,
  which is **REPLACE-ALL** (ace#1133) — `update_app` no longer carries
  `connect_type`. Enforced by `test/skills/nova-uuid-addressing.test.ts`.

See `playbook/integrations/nova-integration.md` for plugin status.

## Mode Behavior
- **Auto:** Build via `/nova:autobuild`, write summary, notify admin,
  proceed.
- **Review:** Build, write summary, present summary for review before
  proceeding.

## Dry-Run Behavior
When `--dry-run` is active:
- Do NOT call `/nova:autobuild` (Nova builds are durable side effects).
- Write the composed brief and the intended Nova invocation to
  `comms-log/dry-run-pdd-to-deliver-app.md`.
- Do not write `app-summaries/deliver-app-summary.md` (no `nova_app_id`
  yet).
- State tracks as `dry-run-success`.

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. An open design question the build could not settle (e.g. no recording path when a whole group refuses the photo) is a row with `review_ask: recommended-confirmation` + `confirm_reason`, not only a residual. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes to the per-run `ACE/<opp-name>/runs/<run-id>/decisions.yaml`
— the register ace-web renders on the public run page, where a reviewer
comments on and answers each row and the answer carries into the next run.
The bar criterion and schema live in `skills/idea-to-pdd/SKILL.md § Decisions
Log Convention` (canonical authority). It owes two kinds of row: one per
latitude taken and per ambiguity hit (REQUIRED, below), and any catalogue row
that meets the bar.

### Every latitude and ambiguity is a decision row (REQUIRED)

Every place the build exercised latitude the PDD granted, and every `[FIXED]`
statement that could not be built exactly as written, is a `decisions.yaml`
row — and the row is the only record of it; there is no second rendering to
keep in step. These are exactly the calls the register exists for: an `[ACE]`
latitude is an `inferred` default, a `[FIXED]` ambiguity is a `conflicting`
one. Until ace#2384 this section was only a catalogue "not a required set",
and the app build wrote zero rows — `poverty-graduation/20260905-1345` and
`20260908-0510` carried 61 and 66 rows, none from Phase 3, while this summary
listed the latitudes in prose. A regression of #399.

| Row field | From the entry |
|---|---|
| `id` | `deliver-latitude-<slug>` / `deliver-ambiguity-<slug>`; slug from the PDD § and the subject, so a re-run of the same PDD re-derives the same id and the atom's idempotent skip holds |
| `phase`, `skill` | `3-commcare`, `pdd-to-deliver-app` |
| `question` | what the PDD left open (latitude) or said two ways (ambiguity) at that § |
| `ai-default` | what ACE chose (latitude) or how it resolved the ambiguity, as a short label, an exact member of `options` |
| `options` | that label plus each alternative the build weighed, 1–8 words each |
| `source` | the PDD § it concerns, naming the document |
| `evidence_basis` | `[ACE]` latitude → `inferred` (`stated` only when the PDD itself names the value chosen); `[FIXED]` ambiguity → `conflicting` |
| `conflict_signals` | ambiguity only, at least 2 entries: the `[FIXED]` statement as written, and the reading or constraint that competed with it — each cited |
| `value_set_by` | `ace` |
| `status` | `ai-default`, always (a caller-asserted `human-decided` is rejected — ace#2307) |
| `reasoning` | why ACE chose it; an ambiguity left OPEN begins `OPEN —`; it ends `Spot-check: <where>.` |
| `plain` | REQUIRED — one line for a programme partner: what was chosen, no field ids, no §-references, no ACE jargon |
| `check_at`, `correct_looks_like` | where in the app a reviewer sees it, and what is there when it is right — whenever the choice is visible |
| `review_ask`, `confirm_reason` | `recommended-confirmation` + one plain sentence, when a person must settle it before launch (an OPEN ambiguity, a gap with no fix this run) |

**Prefer `check_at`; keep the `Spot-check:` sentence too.** Schema v6 gives
the location its own field (`check_at`, `docs/decisions-contract.md`) — write
it directly. Still end `reasoning` with `Spot-check: <app> › <module> › <form>
› <field>.`: the write boundary fills `check_at` from that sentence when it is
absent, and older ace-web summaries built each decision from a fixed set of
keys (`apps/opps/summary.py` on ace-web `main`, c20ef34: id, phase, skill,
question, ai-default, override, options, source, status, reasoning,
override_reasoning, evidence_basis, conflict_signals) and dropped anything
else, so `reasoning` is the copy every renderer shows.

**The boundary checks it.** `verify_phase_artifacts(phase='commcare')`
returns a `decisions` report (`lib/build-phase-decisions.ts`). If
`3-commcare/pdd-to-deliver-app_summary.md` exists while zero rows carry
`phase: 3-commcare` and `skill: pdd-to-deliver-app`, the Phase 3 boundary
fails — a build that took no latitude still owes its catalogue rows (below).
A live partner-facing row with no `plain` is a warning. `app-test-cases` rows
in the same phase do not count.

Worked example (the first entry is the real `20260908-0510` latitude; the
second is illustrative):

```
decisions_append_rows({
  runFolderId: <run-folder file_id>,
  opportunity: <opp-slug>,
  run_id: <run-id>,
  rows: [
    {
      id: "deliver-latitude-transfer-method-capture",
      phase: "3-commcare",
      skill: "pdd-to-deliver-app",
      question: "C6 §12 Q1 leaves open whether one flow serves every transfer method or method is a build variant — which did the build ship?",
      "ai-default": "one flow, method-gated branches",
      options: ["one flow, method-gated branches", "one form per transfer method"],
      source: "C6 PDD §12 Q1 [ACE]",
      status: "ai-default",
      evidence_basis: "inferred",
      plain: "One form covers every transfer method, showing only the questions for the method chosen.",
      check_at: "Deliver app › Transfer record › transfer method",
      correct_looks_like: "Choosing a method shows only that method's questions.",
      value_set_by: "ace",
      reasoning: "One flow reads the method off the household case and relevance-gates three artifact branches. An assumption, not a resolution. Spot-check: Deliver app › Consumption support distribution › consumption_dist › transfer_method."
    },
    {
      id: "deliver-ambiguity-entity-id-grain",
      phase: "3-commcare",
      skill: "pdd-to-deliver-app",
      question: "Targeting §3 and C5 §2 name different payment grains — which does the Deliver entity_id key on?",
      "ai-default": "household",
      options: ["household", "household member"],
      source: "Targeting PDD §3 and C5 PDD §2 [FIXED]",
      status: "ai-default",
      evidence_basis: "conflicting",
      plain: "Payment is counted per household, so one household is paid at most once.",
      check_at: "Deliver app › Asset delivery › payment key",
      correct_looks_like: "Two deliveries to members of the same household share one payment key.",
      review_ask: "recommended-confirmation",
      confirm_reason: "Two parts of the design name different payment grains; the build pays per household until the design's author decides.",
      conflict_signals: [
        "Targeting PDD §3 [FIXED]: one payable survey per household",
        "C5 PDD §2 [FIXED]: an asset is delivered to a named member"
      ],
      value_set_by: "ace",
      reasoning: "OPEN — both are [FIXED]; keyed on household so the Targeting cap holds, flagged for the design author. Spot-check: Deliver app › Asset delivery › asset_delivery › entity_id."
    }
  ]
})
```

The rejection is atomic — one row whose `ai-default` is not in its `options`
costs the whole batch — so check each row before sending. If the atom is
unbound this session, hand-write per `skills/idea-to-pdd/SKILL.md § Schema and
write semantics` (top-level `decisions:`, not `rows:`).

### Common load-bearing decisions for Phase 3

A catalogue of decisions that commonly qualify under the bar — a working
template, not a required set. Emit whichever meet the bar, in the same call
as the latitude and ambiguity rows.

| ID | Question | Map to surface |
|---|---|---|
| `deliver-unit-count` | How many distinct deliver units (modules × forms) does the Deliver app expose? | PDD `Deliver App Specification` numeric |
| `one-form-per-module-workaround` | Are we one-form-per-module to dodge Nova's CCZ marker bug? | `pdd-to-deliver-app-eval` connect-marker-coverage dimension; CLAUDE.md gotcha |
| `multimedia-coverage-strategy` | What multimedia (text vs voice prompts vs both) does the Deliver app surface? | `app-multimedia-coverage` skill output; PDD multimedia note |
| `option-source-binding` | For each PDD-declared select/lookup field, where did its options come from — a Project data table, an inline enumeration, or a named gap? | Step 4f `option_source_gaps`; `pdd-to-deliver-app-eval § Capture fitness` |

The Phase 3 boundary fence enforces these rows
(`agents/orchestrator-reference.md § Phase Write-Back Contract § Decisions
log clause`); the renderer (`skills/decisions-render`) regenerates the gdoc
at end of every phase.

Each row this skill writes uses `phase: 3-commcare` and
`skill: pdd-to-deliver-app`.

## Change log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-19 | **Step 4l sub-step 8 — tile values no form writes BY DESIGN are recorded, not dropped (ace#3220).** connect-fi's Deliver app labels `stage = handed_over` "Handed over at close-out"; no form writes it because the PDD sets it by the Phase 10 close-out bulk case update, so `app-release-qa` check 3 graded a `case-list-enum-drift` BLOCKER on every re-release. Operator decision (2026-10-19): keep the label. The summary now carries `externally_written_case_values` (`{property, values, writer, source}`, each tied to a PDD statement), which `checkCczCaseListEnumFidelity` accepts as `[INFO]` for exactly those values on exactly that property; anything undeclared still fails. *Enforced:* `test/lib/ccz-enum-fidelity.test.ts § declared out-of-form writers`. | ACE team |
| 2026-10-16 | **Step 7 writes a `nova_uuids` block, copied from § 4a step 2's `get_app` and read back (ace#2144).** `app-deploy` Step 2.5 and `app-connect-coverage` both read the Deliver summary's `nova_uuids:` instead of calling `get_app`, but Step 7 never specified one (Learn's Step 7 did). On `spark-facilitator/20260906-2233` the map that was written had all four module/form uuids pattern-truncated (`11110000-…` for `11111111-…`) and the lint's `get_form` failed. The block is now part of the required frontmatter, sourced verbatim from the `get_app` response, with a one-pair `get_form` read-back after the write. *Enforced:* `test/skills/deliver-summary-nova-uuids.test.ts`. | ACE team |
| 2026-10-16 | **§ entity_id: a date-only key component is a per-worker-per-day grain (ace#2935).** The quoted-separator example used `#form/visit_date`, which keys per worker per day; it now uses a time-bearing timestamp and says so, and names the bare-`now()` trap (a hidden field renders it date-only). | ACE team |
| 2026-10-16 | **Step 4f: a lookup's value column must be whitespace-free (ace#2984).** On `kaduna-graduation/20261015-1411` `kgrad_services` had no code-shaped column, three selects saved the display `name` (`"Placeholder: services directory entry 1 …"`), every ACE gate passed (the values were unique), and Nova's `upload_app_to_hq` preflight refused the Deliver app: *"Saved values can't contain whitespace."* Same class as ace#2143, Nova's second rule. `verifyLookupBind` (and so `auditLookupBinds`) now returns `whitespace-values`; authored tables carry a slug `code` column as the saved value. *Enforced:* `test/lib/option-register.test.ts`. | ACE team |
| 2026-10-16 | **Exit gate `nova-app-lint` (Step 6b); Step 4f step 8 runs through it.** The standing instructions this skill briefs are now checked in code right after the build (`scripts/nova-app-lint.ts`, `lib/nova-app-lint.ts`) instead of only by the eval: on `smallholder-seasonal/20261015-1402` the Deliver eval took three passes (~42 min) to clear "module" in 7 bound lookup rows (ace#2976) and a partial `edit_lookup_rows` update that wiped 8 rows (ace#2978); on `kaduna-graduation/20261015-1411` whitespace in a bound value column was first refused by Nova's upload preflight (ace#2984) and case-list labels drifting from form labels were first caught at `app-release-qa` Step 2.8. `verifyLookupBind` gains `whitespace-values`, `blank-values` and `blank-labels`. *Enforced:* `test/lib/nova-app-lint.test.ts` (real blueprints), `test/lib/option-register.test.ts`, `test/agents/phase3-lint-gate.test.ts`. | ACE team |
| 2026-10-12 | **Step 4k prefers the publisher's file over a derived `inputs[]` extraction (ace#2852).** `resolveInstrumentSource` returned the `inputs[]` match before it looked at manifest-recorded subfolders, even when that match classed `derived` — so on `smallholder-seasonal/20261012-1549` the strict path resolved `INSTRUMENT — Nigeria 2018 PPI (… extracted verbatim).md` while the publisher's `nigeria-ppi-2020-scorecard-and-lookup-table.xlsx` sat in the recorded subfolder `official-nigeria-2018-ppi (povertyindex.org)`. The ace#1648 order (inputs[] first) predates the ace#2110 classifier, which disclosed a derived source but never re-ordered the search. Step 2 now walks the subfolders when the `inputs[]` match is derived; the helper resolves a single published subfolder file over it (naming the passed-over entry in its memo), halts on more than one, and keeps the derived entry with its caveat only when nothing published exists. *Enforced:* `test/lib/instrument-constants.test.ts` (real layout and ids from that run). | ACE team |
| 2026-10-03 | **Build memo retired — decisions.yaml is the review artifact (schema v6).** Every `[ACE]` latitude, `[FIXED]` ambiguity, stated exemption and not-computable metric this skill used to tabulate under the summary's `## Build memo` is now a decision row only (`plain`, `check_at`/`correct_looks_like`, `review_ask` + `confirm_reason` for open questions), the non-decision check records move to the summary's `## Build notes`, and the Phase 3 boundary fails a written summary with zero rows under `skill: pdd-to-deliver-app`. Contract: docs/decisions-contract.md. | ACE team |
| 2026-10-01 | **New Step 4o — every PDD § Success Metrics term is SUBMITTED on the paid form (ace#2590).** On `spark-facilitator/20261001-2208` the Community Meeting Record read `#community/number_of_households` inside a validate and never submitted it, so PDD §8.2 S1 (households represented ÷ enrolled households) was not computable in Connect and Phase 7 listed it under "Not computable from visit data" — the run completed and a partner-owned indicator silently vanished. 4h covered taught-vs-collectable; nothing covered measured-vs-submitted. 4o resolves each metric term to a paid-form field, a case property, or an `external` source with a reason, runs `checkMetricTermsSubmitted` (`lib/metric-terms-submitted.ts`) over the paid form, mirrors any case-held term as a hidden `calculate`, and names every term still unsubmitted as not computable in the summary (`metric_terms` frontmatter + build memo). *Enforced:* `test/lib/metric-terms-submitted.test.ts` + `test/skills/deliver-l0-loop-integrity.test.ts`. | ACE team |
| 2026-10-01 | **Step 7: every app check in the build memo is stated at the scope it is keyed on (build-memo-eval, spark-facilitator/20260926-1800).** The Deliver memo called the per-community date check the "one-community-meeting-per-day check" and judged it "coherent" with the per-worker daily cap of 1; Phase 4 and the programme memo then credited the app with enforcing that cap, which only Connect's payment unit `max_daily` does. Paired with `connect-opp-setup` Step 8's scope paragraph and `skills/build-memo`'s `--check`. | ACE team |
| 2026-09-26 | **Step 4j sub-step 6 no longer hard-codes the counter timing (ace#2515).** The snippet hard-coded a pre-increment timing into its `payableCapacity` call, which reads a correct `min(<casedb count> + 1, cap)` clamp as capacity `cap + 1` and HALTs it — then "repairs" it into an under-pay. Observed on `spark-facilitator/20260926-1413` (`min(#form/step_info/prior_index + 1, 3)`, correct, would have halted). It now calls `checkBuiltClampCapacity`, which resolves the timing via `classifyCounterTiming` over the `get_field` read-backs (Nova `#form/` and `#<case_type>/` spellings accepted — captured read-back spells the case read `#community/…`) and returns `unable` rather than assuming one. *Enforced:* `test/lib/payable-cap-build-time.test.ts` (the repro as positive control; `min(<casedb>, cap)` and an under-paying `min(<casedb> + 1, cap - 1)` as negative controls; a skill-text guard against a literal timing), fed from the captured `get_field` read-back `test/fixtures/nova/capped-index-readback-spark-20260926-1413.json`. | ACE team |
| 2026-09-25 | **The case-UPDATE `entity_id` rule now SANCTIONS the case read it used to forbid (ace#2199).** The REQUIRED paragraph still told the architect that a followup `case-ref` could never be built (citing `voidcraft-labs/commcare-nova#458`, closed COMPLETED 2026-08-15) and steered followup forms to `concat(username, <date>)` — the `atomic-visit` grain, which cannot express a per-entity cap and is the ace#1462 failure for a `longitudinal-visits` design. The paragraph's own re-open condition ("re-verify against a live compiled CCZ") is now met: on `spark-facilitator/20260925-1536` the Deliver followup form was briefed with `#case/` reads and the released build `5c1eef4323224550b1c36a7da9521e71` compiles `entity_key` as a live `calculate` over `instance('casedb')` (`@case_id`, `pilot_fcap_step`). The rule now says: read the case with `#case/<property>` in a hidden calculate; `caseWrite` + literal default is still not a read (ace#1224); a visible case-bound field pre-fills the previous answer (ace#2006); never fall back to the username grain for a longitudinal design. *Enforced:* `test/skills/pdd-must-not-assert-mechanisms.test.ts` (inverted to require the read and forbid the retired closure). | ACE team |
| 2026-09-17 | **Step 4j gains sub-step 6 — capped-index arithmetic (ace#2148).** When a per-entity cap rides in `entity_id` as a clamped counter, the clamp constant is NOT the cap: a `casedb` read is the state BEFORE this submission, so `min(<casedb count>, N)` admits `N + 1` distinct keys and the (N+1)-th mints an index that has never existed, which Connect pays. `spark-facilitator/20260906-2233` shipped a cap of 3 binding at 4 — 28 payable events against a declared `total_cap_per_flw` of 21 — with `validate_app`, `compile_app` and `make_build` all green, the CCZ structurally perfect, and the app internally consistent with its own wrong key; `is_payable` was correctly 0 on the fourth meeting and made no difference, because Connect never reads it. Nothing on this path re-derived the arithmetic, so it surfaced only in `pdd-to-deliver-app-eval`, one Nova build later. The step deliberately does NOT compare the clamp to the cap — both correct spellings are live in this same opportunity five weeks apart and share no constant (`min(<casedb count> + 1, 3)` vs `if(pcts >= 3, 2, pcts)`) — it traces the first `cap + 1` submissions, mechanically via `lib/payable-cap-arithmetic.ts`. Paired with `_app-component-library § payability-scoped-key` CAPPED INDEX and the released-form backstop in `app-release-qa § Step 4`. *Enforced:* `test/lib/payable-cap-arithmetic.test.ts` + `test/skills/payable-cap-wiring.test.ts`. | ACE team |
| 2026-09-17 | **Step 4f gains step 8: EVERY lookup-backed select in the app is audited, not just the ones 4f bound (ace#2143).** On `spark-facilitator/20260906-2233` `app-deploy` could not upload the Deliver app — Nova's `upload_app_to_hq` preflight refused it: *"A lookup-powered choice list uses activity_id for its saved values, but malawi_activities repeats the same value in several rows."* The table carried `other` on seven rows, one per FCAP step: unique WITHIN each filter partition (`step_id = step`, so a worker never sees two at once) and not unique across the table, which is what Nova requires. ACE owned the uniqueness rule already — `diffOptionRegister` has carried it since ace#1621 — but only on the PARTNER-REGISTER path, where the PDD names a register file in `inputs/`. `malawi_activities` was authored by the build itself, so that path never fired; and 4f's per-field verify was unreachable too, because steps 1–7 only ever touch a field that FAILED an assertion and this one shipped as a correctly-shaped `single_select` from the start. Every ACE artifact recorded it as "BOUND and read-back-verified" and Nova's preflight was the first thing in the run that noticed — after a full Nova build, media coverage and two translation layers. **The fix is scope, not a second copy of the check.** Nova's preflight sweeps every lookup-powered choice list in the app, so ACE's does too: `auditLookupBinds` over one site per bound field, run unconditionally, including when `degraded` is empty and when no register is declared. `verifyLookupBind` now takes the bound table's ROWS as a **required** argument (an optional one is a check a caller skips by forgetting) and refuses `duplicate-values`, `empty-table`, `no-rows-read-back` and `partial-rows-read-back` — the last because `get_lookup_table_rows` pages at 100 rows and a duplicate on an unread page is invisible. It also splits `bindLanded` out of `verified`, so `scripts/probe-nova-fixtures.ts` keeps reporting on Nova's BINDING capability and never reads a table-content finding as an upstream regression. *Enforced:* `test/lib/option-register.test.ts` (the seven-row `other` repro, blank-value collision, absent/partial/empty rows, and a whole-app sweep whose only failure is an architect-built site the run never bound). | ACE team |
| 2026-09-11 | **Every build-memo `[ACE]` latitude and `[FIXED]` ambiguity is also a `decisions.yaml` row (ace#2384, regression of #399).** § Decisions Log was a catalogue "not a required set" and the app build wrote none — 61 and 66 rows on the two poverty-graduation runs, none from Phase 3, while Step 7's memo listed four latitudes in prose. The rows derive from the same entry list as the memo tables ("one source, two renderings"); the spot-check location goes in `reasoning` because ace-web's summary drops unknown keys. The Phase 3 boundary now fails a memo with entries and no rows under this skill's tag. *Enforced:* `lib/build-phase-decisions.ts` via `verify_phase_artifacts`, `test/lib/build-phase-decisions.test.ts`, `test/skills/build-phase-decision-rows.test.ts`. | ACE team |
| 2026-09-11 | **Step 7 names the Deliver build-memo section `## Build memo`, with `[ACE] latitudes taken` and `[FIXED] ambiguities hit` sub-tables (ace#2371).** Steps 3–4n direct notes "into the build memo" throughout, but the memo had no fixed home: on `poverty-graduation/20260908-0510` it existed as a section headed "Deliver app — build memo" inside this summary, not named as a memo and never linked to a reviewer. `skills/build-memo` now collates this section into the run's programme memo at the end of Phase 4; the section content itself is unchanged. | ACE team |
| 2026-09-06 | **Step 4k records WHAT it diffed against — a derived extraction is no longer indistinguishable from the published source (ace#2110).** 4k's premise is that its oracle is UPSTREAM of ACE; its own text says "read the SOURCE, never the Nova brief and never the PDD's restatement: both are model-authored, and one of them is the artifact this step exists to test." It named two model-authored intermediates and was blind to a third — an EXTRACTION of the workbook, published into `inputs/` as the instrument. `resolveInstrumentSource` proceeded on the mere existence of a manifest entry, with no inspection of mime type, name or provenance, so on `poverty-graduation/20260905-1345` the check resolved a `text/markdown` "(official, extracted verbatim)" file, diffed the build against it, and reported `mismatches: 0` — a fidelity check that compared ACE to ACE, while the publisher's workbook sat in a DIFFERENT opportunity's inputs (`hh-poverty-targeting`, folder `official-nigeria-ppi-2020 (povertyindex.org)`). Sibling of #1648 and its exact inverse: that one is the *unresolvable* branch taking a silent skip, this is the *resolvable-but-wrong-artifact* branch where no branch fires and the run reports green. **Disclosure, not a gate** — a derived source still PROCEEDS, because on that run it was the only instrument artifact in the frozen inputs and halting would block a build over a file that is very likely correct. What changes is what the run may CLAIM: `classifyInstrumentArtifact` ties go to `derived` (under-claiming costs a memo line; over-claiming reports a published-source check that never happened), the memo carries the caveat verbatim, and Step 7 gains `artifact_class`. The point is that a derived check is real but **unfalsifiable** — an error in the extraction is reproduced faithfully by the build and the diff still reads clean. *Enforced:* `test/lib/instrument-constants.test.ts` (positive control is the real poverty-graduation entry; negative controls cover a derivation pasted into a spreadsheet, an unknown container, and a published PDF). | ACE team |
| 2026-09-28 | **ACE-direct edits move into Nova private work (`voidcraft-labs/commcare-nova#693`, deployed 2026-09-27).** Every mutation in Steps 4a–4l now takes `work_id` + `request_id` (no `app_id`) and is staged (`saved: false`) until `save_work`; a stale/refused save is returned as data, so the skill requires `saved: true`, saves before every read-back, and reads back with `app_id`. Step 4f: `create_lookup_table` commits to the Project immediately but the bind is staged — it is now saved before `verifyLookupBind` reads it back, so an unsaved bind can no longer pass as verified while HQ receives the unbound field. Step 4 treats an architect report that names a `work_id` with pending changes as an incomplete build. `no-starter-module` premise corrected (new apps start empty). Contract: `playbook/integrations/nova-integration.md § The private-work authoring contract`. | ACE team |
| 2026-09-06 | **Step 4f's partner-register handoff is RETIRED — ACE builds, binds and PROVES the register (ace#1886).** `voidcraft-labs/commcare-nova#545` closed COMPLETED 2026-09-02 and `scripts/probe-nova-fixtures.ts` returned `both` on 2026-09-06: a select accepts a `{kind:'lookup'}` options source and `get_field` reads it back. All three routes were confirmed live — `add_fields optionsSource`, `set_field_options_source` on an existing select, and `edit_field` converting a `text` field (`set_field_options_source` refuses a `text` field outright, so the conversion is not optional). So 4f now extracts, creates, populates AND binds, and `renderRegisterCsv` is deleted along with the operator step it existed for. **The halt is narrowed, not dropped:** it still fires on an undeclared register (Phase-1 gap), an unreadable declared source, any `diffOptionRegister` finding, and — new — a bind that does not VERIFY. That last one is the point. `add_fields` answers a correctly bound lookup field with `"options": []` and no mention of the source, so the write response cannot distinguish a landed bind from a missing one in either direction; only a `get_field` read-back can, via `verifyLookupBind`. An unverified bind is the ace#1621 defect wearing a better disguise — the select renders empty to a worker while every ACE artifact reports the register shipped. *Enforced:* `test/lib/option-register.test.ts` (`verifyLookupBind`, positive + four negative controls), `test/scripts/nova-fixtures-probe.test.ts`. | ACE team |
| 2026-09-02 | **New Step 4n — derived-chain guard check (ace#1823).** The released `hh-poverty-targeting` Deliver form guards ONE node of its derived PPI chain and leaves twelve unguarded at form root. `/data/roster` is gated on consent, so on a vacant / refused / no-eligible-respondent visit `count()` over the empty nodeset returns 0 and the form submits `member_count = 0`, `hh_size_band = 'le3'`, `size_points = 31` — the 31-point band, by construction, on **1,072 non-payable doors of 3,794** (28%), on the exact field the PDD's Layer-C band-boundary fraud control groups on. `ppi_score` IS guarded (`if(visit_outcome = 'completed', …)`), which is why it survived: nothing looks wrong at the score level and the corruption sits one layer down. A `calculate` over an empty nodeset is valid XForm, so `validate_app`, `app-release-qa`, install, play and submit all pass. Phase 7 blanked the chain in the fixture and declared the deviation — the app still ships this way, so a real deployment would too. 4n runs `lib/derived-chain-guard.ts` over the Step-4a field list: taint PROPAGATES along the chain (guarding the leaf or the final score is not enough), and a conditional whose TEST reads only tainted fields is not a guard — `if(member_count <= 3, 'le3', …)` is the corruption wearing an `if()`. A finding clears by applying the payable path's own discriminator OR by a recorded justification, because a zero over an empty nodeset is sometimes exactly right; what the check forbids is silence. Placed before 4m so every structural check stays ahead of the language layer. *Enforced:* `test/lib/derived-chain-guard.test.ts` (negative control: a naive detector that ignores the inline-guard shape fails 3 assertions, incl. flagging the correct `ppi_score`) + `test/skills/deliver-l0-loop-integrity.test.ts`. | ACE team |
| 2026-08-27 | **Step 4l gains sub-step 7 — the corrected taxonomy propagates to the CASE-LIST ENUMS (ace#1688).** 4l steps 3-4 repair the FORM's option labels via `edit_field` and stop there, while 4l's own trigger (step 1) names a *case-list column* as a surface the taxonomy reaches. On `spark-facilitator/20260820-0817` the Phase-3 FCAP correction landed on the form itemsets and never on the enums, so the `fcap_community` tile rendered the earlier ACE-invented taxonomy while the form offered Spark's real one — stored `1` read as `1. Introduction` before the visit and `1. Planning` during it, off by one on the surface the Learn app explicitly teaches the worker to read (`m3_start`, quiz `q9`). **ACE does not author these enums — the autonomous architect does**, via `add_case_list_columns` / `configure_case_list`'s `kind: 'id-mapping'` column, whose `mapping` the caller supplies; it composes them from the brief independently of the itemset and nothing reconciles the two. Those atoms ARE available ACE-direct (Step 4d already uses the family), so the reconciliation lands here rather than as an upstream Nova issue: derive `mapping` from the itemset, `update_case_list_column`, re-assert, bounded 3-iteration loop. A SUBSET is allowed (a tile may deliberately label fewer options); reconciling the other way is forbidden — the itemset is the authority. Paired with the downstream gate that makes it falsifiable rather than aspirational: `app-release-qa § Step 4` check 3 halts with `[BLOCKER]` `case-list-enum-drift`. *Enforced:* `lib/ccz-enum-fidelity.ts` + `test/lib/ccz-enum-fidelity.test.ts`, whose negative control is the shipped drift itself and must FAIL. | ACE team |
| 2026-08-26 | **Step 4k's skip is split, and its source is resolvable through the manifest's own folder ids (ace#1648).** 4k's trigger ANDed "the PDD marks an instrument `[FIXED]`" with "`inputs-manifest.yaml` carries a source file for it" into ONE silent skip, so *nothing to check* and *the thing I must check is unreachable* were indistinguishable and both reported green. They were not equally rare: `inputs[]` records direct child FILES only, so a published instrument bundle sitting in a SUBFOLDER of `inputs/` — the natural shape for a vendor download — always took the second branch. On `hh-poverty-targeting/20260824-1404` the workbook sat in `official-nigeria-ppi-2020 (povertyindex.org)/` and none of the five `inputs[]` entries was it, so a 4k run following its documented path checks nothing. **A skip that disables a correctness check is worse than one that degrades an output, because the run still says green.** Two changes: step 2 may now resolve through ids the manifest ALREADY records (`subfolders_not_listed[].folder_id`, `source_folder_id`) by walking them ONE level with `drive_list_folder` — walking a recorded id is not guessing, composing a path by name still is and is still forbidden — and orchestrator Step 5c now MANDATES recording those ids. Step 1's trigger is split: no `[FIXED]` instrument → skip cleanly; a `[FIXED]` instrument whose source does not resolve → **HALT**, never a skip. The decision is delegated to `resolveInstrumentSource` in `lib/instrument-constants.ts` so it is unit-tested rather than prose-only. *Enforced:* `test/skills/instrument-source-resolution.test.ts` (5 assertions red against the pre-fix text), `test/lib/instrument-constants.test.ts`, `test/mcp/gdrive/generate-inputs-manifest.test.ts`. | ACE team |
| 2026-08-24 | **Step 4f gains a partner-register halt (ace#1621).** 4f's halt was scoped to payment correctness — a still-degraded select halts only when it `feeds_entity_id` on a PAYABLE deliver unit — so a field that fails neither test recorded an `option_source_gaps` entry and proceeded. That is right for a genuinely unknowable set and wrong for a register that EXISTS: on `spark-facilitator/20260820-0817` the meeting-activity repeat shipped 11 ACE-authored placeholders identical on all 24 FCAP steps while Spark's own 78-activity register sat in the run's `inputs/`, and the recorded gap deferred the catch to an operator reading the residual days later. When the PDD declares `<field> from <tag> [source: …] [filtered by …]`, an inline invented option list is now a **HALT** whatever the payability status, and is never dischargeable as a named gap; both inline rungs of the step-5 escape ladder are withdrawn for such a field. Mechanical via `lib/option-register.ts` (`parseRegisterDeclaration` + `diffOptionRegister`), sourcing rows from the partner's `.ccz` fixture XML in preference to a prose guide because a production CCZ carries the REAL value codes the partner's M&E joins on. Where ACE cannot finish, the terminal behaviour is extract → build the table → halt naming the remaining operator step. *(Both reasons recorded for this halt have since been overtaken. The 2026-08-24 reason — a missing create atom — was superseded 2026-09-01, when `create_lookup_table` proved to ship columns and rows atomically. The 2026-09-01 replacement reason — a refused BINDING, `voidcraft-labs/commcare-nova#545` — was itself superseded on 2026-09-06, when that issue closed COMPLETED and the bind was accepted and read back live. Neither is a current constraint; see the 2026-09-06 row.)* Paired with `_app-component-library § partner-option-register` and the eval's `option_register_fidelity` hard-gate. *Enforced:* `test/lib/option-register.test.ts`. | ACE team |
| 2026-08-23 | **New Step 4l — entity state-taxonomy fidelity (ace#1564).** The followed entity's state model lived only as PROSE in the PDD's § Entity Lifecycle, and nothing in Step 3's brief-composition checklist asked for it — while `longitudinal-visits` REQUIRES a case list showing state, so the architect must name every state and invents the set when the brief carries none. On `spark-facilitator/20260820-0817` the PDD's `1 = Planning (steps 1–14)` … `4 = Transition (steps 23–24)`, sourced from Spark's own published FCAP guide sitting in the run's `inputs/`, shipped as four invented labels over a different partition, with all 24 step names invented too. Learn then teaches one mapping while Deliver offers another, and the invented words reach real workers and the partner. Step 3 now emits `_app-component-library § entity-state-taxonomy` (always for this archetype) and parses `program_parameters.entity_state_taxonomy` with `parseStateTaxonomy` BEFORE briefing — `declared: false` or non-empty `problems` is a **HALT** with a Phase-1 finding, never a licence to invent; where the row names a source document the brief is composed from THAT file out of `inputs/`. 4l then diffs the built option set with `diffStateTaxonomy`: any invented, dropped, relabelled or re-partitioned state is a **HALT with a bounded 3-iteration repair loop**, not a warn. Deliberately ships NO canonical vocabulary — hard-coding one would impose ACE's words on every partner, the mirror image of the defect. Paired with the eval's `entity_state_fidelity` hard-gate. *Enforced:* `test/lib/entity-state-taxonomy.test.ts` + `test/skills/entity-state-taxonomy-component.test.ts` + `test/skills/deliver-l0-loop-integrity.test.ts`. **The language layer moved 4l → 4m** in the same change: it must stay LAST of the 4x steps because every English-editing step has to precede it, and 4l's repair loop calls `edit_field` on option labels — running it after the layer would demote those translations to `out-of-date`. Pointers updated in `_app-component-library § app-language-layer`, both `-eval` change logs, and `test/skills/app-language-layer.test.ts`. | ACE team |
| 2026-08-20 | **New Step 4k — fixed-instrument constant fidelity (ace#1527).** Nothing on this path opened the `[FIXED]` source instrument in `inputs/` and diffed it, so on `hh-poverty-targeting/20260819-1435` the digitised Nigeria PPI 2020 shipped with **9 of 17 point values wrong and all 101 poverty-likelihood values invented** — and every gate passed it, because each one is structurally blind to a constant's VALUE (`validate_app` checks structure, the eval grades against a narrative PDD, `app-release-qa` checks counts and install-time behaviour, and the architect transcribes from a model-authored brief). 4k resolves the source file from `inputs-manifest.yaml`, fetches it with `drive_download_binary` + `writeToPath`, and runs `lib/instrument-constants.ts`: `assertExtractionTrusted` FIRST (endpoints + strict monotonicity + row count — the first repair-round extraction produced `score 4 -> 79.0` from an undecoded `t="s"` shared-string index), then `diffScoringConstants` and `compareMaxScore` over the built literals read via `get_field`. Any mismatch, or a `clampDead` verdict, is a **HALT with a bounded 3-iteration repair loop**, not a warn — a built max of 96 against an official 102 made the PDD's `min(ppi_score, 100)` clamp dead code, which is how the instrument stayed internally consistent with its own wrong numbers. Paired with `_app-component-library § fixed-instrument-transcription` and the eval's `fixed_instrument_fidelity` hard-gate. *Enforced:* `test/lib/instrument-constants.test.ts` + `test/skills/deliver-l0-loop-integrity.test.ts`. | ACE team |
