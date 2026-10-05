---
name: gate-management
description: |
  Manage Gate entities — validation checkpoints that WorkItems, scopes, or
  policy applications must pass (code review, security scan, tests). Use
  when defining or updating a checkpoint for v2 workflow surfaces — code
  review, tests green, security scan, stakeholder approval.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-gate-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Gate]
      mcp_tools:
        - create_gate
        - get_gate
        - list_gates
        - evaluate_gate
      templates: [gate]
---

# Gate Management

## Intro

A Gate is a validation checkpoint — "code review passed", "tests green",
"security scan clean", "stakeholder signed off". In v2, Bindings attach
gates to concrete workflow surfaces such as WorkItems and Scopes.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Gate
metadata:
  id: GATE-code-review
  created: 2026-04-06T00:00:00Z
spec:
  name: code-review
  description: "At least one reviewer has approved the change."
  kind: manual           # manual | automated | hybrid
  validator: "A second actor reviews and approves."
  required_roles: [reviewer]
  blocking: true         # if false, gate is advisory only
---
```

### Workflow

1. Pick `GATE-<name>` where name is a short noun phrase.
2. Set `kind`: `manual` (human does it), `automated` (check runs automatically),
   or `hybrid` (both).
3. Describe the `validator` — the concrete check. One or two sentences.
4. List `required_roles` if specific actors must do the validation.
5. Set `blocking: true` for hard gates (cannot proceed), `false` for advisory.

### Gate outcomes

Gates emit LogEntries when they are evaluated:
- `gate.passed` — validation succeeded
- `gate.failed` — validation failed (include failure details)
- `gate.waived` — validation was bypassed (include `details.waived_by` and reason)

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Defining a Gate without an evaluator.** A Gate that says "code
  review passed" but doesn't say HOW that's checked is decoration,
  not a checkpoint. Every Gate must have either an automated check
  (script, MCP tool, CI job) or a clearly named manual approver.
- **Auto-approving manual gates.** If a Gate is `kind: manual`, the
  agent does NOT have authority to mark it passed. Surface the gate
  to the user, ask for explicit approval, and only then call
  `evaluate_gate` with the approver's ACTOR-ID.
- **Missing the rollback path on failure.** Every Gate that can fail
  must specify what happens when it does — block the process, page
  oncall, escalate, defer to a different gate. A Gate that fails
  silently is worse than no gate.
- **Writing gates that are too coarse.** "Tests pass" is too vague —
  which suite? Which subset? With what coverage threshold?
  Granularity matters because the agent needs to know what
  specifically is being checked when the gate is invoked.
- **Forgetting to log `gate.passed` / `gate.failed` / `gate.waived`.**
  These events are how the audit trail tracks process health. If
  you evaluate a gate without logging the outcome, the index can't
  answer "how often does this gate fail" or "who waived it last".
- **Hand-waving "automated" gates that aren't actually wired.** If
  `kind: automated`, the evaluator must exist and be runnable from
  the agent's environment. Marking a gate automated when it
  actually requires a human is a process failure dressed as a
  technical one.
- **Treating gate failures as warnings.** Gates are blockers by
  design. If a Gate fails, the dependent process step does NOT
  proceed, even under pressure. If the user wants to bypass, that's
  a `gate.waived` event with the waiver's name and reason — never
  an unrecorded continuation.

## Full reference

### Fields

| Field             | Type          | Notes                                          |
|-------------------|---------------|------------------------------------------------|
| `name`            | string        | Short kebab-case identifier                    |
| `description`     | string        | What this gate checks                          |
| `kind`            | enum          | `manual` / `automated` / `hybrid`              |
| `validator`       | string        | Prose description of the check                 |
| `validator_command` | string      | Optional. CLI command that automates the check |
| `required_roles`  | list[string]  | Roles that can sign off                        |
| `blocking`        | bool          | `true` = cannot proceed if failed              |
| `evidence_required` | bool        | Require a link/artifact in the pass event      |

### Binding gates to v2 workflow surfaces

Use `workitem-gate` for a concrete run or task, and `scope-gate` for a
gate that applies across a Scope. Legacy `process-gate` Bindings are
migration-only.

```yaml
kind: Binding
spec:
  type: workitem-gate
  subject: BACK-release-run
  target: GATE-security-scan
  scope: SCOPE-project-x
```

This way the same Gate can apply to multiple runs or scopes, and the
mapping changes without editing the Gate or governed entity.

### Waiving a gate

If a blocking gate is bypassed, log `gate.waived` with `details.waived_by`
(actor ID), `details.reason`, and `details.expires_at`. Do not edit the
Gate definition — the waiver is an event, not a property.
