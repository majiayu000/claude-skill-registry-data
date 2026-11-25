---
name: write-speech
description: Writes a speech for an occasion such as a toast, keynote, eulogy or graduation to a target length, written for the ear and built only from the stories and facts the user provides.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: public-speaking
  source: https://hermes-ide.com/prompts/write-speech
  catalog: 2026.1014.1
---

# Write a speech

## Inputs

- [OCCASION] (required): The occasion and your role in it, for example "best man's toast at my brother's wedding", "eulogy for my grandmother", "opening keynote at a 200-person industry conference".
- [CONTENT] (required): Your raw material: stories, facts, names, the message you want to leave, things to avoid. The more specific, the better.
- [MINUTES] (optional; default: 5): Target speaking time in minutes.
- [TONE] (optional): Optional tone, for example "funny but warm", "solemn", "inspiring without clichés".

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
A speech is heard once, at the speaker's pace, with no rereading. Writing for the ear means short sentences, one idea at a time, concrete stories over abstractions, signposts ("Three things I learned…"), deliberate repetition and callbacks, and an ending the audience can feel coming. People speak a prepared text at about 120 to 140 words a minute.

Occasion conventions matter:
- **Toast:** short (2 to 4 minutes), affectionate, inclusive of the whole room; no stories that embarrass, exclude or mention exes; ends by asking everyone to raise a glass to a named person or couple.
- **Eulogy:** honours a specific life with specific stories; allows both grief and gentle humour; speaks to the family; accuracy matters more than polish.
- **Keynote or talk:** one central idea, a story that carries it, and a clear takeaway or call to action.
- **Graduation or award:** speaks to the honourees, not about the speaker; avoids stock advice ("follow your dreams") in favour of one specific, earned lesson.
</context>

<task>
Write a speech for: [OCCASION]. Target length: [MINUTES] minutes.Only if [TONE] was provided:  Tone: [TONE].
<content>
[CONTENT]
</content>

1. If the content has no specific stories, names or details to build from, ask up to three questions that would draw them out (for example "What is one moment that shows who she was?") and stop.
2. Pick the one message the audience should leave with, drawn from the content.
3. Choose the strongest one to three stories or details from the content that carry that message. Leave out the rest rather than listing everything.
4. Structure: an opening that earns attention in the first 20 seconds (a story, a striking line, a direct address; not "For those who don't know me…" unless that is genuinely needed), a body that builds through the chosen stories, and a close that returns to the opening image or line and lands the message (with the raised-glass line for a toast).
5. Write for the ear, following the conventions above for this occasion. Mark [pause] at two to four key moments.
6. Hit the length: about 130 words per minute of the target.
</task>

<constraints>
- Use only the facts, names and stories in the content. Never invent anecdotes, quotes, dates or details about real people; where the speech needs one, write `[story: …]` describing what kind would fit.
- No humour at anyone's expense, no inside jokes most of the audience will not get, nothing a family member or guest might be hurt by. If the content contains something risky for the occasion, leave it out and say why in Delivery notes.
- Avoid clichés and stock quotations unless the content supplies a quote that matters to the speaker.
- Use the speaker's own phrasing from the content where it is vivid; it will sound like them.
</constraints>

<output_format>
## Speech
The full text, in short paragraphs, with [pause] marks.
## Length
"N words, about M minutes at 130 words a minute" and whether it hits the target.
## Delivery notes
Three to five specific tips for this speech (where to slow down, where to look up, the line to memorise).
## Placeholders
Each `[story: …]` or missing detail to fill. "None" if none.
## If you run long
Which paragraph to cut first, and which second.
</output_format>
