---
name: doc-expert-expertise
description: Deep expertise for documentation lifecycle orchestration. Quality assessment frameworks, workflow patterns, delegation protocols, and release checklists. Auto-loads for doc-expert agent.
---

# Doc-Expert Expertise

These references are the authoritative source for how doc-manager works. Read them for specifics about configuration options, valid values, presets, and syntax.

## Quick Reference

| Topic | Reference | When to Use |
|-------|-----------|-------------|
| Quality criteria | [quality-framework.md](references/quality-framework.md) | Assessing documentation quality |
| Workflows | [workflow-sops.md](references/workflow-sops.md) | Executing sync, setup, migration, config tuning |
| Delegation | [delegation-protocol.md](references/delegation-protocol.md) | Working with doc-writer |
| Releases | [release-checklist.md](references/release-checklist.md) | Pre-release audits |
| Configuration | [config-reference.md](references/config-reference.md) | Setting up or tuning .doc-manager.yml |
| Conventions | [conventions-reference.md](references/conventions-reference.md) | Setting up doc-conventions.yml |

## Quality Framework Overview

7 criteria for documentation quality:
1. **Relevance** - Addresses current user needs
2. **Accuracy** - Reflects actual codebase
3. **Purposefulness** - Clear goals and audience
4. **Uniqueness** - No redundancy
5. **Consistency** - Aligned style
6. **Clarity** - Easy to understand
7. **Structure** - Logical organization

See [quality-framework.md](references/quality-framework.md) for scoring rubrics and detailed evaluation guidance.

## Workflow Quick Reference

**Health Check**: detect_changes → report → offer next steps

**Full Sync**: detect_changes → batch → delegate → validate → assess → baseline

**Quality Audit**: assess_quality → validate_docs → report → offer fixes

**Release Gate**: sync(check) → assess_quality → recommendation

**Setup**: detect_platform → confirm → init → report

**Config Tuning**: assess_quality → identify project type → recommend strategy/presets → apply → verify

See [workflow-sops.md](references/workflow-sops.md) for detailed procedures.

## Delegation Quick Reference

When delegating to doc-writer, always provide:
- Context (what changed)
- Platform (formatting)
- File list with source locations
- Conventions

See [delegation-protocol.md](references/delegation-protocol.md) for templates and feedback patterns.

## Key Principles

1. **Analyze before acting** - Run detection first
2. **Batch large changes** - 10-15 files per delegation
3. **Validate before baseline** - Quality gate required
4. **Escalate appropriately** - User decides on ambiguity
5. **Report transparently** - Successes and failures
