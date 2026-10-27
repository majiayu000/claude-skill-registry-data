---
name: learnings-summary
description: >
  Internal /ace:run step — Summarise what a completed run taught; seed the next PDD.
user-invocable: false
disable-model-invocation: false
---

# Learnings Summary

Synthesize all information from the completed opportunity into actionable learnings.

## Inputs

Pipeline-only: summarises one completed run from that run's artifacts (§ Process).

## Process

1. **Read all opportunity artifacts from GDrive:**
   - PDD (original plan)
   - Test results
   - Monitoring reports from `ACE/<opp-name>/monitoring/`
   - Data reviews from `ACE/<opp-name>/data-reviews/`
   - OCS transcripts (LLO questions and issues)
   - LLO feedback from `ACE/<opp-name>/runs/<run-id>/10-closeout/llo-feedback.md`
   - Comms log

2. **Analyze against original PDD:**
   - What worked as designed?
   - What didn't work or needed adjustment?
   - Were success metrics met?
   - What was unexpected?

3. **Synthesize learnings:**
   - **Process learnings** — what to change about the ACE process itself
   - **Content learnings** — what to change about the intervention design
   - **Technical learnings** — what to change about the apps or configuration
   - **Relationship learnings** — what to change about LLO engagement

4. **Determine if iteration is warranted:**
   - If yes, draft a new PDD incorporating the learnings
   - This new PDD can trigger another ACE cycle

5. **Write to GDrive:**
   - `ACE/<opp-name>/runs/<run-id>/10-closeout/learnings-summary.md` — full learnings document
   - `ACE/<opp-name>/runs/<run-id>/10-closeout/learnings-summary_new-pdd.md` — new PDD if iteration warranted

6. **Write `phases.closeout.products.learnings`** to the current run's
   `run_state.yaml` so downstream readers (ace-web summary, next-cycle
   `idea-to-pdd` if iteration is warranted) can deep-link to the
   learnings doc and the iteration PDD without listing the closeout
   folder.

   ```yaml
   phases:
     closeout:
       products:
         learnings:
           summary_file_id: <Drive fileId of learnings-summary.md>
           summary_web_view_link: <webViewLink returned by Step 5's drive_create_file for learnings-summary.md>
           new_pdd_file_id: <Drive fileId of learnings-summary_new-pdd.md, or null when iteration not warranted>
           new_pdd_web_view_link: <webViewLink for the new-pdd doc, or null>
           iteration_warranted: <true | false>
   ```

   Both `*_web_view_link` fields are populated from the `webViewLink`
   returned by Step 5's `drive_create_file` calls. The Drive URL shape
   for Google Docs (`/document/d/<id>/edit`) differs from the generic
   blob preview URL (`/file/d/<id>/view`), and there's no single
   construction rule that works for every file type — so the producer
   skill (which has the live webViewLink in hand) records it
   directly, and consumers don't have to guess.

   Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
   `merge: 'deep'` (partial phase-child patch — `deep` preserves the
   phase's `status`/`steps` and sibling products; `two-level` would
   drop them, #572/#587). Sole writer of `products.learnings`.

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`, `drive_list_folder`
- OCS: `ocs_list_sessions`, `ocs_get_session`

## Mode Behavior
- **Auto:** Generate learnings, create new PDD if warranted, notify admin group
- **Review:** Present learnings and new PDD for team discussion

## Dry-Run Behavior
When `--dry-run` is active:
- Learnings analysis and new PDD generation proceed normally (written to GDrive)
- Write any notification emails (to admin group) to `comms-log/dry-run-learnings-summary.md` instead of sending
- State tracks as `dry-run-success`
