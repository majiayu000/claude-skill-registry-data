---
name: teach
description: "Teach a concept, explain how or why some code works, or zoom out to the big picture."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills teach (+ LEARNING-RECORD-FORMAT.md, MISSION-FORMAT.md, RESOURCES-FORMAT.md, GLOSSARY-FORMAT.md), zoom-out; cursor/plugins pstack 0.15.25 how (+ references/explainer-prompt.md), why (+ references/epistemics.md), teach"
---

# Teach

The goal is that the user understands it, not that anything changes. This skill reads code and writes only teaching files.

## How every explanation runs

This is the user's standing preference; it holds in every branch.
- **Numbered steps, one idea each.** Open with a plain definition: the thing's common name and what it is in general, the way a senior engineer would say it aloud. Then show how it works here, with `path:line` or a tiny example. A few sentences per step.
- **A checkpoint ends every step**: one question or small task that shows whether the step landed ("What happens if two requests reach `reserve()` at once?"). Then stop and wait. Move on after they answer. If the answer misses, re-explain that step another way before going on.
- **Teach the subject on its own terms.** Build from its own concepts and vocabulary. Mapping it onto tools or skills the user already knows ("it's like React's …") gives them the old thing's shape, not this one's. Use an analogy only if they ask.
- **Build pictures up.** For three or more moving parts, draw a short series where each diagram redraws the last and adds one part (mermaid for flows, ASCII for simple relations). One all-at-once diagram is a reference, not teaching.
- **Plain spoken English**: the concrete mechanism, one name per concept, no framing labels ("the key insight", "TL;DR").
- No live user (one-shot run): deliver all steps, with the checkpoints collected at the end.

| Ask | Branch |
|---|---|
| "teach me X", learning a topic across sessions | 1. Teach a concept |
| "how does X work", "why is it like this", a walkthrough before changing it | 2. Explain how or why |
| "zoom out", "big picture", an unfamiliar area | 3. Zoom out |

## 1. Teach a concept

Learning state lives in a teaching workspace: the current directory unless the user names one. Files are created when there is something to write; formats are in `references/workspace.md`.
- `MISSION.md`: why they're learning this, what success looks like, what's out of scope. Missing or vague: the first job is asking why, until the answer is a concrete outcome.
- `learning-records/NNNN-<slug>.md`: what they have shown they understand, prior knowledge they stated, misconceptions corrected.
- `RESOURCES.md`: annotated high-trust sources. Ground specific claims in these and cite them; a specific fact from memory alone is a guess.
- `GLOSSARY.md`: terms they can already use correctly, in this workspace's canonical words.
- `NOTES.md`: how they like to be taught.

1. Read the mission, records and notes. Pick the next thing just past what the records show: challenging enough, not overwhelming.
2. Find one primary source for it and add it to `RESOURCES.md`.
3. Teach it as numbered steps. Knowledge steps stay easy, because difficulty eats the working memory understanding needs. Skill steps use effortful retrieval: they recall or do it from memory, with feedback right away.
4. Write a learning record only on evidence: a non-trivial checkpoint answered correctly, prior knowledge stated, a misconception corrected, or a mission change (confirm a mission change with the user first). Being covered is not being learned.
5. Close with what they can now do, the primary source to read next, and what to revisit next session so practice is spaced.

Done when: every step's checkpoint is answered and each demonstrated understanding has a record.

## 2. Explain how or why

1. **Orient.** Infer from the conversation why they're asking (about to change it, reviewing, debugging, new to it) and what they already know. Put the depth where their question is. Read the code. For a subsystem spanning many files, send two to four subagents to explore distinct angles and reconcile what they find.
2. **How.** Steps follow the runtime flow: what triggers it, each stage, where data goes, the decision points, each with `path:line`. Finish with where things live and the gotchas.
3. **Why.** Gather evidence: `git log --follow`, `git blame -L`, PR bodies (`gh pr view <n>`), linked issues, comments, ADRs. Tier every claim:
   - **Direct**: someone wrote the reason down. Cite it.
   - **Inferred**: your reading of the context. Show the chain.
   - **Unknown**: say what you searched and that it turned up nothing.
   Code is not evidence of its own intent. When the user offers a guess ("I assume it's for performance?"), test it as one hypothesis among several.
4. **About to change it?** End with Preserve / Change / Avoid / Risk.

Done when: every why-claim carries a tier and a citation, and the last checkpoint is answered.

## 3. Zoom out

Go up one layer of abstraction and map the area in `CONTEXT.md` vocabulary, as three steps with a checkpoint each:
1. Where this area sits in the system, and what it is for.
2. The relevant modules: what each owns (one line) and who calls it.
3. What flows between them, drawn as a diagram that grows by one module per redraw.

Then offer to zoom into one module through branch 2.

Done when: the user can name which module owns the thing they asked about, and who calls it.
