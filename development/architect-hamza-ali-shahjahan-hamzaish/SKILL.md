---
name: architect
description: Define a product's architecture BEFORE Claude Code writes a line. Produces CLAUDE.md, scope.md, and a 1-page architectural decisions doc.
---

# Architect

## When you activate
Before any new product gets code. User says: "let's set up X", "architecture for Y", "start the build for Z".

## What you produce
Three files for the new product:
1. `products/<name>/CLAUDE.md` — Claude Code's working instructions for this codebase
2. `products/<name>/scope.md` — what it does / deliberately doesn't
3. `products/<name>/decisions/0001-architecture.md` — the founding ADR

Use templates from `templates/claude-md-template.md` and `templates/scope-doc-template.md`.

## Protocol
1. Read the validated problem statement (output of `idea/problem-sharpener`) and discovery synthesis (output of `idea/interview-synthesizer`).
2. Read `stack/tech-stack.md` and `stack/stack-selection.md`. Default to the standard stack unless the matrix says deviate.
3. Read `knowledge-base/mvp-stage/architecture-decisions.md`.
4. Talk through with the user:
   - **What this product solves** (1 sentence)
   - **Who it serves** (the validated persona)
   - **6-month scale expectation** (10 users / 1000 / 100K?)
   - **The 1 thing that must be true architecturally** (real-time? offline-first? regulated data? ML inference path?)
5. Generate the three files. The CLAUDE.md includes: project goal, tech stack, dependencies-to-avoid, the must-be-true thing, persona for code style, references to scope.md and decisions/.
6. The scope.md uses the template format strictly. Don't paraphrase — every section gets filled.
7. The first ADR captures: stack chosen, deviations from default (if any) with reasons, and the 3 assumptions the architecture rests on.

## Sources
- `knowledge-base/mvp-stage/architecture-decisions.md`
- `knowledge-base/mvp-stage/claude-md-templates/` (pick the best-fitting one)
- `stack/tech-stack.md`
- `stack/stack-selection.md`

## What you don't do
- Don't open Claude Code yet. Architecture comes first.
- Don't recommend a deviation from the default stack without writing it as an ADR with a reason.
- Don't write more than 1 page for any of the three files. Density > volume.
