---
name: tla-tooling-and-agents
description: Tool integration agent loops iterative repair and advanced workflows for TLA+ including SANY TLC TLAPS grammar constraints Specula-style generation and closed-loop specification agents. Use when improving generation quality with feedback when discussing model checking or when building AI agents that write and verify TLA+.
---

# Tooling and Agent Workflows

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. Tools exist to support the mathematical discipline of Specifying Systems, not to replace it. Prefer progressive generation and iterative repair that keep the specification readable and faithful to the sample-behavior and abstraction principles of the book.

## Overview

Raw next-token generation of TLA+ is weak. Closed-loop agents that can invoke the formal tools and repair based on feedback are dramatically stronger. This skill defines the recommended agentic patterns.

## Essential Tools

- **SANY** — the parser and static analyzer. Every generated module must pass SANY before further work.
- **TLC** — the model checker. Use it for both safety and (with fairness) liveness. Prefer small models first then scale.
- **TLAPS** — the proof system. Use when model checking becomes intractable and inductive invariants must be proved.
- Grammar-constrained decoding (GBNF Guidance or equivalent) — enforce syntactic validity at generation time.
- Trace validation harnesses — compare real execution traces against the model (as in Specula).

## Recommended Agent Loop

1. Generate a candidate module (or PlusCal) using progressive decomposition (module skeleton then variables then Init then actions then Spec then properties).
2. Run SANY. On error repair the exact construct cited and re-check.
3. Run TLC on a small configuration. On counterexample analyze the trace explain the violation and strengthen the model or the invariant.
4. Iterate until SANY is clean and the desired properties hold on the explored state space.
5. If needed add history variables or refine the abstraction and repeat.

## Progressive Generation Pattern

Never emit a full complex specification in one shot. Generate and validate layer by layer

- Module header and EXTENDS
- VARIABLES and TypeOK
- Init
- Individual actions (one at a time)
- Next and Spec including fairness
- Invariants and temporal properties

This matches the only prompting strategy that has shown non-zero semantic success rates in systematic evaluations.

## Advanced Patterns

- Specula-style code-to-spec with control-flow analysis and iterative TLC repair.
- Grammar + documentation retrieval for local models.
- Multi-module refinement hierarchies with explicit refinement mappings.
- Integration of TLA+ as a grounding signal for code generation agents (spec-first then implementation).

## When Tools Are Unavailable

Still reason as if the tools were present. Anticipate the most likely SANY errors and TLC counterexamples. Prefer models that are obviously inductive and that keep the state space small.

The goal of every agentic workflow is a specification that is both mathematically correct and faithful to the system under study.
