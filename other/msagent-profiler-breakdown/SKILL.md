---
name: msagent-profiler-breakdown
description: DB格式Profiling数据场景化性能拆解：自动完成场景确认（框架/任务类型判定）、阶段拆解与单次执行边界拆解，并给出报告。Use when 需要对昇腾 Profiling DB 做阶段拆解、step 归因或生成性能报告, or when the user says "帮我按任务阶段拆解这个Profiling数据", "多层次性能耗时拆解", "分析这个 vllm/sglang/verl 数据，主要耗时都花费在哪里了"。
metadata:
  author: MindStudio Agent Team
  category: profiler
  version: 0.1.0
---

# msagent-profiler-breakdown —— 场景化拆解（一步到位）

> 定位：合并原 stage-decompose / step-decompose / breakdown-report 三份 skill，一份搞定
> **阶段归因（level=阶段）→ 单次执行边界（level=单次执行）→ 报告**。
> 场景差异（推理 / 训练 / RL，vllm / sglang / verl / slime…）下沉到场景资源文件
> `resources/scenarios/<scenario>/<framework>.json`，主 skill 不做框架分支。
> 用户只与本文档交互；`scripts/decompose.py` 一步产出 breakdown.json（统一拆解树）/ HTML 报告 / findings。

## 触发与元信息

| 维度    | 内容                                                                                                                                                          |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 触发关键词 | 模型按层拆解、完整性能分析、一键分析、端到端到层内拆解、框架/并行自动识别、多卡 TP/EP/PP 分析                                                                                                        |
| 外部依赖  | 昇腾 Profiling DB（sqlite）与 `analysis.db`；Python 3 标准库；场景资源 `resources/scenarios/`；拆解树契约 `references/breakdown-schema.md`；报告模板 `references/report-template.md` |
| 权限要求  | 只读打开 Profiling DB（`mode=ro`，保留 WAL 恢复）；在工作区读写中间产物与报告                                                                                                        |
| 预期输出  | breakdown.json（统一拆解树：端到端 → 阶段 + 单次执行分支）+ stage.json（同内容别名，场景信息供 layer-decompose 继承）+ HTML 报告 + findings（8 字段）+ 明细 CSV                                       |

## 一句话调用

```
python scripts/decompose.py --db <ascend_pytorch_profiler_{rank_id}.db> \
    [--framework vllm|sglang|verl|slime|megatron|mindspeed|fsdp] \
    [--task-type inference|train|rl] [--anchor "forward"] [--inspect-index 0]
```

**最少必给只有** **`--db`**；framework / task-type 可省，走自动探测 / 兜底默认 / 由编排层询问用户。

## 三步流程

### 第 1 步：场景确认（framework / task-type 判定）

判定优先级（framework 与 task-type 同构）：

1. **CLI / 编排层显式指定**（`--framework` / `--task-type`）→ high。用户可直接说
   「请帮我分析下这个 vllm 的 profiling 数据」，此时 framework 由上层输入。
2. **自动探测**（从 profiling 数据分析）：`STRING_IDS.value` 含 `vllm%` 前缀 → vllm；
   存在 verl worker 侧 MSTX 打点名（`actor_update` / `actor_compute_log_prob` /
   `ref_compute_log_prob` / `train_batch`）→ verl。框架映射任务类型：
   vllm/sglang→inference、megatron/mindspeed/fsdp→train、verl/slime→rl。→ high
3. **识别不了 → 询问用户**（编排层用 AskUserQuestion 回显候选 + 依据让用户确认/修正）；
   仍缺则默认 vllm/inference + 显式告警（`task_type_source=default`），报告低置信度清单列出。

探测工具：`scripts/db_query.py`（子命令 `string` / `mstx` / `pytorch` / `cann` / `api`），
先查打点再定规则。判定结果（`framework` / `framework_source` / `task_type` /
`task_type_source`）写入 `stage.json`，**供下游 layer-decompose 经** **`--framework`** **继承，
无需重新探测**。

