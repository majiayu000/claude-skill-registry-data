---
name: faa-req-handbook
description: "Knowledge base from the FAA Requirements Engineering Management Handbook (DOT/FAA/AR-08/32). Use for writing requirements for real-time, embedded control systems — the avionics/medical slant — via the Handbook's eleven recommended practices: system overview and boundary (monitored/controlled variables), operational concepts (use cases), environmental assumptions, change-tolerant functional architecture (dependency diagrams), safety-driven architecture revision (FHA/PSSA/fault tree), system modes, detailed behavior and performance requirements (ideal value + tolerance + latency), the four-variable model bridge to software requirements (MON/CON/NAT/REQ, IN'/REQ'/OUT', DO-178B mapping), subsystem allocation, and rationale. Carries the Isolette Thermostat and Flight Control System worked examples. Slanted toward control systems with sensors and actuators; thin on information-system / enterprise / agile requirements, on requirements-management tooling, and on the formal-methods internals of SCR/RSML/SpecTRM (it names them, does not re-teach them). Does not reproduce the IEEE/DO-178B/ARP standards it cites."
---

<!-- argument-hint: [recommended practice, monitored/controlled variable, use case, environmental assumption, functional architecture, mode, detailed requirement, four-variable model, software requirement, allocation, rationale, chapter number] -->

