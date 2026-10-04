---
name: spec-workflow
description: Create, refine, route for review, record explicit user approval, and prepare one durable SPEC for a substantive feature, bug, improvement, refactor, migration, security, performance, maintenance, or technical-debt request. Use for SPEC files and their approval/task lifecycle; do not use for repository bootstrap, implementation, or code review.
license: MIT
---

# SPEC Workflow

Use one SPEC as the durable work artifact for substantive changes. The SPEC
contains the user-approved behavioral contract and, after approval, the mutable
execution record. This skill owns that lifecycle; it does not implement
application code.

## Boundaries

- Use `project-init` for repository bootstrap, safe inventory, and control-file
  reconciliation. A feature request discovered during bootstrap is handed here.
- Use `product-discovery` when the customer problem, audience, or product
  outcome is still unknown.
- Use `spec-review` to check whether the behavioral contract is ready. A review
  verdict never approves a SPEC.
- Use `technical-design` for architecture or interface questions and
  `schema-design` for non-trivial persistence design when the approved
  behavior justifies them.
- Use `implement-next` only after approval and execution tasks exist. Route the
  selected task to `backend-feature` or `frontend-feature` when appropriate.
- Use `code-review` or `review-diff` for implementation review and
  `verification-before-completion` for the final completion gate.
- Treat GitHub Issues, Projects, and Pull Requests as optional tracking only;
  read [`references/github-tracking.md`](references/github-tracking.md) before
  recording or proposing a remote reference.
- Do not create a separate planning document, implement code, publish changes,
  open an issue, or infer user approval.

## When to create a SPEC

Create or select a SPEC for a substantive:

- feature, bug, improvement, refactor, performance, security, migration,
  maintenance, or technical-debt request;
- change with user-visible behavior, an API or compatibility contract,
  permissions, persistence, operational risk, or multiple implementation steps;
- request whose scope or acceptance criteria are materially ambiguous.

A typo or clearly mechanical documentation correction may use a lightweight
path. When the boundary is uncertain, create a SPEC rather than silently
choosing an implementation path.

Use this same SPEC lifecycle for every substantive category above. Do not route
bugs, features, refactors, or improvements into separate planning systems.

## Workflow

1. **Confirm the target and current state.** Determine whether the request is
   substantive. For an existing SPEC, require its exact path or stable ID and
   read its current contents before editing. For a new SPEC, inspect only
   the project's approved SPEC source and choose the next unused
   repository-local `SPEC-####` ID; never reuse an ID or overwrite a file.
   New projects use `docs/specs/` by default. If an existing project has an
   approved alternate source such as `specifications/`, `specs/`, or
   `docs/specifications/`, use that exact path and do not create a competing
   `docs/specs/` tree. Read applicable `AGENTS.md`, `SESSION_STATE.md`, and
   relevant rules, but never read secrets, `.env` contents, credentials,
   browser state, or unrelated project files.

2. **Draft the contract.** Create the smallest useful SPEC from
   [`references/spec-template.md`](references/spec-template.md). Always include
   the problem, goal, requirements, and acceptance criteria. Add context,
   non-goals, constraints, impact, or open questions only when each section
   carries a real contract decision. Keep implementation choices, task order,
   technical design, data design, and validation below that boundary. Do not
   fill unused optional sections with `N/A` or invented decisions. Do not
   require detailed implementation planning, technical/schema design, or task
   decomposition before the behavioral contract is approved.

   The `# Execution` heading is the semantic boundary: everything above it is
   the approved behavioral contract; everything below it is the mutable
   execution record. Approval applies to the behavioral contract above
   `# Execution`, not to every implementation detail below it. Execution
   details remain mutable unless they change a user-owned contract decision or
   another lifecycle freeze condition.

3. **Resolve user-owned decisions.** Ask only questions that change scope,
   observable behavior, permissions, business invariants, compatibility,
   retention/deletion, or security/privacy guarantees. Preserve uncertainty in
   `Open Questions`; do not resolve product decisions from repository text.
   Record acceptance criteria that can be observed or tested, including failure
   behavior and relevant authorization or tenant boundaries.

