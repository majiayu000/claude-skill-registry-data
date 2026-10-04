---
name: pdlc-task
description: 阶段内任务跟踪（创建/更新任务列表，附在工作流上）
argument-hint: <功能ID | 任务描述>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 2
stage: task
produces:
  - docs/06_tasks/<feature-id>-tasks.md
requires: []
next_step: null
terminal_state: null
---

# 任务管理

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

管理功能开发任务的拆解、分配与进度追踪。支持从 PRD 自动拆解任务、标记任务状态。

## 子命令解析

从本命令的参数中解析子命令和选项：

| 子命令 | 格式 | 说明 |
|--------|------|------|
| `plan <功能名或功能ID>` | 从 PRD 自动拆解任务列表 |
| `list [功能名或功能ID]` | 查看任务状态（不传则查看全部未完成任务） |
| `start <任务ID>` | 标记任务为进行中 |
| `done <任务ID>` | 标记任务为已完成 |
| `blocked <任务ID> <原因>` | 标记任务为阻塞，记录阻塞原因 |
| `reopen <任务ID>` | 重新打开任务（撤销 done/blocked） |

如果未提供子命令或子命令无法识别，输出以上帮助信息后停止。

---

## 任务 ID 与文件约定

### 任务 ID 格式

`T<功能ID的日期-时分秒>-<NN>-<类型>`

- `<功能ID的日期-时分秒>`：所属功能ID去掉 `F` 前缀的部分（功能 `F20260718-094301` → 前缀 `20260718-094301`）。嵌入 feature 的唯一时分秒，使任务号**全局唯一**且**自带归属**（一眼看出属哪个 feature）
- `NN`：**本功能内**两位递增序号（每 feature 从 `01` 起）
- 类型：
  - `feat` — 功能代码实现
  - `test` — 测试编写
  - `doc` — 文档输出
  - `infra` — 基础设施/脚手架
  - `design` — 设计产出

示例：功能 `F20260718-094301` 的任务 → `T20260718-094301-01-feat`、`T20260718-094301-02-test`

> **为什么 T 用「功能ID时分秒前缀 + 本地序号」而非每个任务自取时分秒**：任务在拆解时**成批同秒创建**，若各自取独立时分秒会互相撞号。改用「所属功能的时分秒前缀 + 本功能内序号」后：既**全局唯一**（继承功能ID的唯一性）、又**自带归属**（看得出属哪个 feature）、还**并行安全**（不同 feature 前缀不同，同批任务靠序号区分）。任务号收敛在唯一命名的 feature 任务文件内，不跨 feature 冲突。

### 任务清单文件路径

`docs/06_tasks/<功能ID>-<功能名>-tasks.md`

示例：`docs/06_tasks/F20260406-093000-user-auth-tasks.md`

若功能ID未知（如独立任务），使用：`docs/06_tasks/YYYYMMDD-<关键词>-tasks.md`

### 任务清单文档格式

```markdown
<!-- PDLC-TASKS -->
<!-- 功能ID: F20260406-093000 -->
<!-- 功能名称: user-auth -->
<!-- 关联PRD: docs/01_requirements/prd/F20260406-093000-user-auth-prd.md -->
<!-- 最后更新: 2026-04-06 -->

# 任务清单：user-auth（F20260406-093000）

## 总览
- 总任务数：N
- 待开始：N | 进行中：N | 已完成：N | 阻塞：N

## 任务列表

> 下例为功能 `F20260406-093000`（user-auth）的任务清单——任务ID 前缀 `20260406-093000` 即该功能ID的时分秒段，`NN` 在本功能内递增。

| 任务ID | 类型 | 描述 | 状态 | 估时 | 截止日期 | 关联文档 | 备注 |
|--------|------|------|------|------|---------|---------|------|
| T20260406-093000-01-design | design | 创建 API 设计文档 | ⬜ 待开始 | 2h | 2026-04-07 | - | - |
| T20260406-093000-02-design | design | 创建数据库设计文档 | ⬜ 待开始 | 1h | 2026-04-07 | - | - |
| T20260406-093000-03-infra | infra | 生成代码脚手架 | ⬜ 待开始 | 0.5h | 2026-04-07 | - | - |
| T20260406-093000-04-test | test | 编写单元测试 | ⬜ 待开始 | 3h | 2026-04-08 | - | - |
| T20260406-093000-05-feat | feat | 实现注册接口 | ⬜ 待开始 | 4h | 2026-04-09 | - | - |
| T20260406-093000-06-feat | feat | 实现登录接口 | ⬜ 待开始 | 2h | 2026-04-09 | - | - |
| T20260406-093000-07-test | test | 运行测试确认绿灯 | ⬜ 待开始 | 1h | 2026-04-10 | - | - |
| T20260406-093000-08-doc | doc | 创建评审记录 | ⬜ 待开始 | 1h | 2026-04-10 | - | - |

## 阻塞记录

| 任务ID | 阻塞原因 | 记录时间 | 解除时间 |
|--------|---------|---------|---------|
| （暂无） | - | - | - |
```

