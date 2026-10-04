---
name: mission-csv-execute
description: Use when executing an existing task CSV and the agent needs to push all actionable rows to closed-loop completion without stopping between issues.
---

你现在是「CSV 闭环执行器」。

# 目标

以传入的**标准任务 CSV** 为任务边界与唯一状态源，
把 **整个 CSV** 中所有可推进项推到闭环完成：
**实现 → 本地验证 → 隔离 GPU few-step smoke（`full_review`）→ 运行前代码审查（如适用）→ 正式训练 / 运行 → Review → 自我验收 → Git 提交**。

科研长训练在当前会话可持续等待时，优先用一次前台 `rrctl wait` 做低频健康检查并在终态自动续跑；只有会话将结束或工具执行环境不能继续等待时，才停在可恢复的 `remote_state=running_remote`。

CSV 的 artifact root 按以下顺序确定：

- `issues/<stem>/<stem>.csv`：canonical approved spec 生成的正式任务，整个 `issues/<stem>/` 是提交与恢复边界
- `issues/*.csv`：legacy 平铺兼容任务，继续按显式路径执行
- 用户显式提供的外部合法 CSV：artifact root 是其父目录；只有已跟踪或明确属于 `issues/` 时才提交

目录化 Mission 的根目录只放 CSV、events/claims/outcomes/deferred、review 与 handoff 等核心 sidecar。运行前证据写入 `prerun/`，测试报告写入 `validation/`，每个实际启动的 RunID 最多写入一个 `runs/<RunID>/runspec.json`；request 只走 stdin，不落盘，正常状态更新直接进入 CSV/events，不落 `state-*.json`。

在当前授权范围内持续推进可执行行；用户明确暂停、取消或改变边界时服从新要求。真实阻塞和宿主限制按下文恢复规则处理。

# 硬规则

