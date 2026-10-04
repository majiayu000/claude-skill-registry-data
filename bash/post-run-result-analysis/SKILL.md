---
name: post-run-result-analysis
description: Use after remote experiment artifacts are ingested to require an independent strong-model analysis before closing a Mission.
---

# Post-run Result Analysis

本 skill 只处理**运行完成并已 ingest 后的科研结果分析**，不启动、恢复或修改远程运行，也不替代 `pre-run-implementation-review` 或 closing review。

## 目标与硬门禁

- `remote_state=ingested` 的每个非空 `(ExpID, RunID)` 都必须出现在 `reviews/result-analysis.json`。
- 每个条目必须绑定最终的 `research_workspace/experiments/<ExpID>/analysis/analysis.md`、其 SHA-256、原始证据引用和科学结果状态。
- 正式分析必须由独立的强模型 reviewer 完成，模型取 `config/review_contract.toml` 的宿主当前值、thinking 级别同见该文件的 `[thinking].level`；两条等价通道按宿主选择：
  获批模型值定义在 `.agents/harness/config/review_contract.toml`（项目自有，不参与模板同步）；运行时校验与按宿主推导在 `.agents/harness/review_model.py`。额度耗尽等原因需要切换时改前者（一次显式提交），验证器与各 runner 自动跟随，不允许会话内临时传参绕过。 同一逻辑模型在不同宿主的注册名可不同（Pi 用 provider 前缀名，codex CLI 用裸名），`review_model.py` 的 `MODELS` 映射按宿主给出调用名；索引与 CSV 记录统一用 canonical（Pi 侧）名字，验证器接受任一宿主注册名加 thinking 后缀的运行时观测值。
  1. **Pi 通道（`scientific-reviewer-subagent`）**：当前会话派发注册的 `scientific-reviewer` sub-agent（`.pi/agents/scientific-reviewer.md`，`agentScope: project`）；
  2. **codex-exec 通道（`codex-exec-independent`）**：宿主无 sub-agent 派发能力时，用 `scripts/run_result_analysis.py` 启动 fresh、ephemeral、read-only 的独立 `codex exec` 会话（模型取自 `config/review_contract.toml` 的 codex 值）。
- `advisor` 可以在存在冲突解释或研究方向选择时提供辅助意见，但不能生成正式分析、verdict 或关闭分析行。
- 强模型身份无法从 host/session metadata 或 CLI 事件流核验时，停止在分析行；不得回退到主 Executor、自审或把模型自报名称当作证据。两条通道各自只接受可机械核验的证据：
  - Pi 通道：`model_evidence_ref` 必须绑定真实 session UUID 和 `subagent` tool-call ID（`session:<uuid>#tool:<tool-call-id>`），由验证器核对 `scientific-reviewer`、实际模型、成功终态和输出 hash；
  - codex-exec 通道：`model_evidence_ref` 必须是 `exec:reviews/result-analysis-<ExpID>/verdict.json#verdict`（CSV 相对路径），由验证器读取 verdict、核对其 schema、事件流观测到的模型和输出 hash；
  都不能写 `pending`、`unknown` 或占位字符串。
- 主 Executor 只负责整理事实、保存 reviewer 返回内容和更新状态；不能自行补写科学结论、替换 `scientific_outcome` 或把替代验证包装成结果。

## 输入边界

分析前先读取：

1. approved spec / outcome contract、当前 CSV 和 claim/evidence ledger；
2. 每个目标 RunID 的 RunSpec、manifest、record、summary 和原始 artifact；
3. 对应 baseline、fold、shot、ablation 和预注册 gate；
4. `issues/<stem>/<stem>.review.md` 中的客观运行摘要、异常和 validation gap。

不要把主 Executor 已写的结论、主观 handoff 或 advisor 回复作为事实输入。它们最多作为待核对材料；原始指标和可定位文件优先。

## 强模型调用

为每个 ExpID 启动一次全新的 `scientific-reviewer` sub-agent；调用必须显式携带当前仓库 `cwd`，并在 task 中加入机器可解析的目标行，例如：

```text
subagent(agent="scientific-reviewer", agentScope="project", cwd="<repo>", task="...")
result_analysis_targets: {"exp_id":"<ExpID>","run_ids":["<RunID-1>","<RunID-2>"]}
```

- 只读、不得调用 advisor、不得再次委派；
- 请求模型取 `config/review_contract.toml` 的 Pi 当前值、thinking `high`；

codex-exec 通道的调用方式（quota、launcher 失败与静默都是 review-service failure，修好服务后用同一命令重跑，不产生第二次科学意见）：

```bash
python3 .codex/skills/post-run-result-analysis/scripts/run_result_analysis.py \
  --csv issues/<stem>/<stem>.csv \
  --exp-id <ExpID> \
  --run-ids <RunID-1> <RunID-2> \
  --workdir .
```

