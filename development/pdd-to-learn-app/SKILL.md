---
name: pdd-to-learn-app
description: >
  Internal /ace:run step — Build the Learn (training) app from the PDD via Nova.
user-invocable: false
disable-model-invocation: false
---

# PDD to Learn App

Generate the Learn (training) app from the PDD using the Nova plugin
(`voidcraft-labs/nova-marketplace`, slash command `/nova:autobuild`).

## Inputs

Pipeline-only: builds a new Learn app from a run's approved PDD. To change a live app, use `app-modify`.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `1-design/idea-to-pdd.md` | source PDD; archetype + Learn App Specification drive the Nova brief |
| Phase 1 (componentized only) | `run_state.…idea-to-design.products.components[]` + `.program_level[]` | the component set and the program-level Learn PDD — see Step 0 |

## Products

- `3-commcare/pdd-to-learn-app_summary.md` — Learn-app structure summary (modules, forms, fields, `nova_app_id`), ending with a `## Build notes` section (Step 7a: language layer, repairs applied, per-item assessment table, recorded check outcomes)
- `decisions.yaml` rows (`phase: 3-commcare`, `skill: pdd-to-learn-app`) — one per `[ACE]` latitude taken, per `[FIXED]` ambiguity hit, and per framework gap (Learn PDD §6(5)), appended in Step 7a (§ Decisions Log). The decisions log is the run's review artifact; these rows are the ONLY place those calls are recorded. REQUIRED: the Phase 3 boundary fails this skill if it wrote its summary but zero rows under `skill: pdd-to-learn-app` (ace#2384)

## Terminology — every string a worker sees

