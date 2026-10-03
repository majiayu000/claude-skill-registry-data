---
name: software-assurance
description: Route dependency risk, performance diagnosis, and risk-based test design before accepting or releasing software changes.
---

# Software Assurance

Choose one primary mode and read only its workflow. Add another mode only when its distinct evidence is required.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `dependency-risk-triage` | Assess upgrades, advisories, transitive risk, compatibility, licensing, or lockfiles. | [Dependency-risk triage](references/workflows/dependency-risk-triage.md) |
| `performance-profiling` | Establish a baseline, measurement plan, bottleneck, regression, or acceptance threshold. | [Performance profiling](references/workflows/performance-profiling.md) |
| `test-matrix-design` | Map requirements and failure risks to test layers, fixtures, commands, and release gates. | [Test-matrix design](references/workflows/test-matrix-design.md) |

Do not load sibling workflows or artifacts prospectively. Do not treat an unexecuted, zero-case, unstable, or unrepresentative check as validation evidence.
