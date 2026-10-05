---
name: devex-review
preamble-tier: 3
version: 1.0.0
description: |
  开发者体验实测审计。使用 browse 工具真正去 TEST 开发者体验：
  浏览文档、尝试 getting started、计时 TTHW、截图错误信息、评估 CLI help。
  输出带证据的 DX scorecard，并与 /plan-devex-review 的预期分数做对照
  （boomerang：计划说 3 分钟，现实可能是 8 分钟）。
  当用户要求“测试 DX”“做 DX audit”“developer experience test”
  或“试跑 onboarding”时使用；在 developer-facing 功能刚 ship 后也适合主动建议。 (gstack)
  Voice triggers（语音别名）："dx audit"、"test the developer experience"、
  "try the onboarding"、"developer experience test"。
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /devex-review

这是 live DX audit。不是只看文档写得像不像样，而是真的按开发者路径去试、去卡、去截图。

## 核心目标

- 验证 getting started 是否顺畅
- 实测 API / CLI / SDK 的可发现性与人体工学
- 检查错误消息、文档结构、升级路径和开发环境体验
- 形成带证据的 DX scorecard，并与计划阶段的承诺做回旋镖对比

## 审计范围

- 可通过 browse 测试的 surface：docs、web console、API playground、web dashboard
- 无法直接 browse 的部分：本地安装摩擦、CLI 输出质量、repo 内工具链，需要结合 bash / 文件审阅

## 主流程

1. `Target Discovery`：
   - 确认 URL、文档入口和 prior `/plan-devex-review` 基线
2. `Getting Started Audit`：
   - 按真实步骤记录时间、摩擦等级和证据
3. `API / CLI / SDK Ergonomics Audit`
4. `Error Message Audit`
5. `Documentation Audit`
6. `Upgrade Path Audit`
7. `Developer Environment Audit`
8. `Community & Ecosystem Audit`
9. `DX Measurement Audit`

## 必备输出

- 带 evidence 的 `DX Scorecard`
- 若存在计划基线，输出 `Boomerang Comparison`
- `Review Log`
- 明确 next steps，说明应该先修哪些 DX 缺口，再回头复测

## 关键规则

- 每一维都要给证据来源，截图优先，文件引用次之，不能靠猜。
- 编号问题，给出可执行修复建议。
- 如果计划阶段分数和实际体验差距明显，要明确指出落差。
