---
name: cs-paper-logic-revision
description: 计算机论文草稿终审与分层重写工作流。先逻辑后语言：检查全文章节结构 → 章节内部逻辑 → 跨章节一致性 → 写作风格 → 摘要逐句功能 → 图表 → 投稿前 sanity check。问题按 P0/P1/P2 分级。适用于 NeurIPS/ICML/ICLR/KDD/CCS/USENIX/SIGMOD/VLDB/IEEE Transactions 等顶会顶刊。Use when 用户请求论文终审、逻辑诊断、分层重写、投稿前检查，或在草稿已成形阶段进行系统性修改。
tags: [Writing, Academic, Paper, Review, LaTeX, CS]
---

# 计算机论文草稿终审与分层重写 Skill

> 英文名：**CS Paper Logic-First Revision Skill**
> 适用对象：计算机领域论文，包括 AI/ML、Security & Privacy、Systems、Database、Data Mining、Graph Learning、Federated Learning、LLM、Medical AI、Software Engineering、IEEE Transactions 等方向。
> 核心原则：**Logic before language. Structure before sentence. Claim before polish.**

---

## 0. Skill 定位

这个 Skill 用于在一篇计算机论文已经形成完整草稿后，进行系统性的终审、诊断和重写。

它不是普通的投稿 checklist，而是一个从"逻辑线诊断"到"写作风格修改"再到"投稿前细节检查"的完整工作流。

执行顺序必须是：

1. 先检查全文章节结构的逻辑线；
2. 再检查每个章节内部的逻辑与段落衔接；
3. 再检查全文章节结构和各章节内部逻辑是否匹配；
4. 逻辑线稳定后，进入写作风格修改；
5. 然后单独进入摘要打磨阶段；
6. 最后检查投稿前的所有小问题。

不要一开始就润色句子。否则很容易把一篇逻辑不清楚的论文改成"语言更流畅但问题仍然不清楚"的论文。

---

## 1. 输入信息

使用本 Skill 时，用户可以提供以下任意一种材料：

- 论文 PDF；
- LaTeX 源码；
- Word 草稿；
- 摘要与 Introduction；
- 某一章节文本；
- 图表、caption 与对应正文；
- 审稿意见与修改稿；
- 目标会议/期刊名称；
- 投稿要求或 checklist。

如果用户没有说明目标会议或期刊，则默认按照**通用计算机顶会/IEEE Transactions 风格**进行检查。

如果用户说明目标 venue，例如 CCS、NDSS、USENIX Security、SIGMOD、VLDB、KDD、NeurIPS、ICML、ICLR、WWW、AAAI、IJCAI、TIFS、TDSC、TPDS、TMC、JBHI 等，则应根据该 venue 的风格调整检查重点。

---

## 2. 输出要求

每次执行本 Skill，应输出以下内容：

1. 总体判断；
2. 全文逻辑主线；
3. 主要结构性问题；
4. 每章逻辑问题；
5. 跨章节不匹配问题；
6. 写作风格问题；
7. 摘要逐句功能检查；
8. 图表与引用问题；
9. 投稿前 checklist；
10. 优先修改顺序。

所有问题建议按照严重程度分级：

| 等级 | 含义 | 处理方式 |
|---|---|---|
| P0 | 必须修改，否则影响录用，甚至可能 desk reject | 优先处理 |
| P1 | 强烈建议修改，会影响审稿人理解和评价 | 第二优先 |
| P2 | 可优化，会提升可读性和专业度 | 视时间处理 |

---

# Stage 1：全文章节结构逻辑线检查

## 1.1 检查目标

首先判断论文是否有一条清楚的主线。

一篇计算机论文应当能够回答以下七个问题：

```text
Problem: 本文解决什么问题？
Motivation: 为什么这个问题重要？
Gap: 现有方法为什么不够？
Insight: 本文的关键观察是什么？
Method: 本文怎么做？
Evidence: 实验证明了什么？
Impact: 这个工作有什么意义？
```

如果这七个问题不能连成一条自然的链条，不能直接进入语言润色。

---

## 1.2 标题检查

