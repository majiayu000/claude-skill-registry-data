---
name: writing-for-agents
description: 为 agent 撰写文档。在创建或编辑 skill，或修改 AGENTS.md 或 CLAUDE.md 时使用。
---

为 agent 消费的任何文档撰写参考：一个 skill、一份 `AGENTS.md` / `CLAUDE.md`、一个由 pointer 到达的文档。打包方式不同；写作方式相同：同样的杠杆让每一份都 predictable（可预测），因为 agent 每次运行采取相同的_过程_，而不是产出相同的输出。

当你写的文档是 skill 时，阅读 [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md) 了解 frontmatter、invocation 选择和 router skills。

## Context pointers（上下文指针）

**context pointer** 是 agent 上下文中持有的一个 reference，它指名一些上下文之外的材料，并编码到达它的条件。skill 的 description 是一个；`AGENTS.md` 中命名某个文档的一行是同一个东西。指针的_措辞_，而不是它的目标，决定 agent 何时到达材料，以及有多可靠。一个必须命中的目标藏在措辞薄弱的指针后面，是一个 variance bug：先锐化措辞，只有锐化失败才内联材料。

指针做两件事：说明材料是什么，并列出应该 trigger 到达它的**branch**（branch 是文档处理的一个独特情况，所以不同的运行走不同的路径穿过它）。一个始终加载的指针的每个词在每个回合都花钱，所以它应受比正文更严格的修剪：

- **把 leading word 放在最前面**：指针是它做触发工作的地方。
- **每个 branch 一个 trigger。** 把单个 branch 改名的同义词是同一个 branch 写了两遍；合并它们，只保留真正不同的 branch。
- **剪掉正文已经携带的身份。**

## The two loads（两种负载）

你添加的每份文档和每个指针都会花费两种预算之一：

- **context load** 是常驻材料在 agent 窗口上的成本：一行 `AGENTS.md`、一个 skill description、任何每个回合都在 context 里的东西，无论是否触发都花费 tokens 和注意力。
- **cognitive load** 是在人身上的成本：存在哪些文档、何时去够取每一份。人是索引。不是要最小化的成本：它是人类主体性的代价；在人的判断重要的地方花它，在不需要它的地方去掉它。

只有通过指针到达的材料，以指针自身那一行为代价逃出 context load；完全没有指针的材料则完全依靠 cognitive load。

## Information hierarchy（信息层次）

一份文档由两种内容类型构建：**steps**（agent 执行的顺序动作）和 **reference**（按需查阅的定义、规则、事实）。两者自由混合：全部是 steps（一份配方）、全部是 reference（一次 review 的规则、本 skill）、或两者兼有。核心决策是每块内容在 **information hierarchy** 上的位置，一个按 agent 需要材料的紧急性排序的 ladder：

1. **in-file step** 是主层级：agent 按顺序做什么。
2. **in-file reference** 按需查阅。通常是一个合理平坦的同级集合（一次 review 的所有规则都在同一级），这是很好的安排，不是坏味道。
3. **disclosed reference** 被推出去放进单独文件，由 context pointer 到达，只在指针触发时加载。范围从同一文件夹的兄弟文件，到住在任何地方、任何文档都能指向的完全 external reference。

推得太少，顶层臃肿；推得太多，你会藏起 agent 真正需要的材料。这个张力就是整个决策。

**progressive disclosure** 是沿 ladder 向下移动的动作（离开主文件、退到指针后面），让顶层保持可读。主要不是 token 优化：它是保护 hierarchy 的方式。**branching**（分支化）是最干净的披露测试：内联每个 branch 都需要的东西，把只有某些 branch 会到达的东西推到指针后面。当文档有 steps 时，本应披露的 in-file reference 会埋葬它们，让注意它们变成掷硬币：这是一个 variance 杠杆，不只是可读性杠杆。

**co-location** 是文件内的同伴：ladder 决定一块内容_落得多深_，co-location 决定它一旦到达那里_旁边坐着什么_。把一个概念的定义、规则和注意事项放在一个标题下，而不是散落各处，这样读一个部分会带上它的邻居。测试：文档应该读起来像专门为 agent 写的文档。分组的内容是这样读的；散落的内容不会。（不同于 duplication：duplication 是在两个地方重复同一个意思；散落是把一个意思碎片化到很多地方。）

**sprawl** 是这里的失败模式：文档只是太长，即使每一行都活跃且唯一。注意力在多余内容上变薄，而每一行额外内容都是要让它保持 relevant 的更多内容。治愈方法是 ladder：把 reference 披露到指针后面，并按 branch 或 sequence 拆分，让每条路径只携带它需要的内容。

## Steps and completion criteria（步骤与完成条件）

每个 step 都以 **completion criterion** 结束，即告诉 agent 工作已完成的条件。两个属性让它成为杠杆：

