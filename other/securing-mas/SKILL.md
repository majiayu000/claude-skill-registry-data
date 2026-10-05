---
name: securing-mas
description: Apply OWASP MAESTRO, MITRE ATLAS, NIST AI RMF, and ISO 42001/23894 security frameworks to MAS designs
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
  argument-hint: [component-or-feature]
  stability: stable
  content-hash: sha256:94039e17e94bb06a07cb298b68d4b5a02f3ef882ad08837656d1a82d3e0ad8b2
  last-verified-cc-version: 1.0.34
---

# Securing Multi-Agent Systems

**Target**: $ARGUMENTS

## When to Use

Trigger this skill when:

- Conducting security reviews of agent systems
- Threat modeling for multi-agent architectures
- Reviewing plugin implementations for security
- Designing security controls for pipelines

## Framework Stack

```text
MITRE ATLAS (attack taxonomy — what adversaries do)
      |  informs threat identification
      v
OWASP MAESTRO (threat model — what to defend against in MAS)
      |  maps threats to controls
      v
NIST AI RMF (risk framework — how to govern/map/measure/manage)
      |  operationalized by
      v
ISO 42001 + 23894 (certifiable management system + risk methodology)
```

Use all four layers together: ATLAS enumerates attack vectors, MAESTRO maps
them to MAS-specific controls, NIST AI RMF structures governance, and ISO
provides the certifiable management system.

## Workflow

1. **Review the framework stack** — `references/mas-security.md` for the conceptual overview of MAESTRO, ATLAS, NIST AI RMF, and ISO 42001/23894 layers working together.

2. **Apply the 7-layer security check** — for each new component, walk through every MAESTRO layer. See `references/maestro-7-layer-checklist.md` for the actionable per-layer checklist (Model → Orchestration).

3. **Run the plugin security checklist** — before marking an implementation complete, verify input validation, output safety, resource management, observability, and external dependencies. See `references/plugin-security-checklist.md`.

4. **Document threats in the cross-framework matrix** — for each feature, map concerns to ATLAS techniques, MAESTRO layers, NIST functions, and ISO controls. Start from `references/threat-matrix-template.md` and add feature-specific rows.

5. **Avoid common vulnerability patterns** — consult `references/common-vulnerabilities.md` for vulnerable/secure code examples: prompt injection (L1), type confusion (L2), resource exhaustion (L5), secret leakage (L6).

6. **Test security controls explicitly** — write tests that exercise each MAESTRO layer's controls. See `references/security-testing-patterns.md` for pytest examples (input validation, timeout enforcement, error message safety).

## Further Reading

- [OWASP MAESTRO v1.0](https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/)
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI RMF 1.0 (AI 100-1)](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence)
- [NIST AI 600-1 Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)
- [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html)
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)
