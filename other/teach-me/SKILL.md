---
name: teach-me
description: >
  Use this skill whenever the user wants to learn about a topic and have structured
  lesson material generated for them. Triggers include: "teach me X", "I want to learn
  Y", "create a lesson on Z", "build me a course on...", "help me study X", or any
  request for a self-paced course or curriculum on a subject. The skill interviews the
  user on topic, depth, and background, proposes a chapter outline for approval, then
  writes a complete multi-chapter course to disk: markdown chapters with diagrams,
  worked examples, and quizzes, a separate answer key with reasoning, and — when
  possible — a combined PDF.
---

# Teach Me

Turns "I want to learn X" into a self-contained, multi-chapter course written to disk.
The skill interviews the user briefly, proposes a chapter outline they can adjust
before any content is written, then generates the course chapter by chapter: markdown
files with explanations, diagrams, worked examples, and quizzes — plus a separate
answer key with reasoning, and a combined PDF when the tooling allows it.

---

## Phase 0: Intake

Ask the following one at a time — never bundle them into a single message. Prefer
multiple choice where natural.

1. **Topic** — "What would you like to learn about?"
2. **Depth** — Beginner / Intermediate / Advanced (multiple choice)
3. **Background** — a short open-ended question on prior experience with the topic,
   e.g. "Do you have any background with this already, or should I start from
   scratch?" Use the answer to calibrate tone and starting point — skip foundational
   material for someone who already has it, spend more time on it for someone who
   doesn't.
4. **Chapter count** — depth suggests a default the user can override:
   - Beginner ≈ 4 chapters
   - Intermediate ≈ 6 chapters
   - Advanced ≈ 8 chapters

   State the suggested count and ask if they'd like more or fewer. Use whatever number
   they settle on.
5. **Research-grounding (conditional offer)** — judge whether the topic is fast-moving
   or fact-sensitive (e.g. a specific framework's current APIs, recent events, niche or
   contested subjects) versus stable (e.g. algebra, classic literature, established
   science, well-settled history). For fast-moving/fact-sensitive topics, offer an
   optional research pass:

   > "This topic moves quickly, so I can do a quick web research pass first to ground
   > the chapters in current sources and add citations. Want me to do that, or work
   > from general knowledge?"

   For stable topics, skip this question entirely — don't ask it just to ask it.

After all answers are in, restate the plan in one line and confirm before generating
anything: e.g. "Building a 6-chapter intermediate course on Python decorators, with
research grounding — sound good?" Wait for confirmation before moving to Phase 1.

If research-grounding was accepted, run the research pass now (web search on the topic
and its key sub-areas) and keep the sources at hand — they feed citations into the
chapters in Phase 2.

---

## Phase 1: Outline & Approval Checkpoint

Before writing a single file, produce a course outline as a conversational summary
(not yet saved to disk):

- **Course title**
- **One-line description** of what the learner will be able to do by the end
- **Numbered chapter list** — each entry has a chapter title and a one-sentence
  learning objective

Present it and ask explicitly whether to proceed or adjust — reorder chapters, merge
two into one, add or remove a chapter, shift emphasis. Example prompt:

> "Here's the proposed outline — want me to go ahead and start writing, or adjust
> anything first (reorder, merge, add/remove a chapter, change focus)?"

**Do not create any files until the user explicitly approves the outline.** This is
the cheap point to redirect — revising an outline costs nothing; revising five written
chapters costs a lot. If the user requests changes, revise the outline and re-confirm.

