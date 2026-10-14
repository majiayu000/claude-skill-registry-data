---
name: clickmax-playbooks
description: Use when the user wants to create, edit, delete, link to pipelines, preview, or rehearse a CRM playbook (the sales method with stages, questions, tones, keyword triggers and guardrails that guides meetings and calls) in Clickmax.
---

## When this applies

Use for the sales-method document in Contatos & Comercial › Configurações › Playbooks (Contacts & Sales › Settings › Playbooks): write or change one, make pipelines suggest it, preview what a meeting room receives, rehearse it with the AI copilot, or delete it.

Not this skill:

- pipeline board, stages, cards, pipeline settings -> `clickmax-pipelines`
- lead search / identity -> `clickmax-leads`
- an AI agent's own persona/knowledge -> not exposed here; this skill only picks an existing agent by id

## Key assumptions

- A playbook is an independent entity, not a pipeline setting. Pipelines only SUGGEST one when a meeting is booked; whoever books can pick another playbook or none. Suggestion applies only when the booking does not choose (public booking pages, automations, AI bookings, or a `scheduled_calls_create` that omits `playbookId`).
- Effect is limited to the `meeting` scope: the Click Meeting room panel (Roteiro column + AI copilot briefing) and the voice-call window. `whatsapp`, `livechat`, `flows` scopes are shown as "coming soon" and are rejected on save; only `["meeting"]` is valid.
- Structure: stages (title, objective, talk track, watch-out, questions = the meeting checklist) · tones (name, when, delivery) · keyword triggers ("deixas") · attachments (existing http(s) URLs) · guardrails (what the copilot must never suggest). Limits: 20 stages, 30 questions/stage, 12 tones, 40 triggers, 12 terms/trigger, 30 attachments, 20 guardrails.
- Save is WHOLE-DOCUMENT (`playbooks_update` = PUT). Omitted collections are wiped, attachments included, and they cannot be re-uploaded through this surface. Always read-modify-write from `playbooks_get`.
- Ids (stage, question, tone, trigger) are authored by the caller (1-40 chars). Questions must be unique across the WHOLE playbook, not per stage: the room marks a question as covered by id. Keep existing ids stable on edits; a changed id is a different item.
- Keyword triggers are deterministic and model-free: the room compares each GUEST utterance with the terms (case, accents and punctuation ignored, whole words only: `caro` fires on "ficou caro demais", not on "carro alugado"), shows the same cue text instantly, and the same trigger returns at most every 5 minutes. Only the guest speaking fires them. Terms need at least 2 chars.
- Editing a playbook changes meetings booked AFTER the save and future calls. A booked meeting keeps the script it received; the host refreshes it by re-picking the playbook inside the room.
- Delete is hard and permanent. Pipelines that suggested it are left with no suggestion; booked meetings keep their room script.
- Writes (create/update/delete/link/simulate) are for owner/admin/editor; every role can read.
- The talk track accepts 6000 chars but the meeting panel shows the first 2000. `playbooks_meeting_guide_get` shows the truncated, real version.
- Not available here: audio transcription for the simulator, file upload for attachments, AI-generated playbooks ("Com IA" in the editor), templates gallery (NEPQ, SPIN, BANT, Challenger, consultative diagnosis are editor templates, not API objects).

## Thought process

1. Find out what the user has: `playbooks_list` first; edit before creating a near-duplicate.
2. New method from scratch: interview briefly (sales motion, buyer, stages the conversation goes through, top objections, forbidden promises), then design; do not invent pricing or promises the user never gave.
3. Separate three jobs: authoring the document, linking it (suggestion per pipeline), choosing it for one meeting.
4. Validate a draft before or right after saving with the rehearsal; treat its output as one sample, not a verdict.

## Execute guide

