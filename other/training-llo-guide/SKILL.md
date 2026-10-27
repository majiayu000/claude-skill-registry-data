---
name: training-llo-guide
description: >
  Internal /ace:run step — Write the LLO operations guide.
user-invocable: false
disable-model-invocation: false
---

# Training LLO Guide

Produce the LLO Manager Guide — operations-flavored, day-to-day-focused,
written for an LLO admin who manages a roster of FLWs. Audience: someone
running the field operation who needs to know morning check-ins, quality
watch, daily caps, escalation triggers, and Connect/payment mechanics.

## When to run

Phase 6 (`qa-and-training`), after `app-screenshot-capture`. Independent
of `training-flw-guide`, `training-faq`, etc. — re-running this skill
rebuilds only `training-llo-guide.md`.

## Inputs (read from Drive)

Pipeline-only: derives the guide from a run's PDD and app summaries. For a live program's materials, run it in a run on that program.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `ACE/<opp>/runs/<run-id>/1-design/idea-to-pdd.md` | opp framing, archetype, target FLW persona, escalation triggers |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/pdd-to-learn-app_summary.md` | LLO context on what FLWs are learning |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/pdd-to-deliver-app_summary.md` | LLO context on per-visit data shape |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/app-deploy_summary.md` | HQ domain quoted in the "where the data lives" section |
| Phase 4 (`run_state.yaml`) | `connect.opportunity` + `connect.payment_units` + `connect.verification_flags` | payment per visit, max-per-day, verification rules |
| Connect (live) | `connect_get_opportunity(holding_org_slug, opportunity.id)` → `start_date`, `end_date` | **the delivery window**. This is the authoritative source; `run_state.yaml` does not carry the window under `products.connect`. Fallback: PDD `program_parameters.opportunity_{start,end}_date` |
| Phase 4 | `ACE/<opp>/runs/<run-id>/4-connect/previews/connect-opportunity/_previews.yaml` (+ its PNGs) | **the opportunity page the LLO will work in, shown on ACE's own test opportunity**: `01-overview` (dates, budget, Workers / Services Delivered / Worker Payments) and `02-verification` (Approved/Rejected, Earned/Paid). These are NOT the LLO's own screens. On a `pm-nm` run `output-preview-capture` opens the opportunity at the **PM org's** url (ace#2893), so the header names the PM org (`connect_orgs.pm_org`) and its "Program Manager" role. On a self-managed run it is ACE's single org. The partner's own opportunity is a separate one, created in Phase 9, and its header, org name and figures will differ. Caption each frame as an example of that page (§ Format rules). Required for screenshot grounding of every LLO-side action |
| Phase 5 | `ACE/<opp>/runs/<run-id>/5-ocs/ocs-setup_widget-handoff.md` (`widget_url`) | "where to ask questions" link |
| Phase 1 | `ACE/<opp>/runs/<run-id>/2-scenarios/pdd-to-app-journeys.md` | seed the "Pre-deployment UAT" section from per-journey pass criteria |
| Phase 6 Step 1 (`app-screenshot-capture`) | `ACE/<opp>/runs/<run-id>/6-qa-and-training/app-screenshot-capture_manifest.yaml` | optional — embed key screenshots in the "what FLWs see" section |

## Output

Single file: `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-llo-guide.md`.

## Format

Markdown document, structured sections. Audience: an experienced LLO
admin — assume knowledge of how Connect works generally; explain only
opp-specific mechanics. Sections (in order):

```markdown
# LLO Manager Guide — <Opportunity Name>

For LLO operators overseeing FLW deployment of this opportunity.

## What your FLWs are doing
<2-3 sentence paragraph from PDD intervention summary, framed as
"your FLWs are doing X to produce Y outcome">

## Day-to-day responsibilities
- **Morning check-in:** <opp-specific pre-flight items, e.g., MTN
  cards intact, phones charged, etc.>
- **Quality watch:** <what to look for in the first N submissions; pull
  from PDD's Evidence Model § Layer-A>
- **Daily cap enforcement:** <X per FLW per day, Y per <unit>; pulled
  from connect.payment_units max counts>
