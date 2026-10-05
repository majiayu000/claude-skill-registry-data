---
name: teach-me
description: Explain any technical topic from first principles, in a textbook style built for interview preparation and for genuinely understanding something. Optionally reads a CV, a job description and an interviewer profile to tie the topic to the reader's own experience and to what they will actually be asked. Use whenever someone asks to understand, learn or brush up a technical subject — "explain Kafka", "I don't understand React hooks", "teach me time-series databases", "brush up Kubernetes for an interview", or when they paste a passage and say they did not follow it. Delivers the explanation in chat, as a PDF, or both.
license: MIT
---

# teach-me

Explain a technical topic so that somebody who has never met it can understand
it, use it in an interview, and know exactly where the edges of their knowledge
are.

## First — check for local bindings

**If `local.md` exists beside this file, read it and follow it.** It carries the
running user's own settings: where their CV lives, their preferred depth, their
output folder, their house style. Anything in it overrides the generic behaviour
below.

If it is not there, everything below applies as written. That is the normal case
for anyone who has just downloaded this skill, and it works perfectly well —
`local.md` is a personalisation, not a requirement.

**If the user wants their own settings** — where their CV lives, their preferred
depth, an output folder, a house style — tell them to copy `local.example.md` to
`local.md` and edit it. It is git-ignored, so it stays on their machine.

## Ask before writing — but only twice

Two questions, and only when the answer changes the content — **skip either one that `local.md` has already answered:**

1. **What is this for?** An interview, building something, or general
   understanding. If an interview, ask for anything they have: a CV or résumé,
   the job description, the interviewer's name or profile. All optional.
2. **Chat, PDF, or both?**

**If they give you nothing, proceed anyway.** Assume the reader has *very
superficial* knowledge of the topic and teach from first principles. Never
refuse for lack of context and never interrogate someone who asked a simple
question.

## Pick the mode first

**Is this something you write code in, or something you reason about?**

| | **Language mode** | **Concept mode** |
|---|---|---|
| Topics | React, Python, Java, SQL, Go, Spring, TypeScript — anything with syntax | Kafka, cardinality, back-pressure, OAuth, CAP theorem, event sourcing |
| Needs | Real code, syntax, idioms, and **coding questions** | Analogy, mechanism, tradeoffs |
| Extra sections | Syntax · concepts with code · idioms · gotchas · theory Q&A · **coding Q&A** | The standard shape below |

A few topics are both. Kafka is concept mode for a PM and language mode for an
engineer who will write consumers. **When unsure, ask which one they want**, or
infer from the role: if they will be writing it, language mode.

## If the topic is not in their background

**That is the normal case and it is not a problem.** Somebody asking to be taught
a topic usually has not done it — that is why they asked. Teach it fully and
properly as something they are learning.

**Do not open with a warning about the gap.** One honest line in the interview
section is enough, and only when it is interview preparation. A chapter that
keeps apologising for what the reader has not done is a worse chapter.

## Calibrate to the level they will be asked at

Work out the level from the role they are interviewing for and their seniority,
from a CV, job description or `local.md` if any were supplied. Then pitch the
questions accordingly:

| Situation | What to prepare them for |
|---|---|
| **Not their discipline** — a PM asked about React, a designer about SQL | "How deep is this really?" and enough to hold a conversation. **Never algorithm puzzles.** The honest-boundary answer matters more than any code. |
| **Junior in the discipline** | Syntax, definitions, straightforward implementation, "what does this code do". |
| **Mid** | Patterns and idioms, debugging, "why this over that", reading unfamiliar code. |
| **Senior or staff** | Design decisions, performance and failure modes, **when not to use it**, how they would review somebody else's use of it, what they would change in a legacy codebase. |

If you genuinely cannot tell, pitch at mid and say in the chapter which level it
is aimed at, so they can tell you to move it.

## The teaching method

This is the part that matters. Ignore it and the output is just another summary.

1. **Name the word collision first.** If a term means something different here
   from a meaning the reader already knows, say so before anything else.
   *"Kafka is called a log — that is not the logs in logs, metrics and traces."*
   Getting this wrong quietly wastes the whole chapter.

2. **Show the thing before naming it.** Show what a metric literally looks like
   before defining "series". Show the config, the line of code, the actual
   shape of the data. A definition given before the reader has seen the thing
   is just vocabulary.

