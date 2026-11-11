---
name: feature-brief
description: Present a concise high-level briefing of an already-planned application feature, fix, refactor, or maintenance change. Use before implementation to check and communicate the intended behaviour and scope; not for requirements discovery, low-level code design, or implementation.
---

# Feature Brief

Present the established intent of a planned application change so it can be
checked before implementation. Assume planning has already taken place. This
is a read-only, high-level briefing, not another planning or grilling session.

Primarily intended for upgrades and maintenance of existing applications. It
may be used on a new project when the requested slice is bounded; do not
recap an entire project merely because its planning context is available.

## 1. Establish the change context

1. Identify the specific change from the current request, conversation,
   planning decisions, and relevant specifications or project guidance.
2. Reuse relevant findings already available in the session. Inspect only the
   repository areas, behaviour, and tests needed to understand the proposed
   change; avoid rediscovering the entire project. If the repository is not
   accessible, use the available context and state any material limitation.
3. Distinguish established decisions from assumptions, suggestions, and older
   alternatives. Respect existing contracts and explicit user constraints.
   Surface consequential conflicts rather than silently choosing a new scope.

## 2. Check high-level sufficiency

1. Determine whether the available plan establishes the intended outcome,
   material behaviour, scope, and significant constraints well enough for an
   accurate presentation. Implementation details need not be settled.
2. If a consequential gap or contradiction would require inventing a product,
   behaviour, or major architectural decision, **stop before presenting**.
   Identify the smallest set of blocking gaps and explain why each matters.
   Do not launch an interview or fill the gaps with unsupported certainty.
3. Otherwise proceed. Keep minor open points for the end of the presentation;
   do not block on details that can ordinarily be delegated to implementation.

## 3. Present the feature

Explain the intended change in a concise, readable sequence, selecting only
material topics:

1. **Outcome:** What changes, for whom or what, and the reason for the change
   when established.
2. **Behaviour:** Relevant before/after behaviour and important interactions or
   user flows.
3. **Scope:** What is included, relevant exclusions, and significant constraints
   already decided.
4. **Affected areas:** Components, boundaries, integrations, or data affected,
   at the architectural level where known. Label tentative impact as tentative.
5. **Completion:** Observable acceptance conditions or representative scenarios
   supported by the plan, without inventing new requirements.
6. **Residual uncertainty:** Only meaningful non-blocking assumptions or open
   points, clearly separated from agreed decisions.

Scale depth to the change: a minor fix may take a short paragraph, while a
substantial feature can use several sections. Do not repeat the complete
project plan or drift into function-level implementation design.

## 4. Stop at the briefing

- Return the presentation directly in the conversation as text, not slides or
  a persistent document unless separately requested.
- Do not ask for approval, interrogate the user, edit files, create scaffolds,
  write code, run implementation, or invoke a delivery workflow.
- If blocked under section 2, report the blockers instead of producing a
  speculative presentation. Otherwise finish after the briefing.