- **Escalations:** <opp-specific escalation triggers from PDD §
  Escalation, mapped to who handles each>

## Payment mechanics
- FLWs are paid <amount> per <unit>, up to <max> per day, capped at
  <total> total. (from `connect.payment_units`; when the PDD marks the rate,
  organisation fee, budget or dates `[PROPOSED]`, print them as proposed, per
  `skills/_training-template.md § Payment figures and payment channel`)
- How workers are paid: Connect's standard worker payment (Connect accrues
  the earned total; your organisation sends the payment and records it in
  Connect), in the template's canonical wording.
- Verification rules (from `connect.verification_flags`):
  <human-readable list — GPS fence radius, photo-required, duplicate
  detection window, etc.>
- Window: <start_date> to <end_date> (<N> days). Read the dates with
  `connect_get_opportunity` and compute N with `opportunityWindow()`.
- <an example of the Connect opportunity overview, cited by its Drive link
  from `4-connect/previews/connect-opportunity/` so step 7b embeds it, and
  captioned as ACE's test opportunity, not the LLO's own>

## When a paid record turns out to be false
<REQUIRED. What to do when review shows a record was fabricated AFTER
Connect approved it and accrued payment for it. Use only the mechanism in
§ "A paid record found false" below. Cover: holding the record's
payment, sending it to the escalation contact to be rejected (Connect has
no screen for this), what to do about money already paid, and the
consequence for the worker. Cite the verification-panel frame from
`4-connect/previews`.>

## Pre-deployment UAT (do this before inviting FLWs)
<derive a checklist from each journey's pass criteria in
`pdd-to-app-journeys.md` — one tickable line per criterion>

