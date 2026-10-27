---
name: llo-uat
description: >
  Run user acceptance testing with onboarded LLOs: send instructions, track feedback, compile
  sign-off status.
disable-model-invocation: false
---

# LLO User Acceptance Testing

Coordinate UAT with LLOs before the opportunity goes live.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_id`, `organization_slug` | the opportunity under test; UAT deadline | explicit arg; default: `runs/<run-id>/4-connect/connect-opp-setup.md` / run_state `selected_llo.opportunity_id`; else the program context doc |
| `llo_contacts[]` | who tests (name, email, org) | explicit arg; default: run_state `phases.solicitation-management.products.selected_llo` |
| `app_ids` (`learn`, `deliver`, `hq_domain`) | what the LLO installs | explicit arg; default: `runs/<run-id>/3-commcare/app-deploy_summary.md` |
| `training_materials[]` | links in the instructions email | explicit arg; default: `runs/<run-id>/6-qa-and-training/` |
| `archetype` | checklist + sign-off criterion (§ Archetypes) | explicit arg; default: `1-design/idea-to-pdd.md` `archetype:`; else `atomic-visit` |
| `run_id` | run-bound mode: comms-log + `9-execution-manager/` results | optional; absent = live-program mode |
| `out_folder_id` | where UAT results go in live-program mode | explicit arg when `run_id` is absent |

**Live-program mode** (no `run_id`, e.g. UAT of a changed app on a live
program): every input is passed explicitly or read from the program context
doc; message ids go to the board task, and Step 7 writes to `out_folder_id`.
Sends stay approval-gated in both modes.

## Process

1. **Read inputs from GDrive:**
   - Deployment summary: `ACE/<opp-name>/runs/<run-id>/3-commcare/app-deploy_summary.md`
   - Training materials: `ACE/<opp-name>/runs/<run-id>/6-qa-and-training/`
   - Opportunity config: `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md`
   - Awarded LLO: `phases.solicitation-management.products.selected_llo` in the current run's `run_state.yaml` (populated by Phase 8 `solicitation-review`)
   - PDD: `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md` (reads `archetype:`)

2. **Read the PDD's `archetype:` field.** The entire "what to test" list
   and the sign-off criteria differ by archetype — FGD LLOs aren't
   testing a CommCare app; they're dry-running a facilitation. See
   `## Archetypes` below for per-archetype UAT checklists. Fall back to
   `atomic-visit` if unspecified.

3. **Compose UAT instruction email for each onboarded LLO:**
   - From: ACE's mailbox (`config/agent.json` `email`; sent via the `email-communicator` skill, never a shell var)
   - To: each LLO contact email
   - CC: CRISPR Admin Dimagi Google Group
   - Subject: "[Opportunity Name] — Please Test Before Go-Live"
   - Body (archetype-aware — see `## Archetypes`):
     - What to test — archetype-specific checklist
     - How to access — archetype-specific (app download vs. question
       guide review vs. staged materials)
     - How to report issues (reply to this email, or use the OCS widget)
     - UAT deadline (from opportunity timeline)
     - What "sign-off" means — archetype-specific criterion

4. **Send the UAT instruction emails** via the `email-communicator`
   skill (or draft for review). Log message IDs to the opp's comms log
   for later correlation with replies.

5. **Monitor for LLO feedback** during UAT window:
   - Check OCS transcripts for reported issues
   - Track which LLOs have responded
   - Track which LLOs have signed off

6. **Compile UAT results:**
   - Issues reported (with severity and status)
   - LLO sign-off status (signed off / pending / blocked)
   - If blocking issues found: log them and notify admin group

7. **Write UAT results** to `ACE/<opp-name>/runs/<run-id>/9-execution-manager/llo-uat_results.md`:
   - Per-LLO sign-off status
   - Issues found and resolution status
   - Overall UAT verdict (pass / blocked)
   - Archetype noted explicitly so `llo-launch` applies the right
     go-live criteria

## Archetypes

UAT's whole "what to test" checklist is archetype-shaped. An FGD LLO
isn't testing a CommCare app — they're dry-running a facilitation
session. Sign-off criteria shift accordingly.

### `atomic-visit` (default)

**What to test:**
- Learn app modules end-to-end (download, install, run each training
  screen)
- Deliver app forms (every form, including edge cases like
  not-eligible, consent-declined)
