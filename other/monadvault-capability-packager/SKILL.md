---
name: monadvault-capability-packager
description: "Create, audit, improve, or package repeated Steward workflows as focused MonadVault capabilities or Codex Skills. Use when a Steward asks to create a skill, convert a workflow into a capability, improve SKILL.md instructions or discoverability, write trigger descriptions, reduce overlap between skills, choose references/scripts/assets, define required scopes or install mode, add safety metadata and test prompts, or decide whether behavior belongs in a portable Skill or the MonadVault runtime."
---

# MonadVault Capability Packager

## Overview

Use this skill to turn a repeated Steward workflow into a portable capability package. It helps decide what can live as a Skill and what must remain runtime infrastructure.

## Routing

- Use this skill for reusable capability boundaries, packaging, metadata, and validation design.
- Use `monadvault-found-monad` when the requested artifact is a complete governed Monad rather than a reusable workflow.
- Use `monadvault-privacy-sentinel` to audit the proposed scopes and exposure paths.

## Conversion Decision

Convert to a Skill when the workflow is mostly:

- procedural guidance
- domain knowledge
- prompt structure
- review checklist
- repeatable synthesis
- document or memory shaping
- capability packaging

Keep in MonadVault runtime when the workflow requires:

- accounts, sessions, or auth
- persistent encrypted storage
- billing, ledgers, or provider keys
- publication access control
- moderation state
- database writes
- visitor entitlements
- live hosted invocation

## Packaging Workflow

1. Name the capability with lowercase hyphen-case.
2. Write a trigger-rich description that says exactly when to use it.
3. Define the primary output contract.
4. Choose resources:
   - `references/` for templates, checklists, schemas, and domain notes.
   - `scripts/` only for deterministic utilities.
   - `assets/` only for reusable output files.
5. Map required scopes conservatively:
   - prefer `memory:read_selected`
   - avoid broad memory or publication scopes
   - block `billing:write`, `vault:export`, `publication:publish`, and other high-risk scopes unless runtime governance exists
6. Add review gates for privacy, publication, provider exposure, and monetization.
7. Validate that the skill works without hidden runtime privileges.

## Output Contract

Return:

- `Skill name`
- `Description`
- `Use cases`
- `Non-goals`
- `Required scopes`
- `Install mode`
- `SKILL.md outline`
- `References/assets/scripts needed`
- `Safety review`
- `Test prompts`

Use [capability-spec-template.md](references/capability-spec-template.md) for a package spec.

## Guardrails

- Do not pretend a Skill can replace runtime controls.
- Do not request broad scopes because they might be useful later.
- Keep the first version small enough to trigger reliably.
- Prefer one focused skill over a vague mega-skill.
