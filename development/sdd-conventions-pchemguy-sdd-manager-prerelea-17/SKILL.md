---
name: sdd-conventions
description: "Use when designing or reviewing a chosen architecture, design pattern, component boundary, API, module, refactor, Phase → Milestone → Task hierarchy, task breakdown, hosted task mapping, repository hosting-token storage or authentication recovery, workflow branch identities and artifact locations, review/revision campaign records, Markdown document style, or code change; also use during code review and when comparing design options. Assess cohesion, dependencies, testability, complexity, and SOLID, DRY, and KISS where relevant."
---

# Shared conventions

Use the relevant convention only when its concern occurs in the current work. Respect applicable project instructions and established contracts. This skill supplies reusable criteria; it does not perform repository orientation, own project artifacts, execute a workflow, or authorize mutation.

## Available conventions

- **Markdown style:** Read [Markdown style](references/markdown-style.md) whenever authoring, revising or reviewing Markdown documents, templates or hosted drafts of any type.
- **Modularity:** Read [modularity](references/modularity.md) when creating or assessing boundaries among system blocks, components, document nodes, code modules, or executable tasks, including code review.
- **Design heuristics:** Read [design heuristics](references/design-heuristics.md) when evaluating a chosen design or pattern, reviewing an implementation or refactor, or comparing options using SOLID, DRY, or KISS.
- **Task hierarchy:** Read [task hierarchy](references/task-hierarchy.md) when defining or reviewing Phase → Milestone → Task identity and parentage in TASKS, or projecting that hierarchy to hosted issues, labels, and milestones.

- **Backend object lifecycle:** Read [backend object lifecycle](references/backend-object-lifecycle.md) for phase-gated projection, explicit review units, issue/milestone closure, report placement and interruption recovery.

- **Workflow identity:** Read [workflow identity](references/workflow-identity.md) when allocating revision/feature campaign identities, naming workflow branches, or locating active and retained workflow artifacts.

- **Development-document QC:** Read [development-document QC](references/development-document-qc.md) when authoring/reviewing SPEC, PLAN or TASKS, evaluating delivery decomposition, establishing stage readiness, or reassessing affected feature/steering documents.

- **Review campaigns:** Read [review campaigns](references/review-campaigns.md) when organizing review/revision plans and reports, assigning campaign/finding identities, or retaining findings and evidence alongside governing project documents.

- **Hosting tokens:** Read [hosting tokens](references/hosting-tokens.md) when discovering, storing, or supplying repository credentials, or recovering shell/backend authentication.

Add a convention here only when it defines a clear invariant used by multiple workflows, can be applied without absorbing their stage-specific procedures, and does not own an artifact or operational workflow. Give each added concern its own focused reference and explicit trigger. Otherwise place it with the skill that owns the work.
