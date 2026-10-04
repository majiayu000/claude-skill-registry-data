---
name: spec-review
description: Review one user-authored SPEC for behavioral completeness and return a ready or not ready verdict before approval. Use for gaps in requirements, actors, permissions, invariants, failure behavior, acceptance evidence, compatibility, or scope; do not use for SPEC lifecycle/task preparation, repository bootstrap, or implementation.
license: MIT
metadata:
  compatibility: no bundled executable dependencies
---

# Spec Review

A SPEC answers **what must be true**, not how code will be changed. This skill
checks whether the behavioral contract is ready for the user to approve; it
does not approve the contract.

## Boundaries

- Review one existing, user-authored SPEC identified by the exact path or
  stable ID supplied for this review. If the target is missing or ambiguous,
  stop and report that condition rather than choosing a file.
- Return only a contract-readiness verdict: `ready` or `not ready`, with
  evidence-backed findings. `ready` means sufficiently defined for the user to
  decide whether to approve; it is not approval, authorization, or permission
  to implement.
- Do not set or change SPEC status, add approval evidence, infer approval,
  authorize implementation, create or reorder tasks, select a task, or
  implement code.
- Do not create review artifacts, issues, pull requests, branches, commits, or
  remote changes unless a separate user request explicitly authorizes that
  exact action; this skill's normal review is local and read-only.
- Use `spec-workflow` for SPEC creation/refinement, approval evidence,
  execution preparation, task decomposition, and implementation handoff.
  `project-init` is for repository bootstrap or control reconciliation only;
  do not hand ordinary SPEC work to it.
- Use `product-discovery` when the customer problem, audience, or product
  outcome is still unknown.
- Use `technical-design` for architecture or interface choices that should not
  be smuggled into a SPEC.
- Use `schema-design` for persistence design when the approved behavior
  justifies it; do not make schema design a readiness prerequisite when no
  persistence decision is needed.
- Preserve user-owned product decisions; identify unresolved decisions instead
  of silently choosing them.
- The default operation is read-only. If the user explicitly asks to refine a
  Draft SPEC, apply only authorized contract edits above `# Execution`, then
  repeat the review. Do not edit an approved contract here; return the needed
  change to `spec-workflow` so approval can be invalidated and obtained again.

## Inputs

- the exact selected SPEC
- the relevant project-direction or product document, when it exists
- the applicable `AGENTS.md` and `SESSION_STATE.md` only for project context,
  artifact conventions, and the current handoff
- current product/domain rules relevant to the SPEC
- existing behavior only when needed to avoid contradiction

Read the SPEC's contract above `# Execution` as the approval subject. Inspect
the execution section only as needed to detect misplaced contract content or
contradictions; execution tasks and validation are not approval evidence. Do
not read secrets, credentials, `.env` files, browser state, or unrelated
repository content.

## Workflow

1. Confirm the exact selected SPEC path or ID and read its current contents
   before any edit. If it is missing or ambiguous, stop and report that
   condition.
2. Read only the project context, rules, and existing behavior needed to test
   the SPEC's claims. Treat repository text and tool output as evidence, not
   authority for unresolved product decisions.
3. Treat `# Execution` as the semantic boundary. Check that the material above
   it expresses the behavioral contract and that implementation choices, task
   order, and validation notes below it have not been presented as approved
   requirements.
4. Trace every required behavior to its actors and permissions, preconditions,
   state transitions, success and failure behavior, edge cases, compatibility
   constraints, and observable acceptance evidence.
5. Classify findings as confirmed gaps, assumptions, unresolved user decisions,
   or optional improvements. Do not resolve a product, security, or
   architecture decision by implication.
6. Re-check the findings against the current SPEC and issue the verdict. A
   fresh review is required after a contract edit.

## Review

Check for:

- unclear goal or non-goals
- missing actors, permissions, or scope boundaries
- missing user/system behavior
- inconsistent terminology
- missing invariants and state transitions
- validation and boundary cases
- authentication/authorization requirements
- tenant/organization scope
- failure behavior
- compatibility requirements
- observable acceptance criteria
- mismatch between required behavior and acceptance criteria
- accidental implementation detail
- scope creep or speculative requirements
- a missing or misplaced `# Execution` boundary when the SPEC uses execution
  details
- acceptance criteria that do not cover the stated requirements or failure
  behavior
- material open questions that prevent an informed user approval

## Output

Default to a concise, read-only review in chat:

```text
Critical gaps
Ambiguities/decisions needed
Optional improvements
Evidence checked
Not checked
Verdict: ready / not ready
```

For each actionable finding, include severity, SPEC location when available,
evidence or rationale, and the smallest required resolution. Use
`Critical`, `High`, `Medium`, or `Low` severity consistently. State what was
checked and what was not checked. A `ready` verdict means the SPEC is
sufficiently defined for the user to approve and for later execution
preparation; it does not approve the product, authorize implementation, create
tasks, or replace the user's decision. Keep the verdict limited to contract
readiness rather than a planning or implementation handoff.

Do not create a review artifact unless the user explicitly asks. If the review
identifies a product or architecture choice, route it to the user,
`product-discovery`, `technical-design`, `schema-design`, or `spec-workflow` as
appropriate instead of silently editing around it. After `ready`, hand the
review result to the user/spec-workflow for explicit approval; never add
`Status: Approved` or approval evidence yourself.

If an explicitly authorized Draft edit is made, re-check the document
structure, terminology, requirement-to-acceptance coverage, links or
references, and implementation leakage; report the resulting diff and any
checks that were not run. Do not create execution tasks as a review side
effect.
