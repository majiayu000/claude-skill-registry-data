---
name: improve-codebase-architecture
description: "Side-route skill for architecture exploration and deepening opportunities. Use when the user wants to find structural improvements, shallow-module pain, or refactor opportunities that may flow into /request-refactor-plan or /execute. Not for already-scoped implementation tasks."
sources:
  primary:
    - "A Philosophy of Software Design — John Ousterhout"
  secondary:
    - "Clean Architecture — Robert C. Martin"
---

# Improve Codebase Architecture

Explore a codebase like an AI would, surface architectural friction, discover opportunities for improving testability, and propose module-deepening refactors as GitHub issue RFCs.

A **deep module** (John Ousterhout, "A Philosophy of Software Design") has a small interface hiding a large implementation. Deep modules are more testable, more AI-navigable, and let you test at the seam instead of inside.

## Working vocabulary

Use these terms exactly when describing architectural opportunities, in conversation with the user, in candidate write-ups, and in the resulting RFC issue. Do not drift into "component," "service," "API," or "boundary" — they read as synonyms but each one hides a different design decision and the slippage compounds across recommendations.

- **Module** — a unit of code that callers interact with through a stable interface. Files, classes, packages, or directories can all be modules; the test is whether something on the outside depends on something on the inside.
- **Interface** — the surface a module presents to callers: types, methods, parameters, return shapes, errors. Not the implementation.
- **Implementation** — the code behind the interface that callers do not see and should not depend on.
- **Depth** — the ratio of implementation hidden to interface exposed. Deep = a lot hidden behind a narrow surface; shallow = the interface is nearly as complex as the body.
- **Seam** — a place in the codebase where one module ends and another begins. Tests are written *at* seams; refactors *move* them.
- **Adapter** — a concrete implementation of an interface that bridges to a specific technology, transport, or external service. In-memory adapters serve tests; HTTP/SDK/queue adapters serve production.
- **Leverage** — how much downstream work a single change at this seam buys. Deepening a high-leverage module simplifies many callers; deepening a low-leverage one moves complexity around without saving anyone work.
- **Locality** — how much a reader must hold in working memory to understand a module. High locality = fewer files and fewer hops to grasp the behavior.

## Invocation Position

This is a side-route skill for architecture exploration rather than a default feature-delivery step.

Use `/improve-codebase-architecture` when the user wants to find deeper structural improvements, identify shallow-module pain, or turn architectural friction into refactor opportunities.

May also be invoked from `/triage-issue` when a bug exposes a missing test seam — i.e., the right call site for a regression test does not exist as a public, observable surface. In that case, bring the specific call-site pattern with you (the bug, the path it traverses, and why no current seam exercises it). The deepening candidate is the module that should expose that seam.

Do not use it when the work is already a concrete implementation task for `/execute`, or when the next need is a specific refactor plan rather than exploratory architecture analysis — that belongs in `/request-refactor-plan`.

## Process

### 1. Explore the codebase

Use the Agent tool with subagent_type=Explore to navigate the codebase naturally. Do NOT follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small files?
- Where are modules so shallow that the interface is nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called?
- Where do tightly-coupled modules create integration risk in the seams between them?
- Which parts of the codebase are untested, or hard to test?

The friction you encounter IS the signal.

### 2. Present candidates

Before adding a candidate to the list, run two filters. Both compress otherwise-judgmental architecture decisions into checks that anyone reading the recommendation can re-run.

- **Deletion test.** Imagine the candidate module deleted in place. Where does its complexity go? If the complexity vanishes — callers were doing the real work and the module was a pass-through that just renamed things — the candidate is a real deepening target. If the complexity concentrates across N callers — they would each need to re-derive what the module was doing — the module is already carrying real abstraction; leave it alone. A pass-through whose deletion makes callers simpler is a shallow module hiding behind a thin name.
- **Two-adapters rule** (only when the candidate's design would introduce a new seam — i.e., add an interface that did not exist before). Confirm there are at least two real adapters: production *and* test, or two production transports. One adapter is a hypothetical seam — speculative generality with no second user — and should be deferred until a second consumer exists. Two adapters is a real seam worth defining.

Candidates that fail either filter are noted as "considered and rejected" with the reason, not silently dropped — the rejection is part of the recommendation.

Present a numbered list of the candidates that pass. For each, show:

- **Cluster**: Which modules are involved
- **Why they're coupled**: Shared types, call patterns, co-ownership of a concept — fold in a one-sentence summary of what the Deletion test surfaced (what hides behind the current interface, or what the pass-through shows)
- **Dependency category**: See [REFERENCE.md](REFERENCE.md) for the four categories
- **Test impact**: What existing tests would be replaced by seam tests at the deepened module's interface

Do NOT propose interfaces yet. Ask the user: "Which of these would you like to explore?"

### 3. User picks a candidate

### 4. Frame the problem space

Before spawning sub-agents, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would need to rely on
- A rough illustrative code sketch to make the constraints concrete — this is not a proposal, just a way to ground the constraints

Show this to the user, then immediately proceed to Step 5. The user reads and thinks about the problem while the sub-agents work in parallel.

### 5. Design multiple interfaces

Spawn 3+ sub-agents in parallel using the Agent tool. Each must produce a **radically different** interface for the deepened module.

Prompt each sub-agent with a separate technical brief (file paths, coupling details, dependency category, what's being hidden). This brief is independent of the user-facing explanation in Step 4. Give each agent a different design constraint:

- Agent 1: "Minimize the interface — aim for 1-3 entry points max"
- Agent 2: "Maximize flexibility — support many use cases and extension"
- Agent 3: "Optimize for the most common caller — make the default case trivial"
- Agent 4 (if applicable): "Design around the ports & adapters pattern for dependencies that cross a process or network seam"

Each sub-agent outputs:

1. Interface signature (types, methods, params)
2. Usage example showing how callers use it
3. What complexity it hides internally
4. Dependency strategy (how deps are handled — see [REFERENCE.md](REFERENCE.md))
5. Trade-offs

Present designs sequentially, then compare them in prose.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not just a menu.

### 6. User picks an interface (or accepts recommendation)

### 7. Create GitHub issue

Create a refactor RFC as a GitHub issue using `gh issue create`. Use the template in [REFERENCE.md](REFERENCE.md). Do NOT ask the user to review before creating — just create it and share the URL.

## Handoff

- **Expected input:** architectural friction, testability pain, or coupled-module concerns that are not yet shaped into a refactor plan
- **Produces:** candidate deepening opportunities and a refactor RFC issue
- **May be triggered by:** direct user request, or a structural signal surfaced during `/triage-issue` or review work
- **Feeds back into:** `/request-refactor-plan` for detailed sequencing, or `/execute` when a chosen refactor is ready to execute
