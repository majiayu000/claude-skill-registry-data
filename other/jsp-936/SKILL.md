---
name: jsp-936
description: "Knowledge pack synthesized from JSP 936 Dependable Artificial Intelligence (AI) in Defence, Part 1: Directive, V1.1 (November 2024, Ministry of Defence, Open Government Licence v3.0): dependable-AI direction for Defence. SCOPE LIMITS: single-source (JSP 936 Part 1 V1.1); MOD policy, not statute; not the Defence SMS (use jsp-815) and not acquisition-safety policy (use jsp-376); Part 2 is not in this pack; no DEF-STAN text and no other JSP reproduced; reconstructed reference notes, not MOD guidance, and no official status."
---

# JSP 936: Dependable Artificial Intelligence (AI) in Defence, Part 1: Directive

## When to use

**Prerequisites:** none required; plain Markdown. Familiarity with a safety case and with risk management helps; the glossary defines the Defence-specific terms.

Use this skill for questions about how UK Defence directs dependable AI: what falls in scope, how AI ethical risk is rated and escalated, who is accountable, what the lifecycle stage duties are, and how assurance is argued. It is the dependable-AI companion to `jsp-815` and `jsp-376`; it does not replace either pack.

**Source:** Contains public sector information licensed under the Open Government Licence v3.0. JSP 936 Dependable Artificial Intelligence (AI) in Defence, Part 1: Directive, V1.1 (November 2024), Ministry of Defence, © Crown copyright. Reconstructed reference notes, not reproductions; licence text and source link in [LICENSE](LICENSE).

## How to Use This Skill

- **Without arguments**: read Core Frameworks & Mental Models below.
- **With a topic**: use the Topic Index and follow the arrow to a chapter.
- **With a role or lifecycle question**: use the Chapter Index and read the matching chapter.
- **For a term** use `glossary.md`; **for decision rules** use `cheatsheet.md`.

## Core Frameworks & Mental Models

### Dependability is reliance matched by confidence

The directive defines dependability relationally: how much the user can rely on safe, secure and correct operation within a given context of mission, human involvement, environment and system constraints. There is no dependability scale. Confidence must be commensurate with reliance, risk owners judge the evidence through the lifecycle, and uncertainty must be understood and communicated. Grounded underneath it all is meaningful human control, exercised through context-appropriate human involvement.

### The ASR frame: five principles under three perspectives

Adoption of AI is bounded by good governance, demonstration of safety, and legal compliance, and the five MOD AI Ethical Principles from the Ambitious, Safe, Responsible statement connect to all three: Human-centricity, Responsibility, Understanding, Bias and Harm Mitigation, and Reliability. Compliance is determined by how a system does what it does, not by what it does, so no list of acceptable or unacceptable AI concepts can exist; nearly any concept might be delivered responsibly if the directive's precepts are followed.

### Accountability runs through the RAISO and the referral ladder

Every TLB appoints a Responsible AI Senior Officer; every AI project identifies its RAISO; TLB Executive Boards give the 2PUS annual Statements of AI Ethical Assurance backed by auditable evidence. An AI ethical risk rating, set from residual risk, picks the approvals pathway, from business-level handling up to 2PUS or Ministers by exception, with AI in kinetic effects and novel or contentious applications always referred to the Defence AI and Autonomy Unit. Where risk becomes unacceptable, development or deployment halts until reviewed.

### Lifecycle-agnostic duties, honestly limited

The directive mandates no particular lifecycle. Instead it sets stage duties that survive any process: controlled planning that names how ethics are met, hazard analysis that feeds system safety, data provenance and separation, risk-informed model reuse, verification across the operating envelope plus demonstrated safe behaviour outside it, and monitoring that keeps deployed AI inside its approved bounds. Where ML traceability breaks at the low-level requirement stage, the directive demands the loss be met with recorded risk-balance arguments and demonstration against intent, not ignored.

## Chapter Index