- **Clarity（清晰度）**：agent 能分辨完成与未完成吗？一个模糊的边界（"已达成理解"）会招来 **premature completion**：在 step 真正完成之前就结束，注意力滑向_装作完成_。前方仍然可见的 steps（**post-completion steps**）提供拉力；criterion 的清晰度是阻力。按顺序防御：**先锐化边界**（局部且便宜）；只有当它不可约地模糊_且_你实际观察到匆忙时，才通过拆分 sequence 来隐藏后面的 steps。而且隐藏只在真实的 context boundary 上起作用（一次 hand-off 或一次 subagent dispatch；内联调用会让后面的 steps 留在 context 里，什么也清不掉）。
- **Demand（需求度）**：它要求多少。"每个被修改的模型都已处理"强制彻底的工作，而"产出一份变更清单"不会。Demand 驱动 **legwork**（agent 在工作内部做的挖掘，潜伏在措辞中而不是写成自己的 step），而且它不受 step 限制："每个规则都已应用"绑定一整块平坦的 reference，正如"每个 step 都已完成"绑定一个 sequence，这正是全 reference 文档仍然携带穷尽性标准的方式。

最强的 criteria 既可检查又穷尽。

## When to split（何时拆分）

把一份文档拆成两份会花费两种 load 中的一种，所以只在拆分值得时才拆：

- **按 sequence 拆分**：拆一段 steps，其中 post-completion steps 会诱惑 agent 匆忙跳过眼前那个 step。让它们保持不可见，会在当前任务上驱动更多 legwork。警惕反面：合并 sequence 会把每个 step 后面的 steps 暴露给接下来要做的，招来 premature completion。
- **按 invocation 拆分**，skill 特有的：见 [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md)。

## Leading words（引领词）

**leading word** 是一个已经存在于模型预训练中的紧凑概念，agent 运行文档时用它思考（_lesson_、_fog of war_、_tracer bullets_）。作为一个 token 反复出现、而不是作为一个句子出现，它累积起一个分布式定义，并以最少的 tokens 锚定一整片行为区域，通过招募模型已经持有的先验（priors）。自己造一个也行，只要你清楚定义它；但一个编造的词招募不到先验：你用定义用的 tokens 支付一个预训练词免费给予的东西；先伸手拿一个现有词。

它双重锚定。在正文里锚定_execution_（执行）：每次这个词出现，agent 都会伸手拿相同的行为，而在平坦的 reference 内部，它把注意力聚焦在一类要找的东西上。在指针里锚定_invocation_（调用）：当同一个词住在你的 prompts、你的文档、你的 codebase 里时，agent 会把那套共享语言与材料关联起来，更可靠地到达它。

寻找用 leading words 重构的机会。一个在三个地方展开的三元组、一个花一句话去指向一个想法的 pointer。每一段都是渴望塌缩成单个 token 的文字：

- "fast、deterministic、low-overhead" → _tight_（一个 _tight_ 循环）。
- "一个你相信的循环" → _red_，把一个模糊的门变成二进制的可观察状态（循环在 bug 上变 _red_，或者不变）。

你赢两次：更少的 tokens，以及一个更锐利的钩子让 agent 挂载它的思考。假设每份文档都携带 leading words 可以取而代之的重复表述。去找它们。

**negation** 是紧挨这个杠杆的失败模式：通过禁令来引导，会把被禁的行为拖进 context，让它_更容易_被获得，而不是更不容易。_别想大象_，然后大象就是一切；negation 是一个弱修饰符，被强烈激活的概念会压过它，所以禁令有一半会被读成"去做那件事"的指令。提示**正面（positive）**：陈述目标行为（"写一行注释"），这样被禁的那个永远不会被说出。禁令只有作为你无法正面表述的硬护栏时才配有一席之地；即便如此，也要把它与正面目标配对，让注意力落在要做什么上。

## Pruning（修剪）

- 让每个意思保持**single source of truth**：一个权威位置，这样改变行为就是一处编辑。**duplication**（同一个意思出现在多个地方）耗费维护成本和 tokens，并把一个意思在 ladder 上的突出程度抬到超过它真实等级的位置。（这是 leading word 的意外反面：leading word 是故意重复一个 token，绝不重复意思。）
- **environment** 也是真相来源（`package.json` scripts、配置文件、目录布局、`--help` 输出），一份重述它的文档是一份 **cache**：一次查找的副本，只有当查找昂贵时才挣得它的 load。缓存 agent 无法通过查找发现的东西：未写下的约定、选择背后的原因、没有任何 config 会坦白的坑。把单文件、单命令的查找留给 environment，在那里它们不会过时。
- 逐行检查**relevance**：它仍然关系到文档在做什么吗？一行会因为从未关系到任务（纯粹的说明，或一个本应被披露的 branch）而失去 relevance，或因为随着它所描述的行为或世界变化而过时（stale）而失去。更短的文档更容易保持 relevant。没有修剪纪律，默认的命运是 **sediment**：陈旧的层沉淀下来，因为添加感觉安全、删除感觉冒险，直到你必须向下钻穿它们，找到仍然活跃的东西。
- 逐句追捕**no-op**：一个模型默认就会服从的指令，花 load 却什么都没说。测试（它相对默认行为是否改变了行为？）是模型相关的，不是读者相关的：两个对一个 no-op 意见不合的人，是不合在默认上，通过运行文档来解决，而不是辩论。当一个句子失败时，删除整个句子，而不是从里面修剪词。这个测试也给 leading words 打分：一个太弱、打不过默认的词（agent 已相当彻底时还说 _be thorough_）是 no-op，修复方法是更强的词（_relentless_），而不是不同的技术。
