---
name: trade-skill-development-superpowers
description: Use when planning or upgrading an internal skill/workflow for business operations, especially when turning a messy idea into a structured skill plan, migration plan, acceptance checklist, or packaging decision. Particularly useful for Obsidian knowledge base consolidation, workspace migration, content library cleanup, and integrating multiple workbenches into one operating system.
---

# 外贸 Skill 开发超能力

这个 Skill 不是业务节点执行器，而是内部方法层。

适用任务：

- 把一个模糊方向收敛成可开发的 Skill 立项
- 把一个已有方向整理成迁移计划、整合计划或工作台重构计划
- 判断一个方向该做单节点、组合包，还是只做内部方法层
- 给课程版、客户版、内部版拆出不同表达口径
- 为内容库、工作台、Obsidian 仓库整合设计阶段、边界和验收标准

优先输出：

1. 业务目标与成功标准
2. 当前状态与主要断点
3. 最小迁移范围或最小 Skill 范围
4. 分阶段动作
5. 风险与人工复核点
6. 验收标准

## 工作流

### 1. 先收敛任务类型

先判断当前任务属于哪一类，只选一个主类型：

- `新 Skill 立项`
- `已有 Skill 增强`
- `链路串联`
- `发布包装`
- `内容库/工作台迁移`

如果用户同时提了多个目标，先把“当前最需要决策的主任务”单独拎出来。

### 2. 强制拉齐 6 个最小问题

如果上下文里没有明确答案，就根据已有信息先给出保守假设：

- 当前要整合的对象是什么
- 为什么现在要做
- 完成后必须达到什么状态
- 哪些内容必须保留原结构或原链接
- 哪些内容允许重组
- 哪些动作必须人工确认

### 3. 输出结构固定

默认按下面结构输出，不要跳着讲：

```text
一、任务定义
二、当前状态
三、目标状态
四、迁移/建设范围
五、分阶段计划
六、风险与边界
七、验收标准
八、下一步动作
```

### 4. 如果是 Obsidian 迁移任务

优先把问题拆成 5 层：

1. Vault 边界
2. 内容类型分层
3. 工作台分层
4. 链接/附件/模板迁移风险
5. 日常使用路径

不要一上来讨论插件和自动化，先把结构和迁移顺序定清楚。

读取 [references/obsidian-migration-planning.md](references/obsidian-migration-planning.md)。

### 5. 如果任务需要产出正式立项

输出内容必须能映射到：

- `模板/skill立项模板.md`
- `模板/skill验收清单.md`
- `模板/合集收录标准.md`

如果当前任务更像内部方法层，不要硬套成对外业务 Skill。

### 6. 包装口径规则

同一个方向，默认拆 3 层口径：

- 内部版：强调研发流程、迁移顺序、复核点
- 课程版：强调为什么这样设计、如何照着做
- 客户版：强调结果、输入输出、人工确认点

客户版不讲 agent engineering、不讲重工程流程。

## Obsidian 迁移专用规则

当任务涉及 Obsidian 内容库、知识库、工作台整合时，默认做这些约束：

- 先规划，再迁移；不先做大批量搬运
- 先定义目标 Vault 结构，再决定旧内容如何映射
- 先识别高频工作台，再整理历史资料库
- 先保链接与附件，再谈命名美化
- 任何会破坏现有引用、嵌入、模板调用的动作，都标成“人工确认”

输出时至少明确：

- 哪几类内容先迁
- 哪几类内容后迁
- 哪些内容只归档不重构
- 哪些目录是“工作台”
- 哪些目录是“资料库”
- 哪些目录是“成品输出层”

## 默认交付物

根据任务大小，默认从下面几种里选 1 到 3 个：

- 迁移计划
- 目录结构草案
- 内容分层规则
- 验收清单
- 风险清单
- 后续 Skill 立项建议

## 禁止事项

- 不把推断写成既定事实
- 不默认用户愿意一次性迁完整个内容库
- 不把插件选型当成迁移计划主体
- 不先讨论自动化脚本，除非结构已经稳定
- 不为了“看起来完整”而跳过人工复核点
