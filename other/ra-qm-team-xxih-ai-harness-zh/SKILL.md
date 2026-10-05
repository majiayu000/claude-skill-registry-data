---
name: "ra-qm-skills"
description: "面向 Claude Code、Codex、Gemini CLI、Cursor、OpenClaw 的 12 个 regulatory & QM agent skills 与 plugins。覆盖 ISO 13485 QMS、MDR 2017/745、FDA 510(k)/PMA、ISO 27001 ISMS、GDPR/DSGVO、风险管理（ISO 14971）、CAPA、文档控制与审计。附带只依赖标准库的 Python 工具。"
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
---

# Regulatory Affairs & Quality Management Skills

为 HealthTech 与 MedTech 组织准备的 12 个可用于生产环境的合规 skill。

## 快速开始

### Claude Code

```text
/read ra-qm-team/regulatory-affairs-head/SKILL.md
```

### Codex CLI

```bash
npx agent-skills-cli add alirezarezvani/claude-skills/ra-qm-team
```

## Skills 概览

| Skill | Folder | Focus |
|-------|--------|-------|
| Regulatory Affairs Head | `regulatory-affairs-head/` | FDA/MDR 策略、注册提交 |
| Quality Manager (QMR) | `quality-manager-qmr/` | QMS 治理、管理评审 |
| Quality Manager (ISO 13485) | `quality-manager-qms-iso13485/` | QMS 落地、文档控制 |
| Risk Management Specialist | `risk-management-specialist/` | ISO 14971、FMEA、风险文件 |
| CAPA Officer | `capa-officer/` | 根因分析、纠正措施 |
| Quality Documentation Manager | `quality-documentation-manager/` | 文档控制、21 CFR Part 11 |
| QMS Audit Expert | `qms-audit-expert/` | ISO 13485 内审 |
| ISMS Audit Expert | `isms-audit-expert/` | ISO 27001 安全审计 |
| Information Security Manager | `information-security-manager-iso27001/` | ISMS 实施 |
| MDR 745 Specialist | `mdr-745-specialist/` | 欧盟 MDR 分类、CE 标记 |
| FDA Consultant | `fda-consultant-specialist/` | 510(k)、PMA、QSR 合规 |
| GDPR/DSGVO Expert | `gdpr-dsgvo-expert/` | 隐私合规、DPIA |

## Python Tools

共 17 个脚本，全部只依赖标准库：

```bash
python3 risk-management-specialist/scripts/risk_matrix_calculator.py --help
python3 gdpr-dsgvo-expert/scripts/gdpr_compliance_checker.py --help
```

## 规则

- 只加载当前真正需要的那个 `SKILL.md`
- 所有合规输出都必须回到最新法规要求上核实