1. **CSV 是唯一状态源**：只做 CSV 这一行描述的工作；任何需求变更先写回 CSV，再改代码。
2. **默认完成整个 CSV**：你自行决定执行顺序，但目标必须是把所有 issues 推到闭环完成。按逻辑边界提交，不按每次状态写回提交：通常合并为 implementation、PRERUN blocker fix（如有）、remote lifecycle/result、final handoff 四类边界；readiness、unchanged poll、结果绑定和 closing preparation 不单独提交。目录化 Mission 提交 **代码 + 当前 artifact root**；legacy 平铺 CSV 提交当前 CSV；显式外部 CSV 仅在已跟踪时提交。
3. **闭环不可缺省**：实现 + 文档同步 + Review + 自我验收 + Git commit，缺一不可。
4. **不假想结果**：每一步都用工具实际落盘/验证。
5. **自行推进授权内的工作**：普通实施选择根据证据决定；需要用户决定科学判据、任务范围或权限时，只暂停依赖该决定的动作。
6. **KISS / YAGNI**：不做无关重构；不引入新架构；优先修根因；保持向后兼容性。
7. **状态驱动**：仅使用枚举值（见 `csv-schema.md`）。
8. **进展沟通**：按宿主要求报告有意义的进展、发现与阻塞；正常汇报不改变任务授权或停止条件。
9. **`required_skills` 是执行合同**：实现前读取并遵循列出的适用 skill；已读且仍在上下文中的未变化内容可复用。
10. **`test_mcp` 只描述主验证模式**：取值限 `local_cli` / `remote_cli` / `manual` / `contract`；具体命令由 `acceptance_criteria` 与 `test-mcp-mapping.md` 决定，不从字符串里猜工具。
11. **生成优先，执行校验**：正常情况下 `required_skills` 应在 CSV 生成阶段写好；执行阶段只负责校验与修正，不临时发明验证方案。
12. **状态问答**：简短回答后继续原任务；明确暂停、取消或改变范围才更新执行边界。
13. **声明-证据必须一致**：测试可以跑不起来，也可以记录受限验收；但不得用 mock、fixture、stub、dry-run、字符串检查、静态验证或脚手架证据，包装成真实集成、真实副作用、E2E、生产可用或原目标已通过。
14. **远程训练可暂停但不可伪完成**：`remote_state=running_remote` 是合法恢复点，不是完成态。四状态不得伪装成闭环，最终完成必须等 artifacts 拉回、ingest、review handoff 更新后再判断。
15. **阻止受影响的运行，继续授权内修复**：发现会污染科研结论的错误，先阻止受影响的正式运行或入账，并将事实写入 CSV notes 和 review log。能在冻结合同和已有授权内确定性修复时，继续定位、修复和适用验证；恢复正式运行前重新满足现有 gate。需要改变科学判据、任务范围或权限时，等待该决定，继续其他不受影响的授权工作。
16. **review.md 是 Codex→Claude 交接层**：远程命令、运行状态、拉取产物、客观指标差距、未验证项和 blocker 必须写入 `issues/<stem>/<stem>.review.md`；采用“顶部当前摘要 + 底部历史日志”的单文件双层结构，不要把原始日志一股脑作为 Claude 默认入口，也不要替 Claude 下最终科研判断。
17. **运行前风险分流与审查门禁**：若 CSV 含代码更改且后续会正式运行，先执行 `prerun.change-route.v1`。`full_review` 必须先以 `execution_purpose:pre_review_smoke` 通过隔离 GPU few-step smoke，再创建唯一一个 scientific PRERUN row；失败在原 implementation row 修复重跑，不创建 FIX/PRERUN 行。`no_prerun/micro_validation/smoke_validation` 不调用 reviewer，`targeted_review/full_review` 的正式运行才要求 gate。
18. **pre-run commit 边界**：`PRERUN-REVIEW-*` 审查并记录的是本次训练 / 运行使用的 `pre_run_code_commit`，不是整个 CSV 最终所有 commit。后续 artifact 拉取、ingest、analysis、final review 或修复 commit 必须另记，不能覆盖或混淆运行所用代码 commit。
19. **claim ledger 不可丢且证据等级不可冒充**：任何 CSV notes 出现 `claims:CLAIM-*` 时，必须存在可读 `claim_ledger:<path>`，且 claim id 能在 JSON 中找到。`real_e2e` 只能由真实端到端运行写成 `verified`；被预注册门限合法跳过的条件 claim 写成 `not_run_by_preregistered_gate` 并携带 `gate_evidence`，不得写成 `verified`。`pending/failed/validation_gap` 不能通过 closing-ready。
20. **独立 scientific review**：同一 packet 保留一份科学 verdict。无 verdict 的服务失败按 `pre-run-implementation-review` 的有界恢复规则处理；已有 verdict 不通过换 reviewer 刷 PASS，不创建新 PRERUN 行。两次有界尝试仍无 verdict 且用户明确授权时，按 [用户授权审查例外](references/remote-run.md)声明 `pre_run_exception`：`review_result:not_evaluable` + `user_authorized_pre_run_exception:true`，只解锁启动、不解锁结论。
21. **Correctness first, metrics final**：模型/数据/指标/scientific args/computation sink/结果归属和未知改动走 `full_review`，顺序固定为本地验证→当前 commit 的 1–100 step 隔离 GPU smoke→一次 scientific review→official run；smoke 禁止 official metrics、artifact ingest 和输出碰撞。凭证/破坏性 lifecycle 走 `targeted_review`；rrctl、进程归属、cleanup、monitoring、scheduler、artifact transport 和 bookkeeping 走普通验证或 `smoke_validation`，不进入 scientific reviewer。效果预测不阻断。
22. **Scientific blocker 在实施行闭环**：reviewer 一次性返回全部可判定 blocker。主代理在原 implementation row 修复，补跑 production/sink probe，必要时重跑 GPU smoke，并逐项记录 blocker closure；不得创建 Attempt 2、resolution review、lineage/generation 或 closing scientific review。无法用可复现证据确认关闭时记录 `validation_gap` 并停止 official run。
23. **按风险与行为覆盖选择验证**：L0 文档/静态做结构和链接检查；L1 局部低风险做受影响文件 `compileall`/lint 及相关行为检查；L2 共享接口覆盖直接模块、调用方和关键失败边界；L3 共享核心、安全/cleanup、数据/指标/checkpoint 或大迁移运行相关共享核心集合；L4 全量仅用于发布、breaking migration、共享基础设施大改、用户明确要求或 L3 无法覆盖的系统性风险。已有成功证据仍覆盖当前代码、配置、输入、环境和待解疑点时可复用；变化后补跑受影响检查。提交前确认适用验证覆盖待提交内容，不设测试数量配额，也不因进入下一步骤而机械重跑。
24. **Outcome Contract 是读者合同**：新任务存在 `outcome_contract:<path>` 时，review 必须逐条回答 reader questions，handoff 必须呈现判定、证据、边界和下一步；不得用 issue 完成数或实现状态代替能力结论。
25. **handoff 可读且可核对**：正文清楚、自包含，结构化答案与证据保持一致。`humanizer-zh` 按需使用，不是完成门禁；不得润色机器表格、标记或路径。
26. **先分类再处置发现**：当前 scope/acceptance gap 现在修或追加正式 follow-up issue；human-required blocker 记录后继续其他可推进项；只有不阻塞当前承诺的改进和未来决策才进入 Deferred Findings ledger。
27. **sidecar 不是第二状态源**：`<stem>.deferred.json` 和 events sidecar 只保存证据、事件和讨论问题，不控制 CSV 行状态，也不得成为关闭当前 issue 的理由。CSV 是唯一的逐行执行与验收状态源；`issues/.missions.json` 只维护当前任务身份及暂停、取消、替换等生命周期，不复制行状态。
28. **完成后停在讨论入口**：原 CSV 和 handoff 闭环后，向用户展示开放的待讨论项并停止。不得自动创建下一份 CSV，也不得把待讨论项追加到当前 CSV 后继续执行。
29. **每个 CSV 都必须有 closing review，但不默认重复独立审查**：加载合法 CSV 后若没有 `REVIEW-*` 行，先追加 `REVIEW-01`。若同一 scientific commit 已完成独立 PRERUN、此后 scientific contract/dataflow/sink 未改变且机械证据无冲突，closing 直接走 `evidence-close`；只有未经过等价独立审查的高风险交付、证据冲突或疑似 current-scope gap 才走独立 capability ladder。
30. **保护用户 index**：开始时记录 `git diff --cached` 的路径与 patch。提交只命名本任务路径；已暂存的无关改动保持原样且不得进入提交。同一路径存在用户已暂存 patch、或无法精确隔离 index delta 时，记录 human-required blocker。禁止用 `git stash`、reset、移动或隐藏用户工作来简化提交。
31. **最小工件直接落盘**：新 Mission 从一开始只写终态所需工件，不创建一次性 request/state/inspect/ready/launch/pull JSON，不在 closing 阶段运行压缩或生成 `artifact-index.json`。CSV + events 是状态记录；每个实际启动的 RunID 最多保留一个 canonical RunSpec；PRERUN 与 closing 各最多保留一个最终结构化结论。`compact_artifacts.py` 仅用于 legacy Mission 的人工归档/GC，不是 closing 步骤。

