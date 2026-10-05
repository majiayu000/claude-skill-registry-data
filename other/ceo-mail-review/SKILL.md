---
name: ceo-mail-review
description: Use for reviewing an incoming mail card, resolving the complete message or thread, inspecting attachments and links, checking whether a reply already exists, and drafting or sending an authorized reply. Use ceo-document-review for a standalone material review outside the mail workflow. Load dingtalk-mail before any DingTalk mail operation.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Mail Review

Load `ceo-mail-review` for mail review, thread resolution, linked-material
inspection, reply judgment, and authorized reply proposals.

## Compose Operation Skills

Use the platform's mail and material Skills instead of copying their commands
into this business workflow.

| Source | Operation Skills |
| --- | --- |
| DingTalk mail | `dingtalk-mail` |
| Lark mail | `lark-mail` |
| DingTalk linked material | `dingtalk-doc`, `dingtalk-aitable`, or `dingtalk-drive` |
| Lark linked material | `lark-doc`, `lark-base`, or `lark-drive` |

Load `ceo-document-review` when the requested outcome includes a substantive
review of linked material. Load the matching chat Skill only when the result
must also be delivered in the source conversation.

## Resolve Complete Evidence

1. Treat a truncated card or quoted preview only as a locator. Resolve the
   principal's mailbox and the complete original message or thread with the
   loaded mail Skill.
2. Confirm sender, recipients, subject, current thread state, and the exact
   request. Do not ask the sender to paste content that the loaded mail Skill
   can read.
3. Inspect every linked material needed for the requested judgment with its
   matching operation Skill. A link title or mail summary is not its content.
4. Check the current thread, sent state, and safe prior receipts before
   proposing a reply. Do not propose or execute a duplicate reply.

The agent performs the business judgment. The service supplies references and
exact commands without interpreting mail or linked content. Use supplied exact
commands as given and load operation Skills for any additional reads or writes.
Do not infer or invent unread content.

## Authorization And Outcome

Propose a mail reply only when the current request explicitly authorizes
replying. Review-only, summarize-only, or approval-only requests do not
authorize a mail reply. Authorization from an older message does not silently
carry into a materially different current request.

- A justified mail reply is one action in a canonical `proposal`; the mail
  operation Skill owns execution and exact readback.
- If the complete current thread shows an equivalent reply already sent, use
  canonical `no_action` for the mail effect and report the verified state only
  when the current conversation needs it.
- If review is complete but reply authorization is absent, provide only the
  requested review or draft through an authorized channel; do not execute or
  propose a mail send.
- If evidence access fails, report the dependency failure rather than drafting
  from the preview.

When a participant can resolve a genuine evidence gap, ask one concrete
question naming the specifically missing mail or linked material. Do not ask
for a generic resend or for content the loaded operation Skills can retrieve.
