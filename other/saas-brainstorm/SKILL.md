---
name: saas-brainstorm
description: "Guides the user through finding and choosing a product concept. Use when the user wants product ideas, a new concept, a SaaS application jam idea, or to explore other directions, including dropping the current idea and starting over."
argument-hint: "[genre or theme hint, or 'open'] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, WebSearch, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-brainstorm/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation,docs.density,workflow`

Resolved above; use as-is. No block → the defaults in `.claude/docs/config-resolution.md`
(`workflow: minimal`, `review_mode: solo`, `automation: collaborative`, `docs.density: terse`), and
say that the settings were not read.

# Brainstorm

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Turns no idea, or a rough one, into a written design the next step builds from. How much it writes
depends on `workflow`:

- **`minimal`:** the Lean Brief flow below: a one-page `design/product-brief.md`, then stop. No
  discovery questions, pillars, director gates or `product-concept.md`, and do not load
  `references/full-concept.md`.
- **`standard` or `full`:** read `references/full-concept.md` and follow it. It writes
  `design/prd/product-concept.md` from `.claude/docs/templates/product-concept.md`. Its gates follow
  `.claude/docs/director-gates.md`; each director agent is given its own gate file,
  `.claude/docs/director-gates/<gate-id in lower case>.md` (`pd-product-pillars.md`,
  `ds-branding-ui.md`, `td-feasibility.md`, `dp-scope-assessment.md`), and you do not read those files
  yourself.

`--review` in the text typed after the skill name overrides `review_mode` for this run.
`docs.density` sets each section's depth: `terse` = bullets; `balanced` = with brief rationale;
`thorough` = rationale and alternatives. Questions follow `.claude/docs/automation-modes.md`
(collaborative asks, guided asks only for major decisions, autonomous logs and proceeds; the
always-ask categories always ask).

Ask with the question tool. Without one, list the options numbered and end your turn to wait. The
question is the last thing in the reply: no advice or lean after it. A skipped or dismissed
question is not an answer: ask again in plain text.

## Lean Brief flow (`workflow: minimal`)

A few exchanges, not fifteen: capture the thinking that carries the product on one page, then get to
code. Write from the template `.claude/docs/templates/product-brief.md` (six required fields, three
one-liners). If `design/product-brief.md` exists, read it and refine it instead of starting over.

1. **Concept.** From the hint typed after the skill name (or one quick open question if there is
   none), propose **2 or 3 one-line concepts** (verb-first or a mashup of genre and theme), not
   full concept cards. Ask the user to pick or combine them. This is the one creative question
   every run asks.
2. **Fill the brief** in conversation, several fields per exchange:
   - **Working title:** the brief's title line. Offer one from the chosen concept and let the user
     change it; `/saas-create-stories` names the epic folder after it.
   - **Pitch:** the excited one-liner.
   - **Core loop:** the 2 to 4 steps the user repeats.
   - **User goal & fail state**: what the user tries to do, and how they lose.
     `/saas-create-stories` turns it into acceptance criteria.
   - **MVP:** the short list that makes it the MVP; each item becomes a story. **More than 7
     items: push back.** Say it is too long for an MVP, propose which items to cut (the ones the
     core loop works without), and keep the brief to 7 or fewer.
   - **Out of scope:** what they are deliberately not building (the cut items go here).
   - **Build order:** the riskiest or least proven part first.
   - **Who it's for and what they feel**, **Art & audio direction**, **Reference product** (the
     closest shipped product, and the part of it the MVP keeps): one line each; offer, don't force.
3. **Show the filled brief in full.** Then ask, as its own question: "Brief is ready. May I write it
   to `design/product-brief.md`?" `Yes — write it` / `Revise a field first`. Write only on an explicit
   yes to this question; agreeing to a cut or saying "go on" is not a yes to the write. On a
   revision, change the named field, show it before and after, and ask again. Then write
   `design/product-brief.md`, creating folders as needed. Never write `design/prd/product-concept.md`
   at this tier.
4. **Next steps.** Read `stack.frontend` in `project.yaml`:
   1. `/saas-setup-stack`: configure the engine. List it **only** when `stack.frontend` is absent or
      empty: on the minimal path it usually ran before this skill.
   2. `/saas-create-stories`: turn the MVP list into stories. At `minimal` there is no separate
      `/saas-create-epics` or `/saas-sprint-plan`; the build order is the plan.
   3. `/saas-dev-story`: the first line of production code.

   Then one summary line: the pitch, the number of MVP items, and `design/product-brief.md`. End with
   the line `Verdict: COMPLETE — product brief written; next stop is code.`

If the user stops before the write, say the brief was not written, so it lives only in this
conversation.