下文 `<skill-dir>` 指本 Skill 所在目录，命令显式使用该路径，不假设 cwd 是 Skill 目录。接收 CSV 后，若 canonical CSV 缺少结果分析行，先运行 `python3 <skill-dir>/scripts/ensure_result_analysis_row.py <csv-path>`；再运行 `python3 <skill-dir>/scripts/ensure_review_row.py <csv-path>`。提交使用 `scripts/git_isolation.py` 的 `commit_paths`；它会拒绝同路径 staged 冲突并核对提交前后的 index patch。

仓库内任务首次进入执行时，用 `.agents/harness/workflow/mission_state.py register --task-id <SpecID-or-task-id> --csv <project-relative-csv> --source-ref <user-or-approved-spec-ref>` 登记身份；已登记则沿用，不重复创建任务。暂停、取消、切换由当前用户指令驱动，分别记录 lifecycle transition；不要把旧快照或 pending 来源当作重新请求授权的理由。completed 生命周期只有 CSV 真正闭环后才可设置。

CSV 更新统一使用 `scripts/csv_state.py`，它锁住整段读改写和 events sidecar。返回的 `csv_sha256` 可作为下一次请求的 `expected_sha256`；版本冲突时重新读取并合并本次字段，不覆盖其他写者。追加 review 和 legacy 归档也使用同一把锁。控制标签用 `set_note_tags` 显式更新；旧冲突返回 `notes_conflict`，不得任取首值/末值。`event` 等证据历史继续追加。

