---
name: do297
description: "Use when scoping an IMA platform, planning module acceptance, or laying out development assurance steps for an integrated modular avionics system. Plan the integrated modular avionics (IMA) platform architecture in the spirit of DO-297: identify the IMA modules, application partitions, and shared resources, allocate applications to partitions with CPU, memory, and I/O budgets, and check the allocation for resource contention against integrity and availability requirements. Produce the module and application allocation plan, the resource budget table, and the module acceptance criteria that support incremental certification of the platform. Trigger: integrated modular avionics, IMA architecture, module acceptance, incremental certification, partition allocation, resource budget."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: do-178c
    reference-only: true
  - id: do-254
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: ima
  tags: [integrated-modular-avionics, do297, module-acceptance, incremental-certification, partition-allocation, resource-budget, cpu-memory-io, integrity-requirements, ima-architecture, shared-resources]
  version: 0.1.0
  author: Aero Agent Skills
---

# DO-297 IMA Architecture and Acceptance (avionics/ima/do297)

Use when the task is integrated modular avionics (IMA) architecture and
acceptance planning for civil avionics in the spirit of DO-297: identify
the platform modules, partitions, and shared resources, allocate
applications to partitions with CPU, memory, and I/O budgets, check for
resource contention, map integrity and availability requirements, and lay
out module acceptance and incremental certification evidence. The module
is data-driven: you supply the module resources and the application list
with integrity and availability requirements, and the functions allocate
applications to partitions, compute partition and module budgets, flag
over-subscription, and generate deterministic acceptance criteria.

This leaf covers the IMA integration and acceptance process. It is
different from avionics/ima/ima-partitioning, which sizes the ARINC 653
partition schedule, major frame, and inter-partition communication ports.

## Domain quick reference

- DO-297 (proprietary RTCA guidance; name and paraphrase only here)
  describes the IMA development and integration approach: a platform of
  modules hosts multiple applications in isolated partitions, acceptance
  evidence is gathered at module and application level, and incremental
  certification lets an accepted module or application be reused with
  reduced re-verification.
- Platform elements: modules (line replaceable units that host
  partitions), applications (functions hosted inside partitions), and
  shared resources (CPU time, memory, I/O ports, buses, power).
- Allocation rule: each application runs in exactly one partition, one or
  more partitions share a module, and every partition budget must fit
  inside the module resources in every dimension.
- Contention: when the summed demand of the hosted applications exceeds a
  module budget dimension (CPU, memory, or I/O), the platform is
  over-subscribed and the offending application must be flagged.
- Integrity levels: derived from failure-condition severity
  (catastrophic maps to level A, hazardous to B, major to C, minor to D,
  no effect to E), consistent with the DO-178C software level approach
  (referenced only; see standards-map.yaml).
- Availability classes: class 1 functions must remain available on
  demand, class 2 permits loss of function with a warning, class 3
  permits loss of function without a warning.
- Module acceptance: evidence that the module hosts its allocated
  applications within resource budgets and preserves failure containment
  between partitions. Incremental certification records the accepted
  module configuration so later applications reuse it with limited
  re-acceptance.

## IMA architecture model

- Module: name, cpu_units, memory_bytes, io_ports.
- Application: name, integrity (A-E), availability (1-3), cpu_units,
  memory_bytes, io_ports.
- Partition: hosts one or more applications; the partition budget is the
  sum of the demands of the applications it hosts.
- Module totals: sum of the demands of every partition on the module.
- Acceptance criteria: deterministic statements covering platform
  definition, module acceptance testing, resource usage verification,
  failure containment, availability demonstration, and incremental
  certification credit.

## Workflow

1. Identify the platform: list the modules with their CPU, memory, and
   I/O budgets.
2. Identify the applications with their integrity and availability
   requirements; map failure-condition severity to integrity level.
3. Allocate applications to partitions (one partition per application by
   default, or group applications into shared partitions).
4. Compute the partition budgets and the module totals; check every
   dimension against the module budget.
5. Run the contention check: any dimension over budget flags the
   over-budget application for re-allocation or module upgrade.
6. Generate the module acceptance criteria for the incremental
   certification record.
7. Lay out the development assurance steps per integrity level.

## Worked example

A module has 100 CPU units, 1,000,000 bytes of memory, and 16 I/O ports.
Three applications are hosted:

- FMS: integrity A, availability class 1, 40 CPU, 400,000 bytes, 6 ports.
- ADIRU: integrity B, availability class 1, 30 CPU, 300,000 bytes, 4 ports.
- Display: integrity C, availability class 2, 20 CPU, 200,000 bytes, 3 ports.

Module totals: 40 + 30 + 20 = 90 CPU, 900,000 bytes, 13 ports. Every
dimension fits with slack 10 CPU, 100,000 bytes, 3 ports, so the
allocation is accepted with no contention. If FMS grows to 60 CPU units
the total becomes 110 CPU against a budget of 100, the contention check
flags FMS as the over-budget application, and the module must either drop
the growth or move an application to another module.

## Pitfalls

- Checking applications against the module budget one at a time: the
  contention check sums the demand of every hosted application per
  dimension - FMS at 40 CPU fits alone, but with ADIRU and Display the
  module total is 90, and FMS growing to 60 pushes the total to 110
  against the 100 CPU budget, flagging FMS as the over-budget
  application.
- Verifying only one resource dimension: the module budget must hold
  in CPU, memory, and I/O ports at once - an allocation that fits 90
  of 100 CPU units can still bust the 16-port I/O budget, so every
  dimension needs its own total-versus-budget check.
- Double-counting partition demand: the module total is the sum of the
  partition budgets, and each partition budget is the sum of the
  applications it hosts - an application grouped into a shared
  partition must not also be counted at the module level on its own.
- Confusing integrity with availability: integrity levels A-E come
  from failure-condition severity (catastrophic to A, hazardous to B,
  major to C), while availability classes 1-3 say whether loss of
  function is permitted and whether it warns - a class 1 display is
  not automatically level A, and a level D function can still demand
  class 1 availability.
- Treating module acceptance as a one-time certificate: incremental
  certification records the accepted module configuration so later
  applications reuse it with limited re-acceptance - a changed module
  (an application moving in or a budget growing) changes the accepted
  configuration and re-opens the acceptance evidence.
- Routing software-lifecycle questions here: DO-297 is the platform
  integration and acceptance frame (name and paraphrase only - the
  text is proprietary RTCA guidance); per-application software
  assurance belongs to the DO-178C leaves and partition scheduling to
  avionics/ima/ima-partitioning.

## Behavior contract (gate 3)

Run the deterministic contract test (stdlib unittest, offline):

    python3 scripts/test_do297.py
