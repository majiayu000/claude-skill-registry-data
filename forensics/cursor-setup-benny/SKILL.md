---
name: cursor-setup-benny
description: Configure Benny and prepare its triage and repro automations. Use when installing Benny or changing its Slack, tracker, repository, routing, control, model, or budget settings.
---

# Set up Benny on Codex

Benny is a two-workflow automation pack: triage one Slack issue report, then reproduce or verify a trusted bug/performance verdict. These three explicit-only skills distribute its native instructions; distribution alone does not create, enable or schedule either workflow.

## 1. Prepare the complete project-owned pack

Identify the target repository and existing Benny setup. Read [the native intent](references/benny/FOR_AGENTS.md), [configuration template](references/benny/templates/configuration.example.yaml) and both prompt templates in the bundled `references/benny/` pack. If this file is already inside a committed pack at `skills/setup-benny/instructions.md`, locate its root through `../../FOR_AGENTS.md` instead. The complete pack includes all three operational files and their supporting references.

Only when project setup is requested, merge the complete bundled pack into `<target-repository>/.agents/automations/benny/`. Preserve destination-only files, inspect conflicts and retain local changes. Keep user-owned configuration, routing and feature maps outside the managed pack, for example `.agents/benny/`. Stop and ask when ownership of a conflicting file is ambiguous. Never install skills or write Cursor settings as an incidental setup step.

Resolve the ten shared dependencies through actual native discovery in a fresh session rooted in the target project: `cursor-how`, `cursor-why`, `cursor-tdd`, `cursor-unslop`, `cursor-principle-separate-before-serializing-shared-state`, `cursor-principle-minimize-reader-load`, `cursor-principle-guard-the-context-window`, `cursor-principle-sequence-verifiable-units`, `cursor-principle-fix-root-causes`, and `cursor-principle-prove-it-works`. Do not count this session's loaded context or assume another home has them. Native discovery differs from Cursor project plugin enablement; report the scope actually verified. Missing dependencies leave the dependent workflow incomplete.

The project-owned pack's operational files are read directly, not selected implicitly as chat skills. Confirm the pack and referenced secret-free configuration are committed in the same repository before a fresh automation checkout uses them; do not commit unless asked. Live prompts use stable project-relative paths, never installation/cache paths or this mirror's source-repository paths.

## 2. Fill configuration without secrets

Copy the bundled configuration, feature-map and optional routing-map examples into user-owned locations outside the pack. Never overwrite user configuration on refresh. Require explicit source channel, optional operations channel, repository/default branch, triage identity, tracker actions/team/project/labels/intake status, control adapter, complete user-facing feature map, verdict markers, Unicode status strings, draft-PR URL form, observation/repro/fix budgets and available model choices. Read the standing `model-capability-router` and the exact host's available models; do not guess slugs or change the current selection.

Secrets belong in the authorized environment or secret store, not YAML, prompts or committed files. Owner pings remain off unless the configured policy permits the specific feature owner or strongly evidenced regression author. Never guess routing destinations, tracker IDs or priorities.

## 3. Verify integrations and control

Inspect actual supported connector schemas for Slack thread read/reply, attachment download, tracker search/read/create/update/source-link/compensation, repository history and draft pull request creation. An optional bot token may fill only its explicitly authorized narrow capability and must never reach a worker. Do not invent endpoints or infer authority from tool availability.

Read the bundled control-adapter contract and completed feature map. Require all seven capabilities: bring up the correct app/environment; drive mapped features/states; perform real UI actions; inspect state read-only; capture screenshots; start/stop recordings; and clean up only task-owned resources. Repro remains disabled if any capability is absent. A unit test, injected state or source inspection is not real UI reproduction.

## 4. Preserve the event trigger and two separate workflows

Inspect existing native automations before creating duplicates. The triage workflow starts on a new top-level report in the configured Slack channel. Repro starts on the same event, or another explicitly selected supported trigger, and waits for the configured triage identity's marker in that original thread.

The exposed Codex scheduling API has no Slack message-event trigger field. If no authorized event delivery capability is available, report `event trigger unavailable` and leave event-driven activation incomplete. Do not create a cron/heartbeat or silently substitute polling. Bounded observation of a verdict or follow-up inside an already authorized event run is different from polling for new reports.

Create/update/enable either workflow only when explicitly requested. Prepare one draft at a time through the actual native authoring surface, show trigger/tools/configuration/readiness gaps, and finish its review before the second. Existing workflows are updated rather than duplicated. No Cursor automate editor, protocol links or hidden backend are required. Schedules are relevant only if the operator expressly chooses a different scheduled trigger.

Both templates use `source_channel_id`, `message_ts` and empty `thread_ts` for a new top-level event. Normalize once: accept `message_ts` or upstream `ts` only if supplied aliases agree; reject a child-thread event; freeze that timestamp as `SOURCE_THREAD_TS`. Every later action uses the same immutable channel/root and confirms the real parent and permalink. Do not replace it with a reply or operations timestamp.

## 5. Test before activation and report accurately

Use a designated authorized test event to verify exactly one triage verdict in the original source thread, trusted marker identity, duplicate suppression, parent preflight, tracker compensation if verdict delivery fails, coordinator-only posting and worker tool isolation. If worker isolation cannot remove Slack credentials/write tools, retain coordinator execution. Confirm two independent baseline UI reproductions, media review, ownership and root-cause gates before any bounded code edit. After editing, require two patched UI runs plus before-and-after proof and checks before opening a draft PR. Preserve existing human ownership and fix artifacts; never race them, merge or deploy.

Bundled instructions are source-distribution proof only. Fixture gate decisions do not prove live Slack, tracker compensation, worker isolation, event delivery or UI control. Report prepared pack/configuration, missing capabilities, fresh-session discovery, observed thread-safety evidence and activation state separately. Run final names, descriptions and updates through `cursor-unslop` when that dependency is available.
