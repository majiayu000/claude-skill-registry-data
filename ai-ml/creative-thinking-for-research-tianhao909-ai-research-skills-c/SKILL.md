---
name: creative-thinking-for-research
description: Applies cognitive science frameworks for creative thinking to CS and AI research ideation. Use when seeking genuinely novel research directions by leveraging combinatorial creativity, analogical reasoning, constraint manipulation, and other empirically grounded creative strategies.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Creative Thinking, Research Ideation, Analogical Reasoning, Problem Reformulation, Cognitive Science]
dependencies: []
---

# 科研创意思维 | Creative Thinking for Research

八个来自认知科学的经验性框架，应用于计算机科学和人工智能研究。与临时头脑风暴不同，这里的每个框架都有数十年的创造力研究支撑——从Koestler的二元联想（bisociation）到Kauffman的邻近可能（adjacent possible）。它们针对不同的认知操作：组合、重构、类比、约束、反转、抽象、探索边界和保持矛盾。

Eight empirically grounded frameworks from cognitive science, applied to computer science and AI research. Unlike ad-hoc brainstorming, each framework here is backed by decades of creativity research — from Koestler's bisociation to Kauffman's adjacent possible. They target distinct cognitive operations: combining, reformulating, analogizing, constraining, inverting, abstracting, exploring boundaries, and holding contradictions.

## 何时使用此技能 | When to Use This Skill

- 生成真正新颖的想法，而非先前工作的增量扩展
- 在单一子领域的思维中感到陷入局部最优
- 想要系统地应用创造力启发式，而非等待灵感
- 为研究 retreat 或博士级别的创意会议做准备
- 跨领域桥接，寻求结构性（非表面）连接

- Generating genuinely novel ideas, not incremental extensions of prior work
- Feeling trapped in a local optimum of thinking within a single subfield
- Wanting to systematically apply creativity heuristics rather than waiting for inspiration
- Preparing for a research retreat or PhD-level ideation session
- Bridging between fields and seeking structural (not superficial) connections

**请勿在以下情况使用此技能**：
- 你需要结构化的项目级头脑风暴工作流（请使用 `brainstorming-research-ideas`）
- 你有一个明确的问题，需要执行帮助（请使用领域特定技能）
- 你需要文献综述（请使用 `scientific-skkills:literature-review`）

**Do NOT use this skill when**:
- You need structured project-level brainstorming workflows (use `brainstorming-research-ideas`)
- You have a well-defined problem and need execution help (use domain-specific skills)
- You need a literature survey (use `scientific-skills:literature-review`)

**与头脑风暴技能的关系**：头脑风暴技能提供操作工作流（发散→收敛→优化）和实用过滤器。此技能提供更深入的认知引擎，驱动创造性飞跃。结合使用：用创意思维生成原始洞察，用头脑风暴来构建和评估。

**Relationship to Brainstorm skill**: The brainstorm skill provides operational workflows (diverge → converge → refine) and practical filters. This skill provides the deeper cognitive engines that power creative leaps. Use them together: creative-thinking to generate raw insight, brainstorm to structure and evaluate it.

---

## 框架1：组合创造性（二元联想）| Framework 1: Combinatorial Creativity (Bisociation)

新想法来自于以意想不到的方式组合现有概念。Arthur Koestler称之为**二元联想（bisociation）**——连接两个先前无关的参考框架，这与单一框架内的常规联想不同。

Novel ideas arise from combining existing concepts in unexpected ways. Arthur Koestler called this **bisociation** — connecting two previously unrelated frames of reference, as distinct from routine association within a single frame.

**为什么有效**：元研究一致表明，知识广度是创造性输出的先决条件。跨学科阅读的人会产生更多新颖的工作。组合本身才是创造性行为。

**Why it works**: Meta-research consistently shows that breadth of knowledge is a precursor to creative output. People who read across disciplines produce more novel work. The combination itself is the creative act.

**在计算机科学研究中**：
- 生物进化 → 优化（遗传算法）
- 博弈论 → 网络（路由机制设计）
- 统计物理 → 机器学习（玻尔兹曼机、基于能量的模型）
- 语言学 → 编程（类型论、形式语法）

**In CS Research**:
- Biological evolution → optimization (genetic algorithms)
- Game theory → networking (mechanism design for routing)
- Statistical physics → machine learning (Boltzmann machines, energy-based models)
- Linguistics → programming (type theory, formal grammars)

**系统性二元联想工作流**：

1. **选择两个领域**，你至少有一定了解
2. **列出核心原语**：每个领域5-10个基本概念
3. **创建叉积矩阵**：行 = 领域A的概念，列 = 领域B的概念
4. **对每个单元格**，问：「将A的概念应用于B的问题意味着什么？」
5. **筛选**：哪些组合产生了可验证的研究问题？
6. **验证结构性深度**：连接是机制性的还是仅隐喻性的？

