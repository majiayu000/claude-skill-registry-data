---
name: sketch
description: "Use whenever a visual would discuss an idea better than words: choices to weigh, a change to show, a structure or a flow to follow, an idea to picture, a question the person answers better by pointing than by typing; and the moment you catch yourself writing in chat a long comparison, a dense table, or a question with several options. In any work, inside another skill's flow too (an interview, a brainstorm, a plan, a review), on your own decision, never asking first. Produces a sketch through the aiview skill: one self-contained page for one question, filed in the viewer's Sketches. Not for a product screen to be built (design-prototype), a tool reused across sessions (workbench), or a diagram inside a document (write-diagrams)."
---

# Sketch

**A sketch is a page made to align on one question**, and thrown away once it has. The person
sees the whole idea at once, where chat gives it to them line by line. Make it the moment it
would help, then link it: asking whether they want one costs the turn it would have saved.

## The page

- **One question**, said at the top in one line, for someone who was not there: what is shown,
  and what the person is asked to decide or notice.
- **The form the question needs**: options side by side, a before and an after, the parts of a
  structure, the steps of a flow, the same thing at several sizes or states, a list to point
  into. Pick the one that answers the question, never a dashboard of everything.
- **The real material when there is some**: the project's own names, data, text and outputs, read
  before the page is made. Invented filler only where nothing real exists yet, and said so.
- **Names the person can answer with**: each option, part or row carries a short visible label,
  so the answer in chat is "B" or "the second step", and the `point-at` skill can light it.
- **Self-contained HTML**, no build, no network but a pinned CDN library when one is needed. It
  follows the project's look when one is at hand; clear beats polished.

## Filing

Through the `aiview` skill: kind `sketch`, file `YYYY-MM-DD-<topic>.sketch.html`, the topic's
tags, the group of the work it serves when it has one. `open` it, then one line in chat: what it
shows and the question, with the link. The viewer files sketches in their own Sketches list,
apart from the documents.

- **Iterate the same file** while the question is open; a new question is a new sketch.
- **Write the answer where the work keeps it** (the board's decision, the plan, the task), never
  only in the sketch: a sketch is not a record.
- **A sketch that outgrows its question is promoted**: a screen the product will build becomes a
  prototype through the `design-prototype` skill, a page worth keeping becomes a `report` with
  `update --kind`.

## Red flags

| Thought | Reality |
|---|---|
| "Chat is enough for this" | Chat is read in order. A page shows the whole thing at once. |
| "I should ask whether they want a visual" | Asking costs a turn. Make it, then link it. |
| "It isn't a screen, so it isn't for a page" | A sketch is any idea clearer seen. |
| "It has to look finished" | It answers one question. Clear beats polished. |
| "I'll describe the options, then show them" | Show them, then ask. |
| "I'll put it in my scratchpad directory" | That holds temporary files. A sketch goes through the `aiview` skill. |
| "One page can answer all the open questions" | One question per sketch, or the person answers none. |
