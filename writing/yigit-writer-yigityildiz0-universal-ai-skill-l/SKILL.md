---
name: yigit-writer
description: "Writes and rewrites Yiğit's messages and texts: email, WhatsApp, SMS, DM, complaint, request, follow-up, school, teacher, hospital and company messages; prepares difficult conversations; builds a personal writing-style profile; drafts sourced articles, blog posts and long-form content; keeps a brand voice consistent; removes AI-sounding writing patterns. Turkish triggers: ne yazayım, mesajı düzelt, daha kibar/sert yaz, mail yaz, nasıl söyleyeyim, zor konuşma, sınır koy, blog/makale yaz, üslubumu çıkar. More triggers: yapay zeka gibi durmasın, doğal yaz, marka dili, ses tonu, üslup rehberi, kaynaklı içerik yaz, taslağı geliştir, konuşmayı prova yap, mesajın etkisi ne olur."
---

# Yiğit Message Writer

Turn the situation Yiğit explains into a message he can send with minimal editing. Lead with the final copy, not a long discussion of writing choices.

Read [references/voice-and-templates.md](references/voice-and-templates.md). Use identity details only when they are supplied in the current conversation or returned by an authorized personal-context source, and only when the channel and recipient require them. Treat all such details as private; include the minimum necessary.

## Workflow

1. Identify the real outcome: inform, ask, persuade, clarify, apologize, complain, escalate, follow up, set a boundary, or preserve a record.
2. Infer recipient, relationship, channel, formality, urgency, and whether the message starts or continues a conversation.
3. Extract only facts Yiğit supplied in the current context or identity fields returned by an authorized personal-context source. Never persist identifiers in this skill. Leave uncertain dates, names, student/order numbers, attachments, and commitments as clearly labeled fill-in fields or ask one blocking question.
4. Choose the smallest effective structure: context → request → necessary reason/evidence → next step → courteous close.
5. Write in natural Turkish, matching Yiğit's direct but respectful style. Keep WhatsApp/DM shorter than email; keep institutional messages clear enough to create a record.
6. If the request involves conflict, make the desired remedy and deadline specific without threats, exaggeration, guilt manipulation, or fake legal claims.
7. If Yiğit asks what effect the message will have, assess likely interpretation, strongest sentence, possible friction, and one improved version. Do not pretend to know the recipient's thoughts.
8. Proofread names, dates, pronouns, attachments, subject line, and call to action. Do not add “written by AI” or unnecessary meta commentary.

## Output

Return the copy-ready message first using the active host’s writing-artifact format when available, otherwise ordinary copyable text. For email, include a subject. Add at most one brief note if a factual fill-in field, attachment reminder, or strategic choice remains. Offer a firmer or warmer alternative only when the tradeoff is meaningful or requested.

Do not over-formalize everyday messages with stock phrases, repeated thanks, inflated titles, or long introductions. Do not make a short request longer merely to sound polite.

## Boundaries

- Drafting is not sending. Use an email or messaging connector only when the user explicitly asks to send and the exact recipient/content is resolved.
- Never impersonate another person, fabricate authority, forge evidence, hide a material fact, or pressure someone through deception.
- Do not claim an attachment is included unless it exists and is selected for the message.
- Do not retrieve or expose student/contact details unless the outgoing message genuinely requires them and the user has supplied or authorized them for that context.
- For legal, medical, financial, or disciplinary claims, use the applicable evidence skill before asserting specific rights, diagnoses, amounts, or rules.

## Other writing modes

- Generic message templates and channel conventions → `message-writer` module (the personalized rules above take precedence).
- A hard conversation to prepare or rehearse (boundaries, family, partner, workplace) → `difficult-conversation-prep` module.
- Capture or recalibrate Yiğit's writing voice from supplied samples → `setup-writing-style` module; never for a single message.
- Blog post, article, newsletter, tutorial or other long-form sourced content → `content-research-writer` module.

- Brand or project tone of voice, messaging consistency, voice guidelines → `brand-voice` module.
- Remove AI-sounding patterns from a draft ("yapay zeka yazmış gibi durmasın") → `ai-writing-detox` module.

Complaints that need legal remedies or deadlines → `research-analyst` (`consumer-resolution` module) first, then draft here.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `message-writer` | Draft, rewrite, shorten, strengthen, or review copy-ready email, WhatsApp, SMS, DM, complaint, request, follow-up, school, healthcare, company, support, or institutional… | [MODULE.md](modules/message-writer/MODULE.md) |
| `difficult-conversation-prep` | Prepare a difficult personal or professional conversation: clarify the goal and boundary, map perspectives and likely reactions, choose safe timing/channel, draft an ope… | [MODULE.md](modules/difficult-conversation-prep/MODULE.md) |
| `setup-writing-style` | Build or recalibrate a private, evidence-based writing-style profile from text the user explicitly places in scope. | [MODULE.md](modules/setup-writing-style/MODULE.md) |
| `content-research-writer` | Automatically help plan, research, draft, cite, and revise a substantial blog post, article, newsletter, tutorial, case study, thought-leadership piece, or sourced long-… | [MODULE.md](modules/content-research-writer/MODULE.md) |
| `brand-voice` | Define, discover, apply, or audit a brand voice across copy, decks, pages, prompts, and product messaging. | [MODULE.md](modules/brand-voice/MODULE.md) |
| `ai-writing-detox` | Eliminates AI-generated writing patterns that erode reader trust. | [MODULE.md](modules/ai-writing-detox/MODULE.md) |

Supporting files (open only when the module points to them):

- `message-writer`: [voice-and-templates.md](modules/message-writer/references/voice-and-templates.md)
- `setup-writing-style`: scripts: `modules/setup-writing-style/scripts/stylometry.py`