标题应清楚反映问题和解决方案。

检查项：

- 标题是否过于泛泛，例如 "A Novel Framework for ..."；
- 标题是否过于狭窄，限制读者群；
- 标题是否包含至少一个技术关键词；
- 标题是否体现问题对象或方法特征；
- 标题是否使用了罕见、自定义或模糊缩写；
- 标题是否过长。

修改原则：

```text
坏标题：A Novel Framework for Efficient Learning
好标题：Hardness-Aware Caching for Safe Graph Unlearning
```

标题最好同时包含：

```text
研究对象 + 技术关键词 + 核心方法特征
```

---

## 1.3 章节顺序检查

标准计算机论文通常包含：

```text
1. Introduction
2. Related Work
3. Preliminaries / Problem Formulation
4. Method / System Design
5. Experiments / Evaluation
6. Discussion / Limitations
7. Conclusion
```

如果论文结构偏离标准顺序，需要检查是否有充分理由。

常见结构问题：

- 还没有定义问题就介绍方法；
- Related Work 过早出现并打断主线；
- 方法图出现在读者还不知道问题之前；
- 实验部分没有按照 RQ 组织；
- Discussion 中突然提出新的 claim；
- Conclusion 只是重复摘要，没有收束全文。

---

## 1.4 Introduction 全局功能检查

Introduction 的核心任务不是"介绍背景"，而是建立审稿人必须继续阅读的理由。

推荐结构：

```text
Paragraph 1: 研究背景和真实需求
Paragraph 2: 现有方法大致路线
Paragraph 3: 关键问题/挑战
Paragraph 4: 为什么现有方法解决不了
Paragraph 5: 本文核心 insight
Paragraph 6: 方法概述
Paragraph 7: 贡献列表
```

红旗问题：

- 第一页读完仍不知道本文解决什么问题；
- 背景写得很大，但没有落到具体任务；
- 直接出现 "The central question is ..."，但前文没有铺垫；
- 方法名突然出现；
- 贡献列表不可验证；
- 图 1 出现太早，读者还不知道它要解释什么；
- 挑战、方法、实验之间无法对应。

---

## 1.5 Related Work 全局功能检查

Related Work 不是文献堆叠，而是为本文的 gap 服务。

检查项：

- 所有引用是否与任务、方法、baseline 或评估场景相关；
- 是否覆盖近期高影响力 baseline；
- 是否解释本文与已有工作的实质差异；
- 是否避免逐篇流水账；
- 是否在末尾用 1–2 句话自然引出本文工作；
- 是否引用了目标会议/期刊中高度相关的工作。

推荐结构：

```text
Category 1: 与任务最相关的方法
Category 2: 与核心技术路线相关的方法
Category 3: 与评估或应用场景相关的方法
Final paragraph: 当前方法仍缺少什么，因此需要本文工作
```

---

## 1.6 Method 全局功能检查

Method 章节必须从前文问题自然推出。

检查问题：

```text
前文提出的问题，本文分别怎么解决？
每个模块对应哪个挑战？
每个设计选择是否有必要？
方法图、正文、伪代码是否一致？
```

常见问题：

- 方法像技术堆砌，而不是问题驱动；
- 公式很多，但没有说明为什么需要；
- 方法图有 4 个模块，正文有 5 个小节；
- 伪代码和正文顺序不一致；
- 读者必须看 appendix 或代码才能理解主方法；
- 方法名称出现得太晚或太突然。

---

## 1.7 Experiment 全局功能检查

实验不是为了证明"我们效果好"，而是为了验证前文提出的 claim。

推荐按照 RQ 组织：

```text
RQ1: 整体性能是否优于基线？
RQ2: 每个模块是否有效？
RQ3: 在不同数据集/场景下是否稳健？
RQ4: 成本、效率、隐私、安全性或可扩展性如何？
RQ5: 失败案例和边界在哪里？
```

检查项：

