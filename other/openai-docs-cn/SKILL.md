---
name: openai-docs-cn
description: Use when answering Chinese questions about building with OpenAI APIs, models, pricing-sensitive choices, migration, or Codex-related developer workflows using current official docs.
---

# OpenAI Docs CN

用在中文用户询问 OpenAI API、模型选择、迁移、Codex 开发工作流、Responses API、Agents、工具调用、计费敏感决策时。目标是基于官方资料给出可执行中文答案。

## 适用场景

- 用户问“现在该用哪个 OpenAI 模型”“Responses API 怎么接”“Codex 怎么用于开发流程”。
- 需要比较模型、能力、限制、迁移路径或代码示例。
- 信息可能随时间变化，需要查官方文档。

## 不适用场景

- 只是在本地项目里调用一个已有封装，不需要查 OpenAI 最新文档。
- 用户要求非官方爆料、价格预测或绕过限制。
- 医疗、法律、金融等高风险建议，除非只讨论 API 接入本身。

## 工作流

1. 优先查官方来源。
   - 使用 OpenAI 官方 docs、platform docs、developers.openai.com、help.openai.com。
   - 对“最新”“当前”“价格”“模型能力”必须确认日期和来源。

2. 给中文结论。
   - 先回答用户该怎么做。
   - 再给关键限制、取舍和代码方向。
   - 对不确定或会变化的信息注明“截至查询时”。

3. 结合项目上下文。
   - 如果用户在代码仓库中，优先看现有 SDK、环境变量、封装层和测试。
   - 不要建议大改架构，除非迁移收益明确。

4. 给出最小可行示例。
   - 示例要短，能落地。
   - 不暴露 API key。

## 输出要求

- 中文回答。
- 附官方链接。
- 明确区分事实、建议和推断。
- 如果无法联网或无法确认最新信息，直接说明不能确认。

## 验证方式

- 对最新模型、价格、限制、API 行为等易变化信息，必须引用官方页面并说明查询日期。
- 代码建议应与用户项目当前 SDK、框架和语言版本相容。
- 无法访问官方文档时，不要把记忆当成最新事实。

## 安全边界

- 不要指导规避速率限制、地区限制、账号限制或付费规则。
- 不要把用户密钥写入代码示例。
- 涉及成本时提醒用户核对官方价格页。
