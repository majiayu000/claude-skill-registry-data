---
name: llo-feedback
description: >
  Ask an opportunity's LLOs for feedback on the application, process, and next steps, and record
  their responses.
disable-model-invocation: false
---

# LLO Feedback

Collect feedback from LLOs about the completed opportunity.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_id`, `organization_slug` | the opportunity the feedback is about; delivery metrics | explicit arg; default: run_state `phases.solicitation-management.products.selected_llo.opportunity_id` + the run's holding org; else the program context doc |
| `llo_contacts[]` | who is asked (name, email, org) | explicit arg; default: run_state `selected_llo` + the run's comms-log; else the program context doc |
| `archetype` | which question set (§ Archetypes) | explicit arg; default: PDD / launch record frontmatter; else `atomic-visit` |
| `run_id` | run-bound mode: comms-log + `10-closeout/` record | optional; absent = live-program mode |
| `out_folder_id` | where the feedback record goes in live-program mode | explicit arg when `run_id` is absent |

**Live-program mode** (no `run_id`): metrics come live from
`connect_get_deliver_progress` on `opportunity_id`; message ids are logged to
the program project's board task (or the context doc) instead of a run
comms-log, and Step 6 writes to `out_folder_id`. Sends stay approval-gated in
both modes (external LLO contact).

## Process

1. **Read opportunity context** from GDrive:
   - LLO contact info from invite/comms logs
   - Opportunity summary (including archetype from PDD or launch record)
   - Key metrics — archetype-specific (delivery rates for atomic-visit;
     session completion + audio-quality stats for focus-group; stage
     completion + transition-gate outcomes for multi-stage)

2. **Read the `archetype:` field.** The feedback questions — what
   "usability" means, what "FLW experience" means, what improvement
   areas are worth asking about — all shift by archetype. See
   `## Archetypes` below. Fall back to `atomic-visit` if unspecified.

3. **Compose feedback request email (archetype-aware):**
   - From: ACE's mailbox (`config/agent.json` `email`; sent via the `email-communicator` skill, never a shell var)
   - To: each LLO contact email
   - CC: CRISPR Admin Dimagi Google Group
   - Questions branch per archetype — see `## Archetypes`. Keep the
     core envelope consistent (support experience, suggestions, future
     interest) across all archetypes.

4. **Send the feedback request emails** via the `email-communicator`
   skill (or draft for review). Log message IDs to the opp's comms log
   for response correlation.

5. **Monitor for responses** via OCS transcripts or email.

6. **Document feedback** to `ACE/<opp-name>/runs/<run-id>/10-closeout/llo-feedback.md`:
   - Archetype recorded explicitly so `learnings-summary` and
     `cycle-grade` know how to aggregate
   - Responses from each LLO
   - Common themes
   - Specific improvement suggestions (tagged by archetype dimension:
     app usability / session facilitation / stage transitions / support
     / training / other)

## Archetypes

Feedback questions that miss the work the LLO actually did produce
thin responses and training data that drifts toward whatever archetype
was front-loaded in the question. Ask about "app usability" when the
LLO ran focus groups, and you get a shrug plus nothing learnable
about the facilitation that actually happened.

### `atomic-visit` (default)

**Feedback questions:**
- **App usability**: Learn app (training modules clear? friction?),
  Deliver app (forms, case management, offline behavior)
- **FLW experience**: what did FLWs find hard? what tripped them up?
  what did they flag as buggy vs. confusing vs. just hard?
- **Field conditions**: signal / battery / language / literacy
  issues? anything the app assumed that wasn't true?
- **Process experience**: onboarding, support responsiveness,
  communication cadence
- **Suggestions for improvement**: open-ended
- **Future interest**: willingness to participate in similar opps

### `focus-group`

**Feedback questions** (replaces app-usability block — the LLO has no
app):
- **Question guide**: which questions worked? which questions produced
  confused / thin / deflected answers? was the sequencing natural?
- **Facilitation experience**: venue, recording equipment, participant
  comfort, consent flow. Any moments where the technology got in the
  way?
- **Audio + upload workflow**: file sizes, upload reliability, did the
  session-note template capture what mattered? what was redundant vs.
  missing?
- **Participant recruitment**: did the PDD's eligibility criteria
  produce representative participants? any segments under- or
  over-represented?
- **Session cadence**: was the session length right? did the N-sessions
  schedule land well with participants' availability? what about the
  48h write-up deadline?
- **Process experience**: onboarding, support responsiveness,
  communication cadence (shared across archetypes)
- **Suggestions for improvement**: open-ended, with a specific prompt
  for "what would make the question guide better for a follow-up
  round?"
- **Future interest**: willingness to facilitate similar pilots

**Why the swap matters:** the atomic-visit questions don't just waste
the LLO's time — they signal to the facilitator that ACE doesn't
understand what they did, which colors the *whole* response. A
facilitator asked "how was the Learn app?" after running discussion
groups hears "we weren't paying attention" and writes shorter answers
to the rest of the survey.

### `multi-stage`

**Feedback questions:** split per-stage. For each stage the LLO owned,
apply the matching archetype's question set. Cross-stage additions:

- **Stage transitions**: was the hand-off between stages clear? did
  you have what you needed from the prior stage when your stage
  started? did the stage-transition gate give you enough time?
- **Pipeline coherence**: looking across all stages, did the work feel
  like one opportunity or N disconnected ones? any context you
  expected to carry through the pipeline but didn't?

Feedback is typically collected **once per LLO**, not per-stage, to
avoid survey fatigue. If an LLO owned 3 stages, their feedback covers
all 3 in a single response.

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`
- OCS: `ocs_list_sessions` for monitoring responses
- Email: `email-communicator` skill (sends from `ace@dimagi-ai.com`)

## Mode Behavior
- **Auto:** Send feedback requests, monitor and document responses
- **Review:** Present email drafts for review before sending

## Dry-Run Behavior
When `--dry-run` is active:
- Write feedback request email drafts (recipients, subject, body) to `comms-log/dry-run-llo-feedback.md`
- Do not send emails or monitor for responses
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
| 2026-10-18 | Add `## Inputs` as parameters (opportunity, LLO contacts, archetype) with run defaults, plus live-program mode; sender is ACE's mailbox, not the retired `$ACE_GMAIL_ACCOUNT` (ace#1147). ace#3148. | ACE (build-vs-maintain audit) |
| 2026-04-20 | Added `## Archetypes` with per-archetype feedback questions. `focus-group` replaces the app-usability / FLW-experience block with question-guide quality, facilitation experience, audio+upload workflow, participant recruitment, and session cadence. `multi-stage` asks per-stage questions plus cross-stage transition quality. Prevents the "facilitator asked about a Learn app they never used" anti-pattern that drifts responses thin | ACE team |
