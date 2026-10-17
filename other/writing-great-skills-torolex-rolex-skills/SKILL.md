---
name: writing-great-skills
description: Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable.
disable-model-invocation: true
---

# Writing Great Skills（编写优秀的 Skill）

一个 skill 的存在意义是从随机系统中规整出确定性。**predictability**——agent 每次运行采用相同的_过程_，而不是产生相同的输出——是根本美德；下面的每个杠杆都服务于它。

**加粗术语**在 [`GLOSSARY.md`](GLOSSARY.md) 中有定义；在那里查找完整含义。

## Invocation（调用方式）

两个选择，权衡不同的成本：

- **model-invoked** skill 保留**description**，所以 agent 可以自主 trigger 它，_而且_其他 skill 可以 invoke 它（你仍然可以手动输入它的名字）。它贡献于**context load**——description 每轮都在窗口中。机制：省略 `disable-model-invocation`，编写面向模型的 description，包含丰富的 trigger 短语（"当用户想要……、提到……时使用"）。
- **user-invoked** skill 从 agent 的可达范围中移除 description：只有你，输入它的名字，才能 invoke 它——而且没有其他 skill 能。零 context load，但它消耗**cognitive load**：_你_是必须记住它存在的索引。机制：设置 `disable-model-invocation: true`；`description` 变为面向人类——一行摘要，去掉 trigger 列表。

只有当 agent 必须能自行 invoke 该 skill，或其他 skill 必须 invoke 它时，才选择 model-invocation。如果它只通过手动 trigger，使其 user-invoked，不支付 context load。

当 user-invoked skills 多到你记不住时，积累的 cognitive load 由**router skill**治愈：一个 user-invoked skill，列出其他 skill 以及何时使用每个。

## Writing the description（编写 description）

model-invoked 的 **description** 做两件事——说明 skill 是什么，列出应该 trigger 它的**branch**。每个词增加**context load**，所以 description 的修剪比正文更需要严格：

- **把 skill 的 leading word 放在最前面** —— description 是其 invocation 工作的地方。
- **每个 branch 一个 trigger。** 将单个 branch 重命名的同义词是**duplication**——"使用 TDD 构建功能……要求测试优先开发"是一个 branch 写了两遍。合并它们；只保留真正不同的 branch。
- **剪掉正文已包含的身份。** 保持 description 只包含 trigger，加上任何"当其他 skill 需要……"的可达子句。

## Information hierarchy（信息层次）

一个 skill 由两种内容类型构建——**step**和**reference**——它们自由混合：一个 skill 可以全部是 step、全部是 reference、或两者都有。核心决策是使用哪一种，以及每种在**information hierarchy**中的位置，这是一个按 agent 需要材料的紧急性排序的阶梯：

1. **in-skill step** —— `SKILL.md` 中的有序动作，主要层级：agent 做什么，按顺序。每个 step 以**completion criterion**结束，告诉 agent 工作已完成的条件。使其_可检查_（agent 能区分完成与未完成吗？）并且，在必要时，_穷举_（"每个修改过的模型都已处理"，而不是"产生变更列表"）——模糊的标准会导致**premature completion**。
2. **in-skill reference** —— `SKILL.md` 中的定义、规则或事实，按需查阅。通常是一个合法的扁平同级集合（在一个层级上每个审查的所有规则）——很好的安排，不是坏味道。_此 skill 全是 reference。_
3. **external reference** —— 从 `SKILL.md` 推到单独文件的 reference，通过**context pointer**访问，仅在指针 trigger 时加载。（范围从_已披露的_reference——兄弟文件如 `GLOSSARY.md`，仍然是 skill 的一部分——到完全**external reference**，存在于 skill 系统之外，任何 skill 都可以指向。）

严格的 completion criterion 驱动彻底的**legwork**——agent 在工作中的深入挖掘——无论 skill 有没有 step，因为"每个规则都应用了"绑定平面 reference 就像"每个 step 都完成了"绑定序列一样。

往下推得太少，顶部会臃肿；推得太多，你会隐藏 agent 实际需要的材料。这种紧张关系就是整个决策。

**progressive disclosure**是沿阶梯向下移动——从 `SKILL.md` 移出到链接文件中——这样顶部保持可读性。机制：skill 文件夹中的链接 `.md` 文件，以其所持有的内容命名（此 skill 将其完整定义披露给 `GLOSSARY.md`）。有些 skill 以多于一种方式使用，每种不同的方式是一个**branch**——不同的运行走不同的路径通过 skill。branch 是最干净的披露测试：内联每个 branch 都需要的内容，将只有某些 branch 访问的内容推到指针后面。**context pointer**的_措辞_，而不是其目标，决定了 agent 在何时以及以多高可靠性访问材料。