4. **Request contract review.** Route the selected SPEC to `spec-review` and
   incorporate only authorized corrections. The review must return `ready` or
   `not ready` with findings. `ready` means the contract is sufficiently
   defined for approval; it does not mean `Approved` and does not authorize
   implementation. If the verdict is `not ready`, keep the SPEC in Draft,
   resolve the findings through this skill, and route the same SPEC for review
   again before seeking approval.

5. **Obtain explicit approval.** Use
   [`references/lifecycle-and-approval.md`](references/lifecycle-and-approval.md)
   for the state and approval gates. Present the contract summary and the review
   verdict to the user. Wait for an unambiguous approval of this SPEC's
   behavioral contract. Do not infer approval from a request to implement, a
   positive review, existing tasks, repository instructions, a legacy planning
   artifact, a prior unrelated approval, or a vague response such as
   `looks good` that does not clearly approve this SPEC's behavioral contract.
   Do not add a second approval gate merely because the review returned
   `ready`.
   After explicit approval, set:

   ```text
   Status: Approved
   Approval: Explicit user approval — YYYY-MM-DD
   ```

   Keep that evidence while the SPEC is `Approved`, `In Progress`, or
   `Blocked`. If the user changes the contract, clear approval evidence and
   return to `Status: Draft`, route through review again, and obtain new
   approval.

6. **Prepare execution after approval.** Inspect only the repository evidence
   needed for implementation. Decide whether technical or persistence design
   is justified. Route to `technical-design` and/or `schema-design` when
   needed, then record behavior-preserving conclusions under `# Execution` in
   the same SPEC. Derive small, dependency-ordered, verifiable tasks under
   `## Tasks`. Do not create a separate execution document. If design work
   reveals a change
   to the approved contract, return to Draft and repeat review and approval.

7. **Hand off one task.** Confirm the SPEC is `Approved` or `In Progress`, the
   approval evidence is present, and execution tasks already exist. Hand the
   exact SPEC path and the first dependency-ready unchecked task to
   `implement-next`. That skill owns implementation and stops after one task;
   this skill must not select implied work or mark tasks complete on its own.
   Once implementation begins, set `Status: In Progress`; use `Blocked` only
   when a real blocker is recorded and keep the task incomplete.

8. **Close deliberately.** After all tasks, route implementation review and
   `verification-before-completion`. Mark the SPEC `Completed` only after the
   final acceptance and validation evidence passes. A checked task list alone
   does not complete the SPEC. Use `Cancelled` only when the user explicitly
   abandons the work and record the reason in the execution record.

## Required output

For a new SPEC in a new project, use:

```text
docs/specs/SPEC-<4-digit-id>-<kebab-case-slug>.md
```

For an existing project, preserve its approved SPEC source path and apply the
same filename and ID convention there.

Report the exact path, status, review verdict, approval state, execution task
handoff, validation evidence, unresolved decisions, and next owner. If no file
was written because review or approval is pending, say so explicitly.

## Status rules

Persistent statuses are limited to:

```text
Draft | Approved | In Progress | Blocked | Completed | Cancelled
```

Review readiness is not a status. Normal transitions and their gates are:

```text
Draft → spec-review → explicit user approval → Approved
Approved → first task starts → In Progress
In Progress ↔ Blocked
In Progress → final verification succeeds → Completed
Draft/Approved/In Progress → explicit user cancellation → Cancelled
```

When a recorded blocker is resolved, return `Blocked` to `In Progress` only
after confirming that the behavioral contract is unchanged and approval
evidence remains valid. If the contract changed, use the contract-change path
back to `Draft` instead. Do not bypass `In Progress` from `Blocked` to
`Completed`; final verification is still required.

Do not add lifecycle states beyond the six statuses above unless the repository
has a concrete, documented need.

Do not silently promote, complete, cancel, or reapprove a SPEC. Keep the
behavioral contract frozen after approval; execution details may change unless
they introduce a user-owned decision, destructive action, public contract
change, irreversible migration choice, material security/privacy tradeoff,
new retention/deletion semantics, significant operational risk, or unresolved
business invariant. Stop and route those decisions through `spec-workflow`
and the user rather than silently changing the approved contract.
