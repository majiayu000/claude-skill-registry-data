---
name: recall
description: Answer a question from the vault with citations and an honest confidence level, or say the vault does not know. Use when the user asks "what do I know about X", "did we decide Y", "have I talked to Z about W", "remind me", "search my vault", or asks you to confirm something they half-remember.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, retrieval, question-answering]
    related_skills: [prioritize, challenge-decision]
    requires_toolsets: [second_brain]
---

# Recall (Hermes edition)

The tool finds the evidence; you write the answer. The one rule that matters: **an answer with
no citation is a guess**, and a guess in a second brain is worse than a shrug.

1. `sb_recall(question=<the user's question, verbatim>)`. It returns entities, citations with the
   matching lines and their dates, a `confidence` level, and `gaps`.
2. Read the `confidence` before writing a word:
   - `stated` / `high` → answer directly, citing `path` and date for each claim.
   - `medium` → answer, and name what it rests on ("one note, from 2026-03").
   - `speculation` → do not answer the question. Report what the vault has *around* it instead.
   - `unknown` → say the vault does not know. Do not fill the gap from general knowledge.
3. Need more than the excerpt to be sure? `sb_read(path)` on the two or three notes that matter.
   Prefer reading fewer notes fully over skimming many.
4. Never merge what the vault says with what you happen to know. If you add outside context, mark
   it explicitly as outside the vault, and date it `(as of YYYY-MM)`.
5. Answer in the working language, in this shape:
   - the answer in one or two sentences;
   - the citations, one per line: `[[path]] (date) — the line that says so`;
   - confidence, and what would raise it.
6. If `confidence` was `unknown` or `speculation`, offer to capture the answer with `/braindump`
   so the next question lands differently. Do not capture it yourself without being asked.
7. Read-only skill: never write a note here, and never commit.
