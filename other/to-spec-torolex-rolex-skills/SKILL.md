---
name: to-spec
description: 把当前对话变成一份 spec，并发布到项目的 issue tracker：不做访谈，只综合你们已经讨论过的内容。
disable-model-invocation: true
---

本 skill 结合当前对话上下文与对代码库的理解，产出一份 spec。不要访谈用户；只综合你已经知道的信息。

issue tracker 和 triage label 的词汇应该已经提供给你了。如果没有，让用户运行 `/setup-rolex-skills`。

## 流程

1. 如果你还没探索过仓库，先探索一遍，理解代码库的当前状态。在整个 spec 中使用项目的 domain glossary 词汇，并尊重你所触及区域内的任何 ADR。

2. 勾勒出你准备测试该功能的 seam。优先使用已有的 seam，而不是新建 seam。尽可能使用最高层级的 seam。如果需要新建 seam，尽量在你能做到的最高点提出。整个代码库中的 seam 越少越好——理想数量是一个。

   与用户确认这些 seam 符合他们的预期。

3. 使用下面的模板编写 spec，然后发布到项目的 issue tracker。应用 `ready-for-agent` triage label——无需额外的 triage。

<spec-template>

## Problem Statement

用户所面临的问题，从用户的角度出发。

## Solution

问题的解决方案，从用户的角度出发。

## User Stories

一份非常长的、带编号的 user stories 列表。每条 user story 都应符合以下格式：

1. 作为 <角色>，我想 <功能>，以便 <收益>

<user-story-example>
1. 作为移动银行客户，我想查看我账户上的余额，以便我能更明智地做出消费决策
</user-story-example>

这份 user stories 列表应当极其详尽，覆盖该功能的方方面面。

## Implementation Decisions

已做出的实现决策列表。可以包括：

- 将要构建/修改的 modules
- 这些 modules 将要修改的 interfaces
- 来自开发者的技术澄清
- 架构决策
- Schema 变更
- API contracts
- 具体的交互

不要包含具体的文件路径或代码片段，它们可能很快就会过时。

例外：如果 prototype 产出了一个比文字更能精确表达某个决策的片段（state machine、reducer、schema、type shape），把它内联到相关决策中，并简要注明它来自 prototype。只保留决策密集的部分，不是可运行的 demo，只是其中重要的片段。

## Testing Decisions

已做出的测试决策列表。包括：

- 什么构成一个好的测试的描述（只测试外部行为，不测试实现细节）
- 将要测试哪些 modules
- 这些测试的先例（即代码库中相似类型的测试）

## Out of Scope

本 spec 范围之外的内容描述。

## Further Notes

关于该功能的任何进一步备注。

</spec-template>
