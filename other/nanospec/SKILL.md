---
name: nanospec
description: 把一次变更分阶段沉淀成可复读的产物。包含五个动作 — propose（写"为什么 / 改什么 / 影响什么"）、plan（拆"怎么做 / 分几步"）、apply（按 tasks 逐条实现并勾掉）、align（出现偏差或临时变更时纠偏并回写）、run（按现有进度一键跑完）。产物统一落到 nanospec/<YYYYMMDD-task-name>/。命令 `/propose` `/plan` `/apply` `/align` `/run` 进来时跳到对应 phase。
---

# nanospec

## 何时使用

- 需要在动手前把一次变更的范围与方案讲清楚
- 需要分阶段沉淀（proposal / design / tasks），且后续可被人和 agent 复读
- 需要在实现中途处理偏差或临时变更而不偷偷绕开
- 命令路由：`/propose` `/plan` `/apply` `/align` `/run` 进来时直接走对应 phase

不适用：

- 一两行能说清楚的小改动（直接做更省事）
- 探索性研究，还不知道要不要做（先用别的笔记承载）
- 完全推翻当前变更：那不是 align，应起一个新的 propose

## 命名规范

变更目录名一律为 `YYYYMMDD-task-name`：

- 日期前缀用本地当天日期（如 `20260506`）
- 任务名 kebab-case（小写 + 连字符），描述要做什么（如 `add-user-auth`）
- 完整示例：`20260506-add-user-auth`

不要省略日期前缀。

## 产物约定

```
nanospec/<name>/
├── brief.md          # 用户原始需求（run 场景 A 自动写入）
├── proposal.md       # propose 阶段：Why / What Changes / Impact
├── design.md         # plan 阶段：Context / Goals / Decisions / Trade-offs
├── tasks.md          # plan 阶段：可勾选任务清单（apply 阶段勾掉）
└── alignment.md      # align 阶段：偏差日志（按需创建）
```

## 阶段路由

调用进来时，按 phase 跳到对应小节执行；如未指定 phase，先按以下规则推断：

- `/propose <args>` → propose
- `/plan` → plan
- `/apply` → apply
- `/align <args>` → align
- `/run <args>` → run（编排器）

---

## Phase: propose

把一次变更先写成 proposal，作为后续 plan + apply 的入口。

**输入**：

- 完整变更名 `YYYYMMDD-task-name`，或
- 一段对要做什么的描述（自动派生）

如果两个都没有，先用 AskUserQuestion 问"这次要做什么变更？"，然后再继续。**没问清楚之前不要往下做。**

**步骤**：

1. 确认变更名
   - 已给完整名：校验是否符合 `YYYYMMDD-task-name`；不符合就改成符合的并告知用户
   - 只给了任务描述：用今天日期 + 派生 kebab-case 任务名（"add user authentication" → `20260506-add-user-auth`）
   - 同名已存在：问用户是要继续旧的还是另起一个
2. 建目录 `nanospec/<name>/`（不存在则 mkdir）
3. 写 `nanospec/<name>/proposal.md`，结构：

   ```markdown
   ## Why

   <!-- 这个变更解决什么问题？为什么是现在做？ -->

   ## What Changes

   <!-- 具体要新增 / 修改 / 删除什么。要具体，不要"优化体验"。 -->

   ## Impact

   <!-- 影响哪些代码 / API / 依赖 / 系统 -->
   ```

4. 上下文里能推断的填进去；推断不出的关键点用 AskUserQuestion 问，再回填
5. 报告：proposal 路径 + 一句话总结 Why/What + 提示"下一步可以跑 `/plan`"

**纪律**：

- proposal 只回答"为什么 / 改什么 / 影响什么"，**不要在这里写实现方案**——那是 design 的事
- 不写 capability / spec 描述，本工作流不维护 specs
- 写不出"Why"就回头问用户，不要硬编一段听起来合理的话
- 一个 proposal 只承载一个逻辑单元；范围里有两件不相关的事，建议拆两个变更

---

## Phase: plan

承接 proposal，把"怎么做"和"分几步做"分别落到 `design.md` 与 `tasks.md`。

**输入**：

- 已存在的变更名 `<name>`，对应 `nanospec/<name>/`
- 该目录下应已有 `proposal.md`；若没有，先回去跑 propose 或当面跟用户确认 Why/What

**步骤**：

1. 读 `nanospec/<name>/proposal.md` 与 `alignment.md`（若有）
2. 写 `design.md`：

   ```markdown
   ## Context

   <!-- 背景与现状：相关代码 / 既有约束 / 之前的相关变更 -->

   ## Goals / Non-Goals

   **Goals:**
   <!-- 这次设计要达成什么 -->

   **Non-Goals:**
   <!-- 明确不在本次范围内的事 -->

   ## Decisions

   <!-- 关键技术决策与取舍理由。一个决策一段，先写结论再写为什么。 -->

   ## Risks / Trade-offs

   <!-- 已知风险、回滚思路、性能 / 兼容性等取舍 -->
   ```

