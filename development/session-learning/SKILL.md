---
name: session-learning
description: 分析当前会话并持久化学习到三层存储（项目 CLAUDE.md、用户 CLAUDE.md、Memory MCP）
---

# 会话学习技能

分析当前会话，提取有价值的学习内容，并持久化到合适的存储层。

## 分析维度

回顾会话，关注：

| 维度 | 关注点 |
|------|--------|
| **进展顺利** | 成功的方法、有效的解决方案、好的决策 |
| **进展不顺** | 失败的尝试、错误的方向、浪费时间的地方 |
| **用户分歧** | 用户纠正你的地方、拒绝的建议、表达不满的地方 |
| **推断偏好** | 沟通风格、工具偏好、代码风格、工作流习惯 |

## 三层分类

### 决策树

```
对于每个学习项：
│
├─ 是否与当前项目的代码/架构/工具链直接相关？
│   └─ 是 → 项目 CLAUDE.md
│
├─ 是否是用户的通用偏好（适用于所有项目）？
│   └─ 是 → 用户 CLAUDE.md
│
└─ 是否是交互模式/问题解决方法/跨项目经验？
    └─ 是 → Memory MCP
```

### 分类示例

| 学习内容 | 层级 | 理由 |
|----------|------|------|
| "这个项目用 Vitest 测试" | 项目 | 项目特定工具 |
| "用 `bun test` 运行测试" | 项目 | 项目特定命令 |
| "React hooks 中不要用 async/await" | 项目 | 项目特定陷阱 |
| "用户偏好 bun 而非 npm" | 用户 | 跨项目工具偏好 |
| "用户偏好简洁响应" | 用户 | 沟通风格 |
| "用户偏好中文交流" | 用户 | 语言偏好 |
| "动手前先问清楚需求" | Memory | 交互模式 |
| "用户精通 TypeScript" | Memory | 专业领域 |
| "调试时先查日志" | Memory | 问题解决方法 |

## 持久化指南

### 第一层：项目 CLAUDE.md

**位置**: `{repo}/CLAUDE.md` 或 `{repo}/.claude/CLAUDE.md`

**优先级**: 如果 `.claude/CLAUDE.md` 存在，优先使用它（项目内聚）；否则使用根目录的 `CLAUDE.md`。

**插入策略**（保持文档组织性）:
1. **先阅读整个 CLAUDE.md**，理解现有结构和 sections
2. **找到语义上合适的位置**插入学习内容：
   - 如果已有相关 section（如 "Plugin Development Best Practices"），将学习项合并到该 section
   - 如果学习项是新类别，在逻辑上相邻的 section 附近创建新 section
3. **禁止简单追加到文件末尾**——这会破坏文档组织性
4. 编辑后整个 CLAUDE.md 应仍然结构清晰、主题分组合理

**工具**: 使用 `Edit` 工具（精确插入到合适位置）

### 第二层：用户 CLAUDE.md

**位置**: `~/.claude/CLAUDE.md`

**插入策略**（保持文档组织性）:
1. **先阅读整个 CLAUDE.md**，理解现有结构
2. **找到语义上合适的位置**插入偏好：
   - 如果已有相关 section（如 "个人偏好设置"、"工作原则"），将偏好合并到该 section
   - 如果偏好是新类别，在逻辑上相邻的 section 附近添加
3. **禁止简单追加到文件末尾**

**工具**: 使用 `Edit` 工具

### 第三层：Memory MCP

**实体类型**:
- `interaction_pattern` - 用户喜欢的工作方式
- `problem_solving` - 有效的调试/解决方法
- `expertise_area` - 用户的技能和知识领域
- `learning_history` - 会话学习摘要

**工具**:
```
# 创建新实体
mcp__memory__create_entities

# 给现有实体添加观察
mcp__memory__add_observations

# 创建关系
mcp__memory__create_relations
```

**关系类型**:
- `learned_from` - 将学习链接到用户
- `applies_to` - 将模式链接到领域
- `solves` - 将方法链接到问题类型

## 用户确认流程

**重要**: 持久化前必须展示分类结果并获得用户确认。

### 第一步：展示分类

```markdown
## 会话学习摘要

### 项目 CLAUDE.md（下次会话自动加载）
- [项 1]
- [项 2]

### 用户 CLAUDE.md（所有项目自动加载）
- [偏好 1]

### Memory MCP（用 /recall 命令召回）
- [模式 1]
- [经验 1]

**确认？**（y/n，或建议修改）
```

### 第二步：等待确认

用户确认或修改前**不要**持久化。

### 第三步：执行持久化

确认后：
1. 插入到项目 CLAUDE.md 的合适位置（如有项目级内容）
2. 插入到用户 CLAUDE.md 的合适位置（如有用户级内容）
3. 在 Memory MCP 中创建/更新实体（如有跨项目内容）
4. **执行 Memory MCP 整理（MANDATORY）** - 见下方 checklist
5. 报告保存了什么、保存到哪里

### 第四步：Memory MCP 整理（MANDATORY）

⚠️ **CRITICAL**: 每次使用 Memory MCP 后必须执行此 checklist。跳过此步骤是**不完整的执行**。

```markdown
## Memory MCP Cleanup Checklist

1. [ ] **READ**: 调用 `mcp__memory__read_graph` 查看当前图谱
2. [ ] **ANALYZE**: 识别以下问题：
   - 重复/相似实体（可合并）
   - 不一致的命名（如同一用户有多个实体名）
   - 孤立关系（指向不存在的实体）
   - 过时/临时实体（不再相关）
3. [ ] **CLEANUP**: 执行必要的整理操作：
   - `mcp__memory__add_observations` - 合并内容到现有实体
   - `mcp__memory__delete_entities` - 删除重复/过时实体
   - `mcp__memory__delete_relations` - 删除孤立关系
   - `mcp__memory__create_relations` - 修复不一致的关系
4. [ ] **REPORT**: 向用户报告整理了什么
```

**如果图谱已经干净**：明确说明"已检查图谱，无需整理"。

## 错误处理

- 如果 CLAUDE.md 不存在，创建并添加适当的头部
- 如果 Memory MCP 不可用，通知用户并跳过该层
- 如果用户拒绝所有项目，确认并不持久化任何内容
