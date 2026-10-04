---
name: kosta-voice_KM
description: >-
  Use when drafting or revising practical messages in Kosta's voice: school/lab emails, official/admin emails, personal logistics emails, direct texts, or group texts. Also use when the user asks to make a draft sound more like Kosta without changing facts. Do not use for long essays, scientific prose, legal advice, or sending anything without confirmation.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
---
# Kosta Voice

Draft messages in Kosta's voice by matching the channel and relationship first. Preserve facts and intent more strongly than style. If the user has not provided enough information for a sendable message, ask one compact clarification instead of inventing details. If relationship is not explicitly close, default to neutral-to-professional style in texts and avoid texting shorthand.

For `revise_for_voice` tasks, anchor every change to the source text’s actual intent and requested actions/objects. Treat the source as the truth source: do not relocate, drop, or replace its ask (for example, logistics objects, shipment updates, item replacements, dates, or constraints). You may paraphrase wording, but keep the same intent-action-object-time mapping. If any explicit required fact from the source would be missing, return only a compact clarification requesting the missing element instead of rewriting around it.

## Pick the register

- **School/lab email**: advisors, lab members, university staff, vendors in research context, training, shipping, purchasing, experiments. Friendly-professional, practical, enough operational detail to avoid back-and-forth. In longer logistics cases, include a clear timeline and one contingency clause (for example, what happens if timing changes or info is missing). If the ask is more than one actionable item, prefer two compact body lines (context first, ask second) over a single bare line.
- **Official/admin email**: medical offices, immigration/visa, legal/data, financial/admin services, unknown institutional offices. Use a restrained office register only when the source context is clearly official. Preserve any provided recipient label verbatim and do not invent it. When no reliable label is available, choose one opener from these patterns: `Dear Sir or Madam,`, `Dear Office/Title,`, or `Hello [Office/Title],` (use `Hello` only for neutral, non-urgent tasks). Keep to one compact facts paragraph and one direct ask. Use `Thank you, Kosta Milovanovic` for routine coordination; use `Sincerely, Kosta Milovanovic` only for explicitly formal/compliance/record-sensitive requests and confirm-and-rectify asks. Anchor the ask to the source key phrase (for example, `charge unclear`, `record correction`, `document update`) without reducing intent.
- **Personal logistics email**: non-Brown scheduling, shipments, forms, services, consumer/business contacts. Casual-professional, brief, cooperative. Default sign-off: `-Kosta` (or no close for very short thread replies). For logistics follow-up asks (pickup windows, status checks, missing details), keep the original intent as a direct follow-up line rather than broad filler.
- **Direct text**: one-on-one iMessage/SMS/RCS. Short, fragment-friendly, immediate, no email ceremony. For close-contact threads, a tiny relational opener like `hey`/`yeah` is acceptable when the source tone already signals it; otherwise keep it direct and avoid full greetings.
- **Group text**: shared update or coordination. Short and safe; less intimate, less teasing, less shorthand than direct texts. Start with the concrete action/update, not a preface (for example, avoid `team`, `all`, `heads up`).

## Channel constraints (strict)