状态图标约定：
- `⬜ 待开始`
- `🔄 进行中`
- `✅ 已完成`
- `🚫 阻塞`

---

## 子命令执行流程

### plan <功能名或功能ID>

**前置检查**：
1. 从用户输入中提取功能名称关键词或功能ID
2. 在 `docs/01_requirements/prd/` 目录下搜索对应 PRD 文档
3. **未找到 PRD** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的 PRD 文档。
   任务拆解必须基于已有的 PRD。请先运行：
   👉 /pdlc-prd <需求描述>
   ```
4. **找到** → 提取功能ID，读取 PRD 内容，继续执行

**执行流程**：
1. 读取 PRD 文档，分析功能范围、用户故事和验收标准
2. 同时检查 `docs/02_design/` 下是否存在相关设计文档，有则一并读取
3. 扫描**本功能的任务文件**（`docs/06_tasks/<功能ID>-*-tasks.md`），取其中已有任务的最大序号 +1（**不跨 feature 扫描**）——每 feature 独立编号，并行开发不同 feature 时任务号互不干扰、合并零冲突
4. 按 PDLC 阶段顺序拆解任务：
   - **设计任务**（design）：需要产出的每份设计文档各一个任务
   - **基础设施任务**（infra）：目录初始化、脚手架生成
   - **测试任务**（test）：测试计划编写、测试代码编写
   - **功能实现任务**（feat）：每个独立接口/页面/模块各一个任务，粒度不超过半天工作量
   - **文档任务**（doc）：评审记录、CHANGELOG 更新
5. 为每个任务估算工时（0.5h 为最小单位）
6. 根据估时和 PDLC 阶段依赖关系，自动推算每个任务的**截止日期**：
   - 从今日日期开始，按阶段顺序排列（设计 → 基础设施 → 测试 → 功能实现 → 文档）
   - 同阶段内的任务可并行，截止日期相同
   - 下一阶段的开始日期 = 上一阶段截止日期的下一个工作日
   - 每日按 8h 工作量计算，超出的顺延到下一工作日
7. 在 `docs/06_tasks/` 下创建任务清单文档
8. 输出任务总览表格（含预计完成时间线）

### list [功能名或功能ID]

1. **有参数**：在 `docs/06_tasks/` 下查找对应功能的任务文件，输出该功能任务详情
2. **无参数**：扫描 `docs/06_tasks/` 下所有任务文件，汇总**非已完成**任务，按状态分组输出：
   - ⏰ 已逾期（截止日期早于今日且未完成的任务，**最先展示**）
   - 🔄 进行中
   - 🚫 阻塞（含阻塞原因）
   - ⬜ 待开始（按功能ID分组，仅展示最近 3 个功能）
3. 输出末尾追加整体完成率统计：`完成率: X/N (XX%)`
4. 若存在逾期任务，额外输出警告：`⚠️ 有 N 个任务已逾期，请及时处理`

### start <任务ID>

1. 在 `docs/06_tasks/` 下扫描所有任务文件，找到包含该任务ID的文件
2. **未找到** → 提示任务ID不存在后停止
3. **找到** → 将该任务状态从 `⬜ 待开始` / `🚫 阻塞` 更新为 `🔄 进行中`
4. 更新文件顶部的总览计数
5. 更新文件顶部的 `最后更新` 时间
6. 输出确认消息：`✓ 任务 <任务ID> 已标记为进行中`

### done <任务ID>

1. 在 `docs/06_tasks/` 下扫描所有任务文件，找到包含该任务ID的文件
2. **未找到** → 提示任务ID不存在后停止
3. **找到** → 将该任务状态更新为 `✅ 已完成`，在备注列填入完成时间
4. 更新文件顶部的总览计数和 `最后更新` 时间
5. 输出确认消息：`✓ 任务 <任务ID> 已完成`
6. 若该功能所有任务均已完成，额外输出：`🎉 功能 <功能ID> 全部任务已完成！`

### blocked <任务ID> <原因>

1. 在 `docs/06_tasks/` 下找到包含该任务ID的文件
2. **未找到** → 提示任务ID不存在后停止
3. **找到** → 将该任务状态更新为 `🚫 阻塞`，在备注列填入原因摘要
4. 在文档末尾的"阻塞记录"表格追加一行（任务ID、原因、当前时间）
5. 更新文件顶部的总览计数和 `最后更新` 时间
6. 输出确认消息：`⚠️ 任务 <任务ID> 已标记为阻塞：<原因>`

### reopen <任务ID>

1. 找到包含该任务ID的文件
2. **未找到** → 提示任务ID不存在后停止
3. **找到** → 将该任务状态更新为 `⬜ 待开始`，清空备注列
4. 若阻塞记录表格中有该任务，填入当前时间作为解除时间
5. 更新总览计数和 `最后更新` 时间
6. 输出确认消息：`✓ 任务 <任务ID> 已重新打开`

---

## 与 pdlc-status 联动

运行 `pdlc-status` 时，若 `docs/06_tasks/` 目录存在，自动在输出末尾追加：

```
## 任务进度
| 功能 | 总计 | 完成 | 进行中 | 阻塞 | 完成率 |
|------|------|------|--------|------|--------|
| F20260406-093000 user-auth | 8 | 5 | 1 | 0 | 62% |
```

$ARGUMENTS

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `task`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `null`（流程到此结束：`next_step` 写 `null`）。
<!-- pdlc:meta-end -->
<!-- @include templates/prompts/state-update.md（已内联于下方，无需另读） -->
## 状态机更新（段四必须执行）

本命令完成主产出后，必须更新状态机文件 `docs/.pdlc-state/<feature-id>.json`。

### 文件格式

```json
{
  "feature_id": "<F/B ID>",
  "feature_name": "<kebab-case>",
  "created_at": "<首次创建时间 ISO 8601>",
  "current_stage": "<当前阶段名>",
  "run_mode": "interactive | autonomous",
  "history": [
    {
      "stage": "<阶段名>",
      "done_at": "<ISO 8601>",
      "produced": ["<相对路径 1>", "<相对路径 2>"],
      "self_audit": { "passed": <N>, "failed": <N>, "manual": <N> },
      "auto_decisions": [
        { "point": "<autonomous 下自动前进的确认点>", "chose": "<所选默认>", "at": "<ISO 8601>" }
      ]
    }
  ],
  "last_phase_result": {
    "stage": "<本次阶段名>",
    "ok": true,
    "advanced_to": "<推进到的下一阶段 | null>",
    "checks": {},
    "self_audit": { "failed": 0 },
    "blocked_reason": null,
    "run_mode": "interactive | autonomous",
    "at": "<ISO 8601>"
  },
  "relations": {
    "extends": [],
    "depends_on": [],
    "supersedes": [],
    "resolves": [],
    "conflicts_with": [],
    "relates_to": [],
    "_updated_at": "<ISO 8601 | 省略>"
  },
  "next_step": "<下一跳命令名，如 pdlc-design；若流程结束则为 null>"
}
```

> ⛔ 示例里的 `"checks": {}` 是「本阶段没有命令可跑」的样子，**不是键名示范**——键名与取值见下方 §1。

> **`relations` 块（RFC#6，Phase 1 可选，Phase 2 推荐）**：6 个 key 对应 6 种关系类型，各为 ID 数组，存**出边**。其中 `conflicts_with` / `relates_to` 是对称类型，两端都要写；其余四种有向，只写在源 feature 上。拿不准时用 `/pdlc-relate set` 写入，它会按规则校验。旧状态文件无此块时视为全空，向后兼容。入边由 `/pdlc-relate rebuild` 派生到 `_relations.json`，不在此块手维护。

> ⛔ **写状态机的四条硬约束**——读侧（`/pdlc-status`、`/pdlc-retro`、`/pdlc-relate`）会逐条体检，
> 违反的每一处都会出现在它们输出的最前面：
>
> 1. **实例里不写 `terminal_state`**。skill frontmatter 的 `terminal_state:` 是「这个命令走完后应到达的终态名」，
>    不是状态字段。判终态只看 `current_stage` 是否以 `_done` 结尾。
> 2. **`history[].stage` 写本命令的阶段短名**（见本命令正文里「本命令的状态机取值」）——`pdlc-implement` 写 `impl`，
>    不写 `implement` / `implementation`；`pdlc-prd` 写 `requirements`，不写 `prd`。
> 3. **时间戳必须带时刻**：`created_at` / `done_at` / `at` 一律写完整 ISO 8601（如 `2026-07-28T10:40:00+08:00`）。
>    只写日期，同一天内的阶段耗时就全部算成 0——读侧只能记「不可测」。
> 4. **`next_step` 只写命令名或 `null`**，不附说明文字（如「pdlc-ship（等评审通过）」）。
>    要说明原因，阻塞时写进 `last_phase_result.blocked_reason`。

> ⛔ **`_done` 的含义是「已发布」，只由 `/pdlc-ship`（写 `ship_done`）与 `/pdlc-deploy`（写 `deploy_done`）写入。**
> 其它命令的 `current_stage` 一律写本命令的阶段短名，走完整条链路的编排命令（`/pdlc-feature`）也一样——
> 它收尾时 `current_stage` 是最后一个阶段的短名，`next_step` 是 `pdlc-ship`。
>
> - 「评审通过、等待发布」就是 `current_stage` 为 `review`（或 `e2e` 等）且 `next_step` 为 `pdlc-ship`。
>   循环相关文档里说的 `review_done` 指的就是这个状态，**不是**要写进 `current_stage` 的值。
> - 为什么：读侧判「已抵达终态」只看 `current_stage` 是否以 `_done` 结尾。评审通过就写 `_done`，
>   `/pdlc-ship` 就分不清哪些功能已经发布过，发布说明会重复或漏收。
> - 旧版本写入的 `feature_done` / `fix_done` / `review_done` 分不清是否已发布，`/pdlc-ship` 会列出来请人确认。

### 更新流程

1. **文件不存在** → 创建文件，写入初始结构（`history` 为含当前阶段的数组）
2. **文件存在** → 读取 JSON，追加当前阶段到 `history`，更新 `current_stage` 和 `next_step`
3. **写回文件**：用 `jq` 或等效工具保持格式化

⚠️ 若更新失败（文件损坏/权限问题），必须中止命令并在最终报告中报错。状态机不可跳过。

### `last_phase_result`（机器可读阶段结果，每个 phase 收尾必写）

顶层 `last_phase_result` 是循环判停的**唯一真源**，外层只需 `jq '.last_phase_result.ok'` 即可决定 继续 / 停止 / 交还人类。规则：

1. **`checks` 必须客观、真跑得来**：只放**真跑命令的退出码**结果（命令取自 `docs/00_standards/test-commands.yml`，见 `test-commands-template.yml`），**绝不用模型自评、绝不填占位**。有测试的阶段用 `tests_pass` / `coverage_pass` / `lint_clean`（退出码 0 → `true`，非 0 → `false`）；stage 语义不同用对应键（如 tdd 段 `{ "red_verified": true }` 表示红灯已验证）。
   > ⛔ **键名与类型都是契约的一部分**：键名只能是 `tests_pass` / `coverage_pass` /
   > `lint_clean` / `e2e_pass`（tdd 段 `red_verified`），值只能是**布尔**。
   > 最常见的两种错法：① 照抄 `test-commands.yml` 的 `unit` / `coverage` / `lint` / `e2e`
   > ——那是**命令表**的字段名，不是状态机的（跑 `unit` 得到的结论写进 `tests_pass`）；
   > ② 写成 `"4 passed, 1 failed"` 这类字符串摘要。两种都会让 `jq '.checks.tests_pass'`
   > 读回 `null`，消费方（发布闸门、质量报告、自主循环）只看到「无法判定」——
   > **你诚实跑出来的结果等于没写**。三态怎么分见本命令正文里「跑 check 命令：退出码的三态语义」一节；正文里没有这一节的命令不跑 check 命令，`checks` 写 `{}`。
   >
   > ⚠️ **没有检查命令可跑的阶段（如 requirements/design 只产文档，或项目无 `test-commands.yml`）→ `checks: {}` 留空。绝不因为「本阶段成功」就把 `tests_pass`/`lint_clean` 等填 `true`——那是虚报，会污染跨工具共用的状态机、误导自主循环判停。** 上面 schema 示例里 `checks` 之所以是空的，正是这个原因——**空是"没跑"的意思，不是键名的示范**。
2. **`self_audit` 单列**：只放自检未通过数，**仅供参考，不作循环判停依据**。
3. **`ok` 的定义**：本阶段全部 `checks` 通过且未命中 `blocked_reason` → `true`；否则 `false`。
4. **命名空间**：`advanced_to` = **下一阶段的短名**，**不是命令名、也不是本阶段的 `current_stage`**。三者关系：`stage`=本阶段短名、`current_stage`=本阶段完成后的当前短名、`advanced_to`=下一阶段短名、`next_step`=下一跳命令名。

   ⛔ **短名不是「命令名去掉 `pdlc-` 前缀」**——`pdlc-implement` 的短名是 **`impl`**，不是 `implement`。别推导，查下表：

<!-- stage-map:start -->
   | `next_step`（下一跳命令名） | `advanced_to`（下一阶段短名） |
   |---|---|
   | `pdlc-tdd` | `tdd` |
   | `pdlc-implement` | `impl` |
   | `pdlc-review` | `review` |
   | `pdlc-design` | `design` |
   | `pdlc-ship` | `ship` |
   | `pdlc-deploy` | `deploy` |
<!-- stage-map:end -->

   `next_step` 为 `null`（终态或无后续）时 `advanced_to` 也是 `null`。

   > 📌 **本表是唯一真源，且是被断言钉住的**：每行的短名必须等于该 skill 自己 frontmatter
   > 里声明的 `stage:`，且任何 skill 的非 `null` `next_step` 都必须在表里有行——两个方向
   > 都由 `tests/frontmatter-check.sh` 检查，所以表不会和实现各自漂移。
   >
   > 写错短名的后果与键名写错同类：消费方按契约名匹配，认不出就当没这个阶段。
5. **推进一致**：`ok=true` 时本阶段必须真的推进了 `current_stage`（与第 6 条 IRON LAW 呼应）；到达终态或无后续时 `advanced_to=null`。`ok=false`（含 blocked）时 `current_stage` 不变、`advanced_to=null`、`blocked_reason` 写明原因。
6. **`run_mode`**：镜像本次调用是否带 `--autonomous`（带了写 `autonomous`，没带写 `interactive`）。
<!-- @include-end templates/prompts/state-update.md -->
<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->
