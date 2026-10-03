---
name: leeway-quantum-readiness
description: Makes LeeWay skills quantum-aware and hybrid-ready without falsely claiming classical agents are quantum computers. Governs quantum/hybrid capability detection, backend provenance, circuit/job evidence, error/noise boundaries, classical fallback, post-quantum awareness, and promotion of verified quantum accelerators into the skill graph.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: conditional-core-technology-readiness
  stage: capability-readiness
  compatibility: Agent Skills / GitHub Copilot / Codex / MCP / OpenCode / Hermes / quantum-hybrid adapters
---

# LeeWay Quantum Readiness

## Core law

LeeWay must be ready to use quantum computing when real quantum or verified quantum-simulation capability is available, while remaining fully correct on classical hardware.

Quantum-aware does **not** mean quantum-executed.

Never claim quantum speedup, quantum state, entanglement, amplitude behavior, annealing advantage, error correction, hardware execution, or quantum supremacy/advantage unless the relevant runtime and evidence actually support the claim.

## Hybrid-first architecture

Preferred design:

`LeeWay Context/Formula → capability classifier → classical path | quantum/hybrid path → runtime → Veritas → receipt`

Every quantum-capable workflow must define a classical fallback unless the task is inherently quantum-specific.

## Capability states

Use precise states:

- `QUANTUM_NOT_RELEVANT`
- `QUANTUM_AWARE_CLASSICAL_ONLY`
- `QUANTUM_SIMULATOR_AVAILABLE`
- `QUANTUM_HARDWARE_AVAILABLE`
- `QUANTUM_HYBRID_EXECUTED`
- `QUANTUM_EXECUTED`
- `QUANTUM_BLOCKED`
- `QUANTUM_FAILED`

Do not substitute simulator execution for hardware execution.

## Quantum evidence contract

When quantum execution occurs, preserve when available:

- provider/runtime identity;
- backend/device identity;
- SDK/compiler/runtime version;
- circuit/program representation identity;
- circuit/program hash;
- transpilation/compilation settings;
- qubit count / logical problem size;
- shot count or execution sampling policy;
- seed when applicable;
- queue/job/execution ID;
- calibration/noise snapshot identity when exposed;
- mitigation method if used;
- raw measurement/result artifact;
- classical preprocessing/postprocessing;
- comparison baseline;
- Veritas measurements;
- final receipt.

## Math boundary

Keep these distinct:

- theoretical quantum algorithm complexity;
- simulated performance;
- noisy-hardware observed performance;
- fault-tolerant projections;
- end-to-end application performance.

Do not turn asymptotic theoretical advantage into a real-world speed claim without measurement.

## Error/noise law

Distinguish:

- noise characterization;
- error mitigation;
- error detection;
- quantum error correction;
- fault tolerance.

These are not interchangeable.

## Skill graph integration

A skill may declare relationships such as:

- `quantum_accelerable`
- `quantum_native`
- `hybrid_preferred`
- `classical_fallback`
- `post_quantum_security_relevant`

Quantum capability is selected only when Context Engineering and Formula Governance determine that it materially improves the task and the runtime evidence supports the route.

## Quantum-ready data contracts

Where practical, keep problem representations backend-neutral so future quantum adapters can consume them without rewriting the entire skill.

Separate:

`problem definition → mathematical representation → backend adapter → execution artifact → verification`

Avoid binding domain logic directly to one provider SDK unless the skill is provider-specific.

## Post-quantum awareness

Quantum readiness also includes security transition awareness. When cryptographic longevity matters, distinguish current cryptography, migration planning, and post-quantum cryptographic requirements. Do not invent compliance requirements or algorithm status; consult current authoritative standards when making implementation decisions.

## Emerging technology law

Quantum technologies evolve quickly. Treat provider claims, benchmarks, roadmaps and research announcements as discovery evidence until independently verified for the actual task/runtime.

Route new quantum capabilities through `leeway-skill-lifecycle-governance` before promotion.

## Output law

When quantum capability materially affects a decision, explain it in plain engineering language:

`what problem class → why quantum/hybrid might help → what backend actually ran → what was measured → what remains classical → what is still unproven`.
