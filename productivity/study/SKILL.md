---
name: study
description: Learn a topic from the user's own notes and sources (with or without a course), turn it into flashcards, and run spaced-repetition quizzes; use for "/study <topic>", "explain X to me", "make cards for X" or "/study quiz".
model: sonnet
effort: medium
argument-hint: "<topic> | quiz [topic]"
---

# Study

Learn a topic in plain words from your own notes, then remember it with short quizzes.

## When to use

- You say `/study Porter Five Forces`, "help me revise NPV" or "explain this to me".
- You say `/study quiz` or "quiz me". Cards that are due today are asked one at a time.
- You want flashcards from lecture notes or readings that are already in your vault.

## Before you start

1. Read `vault/80_me/USER.md` for your name, what you are learning or working on, and your language.
2. Pick the mode from the first word of the argument:
   - `quiz` (or "quiz me"): follow `workflows/quiz.md` straight away. Do not run clarify: quiz mode needs no topic, course, depth or exam date (a topic after `quiz` only narrows which due cards to ask).
   - anything else: learn mode, `workflows/learn.md`.
3. **Learn mode only:** run the clarify step (`/clarify`, type `study`), and only for what is not already clear. If the topic is obvious from the request or the vault (and the course, when one applies), skip it and show the one-line summary. Otherwise ask one question at a time, and skip anything you can already see in the vault:
   - Topic: what exactly?
   - Course, only if one applies: which one? Look in `vault/20_areas/courses/` first and offer the matches as choices. A topic from work or your own reading needs no course.
   - Depth: quick overview, solid understanding, or exam-ready? (default: solid understanding)
   - Exam date, optional. If there is one, it decides how many cards and how soon.
4. Get today's date from the system, never from memory: `node system/scripts/date.mjs` (local date).

## Steps

### Learn mode (`/study <topic>`)

Full detail is in `workflows/learn.md`. In short:

1. Clarify (above, only if the topic is unclear, or a course applies and is unclear). Show a one-line summary and wait for a yes.
2. Find the user's sources: course notes in `vault/20_areas/courses/<course>/` (when a course applies), source notes in `vault/40_sources/notes/`, wiki pages in `vault/30_wiki/`. Search by topic name, synonyms and, when there is one, the course name.
3. Explain the topic Feynman style: a simple analogy, the idea in plain words, then one worked example. Use only what the sources say. Cite every claim: `[Source: [[note]] | YYYY-MM-DD | confidence: high|medium|low]`.
4. Say clearly what is missing. Offer `/ingest` (add the slides or reading) or research (the `researcher` agent). Never fill gaps from memory without the label `[Inference]` or `[Unverified]`.
5. Create 5 to 10 cards in `vault/50_learning/cards/<topic-slug>/` (format in `workflows/learn.md`). Mix recall questions with application questions. Each card links to its source.
6. Schedule: each new card is box 1 and due tomorrow.
7. Add one task for the review day:
   `node system/scripts/tasks.mjs add "Review N cards" --tag study --due <tomorrow> --priority medium --link "50_learning/cards/<topic-slug>"`
   If a "Review N cards" task already exists for that date, tick it and add one with the new total (see `workflows/learn.md`, step 4).

### Quiz mode (`/study quiz [topic]`)

Full detail is in `workflows/quiz.md`. In short:

1. Collect cards with `status: "active"` and `due` on or before today. Limit to the topic if one was given.
2. Ask one card at a time. Show only the question. Wait for the answer.
3. Grade kindly. Show the correct answer and the source link. Count it right if the idea is right, even if the wording differs.
4. Update `box` and `due` (schedule below).
5. Summarise: score, strongest and weakest topics, next due date.
6. Update the review task for the next due date.

### Leitner schedule (SPEC section 12)

| Box the card lands in | Due again after |
|---|---|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 16 days |
| 5 | 35 days |

Right answer: box plus 1 (box 5 stays at 5). Wrong answer: back to box 1. The new `due` is today plus the days for the new box.

### Model routing

- Card writing and explanations: sonnet / medium (this skill).
- Grading answers in quiz mode: the `helper-triage` agent (haiku / low) is fine. If you delegate grading, send only the question, the correct answer and the user's reply.
- A deep check of a whole card set is a `review` job: give it to the `helper-review` agent (sonnet / high, read-only). Read its findings yourself before you tell the user the set is fine.

## Outputs

- Cards: `vault/50_learning/cards/<topic-slug>/<Card title>.md`.
- A task tagged `#ab/study`: "Review N cards", due on the next review day.
- A short explanation in chat, with citations. Nothing else is saved.
- In quiz mode: updated `box` and `due` on each graded card, and an updated review task.

## Safety

- Ground the explanation only in the user's sources. Label everything else `[Inference]` or `[Unverified]`.
- Never invent a citation, a page number or a quote.
- Never delete a card. To retire one, set `status: "retired"` (ask first).
- This skill helps the user learn. It does not write answers for graded coursework.
- No personal data about other people in cards.
- Cards are written only inside `vault/50_learning/cards/`.

## Extend this

See `system/blueprints/study-extras.md`: session notes from a syllabus (a whole course is set up by `/course`), lecture transcript ingest, FSRS scheduling or Anki export, a mastery map and exam mode.
