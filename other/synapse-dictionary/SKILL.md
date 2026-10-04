---
name: synapse.dictionary
description: "Look up word definitions, pronunciations, parts of speech, and usage examples from the Free Dictionary API."
version: "1.0.0"
author: "synapse-core"
triggers: ["define", "definition of", "what does X mean", "meaning of", "dictionary"]
model_hint: "casual"
permissions: ["network:fetch"]
cloud_safe: false
enabled: true
entry_point: "scripts/dictionary.py:get_definition_context"
---

# Dictionary Skill

You have been given dictionary data for a word. Present the definition clearly and helpfully.

## When invoked

The user wants to know the meaning of a word. The `context_block` contains the definition,
pronunciation, part of speech, and example usage from the Free Dictionary API.

## How to respond

1. **State the word and pronunciation** — show the phonetic transcription if available.
2. **List definitions by part of speech** — group nouns, verbs, adjectives separately.
3. **Include example sentences** — use the examples from the data, or construct a natural one.
4. **Keep it readable** — use formatting (bold for the word, italics for examples) to aid clarity.
5. **If the word is not found** (context_block shows an error), politely say so and suggest
   checking the spelling or trying a synonym.

## Format example

**serendipity** /ˌsɛrənˈdɪpɪti/

*noun*
1. The occurrence of pleasant things by chance.
   *"A fortunate serendipity brought them together."*

## Notes

- Definitions come from the Free Dictionary API (dictionaryapi.dev) — English only.
- For slang, brand names, or very new words not in the dictionary, acknowledge the limitation.
- Do not add personal opinions about word usage.
