---
name: pair-next
description: "Determines the most relevant next action for your project by reading adoption files and PM tool state. Suggests which skill to invoke next. Use at the start of a session, when switching tasks, or whenever you need guidance on what to work on."
version: 0.4.1
author: Foomakers
---

# /pair-next — Project Navigator

Analyze project state and recommend the single most relevant next skill to invoke. Covers the full 30-skill catalog across all lifecycle phases.

## Skill Catalog (30 skills)

### Process Skills (11)

| Skill              | Lifecycle Phase    | Description                                     |
| ------------------ | ------------------ | ----------------------------------------------- |
| `/pair-process-specify-prd`     | Induction          | Create or update Product Requirements Document  |
| `/pair-process-bootstrap`       | Induction          | Orchestrate full project setup                  |
| `/pair-process-plan-initiatives`| Strategic          | Create strategic initiatives from PRD           |
| `/pair-process-plan-epics`      | Strategic          | Break initiatives into epics                    |
| `/pair-process-plan-stories`    | Sprint Planning    | Break epics into user stories                   |
| `/pair-process-refine-story`    | Sprint Planning    | Refine story with AC and technical analysis     |
| `/pair-process-plan-tasks`      | Sprint Planning    | Break story into implementation tasks           |
| `/pair-process-implement`       | Sprint Execution   | Implement story tasks with TDD                  |
| `/pair-process-review`          | Sprint Execution   | Review PR through structured phases             |

### Capability Skills (19)

| Skill                | Category     | Description                                     |
| -------------------- | ------------ | ----------------------------------------------- |
| `/pair-capability-record-decision`   | Decision     | Record ADR or ADL with adoption update          |
| `/pair-capability-write-issue`       | PM Tool      | Create/update issues in adopted PM tool         |
| `/pair-capability-setup-pm`          | PM Tool      | Configure project management tool               |
| `/pair-capability-verify-quality`    | Quality      | Check quality gates against codebase            |
| `/pair-capability-verify-done`       | Quality      | Check Definition of Done criteria               |
| `/pair-capability-verify-adoption`   | Quality      | Check code against adoption files per scope     |
| `/pair-capability-assess-stack`      | Assessment   | Assess tech stack (lifecycle-spanning)           |
| `/pair-capability-assess-architecture`| Assessment  | Assess architecture pattern                     |
| `/pair-capability-assess-testing`    | Assessment   | Assess testing strategy                         |
| `/pair-capability-assess-ai`         | Assessment   | Assess AI development tools                     |
| `/pair-capability-assess-methodology`| Assessment   | Assess development methodology                  |
| `/pair-capability-assess-pm`         | Assessment   | Assess project management tool                  |
| `/pair-capability-assess-infrastructure`| Assessment| Assess infrastructure strategy                  |
| `/pair-capability-assess-observability`| Assessment | Assess observability strategy                   |
| `/pair-capability-assess-debt`       | Assessment   | Assess technical debt with prioritization       |
| `/pair-capability-assess-code-quality`| Assessment  | Assess code quality with metrics                |
| `/pair-capability-estimate`          | Planning     | Estimate story using adopted methodology        |
| `/pair-capability-setup-gates`       | Configuration| Configure CI/CD quality gates                   |
| `/pair-capability-manage-flags`      | Configuration| Manage feature flag lifecycle                   |

## Algorithm

Execute these checks **in order**. Stop at the first match.

### Step 1: Read Adoption Files

Read the following files and classify each as **populated** or **template**:

| File                                                                                               | Template indicator                                        |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| [.pair/adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md)                               | Contains `[Product/feature name]` or `[Creation date]`    |
| [.pair/adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md)                   | Contains only placeholder headings with no real content   |
| [.pair/adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md)                       | Contains only placeholder headings with no real content   |
| [.pair/adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)               | No PM tool specified or only template text                |

**Template detection rule**: A file is a template if it contains square-bracket placeholders (e.g., `[Product/feature name]`) or if its substantive sections contain no project-specific content.

### Step 2: Cascade — Fresh Project Detection

