---
name: plan-first-execution
description: Use when the user asks to write a plan before doing work, start in plan mode, produce an implementation plan, define review gates, choose review strength, or decide how a plan should be checked before execution.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/plan-first-execution/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/plan-first-execution/SKILL.md`
> Source of truth: `registry/skills/plan-first-execution/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Plan-First Execution

Use this skill before arbitrary work only when the user explicitly asks for a plan, a plan-mode start, a written plan document, a review gate, or a plan-to-execution handoff.

Do not use it for trivial one-command answers. Do not keep planning once the user has moved into implementation.

## Workflow

1. Classify the plan scope:
   - `micro`: one file, one command, or one small behavior fix.
   - `standard`: normal feature, repo maintenance batch, project setup, or documentation batch.
   - `high-risk`: auth, secrets, data migration, destructive filesystem work, public push, production deploy, billing, security, or broad refactor.
2. Produce the smallest plan that is still executable.
3. Include a review decision before execution:
   - State whether review is required, recommended, or unnecessary.
   - Pick one review strength from `Review Strengths`.
   - Name the review channel.
4. Mark the handoff boundary:
   - `Stop after plan`: when the user asked only for a plan.
   - `Proceed after review`: when the user requested a review gate.
   - `Proceed automatically`: when the user explicitly wants yolo execution and no blocker exists.

## Required Plan Items

Every plan must include:

- objective
- scope and non-goals
- current evidence or assumptions
- affected files, systems, or accounts
- execution steps
- verification steps
- rollback or recovery path
- review decision
- commit or handoff boundary, if repo work is involved

## Optional Plan Items

Add only when relevant:

- user-visible behavior changes
- data model, schema, or migration notes
- security, privacy, secret, or credential handling
- browser/account automation boundary
- local service, daemon, or port allocation
- deployment or public publishing boundary
- subagent ownership map
- test matrix by platform or browser
- documentation deliverables
- open questions that materially affect risk

## Plan Template

```md
# Plan: <task name>

## Objective
<one or two sentences>

## Scope
- In scope:
- Out of scope:

## Evidence and Assumptions
- Evidence:
- Assumptions:

## Affected Surfaces
- Files:
- Services/accounts:
- Local runtime/ports:

## Steps
1. <step>
2. <step>
3. <step>

## Verification
- <smallest high-signal check>
- <expanded check if needed>

## Recovery
- <reversible fallback or restore point>

## Review Gate
- Required: yes/no/recommended
- Strength: light/standard/strict/external
- Channel: self-check/subagent/codex-review/domain-skill/manual-user-gate

## Handoff
- Stop after plan / proceed after review / proceed automatically
```

## Review Strengths

| Strength | Use when | Channels |
| --- | --- | --- |
| light | Low-risk edits, small docs, simple config, no secrets or deploy | self-check, targeted diff read, smallest command |
| standard | Normal code changes, repo setup, workflow docs, user-facing UI | self-check plus tests, one reviewer subagent, browser or smoke check when UI/runtime is involved |
| strict | Broad refactor, auth, secrets, migrations, destructive-looking file operations, public push, production-like deploy | dedicated reviewer subagent, `codex review --uncommitted` when available, security/privacy checklist, explicit user gate |
| external | Governance, architecture, audit, compliance, or high-impact public artifact | packeted review request, external-audit-orchestrator when available, user-controlled approval before mutation |

## Review Channels

- `self-check`: reread plan against request, repo state, and local instructions.
- `subagent`: use a bounded reviewer with read-only scope and clear files/responsibility.
- `codex-review`: run `codex review --uncommitted` for code diffs when the local CLI supports it.
- `domain-skill`: use a specific skill such as `frontend-design`, `security-threat-model`, `readme-quality`, or `ai-first-readiness-review`.
- `manual-user-gate`: stop and ask the user when risk, account state, irreversible action, or policy boundary requires it.

## Common Mistakes

- Writing a roadmap instead of an executable plan.
- Omitting verification or rollback.
- Treating uncommitted user changes as disposable.
- Picking a strict review for every task; excessive review is a delivery risk.
- Continuing implementation when the user asked only for a plan.