**Systematic Bisociation Workflow**:

1. **Select two domains** you have at least passing familiarity with
2. **List core primitives** in each domain (5-10 fundamental concepts per domain)
3. **Create a cross-product matrix**: row = concepts from Domain A, column = concepts from Domain B
4. **For each cell**, ask: "What would it mean to apply A's concept to B's problem?"
5. **Filter**: Which combinations produce a non-trivial, testable research question?
6. **Validate structural depth**: Is the connection mechanistic or merely metaphorical?

**叉积示例**：

| | 缓存 | 负载均衡 | 容错 |
|---|---------|---------------|-----------------|
| **自然选择** | 驱逐最不适配的条目 | 通过适应度自适应分配 | 种群级冗余 |
| **免疫记忆** | 学习到的威胁签名 | 分布式检测 | 自我/非自我区分 |
| **共生** | 协作预取 | 互惠资源共享 | 相互依赖的弹性 |

**Cross-Product Example**:

| | Caching | Load Balancing | Fault Tolerance |
|---|---------|---------------|-----------------|
| **Natural Selection** | Evict least-fit entries | Adaptive allocation via fitness | Population-level redundancy |
| **Immune Memory** | Learned threat signatures | Distributed detection | Self/non-self discrimination |
| **Symbiosis** | Cooperative prefetching | Mutualistic resource sharing | Co-dependent resilience |

**质量检验**：强有力的二元联想不是表面隐喻（「网络像大脑」），而是结构性映射，其中机制转移（「注意力机制实现了一种类似于认知注意力过滤的选择性门控形式」）。

**Quality Test**: A strong bisociation is not a surface metaphor ("the network is like a brain") but a structural mapping where the mechanism transfers ("attention mechanisms implement a form of selective gating analogous to cognitive attention filtering").

**自检**：
- [ ] 连接是结构性的（机制映射）还是仅语言上的（标签映射）？
- [ ] 组合是否产生可验证的预测？
- [ ] 两个领域的专家是否会觉得这个连接不明显但合理？

**Self-Check**:
- [ ] Is the connection structural (mechanisms map) or merely verbal (labels map)?
- [ ] Does the combination generate testable predictions?
- [ ] Would an expert in both fields find the connection non-obvious but sound?

---

## 框架2：问题重构（表征改变）| Framework 2: Problem Reformulation (Representational Change)

格式塔心理学家发现，突破往往不是来自于解决所陈述的问题，而是来自于**重新表征问题本身**。Kaplan和Simon关于洞察的研究表明，改变问题空间——约束、抽象层次、形式化——通常是创造力所在。

Gestalt psychologists identified that breakthroughs often come not from solving the problem as stated, but from **re-representing the problem itself**. Kaplan and Simon's work on insight shows that changing the problem space — the constraints, the abstraction level, the formalism — is often where creativity lives.

**关键转变**：从「我如何解决这个问题？」到「我是否正确地思考这个问题？」

**The Key Shift**: From "How do I solve this problem?" to "Am I even thinking about this problem correctly?"

**重构策略**：

| 策略 | 示例 |
|----------|---------|
| **改变目标** | 「让算法更快」→「消除这种计算的需求」 |
| **改变形式化** | 图问题 → 线性代数问题（谱方法） |
| **改变粒度** | 每token预测 → 每span预测 |
| **改变主体** | 「模型应该如何学习？」→「数据应该如何教？」（课程学习） |
| **改变时间尺度** | 实时优化 → 摊销推理 |
| **反转方向** | 正向模拟 → 逆问题（从观察中学习） |

**Reformulation Strategies**:

| Strategy | Example |
|----------|---------|
| **Change the objective** | "Make the algorithm faster" → "Eliminate the need for this computation" |
| **Change the formalism** | Graph problem → linear algebra problem (spectral methods) |
| **Change the granularity** | Per-token prediction → per-span prediction |
| **Change the agent** | "How should the model learn?" → "How should the data teach?" (curriculum learning) |
| **Change the timescale** | Real-time optimization → amortized inference |
| **Invert the direction** | Forward simulation → inverse problem (learning from observations) |

**工作流**：

1. 用一句话陈述你当前的问题
2. 找出该陈述中的**隐含假设**：
   - 你使用的是什么形式化？（能用不同的吗？）
   - 目标是什么？（是正确的目标吗？）
   - 什么粒度级别？（能更粗或更细吗？）
   - 主体是谁？（能转换视角吗？）
3. 对每个假设，**生成替代方案**：「如果[相反的假设]呢？」
4. 对每个替代方案，问：「这种重构是否使问题更容易、更难，或以有用的方式不同？」
5. 使难题变容易的重构本身通常就是一个可发表的洞察

**Workflow**:

1. State your current problem in one sentence
2. Identify the **hidden assumptions** in that statement:
   - What formalism are you using? (Could you use a different one?)
   - What is the objective? (Is it the right objective?)
   - What level of granularity? (Could you go coarser or finer?)
   - Who is the agent? (Could you shift perspective?)
3. For each assumption, **generate the alternative**: "What if [opposite assumption]?"
4. For each alternative, ask: "Does this reformulation make the problem easier, harder, or different in a useful way?"
5. A reformulation that makes a hard problem easy is often a publishable insight on its own

**经典计算机科学示例**：
- **PageRank**：将「查找重要网页」从内容分析重构为图特征值问题
- **Dropout**：将「防止过拟合」从正则化重构为近似集成
- **Attention**：将「处理长序列」从记住一切重构为选择性查询

**Classic CS Examples**:
- **PageRank**: Reformulated "find important web pages" from content analysis to graph eigenvalue problem
- **Dropout**: Reformulated "prevent overfitting" from regularization to approximate ensemble
- **Attention**: Reformulated "handle long sequences" from remembering everything to selectively querying

---

## 框架3：类比推理（结构映射）| Framework 3: Analogical Reasoning (Structure-Mapping)

Dedre Gentner的**结构映射理论**和Kevin Dunbar对真实科学家的研究表明，类比是科学创造力的核心引擎。关键发现：表面层面的类比很常见但很弱；**结构性或关系性类比**——深层因果/关系结构跨领域映射——产生最强大的洞察。

Dedre Gentner's **structure-mapping theory** and Kevin Dunbar's studies of real scientists show that analogy is the core engine of scientific creativity. The critical finding: surface-level analogies are common but weak; **structural or relational analogies** — where the deep causal/relational structure maps across domains — produce the most powerful insights.

**Dunbar的发现**：在最成功的实验室中，遥远领域的类比推动了最重要的发现。近处类比完善想法；远处类比生成想法。

**Dunbar's Finding**: In the most successful labs, analogies from distant domains drove the most important discoveries. Nearby analogies refined ideas; distant analogies generated them.

**类比深度层次**：

| 层次 | 描述 | 价值 | 示例 |
|-------|-------------|-------|---------|
| **表面** | 事物看起来相似 | 低 | 「神经网络像大脑」 |
| **关系** | 实体之间的关系匹配 | 中 | 「模型中的注意力分配与经济学中的资源分配类似」 |
| **结构** | 深层因果机制映射 | 高 | 「扩散模型逆转热力学过程；非平衡统计力学的数学直接适用」 |

**Levels of Analogical Depth**:

| Level | Description | Value | Example |
|-------|-------------|-------|---------|
| **Surface** | Things look similar | Low | "A neural network is like a brain" |
| **Relational** | Relationships between entities match | Medium | "Attention allocation in models parallels resource allocation in economics" |
| **Structural** | Deep causal mechanisms map | High | "Diffusion models reverse a thermodynamic process; the math of non-equilibrium stat-mech directly applies" |

**结构映射工作流**：

1. **仅使用关系/因果语言描述你的问题**（去除领域特定的名词）
   - 不好：「我们需要提高transformer注意力效率」
   - 好的：「我们有一个系统必须从大型集合中有选择地聚合信息，其中相关性是上下文相关的，且成本随集合大小呈二次方增长」
2. **寻找结构性匹配**：还有什么其他系统从大型集合中有选择地聚合？
   - 数据库查询优化、神经科学中的视觉Attention、信息检索、资源分配
3. **选择具有真正结构性保真度的最远匹配**
4. **映射解决方案机制**：源领域如何解决这个问题？
5. **迁移和适应**：将该机制带入你的领域时会有什么变化？
6. **生成预测**：类比应该告诉你一些你以前不知道的事情

**Structure-Mapping Workflow**:

1. **Describe your problem** using only relational/causal language (strip domain-specific nouns)
   - Bad: "We need to improve transformer attention efficiency"
   - Good: "We have a system that must selectively aggregate information from a large set, where relevance is context-dependent and the cost scales quadratically with set size"
2. **Search for structural matches**: What other systems selectively aggregate from large sets?
   - Database query optimization, visual attention in neuroscience, information retrieval, resource allocation
3. **Pick the most distant match** with genuine structural fidelity
4. **Map the solution mechanism**: How does the source domain solve this?
5. **Transfer and adapt**: What changes when you bring that mechanism into your domain?
6. **Generate predictions**: The analogy should tell you something you didn't already know

**验证清单**：
- [ ] 映射是否保留了因果/关系结构（而不仅仅是标签）？
- [ ] 我能否识别出类比在我的领域做出的至少一个预测？
- [ ] 源领域的专家是否会确认该机制被正确理解？
- [ ] 类比对目标受众来说是否不明显？

