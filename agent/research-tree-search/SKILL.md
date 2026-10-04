---
name: research-tree-search
description: 树状搜索科研迭代与三轮审查编排。多分支探索 idea/方法/模块/参数变体→执行实验→评分→剪枝→深化；编排三轮连带审查（拆子问题→分派→合并→收敛判定）。触发词：树状搜索、分支实验、迭代搜索、换模块跑迭代、三轮审查、tree search、研究迭代。
metadata:
  short-description: 树状搜索迭代实验 + 三轮连带审查编排。
---

# 树状搜索科研迭代（research-tree-search）

把 AI-Scientist-v2 的 agentic tree search 方法论转写为 Codex 内工作流：**分支生成 → 实验执行 → 评分 → 剪枝 → 深化 → 落账**。Codex 是执行体，当前模型是大脑，`.research/` 是记忆。

## 一轮搜索协议

1. **读上下文**：读取 `.research/`（台账）、用户提供的基线、数据集、想尝试的变体清单。
2. **分支生成**：基于基线生成 3–5 个候选变体（方法/模块/超参方向的组合），每个分支写明：假设、改动点、预期收益、风险、预估成本。写入 `kg.md` 的树结构。
3. **实验执行**：每个分支生成独立实验脚本（优先复用 pytorch-lightning / transformers / scikit-learn / arbor 的执行模式），运行并记录结果到 research-ledger（experiments/）。
4. **评分**：用统一评分脚本：相对基线的提升（主指标）、稳定性（多次运行方差/多个 seed）、成本（时间/显存/参数量）。评分写入矩阵。
5. **剪枝**：明确剪掉的分支保留记录与原因（不删除，便于回溯）；保留高分分支。
6. **深化**：对保留下来的分支生成子变体（≤3 轮/篇），回到步骤 2。
7. **收敛**：当 ① 无分支再产生显著提升 ② 达到轮次上限 ③ 用户叫停，输出最优分支的实验报告，供 S9 写作使用。

## 评分与剪枝规则

- 主指标相对提升 < 阈值（默认 1%，可配置）且无稳定性/效率收益 → 剪枝；
- 结果异常（分数突变、loss NaN、复现失败）→ 标记 failed 并排查，不当作有效分支；
- 每个分支的结果必须可复现（记录 seed、环境、命令）。

## 三轮连带审查编排（S12）

1. **第 1 轮**：academic-research-suite(academic-paper-reviewer) 完整审查（多视角、可拆子问题：按 Originality/Methodology/Evidence/Coherence/Writing 维度拆分）；输出 P1/P2 问题清单与修订路线图。
2. **修订**：按问题清单修订（academic-paper），在 claims.md 记录每条的回应。
3. **第 2 轮**：re-review 模式（验证修订是否回应问题，生成 traceability matrix）；未通过维度继续修订。
4. **第 3 轮**：终检（P1=0、P2 低于阈值，或用户确认接受残余问题）；随后生成返修材料（回复信、cover letter、标红稿）。
5. 每轮结束把审查记录写入 `.research/reviews/`。

## 边界

- 本技能负责"决定试什么"（协调层）；执行与验证可交给 experiment-agent / arbor（执行层）；不重复实现 arbor 的 held-out 优化循环，S7 参数优化默认走 arbor。
- 实验必须真实运行；禁止用"看似合理"的虚构结果替代（对照 academic-workbench 诚信红线）。
