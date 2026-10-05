---
name: unified-taskflow
description: |
  面向真正复杂任务的重型管理系统，使用 anchor、checkpoint、design、恢复和验收追踪。
  仅在用户明确要求使用 unified-taskflow、taskflow、.taskflow，或任务确实需要跨多轮、多文件、多阶段的可恢复记录时使用。
  不用于小修、普通优化、普通重构、单个 Skill 小改、日常 bug fix，或 task-mode-router / minimal-implementation 已足够处理的任务。
---

# Unified Taskflow v4.4

> 更新：2026-08-10

> [!CAUTION]
> **核心规则**
> 1. 只有通过触发门禁后，才启动 unified-taskflow；不要把普通任务流程化
> 2. 启动后，任务管理使用项目根目录下的 `.taskflow/` 目录，**不使用**内置 artifact 目录
> 3. 禁止跨阶段推理 — 执行时不能跳回规划，规划时不能偷跑代码
> 4. 如不确定是否需要启动，先用 `task-mode-router` 判断；仍不确定时询问用户，不默认触发

> **规则优先级**（冲突时按此顺序裁决）：
> **Safety > Correctness > Efficiency > Completeness**
>
> **执行语义优先级**（与执行类 Skill 冲突时按此裁决，详见 execution-discipline「自主执行契约」）：
> **Safety/不可逆授权 > 用户显式目标与约束 > 合法停止策略 > 自主续接 > 流程便利**。
> 本 skill 的任何流程规则不得覆盖 `clarify-before-change` 的更窄询问边界，也不得覆盖 `execution-discipline` 的停止/恢复语义。

## 触发判断

**触发**：
- 用户明确说“使用 unified-taskflow / taskflow / .taskflow”。
- 任务跨多轮、多文件、多阶段，且需要可恢复的执行记录。
- 任务需要明确的 anchor、checkpoint、design、验收标准和回滚路径。
- 用户要求长期复盘、审计轨迹、阶段冻结或复杂交接。

**不触发**：
- 简单问答、单行修改、单文件小修。
- 普通 skill description 小改、文案调整、同步用户级 skill。
- 普通“优化 / 完善 / 重构 / 更稳定”，除非用户明确要求重型流程。
- `clarify-before-change`、`task-mode-router`、`minimal-implementation` 已足够控制风险的任务。

**路由关系**：
- 先由 `task-mode-router` 判断任务模式。
- 小任务和中等任务默认不用 `.taskflow/`。
- 只有大型、长任务、可审计交接任务才进入本 skill。
- 进入本 skill 后，仍遵守 `minimal-implementation`，不为了流程完整性扩大实现范围。

## 按需加载

- 进入 Phase 0 → 读取 [phase0-clarification.md](references/phase0-clarification.md)
- 需要交互决策 → 读取 [interaction-design.md](references/interaction-design.md)
- 治理规则细节 → 读取 [governance.md](references/governance.md)
- Re-grounding 细节 → 读取 [regrounding-protocol.md](references/regrounding-protocol.md)

## 工作流

### Phase 0: 理解快照（Understanding Snapshot）

**目的**：确保 Agent 正确理解用户需求，生成防幻觉锚点。

1. **确认已通过触发门禁**；未通过时退回普通任务流程
2. **禁止**立即创建文档或代码
3. Agent 输出**理解快照**：
   - 用户意图（一句话）
   - 识别到的歧义点
   - Agent 的假设（显式列出并**标注可逆性**：可逆假设记录即推进；仅目标级/不可逆假设需用户确认）
4. 默认直接进入完备性门禁并写入 anchor.md；**仅当存在目标级/不可逆假设或意图级歧义时**才请求用户确认（询问边界以 `clarify-before-change` 意图解析策略为准，一次问完）
5. **完备性门禁**（详见 phase0-clarification.md）
6. 写入 `anchor.md`（北极星文件，含版本号）

> 问题框架（参考，不强制全部使用）：边界 / 约束 / 优先级 / 风险
> 详见 [phase0-clarification.md](references/phase0-clarification.md)

### 执行（Elastic Execution）

