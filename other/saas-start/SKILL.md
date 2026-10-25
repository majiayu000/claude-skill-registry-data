---
name: saas-start
description: "Guides a first-time user through onboarding and picks the right workflow. Use when the user is new, just cloned or installed the studio, has no idea or engine yet, asks where to begin, or wants to bring in an existing product."
argument-hint: "[no arguments]"
user-invocable: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Bash(bash .claude/scripts/project-state.sh*), Bash(bash .claude/scripts/set-stage.sh *), Bash(bash .claude/scripts/config-set.sh *)
model: sonnet
---

# Guided Onboarding

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

The entry point for a new user. It assumes no product idea, no tech stack and no prior setup: it reads
the project, asks where the user is starting from, shows what it assumes about the project, and
names the one next step. It never runs that step itself.

It writes these settings to `project.yaml`, all through helpers, and only after an explicit yes:
`project.stage` (with its legacy mirror `production/stage.txt`), `modes.rigor` and
`modes.automation`. It never writes `modes.review_mode` or `production/review-mode.txt`, and none
of the other knobs rigor fronts (`modes.workflow`, `docs.density`, `qa.level`,
`modes.story_granularity`, `team.size`): a written value pins that knob over the rigor expansion,
and a mirror file outranks it.

Ask with the question tool. Without one, list the options numbered and end your turn to wait. The
question is the last thing in the reply: no path, note or advice after it. A skipped or dismissed
question is not an answer: ask again in plain text.

The questions in Phases 2, 4 and 5 shape the project, so they are asked in every automation mode.
The engine is not one of them: `/saas-setup-stack` chooses it. Phase 6's last question follows a
`modes.automation` already in `project.yaml`, per `.claude/docs/automation-modes.md`; with none
set, ask it.

## Phase 1: Read the project

Run `bash .claude/scripts/project-state.sh` and keep its rows. Do not show them yet; they check
the user's answer in Phase 2.

| Row | Use |
|---|---|
| `engine`, `code_root`, `source_files` | Is an engine set, and how much code is there. `source_files` of `unknown` means the code root could not be found: say that, never "no code" |
| `concept` | `design/prd/product-concept.md` or `design/product-brief.md` exists |
| `prd_files`, `adr` | Design documents and architecture decisions on disk (they set the stage in Phase 4) |
| `prototype`, `sprint`, `milestone`, `story` | Other existing work |
| `origin_url` | Contains `saas-studio-template`, matched case-insensitively: the clone still points at the template repo, so a push or pull request would go there. A fork under another owner is the user's own |
| `stage` | The stage already recorded, if any |