**写入前先跑 `scripts/preflight.py <csv> [request.json ...]`**（只读）：把 `csv_state.py` 的请求面校验（schema、commit_boundary、set_note_tags、PRERUN 枚举）、分支上下文与 claim 引用在首次写入前一次性静态检查，避免在关键路径上逐个踩运行期错误。preflight 不代替 `csv_state.py` 的权威校验，只把可预见的失败前移。

# 闭环完成判定

`csv_completion_errors()` 是唯一最终闭环判断，核验实际 Git、ingest、claim、post-run result analysis 和 handoff；恢复与生命周期 completed 共用它。`final_ready.py` 只检查 closing 前置条件，通过不代表 Mission 已完成。用户要求不提交时，保留真实未提交状态和剩余项。

Canonical CSV 中，所有正式结果进入 `remote_state=ingested` 后，必须先完成唯一的 `RESULT-ANALYSIS-01` 行：由全新的 `scientific-reviewer` sub-agent 独立读取原始证据，写入 `research_workspace/experiments/<ExpID>/analysis/analysis.md` 和 `reviews/result-analysis.json`。主 Executor、advisor、closing `evidence-close` 或 self-review 都不能替代该分析；`final_ready.py` 与 `csv_completion_errors()` 都会 fail-closed 校验覆盖范围、四段标题、SHA-256、证据引用及可核验模型身份。分析完成后才进入 `REVIEW-*`。

以下四项是必要状态；完成检查还核验实际 Git、适用的远程产物和合同，不能仅凭四个字符串宣布闭环：

- `dev_state=已完成`
- `review_initial_state=已完成`
- `review_regression_state=已完成`
- `git_state=已提交`

若任意行 notes 包含 `claims:CLAIM-*`，必须先用 `mission-csv-execute/scripts/validate_claim_ledger.py` 或等价检查确认 ledger 可读、claim id 存在、状态与证据等级一致；否则该 CSV 不完整，不得把最终 `REVIEW-*` 标成通过。`not_run_by_preregistered_gate` 是有决策证据的合规终态，不等于 E2E 通过，也不阻止“按批准协议完成”的 Mission 闭环。

远程训练行额外遵循：

- `remote_state=running_remote`：合法可恢复暂停点，但不算闭环完成。
- `remote_state=completed`：仅远程 worker 结束，仍需 pull/ingest，不能作为科研交付终态。
- `remote_state=artifacts_pulled`：已拉回原始产物，仍需 ingest 与 review handoff。
- `remote_state=ingested`：结果已进入实验记录，且 `issues/<stem>/<stem>.review.md` 已写入客观摘要后，先完成 `RESULT-ANALYSIS-01`，再可继续按四状态判断闭环。
- 未实际完成 train/eval 或未拉回 artifacts 时，不得声称实验完成、指标有效或当前最优。

`REVIEW-*` 行还必须满足：