弹性深度 — 根据任务复杂度自然展开，无固定档位：

- **重型任务最小路径**：anchor.md → checkpoint.md → 执行 → 验收核对
- **需要设计时**：anchor.md → design.md → checkpoint.md → 执行 → 验收核对
- **不做**：为低风险小任务创建 `.taskflow/`、anchor、checkpoint 或 design

执行期间遵守：
- **统一 Checkpoint 协议**：事件驱动的 checkpoint 更新 + 内置 re-grounding 核对（见下方）
- **3-Strike Protocol**：同一问题 3 次失败后触发 DEADBAND 策略重置（见下方，**不自动升级用户**）
- **续接语义**：用户说"继续 / 做完 / 接着做 / 自主推进"时，读 anchor.md + checkpoint.md 恢复 current state 与未闭合 Done-when，直接推进；**禁止**重新走 Phase 0 或重新确认已登记信息（详见 clarify-before-change「续接语义」）

### 完成（Completion）

1. 最终 Re-grounding — 逐项核对 anchor.md 的所有 Done-when 条目
2. 向用户报告完成状态
3. 归档任务（移入 archive/）

> 兼容说明：历史 `index.json` 可能使用 `archived` 状态；读取、list 和 catch-up 必须保留兼容显示，新写入使用 `completed` 或 `abandoned`。

## 运行机制

### 统一 Checkpoint 协议（事件批次 + Re-grounding）

将进度记录和对齐验证合并为单一机制，减少协议数量，提高遵从率。

**触发事件**（事件驱动，替代模糊的步骤计数）：

| 事件 | 说明 |
|------|------|
| 关键文件创建/修改 | 完成一个影响验收、设计、数据或行为的文件操作批次后触发 |
| 子任务完成 | 每完成一个逻辑子任务 |
| 用户新指令 | 用户补充信息或修改要求 |
| 不确定性 | 遇到模糊决策或多种可行方案 |
| 意图漂移 | 用户当前指令与 anchor.md Intent 语义不一致时 |

**每次 Checkpoint 更新包含**：
1. 做了什么 + 发现了什么
2. **Re-grounding 逐项核对**（对 anchor.md 的 Critical Constraints 和 Done-when 逐条检查状态）
3. 刷新 checkpoint.md 顶部的 **Anchor Mirror**（复制 Intent + Critical Constraints）
4. 下一步计划

**滚动压缩**：checkpoint.md 保留最近 3 条完整记录，旧记录压缩为一行摘要移入「历史摘要」区。

> 详见 [regrounding-protocol.md](references/regrounding-protocol.md)

### 脚本边界

- `scripts/task-lifecycle.py` 使用 `assets/templates/` 作为 anchor、checkpoint、design 的唯一模板源；不要在脚本中复制第二份模板。
- 新任务名必须是安全的单一路径组件（字母/数字/`-`/`_`，最多 64 个字符）；不接受绝对路径、`..` 或路径分隔符。
- 可用 `--project-path <path>` 指定项目根目录；`list` 和 `status` 可附加 `--json` 生成机器可读状态。默认仍为当前工作目录。
- `task-lifecycle.py --help` 和 `session-catchup.py --help` 必须显示帮助并以 0 退出；帮助参数不能被当作项目路径或任务名。
- `index.json` 写入经过 schema/lifecycle 校验并采用原子替换；历史 `archived` 状态继续只读兼容。

### 3-Strike Protocol → DEADBAND（策略重置，不是停止）

同一问题连续失败 3 次：
1. Strike 1 — 记录问题和尝试方案
2. Strike 2 — 换一个方向，记录
3. Strike 3 — **DEADBAND_TRIPPED**：作废当前路径假设 → re-grounding → 选择**实质性不同**的恢复路线（Recovery Ladder，见 execution-discipline），继续推进

**3-Strike 不得自动等于升级用户。** 只有 Recovery Ladder 全程走完且满足 execution-discipline「合法停止策略」五类之一时，才可停止并向用户报告（附已排除方案清单）。

### RIPER-Core 思维规则

