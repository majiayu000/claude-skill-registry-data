---
name: model-release
description: "Releases a model version: checks approvals, tags code, data and parameters, updates the registry and writes release notes."
---
<!-- Generated from .claude/skills/model-release/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /model-release — Model Release

**Category:** Governance · **Primary agent:** `project-planning-specialist`

Releases a model version: checks approvals, tags code, data and parameters, updates the registry and writes release notes.

Arguments: whatever the user wrote after the command name.

## Purpose
Release a model version for use: verify that validation, the model-risk decision, the model card and a reproducible package are in place; tag code, data vintage and parameters with hashes; write release notes; update the registry; and notify users. For lego models, the manifest must check cleanly with no stale bricks. The output is a traceable release that anyone can reproduce.

**Use it when** an approved model or model change goes into production use.

**Do not use it when** approval has not been given (`/model-risk-review`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Validation report
   - Model risk decision
   - Model card
   - Replication package
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `project-planning-specialist` — primary agent; coordinates the work and integrates results
- `mlops-engineer` — Engineers MLOps for models
- `reproducibility-engineer` — Guarantees reproducibility
- `model-risk-governance-specialist` — Defines model risk levels and validation depth, enforces builder-validator independence, governs AI/LLM use and recommends release or block

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Workflow
1. Verify approvals: validation, model risk decision, model card, replication
2. Tag code, data vintage and parameter files; record hashes in the registry
3. Write release notes with changes and known limitations
   - Include changes in outputs relative to the previous version
4. Update `production/model-registry.md`; notify users per communication plan
5. If the model has a lego manifest, require a passing `/lego-check`, no stale bricks, and record the manifest revision in the release notes

## Checkpoints with the user
- Before tagging: confirm the version number and scope
- Before notification: confirm release notes

## Common pitfalls
- Releasing without a recorded data vintage
- Release notes that omit output changes
- Stale bricks shipped as validated

## Output
`production/releases/<model>-<version>.md`

The release record lists approvals, tags and hashes, changes, output differences from the previous version, limitations, the manifest revision for lego models, and notifications sent.

## Gate / verdict
- No release without a model-risk approval and a reproducible package
- Output differences from the previous version are documented

## Suggested next steps
- `/retrospective`
