---
name: pdlc-status
description: 查看项目 PDLC 状态总览（读 docs/.pdlc-state/ 输出进度）
argument-hint: [feature-id | --all]
allowed-tools: Read, Glob, Bash
layer: 1
stage: ops
produces: []
requires: []
next_step: null
terminal_state: null
---

# 项目 PDLC 状态总览

读取 `docs/.pdlc-state/` 目录下所有状态机文件，输出项目当前的 PDLC 进度、阶段分布、待办建议。

<!-- @include templates/prompts/state-read.md（已内联于下方，无需另读） -->
## 读状态机之前：先做契约体检

`docs/.pdlc-state/*.json` 不一定都是 `/pdlc-*` 命令写出来的——手写的、旧版本写的、照着格式仿写的
都可能混在里面。字段对不上契约时，**不许边猜边算、再把猜出来的东西当结论**。先体检，再计算；
体检发现的每一处偏差，都必须出现在输出的**最前面**。

### 1. 跑体检

体检脚本随本 skill 一起分发，就在本 skill 目录下：`scripts/pdlc-state-lint.sh`（运行时会告知本 skill 的
所在目录）。它与正在运行的 skill 同一版本，体检规则——合法阶段名、偏差代码——与下方 §2 一致。

在项目根执行 `bash <本 skill 目录>/scripts/pdlc-state-lint.sh .`。stdout 每行一条偏差：`文件<TAB>代码<TAB>说明`。退出码三态：

- `0` 已体检、全部合契约 → 照常出结论，不输出体检块
- `1` 已体检、有偏差 → 照常计算，但输出最前面必须先放「输入契约体检」块（见 §3）
- `2` 无法体检（缺 jq / 无状态目录）→ 体检块写「无法体检：<原因>」，**不得当成合契约**

体检脚本不可用时（找不到，或当前平台没有随 skill 分发它），按 §2 的规则逐条人工核对，
体检块首行注明「体检脚本不可用，以下为人工核对」。

### 2. 体检规则（偏差代码）

读侧跳过 `_` 前缀的索引文件（如 `_relations.json`）与 `statusline.json`，它们不是功能状态机。

<!-- finding-codes:start -->
| 代码 | 判定 | 读侧怎么处理 |
|---|---|---|
| `json-invalid` | 文件不是合法 JSON | 跳过该文件，列入体检块 |
| `missing-field` | 缺 `feature_id` / `current_stage` / `history` / `next_step` / `created_at` 之一 | 用到该字段的指标，对这份文件记「不可判」 |
| `field-type-invalid` | 字段在、类型不对（如 `current_stage` 不是字符串、`history` 不是数组、`last_phase_result` 不是对象、history 条目不是对象） | **按缺失处理**：用到它的指标对这份文件记「不可判」。类型不对的时间戳不再另报 `timestamp-no-time` |
| `missing-last_phase_result` | 缺 `last_phase_result`（多为旧文件） | 不推断本阶段结果与 checks |
| `terminal_state-in-instance` | 实例里出现 `terminal_state` | **忽略该字段**，判终态只看 §4 |
| `non-contract-field` | 其它表外顶层字段（如 `title`） | 忽略 |
| `stage-alias` | `stage` 用了已知别名 | 可按说明里的 `别名→短名` 归一化计数，**但必须在体检块写明归一化了哪些** |
| `stage-unknown` | `stage` 既不是短名也不是已知别名 | 单独成行，不并入任何阶段 |
| `current_stage-unknown` | `current_stage` 既不是短名，也不以 `_done` 结尾 | 该功能归入「❓ 异常」 |
| `next_step-not-command` | `next_step` 不是纯命令名（如带散文后缀） | 按原文展示，不据此推断下一步 |
| `timestamp-no-time` | 时间戳只有日期、没有时刻 | 依赖它的**耗时类指标记「不可测」**，不得算成 0 |
| `relations-not-object` | `relations` 不是六键对象（如数组） | 这份文件的关系**不入图**，列入体检块 |
| `relations-unknown-type` | 关系键不在六类之内 | 该键下的关系不入图 |
| `relations-target-not-id` | 关系目标不是 feature ID（散文、模块路径等） | 该条不入图 |
| `relations-dangling` | 目标 ID 没有对应的状态文件 | 标「悬空」，不参与影响半径计算 |
| `id-prefix-mismatch` | 走的是修复流程（有 `fix` 阶段），ID 却不以 `B` 开头 | 缺陷计数按 ID 前缀的契约口径算，同时在体检块点名这份 |
| `second-state-dir` | 仓库根另有一个 `.pdlc-state/` | 本命令只读 `docs/.pdlc-state/`，提示两处并存 |
<!-- finding-codes:end -->

