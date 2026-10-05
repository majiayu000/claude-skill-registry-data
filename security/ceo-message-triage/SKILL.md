---
name: ceo-message-triage
description: Use for deciding whether an incoming DingTalk message needs a reply, reaction, clarification, handoff, or no action. Use the neighboring workflow Skill for calendar invitations, document review, mail, meetings, personnel matters, or tracked work instead of handling those domains here. Load dingtalk-chat before reading context or sending a chat action.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Message Triage

Determine the smallest justified response to the current message from its full conversation context. Keep domain analysis in the neighboring CEO workflow Skill.

Load `dingtalk-chat` before reading conversation context or proposing any DingTalk reply, reaction, or send operation. Use only command shapes and capabilities documented by the loaded operation Skill.

## Triage Workflow

1. Read the triggering message, quoted material, and newer conversation context. Only the triggering message creates a new request; context establishes intent and whether someone already handled it.
2. Resolve mentions from the supplied identities. Treat a direct mention of the configured agent identity the same as a direct mention of the principal. A broadcast mention alone does not create principal responsibility.
3. Decide whether the message requires a decision, commitment, explanation, correction, or next step from the principal's role. If it does, prepare the smallest grounded proposal that satisfies that request.
4. If the message only acknowledges, thanks, agrees, or closes the exchange and does not change responsibility, delivery, timing, permission, cost, or approval, send no text. Put one context-appropriate reaction action in a canonical `proposal` only when it adds useful acknowledgment without implying a commitment; otherwise use canonical `no_action`.
5. If a required fact is missing and a verified conversation participant can supply it, put one concrete factual question to that participant in a canonical `proposal`. This is not an A/B selection and not `needs_human`.
6. Suppress a late reply, reaction, clarification, or follow-up when newer context shows completion, supersession, or a sufficient response. A principal reaction is sufficient only when the original request did not require a decision or commitment.
7. Keep the action grounded in the source conversation and verified identities. Do not invent recipients, accounts, identifiers, responsibilities, or targets. Do not create a follow-up that the message did not request.

Reuse confirmed facts from the current conversation. Do not replace them with
assumptions, unrelated follow-ups, or newly invented targets or accounts.

## Behavior Cases

Use the canonical Consumer Agent result contract without adding workflow-specific outcome names. A reaction or clarification is an action inside a canonical `proposal`, never a workflow-specific outcome.

- `direct_decision_request`: Use canonical `proposal` with a grounded response or authorized action.
- `acknowledgment_without_responsibility_change`: Use canonical `proposal` only for a useful reaction action; otherwise use canonical `no_action`.
- `broadcast_without_principal_action`: Use canonical `no_action`.
- `direct_agent_mention`: Apply the same responsibility test as a direct principal mention.
- `participant_can_supply_missing_fact`: Use canonical `proposal` with one concrete clarification action.
- `newer_context_completed_matter`: Use canonical `no_action`.

An `@all` broadcast with no principal action follows
`broadcast_without_principal_action`: return no action.

Consumer A remains read-only and proposes any reply, clarification, or reaction. Audit B independently loads the same business and operation Skills, checks their exact receipts and current conversation state, and alone executes an approved effect.
