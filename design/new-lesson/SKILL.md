---
name: new-lesson
description: Scaffold a new bilingual (en/es) lesson or topic for this Lessons site — creates the MDX files in the correct locale folders with valid frontmatter, wires in the reusable interactive components, and regenerates OG images. Use when the user asks to "add a lesson", "add a topic", "create a lesson about X", "new lesson", or provides a subject to teach.
---

# Authoring a Lesson or Topic

This project teaches the subject defined in **TOPIC.md** across multiple
slug-based **lesson** pages, in **English and Spanish**. Its mission: take a
learner with **no prior knowledge of the subject** to **complete expert**.
**Read `TOPIC.md` first** — it is the source of truth for subject, mission,
scope, and voice. Follow these steps to add content consistently.

## Mission fit (REQUIRED before scaffolding)

Every topic sits on the **zero-to-expert ladder** that `TOPIC.md` defines:

- **Assume no background** in the subject at the `beginner` tier — define every
  domain term on first use; never lean on jargon the lesson hasn't taught.
- **Set the `difficulty` frontmatter field** (`beginner` | `intermediate` |
  `advanced` | `expert`) — required, same value in the en/es twins. It renders as
  a badge on the catalog graph.
- **Wire `dependencies`** so every concept a non-`beginner` course assumes is
  taught by one of its prerequisites already on the platform.
- **`expert` means expert** — go all the way to quantitative, real-practitioner
  depth; don't stop at "intro".

## 0. Research first — then write with voice, animation, exercises

Before scaffolding, use the **`research-topic` skill** to build an accurate,
sourced brief and outline (concepts, definitions, misconceptions, analogies,
animation opportunities). Never write non-trivial lesson prose from memory.

As you write, apply the companion skills:

- **`lesson-copy`** — voice/tone: witty, lightly sarcastic, analogy-driven copy
  that is genuinely fun to study, without sacrificing accuracy.
- **`lesson-animations`** — include **at least one animation that teaches** the
  core idea (a process/relationship shown moving, not decoration).
- **`exercise-components`** — include **at least one exercise** (multi-answer
  `MCQ`, `Quiz`, or a `concept → definition` matcher), reusing/extending the
  component library rather than inlining one-off JSX.

## Interaction density (REQUIRED — not just at the end)

Lessons must be **interactive throughout**, not a text wall with one quiz at the
bottom. Retention comes from testing right after learning. Aim for **at least
one exercise per `##` section, ideally two** (a prequestion to open, a check to
close). Err on the side of *more* exercises.

- **Open each `##` with a prequestion** (`MCQ pretest`): make the learner *guess
  before reading*. Pretesting boosts encoding even when the guess is wrong, and
  pretests never count toward a `Quiz` score. See `exercise-components`.
- **Interleave checks**: after **each** explanation, add an exercise or
  animation that checks or shows what was just taught. Don't pool questions at
  the end.
- **Rotate types every time** — never the same format twice running: single
  `MCQ`, **multi-answer `MCQ`** (`allowMultiple`), `MCQ pretest`,
  concept→definition `MatchConcepts`, `Categorize` (sort into buckets),
  `FillBlank` (pick-one-of-three cloze), scored `Quiz`, `Reveal` self-checks.
- **For must-remember terms** reach for `FillBlank` — each blank is the right
  term flanked by two plausible distractors, so the learner discriminates rather
  than just recognises. Keep options equal-length; the answer must never be the
  longest. (No `StepThrough` — it was removed; use a numbered Markdown list.)
- **Spaced recall**: write some questions that reference *earlier* sections so
  the user recalls prior material; the end quiz mixes the whole lesson.
- **Animations per concept**: an animation at *each* major
  transformation/process/relationship, beside its explanation — not one hero
  animation per lesson. See `lesson-animations`.
- **Close with a chunking recap**: end every lesson with a learner-built
  `MindMap` (Mermaid "big picture" linking the section concepts) **plus** a mixed
  `Quiz` — not a passive bullet-list summary. See `lesson-animations`.

Apply the same density to the Spanish twin (parity includes exercises and
animations, with Spanish label props).

## Final exam (REQUIRED — every course ends with one)

**Every course (topic) MUST conclude with a final exam as its LAST lesson.**
This is mandatory, not optional — Claude: whenever you finish a topic, or add
the last teaching lesson to one, that topic is not "done" until a final-exam
lesson sits at the end of it. When building a brand-new topic, plan the exam as
the final lesson from the start.

