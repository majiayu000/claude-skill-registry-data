---
name: science-frontier-to-paper
description: Use when you want to turn a fast-moving implementation from GitHub — a new optimizer, a training trick, a scaling recipe — into a publishable contribution, and you need to find which of them is actually worth reading, extract what it really claims, test whether the field has already filled that slot, and decide what evidence a band-3/4/5 venue would demand; also use when a repo reports a number but no mechanism and you need to know what is missing before writing.
---

# 从 GitHub 前沿到顶刊：把实现变成可证伪的主张

## 为什么这一层存在

一个新优化器的 README 通常写着「1.35x speedup」。这不是 claim，是**观察**。
顶刊要的是「通过什么机制导致什么，以及在什么范围内成立」。
两者之间的距离，就是这一层要量出来的东西。

五个工具是一条链，每一步的产物是下一步的输入：

```
science_frontier_scan       GitHub 上有什么值得读           → frontier_item
science_knowledge_distill   README 里到底声称了什么         → knowledge_claim
science_gap_matrix          这个方向被填了多少               → gap_entry
science_contribution_design 目标档位要求什么证据            → contribution_plan
science_paper_plan          该动笔的结构长什么样            → 标题/图/摘要槽
```

每一步都能单独用。**不要跳步**：跳过 distill 直接 design，你会得到一份针对「1.35x speedup」的
证据清单，而那份清单本身是对的、却完全没打中你真正的问题（缺的是机制，不是样本量）。

## 一、scan：先解决「读什么」

```
science_frontier_scan({ topic: "muon optimizer", domain: "optimization", limit: 5, detail: true })
```

`credibility` 是「这个仓库值不值得读」，权重是：

| 信号 | 权重 | 为什么看它 |
|---|---|---|
| stars | 0.30 | 同行已经替你筛过一次 |
| 52 周 commit 数 | 0.22 | 活着的项目才有可复现的实现 |
| 最近推送 | 0.13 | 一年没动的东西，结果往往跑不出来 |
| release | 0.08 | 有版本号说明作者在乎别人复现 |
| 数学密度 | 0.12 | README 里有定理/收敛/bound/proof |
| 关联论文 | 0.15 | 已经写了 arXiv 的，说明作者正在往论文走 |

再乘类型折扣：`tutorial` ×0.6、`awesome-list` ×0.5、`toolkit` ×0.85、`benchmark` ×0.9、`archived` ×0.3。

实测一组（`topic: "muon optimizer"`，确认过两次）：
`KellerJordan/Muon 0.581` → `zhehangdu/Newton-Muon 0.311` → `LH-Tech-AI/faster-nanogpt 0.282`
→ `vukrosic/muon-optimizer-guide 0.253`（教程，被 0.6 折扣压下去了）→ `nil0x9/flash-muon 0.196`。

**没有类型折扣的话，那个 326 commits 的教程会排第一。** 这就是折扣存在的理由。

### 两个必须知道的坑

**不要用 `topic:` 过滤。** `topic:optimization` 返回的是 `ray`、`czkawka`、`svgo`——
topic 标签是社区随便打的，和「优化理论」无关。工具内置的四个查询模板都不带 topic 过滤，
改用 `in:name` / `in:readme` + 领域词典门。

**必须过领域门。** `muon in:name` 有 20 个仓库，其中 13 个是别的 muon：
`scverse/muon`（单细胞分析）、`muon-build/muon`（构建工具）、`fhunleth/muontrap`（Erlang）、
`wtlnetwork/muon`（无线网）。`relevance()` 用领域词典把它们挡掉，剩 5 个真优化器。
`filteredTotal` 就是被挡掉的数量，它不为 0 是正常的，为 0 才要怀疑词典。

**没有代码搜索。** GitHub 的 `search/code` 需要认证，匿名一律 401。任何人告诉你「搜代码里的
收敛证明」都是没试过。

### 配额现实

| | 匿名 | 带 token |
|---|---|---|
| core 请求 | 60/小时 | 5000/小时 |
| search 请求 | 10/分钟 | 30/分钟 |

一次 `detail: true` 的 scan = 3 次 search + 每个候选仓库 3 次 core（README、统计、release）。
匿名额度下**两三次 scan 就把小时额度用完**，之后 `readme` 全是 `false`、`paperLinks` 全是 0，
而工具不会报错——它只是静默地退化成无细节模式。看到 `detailPartial: true` 就是配额在告警。

想认真用：把 token 放进 `~/.dsh/science/config.json` 的 `retrieval.githubToken`。

## 二、distill：把散文拆成可证伪的句子

```
science_knowledge_distill({ itemId: "g:kellerjordan/muon", maxClaims: 5 })
```

它做四件事：切句 → 按 `theorem / mechanism / result / limitation / marketing` 分类 →
把每个机制句和最近的定理或带数字的结果配对 → 生成反推的证伪条件。

### 唯一的诚实性约束

