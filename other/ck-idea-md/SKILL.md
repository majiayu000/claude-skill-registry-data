---
license: MIT
name: idea-md
description: Create or expand an Idea.md / IDEA.md file from a rough description, existing repo, conversation history, notes, or other early-stage product inputs. Use when the user asks to "write an Idea.md", "turn this into an idea file", "capture this product idea", "expand this concept", or wants a repo-grounded concept brief before validation, PRD, or implementation work.
---

# Idea.md

## Overview

Create a strong `Idea.md` when the user has an early concept but not yet a full PRD. Treat it as the bridge between raw brainstorming and formal product requirements.

An `Idea.md` is **not** universal. If the repo already has a local convention, follow it. If not, default to the house definition in `references/what-is-idea-md.md`: a concise, structured concept brief that captures the problem, user, solution, repo fit, risks, and next validation steps.

Announce at start: `I'm using the idea-md skill to create or refine the idea file.`

## Inputs to Gather

Pull from the richest available sources, in this order:

1. Existing `Idea.md` / `IDEA.md` / related drafts
2. Current repo context: `README`, specs, roadmap docs, issues, package structure, notable constraints
3. Conversation history and user-provided notes
4. Adjacent artifacts such as PRDs, design docs, or research notes

If a repo exists, inspect it before writing. Do not invent technical context that could be learned from the codebase or docs.

## Workflow

### 1. Determine the mode

Pick one:

- **New idea file**: no existing idea doc, user wants one created
- **Expansion**: user has a rough draft and wants it expanded
- **Rewrite**: user wants a cleaner, more structured version of an existing idea file

### 2. Infer the right format

- If the repo already uses an `Idea.md` convention, preserve it.
- If the workflow expects `Idea.md` as an upstream planning artifact, keep it structured and concise.
- If the request is just idea capture, it can be lighter, but still make it legible to someone other than the original author.

Use `references/idea-template.md` when no local template exists.

### 3. Synthesize, do not merely transcribe

Turn rough notes into a coherent narrative:

- sharpen the core thesis
- remove repetition
- surface implicit assumptions
- separate what is known from what is speculative
- preserve genuinely distinctive phrasing or insights from the user

### 4. Ground it in reality

If a repo is available, include concrete repo-aware context:

- which existing surfaces, packages, or systems the idea builds on
- constraints that shape the idea
- relevant integration points or architectural leverage

If there is no repo, make assumptions explicit instead of pretending they are facts.

### 5. Keep the scope at the right level

An `Idea.md` should be:

- more structured than a scratchpad
- less detailed than a PRD
- persuasive enough to explain why the idea matters
- concrete enough to guide validation or next-step planning

Do **not** turn it into a task-by-task implementation plan unless the local workflow explicitly expects that.

## Default Output Shape

When there is no repo-specific format, use this shape:

1. Title
2. One-paragraph overview
3. Problem
4. Who it's for
5. Proposed solution
6. Why this could work / differentiators
7. Repo or technical fit
8. MVP
9. Risks and open questions
10. Validation or next steps

Adjust section names if the repo has established terminology.

## Quality Bar

- Lead with the insight, not throat-clearing
- Use concrete nouns and verbs; avoid hype
- Prefer specific tradeoffs over generic optimism
- Make unknowns legible
- If the idea comes from conversation fragments, resolve contradictions or call them out
- If expanding an existing draft, preserve meaning while raising clarity and usefulness

## When to Ask Questions

Ask only when a missing answer materially changes the document:

- target user is unclear
- the core problem is ambiguous
- there are multiple conflicting product directions

Otherwise, infer conservatively and label assumptions.

## Included References

- `references/what-is-idea-md.md`: researched definition and observed patterns
- `references/idea-template.md`: default house template when no local convention exists
