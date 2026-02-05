---
name: spec-management
description: Central authority for specification-driven development. Use when working with requirements, specifications, acceptance criteria, or any spec-driven workflow. Provides navigation to specialized skills and delegates to docs-management for official documentation.
allowed-tools: Read, Glob, Grep, Skill
---

# Specification Management

Central hub for specification-driven development workflows. This skill provides navigation to specialized skills for different specification formats and workflows.

## When to Use This Skill

**Keywords:** specifications, requirements, acceptance criteria, spec-driven development, SDD, EARS, Gherkin, Kiro, Spec Kit, BDD, user stories, feature specifications, canonical spec

**Use this skill when:**

- Starting a new specification-driven workflow
- Converting between specification formats
- Understanding available specification providers
- Navigating to specialized authoring skills
- Working with the canonical specification model

## Quick Decision Tree

**What do you want to do?**

1. **Start Spec Kit 5-phase workflow** → Use `/spec:speckit:run` or see [speckit-workflow skill](../speckit-workflow/SKILL.md)
2. **Generate a specification** → Use `/spec:specify` command
3. **Write EARS requirements** → See [ears-authoring skill](../ears-authoring/SKILL.md)
4. **Write Gherkin scenarios** → See [gherkin-authoring skill](../gherkin-authoring/SKILL.md)
5. **Sync with AWS Kiro** → See [kiro-integration skill](../kiro-integration/SKILL.md)
6. **Check requirement quality** → See [requirements-quality skill](../requirements-quality/SKILL.md)
7. **Understand canonical format** → See [canonical-spec-format skill](../canonical-spec-format/SKILL.md)
8. **Convert between formats** → Use `/spec:convert` command

## Specification Providers

The canonical specification model (ADR-115) supports multiple providers:

| Provider | Format | Best For |
| --- | --- | --- |
| **ears** | EARS syntax | Precise, unambiguous requirements |
| **gherkin** | .feature files | BDD tests with Reqnroll |
| **kiro** | AWS Kiro | IDE integration with steering files |
| **speckit** | GitHub Spec Kit | AI agent prompts, 5-phase workflow |
| **adr** | MADR format | Architecture decisions |
| **userstory** | Agile format | Product backlog items |
| **canonical** | YAML/JSON | Direct canonical format |

## Spec Kit 5-Phase Workflow

The GitHub Spec Kit workflow guides feature development:

| Phase | Artifact | Purpose |
| --- | --- | --- |
| 0 | `.constitution.md` | Project principles and constraints |
| 1 | `feature.md` | Specification from requirements |
| 2 | `design.md` | Implementation approach |
| 3 | `tasks.md` | Task breakdown |
| 4 | Code | Guided implementation |

**Full workflow:** Use `/spec:speckit:run` or invoke the `speckit-workflow` skill.

## Canonical Specification Model

All providers transform to/from the canonical model:

```yaml
id: "SPEC-001"
title: "Feature Title"
type: feature | bug | chore | spike | tech-debt

context:
  problem: "Description of the problem"
  motivation: "Business value"

requirements:
  - id: "REQ-001"
    text: "EARS-formatted requirement"
    priority: must | should | could | wont
    ears_type: ubiquitous | state-driven | event-driven | unwanted | complex | optional
    acceptance_criteria:
      - id: "AC-001"
        given: "Precondition"
        when: "Action"
        then: "Expected outcome"

traceability:
  adr_refs: ["ADR-115"]
  requirement_refs: ["FR-001"]

metadata:
  status: draft
  created: "YYYY-MM-DD"
  provider: canonical
  bounded_context: "WorkManagement"
```

**Full schema:** See [canonical-spec-format skill](../canonical-spec-format/SKILL.md) or `schemas/canonical-spec.schema.json`

## Available Commands

### Generic Workflow Commands

| Command | Purpose |
| --- | --- |
| `/spec:specify` | Phase 1: Generate specification from requirements |
| `/spec:plan` | Phase 2: Generate implementation plan |
| `/spec:tasks` | Phase 3: Generate task breakdown |
| `/spec:implement` | Phase 4: Guide implementation |
| `/spec:validate` | Validate specification against schema |
| `/spec:refine` | AI-assisted specification refinement |
| `/spec:audit` | Audit specification quality |
| `/spec:convert` | Convert between formats |

### Provider Deep-Dive Commands

| Command | Purpose |
| --- | --- |
| `/spec:ears:author` | Interactive EARS pattern authoring |
| `/spec:ears:convert` | Convert to/from EARS format |
| `/spec:gherkin:author` | Interactive Gherkin scenario authoring |
| `/spec:gherkin:convert` | Convert to/from .feature files |
| `/spec:kiro:sync` | Sync with AWS Kiro specifications |
| `/spec:speckit:run` | Execute full Spec Kit 5-phase workflow |
| `/spec:adr:create` | Create ADR from specification context |
| `/spec:userstory:author` | Author user stories with acceptance criteria |
| `/spec:constitution` | Create or update project constitution |
| `/spec:status` | Show specification status dashboard |

## Delegation Pattern

This skill delegates to specialized skills for detailed guidance:

| Topic | Delegate To |
| --- | --- |
| EARS patterns | `ears-authoring` skill |
| Gherkin/BDD | `gherkin-authoring` skill |
| AWS Kiro | `kiro-integration` skill |
| Spec Kit workflow | `speckit-workflow` skill |
| Quality criteria | `requirements-quality` skill |
| Canonical format | `canonical-spec-format` skill |
| Official Claude Code docs | `docs-management` skill |

## Repository Infrastructure

This plugin integrates with project infrastructure:

| Resource | Purpose |
| --- | --- |
| `schemas/canonical-spec.schema.json` | Canonical specification JSON Schema |
| `prompts/specify.prompt.md` | Generation template for Phase 1 |
| `templates/EARS-REQUIREMENT-TEMPLATE.md` | EARS pattern reference |
| `docs/adr/ADR-115-*` | Specification Provider Abstraction |

## Related Skills

- **ears-authoring** - EARS requirement pattern authoring
- **gherkin-authoring** - Gherkin/BDD scenario authoring
- **kiro-integration** - AWS Kiro specification sync
- **speckit-workflow** - GitHub Spec Kit 5-phase workflow
- **requirements-quality** - INVEST criteria and quality assessment
- **canonical-spec-format** - Canonical specification reference
- **docs-management** - Official Claude Code documentation

## References

**Detailed Documentation:**

- [Canonical Format Reference](references/canonical-format.md)
- [Provider Matrix](references/provider-matrix.md)
- [Workflow Phases](references/workflow-phases.md)

---

**Last Updated:** 2025-12-24

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
