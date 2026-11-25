---
name: analyze-poem
description: Analyses a poem's meaning, form, imagery, sound and context, and offers more than one reading, each supported by evidence from the lines. Use when studying, teaching or reading a poem closely.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: poetry
  source: https://hermes-ide.com/prompts/analyze-poem
  catalog: 2026.1014.1
---

# Analyse a poem

## Inputs

- [POEM] (required): The full text of the poem, with line breaks and stanza breaks preserved, plus the title and poet if known.
- [LEVEL] (optional; default: general reader): Who the analysis is for, e.g. "secondary school", "A-level or AP", "undergraduate", "general reader". Sets the vocabulary and depth.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
Weak poem analysis does one of two things: it paraphrases the poem as if it were a message in code, or it lists devices ("there is alliteration in line 3") without saying what they do. Good analysis starts from the experience of reading, then shows how specific choices on the page (the speaker, the form, line breaks, images, sounds, syntax and shifts in tone) produce that experience, and it accepts that strong poems support more than one reading. Every claim is anchored in quoted words. Context (the poet's life, the period, the tradition the poem answers) can deepen a reading, but it should never replace the words on the page, and invented context is worse than none.
</context>

<task>
Analyse this poem. Audience: [LEVEL].

<poem>
[POEM]
</poem>

1. If the text looks incomplete (it trails off, stanzas seem missing) or only a title was given, ask for the full text and stop. Work only from the text provided; do not quote other lines of the poem from memory.
2. **First reading:** a plain-language paraphrase in three to five sentences, and the first impression or feeling the poem leaves.
3. **Speaker and situation:** who is speaking, to whom, where and when, and what has happened or is happening. Distinguish the speaker from the poet.
4. **Form and structure:** the form (named if it is a received form such as sonnet, villanelle or ghazal, or free verse), stanza pattern, rhyme scheme with letters, and meter. Scan two representative lines, marking stressed syllables, and note where the meter breaks and why that matters. Comment on line breaks and enjambment in at least two specific places.
5. **Imagery and figurative language:** the key images, metaphors, similes and symbols, and the pattern they make across the poem. For each, say what it does, not only what it is.
6. **Sound:** rhyme, assonance, consonance, alliteration, repetition and rhythm, with quoted examples and their effect (speed, weight, music, harshness).
7. **Shifts and tone:** where the tone or argument turns (a volta, a "but", a change of tense or address) and how the ending reframes the opening.
8. **Context:** the poet, period and tradition, only where you are confident and only where it illuminates the text. If the poet is unknown or you are unsure of facts, say so and skip speculation.
9. **Readings:** two or three distinct interpretations (for example personal, historical, formal, or a reading against the grain), each with three or more pieces of quoted evidence and an honest note on what the reading struggles to explain.
10. **Questions to consider:** three open questions for discussion or an essay, matched to [LEVEL].
</task>

<constraints>
- Quote the poem exactly when citing evidence, with line numbers (the first line of verse is line 1; do not count the title, the poet's name, epigraphs or blank lines).
- Match vocabulary to [LEVEL]: define technical terms briefly the first time for school readers; use them freely for undergraduates.
- Do not present one reading as the only correct one, and do not invent biographical facts, dates or critical opinions. Say "I don't know" where the context is uncertain.
- This is a study aid. If the user asks for a finished essay to submit as their own, give the analysis, a thesis and an outline instead, and say they should write the essay themselves.
</constraints>

<output_format>
Use the sections in order as level-two headings. Keep the whole analysis readable in about ten minutes; use short paragraphs and quote, then explain.
</output_format>
