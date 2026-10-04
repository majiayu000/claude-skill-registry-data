---
name: big-project-workflow
description: "A workflow skill that lets Codex keep coding for 60 hours on medium and large projects: Claude Code CLI plans through an interactive requirements questionnaire, PRD, specs, and roadmap; Codex implements verified vertical slices, with resumable Long-Run Execution for lengthy work; Trellis maintains project memory. Use when the user mentions 大项目工作流, Codex 连续开发 60 小时, Codex 长任务, long-running or resumable Codex implementation, large/medium project, new SaaS, multi-module system, requirements questionnaire, Claude Code CLI planning, Codex implementation handoff, Trellis bootstrap, non-system-drive project, or vertical slice. Skip for: single-file edits, casual Q&A, copy polish, throwaway prototypes, or tasks the user explicitly wants done fast without process."
---

# A Skill That Lets Codex Keep Coding for 60 Hours

A two-stage orchestrator on top of [Trellis](https://github.com/mindfold-ai/trellis)
for substantial development runs. Claude Code CLI turns real user answers into
a plan; Codex executes verified vertical slices; Trellis preserves project
memory. For runs stretching toward 60 hours, Stage 2 adds resumable Long-Run
Execution with evidence tracking and final review.
Detailed checklists live in `references/` and load on demand.

## Tool Contract

| Tool | Owns |
|------|------|
| **Trellis** | `.trellis/spec/`, `.trellis/tasks/`, `.trellis/workspace/`, `.trellis/workflow.md`, SessionStart hook |
| **Claude Code CLI** | Stage 1 — project brief, requirements questionnaire & answers, PRD, specs, roadmap, kickoff task |
| **Codex** | Stage 2 — implementation, verification, debugging, doc updates, review |

## Use / Do Not Use

Use for new products, multi-module apps, projects involving
database/API/LLM/deployment decisions, large refactors that need scope and
verification, and any workflow where Claude writes documents first and Codex
implements afterward.

Do not use for tiny one-file fixes, casual Q&A, copy polish, or quick
throwaway prototypes when the user explicitly wants speed over process.

## Phase 0: Inspect Current State (existing repo)

If the user invokes the skill in an existing repository, inspect before
creating or editing any workflow document. Read these anchors when present:

- `AGENTS.md`, `README.md`
- package files (`package.json`, `pyproject.toml`, `requirements.txt`, ...)
- `docs/`
- `.trellis/`, `.trellis/workflow.md`, `.trellis/spec/`, `.trellis/tasks/`,
  `.trellis/workspace/`
- `.claude/`, `.codex/`
- tests, `.env.example`

Then report:

- current repository state,
- whether Trellis exists,
- whether PRD/spec/roadmap exist,
- whether tests and verification commands exist,
- which phase should run next.

Routing: if key Stage 1 documents are missing, run Stage 1. If they are
present and a kickoff task exists, run Stage 2. If only verification is
missing, add a smoke check first.

## Bootstrap A New Project

For a new project, prefer a **non-system drive**. On Windows the script
refuses system-drive targets unless `--allow-system-drive` is passed.

PowerShell:

```powershell
$SkillRoot = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME "skills/big-project-workflow"
} else {
  Join-Path $HOME ".codex/skills/big-project-workflow"
}

python (Join-Path $SkillRoot "scripts/bootstrap.py") `
  --root "<non-system-drive>/codex-projects" `
  --name "<project-slug>" `
  --developer "<developer-name>" `
  --brief "One paragraph describing the project goal" `
  --trellis-version latest
```

Bash / zsh:

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"

python3 "$SKILL_ROOT/scripts/bootstrap.py" \
  --root "$HOME/codex-projects" \
  --name "<project-slug>" \
  --developer "<developer-name>" \
  --brief "One paragraph describing the project goal" \
  --trellis-version latest
```

The script creates the project folder, runs `git init`, runs
`trellis init --codex -u <developer> -y` (default), and renders the
project templates from `assets/templates/` into the project. If `trellis` is not
on `PATH`, the script prints the install command and exits cleanly — it
does **not** silently install npm packages.

### Output language

Pass `--language en` or `--language zh-CN` to control the language of the
rendered templates and the bootstrap `Next steps` hint. Default is
`auto`, which checks `BIG_PROJECT_LANGUAGE`, then `LANG` / `LC_ALL` /
`LANGUAGE` env vars, then the system locale, mapping any Chinese locale
to `zh-CN` and everything else to `en`. To add a new language, drop a
`<template>.<lang>.md` file next to the existing English template; the
renderer prefers the localized variant when present and falls back to
English otherwise.

## Stage 1: Claude Plans

Run from the project root inside an **interactive** Claude Code session.
Do not use `claude -p` (headless / print mode) — Stage 1 produces a
structured questionnaire that needs a human to answer it. Headless mode
silently fills every answer with `(default assumption)`, defeating the
core value of this workflow.

PowerShell:

```powershell
cd <project-path>
claude
```

Bash / zsh:

```bash
cd <project-path>
claude
```

In the Claude Code session, say:

> Read `docs/claude/00-prd-spec-prompt.md` and run Stage 1.

Claude inspects the project, asks you to confirm scope and the
questionnaire size, runs the questionnaire interactively, and only
then writes the PRD / specs / roadmap / kickoff task / handoff doc.

To pick a planning model, use `/model` inside the session. Prefer
Opus-class with 1M context (e.g. `claude-opus-4-7[1m]`); the exact
identifier changes over time, and the bundled prompt does not pin one.

Claude writes or updates the Stage 1 document set:

- `docs/PROJECT_BRIEF.md`
- `docs/REQUIREMENTS_QUESTIONNAIRE.md`
- `docs/REQUIREMENTS_ANSWERS.md`
- `docs/PRD.md`
- `docs/ROADMAP.md`
- `.trellis/spec/*` (only the tiers the project actually needs)
- `.trellis/tasks/001-implementation-kickoff.md`
- `docs/codex/00-implementation-handoff.md`

Detailed per-document field lists are in `references/handoff-flow.md` —
load on demand, do not memorize.

### Stage 1 — Project Mode (Q0, asked first)

Before generating questions, Stage 1 must ask the user:

> Is this a **single-shot project** (everything you want shipped in
> one run, no v2) or an **iterative product** (multiple versions, v1
> intentionally narrow)?

The answer is locked as Q0 in `docs/REQUIREMENTS_ANSWERS.md` and
shapes every later document:

- **single-shot** — `ROADMAP.md` covers *every* feature. PRD has no
  Future Roadmap section. Out of Scope = items the user has ruled
  out forever. Default for tiny / small projects.
- **iterative** — `ROADMAP.md` covers v1 only. PRD § Future Roadmap
  lists deferred features. Out of Scope = never-do items, distinct
  from "later" items. Default for medium / large projects.

When the user is unsure, state the default for their project size
explicitly and let them override.

### Stage 1 — Requirements Questionnaire (THE core value-add)

Before writing the PRD, generate a structured questionnaire. This is the
single largest reason this workflow outperforms ad-hoc prompting.

- Question count by project size:
  - **Tiny project** (single script, smoke test, throwaway tool):
    10-20 questions
  - **Small project**: 30-60 questions
  - **Medium project**: 80-150 questions
  - **Large project**: 150-500 questions
- Pick the band from the brief; if unsure, ask the user before generating.
- Group by module.
- Each question carries four fields: **question**, **type**
  (single-choice / multi-choice / open / boundary condition / acceptance
  criterion), **why it matters**, **default if user skips**.
- Cover, when relevant: target users, roles & permissions, core user
  journeys, pages/interfaces, data objects, business rules, edge cases,
  admin/backoffice, API design, database design, AI/LLM integration,
  prompt & fallback rules, logging & analytics, security & privacy,
  testing, deployment, out-of-scope boundaries.
- In **single-shot** mode, do NOT split questions into "v1 now" vs "v2
  later" or other release buckets — every feature the user wants is in
  scope.

After generating the complete questionnaire and **before answering any
question on the user's behalf**, Claude must ask the user to choose a
questionnaire answering mode:

- **Guided full-answer mode** — Claude asks every question and records the
  user's answers. It may present questions in manageable batches, but it
  must not silently fill unanswered questions with defaults.
- **Default-assisted mode** — the user explicitly authorizes Claude to use
  the proposed defaults for unanswered questions; Claude must still ask
  high-impact questions directly. High-impact questions include anything
  affecting the data model, auth/permissions, payments, privacy/compliance,
  security, external API contracts, deployment or irreversible architecture,
  plus any item tagged as a boundary condition or acceptance criterion.

Record the selected mode near the top of `docs/REQUIREMENTS_ANSWERS.md` as
`Questionnaire Answering Mode`, including whether default use was expressly
authorized. If the user selected guided full-answer mode, any later default
must be individually approved by the user or preceded by an explicit switch
to default-assisted mode. Asking only a few key questions and silently
defaulting the rest is forbidden.

After the user answers (or explicitly authorizes defaults), write
`docs/REQUIREMENTS_ANSWERS.md`. Mark each defaulted item with
`(default assumption)` so Codex can see where the gaps are.

Claude does not implement product code in Stage 1 unless the user
explicitly asks.

## Optional Research Gate: codex-autoresearch

`codex-autoresearch` is an optional companion Codex skill, installed from
`leo-lilinxiao/codex-autoresearch`. It is **not** a hard dependency for
this workflow and should not slow down tiny / obvious tasks.

Use it before Stage 2 implementation, or before a high-risk roadmap
slice, when the task involves:

- unfamiliar third-party APIs or SDKs,
- auth, encryption, secrets handling, database migrations, deployment,
  performance, security-sensitive changes,
- LLM provider behavior, eval strategy, prompt safety, or tool-use
  design,
- large dependency upgrades or cross-cutting refactors,
- failing tests whose root cause is unclear,
- optimization work with a measurable metric (latency, coverage,
  type errors, lint count, bundle size, etc.).

Skip it when the slice is straightforward and the PRD/specs already
contain enough concrete implementation detail.

When research is needed, ask Codex to invoke `$codex-autoresearch` with
a narrow goal and a mechanical verification metric. Capture the outcome
in the Task Plan under "Research notes" before editing production code.
The research loop may run foreground or background, but it must respect
the current repo boundary and the task scope.

## Stage 2: Codex Implements

After Claude finishes, ask Codex:

```text
Read docs/codex/00-implementation-handoff.md and implement the first
vertical slice from the generated roadmap.
```

Codex follows the handoff doc:

1. Read context (Trellis workflow, PRD, roadmap, requirements answers,
   kickoff task).
2. Output a `## Task Plan` block (goal / scope / out-of-scope / files /
   risks / verification / acceptance criteria) **before** editing code.
3. For greenfield projects, build the **smallest runnable vertical slice**
   first — request → handler → DB or LLM → response → assertion — before
   layering on features.
4. Implement one focused task. Do not absorb future-roadmap work.
5. Run verification (`npm run lint/typecheck/test/build`, `pytest`,
   `ruff check .`, `mypy .`, or whatever the project ships). Fix in
   scope; report unrelated failures separately.
6. Summarize: what changed, files changed, acceptance status, verification
   results, known issues, next task.

### Stage 2 Execution Modes

These are **modes inside Stage 2**, not extra stages. Do not name them
Stage 2A / Stage 2B.

- **Normal Execution** — default for a focused slice that can reasonably
  finish in one working session. Use the Task Plan, implement, verify, and
  summarize as described above.
- **Long-Run Execution** — use when a slice is likely to exceed one hour,
  spans three or more dependent implementation steps, crosses multiple
  layers (for example UI + API + database), needs interruption recovery, or
  the user explicitly requests an unattended long run.

For Long-Run Execution:

1. Keep Trellis as the source of truth for specs and tasks. Do **not**
   create a second project-management system.
2. Create or maintain a lightweight execution ledger from
   `docs/codex/01-execution-ledger-template.md`, linked to the current
   Trellis task or roadmap slice.
3. Track each atomic work item through implementation, self-review,
   regression verification, and evidence. Evidence can be command output,
   screenshots, build artifacts, or a commit when appropriate; commits are
   not mandatory.
4. Prefer Codex Goal mode for durable long-running execution when available.
   Treat the exact UI/CLI entry point as product-dependent rather than part
   of this skill's stable contract.
5. End with a mandatory final review against the original acceptance
   criteria and full relevant diff before declaring the slice complete.

## Review Mode

When the user asks for a review (rather than an implementation), do not
implement first. Read PRD, specs, the diff, and verification output;
lead with findings by severity.

Output structure (full template in `references/safety-rules.md`):

```markdown
## Review Result
Status: Pass / Pass with concerns / Fail

## Critical / Major / Minor issues
## Scope violations
## Missing acceptance criteria
## Verification (command + result)
## Recommended fix order
```

If the diff lacks tests, the best status is "Pass with concerns" with
the missing verification flagged under Major. Do not silently apply
fixes during review unless the user requests it.

## Hard Rules

### Stage 1 Belongs To Claude (Codex Must Refuse)

The Stage 1 documents below exist in two states:

1. **Scaffolded** — `bootstrap.py` rendered them with `{{name}}` /
   `{{brief}}` / `{{date}}` / `{{language}}` filled and most sections
   marked TBD.
2. **Stage 1 complete** — an interactive Claude Code session ran the
   structured questionnaire with a real human, recorded the user's
   Questionnaire Answering Mode choice before applying defaults, captured
   real answers or expressly authorized defaults, and refined the docs.

**Codex must NEVER move a file from state 1 to state 2.** That includes
"helpfully" filling defaults, "completing the workflow end-to-end",
"unblocking the user when Claude isn't available", and any other
phrasing the user might use to ask Codex to skip the human-in-the-loop
step. Headless self-fill silently destroys the questionnaire — the
single largest reason this workflow exists.

Files Codex must not author or refine:

- `docs/PROJECT_BRIEF.md` (Codex may render the bootstrap scaffold; it
  must not refine TBD sections)
- `docs/REQUIREMENTS_QUESTIONNAIRE.md`
- `docs/REQUIREMENTS_ANSWERS.md`
- `docs/PRD.md`
- `docs/ROADMAP.md`
- `.trellis/spec/*` (any new spec file beyond what Trellis itself ships)
- `.trellis/tasks/001-implementation-kickoff.md`

When the user asks Codex to "test the workflow end-to-end", "run Stage
1 yourself", "fill the questionnaire with defaults for speed",
"Claude isn't available so just do it", or any equivalent, Codex must
**refuse** with this message (translate to the user's language):

> Stage 1 must run in interactive Claude Code, not Codex. The
> structured questionnaire is this workflow's core value, and any
> automated self-fill silently destroys it. To proceed:
>
>     cd <project-path>
>     claude
>
> Then in the Claude Code session say: *"Read
> `docs/claude/00-prd-spec-prompt.md` and run Stage 1."* Come back to
> Codex when `docs/REQUIREMENTS_ANSWERS.md` contains real answers, not
> only `(default assumption)` lines, and I'll start Stage 2.

Codex MAY always:

- run `bootstrap.py` to produce scaffolds;
- read the planning files to report current state to the user;
- start Stage 2 implementation **only after** the Stage 1 completeness
  gate in `docs/codex/00-implementation-handoff.md` passes.

### Do Not Code Too Early

For medium or large projects, do not implement product code until these
exist or are explicitly substituted by equivalent existing files:

- Project Brief
- Requirements Answers (or confirmed default assumptions)
- PRD
- Technical Specs
- Roadmap or task list
- Acceptance Criteria
- Verification Commands

Exceptions:

- the user explicitly requests a throwaway prototype,
- the task is a small independent edit,
- the project already has equivalent docs.

### Safety Boundaries

Before important changes, run `git status`. Prefer a feature branch for
non-trivial work. Do **not**:

- run destructive commands without explicit approval,
- delete user files unless the task requires it,
- edit outside the current repo unless explicitly asked,
- commit secrets or hardcode API keys,
- edit `.env` (create `.env.example` instead),
- add large dependencies without justification,
- delete tests or weaken assertions to pass checks.

For shareable files, use placeholders (`<project-root>`,
`<developer-name>`, `<non-system-drive>`) instead of personal paths or
usernames. Full discipline lives in `references/safety-rules.md`.

### Control Scope

One task at a time. Do not turn one task into a project-wide rewrite
unless the user approves. Do not implement future-roadmap features
inside the current task.

### Don't Block On Assumptions

If an answer is missing, draft an explicit assumption and continue. Stop
only when the missing answer affects safety, cost, legal risk, or
irreversible architecture.

## Optional References

Load these only when the situation calls for them:

- `references/handoff-flow.md` — full per-document field checklists for
  Project Brief / PRD / specs / roadmap, plus Bad/Good spec examples.
- `references/safety-rules.md` — extended safety, Done Checklist, Review
  Mode template.
- `references/llm-spec-checklist.md` — LLM project checklist (provider
  abstraction, prompt templates, guardrails, evals, tests).
- `references/SKILL.zh-CN.md` — Chinese reading version. Codex loads this
  English file as the contract; the Chinese file is for humans.

## Bundled Resources

- `scripts/bootstrap.py` — cross-platform project bootstrap.
- `assets/templates/` — Markdown templates the bootstrap script renders.
- `agents/openai.yaml` — UI metadata for Codex skill chips.

## Publish Safety Gate

Before publishing this skill repository:

- scan for personal absolute paths, local usernames, machine-specific
  tool directories, tokens, API keys, and private project names,
- keep examples generic and replace user-specific values with placeholders,
- ensure `SKILL.md` contains the complete operational workflow (no hidden
  instructions in references),
- keep scripts parameterized via CLI arguments and environment variables,
- run a smoke bootstrap in a temp folder and remove only the verified
  temp folder afterward.
