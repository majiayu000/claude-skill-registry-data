---
name: project-design-kickoff
description: 新项目"对话式迭代设计"工作流初始化。按复杂度三档（轻量/中等/复杂）建立协作脚手架——CLAUDE.md 协作契约、DesignNotes/ 讨论记录、可选 MkDocs 站点、可选参考项目管理与架构约束体系。触发词："初始化项目"、"新项目"、"project kickoff"、"project design kickoff"、"开始新项目"、"项目初始化"、"design kickoff"。
---

# Project Design Kickoff — 对话式迭代设计工作流初始化

为新项目搭建"边讨论边沉淀"的协作脚手架。**核心理念：最有价值的不是最终文档，而是讨论过程中涌现的想法和决策**。

按项目复杂度分三档初始化：

- **Level 1 轻量**：个人小项目 / POC — DesignNotes + 精简 CLAUDE.md + 首份 session（~5 分钟）
- **Level 2 中等**：中型项目 / 需对外文档 — Level 1 + MkDocs 站点 + 按项目类型切分的若干份 Doc 骨架（~15 分钟）
- **Level 3 复杂**：大型系统 / 长期迭代 — Level 2 + ReferenceItems + 架构扩展性预留 + 更完整的 Doc 体系（~30-60 分钟）

**Doc 数量由项目类型决定**（小到 2 份，大到 10 份都可能合理）——详见 `references/doc-system.md` 的"常见项目类型的 Doc 切分示例"。不要套固定清单。

## 触发条件

- "初始化项目"、"新项目设计"、"project design kickoff"、"开始新项目"、"项目初始化"
- 或者在一个空目录/刚建好的目录里要求搭建协作工作流

## 前置检查

执行前检查当前工作目录：

