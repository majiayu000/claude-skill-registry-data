---
name: infra-kit.workflow
description: Turn an infra ticket into a lightweight spec, implementation plan, task list, and implementation notes (with optional Confluence-ready output).
---

# Infra Kit

Use this skill to run a repeatable workflow from an incoming ticket (Jira/GitHub/Slack/Email) to:

- a clear problem statement and acceptance criteria
- an implementation plan with rollout/rollback and verification
- an executable task list
- implementation notes and a copy/paste Confluence summary

This framework focuses on infra delivery artifacts that are easy to review and operate.

For the end-to-end mapping across skills, see `docs/infras-kit/flow.md`.

## Output Rules

- Write the deliverables to Markdown files in the repo (not only chat output).
- Prefer `docs/infras-kit/work-items/<id>-<slug>/`.
- Keep docs skimmable. Push deep details into `implementation-notes.md`.

## Quick Start

1. Create a work-item directory and starter files:

```bash
bash infras-kit-plugin/skills/infra-kit.workflow/scripts/new-work-item.sh "<short title>" \
  --id "<TICKET-ID>" \
  --link "<ticket url>"
```

2. Fill in `ticket.md`, then generate `plan.md` and `tasks.md`.
3. Execute tasks, using domain skills for the actual work:

- use `infra-kit.domain.iac` for Terraform/Terragrunt changes
- use `infra-kit.domain.helm` for chart work
- use `infra-kit.domain.k8s-doctor` for runtime debugging
- use `infra-kit.domain.github` for repo and CI/CD changes
- use `infra-kit.workflow.verify` to record verification evidence and “definition of done”
- use `infra-kit.workflow.review` to prepare PRs and handle review feedback
- use `infra-kit.workflow.audit` to review before merge/release

Note: skill names were renamed. Use `infra-kit.workflow.*` for workflow skills and `infra-kit.domain.*` for domain skills.

## Workflow

This workflow is intentionally iterative. If you discover new unknowns mid-way, add them as
`[NEEDS CLARIFICATION: ...]`, loop back, and update the upstream artifact instead of guessing.

1. **Intake (ticket.md)**
   - restate the problem and intended outcome
   - list acceptance criteria and explicit non-goals
   - capture constraints (cloud, regions, compliance, timelines)
   - label unknowns as `[NEEDS CLARIFICATION: ...]`
   - gate:
     - if any `[NEEDS CLARIFICATION]` remain, ask targeted questions and stop
2. **Spec (spec.md)**
   - translate ticket into an infra-focused spec: desired behavior, SLO/SLA impact, security boundaries
   - define “done” in testable terms
   - carry forward unknowns; do not “resolve” by guessing
   - gate:
     - if any `[NEEDS CLARIFICATION]` remain, ask targeted questions and stop
3. **Plan (plan.md)**
   - approach, risks, dependencies
   - rollout steps and explicit rollback
   - verification commands and expected signals
   - operational ownership: alerts/runbooks, cost notes
   - gate:
     - if any `[NEEDS CLARIFICATION]` remain, ask targeted questions and stop
4. **Tasks (tasks.md)**
    - produce a checklist with small steps
    - tag each task with the intended skill (e.g., `[infra-kit.domain.iac]`, `[infra-kit.domain.helm]`)
   - mark parallelizable tasks with `[P]`
   - include a short readiness check:
     - are tasks unblocked, verifiable, and do they map back to acceptance criteria?
5. **Implement (implementation-notes.md)**
   - record what changed, gotchas, and final verification outputs
6. **Report (confluence.md)**
   - write a concise update suitable for Confluence/Jira comment

## Interaction Pattern (Make It Less Step-By-Step)

At the end of each phase, always do these two things in chat:

1. **State the single best next step** (one action, not a menu).
2. **List what input is required** to proceed (questions or required confirmations).

If the user explicitly wants an exploratory spike, allow proceeding with labeled assumptions:

- Mark them as `[ASSUMPTION: ...]` and keep them in the doc so they can be revisited.
- Still prefer the smallest test to validate assumptions early.

## Guardrails

- Don’t invent requirements. Ask when unknown.
- Don’t propose destructive rollouts without a rollback.
- Keep “plan” separate from “implementation”; avoid code dumps in `plan.md`.
 - If you must proceed with uncertainty, label it as `[ASSUMPTION: ...]`.
 - Don’t stage/commit generated docs unless the user explicitly asks.

## Template Locations

- `docs/infras-kit/work-items/<id>-<slug>/ticket.md`
- `docs/infras-kit/work-items/<id>-<slug>/spec.md`
- `docs/infras-kit/work-items/<id>-<slug>/plan.md`
- `docs/infras-kit/work-items/<id>-<slug>/tasks.md`
- `docs/infras-kit/work-items/<id>-<slug>/implementation-notes.md`
- `docs/infras-kit/work-items/<id>-<slug>/confluence.md`
