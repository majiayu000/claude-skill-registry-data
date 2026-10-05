---
name: gstack
preamble-tier: 1
version: 1.1.0
description: |
  面向 QA 测试与真实站点试用的快速无头浏览器入口。可导航页面、与元素交互、
  校验状态、比较前后差异、截图并留证。适用于打开站点、验证部署、完整试用用户流程、
  或带截图提交 bug。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。该文件翻译 gstack 的共享 preamble、全局约束和默认浏览器工作流。 -->

# gstack

这是 gstack 的共享入口 skill。它先做全局初始化，再决定是否要提示升级、补齐 telemetry / proactive / routing 配置，最后把浏览器能力作为默认演示面暴露出来。

## 共享前置行为

- 先执行更新检查、会话登记、repo mode 检测、遥测状态检查、learnings 计数加载。
- 如果用户关闭了 `PROACTIVE`，不要主动触发其他 gstack skill；只在用户显式输入 `/qa`、`/ship` 这类命令时运行。
- 如果启用了 `SKILL_PREFIX`，对用户展示和建议 skill 时要使用 `/gstack-qa` 这类前缀；磁盘路径仍然用 `~/.claude/skills/gstack/...`。
- 如果检测到 `UPGRADE_AVAILABLE`，转到 `/gstack-upgrade` 的 inline upgrade flow；如果刚升级完成，要明确告诉用户当前版本。

## 首次会话引导

### Completeness Principle

如果 `LAKE_INTRO=no`，先向用户介绍 gstack 的 **Boil the Lake** 原则：当 AI 让边际成本接近于零时，默认做完整方案，而不是做 80 分的近似品。随后询问是否要在默认浏览器里打开 Garry Tan 的文章。

### Telemetry 选择

如果还没问过 telemetry：

- 先询问是否启用 community telemetry。
- 若拒绝，再询问是否接受 anonymous telemetry。
- 无论结果如何，都要写入 `.telemetry-prompted`。

### Proactive 选择

如果 telemetry 已处理、但还没问过 proactive：

- 询问是否允许 gstack 在对话中主动识别 `/qa`、`/review`、`/investigate` 等适配 skill。
- 无论结果如何，都要写入 `.proactive-prompted`。

### Routing Rules

如果项目根目录的 `CLAUDE.md` 里还没有 gstack 的 `## Skill routing` 段落，并且用户没拒绝过：

- 解释这是一段“一次性接线规则”，让 Claude 优先调用 `/ship`、`/qa`、`/review`、`/investigate` 等专门 workflow。
- 用户同意就把 routing 规则追加到 `CLAUDE.md`，并提交 `chore: add gstack skill routing rules to CLAUDE.md`。
- 用户拒绝则写 `routing_declined=true`，之后不再反复追问。

## 全局写作与协作约束

### Voice

- 语气要直接、具体、像 builder，不要像顾问。
- 点名文件、函数、命令，不说空话。
- 不用企业套话，也不用 AI 腔词汇。
- 用户永远拥有最终裁决权；cross-model agreement 只是建议。

### Contributor Mode

如果 `_CONTRIB=true`：

- 每个主要 workflow 阶段后都要给当前 gstack 体验打 0-10 分。
- 如果不是 10 分，而且存在可复现的 gstack 工具缺陷或体验改进点，就写 field report。
- 只报 gstack 自身问题，不把用户项目 bug、网络问题、第三方鉴权失败记进来。

### Completion Status Protocol

完成任何 skill 时，统一用以下状态收尾：

- `DONE`：全部完成，且能给出证据。
- `DONE_WITH_CONCERNS`：完成了，但要显式列出风险或遗留问题。
- `BLOCKED`：无法继续，要说明阻塞点与已尝试内容。
- `NEEDS_CONTEXT`：缺关键信息，明确写出需要什么。

### Escalation

以下情况可以直接升级为 `BLOCKED` 或 `NEEDS_CONTEXT`：

- 同一件事尝试了 3 次还没有成功。
- 涉及安全敏感改动，但无法验证。
- 任务范围已经超出自己能自证的边界。

## Telemetry

- 在 skill 结束时记录 outcome：`success`、`error`、`abort`，判不清时写 `unknown`。
- 既写本地 JSONL，也在配置允许时写远端遥测。

## Plan Mode 例外

如果当前在 plan mode：

- 允许更新 plan 文件本身，因为它是活文档。
- 退出 plan mode 前，要在 plan 文件里写一段 `## GSTACK REVIEW REPORT`，概述本轮 review / plan 的状态、发现、后续建议和 readiness。

## 默认浏览器工作流

根级 `gstack` skill 同时把浏览器能力当作默认工具面暴露出来，核心场景包括：

- QA 测试：导航、查看可交互元素、填写表单、验证结果。
- 部署验证：打开目标 URL，检查渲染状态、控制台错误、关键交互。
- Dogfooding：完整跑一遍真实用户流程并留图证。
- 响应式检查：不同 viewport 截图、特定区域截图、元素截图。
- 表单 / 上传 / 对话框：验证空提交、错误态、文件上传、确认弹窗。
- 鉴权页面：通过 `/setup-browser-cookies` 导入 cookies 后继续测试。

## Snapshot 与命令族

浏览器能力默认强调：

- snapshot 优先，用于看结构和交互标签。
- annotated screenshot 用于给 bug report 和用户展示证据。
- compare / before-after 适合部署前后或多环境比对。
- 命令按导航、读取、交互、检查、视觉、snapshot、标签页、server 几类组织。

## 使用建议

- 想做完整端到端测试时，优先切到 `/qa` 或 `/qa-only`。
- 想做纯浏览器探索、截图、验证页面状态时，用 `/browse`。
- 碰到 CAPTCHA、多因素认证、复杂登录流时，优先使用 `/connect-chrome` 或 user handoff。
