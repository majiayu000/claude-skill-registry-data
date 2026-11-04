---
name: nist-800-37
description: "Knowledge base from NIST SP 800-37 Revision 2, the Risk Management Framework (RMF) for information systems and organizations. Use for the seven RMF steps (Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor) and their tasks; the three-tier organization-wide risk model; authorization boundaries; the requirements-to-controls relationship; security categorization (FIPS 199/200 high-water mark) and control selection/tailoring (SP 800-53/53B baselines); assessment, the authorization decision and risk acceptance, continuous monitoring and ongoing authorization; the security/privacy distinction; and supply chain risk management. This is the security-and-privacy-risk-governance edge of systems engineering — it governs how much protection and whether to accept residual risk, complementing the disciplines that decide how protection is built. Does NOT reproduce the SP 800-53 control catalog or its baselines, the FIPS impact tables, or the ISO/IEC/IEEE 15288 process text; it names and routes to them rather than restating them."
---

<!-- argument-hint: [RMF step (prepare/categorize/select/implement/assess/authorize/monitor), task ID (e.g. P-11, S-2, R-4, M-6), authorization boundary, categorization, control selection/tailoring, continuous monitoring, supply chain risk, chapter number] -->

# NIST SP 800-37 Rev. 2 — Risk Management Framework (RMF)
**Source**: NIST (US Government work, public domain) | **Chapters**: 7

## When to use
Use this skill to manage **security and privacy risk** across a system's life cycle the
way the federal Risk Management Framework prescribes: preparing the organization and the
system, categorizing by impact, selecting and tailoring controls, implementing and
assessing them, making an accountable risk-acceptance (authorization) decision, and
sustaining that decision through continuous monitoring. It is the governance-and-assurance
overlay that wraps an engineered system — the bridge from systems security engineering
(`nist-sse`) and the broader SE life cycle (`dau-se-guidebook`, `nasa-npr-7123`) into a
defensible, leadership-owned risk decision.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed
at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the RMF seven steps, the
  three-tier risk model, authorization boundaries, the requirements-to-controls seam, and
  the security/privacy distinction.
- **With a topic** — ask about a step (e.g. "categorize", "authorize"), a task ID (e.g.
  "P-11", "S-2", "R-4", "M-6"), or a construct (authorization boundary, high-water mark,
  common control, POA&M, ongoing authorization, supply chain risk).
- **With a chapter** — `ch03` (Prepare), `ch04` (Categorize + Select), `ch05` (Implement +
  Assess), `ch06` (Authorize), `ch07` (Monitor).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **What the RMF is — and isn't.** SP 800-37 Rev. 2 is a *risk-management process for
> information systems*, not a general SE process model. It rides alongside the SDLC and
> the ISO/IEC/IEEE 15288 / SP 800-160 life cycle rather than replacing them. Read this
> pack as the security-and-privacy-risk overlay on top of engineering work, not the
> engineering itself.

## Core Frameworks & Mental Models

### The Risk Management Framework (RMF) — seven steps

The RMF is a repeatable, life-cycle, risk-based process developed by NIST with the
Department of Defense, ODNI, and CNSS. It builds protection into systems, sustains posture
through continuous monitoring, and surfaces risk information to senior leaders for
acceptance decisions. It is **one preparatory step plus six main steps**:

1. **Prepare** — establish context and priorities at both the organization and system
   levels: roles, risk management strategy and tolerance, common controls, tailored
   baselines, authorization boundaries, and requirements. (ch03)
2. **Categorize** — determine the system's impact level from the consequences of losing
   confidentiality, integrity, or availability. (ch04)
3. **Select** — choose an initial control set, then tailor it to reduce risk to an
   acceptable level; allocate, document, and set monitoring. (ch04)
4. **Implement** — put the planned controls into the system and record the as-built
   configuration. (ch05)
5. **Assess** — determine whether each control was built correctly, runs as intended, and
   yields the outcome the requirements demand. (ch05)
6. **Authorize** — a senior official accepts (or refuses) residual risk to operations,
   assets, individuals, other organizations, and the Nation. (ch06)
7. **Monitor** — sustain ongoing situational awareness of posture, supporting near-real-
   time risk management and ongoing authorization. (ch07)

After Prepare, the steps may run **non-sequentially** — driven by system type, leadership
risk decisions, agile/iterative cycles, or changes surfaced during Monitor. An
organization can enter or re-enter at whichever step a current risk assessment dictates.
The one invariant: the authorizing official explicitly accepts risk *before* operation.

Each task has a defined anatomy — potential inputs, expected outputs, primary and
supporting responsibilities, the SDLC phase, a discussion, and references — and those
references identify the correlated systems-security-engineering tasks. That is the
explicit RMF-to-SE bridge.

