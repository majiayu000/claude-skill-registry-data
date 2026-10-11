---
name: default-video-digest
description: Turn a transcript into grounded, structured notes for deep study.
version: 1.0.0
---

# Deep study notes

## Use when

Creating the long-form updated Markdown artifact from a normalized video transcript.

## Rules

1. Preserve the raw transcript separately; never overwrite it.
2. Do not invent claims, speakers, chapters, or timestamps.
3. Write in the transcript's primary language unless metadata strongly indicates
   another language.
4. Every chapter and important claim must link to the nearest source timestamp. If
   useful timing is unavailable, omit links rather than inventing them.
5. Distinguish what the speaker said from your own synthesis or questions.
6. Explain important concepts and reasoning chains instead of merely listing topics.
7. If the transcript is incomplete or low quality, state that prominently.

## Output

Produce these sections:

1. `Core thesis` — the purpose, conclusion, and overall argument.
2. `Knowledge map` — how the major concepts relate.
3. `Guided walkthrough` — timestamped sections with detailed explanations.
4. `Claims and evidence` — important claims paired with their support.
5. `Concepts and terminology` — definitions in context.
6. `Questions and checks` — assumptions, counterarguments, and points to verify.
7. `Study and action list` — review prompts, exercises, or next actions.
