---
name: cso
preamble-tier: 4
version: 1.0.0
description: |
  首席安全官审计。结合 OWASP Top 10、STRIDE、供应链、CI/CD、Secrets、
  Webhook、AI/LLM 风险与技能供应链，生成低噪声安全报告。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /cso

`/cso` 是 gstack 的安全审计面。目标不是列一堆泛泛 checklist，而是生成**低噪声、可验证、带置信度**的安全发现。

## 审计范围

1. 架构与技术栈心智模型
2. 攻击面清点
3. Secrets archaeology
4. 依赖供应链
5. CI/CD pipeline security
6. 基础设施影子面
7. Webhook / integration audit
8. LLM / AI security
9. Skill supply chain
10. `OWASP Top 10`
11. `STRIDE threat model`
12. 数据分级
13. 误报过滤与主动验证
14. findings report、趋势与修复建议

## 输出形式

- 每个 finding 带 severity、confidence、status、category、file:line
- 每个 finding 要有具体 exploit scenario
- 有 confidence calibration，不允许把低置信、未验证的猜测伪装成发现

## 关键规则

- 代码搜索优先用 `Grep`
- 明确过滤误报，避免把用户淹没
- 审计要覆盖传统安全问题，也要覆盖 LLM / agent 时代的新信任边界
