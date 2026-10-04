---
name: light-experiment-coding
description: >-
  Light 科研主线 stage 6：把冻结的 question/estimand、experiment matrix、pre-registration 与 data lineage
  落成最小可运行、测试先行、无泄漏、可复现且能交给 result-analysis 的实验代码。用于实现或复现训练/预处理/评测，
  设计 gold/property/metamorphic 测试，控制 Python/NumPy/框架/CUDA/DataLoader 随机性，审查 train/test 或 CV fit
  穿越，记录 config/code/environment/input hashes、stdout/stderr、raw metrics、patient/entity predictions 与 failure
  artifacts，以及运行 stage-6 checkpoint。数据泄漏或不可复现是 critical；静态扫描和同 seed 两次一致都不证明跨硬件
  绝对复现。
metadata:
  version: 2.2.0-round3
  truth_source: ../../docs/competitors/experiment-coding.md
  resource_map: references/experiment-coding-resource-map.md
  engine: scripts/experiment_execution_contract.py · scripts/repro_gate.py · scripts/seed_audit.py · scripts/review_gate.py · scripts/run_artifact_check.py
  emits: light.findings.v1 · light.run_manifest.v3 · raw run bundles
  consumes: research-plan frozen plan/preregistration/failure-tree report · data-engineering lineage/split_leakage · result-analysis raw-run contract
  stage: 6
---

# 实验编码（stage 6）

任务不是“写出能跑的 notebook”，而是把上游冻结计划逐行实现成**可证伪、可复跑、可审计**的实验。优先级：

1. 不改研究问题；
2. 不让评估信息进入训练；
3. 能用固定环境与 seed 真复跑；
4. 保留足够 raw evidence，让 result-analysis 自己重算；
5. 代码整洁和速度服从以上约束。

先完整阅读 [`references/experiment-coding-resource-map.md`](references/experiment-coding-resource-map.md)。工具机制见
[`references/tools.md`](references/tools.md)，TDD/调试红旗见
[`references/tdd_redflags.md`](references/tdd_redflags.md) 与
[`references/debug_protocol.md`](references/debug_protocol.md)。

## 入口：冻结输入

开始写码前读取并 hash：

- question / estimand；
- experiment matrix 每一行和 fair-comparison 常量；
- pre-registration 及 provenance；
- failure-tree report：每条 hypothesis 的 success/failure/inconclusive 分支、guardrail/counter-metric、kill criterion 与 amendment policy；
- data fixed revision、raw/curated SHA256、lineage、split ID、`split_leakage` evidence；
- result-analysis 对 raw run、predictions、metrics、failures、provenance 的消费契约；
- 当前 git commit 与 dirty state。

primary outcome、comparison family、exclusion、stopping 已冻结。若实现证明计划不可行，带最小复现和影响返回
research-plan，停下让人决策；不得改 config 默认值静默漂移。

## 实现顺序

### 1. 建立最小可运行项目

优先复制 [`assets/project-scaffold/`](assets/project-scaffold/)：

- `uv.lock` + `pyproject.toml`：`uv sync --locked --extra dev`；
- `configs/experiment.schema.json`：每个 matrix row 的机读配置；
- `experiment_contracts.py`：data/model/metric/preprocessing 最小接口；
- `reproducibility.py`：运行期 seed helper；
- CI/pre-commit/debug 资产。

遵循现有仓库框架和配置格式；不要为一个实验引入付费 IDE、云追踪或私有 key。MLflow/DVC 可选，普通本地文件必须能完成
核心闭环。不可用资源明确写 `UNAVAILABLE:原因`，不假装通过。

### 2. 测试先行

在实现 preprocessing/train/eval 前：

1. 写 gold test，验证人工可算的小答案；
2. 写 property test（Hypothesis），验证范围、有限性、对称/单调等不变量；
3. 写 metamorphic test，验证置换/等价变换后的输出关系；
4. 写 train-only-fit 测试，记录 transformer 只收到训练折；
5. 亲眼看新测试因缺实现或真实 bug 失败，再写最小实现使其通过。

浮点断言用 `pytest.approx` / `assert_allclose(rtol, atol)`。先声明 device、dtype、mixed precision 和容差；NaN/Inf
默认 fail。不要测“随机训练一定达到某个漂亮数”，测确定性边界和可重算事实。

### 3. 防泄漏实现

- holdout：先 split，再仅用 train `fit/fit_transform`，test 只 `transform`；
- CV/调参：预处理器与模型放进 sklearn `Pipeline`，每折只 fit training fold；
- 患者/用户/牧场等实体用 group-aware split，不得跨 train/test；
- 目标编码、特征选择、PCA、imputation 同样只在训练折 fit；
- 数据件复核直接复用 data-engineering `split_leakage`，不重造。