# FAA Requirements Engineering Management Handbook (DOT/FAA/AR-08/32)
**Source**: DOT/FAA (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill when you must turn a fuzzy idea of an embedded control system into a complete, testable, change-tolerant requirements specification — and especially when system-level requirements have to hand off cleanly to software requirements. It is the avionics/medical-control complement to general requirements-writing craft: where domain-neutral guidance asks for "complete, consistent, clear" requirements, this Handbook shows the concrete machinery — typed monitored/controlled variables, validity status on every input, explicit latency and tolerance budgets, fail-safe modes, and rationale on every value. Pair it with the `requirements-writing` pack (sentence-level craft) and the safety packs (`faa-system-safety`, `mil-std-882`).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the eleven recommended practices, the monitored/controlled boundary, the functional architecture, the requirement structure (ideal value + tolerance + latency), and the four-variable model.
- **With a topic** — ask about a practice (e.g. "operational concepts", "environmental assumptions", "subsystem allocation"), a concept (e.g. "latency rationale", "mode confusion", "UNSPECIFIED", "four-variable model"), or one of the worked examples (Isolette, FCS/FGS/Autopilot).
- **With a chapter** — `ch02` (boundary), `ch03` (operational concepts/assumptions), `ch04` (architecture), `ch05` (modes/detailed requirements), `ch06` (software/allocation), `ch07` (rationale), `ch08` (worked examples).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One criterion, eleven practices.** The Handbook's quality bar is the Parnas criterion — *specify everything needed for the correct system and nothing more* — which reduces to "say what, not how." The eleven recommended practices are eleven ways to hit that bar for real-time embedded systems. It is a synthesis of prior work (SCR, the four-variable model, CoRE, RSML/RSML-e/SpecTRM, textual use cases), not a brand-new method, and it expects to be tailored.

## Core Frameworks & Mental Models

### The eleven recommended practices
The spine of the Handbook is eleven main-level recommended practices (each with finer sublevels), presented in rough execution order with heavy iteration and tailoring expected:

1. **System overview** (2.1) — orient a new reader: synopsis, life-cycle contexts, external entities, goals.
2. **System boundary** (2.2) — the dividing line, defined as monitored and controlled variables.
3. **Operational concepts** (2.3) — black-box usage scenarios as textual use cases.
4. **Environmental assumptions** (2.4) — the obligations the system places back on its world.
5. **Functional architecture** (2.5) — group functions by what changes together; dependency diagrams.
6. **Revise for constraints** (2.6) — bend the ideal architecture to absorb safety/legacy/platform reality.
7. **System modes** (2.7) — the externally visible behavioral discontinuities and their transitions.
8. **Detailed behavior & performance** (2.8) — ideal value, tolerance, latency per variable.
9. **Software requirements** (2.9) — the four-variable extension from system to software.
10. **Subsystem allocation** (2.10) — split the spec into independently buildable subsystem specs.
11. **Rationale** (2.11) — the *why*, cited as the single most cost-effective practice.

### The system boundary = monitored & controlled variables
The boundary is not an org-chart box; it is the set of **monitored variables** (environmental quantities the system senses directly) and **controlled variables** (quantities it affects directly). The *elimination test* identifies them: a true boundary variable would still exist in the world if the system vanished. Keep variables abstract (a number with range and precision) — never a wire format like an ARINC 429 word — and define the lower, more volatile **physical interfaces** (discrete I/O, messages, fields, protocols) separately. Split a formatted display (altitude in blinking red) into its underlying value plus a status; rendering is HMI design, not boundary.

### Operational concepts via use cases; assumptions pointed outward
Before detailed requirements, describe the system as a black box through **use cases**: actors, primary actor, preconditions, postconditions, a **main success ("sunny day") scenario** first, then exceptions and alternate courses as extensions. Trace each to system goals, link steps to functions, and use the walkthrough as a discovery tool for missing variables. **Environmental assumptions** are requirements pointed outward — the obligations the system levies on its world, from type/range/units up to plant models. Assumptions + requirements form a **precondition/postcondition contract** that enables independent component development and safe reuse. Give every monitored variable a **status attribute** (Valid/Invalid, unknown/stale) so untrustworthy data forces a mode change rather than being silently used.

### Functional architecture: group by what changes together
A real specification cannot be a flat list. Organize requirements around a recursive **functional architecture** — group functions that are closely related and likely to change together (the Isolette's operator-facing functions collapse into one *Manage Operator Interface*). Draw **dependency diagrams** with monitored/controlled/internal variables as arrows. Label arrows with stable, high-level problem-domain concepts; seal volatile dependencies inside functions and push them deep, building **firewalls** against change. The structure doubles as traceability. Build the **ideal** architecture from the problem domain first (2.5), then **revise** it (2.6) to absorb safety, legacy, and platform constraints — deforming it as little as possible, since the problem domain outlasts any implementation.

### Safety drives revision: FHA → PSSA → fault tree
For safety-critical systems, safety analysis forces architecture revision. The **FHA** names hazards (Isolette H1: prolonged exposure to unsafe heat/cold, catastrophic, target < 10⁻⁹/hr); the **PSSA** finds which functions could realize them and, via a **fault tree**, apportions failure-probability budgets. When a per-component budget is infeasible or too costly, change the *architecture* (add an independent **Monitor**) rather than buy ultra-reliable parts — which relaxes the budget. Then follow the change through the full cascade: overview, operational concepts, exception cases, boundary, assumptions, diagrams, high-level requirements.

### Modes and the requirement structure
A **mode** is an *externally visible discontinuity* in behavior — the same stimulus produces different responses in INIT vs. NORMAL vs. FAILED. Only introduce a mode for an observable discontinuity; define every transition, including latching (FAILED persists until power cycle). Then write each detailed requirement as **condition (mode + variable constraints) → assignment of an ideal value**. Build the **ideal value function** variable by variable so every controlled/internal variable has exactly one value in every state; mark **UNSPECIFIED** — and document it — where none is meaningful. Enforce **completeness** (every state assigned), **consistency** (no state assigned twice — watch `<` vs. `<=`), and **non-duplication**; a condition/event/mode **table** makes the first two checkable by inspection. Attach **latency** (max lag) to every controlled variable and **tolerance** (allowed deviation) to every numerical one, each tethered by rationale to the environmental assumptions (the Isolette's 6-second heat latency comes from the 1°F/min drift and the sensor's 0.1°F resolution). Internal variables never get latency or tolerance.

### The four-variable model: system → software requirements
Software cannot touch real-world quantities, so software requirements are an **extension** of system requirements, built on the **four-variable model** (Parnas/Madey, via SCR): **MON, CON, NAT, REQ**, plus the **INPUT/OUTPUT** variables the software actually reads/writes and the **IN/OUT** relations between them. Split the raw software relation into **IN'** (recreate the monitored-variable images MON'), **OUT'** (drive outputs from controlled-variable images CON'), and **REQ'** (which reuses the system's ideal value function unchanged). IN'/OUT' are the *driver layer* (change when hardware changes); REQ' is the *application layer* (changes when behavior changes). Every input/output needs a definition, an accuracy bound, a latency bound, and a status attribute. Confirm the **end-to-end budget** survives sensing lag + actuation lag + computation time. Map artifacts onto **DO-178B** high-level/low-level requirements and flag **derived requirements** (design choices affecting visible behavior or safety) to the safety assessment. The prime mark (MON', CON') is a humility reminder: every software image is a delayed, slightly-wrong copy of reality.

