---
name: trace
description: Follow a request end-to-end through the stack from route to database
type: review
version: v0.1
---

# Trace

Invoke as `$trace`.

Use this skill when the user wants to understand how a specific route, endpoint, or feature flows through the application stack.

## Process

1. Identify the entry point from the user's description.
2. Read CLAUDE.md for architecture context.
3. Trace forward through each layer: entry point → middleware → business logic → data access → response.
4. Map the data flow and types at each boundary.
5. Identify concerns: N+1 queries, auth gaps, type mismatches, performance issues.

## Output

- **Visual trace**: entry → middleware → handler → service → DB → response with file:line refs
- **Layer-by-layer detail**: file, inputs, outputs, what it does
- **Data flow**: how data transforms through the stack
- **Concerns found**: issues identified during the trace

## Constraints

- Follow actual code paths — do not guess from naming.
- Read each file in the chain.
- Do not modify any code — read-only analysis.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
