---
name: exploit-development
description: Authorized exploit development and vulnerability research skill for lab environments, CTFs, owned software, crash analysis, memory corruption, exploitability assessment, fuzzing results, proof-of-concept design, and remediation. Use for defensive validation and education; avoid real-world weaponization, stealth, persistence, evasion, or unauthorized targets.
---

# Exploit Development

## Authorization Boundary

- Work only on owned code, lab targets, CTFs, or explicitly authorized research.
- Keep proof of concept minimal: demonstrate the bug and impact without persistence, evasion, automated exploitation at scale, or post-exploitation.
- Prefer root-cause analysis, exploitability classification, mitigations, and regression tests.

## Workflow

1. Establish target version, build flags, architecture, mitigations, input vector, and crash artifact.
2. Reproduce deterministically in an isolated lab with symbols and sanitizer output when possible.
3. Triage root cause: bounds, lifetime, type confusion, race, injection, logic flaw, or unsafe parser behavior.
4. Assess exploitability at a high level: control of instruction pointer, write primitive, info leak, sandbox, and mitigations.
5. Provide a safe PoC or pseudocode only as needed to validate impact, then produce patch guidance and tests.

## Defensive Outputs

- Crash summary with environment and reproduction constraints.
- Root-cause explanation tied to source or disassembly.
- Severity rationale and affected versions.
- Patch strategy, hardening recommendations, and regression/fuzz tests.

