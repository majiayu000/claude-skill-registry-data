---
name: product
description: "Turn an idea into a feasibility-checked PRD and a parallel-ready roadmap through research and an interview."
when_to_use: "Use when the user runs /ac:product with an idea to specify before any planning; not for a change that is already specified."
argument-hint: "<idea or feature>"
disable-model-invocation: true
effort: high
---

# /ac:product

Acts as the product manager for one idea: reads what exists, checks feasibility with research agents, interviews the user on every decision, and writes a PRD and a roadmap that `/ac:plan`, `/ac:coordinate` and the working rules can build from. It writes documents only. The user decides which consumer runs next.

Request: $ARGUMENTS

## Standing rules

These hold for the whole run and sit before the procedure so a compaction keeps them.

- Writes only `docs/prd/<slug>.md`, `docs/ROADMAP.md`, `.ac/product/<slug>/` (interview log and research) and `.ac/tasks/<slug>-b<N>.yaml`. No application code, no commit, no push.
- Never start `/ac:plan`, `/ac:coordinate` or `ac:flow`. Print the handoff commands and stop.
- Read before asking. Never ask what the repository, `PROJECT.md` or the research answers. Ask only a preference, a priority, a tradeoff or an outward action.
- Interview with `AskUserQuestion`: rounds of up to three questions on related decisions, each option carrying the concrete artifact and your recommendation first, in the user's language. In a session without that tool, end on the open decision as the named blocker.
- You do not decide alone that the interview is complete. It ends when the user confirms the playback in phase 6.
- Research is sized to the work: a full pass for a new product, a light one for a feature in an existing project. Agents are `ac:librarian` (anything external) and `ac:explore` (this repository), never `general-purpose`. Each brief names one angle, and all briefs of a phase go out in one message.
- Interactive sessions run every subagent in the background. After a fan-out end the turn with a one-line status and continue on the notification; do not poll or sleep.
- A research report is a claim. Open what it cites before it changes a decision, and mark what you could not verify as unverified in the PRD.
- Write the documents in the language the project's docs already use, English by default. Talk to the user in their language.

## 1. Frame

Decide the mode: a repository with source files or a `PROJECT.md` is a feature in an existing project; an empty or new directory is a new product. If it is unclear, ask once. Derive a kebab-case slug of at most six words and create `.ac/product/<slug>/interview.md`, a running log of each decision and whether it was the user's statement or an accepted recommendation.

State the request back in two sentences and name the one open question whose answer would change what gets built the most.

## 2. Read (feature) or discover (new product)

Feature: read `docs/PROJECT.md` or `PROJECT.md`, the README, the manifest, the entry points, the data model and the tests that touch the area, directly or through one or two `ac:explore` briefs. New product: skip this and go to phase 3.

## 3. Feasibility

Run the checklist in `${CLAUDE_SKILL_DIR}/references/feasibility-and-interview.md` at the depth its "Pass depth by mode" section gives. Brief shape, one block per angle:

```
CONTEXT: why this research, one or two sentences
GOAL: the specific question to answer
DEPTH: quick | medium | thorough
BUDGET: explore: a pass count. librarian: a number of web searches, five is the working ceiling
DOWNSTREAM: how you will use the result
REQUEST: what to return, the format, what to skip
```

Market research (alternatives, pain, spend, break-even) follows the "Market checklist" in the same reference, sized by mode; a Low-confidence or no-go market on a new product goes to the user as a decision, and no number is invented.
`DEPTH` and `BUDGET` are required; a blank field returns the thin default pass. `ac:librarian` does not read CLAUDE.md, so put anything the user told you to leave out of research into its brief.

Write the findings to `.ac/product/<slug>/feasibility.md`, one row per dimension with the evidence, its source and a go, no-go or unknown signal. A no-go on a core dimension stops the run: ask whether to change the scope, continue with the risk named, or drop the idea.

## 4. Interview

Follow the protocol in the same reference: frame, stories, decisions, scope, then sweep the coverage categories until each has an answer. Lint every question against its list before asking. Append each answer to `interview.md`. A decision that blocks nothing takes your recommendation, stated, and the run carries on.

## 5. Write

Write the PRD and the roadmap from `${CLAUDE_SKILL_DIR}/references/templates.md`, then one task file per bundle in `Now`. Fill the PRD's Market section from `feasibility.md`, keeping its confidence tags, and compute the break-even from the interview's revenue target and conversion range.
Check the traceability rules in that file before showing anything: every requirement realizes a journey and is covered by a bundle or deferred, every bundle has an acceptance a command or a person can check, and bundles that may run together do not touch the same paths.

When the project has no `PROJECT.md`, name `ac:project-md-writer` as a follow-up; when it is a new repository with no Claude Code setup, name `/ac:init-project` too. When the idea has a visual side, name `ac:frontend-design` and `ac:design-md-writer`. Do not run them.

## 6. Playback

Show the user a short playback (the problem, the outcome, the requirements in one line each, the bundles in order), what they said and what you proposed labelled apart. Then ask with `AskUserQuestion` whether to accept or which part to revise. Revise and ask again, at most twice; after that ask what is blocking.

## 7. Review

For a new product, or a feature with more than five requirements, send one `ac:oracle` the PRD, the roadmap, the feasibility file and the interview log. Ask it to check traceability, ambiguity a builder could read two ways, missing non-goals, bundles that claim to be parallel but touch the same paths, and claims that outrun their sources. Fix what it confirms and say which findings you left and why. A smaller feature skips this phase.

## 8. Hand off

Print, with the paths:

- the PRD and roadmap files written and their line counts;
- the commands from the "Handoff commands" section of `templates.md`, filled in for this slug (for `/ac:coordinate`, with the settled bundles written into the request string);
- the assumptions you took and what stayed unverified.

Mention that nothing was committed.

## References

| File | Read when |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/feasibility-and-interview.md` | Phases 3 and 4 |
| `${CLAUDE_SKILL_DIR}/references/templates.md` | Phase 5 and the handoff |
