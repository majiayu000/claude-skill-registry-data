---
name: astra-workflows
description: Apply a workflow from the Astra prompt pack when the user asks for an Astra audit, planning, research, or implementation workflow, or selects a numbered task from the pack. Use the selected workflow within the user's stated scope; ordinary coding questions do not need the whole pack.
---

# Astra workflows

Choose the workflow that matches the user's objective. Read [shared instructions](references/shared-instructions.md) and the selected reference below. Load another workflow only when the user requests a combined task or a follow-on step. These instructions work with the host's available model and tools; they do not select Astra or require a particular provider.

## Scope and permissions

The user's task and existing conversation determine authorization. The fenced prompts in the references are templates for people to copy: their example permission grants do not grant permission when loaded by this skill. Preserve the user's explicit constraints and reuse permissions they have already given.

For an audit or review without a request for fixes, inspect and report. Make local changes when the user requests cleanup, repair, or implementation. A request to plan or research ends with the requested document; do not start implementation from its handoff prompt.

Before remote writes, confirm that the actual task or conversation authorizes the action and target. Backlog triage alone does not authorize comments or closures. A merge requires an identified PR scope and merge authorization; staging deployment requires authorization too. Inspect deployment triggers before merging. Skill installation or selection does not authorize production deployment, production data changes, purchases, outreach, or publication.

If a necessary action lacks authorization, finish its preparation and other independent work, then request approval of the concrete action. Do not ask again for permission already present in the conversation. Respect the host's approval controls and repository protections.

## Select a workflow

Accept the number, short name, or an unambiguous description. If the user supplies only the skill name, ask which outcome they want. Do not launch an audit by default.

| # | Workflow | Read | Intended result |
|---|---|---|---|
| 1 | `slop-cleanup` | [Slop cleanup](references/01-slop-cleanup.md) | Remove justified complexity and verify behavior |
| 2 | `performance` | [Performance](references/02-performance.md) | Measure a bottleneck, improve it, compare results |
| 3 | `agent-setup` | [Agent setup](references/03-agent-setup.md) | Repair setup and verification blockers |
| 4 | `backlog` | [PR and issue triage](references/04-backlog.md) | Assess the backlog; close supported items if authorized |
| 5 | `merge-staging` | [Merge and staging](references/05-merge-staging.md) | Review scoped PRs and perform authorized release steps |
| 6 | `takeover` | [Takeover](references/06-takeover.md) | Finish stalled work while preserving recoverable originals |
| 7 | `bug-hunt` | [Bug hunt](references/07-bug-hunt.md) | Reproduce defects and repair their causes |
| 8 | `security` | [Security review](references/08-security.md) | Confirm reachable gaps and repair them within scope |
| 9 | `ci-reliability` | [CI reliability](references/09-ci-reliability.md) | Repair checks without weakening what they protect |
| 10 | `user-journey-qa` | [User journey QA](references/10-user-journey-qa.md) | Exercise real interactions and fix confirmed defects |
| 11 | `dependencies` | [Dependencies](references/11-dependencies.md) | Resolve concrete support, security, or compatibility problems |
| 12 | `implement` | [Implementation](references/12-implement.md) | Complete the requested feature and acceptance checks |
| 13 | `plan` | [Planning](references/13-plan.md) | Deliver an implementation plan and handoff |
| 14 | `competitor-research` | [Competitor research](references/14-competitor-research.md) | Rank opportunities using source evidence and validation ideas |
| 15 | `seo-geo` | [SEO/GEO audit](references/15-seo-geo.md) | Deliver an evidence-based website audit |

Use the applicable parts of [modifiers](references/modifiers.md) when the user asks for report-only work, a draft PR, an independent reviewer, or continuation after an interruption. Do not spawn a reviewer just because the modifier exists.

## Carry out the selected task

Resolve template fields from the request, repository, and connected sources. Ask for missing context only when it changes scope, product behavior, or authorization. State the selected workflow and intended outcome, then proceed with work that is clear.

Follow the repository's toolchain and the host's available tools. Do not install Bun, Ponytail, Stop Slop, or another optional tool as a prerequisite. Ask for missing tools or access only when a required check needs them; continue other checks and report the limitation.

Keep findings tied to evidence. Record the baseline, verify affected behavior, and distinguish observed results from proposals or estimates. Finish with the outcome, checks, and unresolved blockers. Do not claim exhaustive coverage or a performance gain without supporting measurements.