**「不入图」不是丢弃**：关系目标是散文时，把它硬解读成某个 feature，等于把猜测升格成结构——
影响半径会因此多出一条本不存在的强依赖。宁可在体检块里原样列出，交给人判断。

#### 阶段短名全集

`history[].stage` 与 `last_phase_result.stage` 只能取下表的短名——每个短名由对应命令写入，
等于该命令 frontmatter 的 `stage:`。别名只为**读**旧数据时容忍，归一化必须披露；**写**的时候一律用短名。

<!-- stage-names:start -->
| 短名 | 由哪个命令写入 | 已知别名（读侧可归一化，须披露） |
|---|---|---|
| `requirements` | `pdlc-prd` | `prd` |
| `design` | `pdlc-design` | |
| `tdd` | `pdlc-tdd` | |
| `impl` | `pdlc-implement` | `implement, implementation` |
| `review` | `pdlc-review` | |
| `e2e` | `pdlc-e2e` | |
| `ship` | `pdlc-ship` | |
| `deploy` | `pdlc-deploy` | |
| `fix` | `pdlc-fix` | `bugfix` |
| `refactor` | `pdlc-refactor` | |
| `task` | `pdlc-task` | |
| `feature` | `pdlc-feature` | |
<!-- stage-names:end -->

### 3. 体检块的格式（放在输出最前面）

```
⚠️ 输入契约体检：<N> 份状态文件，<M> 处偏差——以下结论建立在这些处理之上
  · 3/5 份缺 created_at → 时间窗改用 history 末条 done_at
  · 阶段别名 prd→requirements ×1、implementation→impl ×2 → 已归一化计数
  · 5/5 份含 terminal_state → 已忽略（判终态只看 current_stage）
  · 2 份的 done_at 只有日期 → 阶段耗时记「不可测」
```

- **按「偏差类 × 份数 × 处理方式」汇总**，不要把脚本输出原样倒出来
- **放最前面，不放末尾**——结论会被单独引用，偏差得跟着结论走；写在报告末尾的偏差表，
  读者看到的时候已经信了前面的数字
- **计数照抄脚本输出，不要自己重数**：按代码计数用 `cut -f2 | sort | uniq -c`，份数按第一列去重。
  真机验证时脚本报 25 处无时刻的时间戳，报告正文却自己数成了 26——同一份报告里两个数字对不上，
  读者就不知道该信哪个
- 同一次输出里，前面披露了「已忽略 X」，后面的计算就不得再用 X

### 4. 判终态的唯一依据 ⛔

**已抵达终态 ⇔ `current_stage` 以 `_done` 结尾**（终态即「已发布」：`/pdlc-ship` 写 `ship_done`、`/pdlc-deploy` 写 `deploy_done`；旧版本留下的 `feature_done` / `fix_done` / `review_done` 也按终态读）。

- **不看 `terminal_state`**。状态机实例本就没有这个字段。skill frontmatter 里的 `terminal_state:`
  说的是「这个命令走完后**应当**到达的终态名」——是**目标**，不是**事实**。拿它判终态，
  等于把「打算完成」当成「已经完成」。
- **不用封闭列表**（如只认 `[feature_done, fix_done]`）。封闭列表会把合法的终态漏判成「进行中」，
  逼着读侧去别的字段里找答案——而最顺手的那个字段恰好就是 `terminal_state`。
- **`next_step` 为 `null` 也不等于终态**：`/pdlc-task` 写的 `next_step` 恒为 `null`，却未必完成；空的或残缺的状态文件也读得出 `null`。
<!-- @include-end templates/prompts/state-read.md -->

## 执行流程

### 1. 扫描状态机

