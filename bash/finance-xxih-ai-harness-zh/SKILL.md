---
name: "finance-skills"
description: "面向 Claude Code、Codex、Gemini CLI、Cursor、OpenClaw 的 financial analyst agent skill 与 plugin。覆盖 ratio analysis、DCF valuation、budget variance、rolling forecasts。附带 4 个只依赖标准库的 Python 工具。"
version: 1.0.0
author: Alireza Rezvani
license: MIT
tags:
  - finance
  - financial-analysis
  - dcf
  - valuation
  - budgeting
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Finance Skills

面向战略决策的可用于生产环境的财务分析 skill。

## 快速开始

### Claude Code

```text
/read finance/financial-analyst/SKILL.md
```

### Codex CLI

```bash
npx agent-skills-cli add alirezarezvani/claude-skills/finance
```

## Skills 概览

| Skill | Folder | Focus |
|-------|--------|-------|
| Financial Analyst | `financial-analyst/` | 比率分析、DCF、预算偏差、预测 |

## Python Tools

共 4 个脚本，全部只依赖标准库：

```bash
python3 financial-analyst/scripts/ratio_calculator.py --help
python3 financial-analyst/scripts/dcf_valuation.py --help
python3 financial-analyst/scripts/budget_variance_analyzer.py --help
python3 financial-analyst/scripts/forecast_builder.py --help
```

## 规则

- 只加载当前真正需要的那个 `SKILL.md`
- 财务输出始终要回到源数据上核对