- Build: draft `stages` (one clear objective each, 3-8 open questions that steer the buyer, a short talk track, a concrete watch-out), 2-5 `tones` for moments such as opening/objection/closing, `keywords` for predictable moments (price, competitor, "preciso pensar") and `guardrails` for hard "never" rules. Then `mcp__plugin_clickmax_clickmax__playbooks_create` with `scopes: ["meeting"]` and `[]` for collections you have nothing for. Generate ids like `stage-1`, `q-1-1`, `tone-1`, `cue-1`.
- Edit: `mcp__plugin_clickmax_clickmax__playbooks_get` -> change only the intended items -> `mcp__plugin_clickmax_clickmax__playbooks_update` with the full document, ids preserved.
- Make pipelines follow it: `mcp__plugin_clickmax_clickmax__playbooks_pipelines_list` shows every pipeline with `linked` and `currentPlaybookName`. Attaching replaces the pipeline's current suggestion, so confirm when `currentPlaybookName` is not null. Then `mcp__plugin_clickmax_clickmax__playbooks_pipeline_attach` / `mcp__plugin_clickmax_clickmax__playbooks_pipeline_detach`. From the pipeline side use `mcp__plugin_clickmax_clickmax__pipelines_playbook_get` (returns the playbook and the default copilot agent) and `mcp__plugin_clickmax_clickmax__pipelines_playbook_set`: absent field = untouched, `null` = clear; `defaultCopilotAgentId` is a separate concern from the method and no tool here lists AI agents, so only set it with an id the user gives.
- One meeting: `mcp__plugin_clickmax_clickmax__playbooks_meeting_guides_list` gives the choices (`ref` is the playbook id); pass it as `playbookId` on `mcp__plugin_clickmax_clickmax__scheduled_calls_create`, or change it with `mcp__plugin_clickmax_clickmax__scheduled_calls_update` (`null` = no playbook, omitted = keep, and creating without it falls back to the pipeline suggestion).
- Preview: `mcp__plugin_clickmax_clickmax__playbooks_meeting_guide_get` returns what the room receives (panel guide, narrated script, guardrails).
- Rehearse: `mcp__plugin_clickmax_clickmax__playbooks_simulate` runs the real copilot on a made-up conversation. It has no playbook id: pass the method through `briefing`. For a saved playbook take `script` and `guardrails` from `playbooks_meeting_guide_get`; add `briefing.goal` and `briefing.persona`. Send the whole `turns` list each call (host/guest); a guest line as the last turn mimics how the room wakes the copilot. Vary `reason` (`objection`, `question`, `silence`...) to probe stages. Use 3-6 scenarios at most (each is a real AI call).
- Trigger check: the simulator does not run keyword triggers. To verify one, compare the sample sentence with the trigger terms by hand using the matching rule above and say so.
- Delete: `mcp__plugin_clickmax_clickmax__playbooks_list` -> read `pipelinesCount` -> state how many pipelines lose their suggestion -> `mcp__plugin_clickmax_clickmax__playbooks_delete` only after explicit confirmation.

## Report

- Lead with the job: created / edited / linked / previewed / rehearsed / deleted, then the playbook name.
- Created or edited: stages count, questions count, tones, triggers, guardrails, scopes; on edits list what changed and what was kept.
- Link changes: pipelines added/removed by name, plus any suggestion that was replaced.
- Rehearsal: per scenario show the last guest line, then the suggestion (`title`, `text`, `tone`) or "no suggestion" with `reason`; separate "the copilot chose silence" from "the AI call failed" (`reason` starting with `ai_action_`). End with what to tweak in the playbook, offered as opt-in.
- Cap long lists with `+N more`; follow-up mutations are opt-in.

## Warnings

- `playbooks_update` without the full current collections silently deletes them; never send a partial document.
- Attaching to a pipeline that already suggests another playbook replaces it without asking the pipeline's owner.
- Deleting a playbook cannot be undone.
- Rehearsal answers vary between calls and cost AI calls; one silent answer is normal (most turns need no card) and does not mean the playbook is broken.
- Do not promise that editing fixes meetings already booked.

## Anti-patterns

- Treating the playbook as a pipeline setting, or trying to create one per lead.
- Regenerating ids on every edit.
- Writing prices, discounts or deadlines into stages or triggers that the user never provided.
- Marking `whatsapp`/`livechat`/`flows` scopes.
- Looping the simulator to "optimize" the text without the user asking.
- Setting the pipeline's default copilot agent as a side effect of linking a playbook.

---

Clickmax skill revision: `b8294822a4d6`
