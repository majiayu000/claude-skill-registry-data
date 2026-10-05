---
name: ceo-calendar-invite
description: Use for incoming DingTalk calendar invitations, calendar cards, meeting invitations, attendance decisions, schedule conflicts, tentative, accept, or decline responses, and questions about why the principal should attend or what input is expected. Use ceo-meeting-work for meeting content after attendance is settled. Load dingtalk-calendar before issuing any DWS calendar command.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Calendar Invite

Decide from the live invitation, schedule context, attendance value, and requested contribution. Calendar responses and factual clarification questions are Consumer proposals for Audit B to execute and verify.

## Load And Read

Load `dingtalk-calendar` before every calendar read or write. Load `dingtalk-chat` before a chat fallback. Load `dingtalk-doc` or `dingtalk-drive` before reading the corresponding linked material; follow those Skills instead of copying their command catalogs here.

Use the supplied exact event command first. Read the title, time, organizer, attendees, description, comments, linked materials, the principal's current response state, and conflicting accepted events. Reuse confirmed facts from the trigger, conversation, and live results; do not ask for facts already present.

## Decide

- Accept when the principal's decision or customer, product, personnel, or cross-team input has clear value.
- Tentatively hold when the meeting is relevant but confirmation is premature.
- Decline when the event is only broadcast or synchronization and the principal's input is not needed.
- A missing description alone is not a reason to clarify. Decide from the other confirmed facts when they establish the value.

| Case | Decision | Clarification | Required handling |
|---|---|---|---|
| `clear_value` | `accept` | `no` | Propose acceptance. |
| `worth_holding_but_uncertain` | `tentative` | `no` | Propose a tentative hold. |
| `no_principal_input_needed` | `decline` | `no` | Propose decline. |
| `missing_attendance_value` | `clarify_inviter` | `yes` | Ask what decision or input is required. |
| `missing_description_but_clear_title` | `accept` | `no` | Do not clarify only for the description. |
| `silent_meeting_with_material` | `process_material_and_accept` | `no` | Process the material and produce the requested review outcome, then propose acceptance. |
| `silent_meeting_without_material` | `clarify_exact_material` | `yes` | Ask for the referenced material itself. |

## Clarify

If participation value or requested input remains unclear after the reads, ask the verified inviter one concrete factual question; prefer a calendar comment when the installed capability supports it, otherwise use the source chat after loading `dingtalk-chat`. A resolvable factual question is a Consumer proposal, never `needs_human`.

Do not ask broad questions such as whether the principal should attend. Ask for the missing fact, such as the decision to make, the input expected, or the specific referenced material.

## Silent Review

For a silent meeting or asynchronous review, read and process every linked material and produce the requested review outcome; do not merely accept the invitation. Use the linked material's `dingtalk-doc` or `dingtalk-drive` workflow. If the event references material but provides no readable material, ask for that exact material.

## Audit B

Before execution, Audit B rereads the live event state and the applicable Skills. Suppress only an already-applied exact response or an already-sent exact clarification. A different response or corrected question is new work and requires the normal review, execution, and live verification.
