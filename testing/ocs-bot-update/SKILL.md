---
name: ocs-bot-update
description: >
  Change a live OCS chatbot's system prompt, tools or pipeline, then republish and smoke-test it.
  Use when someone asks to fix what a live bot says or how it behaves. Needs the bot id.
---

# Update an OCS chatbot

Changes how an existing bot behaves. Readers only see the **published** version: the public link
and the widget serve it, so an edit without a republish changes nothing for them. For knowledge,
meaning collection files, use `ocs-knowledge-refresh` instead.

Platform facts: [`ocs-integration.md` § Changing a live bot](../../playbook/integrations/ocs-integration.md#changing-a-live-bot).

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `experiment_id` | the integer id the set-atoms take | explicit arg; default: run_state `phases.ocs-setup.products.ocs_chatbot.experiment_id`; else the program context doc's AI coaches and bots |
| `public_id` | the UUID for reads and test messages | explicit arg; default: run_state `phases.ocs-setup.products.ocs_chatbot.*`; else the context doc |
| `changes` | any of `system_prompt`, `description`, `tools` (and `custom_actions` / `built_in_tools` / `mcp_tools`), `pipeline` (prompt, `collection_index_ids`, `max_results`, `generate_citations`, `source_material_id`) | explicit arg |
| `smoke_prompts` | 2–5 questions to ask after publishing | explicit arg; default: the run's quick suite from `pdd-to-test-prompts` when a run is bound |

The bot must be on this session's OCS team (`OCS_TEAM_SLUG`). An `ace-ocs` session cannot reach
another team, so stop and say so if the bot is elsewhere.

## Products

- A change record with the before and after configuration, the published version number and the
  smoke transcript:
  - inside a run, `<N>-<phase>/ocs-bot-update_<YYYYMMDD-HHMM>.md`;
  - on a program project, a dated line in the context doc's Decisions.

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

## Process

1. **Confirm the approval.** A published bot is live to its readers. The caller at level 0 must
   already have the requester's or owner's approval of the before and after. With none recorded,
   return the proposal and stop.
2. **Read the before state.** Run `ocs_inspect_chatbot` twice: once with `version: "default"` (what
   readers see now) and once with no version (the working draft). If the draft differs from the
   default, someone has unpublished edits. Name them in the proposal, because publishing will
   ship them too.
3. **Write the change.** Use `ocs_set_chatbot_system_prompt`, `ocs_set_chatbot_description`,
   `ocs_set_chatbot_tools` or `ocs_set_chatbot_pipeline`, according to `changes`. With two or more
   `collection_index_ids`, the prompt must contain `{collection_index_summaries}` (enforced by
   `assertCollectionPromptInvariant`).
4. **Read the draft back** with `ocs_inspect_chatbot` (no version) and compare it with the
   requested values.
5. **Publish** with `ocs_publish_chatbot_version`. Give it a description naming the change and
   the requester.
6. **Smoke-test the published bot.** Run `ocs-chatbot-qa --quick` against `public_id` with
   `smoke_prompts`. A prompt edit can regress answers an earlier eval passed. If an answer is
   clearly worse, report it with the transcript. The previous version can be made default again
   in the OCS UI; no atom does that.
7. **Record.** Write the before and after, the version number and the transcript link to the
   record named in § Products.

## MCP Tools Used

- ace-ocs: `ocs_inspect_chatbot`, `ocs_get_chatbot`, `ocs_set_chatbot_system_prompt`, `ocs_set_chatbot_description`, `ocs_set_chatbot_tools`, `ocs_set_chatbot_pipeline`, `ocs_publish_chatbot_version`
- Composed skill: `ocs-chatbot-qa` (`--quick`)

## Existing objects

- **The public link and the widget serve the published version only.** Step 5 always republishes.
- **Publishing ships every unpublished draft edit, not just this one.** Step 2 names them first.
- **Never regenerate the public link.** Regenerating revokes the URL partners already have.
  `ocs_ensure_public_link` returns the existing link.

## Mode Behavior

- **Auto:** with approval recorded in the dispatch, runs steps 2–7 and reports a smoke regression
  rather than rolling back.
- **Review:** presents the step 2 diff (including any unpublished draft edits) and waits before
  step 3.

## Dry-Run Behavior

When `--dry-run` is active, run step 2 and write the proposal. Make no set or publish calls.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-18 | Initial version: change a live bot's prompt, tools or pipeline, then republish and smoke-test (audit item 6) | ACE (build-vs-maintain audit) |