**Validation Checklist**:
- [ ] Does the mapping preserve causal/relational structure (not just labels)?
- [ ] Can I identify at least one prediction the analogy makes in my domain?
- [ ] Would an expert in the source domain confirm the mechanism is correctly understood?
- [ ] Is the analogy non-obvious to my target audience?

---

## 框架4：约束操作（Boden框架）| Framework 4: Constraint Manipulation (Boden's Framework)

Margaret Boden的框架根据它们与约束的交互方式区分了三种形式的创造力：

| 类型 | 操作 | 计算机科学示例 |
|------|-----------|------------|
| **探索性** | 在现有概念空间内搜索 | 超参数调优、固定范式内的架构搜索 |
| **组合性** | 组合不同空间的元素 | 多任务学习、神经符号方法 |
| **转换性** | 改变空间本身的规则 | 放弃训练需要标签的假设（自监督学习） |

**Transformational creativity is the rarest and highest-impact.** It happens when you change what is even considered a valid solution.

**Framework 4: Constraint Manipulation (Boden's Framework)**

Margaret Boden's framework distinguishes three forms of creativity based on how they interact with constraints:

| Type | Operation | CS Example |
|------|-----------|------------|
| **Exploratory** | Search within the existing conceptual space | Hyperparameter tuning, architecture search within a fixed paradigm |
| **Combinational** | Combine elements from different spaces | Multi-task learning, neuro-symbolic methods |
| **Transformational** | Change the rules of the space itself | Dropping the assumption that training requires labels (self-supervised learning) |

**转换性创造力是最稀有且影响力最高的。**它发生在你改变什么被认为是有效解决方案的时候。

**Transformational creativity is the rarest and highest-impact.** It happens when you change what is even considered a valid solution.

**约束分析工作流**：

1. **列出**你当前方法的约束（5-10个约束）：
   - 计算：「必须适合GPU内存」
   - 方法论：「需要标注数据」
   - 架构：「使用固定长度上下文」
   - 评估：「通过基准X的准确率衡量」
2. **对每个约束进行分类**：
   - **硬约束**：物理或逻辑上必需的（不能违反）
   - **软约束**：约定或历史偶然（可以质疑）
   - **隐含约束**：未声明但隐含假设（最具创新潜力）
3. **对每个软/隐含约束**，问：
   - 如果放松它会怎样？（从放松「适合内存」产生流式算法）
   - 如果收紧它会怎样？（从收紧计算预算产生效率研究）
   - 如果用完全不同的约束替换它呢？
4. **最具生产力的举措**通常是揭示并放弃隐含约束

**Constraint Analysis Workflow**:

1. **List the constraints** of your current approach (5-10 constraints):
   - Computational: "Must fit in GPU memory"
   - Methodological: "Requires labeled data"
   - Architectural: "Uses fixed-length context"
   - Evaluative: "Measured by accuracy on benchmark X"
2. **Classify each constraint**:
   - **Hard**: Physically or logically necessary (cannot violate)
   - **Soft**: Convention or historical accident (can question)
   - **Hidden**: Not stated but implicitly assumed (most fertile for innovation)
3. **For each soft/hidden constraint**, ask:
   - What if we relaxed it? (streaming algorithms from relaxing "fits in memory")
   - What if we tightened it? (efficiency research from tightening compute budgets)
   - What if we replaced it with a different constraint entirely?
4. **The most productive move** is often exposing and dropping a hidden constraint

**约束转换的经典示例**：
- 「数据必须适合内存」→ 放弃 → 流式算法、外部内存
- 「训练需要人工标签」→ 放弃 → 自监督学习
- 「模型必须是确定性的」→ 放弃 → 变分方法、扩散
- 「推理必须一次完成」→ 放弃 → 迭代优化、思维链

**Classic Examples of Constraint Transformation**:
- "Data must fit in memory" → dropped → streaming algorithms, external memory
- "Training requires human labels" → dropped → self-supervised learning
- "Models must be deterministic" → dropped → variational methods, diffusion
- "Inference must happen in one pass" → dropped → iterative refinement, chain-of-thought

---

## 框架5：否定与反转 | Framework 5: Negation and Inversion

取你所在领域的一个核心假设并否定它。这在De Bono的横向思维和工程领域的**TRIZ方法论**中有正式阐述。

Take a core assumption in your field and negate it. This is formalized in De Bono's lateral thinking and the **TRIZ methodology** from engineering.

**模式**：「如果[普遍持有的假设]是错的、不必要的或可反转的」会怎样？

**The Pattern**: "What if [widely held assumption] is wrong, unnecessary, or invertible?"

**系统性否定工作流**：

1. **列出**你子领域的5-10个核心假设（那些「每个人都知道」的事情）
2. **否定每个假设**并问：你会构建什么系统？
3. **评估每个否定**：
   - 不一致 → 放弃
   - 已探索 → 检查条件是否已改变（见头脑风暴技能，框架5）
   - 未探索且一致 → 潜在研究方向

**Systematic Negation Workflow**:

1. **List 5-10 core assumptions** in your subfield (the things "everyone knows")
2. **Negate each one** and ask: What system would you build?
3. **Evaluate each negation**:
   - Incoherent → discard
   - Already explored → check if conditions have changed (see brainstorm skill, Framework 5)
   - Unexplored and coherent → potential research direction

**计算机科学否定案例名人堂**：

| 假设 | 否定 | 结果 |
|-----------|----------|--------|
| 「我们需要强一致性」 | 如果我们不需要呢？ | 最终一致性、CRDTs |
| 「我们需要精确答案」 | 如果近似可以呢？ | Sketch、LSH、近似最近邻 |
| 「标签是必要的」 | 如果我们无标签学习呢？ | 自监督学习、对比方法 |
| 「更多参数=更多计算」 | 如果我们不完全使用参数呢？ | 混合专家、稀疏模型 |
| 「训练和推理是分开的」 | 如果模型持续学习呢？ | 在线学习、测试时训练 |
| 「错误必须被防止」 | 如果我们拥抱并纠正它们呢？ | 投机解码、自纠正 |

**Negation Hall of Fame in CS**:

| Assumption | Negation | Result |
|-----------|----------|--------|
| "We need strong consistency" | What if we don't? | Eventual consistency, CRDTs |
| "We need exact answers" | What if approximate is fine? | Sketches, LSH, approximate nearest neighbors |
| "Labels are necessary" | What if we learn without them? | Self-supervised learning, contrastive methods |
| "More parameters = more compute" | What if we don't use all parameters? | Mixture of Experts, sparse models |
| "Training and inference are separate" | What if the model keeps learning? | Online learning, test-time training |
| "Errors must be prevented" | What if we embrace and correct them? | Speculative decoding, self-correction

**TRIZ启发的计算机科学原则**：

| TRIZ原则 | 计算机科学应用 |
|---------------|----------------|
| **反转** | 反转过程（生成式vs判别式） |
| **分割** | 将整体分解为模块（微服务、混合专家） |
| **合并** | 合并单独步骤（端到端学习） |
| **通用性** | 一个组件服务多个功能（多任务模型） |
| **嵌套** | 将一个系统放入另一个（元学习） |
| **动态化** | 使静态事物可适应（动态架构、自适应计算） |

**TRIZ-Inspired Principles for CS**:

| TRIZ Principle | CS Application |
|---------------|----------------|
| **Inversion** | Reverse the process (generative vs. discriminative) |
| **Segmentation** | Break monolithic into modular (microservices, mixture of experts) |
| **Merging** | Combine separate steps (end-to-end learning) |
| **Universality** | One component serves multiple functions (multi-task models) |
| **Nesting** | Place one system inside another (meta-learning) |
| **Dynamization** | Make static things adaptive (dynamic architectures, adaptive computation)

---

## 框架6：抽象与泛化阶梯 | Framework 6: Abstraction and Generalization Laddering

在抽象阶梯上上下移动是一个基本的创造性行为。Polya的启发式形式化了这一点：*「你能解决一个更一般的问题吗？一个更具体的？一个类似的？」*

Moving up and down the abstraction ladder is a fundamental creative act. Polya's heuristics formalize this: *"Can you solve a more general problem? A more specific one? An analogous one?"*

**三种移动**：

| 移动 | 问题 | 结果 |
|------|----------|---------|
| **泛化** | 「我的解决方案是更广泛事物的特例吗？」 | 框架论文、统一理论 |
| **专业化** | 「当我添加极端约束时会发生什么？」 | 利基应用、令人惊讶的边缘情况 |
| **类比** | 「这个抽象模式还出现在哪里？」 | 跨领域迁移（见框架3） |

**Three Moves**:

| Move | Question | Outcome |
|------|----------|---------|
| **Generalize** | "Is my solution a special case of something broader?" | Framework papers, unifying theories |
| **Specialize** | "What happens when I add extreme constraints?" | Niche applications, surprising edge cases |
| **Analogize** | "Where else does this abstract pattern appear?" | Cross-domain transfer (see Framework 3) |

**泛化工作流**：
1. 陈述你的具体结果
2. 用变量替换每个具体元素：「ResNet在ImageNet上有效」→「架构X在分布Y上有效」
3. 问：在什么条件下这成立？什么是普遍原理？
4. 如果普遍原理是新颖的 → 那就是贡献

**Generalization Workflow**:
1. State your specific result
2. Replace each specific element with a variable: "ResNet works for ImageNet" → "Architecture X works for distribution Y"
3. Ask: Under what conditions does this hold? What is the general principle?
4. If the general principle is novel → that is the contribution

**专业化工作流**：
1. 获取一个通用方法
2. 添加极端约束：小数据、高维度、对抗输入、实时需求
3. 问：方法仍然有效吗？如果没有，为什么？
4. 失败案例通常揭示方法的真正假设

**Specialization Workflow**:
1. Take a general method
2. Add extreme constraints: tiny data, huge dimensionality, adversarial inputs, real-time requirements
3. Ask: Does the method still work? If not, why not?
4. The failure case often reveals the method's true assumptions

**何时泛化vs专业化**：
- 当你有结果但没有解释时 → 泛化
- 当你有理论但没有依据时 → 专业化
- 当你被困在任一方向时 → 类比

**When to Generalize vs. Specialize**:
- Generalize when you have results but no explanation
- Specialize when you have theory but no grounding
- Analogize when you are stuck in either direction

---

## 框架7：邻近可能（Kauffman / Johnson）| Framework 7: The Adjacent Possible (Kauffman / Johnson)

Stuart Kauffman的概念，经Steven Johnson推广：创新发生在当前可达边界附近——**邻近可能**。一旦先决条件存在，新想法就变得可思考。这解释了为什么同时独立发现如此普遍——多人到达同一边界。

Stuart Kauffman's concept, popularized by Steven Johnson: innovation happens at the boundary of what is currently reachable — the **adjacent possible**. New ideas become thinkable once their prerequisites exist. This explains why simultaneous independent discovery is so common — multiple people reach the same boundary.

**实际意义**：绘制最近变得可能的内容，并探索这些赋能因素开辟的空间。

**Practical Implication**: Map what has recently become possible and explore the space those enablers open.

**邻近可能映射工作流**：

1. **列出最近的赋能因素**（过去1-3年）：
   - 新硬件能力（更长上下文、更快推理、新加速器）
   - 新数据集或基准
   - 新开源工具或框架
   - 新理论结果
   - 新监管或社会条件
2. **对每个赋能因素，问**：「以前不可能或不切实际的，现在这允许什么？」
3. **组合赋能因素**：最强大的邻近可能来自于多个新赋能因素的交叉
4. **检查竞争**：如果很多人能看到相同的邻近可能，速度或独特角度很重要

**Adjacent Possible Mapping Workflow**:

1. **List recent enablers** (last 1-3 years):
   - New hardware capabilities (longer context, faster inference, new accelerators)
   - New datasets or benchmarks
   - New open-source tools or frameworks
   - New theoretical results
   - New regulatory or social conditions
2. **For each enabler, ask**: "What was previously impossible or impractical that this now permits?"
3. **Combine enablers**: The most powerful adjacent possibles arise from the intersection of multiple new enablers
4. **Check for competition**: If many people can see the same adjacent possible, speed or a unique angle matters

**当前的邻近可能（2025-2026）**：

| 赋能因素 | 新可能 |
|---------|---------------|
| 100万+token上下文窗口 | 全代码库推理、书籍长度分析 |
| 推理成本下降（2年内100倍） | 实时agent循环、永远在线AI助手 |
| GPT-4级别的开源模型 | 前沿能力的可复现研究 |
| 多模态模型（视觉+语言+音频） | 统一感知-推理系统 |
| 大规模合成数据 | 无自然数据领域的训练数据 |
| 工具使用模型 | 研究自动化、自我改进系统 |

**Current Adjacent Possibles (2025-2026)**:

| Enabler | Newly Possible |
|---------|---------------|
| 1M+ token context windows | Full-codebase reasoning, book-length analysis |
| Inference cost drops (100x in 2 years) | Real-time agentic loops, always-on AI assistants |
| Open-weight models at GPT-4 level | Reproducible research on frontier capabilities |
| Multimodal models (vision + language + audio) | Unified perception-reasoning systems |
| Synthetic data at scale | Training data for domains with no natural data |
| Tool-using models | Research automation, self-improving systems

**时间信号**：如果你的想法需要尚不存在的技术，它就在邻近可能之外——先搁置。如果你的想法5年前就可以做，很可能有人已经做了——检查文献。最佳点是过去6-18个月变得可行的想法。

**Timing Signal**: If your idea requires technology that doesn't exist yet, it's beyond the adjacent possible — park it. If your idea could have been done 5 years ago, someone probably did — check the literature. The sweet spot is ideas that became feasible in the last 6-18 months.

---

## 框架8：雅努斯式与辩证思维 | Framework 8: Janusian and Dialectical Thinking

Albert Rothenberg对杰出创造者的研究发现，**同时持有两个矛盾的想法**是创造性思维的标志。以罗马双面神雅努斯命名，这种思维方式不会通过选择一边来解决矛盾——它生成超越对立的新框架。

Albert Rothenberg's studies of eminent creators found that **holding two contradictory ideas simultaneously** is a hallmark of creative thinking. Named after Janus, the two-faced Roman god, this mode of thinking doesn't resolve contradictions by choosing a side — it generates new frameworks that transcend the opposition.

**在计算机科学中**：最具影响力的结果往往来自于先前被认为不可调和的张力。

**In CS**: The most influential results often emerge from tensions previously thought irreconcilable.

| 矛盾 | 解决方案 | 影响 |
|--------------|------------|--------|
| 一致性AND可用性（分布式系统） | CAP定理：形式化权衡，然后Raft/CRDTs找到实用的中间立场 | 分布式系统理论基础 |
| 安全性AND可用性 | 零知识证明：证明知识而不泄露它 | 启用私有计算 |
| 可表达性AND可处理性 | 概率编程：表达复杂模型，自动化推理 | 新编程范式 |
| 记忆化AND泛化 | Grokking：模型先记忆，然后随着更多训练泛化 | 对学习动力学的新理解 |
| 压缩AND质量 | 神经编码器通过学习先验超越信息论极限压缩 | 重新定义压缩研究 |

| Contradiction | Resolution | Impact |
|--------------|------------|--------|
| Consistency AND Availability (distributed systems) | CAP theorem: formalized the trade-off, then Raft/CRDTs found practical middle grounds | Foundation of distributed systems theory |
| Security AND Usability | Zero-knowledge proofs: prove knowledge without revealing it | Enabled private computation |
| Expressiveness AND Tractability | Probabilistic programming: express complex models, automate inference | New programming paradigm |
| Memorization AND Generalization | Grokking: models memorize first, then generalize with more training | New understanding of learning dynamics |
| Compression AND Quality | Neural codecs that compress beyond information-theoretic limits via learned priors | Redefined compression research |

**辩证思维工作流**：

1. **识别**你领域中的二元对立：A vs. B（两种被视为对立的方法、目标或范式）
2. **拒绝选择一边**。相反，问：
   - 「一个同时实现A和B的系统会是什么样子？」
   - 「在什么条件下A-B权衡不是根本性的？」
   - 「对立是否是我们形式化问题方式的产物？」
3. **寻求综合**：解决方案通常需要重新定义关系的新抽象
4. **测试综合**：你能实证证明两个目标都可以实现吗？

**Dialectical Thinking Workflow**:

1. **Identify a binary** in your field: A vs. B (two approaches, goals, or paradigms treated as opposites)
2. **Resist choosing a side**. Instead ask:
   - "What would a system look like that achieves both A and B?"
   - "Under what conditions is the A-B trade-off not fundamental?"
   - "Is the opposition an artifact of how we formalized the problem?"
3. **Seek synthesis**: The resolution often requires a new abstraction that reframes the relationship
4. **Test the synthesis**: Can you demonstrate empirically that both goals are achievable?

**自检**：
- [ ] 我是否真诚地保持矛盾（而非过早解决）？
- [ ] 综合是新想法，而不仅仅是妥协（各退一步）？
- [ ] 解决方案是否改变了人们对问题的思考方式，而不仅仅是解决方案？

**Self-Check**:
- [ ] Am I holding the contradiction genuinely (not prematurely resolving it)?
- [ ] Is the synthesis a new idea, not just a compromise (splitting the difference)?
- [ ] Does the resolution change how people think about the problem, not just the solution?

---

## 组合框架：创意思维协议 | Combining Frameworks: A Creative Thinking Protocol

这些框架组合起来最强大。以下是深度创意思维会议的系统协议：

These frameworks are most powerful in combination. Here is a systematic protocol for a deep creative thinking session:

### 阶段1：映射空间（15分钟）| Phase 1: Map the Space (15 min)
1. **约束操作**（框架4）：列出当前范式的所有约束。标记哪些是硬的、软的、隐含的。
2. **邻近可能**（框架7）：列出改变可行性前景的最近赋能因素。

### Phase 1: Map the Space (15 min)
1. **Constraint Manipulation** (F4): List all constraints of the current paradigm. Mark which are hard, soft, hidden.
2. **Adjacent Possible** (F7): List recent enablers that change the feasibility landscape.

### 阶段2：生成突破（30分钟）| Phase 2: Generate Disruptions (30 min)
3. **否定**（框架5）：否定3个软/隐含约束。会出现什么系统？
4. **二元联想**（框架1）：选择一个遥远领域，与你的领域创建叉积矩阵。
5. **问题重构**（框架2）：用3种不同方式重述你的问题（改变目标、形式化、主体）。

### Phase 2: Generate Disruptions (30 min)
3. **Negation** (F5): Negate 3 soft/hidden constraints. What systems emerge?
4. **Bisociation** (F1): Pick a distant field and create a cross-product matrix with your domain.
5. **Problem Reformulation** (F2): Restate your problem 3 different ways (change objective, formalism, agent).

### 阶段3：深化有希望的线索（30分钟）| Phase 3: Deepen Promising Leads (30 min)
6. **类比推理**（框架3）：对每个有希望的想法，找到结构性类比并提取预测。
7. **抽象阶梯**（框架6）：将每个想法向上（泛化）和向下（专业化）移动。
8. **雅努斯思维**（框架8）：识别任何张力。你能综合而非选择吗？

### Phase 3: Deepen Promising Leads (30 min)
6. **Analogical Reasoning** (F3): For each promising idea, find a structural analogy and extract predictions.
7. **Abstraction Laddering** (F6): Move each idea up (generalize) and down (specialize).
8. **Janusian Thinking** (F8): Identify any tensions. Can you synthesize rather than choose?

### 阶段4：评估（15分钟）| Phase 4: Evaluate (15 min)
应用两句话测试（来自头脑风暴技能）：
> 「**[领域]目前因[原因]而困扰于[问题]**。我们通过[机制]来[方法]，这之所以有效是因为[洞察]。」

任何通过所有阶段并通过两句话测试的想法都值得追求。

### Phase 4: Evaluate (15 min)
Apply the two-sentence test (from the brainstorm skill):
> "**[Domain] currently struggles with [problem] because [reason].** We [approach] by [mechanism], which works because [insight]."

Any idea that survives all four phases and passes the two-sentence test is worth pursuing.

---

## 常见创意障碍与解锁策略 | Common Creative Blocks and Unblocking Strategies

| 障碍 | 症状 | 应用框架 |
|-------|---------|-------------------|
| **定势** | 无法停止以某种方式思考问题 | 问题重构（框架2）——强制不同的表征 |
| **隧道视野** | 所有想法都来自同一子领域 | 二元联想（框架1）或类比推理（框架3）——从其他地方导入 |
| **自我审查** | 在探索前就认为想法「太奇怪」而否定 | 否定（框架5）——奇怪是重点；在生成后评估 |
| **渐进主义** | 每个想法都是「在基准X上+2%」 | 约束操作（框架4）——改变规则，而非参数 |
| **分析瘫痪** | 选项太多，无法决定 | 邻近可能（框架7）——现在什么是可行的？ |
| **错误二分法** | 困在两种方法之间选择 | 雅努斯思维（框架8）——寻求综合，而非选择 |

| Block | Symptom | Framework to Apply |
|-------|---------|-------------------|
| **Fixation** | Cannot stop thinking about the problem one way | Problem Reformulation (F2) — force a different representation |
| **Tunnel vision** | All ideas come from the same subfield | Bisociation (F1) or Analogical Reasoning (F3) — import from elsewhere |
| **Self-censoring** | Dismissing ideas as "too weird" before exploring | Negation (F5) — weird is the point; evaluate after generating |
| **Incrementalism** | Every idea is "+2% on benchmark X" | Constraint Manipulation (F4) — change the rules, not the parameters |
| **Analysis paralysis** | Too many options, cannot commit | Adjacent Possible (F7) — what is feasible right now? |
| **False dichotomy** | Stuck choosing between two approaches | Janusian Thinking (F8) — seek synthesis, not selection |

---

## 代理使用说明 | Usage Instructions for Agents

当研究人员请求帮助进行创造性思考或新想法构思时：

1. **评估障碍**：他们陷入哪种思维？（见常见创意障碍表）
2. **选择2-3个框架**，基于障碍类型
3. **交互式引导完成每个框架**，要求研究人员提供领域特定内容
4. **推动结构性深度**：如果类比或组合是表面层面的，深入探讨
5. **维护所有生成想法的运行列表**，即使是不寻常的想法
6. **对通过探索的候选想法应用两句话测试**
7. **移交给头脑风暴技能**进行系统评估（发散→收敛→优化）

**关键原则**：
- 先生成模式，后评估模式——不要过早过滤
- 远距离类比比近处类比更有价值，但需要更多验证
- 研究人员的领域专业知识至关重要——代理提供认知脚手架，而非领域知识
- 鼓励研究人员与矛盾共处，而非快速解决

When a researcher asks for help with creative thinking or novel ideation:

1. **Assess the block**: What kind of thinking are they stuck in? (See Common Creative Blocks table)
2. **Select 2-3 frameworks** based on the block type
3. **Walk through each framework interactively**, asking the researcher to supply domain-specific content
4. **Push for structural depth**: If an analogy or combination is surface-level, probe deeper
5. **Maintain a running list** of all generated ideas, even unusual ones
6. **Apply the two-sentence test** to candidates that survive exploration
7. **Hand off to the brainstorm skill** for systematic evaluation (diverge → converge → refine)

**Key Principles**:
- Generative mode first, evaluative mode second — do not filter prematurely
- Distant analogies are more valuable than nearby ones, but require more validation
- The researcher's domain expertise is essential — the agent provides the cognitive scaffolding, not the domain knowledge
- Encourage the researcher to sit with contradictions rather than resolve them quickly