- **Slug & position**: `final-exam` in both locales
  (`src/content/lessons/<lang>/<topic>/final-exam.mdx`), with `order` set to
  **one higher than every other lesson** so it sorts last. Title it as an exam
  (e.g. *"Final Exam: …"* / *"Examen final: …"*).
- **It must be genuinely hard.** The point is to verify the learner truly
  understood everything — not a victory-lap recap. Use **scenario-based,
  multi-step reasoning** with plausible distractors and subtle traps drawn from
  the misconceptions each lesson warned about.
- **Use the `FinalExam` island — NOT `Quiz` and NOT themed recap sections.**
  The final exam is a graded, **irreversible** run: one MCQ at a time, the
  learner submits, the answer **locks for good** (no Back, no Try again, no
  Restart), the result reveals instantly, and the pass/fail score appears only
  after the last question. Don't rebuild the old elaborate flow (pretest →
  `Callout` → `Categorize`/`FillBlank`/`MatchConcepts` per theme → a separate
  scored `Quiz`); that is exactly the over-complex structure `FinalExam`
  replaces. Present the questions **directly**.
- **Keep the page flat and short:** a one-paragraph intro → a
  `Callout variant="warning"` "How this exam works" box (states: answers are
  final, no retries, score shown at the end, pass mark `70%`) → the
  `<FinalExam client:visible passPercent={70} questions={[…]} />` island →
  `## Course Recap` `MindMap` → `## Key Takeaways` `Callout variant="success"`.
- **Question pool: 20–30 fresh MCQs**, covering ALL prior lessons roughly
  proportionally. Mostly single-answer; include **2–4 multi-answer** questions
  (`allowMultiple: true`, multiple options marked `correct: true`). No `pretest`
  here — an exam tests, it doesn't pre-teach.
- **VARIETY IS MANDATORY — repetition is the #1 failure mode.** Vary every axis:
  question *type* (numeric/calculation with the arithmetic shown in the
  explanation, scenario/application, "which statement is TRUE", spot-the-trap,
  definition, side-by-side comparison, cause→effect, ranking-as-single-answer),
  *stem wording* (never reuse the same sentence frame twice in a row; don't open
  five questions with "Which of the following…"), and *difficulty*. Every
  question carries a concise `explanation` teaching the why.
- **Same rules as any lesson**: keep numbers/LaTeX in MDX prose and tables, never
  baked into island option/question text (put numeric scenarios in a table right
  above the island and phrase the question conceptually); ship a full es-ES twin
  with Spanish label props.

## 1. Decide: new topic or new lesson in an existing topic?

- List existing topics: look under `src/content/topics/en/`.
- A **topic** needs `src/content/topics/en/<topic>.mdx` + the `es` twin.
- A **lesson** goes in `src/content/lessons/en/<topic>/<lesson>.mdx` + the `es` twin.

Slugs must be kebab-case and SEO-friendly (e.g. `getting-started`).

## 2. Topic frontmatter (`src/content/topics/<lang>/<topic>.mdx`)

```mdx
---
title: Getting Started
description: A one-line summary used on cards and as the default meta description.
tagline: From the basics to genuine mastery.       # optional, shown under the hero
icon: 🚀                                            # emoji chip
order: 1                                            # sort order in the catalog
accent: brand                                       # 'brand' (blue) | 'accent' (sky)
---

Short intro prose for the topic landing page (rendered in `.prose-lesson`).
```

The Spanish file is identical structure under `.../es/<topic>.mdx`, translated.

## 3. Lesson frontmatter (`src/content/lessons/<lang>/<topic>/<lesson>.mdx`)

```mdx
---
title: Your First Lesson
description: SEO meta description (≤155 chars), specific and compelling.
topic: "en/getting-started"        # MUST be the owning topic's id: "<lang>/<topic>"
order: 1                            # position within the topic
minutes: 6                         # estimated time
updated: 2026-05-30                # ISO date
---
```

- For the Spanish twin, set `topic: "es/getting-started"`.
- Use `##` and `###` headings — they generate the on-page Table of Contents.

## 4. Use the reusable components (import via the `@` alias)

At the top of the MDX body:

```mdx
import { Callout, MCQ, Quiz, FinalExam, Reveal,
         MatchConcepts, Categorize, FillBlank, MindMap } from '@/components/react';
```

Exercise islands: `MCQ` (add `pretest` for prequestions, `allowMultiple` for
multi-answer), `Quiz`, `MatchConcepts`, `Categorize`, `FillBlank`. `FinalExam` is
the graded, lock-on-submit island reserved for a course's final-exam lesson (see
above). Recap visual: `MindMap`. See `exercise-components` and `lesson-animations`
for each.

