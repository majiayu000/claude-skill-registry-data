---
name: coding-prompt-normalizer
description: "Turn rough, mixed-language, speech-to-text-like, repetitive, or partially specified coding requests into a high-signal task-context brief and handoff prompt for agents working inside hermes-agent-setup. Use when the hard part is reconstructing the user's real task, preserving exact literals such as `~/.hermes/config.yaml`, `~/.hermes/.env`, `gonkagate`, or `npx @gonkagate/hermes-agent-setup`, grounding the ask in the current shipped-runtime repo truth, and packaging it for downstream execution. Prompt polish is secondary to accurate repo-aware task reconstruction."
---

# Coding Prompt Normalizer

## Purpose

Turn noisy user task descriptions into context-rich handoff prompts that help a
coding agent understand the user's real task and start in the right place in
`hermes-agent-setup`.

The primary deliverable is not a polished prompt. The primary deliverable is an
accurate task context model:

- what the user wants
- which exact signals matter
- what this repository truthfully implies today
- what is missing
- which assumptions are safe enough to carry forward

The final handoff prompt is just the packaging for that context.

Be honest about the current repository state:

- this repo ships `npx @gonkagate/hermes-agent-setup` as the public onboarding
  helper for Hermes
- the public installer runtime is implemented
- the current CLI is a shipped entrypoint backed by runtime modules under
  `src/` and product contract docs under `README.md`, `AGENTS.md`, and `docs/`
- today's main contract surfaces are `README.md`, `AGENTS.md`, `docs/`,
  `src/cli.ts`, `src/constants/contract.ts`, `test/`, `package.json`, and the
  release workflows
- launch qualification artifacts live under
  `docs/launch-qualification/hermes-agent-setup/`
- contributor skills are mirrored locally under `.agents/skills/` and
  `.claude/skills/`

Do not normalize a prompt into a fake implementation brief for runtime files or
behaviors that do not exist unless the user is explicitly asking to create
them.

## Use This Skill For

- rough notes, pasted chat fragments, or dictated transcripts
- mixed-language coding requests
- requests like "turn this into a normal prompt", "package this for an agent",
  or "rewrite this for Codex"
- repetitive, nonlinear, partially explained tasks where the downstream agent
  still needs accurate task context before it can act

## Do Not Use It For

- generic translation with no repository work
- writing the code, spec, or review itself; this skill prepares the context and
  handoff prompt
- inventing files, behaviors, or product decisions that the repo does not
  support

## Relationship To Neighbor Skills

- Use this skill first when the main problem is poor task phrasing.
- After the task context is reconstructed, downstream work may use repo skills
  such as `typescript-coder`, `technical-design-review`,
  `verification-before-completion`, or `spec-first-brainstorming`.
- Do not turn this skill into a replacement for those domain skills. Its job is
  to create a better starting context and handoff, not to own the whole
  workflow.

## Workflow

1. Capture and normalize the raw input.
   - Load `references/input-normalization.md`.
   - Remove filler, loops, false starts, and duplicated fragments.
   - Keep code-like literals verbatim.
   - Treat repetition as evidence: collapse duplicates, but preserve repeated
     emphasis when it changes priority, urgency, or non-goals.
2. Infer the task mode.
   - Choose one primary mode:
     `implementation`, `bug-investigation`, `review-read-only`, `refactor`,
     `planning-spec`, `architecture-analysis`, `docs-and-messaging`, or
     `tooling-prompting`.
   - If two modes are present, choose the one that changes the downstream
     agent's first action.
3. Decide whether the request is ready for direct execution.
   - Use a direct coding prompt only when the requested change, likely target
     surface, and success criteria are sufficiently inferable, and the work
     looks like a bounded local change.
   - Default to `bug-investigation` when symptoms are clear but the fix is not.
   - Default to `planning-spec` or `architecture-analysis` when the request is
     too ambiguous for safe coding.
   - Default to `planning-spec` for non-trivial or hard-to-reverse work such as
     Hermes config mutation logic, secret-handling strategy, live model
     catalog/auth behavior, profile or target-home semantics, managed-install
     behavior, or broad repository-wide refactors.
   - Review requests stay read-only.
4. Build the task context model.
   - Separate explicit user signals, repo-grounded facts, inferred assumptions,
     missing context, and open questions.
   - Preserve exact literals before interpreting them.
   - Keep uncertainty visible instead of smoothing it away for prompt polish.
5. Select repository context.
   - Load `references/repo-context-routing.md`.
   - Include only the repo facts, docs, constraints, and code areas that
     materially affect this task.
   - Prefer `2-5` targeted points over a project summary.
