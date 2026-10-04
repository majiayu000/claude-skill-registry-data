---
name: agent-smith
description: Use when a complex task needs parallel decomposition into independent subtasks, when multiple agents must work simultaneously without conflicts, or when recursive task delegation is required
---

# Agent Smith

实现递归自相似多智能体系统的 Skill。每个智能体（史密斯）拥有独立的工作空间，通过目录隔离协议达成无冲突的并行任务分解与执行。

## Overview

Agent Smith 是一个递归自相似的多智能体协作框架。每个智能体（史密斯）遵循相同的协议，在自己的工作空间内独立运行，通过父子间的 inbox/outbox 通信完成复杂任务的分解与汇总。

## When to Use

在以下场景触发本 Skill：

- 用户请求"创建多智能体系统"或"设置 Agent Smith"
- 任务需要分解为多个并行子任务
- 需要协调多个 Agent 同时工作
- 复杂任务需要递归分解处理
- 要求无冲突的并行执行环境

## When NOT to Use

在以下场景请勿触发本 Skill：

- 单个 Agent 可在 15 分钟内独立完成的任务
- 子任务之间存在严格线性依赖（每一步必须等待上一步完成）
- 仅需单 Agent 即可完成，并行执行无收益
- 任务已充分细化，无需进一步分解

## Hard Constraints (Quick Reference)

以下限制由史密斯协议强制执行。修改这些值需要同时更新 `SKILL.md` 和 `smith.md`。

| 限制 | 值 |
|------|-----|
| 最大递归深度 | 3（Level 0 根节点 → 最大 Level 3） |
| 每层最大子代理数 | 5 |
| Level ≥ 3 行为 | 禁止分解，必须直接执行 |

## 核心概念

**史密斯 (Smith)** 是自相似的智能体单元，每个史密斯拥有唯一 ID 和层级，能够执行任务、分解任务、创建子史密斯并汇总结果。所有史密斯遵循相同的协议，形成递归结构。