1. 根因解优先 — 禁止用配置/降级掩盖问题
2. 显式因果链 — Why → Condition → Limitation
3. 无魔法数字 — 常数必须来自输入/约束
4. 明确变量 — 信息不足先按 clarify-before-change「自主解析顺序」自行获取；仅目标级/不可逆信息缺失才询问

## 反模式清单（Anti-Patterns）

> 禁止性指令的遵从率通常高于义务性指令。以下是**不要做**的事：

| 反模式 | 说明 | 正确做法 |
|--------|------|----------|
| 自由文本对齐 | 用"我觉得还在正轨"代替逐项核对 | 必须对 Critical Constraints 和 Done-when 逐条输出状态 |
| Anchor 静默修改 | 未告知用户就修改 anchor.md | 任何 anchor 修改必须用户确认，并更新 Version 和 Change Log |
| Checkpoint 堆积 | 无限追加 checkpoint 不压缩 | 超过 3 条完整记录时，压缩旧记录为摘要 |
| 跳过 Phase 0 | 直接开始执行不做理解快照 | 复杂任务必须先输出理解快照（默认据此推进；仅目标级/不可逆假设需确认）后写入 anchor.md |
| 硬约束降级 | 把 Critical Constraint 当 Soft Preference 处理 | Critical Constraint 违反 = 立即暂停请示 |
| 假设隐含 | 不列出假设就开始执行 | 所有假设写入 anchor.md 的 Assumptions 表并标注可逆性；可逆假设记录即推进，仅目标级/不可逆假设需用户确认 |
| 忽略意图漂移 | 用户隐式改变方向时不确认就跟着走 | 检测到用户指令与 anchor.md Intent 不一致时，主动确认是否修改 Intent |
| 续接重启 | 用户说"继续"后重新走 Phase 0 / 重新确认计划 | 续接 = 恢复 current state + 未闭合 Done-when + next best action，直接推进 |
| 3-Strike 即停 | 连续失败 3 次就停下问用户 | Strike 3 = DEADBAND 策略重置换路线；仅合法停止策略满足时才可停止 |

## 工作目录

```text
.taskflow/
├── index.json
├── active/[task-name]/
│   ├── anchor.md          # 北极星文件（必须，含版本号）
│   ├── checkpoint.md      # 校验点记录（必须，含 Anchor Mirror）
│   └── design.md          # 技术设计（按需）
└── archive/               # 已归档任务
```

## 交互原则

- 选择题优先，3-4 个选项
- 每个选择点有推荐选项
- 可选参考：[interaction-design.md](references/interaction-design.md)

## 输出契约

每个阶段都应明确当前状态、已完成项、未完成项、阻塞项、下一步和验收证据。完成前逐项核对 anchor.md 的 Critical Constraints 与 Done-when；任何未验证项都不能标记为完成。

脚本的机器可读输出使用 `--json`，人类可读输出保留原始错误和实际路径。不会用旧 checkpoint、模糊的“仍在正轨”或静默降级替代逐项核对。

## 验证

最小验证集：

```bash
python3 scripts/task-lifecycle.py new demo-task
python3 scripts/task-lifecycle.py validate
python3 scripts/task-lifecycle.py complete --message "验证完成"
python3 scripts/session-catchup.py --help
```

应在隔离项目中运行，不能把测试任务写入当前仓库的正式 `.taskflow/`。

## 引用文件

| 文件 | 用途 |
|------|------|
| [phase0-clarification.md](references/phase0-clarification.md) | Phase 0 理解快照 + 完备性门禁 |
| [regrounding-protocol.md](references/regrounding-protocol.md) | Re-grounding 逐项核对规则 |
| [governance.md](references/governance.md) | 目录隔离、生命周期、治理规范 |
| [interaction-design.md](references/interaction-design.md) | 交互设计原则（可选参考） |
| [anchor.md 模板](assets/templates/anchor.md) | Grounding Anchor 模板（分层 + 版本号） |
| [checkpoint.md 模板](assets/templates/checkpoint.md) | 校验点记录模板（Anchor Mirror + 滚动压缩） |
| [design.md 模板](assets/templates/design.md) | 技术设计模板（按需） |
