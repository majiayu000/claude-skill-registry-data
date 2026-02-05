---
name: plan-mode
description: "Guidelines for Plan Mode - focus on planning before implementation"
---

# Plan Mode

Provides guidelines for Plan Mode workflow: planning and design before implementation.

## Core Behaviour

**Entry:** Acknowledge with "**Plan mode engaged.**" If this skill was loaded as part of a planning request, acknowledge after loading this skill.

1. **Clarifying questions:** Identify ambiguities or missing requirements before drafting. Ask user open questions with recommended solutions. Ask questions early, don't assume.
2. Present plan to user.
3. Stay in Plan Mode until user says **go** (or **proceed**/**continue**).
4. When the user confirmed with **go**, write the summary of the plan into a markdown file inside `artefacts/`. Do not overwrite, always create a new summary file following this format: `plan-summary-${MMDD hh:mm:ss}`.

- Acknowledge with "**Plan mode disengaged.**"
- Then begin implementation.

**Restrictions:**

- Create/update plans only
- No file edits except Markdown in `artefacts/`
- Ask open questions to clarify requirements
- Use `todowrite` tool for task tracking
- Research allowed: read files, search codebase, run diagnostic commands, answer questions
- No implementation: no edits, installs, or deployments

**Exit:** User says **go**

## Changes summary

Write into a markdown file inside `artefacts/` of a summary of the changes once done. Do not overwrite, always create a new summary file following this format: `change-summary-${MMDD hh:mm:ss}`

## Open Questions

Ask clarifying questions for ambiguity or missing requirements.

In planning modes, if there are points for clarification that will significantly change the plan depending on its answer, ask them _before_ creating plans.

For each question:

- Provide a clear recommended solution with reasoning
- Offer alternative approaches when applicable
- Include relevant considerations (technical, business, UX)

Example:

```
1. **Root page:** Should the root `/` page redirect to a default language (e.g., `/es`), or remain separate?

   - a. Redirect to `/es` based on browser language detection _(recommended)_
   - b. Show a language selection landing page

2. **Default role:** What should be the default user role upon registration?

   - a. Basic user with limited permissions _(recommended)_
   - b. Trial user with time-limited premium features
```

## Example

```
### User:

   /plan add dark mode

### Assistant:

  **Plan mode engaged.**

  [Reads files, creates todo list]

  Before I draft the plan:
  1. System detection? a) Yes (recommended) b) No

### User:

  1a

### Assistant:

  Here is the plan:
  1. Add toggle to settings
  2. Implement theme context
  3. Update CSS variables

  One detail:
  2. Persist preference? a) localStorage (recommended) b) session-only

  Ready when you say **go**.

### User:

  2a, go

### Assistant:

  **Plan mode disengaged.** [Begins implementation]
```
