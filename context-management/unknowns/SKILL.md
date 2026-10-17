---
name: unknowns
description: 实现前走完四个象限，通过盲点扫描、头脑风暴、原型和访谈，交付一份 unknowns map。
disable-model-invocation: true
---

# Unknowns

地图不是疆域。prompt、计划和 context window 是地图；codebase、领域和用户真正的意图是疆域。两者之间的差就是 unknowns。写代码之前发现的 unknown 只花几分钟；三个 PR 之后才发现，代价就是那三个 PR。

本 skill 是一场被引导的对话：**quadrant walk**。你和用户一起填写任务的四象限地图，一次一个象限，用户走完时手里拿着完成的地图。地图是交付物；实现是另一件任务，只在地图交出去之后才开始。

每个阶段都用两个动作：

- **Reacting beats imagining。** 能把具体的东西交到用户手里时，就不要求用户描述自己想要什么：一个渲染好的选项、一个可点击的 mock、一张 decisions table。反应能抽出用户拥有、但无人提示就说不出来的知识。
- **每个 artifact 都预组装回复。** 每个 artifact 结尾都写好用户的下一条消息：steal/skip chips、resonate checkboxes、一张 decisions table、一条可复制的 sharpened prompt。用户的反应几乎不用打字，就变成下一条消息。

## Quadrant Walk

五段，按顺序走，一次一段。**进入一段时，先读它的 reference，再照着做。** 走的时候说出当前象限：用户始终知道自己站在地图的哪里。眼前这一段走完，再打开下一段；stage 4 的显式暂停交接可提前进入 stage 5 保存进度，但不算本次 walk 完成。

1. **[Known knowns](references/stage-1-known-knowns.md)**：扫一遍疆域，然后用已经定下来的地面开场。
2. **[Unknown unknowns](references/stage-2-unknown-unknowns.md)**：执行 `blind-spot-pass`，先发现盲点和缺失的领域知识。
3. **[Unknown knowns](references/stage-3-unknown-knowns.md)**：调用 `brainstorm`，需要实物时调用 `prototype`，抽出口味和 tacit context。
4. **[Known unknowns](references/stage-4-known-unknowns.md)**：调用 `grilling` 和 `domain-modeling`，收敛前面浮现的决策。
5. **[Hand over the map](references/stage-5-hand-over-the-map.md)**：完成的四象限地图。这是整场 walk 唯一的完成条件。

用户难以表达目标、缺少领域词汇，或行为需要参考实现才能说清时，读取 [References](references/references.md)。这条分支可在任意阶段触发：先询问用户，用户委托时再派子代理寻找。

调用型 skill 用 Skill 工具加载；标为 `disable-model-invocation: true` 的 skill 用文件链接读取并执行其正文，不尝试自动调用。`grill-with-docs` 的组合在 stage 4 直接写成调用 `grilling` 和 `domain-modeling`，不修改 Matt 的 skill。

用户接着去构建、review 或 merge 这场 walk 画过的东西时，读 [walk 之后](references/after-the-walk.md)。地图在规划结束之后继续活着。

四象限的地图和阶段完成条件沿用 dzhng 的 [explore-unknowns](https://github.com/dzhng/skills/tree/c7957020f9fcb7321dbc339428b41cdff67c9637/skills/engineering/explore-unknowns)；阶段顺序按 Thariq 文章调整为先教学扫盲、再对具体候选反应、最后访谈收敛。必要的目标澄清可以提前；正式访谈不要求用户在看见候选前凭空定义口味。

## Rules

- 按顺序走象限，一次一段，说出当前象限。各阶段正常完成且地图交到用户手里时，walk 才完成。暂停交接的阶段性地图只保存进度，恢复时回到未完成阶段。没有地图，就没完成。
- 阶段只给 walk 排序，不封存信息。一条发现只要实质影响正在做的决定，拿到的那一刻就披露，再按它所属的象限记到地图上。不为了等它那一段的轮次而扣住。
- 没有东西在屏幕外关闭。地图上记成已关闭的问题和判断，必须先给用户看过，包括疆域自己给出答案的那些。
- 把事项关闭成决定，而不是讨论。每个 resolved unknown 收成一行决定加它的 why，措辞让 spec 能原样带走，当作给定。影响已确认目标、约束或产品合同的承重决策，不应留给实现者默默补全。明确授权的实现细节、非阻塞 OPEN 和后来才可发现的未知可以保留，但必须标明边界；完成地图不等于穷尽所有未知。
- 关于疆域的说法引用真正读过的文件；编出来的数据就标明是编的。一个伪造的具体细节会毁掉地图的权威。
- HTML artifact 是自包含的单文件：CSS/JS 内联，不发外部请求，用像样的假数据，不用 lorem ipsum。
- 在每个需要用户反应的阶段边界停下。不要凭未经确认的猜测冲进实现。实现是另一件任务，从交出去的地图开始。