## Where the data lives
- HQ domain: <ACE_HQ_DOMAIN from 3-commcare/app-deploy_summary.md>
- Connect opportunity URL: <`phases.solicitation-management.products.selected_llo.opportunity_url`
  if set, else verbatim `[PLACEHOLDER — your organisation's Connect opportunity link, sent when your opportunity is set up]` —
  NEVER the Phase 4 opportunity URL: it is held by ACE's own Connect org
  (`connect_orgs.nm_org` / `connect_orgs.pm_org`) and the partner cannot open it (ace#3000)>
- Submission audit: <how LLO can review FLW submissions from Connect>

## Where to get help
- The OCS support widget at <widget_url> answers questions about
  this opportunity in particular
- For Connect platform issues: <support contact>
- ACE program team: <ACE_GMAIL_ACCOUNT>
- <partner/funder escalation contact. Name a person only if the run's
  inputs, PDD or run_state carry one; otherwise use the marked placeholder
  in § "Escalation contacts — no inferred backstory" below>
```

## Format rules

- **Operations-tone, not training-tone.** This is for someone running
  the field — assume experienced. The FLW-facing detail belongs in
  `training-flw-guide.md`.
- **Quote real numbers from `run_state.yaml`.** Payment amounts, max
  counts, GPS fence values come from the actual Connect config — don't
  paraphrase or round.
- **Take the window from the opportunity, never from a picture.** Read
  `start_date` / `end_date` with `connect_get_opportunity` and compute the
  length with `opportunityWindow()` from `lib/opportunity-window.ts`.
  **Never quote a number of days you read off a screenshot.** The job card's
  "Days to complete" counts down from the device clock to the end date
  (`dimagi/commcare-android` `ConnectJobRecord.getDaysRemaining()`). A frame
  captured on 2026-10-01 for a window ending 2027-02-26 reads 149. The
  spark-facilitator guide printed that 149 next to a 116-day window
  (ace#2610). If you describe the card, say it counts down to <end_date> and
  leave the number out. `findDayCountDrift()` is the pre-write check.
- **Show the LLO's own screens, not only the worker's.** Every LLO-side
  action the guide names needs a frame: reading the opportunity overview,
  the Workers tab, the verification and payment panels. Cite the matching
  frame from `4-connect/previews/connect-opportunity/` by its Drive link.
  Phone frames from `app-screenshot-capture` show what the worker sees. A
  guide grounded only on those never shows the reader their own job; the
  spark guide scored 5.0 on screenshot grounding for exactly this (ace#2610).
- **Caption those frames as what they are: an example, not the LLO's own
  screen.** They show ACE's test opportunity, opened as ACE's PM org on a
  `pm-nm` run (ace#2893), so the header names that org. Say so in the
  caption, e.g. "Example: the opportunity overview (ACE's test opportunity;
  your organisation's name and figures will appear here)". Never write "your
  screen" or name the org in the frame's header as the reader's (ace#3234).
- **Derive the Pre-deployment UAT checklist from per-journey
  `pass_criteria` in `pdd-to-app-journeys.md`.** Every journey's
  pass-criterion line becomes a tickable item. Don't paraphrase —
  paste the criterion verbatim with a leading `- [ ]`.
- **Cite screenshots by their exact capture filename, and expect them to be
  SHOWN.** A citation is either a `` `journey-deliver-01-meeting-basics.png` ``
  filename (from `app-screenshot-capture_manifest.yaml`) or a Drive link
  `[Deliver home](https://drive.google.com/file/d/<fileId>/view)`. Step 7b
  turns every such citation into an actual embedded picture, so a citation
  must name a frame the run really captured — a name the manifest does not
  carry is reported as unresolved and stays as bare text. This artifact is
  `illustrated: true` in `lib/artifact-manifest.ts`: the guide published on
  `spark-facilitator/20260813-2126` cited nine frames in prose and rendered
  zero of them, and its content eval passed anyway (ace#1418). See
  `skills/_training-template.md § Illustrated guides — render, THEN embed`.

## A paid record found false — what Connect actually lets the LLO do

Build the guide's "When a paid record turns out to be false" section on
THIS mechanism and nothing else. It was read from `dimagi/commcare-connect`
main @ `27223cc5` (2026-10-02, ace#2610). The durable copy, with source
lines, is `playbook/integrations/connect-api.md § A paid visit found false —
what the holding org can do`.

1. **The per-visit Reject button is usually unavailable.** ACE opportunities
   run with `automatic_visit_verification` on. Under that setting,
   `require_manual_visit_verification` returns 403 on `reject_visits`,
   `approve_visits`, the visit-status import and the review import. Even on a
   manual-review opportunity, reject and the import both skip a visit that
   was already auto-approved (`review_status = agree`). Do NOT tell the LLO to
   "reject the visit in Connect".
2. **Hold the payment and route the rejection through the escalation
   contact.** Connect has NO screen the LLO can use to reject a completed
   work. The completed-work status import exists only as a bare POST route
   (`completed_work_import`) that no Connect page links to (re-checked on
   `commcare-connect` main @ `046c7fd7`, 2026-10-05; ace#2613). So the guide
   tells the LLO to: (a) **hold** that record's payment; (b) send the record
   ID (worker, visit date, entity), the evidence and the reason to the
   program's escalation contact (§ "Escalation contacts" — the ACE program
   team unless the inputs name someone else), who gets the rejection applied
   in Connect; and (c) before the next payment run, **check that the worker's
   earned total on the opportunity's Worker Payments tile went down**. Until
   it does, do not pay the record. Once the record is rejected it drops out
   of the payment recompute.

   **Never describe a self-service path.** Do NOT tell the LLO to "export the
   completed-work status sheet", "set the row to rejected and re-import it",
   or use a "Payment Verification import". There is no such screen, and no
   frame can be cited for it. The Payments tab's **Import Payment Records**
   upload ("Username", "Amount", "Payment Date") is real, but it RECORDS
   payments the LLO has made. It does not reject anything. The Deliver tab's
   visit import is hidden on an ACE opportunity
   (`{% if not opportunity.automatic_visit_verification %}`).
3. **Connect does not claw back money already paid.** Workers are paid
   through Connect's standard worker payment: Connect accrues the earned
   total, and the LLO sends the money and records each payment in Connect.
   Write it in those words, not "off-platform" — see
   `skills/_training-template.md § Payment figures and payment channel`
   (ace#2684). Deleting a recorded
   payment (`payment_delete`) removes only the RECORD, and Connect pushes
   "There has been an adjustment to your earnings" to the worker. Use it only
   when a payment was recorded but never actually made. Recovering money a
   worker was actually paid is between the LLO and the worker, under the
   LLO's own terms. The guide must say so, and must tell the LLO not to
   offset it against other workers' payments.
4. **Stopping future payment to that worker is the program manager's
   action.** `suspend_user` is PM-only. Once a worker is suspended, Connect
   rejects their later visits on arrival. The LLO requests the suspension
   and supplies the evidence.
5. **The organisation fee follows the record.** A record rejected in step 2
   stops accruing the per-visit organisation amount. Do not invoice a record
   that is held or rejected.

If the PDD names a consequence ladder for the worker, quote it. If it does
not, say the consequence is the LLO's decision under its own terms with the
worker, and that the decision should be recorded. Do not invent a ladder.

## Escalation contacts — no inferred backstory

Name a partner, funder or program contact ONLY when the run's inputs, PDD
or `run_state.yaml` name that person **in that role, with a way to reach
them**. A person the PDD cites as a source of design answers is not, on
that basis, the LLO's operational contact. In every other case, write a
clearly marked placeholder that says who fills it and when:

```markdown
- **<Partner> programme contact:** _[to be named by <Partner> at onboarding — name, email, expected reply time]_
```

An honest placeholder is the correct output here, not a gap. CLAUDE.md
§ "No inferred backstory" forbids the alternative, and
`training-llo-guide-eval` scores a placeholder with an owner and a deadline
the same as a named contact (ace#2610). For every tier you CAN name (the
ACE program team, the support chatbot), give a channel and an expected
response time.

## Process

1. **Read inputs.** Drive paths in the table above.

2. **Read connect state for hard numbers.** Open `run_state.yaml` and pull
   `connect.opportunity.{name, max_visits_per_day, claim_limit_total}`,
   `connect.payment_units[].{unit_name, amount, max_visits_per_day,
   max_total_visits}`, `connect.verification_flags`. These are the
   non-negotiable values that get quoted verbatim in the guide.
   **Then read the window:** call `connect_get_opportunity(organization_slug:
   <products.connect.holding_org_slug>, opportunity_id:
   <products.connect.opportunity.id>)` for `start_date` and `end_date`, then
   compute `opportunityWindow(start_date, end_date)`. Use those dates and
   that length everywhere the guide mentions time.
   **Then list the LLO frames:** read
   `4-connect/previews/connect-opportunity/_previews.yaml`. Wherever the guide
   describes the opportunity overview or the verification / payment panels,
   cite the matching frame by its Drive link.

3. **Determine archetype.** From PDD frontmatter. For `focus-group`,
   "Quality watch" reframes around session conduct (consent flow,
   debrief notes); for `multi-stage`, add a "Cohort cadence" section
   between Day-to-day and Payment mechanics.

4. **Draft the guide** following the structure above.

5. **Derive UAT checklist from journey pass criteria.** Read
   `ACE/<opp>/runs/<run-id>/2-scenarios/pdd-to-app-journeys.md` and convert each journey's
   `pass_criteria` lines into checkbox items under the
   Pre-deployment UAT section. The LLO ticks through every journey
   before go-live.

6. **Self-check before write.** Verify:
   - Every payment-unit number quoted matches `run_state.yaml` exactly
   - Every escalation trigger from PDD § Escalation is referenced
   - `findDayCountDrift(markdown, opportunityWindow(start, end))` returns
     `[]`, meaning no stated duration contradicts the configured window
   - The "When a paid record turns out to be false" section is present and
     uses only the mechanism in § "A paid record found false"
   - At least one LLO-side frame from `4-connect/previews` is cited
   - Every named contact traces to the inputs; every other contact is the
     marked placeholder
   - The UAT checklist section has at least 5 line items (real
     checklists do)
   - Word count 500-1200 words excluding the verbatim UAT checklist —
     operations docs should be scannable. The checklist is pasted verbatim
     from every journey's `pass_criteria`, so it scales with journey count
     (7 journeys / 32 criteria = 583 words on bednet-check-2-visit/20260908-1544)
     and is not counted. The band is a guide for the guide's OWN prose; the
     eval is authoritative. `training-llo-guide-eval` has no length dimension
     and hard-gates `operational_realism` on troubleshooting depth, so never
     cut troubleshooting to fit the band (ace#2311).

7. **Write** to `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-llo-guide.md`
   **as a NATIVE Google Doc via `drive_create_doc_from_markdown`** — NOT
   `drive_create_file`, which uploads the body as `text/plain` so every `##`,
   `**`, `|` and `---` stays a literal character on the page. This document is
   read by a human (the LLO coordinator running the deployment), and a partner opening it should see headings,
   bold and tables, not markdown source. The renderer round-trips: a properly
   formatted doc exports back to clean markdown via
   `drive_read_file(exportAs: 'text/markdown')`, so nothing machine-readable is
   lost — whereas a `text/plain` upload exports ESCAPED (`\---`, `run\_id`).
   Same find-or-create semantics: a same-name file under the parent is
   overwritten IN PLACE, so the fileId — and any sharing already applied to it —
   survives. (dimagi-internal/ace#1338; sibling of the PDD fix, ace#1061.)

   **Then persist the source markdown — the same string, written twice.**
   Immediately after the render, write the EXACT bytes you just passed to
   `drive_create_doc_from_markdown` to
   `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-llo-guide.source.md` via
   `drive_upload_binary` with `mimeType: 'text/markdown'` — the same atom
   `skills/_training-template.md` prescribes. **NOT
   `drive_create_doc_from_markdown`**, which renders the source copy into a
   Doc and destroys the very bytes this step exists to preserve; and **NOT
   `drive_create_file`**, which does exactly the same thing while LOOKING like
   the safe choice. `drive_create_file` always creates a Google Doc and has no
   `mimeType` to change that — the key used to be dropped by its schema, so
   this step produced a second rendered Doc and the DOC-FIDELITY check compared
   one Doc against another built by the same importer (ace#1991). It now
   refuses the key and names this call. `drive_upload_binary` uses Drive's
   media-upload path, so the file lands as `text/markdown` and
   `drive_read_file` returns it verbatim.

   Why it is not optional: the renderer CONSUMES its input. Once the Doc
   exists the markdown you composed exists nowhere, and the `.md` in the
   published name is display text, not a file — `drive_list_folder` over a
   finished run returns every one of these as
   `application/vnd.google-apps.document` with no sibling markdown. That is
   what leaves `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` — the only
   check that compares what was PUBLISHED against what was WRITTEN, and the
   only one that could have caught a guide silently losing 44 screenshots and
   224 words with every other check green (ace#1418) — permanently
   unresolvable, because its `--doc-source` remediation has nothing real to
   point at. One extra call turns a blocking gate from decorative into
   operable. (ace#1687 half 2; declared `sourcePersisted` in
   `lib/artifact-manifest.ts`, enforced by
   `test/lib/source-persisted-artifacts.test.ts`.)

7b. **Embed the screenshots into the rendered doc.** Step 7 publishes prose
   and citations; this is what puts the pictures on the page. Required —
   `training-llo-guide.md` is `illustrated: true`.

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/embed-doc-screenshots.ts" <docId from step 7> \
     --screenshots <drive_folders.previews_learn from app-screenshot-capture_manifest.yaml> \
     --screenshots <drive_folders.previews_deliver from app-screenshot-capture_manifest.yaml> \
     --screenshots <folderId of ACE/_common/connect-screenshots/<v>/, if the prose cites common frames>
   ```

   Pass every folder the prose can cite — the flag repeats and the script
   lists each folder recursively. There is no single "screenshots" folder
   since output previews contract v1: passing frames are split per app under
   `3-commcare/previews/`, and `app-screenshot-capture` § Step 6 records each
   id under `drive_folders` (ace#3238). Do not pass `drive_folders.forensics`
   — those are failure frames and ui-dumps, never guide illustrations.
   A manifest written before ace#3238 has no `drive_folders` block: read the
   two ids with `drive_list_folder` on the run's `3-commcare/previews/` folder
   instead of guessing one.

   It anchors only on citations the prose already carries, so nothing is
   reworded and no placement is invented. It re-reads the published document
   and reports the image count an ANONYMOUS reader sees; a non-zero exit means
   the pictures are not there. **Do not record this step as done on the
   strength of the batchUpdate returning 200.** Also read its `NOTE` line: a
   filename citation that matched no captured frame means the guide is citing
   a screenshot this run never took — fix the citation, don't ignore it. Full
   contract: `skills/_training-template.md § Illustrated guides — render, THEN
   embed` (dimagi-internal/ace#1418).

7c. **Close the no-shows loop: run `verify_caption_backing`, then open what
   nobody opened.** `app-screenshot-capture` describes only a subset of the
   frames it uploads (its § Step 5.6 minimum), and every cited frame with no
   `shows:` line is a `no-shows` BLOCKER (`skills/_training-template.md`,
   ace#2902).

   1. Run `verify_caption_backing({publishedFileId: <docId>, manifestFileId:
      <app-screenshot-capture_manifest.yaml>, poolFileIds: [<common pool>],
      showsAddendumFileIds: [<the addendum below, if it exists>]})`.
   2. For each `no-shows` finding, download and LOOK at the frame. Write one
      line saying what it actually shows into
      `6-qa-and-training/app-screenshot-capture_shows-addendum.yaml`, using
      `shows: [{step, file_id, shows}]`. Append to the file if the FLW guide
      already started it. **Never write into the capture manifest.** It is
      the producer's artifact, and the addendum is the consumer's write path,
      which the gate reads.
   3. If a frame does NOT show what your caption says, fix the caption or
      drop the image. Do not describe the frame to fit the caption.
   4. Re-run step 1 with `showsAddendumFileIds`. Repeat until `findings` is
      empty, and read `addendum_unmatched`: an entry there backed nothing.

8. **Self-evaluate (LLM-as-Judge).** Four criteria:
   - **Hard-number fidelity:** every payment / cap / GPS-fence number
     matches `run_state.yaml`
   - **Coverage:** every Layer-A verification rule + every PDD
     escalation trigger referenced, plus the false-paid-record procedure
   - **Audience fit:** operations-tone, not FLW-walkthrough-tone
   - **UAT completeness:** every journey in `pdd-to-app-journeys.md`
     is represented by at least one checklist item, and each item's
     wording matches the journey's `pass_criteria` (no editorial
     dropping)
   - **Screenshot grounding:** every screenshot citation resolves to a
     real captured frame, and the PUBLISHED document carries a non-zero
     image count — quote the number step 7b reported, not the number of
     citations in the markdown. A citation is not a picture.

   Verdict to `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-llo-guide_verdict.yaml`.

9. **Hand off.** Print Drive URL + verdict summary.


10. **Share it anyone-with-link.** The LLO manager guide is a deliverable a partner coordinator opens from
   the run summary — a private Doc opens only for accounts explicitly shared on
   it, so a recipient following the link hits *You need access*. Nothing
   upstream catches this: the doc exists, has the right words, passes every
   content eval, and returns a 401 that a link checker reasonably reads as
   "auth-gated" (the correct verdict for a Connect/HQ/OCS login gate, the wrong
   one here).

   ```
   drive_set_anyone_with_link(fileId: <docId>, role: 'commenter')
   ```

   `role: 'commenter'` rather than `reader` — a partner reviewing a training
   deliverable should be able to leave feedback on it. Do this at creation, not
   as a cleanup step: on hh-poverty-targeting/20260722-1341 all six training
   links shipped private and were shared by hand afterwards. (ace#902; enforced
   by `test/lib/recipient-facing-artifacts.test.ts`.)

## MCP Tools Used
- `ace-gdrive`: `drive_set_anyone_with_link` — share the deliverable (ace#902).

- `ace-connect`: `connect_get_opportunity` — the delivery window (ace#2610).
- `ace-gdrive`: `drive_read_file`, `drive_create_doc_from_markdown` (the guide —
  human-facing prose, must render), `docs_batch_update` (step 7b — the
  `insertInlineImage` requests that put the screenshots on the page; driven by
  `scripts/embed-doc-screenshots.ts`), `drive_upload_binary` with `mimeType:
  'text/yaml'` (the verdict YAML — machine-parsed, so it must be stored as REAL
  BYTES; `drive_create_file` makes a Google Doc, whose export turns every `\n`
  into `\r\n\r\n\r\n`, and it has no mimeType parameter — see
  `skills/_training-template.md § Machine-parsed artifacts must not be written as
  Google Docs`), `drive_list_folder`

## Mode Behavior

- **Auto:** Run end-to-end. Write guide, write verdict.
- **Review:** Pause after step 6, present the drafted guide.
- **Dry-run:** Steps 1-6, skip `drive_create_doc_from_markdown` and step 7b
  (or run the embed script with `--dry-run` against a prior doc). Verdict with
  `dry_run: true`.

## Products

- `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-llo-guide.md`
- `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-llo-guide_verdict.yaml`
- `run_state.yaml.phases.qa-and-training.products.training.docs.llo_guide` — `{file_id, title: "LLO manager guide", web_view_link}` typed handoff. Multi-writer block: apply via read-modify-write following the canonical pattern in `skills/synthetic-data-generate/SKILL.md § Step 6` so sibling sub-keys (`docs.flw_guide`, `docs.quick_reference`, …, `deck`) are preserved. See `agents/qa-and-training.md § Products` for the full per-skill slot table.

## Why a separate skill

Same rationale as `training-flw-guide`: independent iteration, eval,
rerun. The LLO guide and FLW guide have very different audiences and
benefit from different prompts and self-eval criteria.

This is the **third of the per-artifact training skills**, after
`training-deck-generate` (0.10.79) and `training-flw-guide` (0.10.83).

## Payment figures and payment channel (shared contract)

Follow `skills/_training-template.md § Payment figures and payment channel — one
contract, all six skills` (dimagi-internal/ace#2683, #2684). A rate, fee, budget
or date the PDD marks `[PROPOSED]` is printed as proposed, with who sets the
final figure — the payment unit's configured amount is named only as what the
app shows for now. The payment channel is described in the template's
canonical wording (Connect accrues the earned total; the organisation sends the
payment and records it in Connect), never as "Connect pays automatically" and
never as "off-platform".

## Screenshot citations (shared contract)

Follow `skills/_training-template.md § Screenshot citations — canonical frames
only` (dimagi-internal/ace#1304): select captures via `canonicalCaptures` from
`lib/capture-manifest.ts`, and run `findDuplicateCitations` over the steps this
artifact cites before writing. A `duplicate_of` capture is byte-identical to
its canonical step — the same moment, never a second one.

**Checking that every `file_id` resolves does not cover this.** That is
existence; this is distinctness. Two producers asserted the former, self-scored
`image_hygiene` near 10, and still captioned alias frames as distinct states.
The self-eval criterion must assert duplicate handling explicitly.

## Change Log

- v1 (0.10.84): Initial skill. Owns `training-llo-guide.md` only.
- 2026-10-19: **The Phase 4 frames are an example captured by ACE's PM org, not the LLO's own screens (ace#3234).** The Inputs row said they were "captured as the holding (Network Manager) org", but `output-preview-capture` opens the opportunity at the PM org's url on a `pm-nm` run (ace#2893), and on connect-fi/20261018-1440 the frames' header named the PM org as "Program Manager". The guide now captions them as an example of the page. The same run's frames were SA-only and failed step 7b with Docs' generic "problem retrieving the image". `scripts/embed-doc-screenshots.ts` now reads each frame's sharing before writing and names any unshared frame, and `output-preview-capture`'s `index` refuses a frame whose upload did not come back `anyone-with-link`. *Enforced:* `test/lib/doc-image-embed.test.ts`, `test/lib/preview-capture.test.ts`, `test/skills/llo-guide-phase4-frames-honest.test.ts`.
- 2026-10-16: **The word band excludes the verbatim UAT checklist, and the eval is authoritative (ace#2311).** The band was 500-1200 words for the whole guide, but the mandated verbatim checklist alone was 583 words on a 7-journey PDD, and the eval hard-gates troubleshooting depth the remaining budget could not fund. *Enforced:* `test/skills/llo-guide-word-band.test.ts`.
- 2026-10-15: **"Where the data lives" no longer links the Phase 4 opportunity (ace#3000).** That opportunity is ACE's build/QA vehicle, held by ACE's own NM org since ace#2419, and the partner cannot open it. The line now carries `selected_llo.opportunity_url` (Phase 9) or a verbatim labelled placeholder. *Enforced:* `test/skills/partner-artifacts-no-phase4-opp-url.test.ts`.
- 2026-08-14: Added Step 7b — embed the screenshots into the rendered doc via `scripts/embed-doc-screenshots.ts` (Docs API `insertInlineImage`), plus a format rule making filename citations first-class and a `screenshot grounding` self-eval criterion keyed to the PUBLISHED image count. The guide cited nine frames in prose and rendered none. Artifact flagged `illustrated: true`; enforced by `test/lib/illustrated-artifacts.test.ts` (ace#1418).
- 2026-09-06: **The `.source.md` companion goes through `drive_upload_binary`, not `drive_create_file` (ace#1991).** `drive_create_file` ALWAYS creates a Google Doc; it has no `mimeType` that changes that, and the key a caller passed to try was dropped by the MCP schema. So this step produced a SECOND rendered Doc and `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` compared one Doc against another built by the same importer — passing structurally while unable to detect the content loss it exists to catch. Measured on `poverty-graduation/20260905-0924`: 57,178 bytes sent, 58,470 read back, every `#`/`**`/`>`/pipe-table marker gone. `skills/_training-template.md` had prescribed `drive_upload_binary` since 2026-09-01; the six producers had not followed it. `drive_create_file` now REFUSES a `mimeType` and names the `drive_upload_binary` call in the refusal. *Enforced:* `test/lib/source-persisted-artifacts.test.ts` (`PLAIN_WRITE_MARKERS` no longer accepts `drive_create_file`) + `test/mcp/gdrive/create-file-mimetype.test.ts`.
- 2026-10-02: **Window from the opportunity, false paid records, LLO screens, honest contacts (ace#2610).** On `spark/spark-facilitator/20261001-2208` the guide had four defects. It printed "149 days to complete", which is the app's countdown on the capture date (`ConnectJobRecord.getDaysRemaining()`), next to a 116-day window. It had no procedure for a paid meeting later found fabricated. It showed only CBF phone screens. It could not name a Spark contact without inventing one. Fixes:
  - Step 2 reads `start_date`/`end_date` via `connect_get_opportunity` and computes the length with `lib/opportunity-window.ts`; `findDayCountDrift` is the pre-write check.
  - A new required "When a paid record turns out to be false" section is built on the Connect mechanism read from source (`commcare-connect` @ `27223cc5`).
  - `4-connect/previews` is now an input for LLO-side grounding.
  - A named contact must trace to the inputs; otherwise the guide uses a marked placeholder.

  *Enforced:* `test/lib/opportunity-window.test.ts`, `test/skills/training-llo-guide-contract.test.ts`.
- 2026-10-05: **No self-service completed-work rejection (ace#2613).** Step 2 of § "A paid record found false" told the LLO to export the completed-work status sheet, set the row to `rejected` and re-import it, a path the LLO cannot reach. On `commcare-connect` main @ `046c7fd7` the `completed_work_export` / `completed_work_import` routes exist but no template links to them. The guide now says: hold the payment, send the record and evidence to the escalation contact to get it rejected, and do not pay until the Worker Payments total drops. *Enforced:* `test/skills/no-completed-work-import-ui.test.ts`.
