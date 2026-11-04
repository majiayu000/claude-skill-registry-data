---
name: nist-sse
description: "Knowledge base from NIST SP 800-160 Vol 1 (Engineering Trustworthy Secure Systems) and Vol 2 (Developing Cyber-Resilient Systems). Use for systems security engineering (SSE): the three SSE framework contexts (problem/solution/trustworthiness), the 30+ design principles for trustworthy secure design, trustworthiness and assurance/assurance cases, security across the ISO/IEC/IEEE 15288 life-cycle process groups, and the Vol 2 cyber-resiliency engineering framework — 4 goals (anticipate/withstand/recover/adapt), objectives, 14 techniques, implementation approaches, and design principles for the APT/adverse-conditions threat model. Bridges systems engineering and the NIST security cluster (CSF/SSDF/RMF). Does not reproduce ISO/IEC/IEEE 15288 process text, nor cover SP 800-53 control catalogs in depth."
---

<!-- argument-hint: [SSE context, design principle, trustworthiness/assurance, life-cycle process, cyber-resiliency goal/objective/technique/approach, APT, chapter number] -->

# NIST SP 800-160 — Systems Security Engineering (Vol 1 + Vol 2)
**Source**: NIST (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill to engineer security *into* a system rather than bolt it on: framing the security problem/solution/trustworthiness, applying the design principles for trustworthy secure design, building a defensible assurance case, integrating security across the system life cycle, and — for systems that must survive a capable adversary — applying cyber-resiliency goals, objectives, techniques, and approaches. This is the security-engineering bridge between systems engineering (15288/NASA/DoD SE) and the NIST security frameworks (`nist-csf`, `nist-ssdf`, RMF).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the SSE three-context framework, design principles, trustworthiness/assurance, and the cyber-resiliency framework.
- **With a topic** — ask about a design principle (e.g. "least privilege", "minimal trusted elements"), trustworthiness/assurance cases, a life-cycle process, or a cyber-resiliency goal/objective/technique (e.g. "analytic monitoring", "non-persistence").
- **With a chapter** — `ch02` (SSE framework), `ch03` (design principles), `ch05` (cyber-resiliency framework), `ch06` (techniques).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **Two volumes, one discipline.** **Vol 1** = *Engineering Trustworthy Secure Systems* (the SSE foundation). **Vol 2** = *Developing Cyber-Resilient Systems* (a specialty SSE approach for surviving the advanced persistent threat). Chapters 1–4 here cover Vol 1; chapters 5–8 cover Vol 2.

## Core Frameworks & Mental Models

### Systems Security Engineering (SSE) — what it is

SSE is a specialty engineering discipline applying scientific, engineering, and assurance principles to deliver systems that are **trustworthy** and **adequately secure** for their stakeholders, within cost/schedule/risk. Two anchoring ideas:
- **Security is a property of the *whole system*, engineered in across the life cycle** — not a feature added late.
- **Adequately secure**: security is asymmetric (you can observe insecurity but never prove arbitrary security), so the goal is *adequate* security justified by evidence, not absolute security.

### The SSE Framework — Three Contexts (Vol 1)

The SSE framework organizes all security activity into **three interacting contexts** (not strictly sequential — they iterate and share a common base of system security analyses):

1. **Problem Context** — define the security problem: stakeholder security needs, the protection needs, the adversity to be addressed, security requirements, and the security aspects of the operational environment. *"What must be protected, from what, and why?"*
2. **Solution Context** — define and realize the security solution: security architecture and design, the security aspects of every system element, and the security-relevant decisions and trade-offs. *"How is protection achieved?"*
3. **Trustworthiness Context** — produce the evidence that the solution is trustworthy: assurance, the assurance case, and the demonstration that claims are substantiated. *"Why should anyone believe it?"*

### Design Principles for Trustworthy Secure Design (Vol 1, ~30+)

A catalog of principles to apply when designing for security. Key examples (not exhaustive):

| Principle | Essence |
|---|---|
| **Clear Abstractions** | Clean, understandable interfaces; no needless complexity |
| **Least Privilege** | Each element gets only the privileges it needs |
| **Least Functionality / Least Persistence / Least Sharing** | Minimize functions, lifetime, and shared resources |
| **Minimal Trusted Elements** | Shrink the trusted computing base; less to trust, less to verify |
| **Reduced Complexity** | Simpler systems are more analyzable and more secure |
| **Defense in Depth** | Layered, diverse protections so no single failure is fatal |
| **Domain Separation / Hierarchical Protection** | Isolate and order protection domains |
| **Mediated Access / Protective Defaults** | Control every access; fail to a safe default |
| **Protective Failure / Protective Recovery** | Fail securely; recover to a secure state |
| **Distributed Privilege / Diversity / Redundancy** | No single point of compromise; vary and duplicate |
| **Anomaly Detection / Minimize Detectability** | See adversary activity; deny the adversary visibility |
| **Loss Margins / Substantiated Trust** | Engineer margin against loss; trust only what's evidenced |

Principles split broadly into **security architecture & design** principles (how to structure the system) and **security capability/trust** principles (what protection and assurance to provide).

### Trustworthiness & Assurance (Vol 1)

- **Trustworthiness** = worthy of being trusted to meet defined expectations (security, plus safety, reliability, etc.); it is *claimed, then substantiated*, never assumed.
- **Assurance** = the grounds for justified confidence that the system satisfies its security claims.
- **Assurance case** = a structured argument (claims → arguments → evidence) that the security claims hold; the central artifact of the trustworthiness context. (See `nasa-system-safety` for the parallel claim-argument-evidence "safety case".)

### Security Across the Life Cycle (Vol 1)

Vol 1 augments the **ISO/IEC/IEEE 15288 system life-cycle process groups** with security considerations, outcomes, and tasks. The four process groups it addresses:
- **Technical Processes** — security in business/mission analysis, stakeholder needs, requirements, architecture, design, implementation, integration, V&V, transition, operation, maintenance, disposal.
- **Technical Management Processes** — security in planning, assessment/control, decision, risk, configuration, information, measurement, quality.
- **Organizational Project-Enabling Processes** — security in life-cycle model management, infrastructure, portfolio, human-resource, quality, knowledge management.
- **Agreement Processes** — security in acquisition and supply.

*(This pack names these groups and describes NIST's security augmentation in original words; it does not reproduce the ISO/IEC/IEEE 15288 process text — that's third-party copyrighted material.)*

### Cyber-Resiliency Engineering Framework (Vol 2)

Vol 2 is a specialty SSE approach for systems that must keep operating through compromise by an **advanced persistent threat (APT)** — assume the adversary is already (or will get) inside. The framework is a hierarchy:

- **4 Goals** — the highest level, from the definition of cyber resiliency:
  - **Anticipate** — maintain informed preparedness for adversity.
  - **Withstand** — continue essential mission/business functions despite adversity.
  - **Recover** — restore functions during and after adversity.
  - **Adapt** — change functions/supporting capabilities in response to predicted or actual change.
- **Objectives** — more specific, assessable statements (e.g. Prevent/Avoid, Prepare, Continue, Constrain, Reconstitute, Understand, Transform, Re-Architect) that support the goals.
- **14 Techniques** — categories of capability that achieve objectives (see ch06): Adaptive Response, Analytic Monitoring, Contextual Awareness, Coordinated Protection, Deception, Diversity, Dynamic Positioning, Non-Persistence, Privilege Restriction, Realignment, Redundancy, Segmentation, Substantiated Integrity, Unpredictability.
- **Implementation Approaches** — specific methods within each technique.
- **Design Principles** — strategic (cross-cutting) and structural (apply to architecture/design) principles guiding selection and placement.

### How it all connects to risk

Cyber resiliency reduces the **mission/business risk of depending on cyber resources**. It plugs into the NIST risk ecosystem — RMF (SP 800-37), controls (SP 800-53), and the organizational risk strategy — and is selected/tailored against the adversary (the APT and its attack vectors), not applied wholesale.

---

## Chapter Index

| # | Vol | Section | Key content |
|---|-----|---------|-------------|
| [ch01](chapters/ch01-sse-foundations.md) | 1 | SSE Foundations | What SSE is, systems/SE concepts, "adequately secure", asymmetry of security, audience, relationship to RMF/SE |
| [ch02](chapters/ch02-sse-framework.md) | 1 | The SSE Framework (3 Contexts) | Problem / Solution / Trustworthiness contexts; how they interact; the common base of security analyses |
| [ch03](chapters/ch03-design-principles.md) | 1 | Design Principles for Trustworthy Secure Design | The ~30+ principles (least privilege, minimal trusted elements, reduced complexity, defense in depth, protective failure/recovery…) and how to apply them |
| [ch04](chapters/ch04-trustworthiness-and-lifecycle.md) | 1 | Trustworthiness, Assurance & the Life Cycle | Trustworthiness vs. assurance, assurance cases (claim-argument-evidence), security across the four 15288 process groups |
| [ch05](chapters/ch05-cyber-resiliency-framework.md) | 2 | Cyber-Resiliency Engineering Framework | The 4 goals (anticipate/withstand/recover/adapt), objectives, and the hierarchy goals→objectives→techniques→approaches→principles |
| [ch06](chapters/ch06-cyber-resiliency-techniques.md) | 2 | Cyber-Resiliency Techniques & Approaches | The 14 techniques and their implementation approaches; what each defends against |
| [ch07](chapters/ch07-cyber-resiliency-design-principles.md) | 2 | Cyber-Resiliency Design Principles | Strategic vs. structural design principles; selecting and placing resiliency in the architecture |
| [ch08](chapters/ch08-applying-and-risk.md) | 2 | Applying Cyber Resiliency & Risk | The APT/adversary model, tailoring to mission risk, integration with RMF/SP 800-53, analysis and trade-offs |

## Topic Index

- **Adequately secure / asymmetry of security** → ch01
- **Advanced Persistent Threat (APT) / adversary model** → ch08, ch05
- **Anticipate / Withstand / Recover / Adapt (goals)** → ch05, cheatsheet
- **Assurance / assurance case (claim-argument-evidence)** → ch04, cheatsheet
- **Cyber-resiliency framework (hierarchy)** → ch05, cheatsheet
- **Cyber-resiliency objectives** → ch05
- **Cyber-resiliency techniques (the 14)** → ch06, cheatsheet
- **Defense in depth** → ch03
- **Design principles (trustworthy secure design)** → ch03, cheatsheet
- **Design principles (cyber-resiliency: strategic/structural)** → ch07, cheatsheet
- **Domain separation / hierarchical protection** → ch03
- **Implementation approaches** → ch06
- **ISO/IEC/IEEE 15288 process groups (security augmentation)** → ch04
- **Least privilege / least functionality / least persistence / least sharing** → ch03
- **Life cycle (security across)** → ch04
- **Minimal trusted elements / trusted computing base** → ch03
- **Problem / Solution / Trustworthiness contexts** → ch02, cheatsheet
- **Protective defaults / failure / recovery** → ch03
- **Reduced complexity** → ch03
- **Risk management / RMF / SP 800-53 linkage** → ch08, ch01
- **Trustworthiness** → ch04, ch01
- **Specific techniques** (Adaptive Response, Analytic Monitoring, Contextual Awareness, Coordinated Protection, Deception, Diversity, Dynamic Positioning, Non-Persistence, Privilege Restriction, Realignment, Redundancy, Segmentation, Substantiated Integrity, Unpredictability) → ch06

## Supporting Files

- [glossary.md](glossary.md) — key SSE and cyber-resiliency terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (framing via the 3 contexts, applying design principles, building an assurance case, selecting cyber-resiliency techniques against an APT) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the 3 contexts, design-principle list, cyber-resiliency goals→objectives→techniques table, design principles, tells & smells

---

## Scope & Limits

**Covers**: systems security engineering per NIST SP 800-160 Vol 1 Rev 1 and the cyber-resiliency engineering approach per Vol 2 Rev 1 — the three SSE framework contexts; the design principles for trustworthy secure design; trustworthiness, assurance, and assurance cases; the security augmentation of the ISO/IEC/IEEE 15288 life-cycle process groups (named and described, not reproduced); and the full Vol 2 cyber-resiliency framework (goals, objectives, techniques, approaches, design principles) with its APT-centric risk model.

**Does not cover in depth**: the ISO/IEC/IEEE 15288 process definitions themselves (third-party copyrighted — see `se-standards-signpost`; for open SE process models use `nasa-npr-7123` / `dau-se-guidebook`); the SP 800-53 control catalog (referenced, not reproduced); the Risk Management Framework steps (see SP 800-37 / RMF; complemented by `nist-csf`); privacy engineering; and domain-specific security (cryptographic standards, network security configs).

**Jurisdiction**: US Government public domain work (with third-party ISO/IEC/IEEE material not reproduced here). The guidance is voluntary for non-federal organizations and broadly adoptable.
