---
name: idea-to-pdd
description: >
  Internal /ace:run step — Develop and stress-test the run's PDD from source material.
user-invocable: false
disable-model-invocation: false
---

# Idea to PDD

Take an initial idea and iterate on it to produce a complete Program Design Doc (PDD) that specifies a Connect application.

## Inputs

Pipeline-only: authors a run's PDD from that run's frozen `inputs-manifest.yaml`; designing a program is a build. To change a live program, use `partner-on-connect-program`.

| Source | Artifact | Used for |
|---|---|---|
| Operator | `ACE/<opp-name>/runs/<run-id>/inputs-manifest.yaml` | frozen pointer-set to source material captured at run-start |
| Operator | each `file_id` in the manifest | source content (PDFs, docs, sheets, markdown) |
| Reviewer | comment threads on the PRIOR run's PDD, via `drive_list_comments` | what a domain expert asked for IN PLACE, anchored to the section they were reading |
| Reviewer / author | comment threads on every Google Doc / Sheet / Slides entry in the frozen `inputs-manifest.yaml` — a shortcut is read at its `resolved_target_id` — via `drive_list_comments` | what the people maintaining the SOURCE documents asked for in place. On a componentized programme those documents ARE the design, so their threads are the review (ace#2372). Replied to, never resolved — § Process step 1 |

## Products

- `1-design/idea-to-pdd.md` — the PDD
<!-- 0.13.116: legacy `1-design/idea-to-pdd_gate-brief.md` removed.
Pause-time summary at the Phase 1→3 Pause Point is composed by the
orchestrator from the per-skill QA + eval verdicts on the fly. -->

- `ACE/<opp-name>/runs/<run-id>/decisions.yaml` — structured per-run decisions log (always emitted; see `## Decisions Log Convention` below)
- `run_state.yaml.phases.idea-to-design.products.pdd` — `{title, description, file_id}` typed handoff for downstream readers (ace-web summary, future skills) so they don't need to parse the PDD body. This skill is the sole writer. (Pre-2026-05-26: `phases.design.products.pdd` — moved under the actual phase block to satisfy `lib/run-state-validator.ts` which requires every top-level `phases.*` key to be a phase block with `status`; see bednet-spot-check Phase 1 finding.)

### Componentized programmes — two more products

Written **only** when the input set declares components (see Step 0 below);
absent on the single-PDD path, which is every opp before `poverty-graduation`.

- `1-design/component-set.yaml` — the machine-readable component handoff.
- `run_state.yaml.phases.idea-to-design.products` — gains `mode`, `components[]`,
  `program_level[]`, `overview_obligations[]`, `unresolved_references[]` and
  `framework_component_ids` (the framework's FULL component inventory, when a
  document declares one — see Step 0a.6).
  Shape and guards: `lib/component-products.ts`.

**`products.pdd` is still written, and still required.** It points at the
programme OVERVIEW rather than at a synthesized design: which components are
on, the shared case-and-state model, how they compose, and what each downstream
phase should read per component. 17 places read `products.pdd` directly, so a
componentized run does not null it — and an overview that is only a pointer at
the components is not enough, because a build needs enough to execute:

> *"we must have enough information to execute everything downstream from the
> initial inputs or we can't really proceed anyways meaningfully. So the
> programme overview doc needs to explain how to use the components."*
> — Jon, 2026-09-05

## Standing design assumptions (operator directive — do not re-open per run, except by an operator ruling)

Two things are ASSUMED true for every ACE design. They are not open
questions, not go/no-go gates, not risks, and not solicitation asks
(standing operator directive, Jonathan 2026-09-26: *"smart phones and data
can always be assumed by ACE, as well as designed for this to be the system
of record (reality may always be different but you don't need to worry
about that)"*):

1. **Every FLW has a smartphone that runs Connect, with a data connection,
   and can complete PersonalID sign-up.** Do not raise device or
   connectivity availability in `## Open Questions`, the launch-readiness
   check, § Risks, or as a decision row's review ask — even when the
   inputs describe offline-first tooling for the same workforce. A partner
   input that says otherwise is recorded as context, never escalated.
2. **The Connect app is the SYSTEM OF RECORD for the work it records.**
   Design it to replace, not sit alongside, whatever the partner uses today
   for that same record. Do not ask whether workers file it "instead of or
   in addition to" an existing form, and do not cost or flag double entry.
   Reusing the partner's field paths and value codes is still right — it
   keeps the data comparable — but the pilot record is the one that counts.

Reality may differ; that is for the humans running the programme, not for
the design. If a run's inputs are genuinely about device procurement (the
programme IS a device rollout), that is the programme's subject matter, not
this assumption — design for it as scope.

### Per-opp operator rulings override a standing assumption

The assumptions above hold for every opp **unless an operator has ruled
otherwise for this opp** in `ACE/<opp-name>/inputs/operator-rulings.yaml`.
That file is the ONLY sanctioned override. A partner input that contradicts an
assumption is still recorded as context and never escalated. A reviewer
comment cannot override one either: route it as a ruling request to the
operator.

```yaml
schema_version: 1
kind: operator-rulings
opp: spark-facilitator
rulings:
  - id: devices-costed-separately
    ruling: Devices and data are not assumed for this programme. They are costed separately and the implementing organisation is asked about them.
    overrides: devices-assumed        # or system-of-record; omit for a ruling that overrides nothing
    decided_by: jjackson@dimagi.com
    decided_at: 2026-10-04
    applies_to: [pdd, solicitation, work-order]
```

Schema and helpers: `lib/operator-rulings.ts`. The file is opp-level and
operator-written. ACE never writes it, and a malformed file fails the
decisions write rather than being ignored.

Read it in step 1 alongside the inputs (`resolve_opp_path` → `inputs/` →
`operator-rulings.yaml`; it is absent on most opps). For every ruling whose
`applies_to` includes `pdd`:

1. **Honour it over the standing assumption.** For `overrides:
   devices-assumed`, the PDD states who provides and pays for devices and
   data. It may raise device or connectivity availability in `## Open
   Questions` and § Risks, and as a decision row's review ask. For `overrides:
   system-of-record`, the design may sit alongside the partner's existing
   record as the ruling says.
2. **Record one decision row per ruling**, built with
   `rulingDecisionRow(ruling, { phase: '1-design', skill: 'idea-to-pdd' })`.
   That gives id `pdd-ruling-<id>`, `plain` = the ruling, and
   `feedback_ref: operator-rulings/<id>`. Send it as `status: ai-default`, like
   every row. `decisions_append_rows` stamps `status: human-decided` with the
   ruling's `decided_by` / `decided_at` from the file. This is the same
   attribution path as a reviewer's saved ruling in
   `inputs/decision-overrides.yaml`, because a caller may never assert
   `human-decided` itself (ace#2307). The result reports it in
   `operatorRulingsApplied`. A ref in `operatorRulingsUnmatched` means the
   ruling id is wrong: fix the row, do not drop the ruling.

`solicitation-create` and `pdd-to-work-order` read the same file for their own
`applies_to` values (`solicitation`, `work-order`). Live case: on
spark-facilitator the owner ruled on 2026-10-04 that devices are costed
separately and asked about. *Enforced:* `test/lib/operator-rulings.test.ts`
(fixture `test/fixtures/operator-rulings/spark-facilitator.yaml`).

## Terminology — read before drafting any PDD prose

The PDD is upstream of every app label, lesson title, training artifact and solicitation, and they
quote it verbatim — so whatever spelling and naming it uses ships to workers. Write it to
[`skills/_terminology.md`](../_terminology.md), which binds this skill's output:

- **US spelling, always** (owner, 2026-10-20: *"everything should be US spelling"*, no carve-out for
  worker-facing labels): **program, enrollment, enroll, organization, behavior, center** — never
  programme, enrolment, enrol, organisation, behaviour, centre. This holds even when the source
  material, the partner and the country write UK English: quote a source verbatim only inside a
  quotation, and keep an organization's registered name as registered. connect-fi/20261018-1440's PDD
  carried `programme` x12 and `enrolment` x34, and its apps shipped "Enrol adults" and "Adult
  Enrolment" to workers (ace#3232).
- **`Connect`, never `CommCare Connect`.**
- **Identifiers are not prose** — a case property (`days_to_enrolment`), a decision id or a slug keeps
  its spelling; renaming one is a code change.

*Enforced:* `idea-to-pdd-qa` check `us_spelling` (`lib/us-spelling.ts`) fails a PDD with a lower-case
UK spelling and lists capitalized ones; `test/skills/connect-terminology.test.ts` requires this link.

## Process

0. **Classify the input set FIRST — synthesize or ingest?**

   Everything below Step 1 assumes ACE authors one design from raw material.
   That is the right assumption when the human brings raw material, and the
   wrong one when they bring a design that is already N designs. Deciding which
   is the first thing this skill does, and it is DERIVED from the documents,
   never configured:

   ```
   classifyComponentSet(inputs)   // lib/component-set.ts
   designModeFor(set)             // lib/component-products.ts
   ```

   A document declares itself a component on the metadata line under its title
   — `· Component: 4 of the graduation component set` — or declares
   `· Scope: program-level (cross-component)`. **The convention is the AUTHOR'S;
   ACE reads it and mints nothing.** A filename is NOT evidence: a PDD named
   "… (Component 2)" that declares nothing is reported `undeclared-pdd`, with
   the exact line to add, because promoting whoever named the file into the
   component identity is a guess every later phase then builds on.

   - `mode: 'synthesized'` (no component declared) → **continue at Step 1
     unchanged.** This is the existing path and nothing about it moves.
   - `mode: 'componentized'` → **do not synthesize the component PDDs into one
     document.** Follow Step 0a instead, then rejoin at Step 2 for the
     stress-test, which applies to the overview.

0a. **Ingest, don't synthesize.**

   1. `assessProgrammeReadiness(set, bodies)` (`lib/programme-overview.ts`) —
      returns the obligations the overview must answer, derived from the set
      itself, including one per component that leans on a component this
      programme does not carry. Those are not defects: a programme is a
      SELECTION, and leaving a component out is a legitimate choice. But each
      is a question the build cannot answer alone, and if the overview is
      silent some later phase invents an answer.
   2. Author the **programme overview** as `1-design/idea-to-pdd.md`, answering
      every obligation. It composes; it does not restate. A component's own
      forms, payment grain and training requirements stay in that component's
      PDD, which downstream reads by `components[].pdd_file_id`.
   3. `buildComponentProducts(set, readiness)` (`lib/component-products.ts`) →
      write to `products`. It THROWS on `componentized` with zero components
      rather than hand downstream a run that looks componentized and builds
      nothing.
   4. Write `1-design/component-set.yaml` from the same object.
   5. Report every `undeclared-pdd` finding in the phase summary. Do NOT guess
      the id, and do NOT drop the document silently — an undeclared PDD is a
      one-line fix for its author and an invisible hole in the build otherwise.
   6. **`framework_component_ids` — carry it, never derive it.** When a document
      in the set declares the framework's full inventory on its metadata line
      (`· Components: 1, 2, 3, 4, 5, 5b, 6, …`), `classifyComponentSet` reads it
      and `buildComponentProducts` writes it into `products` under that name. It
      is the ONLY thing Phase 3 reads to satisfy Learn PDD §6(5) — "every
      framework component skipped for having no PDD" (ace#2056).

      Report an `inventory-undeclared` finding in the phase summary the same way
      as `undeclared-pdd`: it is a one-line fix for its author and, left open,
      the Learn build's framework-gap decision rows can only name the components another component
      happens to reference — 3 of 9 on `poverty-graduation/20260905-1345`.

      **Do NOT write the inventory yourself.** Not by reading the framework's
      prose component table, not as a freehand `absent_components` list in
      `component-set.yaml`, not by any other name. The three-way naming that
      preceded this is exactly what left the field with no producer; a value you
      composed here is a guess wearing a typed field's name, and the loud
      `inventory-unavailable` decision row from the Learn build is the correct outcome
      until the author declares it.

   7. **`[FIXED]`-survival and conflict pass — run it on the overview you just
      authored, before the stress-test (ace#2365).** Every component PDD's own
      § 0 says a `[FIXED]` element is implemented exactly and that an ambiguity
      is flagged to a human, never resolved. Composition breaks both quietly:
      on `poverty-graduation/20260908-0510` the overview restated Targeting
      § 6's GPS rule without its `> 200m` threshold, and stated Consumption
      Support § 8's conditional reading of the delivered-and-verified gate as
      fact over Productive Asset § 8's unconditional one.

      ```ts
      import { checkFixedClauseSurvival } from '../../lib/fixed-clause-survival';
      const survival = checkFixedClauseSurvival({
        components,   // [{ component, text, citeAs: ['C5', 'Productive Asset'] }] — every carried component PDD, plain-text export
        composed,     // the overview you just wrote
        stateTerms,   // the shared case-and-state model's state names, when it has them
      });
      ```

      Every `survival.findings` entry is an **open question**, never something
      you resolve: write it as a decision row (`evidence_basis: conflicting`,
      `review_ask: recommended-confirmation`, `conflict_signals` = the clause
      ids and texts the finding quotes) and list it in the phase summary with
      the link to where the author answers it. For `quantity-dropped`, the
      repair you MAY make without asking is to carry the `[FIXED]` clause
      verbatim (or cite it by component and section) — never to pick a value.
      For `possible-conflict`, the overview must name both readings and say
      which one the build follows pending the answer; it must not state either
      as settled. Clauses reported `uncarried` are not findings: the overview
      composes, and the component PDD stays the authority. *Enforced:*
      `test/lib/fixed-clause-survival.test.ts` (the real component PDDs and
      composed overview of that run).

   Design: `docs/superpowers/specs/2026-09-05-multi-component-programmes.md`.

1. **Read source material** for the PDD.

   Phase 1 synthesizes a PDD from whatever the human curated into
   `ACE/<opp-name>/inputs/`. The orchestrator captures a frozen
   pointer-set at run-start as
   `runs/<run-id>/inputs-manifest.yaml`. There is no
   required filename inside `inputs/` — anything goes (PDFs, docx,
   sheets, markdown notes, prior-pass drafts).

   **This skill never fetches source material itself.** Inputs are
   human-curated into Drive, and sourcing is an operator act upstream of
   the pipeline. If the official instrument is behind a login (a PPI/PMT
   portal, a Box-hosted resource page), the operator sources it once per
   `playbook/integrations/external-sourcing.md` — which records the Box
   failure ladder so it isn't re-derived — and drops the file in
   `inputs/`. See dimagi-internal/ace#890.

   **No prior-run questions are passed to you, and you fetch none.** The
   open-questions ledger is retired and nothing reads it (ace#2757). Answers
   a person gave bind from `inputs/decision-overrides.yaml` at the decisions
   write boundary; the orchestrator checks after this phase that no ask the
   previous run left open was dropped (§ Asks are decision rows).

   **Read the reviewer's COMMENTS on the prior run's PDD** — `drive_list_comments`
   on that PDD's `file_id`. ACE publishes the PDD as a Google Doc so reviewers can
   comment on it; those comments are review input exactly like an `inputs/` document.
   Treat each unresolved thread as a requirement to honour or to disposition
   explicitly. Use `quoted_text` to bind a comment to the section it sits on, and
   check that section against the comment before you rewrite it — a comment whose
   `quoted_text` no longer matches anything in your draft is the signature of the
   ace#979 regression class, where a fix was reverted while the disposition table
   still claimed it honoured. `resolved: true` means someone closed the thread in
   Drive, NOT that the build honoured it.

   **A COMMENT IS AN INBOX, NOT A STORE — convert it or lose it.** Every run writes a
   NEW PDD document (`runs/<run-id>/1-design/idea-to-pdd.md` has a fresh `file_id` per
   run — verified: `20260813-1612` is `14RRcWZH…`, `20260819-1435` is `1sKoXbVvEN…`).
   So a comment lives on a document no later run produces. This step reads the PRIOR
   run's PDD, which means an unconverted comment is read exactly ONCE, at run N+1, and
   is gone by N+2 — silently, with nothing reporting the loss. Comments accumulating
   on a superseded document are not a durable review record and must never be treated
   as one.

   So for EVERY comment you read, before the phase ends, carry its substance into
   durable **opp-level** state (which every future run re-reads) and then close the
   thread:

   1. **Write it into the opp's feedback record** — `ACE/<opp>/feedback/<YYYYMMDD>-<reviewer>.yaml`,
      verbatim, per `skills/feedback-ledger`. That file is opp-level and is the ledger's
      denominator, so once an item is there a later run that drops it renders as
      **UNROUTED** instead of vanishing. A comment that never reaches this file is not
      UNROUTED — it is absent, and the ledger cannot accuse what it was never told about.
   2. **Route the substance to its durable home**: a requirement → this run's PDD body
      (and it must survive into every later PDD); a question → a decision row carrying
      `review_ask`, `owner`, `needed_by` and `answer_channel` (§ Asks are decision rows),
      stamped `feedback_ref: <slug>/<item-id>`; a choice → a `decisions.yaml` row, or
      `inputs/decision-overrides.yaml` when the reviewer's answer must bind future runs.
   3. **Reply and resolve** — `drive_reply_to_comment` with `action: 'resolve'`, naming
      WHERE it landed (the record slug + item id, the decision id).
      The thread then becomes an audit trail pointing at the durable record rather than
      being the record. Never resolve a thread whose substance is not yet carried
      forward: that destroys the only remaining copy. **This resolve is for ACE's OWN
      generated PDD only.** A thread on an input document is replied to and never
      resolved — see the next block.

   Do not ask the reviewer to maintain this themselves — deleting a comment once it is
   incorporated, or hand-editing the resolution into the body, is the reviewer doing by
   hand what this step exists to do, and it costs them the audit trail.

   **Read the comment threads on the INPUT documents too (ace#2372).** The step above
   reads one document, the prior run's PDD. On a componentized programme that is the
   wrong document: the component PDDs in `inputs/` ARE the design, their author keeps
   them current through live shortcuts, and she reviews them where she writes them.
   Before this block, no step read comments on anything in `inputs/`. Measured
   2026-09-11: `drive_list_comments` on the Targeting PDD behind
   `poverty-graduation/inputs/` returned **8 unresolved threads** by its author
   (27 Jul – 11 Sep), and no `poverty-graduation` run had read one. They reached the
   predecessor programme only because a human retyped them into a decisions document.

   1. **Which entries.** Every entry in the frozen `inputs-manifest.yaml` whose
      EFFECTIVE mime type is a Google Doc (`application/vnd.google-apps.document`),
      Sheet (`…spreadsheet`) or Slides deck (`…presentation`), the three types the atom
      reads. For a shortcut entry (`mime_type: application/vnd.google-apps.shortcut`)
      the effective type is `resolved_target_mime_type`.
   2. **Call it on the TARGET id, never on the shortcut's own `file_id`.**
      `drive_read_file` follows shortcuts, but `drive_list_comments` does NOT, because
      Drive's comments API does not. Measured 2026-09-11 on the same document: the
      shortcut id `1JXV-mBBh9merO1TYlS47ac5VaJchwKER` returned
      `Error: File not found`, and its target `1u-QzTn1G82n5U5J5txjUFjoNOnlQzGEnmU3B57AcYNs`
      returned the 8 threads. A `File not found` on a shortcut id means you called the
      wrong id; it does not mean the document has no comments. Take the target from the
      entry's `resolved_target_id` (the orchestrator records it at capture, per
      `agents/ace-orchestrator.md` step 5c). If a shortcut entry has none (a manifest
      captured before 5c recorded it), resolve the target with `drive_list_folder` on
      the manifest's `source_folder_id` and read that child's `shortcutDetails.targetId`.
      Do not skip the entry. Replies go to the same target id.
   3. **Same inbox-not-store treatment as the prior-run PDD.** Every unresolved thread
      goes verbatim into the opp's feedback record per `skills/feedback-ledger`
      (`channel: gdoc-comments`, `artifact` = the input document's name, `artifact_url`
      = the target's URL). Its substance is routed to a durable home, and it gets a
      disposition in the PDD's reviewer-comments disposition table.
      - **`verbatim` is the whole thread.** Capture the root comment and each human
        reply, in order and attributed. On an author's own document the resolution often
        lives in a reply: thread `AAACBVt3vNM` carries the actual GPS-duplicate rule in
        its author's reply while the thread still reads `resolved: false`.
      - **Record the Drive comment id in the item's `anchor`**
        (`"<section> · drive-comment:<id>"`). Item `id`s must be kebab-case, so the raw
        id cannot be the `id`. This is what makes the step idempotent, and here it has to
        be. A run's PDD is a new document every run, but an input document PERSISTS, so
        every run re-reads the same threads. Before capturing, search
        `ACE/<opp>/feedback/` for the comment id. A thread already captured is NOT
        captured again. Only human replies posted after ACE's last reply on that thread
        become a new item, in a new record (records are append-only).
   4. **Already incorporated: say so, don't duplicate it.** Check each thread (and its
      `quoted_text`) against the input document's CURRENT body, which step 1 reads
      anyway. If the body already says what the thread asks, disposition it
      `accepted-edit` (the author's own edit carries it; `lib/feedback-ledger.ts`),
      status `shipped`, with a summary that cites the section: *"already in
      <document> §X; the build reads it from there."* Do NOT restate it as a new
      requirement in the PDD or the programme overview. A second copy of the author's
      rule drifts from hers the next time she edits, and hers is the one she maintains.
   5. **Not yet in the body: route it, and ask the author to fold it in.** A requirement
      goes to this run's PDD body (synthesized mode) or to the programme overview under
      the component it binds (componentized mode; the overview composes, and ACE writes
      nothing into the author's document). Write a decision row with
      `review_ask: recommended-confirmation`, `owner` = the author and
      `answer_channel: review`, asking her to fold it into her document, because downstream reads a
      component from `components[].pdd_file_id` and a rule that lives only in the
      overview is one a component-level reader can miss. A question or a choice routes
      exactly as in step 2 above.
   6. **Reply, but NEVER resolve. On an input document the thread belongs to the
      author.** Use `drive_reply_to_comment` WITHOUT `action`, naming where the substance
      landed (record slug + item id, the section it is already in, or the decision id). Never pass `action: 'resolve'` on an input document, whoever
      opened the thread. The two cases differ for three reasons:
      - **Ownership.** ACE's generated PDD is ACE's artifact and a new document every
        run, so resolving turns a thread into an audit trail. The input document is
        the author's, and it persists.
      - **What "resolved" means.** On her document a resolved thread means *she* is
        done with it. If ACE closed it, ACE would be asserting on her behalf that her
        design is settled.
      - **Her working list.** Resolving removes the thread from her comment sidebar,
        which is the list she works from.

      This is a rule, not a permission limit. The service account has `canComment` AND
      `canEdit` on all six shortcut targets in `poverty-graduation/inputs/` (read-only
      `files.get capabilities` probe, 2026-09-11). For the same reason ACE never edits an
      input document's body. Resolving is left to her.
   7. **A thread the author already RESOLVED** is her closure, so ACE posts no reply to
      it. If its substance is in the body, nothing more is needed: the body is the
      durable home, and the author both wrote it and closed the thread. If it is NOT in
      the body, capture and route it per 3 and 5, and raise the gap on that decision
      row. A thread closed without its substance reaching the document is exactly what a
      later reader cannot see.
   8. **A failed reply does not halt the phase.** If `drive_reply_to_comment` is
      refused (for example, the service account lacks commenter on that document), the
      durable record from 3 is already written. List the unreplied threads in the phase
      summary with the document name and continue.

   **Contradictions stay loud.** When this run's finding disagrees with a
   recorded, verified answer — a `human-decided` row the run-init ingest
   carried as binding, or a ruling in `inputs/decision-overrides.yaml` —
   surface it in the PDD's open-questions
   section AND at the Phase 1→2 pause summary; never silently overwrite the
   prior answer. On `hh-poverty-targeting/20260812-1613` two verified answers
   were contradicted with no signal at all (ace#1201).

   **Resolving a question MOVES it, it does not annotate it.** A row you
   resolve is removed from `## Open` and appended to `## Archive` with
   `resolved_at` / `resolved_by` / `resolution_note`. Never annotate in place
   ("RESOLVED 2026-05-03 by …") — that is exactly what made this doc grow
   without bound.

   Read `ACE/<opp-name>/runs/<run-id>/inputs-manifest.yaml`
   first via `drive_read_file`. The manifest shape is:

   ```yaml
   opportunity: <opp>
   run_id: <runId>
   captured_at: <ISO>
   inputs:
     - file_id: <id>
       name: <name>
       mime_type: <mime>
     - file_id: <shortcut-id>              # a Drive shortcut in inputs/
       name: <name>
       mime_type: application/vnd.google-apps.shortcut
       resolved_target_id: <target-id>     # the document itself
       resolved_target_mime_type: <mime>
   ```

   For a shortcut entry, dispatch on `resolved_target_mime_type`.
   `drive_read_file` follows the shortcut by itself; `drive_list_comments`
   does not, so comment reads go to `resolved_target_id` (see the INPUT
   documents block above).

   For each entry, read its content **by type** — do not assume
   `drive_read_file` handles everything (it REFUSES binary formats —
   xlsx, zip/`.ccz`, images — with a typed `unsupported_binary_mimetype`
   error, so a naive read silently drops the file's content, not just
   its formatting). Dispatch on the entry's `mime_type` (and, for a
   `.ccz`, the filename extension — its mime is often a generic
   `application/zip` / `application/octet-stream`):

   - **Text-extractable** — Google Docs
     (`application/vnd.google-apps.document`), PDF (`application/pdf`),
     `text/*` (markdown, plain text), CSV / JSON / YAML / XML, and most
     Word (`.docx`) formats → `drive_read_file(file_id=<id>)`.
   - **Google Forms** (`application/vnd.google-apps.form`) →
     `get_google_form_definition(formId=<id>)` — `drive_read_file`
     returns nothing for a Form.
   - **Spreadsheets** — a Google Sheet
     (`application/vnd.google-apps.spreadsheet`) → read its tabs via
     `sheets_list_tabs` + `sheets_batch_read`. A native `.xlsx`
     (`…spreadsheetml.sheet`) → `drive_read_file` refuses it, so either
     read a sibling text/gdoc rendering of the same workbook if the
     human dropped one in (that rendering is authoritative — skip the
     raw file) or `drive_download_binary(file_id=<id>,
     writeToPath="/tmp/ace-pdd-inputs/<name>.xlsx")` and parse the file
     on disk (unzip → `xl/sharedStrings.xml` + `xl/worksheets/*.xml`)
     with a short Bash/python step. **Always pass `writeToPath`** — an
     `.xlsx` over ~30 KB is refused inline with `oversized_binary`, and
     base64 through context costs ~1.33x the file for no benefit when a
     Bash step is going to read the file anyway.
   - **An existing CommCare app (`.ccz`)** → parse it — see step 1b.
     This is ground truth (a real built app), not a notes file.
   - **Images / audio / other true binaries with no extractable text**
     → log the file by name ("supporting file present in `inputs/` —
     reference by name where it matters") and continue. **Do not halt**
     on these — the human dropped them in for downstream skills.

   Track each read's success/failure.

   If `inputs-manifest.yaml` is missing, **stop and return an
   actionable error**:

   "Phase 1 has no source material — `inputs-manifest.yaml` (at the
   run-folder root) is missing. The orchestrator should have written
   the manifest at run-start. Re-run `/ace:run <opp-name>` so the
   manifest is captured from `ACE/<opp-name>/inputs/`."

   Do not invent source material or proceed without source content.