- Case management flow — can an FLW find yesterday's registrations and
  continue the workflow?
- At least one field delivery completed end-to-end with real data (not
  a test case) and landed in the opportunity dashboard

**How to access:** download links + login instructions for the deployed
apps.

**Sign-off criterion:** *"The apps work for your FLWs in real field
conditions — enough that you'd hand the phone to an FLW tomorrow."*

### `focus-group`

**What to test:**
- **Dry-run a facilitation session** with 1–2 friendly / pilot
  participants (not the real study participants — save those for the
  real sessions). Use the actual question guide end-to-end.
- **Recording workflow**: can you start the recorder, capture clean
  audio, and upload the file via the documented path within the
  session-note timeline? Test the upload path with a real file, not a
  placeholder.
- **Consent flow**: walk through the consent script with the pilot
  participant. Does it read naturally? Does the participant have any
  confusion about what they're agreeing to?
- **Session note template**: fill out the post-session template from
  the dry-run. Does every required field fit the dry-run content? If a
  field felt awkward or redundant, flag it — easier to fix now than
  after Session 3.
- **Venue + logistics**: confirm the venue arrangements hold (quiet,
  private, available at scheduled times), participant-contact system
  works, incentive-distribution mechanism works.

**How to access:** question guide, facilitator guide, consent form,
audio-upload instructions from the per-artifact training docs in
`ACE/<opp-name>/runs/<run-id>/6-qa-and-training/`.
Explicitly do NOT ask them to "download an app" — there isn't one for
this archetype.

**Sign-off criterion:** *"You could run Session 1 tomorrow as designed:
the question guide reads naturally, the recording workflow is
practiced, and you have no open questions about consent, logistics, or
the write-up template."*

**Additional FGD-specific signal to surface in the UAT compilation:**
- Dry-run duration — flag if the facilitator reports the session is
  "way too long" or "way too short" for the planned target (PDD's
  session-length spec). This is often the first thing a dry-run
  exposes and the hardest to fix after the fact.

### `multi-stage`

**What to test:** **per-stage** checklists. For the first stage,
include the full atomic-visit or focus-group checklist depending on
that stage's protocol. For later stages, a "materials received and
reviewed, no blockers identified" check is enough at this point —
they get their own dedicated UAT windows before their kickoff.

**How to access:** Stage 1 materials in detail. Later-stage materials
linked as reference.

**Sign-off criterion:** archetype-appropriate for Stage 1 + explicit
acknowledgment that the stage-transition gate and Stage 2 onboarding
will be separate communications. Don't roll all stages into one
go-live decision.

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`, `drive_list_folder`
- OCS: `ocs_list_sessions`, `ocs_get_session`
- Email: `email-communicator` skill (sends from `ace@dimagi-ai.com`)

## Mode Behavior
- **Auto:** Send UAT instructions, monitor for results, proceed when all LLOs sign off or UAT window closes
- **Review:** Present UAT results for approval before proceeding to launch

## Dry-Run Behavior
When `--dry-run` is active:
- Write the UAT instruction emails (recipients, subject, body) to `comms-log/dry-run-llo-uat.md` instead of sending
- UAT monitoring is skipped (no real emails were sent)
- Write a simulated UAT result with all LLOs marked as "dry-run — not contacted"
- State tracks as `dry-run-success`


## Terminology

**The platform is `Connect`, never `CommCare Connect`** — in every word this skill
puts in front of a human. The full rule, including the carve-outs for CommCare the
mobile app, CommCare HQ and code-level identifiers, is
[`skills/_terminology.md`](../_terminology.md). Read it before writing prose; it is
binding on this skill's output.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-18 | Add `## Inputs` as parameters (opportunity, LLO contacts, app ids, training materials, archetype) with run defaults, plus live-program mode; sender is ACE's mailbox, not the retired `$ACE_GMAIL_ACCOUNT` (ace#1147). ace#3148. | ACE (build-vs-maintain audit) |
| 2026-04-20 | Added `## Archetypes` with per-archetype UAT checklists + sign-off criteria. `focus-group` replaces "test the apps" with "dry-run a facilitation session" (question guide + recording + consent + write-up + logistics); sign-off is "you could run Session 1 tomorrow." `multi-stage` uses per-stage checklists — full UAT for Stage 1, reference-only for later stages. Prevents LLOs from getting "download the app" UAT instructions when they have no app to download | ACE team |
