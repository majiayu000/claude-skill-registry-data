---
name: one-person-company
description: "当需要根据任务组建临时 AI Agent 团队协作时使用，覆盖战略、产品、设计、开发、测试、营销、运营、销售等全流程，像拥有完整团队一样独立运作。"
argument-hint: "[任务描述]"
disable-model-invocation: true
---

# One Person Company - 组建你的 AI 团队

你需要根据下面的任务，从公司现有的 AI Agent 中挑选最合适的成员，组建一支临时团队来协作完成。

## 任务

$ARGUMENTS

## 可用 Agent

以下是团队可用的所有专业 Agent。每个 Agent 的完整角色定义存放在 `agents/<name>/SKILL.md`：

| Agent | 文件路径 | 职能 |
|-------|----------|------|
| CEO | `agents/ceo-bezos/SKILL.md` | 战略决策、商业模式、PR/FAQ、优先级 |
| CTO | `agents/cto-vogels/SKILL.md` | 技术架构、技术选型、系统设计 |
| 产品设计 | `agents/product-norman/SKILL.md` | 产品定义、用户体验、可用性 |
| UI 设计 | `agents/ui-duarte/SKILL.md` | 视觉设计、设计系统、配色排版 |
| 交互设计 | `agents/interaction-cooper/SKILL.md` | 用户流程、Persona、交互模式 |
| 全栈开发 | `agents/fullstack-dhh/SKILL.md` | 代码实现、技术方案、开发 |
| QA | `agents/qa-bach/SKILL.md` | 测试策略、质量把控、Bug 分析 |
| 营销 | `agents/marketing-godin/SKILL.md` | 定位、品牌、获客、内容 |
| 运营 | `agents/operations-pg/SKILL.md` | 用户运营、增长、社区、PMF |
| 销售 | `agents/sales-ross/SKILL.md` | 定价、销售漏斗、转化 |

## 执行步骤

### 1. 分析任务，选择成员

根据任务性质，选择 2-5 个最相关的 Agent 作为团队成员。选人原则：
- **只选必要的**：不是人越多越好，精准匹配任务需求
- **考虑协作链**：如果任务涉及从设计到开发，确保链路上的关键角色都在
- **避免冗余**：职能重叠的不要同时选

向创始人简要说明你选了谁、为什么选他们，然后立即开始组建。

### 2. 组建 Agent Team

使用 Agent Teams 功能组建临时团队：
- 创建团队，team_name 基于任务简短命名（英文、kebab-case）
- 为每个成员创建具体的任务（TaskCreate），任务描述要包含足够上下文
- 用 Task 工具 spawn 每个 teammate，`subagent_type` 选 `general-purpose`
- **加载角色设定**：先使用 Read 工具读取对应 Agent 的 `agents/<name>/SKILL.md` 文件，将完整内容注入到 spawn prompt 中作为角色设定
- spawn teammate 时通过 prompt 告知：你的角色设定（来自文件内容）、要完成的具体任务、产出文档存放在 `docs/<role>/` 目录下

### 3. 协调与汇总

- 作为 team lead 协调各成员工作
- 收集各成员产出，汇总为统一的结论或方案
- 如有分歧，列出各方观点供创始人决策
- 完成后清理团队资源

## 注意事项

- 所有沟通使用中文，技术术语保留英文
- 每个成员产出的文档按约定存放在 `docs/<role>/` 下
- 团队是临时的，任务完成后即解散
- 创始人是最终决策者，Agent 提供建议但不替代决策