- Introduction 中的每个 challenge 是否有实验对应；
- Method 中的每个模块是否有消融；
- 摘要中的核心结果是否能在表格或图中找到；
- 是否解释为什么有效，而不是只说 outperform；
- 是否报告必要的统计信息；
- 是否解释负面结果；
- 是否说明硬件环境、软件库和超参数设置。

---

# Stage 2：章节内部逻辑检查

## 2.1 Introduction 内部逻辑

每一段都应承担明确功能。

| 段落 | 功能 | 常见问题 |
|---|---|---|
| P1 | 背景和场景 | 太宽泛，像科普 |
| P2 | 现有方法 | 讲得太细，抢了 Related Work |
| P3 | 挑战 | 问题不具体 |
| P4 | Gap | 没说清楚已有方法为什么失败 |
| P5 | Insight | 突然出现，没有铺垫 |
| P6 | 方法概述 | 太像摘要，缺少机制 |
| P7 | Contributions | 不可验证，太空 |

必查问题：

```text
1. 主问题是否在前两段出现？
2. 每个挑战是否具体？
3. 每个挑战是否与方法模块对应？
4. 方法名称是否自然出现？
5. 贡献是否可验证？
6. 是否有第一页核心图？
7. 图出现前是否已有足够背景？
```

贡献写法应避免：

```text
We provide insights into ...
We improve the understanding of ...
We propose a novel framework ...
```

更好的贡献写法：

```text
We formulate ...
We design ...
We implement ...
We evaluate ... on ... datasets against ... baselines.
```

---

## 2.2 Related Work 内部逻辑

Related Work 应帮助审稿人理解：

```text
已有方法有哪些路线？
这些路线为什么不能解决本文问题？
本文和它们的本质区别是什么？
```

红旗问题：

- 每段都是 "X proposed ..., Y proposed ..."；
- 只讲相似点，不讲差异；
- 没有覆盖重要 baseline；
- 引用太旧；
- 相关工作超过 1.5 页但没有必要；
- 最后一段没有引出本文。

---

## 2.3 Preliminaries / Problem Formulation 内部逻辑

预备知识只保留理解方法必须的内容。

检查项：

```text
1. 符号是否统一？
2. 是否多个符号表示同一概念？
3. 是否一个符号有多个含义？
4. 公式中的每个符号是否首次出现时定义？
5. 是否有符号表？
6. 问题定义是否和后文方法一致？
7. 图、公式、定义出现顺序是否符合阅读顺序？
8. 每个公式是否都有编号和解释？
```

如果某个定义后文没有使用，应删除或移到 appendix。

---

## 2.4 Method 内部逻辑

推荐结构：

```text
Overview paragraph
→ Overall framework figure
→ Module 1
→ Module 2
→ Module 3
→ Training / Optimization / Algorithm
→ Complexity or Implementation Details
```

检查项：

```text
1. 是否先总后分？
2. 方法图是否和小节顺序一致？
3. 每个模块是否对应 Introduction 中的问题？
4. 伪代码是否有行号？
5. 正文解释伪代码时是否引用行号？
6. 公式是否都有解释？
7. 没有被正文引用的公式是否可以删除或内联？
8. 是否避免为了显得高级而加入过多数学表达？
9. 是否足以让读者不看代码也理解方法？
```

方法写作的基本要求：

- 先讲整体流程；
- 再讲每个模块；
- 模块顺序与方法图一致；
- 方法名称、图中术语、正文术语、伪代码术语必须统一；
- 不要让读者频繁回看前文才能理解当前段落。

---

## 2.5 Experiments 内部逻辑

推荐结构：

```text
Experimental Setup
→ Datasets
→ Baselines
→ Metrics
→ Implementation Details
→ RQ1 Overall Performance
→ RQ2 Ablation Study
→ RQ3 Sensitivity / Robustness
→ RQ4 Efficiency / Scalability
→ RQ5 Case Study / Failure Analysis
```

每个实验段落推荐写法：

```text
1. 先概括主要结果；
2. 再比较主要 baseline；
3. 再说明本文方法提升多少；
4. 再解释为什么提升；
5. 最后指出该结果验证了哪个 claim。
```

不要只写：

```text
Our method performs best on all datasets.
```

更好的写法：