Once approved, derive `<topic-slug>` — a kebab-case slug of the topic (e.g. "Python
Decorators" → `python-decorators`) — and create the output directory:
`lessons/<topic-slug>/` in the current working directory.

---

## Phase 2: Chapter Generation

Generate chapters in order, one file per chapter: `lessons/<topic-slug>/NN_<chapter-title-slug>.md`
(e.g. `01_what-are-decorators.md`, `02_writing-your-first-decorator.md`). Use
`references/templates.md` → **Chapter Template** as the structural skeleton — read it
before writing the first chapter.

Each chapter contains, in this order:

1. **Introduction** — what this chapter covers and why it matters, 2-4 sentences
2. **Core content** — explanation scaled to the chosen depth:
   - *Beginner*: more analogies, gentler step-by-step buildup, simpler vocabulary,
     define jargon on first use
   - *Intermediate*: assumes basic fluency with the subject's fundamentals, balances
     theory with application
   - *Advanced*: dense, assumes fluency, emphasizes nuance, trade-offs, edge cases,
     and the "why" behind design decisions rather than the "what"
3. **Illustrations** — Mermaid diagrams or ASCII art embedded inline wherever a visual
   would clarify a concept faster than prose (process flows, relationships,
   comparisons, timelines, mind maps, decision trees). Use Mermaid fenced code blocks
   (` ```mermaid `) by default — they render natively in most markdown viewers and
   convert cleanly through pandoc. Use ASCII art for simple inline diagrams that don't
   need Mermaid's structure. Only add a diagram where it earns its place — don't
   illustrate things that are clearer as a sentence.

   If an image-generation tool is available in the current environment AND a concept
   would genuinely benefit from a generated image rather than a diagram (a visual
   metaphor, a historical scene, something diagrams can't capture), offer to generate
   one and embed/link it. This is always a bonus on top of Mermaid/ASCII, never a
   substitute — if no such tool is available, proceed with diagrams alone and don't
   mention it.
4. **Worked examples** — at least one concrete, complete example illustrating each
   major concept introduced in the chapter. Show the example in full; don't truncate
   with "..." or "etc."
5. **Key takeaways** — a short bullet-point recap (3-6 bullets) of the chapter's main
   points, placed just before the quiz
6. **Chapter quiz** — 3 to 5 questions, mixing multiple-choice and short-answer,
   numbered, at the very end of the file. **Do not include answers in the chapter
   file** — they belong only in `ANSWERS.md` (Phase 3).

If research-grounding was accepted in Phase 0, factual claims in the core content
carry inline citations (markdown links) to the sources the research pass found.

Write each chapter fully before moving to the next — don't draft all chapters as
outlines first and fill them in later.

---

## Phase 3: Index & Answer Key

**`ANSWERS.md`** — generate this incrementally, immediately after each chapter is
written, in the same context that authored that chapter's quiz (this keeps the
reasoning consistent with what was just taught, and avoids re-deriving answers from
scratch later). Use `references/templates.md` → **Answer Key Template**. For every
quiz question in the chapter just written, record:
- The question number and chapter it belongs to
- The correct answer
- **Why** it's correct — the reasoning, not just the fact
- For multiple-choice questions: why each distractor is wrong

By the time the last chapter is written, `ANSWERS.md` is already complete — no
separate "write all the answers" pass is needed.

**`00_index.md`** — write this last, after every chapter file and `ANSWERS.md` exist,
so it can link to final chapter titles. Use `references/templates.md` → **Index
Template**. It contains:
- Course title and one-paragraph description
- Full chapter list with relative links and each chapter's learning objective
- A short "How to use this course" note (e.g. attempt each quiz before checking
  `ANSWERS.md`, work through chapters in order, etc.)

---

## Phase 4: Output Layout

The finished course lives entirely in `lessons/<topic-slug>/`:

```
lessons/<topic-slug>/
├── 00_index.md
├── 01_<chapter-title-slug>.md
├── 02_<chapter-title-slug>.md
├── ...
├── ANSWERS.md
└── <topic-slug>.pdf            (present only if PDF generation succeeds — see Phase 5)
```

---

## Phase 5: PDF Generation

After every markdown file exists, attempt to build a combined course PDF:

1. **Check for pandoc**: run `which pandoc`. If found, skip to step 3.
2. **Offer to install it**: pandoc is a system package — installing it changes the
   user's environment, so ask first. Example: "I don't see `pandoc` installed, which I
   use to build the PDF. Want me to install it (`apt-get install -y pandoc` or your
   platform's equivalent)? If not, I'll leave the markdown as the deliverable and give
   you the command to build the PDF yourself later." Only run the install command if
   the user agrees. If installation fails or they decline, go to step 4.
3. **Build the PDF**: concatenate `00_index.md` and all chapter files in numeric order
   (excluding `ANSWERS.md` — it stays a separate, spoiler-free document) and convert
   with pandoc, e.g.:

   ```bash
   pandoc lessons/<topic-slug>/00_index.md lessons/<topic-slug>/0*_*.md \
     -o lessons/<topic-slug>/<topic-slug>.pdf \
     --metadata title="<Course Title>"
   ```

   Confirm the file was created (`ls lessons/<topic-slug>/<topic-slug>.pdf`) and tell
   the user where it is.
4. **Fallback**: if pandoc isn't available and can't/won't be installed, tell the user
   plainly that the markdown set is the deliverable, and give them the exact command
   to build the PDF themselves once pandoc is available:

   ```bash
   pandoc lessons/<topic-slug>/00_index.md lessons/<topic-slug>/0*_*.md \
     -o lessons/<topic-slug>/<topic-slug>.pdf --metadata title="<Course Title>"
   ```

---

## Tone & Style

- Calibrate density and vocabulary to the chosen depth level above all else — it's the
  single biggest lever on whether the course actually fits the learner
- Prefer concrete, fully-worked examples over abstract description
- Use diagrams purposefully — only where a visual genuinely clarifies something a
  paragraph would belabor; a course stuffed with diagrams is as hard to follow as one
  with none
- Quiz questions should test understanding and application of what the chapter taught,
  not just recall of definitions stated verbatim in the text
- Answer-key reasoning should teach: explain *why* an answer is correct (and why the
  alternatives aren't), not just restate it

---

## Out of Scope

- No interactive quiz-taking inside the chat — quizzes are static markdown; the
  learner self-grades against `ANSWERS.md`
- No versioning or updating of previously generated courses — each invocation produces
  a fresh, independent course folder under `lessons/`
- Research-grounding is opt-in and topic-dependent — it is never silently skipped for
  fast-moving topics, and never silently forced on stable ones

---

## Reference Files

- `references/templates.md` — exact templates for a chapter file, `00_index.md`, and
  `ANSWERS.md`. **Read this before writing the first chapter file.**
