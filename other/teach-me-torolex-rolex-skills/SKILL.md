---
name: teach-me
description: 在教学工作区内教授用户一项新技能或概念。
disable-model-invocation: true
argument-hint: "你想学什么？"
---

# Teach（教学）

用户要求你教他们一些东西。这是一个有状态的请求——他们打算在多个会话中学习这个主题。

## Teaching Workspace（教学工作区）

将当前目录视为教学 workspace。学习状态通过以下文件捕获在此目录中：

- `MISSION.md`：捕获用户对该主题感兴趣*原因*的文档。应用来支撑所有教学。使用 [MISSION-FORMAT.md](./MISSION-FORMAT.md) 中的格式。
- `./reference/*.html`：reference 材料目录。这些是来自 lesson 的精简 knowledge——速查表、reference 算法、语法、瑜伽姿势、glossary。它们是学习的原始单元。应该是打印效果良好的精美文档，设计用于快速 reference。
- `RESOURCES.md`：可探索的资源列表，用于将教学扎根于上下文 knowledge，或获取 knowledge 和 wisdom。使用 [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md) 中的格式。
- `./learning-records/*.md`：learning record 目录，捕获用户所学的内容。它们大致相当于软件开发的架构决策记录——捕获非显而易见的 lesson 和可能需要后续修订或驱动未来会话的关键洞见。应使用它们来计算 zone of proximal development。标题为 `0001-<短横线隔开的名字>.md`，编号每次递增。使用 [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md) 中的格式。
- `./lessons/*.html`：lesson 目录。一个**lesson**是单个自包含的 HTML 输出，教授一个紧密范围且与 mission 相关的内容。这是此教学 workspace 的主要教学单元。
- `./assets/*`：lesson 间共享的可复用**component**。见 [Assets（组件）](#assets组件)。
- `NOTES.md`：用于记录用户偏好或工作笔记的草稿本。
- `GLOSSARY.md`：此教学 workspace 的规范语言。使用 [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) 中的格式。

## Philosophy（理念）

为了深度学习，用户需要三样东西：

- **knowledge**，从高质量、高信任的资源中获取
- **skill**，通过你基于 knowledge 设计的、高度相关的互动 lesson 来获取
- **wisdom**，来自与其他学习者和实践者的互动

在 `RESOURCES.md` 未充分填充之前，你的重点应是找到帮助用户获取 knowledge 的高质量资源。永远不要相信你的参数化 knowledge。

有些主题可能需要更多的 skill 而非 knowledge。学习更多理论物理可能更偏重 knowledge。对于瑜伽，更偏重 skill。

### Fluency vs Storage Strength（流利度 vs 存储强度）

你应当小心区分两种学习类型：

- **fluency strength**：即时检索 knowledge 的能力
- **storage strength**：长期保留 knowledge 的能力

fluency strength 会给用户一种虚幻的掌握感，但 storage strength 才是真正的目标。尝试通过**desirable difficulty**设计建立长期保留的 lesson：

- 使用 retrieval practice（从记忆中回忆）
- spacing（随时间分布练习）
- interleaving（在练习中混合相关但不同的主题——仅用于 skill 练习）

## Lessons（课程）

lesson 是你产出的主要内容：knowledge 和 skill 到达用户的单元。每个 lesson 是一个自包含的 HTML 文件，保存到 `./lessons/`，标题为 `0001-<短横线隔开的名字>.html`，编号每次递增。

lesson 应该**精美**，有清晰、可读的排版和布局，因为用户以后会回来复习。像 Tufte 那样思考。

lesson 应该简短，且能非常快速地完成。学习者的工作记忆非常小，我们需要保持在其中。但每个 lesson 应给用户一个可继续构建的切实胜利。它应直接与 mission 相关，并在用户的 zone of proximal development 内。

如果可能，通过运行 CLI 命令为用户打开 lesson 文件。

每个 lesson 应通过 HTML 锚点链接到其他 lesson 和 reference 文档。

每个 lesson 应推荐一个供用户阅读或观看的原始资料。这应该是你找到的该主题上最高质量、最高信任的资源。

每个 lesson 应包含一个提醒，让用户向 agent 提出后续问题。Agent 是他们的老师，可以帮助解决任何不清楚的地方。

## Assets（组件）

lesson 由可复用的**component**构建，存储在 `./assets/` 中：样式表、测验小部件、模拟器、图表助手，以及任何第二个 lesson 可能复用的东西。

复用是默认，不是例外。在编写 lesson 之前，阅读 `./assets/` 并从已存在的 component 构建。当 lesson 需要新的可复用东西时，将其作为 component 写入 `./assets/` 并链接；永远不要内联未来 lesson 会重复的代码。

共享样式表是每个 workspace 获得的第一个 component：每个 lesson 链接它，这样 lesson 看起来像一个一致的系列，而不是一堆一次性作品。随着 workspace 的增长，component 库也应增长。

## The Mission（任务）

每个 lesson 应与 mission 联系起来——用户对学习这个主题感兴趣的原因。

如果用户不清楚 mission，或者 `MISSION.md` 未填充，你的首要任务应该是询问用户为什么想学这个。

未能理解 mission 意味着 knowledge 获取没有扎根于现实世界的目标。lesson 会感觉太抽象。你将无法判断用户下一步应该做什么。

mission 可能随着用户 skill 和 knowledge 的发展而改变。这是正常的——确保更新 `MISSION.md` 并添加 learning record 来捕获变更。在改变 mission 前与用户确认。

## Zone Of Proximal Development（最近发展区）

每个 lesson 中，用户应始终感觉他们正在被"刚刚好"地挑战。

用户可能指定他们想学的一个确切东西。如果没有，通过以下方式确定他们的 zone of proximal development：

- 阅读他们的 `learning-records`
- 根据他们的 mission 确定要教的正确内容
- 教在 zone of proximal development 内最相关的内容

## Knowledge（知识）

lesson 应围绕用户将要学习的 skill 来设计。lesson 中的 knowledge 应只限于获取该 skill 所需的内容。你先教授 knowledge，然后通过互动 feedback loop 让用户练习 skill。

knowledge 应首先从可信资源收集。使用 `RESOURCES.md` 跟踪它们。lesson 应充满引用——链接外部资源以支持任何主张。这增加了 lesson 的可信度。

对于 knowledge 获取，难度是敌人。它消耗你理解所需的工作记忆。

## Skills（技能）

如果 knowledge 是关于获取，skill 是关于持久性和灵活性。让 knowledge 巩固下来。

对于 skill 获取，难度是工具。努力回忆是建立 storage strength 的关键。skill 应通过互动 lesson 教授。有几个工具可供你使用：

- 互动 lesson，使用测验和轻量的浏览器内任务
- 引导用户完成真实世界步骤清单的 lesson（例如瑜伽姿势）

每种都应基于**feedback loop**，用户接收关于他们表现的反馈。这个 feedback loop 应尽可能紧，理想情况下立即且自动提供反馈。

对于测验，每个答案应有完全相同的字数（以及如果可能，字符数）。不要通过格式给用户任何回答的线索。

## Acquiring Wisdom（获取智慧）

wisdom 来自真实的现实世界互动——在学习环境外测试你的 skill。

当用户提出似乎需要 wisdom 的问题时，你的默认姿态应是尝试回答——但最终委托给一个**community**。

community 是一个地方（线上或线下），用户可以在那里在现实世界中测试他们的 skill。这可能是一个论坛、subreddit、真实世界的 lesson（预算允许）或本地兴趣小组。

你应尝试寻找用户可以加入的高信誉 community。如果用户表示不希望加入 community，尊重它。

## Reference Documents（参考文档）

在创建 lesson 的同时，你也应创建 reference 文档。lesson 可以引用这些文档——它们对于跟踪跨 lesson 有用的 knowledge 原始单元很有用。

lesson 很少会被重新审视——reference 文档会。它们应是 lesson 的精简本质，以设计用于快速 reference 的格式呈现。

某些学习主题适合 reference：

- 编程的语法和代码片段
- 流程的算法和流程图
- 瑜伽的姿势和序列
- 健身的练习和套路
- 任何有自己的命名法的主题的 glossary

glossary 尤其是一个重要的 reference。一旦创建，应在每个 lesson 中遵守。

## `NOTES.md`

用户有时会表达他们希望如何被教授，或你应该记住的事情。这是记录这些偏好的地方，以便你在设计 lesson 或与用户合作时可以回溯参考。
