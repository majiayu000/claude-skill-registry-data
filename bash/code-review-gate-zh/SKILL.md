---
name: code-review-gate-zh
description: 写完代码、提交前或合并 PR 时使用；用户说“帮我 review”“提交前检查一下”“看看这次改动”“PR review”，或要求严格审查/合入门禁时也使用。
---

# 代码审查

> 检查代码缺陷、测试质量和变更影响，并确认已发现的问题是否闭环。

## 资源与执行位置

- `references/`、`scripts/`、`assets/` 均相对本次读取的 `SKILL.md` 所在目录。
- shell 命令从**被审项目根目录**执行；`docs/work/`、代码路径与项目规则均属于被审项目。
- 下文的 `CODE_REVIEW_SKILL_DIR` 指 skill 安装目录的绝对路径。每次 shell 调用都设置它，
  或直接用实际绝对路径替换；不要假定不同 shell 调用会保留变量。
- 脚本需要 Bash 3.2+、Git、awk、grep、sed 等基础命令。通过 `bash` 调用，无需依赖可执行位。
- 报告解析需要 Python 3.9+ 和 PyYAML；默认调用 `python`，可用 `CODE_REVIEW_PYTHON` 指定解释器绝对路径。
  安装方式见发布仓库 README；仓库内入口为 `scripts/install.py`。

## 适用范围

- 审查影响代码行为的功能、bug 修复、重构或配置变更。
- 不影响代码行为的纯文档、格式或错别字改动可跳过。
- 测试失败或尚未运行时仍可静态审查；报告须注明测试状态，不得宣称已满足合入条件。

## 输入

| 输入 | 必需 | 说明 |
|---|---|---|
| git 仓库 + 可 diff 的改动 | 是 | 明确审查未提交改动，还是已提交的 base/head 区间 |
| 验收标准 | 否 | 提供时按“可选收尾”逐条勾验 |
| 覆盖率数据 / 命令 | 否 | 提供时用于 `test-coverage` 的可选测量；未提供时仍执行相关测试代码的静态质量检查 |
| 规则包 | 否 | 默认 skill 内置 `references/rules/`；可用 `CODE_REVIEW_RULES_DIR` 覆盖 |
| 审查标识 | 否 | `{slug}`，默认 `<日期>-<主题>` |

产物根目录 `{output_root}` 默认 `docs/work`，可由项目 `.code-review/config.json` 的 `output_dir` 或 `CODE_REVIEW_OUTPUT_DIR` 覆盖。本次产物写入 `{output_root}/active/{slug}/`。

## 审查流程

> 检查项不写死在本文件里，由 `references/probes.yaml` 注册表驱动。
> 探针的实现细节在 `references/probes/<探针名>.md`；本文件负责**主流程编排及探针共同执行边界**。
>
> **执行边界：默认进行静态审查。** 覆盖率检查优先复用已有报告；
> 需要测量时，可在本轮任务允许的范围内执行覆盖率命令。其他检查仍只读证据。
> 审查过程中不得修改被审源代码。测试与 CI 输出作为审查证据，
> **测试全绿不等于行为正确**。

1. **确定审查范围**：

   主执行器开始时运行一次环境预检，读取 JSON 中的工具路径、版本及缺失项，按需交接可用命令给探针：
   ```bash
   "${CODE_REVIEW_PYTHON:-python}" -X utf8 "$CODE_REVIEW_SKILL_DIR/scripts/check-environment.py"
   ```
   必需项失败时先处理环境问题；需指定 Bash 时加 `--bash /path/to/bash`。`rg` 缺失时使用返回的备用方式，未跟踪文件须单独读取。结果只返回 stdout，无需落盘；工具可用性以执行命令的环境为准。

   **选择模式**，未指定时默认审查未提交改动。下文的 base/head 均记录为具体 commit ID。

   - **未提交改动（worktree）**：base 为当前 HEAD。
     用 `git diff <base> --` 收集暂存与未暂存改动；
     用 `git ls-files --others --exclude-standard -z` 收集未跟踪文件，
     并将其完整内容作为新增代码审查。
   - **已提交区间（commits）**：按用户指定的 base/head，
     用 `git diff <base> <head> --` 收集差异。
     省略 head 时使用当前 HEAD，只审查该提交区间。

   **读取对应源码**：
   - worktree 模式读取工作区文件。
   - commits 模式用 `git show <head>:<路径>` 读取目标版本，
     需要旧版本时读取 base。文件扫描仅使用与目标版本一致的磁盘文件。

   **记录并交接**：保存模式、base、目标（工作区或 head）、变更文件清单及差异，
   供所有探针使用。程序处理文件清单时使用 NUL 分隔，并逐路径引用传参。

   收集完成后执行以下命令初始化本轮目录和报告，避免将产物纳入被审范围：
   ```bash
   bash "$CODE_REVIEW_SKILL_DIR/scripts/collect-metrics" init {slug} --mode worktree
   # 或：init {slug} --mode commits --base {base} --head {head}
   ```
   返回 JSON 给出实际 `review_dir`、`output_dir`、`line_target`、`branch_target` 和 `snapshot_id`。
   带 `--mode` 时 init 同时写入 `review-snapshot.json`，钉住本轮审查源码（worktree 文件哈希，或固定的 base/head 提交）。
   新审查必须带 `--mode`；不带时保持旧行为。
   同名活动目录、归档或历史事件存在时拒绝初始化；新审查换用唯一 slug，不覆盖旧产物。
   明确继续同一轮时复用原目录，不再次 init；不得同时派发两轮写入同一目录。
   将实际目录及有效阈值交给所有探针，覆盖注册表中的默认覆盖率参数。报告模板由 init 创建。
   修复后或收到 `stale-review` 时，先执行 `snapshot {slug}` 更新快照，再重跑受影响的探针、重新渲染报告并检查门禁。
   源码检查只读；本流程会写报告、探针 JSON、review-snapshot.json、事件日志和归档指标。