`review_gate` 只识别静态形态，会漏/误报；领域语义仍要人工核对。指标异常好，先查 leakage。

### 4. 控制随机性与数值边界

分开两个目的：

- `fixed_repro`：固定一个 seed，在同代码/data/config/environment 下做两次独立运行；
- `randomness_estimation`：按预注册 seed 列表做多次运行，估计算法随机性。

多 seeds 不是患者/实体样本量，绝不拿 seed 数替代功效分析 n。

按实际使用覆盖 `PYTHONHASHSEED`（当前进程须启动前设）、`random`、NumPy、框架 RNG、CUDA、cuDNN、
deterministic algorithms、DataLoader generator/worker。记录 device/dtype/AMP、线程数、worker 数、排序键和已知
非确定算子。换 seed 应可变但可追溯；同 seed 一致也只支持同环境契约，不外推跨 release/platform/hardware bitwise 保证。

### 5. 每个 run 保留 raw bundle

从 [`templates/run_manifest.template.json`](templates/run_manifest.template.json) 生成
`light.run_manifest.v3`；说明见 [`templates/run_manifest.md`](templates/run_manifest.md)。
`termination` 只说明进程为何停止，`completion` 才记录矩阵行 oracle 是否真的通过；
timeout / max iterations / cancel 一律不得冒充完成。

每个 matrix row × config × seed × attempt 独立目录，至少保存：

- config schema 校验后的快照；
- code commit/dirty/diff 与代码文件 hash；
- data/input SHA256、source revision、split ID；
- environment（Python/包/OS/CPU/GPU/CUDA/线程）；
- argv 数组、stdout、stderr、exit code；
- 每折/每实体 raw metrics、patient/entity-level predictions；
- test evidence；
- failed run 的 failure artifact。

失败 run 不删除，不覆盖成成功。禁止只交 summary CSV；result-analysis 必须能从 raw evidence 重算。

## 门控与 checkpoint

按此顺序真跑并记录 exit code：

```bash
python scripts/experiment_execution_contract.py --spec experiment_execution_contract.json \
  --report execution_contract_findings.json --json-out execution_contract_report.json
python scripts/review_gate.py src/ --json
python scripts/seed_audit.py src/train.py src/reproducibility.py
python scripts/repro_gate.py --spec repro_spec.json --report repro_findings.json
python scripts/run_artifact_check.py --manifest runs/EXP-01/run-a/manifest.json
python scripts/run_artifact_check.py --compare \
  runs/EXP-01/run-a/manifest.json runs/EXP-01/run-b/manifest.json
python ../light-orchestrator/scripts/run_checkpoint.py \
  --file .light/passport.yaml --stage 6 --findings repro_findings.json --write --ts <ISO-8601>
```

`experiment_execution_contract.py` 消费 `light.experiment_execution_contract.v1`（模板见 [`templates/experiment-execution-contract.example.json`](templates/experiment-execution-contract.example.json)，故意 fail-closed）：核 `as_of`、frozen scope/evaluator/budget、failure-tree handoff、matrix/DAG、run status/termination/failure class、partial checkpoint/resume command、环境与 cache provenance、repro level 分层、远程/付费执行授权。**timeout/OOM/preempted/max-iterations 不得写 completed**；`frozen_at` 与远程授权 `approved_at` 不得来自未来；`decision=NOT_READY/UNKNOWN` 本身阻断推进；run 必须绑定冻结 `matrix_rows` 中的 row，且每个 row 必须绑定 `failure_tree_refs`（hypothesis_ids、branch_action_ids、适用的 guardrail_ids）；新增实验行要先回 research-plan 修订；completed run 若上游要求 guardrail，`completion` 必须留下 `guardrail_evidence_artifacts`，否则不得交 result-analysis；实际 walltime/cost/compute_units 与远程预计成本不得静默超过冻结预算，超限必须有预算覆盖授权；`PARTIAL/RESUMABLE` 必须有 checkpoint SHA 和 resume command；请求 `CLEAN_ENV_RERUN/CROSS_PLATFORM/INDEPENDENT_REIMPLEMENTATION` 必须有对应证据；远程/付费/HPC 运行在 `user_authorization=APPROVED` 前不得 `RUN_READY`。

stage 6 的 canonical critical 只有：

- `leakage`；
- `reproducible`。

