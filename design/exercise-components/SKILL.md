---
name: exercise-components
description: Build and use reusable interactive exercise islands for this Lessons site — multiple-choice and multi-answer questions, quizzes, and concept→definition matching/linking exercises. Covers using the existing components (MCQ, Quiz) AND authoring new reusable React islands the right way (barrel export, design tokens, a11y, i18n label props). Use when the user asks to "add a quiz/exercise", "multi-select question", "match concepts to definitions", "make a reusable exercise component", or to extend the component library.
---

# Exercises & reusable interactive components

Exercises live in `src/components/react/` as React 19 islands and are dropped
into MDX with a `client:*` directive. Always prefer **reusing/extending** an
existing component over inlining one-off JSX in a lesson.

## Placement & density (REQUIRED)

- **Every `##` section gets at least one exercise** — ideally two: a *prequestion*
  to open it and a *check* to close it. Lessons should be exercise-dense, not a
  text wall with a quiz at the bottom. When in doubt, add another exercise.
- **Open sections with a pretest** (`MCQ pretest`): asking the learner to *guess
  before reading* boosts encoding even when the guess is wrong (the
  pretesting effect). See "Pretest mode" below.
- Put the *check* exercises **after each explanation**, interleaved — not pooled
  at the end.
- **Rotate types every time** — never the same format twice in a row. Available:
  single `MCQ`, **multi-answer `MCQ`**, `MCQ pretest`, `MatchConcepts`
  (concept→definition), `Categorize` (sort into buckets), `FillBlank`
  (pick-one-of-three cloze), scored `Quiz`, and `FinalExam` (graded,
  lock-on-submit — final-exam lessons only; see below).
- **Vary the questions themselves — repetition is the #1 quality problem.**
  Rotating the *component* is not enough; the questions inside a `Quiz`/`FinalExam`
  must vary too. Across a question set, deliberately mix:
  - **Type of ask**: numeric/calculation (show the arithmetic in the
    explanation), scenario/application, "which statement is TRUE", spot-the-trap,
    plain definition, side-by-side comparison, cause→effect, ranking-as-single-answer.
  - **Stem wording**: never reuse the same sentence frame twice in a row, and
    don't open five questions with "Which of the following…". Rephrase.
  - **Difficulty**: interleave easy recall with multi-step reasoning.
  If two questions feel interchangeable, rewrite one. A pool that drills the same
  idea with the same phrasing teaches pattern-matching, not understanding.
- **For a term worth pinning down**, reach for `FillBlank`: each blank is a
  pick-one-of-three choice (the right term flanked by two convincing
  distractors), so the learner must still discriminate it from look-alikes
  without being punished for a typo.
- **Spaced recall**: some questions reference *earlier* sections so the user
  recalls prior material, not only the latest paragraph.
- **Close the lesson with a chunking recap** — a learner-built `MindMap` plus a
  mixed `Quiz`, not a passive bullet summary. See the `lesson-animations` /
  `new-lesson` skills for the MindMap close.

## Write options that don't give themselves away (REQUIRED)

The fastest way to wreck a question is to make the correct option the long,
detailed, careful one and the distractors short throwaways — learners pick the
longest answer without reading. So:

- **Length parity.** All options for a question are roughly the same length. The
  correct one is **never** noticeably longer than the rest. If the right answer
  needs a qualifier, give the distractors comparable qualifiers.
- **Plausible distractors.** Every wrong option is a believable mistake — a real
  misconception, an adjacent term, a true-but-irrelevant fact — not an obvious
  joke. (Keep at most one light "nonsense" option per *lesson*, not per question.)
- **Harder than obvious.** Aim for distractors that a learner who *half* gets it
  would fall for. Test discrimination between close ideas, not recall of a single
  keyword sitting alone among nonsense.
- This applies to `MCQ`, `Quiz`, and `FillBlank` choices alike.

## Pretest mode (prequestion)

`MCQ` takes a `pretest` boolean. In pretest mode it shows a low-stakes "Before
you read — take a guess" eyebrow and **never** reports to a `Quiz` score, so a
wrong guess costs nothing. Use one to **open** a section, before you've taught
the answer:

```mdx
<MCQ
  client:visible
  pretest
  question="Guess: which of these best describes the lesson's core idea?"
  options={[
    { text: 'The precise, correct description', correct: true },
    { text: 'A close-but-wrong neighbour' },
    { text: 'A common misconception' },
  ]}
  explanation="The first option is right — keep it in mind as you read on."
/>
```

Spanish twins pass `pretestLabel="Antes de leer — adivina"`.

## Every island must teach or test *in place*