App name, module and lesson titles, lesson text, quiz questions, option labels and feedback text are
reader-visible, and [`skills/_terminology.md`](../_terminology.md) binds them. In particular **US
spelling, always** (owner, 2026-10-20, no carve-out for worker-facing labels): "The program and the
four items", "enrollment", "organization" — never "programme", "enrolment", "organisation", even when
the PDD, the partner or the country uses UK English (connect-fi/20261018-1440 shipped the lesson "The
programme and the four items" — ace#3232). Translations are the target language's own; the rule binds
the English source. **Never respell an identifier** — question ids and case properties keep their
spelling, and the Nova prompt cue "CommCare Connect markers" is a code-level phrase that stays as
written.

## Process

0. **Componentized programme? Plan the modules before briefing Nova.**

   If `products.mode` is `componentized` (set by Phase 1's Step 0 — see
   `skills/idea-to-pdd`), the Learn app is **not** built from one PDD. It is
   foundations plus one module per component, and the two sets below are NOT
   the same set:

   ```
   planLearnModules({ components, activeComponentIds, frameworkComponentIds, referencedAbsentIds })
   // lib/learn-module-plan.ts
   ```

   **Where each argument comes from — all four are read, none is composed:**

   | Argument | Source |
   |---|---|
   | `components` | `products.components[]` |
   | `activeComponentIds` | the model's selection; omit for the first-programme default |
   | `frameworkComponentIds` | `products.framework_component_ids` — **and nothing else** |
   | `referencedAbsentIds` | `products.unresolved_references[].to` |

   `framework_component_ids` is absent when no document in the input set
   declared the framework's inventory. That is a legitimate state: pass
   `undefined` and let the plan emit its `inventory-unavailable` gap. **Do not
   substitute anything for it** — not the framework document's prose component
   table, not a `absent_components` list read out of `component-set.yaml`, not
   a list you assemble from the components you can see. Phase 1 owns that value
   (`skills/idea-to-pdd` § Step 0a.6); a value invented here is the parsed guess
   the plan exists to refuse, and it reports as fact (ace#2056).

   - **BUILT** — a module for every component that HAS a PDD, all present in
     the one app.
   - **SHOWN** — foundations plus only the modules for this model's active
     components; the rest are built and gated off.

   `built ⊇ shown`. For a first programme they are equal, which is exactly why
   collapsing them is tempting — and how a later programme silently loses the
   gating and ships every module to every worker. Brief Nova from `modules[]`,
   and carry `shown` into the gating; scope both assessments to
   `questionBankScope`, never to the built set. *An FLW is tested on what they
   will actually deliver, not on hidden modules* (Learn PDD §4).

   Read each module's content requirements from that component's OWN PDD
   (`modules[].pdd_file_id`), not from the programme overview — the overview
   composes, it does not restate.

   **Record the plan's gap notes (the `buildMemoNotes` field, which keeps its
   legacy name) as decision rows in Step 7a — one `learn-gap-<slug>` row per
   gap.** Learn PDD §6(5) requires naming every framework component skipped
   for having no PDD. When the framework's inventory is unavailable the plan says so
   explicitly rather than reporting none — do not quietly drop that line, and
   do not substitute a parsed guess at the component list.

   If `products.mode` is `synthesized` or absent, ignore this step entirely and
   continue at Step 1. That is every opp before `poverty-graduation`.

1. **Read the PDD** from `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md` via Google Drive MCP.

1a. **Archetype check — focus-group uses the sentinel pattern.** If the
    PDD's `Archetype:` is `focus-group`, this skill still produces a
    Learn app, but a **minimal sentinel** — a single 1-form readiness
    check, not a full training curriculum. It satisfies the
    `connect_create_opportunity` non-null `learn_app` requirement AND
    gates whether the facilitator has completed the out-of-band training.
    Proceed to step 2 with the focus-group sentinel brief described in
    `## Archetypes § focus-group` below. For the sentinel rationale + the
    out-of-band training model, see reference.md § focus-group sentinel
    rationale.

    For `multi-stage` PDDs, follow the multi-stage branch below — each
    stage's Learn app shape depends on the stage's declared archetype.

2. **Extract the Learn app spec** from the PDD. The spec drives the Nova
   brief; what to extract depends on `archetype:` (see `## Archetypes` below).

2a. **More than one worker role in one opportunity? Never role-gate a
    `connect.learn_module` form (ace#3036).** Connect computes Learn
    completion over **every** `learn_module` in the app, whoever can see it.
    Observed on `kaduna-graduation/20261015-1411` (real device + Connect,
    2026-10-16): the Learn app held 14 `learn_module` markers, 9
    display-gated to `#user/kgrad_role = 'FLW'` and 5 to `'enumerator'`. An
    FLW finished all 9 of hers and passed the assessment, then
    `connect_get_learn_progress` read `modules_completed_pct: 64.3` (9/14),
    `learn_complete: false`, and Deliver stayed locked. A role-gated Learn
    app cannot be completed by **any** single role.

    When the PDD names more than one worker role who will claim this one
    opportunity (FLW + enumerator, worker + supervisor, …):

    1. **No display condition on any `learn_module`-bearing form or on the
       module that holds it** — not on a user property (`#user/<role>`),
       and not on anything else. This also covers the assessment form:
       every worker must be able to reach it.
    2. **How the programme restructures its training is the owner's
       decision, not this skill's.** The ways out are: one opportunity
       per role, **each with its own Learn app AND its own Deliver app** —
       Connect allows only ONE active opportunity per Learn or Deliver app
       id (activating a second raises `app_reused`, and every submission is
       routed by app id — read in source, ace#3036: `dimagi/commcare-connect@c7409bd35:commcare_connect/opportunity/forms.py:375-385`,
       `…/form_receiver/processor.py:616-643`), so "one opportunity per
       role" on shared apps is not an option; every role completes every module; or
       `learn_module` markers only on a shared core, with role-specific
       teaching in unmarked forms. Do not pick one as the answer. Record
       the choice as a decision row (§ Decisions Log), id
       `learn-gap-multi-role-learn-completion`, with
       `review_ask: required-before`, `needed_by: go-live`,
       `owner: dimagi` (or the design owner as the reader knows them),
       `answer_channel: review`, and a `confirm_reason` that cites the
       9/14 evidence in plain words.
    3. **Build on the safe default until it is answered: every module is
       visible to every worker, and every worker completes every marked
       module.** It is the only shape this skill can build that Connect can
       complete, and the other options start from it. Role-specific
       modules may say who they are mainly for in their title ("For
       enumerators: …") but stay visible and marked. Put this paragraph
       **verbatim** into the brief, prefixed `REQUIRED:`:

       > REQUIRED: This programme has more than one worker role, but every
       > worker completes the SAME Learn app. Do NOT give any module or
       > form a display condition, including on a user property such as
       > `#user/<role>`. CommCare Connect counts every form carrying
       > `connect.learn_module` toward Learn completion, so a module a
       > worker cannot see means that worker can never complete Learn and
       > never unlocks Deliver. A module mainly for one role may say so in
       > its title, but it must stay visible to everyone.

    4. **The assessment's pass label must never promise the work app
       opens** ("You may now open your work app", "you can start
       delivery") unless every `learn_module` in the app is reachable by
       the worker reading it. Kaduna's label promised exactly that to an
       FLW who could reach 9 of 14 modules. Under the safe default the
       pass label should say what is true: the assessment is passed, and
       the work app opens once every module is complete.

    *Enforced:* `pdd-to-learn-app-eval § 5b learn_module_display_gating`
    (blueprint, hard deduction) and `app-release-qa § Step 4`
    `learn-module-display-gated` (released CCZ, `lib/learn-module-display-gating.ts`).
    The same helper reads the Nova blueprint BEFORE deploy —
    `checkLearnModuleDisplayGatingFromBlueprint({modules})`, each `get_module`
    with its forms' `get_form` `connect` block merged in — so a gate is caught
    at build time, not after release. And the PDD-level rule fires on day 1:
    `idea-to-pdd-qa § platform_constraints` (`learn_module_visibility`).
    A single-role PDD skips this step.

3. **Compose a Nova brief** — a single natural-language description that
   `/nova:autobuild` consumes as its sole argument. Nova does not accept
   file paths or markdown attachments; whatever Nova needs to build the
   right app must be inline in the description string. The brief should:
   - Open with the app's purpose and target FLW persona (1–2 sentences)
   - State the archetype framing explicitly (e.g. "this is a facilitation
     training app, not a form-walkthrough app")
   - **Explicitly state this is a CommCare Connect Learn app and that
     every content form needs `connect.learn_module`, and the GATING
     quiz form needs `connect.assessment`, per CommCare Connect's rules.**
     Load-bearing language — without it, autobuild often skips the
     per-form Connect blocks. For why, see reference.md § Connect-marker
     language is load-bearing.
   - **REQUIRED — exactly ONE form carries `connect.assessment` when the
     PDD declares one gate. A diagnostic pre-test must NOT carry it**
     (ace#1205). Connect stores a single `passing_score` per learn app and
     every "has this worker passed?" surface uses **any-passed** semantics
     (ace#1131), so a second scored form does not become a second gate —
     it becomes an ALTERNATIVE gate, and since a pre-test is by
     construction the easiest instrument in the app, it becomes the one
     that unlocks Deliver. Insert this paragraph **verbatim** into the
     brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Only the FINAL gating assessment may carry a
     > `connect.assessment` block. If you build a diagnostic pre-test, it
     > MUST NOT carry `connect.assessment` — score it with an ordinary
     > hidden `user_score` field and conditional result labels, but leave
     > the Connect marker off. Connect stores one passing score per learn
     > app and treats a pass on ANY marked form as satisfying the gate, so
     > a marked pre-test silently becomes the easiest path to unlocking
     > Deliver, whatever the pre-test's own on-screen text says about not
     > counting.

     `pdd-to-learn-app-eval § 5b single_gating_assessment` is the
     structural backstop; it reads the blueprint and `[BLOCKER]`s a second
     marked form. Healable at L0 with one `configure_connect` call —
     **REPLACE-ALL, so resend the complete participant set**.
   - Describe each module / form, in order
   - List the required Connectify fields (Learn Module, Assessment Score)
   - Reference the relevant PDD section when it shapes Nova's choices
   - **REQUIRED — Forbid angle-bracket placeholder notation in
     label/option/hint text.** Insert this paragraph **verbatim** into
     the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Do NOT use literal `<` or `>` characters in any form
     > label, option label, hint text, constraint message, or itext
     > value. Nova's XForm emitter does not entity-encode `<`/`>` in
     > label text, so a literal "<3 letters>" or "<number>" placeholder
     > becomes invalid XML when CCHQ parses the form during
     > `make_build` (CCHQ rejects with "Error parsing XML: StartTag:
     > invalid element name"). Use words ("three letters", "a number")
     > or backticks (`three letters`) for placeholder syntax. `&` is
     > NOT restricted: Nova entity-encodes it to `&amp;` and HQ builds
     > it, so keep a partner's published name verbatim, `&` included
     > (verified against a released build, ace#2150). This applies especially
     > to pattern-recognition / regex-style quiz options where it's
     > tempting to write `<country><number>.<number>` literally.

     For the upstream filing + the `app-release` Step 2.7 backstop, see
     reference.md § Angle-bracket placeholder ban.
   - **REQUIRED — Set `connect.learn_module.id` AND `connect.assessment.id`
     explicitly to short stable identifiers, separately from the human-
     readable `name`.** This is the load-bearing constraint; the ≤40-char
     name fallback below is just a safety net. Insert this paragraph
     **verbatim** into the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Every `connect.learn_module` and `connect.assessment`
     > block MUST include an explicit `id` field. The id is the Connect
     > slug — it MUST be short (8-20 chars), lowercase, snake_case, code-
     > like, and stable across renames of the human-readable name. Examples:
     > `m1_background`, `m6_sample_prep`, `m1_quiz`. Do NOT rely on Nova's
     > default derivation (`module_<index>_<slugify(name)>`) — that
     > conflates the Connect slug with the display name and trips Connect's
     > 50-char `LearnModule.slug` column on any name that slugifies past
     > ~40 chars. The `name` field is a separate, human-readable string
     > that can be any length and any character set — that's where the
     > descriptive title belongs. Vellum-authored apps (the human-driven
     > authoring path in HQ's form designer) separate these into two UI
     > fields ("Module ID" and "Name") and humans naturally pick short
     > identifiers; Nova's API exposes the same two fields but the
     > architect has to set both explicitly because there's no UI to
     > nudge the separation. See `docs/learnings/2026-05-17-connect-slug-length-50-char-trap.md`
     > § Generalization (Vellum-as-source-of-truth) for the full mechanism
     > + source citations.

   - **REQUIRED — `connect.learn_module.time_estimate` is in HOURS, not
     minutes.** Insert this paragraph **verbatim** into the brief, in its
     own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: The `connect.learn_module.time_estimate` field is the
     > estimated time to complete the module in **HOURS**, not minutes.
     > Nova's tool-schema description for this field says "Estimated
     > minutes" — that description is WRONG (stale; filed upstream as
     > voidcraft-labs/nova-plugin#36). Do not follow it and do not flag
     > the conflict — this instruction is the resolved answer, confirmed
     > against Connect's rendering source end-to-end (2026-07-30,
     > dimagi-internal/ace#1077): Connect's model help_text says
     > "Estimated hours to complete the module"
     > (`commcare_connect/opportunity/models.py:297`); the PM dashboard
     > renders the raw value as `f"{value}hr"`
     > (`commcare_connect/opportunity/tables.py:1677-1678`); ingest is a
     > straight `int()` passthrough from the CCZ's `<time_estimate>`
     > element with no unit conversion
     > (`commcare_connect/opportunity/app_xml.py:107-108`, `tasks.py:95`);
     > and the FLW-facing Connect mobile app sums the raw values and
     > renders "Estimated time: %d hours" (commcare-android
     > `ConnectJobIntroFragment.kt:64-77`, plural resource
     > `connect_opportunity_estimated_hours`). Vellum's plugin help text
     > agrees ("Estimated time to complete the module in hours",
     > `src/commcareConnect.js:158`). For typical Learn modules this is
     > 1 (one hour) or 2; never a two-digit minute count. If a module
     > genuinely takes less than an hour, round up to 1. `app-release-qa`
     > structurally asserts every released value is plausible as hours
     > against the PDD's stated module durations
     > (`lib/time-estimate-check.ts`), so a raw minute count halts the
     > release.

   - **REQUIRED — Keep module/assessment names short enough that the
     derived slug fits Connect's 50-char column (FALLBACK).** This is the
     defense-in-depth fallback for cases where the explicit-id rule above
     is missed. Insert this paragraph **verbatim** into the brief, in its
     own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: If you have not set `connect.learn_module.id` /
     > `connect.assessment.id` explicitly per the rule above, the `name`
     > field MUST be ≤ 40 characters as a fallback — Nova's default slug
     > derivation `module_<index>_<slugify(name)>` overflows Connect's
     > 50-char `LearnModule.slug` column on longer names and triggers an
     > opaque HTTP 500 from `connect_create_opportunity`. Prefer the
     > explicit-id rule above (cleaner; lets `name` be any length); this
     > clause exists only because architects sometimes skip the id field.

     For the reproducer, the `app-release` Step 6 backstop, and removal
     criteria, see reference.md § ≤40-char name fallback.
   - **REQUIRED — Architect must verify-then-retry every `add_fields`
     call.** (Since `voidcraft-labs/commcare-nova#693` the architect's `add_fields` stages
     into private work, so the verifying `get_form` reads the CANDIDATE —
     `work_id`, not `app_id` — until its next `save_work`.) Nova's `add_fields` has a partial-persistence quirk: a
     single call with N items often persists only the first few.
     Mid-build sessions where the architect skipped verification have
     shipped forms that look complete in the build summary but render
     with missing questions. Insert this paragraph **verbatim** into
     the brief, in its own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Nova's `add_fields` has a partial-persistence quirk.
     > After EVERY `add_fields` call, count the entries in the result's
     > `fields` array (Nova returns one `{id, uuid}` per field it
     > persisted) against the number you sent. If fewer came back, or
     > the call errored, call `get_form` on that form, re-issue
     > `add_fields` for the missing fields, and re-verify. Repeat until counts match. Do not move on to the
     > next form before counts match — silent partial persistence on
     > form N becomes invisible once you start working on form N+1.

     For the full failure analysis, see reference.md § add_fields
     verify-then-retry.

     Also insert this paragraph verbatim into the brief
     (dimagi-internal/ace#1181):

     > REQUIRED: a large `add_fields` call can fail with
     > `InputValidationError: could not be parsed as JSON`. This is a
     > HARNESS-side failure, not a Nova one, and not a size limit —
     > `commcare-nova#459` was closed NOT_PLANNED on 2026-08-16 after
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
   - **REQUIRED — `user_score` MUST be a PERCENTAGE (0-100), not a raw
     point sum.** Connect's `passing_score` field on each assessment is
     on a 0-100 scale — `passing_score: 80` means "pass at 80%."

     **First resolve `<THRESHOLD>` — it is NOT a constant.** Read
     `run_state.yaml.phases.idea-to-design.products.pdd.program_parameters.learn_passing_score`;
     fall back to the PDD's § Program Parameters table; use **80 only
     when the PDD decides nothing.** That is the same resolution order
     `connect-opp-setup` uses to set the LIVE gate, and it is the skill
     that owns the value — so following it here is what keeps the two
     numbers equal.

     **Why this matters more than it looks (ace#1333).** This skill
     authors the app's ON-SCREEN result experience; `connect-opp-setup`
     independently sets Connect's live gate. If a PDD pins a different
     score and the brief hardcodes 80, the two diverge with **no error
     anywhere** — no build failure, no `validate_app` complaint, no eval
     finding, no read-back mismatch, because each system is internally
     consistent with its own number. The app tells the worker
     **"Passed"** and Connect keeps Deliver **locked**. Live instance:
     `bednet-check-2-visit/20260814-0856`, whose PDD pins
     `learn_passing_score: 100` and argues it (six items scored as a
     percentage, so the reachable scores are 0/17/33/50/67/83/100).

     Insert this paragraph **verbatim** into the brief, in its own
     paragraph, prefixed `REQUIRED:`, substituting the resolved
     `<THRESHOLD>` everywhere it appears:

     > REQUIRED: The `user_score` hidden field on every quiz form MUST
     > compute a PERCENTAGE on the 0-100 scale, NOT a raw point sum.
     > Formula: `(q1_score + q2_score + ... + qN_score) * 100 div N`
     > where N is the total number of scored questions in that quiz.
     > For a 5-question quiz where each `qK_score` is `if(correct, 1, 0)`,
     > the calculate expression is:
     > `(#form/q1_score + #form/q2_score + #form/q3_score + #form/q4_score + #form/q5_score) * 100 div 5`
     > This produces 0 (0%), 20, 40, 60, 80, or 100 (100%).
     > Connect's `passing_score` for this opportunity is
     > `<THRESHOLD>` (= <THRESHOLD>%). With percentage scoring at a
     > threshold of 80, that means "at least 4 of 5 correct" on a 5-Q
     > quiz, "at least 4 of 4" on a 4-Q quiz (rounds to 100, so
     > 3/4 = 75 < 80 = fail, 4/4 = 100 >= 80 = pass), and "at least 7 of
     > 8" on an 8-Q quiz (7/8 = 87.5 >= 80 = pass); at a threshold of
     > 100 every scored item must be correct. Do NOT emit `user_score`
     > as a raw sum (e.g. 4 out of 5) — Connect compares the raw number
     > against `<THRESHOLD>` and the FLW always fails.

     For the reproducer, see reference.md § user_score percentage scoring.
   - **REQUIRED — Learn forms must NOT carry `<case>` blocks.** Connect's
     Learn-app contract is form-only; case state is the Deliver app's
     domain. Insert this paragraph **verbatim** into the brief, in its
     own paragraph, prefixed `REQUIRED:`:

     > REQUIRED: Learn forms must NOT create or update CommCare cases.
     > Do not declare a `case_type` on Learn modules, do not configure
     > registration forms to create cases, and do not bind any field to a
     > case property via `case_property_on`. Calibration scores, pass
     > flags, and assessment `user_score` MUST live as form-level hidden
     > fields only — Connect reads them via each form's `connect.assessment`
     > block, which is the right channel for cross-form Learn signal. If
     > a downstream Deliver-app query needs the FLW's calibration status
     > (e.g. "did this FLW pass the standardization gate?"), the answer
     > comes from Connect's per-FLW assessment-completion API, NOT from
     > a CommCare case property written by the Learn app.

   - **FIRST — check the PDD's assessment spec against the
     known-unbuildable list, and NAME any substitution you make.**
     `idea-to-pdd § Step 4a` gates Phase 1 against
     `_app-component-library.md § Known-unbuildable mechanisms`, so a PDD
     authored on a current plugin should never reach you specifying one. That
     gate landed on **2026-08-13 (0.13.766, ace#1213)** — every PDD authored
     before it, and every PDD carried forward from an older run, predates it.
     This step is the belt-and-braces for exactly those.

     Read the PDD's assessment blueprint against the list before composing the
     brief. The one that actually recurs: **a randomized / per-attempt item
     draw** ("a bank of 24, 12 served per attempt, retakes drawn from unseen
     items"). It is closed twice over — Nova exposes no per-attempt
     item-selection primitive, and decisively, Connect scores against a single
     absolute `passing_score` per app, so a variable-membership draw makes
     `user_score` incommensurable with the gate. Build the sanctioned
     alternative — **one fixed bank sized for the gate**, plus a distinct
     pre-test bank where a baseline is wanted — exactly as you would anyway.

     **The build is not the defect; the silence is.** On
     hh-poverty-targeting/20260812-2034 the PDD specified the 24-item draw, the
     build correctly shipped one fixed 12-item bank, and **nothing recorded
     that a substitution had happened** — so the PDD, and anything generated
     from it, still told a reader that retakes were draw-resistant. Whenever
     you substitute, record it as a `learn-ambiguity-<slug>` decision row
     (Step 7a) and in the summary as a named deviation: what the PDD asked for, what you built, why the ask is closed,
     and the residual the operator now owns (for the fixed-bank case: unlimited
     re-attempts against a fixed bank let a worker pass by memorising the
     answers, which is a real retake-resistance loss the PDD assumed away).
     Never resolve it silently, and never build the unbuildable thing to be
     faithful to the PDD.

   - **REQUIRED — Deployability (fitness) components.** A label-only
     curriculum + one trivial quiz is NOT a deployable training
     instrument; `pdd-to-learn-app-eval` **hard-fails** it. The canonical,
     parameterized text for each component lives in
     **[`skills/_app-component-library.md`](../_app-component-library.md)** —
     the single source of truth, paired 1:1 with the eval dimension that
     hard-fails a build omitting it. For each Learn component whose
     **Trigger** fires, open the library and insert that component's
     **Brief paragraph** into the brief **verbatim**, in its own
     paragraph, prefixed `REQUIRED:`, substituting any `<PARAM>`
     placeholders from the PDD. Emit-checklist (see the library for full
     text + triggers):

     - `nova-authoring-rules` — always (Learn + Deliver). One paragraph of
       the nine refusals and lookups that recur across Nova builds (ace#3300);
       insert it verbatim, do not restate its clauses here.
     - `assessment-gate` — trigger: PDD specifies a readiness /
       competency gate before delivery. (Gate stays Connect-side — Learn
       forms carry no case blocks per the rule above.)
     - `app-language-layer` (Learn variant) — trigger: PDD names a
       working language other than English. The brief tells the
       architect to build the app in **English ONLY** and to call no
       language atom. **ACE owns the language layer**, ACE-direct, in
       Step 4e below — after every English-editing step has finished.
       That split is the fix for ace#1556: the architect's operating
       prompt forbids it saving self-generated target text, so a brief
       that asked it to author translations produced a silent no-op
       (207 units copied, 0 translated, both targets, on
       `spark-facilitator/20260820-0817`). It also makes translate-LAST
       structural — the architect's turn is over before the language
       exists. Never stack languages inline. (Standing decision
       2026-08-17, PR #1463, superseding ace#968/#1391; ownership split
       2026-08-23, ace#1556 — see
       `_app-component-library.md § app-language-layer` for the proven
       contract and the ACE-direct recipe.) Graded by
       `language_conformance`.
     - `learn-app-naming` — always. App name must contain "Learn app".
     - `no-starter-module` — always (Learn + Deliver). Apps created before
       2026-09-27 were seeded with a placeholder module (top-level menu
       "Survey" → form "Survey" → one text field `question_1` labelled
       "Question 1"); since `voidcraft-labs/commcare-nova#693` a new app starts EMPTY
       (`begin_work({new_app})`, no seed), so the component is now a
       regression guard rather than a live defect. Emit the component
       so the brief tells the architect to DELETE it, and to report whether it
       was present. Removal is currently architect discretion, and discretion
       is what varies run to run: on `bednet-check-2-visit/20260828-0629` the
       Deliver app shipped with the seed while the Learn app, briefed from the
       same template in the same phase, removed it unprompted. Enforced at
       release by `app-release-qa § Step 4` (ace#1787).
     - `end-of-form-previous` — always, every form. End of Form Navigation
       must be "Previous Screen".
     - `grid-menu-display` — always (Learn + Deliver), but **do NOT put it
       in the Nova brief**. Nova's authoring surface exposes no
       menu-display-format control at all: `update_app` sets only the display
       name, `create_module` / `update_module` carry no display-format field,
       `set_menu_media` sets icons and audio labels (Menu ICONS are a different thing and ACE does apply them — `app-media-coverage` at Phase 3 Step 1.7, via this same `set_menu_media`, using Nova's built-in topic/action icon slugs.), and `set_case_list_tile`
       lays out a case LIST — unrelated, and inapplicable to case-less Learn
       modules. The component is real and enforced, just not here: it is
       applied POST-BUILD by `app-hq-settings` (Phase 3 Step 2.65) via
       `commcare_set_menu_display` + `commcare_set_app_menu_display`, and
       BLOCKER-gated by `app-release-qa` off the released app's raw doc.
       Briefing it made every architect build report a spurious "unmet
       requirement" in what was then the build memo — the one artifact meant
       to carry REAL deviations, now the decision rows — and invited the architect to reach for an unrelated atom
       to satisfy the paragraph (dimagi-internal/ace#1632; live on
       bednet-check-2-visit/20260825-1310, where Step 2.65 then applied all
       three fields HQ-side on the first attempt).
     - `connect-supported-capabilities-only` — always (Learn + Deliver). Use
       only capabilities that work WITHOUT an HQ feature flag; `commcare_connect`
       is the sole exception. Learn apps are case-less so the case-search trap
       is a Deliver concern, but the budget applies to every build (ace#1195).
     - **PDD worked examples are ILLUSTRATIVE — never bank content**
       (dimagi-internal/ace#1120). When the PDD supplies worked
       assessment items, they model the *required shape*; they are not a
       bank to ship as-is, and the brief MUST NOT tell the architect to
       "ship these verbatim". Author the bank to the
       `discriminating-assessment-items` standard below and treat every
       PDD example as a candidate that must clear the same two gates —
       **hardening or discarding a PDD example is PDD-COMPLIANT, not a
       deviation**, and does not get a `[FIXED]` ambiguity decision
       row. Say so explicitly in the brief when the PDD carries worked
       examples. Live case: `hh-poverty-targeting/20260730-2210` promoted
       the PDD's three worked items into the brief as verbatim
       post-assessment items; all three were then guessed cold by both
       independent blind probes, and the builder had no discretion to
       fix them. If a PDD example survives the gates, keeping it is fine
       — the point is that the decision is the builder's.
     - `discriminating-assessment-items` — any scored assessment.
       **Step 1 is the lever** — before writing any option, name the
       taught RULE the item tests, the MODULE that teaches it, and the
       OPERATION it protects (unpaid visit / blocked form / corrupted
       data); no module named → discard the item. **Step 2 — concentrate
       the bank on COUNTER-INTUITIVE rules**, the taught rules where
       ordinary common sense gives the WRONG answer (a convention that
       reads backwards, a deliberate non-payment, an inclusion rule, a
       named window or threshold). Aim for roughly half the items on
       those and cover every counter-intuitive rule the curriculum
       teaches at least once — that coverage is exactly what
       `pdd-to-learn-app-eval § assessment_rule_coverage` scores.
       **Step 3** — bank independence, ~1 item per rule. **Step 4** —
       option hygiene: no option rejectable on sight. **Do NOT author
       items to be hard for a clever reader** — the eval no longer
       measures that, and for a CHW curriculum most correct answers are
       sensible, so chasing difficulty produces arbitrary trivia that is
       worse training for the cohort (ace#1206; ~500K tokens were spent
       learning this across ace#1014 / ace#1187). The component's
       **pre-release self-check** is mandatory and its per-item table
       (rule, module, operation, counter-intuitive?, independence,
       any-option-rejectable-on-sight) belongs in the summary's
       `## Build notes` (Step 7a).
     - **Randomise the correct-option POSITION independently per item, and
       never rotate through the letters (ace#2061).** Tell the architect this
       explicitly in the brief. "Spread across a/b/c/d" is not enough and is
       what produced the defect: a balanced-but-CYCLIC key (`a,d,c,b`
       repeating) is more predictable than randomness, not less, and clears an
       80% gate at 90% for anyone who notices. *Enforced:*
       `pdd-to-learn-app § 4c step 3b` + `lib/answer-key-pattern.ts`.
     - `instrument-grounded-examples` — the Learn app teaches
       administration of a fixed instrument. Every worked example and
       good/bad pair built from a REAL instrument item, preferring the
       highest coaching-risk items (self-reported consumption over
       observable assets) (ace#982).
     - `entity-state-taxonomy` — the followed entity carries states the
       curriculum names (always for `archetype: longitudinal-visits`).
       **Teach the PDD's declared `program_parameters.entity_state_taxonomy`
       verbatim** — the same values, labels and step ranges the Deliver app
       ships, parsed with `parseStateTaxonomy` from
       `lib/entity-state-taxonomy.ts` before the brief is composed. Where
       that row names a source document, brief from THAT file out of the
       run's frozen `inputs/`. `declared: false` or non-empty `problems` is
       a **HALT** with a Phase-1 finding, never a licence to invent phase
       names. `stateless: true` (row `stateless [source: …]`, ace#2774) is
       a declaration, not a gap: teach no state vocabulary at all. Both apps deriving from the one declaration is what makes
       Learn and Deliver agree; a Learn app taught on an invented mapping
       sends a trained worker to a phase where the step they were taught
       does not exist (ace#1564).

     Do NOT inline-paraphrase these — reference the library so the build
     and `pdd-to-learn-app-eval` stay symmetric. Skip a component whose
     trigger doesn't fire.

   - **App-test economy (always).** Insert the `REQUIRED:` app-test economy
     paragraph from `skills/pdd-to-deliver-app/SKILL.md` Step 3 **verbatim**
     into the brief, in its own paragraph (batch ≤ 8 `actions` per
     `continue_app_test` with `expect`; no re-observing; paged
     `read_app_test` for evidence; re-test only touched journeys; no
     confirm-`get_form` after a save). Same reason: app-test results are
     35–108 KB each with no compact mode (voidcraft-labs/nova-plugin#71),
     and they accumulate in the architect's context for the whole build.

4. **Invoke `/nova:autobuild "<brief>"`.** This is a one-shot autonomous
   build — Nova will not ask clarifying questions. Capture from the
   response:
   - `app_id` — durable Nova handle, written to the summary as `nova_app_id`.
     Since nova plugin v2 the architect builds in private work and saves
     checkpoints; the `app_id` is the one its first successful `save_work`
     returned. **If the report instead names a `work_id` with pending
     changes, the build is UNFINISHED** — unsaved work is invisible to
     `get_app`, upload and compile. Treat that as an incomplete build, not a
     delivered app.
   - Build summary (the architect distinguishes saved configuration from
     behaviour it observed in app-test journeys — keep that distinction)
   - Any warnings Nova emits

   **Every ACE-DIRECT Nova edit below (§§ 4b, 4c, 4e and § Repair mode) is a
   private-work edit** (`voidcraft-labs/commcare-nova#693`; contract:
   `playbook/integrations/nova-integration.md § The private-work authoring
   contract`). Open work on the built app with `begin_work({app_id,
   request_id})`, stage each mutation with `work_id` + a fresh `request_id`
   (never `app_id`), then `save_work({work_id, request_id,
   expected_revision})` using the revision from the latest staged result.
   **Require `saved: true` in the save answer** — a stale or refused save
   comes back as data (`saved: false`), not as an error, and an unsaved edit
   never reaches HQ. Scripted edits use `lib/nova-work.ts` (`NovaWork.begin`
   → `stage` → `save`, which throws unless Nova saved). Every re-assert
   below reads with `app_id` AFTER the save; a `work_id` read shows the
   candidate even when the save failed. All of this completes before
   `app-deploy` uploads the app.

4a. **Post-build field-count verification — runnable recipe (skill-side safety net).**

    The architect-brief language above puts retry-then-verify discipline
    on the architect agent. This step is the skill-side safety net for
    cases where the architect finished short. For the failure history
    behind this step, see reference.md § Step 4a safety net.

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
    $TSX "$ACE_ROOT/scripts/nova-app-lint.ts" --app <nova_app_id> --type learn \
      --snapshot-out "<scratch>/nova-app-snapshot_<app>.json"
    ```

    Ignore the lint's verdict here (Phase 3 Step 1.4 owns the gate) and use
    only the file it wrote. `FRESH`, or the file you just wrote → take the
    uuid map from `nova-app-snapshot.ts --snapshot <file> --outline` (it also
    prints the app's `connect` type) and each form from `--form <formUuid>`;
    **do not call `get_app` or `get_form`** for steps 2–3 below, nor for
    4b step 1–2 and 4c step 1. Any other result (exit 3/4, no file written) → read live as
    written below, never "close enough". **After ANY edit of this app, take a
    new snapshot with the same lint command** before re-reading — the old
    file predates the edit. Reads that verify this skill's OWN write stay live
    (`LIVE_READS`, `lib/nova-app-snapshot.ts`): the `get_form` inside each
    `/nova:edit` prompt, and the post-save `get_app` / `get_form` re-fetches in 4b step 3 and 4c step 3 (each stays live: it proves the save landed).

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
       - Module "Bednet Basics" [uuid b60055c1-…] (case_type: cbf)
         - Form "Lesson 1" [uuid c3deb000-…] (survey, 9 fields)
           - user_score [uuid c3df54f7-…] (hidden)
       ```

       Build `uuids[module][form] -> {moduleUuid, formUuid}` (and the
       per-field uuids) from this ONE response and carry it through the
       rest of the recipe. One lookup beats N. If you only hold a
       semantic name later, `search_blueprint({query, app_id})` resolves
       it — but prefer the map you already have.

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
       Connect-marker `user_score` (the sum the Connect `assessment`
       block reads) that isn't in `persisted_ids`.
       (`validate_app` flags this class as "X references Y which
       doesn't exist in this form" — same shortfall, different
       detection path. Catching it here means we don't ship to
       `validate_app` with a known gap.)

    5. **If `missing ∪ referenced_missing` is empty across every form,
       proceed to step 5 (`/nova:show`).** No edit needed.

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

    Why we run this even though `validate_app` will catch some shortfalls
    downstream: see reference.md § Step 4a safety net.

    Same shape as `app-connect-coverage` — verify+fix in a bounded
    loop, post-Nova.

4b. **Learn-marker compile pre-check (catch a missing app-level Connect
    type before deploy) — runs ACE-DIRECT.** Mirror of
    `pdd-to-deliver-app` § 4e. The autonomous architect
    (`Agent(nova:nova-architect-autonomous)`) can land a Learn app with
    **no app-level Connect mode** even though every form already carries
    its `connect.learn_module` / `connect.assessment` block. The per-form
    `[Connect enabled]` flag is a **FALSE POSITIVE for compile**: with no
    app-level mode the released CCZ ships with ZERO `<learn:module>` /
    `<learn:assessment>` markers, and Connect's HQ→Connect sync cannot
    register the learn module or the assessment gate. `app-release-qa`
    (Phase 3 Step 2.8) catches it post-release, but that is a full
    deploy→build→release cycle too late — assert it here, cheaply, on the
    already-built app.

    1. Read the app's Connect type and complete form list from the § 4a
       snapshot (`--outline`: `connect` + `forms[]` with uuids); no
       `get_app`. Live fallback only when 4a left no `FRESH` snapshot: call
       `get_app({app_id})` — its summary header prints the Connect type
       (e.g. `Connect type: learn`; a standard app prints none) — and **keep
       that response** for its form list and `[uuid …]` markers.
    2. **Assert the header reads `Connect type: learn`.** Do NOT rely on
       the per-form `[Connect enabled]` flag — it is a false positive for
       compile (see above).
    3. On a miss, heal ACE-direct with **`configure_connect`**, which is
       available to the ACE session that executes this skill.
       `update_app` no longer carries `connect_type` — it was removed in
       Nova's 2026-07-31 redeploy (jjackson/ace#1133); `configure_connect`
       replaced it and sets the app-level mode AND every form's Connect
       block in one atomic call.

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
       begin_work({ app_id, request_id })          // → work_id
       configure_connect({
         work_id, request_id,                       // staged — never app_id
         mode: "learn",
         participants: [
           // EVERY content/quiz form in the app, addressed by formUuid.
           { formUuid: "<content form uuid>",
             connect: { learn_module: { name, description, time_estimate } } },
           { formUuid: "<quiz form uuid>",
             connect: { assessment: { user_score: "#form/<user_score field id>" } } },
           …
         ]
       })
       save_work({ work_id, request_id, expected_revision })  // require saved: true
       ```

       Note the **expression shape** — since `voidcraft-labs/commcare-nova#693`
       `user_score` (like `relevant`, `calculate`, `default_value`) is a
       plain expression STRING that names answers as `#form/<path>`; Nova
       binds the reference to the field's stable identity at request time
       and reads return the same text. The 2026-07-31 `{parts: [...]}`
       shape is gone. Omit each block's `id` and let Nova derive it.
       `time_estimate` is in **hours** despite upstream's schema
       description saying minutes (nova-plugin#36).

       Then, AFTER the save, re-run `get_app({app_id})` and re-assert BOTH
       the header and that every form that carried a Connect block before
       still carries one. **This re-fetch stays live** (`LIVE_READS`): it
       verifies this step's own write, which the § 4a snapshot predates.
       **Bounded loop, max 3 iterations.** If the header still does not
       read `Connect type: learn` after the third attempt (or
       `configure_connect` is itself unavailable), halt with a clear
       `learn-marker-wont-compile` failure and do NOT write the success
       summary.

    Use `update_form({work_id, request_id, moduleUuid, formUuid, connect})` **only** to refine
    one sub-config on a form that ALREADY participates — it cannot enable
    Connect, switch mode, or add a participant, and it refuses a
    whole-slot null. Full division of labour:
    `playbook/integrations/nova-integration.md § configure_connect
    replaced update_app({connect_type})`.

    Reproducer: bednet-spot-check/20260615-0702 — the Learn app scaffolded
    with no app-level Connect type; the first released CCZ had `module=0`/
    `assessment=0`; an L0 heal + re-deploy + re-release fixed it to
    `module=1`/`assessment=1`. The fix is this pre-check, NOT a
    `mcp/connect/backends/commcare.ts` change — the compile is correct
    given a correct app-level mode. See jjackson/ace#783. (That heal was
    `update_app({connect_type: "learn"})` at the time; the parameter was
    removed 2026-07-31 and `configure_connect` is now the only path —
    jjackson/ace#1133.)

4c. **Conditional-result-label pre-check (catch the unconditional pass
    message before deploy) — runs ACE-DIRECT.** This is the structural
    preventer for the exact gap `pdd-to-learn-app-eval § assessment_gating`
    hard-fails on: a quiz with an **unconditional** "Well done!" result
    label that fires regardless of score. The brief above (the
    `assessment-gate` component, § Step 3) REQUIRES conditional pass +
    fail/retry labels — but when the brief is hand-composed (e.g. the
    orchestrator executing this skill inline at L0) and the
    `assessment-gate` component paragraph is skipped, the architect emits
    one always-on congratulatory label. The eval catches it, but only
    **after** a full deploy→build→release cycle. Assert it here, cheaply,
    on the already-built blueprint.

    **Trigger:** the PDD specifies a readiness / competency gate before
    delivery (the same trigger that put the `assessment-gate` component in
    scope in § Step 3). If the PDD specifies no gate, skip this step.

    1. For each form carrying a `connect.assessment` block (`--outline`
       lists each form's `connect` keys), read it with
       `nova-app-snapshot.ts --snapshot <file> --form <formUuid>` from the
       § 4a snapshot — no `get_form`. Live fallback only when 4a left no
       `FRESH` snapshot: `get_form({app_id, moduleUuid, formUuid})` (uuids
       from the § 4a step-2 map, or `search_blueprint({query, app_id})`).
    2. **Assert the form has a genuine pass/fail result EXPERIENCE:** at
       least one `label` field whose `relevant` references
       `user_score >= <threshold>` (the PASS message) AND a separate
       `label` field whose `relevant` references `user_score < <threshold>`
       (the FAIL/retry message). A single result `label` with NO
       `relevant` condition (fires unconditionally) FAILS this assertion —
       that is the `assessment_gating` hard-gate trigger.
    2b. **Assert the fail/retry label does NOT contain the correct answer**
       (dimagi-internal/ace#1041). `get_form` returns both the option labels
       and the fail label, so this is a deterministic string check on data
       already in hand — not another adjective. The correct answer is
       whatever literal the scoring `calculate` compares the question
       against (CommCare has no correct-option primitive, so that literal
       IS the answer key). Compare case-insensitively with whitespace
       collapsed; a reworded restatement leaks just as much as a verbatim
       one. On a hit, heal at L0 via `edit_field` to replace the retry text
       with a pointer to the module content, then re-assert.

       A leak makes the gate DECORATIVE while every structural check still
       passes: with no attempt limit, a worker who fails once is shown the
       answer and passes on attempt 2. Live case
       (bednet-spot-check/20260729-0002): `fail_msg` restated the correct
       option verbatim and told the worker to answer again — and the golden
       run it forked from carries the identical leak.

       The released-CCZ backstop is `lib/assessment-retry-leak.ts`
       (`checkAssessmentRetryLeak`), run by `app-release-qa`, which catches
       the class even when this step is skipped — which is exactly what
       happened live, because the brief was hand-composed at L0 and the
       `assessment-gate` component paragraph was never inserted.

    3. On a miss, heal ACE-direct (`edit_field` / `add_fields` are
       available to the ACE session that executes this skill):
       in ONE private work on the built app (`begin_work({app_id,
       request_id})`), stage
       `edit_field({work_id, request_id, moduleUuid, formUuid, fieldUuid, updates})`
       to add a pass condition to the existing pass label, and
       `add_fields({work_id, request_id, moduleUuid, formUuid, fields})` to append a
       `result_fail` label carrying retry guidance (review the content,
       answer again), then `save_work({work_id, request_id,
       expected_revision})` and require `saved: true`. Use `<threshold>` = the SAME resolved value the
       brief used (`learn_passing_score` → PDD § Program Parameters →
       80), never a hardcoded 80 — an on-screen pass label that
       disagrees with Connect's live gate tells a worker they passed
       while Deliver stays locked (ace#1333). Then, after the save, re-fetch
       via `get_form({app_id, moduleUuid, formUuid})` and re-assert — **this
       re-fetch stays live** (`LIVE_READS`): it verifies this step's own write.
       **Bounded loop, max 3 iterations.** If the form still lacks a
       conditional pass+fail pair after the third attempt, halt with a
       clear `assessment-result-unconditional` failure and do NOT write
       the success summary.

    3b. **Check the ANSWER KEY is not periodic (ace#2061).** Extract each
       `qN_score`'s calculate literal — the value the score compares against IS
       the answer key, since CommCare has no correct-option primitive — and run:

       ```ts
       const r = checkAnswerKeyPattern({ key, passMark });  // lib/answer-key-pattern.ts
       ```

       It returns a `CheckOutcome` — **narrow on `r.status` before reading
       `r.ok`.** Three outcomes, and they are three different actions:

       - `status: 'unable'` — the bank has fewer than 2 items, so no period
         fits twice and NOTHING was examined. **This is not a pass.** Record
         `r.reason` in the summary's `## Build notes` verbatim; do not re-key. If a Connect
         gate depends on a bank this short, that is the finding — a 1-item
         gate is guessable for reasons this check does not measure.
       - `status: 'checked'`, `ok: true` — no periodic guess reaches the mark.
       - `status: 'checked'`, `ok: false` — re-key the offending items: move
         the correct option's TEXT to a different position and update that
         item's calculate to match. **Do NOT simply point the calculate at a
         different letter** — that makes a wrong answer correct. **Bounded
         loop, max 3 iterations**, re-running the check after each; if it
         still fails on the third, halt with `assessment-key-periodic` rather
         than re-keying indefinitely.

       It fails when any fixed periodic guess reaches the pass mark, testing
       every phase alignment at every period up to `min(6, floor(n / 2))`.
       **The cycle must fit in the bank at least twice** — a longer "cycle" is
       a transcription of the key, not a pattern (ace#2179). That bound is
       what makes a re-key ACHIEVABLE: at `period <= n / 2` at most 50% of
       items can match by construction, so a finding is always breakable. The
       shipped version tested up to `period === n`, where the cycle IS the
       key, so every bank of 6 or fewer items failed at 100% regardless of
       content and the re-key branch above could never be satisfied —
       seen on `bednet-check-2-visit/20260907-1126`, a 3-item pre-test keyed
       `b,c,a`. *Enforced:* `test/lib/answer-key-pattern.test.ts` § degenerate
       periods (ace#2179).

       Measured on `poverty-graduation/20260905-1345`: a 32-item gate whose key
       ran `c a d b` then `(a d c b)` seven times without deviation. Answering
       that cycle cold scores **29/32 = 90%** against an 80% gate, so the Learn
       gate certified a worker who had read nothing. **The letter distribution
       was perfect — 8 each of a/b/c/d** — which is exactly why no frequency
       check saw it and why this one reads the sequence instead. It is also a
       different mechanism from ace#981 / ace#1014 / ace#1187, which are about
       whether an item is guessable from its WORDING: every item on that build
       had plausible distractors and tested a real taught rule.

    4. **Check what the pass label CLAIMS against what the bank tests
       (ace#1368).** Run `checkPassLabelScope` from
       `lib/pass-label-scope.ts` over the built `result_pass` text, with
       the rules the bank actually keys on and whether the PDD declared
       the gate is not a competence certification:

       ```ts
       checkPassLabelScope(resultPassText, {
         certifiedRules,                 // the rules the bank tests
         declaredNotCompetence,          // from the PDD's residual/deviation
         untestedPaymentPredicate,       // e.g. 'consent_confirmed on the follow-up form'
       });
       ```

       On a finding, rewrite the label to claim only what was examined —
       do NOT regenerate the PDD, and do not widen the bank to justify
       the sentence.

       Live: `bednet-check-2-visit/20260813-2333` built
       **"You can now begin delivery work"** after examining TWO
       payment-model facts, directly contradicting the PDD's own D-1
       residual (*"not a competence certification and must not be
       described as one"*). The PDD wrote the residual honestly; the
       builder wrote a label that violates it, and nothing compared the
       two. **The pass label is what the WORKER reads.**

       That gate also never tests the follow-up **consent
       re-affirmation** — the sole server-side payment predicate
       (`form_field_rules` keys on `consent_confirmed`) — so a worker can
       clear it and still fail the only check that decides whether they
       get paid. Pass that predicate as
       `untestedPaymentPredicate` so the finding names it.

       **`relevant` is an expression STRING that names the score by
       `#form/` path** (since `voidcraft-labs/commcare-nova#693`; the 2026-07-31
       `{parts: [...]}` shape is retired):

       ```
       relevant: "#form/<user_score field id> >= <threshold>"
       ```

       `required`, `validate.expr`, `calculate` and `default_value` take
       the same string form; `label`, `hint` and `help` are Markdown
       strings where `{{field_id}}` inserts an answer. A BARE id in an
       expression (`user_score >= 80`) is now REFUSED with *"Unknown or
       ambiguous reference"* — observed live 2026-09-28 — so the ace#1119
       silent-raw-text failure fails loud instead. Two rules that bite here:
       a **`hidden` field is rejected unless it has `calculate` or
       `default_value`**, and Nova **applies nothing on rejection**
       ("Nothing was changed") while naming the exact problem — so read
       the error and re-call rather than assuming a partial apply.

    Note: the `relevant` expression legitimately contains `<` / `>=`;
    that is an attribute expression Nova entity-encodes at compile, NOT
    label text — the angle-bracket ban (§ Step 3) applies only to
    label/option/hint TEXT, so a `user_score < 80` relevance is fine.

    Reproducer: bednet-spot-check/20260615-1309 — the inline Phase-3 Learn
    brief omitted the `assessment-gate` component paragraph; the architect
    built one unconditional result label; `pdd-to-learn-app-eval` hard-gated
    it (`assessment_gating` 2.0 → overall 6.58 → fail). An L0
    `edit_field`(relevant) + `add_fields`(result_fail) heal + re-deploy +
    re-release + re-eval lifted it to `assessment_gating` 5.0 → 7.29 / warn.
    Sibling run 20260615-0702 (conditional labels present) scored 7.10 / warn
    — the single dimension is the whole swing on this minimal opp. See
    jjackson/ace#787.

4d. **(Retired 2026-08-13 — no build-time cold-read probe.)** A measured
    cold-read probe briefly lived here: two dispatched agents on a PDD-derived
    FLW persona, stems and options only, blocking the build when the untrained
    reader cleared the PDD's unlock threshold. It was removed the day after it
    landed, together with the eval-side contrast it fed
    (`pdd-to-learn-app-eval § assessment_discrimination` → now
    `§ assessment_rule_coverage`).

    **Why:** the probe's untrained reader is an LLM told to role-play a
    low-literacy CHW, and an LLM's floor is its own competence, not the
    persona's — it still reads English fluently, does the arithmetic, and
    eliminates options. For a CHW curriculum, whose taught rules are largely
    "record what happened, honestly", the protected population's proxy passing
    cold is the EXPECTED result for a well-built bank, not a catastrophe. The
    filter fired on `spark-facilitator/20260812-1635` — a build with complete
    trilingual coverage, worked examples from the real instrument and correct
    conditional gating — and the only way to clear it would have been to
    author arbitrary trivia, which is harder to learn and less useful in the
    field. No ACE bank has ever been put in front of a real CHW, so the
    LLM→CHW inference was never validated. See ace#1206.

    **What replaced it:** the same question, asked structurally. Rather than
    simulating a reader, `pdd-to-learn-app-eval § assessment_rule_coverage`
    audits which taught rules the bank keys on and whether the
    **counter-intuitive** ones — where common sense gives the WRONG answer —
    are covered. That answers "is this bank mostly common sense?" from the
    artifact, with no persona, no dispatched agents and no run-to-run noise,
    and it returns `repairs[]` naming the specific items to re-key (see
    § Repair mode below). Do not reinstate a persona probe here without
    reading ace#1206 first.
4e. **Language layer — runs ACE-DIRECT, LAST of the 4x steps (ace#1556).**
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
    English-editing step (4a–4d, and any `repairs[]` pass) is already done, so
    nothing can demote a translation to `out-of-date` behind you.

    Execute `_app-component-library.md § app-language-layer` **ACE's ACE-direct
    recipe** verbatim — `get_languages` → `add_language` (ISO 639-3 identity, `copyFrom: {language: 'eng'}`) →
    page `get_translatable_content` and author real values via
    `update_translations` (≤50 units/call, echoing each just-read
    `sourceFingerprint`) → `get_languages` again. `add_language` and
    `update_translations` are STAGED private-work mutations (`work_id` +
    `request_id`); read `get_translatable_content` with the same `work_id` so
    fingerprints match the candidate, then `save_work` and require
    `saved: true` — the gate below reads `get_languages({app_id})` AFTER
    that save, because unsaved translations ship nothing. Read the atoms'
    live schemas from Nova's `tools/list`; do not paraphrase them here.

    **Gate:** `out-of-date` and `missing` must both be 0 at hand-off. Record
    the final per-language coverage counts in the summary's `## Build notes`
    (Step 7a), plus one line
    stating the translations are ACE-authored (`origin: ai`) and carry
    `needs-review` until a speaker of the language reviews them. If the layer
    cannot be completed, halt loud with the counts — do NOT write a summary
    claiming a language layer the app does not carry. Partial coverage is the
    false affordance the issue was filed about: units left `origin: copied`
    are English strings wearing the language's name, and a worker cannot tell
    them apart from real translations.

5. **(Optional) Inspect the built app** via `/nova:show <app_id>` to
   cross-check the structure against the PDD before writing the summary.

6. **Exit gate — `nova-app-lint` must exit 0, then self-evaluate.** Run
   `scripts/nova-app-lint.ts --app <nova_app_id> --type learn` (invocation in
   `agents/commcare-setup.md § Step 1.4`) on the SAVED app. It checks in code
   the app name, post-submit navigation, the Connect-marker floor (≥1
   `learn_module`, each with name + time_estimate; EXACTLY one
   `assessment` with a `user_score`), learn-module display gating (ace#3036 —
   any role-gated `learn_module` form blocks: Connect counts every module, so
   no single role can complete), casedb preloads and the starter module. Fix
   every `[BLOCKER]`, save, re-run; never edit for a `[WARN]` (record it in
   `## Build notes`). Quote its first line in `## Build notes`. Then:
   - Does the app structure match the PDD Learn spec?
   - Are all required Connectify fields configured (Learn Module,
     Assessment Score, passing score)?
   - For `focus-group`: does the app actually teach facilitation craft
     rather than form completion?

7. **Write the summary** to
   `ACE/<opp-name>/runs/<run-id>/3-commcare/pdd-to-learn-app_summary.md`. Required
   frontmatter:

   ```yaml
   ---
   nova_app_id: <id-returned-by-autobuild>
   # `/build/`, NOT the legacy `/apps/` route, which 404s (ace#1431).
   # Built by `novaAppUrl()` in `lib/nova-url.ts` — the single source.
   nova_app_url: https://commcare.app/build/<id-returned-by-autobuild>
   archetype: <atomic-visit | longitudinal-visits | focus-group | multi-stage>
   # Addressing map — Nova is uuid-addressed (2026-07-31, ace#1132).
   # Persist what § 4a step 2 already read so downstream steps and the
   # -eval rubrics address by uuid without re-resolving. One lookup at
   # build time beats N lookups later.
   nova_uuids:
     modules:
       - name: <module name>
         uuid: <moduleUuid>
         forms:
           - name: <form name>
             uuid: <formUuid>
             # Only the fields later steps address directly (the
             # assessment score field, result labels). Not every field.
             fields:
               user_score: <fieldUuid>
   # Componentized runs ONLY (Step 0): the component ids this app built a
   # module for — `learnComponentsBuilt(plan)` from lib/commcare-products.ts
   # over Step 0's `planLearnModules` result. app-deploy copies it into
   # products.apps.learn.components_built (ace#2157). Omit on the synthesized
   # path. Never spell it `components_covered`.
   components_built: [<component_id>, ...]
   ---
   ```

   Body content stays the same as before: module list, Connect
   configuration, decisions made, Nova warnings — ending with the
   `## Build notes` section Step 7a specifies.

   Anything downstream that lost this map can re-derive it with one
   `get_app({app_id})` (whole-app) or `search_blueprint({query, app_id})`
   (one semantic name) — but persist it here so they don't have to.

7a. **Record the build's calls as decision rows, and its notes in the
   summary.** **On every path**, not only the componentized one, immediately
   after Step 7's summary write. The decisions log (`decisions.yaml`, schema
   v6) is the run's review artifact: ace-web renders every row with a comment
   box and an answer editor, and an answer carries into the next run. A call
   that is not a row is not in front of the reviewer — on
   `poverty-graduation/20260905-1345` and its fork `20260908-0510` the
   latitudes taken during authoring were held only in the build's context and
   lost with it, so the post-hoc summary had to record that they "cannot be
   established".

   **Decision rows** — ONE `decisions_append_rows` call (§ Decisions Log):

   - **`[ACE]` latitudes taken** — one `learn-latitude-<slug>` row per place
     the build exercised latitude the PDD granted.
   - **`[FIXED]` ambiguities hit** — one `learn-ambiguity-<slug>` row per
     `[FIXED]` statement that could not be built exactly as written
     (including a substituted unbuildable ask — Step 4's fixed-bank case —
     and any `repairs[]` entry that could not be satisfied, § Repair mode).
   - **Framework gaps (Learn PDD §6(5))** — on a componentized run, ONE
     `learn-gap-<slug>` row per gap in Step 0's plan notes (the
     `buildMemoNotes` field): each framework component skipped for having no
     PDD and, when the framework's inventory was not declared, a
     `learn-gap-inventory-unavailable` row that says so rather than reporting
     none. When only the design owner or operator can close a gap (author the
     missing component PDD, declare the inventory), set
     `review_ask: recommended-confirmation` with a `confirm_reason` naming who
     closes it and how. A synthesized run writes no gap rows.

   Cite the PDD section in every row's `source`.

   **`## Build notes`** — the last section of Step 7's summary
   (`3-commcare/pdd-to-learn-app_summary.md`), each subsection present even
   when empty (write `None.` — never drop the heading):

   - `### Language layer` — Step 4e's final per-language coverage counts and
     the `origin: ai` / `needs-review` line, or `No working language other
     than English.`
   - `### Repairs applied` — § Repair mode's per-item table and which
     `repairs[]` entries were applied, or `None.`
   - `### Assessment self-check` — the `discriminating-assessment-items`
     per-item table, plus any `checkAnswerKeyPattern` `unable` reason,
     verbatim.

   **`## Build notes` is internal, and it is the ONLY place the built answer
   keys go** (dimagi-internal/ace#2869). This summary is also indexed into the
   FLW support chatbot's knowledge base (`ocs-agent-setup` § Step 5), whose
   audience is the workers these assessments gate. That path drops
   `## Build notes` whole and redacts any key-shaped line elsewhere
   (`scripts/redact-kb-answer-keys.ts`), so a key written under the module
   list or the Connect configuration would cost that section a line rather
   than leak, but keep keys, correct options and `qN_score` literals here.

   The Phase 3 boundary fails this skill if it wrote its summary but zero
   decision rows carry `skill: pdd-to-learn-app` (ace#2384).

8. **Notify admin group** that Learn app generation is complete, with the
   Nova app URL and a link to the summary in GDrive.

## Repair mode — consuming a `repairs[]` work order

`pdd-to-learn-app-eval § assessment_rule_coverage` does not just score the
assessment; when the bank leaves a taught rule untested it returns a typed
`repairs[]` list naming the uncovered rule, the module that teaches it, and a
`suggested_target` item to re-key. The orchestrator dispatches THIS skill to
apply them — the judge never repairs the bank it grades, because a grader that
authors its own fix and re-scores it converges on passing itself.

When invoked with a `repairs[]` list:

1. **Re-key, don't grow.** For each entry, edit the `suggested_target` item in
   place via `edit_field` (and `set_field_options_source` when the options
   change) — staged in one private work on the app and saved with
   `save_work` (require `saved: true`) before step 3's read-back, which
   uses `app_id`. Keep the stem's subject where you can; change what the options
   *differ on*, so the answer turns on the uncovered rule rather than on general
   judgment. Adding items instead of re-keying inflates the bank and lowers the
   effective bar the gate applies.
2. **Preserve the invariants.** Every edited item keeps: an English source
   stem AND options (`app-language-layer` — repairs edit the English, which is
   the source language), no option rejectable on sight, no literal `<` / `>` in
   label text, and a `qN_score` whose calculate references the question as
   `#form/<id>` — a bare id persists as raw text with no error and silently
   breaks the scoring chain (ace#1119). **If the app carries a working
   language, every repaired string's translation is now `out-of-date` and
   falls back to English** — re-run § Step 4e (the ACE-direct language layer;
   never the architect, ace#1556) for the repaired units and re-confirm
   `out-of-date` is 0 before hand-off.
3. **Read back the scoring chain.** After any pass that rewrites options or
   keys, `get_field({app_id, …})` (after the save) on the edited `qN_score`
   and on `user_score` and assert each `calculate` string still references
   the question as `#form/<id>` — reads return the authored text, e.g.
   `"if(#form/q1 = 'c', 1, 0)"`.
4. **Update the summary's `## Build notes` per-item table** (Step 7a) for
   every item you touched, and record which `repairs[]` entries you applied.
5. **One round, then re-lint.** Run `scripts/nova-app-lint.ts --type learn`
   on the saved app (exit 0 required) before returning. A `repairs[]` list is
   only dispatched for a `fail` — never for a `warn` (`agents/commcare-setup.md
   § Step 1.4` repair policy). Return after applying the list; the orchestrator re-runs the
   eval once. Do not iterate against the score — roughly 500K subagent tokens
   were spent across two prior authoring cycles looping against a number that
   could not move (ace#1014, ace#1206).

If a `repairs[]` entry cannot be satisfied — the rule genuinely has no
non-guessable formulation, or re-keying would break a load-bearing teaching
example — say so explicitly in a `learn-ambiguity-<slug>` decision row with
the reason (`review_ask: recommended-confirmation` + `confirm_reason`), and leave the
item alone. An unfixable entry is a finding for a human, not a licence to
fabricate an arbitrary item.

## Archetypes

The Learn app's job depends on the PDD's `archetype:` field. Read it
before composing the brief.

### `atomic-visit`
Learn app teaches FLWs to **collect data** at individual visits. Standard
form-walkthrough Learn app: how to open a case, complete each form field,
what good vs. bad inputs look like (e.g., the photo standardization
protocol from the Evidence Model — Layer A), how to handle edge cases (no
stock, hostile vendor, duplicate), submission and case closure.

### `longitudinal-visits`
Everything in `atomic-visit`, plus the three things an FLW working a case
list has to be taught and a fresh-sample FLW does not:

- **Working the case list** — finding an entity, reading its tile to see
  which visit is due, and what to do when the entity is missing.
- **The sequence** — which visits exist, in what order, at what cadence,
  and how to tell whether a case is on track or behind.
- **What gets paid, given history** — teach the
  `payability-against-history` decision plainly: whether repeating an
  activity on the same entity pays, and what happens if it does not.
  This is the single most expensive thing for an FLW to learn by
  discovering it in a payment statement.

Skip the parts of the `atomic-visit` walkthrough that assume a fresh
subject each time (duplicate-vendor handling, per-day caps) unless the
PDD actually declares them.

### `focus-group`

**Produce a minimal sentinel Learn app** — one module, one form, ~7
fields, both Connect markers (`connect.learn_module` +
`connect.assessment` with passing_score 1). It satisfies the
`connect_create_opportunity` non-null `learn_app` requirement AND is a
coordinator-confirmed in-app readiness gate. For the rationale, see
reference.md § focus-group sentinel rationale.

**Sentinel app spec (the Nova brief):**

- **App name:** `"<Opp display name> — Facilitator Readiness Check"`
  (e.g., "Malaria ITN FGD — Facilitator Readiness Check").
- **One module:** "Readiness Check" (case_type: `facilitator`).
- **One form:** "Briefing Acknowledgement" (case-create form,
  `connect.learn_module` set AND `connect.assessment` with
  `passing_score=1` and `user_score: #form/user_score`).

Fields (the complete sentinel form):

1. `intro` (label) — out-of-band training overview pointing the
   facilitator at the per-opp OCS chatbot + the LLO's handbook gdoc +
   the practice-session audio review the coordinator grades.
2. `case_name` (hidden, calculate `concat(#user/username, ' - readiness')`).
3. `acknowledge_readiness` (single_select yes/no, required, constraint
   `. = 'yes'` — the facilitator must answer `yes`, i.e. coordinator-
   confirmed practice-session-pass). Saves to case property
   `readiness_acknowledged`.
4. `acknowledgement_date` (date, required, default `today()`). Saves
   to `readiness_date`.
5. `q1_score` (hidden, `calculate: if(#form/acknowledge_readiness = 'yes', 1, 0)`).
6. `user_score` (hidden, `calculate: #form/q1_score`). Referenced by
   the `connect.assessment` block.
7. `result_label` (label) — readiness-acknowledged closing message.

The sentinel **does not duplicate or replace** the out-of-band training.
It's a thin in-app artifact whose only operational job is to gate
attestation submissions on coordinator-confirmed practice-session-pass.
The real facilitator training (OCS chatbot + handbook gdoc + coordinator-
graded practice-session audio review) lives out-of-band. For where that
training lives, the "why sentinel and not real training" rationale, and
the full archetype redefinition spec, see reference.md § focus-group
sentinel rationale.

### `multi-stage`
Generate one Learn app per stage that has its own delivery work,
branching on each stage's archetype. If only Stage 2 involves FLW
delivery, only that stage gets a Learn app. The Stage Gate from the PDD
determines whether Stage 2 training launches before or after Stage 1
results.

## MCP Tools Used

- **Google Drive MCP:** `drive_read_file`, `drive_create_file`
- **ACE decisions MCP:** `decisions_append_rows` (Step 7a — § Decisions Log)
- **Nova plugin slash commands:** `/nova:autobuild`, `/nova:show`,
  `/nova:list`, `/nova:edit` (for follow-up tweaks)

The Nova plugin is installed separately
(`/plugin install nova@nova-marketplace`) and signs in via OAuth on first
use. ACE does not call Nova MCP tools by name; it invokes the user-facing
slash commands listed above. See
`playbook/integrations/nova-integration.md` for current status.

## Mode Behavior
- **Auto:** Build via `/nova:autobuild`, write the summary (with
  `## Build notes`) and the decision rows, notify admin, proceed.
- **Review:** Build, write summary, present summary for review before
  proceeding.

## Dry-Run Behavior
When `--dry-run` is active:
- Do NOT call `/nova:autobuild` (Nova builds are durable side effects;
  a dry run that creates a real app would clutter Nova's app list).
- Write the composed brief and the intended Nova invocation to
  `comms-log/dry-run-pdd-to-learn-app.md` (recipients: nova / brief /
  expected Connectify fields).
- Do not write `app-summaries/learn-app-summary.md` (no `nova_app_id`
  to record).
- Do not call `decisions_append_rows`; list the rows you would append in
  the same dry-run comms-log.
- State tracks as `dry-run-success`.

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. Every framework gap the build hit (§6(5)) is a row too, with `review_ask: recommended-confirmation` when only the design owner or operator can close it. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes to the per-run `ACE/<opp-name>/runs/<run-id>/decisions.yaml`
— the register ace-web renders on the public run page, where a reviewer
comments on and answers each row and the answer carries into the next run.
The bar criterion and schema live in `skills/idea-to-pdd/SKILL.md § Decisions
Log Convention` (canonical authority). Until ace#2384 this skill had no
Decisions Log section at all, and the Learn build wrote zero rows:
`poverty-graduation/20260905-1345` and `20260908-0510` carried 61 and 66 rows,
none from Phase 3 — including the quiz item count, which was derived rather
than read (ace#2364). A regression of #399.

### Every latitude, ambiguity and framework gap is a decision row (REQUIRED)

Every `[ACE]` latitude taken, `[FIXED]` ambiguity hit and framework gap
(Learn PDD §6(5)) the build met is a `decisions.yaml` row — and the row is the
ONLY rendering; nothing else lists these calls. They are exactly the calls the
register exists for: an `[ACE]` latitude is an `inferred` default, a `[FIXED]`
ambiguity is a `conflicting` one, and a framework gap is a value outside the
build's authority that the design owner or operator must close.

Build each row from one entry —
`{pdd_section, kind, chose, alternatives, why, spot_check, signals}`.

| Row field | From the entry |
|---|---|
| `id` | `learn-latitude-<slug>` / `learn-ambiguity-<slug>` / `learn-gap-<slug>`; slug from the PDD § and the subject, so a re-run of the same PDD re-derives the same id and the atom's idempotent skip holds |
| `phase`, `skill` | `3-commcare`, `pdd-to-learn-app` |
| `question` | what the PDD left open (latitude), said two ways (ambiguity), or needs and the build could not supply (framework gap) at that § |
| `ai-default` | what ACE chose / how the ambiguity was resolved / how the build proceeded without the gap closed, as a short label, an exact member of `options` |
| `options` | that label plus each alternative the build weighed, 1–8 words each |
| `source` | the entry's PDD §, naming the document |
| `evidence_basis` | `[ACE]` latitude → `inferred` (`stated` only when the PDD itself names the value chosen); `[FIXED]` ambiguity → `conflicting`; framework gap → `inferred` |
| `conflict_signals` | ambiguity only, at least 2 entries: the `[FIXED]` statement as written, and the reading or constraint that competed with it — each cited |
| `value_set_by` | `ace` |
| `status` | `ai-default`, always (a caller-asserted `human-decided` is rejected — ace#2307) |
| `reasoning` | why; an ambiguity left OPEN begins `OPEN —`; it ends `Spot-check: <where>.` |
| `plain` | REQUIRED — one plain-language line for a programme partner (no §-refs, field ids or ACE tags) |
| `check_at` + `correct_looks_like` | where in the Learn app a reviewer sees the choice, and what they see there when it is right (the atom fills `check_at` from the `Spot-check:` sentence if omitted) |
| `review_ask` + `confirm_reason` | framework gap (and an unsatisfiable `repairs[]` entry) that only the design owner or operator can close → `recommended-confirmation` + one plain sentence naming who closes it and how. `OPEN` rows get their ask derived by `decisions_enrich`; do not duplicate it. **Exception:** `learn-gap-multi-role-learn-completion` (Step 2a) is `required-before` + `needed_by: go-live` + `owner` + `answer_channel`, because no default is safe past go-live without the owner's restructuring choice |

**Keep the `Spot-check:` sentence at the end of `reasoning`** even when you
set `check_at`: `reasoning` renders as the row's note, and the write boundary
derives `check_at` from it when a producer omits the field. End it with
`Spot-check: <app> › <module> › <form> › <field>.`

**The boundary checks it.** `verify_phase_artifacts(phase='commcare')`
returns a `decisions` report (`lib/build-phase-decisions.ts`). If this skill
wrote its summary (`3-commcare/pdd-to-learn-app_summary.md`) but zero rows
carry `phase: 3-commcare` and `skill: pdd-to-learn-app`, the Phase 3 boundary
fails; it also warns on any live partner-facing row with no `plain`. Rows
another skill writes in the same phase (`app-test-cases`) do not count toward
this one. A build that genuinely took no latitude and hit no ambiguity or gap
still owes at least one row — record the most consequential build choice
(e.g. the assessment item count) so the reviewer has something to confirm.

Worked example (illustrative values):

```
decisions_append_rows({
  runFolderId: <run-folder file_id>,
  opportunity: <opp-slug>,
  run_id: <run-id>,
  rows: [
    {
      id: "learn-latitude-quiz-item-count",
      phase: "3-commcare",
      skill: "pdd-to-learn-app",
      question: "Learn PDD §5 sets a pass mark but no item count — how many items does the final quiz carry?",
      "ai-default": "10 items",
      options: ["10 items", "5 items", "one per taught rule"],
      source: "Learn PDD §5 [ACE]",
      status: "ai-default",
      evidence_basis: "inferred",
      plain: "The final quiz has 10 questions.",
      check_at: "Learn app › Final quiz",
      value_set_by: "ace",
      reasoning: "Ten keeps one item per taught rule at the stated pass mark. Spot-check: Learn app › Assessment › Final quiz."
    },
    {
      id: "learn-ambiguity-module-per-component",
      phase: "3-commcare",
      skill: "pdd-to-learn-app",
      question: "Learn PDD §1 and §2 disagree on whether every framework component gets a module — which did the build follow?",
      "ai-default": "components this programme carries",
      options: ["components this programme carries", "every framework component"],
      source: "Learn PDD §1 and §2 [FIXED]",
      status: "ai-default",
      evidence_basis: "conflicting",
      plain: "The training has a lesson for each part of the framework this programme uses, not for every part.",
      check_at: "Learn app › module list",
      conflict_signals: [
        "Learn PDD §1 [FIXED]: a training module per component, all present",
        "Learn PDD §2 [FIXED], 1 Sep edit: modules only for the components this programme carries"
      ],
      value_set_by: "ace",
      reasoning: "OPEN — both statements are [FIXED]; built to the later §2 edit and flagged for the design author. Spot-check: Learn app › module list."
    },
    {
      id: "learn-gap-savings-group-component",
      phase: "3-commcare",
      skill: "pdd-to-learn-app",
      question: "Learn PDD §6(5): the framework's savings-group component has no PDD — what does the training carry for it?",
      "ai-default": "no module until a PDD exists",
      options: ["no module until a PDD exists", "module from the overview only"],
      source: "Learn PDD §6(5)",
      status: "ai-default",
      evidence_basis: "inferred",
      plain: "The training has no lesson on savings groups yet, because that part of the programme has not been designed.",
      check_at: "Learn app › module list",
      correct_looks_like: "No savings-group lesson appears in the module list.",
      review_ask: "recommended-confirmation",
      confirm_reason: "Only the design owner can add the savings-group design; until then workers are not trained on it.",
      value_set_by: "ace",
      reasoning: "Learn PDD §6(5) requires naming every component skipped for having no PDD. Spot-check: Learn app › module list."
    }
  ]
})
```

The rejection is atomic — one row whose `ai-default` is not in its `options`
costs the whole batch — so check each row before sending. If the atom is
unbound this session, hand-write per `skills/idea-to-pdd/SKILL.md § Schema and
write semantics` (top-level `decisions:`, not `rows:`).

## Change log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-16 | **Step 6 opens with the `nova-app-lint` exit gate; a repair round re-lints and never runs on a warn.** App name, post-submit navigation, the Connect-marker floor (exactly one assessment), learn-module display gating (ace#3036) and preloads are checked in code on the saved app before return — the kaduna Learn blueprint (`56057841-…`) lints FAIL with 14 display-gating blockers, the defect the eval passed. *Enforced:* `test/lib/nova-app-lint.test.ts`. | ACE team |
| 2026-10-16 | **Step 2a: never role-gate a `connect.learn_module` form when one opportunity carries more than one worker role (ace#3036).** Connect computes Learn completion over every `learn_module`; `kaduna-graduation/20261015-1411` gated 9 modules to FLWs and 5 to enumerators, so an FLW who passed read 9/14 = 64.3%, `learn_complete: false`, Deliver locked, under a pass label promising the work app opens. The build now keeps every marked module visible to every worker, puts the restructuring choice to the owner as `learn-gap-multi-role-learn-completion` (`required-before`, `needed_by: go-live`), and the pass label may not promise the work app opens unless every marked module is reachable. *Enforced:* `pdd-to-learn-app-eval § 5b learn_module_display_gating`, `app-release-qa` `learn-module-display-gated` (`lib/learn-module-display-gating.ts`), `test/skills/learn-module-role-gating-rule.test.ts`. | ACE team |
| 2026-10-03 | **Build memo retired — decisions.yaml is the review artifact (schema v6).** Step 7a no longer writes `3-commcare/pdd-to-learn-app_build-memo.md`: `[ACE]` latitudes, `[FIXED]` ambiguities and every framework gap (`learn-gap-<slug>`, with `review_ask` + `confirm_reason` when only the design owner can close it) are decision rows only, and the language layer, repairs applied and assessment self-check move to a `## Build notes` section of the summary; the Phase 3 boundary now fails a summary with zero rows under `skill: pdd-to-learn-app`. Contract: docs/decisions-contract.md. | ACE team |
| 2026-09-28 | **ACE-direct edits move to Nova private work (`voidcraft-labs/commcare-nova#693`).** Nova's 2026-09-27 deploy removed `create_app` and made every mutation staged: `work_id` + `request_id`, no `app_id`, nothing lands until `save_work`, and a refused save answers `saved: false` as data. §§ 4b / 4c / 4e and § Repair mode now open work, stage, save (requiring `saved: true`) and read back with `app_id` after the save; Step 4 treats an architect report naming unsaved work as an unfinished build; `no-starter-module` is re-framed as a regression guard (new apps are unseeded). Contract: `playbook/integrations/nova-integration.md § The private-work authoring contract`. | ACE team |
| 2026-09-11 | **Added § Decisions Log: every build-memo `[ACE]` latitude and `[FIXED]` ambiguity is also a `decisions.yaml` row (ace#2384, regression of #399).** The skill had no Decisions Log section, so the Learn build contributed zero rows to the register a reviewer comments on and answers — 61 and 66 rows on the two poverty-graduation runs, none from Phase 3. Rows derive from the same entry list as Step 7a's tables, with the spot-check location in `reasoning` because ace-web drops unknown keys. The Phase 3 boundary now fails a memo with entries and no rows. *Enforced:* `lib/build-phase-decisions.ts` via `verify_phase_artifacts`, `test/lib/build-phase-decisions.test.ts`, `test/skills/build-phase-decision-rows.test.ts`. | ACE team |
