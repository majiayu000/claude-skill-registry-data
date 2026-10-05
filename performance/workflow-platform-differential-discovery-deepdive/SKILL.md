---
name: workflow-platform-differential-discovery-deepdive
description: Use when 深钻已选定的单个用例，贯通性能、JIT、ISA/微架构证据并验证优化价值。
---

# Platform Differential Discovery Deepdive Workflow

## 定位

按用例深钻的端到端剧本。输入是单个用例（来自粗筛 `workflow-platform-differential-discovery` 的候选用例清单，或用户直指），产物是单用例证据表 + 备选优化项。与粗筛 workflow 是流水线关系但相互独立——用户也可跳过粗筛直接指一个用例深钻。

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | 对应用户流程步骤 | Agent | 技能 | Gate |
|------|-----------------|-------|------|------|
| 0 选例 | ① 先钻哪个用例 | `cinderx-orchestrator` | 读粗筛清单或用户直指 | 用例已锁定，实验轴齐全 |
| 1 环境确认 | — | `cinderx-environment-verifier` | `cinderx-env-validate` | 双平台环境可复用 |
| E1 性能基线 | ② 总性能数据 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` | 差距 > 噪声带，置信区间不含 0 |
| E2 用例画像 | ③ 用例内容 + autojit 函数形状 | `cinderx-jit-analyst` | `cinderx-hir-lir-analyze` | 函数形状与 perf 热点吻合 |
| E3 HIR 分布 | ④ HIR 分布 | `cinderx-jit-analyst` | `cinderx-hir-dump`、`cinderx-hir-lir-analyze` | 差异点定位到节点级 |
| E4 LIR + wall clock | ⑤ LIR 分析，含调用数与 wall clock | `cinderx-jit-analyst` | `cinderx-hir-lir-analyze` | wall clock 拆解与 LIR 段对齐 |
| E5 差异点 | ⑥ 差异点（bb 级或单条机器码级） | `cinderx-jit-analyst` | `cinderx-hir-lir-analyze` | 双平台指令逐条对齐，差异序列可枚举 |
| E6 根因下钻 | ⑦ 拆解根因到 ISA/指令集/微架构/硬件 | `cinderx-evidence-analyst` | `cinderx-evidence-table`、`cinderx-isa-microarch-compare` | 根因落到 ISA/微架构/硬件，证据闭环（含采样可用性探测） |
| E7 优化方向 | ⑧ 优化方向 | `cinderx-evidence-analyst` | `cinderx-evidence-table` | 策略 ↔ 根因一一对应 |
| E8 穿刺（跑） | ⑨ 穿刺 | `cinderx-orchestrator` → `pyperformance-candidate-runner` | `cinderx-ab-run-slot`、`pyperformance-worker-run` | 隔离满足、可重复 |
| E8 穿刺（判读） | ⑨ 穿刺数据可信度 | `cinderx-evidence-analyst` | `cinderx-evidence-table` | 收益落噪声带外，证据表签发可信度 |
| E9 优化价值 | ⑩ 备选优化项 | `cinderx-evidence-analyst` | `cinderx-evidence-table`、`cinderx-optimization-report` | 收益/成本均有数据支撑 |

## Gate

E1–E5 是证据采集（贴事实），E6–E9 是收口判读（下判断），分界线在 E6。阶段 Gate 不满足时，补齐证据再作依赖它的判断；独立证据可继续采集，不因缺口暂停整个任务：

- evidence-analyst 在 E6 接手时拿到 E1–E5 证据，填入证据表前 5 段（或标记 `evidence_gap` 要求补），再推进 E6–E9。
- evidence-analyst 在 E6 有权回退要求 E3–E5 补证据（如指令没对齐回到 E5）。
- E8 分别记录穿刺跑分与可信度判读；可以由同一 Agent 顺序完成，但不能用已执行跑分替代隔离、可重复性和噪声判断。

有了足够深层的根因（E6），才不被表面原因迷惑；有了优化方向（E7），才进入穿刺（E8）；穿刺数据可信，才判定优化价值（E9），产出最终备选优化项。