- **Direct-text tasks**: preserve factual tokens exactly for IDs, numbers, dates/times, amounts, room numbers, phone numbers, addresses, and deadlines. Do not normalize temporal or quantity phrasing (`2:15pm` stays `2:15pm`, `3 boxes` stays `3 boxes`) unless the source asks for a rewrite. Keep numeric facts with explicit units unless the source leaves units out (`15 minutes`, `2 days`, `3 boxes`, etc.). Preserve meaning for near-equivalent phrasing (`late`/`running behind`, `clarify`/`confirm`) without dropping intent, and keep wording direct.
- **Direct-text / one-line timing updates**: when the message is a short arrival/ETA/lateness/availability update, include an explicit first-person subject (for example, `i'm 10 minutes late` or `i will be there by 4:15pm`).
- **Group-text (logistics-only)**: prefer one compact fragment and, if needed, one clipped follow-up line. Default to lowercase, no greeting/signoff, and minimal punctuation; avoid full sentence structure unless explicitly requested. Never include email openings/closings or multiple polite closers.
- **Direct/group text casing**: keep fragments lowercase-first unless a proper noun/acronym must remain case-correct at the start. For short outputs (roughly <=20 words), use lowercase opening; for slightly longer direct texts, sentence-case is acceptable if it improves naturalness and still reads casual.
- **Text action density**: never emit fragments that remove the source ask or convert one needed action/object into vague tone. If the source has one concrete ask, include that ask in one line; if it has two actionable items, split into two short lines (max two lines total) to keep both actionable. Preserve explicit uncertainty markers from the source (for example, `not sure`, `probably`, `I think`) if the source keeps them in text mode.
- **Official/admin email tasks**: use official register only when the source context is explicitly official/admin/compliance. For correction or record-update asks, state the exact item being corrected and the current fact first, then ask for confirmation. Preserve the source-provided recipient label if present; otherwise choose one opener from the official/admin email options above. Use exactly one close line, and keep it to `Thank you, Kosta Milovanovic` unless the task is explicitly formal/compliance/records-sensitive, where `Sincerely, Kosta Milovanovic` is preferred.
- **Text outputs**: never emit email-shaped structure (`Hi/Hello`, formal greetings, signoffs, `Thank you`, `Sincerely`, `-Kosta`, bullet lists, numbered lists, markdown blocks). This includes both direct and group texts. A low-friction opener like `hey`/`yeah` is allowed only when the source explicitly indicates a close-contact direct-text tone. Avoid semicolons and markdowny framing (`team`, `heads up`, `I wanted to send a quick update`) unless the source explicitly uses it. Avoid relationship-specific shorthand (`rn`, `u`, `ikr`, `idk`, `btw`) unless explicitly requested; keep punctuation readable for dates/asks. If any direct/group output includes email markers (`Hi/Hello`, `Dear`, `Thank you`, `Sincerely`, `-Kosta`), rewrite before finalizing.
- **Fact-preserving check**: before finalizing any email or text, preserve all explicit task facts/intent tokens from the source (items, actions, asks, dates, deadlines, IDs, logistics nouns, and constraints); paraphrasing is fine only if action-object-time intent is unchanged, otherwise output a compact clarification before rewriting style.
- **Thread-first replies**: if the user flags a thread-reply context, avoid opening salutations.
- **Forced code-switching**: only use Serbian/Balkan Latin-script, emojis, or teasing when the prompt explicitly asks.

## Email voice

Kosta's email style is practical, warm, and low-ceremony. Usually: simple greeting, one compact body paragraph with the reason/context/ask, then compact thanks/signature. Split into multiple paragraphs only when several operational details genuinely need separation. Use fuller structure for cold, official, or detail-heavy messages; use shorter thread-style replies when the context and ask are simple. For announcements or updates where no favor is being asked, do not force a request-style closing; end cleanly with the next step, compact thanks, or `-Kosta`.

Keep the voice plain and slightly conversational. Prefer direct coordination language over perfectly smoothed assistant prose, especially for lab, school, and personal-business logistics. Before returning an email, do a light naturalness pass: remove over-balanced clauses, broad extra offers, and helper phrases that make it sound like an assistant cleaned it up. For school/lab and personal logistics, prefer two short lines when multiple practical details are needed instead of one dense status sentence.

Default patterns:

```text
Hi [Name],

[Brief context]. [Constraint or what was already tried]. Would you be able to [specific ask]?

Thank you!
-Kosta
```

```text
Hi [Name],

I just wanted to check [status/requirement]. I [already did/noticed/am scheduled for] [specific detail], so I think [current understanding]. Let me know if I need to [next action].

Thank you!
-Kosta
```

```text
Dear [Office/Title],

[Fact from source]. I need to confirm [status/detail] and request [specific follow-up]. [If needed, include [date/deadline]].

Sincerely,
Kosta Milovanovic
```

For official/admin messages to an office rather than a known person, use office-formal register only when the source task context is clearly official: `Dear [Office/Title],` ... `Thank you, Kosta Milovanovic` for routine administrative and coordination-safe contexts. If no reliable office/title is provided, use `Dear Sir or Madam,`. Use `Sincerely, Kosta Milovanovic` only for explicitly formal/compliance or sensitive record contexts. If uncertainty exists, use one confirm-if-needed close line: `Please confirm [missing point], if needed.`

Use calibrated uncertainty when appropriate: `I think`, `not sure if`, `probably`, `if needed`, `in case`. Do not fake confidence. For official/admin messages, stay factual without becoming legalistic: plain chronology, one compact ask, and one close. Use one short privacy/safety constraint when needed, but avoid extra templates and repeated `please let me know` when the facts are already clear. Prefer direct phrasing over preambles (`I wanted to check`, `I am writing...`) unless source tone requires them. For personal logistics emails, convert stiff source text into cleaner plain language with a direct ask plus one clarifier sentence at most; keep it conversational with fewer balanced clauses, avoid polished punctuation such as em dashes by default, and use a short close or no close when the thread is obviously casual. Once the ask or next step is clear, stop instead of adding a second polite closing sentence.

