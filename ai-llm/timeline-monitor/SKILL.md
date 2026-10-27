---
name: timeline-monitor
description: >
  Check whether an opportunity's LLOs are hitting milestones on schedule and email a nudge to any
  that are behind.
disable-model-invocation: false
---

# Timeline Monitor

Check LLO progress against expected timeline and prompt action if behind.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_id` + `program_org` | the opportunity whose progress is checked, read at the program's org | explicit arg; default: the current run's run_state `selected_llo.opportunity_id` (the LLO's own opportunity, once Phase 9 created it); else the program context doc's Scope |
| `milestones` | the expected timeline | explicit arg; default: the PDD; else the context doc |
| `experiment_id` | the program's chatbot, for the OCS session signals | explicit arg; default: `5-ocs/ocs-agent-setup.md`; else the context doc |
| `llo_contact_email` | where a nudge goes | explicit arg; default: run_state `selected_llo.contact_email`; else the context doc |
| `report_folder` | where reports land | default `ACE/<opp-name>/monitoring/`; on a program project, the project's folder |

No `run_state.yaml` is needed when the ids are passed (a program project, `partner-on-connect-program`).

## Process (runs periodically)

1. **Read opportunity state** from GDrive:
   - Timeline/milestones from PDD
   - Current status from the opp's **current run's** `run_state.yaml` — `run_state.yaml`
     is per run, never per opp: resolve the run with `resolve_current_run_id({opp})`
     (or take an explicit `<opp>/<run-id>`), then read
     `ACE/<opp-name>/runs/<run-id>/run_state.yaml`. For a live program with no ACE run
     (a program project — `skills/partner-on-connect-program`), take the opportunity
     id from the program's context doc instead.
   - Previous monitoring reports from `ACE/<opp-name>/monitoring/`

2. **Check progress indicators:**
   - Have LLOs started onboarding FLWs?
   - Are FLWs submitting forms in the expected timeframe?
   - Are delivery targets on track?
   - Use Connect opportunity status and progress: `connect_get_opportunity`,
     `connect_get_learn_progress`, `connect_get_deliver_progress` (ace-connect)

3. **Self-evaluate (LLM-as-Judge):**
   - Is the assessment accurate given the data available?
   - Are the recommendations actionable?
   - Is the tone appropriate for LLO communication?

4. **If behind schedule:**
   - Draft a prompting email to the LLO via ace@dimagi-ai.com
   - Include specific areas of concern and suggested actions
   - CC admin group

5. **Write monitoring report** to `ACE/<opp-name>/monitoring/YYYY-MM-DD-timeline-check.md`.

## OCS Integration

The timeline-monitor skill consumes OCS session data to detect LLOs who are
stuck or going quiet between milestone checks. Uses these MCP atoms:

- `ocs_list_sessions({ experiment_id, since })` — pull recent session activity for this opportunity's chatbot
- `ocs_get_session({ session_id })` — read the transcript of any session flagged as stuck or confused
- `ocs_trigger_bot_message({ experiment_id, identifier, platform, prompt_text })` — push a proactive nudge to an LLO who's behind schedule (only in Auto mode)
- `ocs_add_session_tags({ session_id, tags: ['ace-reviewed', 'needs-followup'] })` — mark reviewed sessions so they aren't re-processed

The `experiment_id` and `public_id` for this opportunity's chatbot come from
`ACE/<opp-name>/runs/<run-id>/5-ocs/ocs-agent-setup.md`, written by the `ocs-agent-setup` skill.

### Heuristics

- **Stuck:** LLO sent a message > 24 hours ago and received a response, but no follow-up message. Trigger a nudge.
- **Confused:** LLO asked the same question (or similar) in three consecutive sessions without acting on the answer. Escalate to admin group.
- **Silent:** LLO has sent zero messages in the past 7 days during an active opp phase. Trigger a check-in message.

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`
- Connect (ace-connect): `connect_get_opportunity`, `connect_get_learn_progress`,
  `connect_get_deliver_progress` — opportunity status and per-worker progress
- Connect (connect-labs): `get_opportunity_apps` for app structure; `explorer_describe` /
  `explorer_query` for visit-level activity (through canopy, `explorer_query` returns rows
  only for SYNTHETIC opportunities — on a real one use `connect_get_deliver_progress`)
- OCS: `ocs_list_sessions`, `ocs_get_session`, `ocs_trigger_bot_message`, `ocs_add_session_tags`

## Mode Behavior
- **Auto:** Check timeline, send prompting emails if needed, log report
- **Review:** Present findings and draft emails for approval before sending

## Dry-Run Behavior
When `--dry-run` is active:
- Write any prompting email drafts (recipients, subject, body) to `comms-log/dry-run-timeline-monitor.md`
- Monitoring report is still written to `ACE/<opp-name>/monitoring/` as normal
- Do not send emails to LLOs
- State tracks as `dry-run-success`

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.