runner 从 CSV 校验 `(ExpID, RunID)` 覆盖、写 `reviews/result-analysis-<ExpID>/verdict.json`（schema `post-run.result-analysis-verdict.v1`，含 task/事件流/规范化输出的 SHA-256 与事件流观测模型）；`observed_model` 只来自 CLI JSON 事件流的可信事件（`thread.started`/`session_meta` 等），reviewer 自报文本不算证据。
- prompt 明确要求独立读取证据，不信任主代理总结；
- 每个 ExpID 只启动一次 reviewer，并将该 ExpID 的全部目标 RunID 放入 `run_ids`；
- 最终 assistant message 必须是**不带代码围栏或额外 prose 的严格 JSON 对象**，且只能包含以下字段：

```json
{
  "exp_id": "<ExpID>",
  "run_ids": ["<RunID-1>", "<RunID-2>"],
  "analysis_markdown": "## Change\n...\n\n## Result\n...\n\n## Finding\n...\n\n## Next\n...\n",
  "scientific_outcome": "inconclusive",
  "limitations": [],
  "validation_gaps": []
}
```

`scientific_outcome` 必须是 `hypothesis_supported`、`hypothesis_not_supported`、`gate_failed`、`inconclusive` 或 `not_applicable`；主 Executor 不得改写 JSON 中的任一科学字段。

## 持久化

1. 将 sub-agent 的四段正文原样保存为：

   ```text
   research_workspace/experiments/<ExpID>/analysis/analysis.md
   ```

   `analysis.md` 必须逐字保存 JSON 的 `analysis_markdown`（仅允许换行规范化），不得补写或改写科学语义。

2. 将索引保存为：

   ```text
   issues/<stem>/reviews/result-analysis.json
   ```

   最小结构：

   ```json
   {
     "schema_version": "post-run.result-analysis.v1",
     "status": "complete",
     "analysis_agent_mode": "scientific-reviewer-subagent | codex-exec-independent",
     "analysis_independence": true,
     "requested_model": "<review_model 的宿主当前值>",
     "observed_model": "<同一模型的运行时观测值>",
     "model_evidence": "session-metadata | event-stream",
     "model_evidence_ref": "session:<uuid>#tool:<subagent-tool-call-id> 或 exec:reviews/result-analysis-<ExpID>/verdict.json#verdict",
     "entries": [
       {
         "exp_id": "<ExpID>",
         "run_id": "<RunID>",
         "analysis_path": "research_workspace/experiments/<ExpID>/analysis/analysis.md",
         "analysis_sha256": "<sha256>",
         "scientific_outcome": "inconclusive",
         "review_evidence_ref": "session:<uuid>#tool:<subagent-tool-call-id> 或 exec:reviews/result-analysis-<ExpID>/verdict.json#verdict",
         "review_output_sha256": "<sha256-of-normalized-final-reviewer-json>",
         "evidence_refs": ["remote_artifacts/<ExpID>/<RunID>/..."],
         "limitations": [],
         "validation_gaps": []
       }
     ]
   }
   ```

3. 对当前 ExpID 的 `research_workspace` 产物使用 `research-result-commit` 单独提交。分析 CSV 行使用 `git_repo:research_workspace`、`commit_hash:<nested repo commit>`、`refs` 指向 `analysis.md` 和索引。

## 机械验证

在关闭 CSV 前执行：

```bash
python3 .codex/skills/post-run-result-analysis/scripts/validate_result_analysis.py \
  --csv issues/<stem>/<stem>.csv \
  --index issues/<stem>/reviews/result-analysis.json \
  --workdir .
```

验证器必须 fail-closed 检查：

- canonical CSV 中所有已 ingest 的 `(ExpID, RunID)` 均被覆盖，且无重复或额外条目；
- index schema、状态、强模型身份、独立性和模型证据完整（Pi 通道为 parent-session 记录，codex-exec 通道为 verdict 文件 + 事件流模型）；
- 每个 entry 的 reviewer 证据可定位到真实评审输出：Pi 通道解析 `session:<uuid>#tool:<id>` 并核对 `scientific-reviewer`、实际模型、退出码 0、输出 SHA-256；codex-exec 通道解析 `exec:<path>#verdict` 并核对 verdict schema、事件流观测模型精确匹配、`review_output_sha256` 一致；两种通道都要求 `analysis.md` 内容来自该输出；
- analysis 文件存在、在工作区内、四段顺序正确且 SHA-256 一致；
- evidence refs 可解析到工作区内的文件/目录；
- scientific outcome 属于固定枚举；
- `status=not_applicable` 只能在没有已 ingest 正式结果且有明确 reason 时使用。

验证通过后，才可把 `RESULT-ANALYSIS-01` 的四状态置为完成；随后才进入 `REVIEW-*`。closing review 必须消费该索引和 analysis 文件，但不能代替本阶段。
