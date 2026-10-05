---
name: capability-delivery-gate
description: >-
  Codex 在执行任何项目级 / board / sprint 任务,或任何声称"推进某个系统能力"的多轮
  工作时,强制启用的"目标函数保证器"。它与 project-lifecycle 并行:project-lifecycle
  保证流程走完,本 skill 保证能力真的交付。专治这一类失败 -- 做了一堆安全、合规、
  准备性工作(adapter / gate mapping / queue contract / schema / 设计文档),每一步都
  PASS,十几轮下来却没有产生任何真实业务结果(没有候选、没有跑通的链路、没有分布、
  没有 flywheel 写入)。任何即将给出 board 级裁决 / closeout / PASS 之前,必须先过本门。
  不要用于单轮问答、查文档、改一行字、闲聊。
---

# capability-delivery-gate -- 能力交付门(目标函数保证器)

## 0. 这个 skill 解决什么(以及为什么其他 skill 挡不住)

其他 skill 是**过程治理工具**:防乱提交、防脏工作树、防泄露 key、防下载全表、
防越界、防伪称 OOS。它们证明的是"没犯错"。

它们**不证明"有能力"**。本 skill 是唯一一根反方向的护栏:它不问你有没有越界,
它只问一件事 -- **终端能力到底交付了没有**。

它专治的失效模式只有一个,但精确:
> 十几轮全 PASS,产出一堆名词性的安全准备层,真实业务结果是 0。

为什么旧规则没拦住:旧规则(throughput test、贪婪陷阱审查)是**判断题**,模型
当场可以回答"看着没问题"。本 skill 的所有门都是**机械检查**:计数、文件存在性、
数值比较、词表。模型能合理化判断,不能合理化 `0 > 0`。

## 1. 触发条件(强制)

满足任一即**强制启用**,与 project-lifecycle 并行(不是二选一,两个都要过):
- 任何 LARGE / 项目级 / board / sprint 任务。
- 任何声称"推进 / 接入 / 打通某个系统能力"的工作。
- 任何即将给出 board 级裁决 / closeout / PASS 的时刻 -- 裁决前必须先过本门。

明确不触发:单轮事实问答、查一条文档、改一行字、闲聊。

> project-lifecycle 管"流程走完了没",本 skill 管"能力交付了没"。正交,叠加。

## 2. 核心规则(不可违背)

### D1 -- 终端产物先行,禁止代理替换
第一轮动手前,必须声明唯一的【终端产物】:**它存在 = 任务完成**的那个东西。
它必须是一条**可运行链路的输出**(候选、trial ledger、KILL/HOLD/PROMOTE 分布、
flywheel 写入)。它**不能**是名词性中间物 -- adapter / gate mapping / queue
contract / schema / 设计文档一律不是终端产物。中间步骤显式标记为【非交付物】。
此后,除了"距终端产物还差多远",不许汇报任何"进度"。

### D2 -- 验收断言必须硬、能力性、可机器判定
终端产物配一组【硬验收断言】。每一条必须同时满足三点:
- **可机器判定**:一个数、一个文件存在性、一个分布非空。"已设计""已对齐""已映射"
  一律不合格。
- **是能力断言,不是边界断言**。`generated_candidates > 0` 合格;`没有 OOS`
  `没有泄露` `raw data 没进 repo` **不合格** -- 那是边界检查。边界检查继续保留,
  但它**永远不能当作 done 的定义**。
- 至少一条必须是"链路**端到端真的跑通了**"。

### D3 -- 最高信息量的一步,必须在第 1-2 轮做
任何"准备"只要能被"直接跑一次看看"替代,就**必须**用跑一次替代 -- 哪怕粗糙、
哪怕只跑子集、哪怕绕过非安全的中间层。
判据:这一步产生的是【关于终端产物能不能成立的信息】,还是【零信息的安全产物】?
后者一律延后或删除。若 round >= 3 仍未做最高信息量动作 -> 触发 D5 硬停。