| Ch | Chapter | Sources | Coverage |
|---|---|---|---|
| 01 | [ch01-introduction.md](chapters/ch01-introduction.md) | pp. 1-5 | Policy base, AI characterisation, dependability, scope, applicability, tailoring, delegation, associated standards. |
| 02 | [ch02-ai-in-defence-systems.md](chapters/ch02-ai-in-defence-systems.md) | pp. 5-8 | RAS and digital systems, autonomy continuum, ODD, dual-use military delta, AI labelling and advice provenance. |
| 03 | [ch03-legal-ethics-governance.md](chapters/ch03-legal-ethics-governance.md) | pp. 8-18 | Legal duties, five ethical principles, AI ethical risk rating and referral ladder, RAISO and governance roles, non-sovereign AI. |
| 04 | [ch04-human-ai-teams.md](chapters/ch04-human-ai-teams.md) | pp. 18-21 | Human centred design, HFI, function allocation and the accountability gap, workforce and training implications. |
| 05 | [ch05-ai-lifecycles.md](chapters/ch05-ai-lifecycles.md) | pp. 21-28 | MLOps, stage duties from planning through integration, data classes and properties, model reuse, V&V, competencies. |
| 06 | [ch06-quality-safety-security.md](chapters/ch06-quality-safety-security.md) | pp. 28-29 | JSP 940 quality overlay, JSP 815 safety obligations, Secure by Design and continuous security assurance. |
| 07 | [ch07-suppliers.md](chapters/ch07-suppliers.md) | pp. 29-30 | Supplier competence, third-party component arguments, data provenance, contracting and export-control freedom of action. |
| 08 | [ch08-ai-assurance.md](chapters/ch08-ai-assurance.md) | pp. 30-31 | Assurance risk as an adoption gate, system-context tolerance, replacement argument, ODD excursions and failure postures. |

## Topic Index

- Dependable AI scope and definitions → ch01
- Policy base, ASR, tailoring and delegation → ch01
- Robotic and autonomous systems → ch02
- Digital systems, generative AI and AI labelling → ch02
- Legal considerations and IHL → ch03
- AI ethical principles (human-centricity, responsibility, understanding, bias and harm mitigation, reliability) → ch03
- AI ethical risk rating, referral and approval → ch03
- AI ethics governance, RAISO, statements of assurance → ch03
- Non-sovereign and internationally shared AI → ch03
- Human/AI teaming and human centred design → ch04
- Function allocation and the accountability gap → ch04
- Workforce and training implications → ch04
- AI lifecycles, MLOps and planning duties → ch05
- Requirements, traceability and hazard analysis → ch05
- ML data collection, preparation and control → ch05
- Model development, reuse and interpretability → ch05
- AI verification and validation → ch05
- AI integration, use and modification → ch05
- Quality, safety and security overlays → ch06
- Suppliers, contracting and provenance → ch07
- AI assurance and assurance risk → ch08
- ODD excursions and failure postures → ch08
- Policy interfaces to JSP 815, JSP 376 and other JSPs → ch01, ch06

## Supporting Files

- `glossary.md`: Defence dependable-AI terms the directive defines or characterises, alphabetical, with the chapters that use each.
- `cheatsheet.md`: decision rules (scope, dependability, risk referral, data properties, assurance) and the role and lifecycle structures, in text.

## Scope & Limits

- **Source version:** JSP 936 Dependable Artificial Intelligence (AI) in Defence, Part 1: Directive, V1.1 (November 2024); pin verified 2026-10-27 against the publication page and the PDF (41 pages).
- **Policy, not statute:** MOD policy and direction, not legislation; nothing in it removes duties under UK or international law.
- **Builds on JSP 815 and JSP 376.** Neither is reproduced. Use the `jsp-815` pack for the Defence safety management system and the `jsp-376` pack for acquisition safety policy; this pack does not replace them.
- **Part 2 absent:** the guidance part of JSP 936 is a separate publication and is not in this pack; where the directive points at it, the pack says so and invents nothing.
- **No DEF-STAN text:** Def Stan 00-055, 00-056 and others are named, not quoted.
- **No other JSP reproduced:** every related JSP, from JSP 200 to JSP 985, is named only.
- **Not a general AI risk-management pack:** `nist-ai-rmf` and `eu-ai-act` stay outside this skill; this pack carries MOD dependable-AI direction only.
- **No MOD endorsement.** Reconstructed reference notes, not MOD guidance, and no official status. Source and licence links live only in [LICENSE](LICENSE).