3. **One concrete physical analogy, sustained.** Not three competing ones. A
   numbered notebook. A city water system. A goods-in loading dock. Introduce it
   *before* the technical definition and keep mapping back to it.

4. **Map every piece of jargon onto that analogy**, in a table. Topic = one
   notebook. Offset = the line number. Partition = a second notebook.

5. **Build the arithmetic up.** Show 3 × 2 = 6 before 500 × 200,000. **Never
   assert a conclusion without showing what it was drawn from** — this is the
   single most common failure, and the reader will not tell you they lost the
   thread, they will simply stop understanding.

6. **Contrast it with what they would most likely confuse it with**, and give
   the *consequences* of the difference, not just the difference. A queue versus
   a log is uninteresting; "if your program crashes, a queue has lost the ticket
   and the log has not" is the point.

7. **Say what matters and what is only vocabulary.** Tell them explicitly what
   to skip if short of time.

8. **End with 3–5 check questions, each with a model answer** in a green panel
   they can cover. They attempt it, then verify.

## When it is interview preparation, also include

- **"Say it like this" boxes** — the exact sentence to speak out loud, in
  natural spoken English rather than written prose.
- **An honest-boundary section.** What they can legitimately claim and what they
  cannot. "I have not operated this; I have made product decisions about it" is
  a strong answer. Never coach anyone to overstate.
- **If a CV or profile was supplied:** a section connecting the topic to what
  they have actually done, and be specific about it. **Never invent experience.**
  If the CV shows nothing relevant, say so plainly and frame the topic as new
  ground rather than manufacturing a link.
- **If a job description was supplied:** tie the topic to the requirement it
  actually maps to, quoting the wording used.
- **If an interviewer profile was supplied:** predict what they are likely to
  probe, based on their background, and suggest one question to ask them.

## Chapter shape — concept mode

Masthead · what this is and why it matters · the analogy · the mechanism built
up step by step · a table of the vocabulary · the contrast with its confusable
neighbour · where it connects to the reader's own experience (if known) · what
they can and cannot claim · check questions with answers · what to read next.

## Chapter shape — language mode

⚠️ **The failure mode here is a chapter that is mostly framing.** Analogies,
word collisions and "what to skip" are useful, but they are the seasoning. If
somebody is learning a language to be interviewed on it, **the substance is
concepts, code and practice problems.**

**Budget the document:**

| Part | Share |
|---|---|
| Framing — what it is, the mental model, word collisions | **at most 20%** |
| **Concepts, each with real code** | **at least 40%** |
| **Practice — theory questions and coding problems with solutions** | **at least 30%** |
| Gotchas, idioms, what to skip | the remainder |

**Sections, in order:**

1. **What it is and is not** — half a page. Not two.
2. **The mental model** — one analogy, briefly. Do not spend three sections on it.
3. **Word collisions** — only if there genuinely are any. Skip it otherwise.
4. **Setup** — how to actually run it in five minutes. A learner needs to type
   something and see it work, or none of this sticks.
5. **The concepts — 8 to 12 of them, and this is the bulk of the document.**
   Each one gets: what it is in a sentence · **real, runnable code** · why it
   exists · the mistake everybody makes with it. Order them so each builds on
   the last.
6. **Idioms and conventions** — how code in this language actually looks.
7. **The gotchas** — the things that produce a confusing bug rather than an error.
8. **Theory questions — 8 to 12.**
9. **Coding problems — 5 to 8.**
10. **What to practise next** — concrete, named exercises.

### Theory questions — 8 to 12

The questions actually asked at that level. Each needs the model answer **and a
sentence on what the interviewer is really checking.**

### Coding problems — 5 to 8

**For anyone inside the discipline these are "write this", not "read this".**
Real problems of the kind actually set — the ones that recur in that ecosystem.
Each needs:

- the problem as an interviewer would state it;
- **the complete worked solution as code** — not a sketch, not pseudocode;
- **why the solution is shaped that way**;
- the common wrong turn, and what a follow-up question would be.

Order them easy to hard. Only replace these with comprehension questions when
the reader is genuinely outside the discipline — a PM, a designer — and say in
the chapter that you have done so.

### Length

**8 to 16 pages in language mode.** A language is not a concept; it does not fit
in five pages and pretending otherwise produces something too thin to learn from.
If it will not fit, **split it into Part 1 and Part 2** and say so — do not
compress it into uselessness.

## Teach the ground floor first — the most common failure

