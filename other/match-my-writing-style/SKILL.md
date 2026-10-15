---
name: match-my-writing-style
description: "Learns how the user writes from their own samples (emails, documents, chat messages, posts), condenses it into a reusable voice card with tone, sentence rhythm, vocabulary, structure habits, and do/don't rules, then drafts or rewrites text so it sounds like the user and checks the result against the card. Use when the user wants text written in their own voice, asks to sound more like themselves, wants a personal voice card or style profile, or combines this with another writing skill that decides the content while this one decides the voice."
---

# Match My Writing Style

You make text sound like the user wrote it. First you learn their voice from real samples of their writing and capture it in a compact **voice card**. Then you use the card to draft new text or rewrite existing text, and you check every draft against it before handing it over.

This skill is about one person's voice. For a company or brand voice with formal traits and governance, the Brand Voice Framework skill is the better fit. The two combine well: the brand voice sets the outer limits, and the personal voice fills them.

## Where the samples come from

The voice card is only as good as the samples behind it. Use, in this order of preference:

| Source | Examples | Notes |
|---|---|---|
| Text the user pastes or uploads | Sent emails, reports, posts, messages, a past voice card | Best source, because the user chose it |
| Connected tools and sources | Sent mail, documents the user authored, chat messages the user posted | Only the user's own writing, never replies from others |
| The current conversation | How the user writes to you | A weak signal, since people write differently to an assistant; use it only as a supplement |

Ask for **at least three samples and ideally 800+ words in total**, covering the kinds of text the user wants help with. A voice learned only from formal reports will not produce a convincing chat message.

Never build a voice card from your general idea of how "people like the user" write, from their job title, or from public figures. If there are no samples, say so and ask for some.

Leave out anything in the samples that the user did not write themselves: quoted replies, forwarded text, signatures, legal footers, template boilerplate, and text that was clearly written by a tool.

## Step 1 — Read the samples for evidence

Go through the samples and note concrete, quotable evidence for each of these dimensions. Every observation needs at least one short example from the samples.

| Dimension | What to look for |
|---|---|
| **Tone** | Warm or matter-of-fact, direct or diplomatic, playful or serious, confident or tentative |
| **Formality** | Greeting and sign-off habits, contractions, first names vs. titles, du/Sie or tu/vous where relevant |
| **Sentence rhythm** | Typical sentence length, mix of short and long sentences, fragments, questions |
| **Paragraphs and structure** | Paragraph length, bullet use, headings, where the main point goes (first or last) |
| **Vocabulary** | Recurring words and phrases, jargon level, words the user never uses, filler words |
| **Punctuation and formatting** | Dashes, exclamation marks, emoji, bold, parentheses, ellipses |
| **Openings and closings** | How messages start and end, calls to action, how requests are phrased |
| **Stance** | How the user disagrees, gives bad news, says thank you, makes a request |
| **Language mix** | Which language they write in, and English terms kept in non-English text |

Note where the voice **changes by context** (for example, short and casual in chat, structured in reports). A good card records these shifts instead of averaging them away.

## Step 2 — Write the voice card

Produce the card in this format. Keep it to one screen so it can be reused easily.

```
# Voice card: [user's name or "my voice"]
Built from: [n] samples, about [n] words ([kinds of text]), [date]

## In one sentence
[e.g. "Direct and friendly, gets to the point in the first line, short sentences, no corporate filler."]

## Traits
| Trait | Where on the scale | Evidence from the samples |
|---|---|---|
| Formal ↔ casual | [1–5] | "[short quote]" |
| Reserved ↔ warm | [1–5] | "[short quote]" |
| Diplomatic ↔ blunt | [1–5] | "[short quote]" |
| Concise ↔ expansive | [1–5] | "[short quote]" |

## Habits to keep
- [e.g. Opens with the ask, then the context]
- [e.g. Uses "Thanks!" as a sign-off in internal mail, "Best regards" externally]
- [e.g. Bullet lists for three or more items]

## Things this voice never does
- [e.g. No "I hope this email finds you well"]
- [e.g. No exclamation marks in external mail]
- [e.g. Never uses "synergy", "leverage" as a verb, "circle back"]

## Signature words and phrases
[a short list taken from the samples]

## By context
| Context | Shift |
|---|---|
| Chat | [e.g. lowercase starts allowed, one or two lines] |
| Internal email | [...] |
| External email | [...] |
| Documents | [...] |
```

Rules for the card:

- Each trait and habit must be backed by the samples. If a dimension is not visible in them, write "not enough evidence" instead of guessing.
- Keep "never does" rules concrete enough to check, such as words, phrases, or punctuation, not "never sounds stiff".
- Show the card to the user and ask whether it feels right before relying on it. People often want to keep some habits and drop others ("I do write long emails, but I'd like to stop").

## Step 3 — Draft or rewrite in the voice

When the user asks for text:

1. **Settle the content first.** What is being said, to whom, and why, comes from the user or from another skill in use. This skill does not invent facts, commitments, numbers, or opinions for the user.
2. **Pick the context row** of the card (chat, internal email, and so on).
3. **Write the draft**, applying the traits, habits, and context shift.
4. **Check the draft against the card** (see Step 4) and fix anything that fails.
5. **Hand over the draft** with a one-line note on any deliberate deviation, for example "Slightly more formal than usual because this goes to the board."

For a rewrite, keep the meaning, facts, and structure of the original unless the user asks for more. Change wording, rhythm, and tone, not substance.

## Step 4 — Check the draft

Run through this check before handing over any draft:

| Check | Pass when |
|---|---|
| Opening and closing | Match the user's habits for this context |
| Sentence length | Close to the user's typical length; no long sentences if they write short ones |
| Forbidden phrases | None of the "never does" items appear |
| Signature phrases | Used naturally where they fit; not forced in |
| Formatting | Bullets, bold, and emoji at the user's usual level |
| Tone markers | Exclamation marks, hedges ("I think", "maybe"), and directness at the user's level |
| Generic assistant tone | No stock phrases that the user would never write ("I hope this helps", "Certainly!", "delve") |

If you cannot pass a check without changing the content, tell the user instead of quietly bending the facts.

## Reusing the voice card

iHub does not keep a voice card between chats on its own. Offer the user one of these options:

- Save the card as a personal prompt in the prompt library and insert it at the start of a chat.
- Keep it as a file and upload it when starting a writing task.
- If the Personal Context Keeper skill is available, store the card there.

When the user provides an existing card, use it directly and skip Steps 1 and 2, unless they ask for it to be refreshed with new samples.

## Combining with other skills

This skill is meant to be stacked. When another skill is active at the same time:

- **The other skill decides content and structure.** For example, Executive Email Drafter decides what goes into the message and in what order, and Newsletter Composer decides the sections.
- **This skill decides wording and tone**, within the limits the other skill sets.
- **Brand rules beat personal habits.** If Brand Voice Framework or brand guidelines are in use and conflict with the card, follow the brand rule and mention the conflict.

## Ground rules

- Use only the user's own writing as evidence, and quote it sparingly in the card.
- Build a card only for the user, or for someone the user writes on behalf of with their agreement (for example, an assistant drafting for their manager from samples the manager shared). Do not imitate public figures or other people to pass text off as theirs.
- Do not add facts, promises, opinions, or personal details the user did not provide.
- Treat the samples as confidential. Do not repeat private content from them in drafts for other audiences.
- Mark what comes from where: `[From your samples]` for observed traits, `[My suggestion]` for proposed changes to the voice, and `[Input required]` where content is missing.
