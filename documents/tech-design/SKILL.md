---
name: tech-design
description: Draft, review, pressure-test, compare, and polish technical design documents for product, API, SDK, infrastructure, storage, migration, reliability, security, privacy, performance, data model, or architecture work. Use when an engineer wants to make and defend a technical decision, turn rough notes into a review-ready TD, review an existing TD, compare alternatives, or plan rollout/testing/migration/rollback for a proposed technical change.
---

# Tech Design

Help engineers create clear, readable technical designs. The goal is to get co-workers on board with a plan — or to start a collaborative discussion toward one. These documents are read by senior engineers who are busy and value their time. Write for humans, not for robots.

## Operating Modes

Infer the mode from the user's request. Ask only when the intent is genuinely ambiguous.

- **Draft mode**: Create a TD from an idea, issue, PRD, thread, or notes.
- **Review mode**: Review an existing TD for gaps, weak assumptions, missing risks, and likely reviewer objections.
- **Sparring mode**: Help explore a design before it is settled — clarifying questions, possible approaches, trade-offs, recommended next step.
- **Decision mode**: Compare alternatives and recommend one.
- **Compression mode**: Turn messy notes into a polished TD while preserving intent.

## Output

Whenever the deliverable is a TD (draft, compression, or revised document), write it to a local markdown file on disk rather than printing it in the chat. Choose a sensible filename derived from the title (e.g. `tech-design-create-op-redesign.md`) and write it to the current working directory. Then tell the user the filename in one line, and offer to start a `/grill-me` session to refine the document.

Do **not** print the document body in the chat — it's long, the user will read it in an editor, and repeating it here adds no value.

On revisions, overwrite the same file.

Write the markdown in the dialect Notion understands on paste (for when the user copies it into Notion):

- **Headings:** only `#`, `##`, `###`. Notion has three heading levels; `####` and deeper paste as plain text. Use `#` for the title, `##` for sections, `###` for subsections.
- **Tables:** GFM pipe tables. Inline formatting only inside cells.
- **Checkboxes:** `- [ ]` and `- [x]` become to-do blocks.
- **Code:** triple-backtick fenced blocks with a language hint.
- **Dividers:** `---` on its own line.
- `**bold**`, `*italic*`, `inline code`, and `[links](url)` all work. Avoid raw HTML, footnotes, definition lists, and nested blockquotes.

## Intake

Ask for missing information only when it materially changes the design. Prefer 3–5 high-leverage questions over a long questionnaire. If enough context exists, proceed with clearly marked assumptions. Use `[TODO: ...]` placeholders where facts are unknown.

Try to identify: the problem, what breaks or becomes painful if nothing changes, who is affected, the proposed change (if any), constraints, known risks, and open questions.

## Writing style

These docs are read by senior engineers on a couch, not studied by a junior dev in an IDE. Write accordingly.

**Be short.** Length is a cost the reader pays. Most TDs fit on one screen-and-a-bit; a big one is two pages. Before keeping a paragraph, ask what decision it changes for the reader — if none, cut it. Two tight paragraphs beat five loose ones. Never restate a point in different words for emphasis.

**Ground every abstraction in an example.** Abstraction is fine, but a reader can only agree with a claim they can picture. Any sentence that stays at altitude — "makes composition awkward", "hard to reason about", "doesn't scale" — needs a concrete anchor immediately after it: a real call, a real type, a real number. Not:

> The current API makes multi-step operations hard to reason about.

But:

> Today `createThread` + `attachFile` are two calls, so a crash in between leaves a thread with no file.

The example should be one sentence or one small code block, not a subsection. If you can't produce one, the claim is probably too vague to keep.

**Structure:** Let the content determine the structure, not the other way around. There is no fixed template. Every TD is different — a type-design doc looks nothing like a rollout plan. Use only the sections that genuinely add value. Don't add a section just because the template has one.

**Prose over bullets:** Write in flowing paragraphs. Use bullet lists only when items are truly parallel and enumerable. Avoid the `- **Bolded Label:** Explanation` pattern except sparingly for the most important callouts. A wall of bold-bullets is exhausting to read.

**Skip the obvious:** Don't explain things senior engineers already know. Don't enumerate consequences that follow trivially from the proposal. Don't state that tests should test the feature. Don't write a paragraph of setup before the point — lead with the point.

**Code and references:** Use code blocks for types, schemas, and short snippets when they clarify the design — they're often the clearest way to show a proposed type. Avoid long file paths and line numbers in prose; they make the doc feel like a robot wrote it and add no value to someone reading it on an iPad. If you need to point to something, say the function name or concept, not the full path.

**Tone:** Direct and matter-of-fact. Dry wit is fine when it fits. Never pad the document.

## Document structure

Start every TD with a short **untitled intro block** — one or two short paragraphs of plain prose that state the problem and the proposed fix (if there is one). No heading, no "TL;DR" label. If the document is early-stage or open for discussion, say so here in one sentence.

Then use sections as the content demands. Common ones:

### Context / Background

What's the current situation? What breaks, slows down, or becomes painful? Prefer concrete examples over vague claims. Code snippets showing the problematic current shape are often the most efficient way to explain.

### Proposed solution

The heart of the doc. Explain the design — new types, API surface, data flow, behavioral changes, whatever is relevant. Don't force it into sub-sections. If there are multiple moving parts, describe them in the order a reader needs to understand them. Code blocks here are often worth a thousand words. When a block is long, use inline comments to call out the lines that matter — let the signal stand out from the noise.

### Alternatives considered

Only include this if real alternatives were considered and rejected. For each: what it is, why it's attractive, why it was rejected. Skip strawmen. A short prose paragraph per alternative is usually enough — tables only if comparing more than three options across several dimensions.

### Recommendation

If there's more than one viable option, state the recommended one clearly and explain _why_ in plain prose. What makes this the right trade-off? What assumptions does it rest on? What would change the recommendation? Keep it short and readable — don't cross-reference every earlier section by label or number, just say what you mean.

### Rollout

Only include when there's something non-obvious to say about ordering, phasing, or risk management. Keep it short — ideally a brief paragraph or a small bullet list of steps and their rationale. Skip it if the rollout is straightforward.

### Open questions

A bullet list. No table, no owner column, no "needed by" or "impact" fields. Just the questions. Only include genuine blockers or decisions that need input.

## What to leave out

These sections add almost no value in most TDs and should be omitted unless the specific content is genuinely interesting:

- A formal metadata block (status, reviewers, dates) — at most mention "Draft" or "RFC" in the intro if relevant
- A numbered requirements section
- A testing strategy section
- A failure modes table
- Security/privacy/abuse boilerplate
- Operational considerations boilerplate
- Documentation and DX boilerplate
- A decision log

For migration and compatibility: only write about these if there's something genuinely tricky or non-obvious. If the change is purely internal or trivially backward-compatible, skip it.

## After drafting

Once the file is written, offer to run `/grill-me` to pressure-test the design — poke holes in assumptions, surface likely reviewer objections, and sharpen the recommendation. This is the refinement loop, not part of the document itself.

## Review behavior

When reviewing a TD, act like a senior technical reviewer. Check for: unclear problem, missing or unmeasurable goals, hidden scope creep, weak alternatives, unsupported recommendation, missing migration or rollback plan when it's non-trivial, vague claims ("fast", "scalable", "simple"), abstract statements with no concrete example behind them, padding, and unclear ownership.

For each issue: severity (blocking / important / nice-to-have), why it matters, suggested fix. Lead with the most important risks.