1. 列出 `docs/.pdlc-state/*.json` 所有文件（跳过 `_` 前缀的索引文件与 `statusline.json`）
2. 若无文件 → 输出：`📭 尚无 PDLC 追踪记录。运行 /pdlc-feature 或 /pdlc-fix 开始第一个功能。`
3. **跑契约体检**（见上方「读状态机之前：先做契约体检」）。有偏差或无法体检时，体检块放在总览**最前面**
4. 进入下一步

### 2. 解析与分类

按 `current_stage` 字段分组：

- ✅ 已完成：`current_stage` 以 `_done` 结尾——**判终态的唯一依据**，不看 `terminal_state`、不用封闭列表（见上方「判终态的唯一依据」）
- 🚧 进行中：`current_stage` 有值且不以 `_done` 结尾
- ❓ 异常：JSON 无法解析、缺 `current_stage`，或体检对 `current_stage` 报 `current_stage-unknown` / `field-type-invalid`

### 3. 输出概览

```
⚠️ 输入契约体检：<N> 份状态文件，<M> 处偏差——以下结论建立在这些处理之上
  · …（仅在体检有偏差或无法体检时出现，且必须放在最前面）

📊 PDLC 状态总览（共 <N> 个功能）

🚧 进行中（<M> 个）
  - F20260419-090000 user-auth      当前：design       下一步：/pdlc-tdd
  - F20260419-100000 pwd-reset      当前：impl         下一步：/pdlc-review

✅ 已完成（<K> 个）
  - F20260415-110000 feature-xyz    完成于 2026-04-16
  - B20260418-090000 login-crash    完成于 2026-04-18（ship_done）

⚠️ 待办建议
  - F20260419-090000 停留在 design 超过 2 天，建议推进 /pdlc-tdd
```

### 3.5 关系树视图（RFC#6）

若存在 `docs/.pdlc-state/_relations.json`，附加关系视图（读其 index 的 inbound/outbound）：

```
🔗 关系链
  F20260419-090000 user-auth
    ├─ extends → F20260415-110000 feature-xyz
    └─ ← depended_on_by F20260419-100000 pwd-reset

  🧩 孤立 feature（无任何关系）：F20260420-130000
```

- 出边用 `→`，入边用 `← <反向类型>`
- 末尾列 orphans（inbound + outbound 均空的 feature）
- `_relations.json` 不存在时跳过本节（Phase 1 向后兼容）；Phase 2 起关系视图进入默认总览

### 3.6 循环运行（仅当用多功能循环驱动跑过）

驱动脚本随本 skill 分发：`scripts/pdlc-loop.sh`。在项目根执行 `bash <本 skill 目录>/scripts/pdlc-loop.sh --status --project .`。
它读最近一次循环运行的记录，打印运行概况、各功能进度与提示：

- **没有输出** → 项目没用驱动跑过循环，跳过本节
- **有输出** → 以「🔁 循环运行」为小节标题，把输出**原样**放进总览（放在关系视图之后）。
  计数、耗时、提示都由脚本算好，**不要重算、不要改写**，也**不要自己推算预计完成时间**——
  各步耗时差异很大，给出的时间只会误导
- 输出里有功能的产物在 worktree（「产物在 .worktrees/pdlc-loop/…」）时，主工作区里这些功能的状态文件
  不是最新的——在「进行中 / 已完成」分组里给这些功能注明「最新进度见循环运行」，不要按主工作区的旧状态下结论
- 脚本不可用（找不到、缺 jq）→ 跳过本节，并在末尾注明「循环运行记录无法读取：<原因>」

### 4. 参数处理

- 参数为空或为 `--all` → 输出所有功能
- 参数为功能ID → 只输出该功能的详情（含 history 全量 + 该 feature 的关系）
- `--relations` → 只输出关系树视图
- `--loop` → 只输出循环运行一节（见 3.6）

## 参数

- `--all`（默认）：全部功能总览
- `<feature-id>`：单个功能的完整 history
- `--relations`：只输出关系树视图（出边 + 入边 + orphans）
- `--loop`：只输出最近一次循环运行的进度
- `--stale <days>`：列出停留在同一阶段超过 `<days>` 天的功能（默认 3 天）

---

**参数**：$ARGUMENTS
