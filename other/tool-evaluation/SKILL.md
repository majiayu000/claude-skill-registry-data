---
name: tool-evaluation
description: >
  Quick evaluation of external tools, projects, services, or platforms.
  Trigger: user asks “这个能干什么”, “有什么优点”, “是什么”, “值得用吗”, or shares a URL and wants a verdict.
  Output: concise pros/cons, core value, key limitations, and a bottom-line recommendation.
  Use for GitHub repos, SaaS products, open-source tools, APIs, and developer services.
---

# Tool Evaluation

## When to use

- User shares a URL and asks what it is / what it does.
- User asks whether a tool/service/project is useful, worth using, or what its advantages are.
- User wants a quick “pros and cons” before investing time to adopt something.

## Required depth

1. **官方主页 / README** — 先读官方描述，提取核心定位和卖点。
2. **实际能力边界** — 再看文档/示例/配置，确认它真能做什么、不能做什么。
3. **现实信号** — stars、commit 频率、issue/PR 活跃度、社区反馈、竞品对比。
4. **成本与门槛** — 免费/付费、API 费用、登录态、代理、系统依赖。

## Output format

- **一句话定位**：这个工具到底是什么。
- **核心价值**：它解决什么痛点。
- **关键能力**：用 bullet 列出最主要的功能点。
- **优点**：3-5 条，简洁具体。
- **缺点/注意**：限制、风险、成本、平台依赖。
- ** verdict**：一句话结论，适合什么场景，不适合什么。

风格：**直接、无废话、不用营销腔**。用户偏好简洁，不要写成官方简介。

## Pitfalls

- 不要只复述首页文案；要区分“声称能做”和“实际能做”。
- 免费工具也要写明隐形成本：代理、登录态、账号风险、上游依赖稳定性。
- 如果用户明确问“优点”，至少给出 3 条具体优点，再给缺点，不要只说好话。
- 若平台/工具不支持中文场景，直接说明，不要含糊。

## Related

- `references/tool-eval-platform-limitations.md` — 常见调研渠道的平台覆盖限制与替代方案。