Ignore `phase_inferred`: it guesses from file counts, and a project with code but no design
documents is not in Production. If the helper fails, say so and read the same facts by hand
(engine in `project.yaml`, the two concept files, the code root's files, `design/prd/`).

The helper does not report rigor or automation. Read `project.yaml`, if it exists, and note
whether `modes.rigor` and `modes.automation` are set: a set value is kept, and its question is
not asked (Phases 4 and 5).

**Returning user** (an engine is set and `concept` is present): ask nothing. Say the engine, the
concept or brief found, and the review mode: `modes.review_mode` if set, otherwise the one
`modes.rigor` implies (`minimal` → `solo`, `standard` → `lean`, `full` → `full`). Suggest `/saas-help` for the next step, add the
template-remote note if it applies, and stop.

## Phase 2: Ask where the user is

Ask with the question tool (Render in Portuguese for PT-BR sessions, while processing internally in English):
- PT-BR prompt: "Bem-vindo! De onde você está começando o seu produto SaaS?"
  - `A) Nenhuma ideia ainda`: sem conceito de produto; explorar e encontrar o que criar.
  - `B) Ideia inicial`: um tema, nicho ou ideia vaga ("um analisador de faturas com IA").
  - `C) Conceito claro`: ideia central e modelo de negócios definidos, nada escrito ainda.
  - `D) Projeto existente`: código, documentação, protótipo ou planos já existentes.
- EN prompt: "Welcome! Where are you starting from with your SaaS product?"
  - `A) No idea yet`: no product concept; explore and find what to make.
  - `B) Vague idea`: a theme, feeling or niche ("an AI invoice parser").
  - `C) Clear concept`: the core idea and business model are known, nothing is written down yet.
  - `D) Existing work`: design documents, prototypes, code or plans already exist.

Wait for the answer. If it contradicts Phase 1, say what you found once and ask again: D on an
empty project ("this looks like a fresh template; would A or B fit better?"), or A with code on
disk ("I found code in `[code_root]`; did you mean D?"). If no option fits, let the user describe
their situation and route from that.

## Phase 3: Route

Name the immediate next step only. The full path waits for Phase 6, after the rigor is known.

- **A, no idea:** starting from zero is fine. `/saas-brainstorm open` explores freely; `/saas-brainstorm
  [hint]` starts from a word or theme. Next step: `/saas-brainstorm open`, or a hint if one comes to
  mind. Describe it as "turns no idea into a written design the next step builds from"; how long
  that design is depends on the rigor, so leave that for Phase 6.
- **B, vague idea:** ask for the idea in a few words, take it as it is, and name
  `/saas-brainstorm [their words]`.
- **C, clear concept:** ask for the concept in one sentence (product domain and core workflow), as plain
  text. Then ask: "How would you like to proceed?" Options: `Formalize it first` (`/saas-brainstorm
  [concept]` writes it down) / `Jump straight in` (`/saas-setup-stack` now, write the design after).
  The next step is their pick.
- **D, existing work:** say what Phase 1 found ("N source files under `[code_root]`, N design
  documents, engine [X / not set]"). Next step: `/saas-setup-stack` when no engine is set and there is
  no more than a concept; otherwise `/saas-project-stage-detect`.

Then say: "I'll lay out the full path in a moment."

## Phase 4: Show what you assume, then save it

Work out two values.

**Stage.** Paths A, B and C: `Concept`. Path D, from the Phase 1 rows:

| On disk | Stage |
|---|---|
| no stack, or nothing beyond a concept (`prd_files` 0) | `Concept` |
| `prd_files` 1 or more, `adr` 0 | `Systems Design` |
| `adr` 1 or more | `Technical Setup` |

**Rigor.** If `modes.rigor` is already set in `project.yaml`, keep it and say so. Otherwise infer
it from what the user said in Phases 2 and 3, using the signals in
`.claude/docs/settings-guidance.md` §3:

| The user's words mention | Rigor |
|---|---|
| enterprise SaaS, multi-tenant portal, workflow automation, complex billing, real-time collaboration, many integrations | `full` |
| release, commercial, B2B SaaS, one clear core workflow | `standard` |
| hackathon, weekend, prototype, first SaaS, weekend MVP, small, just trying | `minimal` |
| nothing above, or no idea yet | `minimal` (the default) |

A path B hint is still a description: "an enterprise multi-tenant analytics platform" is `full`.

Show the card:

```
What I'll set up
  Stage:  [stage]  ([why, from what was found or picked])
  Rigor:  [value]  ([why, in the user's words] | already set)
          minimal: short brief, coarse stories, tests optional; about 4 steps to code
          standard: about 8 design documents before code; standard QA evidence
          full: everything in standard plus validation builds; evidence everywhere
  /saas-settings changes either of these any time.
```

Then ask with the question tool: "Save these to `project.yaml` (and the stage to
`production/stage.txt`)?" Options: `Save them` / `Don't save`. Ask no question about the rigor
itself: the card shows it, and `/saas-settings` changes it.

- **Save them:** run `bash .claude/scripts/set-stage.sh "[stage]"`, then, only when rigor was not
  already set, `bash .claude/scripts/config-set.sh modes.rigor [value]`. Check the read-back rows
  match. Say: "Saved. Rigor `[value]` sets six other settings; `/saas-settings` shows them and changes
  any of them."
- **Don't save**, or anything other than an explicit yes: write nothing, keep the values for this
  run, and say they were not saved.

If a helper exits non-zero, show its output, say which setting was not written, and go on with the
value for this run.

## Phase 5: Ask how much to confirm

If `modes.automation` is already set, say "Automation is `[value]`" and go on. Otherwise ask:
"Last one: how much should I confirm with you as we work?" Options:
- `Guided (Recommended)`: I decide small things and still stop for big ones (scope changes,
  deletions, schema changes).
- `Collaborative`: I ask before each significant step and show drafts before writing.
- `Autonomous`: I proceed and log decisions, stopping only for the always-ask categories. Fastest,
  most tokens.

Mapping: `Guided` → `guided`, `Collaborative` → `collaborative`, `Autonomous` → `autonomous`. The
pick is the consent to write it: run `bash .claude/scripts/config-set.sh modes.automation [value]`,
unless the Phase 4 save was declined (then say it was not saved).

## Phase 6: Show the path

Say: "Here's your path at rigor `[value]`. Every skill still runs at any rigor; rigor changes
what's required, not what's allowed."

The path starts with the step Phase 3 named. When that was `/saas-brainstorm` (paths A and B, and C's
`Formalize it first`), list `/saas-brainstorm` first and `/saas-setup-stack` second: each runs without the
other.

**`minimal`: 4 steps to running code**
1. `/saas-setup-stack`: choose and configure the engine
2. `/saas-brainstorm`: write the one-page `design/product-brief.md`
3. `/saas-create-stories`: turn the brief's MVP list into stories (no epics or sprint plan needed)
4. `/saas-dev-story`: the first line of production code

**`standard`**
- Concept: `/saas-setup-stack` → `/saas-brainstorm` → `/saas-prototype` → `/saas-design-tokens` → `/saas-gate-check`
- Systems Design: `/saas-map-features` → `/saas-design-system` (once per system) → `/saas-review-all-prds` →
  `/saas-gate-check`
- Architecture: `/saas-create-architecture` → `/saas-architecture-decision` (once per decision) →
  `/saas-create-control-manifest` → `/saas-architecture-review` → `/saas-test-setup` → `/saas-ux-design`
  (accessibility and interaction patterns) → `/saas-gate-check`
- Pre-Production: `/saas-ux-design` (App Shell and key views) → `/saas-create-epics` → `/saas-create-stories` →
  `/saas-sprint-plan` → `/saas-gate-check`
- Production: `/saas-dev-story`

Each `/saas-gate-check` moves the project one stage, and only when it passes.

**`full`:** everything in `standard`, plus `/saas-vertical-slice` and `/saas-usability-test` in
Pre-Production and `/saas-design-review` after each PRD.

**Path D with existing work** (stage `Systems Design` or later, or code on disk) gets this instead.
Print only the steps that apply, and for the brief only the one source that applies. At `minimal`:
1. `/saas-project-stage-detect`: what stage the project is at and what is missing
2. `/saas-adopt`: whether the existing files are in the format the skills read
3. `/saas-setup-stack`: only when no engine is set; leave it out when `engine` names one
4. The brief, only if `concept` is absent: `/saas-reverse-document design [code_root]` when the code
   root holds 10 or more source files (it writes the brief from the codebase), and then do not mention
   `/saas-brainstorm` at all; `/saas-brainstorm` only when it holds fewer

At `standard` and `full`, steps 1 to 3, then `/saas-design-system retrofit [path]`,
`/saas-architecture-decision retrofit [path]`, `/saas-architecture-review` and `/saas-gate-check`.

Present `minimal` as the documented floor, not a lesser mode, and name its trade once: no PRDs, so
design problems show up in code.

If `origin_url` pointed at the template repo, add: "Your clone's `origin` still points at the
SAAS_STUDIO template repo, so a push or pull request would go there. When you're ready, run
`git remote rename origin template`, then `git remote add origin <your repo URL>`. `UPGRADING.md`
pulls updates from `template`; skip its own `git remote add template` step, since that remote now
exists." Suggest it; do not run it.

Ask: "Would you like to start with [first step]?" Options: `Yes, start with [first step]` /
`Something else first`. Either answer leads to Phase 7, never to running the step.

## Phase 7: Hand off

Respond with exactly one line: "Type `[skill]` to begin." Do not start that skill or call the
skill tool for it, even after a yes: the user types it. If they picked something else, name the skill for that instead, the same
way.

Verdict: **COMPLETE**, the user is oriented and handed off. If the user stopped before Phase 7,
say which settings were saved and which were not.