**`mechanism` 永远是原文句子，不改写。** 一旦改写，你就再也分不清「作者说的」和「工具编的」。
`prediction` 和 `falsifier` 是模板生成的，每条都带 `derived: true`。
`needsHumanReview` 恒为 `true`——工具没有能力判断证明对不对。

所以读 distill 的输出时，你要看的是**比例**：

| 典型配比 | 说明 | 下一步 |
|---|---|---|
| 定理 2+ / 机制 2+ / 结果 2+ | 作者在认真写文档 | 直接进 gap |
| 机制 0 / 结果 3+ | 只有数字，没有解释 | **先别进 design**，见下 |
| 营销 ≥ 2 | `revolutionary` / `blazing` / `guaranteed` | 打折看待其余句子 |
| 句数 < 5 | README 是图或纯代码 | 去读它关联的 arXiv 论文 |

### 「只有结果」是最常见的死法

实测 Muon 的 README，distill 出来的是：

```
[experiment/medium] Lowered the record for training to 94% on CIFAR-10 from 3.3 A100-seconds
[experiment/medium] Improved the training speed record for attaining GPT-2 (small) performance
```

两条都是 result-only，`note` 里写着「这是被报告的结果，不是机制」。
接下来 `science_paper_plan` 会把它标成**高风险**并拒绝硬拼标题——
`mechanismPresent: false`，标题槽留成「（待填机制主语——当前 claim 只报了结果）」，
Figure 1 留成「（还没有 Figure 1：当前 claim 只报结果，没有机制可画）」。

这不是工具坏了。这是它在告诉你：**现在还没有可发表的东西，只有一条记录。**

要跨过这一步，你得补一个能直接测中间量的实验——测谱范数、测条件数、测梯度噪声，
而不是再刷一个 benchmark。

## 三、gap：缺口不是「没人做」，是「这五类里缺哪类」

```
science_gap_matrix({ claimId: "kc_...", limit: 8 })
```

五个方向各有自己的检索式和覆盖判定：

| 方向 | 检索式后缀 | 什么算「已覆盖」 |
|---|---|---|
| `theory` | `convergence rate analysis bound` | 标题/摘要/刊名含 convergence / regret / bound / theorem / proof |
| `scale` | `large scale scaling law` | large-scale / scaling / billion / at scale |
| `transfer` | `transfer cross-domain generalization` | transfer / cross-domain / generalization / OOD |
| `reproduction` | `reproducibility replication` | reproduc / replicat / independent verification |
| `benchmark` | `benchmark evaluation suite` | benchmark / suite / leaderboard / evaluation framework |

判定：覆盖 0 篇 = `gap`，1–2 篇 = `thin`，≥3 篇 = `crowded`。
`theory` 方向在 claim 本身已有定理证据时直接标 `not-needed`——不要让人去补已经有的东西。

### 关键词决定一切，锚点救它

Muon 那条 claim 自动抽出来的词是 `["lowered","record","training"]`——
拿去查「training speed record convergence rate analysis bound」，命中 20 篇，覆盖 0 篇。
**这个 0 是假的**，它只是说明检索式不对。

工具因此有 `anchorKeywordsFromItem()`：从仓库名推锚点，`KellerJordan/Muon` → `["muon","optimizer"]`，
`zhehangdu/Newton-Muon` → `["newton","muon"]`。带上锚点后检索词变成
`["muon","optimizer","training","cifar-10"]`，结果才有意义（theory 1 篇、reproduction 0 篇）。

**中文 claim 不做自动分词。** 中文返回空数组，`overall: "needs-keywords"`，
要你自己给 `keywords: ["orthogonalized momentum", "spectral norm"]`。
用整段中文去检索只会更空——这不是限制，这是不假装能分词。

### 铁律

**检索不到 ≠ 全新。** 十源覆盖的是已发表和预印本，代码仓里的私有结果查不到；
一个 `verdict: "gap"` 的完整含义是「**用这组关键词**没查到」。
投稿前还要用 `science_novelty` 撞一次标题，那是另一层。

## 四、design：band 3 和 band 5 要的东西不是一回事

```
science_contribution_design({ claimId: "kc_...", gapId: "gap_...", targetBand: 4 })
```

先把 claim 归入七类之一：`new-theory` / `new-algorithm` / `empirical-law` / `negative-result` /
`benchmark` / `unification` / `systems`。判定靠句式特征，`equivalent to`、`fail to reproduce`
这种标志性说法权重更高（+2），因为它们本身就是结论。

然后按目标档位给证据清单。**同一份工作，band 3 和 band 5 的清单完全不同**：

以 `new-theory` 为例，band 3 只要「标准假设下的收敛率 + 与 2-3 个基线对比 + 可复现实现」；
band 5 要「上下界匹配或首个紧界 + 假设弱于已有最好结果 + 理论常数项在真实模型上量级相符
+ 跨 3 个数量级 2 个模态一致 + 能抽出可复用的设计原则」。

