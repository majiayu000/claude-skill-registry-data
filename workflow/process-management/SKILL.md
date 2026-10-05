---
name: process-management
description: |
  Legacy/migration guidance for v1 Process entities — declarative workflow
  definitions with roles, gates, and a definition of done. In v2, use
  process-instance WorkItems plus Artifact-backed definitions instead of
  creating new Process records.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-process-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: role-management
        purpose: Resolve Role IDs when entities need role-based assignment.
      - skill: gate-management
        purpose: Evaluate gate conditions before allowing transitions.
    provides:
      primitives: [Process]
      templates: [process]
---

# Process Management

## Intro

In v1, a Process was a declarative workflow definition: a sequence of
steps, roles, gates, and a definition of done. In v2, Process is not a
first-class primitive authoring surface. Model a concrete run as a
WorkItem with `spec.type: process-instance`, keep the reusable definition
as an Artifact, and attach gates, scope, time, and budget policy through
Bindings.

## Overview

### Legacy v1 shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: <legacy Process>
metadata:
  id: PROC-code-review
  created: 2026-04-06T00:00:00Z
spec:
  name: code-review
  description: "Review a pull request before merge."
  triggers: [pr.opened, pr.review-requested]
  roles: [developer, reviewer]
  steps:
    - name: author-self-check
      role: developer
      uses_skill: code-review
      description: "Author runs the self-review checklist."
    - name: peer-review
      role: reviewer
      uses_skill: code-review
      description: "A different actor reviews the diff and leaves comments."
      gates: [GATE-no-blocking-comments]
    - name: approval
      role: reviewer
      description: "Reviewer approves the PR."
      gates: [GATE-code-review-passed]
    - name: merge
      role: developer
      description: "Author merges after approval and CI pass."
      gates: [GATE-ci-passed, GATE-code-review-passed]
  definition_of_done: "PR merged with at least one approval, all CI gates passed."
---
```

### v2 workflow

1. Create or reuse an Artifact that describes the reusable workflow.
2. Create a WorkItem with `spec.type: process-instance` for each run.
3. Reference the definition Artifact from the WorkItem.
4. Attach gates with `Binding(type=workitem-gate)` or
   `Binding(type=scope-gate)`.
5. Attach recurrence or active windows with `Binding(type=time-window)`.
6. Attach cost policy with `Binding(type=budget-application)`.

### Running a v2 process instance

An agent running a process-instance WorkItem:
1. Reads the definition Artifact referenced by the WorkItem.
2. Performs the next action, often guided by a skill.
3. Evaluates attached Gates and logs `gate.passed` / `gate.failed`.
4. Transitions the WorkItem through the owning MCP server.
5. Exits when the WorkItem reaches a terminal state or a blocking gate fails.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Defining a Process without ownership.** Every Process needs an
  owner Actor — the person or role responsible for keeping it
  current. Unowned Processes drift and become "the way we used to
  do things".
- **Process with no termination criteria.** A Process must answer
  "how do I know this is done". Open-ended processes that never
  terminate become noise; the agent has no signal to stop
  participating.
- **Hand-waving "automated steps" that aren't actually wired.** If
  a Process step says "CI runs automatically", verify the CI hook
  exists. A Process that lies about its automation is worse than
  one that admits everything is manual.
- **Forgetting to version Process changes.** When a Process
  definition changes, bump the version. Existing in-flight runs
  should reference the version they started under, not silently
  inherit the new rules mid-flight.
- **Mixing Process steps with WorkItems.** A Process step
  ("review the PR") is reusable across many runs; a WorkItem
  ("review BACK-1234") is one specific instance. Don't put
  workitem-specific data in the Process definition.
- **Process documentation without examples.** A Process that says
  "follow the release checklist" without linking to a worked
  example of a past release is incomplete. Examples are the
  difference between followable and theoretical.
- **Authoring a Process for a one-off operation.** If you only run
  it once, it's a runbook entry or a project log, not a Process.
  Processes earn their cost through repetition.

## Full reference

### Fields

| Field                | Type          | Notes                                              |
|----------------------|---------------|----------------------------------------------------|
| `name`               | string        | kebab-case identifier                              |
| `description`        | string        | One sentence                                       |
| `triggers`           | list[string]  | Event types that start the process                 |
| `roles`              | list[string]  | Role names involved                                |
| `steps`              | list[object]  | Ordered list; see below                            |
| `definition_of_done` | string        | The acceptance criterion for the whole process     |
| `parallel`           | bool          | Default false; true = steps run in parallel        |
| `retryable`          | bool          | Can the process be re-run if it fails?             |

### Step object

```yaml
- name: <step-name>
  role: <role-name>         # who performs this step
  description: <one-sentence>
  uses_skill: <skill-name>  # optional — skill that guides execution
  inputs: [<entity-ref>]    # optional — what this step needs
  outputs: [<entity-ref>]   # optional — what this step produces
  gates: [<gate-id>]        # optional — gates that must pass
  on_failure: <action>      # halt | retry | skip | escalate
```

### Parallel vs sequential

Default is sequential. Set `parallel: true` to run steps concurrently when
they are independent. For conditional branching, write multiple processes
and trigger them conditionally rather than embedding complex logic.

### Applying workflow policy in v2

Use v2 Binding types against the concrete governed entity:

```yaml
kind: Binding
spec:
  type: workitem-gate
  subject: BACK-release-run
  target: GATE-security-scan
  scope: SCOPE-project-x
```

### No workflow engine

processkit does not ship an engine that executes workflows. The
process-instance WorkItem and its definition Artifact form a contract
between the definition and whoever runs it. Agents are the default runners;
automation can take over specific steps.