### D4 -- 禁用裸 PASS,裁决词表固定为五选一
board 级 / 阶段级裁决**只能**用下面五个词之一,**禁止出现裸 "PASS"**:
- `CAPABILITY_DELIVERED` -- 终端产物存在,**全部**硬断言通过,端到端跑通。
- `IMPLEMENTATION_PASS_CAPABILITY_NOT_DELIVERED` -- 代码/测试/边界都没问题,
  但终端产物不存在或硬断言未过。**这不是成功**,是"接住了合规、没接住能力"。
- `BLOCKED` -- 无法推进,必须给出唯一阻塞点。
- `STOP_IDLE` -- 空转门触发(见 D5)。
- `STOP_FORMALISM` -- 删除测试未过(见 D6)。

只有 `CAPABILITY_DELIVERED` 算 board 成功。其余四个都意味着系统能力**没有**推进。
注意:早期轮次(终端产物还没做出来)如实判 `IMPLEMENTATION_PASS_CAPABILITY_NOT_DELIVERED`
是**正常且正确**的 -- 该裁决描述的是能力状态,不是对本轮努力的打分。

### D5 -- 空转门(轮次预算,硬停)
全程维护一个【能力台账】,每轮追加一条 §3 的裁决块。
若连续 **K 轮(默认 K=2,上限 3)** 终端产物的硬断言**没有任何一条**从 FAIL 变
PASS,**硬停**。不许开始第 K+1 轮。必须输出:
> "已 N 轮,终端产物未移动,根因 X,唯一阻塞点 Y" -- 然后停,交用户。
`STOP_IDLE` 之后,必须由用户**显式批准**才能续轮,模型不得自行续轮。

### D6 -- 删除测试(贪婪陷阱的硬 veto,不是审计文字)
每个 board / sprint 启动前,问一句机械的问题:
> "如果这个 board 整个删掉,系统会不会少掉一个真实的、可运行的能力?"

答案是"不会" -> 判 `STOP_FORMALISM`,**不准做**。
这条把"一个 board 不产生新的可执行能力就不要做"从审计文字变成**硬 veto**。

### D7 -- 能力裁决是天花板,压过一切边界 PASS
任何审计角色(**包括项目级 AGENTS.md 里定义的 5 个审计角色**)在记录任何
PASS 之前,必须先回答机械问题:"终端产物存在并跑通了吗?Yes/No"。
若 No -> board 级裁决被**封顶**在 `IMPLEMENTATION_PASS_CAPABILITY_NOT_DELIVERED`,
**无论多少个审计角色说边界 OK**。边界合规永远不能把能力裁决顶上去。

## 3. 能力台账(每轮必须产出的可验证收据)

每一轮 / 每个 board 收尾,**必须**逐字段输出下面这个块。不许省略字段,不许散文化:

```text
CAPABILITY VERDICT
terminal_artifact   : <一行,可运行链路的输出>
round               : <整数>
rounds_since_moved  : <整数 -- 终端产物硬断言上次出现 FAIL->PASS 至今几轮>
hard_assertions:
  <断言1>           : PASS | FAIL(<实测值>)
  <断言2>           : PASS | FAIL(<实测值>)
  ...
moved_this_round    : YES | NO
deletion_test       : PASS(删了会丢能力)| FAIL(删了不丢 -> STOP_FORMALISM)
highest_info_action_done : YES | NO
VERDICT             : <D4 五选一,禁止裸 PASS>
single_blocker      : <若 VERDICT 非 CAPABILITY_DELIVERED,必填,唯一阻塞点>
next_action         : <若继续:下一轮唯一目标,必须直指终端产物>
```

这个块就是用户的验证入口。用户打开任何 closeout,**看不到这个块**、或
`hard_assertions` 里填的是"已设计"而不是真实数字 -- 即说明本 skill 被跳过或工作失败。

## 4. 执行路径(在 Codex 中如何运作)

1. 项目级任务进来 -> project-lifecycle 启动 PHASE 0 -> 本 skill 同时启动。
2. PHASE 0 / AUDIT 内,除《目标契约》外,本 skill 强制追加:【终端产物声明】(D1)
   +【硬验收断言】(D2)+【删除测试】(D6)。删除测试 FAIL -> `STOP_FORMALISM`,
   项目不启动。
