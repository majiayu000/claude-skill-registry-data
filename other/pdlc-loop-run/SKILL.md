---
name: pdlc-loop-run
description: 收敛循环引擎（自动推进 tdd→implement→review 到 review_done 或 blocked）
argument-hint: <功能ID> [--max-steps N]
allowed-tools: Read, Glob, Bash, Task
layer: 3
stage: ops
produces: []
requires:
  - docs/.pdlc-state/
next_step: null
terminal_state: null
---

# 收敛循环引擎（loop-run）

把机械收敛段 `tdd → implement → review` 烧成一个自主循环：从 `current_stage` 出发逐阶段自动推进，直到 `review_done` 或被 `blocked`。这是 `/pdlc-loop-next` 之上的高层引擎——用户不必自己写 bash 循环。

<!-- @include templates/prompts/noninteractive.md（已内联于下方，无需另读） -->
## 非交互模式（`--autonomous`）

若本命令的参数含 `--autonomous`，本命令进入**无人值守**模式，按以下规则处理原本需要人应答的交互点。**参数是唯一真源**：不带 `--autonomous` 即为交互模式，一切照旧正常询问用户；绝不回读状态机 `run_mode` 兜底（「掉出 autonomous」是安全的失败方向）。

1. **流程性确认**（如「测试已绿是否继续」「是否覆盖已有文件」）→ **不询问**，按预设默认前进，并把决策追加到状态机 `history[].auto_decisions[]`：
   ```json
   { "point": "<确认点描述>", "chose": "<所选默认>", "at": "<ISO 8601>" }
   ```
2. **真需人判断**（PRD 关键取舍、评审「需人工确认」项、真实循环依赖等无法安全默认的点）→ **不猜**：
   - `current_stage` 保持不变（不推进）
   - 写 `last_phase_result.ok = false` 且 `blocked_reason = "<原因>"`
   - 末行输出哨兵：`<<<PDLC blocked reason="<原因>">>>`
   - 立即结束命令，交还人类
3. **破坏性操作**（发布 / 部署 / 打 tag / 触发 CI / DROP / force-push 等不可逆·外发操作）→ `--autonomous` **无效**，仍必须人工显式确认。
4. **顺手的 sidecar 产物**（如缺失时创建 `CHANGELOG.md`、补全文档 PDLC-TRACE 的创建时间等本阶段职责内、可安全默认的辅助改动）→ 视为流程性默认，**直接做并记入 `auto_decisions[]`**；这类改动不新增外部副作用，不属破坏性操作。

> 进入 autonomous 模式时，在状态机顶层写 `run_mode: "autonomous"` 仅供留痕（复盘区分人工 vs 循环产出）。
<!-- @include-end templates/prompts/noninteractive.md -->

> ⛔ **终态即 `review_done`（设计如此）**：本引擎**只覆盖机械收敛段**。到达 `review_done` 即**成功停机**，交人工决定是否 `/pdlc-ship`。**绝不**自动进入 `pdlc-ship` / `pdlc-deploy`——发布/部署是不可逆·外发操作，永远留人（`--autonomous` 对它们无效）。prd/design 的关键取舍同样不在本引擎范围内。

## 两种运行形态

- **默认推荐 · 外部 Runbook（真进程隔离）**：长跑 / 过夜 / 多 feature 并行时，用独立进程逐轮跑，每轮全新进程 = 真 fresh context 最可信。本命令可打印该 Runbook 脚本（见 usage-guide「自主循环 Runbook」）。
- **便捷 · 插件内 Task 版（本命令默认行为）**：适合短收敛。每个 stage 派发给一个 **fresh Task subagent**（context 相对隔离），返回后读状态机决定推进 / 停 / block。

## 多个功能 / 并行：用驱动脚本

一次要推多个功能、要并行、或要长跑过夜时，**不要自己写外层循环**——用随本 skill 分发的驱动脚本
`scripts/pdlc-loop.sh`（在本 skill 目录下）。它就是上面说的外部 Runbook 形态，护栏与下面的 Task 版一致：

