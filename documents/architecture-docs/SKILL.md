---
name: architecture-docs
description: Write architecture documentation and ADRs for software systems, repos, libraries, and workflow bundles. Use when Codex is asked to document system structure, module boundaries, decisions, tradeoffs, dependencies, diagrams, or architecture decision records.
license: MIT
---

# Architecture Docs

## Core Workflow

1. Identify the audience, system boundary, source of truth, and decision the doc
   supports.
2. Read the relevant code, configs, diagrams, existing docs, and tests before
   describing architecture.
3. Document structure, responsibilities, data flow, integration points,
   dependencies, constraints, and operational assumptions.
4. For decisions, capture context, options considered, tradeoffs, decision,
   consequences, and review triggers.
5. Separate current architecture from planned architecture.
6. Include validation notes and open questions.

## Safety Rules

- Do not invent architecture, dependencies, guarantees, or operational behavior.
- Do not expose sensitive infrastructure, secrets, private endpoints, or threat
  details in public docs.
- Mark inferred architecture clearly when source evidence is incomplete.

## Deliverable Shape

For architecture docs, provide:

- Scope and audience
- System overview
- Components and responsibilities
- Data or control flow
- Key decisions and tradeoffs
- Constraints and risks
- Validation notes
- Open questions

## References

- Read `references/architecture-docs-checklist.md` when writing architecture
  docs or ADRs.