2. **读注册表，确定探针清单**：Read `references/probes.yaml`，按 `requires` 判断：
   - 指定了但缺失 / 不可读 → `error`
   - 未提供可选输入 → `skipped`，写明缺什么
   - 可用 → 执行

3. **并行执行探针**：

   **派发**：主执行器按注册表为每个探针派发独立代理，提供审查范围、diff、项目根、skill 路径、该探针的输入和 `params`、`references/probes/common.md` 的路径，以及上文“执行边界”。要求每个代理先读 `common.md`，再读探针专属说明。
   同时交接本轮已提供的需求、验收标准及变更背景（原文或路径），要求探针按相关性读取；未提供则注明，不额外编写。
   已有可用依赖源码或契约材料时，交接其路径、版本及来源供按需复用；不预先下载全部依赖。

   代理读取注册项 `file` 指向的说明和 `references/output-schema.md`，按参数执行。
   并发槽位不足时分批执行；没有独立代理能力时串行执行并记录限制。

   **探针共同约束**：统一定义在 `references/probes/common.md`。每次派发都提供该路径，不在各探针文档中重复或改写这些规则。

   **交接**：每个探针均须有本轮 JSON。跳过或出错时按输出契约记录原因；执行出错保留已发现问题，其余探针继续。启动失败或无有效结果时，由主执行器记录 `error` 及原因，不复用旧结果。

   `test-coverage` 通过返回消息交接有效覆盖率的报告路径、目标版本、分子/分母及百分比，
   由主执行器上报；`--line` 仅接收 diff 行覆盖率：
   ```bash
   bash "$CODE_REVIEW_SKILL_DIR/scripts/collect-metrics" coverage {slug} --line {diff-line-coverage}
   ```
   有分支数值时加 `--branch {branch-coverage}`，或仅上报该项；未测量或不适用的指标省略，不补 0，两项均无有效数值时不调用。单项上报仅更新该项，脚本不验证统计口径。

   **汇总**：全部代理结束后，由主执行器执行同步命令；脚本从注册表读取 `required`，从探针 JSON 计算各级数量，不改写原始结果，不手填计数。
   暂不做跨探针去重，按原始 finding ID 计数，可能包含同根因问题的重复记录：
   ```bash
   bash "$CODE_REVIEW_SKILL_DIR/scripts/collect-metrics" sync {slug} --probes
   ```
   此步使上一批对账状态失效，尚不记录 reconciliation。

4. **reconciliation 完整性检查**：
   从探针 JSON 自动派生最终计数：
   ```bash
   bash "$CODE_REVIEW_SKILL_DIR/scripts/collect-metrics" sync {slug}
   ```
   `required` 只控制该探针的 `failed/error` 执行状态是否直接阻塞，不改变 finding 的闭环要求。
   任意探针的 high finding 都进入 reconciliation，未闭环仍阻塞合入；medium/low 记入报告，不计入对账总数：
   ```text
   RECONCILE_TOTAL   = high finding 总数
   RECONCILE_DONE    = 其中 status 为 reconciled 或 false-positive 的条数
   RECONCILE_PENDING = TOTAL - DONE
   ```
   没有 high 也须执行，显式记录零结果，不能用旧计数或手填数字代替。
   格式错误须先修正；记录缺失、重复 ID 或状态矛盾时同步失败，不写计数，不以旧结果放行。
   有未处置问题（`RECONCILE_PENDING > 0`）时，本轮仍交付报告并列明阻塞项，不得推进合入。
   后续修复任务完成后，再复审受影响的部分；重派上限见 `references/probes.yaml` 的 `execution.max_retry`。

