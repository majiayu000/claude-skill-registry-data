---
name: mapping-architecture
description: Use when needing component relationships, layer boundaries, module structure, or understanding how parts of a codebase fit together before modification or refactoring
---

## Announce at start: "Using codebase-analyzer to map the architecture."

## Overview

Map the codebase's structural architecture: components, layers, boundaries, and communication patterns.

## Process

1. Identify entry points (main files, index files, routing, public API exports)
2. Map directory structure to logical layers (presentation, business, data, infrastructure)
3. Trace component boundaries — which dirs/modules form cohesive units
4. Identify cross-cutting concerns (auth, logging, config, error handling)
5. Map communication between components (imports, function calls, events, message queues)
6. Find shared state and coupling points

## Quick Reference

Directory names suggest layers, but imports reveal the truth. Use the table as a starting hypothesis, then verify with actual import analysis.

| Signal | Hypothesized Layer | What to verify |
|--------|--------------------|----------------|
| routes/, pages/, views/, controllers/ | Presentation | Do these import only from business/data, or do they bypass directly to infrastructure? |
| services/, domain/, business/, use-cases/ | Business Logic | Do these stay free of framework/DB imports, or are they coupled to infrastructure? |
| models/, repositories/, data/, db/ | Data Access | Do these have business logic mixed in (validations, calculations in models)? |
| config/, middleware/, utils/, lib/ | Infrastructure | Check fan-in: if everything imports from here, it may be a hidden god module |
| tests/, __tests__/, spec/ | Test | Are tests colocated with code (unit) or separated (integration)? |

## Trigger Signals

- **HIGH confidence**: Generated code mixed with hand-written (e.g., GraphQLcodegen output in src/) -> `trace-codebase-provenance`
- **HIGH confidence**: Hidden/private modules not referenced from entry points -> `classify-repo-artifacts`
- **MEDIUM confidence**: Unclear layer boundaries, tangled imports -> `tracing-dependencies`
- **LOW confidence**: Clean separation, well-defined layers -> no deep dive needed

## Layer Violation Detection

The declared directory structure is the team's aspiration. The import graph is reality. When these diverge, the architecture doc is lying.

**How to detect violations:**
1. If `services/` imports from `controllers/`, the layer boundary is violated. Map ACTUAL dependency flow, not declared structure. Directory names lie; imports tell the truth.
2. If every module imports from `utils/shared`, you don't have a shared layer -- you have a hidden god module. The import fan-in reveals more than directory structure.
3. If a "domain" layer imports a database driver or HTTP client, it isn't a domain layer -- it's infrastructure in disguise. The dependency direction determines the layer, not the folder name.

**Diagnostic reasoning (not lookup tables):**
- If X imports from Y, and Y is declared as a lower layer, this isn't actually layered -- it's a different pattern. Name what it really is.
- Bidirectional imports between two directories mean they form a single coupled component, not two separate layers.
- A module imported by everything else isn't "shared infrastructure" -- it's the actual center of the architecture.

## SECURITY_SIGNAL

Watch for these during layer mapping:
- Auth logic in presentation layer (controllers handling permissions)
- Data access without authorization checks (repositories bypassing auth)
- Mixed public/private endpoints in the same module
- Secrets or credentials in configuration modules that presentation layer can reach
- Cross-cutting security concerns handled inconsistently across layers

## Adversarial Lens

If the team wanted to hide a backdoor, where in this architecture would they put it? Look for: utility modules that everything imports from (god modules with hidden functionality), middleware that sees all requests, "config" modules that execute code. The best hiding spots are where nobody looks.

## Red Flags

- Assuming directory names map directly to layers without verification
- Missing internal packages that aren't obvious from top-level structure
- Not checking for generated code markers
- Trusting the "architecture.md" in the repo without verifying against imports

## When NOT to Use

- When you only need a quick "what does this project do?" -- check the README instead.
- When the codebase is under 10 files -- the architecture is trivially visible.
- When you need runtime behavior, not static structure -- use tracing/profiling tools instead.

## Output Contract

Write `docs/analysis/architecture.md` using standard contract.
Include: layer diagram, component list, cross-cutting concerns, coupling points.