6. Compose the handoff prompt.
   - Do not mention the source language unless the user explicitly asks.
   - Default the output prompt to English because the repo docs, code, and
     agent instructions are English-first.
   - If the user explicitly requests another output language, honor that.
   - Write for an agent that already has repo access and knows how to inspect
     files, edit code, and navigate the workspace.
   - Keep the handoff dense, context-rich, and action-oriented.
7. Run a final quality gate.
   - No hallucinated files, requirements, or overclaims about shipped
     behavior.
   - No generic stack dump.
   - Exact literals preserved.
   - User intent, repo facts, assumptions, and open questions are not blurred
     together.
   - Assumptions and open questions explicit where certainty is weak.

## Literal Preservation Rules

- Preserve exact file paths, CLI commands, env vars, code identifiers, config
  keys, model ids, field names, and domain terms verbatim.
- Wrap preserved literals in backticks inside the final handoff prompt.
- Do not "improve" or rename tokens like `~/.hermes/config.yaml`,
  `~/.hermes/.env`, `npx @gonkagate/hermes-agent-setup`,
  `hermes-agent-setup`, `gonkagate-hermes-agent-setup`,
  `gonkagate`, `https://api.gonkagate.com/v1`, `HERMES_HOME`,
  `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `GET /v1/models`, `gp-...`,
  `src/cli.ts`, `src/constants/contract.ts`,
  `docs/specs/hermes-agent-setup-prd/spec.md`, or
  `release-please-config.json`.
- If transcript noise makes a literal uncertain, keep that uncertainty explicit.
  Use a phrase like `Possible original literal:` rather than silently
  normalizing it.
- Preserve user constraints exactly when they change execution:
  `read-only`, `do not edit files`, `no refactor`, `investigate first`,
  `do not touch docs`, `keep README and AGENTS truthful`,
  `do not pretend the runtime already exists`, `do not add shell profile
mutation`, `do not widen public scope`, or `do not position for U.S. users`.

## Readiness Rules

Emit an `implementation` or `refactor` handoff only when all are true:

- the requested change is understandable
- the likely code area is narrow enough to inspect first
- ambiguity does not materially change the execution path
- the work does not appear to change fixed product invariants, secret-storage
  rules, config-target assumptions, availability positioning, or other
  hard-to-reverse behavior
- the target surface already exists, or the user is explicitly asking to create
  that new surface

Emit a `bug-investigation` handoff when any are true:

- the text is symptom-first or regression-first
- the root cause is unclear
- multiple docs, tests, or runtime seams could explain the issue
- the task may involve mismatch between docs, PRD, runtime behavior, and
  repository contract tests

Emit a `review-read-only` handoff when the user asks to inspect, review, audit,
or explicitly avoid edits.

Emit a `planning-spec` or `architecture-analysis` handoff when:

- the task is exploratory or cross-cutting
- requirements are incomplete
- the user asks for a plan, spec, or design direction
- the request touches Hermes config mutation, secret storage, auth checks,
  `/v1/models` behavior, managed-install handling, model qualification, or
  other product-contract decisions
- resolving ambiguity is more important than coding immediately

Emit a `docs-and-messaging` handoff when the task is mainly about `README.md`,
`AGENTS.md`, `docs/`, `CHANGELOG.md`, or keeping the shipped helper truthfully
described.

Emit a `tooling-prompting` handoff when the task is about local skills, prompt
rewriting, agent instructions, `.agents/skills/`, or repo-local workflow
surfaces.

When ambiguity remains high, keep `Assumptions` and `Open questions` short but
explicit. Do not hide uncertainty behind polished wording.

## Output Template

Adapt the sections to the mode. Default order:

- `Objective`
- `User intent and context`
- `Relevant repository context`
- `Likely relevant code areas / files`
- `Problem statement` or `Requested change`
- `Constraints / preferences / non-goals`
- `Acceptance criteria` or `Expected outcome`
- `Validation / verification`
- `Assumptions / open questions`

Mode-specific adjustments:

- `review-read-only`
  - say the task is read-only
  - ask for findings first
  - replace implementation acceptance criteria with review deliverable
    expectations
- `bug-investigation`
  - ask the agent to confirm the symptom path and identify root cause before
    coding
  - describe the expected evidence, likely seams, and what should be verified
- `planning-spec` and `architecture-analysis`
  - emphasize boundaries, risks, missing information, and candidate decisions
    rather than edits
- `docs-and-messaging`
  - emphasize user-visible truthfulness and keeping `README.md`, `AGENTS.md`,
    `docs/`, and `CHANGELOG.md` aligned when behavior changes
- `tooling-prompting`
  - keep repo context focused on local skills, prompts, agent support files,
    and mirrored contributor workflow assets inside this repository

Use `User intent and context` to preserve the reconstructed ask, priority
signals, and missing context before listing repo facts. Keep the prompt compact.
Do not force all sections when `1-2` focused paragraphs do the job better.

## Context Handoff Rules

- Start with the real objective, not with "rewrite this prompt".
- Prefer concrete repo surfaces when they are grounded by the input or the
  repository.
- Turn vague references like "here", "this config", or "that flow" into
  hypotheses only when the repo strongly supports one interpretation.
- Separate grounded repo facts from assumptions.
- Mention the first files or docs to inspect when that is reasonably inferable.
- Keep validation realistic: focused tests, `npm run ci`, targeted doc sync
  checks, or specific workflow checks. Do not default to broad repo-wide
  validation unless the change is broad.
- Do not repeat repo-wide instructions unless they materially affect this task.
- Use the existing shipped-runtime surfaces under `src/`, `docs/`, `test/`, and
  `.agents/skills/` when they are materially relevant.
- When the task touches a local skill, prefer the `.agents/skills/` copy that
  actually exists in this repo instead of inventing a `.claude` mirror.
- Do not propose shell profile edits, arbitrary custom base URLs, secrets in
  `config.yaml`, project-local `.env` mutation, or overclaims about behavior
  the shipped helper or live `/v1/models` catalog does not actually support.
- Do not optimize mainly for eloquence. A plain handoff with the right context
  is better than a polished prompt that hides uncertainty or repo truth.

## Examples

### Example 1: Implementation Prompt

Input:

```text
Turn this into a context-rich handoff prompt for an agent. Tighten
`.agents/skills/coding-prompt-normalizer/SKILL.md`,
`.agents/skills/coding-prompt-normalizer/references/`, and
`test/skills-contract.test.ts` so the skill is Hermes-specific, preserves
`~/.hermes/config.yaml` and `~/.hermes/.env`, removes stale prior-project wording,
and keeps the change small.
```

Output:

```text
Objective
Make the smallest change needed to adapt the local `coding-prompt-normalizer`
skill to `hermes-agent-setup`, preserving `~/.hermes/config.yaml` and
`~/.hermes/.env` as exact literals, removing stale prior-project wording,
and adding the smallest verification needed to stop regression.

