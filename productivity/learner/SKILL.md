---
name: learner
type: workflow
description: "Turns real agent failures, repeated prompts, team-specific workflows, and durable project lessons into better SDD skills or memory entries. Use when the user asks to create/update/refine skills, extract reusable lessons, improve skill routing, encode team process, or save patterns for future sessions."
argument-hint: "[session summary, failure mode, repeated prompt, or skill improvement request]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
user-invocable: true
effort: 3
when_to_use: "Use when a lesson should become durable: after repeated corrections, wrong skill routing, repeated long prompts, team-specific process discovery, or a complex session worth converting into a skill or memory entry."
---

# Learner

Convert real SDD usage into durable operating knowledge.

Use this workflow to decide whether a lesson belongs in:

- an existing skill,
- a new skill,
- `.claude/memory/annotations.md`,
- another Tier 2 memory file,
- or no durable artifact.

## Source Principles

This workflow adopts the Agent Skills guidance that durable skills come from
real expertise, project artifacts, execution traces, and repeated refinement.
Skills should capture team-specific process and failure modes, not generic
best practices or deterministic glue better handled by scripts, hooks, or MCP.

## Extraction Gate

Create or modify a skill only when at least one signal is present:

- Agent made a wrong choice despite a correct prompt.
- Existing skill fired but failed its mission.
- Needed skill did not fire because `description` was weak or absent.
- A teammate/user wrote the same long prompt, plan, or checklist a second time.
- Session repeated a costly investigation, setup, verification, or handoff loop.
- User corrected a project convention, team preference, or non-obvious edge case.
- Internal process, internal system, or proprietary data pattern must be reused.

Do not create a skill for:

- General advice the model already knows.
- One-off code snippets.
- Secrets, credentials, or environment-specific auth hacks.
- Simple deterministic checks better implemented as hooks, scripts, tests, or MCP.
- Large copied docs without a clear load condition.

## Decision

Classify the lesson before editing:

| Lesson type | Target |
| --- | --- |
| Existing workflow missed a rule, edge case, or output shape | Update that skill body |
| Existing skill should have fired but did not | Tighten that skill `description` |
| Repeated team-specific process forms a coherent unit | Create or update a skill |
| Non-obvious caveat tied to a service/library/repo area | Use `annotate` memory |
| Broad preference or project operating rule | Update the right Tier 2 memory/doc |
| Deterministic repeated operation | Prefer tested script/hook/MCP; skill only orchestrates when needed |

Prefer updating an existing skill over adding a new one when the lesson fits an
existing coherent workflow.

## Workflow

1. Gather evidence:
   - original prompt or task,
   - correction or failure mode,
   - first point where the agent went wrong,
   - skills that fired or failed to fire,
   - files, commands, traces, review comments, or user preferences involved.
2. Choose the smallest durable target using the Decision table.
3. Edit with progressive disclosure:
   - keep `SKILL.md` under 500 lines when practical,
   - keep only always-needed instructions in `SKILL.md`,
   - move long examples, schemas, or domain references into `references/`,
   - state exactly when to read each reference file.
4. Tune invocation:
   - put trigger phrases and scope in `description`,
   - add exclusions when false positives are likely,
   - avoid relying on body-only "when to use" text for activation.
5. Preserve SDD gates:
   - do not weaken `using-sdd`, permissions, hooks, or source-of-truth rules,
   - route spec, plan, code, review, and release changes through their owning skills.
6. Validate:
   - run `powershell -ExecutionPolicy Bypass -File scripts\validate-skills.ps1`,
   - run `node scripts\validate-readme-sync.js` if counts or README inventory changed,
   - run `node scripts\harness-audit.js --compact` for routing, hook, or harness changes.

## Skill Edit Rules

- Add what the agent lacks; cut what generic model knowledge already covers.
- Prefer procedures over declarations.
- Use defaults, not broad menus of equal options.
- Make fragile operations prescriptive; leave flexible judgment where multiple approaches are valid.
- Add concrete gotchas where the agent is likely to make the wrong assumption.
- Keep bundled scripts deterministic and tested.
- Treat each skill like a function: one coherent responsibility, composable with other skills.

## New Skill Template

Use this shape when a new SDD skill is justified:

````markdown
---
name: short-action-name
type: workflow
description: "What this skill does. Use when <specific trigger phrases, task contexts, and boundaries>."
argument-hint: "[expected input]"
user-invocable: true
allowed-tools: Read, Glob, Grep
effort: 2
when_to_use: "One sentence matching the description scope for SDD docs and humans."
---

# Purpose

State the reusable team-specific capability.

## Workflow

1. Do the first required action.
2. Make the context-dependent decision.
3. Verify with a concrete check.

## Gotchas

- Add only non-obvious failure modes discovered from real use.

## Output

Specify the exact artifact or response shape when consistency matters.
````

## Completion Output

Report:

- artifact changed or created,
- evidence source that justified it,
- validation commands and results,
- remaining skill debt or telemetry gap.
