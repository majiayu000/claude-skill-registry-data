---
name: training-flw-guide
description: >
  Internal /ace:run step — Write the step-by-step FLW guide to the apps.
user-invocable: false
disable-model-invocation: false
---

# Training FLW Guide

Produce the FLW-facing training document — concrete, screenshot-rich,
step-by-step. Audience: a field worker with no prior context who needs
to know exactly which buttons to tap, in what order, to deliver one
visit successfully.

## When to run

Phase 6 (`qa-and-training`), after `app-screenshot-capture` has uploaded
the per-opp screenshots. Independent of `training-llo-guide`,
`training-faq`, etc. — re-running this skill rebuilds only
`training-flw-guide.md`.

## Inputs (read from Drive)

Pipeline-only: derives the guide from a run's PDD, app summaries and screenshots. For a live program's materials, run it in a run on that program.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `ACE/<opp>/runs/<run-id>/1-design/idea-to-pdd.md` | opp framing, archetype, target FLW persona, support contact + escalation triggers |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/pdd-to-learn-app_summary.md` | Learn modules + assessment threshold |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/pdd-to-deliver-app_summary.md` | Deliver form structure (the "what to do here" section) |
| Phase 4 (`run_state.yaml`) | `connect.opportunity` (claim flow), `connect.payment_units` | "what FLWs get paid for" framing |
| Phase 6 Step 1 (`app-screenshot-capture`) | `ACE/<opp>/runs/<run-id>/6-qa-and-training/app-screenshot-capture_manifest.yaml` + per-opp PNGs | embed step-by-step Learn/Deliver screenshots |
| Common assets | `ACE/_common/connect-screenshots/<v>/manifest.yaml` + PNGs | embed common Connect navigation (sign-in, claim opp, sync, payments) |

## Output

Single file: `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-flw-guide.md`.

## Format

The guide is a markdown document with embedded image references. The
structure is opinionated and written for a high-school-reading-level
audience. Sections (in order):

```markdown
# FLW Training Guide — <Opportunity Name>

For field workers delivering this opportunity.

## What you'll be doing
<2-3 sentences from PDD intervention summary; concrete and outcome-focused>

## Before you start (one-time setup)
1. <step with embedded common-pool screenshot for sign-in>
2. <claim the opportunity — common-pool screenshot>
3. <install the Learn app — common-pool screenshot if available>

## Complete the Learn app
<one section per Learn module, with the per-opp screenshot for each>
- The assessment passing score is <X>%. You can retake it as many times as you need.

## Doing one delivery (the Deliver app)
<one section per Deliver form, walking through every required field
with a screenshot. Includes "what good looks like" guidance pulled
from PDD's Evidence Model.>

## Common pitfalls
<bullet list pulled from PDD stress-test appendix + pdd-to-app-journeys.md edge cases>

## What you get paid for
<short framing from connect.payment_units in run_state.yaml>

## Where to get help
- Your coordinator: ______________  Phone: ______________
  (a fill-in the LLO completes at onboarding — see § Support channel)
- Your LLO manager: <name from connect-setup/opportunity.md>
- For technical issues with the app, contact <support contact from PDD>
```

## Format rules

- **One screenshot per step where possible.** A step with a screenshot
  is far more useful than three steps with no screenshot. If a step
  has no matching screenshot in the manifest, write the step in plain
  text without a placeholder image — never reference a fileId you
  haven't verified exists.