1. **已有 CLAUDE.md** → 告知用户，询问覆盖 / 追加协作章节 / 跳过
2. **已有 DesignNotes/** → 告知用户，询问接续（读最新 session 编号）还是重置
3. **全新目录** → 正常走完整流程

## Phase 1：收集信息 + 推荐复杂度等级

通过自然对话 + AskUserQuestion 收集：

### 必问
- **项目名称**：用于 CLAUDE.md 标题 + 目录命名
- **一句话描述**：项目做什么
- **项目类型**：Web 应用 / CLI 工具 / 库 / ML 系统 / Agent 系统 / 学术项目 / 其他
- **预期规模**：单人小项目 / 团队中型 / 长期复杂系统

### 按需问
- 当前阶段：构思期 / 调研期 / 设计期 / 开发初期
- 语言偏好：中文 / 英文（默认中文讨论 + 英文术语）
- 是否有参考资料：论文、外部项目、前期讨论

### 推荐 Level 的启发式

根据已收集信息推荐 Level（**推荐时说明理由**，用户可以调整）：

| 信号 | 推荐 |
|------|------|
| 单人 POC / 探索 / 小脚本 | **Level 1** |
| 个人/小团队中型项目 / 前后端分离 / 需要对外文档 | **Level 2** |
| 长期系统 / 多模块 / 有参考项目 / 涉及架构演进 | **Level 3** |

**最后一步**：用 AskUserQuestion 明确让用户选 Level（给出推荐默认值）。

## Phase 2：按 Level 执行初始化

根据 Level 选择对应 CLAUDE.md 模板并创建目录。

### Level 1 脚手架

读取 `references/claude-md-level-1.md` → 填充用户信息 → 写入项目根 CLAUDE.md

创建目录：
```bash
mkdir -p DesignNotes/
```

### Level 2 脚手架

读取 `references/claude-md-level-2.md` + `references/doc-system.md` + `references/mkdocs-setup.md` → 填充信息 → 写入

创建目录：
```bash
mkdir -p DesignNotes/ doc/docs/{overview,development,architecture,discussion/sessions}
```

**Doc 体系**：**识别项目的契约边界**（业务↔技术 / 模块↔模块 / 系统↔外部 / 用户↔系统 / 开发↔部署），**每个边界一份 Doc**，按项目类型命名。具体切分示例和思路参考 `references/doc-system.md`。小项目可能只需 2-3 份，不要强行凑数。

**MkDocs 站点**：生成最小 `doc/mkdocs.yml`（参考 `references/mkdocs-setup.md`）。

### Level 3 脚手架

读取 `references/claude-md-level-3.md` + `references/doc-system.md` + `references/architecture-patterns.md` + `references/references-management.md` + `references/session-workflow.md` + `references/mkdocs-setup.md` → 综合填充 → 写入

创建目录：
```bash
mkdir -p DesignNotes/ ReferenceItems/ doc/docs/{overview,development,architecture,references,discussion/sessions}
```

**Doc 体系**：按项目契约边界切分的完整 Doc 集合（Web 应用可能 6-8 份，ML/Agent 可能 5-7 份、纯库可能 2-3 份——参考 `references/doc-system.md` 示例）。

**架构扩展性 4 条硬原则**写进 CLAUDE.md 的"特别约束"章节（见 `references/architecture-patterns.md`）。

**ReferenceItems 管理规范**写进 CLAUDE.md 并建 `ReferenceItems/README.md`。

## Phase 3：创建首份 Session 文档

所有 Level 都创建：`DesignNotes/{今天日期}_session-00_{主题}.md`

**Level 2/3** 额外：
- `DesignNotes/README.md`（session 索引 + 项目状态汇总）
- `doc/docs/discussion/sessions/` 创建 session-00 的符号链接
- `doc/mkdocs.yml` nav 加入 session-00

模板：

```markdown
# Session 00 — {主题}
> 日期：{YYYY-MM-DD}
> 阶段：{项目阶段}

---

## 本次会话背景

- 项目初始化，建立了协作工作流（Level {X}）
- {用户提到的初始背景信息}

## 已确定的事项

（在讨论过程中逐步填充）

## 衍生的新问题

（在讨论过程中逐步填充）
```

## Phase 4：进入首次设计讨论

初始化完成后，**不要停在"初始化成功"**——直接进入第一轮实质性讨论：

1. 简要展示创建了哪些文件（按 Level 分类）
2. 根据用户聚焦主题开始实质性讨论
3. 讨论过程中遵循 CLAUDE.md 的协作规则，即时捕获有价值的想法到 session 文档

---

## 关键原则

1. **CLAUDE.md 是协作契约，不是 README**——它告诉 Claude 怎么与用户协作，内容要精练，每条规则都应该影响 Claude 的实际行为
2. **不要把具体操作命令硬编码到 CLAUDE.md**——原则写清楚即可，具体步骤交给 Claude 实时判断
3. **Level 不是一锤子买卖**——项目可以从 Level 1 起步，后来升到 Level 2/3。复杂度评估做错了不是世界末日
4. **参考文件是"渐进披露"的**——SKILL.md 本身不塞全部模板，按 Level 读对应 `references/*.md`，避免浪费 context
5. **不生成空洞的模板感内容**——如果某个 section 当前没有实质内容，留空或写一行占位即可

## 参考文件清单

| 文件 | 用途 | 主要 Level |
|------|------|-----------|
| `references/claude-md-level-1.md` | 轻量 CLAUDE.md 模板 | L1 |
| `references/claude-md-level-2.md` | 中等 CLAUDE.md 模板（+ doc 双轨） | L2 |
| `references/claude-md-level-3.md` | 完整 CLAUDE.md 模板（+ 架构约束、参考管理、隐私预留） | L3 |
| `references/doc-system.md` | Doc 1-8 体系说明、产出顺序、状态标记、项目类型选型 | L2, L3 |
| `references/architecture-patterns.md` | 架构扩展性 4 条硬原则（薄封装、插件化、adapter 预留、多用户预留） | L3 |
| `references/references-management.md` | ReferenceItems/ 参考项目管理规范、分层借鉴策略 | L3 |
| `references/session-workflow.md` | session doc 编号、触发规则、完整收尾流程 | L2, L3 |
| `references/mkdocs-setup.md` | MkDocs Material 最小配置 + nav 约定 | L2, L3 |
