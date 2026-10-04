---
name: offspine-experiment-discipline
description: Use when running research prototypes beside a requirement-traced process (experiments that inform decisions but must not corrupt traceability) — deterministic pinned-input scripts that print their own honest verdict, findings recorded with numbers (negative ones especially), and a resume surface a successor can pick up cold.
stacks: [python, any]
domains: [any]
phases: [dev]
tags: [experiments, determinism, reproducibility, findings, resume, process]
scope: kit
---
**When to use.** Any prototype/research work in a gated repo. *Why:* the experiments lane's value is
that any session — or any successor — can re-run and extend it; an unrecorded conclusion or an
unreproducible number is the failure mode.

**Procedure.**
1. Keep experiments off the requirement spine by contract (no registry rows; conclusions to the
   design doc, scripts as evidence, promotable cores named for later placement).
2. Pin inputs and seed randomness (`cv2.setRNGSeed` etc.); separate camera/hardware-dependent steps
   from headless ones and pin the regeneration commands for the former.
3. Scripts end with an explicit verdict line + matching exit code, including designed reds
   (`INSUFFICIENT OVERLAP`, "met, but saturated") — honest nonzero exits are recorded facts.
4. Record findings with numbers, negative results first-class; flag interpreted defaults as
   veto-able; when metrics change, keep the old number as a reference column.
5. Maintain the resume surface every session: where it stands, exact resume commands, the human's
   bench errands as copy-pasteable blocks with consequences stated.
6. **Done when:** a fresh clone can run the headless set and reproduce the cited numbers, and a cold
   session can resume from the surface without re-surveying the repo.

**Knowledge:** FIELD-KNOWLEDGE-GILBERT.md §G1 + §G4.
