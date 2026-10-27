---
name: training-faq
description: >
  Internal /ace:run step — Write the LLO/FLW training FAQ from the PDD and apps.
user-invocable: false
disable-model-invocation: false
---

# Training FAQ

Produce the FAQ document — Q&A pairs anticipating the questions LLOs
and FLWs will ask once they're using the system. Audience: someone
who's mid-task and stuck, scanning for their question.

## When to run

Phase 6 (`qa-and-training`). Reads upstream Phase 1 artifacts —
`pdd-to-app-journeys`'s `pdd-to-app-journeys.md` for journey edge cases
and `pdd-to-test-prompts`'s `test-prompts.md` for OCS-side seed
questions.

## Inputs (read from Drive)

Pipeline-only: derives the FAQ from a run's PDD and app summaries. For a live program's materials, run it in a run on that program.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `ACE/<opp>/runs/<run-id>/1-design/idea-to-pdd.md` | escalation triggers, evidence model rules, opp framing, support contact |
| Phase 1 | `ACE/<opp>/runs/<run-id>/2-scenarios/pdd-to-test-prompts.md` | seed Q's that the OCS bot was tested on (high-confidence "FLWs will ask this") |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/pdd-to-learn-app_summary.md` | content-clarification questions |
| Phase 3 | `ACE/<opp>/runs/<run-id>/3-commcare/pdd-to-deliver-app_summary.md` | per-form field-clarification questions |
| Phase 4 (`run_state.yaml`) | `connect.payment_units` + `connect.verification_flags` | "why was my submission flagged?" answers |
| Phase 1 | `ACE/<opp>/runs/<run-id>/2-scenarios/pdd-to-app-journeys.md` (edge cases per journey) | seed Q's about boundary conditions |

## Output

Single file: `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-faq.md`.

## Format

Markdown grouped into 4 categories. Each Q is in **bold**, answer
follows in plain text. Audience: split between LLO operations
questions and FLW field questions; mark each with a `[LLO]` or
`[FLW]` tag in the question line so a reader scanning the doc can
filter mentally.

```markdown
# FAQ — <Opportunity Name>

Common questions from LLOs and FLWs.

## <Vendor / Subject> interaction

**[FLW] Q: <question 1>**

<answer — 2-4 sentences, authoritative, action-oriented>

**[FLW] Q: <question 2>**

<answer>

## App / Device

**[FLW] Q: The app crashed mid-form. Did I lose my data?**

<answer pulled from CommCare's actual draft-save behavior + PDD's
escalation guidance>

## Payment & Verification

**[LLO] Q: Why was FLW Asha's submission flagged?**

<answer pulled from `connect.verification_flags` rules — explain
which rule triggered, what to do>

**[LLO] Q: When does payment hit the FLW account?**

<answer from connect Programs payment cadence>

## Logistics

**[LLO] Q: <opp-specific operational question>**

<answer>
```

## Format rules

- **20-30 Q&A pairs total.** Fewer is too thin; more becomes
  hard-to-scan.
- **Bold the question, plain the answer.** Markdown `**Q:**` makes
  scanning fast.