Interactive islands need `client:visible`; `Callout` is presentational (no directive).

These are the **only** islands the template ships in `@/components/react`: `MCQ`,
`Quiz`, `FinalExam`, `Reveal`, `Callout`, `FillBlank`, `MatchConcepts`,
`Categorize`, `MindMap`, `CourseGraph`, `LessonComplete`, `CourseComplete`,
`ProgressTransfer`. **No subject-specific chart or animation islands exist** —
those you build for your topic (see `lesson-animations` and `exercise-components`
for how to author one the right way).

```mdx
<Callout variant="tip" title="Key idea">State the one thing the learner must remember.</Callout>

<MCQ
  client:visible
  question="What is the core point of this section?"
  options={[
    { text: 'The correct, precise answer', correct: true },
    { text: 'A plausible near-miss' },
    { text: 'A common misconception' },
  ]}
  explanation="Explain why the right answer holds and the distractors don't."
/>

<Quiz client:visible questions={[ /* array of MCQ prop objects */ ]} />

<FillBlank
  client:visible
  text="The {{correct-term|sibling-term|another-sibling}} is what makes this idea {{work|fail|repeat}}."
/>

<Reveal client:visible><Callout>Animates in on scroll.</Callout></Reveal>
```

**Spanish lessons must pass Spanish label props** so the UI is fully localized, e.g.
`<MCQ ... checkLabel="Comprobar" retryLabel="Reintentar" />`,
`<Quiz ... questionLabel="Pregunta" ofLabel="de" scoreLabel="Tu puntuación" restartLabel="Reiniciar" nextLabel="Siguiente" backLabel="Atrás" />`,
`<FillBlank ... checkLabel="Comprobar" retryLabel="Reintentar" instructions="Elige la opción correcta para cada hueco y comprueba." />`.
The `FinalExam` island needs its own Spanish props:
`<FinalExam ... questionLabel="Pregunta" ofLabel="de" submitLabel="Enviar respuesta" lockWarningLabel="Atención: una vez que envíes, esta respuesta es definitiva. No podrás cambiarla." selectHintLabel="Selecciona una respuesta para continuar." nextLabel="Siguiente pregunta" seeResultsLabel="Ver resultados" correctLabel="Correcto" incorrectLabel="Incorrecto" correctAnswerLabel="Respuesta correcta" explanationLabel="Explicación" completeTitleLabel="Examen completado" scoreLabel="Has acertado" passLabel="Aprobado" passMessage="Has superado el listón: buen trabajo." failLabel="No superado" failMessage="Esta vez por debajo del aprobado: repasa las lecciones y vuelve a intentarlo." reviewLabel="Tus respuestas" />`.
See `DESIGN.md` for the full prop reference of every component.

## 5. Always create BOTH locales

Every English file needs a Spanish twin at the mirrored `es` path. This keeps `hreflang`,
the sitemap, and the header language switcher correct. If a translation is genuinely
unavailable, the alternates helper falls back to the locale home — but prefer real twins.

## 6. Verify

```bash
bun run check       # check:latex + astro check + tsc — must be 0 errors
bun run check:latex # standalone: renders every $...$/$$...$$ through KaTeX, fails on parse errors
bun run build       # routes for the new pages should appear
```

**LaTeX gotcha — `\$` inside a `$...$` span breaks rendering.** `rehype-katex`
renders bad math as silent red error text (build stays green), so it's easy to
miss. The classic trap: writing a currency amount *inside* inline math, e.g.
`$0.08 \times 1000 = \$80$`. The math-delimiter scanner closes the span at that
`$`, leaving a stray `\` → KaTeX parse error. **Fix: keep currency OUT of the
math span** — `$0.08 \times 1000$, i.e. \$80`. `bun run check:latex` (also run
inside `bun run check` and `pre-commit`) catches this class of bug across en+es.

Routes appear automatically (no route file edits needed) because pages use
`getStaticPaths` over the content collections.

## 7. Regenerate OG images

```bash
bun run og:build   # build, then Playwright screenshots new /og cards into public/og/
```

(`bun run pre-commit` also does this; run it before committing, then `git add public/og`.)

## Conventions recap

- `@` import alias only — never relative `../`.
- Tailwind design tokens only (no raw hex) — see `DESIGN.md`.
- Keep content accurate, concise, and genuinely interactive — at least one exercise per lesson.