- **Every screenshot ref uses the fileId from the manifest** — no guessed IDs,
  no `[screenshot needed]` markers — and is emitted as a **markdown LINK to a
  real Drive URL**, never a markdown IMAGE against the internal `drive:` scheme:

  ```markdown
  [Connect home](https://drive.google.com/file/d/<fileId>/view)     ✅
  ![Connect home](drive:<fileId>)                                   ❌
  ```

  `drive:<fileId>` is an ACE-internal reference, not a resolvable URL. This
  guide is written as a native Google Doc (step 7), and **Drive's markdown
  importer drops an image node whose src it cannot fetch — silently, alt text
  and all.** Measured on `spark-facilitator/20260813-2126`: all 44 screenshot
  references disappeared from the rendered doc, 224 words gone, and every
  content check still passed (ace#1338). The link form survives the conversion
  AND is clickable, which the literal `drive:<id>` text never was.

- **The link is the CAPTION, not the picture. Step 7b embeds the picture.**
  The link form above fixed the missing *words*; it did not put a single
  screenshot on the page. The same run published this guide with 44 links and
  zero images, and all five content evals passed it — a field worker following
  it mid-visit got a list of links (ace#1418). This artifact is
  `illustrated: true` in `lib/artifact-manifest.ts`, which means writing it is
  a two-step write: render the markdown (step 7), then run
  `scripts/embed-doc-screenshots.ts` (step 7b) to insert the frames the prose
  already cites. See `skills/_training-template.md § Illustrated guides —
  render, THEN embed` for the mechanism and why the images cannot ride in the
  markdown. Never treat step 7 as finished on its own.
- **Common-pool screenshots come first** (sign-in, claim, sync) — these
  are the Connect navigation surfaces shared across opps. They live
  under `ACE/_common/connect-screenshots/<v>/`.
- **Per-opp screenshots come second** (Learn modules, Deliver form
  walkthrough) — these are unique to this opp. Reach them by `file_id` through
  `6-qa-and-training/app-screenshot-capture_manifest.yaml`; the PNGs themselves
  live under `ACE/<opp>/runs/<run-id>/3-commcare/previews/<app-output-slug>/`
  (output previews contract v1 — filed with the phase that built the apps).
- **Speaker-style prose, not bullet-list-only.** A working FLW guide
  has narrative connecting the bullets, not just a flat checklist.

## Process

1. **Read inputs.** Drive paths in the table above.

2. **Resolve the common-screenshots set.** Read
   `ACE/_common/connect-screenshots/<v>/manifest.yaml`, where `<v>` is the
   pinned Connect APK version (`ACE_CONNECT_APK_VERSION`, else the code
   default).

   **Preflight the common pool first (ace#3060):**

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/doctor-common-screenshot-pool.ts" --format=json
   ```

   Exit 0 means the pinned APK's pool is usable. Exit 1 means it
   is missing or incomplete; the JSON `summary` names which. Exit 2 means the
   check could not run, and that is not a pass. On exit 1 or 2:
   - add `severity: FAIL` `[COMMON-POOL-MISSING] <summary>` to the verdict's
     `auto_surfaced`, and cap the verdict at `warn` (never `pass`);
   - **do not read another version's pool.** Older screens captioned as the
     current app are the false-promise class `lib/screenshot-pool-distinctness.ts`
     exists to stop. Load only the aliases the probe lists as `live`, and let
     every other common alias fall through to the template/placeholder path;
   - do not halt. The opp-specific content is still worth shipping. The fix is
     `common-screenshot-capture`, which runs outside the run.

3. **Build the screenshot resolution map.** Two pools merged into one
   `{ alias → drive_file_id }`:
   - Per-opp aliases from `ACE/<opp>/runs/<run-id>/6-qa-and-training/app-screenshot-capture_manifest.yaml` (e.g.,
     `learn-mod-1-step-3`, `deliver-form-photo-step-1`)
   - Common-pool aliases from
     `ACE/_common/connect-screenshots/<v>/manifest.yaml` (e.g.,
     `connect-signin-splash`, `claim-opp-detail`)

   Cross-pool alias collisions: per-opp wins (per-opp is more specific
   to this guide).

4. **Determine archetype.** Read `Archetype:` from PDD frontmatter.
   - `atomic-visit` (default): one Deliver form, one delivery per
     vendor/visit. Section "Doing one delivery" has one form
     walkthrough.
   - `focus-group`: **the FLW guide's shape changes fundamentally.**
     The mobile-app footprint is tiny (one sentinel Learn form
     "Briefing Acknowledgement" + one 5-field Deliver attestation
     form). The bulk of the FLW's work is **out-of-band**: running
     the FGD verbally, then writing the qualitative content into a
     Google Doc per the PDD's § Output Specification. The guide
     should:
     - Replace "Complete the Learn app" with a brief "Acknowledge
       readiness in the Learn app (one form, ~30 seconds)" pointing
       at the sentinel + noting that real facilitator training lives
       in the per-opp **OCS chatbot** (primary surface) + the
       handbook gdoc + the coordinator-graded practice-session audio
       review.
     - Replace "Doing one delivery" with a **two-step session
       workflow** section: (1) run the 75–90 min FGD per the
       Question Guide; (2) within 24 hours, fill the 5-field
       attestation form (consent / date / venue / GPS / photo);
       (3) within 72 hours of the attestation, write the per-session
       gdoc per the PDD's Output Spec (themes, quotes, consensus,
       post-FGD report, reflection) and submit to the coordinator.
     - Add a "How to use the OCS chatbot" subsection pointing
       facilitators at it for both pre-session prep questions and
       post-session gdoc-writing guidance.
     - Drop the "common pitfalls" form-fill-error patterns (mostly
       N/A for a 5-field form) and add FGD-specific pitfalls (e.g.
       leading questions in Section 3, previewing Section 5 options).
   - `multi-stage`: hybrid; first-stage and follow-up stages get their
     own subsections. If a stage's archetype is `focus-group`, use the
     focus-group section shape for that stage.

5. **Draft the guide.** Use the format above. For each Learn module
   and Deliver form, walk through the screenshots referenced in the
   manifest, weaving prose around them. Stay concrete — "Tap GO TO
   CONNECT MENU" beats "navigate to the Connect menu".

6. **Self-check before write.** Verify:
   - Every screenshot link's fileId exists in the resolved map (no
     fabricated IDs)
   - Every Learn module from `learn-app-summary.md` is referenced at
     least once
   - Every required Deliver field is mentioned at least once
   - Word count is 600-1500 — shorter feels skeletal, longer is
     unrealistic for a field worker to absorb

7. **Write** to `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-flw-guide.md`
   **as a NATIVE Google Doc via `drive_create_doc_from_markdown`** — NOT
   `drive_create_file`, which uploads the body as `text/plain` so every `##`,
   `**`, `|` and `---` stays a literal character on the page. This document is
   read by a human (a field worker following it step by step), and a partner opening it should see headings,
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
   `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-flw-guide.source.md` via
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
   and captions; this is what puts the pictures on the page. Required —
   `training-flw-guide.md` is `illustrated: true`.

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

   It anchors only on references the prose already carries, so nothing is
   reworded and no placement is invented. It re-reads the published document
   and reports the image count an ANONYMOUS reader sees; a non-zero exit means
   the pictures are not there. **Do not record this step as done on the
   strength of the batchUpdate returning 200** — that is the exact failure
   mode this whole class came from. Halt on non-zero exit and report the
   script's output. Full contract: `skills/_training-template.md § Illustrated
   guides — render, THEN embed` (dimagi-internal/ace#1418).

7c. **Close the no-shows loop: run `verify_caption_backing`, then open what
   nobody opened.** `app-screenshot-capture` describes only a subset of the
   frames it uploads (its § Step 5.6 minimum). A step-by-step guide cites more
   than that subset, and every cited frame with no `shows:` line is a
   `no-shows` BLOCKER (`skills/_training-template.md`). Measured on
   `turmeric-market-study-ghana/20261012-1749`: 90 frames uploaded, 5
   described, 16 cited, 15 `no-shows` (ace#2902).

   1. Run `verify_caption_backing({publishedFileId: <docId>, manifestFileId:
      <app-screenshot-capture_manifest.yaml>, poolFileIds: [<common pool>],
      showsAddendumFileIds: [<the addendum below, if it exists>]})`.
   2. For each `no-shows` finding, download and LOOK at the frame. Write one
      line saying what it actually shows into
      `6-qa-and-training/app-screenshot-capture_shows-addendum.yaml`, using
      `shows: [{step, file_id, shows}]`. **Never write into the capture
      manifest.** It is the producer's artifact, and a session write
      classifier rightly refuses a consumer overwriting it. The addendum is
      the consumer's write path, and the gate reads it.
   3. If a frame does NOT show what your caption says (on the turmeric run,
      4 of 21 reads contradicted the step name), fix the caption or drop the
      image. Do not describe the frame to fit the caption.
   4. Re-run step 1 with `showsAddendumFileIds`. Repeat until `findings` is
      empty, and read `addendum_unmatched`: an entry there backed nothing,
      usually because of a typo in the step name.

8. **Self-evaluate (LLM-as-Judge).** Four criteria:
   - **Coverage:** every Learn module + every Deliver form referenced
     by name
   - **Concreteness:** uses real button/field names from the
     app-summaries, not generic "tap the button"
   - **Image hygiene:** zero unresolved screenshot refs, every
     embedded image came from the resolved map, no `duplicate_of`
     capture cited as a distinct state, **and the PUBLISHED document
     carries a non-zero image count** — quote the number step 7b
     reported, not the number of references in the markdown. A
     reference is not a picture; that gap is what shipped twice.
   - **Audience fit:** language a high-school reader can follow; no
     jargon without explanation

   Write a verdict YAML to
   `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-flw-guide_verdict.yaml` in the standard shape
   (see `lib/verdict-schema.ts`). `passed: true` only if all four
   pass.

9. **Hand off.** Print the guide's Drive URL + the verdict summary.
   Phase 6 orchestrator continues with the next training skill.


10. **Share it anyone-with-link.** The FLW training guide is a deliverable a field worker or their supervisor opens from
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

- `ace-gdrive`: `drive_read_file`, `drive_create_doc_from_markdown` (the guide —
  human-facing prose, must render), `docs_batch_update` (step 7b — the
  `insertInlineImage` requests that put the screenshots on the page; driven by
  `scripts/embed-doc-screenshots.ts`), `drive_upload_binary` with `mimeType:
  'text/yaml'` (the verdict YAML — machine-parsed, so it must be stored as REAL
  BYTES; `drive_create_file` makes a Google Doc, whose export turns every `\n`
  into `\r\n\r\n\r\n`, and it has no mimeType parameter — see
  `skills/_training-template.md § Machine-parsed artifacts must not be written as
  Google Docs`), `drive_list_folder`

No live AVD or Slides — this skill is pure document generation against
existing per-opp + common-pool artifacts.

## Mode Behavior

- **Auto:** Run end-to-end. Write guide, write verdict.
- **Review:** Pause after step 6 (self-check), present the drafted
  guide, resume on approval.
- **Dry-run:** Steps 1-6 in memory, skip the `drive_create_doc_from_markdown`
  and step 7b (or run the embed script with `--dry-run` against a prior doc).
  Verdict written with `dry_run: true`.

## Products

- `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-flw-guide.md`
- `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-flw-guide_verdict.yaml`
- `run_state.yaml.phases.qa-and-training.products.training.docs.flw_guide` — `{file_id, title: "FLW training guide", web_view_link}` typed handoff. Multi-writer block: apply via read-modify-write per `skills/synthetic-data-generate/SKILL.md § Step 6`. See `agents/qa-and-training.md § Products` for the full slot table.

## Known limitations

- **Single-language only.** v1 produces English. Multilingual rollouts
  need a separate `training-flw-guide-translate` skill that takes the
  English guide + target locale and produces a translated copy.
- **No images-only sections.** Every section has at least some prose;
  there's no "screenshot wall" mode for FLWs who prefer pure visual
  walkthroughs. Could add a hint syntax (e.g.,
  `<!-- mode: visual-walkthrough -->` in PDD's audience section)
  later if needed.

## Why a separate skill

The original `training-materials` monolith emitted 7 docs in one LLM
call. Splitting per artifact gives:
- **Independent iteration.** Improving the FLW-guide prompt doesn't
  risk regressing the LLO guide.
- **Independent eval.** A failing FLW-guide judge doesn't block the
  LLO guide from shipping.
- **Independent rerun.** Re-running this skill regenerates only the
  FLW guide, not the other 4 artifacts.

This is the **second of the per-artifact training skills**, after
`training-deck-generate`. Planned siblings (next migration cycles):
- `training-llo-guide` — `training-llo-guide.md`
- `training-quick-reference` — `training-quick-reference.md`
- `training-faq` — `training-faq.md`
- `training-onboarding-email` — `training-onboarding-email.md`

## Payment figures and payment channel (shared contract)

Follow `skills/_training-template.md § Payment figures and payment channel — one
contract, all six skills` (dimagi-internal/ace#2683, #2684). A rate, fee, budget
or date the PDD marks `[PROPOSED]` is printed as proposed, with who sets the
final figure — the payment unit's configured amount is named only as what the
app shows for now. The payment channel is described in the template's
canonical wording (Connect accrues the earned total; the organisation sends the
payment and records it in Connect), never as "Connect pays automatically" and
never as "off-platform".

## Support channel (shared contract)

Follow `skills/_training-template.md § Support channel — one contract, all six
skills` (dimagi-internal/ace#1303): this artifact is **worker-facing**, so its
support line names a HUMAN (LLO coordinator / Partner Trainer) as a labelled
fill-in — never the `openchatstudio.com` host, the chatbot `public_id`, or the
`embed_key`, and never an in-app control (a grievance menu, a "Report a
problem" option) unless this run's own evidence shows one exists (ace#2106). Those are embed credentials, not a destination a CBF can open
(the embed path is a dead route; Connect has no per-opp widget field, CCC-301).
The one OCS link allowed is the bot's public start URL
(`phases.ocs-setup.products.ocs_chatbot.public_url`, `/a/<team>/chatbots/<public_id>/start/`),
which opens a live chat page (ace#3002) — in addition to the coordinator, never
instead; do not quote its greeting (blank topic, ace#2992).
Run `checkWorkerFacingSupportChannel` from `lib/support-channel-guard.ts` over
the composed markdown before writing and rewrite any finding.

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

- v1 (0.10.83): Initial skill. Owns `training-flw-guide.md` only.
  Common + per-opp screenshot layering. Archetype-aware structure.
- 2026-05-07: Per-opp screenshot path corrected from `ACE/<opp>/screenshots/` to `ACE/<opp>/runs/<run-id>/6-qa-and-training/screenshots/` to match the runs/<run-id>/<phase>/ scheme producers actually use. Doc-only fix; matches what `app-screenshot-capture` writes.
- 2026-05-15: Expand `focus-group` archetype branch (Step 4) from one-line "session-based" note to full shape spec: (1) acknowledge sentinel readiness form instead of full Learn-app walkthrough, (2) two-step session workflow (run FGD verbally → submit attestation within 24h → write gdoc within 72h), (3) add OCS chatbot subsection (primary writing-guidance surface), (4) drop form-fill pitfalls + add FGD-specific pitfalls (leading questions, premature Section 5 preview). Prompted by `malaria-itn-fgd/20260514-2352` Phase 6 observations.
- 2026-08-14: Added Step 7b — embed the screenshots into the rendered doc via `scripts/embed-doc-screenshots.ts` (Docs API `insertInlineImage`). The link form added for ace#1338 restored the WORDS but published 44 links and zero pictures; a CBF reading the guide mid-visit cannot use that. Artifact flagged `illustrated: true`; enforced by `test/lib/illustrated-artifacts.test.ts` (ace#1418).
- 2026-09-06: **The `.source.md` companion goes through `drive_upload_binary`, not `drive_create_file` (ace#1991).** `drive_create_file` ALWAYS creates a Google Doc; it has no `mimeType` that changes that, and the key a caller passed to try was dropped by the MCP schema. So this step produced a SECOND rendered Doc and `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` compared one Doc against another built by the same importer — passing structurally while unable to detect the content loss it exists to catch. Measured on `poverty-graduation/20260905-0924`: 57,178 bytes sent, 58,470 read back, every `#`/`**`/`>`/pipe-table marker gone. `skills/_training-template.md` had prescribed `drive_upload_binary` since 2026-09-01; the six producers had not followed it. `drive_create_file` now REFUSES a `mimeType` and names the `drive_upload_binary` call in the refusal. *Enforced:* `test/lib/source-persisted-artifacts.test.ts` (`PLAIN_WRITE_MARKERS` no longer accepts `drive_create_file`) + `test/mcp/gdrive/create-file-mimetype.test.ts`.
- 2026-09-07: **Dropped the in-app GRM/grievance escalation route from the worker-facing support line (ace#2106).** The shared contract in `skills/_training-template.md` asserted "the app's own in-app grievance route (the **GRM menu**), which the PDD already designates as the complaint channel" as settled fact. Both halves are false: `templates/pdd-template.md` and both shipped example PDDs grep ZERO for `grievance|GRM|complaint` (there is no PDD section that would designate one), and the released Deliver CCZ of `hh-poverty-targeting` (HQ `ce668763ad6c4b48ac5f4cd4502f3f8c`, `connect-ace-prod`) greps zero across `suite.xml`, `modules-0/forms-0.xml` and both `app_strings.txt` — its whole menu is one module and one form. A worker sent to a menu that is not there stops escalating rather than falling back. The support line is now the coordinator name + phone fill-in the LLO completes at onboarding; an in-app route may be named only when this run's own CCZ grep or ui-dump shows one. *Enforced:* `test/skills/in-app-control-existence-claims.test.ts` (corpus ratchet, `.md` + `.ts`) + `unverified-in-app-control` in `lib/support-channel-guard.ts`.
- 2026-09-29: Per-opp screenshots are reached by `file_id` through the capture manifest; the PNGs moved to `3-commcare/previews/<app-output-slug>/` (output previews contract v1). No behaviour change for a skill that already resolved by id.
