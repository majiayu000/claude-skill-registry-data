---
name: "ra-qm-skills"
description: "Manage — 12 regulatory & QM agent skills and plugins for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. ISO 13485 QMS, MDR 2017/745, FDA 510(k)/PMA, ISO 27001 ISMS, GDPR/DSGVO, risk mana"
version: 1.0.0
author: Alireza Rezvani
license: MIT
tags:
  - regulatory
  - quality-management
  - iso-13485
  - mdr
  - fda
  - iso-27001
  - gdpr
agents:
  - claude-code
  - codex-cli
  - openclaw
executor: LLM_BEHAVIOR
skill_id: business.ra-qm-team
status: ADOPTED
security: {level: high, pii: false, approval_required: true}
anchors:
  - business
  - llm
  - agent
  - compliance
tier: 2
input_schema:
  - name: code_or_task
    type: string
    description: "Code snippet, script, or task description to process"
    required: true
output_schema:
  - name: result
    type: string
    description: "Generated or refactored code output"
  - name: explanation
    type: string
    description: "Explanation of changes or implementation decisions"
---

# Regulatory Affairs & Quality Management Skills

12 production-ready compliance skills for HealthTech and MedTech organizations.

## Quick Start

### Claude Code
```
/read ra-qm-team/regulatory-affairs-head/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/ra-qm-team
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Regulatory Affairs Head | `regulatory-affairs-head/` | FDA/MDR strategy, submissions |
| Quality Manager (QMR) | `quality-manager-qmr/` | QMS governance, management review |
| Quality Manager (ISO 13485) | `quality-manager-qms-iso13485/` | QMS implementation, doc control |
| Risk Management Specialist | `risk-management-specialist/` | ISO 14971, FMEA, risk files |
| CAPA Officer | `capa-officer/` | Root cause analysis, corrective actions |
| Quality Documentation Manager | `quality-documentation-manager/` | Document control, 21 CFR Part 11 |
| QMS Audit Expert | `qms-audit-expert/` | ISO 13485 internal audits |
| ISMS Audit Expert | `isms-audit-expert/` | ISO 27001 security audits |
| Information Security Manager | `information-security-manager-iso27001/` | ISMS implementation |
| MDR 745 Specialist | `mdr-745-specialist/` | EU MDR classification, CE marking |
| FDA Consultant | `fda-consultant-specialist/` | 510(k), PMA, QSR compliance |
| GDPR/DSGVO Expert | `gdpr-dsgvo-expert/` | Privacy compliance, DPIA |

## Python Tools

17 scripts, all stdlib-only:

```bash
python3 risk-management-specialist/scripts/risk_matrix_calculator.py --help
python3 gdpr-dsgvo-expert/scripts/gdpr_compliance_checker.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Always verify compliance outputs against current regulations

---

## Why This Skill Exists

Manage — 12 regulatory & QM agent skills and plugins for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. ISO 13485 QMS, MDR 2017/745, FDA 510(k)/PMA, ISO 27001 ISMS, GDPR/DSGVO, risk mana

<!-- SR_40: auto-generated from frontmatter `purpose`/`description` (OPP-Phase3). Expand with domain-specific rationale. -->

## When to Use

Use this skill when the task requires ra qm skills capabilities.

<!-- SR_40: auto-generated from frontmatter `when`/`description` (OPP-Phase3). -->

## What If Fails

If this skill fails to produce the expected output: (1) verify input completeness, (2) retry with more specific context, (3) fall back to the parent workflow without this skill.

<!-- SR_40: auto-generated from frontmatter `what_if_fails` (OPP-Phase3). -->