```bash
# 先看决策，不花钱
bash <本 skill 目录>/scripts/pdlc-loop.sh F20260924-100000 F20260924-110000 --platform claude --dry-run
# 真跑：claude 平台必须给每次调用的预算上限
bash <本 skill 目录>/scripts/pdlc-loop.sh F20260924-100000 F20260924-110000 --platform claude --max-budget-usd 5
# 所有处于收敛段、未阻塞的功能，两个一起跑（每个功能一个 git worktree）
bash <本 skill 目录>/scripts/pdlc-loop.sh --ready --platform claude --max-budget-usd 5 --parallel 2
# 看进度（/pdlc-status 也会显示）
bash <本 skill 目录>/scripts/pdlc-loop.sh --status
```

- `--platform claude|codex`：每一步用 `claude -p` 或 `codex exec` 起一个全新进程
- 并行参数 `--parallel N`（默认 1）：N>1 时每个功能在 `.worktrees/pdlc-loop/<ID>`（分支 `pdlc-loop/<ID>`）里跑，互不干扰；
  产物留在 worktree 里，由人审阅、合并，驱动不提交、不合并。状态文件要先提交，worktree 里才看得到
- 按状态机里的 `depends_on` 排先后：依赖没收敛，依赖方就不跑；成环的全部跳过
- 退出码：`0` 全部收敛；`2` 有功能阻塞或被跳过；`3` 达步数上限；`4` 平台命令出错；`5` 状态没推进
- 跑之前把命令与预计的并行数、预算告诉用户并等确认——自主循环持续花钱

## 循环算法（Task 版）

1. 从本命令的参数取功能ID；`--max-steps` 取迭代上限（缺省 **4**）。读 `docs/.pdlc-state/<功能ID>.json`。
2. 循环，每轮：
   1. 按 `/pdlc-loop-next` 的映射判定下一条命令：`pdlc-tdd` / `pdlc-implement` / `pdlc-review` / `done` / `blocked`。
   2. `done` → **成功停机**，输出 `<<<PDLC done stage=review>>>`，提示交人工 `/pdlc-ship`。
   3. `blocked` → 停机交还人类，输出 `<<<PDLC blocked reason="...">>>`。
   4. 否则用 **Task 工具派发**该命令到一个 fresh subagent，**带 `--autonomous`**，模型取目标 skill frontmatter 的 `recommended_model`（无则继承）。
   5. subagent 返回后重新读状态机 `last_phase_result`：
      - `ok=false` → **fail-stop**：停机、不重跑同一 stage，输出 blocked 哨兵。
      - `current_stage` 未推进（违反 IRON LAW 第 6 条）→ **stuck-stop**：停机报错。
      - `ok=true` 且已推进 → 记一步，继续下一轮。
   6. 步数 > `--max-steps` → **上限停机**（防病态空转烧 token）。
3. 输出循环小结（跑了几步、终态、每步 `last_phase_result` 摘要）。

## 护栏（不可协商）

- **迭代上限**：收敛段线性前进 `tdd→implement→review`（3 段），默认上限 **4** = 3 段 + 1 段容错余量（供「首轮 block、人工修好后从原 stage 续跑一次」）。不给更多余量。
- **只前进不回炉**：循环只在**不同 stage 间前进**，永不原地重跑同一 stage（与 IRON LAW「修复单次不递归」一致——单 stage 内的修复仍是单次）。
- **fail-stop / stuck-stop**：任一 stage `ok=false` 或状态未推进即停，绝不空转。
- **预算**：外部 Runbook 形态必须配 `--max-budget-usd`（见 usage-guide）。自主循环持续烧 token，护栏是硬要求。

## 与 IRON LAW 的关系

本引擎不违反「修复单次不递归」：单个 stage 的自检-修复仍单次；引擎做的是**跨 stage 前进 + 失败即停 + 上限**，不是「重试同一步」。

功能ID: $ARGUMENTS