3. 写 `tasks.md`：

   ```markdown
   ## 1. <Task Group>

   - [ ] 1.1 <task 描述，可执行、可验证>
   - [ ] 1.2 ...

   ## 2. <Task Group>

   - [ ] 2.1 ...
   ```

4. 关键点缺信息时，用 AskUserQuestion 问，再回填——不要靠推测把 design 编圆
5. 报告：产物路径 + Decisions/Non-Goals 各 1–2 条提要 + 任务总数 + 提示"下一步可以跑 `/apply`"

**纪律**：

- design 写"怎么做 / 为什么这样做"；不要把 proposal 的 Why 复制过来
- Decisions 要带理由（"为什么这样而不是那样"），单纯写一行结论等于没决策
- tasks 必须是可执行、可验证的颗粒度——读完一条就能知道动哪段代码、改完怎么算完
- 一条任务对应一个变更行为；不要把"实现 + 测试 + 文档"塞进同一条
- 任务序号 `n.m`，按 Task Group 分组，便于 apply 按顺序勾掉
- 如果发现 proposal 的 Why/What 模糊到没法做 design，先回去补 proposal，不要硬编

---

## Phase: apply

按 `tasks.md` 逐条实现，每条做完立刻把 `- [ ]` 改成 `- [x]`。

**输入**：

- 变更名 `<name>`；如未给：
  - 从对话上下文推断
  - `nanospec/` 下只有一个活跃变更时直接选它
  - 多个变更时用 AskUserQuestion 让用户选
- 公布选择："使用变更：`<name>`，要切换其它变更请告诉我"

**步骤**：

1. 读上下文：`nanospec/<name>/proposal.md`、`design.md`、`tasks.md`、`alignment.md`（存在的都读），没读完不要动代码
2. 盘点进度：总数 / 已完成 / 剩余；简要列出剩余任务
3. 逐条实现（循环直到清单走完或被打断）
   - 公布"正在做：n.m <task 描述>"
   - 改最少必要的代码完成这条
   - 立刻把 tasks.md 里对应的 `- [ ]` 改成 `- [x]`
   - 进入下一条
4. 完成 / 暂停时
   - 完成全部：报告 N/N + 列出本次会话动过的任务
   - 暂停：说明原因（任务模糊 / 设计冲突 / 报错 / 用户打断）和当前进度

**纪律**：

- 一次只做一条任务；不要把多条糅成一个大改动
- 每条任务做完**立即**勾选 `- [x]`，不要攒到最后一起改
- 改动保持最小、最聚焦；不要顺手重构无关代码
- **遇到以下情况一律暂停，不要硬猜**：
  - 任务描述含糊到不知道动哪——回去问，必要时切到 align 把歧义记下
  - 实现时发现 design 决策站不住 / 用户中途改需求——切到 align，把偏差落到 alignment.md，并回写 tasks
  - 报错或卡点——报告并等指引
- 不要"看起来像完成了"就报告完成；跑该跑的命令、看到证据，再下结论
- 不归档

---

## Phase: align

横切阶段。出现"实现偏离预期 / 口径需要补充 / 临时变更"时，先把问题落到 `alignment.md`，再把影响传播到 proposal/design/tasks，最后把后续动作变成 tasks 中可勾选的任务。

**何时切到 align**：

- 实现过程中发现 design 决策站不住
- 用户中途追加 / 修改 / 删减需求
- 需求在 proposal 里有歧义、冲突，或漏掉了某个边界
- apply 跑到一半发现某条任务的前提变了

**步骤**：

1. **追加到 `alignment.md`**（不存在则新建）
   - 标签：`[偏差]` `[变更]` `[缺失]` `[歧义]` `[冲突]`
   - `⏳ 待确认` 标记需要用户确认的条目；用户确认后移除该标记并把条目改成 `[x]`
   - 每条记日期 `@YYYY-MM-DD`
2. **传播影响**
   - 口径变了：回去改 `proposal.md` / `design.md` 中受影响的段落，不能让产物互相打架
   - 决策变了：在 `design.md` 的 `Decisions` 里加一条新决策，旧决策保留并标"已被 X 取代"
3. **落到任务**
   - align 产生的"后续动作 / 修正步骤 / 补充工作"必须变成 `tasks.md` 里的新任务（编号续到现有组之后或新建组），不要只停留在 alignment.md 里
4. 报告：哪些条目入 alignment、哪些产物被同步、新增了哪几条任务

**`alignment.md` 默认结构**：

```markdown
# Alignment Log

- [ ] **[标签]** 问题描述。 `@YYYY-MM-DD`
  - 详细说明 / 上下文

- [ ] **[标签]** `⏳ 待确认` 需要用户确认的问题。 `@YYYY-MM-DD`
  - 选项 / 建议

- [x] **[标签]** 已解决的问题描述。 `@YYYY-MM-DD`
  - **Resolved:** 最终结论或决策。 `@YYYY-MM-DD`
```

