---
name: create-sub-agent
description: 指导创建符合项目规范的自定义子 Agent。触发："创建子 agent"、"新建 agent"、"create agent"、"create sub-agent"，或为评审/测试/文档/信息收集等领域建专用 agent。
---

# 创建自定义子 Agent

## 概述

**目的**：指导主 Agent 从需求收集到产出完整子 Agent（`agent.md` + `rules/` + `skills/`），复用 `agents/sub-agent/agent.md` 的成熟提示词结构，保证子 Agent 质量与一致性。

**功能**：
- 生成子 Agent 目录骨架（`agents/{agent-name}/`）
- 按 sub-agent 结构编写 `agent.md` 提示词
- 按需创建 `rules/`（专属规则）与 `skills/`（专属能力）
- 输出前对照验证清单自检

**使用场景**：
- 用户说"创建子agent"、"新建一个agent"、"create agent"
- 需要为特定业务领域（评审、测试、文档编写、信息收集）建立专用子 Agent
- 现有子 Agent 需要按新定位重构提示词

## 前置守门

创建前快速自检（满足任一则不新建，与用户说明后停止）：
- 现有 `agents/` 中已有功能重叠的 agent → 建议扩展而非新建
- 用户实际只需通用辅助能力，无需领域定制 → 直接委派 `sub-agent` 即可

## 开始之前：收集需求

向用户确认以下信息（可从上下文推断，缺省时做合理假设并注明）：

1. **Agent 名称**：kebab-case 小写短横线，语义化（如 `course-reviewer`、`api-tester`）
2. **角色定位**：一句话说明该 agent 是做什么的（评审者 / 测试执行者 / 文档编写者…）
3. **任务边界**：可做什么、不可做什么（越权行为清单）
4. **使用场景**：主 Agent 在什么节点委派它
5. **配套资产**：是否需要专属 `rules/` 或 `skills/`

## 目录结构

每个子 Agent 独占一个目录，放在 `agents/`（或 `.agents/`）下：

```
agents/{agent-name}/
├── agent.md      # 必需：子 Agent 的描述与提示词
├── rules/        # 可选：agent 专属规则（规范同 create-rules）
└── skills/       # 可选：agent 专属能力（规范同通用 skill）
```

| 存放位置 | 说明 |
|----------|------|
| `agents/` | 项目内 agent 资产，随项目走（默认） |
| `.agents/` | 隐藏目录，不希望暴露在常规列表时使用 |

### 各目录职责

| 目录/文件 | 职责 | 规范来源 |
|-----------|------|----------|
| `agent.md` | 子 Agent 提示词全文，主 Agent 委派时作为独立 AI 调用提示词 | 参考 `agents/sub-agent/agent.md` |
| `rules/` | agent 专属行为规则（如"只读不改"、"必须三段式上报"） | create-rules skill |
| `skills/` | agent 专属能力（如"课程评审要点"、"API 测试方法"） | create-skill skill（通用规范） |

## 创建流程

### 阶段 1：搭建目录骨架

在 `agents/` 下创建 `{agent-name}/` 目录，按需创建 `rules/`、`skills/` 子目录。

### 阶段 2：编写 agent.md

参考 `agents/sub-agent/agent.md` 结构编写（完整模板见 [reference.md](reference.md)）。核心章节：

1. **frontmatter**：`description`（角色 + 职责 + 使用时机，第三人称）、`provider: user`
2. **角色定位**：你是什么、被谁委派、定位标签（执行者/低成本/诚实上报）
3. **能力假设**：所需能力表 + 缺失时显式上报
4. **文件操作权限边界**：可写 / 需主 Agent 确认 / 禁写 三档（硬约束）
5. **任务边界**：可做清单 + 不可做清单（越权拒绝，禁再委派）
6. **输入契约**：【任务】【背景】【目标】【验收标准】【输出格式】五字段
7. **执行要求**：token 节俭、结论前置、重试 ≤ 2 次、副作用清理
8. **输出契约**：三段式（结论 / 证据 / 自检与失败声明）
9. **失败上报机制**：不达标显式声明、重试上限、允许主 Agent 兜底
10. **质量自检清单**：返回前过一遍

### 阶段 3：创建配套 rules/

agent 专属规则遵循 **create-rules skill** 规范（frontmatter 五字段：`description` / `alwaysApply` / `enabled` / `updatedAt` / `provider`；内容结构：规则 / 执行 / 例外）。直接调用 `create-rules` skill 执行，规范以该 skill 为准，此处不重复。

> 若运行环境无 `create-rules` skill：按最小规范直接创建——frontmatter 五字段 + 正文分「规则 / 执行 / 例外」三节，规则文件 ≤ 100 行。

### 阶段 4：创建配套 skills/

agent 专属能力遵循 **通用 skill 规范**（create-skill skill）：`SKILL.md` + YAML frontmatter（`name` / `description`）+ AI 说明层（目的 / 功能 / 使用场景），渐进式展开（`reference.md` / `examples.md` / `scripts/`）。直接调用 `create-skill` skill 执行，规范以该 skill 为准，此处不重复。

> agent 专属 skill 通常聚焦单一领域、规模小，不必完整走 create-skill 全流程：给出 `SKILL.md`（frontmatter + 概述 + 核心指令）即可，按需补 reference/examples。若运行环境无 `create-skill` skill，按上述最小结构直接创建。

> `skills/` 下的专属 skill 是独立资产，由 agent.md 或主 Agent 在委派时按需加载/引用，不嵌入 agent.md 正文。

### 阶段 5：验证

对照下方清单自检，通过后向用户展示产物摘要。

## 验证清单

- [ ] 目录结构符合 `agents/{name}/agent.md` + `rules/` + `skills/`
- [ ] agent.md frontmatter 含 `description` 与 `provider`
- [ ] agent.md 含核心章节（角色定位 / 能力假设 / 权限边界 / 任务边界 / 输入契约 / 执行要求 / 输出契约 / 失败上报 / 自检清单）
- [ ] 输出契约为三段式（结论 / 证据 / 自检与失败声明）
- [ ] 权限边界为三档（可写 / 需确认 / 禁写）
- [ ] 含"禁再委派"约束（防止委派链失控）
- [ ] `rules/` 文件符合 create-rules frontmatter 规范
- [ ] `skills/` 文件符合 create-skill 规范
- [ ] 全文术语一致、无 Windows 风格路径

## 其他 skill 如何引用本 agent

其他 skill 的 SKILL.md 中引用本 agent 时，直接用 **`use_agent({agent-name})`**（如 `use_agent(course-reviewer)`）即可：

- 不写文件路径、不重复 agent 内容
- agent 定义唯一事实源在 `agents/{agent-name}/agent.md`，引用方按需裁剪使用
- 委派时仍按 agent.md 的输入契约传入【任务】【背景】【目标】【验收标准】【输出格式】

## 更多资源

- agent.md 完整模板与写作要点，参见 [reference.md](reference.md)
- 完整创建示例，参见 [examples.md](examples.md)
- 规则规范：调用 `create-rules` skill
- skill 规范：调用 `create-skill` skill