Don't use a component as a **fake-interactive list** or to **point the learner
at an exercise to do elsewhere** ("now try sketching this", "go work through an
example on paper"). An off-page instruction adds nothing — the learner won't
leave the page to do it. If a step is worth doing, make it a real, graded island
here (`FillBlank`, `Categorize`, `MCQ`, `MatchConcepts`).

**No `StepThrough`.** It was removed — a click-to-advance wrapper around a
static list adds nothing a plain numbered list doesn't, and its children-API
silently rendered *nothing* under Astro islands. For genuinely sequential
*content*, just author a numbered Markdown list (`1.` `2.` `3.`). For a sequence
worth *testing*, use `Categorize` or `FillBlank`.

## Misconfigured components MUST fail the build, not ship blank (REQUIRED)

This is non-negotiable. A component handed bad/empty/mis-shaped input must
**`throw` during render** (top of the function body, before any hooks-free early
return) so `astro build` fails loudly — **never** silently return `null`, render
an empty card, or render nothing. A green build must mean every exercise on the
page is answerable and correct. Silent-empty exercises are a release blocker.

Every exercise component now enforces this: `MCQ` (≥2 options, ≥1 correct),
`Quiz` (every question has a prompt, ≥2 options, a marked correct answer),
`Categorize` (≥2 buckets, every item's `bucket` matches one), `MatchConcepts`
(≥2 pairs, non-empty term+definition), `MindMap` (non-empty `root.label` and
children), `FillBlank` (each blank ≥2 choices, `text` has ≥1 blank). Hold any new
component to the same bar.

### The island-boundary trap (this is what bit us)

**Never author a `client:*` island that takes its content as React *children*.**
Across a `client:visible` boundary Astro renders children to an opaque HTML
**slot** — the client component receives a slot wrapper whose `props` carry
**none** of your data. So `Quiz` built from `<MCQ>` children, and the old
`StepThrough`, both rendered **blank** after hydration while the build stayed
green. Authoring API for composed exercises is always a **prop**, not children:

```mdx
{/* ✅ works — data crosses the boundary as a prop */}
<Quiz client:visible questions={[{ question, options, correct, explanation }, …]} />

{/* ❌ renders an empty card — children become an HTML slot, props are lost */}
<Quiz client:visible><MCQ question="…" options={[…]} correct={0} /></Quiz>
```

If a component *must* accept children, it has to detect the slot case and
`throw` (as `Quiz` now does when a derived question lacks a `question`/`options`).

### Prove the guard fires (REQUIRED before you commit)

A guard you didn't watch fail is a guard you don't have. After adding one,
temporarily author the broken input in a throwaway lesson
(`src/content/lessons/en/<topic>/_guardtest.mdx`), run `bun run build`, confirm
it exits **red** with your named error, then delete the file and confirm a clean
build. Don't skip this — it's the only proof the build actually catches the
mistake.

## Existing components (reuse these first)

Import from the barrel: `import { MCQ, Quiz } from '@/components/react';`

- **`MCQ`** — single- or **multi-answer** question. Set `allowMultiple` to turn
  radios into checkboxes (multiple correct options):

  ```mdx
  <MCQ
    client:visible
    allowMultiple
    question="Which of these belong to the category being taught? (select all)"
    options={[
      { text: 'A correct member', correct: true },
      { text: 'Another correct member', correct: true },
      { text: 'A plausible non-member' },
      { text: 'A third correct member', correct: true },
    ]}
    explanation="The non-member is an adjacent concept, not part of this category."
  />
  ```

- **`Quiz`** — sequences several `MCQ` prop objects and tracks a score. Practice
  exercise: the learner can go Back, retry a question, and Restart at the end. Use
  it inside *teaching* lessons.
- **`FinalExam`** — the graded, **irreversible** exam island, reserved for a
  course's `final-exam` lesson. Takes a 20–30 question pool via
  `questions={[{ question, options, correct?, explanation?, allowMultiple? }]}`
  (same per-question shape as `MCQ`). One question at a time; the learner selects
  and clicks **Submit**, which **locks the answer for good** — there is no Back,
  no Try again, and no Restart, so a wrong answer simply fails that question. The
  result reveals instantly on submit, but the running score stays hidden until the
  final screen, which shows a pass/fail verdict (`passPercent`, default `70`) and a
  per-question review. Because nothing resets, the exam can't be retaken in-session.
  Author it directly — do **not** wrap it in themed recap sections.

  ```mdx
  <FinalExam
    client:visible
    passPercent={70}
    questions={[
      { question: "…", options: [{ text: "…", correct: true }, { text: "…" }, { text: "…" }], explanation: "…" },
      { question: "Select every true statement.", allowMultiple: true, options: [{ text: "…", correct: true }, { text: "…", correct: true }, { text: "…" }], explanation: "…" },
      /* … 20–30 total, varied (see "Vary the questions themselves") … */
    ]}
  />
  ```

All three accept i18n label props (`checkLabel`, `retryLabel`, `scoreLabel`,
`submitLabel`, `lockWarningLabel`, `passLabel`, …) — pass the Spanish strings in
`es` lessons (see the `translate-lesson` and `new-lesson` skills for the full
`FinalExam` Spanish prop set).

## Concept → definition matching (new component pattern)

For "link concepts to their definitions" exercises, build a reusable
`MatchConcepts` (a.k.a. concept-linking) island rather than ad-hoc markup.
Shape it like the others:

```tsx
// src/components/react/MatchConcepts.tsx
export interface MatchPair {
  /** The concept/term shown on the left. */
  term: string;
  /** Its correct definition shown on the right. */
  definition: string;
}
export interface MatchConceptsProps {
  pairs: MatchPair[];
  /** Revealed-on-success / labels, localizable. */
  checkLabel?: string;   // default 'Check'
  retryLabel?: string;   // default 'Try again'
  className?: string;
  onResult?: (correct: boolean) => void;  // lets Quiz aggregate score
}
```

Behavior: shuffle definitions, let the user link each term→definition
(click-to-pair or drag), **Check** grades, correct links go success-green and
wrong ones danger-red, an `aria-live` region announces the result, **Try again**
resets. Mirror `MCQ`'s interaction and grading model exactly so it composes
inside `Quiz`.

For a lighter "term ⇒ meaning" glossary link (definition on hover/expand, not a
graded exercise), prefer `Reveal`/`Callout` or a small `Defn` inline component
over a full matcher.

## `Categorize` — sort items into buckets

For "which group does this belong to?" ideas (any two-or-more-way split your
subject offers). Each item exposes one button per bucket; **Check** grades all of
them and reveals the right bucket on a miss.

```mdx
<Categorize
  client:visible
  question="Sort each item into the group it belongs to."
  buckets={['Group A', 'Group B']}
  items={[
    { text: 'First item', bucket: 'Group A' },
    { text: 'Second item', bucket: 'Group A' },
    { text: 'Third item', bucket: 'Group B' },
  ]}
  explanation="Explain the distinguishing rule that separates Group A from Group B."
/>
```

## `FillBlank` — pick-one-of-three cloze

Each blank is a small inline choice group, not a text input. Author the blank as
`{{correct|distractor|distractor}}`: pipe-separated options where the **first**
is correct and the rest are distractors. The component shuffles them with a
stable, content-seeded order (so the answer isn't always in the same slot and
SSR/CSR markup match). **Three options per blank** is the target; fewer than two
throws at build time.

Make distractors *plausible* — same category as the answer (sibling terms from
the same part of your subject), never throwaway nonsense. That's what keeps it
a real discrimination test rather than a freebie.

```mdx
<FillBlank
  client:visible
  question="Fill in the right term for each blank."
  text="The {{correct-term|sibling-term|another-sibling}} is the one that {{does the key thing|does a related thing|does an unrelated thing}} in this lesson."
  explanation="State why the correct term fits and the look-alikes don't."
/>
```

Exposes `onResult(correct)`, so it composes inside `Quiz` like `MCQ`. Pass
Spanish label props (`checkLabel`, `retryLabel`, `explanationLabel`, plus
`instructions`) in the `es` twin.

## Rules for ANY new reusable component

1. **File + barrel.** Create `src/components/react/<Name>.tsx`; export the
   component, its `default`, and all prop/option types from
   `src/components/react/index.ts` (follow the existing pattern exactly).
2. **`@` alias only**, and use the shared `cx` helper (`@/components/react/cx`)
   for class merging — never relative imports, never `clsx` ad-hoc.
3. **Design tokens only.** Style with Tailwind token utilities
   (`bg-surface`, `text-ink-700`, `bg-brand-600`, success/danger tokens) — no
   raw hex. See `DESIGN.md`.
4. **Accessibility is required.** Real form controls (`<input>`/`<button>`),
   `radiogroup`/`group` semantics, full keyboard operability, `aria-live` for
   dynamic results, visible focus rings, and honor `prefers-reduced-motion`.
5. **i18n.** Every user-facing string is a prop with an English default so
   Spanish lessons can pass translated labels. No hard-coded copy inside.
6. **Composability.** Graded exercises expose `onResult(correct)` so `Quiz` can
   aggregate them.
7. **Build-time guards (REQUIRED).** Validate inputs at the top of the render and
   `throw` on anything mis-shaped — empty/too-few options, no correct answer,
   orphan references, empty data — with a message naming the offending prop. The
   content authoring API is a **prop, never children** (see the island-boundary
   trap above). Then *prove it*: temp-author the broken input, confirm `bun run
   build` goes red, delete it. A misconfigured exercise must never ship blank.
8. **Type + verify.** Document props with JSDoc, then `bun run check` (0 errors).

## Wire it into a lesson

```mdx
import { MCQ, Quiz, MatchConcepts, Categorize, FillBlank, MindMap } from '@/components/react';

<MatchConcepts
  client:visible
  pairs={[
    { term: 'First term', definition: 'A crisp, correct definition of the first term.' },
    { term: 'Second term', definition: 'A crisp, correct definition of the second term.' },
  ]}
/>
```

Aim for **at least one exercise per lesson**. Then regenerate OG and run
`bun run check`.