**标签含义**：

- `[偏差]` 实现与口径不一致
- `[变更]` 用户主动改 / 加 / 减需求
- `[缺失]` 口径里漏了某个场景或边界
- `[歧义]` 表述不清，多种解读
- `[冲突]` proposal / design / tasks 之间互相矛盾

**纪律**：

- 口径变了**必须传播**：不要只更新 alignment 而让 proposal / design 继续过时
- align 产生的活儿**必须落任务**：写在 alignment 注释里 ≠ 完成
- `⏳ 待确认` 是给用户的硬阻塞，没确认前不要替用户做决定
- align 不替代 propose：如果整个变更立项站不住，停下来跟用户讨论是否起一个新的 propose

---

## Phase: run

编排器。一次性把 propose → plan → apply 串起来跑：检测 `nanospec/<name>/` 里已有什么、缺什么，从缺口处接续。

**两种场景**：

### 场景 A：用户附带需求描述

例：`/run 实现用户登录，支持手机号和邮箱两种方式`。

判断：输入里带有较完整的功能描述（>10 个字 / 有动作 + 对象）。

执行：

1. 从描述里提取 kebab-case 任务名（如 `add-user-login`）
2. 用今天日期拼出 `<name> = YYYYMMDD-add-user-login`
3. 建目录 `nanospec/<name>/`
4. 把用户描述原文写到 `nanospec/<name>/brief.md`
5. 从 propose 阶段开始顺序执行，**不再每步征求用户同意**——除非遇到必须确认的歧义

### 场景 B：仅给变更名或不给参数

例：`/run` 或 `/run 20260506-add-user-login`。

执行：

1. 确定 `<name>`：
   - 用户显式给了：直接用
   - 没给：在 `nanospec/` 下找唯一活跃变更；多个变更时用 AskUserQuestion 让用户选
   - 找不到：提示用户改用场景 A，附带需求描述
2. 进入"检测进度 → 接续执行"

**进度检测表**：

| 检查项 | 文件 | 算"已完成"的标准 |
|--------|------|-------------------|
| Brief | `brief.md` | 文件存在且非空 |
| Proposal | `proposal.md` | 文件存在，且 Why / What Changes / Impact 三节都填了 |
| Plan | `design.md` + `tasks.md` | 两份都存在，design 有 Decisions，tasks 至少 1 条 |
| Apply | `tasks.md` | 全部任务勾成 `[x]` |

**起始点判断**：

```
有 brief 但没 proposal     → 从 propose 开始
有 proposal 但没 plan      → 从 plan 开始
有 plan 但 tasks 未跑完    → 从 apply 接续
全部完成                   → 报告"全流程已完成"
brief 也没有 + 场景 A      → 先写 brief，再从 propose 开始
brief 也没有 + 场景 B      → 提示用户先给需求描述
```

**执行**：按起始点顺序调用对应 phase 的能力，每跑完一个阶段做阶段报告：

```markdown
✅ <阶段名> 完成
   产物：<文件路径>
   下一步：<下一阶段> 或 全流程完成
```

**完成汇总**：

```markdown
## 工作流完成

| 阶段 | 状态 | 产物 |
|------|------|------|
| propose | ✅ | nanospec/<name>/proposal.md |
| plan    | ✅ | nanospec/<name>/design.md, tasks.md |
| apply   | ✅ | tasks.md（N/N 完成） |

### 主要交付

- <列出本次会话动过的代码 / 文档 / 配置>

### 建议下一步

- 跑相关验证命令并提交
- 或者发现偏差时跑 `/align`
```

**纪律**：

- 每个阶段必须**完整执行**对应 phase 的所有动作，不能因为是 run 就偷工
- 阶段之间**严格顺序**：propose → plan → apply，不能跳步
- 每个阶段产物**先写盘再进下一步**，确保中途中断也能从上次的产物接续
- 单个阶段失败**就地停下**，报告失败原因和当前进度，不要硬跑下一阶段
- 任何阶段命中需要用户确认的歧义，先暂停问用户
- 不替用户判断"这个变更要不要做"——run 假设用户已经同意要做了；中途自己怀疑该不该做，停下来问
- 不要把 run 当成"跳过 plan 的捷径"：plan 阶段照常拆 design / tasks，否则 apply 没东西可跑
- 不归档；apply 跑完到此为止
- 中断恢复时再跑一次 `/run` 应当从上次断点继续——所以"每个阶段写完产物再进下一步"是硬约束

---

## 跨阶段纪律

- 所有产物必须落盘到 `nanospec/<name>/`，不要只在回复里输出
- 任何阶段缺关键信息**必须问用户**，不要靠"听起来合理"硬编
- 实现层的偏差走 align，不要在代码里偷偷绕开
- 完成声明前先跑该跑的命令、看到输出，再下结论
- 不要自动归档；apply 跑完后由用户决定下一步
