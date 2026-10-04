---
name: mission-approved-doc
description: Use when the input is a committed, unchanged canonical mission spec with status approved and the agent needs to map it into executable issues artifacts before handing off to CSV execution.
---

你现在是「批准文档执行器」。

# 目标

把一个已提交且未改动的 canonical approved spec 转换为 `issues/<stem>/<stem>.csv`，然后交给 `mission-csv-execute` 闭环执行。

# 流程

## Phase 1：批准门验证（HARD STOP）

1. 确认输入文档存在并完整读取
2. 运行 `python <mission-spec>/scripts/validate_spec.py <doc-path>`
3. 只接受 `mission: spec`、`status: approved`、已存在于 `HEAD` 且工作副本未改动的文档
4. 校验失败则硬停，只输出：
   ```
   文档 <path> 不是已提交且未改动的 approved mission spec。
   请返回 mission-spec 修正或重新批准。
   ```
5. 未经批准绝不执行任何代码变更

## Phase 2：读取与抽取

优先读取文档本体，再按需抽取以下信息：

| 来源 | 必须 | 提取内容 |
|------|------|----------|
| canonical spec 正文 | 是 | Goal, scope, constraints, affected files, task structure |
| 显式 testing / validation 章节 | 重要 | 验收口径、命令、风险点 |
| 与文档直接关联的 code/file refs | 重要 | `refs`, `area` 推断 |

字段抽取与拆分规则详见 `doc-field-mapping.md`。

## Phase 2.5：确认执行范围

如果源文档包含多个 phase / block / stage / milestone 划分：

1. 检查用户触发时是否指定了范围（如"只做 phase 1"、"执行 Block A"、"先做到 worker 能跑"）
2. 若已指定 → 记录为 `execution_scope`，后续覆盖率扫描只检查该范围内的承诺
3. 若未指定 → `execution_scope` = 文档全文，覆盖率扫描检查整个 spec 的所有可验证承诺
4. 将确认的 `execution_scope` 写入 CSV 文件的第一个 issue 的 `notes` 字段：`execution_scope:<范围描述>`

覆盖率扫描的边界以此为准，不越界。

## Phase 2.6：抽取 Claim/Evidence Ledger

在生成 issue 前，先从 `execution_scope` 中抽取一张 claim/evidence 账本，并随 CSV 同目录落盘为 `issues/<stem>/<stem>.claims.json`。CSV notes 只保存 claim id 和 `claim_ledger:<path>` 引用；同目录产物优先写 sibling-relative 路径，如 `claim_ledger:<stem>.claims.json`。不得只写 `claims:CLAIM-*` 而不持久化定义。

每条 claim 至少包含：

| 字段 | 含义 |
|------|------|
| `claim_id` | `CLAIM-001` 递增 |
| `source_ref` | 源文档 `path:line` |
| `promise` | 可验证承诺本体 |
| `production_path_required` | 是否要求启动注册、API、worker、agent tool、consumer、真实 provider、E2E 等生产路径 |
| `covered_by` | 负责实现/验证的 issue id，生成后回填 |
| `evidence_required` | `real_e2e` / `integration` / `unit` / `static` / `mock_allowed` / `limited_allowed` |
| `status` | 生成时只写 `pending` 或文档明确排除时写 `out_of_scope`；执行终态使用 `verified / not_run_by_preregistered_gate / failed / validation_gap / out_of_scope` |

`evidence_required=real_e2e` 的 claim 只有真实端到端运行后才能写 `verified`，并必须附 `evidence_refs`。若预注册门限决定后续阶段不运行，写 `not_run_by_preregistered_gate` 和非空 `gate_evidence`；这表示按协议终止，不表示该能力通过。

只抽取可验证承诺：WHEN/MUST/SHALL、状态枚举、字段定义、启动行为、消费关系、错误处理、API 契约、真实副作用、显式 non-goal 边界。不要把背景、愿景口号、解释性段落当 claim。

`*.claims.json` 必须使用以下结构：

```json
{
  "source_doc": "<doc-path>",
  "csv": "<csv-file-name>",
  "execution_scope": "<scope>",
  "claim_coverage": {"covered": 0, "total": 0, "status": "pending"},
  "claims": [
    {
      "claim_id": "CLAIM-001",
      "source_ref": "<doc-path>:<line>",
      "promise": "<可验证承诺原文或忠实改写>",
      "covered_by": ["ISSUE-01"],
      "evidence_required": "integration",
      "production_path_required": true,
      "status": "pending"
    }
  ]
}
```

