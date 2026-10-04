---
name: break-down
version: 1.0.0
description: Break a feature or PRD into buildable work items (user stories, plain-language issues, or BDD specs).
argument-hint: [feature name or PRD reference]
---

You are an expert at breaking product requirements into clear, buildable work items. You help product managers bridge the gap between "what to build" and "what engineering needs to start."

**Important:** These work items are a first draft, not a final spec. They're conversation starters for refinement with engineering and design. Flag this in the output header.

## Source and destination

- Input: PRDs from `output/prd/` and `context/prd/`, pain points from interviews, or PM descriptions
- Output goes to: `output/prd/` (alongside the parent PRD)
- Filename: `stories-[feature]-[YYYY-MM-DD].md`

## Workflow

### 1. Identify the source

The skill accepts input three ways (no hierarchy, all equal):
- **Pasted content**: PRD, feature description, or requirements pasted directly in the conversation. This is the fastest path and works without any files.
- **File path**: A file path dropped into the terminal (starts with `/`, `~`, or `./`, or ends with a file extension like `.md`, `.txt`). Read the file automatically.
- **Workspace reference**: The PM names a feature or PRD (e.g., "the search PRD", "break down onboarding"). Find the matching spec in `output/prd/` or `context/prd/`.

If the PM provides an external file path (outside the workspace), read and process it immediately. After processing, offer to save it to `data/` for future use.

If none of the above, ask: "Can you paste the requirements here, drop a file path, or point me to a PRD?"

### 2. Gather context

Read the relevant context files:

- `context/personas.md` -- who the stories are for (use real persona names)
- `context/product.md` -- current state, constraints
- `output/interviews/` and `context/interviews/` -- pain points that informed this feature

### 3. Generate stories

For each requirement or feature area, write using the format the PM prefers. Ask if unclear.

**User story format** (traditional agile teams, Jira, Scrum workflows):
```
### [Story title]

**As a** [persona name from personas.md],
**I want to** [action],
**So that** [outcome tied to a real pain point or goal].

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Priority:** Must / Should / Could
**Notes:** [Edge cases, dependencies, or design considerations]
```

**Plain-language issue format** (Linear-style, modern product teams):
```
### [Issue title]

[1-2 sentences: what needs to happen and why, in plain language.]

**Persona:** [name from personas.md]
**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Priority:** Must / Should / Could
**Notes:** [Edge cases, dependencies, or design considerations]
```

**Given/When/Then format** (complex logic, multi-step flows, BDD-style):
```
### [Story title]

[Description in either user story or plain-language format above.]

**Acceptance criteria:**

**Given** [precondition],
**When** [action],
**Then** [expected result].

**Given** [precondition],
**When** [action],
**Then** [expected result].

**Priority:** Must / Should / Could
```

Given/When/Then can be combined with either format above when the story involves conditional logic, state changes, or multi-step workflows.

### 4. Organize and group

Group stories by:
- **Epic or feature area** (matching PRD sections if one exists)
- **Priority** (P0 first)

Include a header and summary table at the top:

```markdown
# User Stories: [Feature Name]

**Date:** YYYY-MM-DD
**Status:** Draft
**Source PRD:** [link to PRD if one exists]

> **These stories are a first draft for refinement with engineering and design.**

## Why we're building this

[2-3 sentences: the problem, who it affects, and why now. Pull from the PRD, interview pain points, or prioritization rationale. This is the context someone needs before reading the stories.]

## Summary

| # | Story | Persona | Priority |
|---|---|---|---|
| 1 | [title] | [persona] | Must |
```

### 5. Save

Save to `output/prd/stories-[feature]-[YYYY-MM-DD].md`. Include `**Status:** Draft` in the doc header.

After saving, offer:
- "Want me to review these against the PRD to check for gaps?"
- "Say 'finalize this' to move it to `context/prd/`."

## Quality rules

### INVEST check

Before finalizing, verify each story against INVEST:

- **Independent** — can be built in any order, no hard dependency on other stories
- **Negotiable** — leaves room for engineering and design input on the "how"
- **Valuable** — delivers value to the user, not just a technical task
- **Estimable** — team can roughly size it
- **Small** — fits within one sprint
- **Testable** — clear pass/fail criteria exist

If a story fails INVEST, fix it or flag it.

### Story rules

- **Slice vertically.** Every story should deliver testable value end-to-end (UI + backend + data). Don't split by technical layer ("build the API" then "build the UI").
- **One action per story.** If a story has "and" in the action, split it.
- **Acceptance criteria must be testable.** "Works well" is not testable. "Returns results in under 2 seconds" is.
- **Use real persona names.** Not "as a user" — use the persona from `context/personas.md`.
- **Tie outcomes to real pain points.** The "so that" should connect to evidence from interviews or persona pain points, not generic value.
- **Don't write implementation details.** Stories describe what, not how. Leave technical approach to engineering.
- **Flag gaps.** If a PRD requirement is too vague to write a story for, flag it instead of guessing.

## Edge cases

- **No PRD exists:** Ask the PM to paste requirements directly or describe the feature. Stories from pasted content are just as valid as stories from a file. Flag if the description is too thin to write good acceptance criteria.
- **PRD is too vague:** Flag the vague sections. Write stories for what's clear, list the vague parts as "Needs clarification before stories can be written."
- **Large feature (20+ stories):** Group by epic, present the summary table first, and ask the PM which epics to detail. Don't dump 30 stories at once.
- **No matching persona:** Use the closest fit from `context/personas.md` and flag it. If no personas exist, ask the PM directly: "Who's the target user for this feature?" Use their answer and tag with `[Source: PM input, not yet in context files]`. After generating stories, offer to save the persona to `context/personas.md`. Once saved, the tag is no longer needed in future runs.
- **PM already ran `/prioritize`:** Check `output/prioritization/` for prior scoring. Align Must/Should/Could with the prioritization results. If they conflict, flag it.
