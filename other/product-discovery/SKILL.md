---
name: product-discovery
description: This skill should be used when the user has a product idea but is not sure what to build, what the MVP is, or where to start. Trigger phrases include "I have an idea for a product", "not sure what to build", "what should the MVP be", "where do I start", "is this idea any good", "help me scope this", "I want to build something but". Inspired by Design Sprint and Lean Startup. It separates the problem from the solution, validates the market, and defines a prioritized MVP.
---

# Product Discovery

This skill turns a fuzzy idea into a sharp, buildable MVP. It is inspired by Design Sprint and Lean Startup, and it resists the urge to jump to features before the problem is understood.

Analogy: do not prescribe medicine before diagnosing the illness. Most failed products are perfectly built cures for a disease nobody has.

## Workflow

### PHASE 1 — Understand the problem (not the solution)

Force the conversation onto the problem first. Ask:

- What specific problem are you solving?
- Who has that problem? Describe that person concretely.
- How do they solve it today? (even if it is Excel, WhatsApp, or by hand)
- Why is that current solution not good enough?

Do not let the discussion drift to features yet. If the user describes a solution, redirect to the problem it serves.

### PHASE 2 — Validate the market

- Do you (or your target users) already pay for something similar? How much?
- Do you know other people with this same problem?
- Do you have access to potential customers to validate with?

The goal is evidence that the problem is real and painful enough that someone will pay.

### PHASE 3 — Define the MVP

- What is the minimum result that would make someone pay?
- Which features are "nice to have" but not essential?
- How soon do you want something to show?

The MVP is the smallest thing that delivers the core result — not a small version of the full vision.

### PHASE 4 — Output

Deliver these five items:

1. **Problem definition** — in one sentence.
2. **Ideal customer avatar** — who they are, concretely.
3. **MVP scope** — a prioritized feature list:
   - **P0** — must exist for the MVP to deliver its core result.
   - **P1** — important, but can wait for v1.1.
   - **P2** — nice to have; explicitly deferred.
4. **Success metric** — how we will know it worked (e.g. "10 paying users in 30 days," "40% of signups complete the core action").
5. **Concrete next step** — the single next action to take.

## Handoff

Once the MVP is defined, hand off to `architecture-primer` to decide how to build it, then `ui-design` to build the interface. Discovery answers (scale expectations, user type, timeline) feed directly into the architecture discovery phase — pass them along.
