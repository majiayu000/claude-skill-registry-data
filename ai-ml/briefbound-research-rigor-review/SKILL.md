---
name: briefbound-research-rigor-review
description: "Use when an AI/ML research result, baseline promotion, ablation conclusion, benchmark claim, paper claim, surprising finding, or high-cost next experiment needs an evidence-focused rigor review before it is accepted, generalized, published, or used to redirect the research program."
license: MIT
---

# 研究严谨性审查

## 目标

判断“现有证据到底允许我们说什么”，防止偶然涨分、评价泄漏、错误归因或过度外推进入 active baseline 和正式 claim。

本 skill 是关键结论的 gate，不是每条实验 lane 的固定尾声。普通候选由 `briefbound-score-loop` 自行 gate；只有结论将影响研究方向、论文、发布或高成本投入时才触发。

## Briefbound task contract

- Context Boundary: 待审结论、研究问题、baseline、实验协议、数据与 split、对照/消融、重复结果、artifact 和适用范围。
- Output Contract: 按证据排序的 findings、允许表述、缺失证据、严谨性判定和最小补强动作。
- Allowed Action: 只读审查证据并运行必要的低风险复核；未经授权不修改研究代码、metric、数据或 claim 来源。
- Success Evidence: 可定位的命令、结果、表格、diff/config、统计信息、对照、复现记录和来源映射。
- Stop Condition: 关键 artifact 缺失、baseline/协议无法确认、数据泄漏或评价漂移未排除、结果不可复现，或结论与证据对象不一致。
- Route Out: 返回 `briefbound-ai-research-loop`、返回 `briefbound-score-loop` 补实验、路由确定性 bug owner、限定/接受结论，或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准，末行 `下一步建议: <一个具体动作>`，且限于决策类建议（推荐方向、优先级或需用户拍板的选项），不把可自行完成的执行步骤包装成建议交回。

## 触发闸门

满足任一条件才进行完整审查：

- 候选将成为重要 best-known 结果、改变研究方向，或晋升依据超出普通 score gate；
- 结论准备进入论文、报告、README、发布说明或对外宣传；
- 结果反直觉、与先验冲突或将触发研究方向转向；
- 下一步需要显著更多算力、数据、人工或外部提交机会；
- 用户明确要求科研审查、证据审计或 claim 校准。

单次普通失败、低成本 smoke 或尚未形成结论的探索只做局部检查，不输出完整矩阵。

## 审查方法

先写出一个可审查句子：

```text
在 <数据/协议/范围> 下，<候选> 相比 <baseline> 产生 <观测>，因此支持 <最窄解释>。
```

然后只检查与当前 claim 有关的维度：

1. **证据相关性**：metric 和实验是否直接测量 claim，还是只使用 proxy。
2. **可证伪性**：是否存在能推翻解释的对照、消融或结果；失败条件是否预先明确。
3. **范围校准**：结论是否超出数据、seed、模型规模、任务、硬件或评价协议。
4. **归因一致性**：一个主要机制是否被隔离；是否混入数据、参数量、训练预算或实现差异。
5. **探索完整性**：负结果、异常值和冲突证据是否被保留；是否只报告赢家。
6. **方法严谨性**：baseline、split、泄漏、重复、方差、统计、复现和 artifact 是否足以支持风险等级。

无需机械输出六项。没有 finding 的维度一句结论即可；有问题时给出精确证据和影响。

## 严重度与判定

Findings 按影响排序：

- `P0 BLOCKER`：证据无效或不可定位，例如泄漏、错误 metric、错误 baseline、结果无法复现。
- `P1 MAJOR`：会改变 claim 或方向，例如缺关键对照、混杂变量、强 seed/split 敏感。
- `P2 LIMITATION`：结论仍可保留但必须限定范围或降低置信度。
- `P3 IMPROVEMENT`：不会改变当前结论的可选增强。

最终只给一个 verdict：

- `ACCEPT`：证据足以支持当前窄 claim；
- `QUALIFY`：保留结论，但必须收窄表述或明确限制；
- `REJECT`：当前证据不支持该解释或晋升；
- `BLOCKED`：缺少决定性 artifact，无法审查。

审查不以“测试通过”替代研究证据，也不因一个指标上涨默认 `ACCEPT`。

## 最小补强原则

发现缺口后，只推荐最能改变 verdict 的动作：

- 一个负对照或关键消融；
- 一个独立 seed/split/规模复现；
- baseline 与候选的协议一致性检查；
- 重新解析原始 artifact；
- 将 claim 收窄到已有证据真正覆盖的范围。

多个修复互相独立且当前契约允许时，可按依赖顺序连续完成，不要求用户逐项确认。超出写入范围时返回研究 owner 重新规划。

## 输出

用户可见输出默认中文，采用 code review 式 findings-first：

```text
审查结论: ACCEPT / QUALIFY / REJECT / BLOCKED
关键发现:
- [P级] 发现、证据、对结论的影响
允许表述:
缺失证据:
最小补强动作:
路由出口:
```

没有实质 finding 时明确说明“未发现会改变结论的问题”，并列出剩余不确定性。正文末尾输出：`下一步建议: <一个具体动作>`，限于推荐方向、优先级或需用户拍板的选项。
