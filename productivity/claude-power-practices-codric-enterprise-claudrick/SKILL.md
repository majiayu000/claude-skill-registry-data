---
name: claude-power-practices
description: >-
  Power-user guardrails for getting professional-grade results from Claude —
  distilled from the "Top 50 Game-Changing Claude Tips" cheat sheet. Use when
  tackling a complex, multi-step, or high-stakes task (analysis, planning,
  research, drafting deliverables, or automation) and you want maximum rigor:
  choosing the right model, structuring prompts with XML tags, extended
  thinking, verifying facts, avoiding fabricated links/citations, and producing
  real deliverables. Triggers on requests to "think harder", "be thorough",
  "no hallucinations", "double-check", "make it rigorous", or "automate this".
---

# Claude Power Practices

Guardrails distilled from the "Top 50 Game-Changing Claude Tips" sheet, turned
into operating rules. Apply the ones relevant to the task; don't recite them.

## Thinking & reasoning

- **Match the model to the job.** Heaviest reasoning / tradeoff analysis →
  Opus; balanced speed+quality → Sonnet; fast, cheap iteration → Haiku.
- **Extended thinking for hard problems.** For scenario planning, multi-step
  tradeoffs, or anything with hidden dependencies, reason step by step before
  answering. (`/think` command wraps this.)
- **Challenge assumptions.** Before committing to a plan, name the load-bearing
  assumptions and stress-test them. (`/challenge`.)

## Prompt structure (CSI + FBI)

Frame non-trivial requests with: **C**ontext, **S**pecific ask,
**I**nstructions + desired **F**ormat, **B**lueprint/example, **I**dentity
(who it's for). Wrap distinct pieces in **XML tags**
(`<context>…</context>`, `<instructions>…</instructions>`,
`<format>…</format>`) so requirements don't bleed together.

## Truthfulness guardrails

- **Don't guess — verify.** Distinguish what you know from what you're
  inferring. For anything past the model's knowledge cutoff, use web search
  rather than asserting.
- **No fabricated links or citations.** Never present a URL, file, citation, or
  "I sent it" claim you can't stand behind. If you can't verify it, say so.
- **Compare runs for consistency** on high-stakes numbers or claims; flag
  discrepancies instead of smoothing over them.

## Real deliverables & automation

- **Produce the artifact, not just talk about it.** When the ask implies a file
  or app (spreadsheet, doc, dashboard, prototype), create/edit it directly
  rather than describing it. Artifacts for shareable prototypes.
- **Systematize repeatable work.** For anything done more than once, define a
  workflow (steps → I/O → checks) and note what a script, Claude Code, or CI
  could automate. (`/workflow`.)
- **Data → analysis → deliverable.** Structure analytical tasks in that order,
  and state the materiality threshold and time window up front.
- **Cite your sources** in analysis so claims are traceable, and keep a short
  "work log" of what changed when the task is multi-step.

## Companion commands (80 total)

The `.claude/commands/` directory turns the full command cheat-sheet into real
slash commands, grouped as:

- **Focus & context:** `/focus`, `/context`, `/details`, `/examples`,
  `/clarify`, `/define`, `/assumptions`, `/priorities`, `/constraints`, `/brief`
- **Think & solve:** `/think`, `/analyze`, `/compare`, `/pros-cons`,
  `/proscons`, `/evaluate`, `/recommend`, `/brainstorm`, `/solve`, `/challenge`, `/model-picker`
- **Organize & structure:** `/outline`, `/structure`, `/bullet`, `/numbered`,
  `/table`, `/summary`, `/key-points`, `/mindmap`, `/flowchart`
- **Code & tech:** `/code`, `/debug`, `/explain`, `/optimize`, `/refactor`,
  `/test`, `/convert`, `/documentation`, `/review`
- **Automate & integrate:** `/workflow`, `/automate`, `/api`, `/integrate`,
  `/schedule`, `/trigger`, `/tasklist`, `/checklist`
- **Personalize & control:** `/preferences`, `/memory`, `/tone`, `/style`,
  `/length`, `/format`, `/reset`, `/clear`, `/about-me`
- **Write & edit:** `/write`, `/edit`, `/rewrite`, `/shorten`, `/expand`,
  `/improve`, `/paraphrase`
- **Data & analysis:** `/insights`, `/forecast`, `/report`, `/stats`, `/clean`
- **Learn & research:** `/research`, `/learn`, `/sources`, `/explore`
- **Collaborate:** `/email`, `/feedback`
- **Content transforms:** `/eli5`, `/tldr`, `/factcheck`, `/proofread`,
  `/glossary`, `/keypoints`

`/clear`, `/memory`, and `/review` collide with Claude Code built-ins — the
built-in takes precedence. See `docs/commands-pack.md` for the paste-ready
prompt versions, or `docs/claude-playbook.md` for the full reference.
