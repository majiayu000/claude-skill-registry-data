---
name: to-tickets
description: 将计划、spec 或当前对话拆解为一组 tracer bullet tickets，每张 ticket 声明其 blocking edges，并发布到已配置的 tracker（本地以每张 ticket 一个文件用文本记录 edges，或在真实 tracker 上使用原生 blocking 链接）。
disable-model-invocation: true
---

# To Tickets

将计划、spec 或对话拆解为一组 **tickets**：tracer bullet 式的 vertical slices，每张 ticket 声明**阻塞**它的那些 tickets。

issue tracker 与 triage label 词汇应该已经提供给你。若没有，让用户运行 `/setup-rolex-skills`。

## 流程

### 1. 收集上下文

从对话上下文中已有的内容入手。如果用户把某个引用（spec 路径、issue 编号或 URL）作为参数传入，就去获取它，并通读其完整正文与评论。

### 2. 探索代码库（可选）

如果你尚未探索过代码库，先这样做，以了解代码当前的状态。ticket 标题与描述应使用项目的 domain glossary 词汇，并尊重你将要改动区域内的 ADRs。

留意是否有机会 prefactor 代码，让实现变得更容易。"先把变更变容易，再去做那个容易的变更。"

### 3. 起草 vertical slices

把工作拆解为 **tracer bullet** tickets。

<vertical-slice-rules>

- 每个 slice 都要切出一条窄但**完整**贯穿每一层（schema、API、UI、tests）的路径：是 vertical，而不是某一层的 horizontal slice
- 完成的 slice 可以独立 demo 或独立验证
- 每个 slice 的大小以能放进一个全新的 context window 为准
- 任何 prefactoring 都应先做

</vertical-slice-rules>

为每张 ticket 给出其 **blocking edges**：在它开始之前必须先完成的其他 tickets。没有 blocker 的 ticket 可以立即开始。

**Wide refactor 是 vertical slicing 的例外。** **wide refactor** 是单一机械变更（重命名一列、重写某个共享符号的类型），其 **blast radius** 波及整个代码库，一次编辑就会同时破坏成千上万个调用点，没有任何 vertical slice 能保持 green。别硬把它塞进 tracer bullet；把它编排成 **expand–contract** 序列。先 expand：在旧形式旁加入新形式，这样什么都不破坏。然后按 blast radius 决定批量大小（按 package、按 directory）将调用点迁移过来，每批都是各自的 ticket、被 expand 阻塞，由于旧形式仍然存在，CI 得以一批接一批保持 green。最后 contract：当不再有调用者时删除旧形式，用一个被所有 migrate 批次阻塞的 ticket 完成。当即便批次本身也无法单独保持 green 时，保留这个序列，但让它们共享一个 integration branch，并让它们共同阻塞一个最终的 integrate-and-verify ticket；green 只在那里被承诺。

### 4. 追问用户

把提议的拆解方案以编号列表呈现。对每张 ticket，展示：

- **Title**：简短描述性的名称
- **Blocked by**：哪些其他 tickets（如果有）必须先完成
- **What it delivers**：这张 ticket 使哪些端到端行为生效

询问用户：

- 粒度是否合适？（太粗 / 太细）
- blocking edges 是否正确：每张 ticket 是否只依赖真正 gate 它的 tickets？
- 是否有 tickets 应该合并或进一步拆分？

反复迭代，直到用户认可这个拆解方案。

### 5. 将 tickets 发布到已配置的 tracker

发布已认可的 tickets。**如何**发布取决于 `/setup-rolex-skills` 配置的 tracker；tickets 本身无论哪种方式都一样，只有 blocking edges 的形态不同：

- **Local files** → 在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md` 下每张 ticket 写一个文件，按依赖顺序从 `01` 编号（blocker 在前）。每个文件的 "Blocked by" 列出它所依赖的编号/标题。使用下面的 per-ticket 文件模板：每张 ticket 一个文件，绝不合并成单个文件。
- **A real issue tracker（GitHub、Linear……）** → 按依赖顺序（blocker 在前）每张 ticket 发布一个 issue，这样每张 ticket 的 blocking edges 可以引用真实标识。在平台支持的情况下使用其原生的 blocking / sub-issue 关系；否则把每张 ticket 的 "Blocked by" 设为阻塞它的 issues。除非另有指示，应用 `ready-for-agent` triage label；这些 tickets 构造上就是 agent 可直接认领的。GitHub 原生关系的接线命令见 [`references/github-tracker.md`](./references/github-tracker.md)。

推进 **frontier**：任何 blockers 全部完成的 ticket。对纯线性链条而言，就是自上而下。

不要关闭或修改任何 parent issue。

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** 这张 ticket 使哪些端到端行为生效，从用户视角描述，不是逐层罗列的实现清单。

**Blocked by:** gate 这张 ticket 的 tickets 的编号/标题，或 "None (can start immediately)"。

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

对 tracker 上 parent issue 的引用（如果来源本身就是一个现有 issue；否则省略本节）。

## What to build

这张 ticket 使哪些端到端行为生效，从用户视角描述，不是逐层实现。

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- 对每张阻塞 ticket 的引用，或 "None (can start immediately)"。

</issue-template>

> **GitHub Issues 注意：** body 中的 `## Blocked by` 段是辅助文档，GitHub 的原生 blocked-by 关系是主机制。两个都保留，不冲突。

无论哪种形式，都要避免具体的文件路径或代码片段：它们很快就会过时。例外：如果 prototype 产出了比散文更精确地编码决策的片段（state machine、reducer、schema、type shape），就内联它，并简短注明它来自 prototype。裁剪到决策密集的部分，不是可运行的 demo，只是重要的那几处。
