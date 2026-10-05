---
name: flight-brainstorm
description: 执行显式、编码前的 Product Discovery，把早期或模糊的软件想法转化为用户确认的 Intent、丰富方案卡片、对比矩阵、可编辑画布和可持续 D0 文档基线。仅当用户明确调用 $flight-brainstorm，准备在 Flight Control Run 之前探索空白、稀疏、不确定或方向发生重大变化的项目时使用；禁止因模糊请求或普通开发工作隐式触发。
---

# 飞控头脑风暴

把用户想法转化为持久项目文档，但不开始实现。Codex 可以综合信息和提出建议；MCP
状态、当前用户 turn 授权、版本、provenance 和 Gate 才是规范事实。

打开第一个 Discovery Wave、记录 Intent 或解释最终审阅前，必须阅读
[Discovery 协议](references/discovery-protocol.md)。

## 只能从显式用户 turn 开始

1. 调用 `flight_status`，再调用 `flight_surface_status`。仅在本轮
   `$flight-brainstorm` authorization 与当前 Project/Host Session 匹配时，使用 exact
   Lead credential 调用 `flight_surface_select` 选择 `DISCOVERY`；禁止选择
   `FULL_COMPAT` 或在选择失败后继续。
2. 使用 `UserPromptSubmit` Hook 注入的 `start_token`，只调用一次
   `flight_discovery_start`。
3. `seed_summary` 只能是简短模型摘要。服务端会单独保存授权 turn 中的有界用户陈述；
   禁止把摘要冒充用户原话。
4. Hook 报告已有 Session 时，调用 `flight_discovery_status`，禁止创建替代 Session。
5. `PAUSED` Session 收到 `resume_token` 时，调用 `flight_discovery_resume`。
6. MCP、Host attestation、迁移或持久状态不可用时立即停止，并说明受治理 Discovery
   无法继续。禁止用聊天文本或临时文件模拟控制面。

本 Skill 禁止创建 Mission、Run、执行 Wave、Agent、业务代码、构建配置、测试、Git
状态、Private Skill、远端状态或 Computer Use 动作。

## 每次只执行一个服务端允许动作

每次工具返回后：

1. 重新读取 `state`、`version`、`active_wave`、`pending_question`、
   `blocking_reasons`、`allowed_next_actions` 和 `instruction`。
2. 只能选择 `allowed_next_actions` 中的一个动作。
3. 只使用最新结果返回的 ID 和 exact expected version。
4. 新语义动作使用新的稳定幂等键；只有完全相同的重试才能复用幂等键。
5. 错误或上下文丢失后调用 `flight_discovery_status`。禁止根据会话记忆猜测进度。
6. 禁止提交目标状态、模型计算的序号、伪造用户确认、旧版本或模型自报完成。

除非当前用户明确选择另一个已允许动作，否则优先执行列表中的第一个动作。禁止在一个
推测性 turn 中批量执行多个状态迁移。

## 依次完成四个 Discovery Wave

只能打开服务端返回的下一个 Wave kind：

1. `FRAMING`：项目名称、问题和目标用户；
2. `VALUE`：核心场景、价值和可衡量成功；
3. `BOUNDARIES`：scope、non-goals、安全、数据、成本、合规和风险；
4. `ENGINEERING`：架构方向、验证方法和计划中的开发命令。

每个 Wave：

- 提问前先综合当前证据；
- 同时最多打开一个 Question；Question 只对应一个 `intent_kind`，包含两到三个有实质
  差异的选项；
- 解释每个选项的后果，最多标记一个 recommendation；
- 原样展示 pending Question，然后等待用户下一个 turn；
- 只有收到 Question-bound token 时才能调用 `flight_discovery_answer`；
- 模型假设必须记录为 `MODEL_PROPOSAL`，不能记录为已确认事实；
- 项目事实只有绑定权威引用时才能记录为 `PROJECT_EVIDENCE`；
- `LEAD_DECISION` 只能用于服务端允许的可逆技术决定；
- 创建或更新有类型的 Artifact；
- 调用 `flight_discovery_wave_review`，修复明确缺口；只有返回允许时才能调用
  `flight_discovery_wave_complete`。

宿主支持结构化提问时优先使用；否则用普通文本展示完全相同的两到三个选项。两种路径都
禁止代替用户选择。

## 建立专业决策界面

- 在 `FRAMING` 创建并持续更新 `INTENT_CANVAS`；
- 在 `VALUE` 创建 `OPTION_CARDS` 和 `COMPARISON_MATRIX`；
- 在 `BOUNDARIES` 和 `ENGINEERING` 增加有界 proposal 或 risk；
- 只有可视 Workbench 能显著帮助比较或编辑时，调用 `flight_discovery_render`。

UI 是可选、draft-only 的交互层。UI 缺失不改变状态、authority 或完成要求。禁止把
widget permit 复制到会话、文件或其他工具。

## 最终审阅、物化并停止

四个 Wave 全部完成后：

1. 调用 `flight_discovery_review`。
2. 展示返回的 review 和 document preview，但禁止声称已接受。
3. 等待新的显式用户确认 turn。
4. 只有收到对应一次性 token 时，调用 `flight_discovery_confirm`。
5. 用户要求修改时，返回服务端给出的 exact Discovery action。
6. 用户接受后调用 `flight_discovery_materialize`；该工具不接受调用方路径或 Markdown。
7. 调用 `flight_discovery_promote`，并要求真实 P3 assessment 结果。
8. 状态变为 `DOCUMENTATION_READY` 后停止，并明确说明：实现必须等待用户在后续 turn
   显式调用 `$flight-control`。

Brainstorm turn 中禁止调用任何 Run 创建工具。即使 Document Map 已 READY，也只有后续
`$flight-control` 的 `UserPromptSubmit` handoff 才能解锁 Run 创建。
