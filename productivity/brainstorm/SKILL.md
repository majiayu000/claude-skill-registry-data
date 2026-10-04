---
name: epci:brainstorm
description: >-
  Transform vague ideas into structured specifications (CDC) through guided exploration.
  Uses iterative refinement with EMS (Exploration Maturity Score) to progressively clarify requirements.
  Features 4 adaptive personas, divergent/convergent phases, HMW questions, and Perplexity research prompts.
  Generates brief PRD v3.0 and exploration journal. Chains with /spec and /implement.
  Trigger words: brainstorm, explore idea, clarify requirements, vague concept, help me think through.
  Not for: simple Q&A, direct task execution, clear specifications.
user-invocable: true
argument-hint: "<idea> [--quick|--continue <id>|--template <type>]"
allowed-tools: Read, Write, Glob, Grep, Task, AskUserQuestion
---

# Brainstorm - Intelligent Ideation Facilitator

Transform vague ideas into actionable specifications through structured co-exploration.

## Quick Start

```
/brainstorm "add OAuth login to the app"
/brainstorm "improve search performance" --quick
/brainstorm --continue auth-oauth-20260126
/brainstorm "new microservice architecture" --template project
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip EMS calculation between iterations
- 🔴 NEVER generate outputs with EMS < 60 without --force
- 🔴 NEVER skip the BREAKPOINT at framing validation (step-03)
- 🔴 NEVER exceed 10 iterations without user consent
- ✅ ALWAYS start with step-00-init.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS use @ems-evaluator for EMS calculation
- ✅ ALWAYS use breakpoint-system for interactive breakpoints
- ⛔ FORBIDDEN proceeding without brief validation
- 🔵 YOU ARE A PROACTIVE INTELLECTUAL PARTNER

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoints via breakpoint-system
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step or loop condition

## CONTEXT BOUNDARIES:

- IN scope: Ideation, exploration, requirement clarification, brief generation
- OUT scope: Implementation (use /implement), debugging (use /debug), simple Q&A

## Workflow Overview

```
+---------------------------------------------------------------------+
|                    BRAINSTORM WORKFLOW (EMS-driven)                 |
+---------------------------------------------------------------------+
|                                                                     |
|  Step 00: INIT                                                      |
|  +- Parse input (idea, flags)                                       |
|  +- Load project-memory context                                     |
|  +- Launch @Explore in background                                   |
|                                                                     |
|  Step 01: CLARIFY                                                   |
|  +- Assess input clarity (score 0-1)                                |
|  +- Generate clarification questions (if needed)                    |
|  +- BREAKPOINT: Brief validation                                    |
|                                                                     |
|  Step 02: FRAMING                                                   |
|  +- Auto-detect template                                            |
|  +- Generate HMW questions                                          |
|  +- Generate Perplexity prompts                                     |
|  +- Initialize EMS baseline                                         |
|                                                                     |
|  Step 03: BREAKPOINT-FRAMING                                        |
|  +- BREAKPOINT: Validate framing before iterations                  |
|                                                                     |
|  Step 04: ITERATION (LOOP)  <---------------------------------+     |
|  +- Integrate user responses                                  |     |
|  +- Recalculate EMS via @ems-evaluator                        |     |
|  +- Check persona auto-switch                                 |     |
|  +- Check technique suggestion                                |     |
|  +- BREAKPOINT: EMS status + questions                        |     |
|  +- Check phase transition (EMS=50)                           |     |
|  +- Check finalization (EMS>=70)                              |     |
|  +- Loop until finish or max 10 iterations ------------------+      |
|                                                                     |
|  Step 05: BREAKPOINT-FINISH                                         |
|  +- BREAKPOINT: Validate end of exploration                         |
|                                                                     |
|  Step 06: PREVIEW                                                   |
|  +- @planner preview                                                |
|  +- @security-auditor (if auth patterns)                            |
|                                                                     |
|  Step 07: VALIDATE (skip if --quick)                                |
|  +- Section-by-section brief validation                             |
|                                                                     |
|  Step 08: GENERATE                                                  |
|  +- Write brief-{slug}-{date}.md                                    |
|  +- Write journal-{slug}-{date}.md (unless --quick)                 |
|                                                                     |
|  Step 09: REPORT                                                    |
|  +- Calculate complexity routing                                    |
|  +- Execute hook post-brainstorm                                    |
|  +- Display completion summary                                      |
|                                                                     |
+---------------------------------------------------------------------+
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--template [type]` | auto | feature, audit, project, research, decision, problem, strategy |
| `--quick` | off | Simplified flow (3 iter max, report only) |
| `--turbo` | off | Use @clarifier (Haiku) for faster responses |
| `--party` | off | Multi-persona mode (5 voices) via @party-orchestrator |
| `--panel` | off | Expert panel (5 dev experts) via @expert-panel |
| `--no-hmw` | off | Skip HMW question generation |
| `--no-security` | off | Skip @security-auditor |
| `--no-clarify` | off | Skip input clarification |
| `--continue [id]` | - | Resume existing session |

## Steps

| Step | Name | Description | Skippable |
|------|------|-------------|-----------|
| 00 | init | Parse input, load context, launch @Explore | No |
| 01 | clarify | Clarification questions, brief validation | --no-clarify |
| 02 | framing | Template, HMW, Perplexity, EMS baseline | No |
| 03 | breakpoint-framing | Validate framing before iterations | No |
| 04 | iteration | Main loop: EMS, personas, techniques | No |
| 05 | breakpoint-finish | Validate end of exploration | No |
| 06 | preview | @planner preview, @security-auditor | No |
| 07 | validate | Section-by-section validation | --quick |
| 08 | generate | Write brief and journal files | No |
| 09 | report | Routing, hook, completion summary | No |

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-01-clarify.md](steps/step-01-clarify.md) — Clarification
- [steps/step-02-framing.md](steps/step-02-framing.md) — Framing
- [steps/step-03-breakpoint-framing.md](steps/step-03-breakpoint-framing.md) — Framing validation
- [steps/step-04-iteration.md](steps/step-04-iteration.md) — Iteration loop
- [steps/step-05-breakpoint-finish.md](steps/step-05-breakpoint-finish.md) — Finish validation
- [steps/step-06-preview.md](steps/step-06-preview.md) — Preview
- [steps/step-07-validate.md](steps/step-07-validate.md) — Brief validation
- [steps/step-08-generate.md](steps/step-08-generate.md) — File generation
- [steps/step-09-report.md](steps/step-09-report.md) — Report

## Reference Files

- [references/ems-system.md](references/ems-system.md) — EMS with objective anchors
- [references/personas.md](references/personas.md) — 4 personas and auto-switch rules
- [references/brief-format.md](references/brief-format.md) — PRD v3.0 output template
- [references/journal-format.md](references/journal-format.md) — Exploration journal template

## Shared Components Used

- `epci:project-memory` — Load context, patterns, preferences
- `epci:clarification-engine` — Smart clarification questions
- `epci:breakpoint-system` — All interactive breakpoints
- `epci:complexity-calculator` — Final routing to /spec or /quick

## Subagents

| Agent | Model | Trigger |
|-------|-------|---------|
| `@Explore` | - | Always at init (background) |
| `@ems-evaluator` | Haiku | Each iteration |
| `@technique-advisor` | Haiku | Weak axes detected |
| `@clarifier` | Haiku | --turbo mode |
| `@planner` | Sonnet | Preview at finalization |
| `@security-auditor` | Opus | Auth patterns detected |
| `@party-orchestrator` | Sonnet | --party mode |
| `@expert-panel` | Sonnet | --panel mode |

## EMS System (Summary)

| Axis | Weight | Question |
|------|--------|----------|
| Clarity | 25% | Is the subject well defined? |
| Depth | 25% | Have we dug deep enough? |
| Coverage | 20% | Have we explored all angles? |
| Decisions | 20% | Have we made progress? |
| Actionability | 10% | Can we act concretely? |

**Thresholds**: 0-29 Beginning | 30-59 Developing | 60-89 Mature | 90-100 Complete

See [references/ems-system.md](references/ems-system.md) for objective anchors.

## Personas (Summary)

| Persona | Icon | When Activated |
|---------|------|----------------|
| Maieuticien | [?] | Exploration, unclear topics |
| Sparring | [!] | Unsubstantiated claims |
| Architecte | [#] | Complex topics, synthesis (DEFAULT) |
| Pragmatique | [>] | Stagnation, decisions needed |

See [references/personas.md](references/personas.md) for complete specifications.

## Session Commands

| Command | Action |
|---------|--------|
| `continue` | Next iteration |
| `dive [topic]` | Deep dive on specific point |
| `pivot` | Reorient toward emerging subject |
| `finish` | Generate outputs |
| `checkpoint` | Save for later resumption |
| `status` | Display complete state |
| `mode [name]` | Switch persona |

## Constraints

| Constraint | Value |
|------------|-------|
| Max iterations | 10 |
| EMS minimum for finish | 60 (70 recommended) |
| Questions per iteration | 3 max |
| Techniques per session | 5 max |

## Error Handling

| Error | Resolution |
|-------|------------|
| @Explore timeout | Continue with partial context |
| @ems-evaluator failure | Manual estimation |
| EMS stagnation | Propose pivot or technique |
| Brief rejected x 3 | Reformulate topic |

## Storage

```
.claude/state/sessions/
  brainstorm-{slug}-{timestamp}.json

docs/briefs/{slug}/
  brief-{slug}-{date}.md
  journal-{slug}-{date}.md
```

## Limitations

This skill does NOT:
- Execute tasks (it ideates about them)
- Replace project management tools
- Generate code or technical implementations
- Work without user engagement