⛔ **A topic almost always sits on top of another one.** React sits on
JavaScript. Django sits on Python. SQL joins sit on tables and keys. Kubernetes
sits on containers.

**If the reader does not have the layer underneath, teaching the top layer is
useless — and it will feel "too complex" without them being able to say why.**

So: **before the main concepts, add a section teaching the minimum of the layer
below.** Only what actually appears in your examples, nothing more. For React
that is const and let, functions, arrow functions, objects, arrays, map and
filter, destructuring, the spread operator, and what the DOM is. Roughly a page.
Skip it only if you know the reader already has it.

## Never use a thing before you have explained it

Read your own code samples back and list every piece of syntax in them. **If a
sample uses `=>` or `...` or `const [a, b] =`, those must already have been
explained above it.** This is the single easiest way to lose somebody, and they
will not tell you it happened — they will just quietly stop following.

Annotate the first two or three code samples **line by line**. After that the
reader can carry it.

## Define every term, including the ones that feel obvious

DOM. Pure function. Signature. Destructuring. Reference. Callback. Immutable.
**You have seen these so often they feel like plain English. They are not.** If
a word would make somebody reach for a search engine, define it in the sentence
where it first appears — in brackets, in six words.

## Write plainly

- **One idea per sentence.** Stop. Then the next one.
- **No stacked clauses.** An em-dash carrying a third thought is how a sentence
  becomes unreadable.
- **Short words.** "Use", not "utilise". "Change", not "mutate", unless mutate is
  the term being taught.
- **No flourishes.** "Which is the whole point" and "and that is precisely why"
  add length and no meaning.
- **Detail is not complexity.** Being asked to simplify usually means *more*
  words in *smaller* steps, not fewer words. Do not respond to "too complex" by
  cutting content — respond by breaking it into more, smaller pieces.

## Producing the PDF

`sheet.py` in this skill folder is a self-contained reportlab toolkit. Import it
and compose a story:

```python
import sys; sys.path.insert(0, '<this skill folder>')
from sheet import *

S = sheet(mode='textbook')          # or 'reference' for a denser page
s  = masthead(S, 'Kafka and Streaming', 'deck line', 'standfirst paragraph')
s += section(S, '1', 'A log, not a queue')
s += analogy(S, 'Think of a numbered notebook. ...')
s += body(S, 'Ordinary prose with <b>bold</b> and <i>italic</i>.')
s += table(S, ['Word', 'What it is'], [['Topic', 'One notebook.']], widths=[20, 80])
s += flow(S, [('01', 'Produce', 'the fact exists'), ('02', 'Collect', 'gather it')])
s += sayit(S, 'The sentence they say out loud.')
s += callout(S, 'Heading', 'Body text.', 'amber')     # blue amber red green teal
s += code(S, 'def add(a, b):\n    return a + b')   # monospace block
s += qa(S, [('Question?', 'Model answer.')])
s += footer(S, 'Sources and caveats.')
build(S, s, '/absolute/path/Topic-EXPLAINER.pdf', title='...', running='...')
```

Write the build script to a temporary or working directory, run it with the
system Python, and put the PDF where the user asked — their Desktop or current
directory if they express no preference. Name it
`YYYY-MM-DD_Topic-EXPLAINER.pdf`.

**Requires `reportlab`** (`pip install reportlab`). If it is missing, say so and
offer the chat-only version rather than failing.

## Hard rules

- **Never author HTML.** No Mermaid, no Chromium, no browser.
- **Never type an arrow, a tick, a cross or an emoji into the PDF.** The built-in
  fonts are WinAnsi-encoded, so anything outside that set renders as a solid
  black box — silently, and a text extract still returns the character. `safe()`
  catches the usual offenders; arrows inside diagrams are drawn as vectors by
  `flow()`.
- **`twocol()` takes lists of flowables; `box()` returns one flowable.** Wrap it:
  `twocol(S, [box(...)], [box(...)])`.
- **Always give the explanation in chat too**, even when a PDF was requested.
  Nobody should have to open a file to get the answer.

## Verify before saying it is done

1. Page count, characters per page and fonts, with `pdfplumber` if available.
2. **Then render every page with `pypdfium2` and look at the images.** Metrics
   pass on documents that are visually broken — clipped labels, text overlapping
   text, a whole section silently missing. This is not optional and it is the
   only check that has ever caught a real defect.

If those libraries are not installed, say that verification was skipped rather
than implying the document was checked.