Relevant repository context
- This repository ships `npx @gonkagate/hermes-agent-setup`; prompt assets
  should reflect the current shipped runtime and live `/v1/models` model
  catalog contract.
- The current contract surfaces are `README.md`, `AGENTS.md`, `docs/`,
  `src/cli.ts`, `src/constants/contract.ts`, and the contract tests.
- Local contributor skills are mirrored under `.agents/skills/` and
  `.claude/skills/`.

Likely relevant code areas / files
- `.agents/skills/coding-prompt-normalizer/SKILL.md`
- `.agents/skills/coding-prompt-normalizer/references/`
- `.agents/skills/coding-prompt-normalizer/evals/evals.json`
- `test/skills-contract.test.ts`

Requested change
Inspect the current skill content, replace stale prior-project assumptions
with Hermes-specific ones, update any stale literals or examples, and add the
smallest contract test needed so the skill does not drift back to the old
project wording.

Validation / verification
- Run the relevant skill contract test slice or `npm run ci`.
- Confirm the updated skill preserves exact literals such as
  `~/.hermes/config.yaml` and `~/.hermes/.env`.
- Confirm the updated skill does not understate shipped behavior or overclaim
  unsupported behavior.
```

### Example 2: Review Prompt

Input:

```text
Package this as a review prompt. Read-only. I think `README.md` and
`docs/how-it-works.md` may overstate what the current CLI actually does around
`npx @gonkagate/hermes-agent-setup` and `GET /v1/models`. Need findings first,
severity ordered, with file anchors. Focus on truthfulness and product
contract.
```

Output:

```text
Objective
Perform a read-only truthfulness review of the current public product docs,
with findings first and ordered by severity.

Relevant repository context
- This repository ships the helper runtime, so docs should distinguish current
  shipped behavior from PRD non-goals or future product changes.
- `README.md` and `docs/how-it-works.md` are major contract surfaces for the
  `npx @gonkagate/hermes-agent-setup` story.
- `GET /v1/models` is part of the shipped onboarding flow, but it is still only
  an auth-plus-catalog signal rather than full billing or first-request proof.

Likely relevant code areas / files
- `README.md`
- `docs/how-it-works.md`
- `src/cli.ts`
- `docs/specs/hermes-agent-setup-prd/spec.md`
- `test/docs-contract.test.ts`

Review deliverable
Review the current repository in read-only mode. Report findings first,
ordered by severity, with file anchors. Focus on truthfulness, product
contract mismatches, and places where docs or placeholder behavior may mislead
users about what is currently implemented.
```