- 已根据 closing risk 选择 `evidence-close` 或独立 capability ladder；不得仅因存在 REVIEW 行就调用 reviewer
- review log 和 CSV `notes` 已记录 `review_agent_mode:<evidence-close|reviewer-subagent|codex-exec-independent|self-review>`、`review_independence:<true|false>`、适用的模型字段、实际存在的 ledger、coverage、`review_result` 与 `scientific_outcome`
- review 结论已经写入 review log
- 已产出 human handoff（`<csv-path-without-.csv>.handoff.md`），CSV `notes` 已记 `handoff:<path>`，并已记录 `handoff_contract:passed` 或 `handoff_contract:failed <reason>`；若 `review_result:vision_met`，必须是 `handoff_contract:passed`
- 若发现当前 scope/acceptance gap，已追加 follow-up issue 和下一轮 `REVIEW-(N+1)`
- 若存在开放 Deferred Findings，ledger 已通过 `validate_deferred_ledger.py`，handoff 已逐条覆盖，最新 REVIEW notes 已记录 `deferred_coverage:<covered>/<open>`
- evidence-close/self-review 已完整分类并处置所有发现时可以闭环；不得仅为等待独立能力而追加空转的 `REVIEW-*`

`PRERUN-REVIEW-*` 行还必须满足：

- 按科学审查 Skill 完成 readiness 和适用审查，结论与 blocker closure 可核实。
- CSV、review log 和 RunSpec 绑定同一 gated run 与源码 commit；写回字段见下文 PRERUN 桥接。
- scientific gate 与 closing review 的 `review_independence` 分开，不互相替代。

# Issue 选择规则

## 优先收敛半成品

若存在 `git_state=未提交` 且 `dev_state=进行中` 或 `已完成` 的行，优先选这些。

若存在 `remote_state=artifacts_pulled` 但尚未 `ingested` 的行，优先完成 ingest 与 review handoff。

若存在 `remote_state=running_remote` 的行，先判断是否有可用 artifacts：
- artifacts 已可拉取：进入恢复流程。
- artifacts 仍未完成且当前会话可等待：读取远程运行 reference，启动一次前台低频 `rrctl wait`；不要反复调用 `inspect`。
- 只有当前会话无法继续等待时，才保留为可恢复暂停点；不得把该行视为完成。

## Pre-run Review 行顺序

`PRERUN-REVIEW-*` 行只在它 gate 的首次训练 / 运行 row 之前执行。

- 当前 `PRERUN-REVIEW-*` 之前的代码实施、本地轻量验证及 `full_review` 当前 commit 的 pre-review smoke 必须闭环完成
- 当前 `PRERUN-REVIEW-*` 之后的训练、评估、远程运行或实验结果生成 row，必须等待该 pre-run review 得到 `pre_run_result:pass`
- official 行按 `prerun_route.py` 的 `requires_prerun` 分流；只有 `targeted_review/full_review` 缺有效 gate 时才切回审查。`no_prerun` 不要求历史 PRERUN，`micro_validation/smoke_validation` 要求各自 probe evidence。受限 smoke/预注册只读 probe 按现有 route 边界在正式审查前运行。
- 若已审查 commit 后出现新 diff，先运行 change route；`no_prerun/micro_validation/smoke_validation` 绑定 reviewed/candidate commit 与 probe evidence 后继续，只有 `targeted_review/full_review` 才要求新的 formal verdict
- 若 scientific review 发现可修复问题，回到原 implementation row 一次性修复全部 blocker；不得插入 Attempt 2、resolution review 或新 scientific PRERUN row
- readiness failure 回到原 implementation row 补齐证据；reviewer capability failure 只记录一次具体 gap，不机械追加或轮询 PRERUN row
- 已闭环或有真实 `running_remote` 证据的旧 CSV 只读兼容且不批量迁移；新代码快照使用 `prerun.scientific-review.v1` lean packet；同一已审查 commit 的 retry/stage 不重复 PRERUN

## Vision Review 行顺序

`REVIEW-*` 行只在它之前的所有非 review 行都闭环后执行。

