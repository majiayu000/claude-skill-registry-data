---
name: "architecture-strategy-expert"
description: "Master guide for architecture documentation and technical contracts. Covers ADR (Architecture Decision Records), Design by Contract, and C4 modeling."
---

# Architecture Strategy Expert Guide

This skill provides the standards for documenting and enforcing high-level architectural decisions and technical boundaries.

## 📜 ADR (Architecture Decision Records)
- **Context**: Describe the problem and the current state.
- **Decision**: State the chosen path clearly.
- **Rationale**: Explain WHY the choice was made, including trade-offs.
- **Consequences**: Document the impact (positive or negative) of the decision.

## 🤝 Design by Contract (DbC)
- **Preconditions**: Validate inputs at the module boundary.
- **Postconditions**: Guarantee the state and return value after execution.
- **Invariants**: Maintain system consistency across all operations.

## 📐 Modeling (C4)
- **Context**: Show the system in its environment.
- **Container**: Decompose the system into independent deployable units.
- **Component**: Show the internal structure of containers.

## 🔗 References
- [ADR Github Org](https://github.com/adr)
- [C4 Model](https://c4model.com/)