- **A blank line between the bold question and its answer is required.**
  Two adjacent markdown lines are one paragraph (a soft line break), so
  without it `drive_create_doc_from_markdown` publishes each answer as a
  continuation of its question's paragraph and the Doc merges Q and A
  (ace#2998).
- **Tag each Q with `[LLO]` or `[FLW]`** at the start. Lets readers
  jump to their role's questions.
- **Authoritative, not hedging.** "Yes, you can resubmit." not "You
  may possibly be able to resubmit if conditions allow."
- **Reference real config when it matters.** "The GPS fence is 50m"
  not "the GPS fence is small" — the LLO needs the actual number
  from `connect.verification_flags`.

## Process

1. **Read inputs.** Drive paths in the table above.

2. **Seed Q list from test-prompts.md.** Every prompt that has
   `expected_answer_summary` becomes a candidate FAQ entry; pick the
   ones an FLW or LLO would actually ask outside the OCS chat
   context (most will).

3. **Add edge-case Q's from pdd-to-app-journeys.md.** For each
   journey's `edge_cases` block (UX-outcome phrasing), generate a
   question framed as the failure mode the FLW would encounter
   (e.g., edge case "FLW understands why a submission outside the
   GPS fence was rejected" → FAQ Q "Why did my submission fail when
   I was just outside the market?").

4. **Add LLO-operations Q's from PDD § Escalation + run_state.yaml verification flags.**

4b. **Consent coverage — REQUIRED, and not an archetype question (ace#1687).**

   If the PDD declares a consent protocol, the FAQ **must** answer for it.
   This is a floor, not a preference: emit **at least two `[FLW]` entries** —
   one on *what the worker says* (that a consent script exists, that it is read
   aloud before anything is recorded, and where in the app it appears) and one
   on *what the worker does when consent is refused or withdrawn* (which
   outcome to record, what still gets submitted, and that it is not a failure
   on their part).

   **Trigger — do not re-derive it.** Consent coverage is required whenever
   `_app-component-library.md § consent-script-floor` fires. Read that
   component's trigger clauses and apply them verbatim; they are deliberately
   wide and evaluated INDEPENDENTLY, and **a PDD that never uses the word
   "consent" can still fire them** (a photograph of identifiable people is
   enough). Grep the PDD for the protocol rather than assuming its shape: the
   script may live in a consent field's `hint` or `label`, a read-aloud `label`
   node, or a Learn-app passage.

   **Why this is a required item and not left to chance.** Consent used to
   reach the FAQ only through the `focus-group` branch of step 5's category
   set. Every `atomic-visit` and `multi-stage` opp therefore depended on a
   consent question happening to survive the seeding in steps 2–4 — and on
   `hh-poverty-targeting/20260824-1404` none did. `grep -in consent` over the
   published FAQ returned **zero hits** across 11,822 characters, on a PDD that
   mentions consent 35 times, mandates a six-element read-aloud script in
   § 7.5, and makes refusal one of three non-payable visit outcomes. The
   independent `training-faq-eval` caught it; nothing in this skill did. The
   worker-facing document that exists to answer "what do I do when they say
   no" said nothing about it.

   **What the answers must be consistent with.** The script itself is a
   BUILD-TIME artifact with a six-element floor — (a) purpose · (b) voluntary ·
   (c) may stop · (d) confidential · (e) where the data goes / who sees it ·
   (f) whether participation guarantees a benefit. Do not restate the elements
   as FAQ prose and do not invent script wording: quote the deployed script's
   own text where an answer needs it, and otherwise point the reader at it.
   Element (c) is the one that drives worker behaviour mid-visit — a household
   may withdraw *after* being asked — so the refusal/withdrawal entry must say
   what the app expects in that case, matching the consent-gated relevance the
   build applied (`_app-component-library.md § consent-script-floor`,
   `consent-branch-completeness`).

   If the trigger genuinely does not fire, say so explicitly in the verdict's
   notes rather than silently omitting the topic.

5. **Categorize into 4 sections, archetype-aware.**

   For `atomic-visit` / `multi-stage` (default): Vendor/Subject
   Interaction, App/Device, Payment & Verification, Logistics. **Step 4b's
   consent entries belong under Vendor/Subject Interaction** — the category
   set changes where consent is filed, never whether it is covered. Only the
   `focus-group` set names consent in its own title, and reading that as "the
   other archetypes don't need it" is exactly the misread that shipped a
   consent-free FAQ.

   For `focus-group`: swap the category set to match the FGD operational
   model (out-of-band gdoc + minimal in-app attestation):
   - **Facilitation & Consent** (replaces "Vendor/Subject Interaction") —
     how to handle one-voice domination, leading questions, audio
     consent decline, the verbatim consent script.
   - **Attestation Form & Layer A** (replaces "App/Device") — the
     5-field form, GPS-out-of-radius cases, the 24h submission window,
     "what counts as a valid photo" (attendance sheet, no faces).
   - **Gdoc Writing & Layer B** (new for focus-group) — what to put in
     each section, what makes a "good theme" vs "weak theme", verbatim
     quote rules, when coordinator review flags content.
   - **Payment & Logistics** (merges "Payment & Verification" +
     "Logistics") — per-session rate, training stipend on
     practice-session-pass, venue acceptable list, refreshments.

6. **Draft answers** that are 2-4 sentences each. Authoritative tone.

7. **Self-check before write.** Verify:
   - 20-30 Q&A pairs total
   - Every Q has `[LLO]` or `[FLW]` tag
   - Every payment / verification number quoted matches `run_state.yaml`
   - At least 4 Q's seeded from `test-prompts.md`
   - At least 2 Q's seeded from `pdd-to-app-journeys.md` edge cases
   - **Consent (step 4b): run `grep -in consent` over the drafted body and
     read the hits.** If `consent-script-floor` fires, at least two `[FLW]`
     entries must cover the script and the refusal/withdrawal path, and a
     zero-hit grep is a hard stop — do not write. Checking by recollection is
     what failed: the skill "knew" consent mattered and the published document
     contained the word zero times.
   - **Every unanswered `test-prompts.md` prompt on a topic the PDD treats as
     a worker-facing control is accounted for**, either by an FAQ entry or by
     a named reason in the verdict notes. The consent miss also left an
     upstream test prompt about the consent script unanswered, and nothing
     noticed because nothing was looking.

8. **Write** to `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-faq.md`
   **as a NATIVE Google Doc via `drive_create_doc_from_markdown`** — NOT
   `drive_create_file`, which uploads the body as `text/plain` so every `##`,
   `**`, `|` and `---` stays a literal character on the page. This document is
   read by a human (an FLW or LLO supervisor scanning for their question), and a partner opening it should see headings,
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
   `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-faq.source.md` via
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

9. **Self-evaluate (LLM-as-Judge).** Five criteria:
   - **Coverage:** every PDD escalation trigger + every Layer-A
     verification rule has at least one FAQ entry
   - **Consent coverage (BLOCKER when `consent-script-floor` fires):**
     the script and the refusal/withdrawal path each have at least one
     `[FLW]` entry, and the answers are consistent with the deployed
     script rather than invented. Grade it against the published body,
     not the draft in your head. Absent → `passed: false`; if the
     trigger does not fire, record that judgement and why.
   - **Tag fidelity:** every Q has `[LLO]` or `[FLW]`
   - **Answer authority:** answers cite real config / real numbers,
     not generic guidance
   - **Audience split:** at least 30% LLO Q's and at least 30% FLW
     Q's (otherwise the doc is over-skewed)

   Verdict to `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-faq_verdict.yaml`.

10. **Hand off.** Print Drive URL + verdict summary.


11. **Share it anyone-with-link.** The FAQ is a deliverable a partner or field worker opens from
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
  human-facing prose, must render), `drive_upload_binary` with `mimeType:
  'text/yaml'` (the verdict YAML — machine-parsed, so it must be stored as REAL
  BYTES; `drive_create_file` makes a Google Doc, whose export turns every `\n`
  into `\r\n\r\n\r\n`, and it has no mimeType parameter — see
  `skills/_training-template.md § Machine-parsed artifacts must not be written as
  Google Docs`), `drive_list_folder`

## Mode Behavior

- **Auto:** Run end-to-end.
- **Review:** Pause after step 7, show drafted FAQ.
- **Dry-run:** Steps 1-7, skip write. Verdict with `dry_run: true`.

## Products

- `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-faq.md`
- `ACE/<opp>/runs/<run-id>/6-qa-and-training/training-faq_verdict.yaml`
- `run_state.yaml.phases.qa-and-training.products.training.docs.faq` — `{file_id, title: "FAQ", web_view_link}` typed handoff. Multi-writer block: apply via read-modify-write per `skills/synthetic-data-generate/SKILL.md § Step 6`. See `agents/qa-and-training.md § Products` for the full slot table.

## Why a separate skill

Independent rerun is especially valuable for the FAQ — once an opp is
live, real FLW questions surface that weren't anticipated. Re-running
just this skill (with new seed Q's appended manually or via a future
"observed Q's" log) regenerates the FAQ without re-emitting the LLO
guide.

Fifth of the per-artifact training skills.

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

## Change Log

- v1 (0.10.84): Initial skill. Owns `training-faq.md` only.
- 2026-05-15: Replace the one-line "Participant Interaction" focus-group note in Step 5 with a full archetype-branched 4-category set: Facilitation & Consent / Attestation Form & Layer A / Gdoc Writing & Layer B / Payment & Logistics. Atomic-visit / multi-stage keep the default Vendor-Subject-Interaction / App-Device / Payment-Verification / Logistics categories. Prompted by `malaria-itn-fgd/20260514-2352` Phase 6 observation.
- 2026-08-26: **Consent coverage becomes a required item, keyed on the PDD rather than on the archetype (ace#1687).** Consent previously reached this FAQ only through step 5's `focus-group` category set ("Facilitation & Consent"); every `atomic-visit` / `multi-stage` opp depended on a consent question happening to survive the seeding in steps 2–4. On `hh-poverty-targeting/20260824-1404` none did — `grep -in consent` over the published document returned zero hits across 11,822 characters, on an `atomic-visit` PDD that mentions consent 35 times, mandates a six-element read-aloud script in § 7.5, and makes refusal one of three non-payable visit outcomes; an upstream test prompt about the script went unanswered too. The independent `training-faq-eval` found it; nothing in this skill did. New step 4b requires at least two `[FLW]` entries (the script, and the refusal/withdrawal path) whenever `_app-component-library.md § consent-script-floor` fires — the same trigger the build and the Deliver-app eval already share, cited rather than restated, so a PDD that never says "consent" still fires it. Step 5 now states that the category set changes where consent is filed, not whether it is covered; step 7 makes it a grep-and-read check rather than a recollection; step 9 adds a BLOCKER dimension. Graded symmetrically by `training-faq-eval § consent_coverage`. *Enforced:* `test/skills/training-faq-consent-coverage.test.ts`.
- 2026-08-26: **Persist the composed markdown as `training-faq.source.md` (ace#1687 half 2).** `drive_create_doc_from_markdown` consumes its input, so after step 8 the markdown existed nowhere and `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` — the only check comparing PUBLISHED against WRITTEN — could only ever report UNVERIFIED, leaving a blocking gate permanently unresolvable. Step 8 now writes the same string a second time as a plain `text/markdown` file. (That entry originally named `drive_create_file`, which cannot do it — superseded by the 2026-09-06 entry below; ace#1991.) Declared `sourcePersisted` in `lib/artifact-manifest.ts`; *enforced:* `test/lib/source-persisted-artifacts.test.ts`.
- 2026-09-06: **The `.source.md` companion goes through `drive_upload_binary`, not `drive_create_file` (ace#1991).** `drive_create_file` ALWAYS creates a Google Doc; it has no `mimeType` that changes that, and the key a caller passed to try was dropped by the MCP schema. So this step produced a SECOND rendered Doc and `run-surface-audit`'s `DOC-FIDELITY-UNVERIFIED` compared one Doc against another built by the same importer — passing structurally while unable to detect the content loss it exists to catch. Measured on `poverty-graduation/20260905-0924`: 57,178 bytes sent, 58,470 read back, every `#`/`**`/`>`/pipe-table marker gone. `skills/_training-template.md` had prescribed `drive_upload_binary` since 2026-09-01; the six producers had not followed it. `drive_create_file` now REFUSES a `mimeType` and names the `drive_upload_binary` call in the refusal. *Enforced:* `test/lib/source-persisted-artifacts.test.ts` (`PLAIN_WRITE_MARKERS` no longer accepts `drive_create_file`) + `test/mcp/gdrive/create-file-mimetype.test.ts`.
- 2026-09-07: **Dropped the in-app GRM/grievance escalation route from the worker-facing support line (ace#2106).** The shared contract in `skills/_training-template.md` asserted "the app's own in-app grievance route (the **GRM menu**), which the PDD already designates as the complaint channel" as settled fact. Both halves are false: `templates/pdd-template.md` and both shipped example PDDs grep ZERO for `grievance|GRM|complaint` (there is no PDD section that would designate one), and the released Deliver CCZ of `hh-poverty-targeting` (HQ `ce668763ad6c4b48ac5f4cd4502f3f8c`, `connect-ace-prod`) greps zero across `suite.xml`, `modules-0/forms-0.xml` and both `app_strings.txt` — its whole menu is one module and one form. A worker sent to a menu that is not there stops escalating rather than falling back. The support line is now the coordinator name + phone fill-in the LLO completes at onboarding; an in-app route may be named only when this run's own CCZ grep or ui-dump shows one. *Enforced:* `test/skills/in-app-control-existence-claims.test.ts` (corpus ratchet, `.md` + `.ts`) + `unverified-in-app-control` in `lib/support-channel-guard.ts`.
- 2026-10-15: **Blank line between each bold question and its answer (ace#2998).** The § Format template put each answer on the line directly under its `**[..] Q: ...**` line; markdown joins adjacent lines into one paragraph, so the published Doc of `smallholder-seasonal/20261015-1402` ran every answer into its question until a blank line was added and the Doc republished. The template now has the blank line and § Format rules requires it. *Enforced:* `test/skills/training-faq-template-blank-line.test.ts`.