```text
SafeCache achieves the lowest deletion latency on all datasets because hardness-aware selection concentrates precomputation on high-cost deletions. This confirms that deletion hardness is a useful signal for cache allocation.
```

---

# Stage 3：跨章节一致性检查

## 3.1 Claim–Evidence Matrix

建立 claim 与 evidence 的对应矩阵。

| Claim | 出现位置 | 支撑位置 | 是否充分 | 修改建议 |
|---|---|---|---|---|
| 本文降低 unlearning latency | Abstract / Intro | Table 2 / Fig. 4 | 充分 | 摘要保留量化结果 |
| 本文减少 leakage | Intro / Method | RQ3 | 不充分 | 增加 attack setting |
| 本文适用于大规模图 | Intro | 无实验 | 不充分 | 删除或补实验 |

检查原则：

- 摘要中的 claim 必须在实验中找到证据；
- Introduction 中提出的 challenge 必须在 Method 中回应；
- Contribution 中声明的创新必须在实验中验证；
- Method 中的每个模块最好有消融或分析；
- 如果实验无法支撑某个 claim，应删除或降调表述。

---

## 3.2 Challenge–Module–Experiment Matrix

| Challenge | Method Module | Experiment | 是否闭环 |
|---|---|---|---|
| 高延迟 | Hardness-aware selection | Latency RQ | 是 |
| 缓存泄漏 | Safety shell | Privacy RQ | 部分 |
| stale state | cleanup mechanism | Case study | 需要加强 |

如果某一行缺失，说明论文逻辑链条不完整。

---

## 3.3 Figure–Text Consistency

检查：

```text
1. 图 1 的模块是否都在正文解释？
2. 正文小节顺序是否和图一致？
3. 图中术语是否和正文术语一致？
4. 图题是否解释了图的 message，而不只是描述元素？
5. 是否出现图比正文更复杂的情况？
6. 是否正文提到的模块没有在图中出现？
```

---

# Stage 4：写作风格修改

## 4.1 删除华而不实的词

重点检查以下词汇：

```text
novel
significant
important
complex
comprehensive
intricate
encompass
robust
seamless
efficient
effective
state-of-the-art
fundamentally
substantially
notably
```

这些词不是不能用，而是不能没有证据地用。

| 原表达 | 问题 | 修改方式 |
|---|---|---|
| a novel framework | 空泛 | 说清楚 novel 在哪里 |
| significantly improves | 没有数字 | 写出提升比例 |
| complex interactions | 太虚 | 说明是哪类 interaction |
| robust performance | 太泛 | 说明在哪些设置下稳定 |

---

## 4.2 拆分冗长句

检查规则：

```text
1. 一个句子超过 25–30 个英文词，要考虑拆分；
2. 一个句子包含两个以上因果关系，要拆分；
3. 一个句子同时介绍背景、问题、方法，要拆分；
4. 段首句不能太长；
5. 避免多个从句连续嵌套；
6. 长句拆分后，尽量不要用含糊代词开头。
```

改写示例：

原句：

```text
Although existing graph unlearning methods can remove requested data by updating affected model parameters, they often ignore the heterogeneous hardness of deletion requests, which causes unnecessary latency for easy cases and insufficient preparation for hard cases.
```

修改：

```text
Existing graph unlearning methods update affected model parameters after a deletion request. However, they usually treat all requests uniformly. This ignores deletion hardness and leads to unnecessary latency for easy cases and poor preparation for hard cases.
```

---

## 4.3 避免反复 recall 其他章节

高风险表达：

```text
As discussed in Section 2 ...
As mentioned earlier ...
As shown previously ...
Recall that ...
The problem introduced above ...
```

修改原则：

- 如果只需要一个概念，直接用一句话重新给出最小上下文；
- 如果必须引用章节，要说明为什么需要回看；
- 不要让一个段落依赖前面很远的内容才能读懂；
- 避免让审稿人频繁跳转。

不推荐：

```text
As discussed in Section 3.1, deletion requests have different hardness levels. Based on this observation, we ...
```

更好：