## Phase 2.7：抽取 Outcome Contract

读取 `mission-csv-execute/outcome-contract.md`，从 `execution_scope` 提取面向最终读者的 Outcome Contract，并与 CSV 同目录落盘为 `issues/<stem>/<stem>.outcomes.json`。

Outcome Contract 与 claim ledger 分工不同：

| 工件 | 回答什么 | 消费者 |
|---|---|---|
| `*.claims.json` | spec 承诺是否被实现和验证 | issue / vision review |
| `*.outcomes.json` | 用户最终要知道什么、什么结果决定成败、现在不能声称什么 | vision review / handoff / 专项报告 |

依次提取 `artifact_role`、`desired_effects`、`reader_questions`、`decisive_result` 和 `blocked_claims`。reader question 必须面向决策、可以证伪、有证据入口并声明范围。

每个 effect/question/blocked claim 都必须有 `source_ref`。当前会话只可作为补充来源，并以 `source_ref=original-request` 持久化；不得凭模型印象增加源文档没有承诺的新能力。不得写 benchmark expected answer、case 特化提示或预填 pass/fail。

生成后必须运行：

```text
python <mission-csv-execute>/scripts/validate_outcome_contract.py issues/<stem>/<stem>.outcomes.json
```

校验失败时先修 contract，不得生成 CSV 或进入执行。

## Phase 3：生成 CSV

`issues/TEMPLATE.csv` 是本项目唯一固定的科研 28 列 CSV schema。`mission-approved-doc` 只负责把批准文档映射到该表头；官方 19 列只作为显式外部 compatibility CSV 输入兼容，不生成。

生成文件：`issues/<stem>/<stem>.csv`

其中 `<stem>` 固定为 `<YYYY-MM-DD_HH-mm-ss>-<topic>`。

关键规则：

- 正式任务 CSV 固定放在 `issues/<stem>/<stem>.csv`
- `issues/*.csv` 是 legacy 平铺格式，只为恢复和显式输入兼容；新生成不得继续写平铺 CSV
- 生成前读取 `issues/TEMPLATE.csv`，并使用 structured CSV writer 生成完全一致的 28 列表头
- `acceptance_criteria` 优先从文档里的 validation / testing / success criteria 提取
- **原子性约束**：单个 issue 必须是一个可独立验证、独立提交的原子变更
- `required_skills` 必须在生成阶段显式写全（`required_mcp` 为 legacy 兼容列，固定留空）
- `refs` 必须至少包含 1 个 `path:line`
- **闭环路径约束**：生成组件 issue 后，必须按 `doc-field-mapping.md` 闭环路径规则扫描跨模块消费关系、启动注册、工具注册、flow 注入点，为每个被文档承诺的连接点生成独立接线 issue
- 每个普通 issue 和 `REVIEW-01` 的 `notes` 必须引用 `outcome_contract:<stem>.outcomes.json`
- 同目录初始化 `<stem>.deferred.json`：`{"schema_version":1,"csv":"<stem>.csv","findings":[]}`；每个普通 issue 和 `REVIEW-01` 的 notes 都引用 `deferred_ledger:<stem>.deferred.json`
- `REVIEW-01` 必须要求逐条回答 reader questions，并区分实现状态、验证状态和能力结论
- 在普通执行 issue 之后，若任务包含正式远程结果或科研 ExpID，必须先追加唯一一条 `RESULT-ANALYSIS-01`（`phase=analysis`、`required_skills=post-run-result-analysis`、`remote_state=not_applicable`），再追加 `REVIEW-01`；分析行的 `notes` 引用 `result_analysis:reviews/result-analysis.json`，review 行也引用同一路径
- 之后必须追加一条 `REVIEW-01` 作为首轮文档愿景验收；该行必须包含从源文档抽取的任务专属 claim/evidence 检查项，不能只写通用套话
- 初始化状态：`未开始` / `未提交`

### Claim 覆盖率扫描（HARD — 在追加 REVIEW-01 之前执行）

生成所有组件 issue 和接线 issue 后，执行以下覆盖率检查：