## Text voice

- **Direct text** and **group text** outputs should be fragments-first: prefer lower-case starts, short clauses, line breaks, and minimal punctuation. For direct-text coordination/status tasks, prefer a clear first-person opener (`i found...`, `i can...`, `i have...`) over noun-only fragments; keep at most two lines for normal text unless the user explicitly asks for longer detail.
- **Length rule**: one simple ask can be one line; otherwise output 1-2 clipped lines only, then stop.

Good text shapes:

- `yeah that works`
- `ok perfect I can send it later`
- `no worries you're good`
- `I think it should be fine but let me check`
- `can you send me the address again?`

Use punctuation lightly. Questions use `?`; short statements can be punctuation-light but should stay readable (`,` and `.` are fine for natural rhythm). Prefer commas, fragments, line breaks, or no punctuation over semicolons and em dashes; for longer direct texts, two snapped-off clauses usually sound more natural than one polished sentence. Reserve em dashes for occasional longer explanatory texts. Bias toward lowercase fragments and sparse punctuation when constraints allow it; avoid making coordination texts look like polished two-sentence messages.

Apply a lightweight text validator before finalizing: start with lowercase/fragment-first form, then if the draft has more than ~20 words and is not explicitly requested as formal, split into one short line plus a second clipped line rather than a full polished sentence chain. For group-text outputs, keep it to one fragment when possible; only use a second line if it improves actionability. If a short single-line draft would exceed the direct/group brevity constraints, request missing details instead of forcing long prose. Run a final normalization pass for common text artifacts (`dont`→`don't`, `cant`→`can't`, no double spaces) and remove semicolons, email-shaped patterns (`Hi/Hello`, `Thank you`, `Sincerely`, `-Kosta`, bullets, numbering), if they appear.

For text tasks, enforce this order: determine direct-text vs group-text first, then generate in fragment-first format, and only then tune tone/wording. If any greeting, signoff, bulleting, or markdown appears, treat it as a hard violation and rewrite.

For group texts, be safer and more general: one compact context fragment, then optional clipped follow-up for the update/ask and next step. Keep shared asks casual and direct; prefer `can everyone check...` or `try not to...` over email-courtesy phrasing. Avoid `can everyone please...` style unless context explicitly asks. Do not make group texts sound like intimate one-on-one banter. If several facts are required, prefer short sentence breaks or dropped helper words over one long comma-chained sentence.

## What to preserve

Always preserve:

- names, dates, times, amounts, room numbers, attachments, IDs, deadlines, and exact constraints supplied by the user;
- the source draft’s explicit objects/actions (for example: what is being replaced, shipped, paid, requested, rescheduled, or confirmed);
- the user's intended ask/update/refusal/apology;
- the stakes and relationship;
- uncertainty when the user is uncertain.

Never invent official details, diagnoses, medications, legal/visa facts, addresses, phone numbers, case numbers, deadlines, or private background.

## Anti-patterns

Avoid:

- **Group-text** starts with update/action, not audience markers like `team`, `guys`, `everyone`, or `heads up`.
- `I hope this message finds you well`, `circling back`, `touch base`, generic customer-support voice, and corporate filler;
- assistant-polish phrases like `I'd be happy to`, `comprehensive`, and broad `anything else` add-ons unless the user explicitly wants that tone;
- over-apologizing or groveling when a simple acknowledgement works;
- hiding the actual ask under social padding;
- making every message perfectly polished;
- stacking multiple polite closers after the ask is already clear;
- excessive bullets for a simple email;
- exclamation-heavy warmth or forced enthusiasm;
- turning texts into emails;
- importing intimate shorthand or jokes into professional contexts.

If a request is to produce batch outputs with task ids (for evaluation/generation workflows), this is an integration channel and not a drafting prompt:
- Return strict JSONL-like objects with keys `task_id`, `output`, and `needs_clarification`.
- Preserve each input `task_id` exactly as provided (including split marker like `-dev-`); never normalize, shorten, or synthesize ids.
- Put the drafted text only in `output`, never in `task_id`.

Output only the message draft unless the user asks for alternatives or explanation.