```text
Instead of routing every deletion through the same workflow, SafeCache uses deletion hardness to decide whether precomputation is worthwhile.
```

---

## 4.4 检查段落衔接

每段开头都应有承接功能。

常见承接类型：

```text
Problem continuation: This limitation becomes more severe when ...
Contrast: Unlike these methods, our setting requires ...
Causal transition: This motivates a caching layer that ...
Scope narrowing: We focus on ...
Design transition: To address this challenge, we ...
Evidence transition: We next evaluate whether ...
```

红旗问题：

- 段落之间像拼接；
- 这一段的第一句和上一段最后一句无关；
- 突然出现新概念；
- 方法名称突然出现；
- central question 突然出现。

---

## 4.5 缩写和术语检查

规则：

```text
1. 首次出现：full name (abbreviation)；
2. 后续统一使用 abbreviation；
3. 不要重复定义；
4. 不要使用小众缩写；
5. 图、表、正文中的术语必须一致；
6. 同一概念不要使用多个近义词反复替换。
```

示例：

```text
Graph neural networks (GNNs)
large language models (LLMs)
out-of-distribution (OOD)
```

---

# Stage 5：摘要逐句功能检查

## 5.1 摘要的基本功能

摘要至少应包含：

```text
1. 问题/任务定义；
2. 提出的方法或想法；
3. 主要结果；
4. 更广泛的影响或意义。
```

更完整的计算机论文摘要可以采用以下功能结构：

```text
S1: 背景/场景
S2: 任务/问题
S3: 现有方法不足
S4: 核心 insight
S5: 本文方法
S6: 方法机制
S7: 主要结果
S8: 意义/影响
```

不是每篇摘要都必须 8 句，但每一句都必须承担明确功能。

---

## 5.2 摘要逐句检查表

| 句子 | 应承担功能 | 是否完成 | 问题 | 修改建议 |
|---|---|---|---|---|
| S1 | 建立场景 | 是/否 | 是否太泛 | 缩小到具体任务 |
| S2 | 定义问题 | 是/否 | 问题是否清楚 | 明确对象和挑战 |
| S3 | 指出现有不足 | 是/否 | 是否太空 | 说明失败原因 |
| S4 | 提出 insight | 是/否 | 是否突兀 | 增加铺垫 |
| S5 | 介绍方法 | 是/否 | 是否太细 | 保留核心机制 |
| S6 | 解释机制 | 是/否 | 是否重复 | 合并或删除 |
| S7 | 给出结果 | 是/否 | 是否量化 | 加数字 |
| S8 | 说明意义 | 是/否 | 是否夸大 | 克制表达 |

---

## 5.3 摘要禁忌

```text
1. 不要出现未定义缩写；
2. 不要用 important / novel / state-of-the-art 但不给证据；
3. 不要只说提出方法，不说解决什么问题；
4. 不要只说效果好，不给数字；
5. 不要把实验设置写得过细；
6. 不要在摘要里引用文献；
7. 不要让第一句话太宽泛；
8. 不要让方法名先于问题出现。
```

---

# Stage 6：图表检查

## 6.1 图表功能检查

每张图表都必须回答：

```text
这张图/表让审稿人多理解了什么？
如果删除它，论文会损失什么信息？
```

---

## 6.2 图表 checklist

```text
1. 所有图表是否在正文中引用？
2. 图表是否提供新信息？
3. 图题是否至少包含解释或背景？
4. 图题是否说明 take-away？
5. 图中字体是否足够大？
6. 图例是否完整？
7. 颜色灰度打印是否可区分？
8. 是否使用矢量图或无损格式？
9. 是否有两个图表连续出现，中间没有正文解释？
10. 图表位置是否尽量在页面顶部？
```

---

## 6.3 Caption 推荐格式

```text
Figure X: [What the figure shows]. [Main takeaway and why it matters].
```

示例：

```text
Figure 1: Overview of SafeCache. SafeCache first estimates deletion hardness, then precomputes selected hard deletions, and finally routes requests through a safety shell to reduce cache-induced leakage.
```

---

# Stage 7：投稿前最终检查