阶梯决定了一个片段在层级中_多深_的位置，而**co-location**则决定了一旦到达那里，_什么与它相邻_：将一个概念的定义、规则和注意事项放在一个标题下，而不是分散的，这样阅读一部分就会带来相邻部分。

## When to split（何时拆分）

**granularity**是你将 skill 划分的精细程度，每次切割消耗两种负载之一，所以只有切割能带来回报时才拆分。两种拆分：

- **按 invocation 方式拆分** —— 当你有一个应该独立 trigger 的**leading word**，或其他 skill 必须 invoke 它时，拆出一个 **model-invoked** skill。你为新的始终加载的 **description** 支付**context load**，所以这种独立可达必须值得。
- **按顺序拆分** —— 当剩余的 step（step 的 **post-completion steps**）诱使 agent 急于完成当前 step（**premature completion**）时，拆分一系列**step**。将它们保持不可见，鼓励 agent 在当前任务上做更多**legwork**。

## Pruning（修剪）

将每个含义保持在**single source of truth**：一个权威位置，这样改变行为是一次编辑。

检查每一行的**relevance**：它仍然与 skill 做的事情相关吗？

然后逐句（不只是逐行）追捕**no-ops**：对每个句子单独运行 no-op 测试，当它失败时，删除整个句子而不是从中修剪单词。要激进——大多数测试失败的散文应被删除，而不是重写。

## Leading words（引领词）

**leading word**是一个已经存在于模型预训练中的紧凑概念，agent 在执行 skill 时用它来思考（例如_lesson_、_fog of war_、_tracer bullets_）。在文本中反复使用（尽管不一定——一个强的 leading word 可能只需要出现一次），它积累了一个分布式定义，并用最少的 token 锚定整个行为区域，通过利用模型已经持有的先验知识。

它两次服务于 predictability。在正文中它锚定_执行_：每次这个词出现时，agent 都会采用相同的行为。在 description 中它锚定_invocation_：当同一个词存在于你的提示、文档和代码中时，agent 将该共享语言与 skill 关联起来，更可靠地 trigger 它。

寻找将 skill 重构为使用 leading word 的机会。在三个位置拼写的三元组（**duplication**），花一个句子来描述一个想法的 description——每一个都是渴望**压缩**为单个 token 的段落。例如：

- "快速、确定、低开销" -> _tight_ —— 一个跨阶段重复的品质 —— 压缩为一个预训练词（一个 _tight_ 循环）。
- "你相信的循环" -> _red_ —— 将一个模糊的门控转换为一个二进制的可观察状态（循环在 bug 上变 _red_，或者没有）。

你赢两次：更少的 tokens，_和_一个更锐利的钩子让 agent 挂载其思考。假设每个 skill 都携带了 leading word 可以退休的重复表述——去找它们。

## Failure modes（失败模式）

用这些来诊断用户可能遇到的 skill 问题。

- **premature completion** —— 在 step 真正完成前结束，注意力滑向_已做完_。防御，按顺序：首先锐化 completion criterion（便宜、局部）；只有它在本质上模糊_并且_你观察到匆忙，才通过拆分隐藏 post-completion steps（顺序切割）。
- **duplication** —— 同一含义出现在多个地方。消耗维护成本和 tokens，并膨胀含义在阶梯上的突出程度超出其实际级别。
- **sediment** —— 因添加感觉安全而删除感觉冒险而沉淀的陈旧层。任何没有修剪纪律的 skill 的默认命运。
- **sprawl** —— skill 太长了，即使每一行都是活跃且唯一的。损害可读性和可维护性，浪费 tokens。解法是阶梯：将**reference**披露到指针后面，并按**branch**或顺序拆分，这样每条路径只携带它需要的内容。
- **No-op** —— 模型已经默认服从的行，所以你支付负载却什么也没说。测试：它是否改变了与默认相比的行为？弱的 leading word（_be thorough_ 当 agent 已经相当 thorough 时）是 no-op；修复是更强的词（_relentless_），而不是不同的技术。
- **negation** —— 通过禁令引导适得其反：_不要想大象_ 命名了大象并使其更易获得，而不是更难。提示**正面**——陈述目标行为，使被禁止的行为从不会被提及；只将禁令保留为无法用正面表述的硬性护栏，即使如此也要配上替代方案。