### Subsystem allocation and rationale
For large systems, **allocate** by carving along function boundaries (FCS → Flight Guidance + Autopilot). Keep a duplicate of each allocated function and its high-level requirements in the parent so each subsystem's topmost requirement traces to an identical parent requirement. Expose the parent's internal variables as monitored/controlled variables at the subsystem interface; make each subsystem spec complete on its own; keep composed latencies/tolerances within the parent's end-to-end budgets. Finally, **rationale** records the *why* (separate from the *what* of requirements and the *how* of design) for non-obvious requirements, non-obvious assumptions, and every specific value or range. Capture it at the moment of authoring; keep it short; cite long documents rather than copying; and never park binding behavior in it (it is non-binding and never verified). The "93°F test": a bare safety-critical number without rationale invites a cost-driven substitution that could be fatal.

---

## Chapter Index

| # | Practices | Key content |
|---|-----------|-------------|
| [ch01](chapters/ch01-faa-req-handbook-foundations-and-introduction.md) | Foundations | What separates a good spec from a bad one (Parnas: "what, not how"); the named lineage (SCR, four-variable model, CoRE, RSML/RSML-e/SpecTRM, use cases); the eleven recommended practices; the two running examples |
| [ch02](chapters/ch02-faa-req-handbook-system-overview-and-boundary.md) | 2.1–2.2 | System overview (synopsis, contexts, goals); the boundary as monitored/controlled variables; the elimination test; abstraction over wire format; physical interfaces |
| [ch03](chapters/ch03-faa-req-handbook-operational-concepts-and-environmental-assumptions.md) | 2.3–2.4 | Operational concepts as textual use cases (sunny-day first); environmental assumptions as outward obligations; the precondition/postcondition contract; status attributes |
| [ch04](chapters/ch04-faa-req-handbook-functional-architecture-and-implementation-constraints.md) | 2.5–2.6 | Functional architecture grouped by change; dependency diagrams; firewalls; ideal vs. revised architecture; FHA/PSSA/fault tree driving safety revision; the change cascade |
| [ch05](chapters/ch05-faa-req-handbook-system-modes-and-detailed-requirements.md) | 2.7–2.8 | Modes as observable discontinuities and transitions; condition→assignment; ideal value function; completeness/consistency/non-duplication; latency and tolerance; tabular formats |
| [ch06](chapters/ch06-faa-req-handbook-software-requirements-and-subsystem-allocation.md) | 2.9–2.10 | The four-variable model; IN'/REQ'/OUT' extended software requirements; bit-level inputs/outputs; DO-178B mapping; derived requirements; subsystem allocation and composed budgets |
| [ch07](chapters/ch07-faa-req-handbook-rationale-and-summary.md) | 2.11 + Summary | Rationale as the *why* (three targets); non-binding; capture at authoring; the cost case; the "93°F test"; the Handbook's overall framing and tailoring message |
| [ch08](chapters/ch08-faa-req-handbook-worked-avionics-examples.md) | Appendices A–D | The Isolette Thermostat (deep, single-system) and the FCS/FGS/Autopilot trio (broad, allocation); concrete variable tables, modes, safety requirements, hysteresis, fail-safe defaults |

## Topic Index

