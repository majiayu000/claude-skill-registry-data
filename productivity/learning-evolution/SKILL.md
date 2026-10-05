---
name: learning-evolution
description: 当用户要求复盘、沉淀经验、记录长期规则、整理 support 卡，或继续把这些候选 codify 成正式资产时使用。
---

# Learning Evolution

把“这次值得留下什么”变成明确出口，而不是模糊笔记。这个 skill 先做第一阶段 `Observation -> Selection -> Representation`，只有用户明确要求 `evolution`、演化、继续 codify 正式资产时，才进入第二阶段。默认写回 `.learned/rules.md`、`.learned/support.md`、当前上下文已有记录位置，或目标正式资产。

## 何时使用

- 用户要求“复盘一下”“沉淀经验”“整理规则”“记录 support”“做一次 stocktake”
- 本轮出现了明确的用户纠正、重复 workflow、失败与修复链路、研究结论或验证教训
- 需要判断这条经验应该留在任务内、进入长期候选，还是直接写回正式资产
- 用户明确要求把已有候选继续演化为 skill、command、eval、README 或其他正式资产

不适用：

- 只是一次性 typo、机械改名或偶发问题
- 没有证据，只有模糊印象
- 目标资产已经非常明确，且用户只要求直接修改那个资产；此时应优先用对应 skill 或直接执行改动

## 核心判断

每次使用本 skill，都要把每条信号收口到以下四个出口之一：

1. `drop`
   - 噪音、一次性问题或证据不足，直接丢弃
2. `keep-task-local`
   - 只影响当前工作后续动作，写回当前上下文已有记录位置，不进入 `.learned/`
3. `queue-support`
   - 跨任务仍有价值，但暂时还不该直接改正式资产，写入 `.learned/support.md`
4. `codify-now`
   - 证据与目标都已足够明确，直接更新正式资产

如果最后没有落到这四个出口之一，说明这次 learning 还没整理完。

## 默认输入

优先读取以下材料，再开始判断：

1. 当前上下文已有材料
   - 若当前环境已有 brief、研究记录、工作清单或其他上下文文件，先读这些已有材料
2. 本轮真实证据
   - 用户纠正、diff、命令输出、验证结果、review 结论、研究记录、失败与修复过程
3. 现有长期沉淀
   - 需要时再读 `.learned/rules.md`、`.learned/support.md`，避免重复写同类条目

## 输出位置

### 1. `keep-task-local`

- 只服务当前工作的 learnings，优先写回当前上下文已有记录位置
- 至少写清：learning 是什么、影响当前工作哪一步、下一步如何消费

### 2. `.learned/rules.md`

- 只记录项目级 / 团队级 / 分发级长期规则
- 典型来源：用户明确纠正、稳定接受 / 拒绝标准、长期口径修正
- 每条至少写：规则、证据、建议落点、下一步

### 3. `.learned/support.md`

- 只记录跨任务长期候选的“资产支撑卡”
- 它不是普通 notes；每条都必须回答“它在支持什么资产”
- 每条至少写：类型、触发、证据、原料、建议动作

### 4. `codify-now`

当证据足够、目标资产明确、且本轮允许演化时，直接更新正式资产：

- 规则 -> `AGENTS.md`、README、skill、eval 或其他长期文档
- 可复用 workflow -> skill 或 command
- 验证标准 -> eval
- 说明性沉淀 -> README 或包内文档

## 两阶段动作

### 第一阶段：Observation -> Selection -> Representation

这是默认动作，不需要用户额外说明：

1. `Observation`
   - 列出本轮值得看的信号：用户纠正、重复 workflow、失败修复、研究判断、验证结果
   - 没有证据的印象，不进入长期沉淀
2. `Selection`
   - 判断每条信号的作用域：`task-local` | `project` | `cross-task`
   - 判断每条信号的出口：`drop` | `keep-task-local` | `queue-support`
3. `Representation`
   - 把选择结果写回当前上下文已有记录位置、`.learned/rules.md`、`.learned/support.md`
   - 不要只停留在对话里

### 第二阶段：Evolution

`Evolution` 不是默认动作。只有在以下条件同时满足时才执行：

1. 用户明确要求 `evolution`、演化、继续 codify、收敛正式资产，或当前任务目标本身就是正式沉淀
2. 目标资产可以明确指向
3. 证据足以支撑修改

进入第二阶段后，再继续判断是否 `codify-now`。没有明确演化信号时，即使已经写了 `rules` 或 `support`，也不要自动升级为正式资产。

## 执行步骤

1. 确认边界
   - 判断本轮只是做第一阶段，还是已经允许进入 `Evolution`
   - 若当前环境已有既定工作面或更新约束，先读取现有口径
2. 收集信号
   - 只保留有证据的信号
   - 相同模式优先合并，不重复记碎片
3. 逐条选择出口
   - 当前工作内可消费 -> `keep-task-local`
   - 长期规则 -> `rules.md`
   - 资产原料但暂不正式化 -> `support.md`
   - 已允许演化且目标明确 -> `codify-now`
4. 落盘
   - 先把结果写进对应文件
   - 不新建随意命名的临时 learnings 文件
5. 如允许 Evolution，再正式沉淀
   - 更新目标 skill / command / eval / README / `AGENTS.md`
   - 必要时同步相应说明或分发副本
6. 如当前工作口径变化，继续同步受影响记录
   - 若这次沉淀改变了当前工作范围、方案或后续动作，更新现有工作文件
   - 若当前环境已有任务清单或协作工作面，也同步回写

## 自动化接入

这个 skill 允许未来接入自动观察层，但自动化只负责发现信号，不负责替你做最终判断：

- `manual-first`
  - 用户或 agent 显式触发
- `reminder-first`
  - 在阶段结束、`Stop`、stocktake 时提醒是否需要学习沉淀
- `observation-first`
  - 用 hooks / observer 自动采集 prompt、tool use、diff、session event，再交给本 skill 判断出口

无论采用哪条路径，都不能绕过作用域判断、证据判断和出口判断；没有明确 `Evolution` 指令时，也不能自动进入正式资产演化。

## 纪律约束

- 不要把 `support.md` 当杂记桶；回答不了“支持什么资产”的内容，不应进入 `support.md`
- 不要把 task-local learnings 与长期候选混在一起
- 不要把用户对 agent 的当场纠正原样写回 prompt 正文，应提炼为稳定规则或支持卡
- 若已有相同候选，优先更新原条目，不要制造碎片
- 若证据与目标已经足够明确，不要只留候选，应继续 `codify-now`
- 不要默认把所有高价值经验都沉淀成 skill；`rules`、`doc`、`eval` 同样是正式出口

## 模板

需要模板时，读取 [references/templates.md](references/templates.md)。
