---
name: tla-refinement
description: Refinement in TLA+ including refinement mappings successive refinement and proving that one specification implements another. Use when moving from a high-level specification to a lower-level one or when verifying that an implementation satisfies an abstract specification. Trigger on refinement mappings implementation proofs or stepwise refinement.
---

# TLA+ Refinement

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. Refinement is the mathematical relationship that connects an abstract specification to a more concrete one. Follow the discipline of Specifying Systems: a lower-level specification implements a higher-level one when every behavior of the lower-level specification (under a refinement mapping) is a behavior of the higher-level specification.

## Overview

Refinement is the primary way large systems are developed and verified in TLA+. An abstract specification SpecA is refined by a more concrete specification SpecC when there exists a refinement mapping that makes every behavior of SpecC correspond to a behavior of SpecA.

## Core Concepts

- **Refinement mapping**: A mapping from the variables (and possibly auxiliary variables) of the concrete specification to the variables of the abstract specification.
- **Implementation**: SpecC implements SpecA under refinement mapping f if SpecC ⇒ SpecA with the variables of SpecA replaced by their images under f (plus possible stuttering).
- **Successive refinement**: A chain of specifications Spec0 ⇐ Spec1 ⇐ Spec2 … where each step is a refinement. This is the normal industrial development path.
- **Auxiliary variables**: History variables, prophecy variables, or other auxiliary state may be added to the concrete specification to make the refinement mapping possible.
- **Stuttering**: The concrete specification is allowed to take steps that leave the abstract state unchanged.

## Practical Discipline

1. Begin with a clear high-level specification that captures the essential safety (and if needed liveness) properties.
2. Decide what additional detail the next level must expose.
3. Write the concrete specification.
4. Construct an explicit refinement mapping (usually as a TLA+ operator or set of definitions).
5. Prove or model-check that the concrete specification, under the mapping, satisfies the abstract specification.
6. Hide internal variables of the concrete level that are not part of the interface to the next higher level.

## Common Pitfalls

- Claiming refinement without an explicit mapping.
- Forgetting that the concrete specification may stutter relative to the abstract one.
- Adding so much detail that the state space becomes intractable before the interesting properties have been checked at higher levels.
- Confusing data refinement with algorithmic refinement.

## When to Invoke This Skill

Invoke whenever the user moves from an abstract design to a more detailed design, when verifying that code or a lower-level model satisfies a higher-level specification, or when structuring a multi-level development.