- **Allocation / subsystem allocation** → ch06, ch08
- **And/or tables** → ch05
- **Architecture (functional)** → ch04
- **Architecture revision for constraints** → ch04
- **Boundary (system boundary)** → ch02
- **Completeness / consistency / non-duplication** → ch05
- **Context diagram** → ch02, ch08
- **Controlled variable** → ch02, ch05
- **CoRE methodology** → ch01, ch04, ch05
- **Deadband / hysteresis** → ch08
- **Dependency diagram** → ch04
- **Derived requirement** → ch06
- **Detailed behavior and performance requirements** → ch05
- **DO-178B / DO-248B mapping** → ch06
- **Elimination test** → ch02
- **Environmental assumptions** → ch03
- **Exception case / alternate course** → ch03, ch04
- **External entity** → ch02, ch03
- **FHA (Functional Hazard Assessment)** → ch04, ch08
- **Firewalls (against change)** → ch04
- **Four-variable model (MON/CON/NAT/REQ)** → ch06, ch01
- **Functions (system functions)** → ch04, ch03
- **Goals (system goals)** → ch02, ch07
- **Hazard / safety requirement** → ch08, ch04
- **Ideal value function** → ch05
- **IN' / REQ' / OUT' (extended software requirements)** → ch06
- **Internal variable** → ch04, ch05
- **Intent specification** → ch01
- **Isolette Thermostat (example)** → ch08
- **Latency** → ch05, ch06
- **Lineage (SCR / CoRE / RSML / SpecTRM / use cases)** → ch01
- **Mode** → ch05
- **Mode confusion** → ch05
- **Monitored variable** → ch02, ch05
- **NAT relationship (assumptions)** → ch03, ch06
- **Operational concepts** → ch03
- **Parnas criterion ("what, not how")** → ch01
- **Physical interface** → ch02
- **Precondition / postcondition contract** → ch03
- **PSSA / fault tree** → ch04
- **Rationale** → ch07
- **Recommended practices (the eleven)** → ch01
- **REQ relationship** → ch05, ch06
- **SCR (Software Cost Reduction)** → ch01, ch06
- **Software requirements** → ch06
- **Status attribute (Valid/Invalid, stale/unknown)** → ch03, ch06
- **System overview** → ch02
- **Tabular specification (condition/event/mode tables)** → ch05
- **Tolerance** → ch05
- **Traceability** → ch04, ch06
- **UNSPECIFIED** → ch05, ch08
- **Use cases** → ch03, ch08
- **Worked examples (Isolette; FCS/FGS/Autopilot)** → ch08

## Supporting Files

- [glossary.md](glossary.md) — key terms (monitored/controlled variables, four-variable model, ideal value function, latency/tolerance, modes, rationale…), alphabetical, with chapter references
- [patterns.md](patterns.md) — eleven reusable techniques (define the boundary, drive operational concepts with use cases, change-tolerant architecture, safety-driven revision, condition→assignment requirements, four-variable software bridge, allocation, rationale) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the eleven practices table, the four-variable model at a glance, the requirement structure, the three quality checks, decision rules, and tells & smells

---

## Scope & Limits

**Covers**: requirements engineering for real-time, embedded control systems per the FAA Requirements Engineering Management Handbook (DOT/FAA/AR-08/32) — the eleven recommended practices (system overview through rationale); the monitored/controlled-variable system boundary and physical interfaces; operational concepts via textual use cases; environmental assumptions and the requirements contract; the change-tolerant functional architecture and its safety-driven revision (FHA/PSSA/fault tree); system modes; detailed behavior and performance requirements (ideal value, tolerance, latency, completeness/consistency); the four-variable model bridge to software requirements (IN'/REQ'/OUT', DO-178B high/low-level and derived requirements); subsystem allocation; and the Isolette Thermostat and Flight Control System worked examples.

**Thin on / does not cover**: information-system, enterprise, business, and agile/iterative requirements styles (the slant is sensor/actuator control systems — reinterpret "monitored/controlled" with care elsewhere); requirements-management process, tooling, and DOORS-style traceability databases; full HMI/operator-interface design (named as a parallel track, not taught); and the *formal-methods internals* of SCR, RSML/RSML-e, SpecTRM, and the SCR analysis tools — the Handbook names this lineage and borrows its ideas but does not re-teach the notations. For sentence-level requirement craft (singular, verifiable, EARS-style) use the `requirements-writing` pack; for the safety process the Handbook hooks into, use `faa-system-safety` / `mil-std-882`; for the broader SE canon use `sebok` / `nasa-npr-7123`.

**Does not reproduce** the standards it cites — IEEE Std 1233, IEEE Std 830-1998, RTCA DO-178B / DO-248B / DO-278, and SAE ARP 4754 / ARP 4761 — which remain the copyright of their publishers; it names them and describes how its practices relate to them in original words.

**Jurisdiction**: US Government work prepared for the FAA — public domain (not subject to US copyright). The guidance is a set of *recommended practices*, explicitly meant to be tailored, not a mandatory standard. **Source version**: DOT/FAA/AR-08/32, Final Report, June 2009.
