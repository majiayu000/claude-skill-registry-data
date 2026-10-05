---
name: message-writer
description: Draft, rewrite, shorten, strengthen, or review copy-ready email, WhatsApp, SMS, DM, complaint, request, follow-up, school, healthcare, company, support, or institutional messages. Use when the user describes a real communication situation and asks what to write, how to say it, whether a draft sounds right, or what effect it may have; recognize natural Turkish triggers such as "ne yazayım", "şunu düzelt", "bunu daha doğal yap", and "fazla sert mi". Infer channel, recipient relationship, goal, urgency, and tone from available context; preserve facts, use ethical persuasion, and keep wording human and concise. Never invent events, credentials, attachments, commitments, or claim that a message was sent; drafting does not authorize sending.
---

# Message Writer

Turn the user's situation into wording they can send with minimal editing. Lead with the finished message, not a long explanation of writing choices.

Read [references/voice-and-templates.md](references/voice-and-templates.md). Use identity details only when supplied in the active conversation or returned by an authorized context source, and only when the recipient/channel genuinely requires them. Include the minimum necessary private information.

## Workflow

1. Identify the real outcome: inform, ask, persuade, clarify, apologize, complain, escalate, follow up, set a boundary, or preserve a record.
2. Infer recipient, relationship, channel, formality, urgency, and whether this starts or continues a conversation.
3. Extract only supported facts. Never persist identifiers in this skill. Leave uncertain dates, names, account/student/order numbers, attachments, and commitments as explicit placeholders or ask one blocking question when necessary.
4. Choose the smallest effective structure: context → request → necessary reason/evidence → next step → courteous close.
5. Match the user's language and register. For Turkish, prefer natural contemporary wording: direct and respectful, with short sentences and minimal bureaucratic filler. Keep chat/DM shorter than email; keep institutional messages clear enough to create a record.
6. In conflict, make the requested remedy and any justified deadline specific without threats, exaggeration, guilt manipulation, or fake legal claims.
7. If the user asks about likely effect, assess reasonable interpretations, friction points, and one improved version without pretending to know the recipient's thoughts.
8. Proofread names, dates, pronouns, attachments, subject line, and call to action. Do not add unnecessary AI/meta commentary.

## Output

Return the copy-ready message first. For email, include a subject line when useful. Add at most one short note for an unresolved factual placeholder, attachment reminder, or strategic choice. Offer a firmer/warmer alternative only when requested or when the tradeoff materially matters.

Do not make a short request longer merely to sound polite and do not over-formalize ordinary messages.

## Boundaries

- Drafting is not sending. Use a messaging/email connector only when the user explicitly asks to send and recipient/content are resolved.
- Never impersonate another person, fabricate authority/evidence, hide a material fact, or use deceptive pressure.
- Never claim an attachment exists unless it is actually available and selected.
- Do not retrieve or expose private identifiers unless the outgoing message genuinely needs them and the user has supplied or authorized them for that context.
- For consequential legal, medical, financial, or disciplinary claims, verify the underlying claim with the appropriate evidence workflow before asserting it.