`estimatedWeeks` 只算**目标档**的未拥有项——把 4/5 档算进来会让「目标是 band 3」看起来比
「目标是 band 5」更久，那没有意义。上行空间单独用 `upwardWeeks` 报。

`gateGaps` 给的是「为什么会被拒」，不是「还差什么实验」：

> band 5 必须有紧界或普适机制；只分析一个算法的收敛率，再干净也上不去

### 最该看的字段是 gapFit

```
⚠ 缺口是 theory，但方案落在 new-algorithm 上。
  要么换贡献类型，要么先补 new-theory 的证据——用实验去填理论缺口是最常见的失败设计。
```

缺口类型和贡献类型有天然配对：`theory→new-theory`、`scale→empirical-law|new-algorithm`、
`transfer→unification`、`reproduction→negative-result`、`benchmark→benchmark`。
配错了，你做出来的东西填不上你发现的那个洞。

**没有「好」和「坏」，只有「配对」和「不配对」。** 工具不评优劣，只指张力。

## 五、plan：结构，不是措辞

```
science_paper_plan({ planId: "cp_...", journalId: "neurips" })
```

给三样东西：三个断言式标题结构、摘要五槽、图的顺序。

### 标题

五套结构，每套都是「主语 + 方向 + 可证伪」：

| 结构 | 适合 | 例子 |
|---|---|---|
| `{X} sets {Y}` | 机制主张 | Chaperone concentration sets the folding rate |
| `{X} bounds {Y}` | 有定理 | Orthogonalized momentum bounds the update spectrum |
| `{X} governs {Y} across {Z}` | 跨规模普适 | A single exponent governs performance across four orders |
| `{X} does not {Y} when {Z}` | 反例 | Second-order optimizers do not improve wall-clock time below 1B |
| `{X} is equivalent to {Y} under {Z}` | 统一 | Adaptive methods are sign-SGD under a diagonal preconditioner |

**草稿是机械填充的，必然要重写。** 工具标了 `draftIsRough: true`，并且给了三个自检问题：
主语在前 5 词内吗、动词是方向词吗、能被一个实验推翻吗。
从「结构对不对」开始改，不要从「措辞好不好」开始改。

如果 claim 原句本身已经满足三个条件（有主语、有方向、可证伪、≤14 词），
工具直接把它作为第一个候选并标 `fromClaim: true`。这种情况很常见——
**好的 claim 和好的标题本来就是一个东西。**

### Figure 1

硬规则：**必须是全文的核心发现，不是示意图、不是流程图。**
把 Figure 1 和标题一起给别人看，他能否说出你在主张什么；不能就重画。
`figureOrder` 里不存在「示意图」这个位置——理论工作最多在最后加一张假设与结论的关系图。

### 摘要五槽

第 2 槽（**空白**）最容易漏，也是编辑判断「为什么现在」的唯一依据。
第 4 槽必须有数字和样本量。工具会标出哪几槽是 `partial`、哪几槽是 `empty`；
`nextActions` 直接把 `empty` 的槽名列出来。

## 六、常见误读

- **「credibility 0.58，说明这条路能中」**——它只说明这个仓库值得读。0.581 的 Muon 和
  「能发 Nature」之间没有任何联系。工具链里没有任何一处预测录用。
- **「五个方向都没缺口，那就没法做了」**——`crowded` 不等于关门。它只说明这些方向已有工作；
  真正的问题变成「在这些工作之上再往前一步是什么」，`gateGaps` 会告诉你那一步是什么。
- **「band 5 清单太长，先按 band 3 做」**——可以，但要清楚 band 3 的东西投 band 5 会被
  desk reject，不是因为质量差，是因为**它们量的不是同一件事**。
- **「distill 出了 5 条 claim，我挑最长的写」**——挑 `evidenceKind: "theorem"` 且
  `confidence: "high"` 的。长度和重要性无关。
- **「gap 说 theory 是空白，我去补个收敛证明就能发」**——先看 `gateGaps`。
  只分析一个算法的收敛率，再干净也到不了 band 5。

## 七、一条完整链

```
science_frontier_scan({ topic: "muon optimizer", limit: 5 })
  → g:kellerjordan/muon (0.581, method, 2 篇关联论文)
science_knowledge_distill({ itemId: "g:kellerjordan/muon" })
  → 2 条 claim（都是 result-only，note 提示缺机制）
science_gap_matrix({ claimId: "kc_..." })
  → theory thin(1) / scale thin(1) / transfer thin(2) / reproduction gap(0) / benchmark thin(2)
science_contribution_design({ claimId: "kc_...", gapType: "theory", targetBand: 4 })
  → new-algorithm，4 项目标档证据，3 处门槛差距，gapFit ⚠
science_paper_plan({ planId: "cp_..." })
  → mechanismPresent: false，标题槽留空，风险 high，下一步：先补机制实验
```

最后一行就是这一层的全部价值：**它在你写第一句话之前，告诉你还差什么。**