### The three-tier organization-wide risk model (from SP 800-39)

Risk lives at three levels, with risk information flowing across all three:
- **Level 1 — organization** (risk strategy, tolerance, governance).
- **Level 2 — mission/business process** (prioritized missions, enterprise and
  security/privacy architecture, common controls).
- **Level 3 — information system** (the system's own risk, guided and constrained by the
  upper tiers).

**Risk gravity flows downhill:** strategy, tolerance, architecture, and boundary decisions
made above fall onto the system tier and constrain the controls selected there. Getting
the upper-tier groundwork right (the "Prepare" work) is what makes system-level risk work
affordable, repeatable, and effective.

### Authorization boundary

The **authorization boundary** defines the system for RMF purposes: the set of system
elements (people, processes, technologies) authorized for operation — or the set of common
controls authorized for inheritance. It replaces the older term "system boundary." Size it
as a deliberate trade-off: too wide adds needless complexity, too narrow multiplies
separately managed systems and inflates cost. Group elements that share mission,
requirements, information impact level, and environment of operation, under common direct
management. Each piece of the environment is either *in scope* (its protections land in
your plan) or *inherited* as common controls.

### Requirements → controls → engineering (the SE seam)

Requirements (legal/policy obligations and, more broadly, stakeholder protection needs)
drive **controls** — descriptions of safeguards and protection capabilities. Controls in
turn decompose into *specification* and *statement-of-work* requirements that engineers
build, derive, and test. This is the seam where the RMF meets systems-engineering
requirements practice (SP 800-160 v1 / ISO/IEC/IEEE 15288). Controls are designated
**system-specific, common (inherited), or hybrid**, and allocated only to the elements
that need the capability.

### Security and privacy: distinct but collaborating

Information security protects confidentiality, integrity, and availability. Privacy
programs manage risk to individuals from the *processing* of PII. The crucial asymmetry:
not all privacy risk comes from unauthorized activity — some arises from fully *authorized*
processing — so securing PII does not by itself protect privacy. Controls meeting both
objectives are simply "controls"; the qualifiers are used only when a control is selected
for a particular objective. Privacy entered the RMF via OMB Circular A-130 (2016).

### Posture, authorization, and residual risk

**Posture** — the current status of systems and resources given the defenses in place — is
built from ongoing assessment of system-specific, hybrid, and common controls. It is the
evidence base the authorizing official reads to judge whether residual risk is acceptable
against the organization's risk tolerance. **Residual risk always remains**; the job is to
land it inside tolerance and write down what was accepted. **Risk acceptance cannot be
delegated** — it is one named senior official's accountability, and the one RMF step an
external provider can never perform.

### Continuous monitoring and ongoing authorization

Monitor turns a one-time authorization into a continuously re-evidenced one. A robust,
mature continuous monitoring program lets the organization replace a fixed authorization
termination date with a time-driven re-judgment **frequency** — *ongoing authorization* —
supporting near-real-time risk management. Independence-qualified assessment results can be
reused for ongoing authorization, reauthorization, and the annual FISMA requirement.

### Supply chain risk management (SCRM)

External providers and COTS components carry risk *inside* your boundary, so the RMF folds
SCRM in rather than treating it as a parallel track. Single-use acceptable can become
systemic-unacceptable when an element is everywhere. Every RMF step can be executed by a
nonfederal external provider **except Authorize** — risk acceptance stays a federal
responsibility, and the obtainable assurance depends on the degree of control (contract /
SLA terms) and the evidence of control effectiveness the provider supplies.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-nist-800-37-introduction.md) | Introduction | Why manage security and privacy risk; the RMF; reciprocity; privacy via OMB A-130; SCRM and CSF integration; the broad definition of *information system* |
| [ch02](chapters/ch02-nist-800-37-fundamentals.md) | The Fundamentals | Three-tier risk model; the seven RMF steps structurally; system/elements/boundary; requirements-to-controls; posture; supply chain risk |
| [ch03](chapters/ch03-nist-800-37-process-and-prepare.md) | RMF Process + Prepare step | RMF-as-SDLC-overlay; iterative flow; Prepare tasks P-1…P-18 (roles, risk strategy, common controls, tailored baselines, boundary, requirements, registration) |
| [ch04](chapters/ch04-nist-800-37-categorize-and-select.md) | Categorize + Select steps | C-1…C-3 impact-level categorization (high-water mark vs. three-value); S-1…S-6 baseline vs. organization-generated selection, tailoring, allocation, monitoring strategy |
| [ch05](chapters/ch05-nist-800-37-implement-and-assess.md) | Implement + Assess steps | I-1/I-2 build-and-record; A-1…A-6 the three-part assessment test, independence, evidence reuse, findings/POA&M; privacy assessment |
| [ch06](chapters/ch06-nist-800-37-authorize.md) | Authorize step | R-1…R-5 authorization package, risk determination, risk response, the non-delegable decision, authorization types, ongoing authorization |
| [ch07](chapters/ch07-nist-800-37-monitor.md) | Monitor step | M-1…M-7 change detection, ongoing assessment, risk response, package updates, reporting, ongoing authorization, disposal |

