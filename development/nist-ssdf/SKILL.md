---
name: nist-ssdf
description: "Knowledge base from NIST Secure Software Development Framework (SSDF) v1.1 (SP 800-218). Use for secure software development practices, SDLC security integration, software supply chain security, vulnerability disclosure, SBOM, threat modelling, secure coding, build hardening, EO 14028 compliance. Covers the four SSDF practice groups (PO, PS, PW, RV) only; does not cover NIST CSF, SP 800-53 controls, or cloud-specific security frameworks in depth."
---

<!-- argument-hint: [topic, practice ID, or chapter number] -->

# NIST Secure Software Development Framework (SSDF) v1.1 (SP 800-218)
**Source**: NIST (US Government work, public domain) | **Chapters**: 5

## When to use
Reach for this pack whenever you need to integrate security into a software development life cycle, communicate secure development requirements to suppliers or acquirers, or respond to software vulnerabilities in a structured way. It is particularly useful when aligning development practices with EO 14028 Section 4e requirements, establishing supply-chain security controls, or building a vulnerability disclosure programme. It is not a substitute for NIST CSF (operational security) or SP 800-53 (control selection for information systems).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about threat modelling, SBOM, secure coding, code signing, vulnerability disclosure, compiler hardening, supply chain; I read the relevant chapter.
- **With a practice ID** — ask for `PO.1`, `PW.4.4`, `RV.3`, etc.; I return the practice definition, tasks, and implementation guidance.
- **With a chapter** — ask for `ch04`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Four SSDF Practice Groups

The SSDF organises all secure software development activity into four groups, applied throughout the SDLC:

**PO — Prepare the Organization**
Ensures people, processes, and technology are ready before and during development. Contains five practices:
- PO.1: Define security requirements for both the development infrastructure and the software being produced; flow requirements to suppliers.
- PO.2: Define roles, responsibilities, and role-based training for all SDLC participants.
- PO.3: Automate the toolchain; configure tools to generate audit artefacts (pipelines-as-code, toolchains-as-code).
- PO.4: Define KPI/KRI security check criteria and integrate them into development gates (e.g., Definition of Done).
- PO.5: Separate, harden, and continuously monitor all development environments (dev, build, test, distribution); apply zero-trust principles to build infrastructure.

**PS — Protect the Software**
Prevents tampering with and unauthorised access to all code forms and release artefacts:
- PS.1: Store source, executable, and configuration-as-code under least-privilege access with commit signing and code signing.
- PS.2: Publish cryptographic hashes and digital signatures with every release so acquirers can verify integrity.
- PS.3: Archive each release with its integrity verification data and provenance (SBOM); keep provenance separate from or signed independently of release files.

**PW — Produce Well-Secured Software**
Covers the activities that directly produce secure software:
- PW.1: Threat model at design time; document risk responses; reuse standardised security modules rather than building proprietary implementations.
- PW.2: Have a qualified, independent person (or automated toolchain process) review the design against security requirements and risk models.
- PW.4: Acquire vetted third-party components; verify them continuously against newly disclosed CVEs throughout their life cycles.
- PW.5: Follow language-appropriate secure coding practices: validate inputs, encode outputs, avoid unsafe functions, handle errors, provide logging.
- PW.6: Enable compiler and build tool security features (hardening flags, memory randomisation); enforce clean-build discipline (warnings-as-errors).
- PW.7: Apply static code analysis and human code review against secure coding standards as CI gates; record and triage all findings.
- PW.8: Perform dynamic executable testing (functional, fuzz, penetration) before release; incorporate regression tests for previously reported vulnerabilities.
- PW.9: Define and implement secure default configuration baselines; document each setting's purpose, options, and operational impact.

**RV — Respond to Vulnerabilities**
Closes the loop by identifying, remediating, and learning from post-release vulnerabilities:
- RV.1: Continuously gather vulnerability information from all sources (databases, users, researchers); investigate credible reports; maintain a formal disclosure programme and PSIRT.
- RV.2: Risk-score each vulnerability; implement permanent fixes or temporary mitigations; issue security advisories; deliver remediations via trusted automated channels.
- RV.3: Determine root causes; proactively sweep for the same class of vulnerability; update SDLC practices to prevent recurrence.

