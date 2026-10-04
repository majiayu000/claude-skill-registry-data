---
name: skill-threat-model
description: Threat model agent skills, skillsets, and install paths. Use when Codex is asked to identify risks in a skill, define assets and trust boundaries, review permissions, or summarize security risks before installing or publishing a skill.
license: MIT
---

# Skill Threat Model

## Core Workflow

1. Identify what is being reviewed: skill, bundle, script, MCP preset, install
   path, or third-party source.
2. Inventory assets, data types, permissions, tools, scripts, dependencies, and
   host-specific install steps.
3. Map trust boundaries between user instructions, skill instructions,
   references, scripts, tools, network calls, and external content.
4. Identify threat paths: prompt injection, data exfiltration, privilege
   escalation, unsafe script execution, secrets exposure, and supply-chain risk.
5. Rate risks by likelihood, impact, evidence, and required mitigation.
6. Recommend approve, approve with changes, block, or defer.

## Safety Rules

- Do not run unreviewed third-party scripts to learn what they do.
- Do not access secrets or private data during threat modeling.
- Do not approve broad write/network permissions without a clear workflow need
  and explicit user approval path.
- Treat skills with executable code as higher risk than instruction-only skills.

## Deliverable Shape

For threat models, provide:

- Review scope
- Asset and capability inventory
- Trust boundaries
- Threat paths
- Risk matrix
- Required mitigations
- Approval recommendation

## References

- Read `references/skill-threat-model-checklist.md` when threat modeling a
  skill, bundle, script, MCP preset, or install path.