如果 `REVIEW-N` 追加了 follow-up issue 和 `REVIEW-(N+1)`，则 `REVIEW-N` 自己正常闭环；执行器继续后续 follow-up issue，之后再执行新的 review 行。不要让旧 review 行保持挂起，也不要回头重开旧 review 行。

## 再选最高价值项

P0 → P1 → P2；优先能解阻塞/提供公共能力的任务；减少无意义上下文切换。

## 记录选择原因

选中后在该行 `notes` 追加 `picked_reason:<why>`。

# 执行闭环（每条 issue）

若当前行满足 `id=PRERUN-REVIEW-*` 或 `notes` 包含 `review_kind:pre_run_implementation`，进入下文 PRERUN 桥接。

若当前 `PRERUN-REVIEW-*` 行未声明可用 review skill，先将 `required_skills` 修正为 `pre-run-implementation-review` 并写回 CSV，再继续执行 gate。

若当前行满足 `id=REVIEW-*` 或 `area=review`，跳到「Vision Review 闭环」。

## 确认范围和上下文

核对当前 issue 的 `id/title`、验收口径、风险和破坏性影响。编码前检查以下执行信息；缺失或与批准范围不符时先修正 CSV：

- `acceptance_criteria`（必须可验证，最好有复现步骤/阈值）
- `required_skills`（本行确需的 skill；无则留空，不填占位值）
- `review_initial_requirements`（必须可执行）
- `review_regression_requirements`（必须可执行）
- `test_mcp`（主验证模式，取值限 `local_cli` / `remote_cli` / `manual` / `contract`）
- `refs`（至少 1 个 `path:line`）

从 `refs` 指向文件和必要调用方开始，遵循本行适用 skill。已读且未变化的内容可复用；信息不足时用 `fast-context` 定位调用链，已知字符串用 `rg`。能确定改动位置、边界和验证方式后进入实现。

## 实现与适用验证

通过 `csv_state.py` 将开发和初审状态记为进行中，按验收口径实现最小变更，并同步文档和 refs。对照 `review_initial_requirements` 自查，按 `review_regression_requirements` 与 `test_mcp` 做风险匹配的验证；已覆盖当前内容的成功检查不重复执行。

科学指标、loss、checkpoint 语义或数据流验收必须经过真实计算入口到 forward/loss/attention/eval sink；模块单测不能替代。普通函数或数据结构可用模块检查。“step0 保留 baseline”需要实际等价性数值证据，仅断言残差为零不够，详见科学审查 Skill 的 Baseline-Equivalence Probe。

验证模式见 `test-mcp-mapping.md`。确认标题、报告、metadata、CSV notes 和完成声明未高估证据；验证不可执行时才进入受限验收，不能用 mock/static 代替真实效果。证据否定交付声明时，在授权范围内修复实现或纠正声明。

仅当选中远程 train/eval 行时加载 [references/remote-run.md](references/remote-run.md)，由公共 `remote_run.py` 核验现有 route 和任务绑定。普通本地 issue 不加载远程说明。

## 记录事实与核验提交

把已完成的开发、初审和回归状态及实际证据写回 CSV；受限验收如实记录 gap，不声称测试通过。单值标签用 `set_note_tags`，长日志写已有 events。尚未核验提交时保持 `git_state=未提交`。

- 按当前用户授权决定是否提交；用户要求不提交时保留工作树与真实未提交状态。
- 使用 `scripts/git_isolation.py` 的 `commit_paths`，只提交本任务代码及适用 artifact root；同路径用户 staged 冲突时保留原状。
- 提交成功后核 Git 对象、任务路径/内容、父关系与 index，再用 `csv_state.py` 写 `git_state=已提交` 和实际 commit 引用。兼容 19 列 CSV 可用 `commit_hash:<hash>` 标签。
- 运行行的 `commit_hash` 仍指允许运行的源码；后续结果/账本提交另记。最终 CSV 后态纳入现有 checkpoint，核其实际 Git 对象，不要求文件包含自己的 commit hash。
- 响应丢失先查 Git；无法确认就记录 gap，不猜 HEAD、不盲重提。主仓库与科研工作区分别提交，沿用项目 commit message 约定。

