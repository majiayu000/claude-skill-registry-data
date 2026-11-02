---
name: teach-me
description: |-
  Use when the user wants to be taught a subject, not just answered — "teach me X", "help me learn X", "help me understand X", "help me grok X", "explain how X works", "quiz me on X", "I keep bouncing off X" — where X can be anything: a historical period, a statistical method, music theory, a poem, a legal concept, a cooking technique, a library, a codebase, or a code change. Change-focused asks belong here too: "explain this diff/PR/branch", "walk me through this change", "onboarding doc for this change", "teach me what changed", "help me/my team understand this PR". Spans a quick in-chat lesson up to a saved, dated lesson artifact. Not for: a quick factual answer (just answer), needing only to see a shape or sketch (use show-me), writing a commit message (use commit-message), or reviewing code for defects (use code-review).
---

# Teach Me

Turn a subject into a lesson, not a summary.
A summary tells the reader what is true; a lesson leaves them able to explain it, apply it, and check themselves.
The structure comes from learning science — each design choice names its principle inline, and full citations live in `ATTRIBUTION.md`.

## Invocation Notice

- Tell the user when this skill is running: `teach-me`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Writing Style

Write as a professional technical writer, with the clarity of Martin Kleppmann.
Lean toward ASD-STE100: short sentences, active voice, one term per concept.
Keep identifiers, commands, and paths exact.

Use industry- or domain-standard terms, and define each on first use.
Never coin your own terms.
A made-up label reads as standard vocabulary, teaches a word that exists nowhere else, and blocks the reader from finding real sources.
If a concept has no standard name, describe it in plain words instead of naming it.

## Sizing the Lesson

Decide two axes per invocation:

- **State** — ephemeral in-chat lesson, or a saved artifact.
- **Intensity** — how much you build (latency the user waits through) and how much the reader must hold (cognitive load).

A full-intensity lesson has four sections in order: **Background, Intuition, Walkthrough, Quiz**.
Lighter asks deliver a subset: "just help me grok it" is Intuition plus a line of Background.

Default light-first.
Deliver the sized lesson, then close with a one-line offer of more depth or a saved artifact.
Two overrides:

- When the ask names the heavy thing ("an onboarding doc", "a lesson I can revisit"), build it directly.
- Never run an upfront sizing questionnaire — persistence is a save-at-the-end decision, not an intake question.

## Gathering Material

Ground every lesson in real sources; never trust parametric knowledge alone.

- At full intensity, research before teaching: use the `mcp-research` skill for library and API subjects, and `deep-research` for anything else beyond your reliable knowledge.
  Cite what you used.
- A light pass may skip the research hop; say so when confidence is low.
- If the subject lives in the user's local files — a codebase, documents, notes, or data — read the actual files before explaining them.
- If the subject is a specific code change, follow `references/code-change.md` for resolving and exploring the diff.

## Section Guide

**Background — activate prior knowledge** (advance organizers).
Write two layers: a deep layer a novice needs and an expert skips, then a narrow layer specific to the subject at hand.
The split exists because extra scaffolding helps novices but hurts experts (expertise-reversal effect).
For a lesson on the Reformation, the deep layer covers how the medieval church held authority; the narrow layer covers the indulgence controversy Luther answered.
For a code change, the narrow layer is the subsystem the diff lands in.

**Intuition — essence first.**
Open with one concrete toy example, then generalize (concreteness fading).
To teach compound interest, follow one $100 deposit through three years before writing the formula; to teach a cache, trace one repeated lookup before defining eviction.
Pair the idea with a figure — words plus pictures beat words alone (dual coding).

**Walkthrough — the substance itself.**
Chunk it, and order the chunks purposefully so working memory is never overloaded (cognitive load theory).
Build from primitives to composition: intervals before chords before progressions; functions before the pipeline that composes them.

**Quiz — retrieval practice** (testing effect).
Five interactive multiple-choice questions with per-option feedback.
Read `references/quiz-design.md` and apply its rules, including the self-check pass — do not write items from memory.
In chat, run the quiz conversationally: pose the questions and end your turn, then give the per-option feedback after the user answers — never print the answers alongside the questions.

## Figures

When a figure's point is a shape or structure, use the `show-me` skill's palette.
If it becomes clear mid-lesson that the user only needed to see the shape, give them the visual and stop.

## Format Rules

Full contracts for both formats are in `references/output-formats.md`.
Easy to miss:

- No ASCII-art diagrams; embed figures so the file works offline.
- HTML code blocks styled as `div`s need `white-space: pre` or the browser collapses newlines.
- The quiz must be interactive in every medium — conversational in chat (ask, wait, then feedback), vanilla JS in HTML, `<details>` blocks in Markdown.
- Use callouts for key concepts, definitions, and edge cases.

## Output

- **Light path:** the sized lesson in chat, closing with the one-line offer of depth or a saved artifact.
- **Deep path:** one dated artifact — HTML by default, Markdown on request — saved in the user-chosen directory (default `.teach/`), with the path returned to the user.

## Lesson Series

One invocation teaches one lesson; invoke the skill again for the next.
Saved lessons accrete in `.teach/` into a curriculum: when the user returns to a subject, read the artifacts already there and build the next lesson on top of them — advance, don't repeat.
No syllabus or planning file is needed; the dated lessons are the record.

## Related Skills

- `show-me` — when seeing a shape settles the question; also supplies the figure palette.
- `interactive-notebook-demo` — when the subject is best understood by running it; an executable walkthrough.
- `mcp-research` / `deep-research` — source grounding before teaching.
- `code-review` — judging a change, not explaining it.
- `commit-message` — writing the commit message for a change.

## References

- `references/quiz-design.md` — item-writing rules and the pre-save self-check for the quiz.
- `references/output-formats.md` — the HTML and Markdown artifact contracts.
- `references/code-change.md` — resolving and exploring a diff when the subject is a code change.
- `ATTRIBUTION.md` — source prompts and the learning-science citations behind each design choice.