### Key Cross-Cutting Principles
- **Shift left**: Earlier security activity costs less and produces stronger outcomes.
- **Outcome focus**: SSDF specifies what to achieve, not which specific tools to use.
- **Risk-based selection**: Not every practice applies to every context; select based on risk, cost, feasibility.
- **Artefact generation**: If a security activity does not produce a traceable record, it cannot be demonstrated to regulators, acquirers, or auditors.
- **Shared responsibility**: In IaaS/PaaS/SaaS delivery, formally allocate SSDF responsibilities between provider and tenant in contracts.

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-introduction-and-how-to-use.md) | Introduction & How to Use the SSDF | SSDF purpose, audience, SDLC models, shifting left, risk-based adoption, shared responsibility |
| [ch02](chapters/ch02-prepare-the-organization.md) | Prepare the Organization (PO) | PO.1–PO.5: security requirements, roles & training, toolchains, security check criteria, secure environments |
| [ch03](chapters/ch03-protect-the-software.md) | Protect the Software (PS) | PS.1–PS.3: code access control, release integrity, SBOM, provenance archival |
| [ch04](chapters/ch04-produce-well-secured-software.md) | Produce Well-Secured Software (PW) | PW.1–PW.9: threat modelling, design review, component reuse, secure coding, compiler hardening, code review, dynamic testing, secure defaults |
| [ch05](chapters/ch05-respond-to-vulnerabilities.md) | Respond to Vulnerabilities (RV) | RV.1–RV.3: ongoing vulnerability identification, PSIRT, risk-based remediation, security advisories, root cause analysis, SDLC feedback loop |

## Topic Index
- **Artefact generation / audit evidence** → ch02 (PO.3.3)
- **Build pipeline security** → ch02 (PO.3), ch04 (PW.6)
- **Code review** → ch04 (PW.7)
- **Code signing** → ch03 (PS.1.1), ch03 (PS.2.1)
- **Compiler hardening / clean build** → ch04 (PW.6)
- **CVE monitoring / dependency scanning** → ch04 (PW.4.4), ch05 (RV.1.1)
- **Default configuration / secure by default** → ch04 (PW.9)
- **EO 14028 mapping** → ch01 (Appendix A reference), ch02 (PO.5)
- **Fuzz testing** → ch04 (PW.8.2)
- **Penetration testing** → ch04 (PW.8.2)
- **PSIRT** → ch05 (RV.1.3)
- **Provenance** → ch03 (PS.3.2), ch04 (PW.4.1)
- **Risk-based approach** → ch01, ch02 (PO.4), ch05 (RV.2.1)
- **Roles and responsibilities** → ch02 (PO.2)
- **Root cause analysis** → ch05 (RV.3)
- **SBOM** → ch03 (PS.3.2)
- **Secure coding** → ch04 (PW.5)
- **Secure design / threat modelling** → ch04 (PW.1)
- **Security requirements** → ch02 (PO.1)
- **Shifting left** → ch01
- **Shared responsibility model** → ch01
- **Static analysis** → ch04 (PW.7)
- **Supply chain / third-party components** → ch02 (PO.1.3), ch03 (PS.3), ch04 (PW.4)
- **Toolchain / pipeline-as-code** → ch02 (PO.3)
- **Vulnerability disclosure** → ch05 (RV.1.3)
- **Vulnerability remediation** → ch05 (RV.2)
- **Zero-trust for dev environments** → ch02 (PO.5.1)

## Supporting Files
- [glossary.md](glossary.md) — ~40 terms with chapter references; alphabetical
- [patterns.md](patterns.md) — 13 When/How/Trade-offs patterns covering all four practice groups
- [cheatsheet.md](cheatsheet.md) — Decision table by situation, practice quick-reference, tells & smells, key thresholds

---

## Scope & Limits
This pack covers NIST SP 800-218 (SSDF v1.1, February 2022) in its entirety — all four practice groups (PO, PS, PW, RV), their practices, tasks, and notional implementation examples. It does not provide in-depth coverage of referenced standards (NIST CSF, SP 800-53, SP 800-161, IEC 62443, OWASP ASVS, ISO 27034, ISO 29147, ISO 30111) — use those packs or their source documents for deeper dives. The document is a US Government work and is in the public domain; no licence restrictions apply to its contents.
