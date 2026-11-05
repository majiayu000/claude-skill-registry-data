---
name: concept-design-cn
description: "仅在显式调用时，用 Daniel Jackson 的概念与同步方法设计、写规格、实现、审查、重构或解释软件。将功能放进独立模块，将协作写成明确规则，让软件更模块化、行为更透明、更容易理解与修改。支持 CONCEPT.md/SYNCS.md 结构检查与 Mermaid 关系图。"
metadata:
  language: zh-CN
  translation_of: concept-design
  version: "2.0.1"
---

# 概念设计：模块独立，协作清楚

先定义有用行为，再选择实现。

本技能借鉴 **WYSIWID**（Meng 与 Jackson，MIT）的概念与同步方法。

软件结构应直接表达用户可观察的行为。
概念定义独立功能，同步规则定义概念之间的协作。
理解或修改一项行为时，应能找到对应的概念与规则。

## 从需要出发

- 明确受益者及其需要的可观察结果。
- 概念为一个目的提供独立行为。
- 状态与动作定义允许的行为。
- 运作原理（OP）用一段代表性历史说明行为如何达成目的。
- OP 不覆盖全部行为，也不保证进展。
- 每个概念实例拥有自己的状态。
- 概念 MUST NOT 互调或互读状态。
- 外部身份不假定另一概念的字段。
- 应用协调放在概念之外的同步规则中。
- 组合 MAY 限制行为，但 MUST 保持各概念契约。

## 检验论证

- 说明主张、证据及其所需前提。
- 寻找能使主张不成立的场景。
- 比较备选，包含不改。
- 多次修复在同一前提下失败时，重新检验该前提。
- 检查契约能否支持 OP。
- 检查 OP 能否达成目的。
- 应用场景与概念正确性分别检查。
- 所需时限、失败与一致性前提须明确。
- 缺少的决定保留未决；未执行的测试保留未验证。

## 每项决定只定义一次

- 区分 `confirmed`（已确认）、`proposed`（建议）、`inferred`（推断）、`open`（未决）。
- 建议或推断 MUST NOT 经转录变成确认需求。
- 每个模型元素只有一处权威定义。
- 沿用已确认决定，直到需求或证据支持重新评估。
- 增加机制前，检查能否删除规则或职责而保持所需行为。
- 重构保持行为，有意重新设计须另行说明。

## 选择工作

以下为提示词选择器，不是已安装的 shell 命令：

```text
$concept-design-cn [design|settle|prd|build|review|guard|refine|explain] [范围与请求]
$concept-design-cn guard [audit|concept|drift|pipeline|sync|map] [范围]
```

未指明模式时按请求判断。
意图不清时先只读检查，再询问阻碍工作的取舍。
只读当前工作所需流程。
跨模式沿用已有授权。

| 模式 | 按需读取 | 产出 |
| --- | --- | --- |
| `design` | [设计](references/design.md) | 概念、组合与决策 |
| `settle` | [整理](references/settle.md) | 带确认状态的讨论结论 |
| `prd` | [规格](references/prd.md) | 记录确认模型与验收 |
| `build` | [实现](references/build.md) | 范围内实现、结构审查或重构 |
| `review` | [审查](references/review.md) | 带证据的只读发现 |
| `guard` | [维护](references/guard/workflow.md) | 覆盖、回填、漂移、管道或概念与同步关系图 |
| `refine` | [精炼](references/refine.md) | 修正建议或授权修复 |
| `explain` | [图解](references/explain/workflow.md) | 有源码依据的行为解释 |

审查、审计、漂移和仅规划请求 MUST 保持只读。
其他模式只在本次范围内写入。
回填 MUST 区分观察行为、推断目的、缺陷与确认需求。
MUST NOT 改规格掩盖代码缺陷。

## 规格与检查

图 MUST 使用 Markdown 中的 Mermaid 代码块。
编写或比较规格时使用 [CONCEPT/SYNCS 格式](references/spec-format.md)。

```sh
python3 <技能目录>/scripts/concept_lint.py <CONCEPT.md或SYNCS.md> [其他文件] --json
```

语法结果不证明目的达成、契约符合性或运行时正确性。
[来源与本地约定](references/sources.md)。