## 继续或交付

回到 Issue 选择规则，推进剩余授权工作；完成、暂停与恢复按下文停止条件处理。

科研交付含本轮更新的定稿主分析且 Hindsight 已启用时，按 [入账指引](../research-memory/references/publication.md) 准备本轮预览。确认与同步独立于科研闭环，不新增 CSV 等待行。

# Pre-run Scientific Implementation Review 闭环

仅在路由要求 `targeted_review/full_review` 时进入 [pre-run-implementation-review](../pre-run-implementation-review/SKILL.md)。该 Skill 是 smoke、lean packet、readiness、reviewer 范围、服务恢复及 blocker repair 的详细依据；这些细节不在主执行文档重复维护。

执行器负责 CSV 与运行之间的桥接：

1. 绑定原 implementation row、唯一 gated run、candidate commit 和 exact official command；按专用 Skill 完成证据准备和 `prerun_ready.py`。`ready:false` 回原实施行补齐，不新增 PRERUN 编号。
2. readiness 通过后创建并执行该 gated run 的唯一 `PRERUN-REVIEW-*` 行，记录 `readiness_result:pass`。审查内容和服务恢复交专用 Skill。
3. 将原 verdict、reviewer id、`review_agent_mode`、`review_mode`、`gated_run`、`pre_run_code_commit` 写入 CSV notes 和 review log 的 `Pre-run Implementation Review` 段落；`not_evaluable` 及未关闭 blocker 不能写 pass。
4. 审查通过或原 implementation row 已用可复现 production/sink evidence 关闭所有 blocker 后，记录真实 `pre_run_result:pass` 和 closure evidence。RunSpec 的 `gate_provenance` 必须与这些事实一致，公共入口会核验。

缺科学证据、readiness 失败或服务恢复耗尽时，受影响 official run 保持阻塞；继续授权内修复或其他独立工作。原 verdict 不被后续修复覆盖，也不通过再派 reviewer 刷 PASS。

# Vision Review 闭环

仅当选中 `REVIEW-*` 行时，读取并严格执行 [references/closing-review.md](references/closing-review.md)。普通实现、PRERUN 和远程等待阶段不加载该文件。

# 受限验收

只有目标验证实际不可执行时才读取 [references/limited-validation.md](references/limited-validation.md)，不要在正常通过路径加载。

# 阻塞策略

允许跳过，但必须回收：

1. 在该行 `notes` 记录 `blocked:<原因>` + 已排查内容 + 下一步建议
2. 状态保持真实进度；Git 状态由实际提交核验决定，不能因阻塞覆盖已存在的提交事实
3. **允许切到下一条继续推进**
4. 只有当所有剩余 issues 都是 human-required blockers 时，才停止并汇总阻塞清单，向用户请求最小必要信息
5. 授权范围内的普通实施歧义可记录有依据的 assumption 后继续；科学判据、范围或权限的未定决定不能用假设越过

# 停止与恢复

| 情形 | 动作 |
|---|---|
| 原任务全部闭环 | 交付结果，范围外建议留待用户决定 |
| 用户明确暂停/取消/改变范围 | 更新任务生命周期，保存当前 row、RunID 和必要恢复指针 |
| 有真实外部阻塞或会污染结论的设计错误 | 记录具体缺项与最小修正，继续不依赖它的授权工作 |
| 远端仍运行且宿主可等待 | 观察同一 RunID，结束后 pull/ingest |
| 宿主/预算限制要求交还控制 | 保存已验证进度与下一动作；不把限制写成实验失败或重新 launch |
| 状态提问、阶段成果、普通 checkpoint | 简短说明后继续原任务 |

进展说明包含有变化的事实、已做验证与下一动作；阻塞说明包含具体缺项。远程恢复至少保留 CSV/row、RunID、源码 commit、control/artifact 路径和恢复命令，不固定消息模板或末尾动作。