5. **汇总报告**：

   按模板填写审查范围、解释、修复建议和限制，原始 JSON 不嵌入正文；提供了验收标准时，先完成逐条勾验。

   `unverified_items` 由脚本以“待确认”展示在问题区，不计入各级 finding 数量；原始记录保留 ID、证据及计数；展示独立问题数量时按同一根因和后果归组并列明对应 ID，不因重复提高严重级别，也不以展示数量替代探针或对账计数。

   执行以下命令，从 JSON 生成报告事实区、校验展示并取得最终答复摘要；任一步失败立即停止：
   ```bash
   bash "$CODE_REVIEW_SKILL_DIR/scripts/collect-metrics" finalize {slug}
   ```

   脚本只更新报告“发现的问题”和“审查结论”中的 `code-review:probes` / `gate` 标记区域，保留其他正文和原始 JSON。渲染先校验再原子更新，可重复执行；标记缺失或重复时停止。校验覆盖 ID、位置、证据、严重级别、状态和计数。

   `summary` 先校验报告，一致后才输出机器摘要。最终答复中的 high/medium/low 数量、finding ID 和阻塞结论须以摘要为准，不新增未记录的问题，不遗漏已记录的 high。向用户交付报告、阻塞项及未验证内容，可补充解释和建议，不得改写自动区域或推翻已知阻塞事实。

   “无已记录阻塞项”不代表验收、覆盖率、测试或 CI 已通过。`gate-pass {slug} code-review` 与有审查记录的 `archive` 均先校验报告，再同步计数，不自动修正被改写的展示。

   `verify-report` 只校验报告区域与探针 JSON 一致，不校验源码新鲜度。
   `gate-pass {slug} code-review` 会先重算 `review-snapshot.json`；被审源码变化时返回 `stale-review`（exit 3），不写门禁事件。

## <HARD-GATE>

**以下任一条件命中，阻塞合入**。本轮报告列明阻塞项，下表为后续处置要求：

| 阻塞条件 | 后续动作 |
|---|---|
| required 探针为 `failed` / `error`（`PROBE_REQUIRED_FAILED > 0`） | 处理已发现的问题或执行错误后，重跑对应探针 |
| 被审源码与 `review-snapshot.json` 不一致（`stale-review`） | 按步骤 1 更新快照并复审 |
| high finding 未完成 reconciliation（`RECONCILE_PENDING > 0`） | 按步骤 4 处理，修复后重派受影响的探针 |
| reconcile 从未上报（`RECONCILE_REPORTED=0`） | 完成步骤 4；没有 high 也须执行最终同步 |
| 提供了覆盖率数据且低于基线（增量行覆盖率低于项目 line_target，默认 85%） | 列明覆盖缺口，补测试后重新审查 |
| 提供了验收标准且未全过，或标准本身有歧义 | 列明未通过项；有歧义先澄清，不得自行勾验通过 |
| 有 high finding 停在 `wontfix` | 按输出契约完成处置，不能用“不修”冲抵待办 |

执行状态与输入错误的判定见 `references/output-schema.md` 第 4 节。

脚本验证报告记录与计数的一致性，不能证明检查是否充分。

## 输出契约

- **主报告**：`{output_root}/active/{slug}/code-review.md`，按
  `assets/code-review.md` 的章节和填写要求生成。
- **机器记录**：`{output_root}/active/{slug}/probes/<探针名>.json`，
  格式见 `references/output-schema.md`；人类报告的事实区域由它们派生。
- **审查快照**：`{output_root}/active/{slug}/review-snapshot.json`，由 `init --mode` 写入；
  `gate-pass code-review` 用它拒绝过期证据。

历史记录须明确迁移为独立 JSON；不从自由文本猜测或自动补零，也不同时读取旧内嵌区块。

## 可选收尾

以下事项按条件执行，不作为每轮必经步骤：

- **验收**：提供了验收标准时，在最终结论前逐条勾验；没有则跳过并说明。
- **lessons**：有 `lessons/` 目录，且本次有实际发生、值得复用的经验时记录，说明具体问题、原因和处理方式：
  - 实现过程中踩的坑 → `lessons/pitfalls.md`
  - AI 产出被纠正的案例 → `lessons/bad-cases.md`
  - 新的架构决策 → `lessons/arch-decisions.md`
- **归档**：如需归档，将 `{output_root}/active/{slug}/` 移到 `{output_root}/archive/{YYYY}/`。