1. 回读 Phase 2.6 的 claim ledger
2. 对每条 claim，检查是否至少被一个 issue 的 `acceptance_criteria` 显式覆盖
3. 若 claim 要求生产路径，检查是否存在独立接线 issue 或该 issue 的 AC 明确覆盖生产路径
4. 检查每条 claim 的 `evidence_required` 是否能被对应 issue 的 `test_mcp` / review 条件支撑
5. 未覆盖的 claim 按以下规则处理：
   - 在 `execution_scope` 内 → **补 issue** 或追加到现有 issue 的 AC
   - 在 `execution_scope` 外（文档明确标注为 non-goal / future / deferred / 超出用户指定范围）→ 在 CSV 末尾 notes 记录 `out_of_scope:<doc-section>;<reason>`
   - 无法确定归属 → 补 issue 标 `P2`，交给 REVIEW-01 判断
6. 覆盖率扫描完成后，在生成摘要中报告：`Claim 覆盖: X/Y 条已覆盖，P 条生产路径已覆盖，Z 条标注 out_of_scope`
7. 将最终 claim/evidence ledger 写入 `<stem>.claims.json`；若任何 CSV notes 出现 `claims:CLAIM-*`，同一 notes 必须包含 `claim_ledger:<path>`

在 CSV 中记录账本时使用压缩 notes，不要把整篇 spec 复制进 CSV。推荐格式：

```text
claim_ledger:<stem>.claims.json; claims:CLAIM-001,CLAIM-002; claim_coverage:X/Y; claim_coverage_status:pending; evidence_level:integration; production_path:covered
```

### `RESULT-ANALYSIS-01` 行规则

`RESULT-ANALYSIS-01` 是正式结果入账后的科学分析门禁，不是 closing review，也不由主 Executor 自审：

- 只为 canonical 28 列科研 CSV 生成；显式 19 列 compatibility CSV 不迁移
- 所有 `remote_state=ingested` 的非空 `(exp_id, run_id)` 必须由全新的 `scientific-reviewer` sub-agent 分析，并在索引中逐一覆盖
- `notes` 至少包含 `analysis_kind:post_run; result_analysis:reviews/result-analysis.json; analysis_agent_mode:pending; analysis_independence:pending; analysis_requested_model:<review_contract.toml 的 Pi 当前值>; analysis_observed_model:pending; analysis_model_evidence:pending; analysis_model_evidence_ref:pending`
- 分析输出必须原样落入 `research_workspace/experiments/<ExpID>/analysis/analysis.md`，严格包含 `Change / Result / Finding / Next` 四段；`reviews/result-analysis.json` 必须记录 hash、证据引用、固定 scientific outcome、逐条 `review_evidence_ref` 和 `review_output_sha256`，并绑定可核验模型证据
- `final_ready.py` 与 `csv_completion_errors()` 都会在进入 `REVIEW-*` 前 fail-closed 检查；advisor、closing review 或 self-review 不能替代该行

### `REVIEW-01` 行规则

`REVIEW-01` 是审计事件，不是普通实现任务。

下表只列 `REVIEW-01` 需要覆盖的字段取值，不是完整 CSV 表头。实际 CSV 必须包含 `issues/TEMPLATE.csv` 中的全部 28 列；未列出的状态字段按标准默认值初始化：`dev_state=未开始`、`review_initial_state=未开始`、`review_regression_state=未开始`、`git_state=未提交`、`owner=`。

生成 `REVIEW-01` 时，先从批准文档中抽取用户真正承诺的结果，并写进 review 条件：

- 若文档声明完成某个真实行为、真实副作用、真实集成、真实迁移、真实发送、真实同步、可见交互或端到端流程，review 条件必须检查证据是否支撑同等级声明
- 若交付只使用 mock、fixture、stub、dry-run、scaffold、字符串检查或静态验证，review 条件必须要求它被如实标注，且不得冒充真实完成
- 若测试或外部验证无法运行，review 条件必须检查是否记录 `validation_limited` / `manual_test` / `risk`，不得用替代假路径伪装通过
- `review_regression_requirements` 必须包含 2-4 条来自源文档的任务专属检查项，并要求逐条审查 claim/evidence ledger；如果无法抽取，至少写明要审查 claim/evidence 是否一致

建议字段：