| #   | Condition                                                 | Suggestion        | Rationale                        |
| --- | --------------------------------------------------------- | ----------------- | -------------------------------- |
| 1   | PRD.md is template                                        | `/pair-process-specify-prd`    | Product vision must come first   |
| 2   | PRD.md populated AND 3+ tech adoption files are templates | `/pair-process-bootstrap`      | Project needs foundational setup |

If any of the above matched, output the suggestion and stop.

### Step 3: Cascade — Established Project Detection

All adoption files are populated. Query the PM tool to determine backlog state.

**PM tool discovery**: Read [.pair/adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) to identify the PM tool (GitHub Projects, Jira, Linear, etc.) and access method.

| #   | Condition                                                        | Suggestion          | Rationale                                   |
| --- | ---------------------------------------------------------------- | ------------------- | ------------------------------------------- |
| 5   | No initiatives or epics exist in PM tool                         | `/pair-process-plan-initiatives` | Strategic planning needed                   |
| 6   | Initiatives exist but no epics                                   | `/pair-process-plan-epics`       | Epic decomposition needed                   |
| 7   | Epics exist but no user stories                                  | `/pair-process-plan-stories`     | Story breakdown needed                      |
| 8   | Stories exist without acceptance criteria or with `status:draft`  | `/pair-process-refine-story`     | Stories need refinement before work         |
| 9   | Refined stories exist but have no task breakdown                  | `/pair-process-plan-tasks`       | Tasks must be created before implementation |
| 10  | Tasks in "ready" or "todo" state exist                            | `/pair-process-implement`        | Work is ready to start                      |
| 11  | Open pull requests or tasks in "review" state                     | `/pair-process-review`           | Code review pending                         |

### Step 4: Capability Skill Suggestions

If no process skill matched in Steps 2-3, check for capability skill opportunities:

| #   | Condition                                                                | Suggestion           | Rationale                                      |
| --- | ------------------------------------------------------------------------ | -------------------- | ---------------------------------------------- |
| 12  | Quality gate not configured (no Quality Gates section in way-of-working) | `/pair-capability-setup-gates`       | Quality gates should be established             |
| 13  | Tech stack has unlisted dependencies detected                            | `/pair-capability-assess-stack`      | Stack registry needs updating                   |
| 14  | Technical debt flags present (TODO/FIXME/HACK comments detected)         | `/pair-capability-assess-debt`       | Debt should be cataloged and prioritized        |
| 15  | No estimation methodology adopted in way-of-working                      | `/pair-capability-estimate`          | Estimation process should be established        |

### Step 5: Fallback

If no condition matched in Steps 2-4:

> All adoption files are populated and no actionable backlog items detected.
> Consider: starting a new iteration with `/pair-process-plan-stories`, or running `/pair-process-review`
> to check for open items.

## Output Format

Present results as:

```text
PROJECT STATE:
├── PRD: [populated | template]
├── Bootstrap: [complete | incomplete — N/M adoption files populated]
├── PM Tool: [tool name | not configured]
└── Backlog: [summary of current items]

RECOMMENDATION: /skill-name
REASON: [one-line explanation]
```

Then ask: "Shall I run `/skill-name`?"

## Graceful Degradation

- If a suggested skill is not installed, tell the user which skill is needed and where to find it.
- If the PM tool is not accessible (no MCP connection, no credentials), skip Step 3 and report: "PM tool not accessible — recommendation based on adoption files only."
- If adoption files cannot be read (not installed yet), suggest `/pair-process-bootstrap` as the entry point.

## Notes

- This skill is read-only: it inspects state but never modifies files or PM tool data.
- When multiple items are actionable (e.g., tasks to implement AND PRs to review), prefer the item closest to delivery (`/pair-process-review` > `/pair-process-implement` > `/pair-process-plan-tasks`).
- Re-run `/pair-next` after completing any skill to get an updated recommendation.
- **Full catalog coverage**: this navigator can suggest any of the 30 skills based on project state. Process skills are suggested through the cascading checks (Steps 2-3). Capability skills are suggested through targeted checks (Step 4) or as part of process skill composition.
