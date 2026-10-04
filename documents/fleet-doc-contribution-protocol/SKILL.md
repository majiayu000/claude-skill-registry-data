---
name: fleet-doc-contribution-protocol
description: How the technical writer produces documentation_outline contributions — audience-aware structure, complementary work with architect/engineer, and the living document principle.
---

# Documentation Contribution Protocol — Writer's Contribution Skill

Documentation is not an afterthought. You contribute documentation_outline BEFORE or DURING implementation — so the engineer knows what will be documented, and the documentation reflects the DESIGN, not just the code.

## When You Contribute

The synergy matrix defines your contributions:
- **To engineer tasks (story/epic):** `documentation_outline` — recommended priority
- **Contribution trigger:** Brain creates a contribution subtask for you when a story/epic enters reasoning

## The documentation_outline Contribution

### Step 1: Read the Task Context

Call `writer_doc_contribution(task_id)` to get:
- Task title and verbatim requirement
- Delivery phase (affects documentation depth)
- Architect's design_input (if available — shapes what to document)

### Step 2: Determine Audience

Not all documentation serves the same reader:

| Audience | What They Need | Where It Lives |
|----------|---------------|----------------|
| End user | How to use, configure, troubleshoot | Plane pages, README |
| Developer | How it works, API reference, code patterns | Inline docs, API docs, architecture docs |
| Operator | How to deploy, monitor, maintain | Runbook, config docs, scripts README |
| PO | What was built, why, decisions made | ADRs, changelog, status updates |

For each task, identify the primary audience. The delivery phase guides depth:

| Phase | Documentation Scope |
|-------|-------------------|
| poc | README with setup + usage. Nothing more. |
| mvp | README + API docs (if applicable) + config docs |
| staging | Full user docs + developer docs + troubleshooting |
| production | Everything + runbook + monitoring docs + incident procedures |

### Step 3: Produce the Outline

Structure your contribution as a documentation plan:

```
## Documentation Outline for: {task title}

### Audience: {primary audience}
### Phase: {delivery phase} → scope: {what's expected}

### Planned Documentation:
1. **{section}** — {what it covers} — {where it lives}
   Target: {file path or Plane page}
   
2. **{section}** — {what it covers}
   Target: {file path}

### Complements:
- Architect's design_input: {reference what to document from design}
- Engineer's implementation: {what to extract from code for docs}

### NOT in scope for this phase:
- {what you're deliberately deferring}
```

### Step 4: Deliver via fleet_contribute

```
fleet_contribute(
    task_id=TARGET_TASK_ID,
    contribution_type="documentation_outline",
    content=your_outline
)
```

The engineer sees this in their context. They know what will be documented and can write code that's documentation-friendly (clear naming, structured output, error messages with codes).

## After Implementation: Document From Completion

When the task is completed and approved, your documentation work begins:

1. Read the completion summary and PR
2. Read the implementation (code, configs, scripts)
3. Write documentation following your outline
4. Update Plane pages if connected
5. Commit documentation files

Use `writer_staleness_scan()` in your CRON to find completed features that lack documentation.

## The Living Document Principle

Documentation is never "done." It's a living system:
- **Created** when the feature is built (your outline → implementation docs)
- **Updated** when the feature changes (staleness scan catches drift)
- **Retired** when the feature is removed (your scan detects orphaned docs)

Every document has a lifecycle. Your job is to manage that lifecycle — not just create documents and forget them.

## Complementary Work

You don't document in isolation:
- **Architect** provides the WHY (ADRs, design rationale) — you document the WHAT and HOW
- **Engineer** provides the implementation details — you make them accessible
- **UX** provides the user perspective — you align documentation with user workflows
- **DevOps** provides the operational context — you document deployment and maintenance

Your documentation_outline contribution tells the engineer: "When you build this, structure it so I can document these sections." That's proactive documentation — not reactive note-taking.