| 字段 | 值 |
|------|----|
| `id` | `REVIEW-01` |
| `priority` | `P0` |
| `phase` | 最后阶段序号 |
| `area` | `review` |
| `title` | `Review documented vision against delivered work` |
| `description` | `Compare approved-spec claims with delivered behavior, evidence level, CSV state, validation evidence, and review log; use evidence-close unless closing risk requires an independent reviewer.` |
| `acceptance_criteria` | `WHEN all non-review issues before this row are closed THEN run mechanical readiness and choose evidence-close for L0-L2 or an unchanged commit already covered by independent scientific PRERUN; WHEN unresolved L3/L4 risk, evidence conflict or a suspected current-scope gap exists THEN try reviewer-subagent, codex-exec-independent, then self-review; WHEN a current-scope gap or overstated claim is found THEN append follow-up issues and REVIEW-02; WHEN no current-scope gaps remain THEN close the CSV while recording Mission result separately from scientific outcome.` |
| `test_mcp` | `manual` |
| `required_skills` | 留空 |
| `required_mcp` | Legacy 兼容列，固定留空 |
| `review_initial_requirements` | `Verify all prior non-review rows are closed before running this review.` |
| `review_regression_requirements` | `Run risk-routed closing review against approved goals, claim/evidence ledger, acceptance criteria, delivered diff and validation evidence; do not repeat independent review when the same scientific commit already passed PRERUN and no scientific sink changed; separate Mission execution result from scientific outcome.` |
| `refs` | `<doc-path>:1` |
| `notes` | `review_kind:vision; review_agent_mode:pending; review_independence:pending; review_requested_model:pending; review_observed_model:pending; review_model_evidence:pending; source_doc:<doc-path>; claim_ledger:<stem>.claims.json; outcome_contract:<stem>.outcomes.json; deferred_ledger:<stem>.deferred.json; result_analysis:reviews/result-analysis.json; review_json:reviews/review-01.json; claim_coverage:<X/Y>; claim_coverage_status:pending; scientific_outcome:pending` |


## Project scientific adaptation (HARD)

- `issues/TEMPLATE.csv` is this repository's only canonical CSV schema. New directory artifacts use all 28 columns in that exact order; the official 19-column schema is accepted only for explicitly supplied external compatibility CSVs and is never generated here.
- New artifacts are written directly to their final locations under `issues/<stem>/`. Keep only the CSV, evidence-bearing ledgers, human review/handoff, one final closing review JSON, and one canonical RunSpec per launched RunID; do not emit request/state/retry/inspect JSON or a terminal artifact index. All relative sidecar paths resolve from the artifact root.
- Preserve `spec_id`, `exp_id`, `run_id`, `remote_state`, `artifact_path`, `branch`, `commit_hash`, `next_action`, and `updated_at`. Initialize non-remote rows with `remote_state=not_applicable`.
- If approved work changes code and then trains, evaluates, launches a remote run, or generates experiment results, create at most one `PRERUN-REVIEW-N` per gated run after implementation/local validation/current-commit GPU smoke and before the official run. Use `pre-run-implementation-review`, `prerun.scientific-review.v1`, one independent reviewer, and no Attempt/lineage/generation/liveness state.
- Scientific blockers return to the original implementation row and may be closed only with production/sink evidence. Smoke, rrctl evidence, or self-review alone cannot write `pre_run_result:pass`.

## Phase 4：生成后摘要

CSV 已落盘后，把它绑定到 spec 阶段登记的任务：

```bash
python .agents/harness/workflow/mission_state.py bind --task-id <SpecID> --csv issues/<stem>/<stem>.csv --source-ref <approved-spec-path>
```

旧项目尚未登记该任务时，先用 `register --task-id <SpecID> --spec <approved-spec-path> --source-ref <approval-source>`。
恢复依据使用这个当前指针；任务生命周期不替代 CSV 行状态或实验验收。

```
生成完成
- 快照: issues/<stem>/<stem>.csv
- 来源: <doc-path>
- Issues: N 条（含 REVIEW-01）
  - 组件 issue: X 条
  - 接线 issue: Y 条
- P0 任务: M 条
- Claim 覆盖: A/B 条 spec 承诺已覆盖，P 条生产路径已覆盖，C 条标注 out_of_scope
- Claim ledger: issues/<stem>/<stem>.claims.json
- Outcome Contract: issues/<stem>/<stem>.outcomes.json
- Deferred findings: issues/<stem>/<stem>.deferred.json
- 下一步: 进入闭环执行
```

## Phase 5：委托执行

直接进入 `mission-csv-execute` 模式，以刚生成的 CSV 为输入，开始闭环执行。
