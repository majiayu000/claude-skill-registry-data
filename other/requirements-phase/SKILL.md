---
name: requirements-phase
description: Close bounded product decisions and project the accepted delivery backlog.
disable-model-invocation: true
---

# Requirements Phase

Requirements Phase is independently invocable. It is the only orchestration
route for `requirements-grill -> create-architecture -> create-spec -> write-backlog`.

## Inputs

- Direct bounded requirements input, including any narrower caller-supplied
  provider projection boundary. This route creates no Fog or Finder
  artifact and no Grilling provider item implicitly.
- Optional Finder context, only when the caller supplies a Fog, Finder child,
  Research child, Prototype child, or durable Finder handoff. Resolve the exact
  identity and its owning Fog graph. Load only that graph. Requirements Phase
  does not load or take ownership of sibling work.

The optional context loader is an input adapter to this phase, not a second
workflow or a Finder lifecycle owner.

## Workflow

1. Select the applicable input contract above. Complete entry when the direct
   scope is bounded or the supplied context graph resolves exactly.
2. Read the matching `requirements-grill` status before its log. Summarize
   accepted, rejected, superseded, parked, and unresolved branches. If no
   matching status exists, start the bounded Requirements Grill directly.
3. While material decisions remain open, use `requirements-grill` for the HITL
   interview. Research recommendations are evidence, not decisions. Complete
   this step when every material branch is settled at its Target Altitude or
   explicitly parked.
4. When the user confirms shared understanding and the remaining branches are
   closed or explicitly parked, invoke `create-architecture` with the current
   grill status and log. Require its
   artifact contract in the installed `create-architecture` skill's
   `references/artifact-contract.md`:
   sibling `ARCHITECTURE.md`, `status: compiled`, `readiness: agent-ready`, exact
   source identities and accepted details, and verified retained blob URL.
   Architecture compilation precedes `SPEC.md` and requires no spec input.
   An `architecture-not-ready` result returns each exact gap to its upstream
   owner; unresolved decisions return to `requirements-grill`.
5. After `architecture-written`, invoke `create-spec` with that exact retained
   architecture and the same confirmed sources. Create Spec assigns real outcome
   and criterion codes, completes the architecture's canonical Spec traceability
   mapping, and retains the enriched architecture before binding its final
   immutable identity in the spec. This metadata amendment accepts no new design.
   The compiler preserves source question anchors and unchanged codes/selectors.
   This order applies to every delivery, including existing, resumed and local
   work; reuse only current, matching retained artifacts with complete mapping.
6. Require `create-spec` to verify both retained artifact URLs and the spec's
   reference to the enriched architecture, then push or explicitly retain the
   spec commit before `write-backlog` can run. Pending or unresolved mappings and
   local-only artifacts return the compiler's atomic `spec-not-ready` result.
7. Honor the caller's accepted provider projection boundary; missing authority
   returns a blocked backlog delta while retaining the compiled pair.
   After `spec-written`, pass the verified stable blob URL and current provider
   evidence to `write-backlog`. Write Backlog derives the Stories, Tasks, and
   blocker graph supported by the accepted result. With no prior Finder
   projection, it may reuse, enrich, or create the accepted placement through
   Product Area, Initiative, and Epic before placing those delivery items. Each
   Story is a shippable product outcome. Each Task is atomic, independently
   ownable, and understandable from its Story and stable specification.
8. Return one stable Requirements result naming the retained architecture and
   specification, their exact identities and verified stable blob URLs, plus the
   Write Backlog result and exact residual delta. The result is ready for
   `delivery-phase` and `create-plan`.

## Boundary

Requirements Phase owns decision closure, compilation order, and authorization
of delivery-depth projection. `write-backlog` owns hierarchy derivation,
provider mechanics, mutation approval, and readback. Finder remains optional
context and owns no part of this workflow.

Grilling-child, specification, Story, and Task cardinality are outputs of the
accepted requirements and current evidence, never invocation prerequisites.