## 7.1 LaTeX 和 PDF

```text
1. 无编译错误；
2. 无 bad boxes；
3. 无 overfull hbox；
4. 无孤立标题；
5. 无孤行；
6. 页数符合要求；
7. appendix 是否计入页数已确认；
8. PDF 在不同设备打开正常。
```

---

## 7.2 匿名检查

```text
1. 文件名不含作者姓名；
2. PDF metadata 不含作者信息；
3. GitHub/code repository 匿名；
4. 图片路径不暴露用户名；
5. supplementary material 不含身份信息；
6. acknowledgment 是否按要求隐藏；
7. artifact、demo、video、README 是否匿名。
```

---

## 7.3 引用检查

```text
1. 所有引用真实存在；
2. 题名、作者、年份、venue 正确；
3. BibTeX 无重复；
4. 数据集、模型、工具包均已引用；
5. 至少引用目标 venue 的相关论文；
6. 自引比例不过高；
7. LLM 推荐的引用必须人工核对；
8. 不存在虚假引用；
9. 同时引用多个参考文献时格式统一。
```

---

## 7.4 Open Science / Artifact 检查

适用于 CCS、USENIX、ML/Systems 等重视 artifact 的会议。

```text
1. 是否需要 artifact appendix？
2. 是否需要说明代码可用性？
3. 是否需要匿名仓库？
4. 是否需要数据集使用声明？
5. 是否需要 ethics statement？
6. 是否需要 reproducibility statement？
7. 是否需要说明不开源原因？
8. 是否存在违反匿名政策的链接或 metadata？
```

---

# 8. 标准调用提示词

以后可以直接这样使用本 Skill：

```text
请使用"计算机论文草稿终审与分层重写 Skill"检查下面这篇论文。

要求：
1. 不要先润色句子，先检查全文章节结构的逻辑线；
2. 再检查每个章节内部的段落逻辑和铺垫；
3. 再检查章节之间是否前后匹配；
4. 然后进入写作风格修改，重点检查华而不实的词、冗长句、LLM 味表达、反复 recall 其他章节的问题；
5. 然后逐句检查摘要中每句话的功能；
6. 最后给出投稿前 sanity checklist；
7. 所有问题按 P0/P1/P2 分级；
8. 给出可执行修改建议，不要只给笼统评价。
```

---

# 9. 标准输出模板

```markdown
# Paper Revision Report

## 1. Overall Diagnosis

## 2. Global Logic Line

## 3. P0 Problems: Must Fix

## 4. P1 Problems: Strongly Recommended

## 5. P2 Problems: Optional Polishing

## 6. Section-by-Section Logic Review

### 6.1 Abstract
### 6.2 Introduction
### 6.3 Related Work
### 6.4 Preliminaries
### 6.5 Method
### 6.6 Experiments
### 6.7 Discussion / Conclusion

## 7. Cross-Section Consistency Matrix

## 8. Writing Style Problems

## 9. Abstract Sentence-Function Table

## 10. Figure and Table Review

## 11. Reference and Citation Sanity Check

## 12. Final Submission Checklist

## 13. Priority Revision Plan
```

---

# 10. 最终判断标准

检查一篇计算机论文时，最终只问五个问题：

```text
1. 审稿人是否能在第一页知道本文解决什么问题？
2. 审稿人是否能理解为什么已有方法不够？
3. 审稿人是否能看到本文方法是从问题自然推出来的？
4. 审稿人是否能通过实验确认每个核心 claim？
5. 审稿人是否能顺畅读完，而不需要反复翻前文或猜作者意思？
```

如果这五个问题都能回答清楚，论文就不仅是"写完了"，而是具备了投稿前打磨的基本质量。

---

# 11. 来源与整合说明

本 Skill 综合了以下材料：

1. 用户提供的《论文写作经验总结》；
2. GitHub 项目 `yzhao062/cs-paper-checklist`；
3. 面向计算机论文审稿与修改的通用经验；
4. 针对 CCS、NDSS、IEEE Transactions、AI/ML 会议和系统类会议的论文写作习惯总结。