### 第 2 步：执行拆解（按场景资源规则）

引擎 `decompose.py` 框架无关，按场景资源文件声明式规则执行，主 skill 不过多呈现框架分支：

- 阶段归因：读取 `resources/scenarios/<scenario>/<framework>.json` 的
  `stage_decompose.stages`（name + scopes + backing），直连 DB 统计每个 stage 的
  count / 累计 / 均值 / 最大 / 最小 / 首个。

- 单次执行边界：读取 `step_decompose.anchor`（默认 `forward`），锚点 scope 每次出现
  记一个 step，按位置（前 2 步 graph\_capture/compile）+ 阈值（wall\_time > factor×median）
  判热身并写 `warmup_reason`；`--skip-first-step` 另标首个 step 为疑似 prefill；
  剔除后算稳态统计（count/mean/P50/P99/min/max/variance/CV）。

- 锚点优先级：CLI `--anchor` 显式覆盖 > 场景资源 `step_decompose.anchor`；锚点为空
  （如 RL/训练待核验）→ 跳过 step 拆解并告警。

新增框架 = 在场景目录放一个 `<framework>.json`（支持 `extends` 继承父规则），不改引擎，
详见 `references/frameworks/README.md`。

### 第 3 步：生成报告（模板即资源，无独立 report skill）

按 `references/report-template.md` 组织结论先行 HTML（自包含、无 JS 依赖）：
一句话结论 → 逐级耗时（仅列出现过的级别）→ 阶段统计表 → TOP-N 下钻链 → per-step 明细 →
稳态统计 → 异常/漂移 → 低置信度清单 → 建议下一步 → findings（8 字段）。
场景信息（框架/任务类型，用户已知）与守恒自检不做独立章节，守恒缺口告警保留在 findings 中。
同时落盘 findings JSON 与明细 CSV；多 run A/B 对比用 `scripts/compare_runs.py`。

## 输入

| 输入              | 必填 | 来源                                                          |
| --------------- | -- | ----------------------------------------------------------- |
| 昇腾 Profiling DB | 是  | 用户给定路径（`ascend_pytorch_profiler_{rank}.db` / `analysis.db`） |
| framework       | 否  | 场景确认（CLI > 自动探测 > 询问 > 默认 vllm + 告警）                        |
| task-type       | 否  | 场景确认（CLI > 框架映射 > 默认 inference + 告警）                        |
| anchor          | 否  | 覆盖 step 边界锚点（默认取场景资源 `step_decompose.anchor`）               |

## 输出（workspace 落盘）

| 产物                                             | 内容                                                                          |
| ---------------------------------------------- | --------------------------------------------------------------------------- |
| `breakdown.json`                               | 统一拆解树：端到端（会话）→ children（阶段... + 单次执行分支含 per-step 序列与稳态统计）+ 框架/任务类型来源 + 守恒自检 |
| `stage.json`                                   | 与 breakdown.json 同内容别名；场景信息供 layer-decompose `--framework` 继承               |
| `<prefix>.html`                                | 结论先行报告（模板见 `references/report-template.md`）                                 |
| `<prefix>_findings.json`                       | 结构化结论（8 字段：问题/证据/影响/根因/优化动作/预期收益/验证路径/置信度）                                  |
| `<prefix>_detail.csv` / `<prefix>_handoff.csv` | per-step 明细 / 层拆解交接清单（暂缓期间为占位）                                              |

## 涉及的 skill

| skill                      | 职责                         | 状态                       |
| -------------------------- | -------------------------- | ------------------------ |
| msagent-profiler-breakdown | 场景确认 + 阶段/单次执行拆解 + 报告，一步到位 | 在链路内                     |
| layer-decompose            | 单层归属 + 层内归因 + 结构校验（直连 DB）  | 暂缓保留（经 --framework 继承场景） |