所有史密斯均受上述 [Hard Constraints](#hard-constraints-quick-reference) 约束。

**无冲突协议** 通过严格的目录隔离实现并行安全：每个史密斯只能写入自己的 `private/` 和 `outbox/`，只能读取自己 `inbox/` 中父史密斯分配的任务。父史密斯拥有创建子目录和写入子史密斯 inbox 的专属权限。

## 目录结构

```
.agent-smith/
├── smiths/
│   ├── smith-root/             # 根史密斯
│   │   ├── smith.md            # 史密斯定义（只读）
│   │   ├── inbox/              # 任务队列（外部/父写入，自己读取）
│   │   ├── private/            # 私有工作区
│   │   ├── outbox/             # 结果输出
│   │   │   └── result.md
│   │   └── children/           # 子史密斯目录
│   │       └── smith-001/
│   │           ├── smith.md
│   │           ├── inbox/      # 父写入，子读取
│   │           ├── private/
│   │           ├── outbox/
│   │           └── children/
└── results/
    └── final.md                # 最终结果
```

## 初始化矩阵

当用户请求初始化 Agent Smith 时，执行以下步骤：

**1. 创建目录结构**

创建根史密斯环境：
- `.agent-smith/smiths/smith-root/inbox/` —— 任务队列
- `.agent-smith/smiths/smith-root/private/` —— 私有工作区
- `.agent-smith/smiths/smith-root/outbox/` —— 结果输出
- `.agent-smith/smiths/smith-root/children/` —— 子史密斯容器
- `.agent-smith/results/` —— 最终结果

**2. 读取 `smith.md` 模板**

从 `smith.md` 读取史密斯定义模板。

**3. 替换占位符**

替换模板中的变量：
- `{SMITH_ID}` → `smith-root`
- `{PARENT_ID}` → `none`
- `{LEVEL}` → `0`

**4. 写入根史密斯定义**

将替换后的内容写入 `.agent-smith/smiths/smith-root/smith.md`。

**5. 创建任务文件**

基于 `templates/task.md.template` 创建根任务文件 `.agent-smith/smiths/smith-root/inbox/task-root.md`。

替换模板占位符：
- `{TITLE}` → 任务标题
- `{TASK_ID}` → `root`
- `{SMITH_ID}` → `smith-root`
- `{PARENT_TASK_ID}` → `none`
- `{TIMESTAMP}` → 当前时间
- `{LEVEL}` → `0`
- `{DESCRIPTION}` → 任务描述
- `{CONTEXT}` → 相关上下文
- `{EXPECTED_OUTPUT}` → 期望输出

**6. 生成启动指南**

在 `.agent-smith/smiths/smith-root/private/START_HERE.md` 生成启动指南，包含：
- 当前身份确认
- 任务文件位置
- 执行流程说明
- 输出要求

## 创建子史密斯

当父史密斯需要创建子史密斯时，执行以下步骤：

**前置检查（强制）**

创建任何子史密斯之前，必须确认：
- [ ] 当前层级 < 3（若层级 ≥ 3，停止——直接执行）
- [ ] 现有子代理数量 < 5（若已达 5 个，停止——直接执行或重新分解）

**1. 确定新史密斯 ID**

按序号递增生成 ID，如 `smith-001`、`smith-002`。

**2. 创建子目录**

在父史密斯的 `children/` 下创建 `{smith-id}/` 目录结构：
- `inbox/` —— 父写入任务，子读取
- `private/` —— 私有工作区
- `outbox/` —— 结果输出
- `children/` —— 子史密斯容器

**3. 读取模板并替换**

读取 `smith.md` 模板，替换占位符：
- `{SMITH_ID}` → 新 ID（如 `smith-001`）
- `{PARENT_ID}` → 当前史密斯 ID
- `{LEVEL}` → 当前层级 + 1

**4. 写入子史密斯定义**

将替换后的内容写入子目录的 `smith.md`。

**5. 生成子任务文件**

基于 `templates/task.md.template` 在子史密斯的 `inbox/` 下创建任务文件 `task-{SMITH_ID}.md`。

替换模板占位符：
- `{TITLE}` → 子任务标题
- `{TASK_ID}` → 子史密斯 ID（如 `smith-001`）
- `{SMITH_ID}` → 子史密斯 ID
- `{PARENT_TASK_ID}` → 父任务 ID
- `{TIMESTAMP}` → 当前时间
- `{LEVEL}` → 当前层级 + 1
- `{DESCRIPTION}` → 子任务描述
- `{CONTEXT}` → 父上下文
- `{EXPECTED_OUTPUT}` → 期望输出

确保任务文件只写入该子史密斯的 `inbox/`，不得写入任何其他史密斯的目录。

**6. 生成子史密斯启动指南**

在子史密斯的 `private/START_HERE.md` 生成启动指南，包含：
- 子史密斯身份确认
- 父史密斯引用
- 任务文件位置
- 执行约束说明

## 执行流程

1. 读取 `inbox/` 中的任务
2. 分析任务复杂度
3. 判断：能否直接完成？
   - **是** → 执行任务 → 将结果写入 `outbox/result.md` → 结束
   - **否** → 对照 [Hard Constraints](#hard-constraints-quick-reference) 检查当前层级
     - 若层级 ≥ 3：**必须直接执行**（禁止分解）
     - 若层级 < 3：设计子任务（最多 5 个）→ 创建子史密斯目录 → 在子史密斯 `inbox/` 中创建任务文件 → 等待子结果 → 汇总 → 写入 `outbox/result.md` → 结束

## 最终结果汇总

根史密斯（Level 0）在完成自身 `outbox/result.md` 后，还有一项额外职责：

- 将根史密斯的 `outbox/result.md` 复制或汇总到 `.agent-smith/results/final.md`

该文件作为用户获取多智能体会话完整输出的统一入口。

## 写约束协议

**允许写入**：
- 自己的 `private/` —— 草稿、思考、临时文件
- 自己的 `outbox/result.md` —— 最终结果
- 自己的 `children/` —— 创建子史密斯目录（父权限）
- 自己 `children/` 下子史密斯的 `inbox/` —— 创建子任务（父权限）

**禁止写入**：
- 其他史密斯的 `private/` 或 `outbox/`
- 父史密斯的任何目录
- 其他史密斯的 `inbox/`（只能写自己创建的子史密斯的 inbox）

## 常见错误与修复

### Red Flags —— 停止并重新评估

遇到以下任何情况时，**禁止**继续分解，应直接执行：

- 子任务预计耗时少于 15 分钟
- 当前层级已 ≥ 3，仍在考虑分解
- 同层子代理数量将超过 5 个
- 子任务之间耦合紧密或需要频繁同步

### 错误：过度分解

**症状：** 为简单任务创建子史密斯，子任务只需几分钟即可完成。
**修复：** 若任务少于 3 个主要步骤或预计 15 分钟内可完成，直接执行。分解带来的协调开销会超过收益。

### 错误：超出递归深度

**症状：** 在 Level 3 或更深层级仍试图创建子史密斯。
**修复：** 硬限制为 Level 3。当层级 ≥ 3 时，必须直接执行。若任务仍过大，应优化任务定义而非违反协议。

### 错误：写入错误目录

**症状：** 在自己子代理的 `inbox/` 以外创建任务文件，或修改其他史密斯的 `private/` 或 `outbox/`。
**修复：** 重新阅读 [写约束协议](#写约束协议)。只允许写入：自己的 `private/`、自己的 `outbox/`、自己的 `children/`、自己子代理的 `inbox/`。

### 错误：子代理 ID 冲突

**症状：** 两个同层子史密斯使用相同 ID（例如同一父节点下有两个 `smith-001`）。
**修复：** 每个父节点使用严格递增序号（`smith-001`、`smith-002`...）。创建目录前验证无冲突。

## 参考资料

- [核心概念详解](./references/concepts.md) —— 史密斯的定义、目录隔离机制、递归分解策略
- [协议规范](./references/protocol.md) —— 详细的通信协议和约束规则
- [最佳实践](./references/best-practices.md) —— 任务分解原则、结果汇总技巧

## 示例

- [市场研究示例](./examples/market-research.md) —— 展示如何将复杂的市场研究任务分解为 4 个并行子任务
- [代码重构示例](./examples/code-refactor.md) —— 展示如何并行处理大规模代码重构

## 安装

将此目录复制到 Claude Code skills 目录：

```bash
# 从仓库根目录执行
cp -r agent-smith/agent-smith ~/.claude/skills/agent-smith
```