1a. **Pre-flight Drive accessibility — halt on permission failures.**

    The reads in step 1 surface permission failures implicitly, but
    surface them ALL as a single actionable error before any
    synthesis work — a session-interrupting OAuth dance turns into a
    30-second share-with-the-SA fix.

    Track every entry from `inputs-manifest.yaml` whose
    `drive_read_file` returned a permission error.

    If any read failed with a permission error, **stop and return an
    actionable error listing every inaccessible doc**:

    "The following files are not accessible to the ACE service
    account:
      - `<file_id>` (`<name>` from inputs/)
      - …
    Share each with
    `ace-service-account@connect-labs.iam.gserviceaccount.com`
    (Viewer is sufficient) and re-run `/ace:step idea-to-pdd
    <opp>/<run-id>`. If a doc is shared only with your personal
    account and cannot be re-shared with the service account, use
    `read_personal_drive_doc` (when available) as a fallback."

    Why: a recent design-review session was cancelled mid-run
    because the LEEP data sheet wasn't shared with the SA.

1b. **Existing CommCare app (`.ccz`) inputs — parse the app, design around it.**

    A `.ccz` in `inputs/` is an EXISTING CommCare application the partner
    already runs (e.g. Spark's FCAP app). It is authoritative ground
    truth about what forms exist and what each collects — so do NOT just
    "reference it by name," parse it and let it shape the design. (ACE
    has never had a `.ccz` input before this capability landed; the
    partner's built app is the highest-signal input there is.)

    Parse recipe — the download differs from `app-release-qa` (which
    pulls the CCZ from HQ by `app_id`); a Drive-sourced CCZ is fetched
    with `drive_download_binary`. The unzip + XForm parse is identical:

    1. `drive_download_binary(file_id=<id>,
       writeToPath="/tmp/ace-pdd-ccz/<name>.ccz")` → the atom writes the
       bytes to disk and returns `{path, size}`, no base64. **`writeToPath`
       is required in practice**: a CCZ is a zipped CommCare app, so it is
       essentially always over the ~30 KB inline ceiling and an omitted
       `writeToPath` fails with `oversized_binary`. Verify the file starts
       with the zip magic `PK\x03\x04` (`head -c4`); if not, log
       `ccz-download-failed` and fall back to logging the file by name (do
       not halt the whole PDD).
    2. Unzip the file at `path` (Bash/python `zipfile`). Read `suite.xml` at the zip root
       and parse it for `<menu>` / `<entry>` → the per-form XForm paths
       (`modules-N/forms-M.xml`) and their display names.
    3. For each form XForm, extract: the form title, its question labels
       + bind types (`<input>` / `<select1>` / `<select>` / `<upload>`
       and `<bind type=…>`), and any CommCare Connect markers
       (`deliver` / `module` / `task` / `assessment`, in either the
       default `xmlns="http://commcareconnect.com/…"` form or the legacy
       `learn:`-prefixed form).
    4. Summarize into your synthesis: the menu/module map, the per-form
       field inventory (labels + types), and where Connect markers
       already exist.

    Then **design AROUND it**: when an existing app is present, the PDD
    is a Connect program that REUSES this app as the delivery substrate,
    not a spec for a net-new build. Identify and state explicitly in the
    PDD (a) which existing form(s) are the per-visit delivery record a
    Connect deliver-unit verifies + pays on, (b) which forms map to Learn
    modules / assessments, and (c) what (if anything) is genuinely
    net-new. Make the reused-vs-new split explicit so downstream phases
    build the delta, not a duplicate app. If NO `.ccz` is present, this
    step is a **no-op** — design the app from the other inputs as usual.

2. **Determine the delivery archetype** (see `## Archetypes` below). The archetype shapes the section list and the questions you ask in step 3. If the same subject is visited more than once and the visits are not interchangeable, pick `longitudinal-visits` — NOT `atomic-visit` (which has no entity to track) and NOT `multi-stage` (which stages the programme, not the entity). Reserve `multi-stage` for a programme whose stages use *different archetypes* (e.g., focus groups in Stage 1, atomic visits in Stage 2), assigning an archetype to each stage.

3. **Research and expand** the idea:
   - What health/development problem does this address?
   - What is the intervention mechanism?
   - Who are the target beneficiaries?
   - What data needs to be collected (Learn app)?
   - What services need to be delivered (Deliver app)?
   - For non–`atomic-visit` archetypes, also work through the archetype-specific questions in `## Archetypes`.

3a. **Author the decisions log.** Before drafting the PDD, populate
    `ACE/<opp-name>/runs/<run-id>/decisions.yaml` with rows that meet the
    bar criterion in `## Decisions Log Convention` below. Each row
    records a load-bearing default the skill is about to apply when
    drafting the PDD. Use the AI's best inference from the source
    material for each `ai-default` value; status is `ai-default` (the AI
    proceeded with its default).

    See `## Decisions Log Convention § Common load-bearing decisions for
    Phase 1` for a working template of decisions that often qualify under
    the bar. Use it to guide judgment, not as a checklist — emit what
    meets the bar, skip what doesn't, add others when warranted.

4. **Draft the PDD** with the **base sections** below, plus **archetype-specific additions** from `## Archetypes`. Use the values selected in step 3a's `decisions.yaml` as authoritative — every numeric or named-entity in the PDD body should match the corresponding row's effective value (`override` if present else `ai-default`). If a re-run reads a `decisions.yaml` from a prior run with `status: overridden` rows (human edited via the renderer + sync skills), use the `override` value instead of the `ai-default`.

   **Base sections (all archetypes):**
   - **Document metadata** — the PDD's identifying facts (archetype, opportunity,
     run id, status, sources) go at the very top as a RENDERED block, one bold-label
     line per fact — e.g. `**Archetype:** atomic-visit`, `**Opportunity:** <slug>`,
     `**Run:** <run-id>`, `**Status:** …`, `**Sources:** …`. Do **NOT** emit a raw
     `---` YAML frontmatter block: the PDD is written as a native Google Doc
     (step 6), where `---` renders as a horizontal rule and the keys render as a
     wall of `key: value` noise above the title — the first thing a partner sees.
     Nothing parses the frontmatter: `idea-to-pdd-qa` check 2
     (`archetype_declared_and_valid`) reads the archetype from frontmatter **or**
     the body, and the bold-label form satisfies the body branch.
   - **Archetype** — declared in the metadata block, repeated as the first heading
   - **Problem Statement** — what problem this solves
   - **Intervention Design** — how the intervention works
   - **Learn App Specification** — what FLWs need to learn (data collection, facilitation, etc., depending on archetype)
   - **Deliver App Specification** — what FLWs deliver (forms, sessions, etc., depending on archetype)
   - **Target Population** — beneficiary criteria, expected reach
   - **FLW Requirements** — number of FLWs, skills needed, geographic distribution
   - **LLO Preference** — preferred or known LLOs to execute, from LLO Directory
   - **Solicitation** — Phase 8 publishes a solicitation to labs.connect.dimagi.com so LLOs respond. All three fields are optional; defaults apply if omitted. Always ask once: "do you want a custom solicitation type (EOI vs RFP), a non-default deadline (default 14 days), or a custom response template?" If not, leave the section with default placeholders (the `solicitation-create` skill reads them as defaults).
   - **Success Metrics** — how to measure if the intervention worked
   - **Evidence Model** — Layer A / B / C verification plan (see `## Evidence Model` in `templates/pdd-template.md`)
   - **Timeline** — expected duration of the opportunity
   - **Program Parameters** — the typed handoff table. A `| Key | Value | Provenance |` table
     of every decision THIS document makes that a LATER phase must apply
     verbatim and that cannot be applied in the artifact this phase produces:
     `learn_passing_score`, `assessment_items`, `payment_rate_min` /
     `payment_rate_max` / `payment_rate_currency` / `payment_rate_unit`,
     `daily_cap_per_flw`, `total_cap_per_flw`, `flw_count_min` /
     `flw_count_max`, `expected_reach_min` / `expected_reach_max`,
     `entity_id_grain`, `entity_state_taxonomy`, `followed_entity_case_type`,
     `duplicate_gps_rule`, `cap_rationale`, `connect_delivery_type`, `opportunity_country`,
     `opportunity_currency`. **The last three are the program shell and are
     IMMUTABLE after `connect_create_program`** — `connect_update_program`
     accepts only name/description/budget/start_date/end_date, so a wrong value
     is correctable only by creating a replacement program. Settle them here:
     confirm the delivery-type slug against `connect_list_delivery_types` on the
     PM org, and denominate the currency in the LOCAL money of
     `opportunity_country` (Nigeria → `NGN`, India → `INR`; never default to
     USD). Take the
     canonical key vocabulary and the per-key guidance from `## Program
     Parameters` in `templates/pdd-template.md` — snake_case keys, unknown keys
     allowed, omit a row only when this PDD genuinely does not decide it.
     Prose elsewhere in the PDD is **not** a handoff: a later phase has to
     notice it, and when it does not the value silently falls back to a skill
     default. **Machine-checked** — a missing section fails
     `idea-to-pdd-qa § all_required_sections_present` and a missing or
     incoherent table fails `§ program_parameters_coherent`, both blockers.
     Step 7.5 writes the SAME values again as the `program_parameters` block in
     `run_state.yaml`; author this table first and transcribe it there, so the
     body and the state block cannot diverge.

     **Every row carries a third `Provenance` cell (ace#2364)** — the table is
     what later phases read, so a value ACE worked out must not look like one
     an author wrote. Exactly one of:
     - `read: <document § ref>` — an author document for THIS programme
       states it. Only a `read` value may be attributed to the author — in an
       email, the Work Order, a solicitation or an eval.
     - `derived: <decision-id>` — ACE chose it. **Write the `decisions.yaml`
       row first, then name it**: a number a reviewer could challenge (an
       assessment item count, a cohort size, a cap sized from an estimate, a
       `[PROPOSED]` rate) must be findable as a decision, or the reviewer
       cannot tell where it came from. A purely mechanical value computed from
       other rows of this table names those keys instead
       (`derived: daily_cap_per_flw, flw_count_max`) and needs no row of its
       own — that is the scope line: every row carries provenance, and only a
       derived or borrowed value a reviewer could challenge gets a decision
       row.
     - `borrowed: <source>` — taken from reference material about a
       DIFFERENT programme (a model-comparison column, another rollout).
       Never mark it `read`, and never call it anchored. When it drives a live
       value, record a decision row so it reaches a reviewer as a question.

     Canonical failure: poverty-graduation/20260908-0510, where
     `assessment_items: 30` / `pre_assessment_items: 20` appeared in no input,
     sat in the table exactly like author values, and were then called "your
     Annex's 30 and 20" in ACE's email. *Enforced:* `idea-to-pdd-qa §
     program_parameters_provenance`.

4a. **Spec for deployability, not just topic presence.** `[ai-iteration: 2026-05-29]` The downstream
    build skills faithfully transcribe the PDD, and the app evals now
    **hard-fail** a build that is structurally complete but undeployable
    (see `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md` — the
    ITN run produced a topic-complete app that an expert had to
    substantially rebuild). A PDD that only *names* topics produces a
    faithfully-thin app. So when the source material or evidence model
    *implies* any of the following, the **Deliver/Learn App
    Specification and Evidence Model MUST spec it explicitly** — don't
    leave it for Nova to infer (it won't):

    **ZEROTH — mark every app-spec statement as a REQUIREMENT or a
    MECHANISM. This governs everything else in 4a.** Specificity is the
    point of this step; *unmarked* specificity is what costs runs. Two
    different kinds of sentence live in the app specs and they must not
    read alike:

    - A **requirement** is an observable program fact that must hold in the
      built app. It is **binding**: it flows into the Work Order and the
      Phase-6 training materials, downstream evals grade against it, and a
      build that does not satisfy it has failed. *"A household that declines
      consent must never appear on the follow-up list and must never be
      payable."*
    - A **mechanism** is how CommCare/Connect/Nova achieves it. It is
      **advisory**: Phase 3 may implement it differently, and doing so is a
      normal build choice, **not a deviation**, and needs no PDD correction.
      *"…by ending the form without creating a case."*

    Write requirements as prose the program owner would recognise. Where a
    mechanism is genuinely useful to suggest, mark it explicitly — a
    `Mechanism (advisory):` prefix, or a `> **Requirement, not mechanism**`
    callout naming the requirement and leaving the how to the build. Field
    names, types, constraints, case write-backs, and the data model ARE
    requirements (they define the instrument); module/form partitioning,
    marker placement, `entity_id` construction, case-operation ordering, and
    anything phrased as "the app enforces X by doing Y" are mechanisms.

    **Never escalate a requirement into a mechanism.** This is the specific
    failure this rule exists to stop. On `bednet-check-2-visit/20260813-2313`
    the source brief said `consent_given` was *"required, must be yes to
    proceed"* — a requirement, and an ambiguous one. Phase 1 rendered it as
    *"a `no` ends the form without creating a case"* — an invented mechanism,
    unbuildable (a registration form creates its primary case
    unconditionally; a conditional `add_case_operations` create is accepted
    but adds a SECOND case). Because it read as binding, Phase 3 finding it
    unbuildable became a deviation from an approved design document that had
    already reached the Work Order, and cost a mid-run PDD correction
    (dimagi-internal/ace#1294). The requirement itself was satisfiable and
    was satisfied — by gating the later questions on consent and filtering
    the follow-up case list. Had the mechanism been marked advisory, nothing
    downstream would ever have been wrong.

    When you are unsure which one a sentence is, ask: **would a program
    owner who has never heard of CommCare recognise this as part of their
    program?** If yes it is a requirement; if it only makes sense to someone
    building the app, it is a mechanism.

    **FIRST — check every mechanism against the must-not-assert list.**
    Before specifying any **enforcement or verification** mechanism (a gate,
    a threshold that refuses something, a control that "the app enforces"),
    check it against `skills/_app-component-library.md § Mechanisms a PDD
    must not assert` — **both tables**. A listed mechanism **MUST NOT be
    asserted as enforced or delivered.** Where the design intent is still
    wanted, either:

    - state the **buildable approximation and name the residual** — the
      shape `gps-accuracy-capture` models ("each fix's accuracy is captured
      and submitted; readings worse than 50 m are flagged and down-weighted
      in dedup" — observability, stated honestly, not enforcement); or
    - record it as a decision row with a **`review_ask`** for a human
      (§ Asks are decision rows), rather than asserting a control ACE will
      not deliver this cycle.

    This is a hard check, not a style note, because the PDD's sentence flows
    **verbatim into the Work Order** and into the Phase-6 training
    materials. Three mechanisms have now shipped into all three documents
    while being inert in the built app (ace#995, ace#1006, ace#1121) — and
    Phase 3 discovering it at build time does not retro-correct the
    documents that already went out. The bullets below are the per-topic
    instances of this rule; the list is the enumerable version, and it is the
    list that gets checked.

    **Say WHY correctly.** Table A is closed at the platform surface; Table B
    is buildable but outside ACE's toolchain today. The PDD behaviour is the
    same for both — don't assert it — but the wording is not. Writing "the
    platform cannot do X" about a Table B mechanism puts a false constraint
    into a document that will outlive it, and forecloses a capability request
    someone should be making. If you are not certain which table a mechanism
    is in, say "ACE does not build this today" rather than "this is
    impossible."

    **ALSO check the RETIRED rows — this check is bidirectional.** The rule
    above guards a mechanism the PDD is about to *assert*. The inverse is not
    covered by it and has now cost a run: **source material that states a
    constraint, a fixture pin, or a "this is unreachable / not possible on
    this instance" claim** which a mechanism decision then rests on. Check
    that claim against `skills/_app-component-library.md` too — including its
    **RETIRED / struck-through rows**, not only the live ones. A retired row
    is history, so it will never trip the must-not-assert check above; the
    source sentence leaning on it is exactly what goes unexamined.

    If the premise is retired, the source-stated value still **stands for
    this run** — source is authoritative and re-minting a fixture golden is
    an operator act — but the PDD MUST do all three of:

    - record it as a `conflicting` `decisions.yaml` row (§ Step 3a), citing
      the retired row in `conflict_signals` next to the source's own
      sentence;
    - mark the pinned value as an **advisory mechanism** rather than a
      requirement, per the requirement-vs-mechanism rule above, and state the
      underlying **requirement** separately — so a later phase implementing
      the now-available approach is a normal build choice, **not a
      deviation**;
    - record the stale premise as a decision row with a **`review_ask`**
      naming exactly what needs re-minting.

    Why this has to be said here: repo-side citations of a closed upstream
    issue are already caught by `scripts/probe-upstream-asks.ts`, but it
    walks repo directories only (`SCAN_DIRS` / `SCAN_FILES`) and cannot see
    Drive-resident opp inputs — so a fixture brief goes stale with no signal
    (ace#1924). Live case: on `bednet-check-2-visit/20260902-1555` the
    brief's `entity_id` pin ("the household case id is unreachable — a
    followup form cannot read its own case on this Nova instance") rests on
    the `voidcraft-labs/commcare-nova#458` closure that Table A **retired 2026-08-29**, and
    the fallback it pins is precisely the `atomic-visit` grain that row's
    sanctioned alternative warns silently degrades a `longitudinal-visits`
    design.

    - **Capture fidelity.** If the Evidence Model implies a GPS/location
      radius, spec **accuracy-aware GPS** (a stated target accuracy, the
      accuracy value submitted on every visit, an on-screen advisory),
      not a bare "capture GPS."

      **A stated GPS accuracy tolerance MUST NOT be written as an
      enforced control** (dimagi-internal/ace#1006). It is unenforceable
      on both surfaces: Nova rejects `validate` on `kind: geopoint`, and
      Connect's verification-flags form no longer carries `gps` /
      `gps_radius_meters` (ace#1013). So the Evidence Model must phrase
      it as what it is — e.g. *"each fix's accuracy is captured and
      submitted; readings worse than 50 m are flagged to the FLW and
      down-weighted in dedup"* — and must NOT say "rejected", "must be
      ≤ 50 m to submit", "the app enforces", or "Connect enforces". The
      same sentence flows verbatim into the Work Order, so a PDD that
      overstates the control puts a promise ACE cannot keep into a
      contractual document. If the design genuinely needs a hard gate,
      record that as a decision row with a **`review_ask`** rather than
      asserting it.

      If an answer is enumerable, spec it as a **select with the option
      list** (+ "Other, specify"), not free text. Prefer bucketed ranges
      over raw integers where field-reliable.
    - **Data quality.** Spec the **constraints**: numeric bounds and
      cross-field checks on counts, phone-format expectations, free-text
      length caps, and which fields are required-for-credit.

      **A per-row qualifier and an aggregate over the same repeat MUST
      agree** (dimagi-internal/ace#1123). If the PDD asks a
      confirmation / eligibility / membership question on each row of a
      repeat, then every aggregate the PDD derives from that repeat —
      `count()`, `sum()`, a band, a score — MUST reference the
      qualifier in its predicate: write
      `count(/data/<repeat>[<qualifier> = 'yes'])`, never a bare
      `count(/data/<repeat>)`. A PDD that names a per-row confirmation
      **and** an unfiltered aggregate over the same nodeset is
      self-contradictory on its face, and the contradiction is
      detectable without any domain knowledge — so check it before the
      PDD ships. The build follows the data-quality table, so the
      unfiltered version wins: the app asks the FLW a required question
      and then throws the answer away. On `hh-poverty-targeting` v2.1
      that field was the roster's membership confirmation and the
      aggregate was household size — **31 of 102 attainable PPI points
      across a sharp band boundary**, so one wrongly-retained member
      moved the score 21 points, and the FLW's honest answer changed
      nothing. If the intended reading really is "non-members are never
      entered", then **drop the per-row confirmation** — do not leave
      both in the document.

      Same failure family as the dead-`now()` (ace#995) and the
      unenforceable GPS gate (ace#1006): a control that reads as
      configured in the PDD, the Work Order and the training materials,
      and does nothing in the built app.
    - **Case persistence.** For multi-visit / follow-up designs, spec
      **which observations each follow-up visit writes back to the
      case** (the whole point of a follow-up is to record change).
    - **Assessment enforcement.** If FLWs must pass a readiness gate,
      spec a **pre-test + post-test**, the threshold, the item count
      (enough to test the curriculum), and that the result experience is
      pass/fail-conditional — not "a quiz exists."

      **Do NOT spec a randomized or per-attempt item draw**
      (dimagi-internal/ace#1121, ace#1213) — and be precise about why. "12
      items served per attempt from a bank of 30, fresh draw each retake" is
      **Table B**: it is expressible in XForms (a seeded `once(random())`
      driving selection from a lookup-table/fixture nodeset, or hidden
      questions gated on `relevant`), and Connect scores a fixed-size draw
      normally — 12 of 30 served keeps the denominator at 12, so a
      `passing_score` works as usual. What is missing is a **Nova authoring
      primitive** for it, plus the complexity of the fixture/relevance
      machinery. So: spec **one fixed bank sized for the gate** (plus a
      distinct pre-test bank where a baseline is wanted), and **do not write
      that rotation is impossible** — it is not.

      If retake-resistance genuinely matters — and note that unlimited
      re-attempts against a fixed bank means a worker can pass by memorising
      the answers, which softens the Deliver-unlock gate on every retry —
      record it as a decision row with a **`review_ask`**, consider whether unlimited
      re-attempts is the right policy, and where the program really needs
      rotation, file it as a **Nova capability request**.

      **Any worked assessment item the PDD emits MUST be labelled
      ILLUSTRATIVE** (dimagi-internal/ace#1120). A PDD specifies the
      assessment *blueprint* — bank size, items served per attempt, stem
      format, distractor rules, the discrimination target. A specific
      quiz item is build content, not design. So if you include a worked
      example at all, mark it in the PDD text as *"illustrative of the
      required shape — Phase 3 authors the bank and may harden or
      discard this item"*, and never as mandated content. Two reasons,
      both measured: an item authored here is never cold-read-tested
      (all three of `hh-poverty-targeting` v2.1's worked items were
      guessed cold by both independent blind probes), and worked items
      **anchor the tone** of the other ~21 items Phase 3 authors, so a
      guessable model teaches the builder to write guessable items.
      Asserting *why* an item discriminates does not make it so — v2.1's
      stated rationale for its compound item was rejected on sight by
      both probes.
    - **Working language.** If the program runs in a non-English
      language, state it as a **Working language** line in the Learn and
      Deliver App Specifications, with its CommCare language code — it is
      real design context, it drives the training materials, the
      facilitator briefing, the per-opp OCS chatbot and the solicitation's
      language requirement, **and as of 2026-08-17 it is also delivered in
      the app.** Nova shipped a real per-language channel, so ACE builds
      the app's strings in the working language on top of an
      always-complete English source (standing decision 2026-08-17,
      PR #1463, superseding ace#968/#1391 — see `_app-component-library.md §
      app-language-layer`). What the PDD may now assert: labels, choices,
      hints and assessment items appear in the working language, and the
      app carries English as its source language. What it must still NOT
      assert: that the translations are **professionally or
      native-speaker reviewed** at delivery — ACE authors them, Nova marks
      them `needs-review`, and review is a normal downstream obligation
      exactly like review of the English copy, not a completed step. Also
      do not promise an in-app language-*selector question*; language
      choice is CommCare's own runtime affordance. English remains the
      runtime default for now, so if the design depends on an FLW seeing
      the working language first, record that as a decision row with a
      **`review_ask`** rather than asserting it.

    These become `decisions.yaml` rows where they meet the bar (§
    Decisions Log Convention). This is the upstream half of the
    eval-fitness fix: a thin PDD is the root cause, a deployable PDD is
    the cure.

5. **Self-evaluate (LLM-as-Judge) — Stress-Test Rubric.** Run the rubric defined in `## Rule provenance — human rulings vs AI iteration

**Not every rule in this file is a durable learning.** ACE iterates hard: about
half of the last 200 commits carry a `Co-Authored-By: Claude` trailer, so a large
share of the rules here were written by an AI mid-cycle, to fix a problem that
may since have moved. Others are human rulings — an operator deciding how ACE
should behave. **Those two things read identically today, and they should not.**

### The three classes

- **`[human: <name>, <date>]` — a human ruling. Honor it diligently.** Follow it
  even when it is inconvenient, and *especially* when following it makes a build
  harder. Do not reinterpret it to make a phase pass, do not narrow it to the
  case in front of you, and do not quietly drop it. If it appears to conflict
  with something else, **surface the conflict rather than picking a side.** A
  human ruling that an agent has silently optimised away is the single most
  expensive kind of drift in this repo, because the human has no way to see it
  happened.
- **`[ai-iteration: <date>]` — added by an AI during an improvement cycle.**
  Presumed useful, **not sacred.** It encodes what was true when it was written.
  If it is now causing harm, contradicts a human ruling, or was written for a
  problem that has since changed shape, it is **fair game to revise** — but say
  so explicitly, cite the evidence, and change it in the open rather than
  ignoring it in place.
- **`unmarked` — provenance not established. Treat as `ai-iteration`.** This is
  the default and most of this file is currently in it. Tag rules as you touch
  them rather than in a big retrofit. **Do not promote an unmarked rule to
  `human` on a hunch** — confirm with the operator, then tag it so the next
  reader does not have to ask again.

**Precedence: a human ruling beats an AI-iteration rule, always.** Two human
rulings that genuinely conflict go to the operator — do not arbitrate them.

### Establishing provenance when it is not tagged

The signal already exists in git history and cannot be faked after the fact:

```bash
scripts/rule-provenance.sh "<distinctive phrase from the rule>" [path...]
```

It reports `human`, `ai-iteration`, or `unmarked`. Two things make this less
obvious than it looks, and the script encodes both:

1. **Git authorship is useless here.** Every commit carries the operator's name,
   including AI-authored ones. The `Co-Authored-By: Claude` trailer is the only
   authorship signal in the history.
2. **The trailer is a one-way signal.** Present → reliably AI. *Absent → proves
   nothing*: measured 2026-08-14, **45 of the last 300 non-merge commits carry no
   trailer** and sampled ones are plainly AI-written. So a missing trailer yields
   `unmarked`, never `human`. Inferring "human" from a missing trailer would
   sanctify stale AI rules — the exact failure this section exists to prevent.
3. **A trailer tells you who TYPED the rule, not whose DECISION it was.** An AI
   transcribing an operator ruling carries the trailer while the rule is
   genuinely human. So the script checks the **rule text itself** for a human
   citation first (`Operator ruling (Jon, 2026-08-13)`, `(Jon, 2026-07-01)`,
   `standing operator directive` — how this repo already records them), and that
   outranks the trailer.

Merge commits are skipped: a PR merge carries no trailer regardless of who wrote
the work, and would otherwise read as human.

### Why this section exists

Both rules that collided on `bednet-check-2-visit/20260813-2313` turned out to be
AI-authored during heavy iteration, and neither was marked:

| Rule | Commit | Provenance |
|---|---|---|
| Step 4a "spec for deployability, not just topic presence" | `336039b1`, 2026-05-29 | `ai-iteration` |
| `pdd-to-learn-app` "Connect's `passing_score` is ALWAYS 80" | `d6c26e86`, 2026-05-23 | `ai-iteration` |

The second one is the instructive case. The PDD specified a 6-of-6 gate
(`passing_score: 100`) sourced directly from the operator's brief; the build
skill said *always 80*. Read as equally authoritative, that is an unresolvable
standoff, and picking 80 would have let 5-of-6 through and defeated the gate the
brief asked for. Read with provenance, it is not close: a source-stated program
decision beats a generalisation an AI wrote while fixing a different bug. The run
picked 100 and was right to — but it had to reason its way there from scratch,
and a headless run might not have.

**Applying this in practice:** when you hit a conflict between what the source
material says and what a rule in a skill file says, check the rule's provenance
before deciding. If the rule is `ai-iteration` and the source is explicit, the
source wins and you note the override. If the rule is `[human: …]`, honor it and
raise the conflict.

## LLM-as-Judge Rubric` below against the drafted PDD. If **two or more** checks grade other than `pass`, the PDD is **not approved** — iterate on the weak sections and re-run before proceeding. **Check 6 (Launch readiness) blocks on its own** — see the rubric's own note.

6. **Write the PDD** to `1-design/idea-to-pdd.md` **as a NATIVE Google Doc via
   `drive_create_doc_from_markdown`** — NOT `drive_create_file` with a `text/*`
   mimeType (dimagi-internal/ace#1061).

   **Compose the markdown to a LOCAL FILE first, then pass
   `localFilePath` — do not emit the document inline (ace#1780).** Write the
   composed markdown to an absolute scratch path, then call
   `drive_create_doc_from_markdown({name, localFilePath, parentFolderId})`.
   The server reads the bytes off disk, so the call costs ~zero context
   regardless of document size; a PDD emitted inline costs roughly one output
   token per four characters, and this document is written TWICE (step 6b).
   The inline `markdown` param still works and is fine for something small.
 The PDD is the only artifact in this
   pipeline whose purpose is to be *argued with* by a human: the entire
   feedback → ledger → next-run loop starts with a domain expert leaving
   ANCHORED comments on it. A `text/markdown` upload renders in Drive's
   plain-text previewer — no comment gutter, no suggesting mode, no way to
   anchor to a section — and the failure is silent, because every content check
   still passes. It regressed exactly that way between two runs of the same opp
   six days apart (9 anchored comments → zero). `idea-to-pdd-qa` check 7
   (`pdd_is_native_google_doc`) is the structural backstop. **FIRST resolve-or-create the phase subfolder** — `drive_create_folder({name: '1-design', parentFolderId: <runFolderId>, findOrCreate: true})` — and use the returned id as `parentFolderId` for this write **and** for the QA + eval verdicts and the phase summary. Do NOT pass the run-folder id directly as the write parent: that lands the artifact flat at the run root and fails the Phase boundary's `verify_phase_artifacts` (it walks `1-design/`; jjackson/ace#623). `decisions.yaml` is the exception — it stays at the run-folder root. Include the stress-test rubric results as a `## Stress Test Results` appendix at the bottom of the PDD, so downstream skills (and humans) can see what was caught and what was waived.

6b. **Persist the PDD's source markdown — the SAME LOCAL FILE, written
   twice.** Immediately after step 6's render, write the EXACT bytes to
   `1-design/idea-to-pdd.source.md` via **`drive_upload_binary`** with
   `mimeType: 'text/markdown'` (same `parentFolderId` as step 6) — the same
   atom `skills/_training-template.md` prescribes for every `.source.md`
   companion.

   **NOT `drive_create_doc_from_markdown`**, which renders the source copy
   into a Doc and destroys the very bytes this step exists to preserve. And
   **NOT `drive_create_file`**, which does exactly the same thing while
   LOOKING like the safe choice: it always creates a Google Doc, it has no
   `mimeType` that changes that, and until ace#1991 the key was silently
   dropped by its schema. This step therefore produced a SECOND rendered Doc,
   and `run-surface-audit`'s DOC-FIDELITY check compared one Doc against
   another built by the same importer — passing structurally while unable to
   detect the loss it exists to catch. Measured on
   `poverty-graduation/20260905-0924`: both writes pointed at the same local
   file, both landed as `application/vnd.google-apps.document`, and the
   round-trip was 58,470 bytes against 57,178 sent. `drive_create_file` now
   REFUSES a `mimeType` and names this call in the refusal.

   `drive_upload_binary` uses Drive's media-upload path, so the file lands as
   `text/markdown` and `drive_read_file` returns it verbatim (`alt=media`,
   not a Doc export). Despite its name it is the right atom for text whose
   bytes matter.

   **Pass `localFilePath` pointing at the SAME file step 6 used
   (ace#1780).** That is what makes this step's premise true rather than
   aspirational. The premise is byte-identity — it is what gives
   `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` check something real to
   compare — and re-emitting the document inline a second time means the
   agent types it out twice, independently, with **nothing verifying the two
   emissions match**. A dropped paragraph in the second emission produces a
   source companion that silently disagrees with the published doc, which is
   exactly the class the check exists to catch, reintroduced in the check's
   own input. Two calls against one local file make the copies identical by
   construction instead of by diligence.

   Why it is not optional: the renderer CONSUMES its input. Once the Doc
   exists the markdown you composed exists nowhere, and the `.md` in
   `idea-to-pdd.md` is display text, not a file — `drive_list_folder` over a
   finished run's `1-design/` returns it as
   `application/vnd.google-apps.document` with no sibling markdown. That
   leaves `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` — the only check
   that compares what was PUBLISHED against what was WRITTEN, and the only one
   that could have caught a document silently losing content with every other
   check green (ace#1418) — permanently unresolvable, because its
   `--doc-source` remediation has nothing real to point at. One extra call
   turns a blocking gate from decorative into operable.

   This is a plain companion file, not a second deliverable: it is never
   shared, never linked, and never read by a human. Do NOT share it
   anyone-with-link. (ace#1687 half 2; declared `sourcePersisted` in
   `lib/artifact-manifest.ts`, enforced by
   `test/lib/source-persisted-artifacts.test.ts`.)

6c. **Share the PDD at creation (ace#1843) — anyone-with-link `commenter`,
   UNLESS the opp is confidential (ace#3191).** Immediately after step 6b, on
   the `fileId` step 6 returned, first get the share plan. One signal decides
   it, defined once in `lib/opp-confidentiality.ts`: **the opp is confidential
   when `ACE/<opp>/inputs/confidentiality.yaml` exists.** Look for it in the
   inputs folder (`resolve_opp_path` → `drive_list_folder(inputs_id)`); if it
   is there, `drive_read_file` it with the default `text/plain` export (never
   `text/markdown`, which escapes YAML) and save the text locally:

   ```bash
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/design-doc-share-plan.ts" <local confidentiality.yaml | none>
   ```

   Act on the plan's `mode`, and nothing else:

   - `anyone-with-link` (no confidentiality file — the normal case):
     ```
     drive_set_anyone_with_link(fileId: <pddDocId>, role: 'commenter')
     ```
   - `named-reviewers` (confidential; the file lists `reviewers:` emails): for
     each email, `drive_share_with_person(fileId: <pddDocId>, email: <e>, role: 'commenter')`
     — no Drive notification email (the atom's default); never anyone-with-link.
   - `unshared` (confidential; no reviewers listed): do NOT share. The ACE
     Shared Drive's members can still open it.

   Record the plan's `mode` as `products.pdd.share_mode` in step 7.5, and on a
   confidential opp a decision row (`id: design-document-sharing`, the plan's
   `reason` as the rationale). **Why:** the PDD is internal and may name a party
   the opp's deny list hides from LLOs — connect-fi/20261018-1440's names its
   funder — and ace-web's public run-summary page links it, so a link share
   hands that name to whoever the URL reaches. Pass `none` only when the file
   is genuinely absent: guessing "not confidential" is the leak.

   **`commenter`, not `reader`.** A Drive reader physically CANNOT leave a
   comment, and the PDD is the one artifact in this pipeline whose purpose is
   to be argued with: `skills/feedback-ledger`'s `channel: gdoc-comments` and
   step 1's read-back of anchored reviewer comments both assume the reviewer
   can write one. Sharing `reader` produces a link that opens and a review
   loop that is structurally impossible.

   **At creation, not as a cleanup step, and not left to
   `/ace:share-run-access`.** `drive_create_doc_from_markdown` creates
   UNSHARED, and nothing downstream tests reachability: the doc exists,
   `verify_phase_artifacts` finds it, `classify_phase_writeback` is `ok`,
   `validate_run_state` is clean, every content eval passes — and the
   recipient gets *You need access*. Measured on three independent runs in
   three days (hh-poverty-targeting/20260828-0702,
   bednet-check-2-visit/20260828-0629, spark-facilitator/20260828-0703): the
   PDD and Work Order 401 anonymously on all three while the six Phase 6
   training documents, whose producers already do this, were readable on all
   three. The split tracks the producing skill, not the run.

   Second-order effect, which is why a dead link understates it: ace-web
   MEASURES the `access` tag of each Drive link (`_read_design` →
   `LinkAccessReader.tag`), so a private PDD renders as **ADMIN ONLY**. The
   partner reads "we deliberately withheld the design" rather than "we forgot
   to share it" — a true story about a wrong state. Sharing corrected the tag
   with no ace-web change, which is what confirms the defect is producer-side.

   (Declared `recipientFacing` + `shareRole: 'commenter'` in
   `lib/artifact-manifest.ts`; enforced by
   `test/lib/recipient-facing-artifacts.test.ts`.)

<!-- 0.13.116: gate-brief write step removed. The orchestrator composes a
pause-time summary from this skill's QA verdict (idea-to-pdd-qa) +
eval verdict (idea-to-pdd-eval) at the Phase 1→3 Pause Point. -->

7.5. **Write the `products.pdd` block to `run_state.yaml`** so
   downstream readers (ace-web's summary page in particular) don't
   have to fetch and regex the PDD body.

   - `title`: the friendly intervention name from the PDD's H1 / opening
     line (e.g. "Turmeric Market Survey"). Strip trailing punctuation
     and any Google Docs comment markers (`[a][b]`).
   - `description`: a one-paragraph plain-prose overview, ~1–3
     sentences, drawn from the PDD's `## Overview` (or `## Summary` /
     `## Abstract`) section. Strip markdown bold/italic wrappers; keep
     content as a single line.

     **This is the first thing an outside partner reads.** ace-web renders
     it as the opening paragraph of the PUBLIC run-summary page (ace-web
     `apps/opps/summary.py` `_read_opp`). Write it for a partner who has
     never seen the PDD: what the programme does, for whom, and what
     Connect pays for — in words. **No form field names, code values,
     `=` / `AND` / `OR` expressions, snake_case identifiers, run ids or
     backticks.** Translate rather than lift: *"Connect pays for each
     community meeting the facilitator confirms took place, up to three"*,
     never *"verified as meeting_conducted = yes AND meeting_type =
     community_meeting"* (verbatim from spark-facilitator/20261001-2208,
     whose summary page failed its outsider review on it). The PDD body
     keeps its identifiers; only this one-liner is for outsiders.
     *Enforced:* `idea-to-pdd-qa` check `pdd_description_plain_language`
     (`lib/pdd-description-plain-language.ts`).
   - `file_id`: the Drive `fileId` returned by Step 6's
     `drive_create_doc_from_markdown`.
   - `program_parameters`: the typed handoff block — **every PDD decision
     that a LATER phase must apply verbatim and that cannot be applied in
     the artifact this phase produces.** Prose in the PDD body is not a
     handoff: a later phase has to notice it, and when it doesn't the value
     silently falls back to a skill default. Emit every key you can
     determine; omit one only when the PDD genuinely does not decide it.

     These are the SAME decisions the PDD body's `## Program Parameters`
     table carries (step 4). Author that table first and transcribe it here —
     the body table is what `idea-to-pdd-qa` reads, this block is what
     downstream phases read, and the two must agree.

     | Key | Applied by | Failure if it defaults instead |
     |---|---|---|
     | `learn_passing_score` | Phase 4 `connect_create_opportunity.learn_app.passing_score` | Nova exposes no `passing_score` slot — `connect.assessment` carried only `{id, user_score}` when the Learn build read it back (repro: run `bednet-check-2-visit/20260813-2313`, Nova app `53583a46-298a-4a02-857a-bb86cd8e9a75`) — so a PDD gate of 100% silently becomes the skill's default 80 and 5-of-6 passes |
     | `payment_rate_band` | Phase 4 payment unit; Phase 8 solicitation | The band reads as an agreed price, or the awarded rate is applied without reference to it |
     | `daily_cap` / `total_cap` | Phase 4 opportunity config | Caps that do not match the PDD's stated economics |
     | `entity_id_grain` | Phase 3 `pdd-to-deliver-app`; Phase 4 payment unit | A payment grain chosen per-run rather than per-design |
     | `duplicate_gps_rule` | Phase 3 `threshold-coherence-flag` + `pdd-to-deliver-app-eval § threshold_coherence`; the dedup rule's `connect-opp-setup` decision row (applied in review — Connect carries no GPS-duplicate control, ace#1013) | The accuracy condition is dropped: an accuracy-conditioned radius reads as a bare radius under the GPS tolerance, is flagged incoherent, and invites a builder to "fix" an author's decision (ace#2373) |

     **`duplicate_gps_rule` is the WHOLE dedup rule, never a bare radius
     (ace#2373).** Emit it as an object —
     `{radius_m, applies_when: both_accuracies_below_radius, fallback: identifiers}`
     — dropping `applies_when` only when the PDD runs the GPS test whatever
     the readings' accuracy. **Do not emit `duplicate_gps_radius_m`**: a scalar
     cannot carry the condition. Per ace#2373, `poverty-graduation/20260908-0510`
     held `duplicate_gps_radius_m: 15` for a rule its author later [FIXED] as
     *"same GPS point (< 15m) where both readings have accuracy better than
     15m. Where either reading is less accurate than the radius, duplicate
     detection relies on identifiers alone"* — so a reader of the state block
     sees only a 15 m radius beside a 50 m GPS tolerance, which is the
     ace#984 incoherence the author's condition exists to avoid. Transcribe the rule as the author
     wrote it; never raise the radius or tie it to the tolerance to make it
     look coherent — `lib/gps-dedup-coherence.ts` classifies the conditioned
     form coherent as written.

     ```yaml
     program_parameters:
       learn_passing_score: 100
       payment_rate_band: { currency: USD, min: 1.00, max: 2.50, unit: "verified follow-up visit" }
       daily_cap: 5
       total_cap: 30
       entity_id_grain: "worker username + follow-up visit date"
       # Only when the PDD de-duplicates by GPS proximity — the whole rule (ace#2373).
       duplicate_gps_rule: { radius_m: 15, applies_when: both_accuracies_below_radius, fallback: identifiers }
       # Only when the PDD mandates an EXACT assessment item count — see below.
       assessment_coverage_deviation:
         accepted_max_ratio: 0.31
         reason: "D-1: the gate certifies two payment-model facts and is not a competence certification"
     ```

   **If the PDD mandates an EXACT assessment item count, check it is
   satisfiable before writing it (ace#1250).** Enumerate the Deliver app's
   **high-consequence operations** and the **counter-intuitive rules** the
   same way `pdd-to-learn-app-eval § 5c` step 2 does, then run
   `checkCoverageFeasibility` from `lib/assessment-coverage-feasibility.ts`.
   Coverage is the fraction of those two sets carrying ≥1 qualifying item,
   **counter-intuitive weighted double**, and it must reach **0.50** or the
   dimension hard-gates at ≤3.

   A mandate below that ceiling **pre-commits Phase 3 to a `fail` and the
   builder is graded down for obeying its brief.** It also cannot be repaired
   downstream: the auto-fix loop is capped at one round against an immovable
   number, and it pins `/ace:iterate` at 0% on the opp forever, because the
   loop's clean gate requires `pdd-to-learn-app-eval == pass`.

   **Before declaring a shortfall, check whether your blueprint PAIRS items
   (ace#1433).** The helper assumes one entry per item unless told otherwise,
   and that under-estimates the ceiling whenever a single question genuinely
   *requires* two rules — the qualifying test is "does answering REQUIRE the
   rule", and one item can require two. On
   `bednet-check-2-visit/20260814-2019` the helper declared 0.667 the ceiling
   and the built 6-item bank measured **0.867**; the PDD had already written
   "reaching the next band would require 7 items, which the source forbids".
   If your blueprint table pairs rules on an item — an item whose key is
   unreachable knowing only one of them — pass `maxEntriesPerItem` and
   `pairedItems` (how many of the mandated items are paired, NOT all of them)
   and re-read the ceiling before reaching for a deviation. A spurious
   deviation is exactly the escape hatch ace#1250 built the channel to keep
   honest.

   Two legitimate resolutions, in order of preference:

   1. **Mandate at least `minimumItems`** — the number the check returns.
   2. **Declare the shortfall.** Write `assessment_coverage_deviation` with
      an `accepted_max_ratio` the mandate can actually reach and a `reason`
      saying why the narrow scope is correct. `pdd-to-learn-app-eval` grades
      the dimension against the declared ceiling and surfaces a `[WARN]`
      instead of a `[BLOCKER]`. A deviation claiming MORE coverage than the
      item count permits, or carrying no reason, is refused — that is an
      escape hatch, not a decision.

   Live: `bednet-check-2-visit/20260813-2333` mandated "exactly 2 questions"
   against 3 counter-intuitive rules + 7 high-consequence operations →
   weighted coverage 4/13 = 0.31 → dimension 3.0 → `[BLOCKER]` → overall 7.52
   → `fail`. It needed 4 items, or the deviation it had already argued in
   prose as D-1 but had no channel to declare.

   ```yaml
   phases:
     design:
       products:
         pdd:
           title: "Turmeric Market Survey"
           description: "FLWs visit markets to photograph turmeric vendors..."
           file_id: <fileId>
           share_mode: anyone-with-link   # step 6c plan: anyone-with-link | named-reviewers | unshared (ace#3191)
           program_parameters:
             learn_passing_score: 100
             daily_cap: 5
   ```

   Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
   `merge: 'deep'` on the current run's `run_state.yaml`. This skill is
   the sole writer of `products.pdd`, but the `design` phase block also
   carries `status`/`steps` and a sibling `products.work_order` (written
   by `pdd-to-work-order`) — so this must be a `deep` partial-patch, not
   `two-level` (which would replace the whole `design` block). #572/#587.

8. **Render the decisions log to a human-readable Google Doc** by
   invoking the `decisions-render` skill against the run-id. The
   renderer produces `ACE/<opp-name>/runs/<run-id>/decisions.gdoc`
   at one stable URL; humans review and iterate on this doc, not the
   YAML. The orchestrator also invokes the renderer at end of every
   subsequent phase, so the gdoc stays current as later phases append
   rows.

## LLM-as-Judge Rubric

Run this 6-question stress test against the drafted PDD. Each check is **pass / partial / fail**. If **two or more** checks are anything other than `pass`, the PDD is **not approved** — iterate on the weak sections and re-run the stress test before outputting.

**Check 6 (Launch readiness) is exempt from the two-or-more rule — it blocks on its own.** Checks 1-5 grade whether the design is *good*; check 6 grades whether it is *buildable and launchable*, and a PDD that Phase 4 cannot create an opportunity from is not 5/6 acceptable. One non-`pass` there is a halt (operator decision 2026-09-09).

Background and worked examples live in `docs/examples/pdd-stress-test-observations.md`. Quote specific evidence from the PDD when grading; do not grade in the abstract.

1. **Executability** — *Could an LLO read this PDD on day one and start work without asking clarifying questions?*
   Common failure modes: recruitment criteria unspecified (how is "under-vaccinated" determined? self-report vs. card vs. records), language and translation not addressed, facilitator/FLW skill level not stated, consent process missing, venue selection unspecified, participant compensation not mentioned.

   **REQUIRED — walk the form flow for ANSWERABILITY, screen by screen
   (dimagi-internal/ace#1211).** Being fully *specified* is not the same as
   being *answerable*. For each screen in the § Deliver App form flow, in order,
   confirm every field on it can be answered from what the worker knows or has
   observed **at that point in the real-world sequence**. A field whose value is
   a function of a LATER screen's answer fails this check — regardless of
   whether a recode or a relevance condition patches it downstream.

   **The recode is the tell.** A spec that assigns a value and then reassigns it
   later is asserting the first assignment was premature. On
   `hh-poverty-targeting/20260812-2034` the flow asked `visit_outcome` as a
   `select1` on screen 2 — before eligibility (4) and consent (5) — then recoded
   it on screen 6, and this self-eval graded Executability **pass** while
   *citing* §6.1 approvingly ("specified screen by screen with relevance
   conditions"). That is ace#979 reintroduced against a binding reviewer
   correction which had supplied the fix verbatim:

   ```
   visit_outcome = if(occupied='no','vacant',
                   if(eligible_respondent='no','no_eligible_respondent',
                   if(consent='no','refused','completed')))
   ```

   Catching it here is worth more than catching it downstream: Phase 3 builds
   forms directly from this section, so a miss ships a form an FLW cannot
   complete in order. Four gates missed it on that run and only Phase 2 caught
   it, incidentally.

2. **Verifiability** — *For every claimed output, is there a concrete artifact we can collect and check?*
   Common failure modes: "summary of key themes" with no format/length/template, photo capture without standardization protocol (lighting, angle, distance, color reference), self-reported education delivery with no audit mechanism, qualitative outputs with no path from raw data to AI-ingestable form.

3. **Measurability** — *Are success criteria defined for this stage, with units and targets?*
   Common failure modes: success described as "improved understanding" with no metric, sampling cap stated but no target, no per-segment or per-region targets, primary vs. secondary metrics not separated.

4. **Stage-gate clarity** — *For multi-stage PDDs, what must be true at the end of this stage to proceed to the next?*
   Common failure modes: Stage 1 → Stage 2 transition undefined, no explicit "go / no-go / iterate" criteria, downstream stage references findings the upstream stage isn't required to produce.

5. **Resource realism** — *Are the LLO's capabilities matched to what's being asked, **and does the money match the work?***
   Common failure modes: focus-group facilitation skill assumed without training, ~50 participants to recruit across 6 segments with no recruitment plan, FLW asked to make subjective research judgments (Q12/Q13-style) the artifact should answer instead, photo/data quality dependencies on equipment LLOs may not have.

   **Cost the labour, not just the capability.** This half is mandatory and
   was missing until 2026-08-14: the question asked only whether the LLO
   *could* do the work, never whether the rate covers it, so a PDD with
   uncosted labour could pass 5/5. Compute and state, in the PDD:

   - **Gross earnings per working day** at the proposed rate and daily cap.
   - **Effective earnings per day of TOTAL field time** whenever any visit
     type, travel leg, or preparation step is unpaid. Divide by all the time
     the work actually takes, not just the payable units.
   - The gap between those two numbers, stated plainly, when unpaid work is
     a material share of the day.

   Grade `partial` at best when unpaid work is material and the PDD never
   computes its effect; grade `fail` when effective earnings fall below a
   plausible local floor and the PDD does not acknowledge it. Where no
   geography is named there is no market floor to compare against — say so
   rather than assuming the rate is fine, and record it as a decision row
   with a `review_ask` (§ Asks are decision rows).

   Worked failure (`bednet-check-2-visit/20260813-2313`): R2 makes
   registration unpaid while registration is the heavier visit, so roughly
   half of a worker's field time earned nothing. Stated gross was
   USD 5.00–12.50/day; effective was USD 2.50–6.25. The PDD self-graded
   this check `pass` and the independent eval scored `resource_realism`
   6.5 — a 1.88-point self-eval gap concentrated entirely here.

6. **Launch readiness** — *Is every parameter Phase 3 and Phase 4 need decided
   HERE, or will someone have to invent it at setup time?* **This check is
   MANDATORY and it is a HARD gate: any grade other than `pass` blocks the PDD
   on its own, regardless of the two-or-more rule above** (operator decision
   2026-09-09).

   The PDD is where these get decided because it is the last point a human is
   reliably in the loop. Phase 3 builds forms from them and Phase 4 passes them
   straight into `connect_create_opportunity`, `connect_create_payment_unit`
   and `connect_set_verification_flags` — so a parameter this document leaves
   silent is not deferred, it is delegated to whichever agent notices first, or
   silently defaulted by a skill.

   Every one of these must appear as a row in § Program Parameters:

   | PDD key | Connect field it feeds |
   |---|---|
   | `payment_rate_min` / `payment_rate_max` (band), or `flw_payment_per_visit` | payment unit `amount` — FLW pay per visit |
   | `llo_payment_per_visit` | payment unit `org_amount` — LLO pay per visit |
   | `daily_cap_per_flw` | payment unit `max_daily` — daily target |
   | `total_cap_per_flw` | payment unit `max_total` — per-FLW campaign cap |
   | `campaign_target_visits` | campaign target / opportunity sizing |
   | `total_budget_usd` | opportunity `total_budget` |
   | `opportunity_start_date` / `opportunity_end_date` | opportunity `start_date` / `end_date` |
   | `verification_flags` | `connect_set_verification_flags` |

   Also confirm the Phase 3 inputs the app build cannot proceed without, where
   the archetype implies them: `learn_passing_score` + `assessment_items` when
   a gating assessment exists, and `entity_id_grain` (the payment dedup key).

   **`llo_payment_per_visit` is the one most likely to be missing, and it is
   not optional downstream.** `connect_create_payment_unit` requires
   `org_amount` for managed opportunities — the API rejects the create without
   it (`org_amount is required for managed opportunities`) — and until
   2026-09-09 the PDD vocabulary had a key for the FLW side and none at all for
   the LLO side. Half the payment model was reaching Connect as a number nobody
   had recorded a decision about.

   **Ask, then propose — do not proceed on silence.** Put these to the human
   during review. If they do not confirm a value, **propose one yourself with
   your reasoning** and get it approved; the point is that a number exists and
   someone agreed to it, not that the human types it. Never advance to Phase 3
   with the question still open.

   **Mode behaviour** — in `auto` / autonomous mode there is nobody to approve,
   so the rule adapts rather than deadlocking: write the proposed value into
   § Program Parameters marked `[PROPOSED]` with provenance
   `derived: <that row's id>`, record the matching `decisions.yaml`
   row with `evidence_basis: inferred` plus reasoning, and flag it
   **unapproved** in the phase summary so the Phase 1→3 pause point surfaces
   it. A proposal on the record is auditable; a silent default is not. In
   interactive / review mode the gate is real: stop and ask.

   *Enforced:* `idea-to-pdd-qa § launch_parameters_present` (check 0, runs
   first) fails the PDD when any row is absent. `[PROPOSED]` / `[TBD]` values
   pass that check by design — it enforces that the parameter was considered
   and written where Phase 4 will look; sign-off is tracked separately via
   `evidence_basis`.

**Grading anchors (worked examples):**

The vaccine-hesitancy PDD at `docs/examples/pdd-vaccine-hesitancy.md` is the canonical "fail" case. Expected grades:
- Executability: **fail** — recruitment, language, facilitation, consent, venue all underspecified
- Verifiability: **fail** — "summary of key themes" output spec is too thin to verify
- Measurability: **partial** — Stage 2 has metrics, Stage 1 does not
- Stage-gate clarity: **fail** — Stage 1 → Stage 2 transition undefined
- Resource realism: **partial** — facilitation skill assumed; ~48-person recruit unscoped

The turmeric-market-survey PDD at `docs/examples/pdd-turmeric-market-survey.md` is the canonical "near-pass" case. Expected grades:
- Executability: **partial** — "market" is free text but the cap depends on market identity
- Verifiability: **partial** — photo standardization protocol missing; vendor education self-report unverifiable
- Measurability: **partial** — caps stated, sampling targets missing
- Stage-gate clarity: **pass** — single stage
- Resource realism: **pass** — atomic-visit pattern is well-matched to FLW capability

Both PDDs fail the rubric in their current form. Surface specific failures and either (a) iterate on the PDD to fix them, or (b) in review mode, hand off to a human with the failure list attached.

<!-- 0.13.116: ## Gate Brief section removed. The orchestrator composes
a pause-time summary at the Phase 1→3 Pause Point from this skill's
QA verdict + eval verdict directly (per `agents/ace-orchestrator.md §
Pause Points`). The producer no longer authors a separate gate-brief
artifact. -->

## Asks are decision rows (the open-questions ledger is retired)

`ACE/<opp-name>/open-questions.md` is no longer written — by this skill or
any other (owner decision 2026-10-04,
`docs/superpowers/specs/2026-10-04-open-questions-into-decisions-design.md`).
Its job is done by the decisions log. Measured on spark-facilitator, 31 of the
ledger's 32 open rows were already decisions, defaults the build took without
a row, future-phase questions, or not decisions at all. Keeping two stores
asked reviewers twice and let the ledger drift from the run it was shown
with.

**The producer rule: a default you build on is a decision row.** Whenever
this skill would once have "raised an open question", it writes a decision
row instead (`skills/_decisions-review-fields.md § The producer rule`;
`docs/decisions-contract.md § The producer rule`):

- the working answer the PDD builds on goes in `ai-default`, with the
  alternatives in `options`;
- where the sources do not settle it, add `review_ask`
  (`recommended-confirmation`, or `required-before` + `needed_by` when no
  default is safe past a gate — e.g. an answer that changes who may be
  awarded), `confirm_reason`, `owner`, `needed_by` and `answer_channel`;
- a question this pilot does not need answered is `status: deferred` with
  `revisit_when`;
- a chore goes to `phases.idea-to-design.residuals`, an upstream request to
  an issue in the owning system's tracker (cited from the row it affects),
  and a factual partner input to a solicitation question
  (`answer_channel: solicitation:<question-id>`).

The PDD's own `## Open Questions` section may still list the asks for the
reader of the PDD, but every item in it must also be a decision row: the
decisions review in ace-web is where a reviewer answers it, and an item that
lives only in the PDD reaches nobody.

**What a reviewer sees is held to the plain-language gate** —
`plain`, `plain_question`, `confirm_reason` and `revisit_when` are written for
the named `owner`, with no field ids, file names, run ids, issue numbers, tool
names or `§` references (`docs/decisions-contract.md § Plain-language gate`).
The verbatim spark rows that taught this, and their plain rewrite:
`test/fixtures/open-questions/spark-facilitator-outsider-{jargon,plain}.text-markdown.md`.

**Durability across runs.** Answers persist through
`inputs/decision-overrides.yaml` and bind at the write boundary. Unanswered
asks are re-derived by every run from the design and inputs. Open asks are a
filter over decision rows, never a file (operator decision 2026-10-07,
ace#2757): as a safety net, after Phase 1 the orchestrator filters the
PREVIOUS run's decisions log the same way and checks its asks against this
run's rows; an ask you did not re-derive comes back as a run residual. No
value is ever read out of the previous run.

**Legacy ledgers** are never read by a run. `scripts/migrate-open-questions.ts`
is the only code that opens one, to fold it into decision rows once.

## Decisions Log (rendered)

The skill always emits `decisions.yaml` and invokes `decisions-render`
to produce a prose Google Doc rendering at one stable URL
(`ACE/<opp-name>/runs/<run-id>/decisions.gdoc`). The YAML lives at
`ACE/<opp-name>/runs/<run-id>/decisions.yaml`; the gdoc is its
human-friendly rendering and is regenerated after every phase. The
orchestrator's pause-time summary at the Phase 1→3 Pause Point
includes a `Decisions Log: <gdoc-url>` line.

## Decisions Log Convention

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. Mark a value outside ACE's authority that no `PROPOSED` tag covers with `review_ask: recommended-confirmation` + `confirm_reason`; every `[PROPOSED]` program parameter is asked about automatically once the build configures it. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

Every Phase 1 run emits `ACE/<opp-name>/runs/<run-id>/decisions.yaml`
with a calibrated set of load-bearing default-decisions the skill applied
while drafting the PDD. The log is the per-run audit trail and the
human-iteration surface — humans edit it (via the renderer + sync skills
landing in PRs #2–#4) to redirect a subsequent run's PDD draft.

### Bar criterion — what counts as a row

Two filters, both must be true:

1. **Load-bearing.** A reasonable person could pick differently AND it
   materially shapes downstream phases or eval scores.
2. **Maps to a known surface.** The default ties to one of: an
   `*-eval` rubric dimension, an `*-qa` structural check, a Phase
   Write-Back field that downstream phases read, or a numeric / named
   entity surfaced in the PDD body.

Form-field-level choices, Connect program slugs, email copy, font sizes
— below the bar.

### Common load-bearing decisions for Phase 1

These rows commonly qualify under the bar criterion for Phase 1 — a
working template, not a required set. The skill applies the bar
criterion and emits whatever rows meet it; this catalog is a teaching
device that improves over time as we learn from runs. Five rows are
marked `(eval input)` because `idea-to-pdd-eval`'s viability axis
(PR #144) grades on those specific decisions — when they're present in
the log, the rubric has structured input instead of grading on PDD
prose.

The catalog branches on archetype. The **base table** rows fit every
archetype; the per-archetype tables below it add rows that are
load-bearing for that archetype and meaningless for others (e.g.
`ai-photo-threshold` doesn't apply to FGDs; `submission-window`
doesn't apply to atomic visits). Emit base rows on every run, plus
the matching archetype's rows; skip a row when it's not applicable
to the opp; add others not listed when they meet the bar.

**Base (all archetypes):**

| ID | Question | Map to surface |
|---|---|---|
| `archetype-selection` | Which delivery archetype best fits? **Options:** `atomic-visit` · `longitudinal-visits` · `focus-group` · `multi-stage` | `archetype_coherence` (eval input) |
| `budget-plausibility` | Is the budget plausible for implied labor + AI infra? | `resource_realism` (eval input, PR #144) |
| `named-downstream-consumer` | Pre-committed downstream consumer? | `demand_reality` (eval input, PR #144) |
| `primary-metric-vs-goal` | Does the primary metric measure the goal itself, or a proxy upstream of it? **Options:** `direct-goal` · `upstream-proxy` | `mission_alignment` (eval input, PR #144) |
| `ai-fallback-design` | True validation harness or parallel sampling? | `fallback_validates_primary` (eval input, PR #144) |
| `flw-count` | How many FLWs? | PDD `FLW Requirements` numeric |
| `working-language` | Working language(s) + CommCare language code? Who reviews the translations? | PDD `Learn App Specification` |
| `verification-layers` | Which evidence-model layers are in scope? Qualifiers ("Layer C partner-led", "largely unavailable") go in `params.caveat`, never in the value. **Options:** `A` · `A+B` · `A+B+C` | PDD `Evidence Model` section |
| `solicitation-type` | Which solicitation kind? **Options:** `EOI` · `RFP` · `custom` | PDD `Solicitation` section |
| `solicitation-deadline` | How long from publish to deadline? **Options:** `7-days` · `14-days` · `21-days` · `30-days` | PDD `Solicitation` section |
| `candidate-llo-roster` | Named candidates, public listing, or both? WHICH orgs are named goes in `params.named`. **Options:** `public-only` · `named-plus-public` · `named-only` | `LLO Preference` named entity |

**These base rows are `value_set_by: external` — always.** Their real value is
fixed by a solicitation response, a contract, or deployment, never by ACE:
`flw-count`, `payment-rate`, `budget-plausibility`, `named-downstream-consumer`,
plus the work-order rows `wo-period-of-performance` and
`wo-total-not-to-exceed-usd`. Still emit your best estimate as `ai-default` and
keep going — but tag them `external` so the estimate is not read downstream as a
commitment. Measured across 22 runs of two opps, these are precisely the rows
that produced a different confident-looking number on nearly every run.

Everything else in the base table is `value_set_by: ace`.

**`atomic-visit` (additive):**

| ID | Question | Map to surface |
|---|---|---|
| `payment-rate` | Per-visit payment rate band (range, not fixed) to propose to the LLO. The PDD captures a target range or anchor + rationale; the actual rate is **negotiated via the solicitation response** where the LLO proposes a number with justification. | PDD `FLW Requirements` numeric (range or band) |
| `pilot-sample-size` | Pilot sample size for AI calibration? | `verifiability` rubric |
| `ai-photo-threshold` | AI auto-accept confidence threshold? | `verifiability` rubric |
| `gps-verification-radius` | Acceptable GPS radius (meters) for visit-at-location? | `verifiability` rubric |
| `duplicate-detection-key` | What constitutes a duplicate? The exact field list goes in `params.key_fields`. **Options:** `identifier-only` · `identifier-plus-gps-radius` · `identifier-plus-ranked-proximity` · `gps-only` | PDD `Evidence Model` Layer A |
| `per-visit-daily-cap` | Daily / weekly cap per FLW? | PDD `FLW Requirements` numeric |

**`longitudinal-visits` (additive):**

| ID | Question | Map to surface |
|---|---|---|
| `longitudinal-entity` | What entity is followed over time, and what case type represents it? | PDD `Entity Lifecycle` + § Program Parameters `followed_entity_case_type` (ace#2889) |
| `entity-registration-path` | Registered by a separate form, by the first visit, or already existing in the partner's system? | PDD `Entity Lifecycle` + `pdd-to-deliver-app` case ops |
| `visit-sequence-and-cadence` | Expected visits, their order, and the interval — including any change in cadence across the arc. | PDD `Entity Lifecycle` |
| `payability-against-history` | Is the same activity twice payable? An out-of-order visit? A per-entity cap over a window? **Never leave unanswered** — silence degrades Layer A to "any visit counts" (ace#1462). | PDD `Evidence Model` Layer A |
| `payment-unit-entity-id` | The Connect dedup business key expressing the row above. Default for this archetype: `concat(<case_id>, '-', <activity_code>)` = one entity row per activity per entity. The key GROUPS visits; it does not stop a repeat being paid (ace#2512) — any per-entity cap needs a Connect-side stop (`payable_slot` form rule or payment-unit caps). Never the case id alone (that folds the whole arc onto one entity row). | `connect-opp-setup` Connect form; `pdd-to-deliver-app` §entity_id |
| `case-state-read-write` | What each visit preloads from the case and writes back. | `pdd-to-deliver-app` case ops |
| `visit-ownership` | Payable only from the FLW who owns the case, or from any FLW? | PDD `Evidence Model` Layer A |
| `progression-affects-payment` | Does a stalled entity affect payment, or is progression monitored only? | PDD `Evidence Model` + `Success Metrics` |
| `entity-completion` | What "complete" means for an entity, and what happens to the case then. | PDD `Entity Lifecycle` |
| `payment-rate` | Per-visit payment rate band (range, not fixed) to propose to the LLO — same negotiation principle as `atomic-visit`. | PDD `FLW Requirements` numeric |

**`focus-group` (additive):**

| ID | Question | Map to surface |
|---|---|---|
| `payment-unit-model` | Per-session attestation-form payment via Connect deliver_unit (default) vs per-month invoice via Connect web (rare)? | PDD `Budget` + `connect-opp-setup` payment unit |
| `per-session-rate` | Per-verified-session rate band (range, not fixed) for facilitator + notetaker. Same negotiation principle as `payment-rate` — PDD captures a range with rationale; LLO proposes a number in their solicitation response and explains why. The awarded LLO's proposed rate becomes the actual `connect.deliver_unit` payment_unit amount at Phase 4 setup time. | PDD `FLW Requirements` numeric (range or band) |
| `facilitator-training-stipend` | Flat training stipend on **practice-session-pass** (coordinator-graded audio review). Note: not Learn-app completion — focus-group archetype has no Learn app. | PDD `FLW Requirements` numeric |
| `gdoc-content-template` | What sections / fields should the facilitator's gdoc contain? Default: the PDD's Output Specification verbatim. Where does the gdoc template live (a template URL the facilitator copies, or a free-text starting point)? | PDD `Output Specification` |
| `participant-compensation-cap-usd` | Per-participant compensation USD-equivalent cap? | PDD `Budget` numeric |
| `submission-window` | Hours between session end and **attestation form** submission. Gdoc submission window may differ — default: same. | PDD `Evidence Model` Layer A |
| `audio-min-duration` | Minimum audio duration for a session, captured out-of-band (audio is not in the CommCare form). Tracked for coordinator gdoc review, not for Layer A. | PDD `Facilitation Protocol` |
| `audio-consent-fallback` | What happens when one participant declines audio recording? (Audio is out-of-band — this is a facilitator protocol decision, not a CommCare form behavior.) | PDD `Facilitation Protocol` |
| `gps-verification-radius` | Acceptable GPS radius (meters) for the attestation form's `gps` field to clear Layer A as "at the planned venue"? | PDD `Evidence Model` Layer A + `connect-opp-setup` verification flags |
| `gdoc-submission-window` | Hours allowed between attestation submission and gdoc receipt (coordinator follow-up trigger). Default: same as `submission-window`. | PDD `Evidence Model` Layer B + coordinator workflow |
| `notetaker-required` | Is a separate notetaker required? Always / when audio recording / never? | PDD `Facilitation Protocol` |
| `venue-acceptable-list` | Which venue types are acceptable / disallowed? | PDD `Facilitation Protocol` |
| `site-selection` | Sites pre-named in PDD, or deferred to solicitation review? | PDD `Target Population` + `solicitation-review` |
| `payment-unit-entity-id` | `entity_id` is a business key (Connect's dedup grain), never the case id. Default `concat(username, today())` = one entity row per facilitator/day (a same-day repeat is still paid unless `max_daily` = 1 — ace#2512); if ≥2 sessions/day per facilitator, override to a finer-grained business key (e.g. `concat(username, '-', session_date, '-', venue)`). Affects payment collapse. | `connect-opp-setup` Connect form; `pdd-to-deliver-app` §entity_id |
| `saturation-early-stop` | Threshold + sign-off for stopping the pilot before the planned session count? | PDD `Success Metrics` |

**`multi-stage` (additive):**

| ID | Question | Map to surface |
|---|---|---|
| `stage-gate-criteria` | What must be true at the end of stage N to proceed to N+1? | PDD `Stage Gate` per stage |
| `per-stage-archetype` | Which archetype for each stage? | Per-stage Archetype declaration |
| `stage-launch-policy` | Does stage N+1 launch before stage N is fully reviewed, or after? | PDD `Timeline` |

The bar criterion alone determines what rows belong in the log — the
tables above are teaching templates that improve over time.

**Rows above that carry an `**Options:**` annotation are CATALOGUED** in
`lib/decision-vocabularies.ts`: that option set is closed, the atom
rejects anything outside it, and the printed values are the declared
vocabulary verbatim. Every other id in these tables is unconstrained —
choose its options to fit the opp. See § Schema and write semantics §
The vocabulary contract.

### Schema and write semantics

Schema is defined in `lib/decisions-schema.ts` (`DecisionRowSchema` /
`DecisionRowStrictSchema` / `DecisionsLogSchema`, v4), and the closed
option sets for the recurring decisions in `lib/decision-vocabularies.ts`
(`DECISION_VOCABULARIES` / `checkVocabulary`). Do not
hand-construct YAML — call the `decisions_append_rows` MCP atom
(ace-decisions server). The atom's input schema is
`DecisionRowStrictSchema` (the strict write-boundary variant), so
unknown / misspelled field names AND violations of the load-bearing
invariants below are rejected at the call boundary before they touch
Drive.

**The vocabulary contract (load-bearing) — read this before writing any
row.** `lib/decision-vocabularies.ts` anchors a handful of decision ids
to a **closed option set**, and the atom enforces it:

- **An id ABSENT from `DECISION_VOCABULARIES` is unconstrained.** The bar
  criterion has to let a skill raise a row nobody anticipated, and that
  must stay possible — invent the id, invent its options, write it.
- **An id PRESENT in `DECISION_VOCABULARIES` MUST draw its `options` from
  the declared set, verbatim.** A subset is fine (not every archetype
  applies to every opp); a stray member is not. Wording, qualifiers and
  specifics belong in `reasoning` or `params` — `params.caveat` for a
  hedge ("pending Nigerian data-protection confirmation"),
  `params.named` for the orgs behind `named-plus-public`,
  `params.key_fields` for the field list behind a duplicate key.

Grep `lib/decision-vocabularies.ts` for the current set rather than
trusting a list pasted anywhere — that file is the authority, and the
catalogue tables above print each catalogued id's vocabulary inline for
exactly this reason. *Enforced:* `checkVocabulary` at the atom boundary,
and `test/skills/decisions-vocabulary-drift.test.ts` on the docs.

**The rejection is ATOMIC — one stray string costs the whole batch.**
`decisions_append_rows` validates every row before writing any, so a
31-row call with one prose option for `verification-layers` writes
nothing and must be re-sent in full (~14k tokens, twice, on
`poverty-graduation/20260905-0924`). Check the catalogued ids in your
payload before you send it, not after (ace#1994).

**`rows:` is the ATOM ARGUMENT, not the file's top-level key.** The
`decisions_append_rows` call takes `rows: [...]` (the array of new rows
to append), but the persisted `decisions.yaml` is keyed `decisions:` at
top level — `DecisionsLogSchema` in `lib/decisions-schema.ts` is
`{ schema_version, decisions: [...] }`. `decisions-render` /
`render_decisions_log` and ace-web's parser read `decisions:` and reject
a file whose top-level key is `rows:`. Do not confuse the two: the atom
example below shows `rows:` because that is the argument name; the file
on Drive uses `decisions:`.

**If `decisions_append_rows` is unavailable this session** — the
`ace-decisions` MCP failed to bind at session start (the same
session-binding class as the ace-mobile / Nova gotchas; confirm by
checking whether any `decisions_*` atom resolves via `ToolSearch`) — then
the atom path is closed and you must hand-write `decisions.yaml` in the
**persisted** shape (top-level `decisions:`, NOT `rows:`):

```yaml
schema_version: 4
decisions:
  - id: archetype-selection
    phase: 1-design
    skill: idea-to-pdd
    question: Which delivery archetype best fits the intervention?
    ai-default: atomic-visit
    options: [atomic-visit, longitudinal-visits, focus-group, multi-stage]
    source: idea.md §1
    status: ai-default
    evidence_basis: stated
    value_set_by: ace
    reasoning: Single per-FLW visit producing one structured delivery.
```

Each row obeys the identical field contract documented below; only the
container key differs from the atom argument (`decisions:` list in the
file, `rows:` array in the atom call). Prefer the atom whenever it
resolves — hand-writing skips the strict write-boundary validation, so
re-validate against `DecisionsLogSchema` mentally before saving. (This
exact `rows:`-vs-`decisions:` confusion bit a hand-written fallback when
`ace-decisions` was unbound — jjackson/ace#782.)

**The `value_set_by` contract (load-bearing, v5).** Every row MUST also
declare `value_set_by`: `ace` or `external`. It answers a different
question from `evidence_basis` — not *how well-grounded is this default*
but *whose value is it in the end*.

- **`ace`** — ACE's judgment to make from the source material. Archetype
  selection, verification layers, solicitation type. A reviewer may
  override it; a later run may decide it better.
- **`external`** — the real value gets fixed later by someone else: a
  rate negotiated in a solicitation response, dates set on contract
  execution, an FLW count set at deployment.

**`external` does not defer, escalate, or block anything.** ACE still
picks a value, still writes it as `ai-default`, and the run still
proceeds — exactly as before. `"open"` is still not a valid `status`,
and there is deliberately no `needs-human`. The flag exists so a
downstream phase does not cite a projection as a settled commitment, and
so a later run re-deriving it differently reads as *expected* rather
than as drift.

**Why it was added.** Measured across 22 runs of two opportunities,
`flw-count`, `payment-rate`, `wo-period-of-performance` and
`wo-total-not-to-exceed-usd` produced a different confident-looking
answer on nearly every run. ACE had originally got this right and had
nowhere to put it: hh-poverty run `20260702-1456` wrote *"Deferred to
deployment (Annex B); negotiated via solicitation response"* **inside
the `ai-default` string** on four rows. Prose in a value field is
invisible to every consumer, so within a few runs all four had become
specific numbers.

Note the name: **`value_set_by`, not `resolved_by`** — `resolved_by`
already means something else in this skill (which run closed an
open-question, § Open questions), and the collision would be silent.

**The `evidence_basis` contract (load-bearing, v4).** Every row MUST
declare `evidence_basis`: one of `stated`, `inferred`, or `conflicting`.
This is the forcing function that stops Phase 1 from silently resolving a
contested fork and presenting it as a confident, single-cited default —
the highest-leverage failure mode in the whole lifecycle, since every
downstream phase builds on the PDD.

- **`stated`** — the chosen value is directly stated in a source input.
  `source` cites where.
- **`inferred`** — no source states it; this is a reasoned default the
  AI extrapolated. Say so in `reasoning`. (The cadence "visited twice"
  was stated in the ITN source; the *distinct Visit-2 form content* ACE
  then built was `inferred` — and should have been tagged as such.)
- **`conflicting`** — the source signals **disagree**, and this row
  resolves the conflict. You MUST populate `conflict_signals` with **≥ 2
  entries**, one per competing reading, each citing where it came from.
  Put *why this resolution won* in `reasoning`. Canonical case: the ITN
  app-spec described **one** visit instrument (Sections 1–6) yet
  separately said households are **"visited twice"** — a genuine conflict
  that was silently resolved into two distinct forms with no audit trail.

When in doubt between `stated` and `inferred`, prefer `inferred` — and if
*any* source pulls against the default, it is `conflicting`, not
`inferred`.

**Whose sources disagree decides the basis (ace#2266).** `conflicting` means
the AUTHOR's material disagrees with itself; it is the row a reviewer is asked
to look at. Classify by the owners of the competing signals:

| Competing signals | `evidence_basis` | `conflict_owner` | Surfaced to the author? |
|---|---|---|---|
| Author document vs author document — **including the programme source vs its own instrument** | `conflicting` | `author` | Yes, with both signals |
| An ACE default or skill rule vs a `[FIXED]` author instruction | `stated` — cite the instruction; note the losing ACE default in `reasoning` | — | No. The PDD governs; a losing ACE default is a skill defect to file, not a review item |
| ACE artifact vs ACE artifact (two skill docs, a Phase 3 memo vs Phase 4 config) | not a Phase 1 row; if one must be recorded, `conflicting` with `conflict_owner: ace` | `ace` | No. If it hides a real author question, raise THAT question on its own row |

Canonical under-flagged case, bednet-check-2-visit/20260907-1126:
`inputs/idea.md § Program intent` says FLWs distribute the nets, while the
visit-1 instrument has **no handover step** and records the net date as
*"today or earlier"*. The instrument is the stronger evidence and the
resolution (nets are distributed separately) was right — but the row shipped
`stated`, so nobody reviewing the Work Order could see that `"a separate
distribution activity"` was resolving a contradiction (and that *"today or
earlier"* permits a same-day handover). Source vs instrument is the author's
own contradiction: `conflicting`, `conflict_owner: author`, both readings in
`conflict_signals`, and why the instrument won in `reasoning`. The
over-flagged mirror, poverty-graduation/20260908-0510: 9 of 66 rows were
`conflicting`, but only 3 were author-vs-author; `cs-payment-unit-shape` (an
ACE skill rule vs the PDD's [FIXED] §12.2) should have been `stated`.
*Enforced at the write boundary:* `conflict_owner` is refused on any
non-`conflicting` row (`lib/decisions-schema.ts`). Do not omit `conflict_signals` on a `conflicting` row, and do
not attach them to a non-conflicting one; both are rejected at the write
boundary.

**The `ai-default` contract (load-bearing).** Every row's `ai-default`
MUST be one of the literal strings in its `options` array, exact-match.
Same for `override` when `status: overridden`. Rationale goes in
`reasoning` (AI side) or `override_reasoning` (human side); citations
go in `source`. Never put prose, qualifications, or rationale into
`ai-default` itself.

Why this matters: ace-web's decisions UI renders each option as a
clickable pill, highlights the pill whose text matches the row's
effective value (`override` if present else `ai-default`), and lets the
human override by simply clicking another pill. The frontend keys the
selection off exact string equality, so any prose extension or
categorical drift in `ai-default` leaves no pill highlighted and breaks
the click-to-override flow. The Zod schema's rejection message names
both the violating value and the expected `options` array so the agent
can self-correct on retry.

The pattern is: pick the option whose text best fits the answer, copy
that string verbatim into `ai-default`, and put the explanation in
`reasoning`. If none of the options fits, the `options` set is wrong —
add another option that matches what the AI is trying to say, **unless
the id is catalogued in `lib/decision-vocabularies.ts`**. For a
catalogued id the option set is closed and adding to it is exactly what
gets the write rejected: pick the nearest declared member and put what
you were trying to say in `reasoning` or `params` (see § Schema and
write semantics § The vocabulary contract). If no declared member is
even close, that is a signal the vocabulary is wrong — file it against
ACE rather than routing around it in the payload. Sibling
skills (`pdd-to-work-order`, `connect-opp-setup`, `ocs-agent-setup`,
`synthetic-narrative-plan`, `solicitation-create`, `app-test-cases`,
`pdd-to-deliver-app`) inherit this contract via this canonical doc —
no copy-paste needed in their own SKILLs.

Tool call (idiomatic shape for this skill):

```
decisions_append_rows({
  runFolderId: <run-folder file_id resolved at run start>,
  opportunity: <opp-slug>,
  run_id: <run-id>,
  rows: [
    {
      id: "archetype-selection",
      phase: "1-design",
      skill: "idea-to-pdd",
      question: "Which delivery archetype best fits the intervention?",
      "ai-default": "atomic-visit",
      options: ["atomic-visit", "longitudinal-visits", "focus-group", "multi-stage"],
      source: "idea.md §1; one-FLW-one-delivery pattern",
      status: "ai-default",
      evidence_basis: "stated",
      plain: "Each household is visited once; there is no follow-up visit.",
      value_set_by: "ace",
      reasoning: "Single per-FLW visit producing one structured delivery."
    },
    {
      id: "visit-cadence-and-form-model",
      phase: "1-design",
      skill: "idea-to-pdd",
      question: "How many visits per household, and is each a distinct form?",
      "ai-default": "Two distinct forms (V1 + V2)",
      options: ["One instrument administered twice", "Two distinct forms (V1 + V2)"],
      source: "ITN Exploration App doc",
      status: "ai-default",
      evidence_basis: "conflicting",
      plain: "Each household is visited twice, and each visit has its own form.",
      conflict_signals: [
        "Exploration App § Visit structure: describes ONE instrument (Sections 1-6); no distinct Visit-2 content",
        "Exploration App § Open-Q4 + Photos: households are 'visited twice' / 'across both visits'"
      ],
      reasoning: "Source confirms a two-visit cadence but never specifies distinct Visit-2 content; picked two forms to model retention, flagging that the Visit-2 content is inferred, not sourced."
    },
    ...
  ]
})
```

The atom seeds a fresh v4 log header (`schema_version`, `opportunity`,
`run_id`, `generated_at`) on the first call and is idempotent: rows
whose `id` is already in the log are silently skipped and returned in
`skipped[]`, so a retry never duplicates rows.

This skill writes only `status: "ai-default"` rows. `overridden` rows
appear when a prior run's human edits carry forward via the fork
endpoint's `keep-all` or `keep-overrides-only` mode. The canonical
worked fixture is `test/skills/idea-to-pdd/fixtures/turmeric-decisions.yaml`
— useful as a reference shape, not as something to copy into Drive.

## Archetypes

ACE skills branch on the PDD's declared `archetype:` field. This skill generates archetype-appropriate sections during step 4 (Draft).

### `atomic-visit` (default)
The PDD describes one FLW visit producing one structured delivery (photo + GPS + form). Use the base sections as-is. Examples: turmeric market survey, household-level data collection.

**Additional questions to answer in step 3:**
- What is the exact form structure (every field, every type)?
- What's the standardization protocol for any photo/measurement (lighting, angle, distance, color reference)?
- What's the per-FLW daily cap, and the per-FLW total for the whole opportunity?
  These are the only two caps Connect enforces — they land as a payment unit's
  `max_daily` and `max_total`, both scoped **per worker**. A campaign-wide visit
  total is not a field: it is carried by `total_budget`, because Connect derives
  `number_of_users = total_budget / Σ(max_total × (amount + org_amount))`.
  **Do NOT specify a per-location cap** (per market, per village, per facility).
  Nothing can enforce one: Connect caps per worker rather than per place, and a
  CommCare form cannot count other workers' submissions — they are offline until
  sync. A PDD that states one commits the programme to a rule the platform will
  not keep, and over-cap visits still get paid. If a deployment genuinely needs
  to spread coverage across locations, write it as LLO supervisory practice in
  the operations guidance, never as a Program Parameter or an FLW-facing rule.
- How is duplicate detection handled (vendor ID, stall number, GPS resolution)?

### `longitudinal-visits`

The PDD describes **repeat visits to a durable entity over time** — a
community, household, patient, farm, savings group — where the entity
persists between visits, carries state, and the visits are ordered. This
is CommCare case management: a case type, a registration form, and
follow-up forms against a case list.

The paid unit is still one visit producing one structured delivery, as in
`atomic-visit`. **What differs is that a visit's validity can depend on
the entity's history** — whether this activity has already been
delivered to this entity, whether the sequence is advancing, whether the
visit came from the FLW who owns the case.

**Choose this over `atomic-visit`** whenever the same subject is visited
more than once and the visits are not interchangeable. The tell is that
someone in the program can ask *"is this community/household on track?"*
— a question `atomic-visit` cannot answer, because it has no entity to
track. `atomic-visit`'s duplicate-detection question is framed purely
cross-sectionally ("vendor id, GPS bucket, household id" — *is this the
same subject as some other submission*); it cannot express *duplicate
within this entity's own sequence*.

**Choose this over `multi-stage`** whenever the entities progress
**independently and asynchronously** through the same activity type.
`multi-stage` stages the *program*: one clock, the whole cohort advances
together through a management go/no-go gate, and it builds one Learn app,
one Deliver app and one payment unit **per stage**. `longitudinal-visits`
stages the *entity*: N clocks running at their own pace, one Learn app,
one Deliver app and one payment unit for the whole arc, and the gate is
data written by the visits themselves. Same word "stage", different
subject — picking `multi-stage` for an entity-asynchronous program builds
a fan-out of apps nobody needs and announces "Stage 2 is live" to a
cohort that is not uniformly in Stage 2.

**The `entity_id` lever — read this before writing the Evidence Model.**
Connect's grouping grain is `entity_id`, an arbitrary business key
(see `payment-unit-entity-id` in the decisions table): it decides which
`CompletedWork` row a visit lands on. That is what makes this archetype
implementable today with no new platform capability:

- `atomic-visit` sets it cross-sectionally — `concat(username, today())`
  = one entity row per FLW per day.
- **`longitudinal-visits` sets it to entity + sequence position** — e.g.
  `concat(<case_id>, '-', <activity_code>)` = one entity row per activity
  per entity, for the life of the case.

**The key groups; it does not cap.** A repeat on an existing key is NOT
collapsed into the earlier payment: with the `duplicate` flag off — always,
on ACE opportunities — Connect resets it to `pending`, auto-approves it and
pays it again (ace#2512; source cited in `playbook/integrations/connect-api.md
§ A repeated entity_id is PAID AGAIN`). So every "at most N paid" rule in
Layer A must name a Connect-side stop: `max_daily` / `max_total` on the
payment unit, or a computed form field (e.g. `payable_slot`, `yes` only for
an in-cap payable encounter) plus the `form_field_rules` row Phase 4 adds
requiring it. And because every visit on the paid deliver unit counts toward
`max_daily` / `max_total` whether payable or not, **record kinds the design
does not pay for (committee meetings, did-not-happen reports) go on a form
with no `deliver_unit` marker**, or the caps must be sized for them. Never
write "Connect pays each key once" or "collapses to a single payment" in the
PDD (ace#2512) — the Work Order copies it and the partner signs it.

If the Evidence Model does not say which longitudinal facts Layer A
reads, this archetype degrades silently into `atomic-visit` — the PDD
prose stays longitudinal-aware while the payment predicate quietly
becomes "any visit counts." That is a real, measured failure
(`spark-facilitator/20260813-2126`, ace#1462), and it is the specific
thing this archetype exists to prevent.

**A stateless followed entity is legitimate — declare it, never invent
states (ace#2774).** "Carries state" above is the common case, not a
requirement. A durable entity can be revisited repeatedly where every visit
is the same activity and nothing progresses — a savings group paid per
weekly session for two years, a group record paid per session
(`group-payment-test/20261007-1700`). That is still `longitudinal-visits`
(durable case, case list, per-entity history for Layer A), NOT
`atomic-visit`. Write `| entity_state_taxonomy | stateless [source: <doc>] |`
in § Program Parameters when, and only when, the source material names no
phase / stage / status vocabulary for the entity AND nothing in the design
(payment, eligibility, the case list, a success metric) depends on one.
`parseStateTaxonomy` reads it as declared with zero states, `idea-to-pdd-qa`
check 10 passes it, and Phase 3 builds no state field. Do not use it to dodge
a vocabulary the source does carry, and do not write `none` / `n/a` — those
read as an unfilled row and fail.

**Every paid form records the followed entity's id (ace#2889).** Write the
followed entity's case type as `| followed_entity_case_type | <case_type> |`
in § Program Parameters (required for this archetype and for `multi-stage`;
`idea-to-pdd-qa` fails its absence). It is the entity the PROGRAMME follows,
not whatever case a form happens to update: on a child-case design (crop
cycles, sessions or pregnancies under a woman) it is the parent. Phase 3
records that id in a hidden `<case_type>_case_id` on every paid form and
`app-release-qa` fails a paid form without it — on
`smallholder-seasonal/20261012-1549` the paid Harvest visit updated the crop
cycle and named nothing that identified the woman, so no report could
attach it to her. If some paid visit genuinely serves no followed entity, say
so in the Deliver spec; the build records that form as an explicit exemption,
never a silent gap.

**Additional questions to answer in step 3:**

- **The entity**: what is followed over time, what case type represents
  it, and what identifies one instance?
- **Registration**: is the entity registered by a separate form, by the
  first visit, or does it already exist in the partner's system (and if
  so, how does the case get created — import, sync, or re-registration)?
- **Expected sequence and cadence**: what visits are expected, in what
  order, at what interval — and does the cadence change across the arc?
- **State read and written**: what does each visit preload from the case,
  and what does it write back? (This is what makes progression
  measurable at all.)
- **Payability against history**: is the same activity twice payable? Is
  an out-of-order visit payable? Is there a per-entity cap over a
  window? **Answer this explicitly — silence here is what produces
  "any visit counts."**
- **`entity_id` composition**: the business key that expresses the
  answer above (see the lever, above).
- **Ownership**: is a visit payable only from the FLW assigned to that
  case, or from any FLW?
- **Progression vs payment**: does a stalled entity affect payment, or
  is progression monitored only? (Both are legitimate; leaving it
  undecided is not.)
- **End of arc**: what does "complete" mean for an entity, and what
  happens to the case — graduation, handover, closure?

**Additional sections to include in the PDD draft:**

- **Entity Lifecycle** — the entity, its states/phases, what moves it
  between them, the expected visit sequence, and what completion means.
- The **Evidence Model** gains an explicit *longitudinal clause* under
  Layer A: which case facts the payment predicate reads, and the
  resulting `entity_id`. A Layer A that reads only the current form's
  fields is the degradation described above.

### `focus-group`

The PDD describes FLW-facilitated group discussions producing qualitative
content. **The FGD operational model is attestation-form-only on
CommCare; all qualitative content (themes, quotes, post-section
summaries, post-FGD report, facilitator reflection) is captured
out-of-band in a Google Doc.** Facilitator training is correspondingly
out-of-band — OCS chatbot + handbook gdoc + coordinator-graded
practice-session audio review. No Learn app is produced. See
`docs/superpowers/specs/2026-05-15-focus-group-archetype-redefinition.md`.

**Additional questions to answer in step 3:**

- **Recruitment**: Who are the segments? How will participants be identified? What sample size per segment? Comparison groups and their justification?
- **Language**: Working language, and its CommCare language code? Facilitator language fluency? (The APP is now translated into the working language on top of an always-complete English source — PR #1463, superseding ace#968/#1391, 2026-08-17. Also ask which OTHER surfaces need the working language: training materials, facilitation, OCS chatbot. Translations are ACE-authored and carry `needs-review` — ask who reviews them, same as you would for the English.)
- **Facilitation skill level**: Existing skill assumed, or training required? Training surface is the per-opp **OCS chatbot** (loaded with the FGD Guide + Output Specification + handbook gdoc) plus a coordinator-graded practice-session audio review. The Learn app produced for focus-group is a **minimal sentinel** (one-form readiness gate, not a training curriculum) — it exists to satisfy Connect's API + gate attestation submissions on coordinator-confirmed practice-session-pass, NOT to carry training content. See `pdd-to-learn-app/SKILL.md § Archetypes § focus-group` for the sentinel spec.
- **Consent**: Verbal/written? Audio recording consent? Photo consent? Documented how?
- **Venue**: Neutral / facility / leader's compound? Each biases differently — which is acceptable?
- **Duration & compensation**: Expected session length? Participant opportunity cost compensated? Per-session facilitator + notetaker rate? Facilitator training stipend tied to practice-session-pass?
- **Question guide**: Sequencing (sensitive/program-specific questions last to avoid anchoring), prioritization (a 90-minute group covers 8–10 questions well, not 15+), warm-up questions, probing prompts.
- **Output spec — the gdoc structure**: What does a "good gdoc" look like? Per-section themes (3–6 bullets, with specifics), notable verbatim quotes (2–4 per section, role attribution like "mother" / "father" / "grandmother" not by name), level of consensus (strong / mixed / disagreement + justification), time spent per section, post-FGD report (top 5 things we heard, most-cited barriers, per-option reactions, surprises, recommendations), facilitator reflection (150–300 words). This structure goes in the **PDD's Output Specification** section and seeds both the gdoc template the facilitator fills out and the OCS chatbot's RAG content for post-session writing guidance.
- **Attestation form fields**: What does the per-session CommCare attestation form capture? Default: 5 fields — consent attestation (single yes/no, must be yes to submit), session date, venue (free text), GPS (geopoint), one evidence photo. Audio is NOT captured through CommCare (out-of-band, lives in Drive). The gdoc link is NOT captured (gdoc is written after submission). Everything else (participant count, segment, start/end times, per-section summaries, facilitator reflection) goes in the gdoc, not in the form. See `pdd-to-deliver-app/SKILL.md § Archetypes § focus-group` for the canonical 5-field list.

**Additional sections to include in the PDD draft:**

- **Recruitment Plan** — segments, sample sizes, identification mechanism, comparison groups.
- **Facilitation Protocol** — skill level, training surface (OCS chatbot + handbook gdoc + practice-session audio review), venue, language, consent, recording, compensation.
- **Question Guide** — ordered questions per section, with probes and warm-ups, and time allocation.
- **Output Specification** — **the gdoc structure** the facilitator fills in. Per-section format with concrete fields (themes, notable quotes, level of consensus, time spent, facilitator reflection). The Deliver app's attestation form captures *metadata and artifacts*, not this content — but the OCS chatbot's RAG content is seeded from this section so facilitators can ask "what should I put in section 3?" during write-up.

### `multi-stage`
The PDD has two or more sequenced stages with different archetypes. Treat the base sections as describing the overall intervention and create one **Stage X** subsection per stage, each declaring its own archetype and following that archetype's additional sections.

**Required for multi-stage PDDs:** an explicit **Stage Gate** subsection between every pair of stages, stating exactly what must be true at the end of stage N to proceed to stage N+1 (with go / no-go / iterate criteria).

## MCP Tools Used
- Google Drive: `drive_read_file` (pass `exportAs: 'text/markdown'` when re-reading the PDD — it is a rendered gdoc, and the default plain-text export drops the `#` heading markers and flattens pipe tables to one cell per line), `drive_create_doc_from_markdown` (the PDD — human-facing prose; the retired open-questions ledger is never written — § Asks are decision rows), `drive_create_file` (machine-parsed YAML only), `drive_update_file`, `drive_download_binary` (binary/`.ccz`/`.xlsx` inputs), `drive_set_anyone_with_link` (the PDD, `role: 'commenter'` — § Process step 6c; ace#1843; NOT on a confidential opp, ace#3191), `drive_share_with_person` (the PDD to each `reviewers:` email on a confidential opp, `role: 'commenter'` — step 6c), `drive_list_comments` (the prior run's PDD AND every Google Doc / Sheet / Slides input, called on a shortcut's `resolved_target_id` — § Process step 1; ace#2372), `drive_reply_to_comment` (`action: 'resolve'` on ACE's own PDD only; on an input document, reply with no `action`), `drive_list_folder` (a shortcut entry whose manifest row lacks `resolved_target_id`)
- Google Sheets: `sheets_list_tabs`, `sheets_batch_read` (Google-Sheet inputs)
- Google Forms: `get_google_form_definition` (Google-Form inputs)

## Mode Behavior

- **Default (auto):** Author `decisions.yaml` (step 3a), draft PDD using
  those defaults, write the PDD, email summary to admin group,
  proceed. The decisions.yaml ships with the run; humans review post-hoc
  and re-run via `/ace:step idea-to-pdd <opp>/<run-id>` after editing if
  they want a different PDD.
- **Review:** Author `decisions.yaml` (step 3a), then **pause** before
  drafting the PDD. Surface an interim `auto_surfaced` `[INFO]` stating
  "Decisions log written; edit any defaults you want changed, then
  resume." On resume, re-read `decisions.yaml` and draft the PDD using
  the (possibly edited) values. Continue to the PDD-final pause as today.

## Dry-Run Behavior
When `--dry-run` is active:
- Write the PDD to `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md` as normal
- Write the admin email summary (recipients, subject, body) to `comms-log/dry-run-idea-to-pdd.md`
- Do not send emails to the admin group
- State tracks as `dry-run-success`

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-09-11 | **`duplicate_gps_rule` joins the canonical Program Parameters vocabulary; a bare `duplicate_gps_radius_m` is retired (ace#2373).** Nothing in the vocabulary covered GPS de-duplication, so runs invented an unknown key and wrote the radius alone — which cannot carry the Targeting PDD author's accuracy condition ("where both readings have accuracy better than 15m … identifiers alone"). Downstream, `threshold-coherence-flag` then read a coherent-by-construction rule as a 15 m radius under a 50 m tolerance. Step 4's key list, `templates/pdd-template.md § Program Parameters` and Step 7.5's handoff table now carry the whole rule as `{radius_m, applies_when, fallback}`, with an instruction to transcribe the author's rule rather than raise or tie the radius. Classified by `lib/gps-dedup-coherence.ts`. *Enforced:* `test/skills/threshold-coherence-conditioned-radius.test.ts`. | ACE team |
| 2026-08-13 | **CORRECTION — the randomization rule stands, its stated reason does not (ace#1213; ace#1121 reopened).** The entry below justified 'do not spec a per-attempt item draw' by claiming Connect's single `passing_score` makes a draw unusable. That argument only applies to a **variable-size** draw; the specified mechanism was a fixed 12-of-30, which keeps the denominator constant, so it never bit. And per Jonathan the same day, a per-attempt draw **is** expressible in XForms — a seeded `once(random())` selecting from a lookup-table/fixture nodeset, or hidden questions gated on `relevant`. What is actually missing is a **Nova authoring primitive** plus the complexity of that machinery. Step 4a's guidance is unchanged in effect (still: spec one fixed bank) but now states the reason correctly, points at `_app-component-library.md § Mechanisms a PDD must not assert` — **Table B**, buildable-but-unsupported — and adds an explicit instruction: **do not write that rotation is impossible**, and where a program genuinely needs it, file a Nova capability request. New standing rule in Step 4a: when uncertain whether a mechanism is platform-closed or merely unsupported, write *'ACE does not build this today'* rather than *'this is impossible'* — a false platform constraint in a Work Order outlives the constraint and forecloses the capability request someone should be making. | ACE team |
| 2026-08-13 | **Step 4a checks every enforcement mechanism against the known-unbuildable list before specifying it (ace#1213, closes ace#1121).** Phase 1 could spec a mechanism the platform cannot build and nothing caught it until Phase 3 — `idea-to-pdd-qa` passed 6/6 and `idea-to-pdd-eval` scored the PDD 7.97 `pass`. By then the PDD, the **Work Order** and the Phase-6 **training materials** all described a control that does not exist, and a build-time deviation memo does not retro-correct three shipped documents. Step 4a gains a leading hard check against `_app-component-library.md § Known-unbuildable mechanisms`: a listed mechanism MUST NOT be asserted as enforced; state the buildable approximation and name the residual (the shape `gps-accuracy-capture` already models), or raise an open question. The per-topic bullets are now explicitly the instances, and the list is the enumerable version that gets checked. Also adds the rule **do not spec a randomized or per-attempt item draw** — spec one fixed bank sized for the gate, and where retake-resistance genuinely matters raise it as an open question, noting that unlimited re-attempts against a fixed bank lets a worker pass by memorising the answers. **The RATIONALE shipped in this entry was wrong and is retracted — see the correction entry above; ace#1121 is reopened.** *Enforced (structurally):* `test/skills/known-unbuildable-mechanisms.test.ts`. | ACE team |
| 2026-05-15 | Pare attestation-form-fields question + Decisions Log to match the 5-field form: consent / date / venue / GPS / photo. Audio is out-of-band; gdoc_link is removed (gdoc is written after submission). Add `gps-verification-radius` and `gdoc-submission-window` decisions; recharacterize `audio-min-duration` and `audio-consent-fallback` as facilitator-protocol concerns (out-of-band, not in the form). | ACE team |
| 2026-05-15 | Recharacterize `payment-rate` and `per-session-rate` Decisions Log rows: PDD captures a **range** (not a fixed number), and the actual rate is **negotiated via the solicitation response** where the LLO proposes a number with rationale. The awarded LLO's proposed rate becomes the `connect.deliver_unit` payment_unit amount at Phase 4 setup. Pairs with `solicitation-create/SKILL.md § Process`'s "per-unit payment is negotiated, not declared" design principle. | ACE team |
| 2026-05-22 | **Retire the optional `idea.md` operator-seed input.** The 2026-05-05 refactor reduced `idea.md` to an optional `--idea FILE\|-` seed alongside the `inputs/` evidence pack; the dual-path persisted but was rarely used in practice and added cognitive load (eval rubric branches, manifest-vs-idea precedence, permission-scan URL extraction). Operators now put any free-text seed directly into `inputs/` as a regular source file. Removed: optional table row, idea.md read paragraph, idea.md-URL permission scan, "or no idea.md" branch of the missing-source error. The `--idea` flag and run-root `idea.md` artifact are gone. | ACE team |
| 2026-05-29 | **Spec-for-deployability guidance (ITN post-mortem, upstream half).** Added Step 4a: when the source/evidence model implies capture fidelity (GPS accuracy radius, enumerable answers, bucketed numerics), data-quality constraints, case write-back on follow-up visits, assessment enforcement (pre/post + threshold + item count + conditional result), or a non-English working language, the PDD MUST spec it explicitly rather than only naming the topic. A thin PDD produces a faithfully-thin app that the new app-eval fitness gates hard-fail. The cure is a deployable PDD. See `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md`. | ACE team |
| 2026-07-28 | **A stated GPS accuracy tolerance may no longer be asserted as enforced (ace#1006).** Step 4a's capture-fidelity bullet used to say "spec accuracy-gated GPS (preferred + minimum accuracy, capture-gate)". No such gate is buildable — Nova rejects `validate` on `kind: geopoint`, and Connect's verification-flags form no longer renders `gps` / `gps_radius_meters` (ace#1013). Since the PDD's Evidence Model sentence flows verbatim into the Work Order, an enforced-sounding tolerance puts a promise ACE cannot keep into a contractual document. The bullet now requires accuracy-AWARE phrasing (captured + submitted + advisory + down-weighted in dedup) and forbids "rejected" / "must be ≤ X to submit" / "the app enforces" / "Connect enforces"; a genuine need for a hard gate is raised as an open question instead. | ACE team |
| 2026-08-02 | **A per-row qualifier and an aggregate over the same repeat must agree (ace#1123).** Step 4a's data-quality bullet now forbids pairing a per-row confirmation/eligibility question with an unfiltered `count()`/`sum()` over the same nodeset — the aggregate MUST carry the qualifier in its predicate. `hh-poverty-targeting` v2.1 specified a roster membership confirmation on screen 5 AND `count(/data/roster)` in the data-quality table; the build followed the table, asked the required question on every row, and ignored the answer. Household size is 31 of 102 attainable PPI points across a sharp band boundary, so one wrongly-retained member moved the score 21 points. Same family as ace#995 (dead `now()`) and ace#1006 (unenforceable GPS gate): a control that reads as configured everywhere and does nothing in the built app. | ACE team |
| 2026-08-02 | **Worked assessment items emitted by the PDD must be labelled ILLUSTRATIVE (ace#1120).** Step 4a's assessment-enforcement bullet now requires any worked example to be marked as illustrative of the required shape, never as mandated bank content — a PDD specifies the assessment blueprint; a specific quiz item is build content. All three of `hh-poverty-targeting` v2.1's worked items were guessed cold by both independent blind probes, and worked items anchor the tone of the ~21 items Phase 3 authors. Paired with the matching builder-side rule in `skills/pdd-to-learn-app/SKILL.md` (hardening or discarding a PDD example is PDD-compliant, not a deviation). | ACE team |
| 2026-09-01 | Steps 6 + 6b: compose the PDD to a LOCAL FILE and pass `localFilePath` to BOTH writes rather than emitting the document inline twice. The rendered gdoc and its `.source.md` companion are now byte-identical BY CONSTRUCTION — step 6b's premise, and `run-surface-audit`'s DOC-FIDELITY check with it, previously rested on the agent re-typing a ~52 KB document identically with nothing verifying it (dimagi-internal/ace#1780). | ACE team |
| 2026-09-02 | **Step 4a's must-not-assert check is now bidirectional — RETIRED rows count (ace#1924).** The check only ever ran forward: mechanisms the PDD was about to assert, against the LIVE rows of `_app-component-library.md § Mechanisms a PDD must not assert`. Nothing covered the inverse — a **source-stated** constraint or fixture pin whose justifying premise is a row since RETIRED. A retired row is history, so it never trips the forward check, and the source sentence leaning on it goes unexamined. Step 4a now requires checking such claims against the retired rows too, and when the premise is stale: keep the source-stated value binding for the run (source is authoritative; re-minting a fixture golden is an operator act) but record it as a `conflicting` decisions row citing the retired row, demote the pinned value to an **advisory mechanism** with the requirement stated separately (so a later phase using the now-available approach is not a deviation), and raise the re-mint as an open question. `scripts/probe-upstream-asks.ts` is the tripwire for this class repo-side but walks `SCAN_DIRS` / `SCAN_FILES` only, so it cannot see Drive-resident opp inputs — the fixture brief for `bednet-check-2-visit` pinned `entity_id` on the `voidcraft-labs/commcare-nova#458` closure that Table A retired 2026-08-29, three days after the brief was last written, and went stale with no signal (run `20260902-1555`). The Drive-scanning half of ace#1924 remains open. | ACE team |
| 2026-09-06 | **Stop routing concerns to a gate brief that does not exist (dimagi-internal/ace#1884).** 0.13.116 removed the per-skill gate-brief file class and the ace#1880 sweep removed the remaining `*.md` PATHS, but prose directives naming the gate brief as a DESTINATION survived in 15 files — a concern "surfaced in the gate brief" is surfaced nowhere. Repointed at the verdict YAML's `auto_surfaced` block, which is what the orchestrator actually renders the pause summary from. Gated by the new destination check in `test/skills/gate-brief-removal-complete.test.ts`. | ACE team |
| 2026-09-11 | **Step 1 reads the comment threads on the INPUT documents, not only on the prior run's PDD (ace#2372).** Until now `drive_list_comments` had exactly one caller, and it read the prior run's PDD. On a componentized programme the component PDDs in `inputs/` are the design, and their author reviews them in place, so her threads were invisible to every build. Measured: 8 unresolved threads on the `poverty-graduation` Targeting PDD, none ever read. The same inbox-not-store treatment now applies to every Google Doc / Sheet / Slides input. Four differences are decided explicitly in the skill. (1) **Reply, never resolve**: the thread belongs to the author, resolving stays for ACE's own PDD, and ACE never edits an input document. (2) **Already incorporated**: a thread whose substance is in the document's body gets an `accepted-edit` disposition citing the section, not a duplicate requirement. (3) **Idempotent**: input documents persist across runs, so the Drive comment id goes in the item `anchor` and a thread is captured once. (4) **The target id**: `drive_list_comments` does not follow shortcuts (the shortcut id returns `File not found`), so the call uses `resolved_target_id`, which `agents/ace-orchestrator.md` step 5c now records in the frozen manifest. *Enforced:* `test/skills/idea-to-pdd-input-doc-comments.test.ts`. | ACE team |
| 2026-09-06 | **Step 6b: the `.source.md` companion goes through `drive_upload_binary`, not `drive_create_file` (ace#1991).** Step 6b named `drive_create_file` with `mimeType: 'text/markdown'` and warned against the renderer for destroying the bytes — but `drive_create_file` ALWAYS creates a Google Doc, has no `mimeType`, and the key was dropped by the MCP schema. The instruction reached the exact outcome it forbade, through the atom it named as safe. Measured on `poverty-graduation/20260905-0924`: two calls, one local file, both files `application/vnd.google-apps.document`; 57,178 bytes sent, 58,470 read back, every markdown marker gone — so DOC-FIDELITY compared one Doc against another built by the same importer. `skills/_training-template.md` had prescribed `drive_upload_binary` since 2026-09-01. `drive_create_file` now REFUSES a `mimeType` and names the right call. *Enforced:* `test/lib/source-persisted-artifacts.test.ts` + `test/mcp/gdrive/create-file-mimetype.test.ts`. | ACE team |
| 2026-09-26 | **The `entity_id` lever no longer promises that a repeat collapses to one payment (ace#2512).** With the `duplicate` flag off — always, on ACE opportunities — Connect resets a repeat key to `pending`, auto-approves it and pays it again (`processor.py` `clean_form_submission`; `CompletedWork.payment_accrued` "Includes duplicates"). The lever now says the key GROUPS visits, names the two Connect-side stops (payment-unit caps; a computed `payable_slot` field + `form_field_rules` row), and requires non-payable record kinds to live on a form with no `deliver_unit` marker, since every visit on the paid unit counts toward `max_daily` / `max_total`. Found on `spark-facilitator/20260926-1413` by both the PDD and Work Order evals. *Enforced:* `test/skills/repeat-entity-id-payment.test.ts`. | ACE team |
| 2026-10-16 | **§ Program Parameters rows carry provenance (ace#2364).** A third `Provenance` cell on every row: `read: <doc § ref>`, `derived: <decision-id>` (or the table keys a mechanical value is computed from) or `borrowed: <source about a different programme>`. A value ACE chose must name the decision row recording it, and only `read` values may be attributed to the author. Scope default: every row carries provenance; only derived/borrowed values a reviewer could challenge get a decision row. Reproducer: poverty-graduation/20260908-0510 (assessment counts 30/20 with no source and no decision row, attributed to the author by email). *Enforced:* `idea-to-pdd-qa § program_parameters_provenance`. | ACE team |
| 2026-10-16 | **`evidence_basis` is classified by WHOSE sources disagree (ace#2266).** Author-vs-author (including source vs instrument) → `conflicting`, `conflict_owner: author`; an ACE default losing to a `[FIXED]` author instruction → `stated` with the losing default noted; ACE-vs-ACE → `conflict_owner: ace`, never put to the author. New optional `conflict_owner` field in `lib/decisions-schema.ts`, refused on non-`conflicting` rows. Reproducers: bednet-check-2-visit/20260907-1126 (source vs instrument recorded `stated`) and poverty-graduation/20260908-0510 (6 of 9 `conflicting` rows were not the author's). | ACE team |
