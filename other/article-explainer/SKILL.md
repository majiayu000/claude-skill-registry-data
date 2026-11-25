---
name: article-explainer
description: Turns an article, paper or long post into a single self-contained HTML explainer, built around one diagram that assembles itself as the reader scrolls, with plain, quotable prose tied to the reader's own project. Use when asked to explain, break down or visualise an article, or to make an "article explainer".
metadata:
  category: visual-media
---

# Article explainer

Make one offline HTML file that teaches the ideas in a single article. The reader should finish it able to redraw the author's model from memory and know where it fits in their own work.

`examples/guides-and-sensors.html` is a reference that Iury approved. It explains Birgitta Böckeler's "Harness engineering for coding agent users" for a conference talk. Study it for **taste**, not layout. Don't copy its structure, palette or copy. Derive each new explainer from its own article.

For a system we built (a tool, extension or mode), use `interactive-explainer` instead.

## The thesis

The page is **one diagram that grows as you scroll**, beside a column of short steps. Everything else is quiet prose that supports that diagram.

The first version of the reference was a dark page of cards, tabs, buttons, coloured badges and seven small widgets. Iury called it shit. The fix wasn't polish. It was a different idea:

| Rejected | Approved |
|---|---|
| Seven widgets, one per idea | One diagram that holds the whole model |
| Cards with borders and fills everywhere | No cards. Hairlines, white space and columns |
| Dark dashboard with five accent colours | Pale paper, ink, and two meaningful colours |
| Legends that explain colours after the fact | Meaning built into the lines themselves |
| "In the talk" boxes shouting in every section | One quiet label and a paragraph |
| Buttons to click through states | Scroll position is the state |

## Process

### 1. Read the whole article

Fetch the full text, for example with `curl -sL https://r.jina.ai/<url>`. Read all of it before you design anything. Note:

- The author's **core model**. Most good articles have one: two axes, a loop, a stack or a pipeline. That model is your diagram.
- 3 to 5 lines worth quoting, word for word.
- The author's terms, and plainer words for them.
- Claims you can't verify. Mark them as the author's claim.

### 2. Find the reader's context

Ask, or infer it from the conversation: who reads this, and why? In the reference, it was a speaker deciding which slides to build. Every section ends by linking the article to that context. Without a context, the explainer is just a summary.

### 3. Design the diagram first

- **Encode both of the author's dimensions in the drawing itself.** In the reference: colour shows *when* (blue before, orange after), and stroke shows *who* (solid is code, dashed is a model). The reader learns the model just by looking at the lines.
- Use at most **two semantic colours** plus ink. Every colour must mean something.
- Plan **6 to 9 steps**. Each step adds exactly one idea. Start from the simplest core and finish with the reader's own role in the system, for example "you steer it".
- Add one step that places **the reader's own world** on the author's model. In the reference, that was the show-of-hands ladder (AGENTS.md, skill, hook, extension), numbered onto the diagram. That step is what makes the page feel made for them.
- Make the scene **a pure function of the step**: each element has a `data-from="n"` attribute and shows when `step >= n`. Scrolling up undoes it cleanly.
- Hand-write the SVG. Use a `viewBox`, mono labels, thin strokes (1.25 to 2.25), rounded pills, arrowheads with `markerUnits="userSpaceOnUse"`, and one quiet motion, such as a dot running the feedback path.

### 4. Write the steps and the prose

See "Voice" below. Each step gets a mono label ("Click 3 of 8"), a short heading, 1 to 3 short paragraphs, and at most one quote.

### 5. Below the diagram

Add 2 to 4 essay sections for the ideas that don't belong in the diagram. Give each one a different, *quiet* form chosen for its content:

- a sequence becomes a timeline drawn on a single rule
- a "what works and what doesn't" split becomes three columns divided by hairlines
- a strong line becomes a large pull quote

End with a table that maps each idea to where it's used, with a line the reader could say, then **push-back**: what to leave out, what is jargon and what to credit.

### 6. Build, look, fix

- Use one file with inline CSS and a small amount of vanilla JS. Load nothing from the network.
- Embed fonts with `scripts/embed-fonts.py` so the file works offline.
- Screenshot it with agent-browser at 1512×945 and 390×844, at the hero, at 2 or 3 diagram steps, and at one prose section. **Look at every image.** Fix label collisions, lines crossing text and sideways scrolling.
- Check that `document.documentElement.scrollWidth` equals the viewport width and that the console has no errors.

## The visual system

Treat these as invariants. Keep them unless the user asks otherwise.

- **Paper and ink.** A cool, pale paper (around `#eceef0`), near-black ink, one muted grey and one hairline grey. It shouldn't be the cream-and-serif look or a dark dashboard.
- **Two semantic accents, picked for the article's own model.** For example, one cool and one hot colour for an opposition. Use them in the diagram and in the text that refers to them, and nowhere else.
- **Type.**
  - A grotesk for display and body, at weights 400 and 500 only.
  - A mono for labels, captions and diagram text, small and uppercase with letter-spacing.
  - The headline is huge (about 8vw), tight (letter-spacing around −0.045em) and in two short lines, stating the article's thesis as a claim, such as "A harness is a control system."
  - If the reader has a brand or deck, use its typefaces. The reference uses the talk's Satoshi and Commit Mono.
- **No cards, shadows, gradients, badges or emoji.** Separate content with white space, hairlines and columns.
- **Desktop scale: 125%.** Iury liked the reference best at 125% browser zoom, so build it in. Design at a base of 18px body text, a 1400px container with 6vw padding and a 440px step column. Then add `@media (min-width:1100px){html{zoom:1.25}}`, shorten the sticky stage to `80vh` and the steps to about `62vh` so they fit the zoomed viewport, and cap the headline near `6.7vw`. Check at 1512×945 that the whole diagram is visible while it's pinned.
- **Mobile:** the diagram sticks to the top at about 44vh and the steps scroll under it. Tables collapse into stacked rows.
- Respect `prefers-reduced-motion`, show a visible `:focus-visible` outline, and use semantic headings.

## Voice

Write like the reference. It is plain and declarative, and every sentence does one job.

- **Lead with the claim.** "A harness is a control system." Not "Exploring harness engineering".
- **Use short sentences in the active voice.** "A sensor checks what the agent did and feeds the result back."
- **Translate jargon once, then use the plain word.** "Code (her word: computational)…". Afterwards, say "code".
- **Quote the author word for word, in quotation marks, with a name.** Never paraphrase inside quotation marks.
- **Speak to the reader as "you".** "Your job is the outermost loop."
- **Give each section one line to remember.** "Fix the harness, not the code." "AGENTS.md asks nicely. A hook checks."
- **Be honest.** Mark claims you can't verify, say what the author leaves open, and credit the author's model on the diagram itself.
- **Use sentence case, no filler and no sales words.** No "dive into", "unlock" or "powerful". Run the `unslop` skill on the copy.

## Output

- Save the file next to the work it supports, for example `inbox/YYYY-MM-DD-<slug>-explainer.html`. If there's no project, use `ai-artifacts/explainers/`.
- Open it for the user. Report its size, the viewports you checked and any open questions.
- Offer the diagram's steps as a click-by-click plan if the reader builds slides or docs.