## Topic Index

- **Assess step / assessment report** → ch05
- **Assessment criterion (correct / operating / effective)** → ch05
- **Assurance** → ch05, ch03
- **Authorization boundary** → ch02, ch03
- **Authorization package** → ch06
- **Authorization types (operate / use / common control)** → ch06
- **Authorize step / risk acceptance** → ch06
- **Authorizing official** → ch06
- **Categorize step** → ch04
- **Common control / inheritance** → ch03, ch04
- **Continuous monitoring strategy** → ch07, ch04
- **Control selection** → ch04
- **High-water mark** → ch04
- **Hybrid control** → ch03, ch04
- **Impact level** → ch04
- **Implement step** → ch05
- **Information system (definition)** → ch01
- **Monitor step** → ch07
- **Ongoing authorization** → ch06, ch07
- **Plan of Action and Milestones (POA&M)** → ch05, ch06
- **Posture (security and privacy)** → ch02
- **Prepare step** → ch03
- **Privacy risk / security-privacy distinction** → ch01, ch02
- **Reciprocity** → ch01
- **Requirements and controls** → ch02, ch03
- **Residual risk** → ch06
- **Reuse of assessment evidence** → ch05, ch07
- **Risk Management Framework (RMF)** → ch01, ch02
- **Risk tolerance / risk management strategy** → ch03
- **Select step / tailoring** → ch04
- **Supply chain risk management (SCRM)** → ch02
- **System elements / components** → ch02, ch03
- **System disposal** → ch07
- **Three-tier risk model** → ch02
- **Vulnerability vs. finding** → ch05

## Supporting Files

- [glossary.md](glossary.md) — key RMF terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — operating patterns (RMF-as-SDLC-overlay, maximizing common
  controls, sizing the boundary, baseline vs. organization-generated, shift-left assessment
  and reuse, routing deficiencies, ongoing authorization, disposal as a risk event) with
  When / How / Trade-offs
- [cheatsheet.md](cheatsheet.md) — the seven steps and tasks, the three-part assessment
  test, categorize roll-up table, baseline-vs-organization-generated table, control
  allocation, deficiency routing, authorization types, dated-vs-ongoing authorization,
  tells & smells, and the RMF-to-SE seams

---

## Scope & Limits

**Covers**: the Risk Management Framework per NIST SP 800-37 Revision 2 — the seven steps
(Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor) and their tasks
(P-1…P-18, C-1…C-3, S-1…S-6, I-1…I-2, A-1…A-6, R-1…R-5, M-1…M-7); the three-tier
organization-wide risk model; authorization boundaries; the requirements-to-controls
relationship; security categorization and control selection/tailoring at the *process*
level; assessment, the authorization decision and risk acceptance; continuous monitoring
and ongoing authorization; the security/privacy distinction; and supply chain risk
management as the RMF folds it in.

**Does not cover in depth**: the **SP 800-53 control catalog** and its **SP 800-53B
baselines** (the RMF *selects from* them — they are named and routed to, not reproduced);
the **FIPS 199 / FIPS 200 / CNSSI 1253 impact tables** (the categorization scheme is
described, the tables are not restated); the **ISO/IEC/IEEE 15288** process definitions
(third-party copyrighted — see `se-standards-signpost`; for open SE process models use
`dau-se-guidebook` / `nasa-npr-7123`); the detailed **continuous-monitoring mechanics** of
SP 800-137, **risk-assessment methodology** of SP 800-30, **SCRM practice** of SP 800-161,
and **privacy engineering** of IR 8062 (all referenced, not reproduced); and the systems-
security-engineering practice *beneath* the RMF (see `nist-sse` for SP 800-160). The RMF
governs **how much** protection and **whether to accept residual risk**; those companions
govern **how** protection is built.

**Source version**: NIST SP 800-37 Revision 2 — the RMF publication, subtitled a
system-life-cycle approach to security and privacy for information systems and
organizations (December 2018).

**Jurisdiction**: US Government public domain work. The framework is mandatory for federal
information systems and voluntary (but broadly adoptable) for state, local, tribal, and
private-sector organizations.