float/security 在研究 checkpoint 按 spec 为 warn；`review_gate` 可作为独立交付阻断门，不得借此扩大 checkpoint critical 面。
stage-6 门失败就在本阶段修，**不伪造 `ROUTES[6]` 出边**。

同固定 seed 两次必须是独立 run dir；`run_artifact_check.py` 先核 matrix/config/env/code/input 身份和
`started_at/ended_at` 时间轴（带时区、不倒序、不来自未来），再比较 predictions/raw_metrics hashes。
静态 seed/leakage 门 + 同 seed pair 都通过，仍只是一组有边界的证据。

## 交 result-analysis 与 7→6

交付全部 completed/failed runs、coverage、manifests、predictions、raw metrics、logs、test evidence 和 canonical findings。
不要在 stage 6 替 result-analysis 选择性丢 run 或先写结论。

只有 result-analysis 产出**真实实现 bug 或不可复现 root cause**时，orchestrator 才可：

```bash
python ../light-orchestrator/scripts/reroute.py \
  --findings result_findings.json --stage 7 --passport .light/passport.yaml
```

reroute 只给建议。**落 7→6 back-edge 前停下，让用户拍板**；用户确认后才调用 passport `add-back-edge`，并带回失败命令、
期望 vs 实得、artifact pointers 修根因。统计不显著、效果小、计划不可行不自动等于实现 bug。

## 不可协商

1. 不在全量数据上 fit scaler/encoder/imputer/PCA/feature selector 后再 split/CV。
2. 不只设一个框架 seed 就声称可复现。
3. 不用浮点 `==` 断言，不静默吞 NaN/Inf。
4. 不把固定 seed 与多 seeds 的科学目的混在一起。
5. 不删失败 run，不只留汇总数，不缺 stdout/stderr/predictions/raw metrics/provenance。
6. 不把静态扫描写成“证明无泄漏”，不把同 seed 两次一致写成“跨硬件绝对复现”。
7. 不改冻结研究设计；不可行就回 research-plan 让人决策。
8. 不由 stage 6 自己制造出边；7→6 只由下游真实 root cause 建议，且用户批准后才落边。

## 完成判据

- [ ] 每个 matrix row 有 schema-valid config 和稳定 run ID；
- [ ] 跑过 `experiment_execution_contract.py` 吗？scope/evaluator/budget、DAG、run status、failure class、resume、资源成本、repro level 和远程授权都闭合了吗？
- [ ] execution contract 是否绑定 `.light/failure_tree_report.json` 的 locator/hash/status？每个 matrix row 是否有 failure_tree_refs？completed run 是否留了 guardrail evidence？
- [ ] `as_of`、`frozen_at`、远程 `approved_at`、run `started_at/ended_at` 都是真实已发生时间吗？没有未来预填或结束早于开始吧？
- [ ] run 的 `matrix_row_id` 是否来自冻结 experiment matrix？实际 walltime/cost/compute_units 或远程预计成本超预算时，有预算覆盖授权吗？
- [ ] gold/property/metamorphic/train-only-fit 测试先红后绿；
- [ ] lock、接口、device/dtype/AMP/NaN/Inf/容差边界明确；
- [ ] review/seed/repro 门与 stage-6 checkpoint 通过；
- [ ] 固定同 seed 两次 predictions/raw_metrics hashes 一致；
- [ ] 换 seed 的变化有 manifest 可追溯；
- [ ] 每个 run 的 config/env/code/input/log/raw metric/prediction/failure evidence 齐全且 hash 可验；
- [ ] result-analysis 能只凭 bundle 消费，未发生 plan drift 或未授权 back-edge。

## 名实对齐

TDD、seed、安全扫描、复现实验都不是 Light 独有。R1 真同类已普遍具备 config-first、smoke、immutable run、
lineage 与 keep/discard。这里的实际增量是：

1. 代码级 holdout/CV leakage；
2. 框架感知 seed audit；
3. 复用数据件 `split_leakage`；
4. frozen execution contract（scope/evaluator/budget/DAG/status/resume/repro level/remote authorization）；
   Round 3 再补 run→冻结 matrix row 身份绑定与实际/预计资源成本预算超限门，防止新实验行或付费扩跑绕过上游批准；
   Round 3 续补 failure-tree handoff 与 guardrail evidence，让 research-plan 的失败/无结论/kill criterion 不在执行端丢失；
5. hash-verified raw run bundle + same-seed pair；
6. canonical findings/stage-6 checkpoint + 受用户控制的 7→6。

诚实落后项：没有 MLflow 式查询 UI、DVC remote、GPU scheduler、仓库语义索引或自主 experiment search；静态门仍有边界。
