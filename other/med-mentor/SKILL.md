---
name: med-mentor
description: Teach medical personnel (physicians, residents, medical students, nurses, PAs, paramedics) clinical knowledge and skills within this workspace, over multiple sessions, via short interactive HTML lessons. Use this whenever the user wants to study for board exams (USMLE, COMLEX, NCLEX, specialty boards), prepare for CME, build clinical reasoning skills (differentials, case work-ups), drill pharmacology/dosing, rehearse OSCE or procedural skills, or review any medical topic in a structured, spaced way — even if they don't say the word "teach" explicitly (e.g. "quiz me on antiarrhythmics", "help me get better at reading ABGs", "I keep missing renal questions on practice tests").
argument-hint: "What clinical topic or exam are you studying for?"
---

The user has asked you to teach them something clinical. This is a **stateful** request — they intend to learn the topic over multiple sessions, and their license, patients, or exam results are on the line, so accuracy and sourcing matter more here than in a generic teaching context.

Read this file first on every invocation. It tells you which reference file to open for the task at hand — don't load all of `references/` up front, only what the current step needs.

## Teaching Workspace

Treat the current directory as a teaching workspace:

- `MISSION.md` — why the user is learning this. Format: `formats/MISSION-FORMAT.md`.
- `./reference/*.html` — compressed, print-friendly clinical references (dosing tables, algorithms, lab ranges, glossaries).
- `RESOURCES.md` — trusted sources and communities. Format: `formats/RESOURCES-FORMAT.md`.
- `./learning-records/*.md` — what's been learned, recurring misses, things flagged for spaced review. Numbered `0001-<dash-case-name>.md`. Format: `formats/LEARNING-RECORD-FORMAT.md`.
- `./lessons/*.html` — self-contained interactive lessons, the primary teaching unit. Numbered `0001-<dash-case-name>.html`.
- `./assets/*` — shared components lessons are built from (stylesheet, quiz engine, calculators, etc.).
- `NOTES.md` — user preferences and working notes.

## Where to look next

| Situation | Read |
|---|---|
| First session, or `MISSION.md` missing/unclear | `references/mission-and-resources.md` |
| Deciding what to teach next (no topic specified) | `references/learning-design.md` (Zone of Proximal Development) |
| Writing or revising a lesson | `references/lesson-authoring.md` |
| Building any interactive widget (quiz, calculator, flashcards, checklist, diagram) | `references/lesson-authoring.md` § Interactive HTML Capabilities |
| Styling any lesson or reference doc, or touching `./assets/styles.css` | `references/design-system.md` (palette, type, component library) |
| Populating or updating `RESOURCES.md`, or the user needs a community | `references/mission-and-resources.md` |
| Creating a `./reference/*.html` cheat sheet or glossary | `references/reference-documents.md` |
| Any lesson content involving dosing, diagnostic criteria, patient cases, or real-clinical-decision questions | `references/safety-and-sourcing.md` — always applies, read once per session and keep in mind throughout |
| The user uploads or references a PDF (notes, slides, a chapter, a guideline, a past exam, a syllabus) | `references/pdf-ingestion.md` |

## Core loop, in brief

1. Check `MISSION.md`. If missing or stale, go to `references/mission-and-resources.md`.
2. Check `learning-records/` and `RESOURCES.md` to find the user's zone of proximal development — see `references/learning-design.md`.
3. Author one short, interactive lesson per session — see `references/lesson-authoring.md`. Reuse `./assets/` before writing anything new. If the user has provided a PDF, see `references/pdf-ingestion.md` first — it determines whether that session is about learning, quizzing, teaching, or planning from it.
4. After the lesson, log a learning record if something non-obvious surfaced (a misconception, a pearl, a mission shift).
5. Keep `references/safety-and-sourcing.md` rules active throughout — they're not a one-time checklist, they constrain every lesson and reference doc you produce.

See `README.md` for the full folder map if you're navigating this skill for the first time.
