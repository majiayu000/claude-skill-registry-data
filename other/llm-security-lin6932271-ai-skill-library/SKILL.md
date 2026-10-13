---
name: llm-security
description: "LLM Security Assessment"
---

# LLM Security Assessment

## Scope

Use this module only for LLM-integrated systems you own or have explicit authorization to assess. Evaluate prompt injection resistance, system prompt protection, and output filtering controls.

## Workflow

1. Document target architecture: model provider, prompt template structure, tool integrations.
2. Assess input boundary isolation: verify system instructions are not extractable via user input.
3. Test prompt injection vectors: direct injection, indirect via retrieved content, multi-turn manipulation.
4. Evaluate output filtering: PII leakage detection, format injection, harmful content generation blocks.
5. Review tool-use authorization: scope limits, credential exposure, action boundary enforcement.
6. Document defense mechanisms and identify gaps in sanitization, filtering, and monitoring.

## Safety Rules

- Do not assess LLM systems you do not own or have explicit authorization to test.
- Do not use injection techniques to extract real user data from production systems.
- Do not bypass safety controls to generate harmful or illegal content.
- Do not publish working injection payloads for unauthorized systems.

## Output

Return an evidence table with columns: Vector, Test Case, Result, Defense Gap, Remediation.

## 使用前核对

目标与操作范围以用户当前请求为准；核对方法前置条件、工具和附件，按实际执行层级记录结果。正文不表示示例代码已经在本机执行或验证。
