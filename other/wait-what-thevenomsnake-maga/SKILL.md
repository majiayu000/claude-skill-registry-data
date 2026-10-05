---
name: wait-what
description: "Re-pitch an explanation that did not land. Use automatically when the user signals that they did not understand the previous explanation, asks for the actual problem or missing premise, or requests a clearer explanation in different words. Also use when explicitly invoked as $wait-what. Do not use for an ordinary follow-up that asks for new information."
---

# Wait What

Stop. The previous explanation did not land. Re-pitch that explanation:

- add the premise or context the listener was missing;
- use the listener's current language and the project's ubiquitous language from
  `CONTEXT.md` when available (follow `CONTEXT-MAP.md` to the right one if the
  repository has more than one);
- when writing English, prefer ASD-STE100 Simplified Technical English; in
  another language, use the same controlled plain-language discipline;
- prefer a concrete observable sequence over invented jargon or process labels;
- make it shorter and clearer, not shorter and blunter.

Answer in place. Keep the current conversation and create no Ticket, file, task,
or repeated implementation work. Treat a genuinely new question as new
information instead of failed comprehension.