3. 第 1 轮 BUILD 的唯一目标必须是 D3 的"最高信息量动作"。若一个粗糙的端到端跑
   是可行的,**不许**第 1 轮去做 adapter / mapping / contract / 设计层。
4. 每一轮收尾 -> 产出 §3 能力台账块 -> 更新 `rounds_since_moved`。
5. `rounds_since_moved` 达到 K,或 round >= 3 而 `highest_info_action_done` 仍为 NO
   -> D5 硬停,输出 `STOP_IDLE` 诊断,不进下一轮。
6. 任何审计 / closeout / 阶段裁决前 -> 先跑 D7 能力问题 -> 给不出
   `CAPABILITY_DELIVERED` 就封顶;裸 `PASS` 一律改写成 D4 词表里的词。
7. 终端产物全部硬断言 PASS 且端到端跑通 -> `CAPABILITY_DELIVERED` -> 本 skill 放行。

## 5. 与现有体系的关系(不冲突、不重复)

- **project-lifecycle / R4 / G3.0**:防【偏航】和【过度】-- 做太多、做偏、过度优化。
  本 skill 防【空转】和【代理替换】-- 做太少、永远在准备、用名词冒充能力。
  正交的另一根护栏,不是重复。
- **alpha-validation-gate**:负向边界门(不许越界)。本 skill 是它的**正向对偶**
  (必须交付)。两者合起来,路的两侧都有栏杆。
- **项目级 5 个审计角色**:本 skill 不重定义它们,只给它们一条**封顶规则**(D7)。

## 6. 风险边界(本 skill 的已知失效模式)

- 本 skill 靠"模型自填能力台账"运作。若模型不产出 §3 的块、或在 `hard_assertions`
  里填假数字,本 skill 即失效 -- 这是 Codex 无真权限隔离的固有上限。对抗手段是
  §3 的收据**可被用户秒验**:skill 能做的是让"被跳过"变得**可见**,不能让它不可能。
  用户必须真的去看那个块。
- K(轮次预算)默认 2,由用户在使用中校准。少数任务确实需要一轮纯准备 -- 允许,
  但触发 `STOP_IDLE` 后必须由用户显式批准才续轮。
- 本 skill **不判断终端产物定义得对不对** -- 那是《目标契约》和用户的事。若终端
  产物定义错了,本 skill 会把错的目标也忠实地逼出来。定义对错由 PHASE 0 把关。

## 7. 反例(以下每一条都是本 skill 要拦的真实失败)

- "我把数据路径接入了 gate 可读状态" -- 边界检查,不是终端产物。**D1 拦**。
- "我做了配层证明 CRSP 不能绕过 gate" -- 零能力信息的安全产物。**D3 拦**:
  绕过非安全中间层直接跑一次,才知道因子死活。
- "我重新设计了候选队列" -- 早就设计过,纯运动,终端产物没动。**D5 计入未移动轮次**。
- 十几轮 closeout 全是 PASS、`generated_candidates` 始终是 0 -- **D4 禁裸 PASS**,
  **D7 封顶**为 `IMPLEMENTATION_PASS_CAPABILITY_NOT_DELIVERED`,**D5 在第 2-3 轮就硬停**。

## 附:CRSP 接入的样板填法(展示"硬断言"长什么样)

```text
terminal_artifact : CRSP_BATCH0_FACTORY_FUNNEL_RUN -- 现有 Alpha Factory 以 CRSP
                    为数据源跑出的一批候选
hard_assertions:
  generated_candidates > 0                         : ...
  crsp_candidate_trial_ledger 文件存在              : ...
  每个候选都有 gate verdict                         : ...
  summary 含 KILL/HOLD/PROMOTE 计数                 : ...
  flywheel 写入了 next_batch_constraints            : ...
  funnel 端到端跑通(输入 CRSP -> 候选 -> ledger -> verdict): ...
```

对照:"没有 OOS""没有 stock rankings""没有 weights" -- 这些是**边界断言**,
继续保留在 alpha-validation-gate 里,但**不得**出现在本 skill 的 hard_assertions。
