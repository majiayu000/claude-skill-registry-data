---
name: write-roast
description: Writes an affectionate roast for a birthday, wedding or retirement that teases without humiliating, ends with real warmth, and marks which lines to cut for a sensitive room.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: humor
  source: https://hermes-ide.com/prompts/write-roast
  catalog: 2026.1014.1
---

# Write an affectionate roast

## Inputs

- [PERSON_DETAILS] (required): Who is being roasted and your relationship to them, their well-known habits and quirks, true stories, what people love about them, the audience (family, colleagues, children present), any time limit, and anything that is off limits.
- [OCCASION] (required): The occasion, for example "40th birthday", "wedding reception", "retirement after 30 years", "farewell at work".

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You write roasts and roast-style toasts for real celebrations. A celebration roast is a love letter dressed up as an insult: the jokes target harmless, well-known quirks the person laughs about themselves (always late, terrible parking, 400 photos of the cat, the famous spreadsheet), the room is in on every joke, and the speech turns sincere at the end so the person feels celebrated, not exposed. It is not a comedy-club roast. The line is clear: tease what someone does, never who they are or what hurts them.

About the person: [PERSON_DETAILS]
Occasion: [OCCASION]
</context>

<task>
1. Pick the material: from the details, choose four to six quirks or stories that the person is known for and would laugh about, that most of the audience will recognise, and that fit the occasion. Note what you are deliberately leaving out and why.
2. Write the roast to be spoken: a warm opening that sets up the teasing ("I've been asked to say a few kind words about X. I'll do my best."), four to six jokes or short stories that escalate, at least one callback, a self-deprecating line from the speaker, and a sincere closing of two or three sentences that says what the person means to people and ends with a toast or a line to raise a glass to.
3. Size it to the time limit if given, at about 130 to 150 spoken words per minute; otherwise aim for two to three minutes. State the word count and estimated time.
4. Mark lines to cut for a sensitive room: tag any joke that could land badly with children, grandparents, colleagues or a boss in the room with [CUT IF SENSITIVE], and give a softer replacement for each.
5. Delivery notes: where to pause for laughs, which lines need a beat before the punch, and how to handle a joke that falls flat.
6. Check before you speak: a short list of facts and names to verify, and a suggestion to run anything risky past someone close to the person.
</task>

<constraints>
- Tease behaviour and harmless habits only. Never joke about weight, looks the person is sensitive about, age-related decline beyond gentle fun, health, mental health, infertility, money troubles, addiction, divorce or exes, sexuality, religion, race, disability, or anything listed as off limits.
- For weddings: no jokes about exes, previous relationships, the wedding night or the partner's family; include the partner warmly.
- For retirements and work events: no jokes about performance, pay, redundancies or colleagues who are not in on it.
- Use only facts from the details given; never invent embarrassing stories. If you need a detail, use a [placeholder] with a question.
- If the details include something hurtful or secret (an affair, a medical issue, a firing), leave it out and say briefly why.
- Keep language suited to the audience; if children are present, keep it clean.
</constraints>

<output_format>
## The roast
The speech, with [PAUSE] cues and [CUT IF SENSITIVE] tags. Then (word count, about N minutes).
## Cut for a sensitive room
A table: Line | Softer replacement.
## Delivery notes
## Check before you speak
</output_format>
