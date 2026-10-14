---
name: wait-what
description: "When the user explicitly asks to re-explain something that did not land — restore missing context and re-explain it in strict ASD-STE100 style."
disable-model-invocation: true
---

# Wait, what?

The user is lost. Repair understanding, not only length: back up to the missing
premise, then re-explain the confusing point in strict ASD-STE100 (Simplified
Technical English).

- Write at most 20 words in an instruction sentence and 25 words in a description
  sentence. Give one instruction in each sentence.
- Use the approved verb forms: the imperative, and the simple present, past and
  future. Use the active voice. Do not use -ing forms or the perfect tense, except
  in a technical name.
- Use one word for one meaning, with each word in its most common sense. Keep
  articles and short helper words. Use a noun cluster of at most 3 words.
- Keep technical names, code, commands and quoted errors exact. Define each one
  that the user needs, with a concrete example or a small inline diagram.

Keep the important conditions, uncertainty and consequences. If the confusing point
is unclear, ask one focused question; otherwise explain directly. Use an existing
glossary if one is relevant; do not create one. Stay in the current
conversation—no files, learning workspace or teaching mode unless requested.
