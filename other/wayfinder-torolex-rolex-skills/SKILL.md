---
name: wayfinder
description: 把一大块工作（超过一个 agent 会话能容纳的体量）规划为 issue tracker 上共享的 decision tickets 的 map，然后逐个解决它们，直到通往 destination 的路清晰可见。
disable-model-invocation: true
---

一个模糊的想法到来了，太大，一个 agent 会话装不下，而且被迷雾包裹：从这里到 **destination** 的路还看不见。Wayfinding 的意义在于找到那条路，而不是冲向 destination。本 skill 把这条路绘制为 repo 的 issue tracker 上的**共享 map**，然后逐个处理它的 **decision tickets**（这些问题的解决是一项 decision，而不是要执行的构建切片），直到路线清晰。

destination 因工作而异，命名它是绘制的第一个动作：它塑造每一个 ticket。它可能是一份要交接并迭代的 spec、一个在规划开始前要锁定的 decision，或一个原地进行的变更，比如数据结构迁移。map 是领域无关的：工程工作、课程内容、任何符合这种形态的东西。

## 规划，而不是执行

Wayfinder 默认是**规划**性质的：每个 ticket 解决一个 decision，当路线清晰时 map 就完成了，在某人去动手之前，没有剩下需要决定的事了。那种"干脆直接去做"的冲动，通常就是你已到达 map 边缘、该交接的信号。一项工作可以在其 **Notes** 里覆盖这一点（把执行本身带进 map），但若没有，就产出 decisions，而不是 deliverables。

## 用名称引用

每个 map 和 ticket 都是一个 issue，所以它有一个**名称**：它的标题。在人类阅读的一切内容里（叙述、map 的 Decisions so far），都要用这个名称来引用它，绝不用裸的 id、编号或 slug。满屏 `#42, #43, #44` 难以阅读；名称一眼就能看懂。id 和 URL 不会消失；名称包住了它的链接，但它们_在_名称内部，绝不代替它。

## Map

map 是本 repo 的 issue tracker 上的一个 issue，标注 `wayfinder:map`，这是规范的工件。它的 tickets 是 map 的 child issues。

map 是一个**索引**，而不是存储。它列出已做出的 decisions，并指向持有其细节的 tickets；一个 decision 只存在于一个地方（它的 ticket），所以 map 从不重述它，只做摘要并链接。

**map、它的 child tickets、blocking 关系和 frontier 查询在物理上位于 tracker 的哪个位置，取决于 tracker 类型。** issue tracker 应该已经提供给你了。如果没有，让用户运行 `/setup-rolex-skills`。查阅 tracker 文档的 "Wayfinding operations" 一节，了解 _本_ repo 如何表达它们。如果没有提供任何 tracker，默认使用 local-markdown tracker。

Tracker 特定的接线细节（原生关系 API、label 命名约定、frontier 查询写法）见 `references/<tracker>.md`。**Charting 之前**先用一次小探测确认 tracker 的原生关系能力（sub-issue / blocked-by / 自定义字段），再批量发 ticket，避免走 body 文字降级；如果只有 body 约定可用，停下来跟用户确认走降级方案。

### Map 正文

整个 map 的低分辨率视图，每个会话加载一次。打开的 tickets **不**列出：它们是打开的 child issues，通过查询找到。

```markdown
## Destination

<到达此 map 终点看起来是什么样：这项工作正在通往的 spec、decision 或变更。一两行；每个会话在选择 ticket 之前都以此定向。>

## Notes

<领域；每个会话应查阅的技能；此工作的常设偏好>

## Decisions so far

<!-- 索引：每个已关闭 ticket 一行，足以判断相关性，然后放大链接查看 ticket 持有的细节 -->

- [<已关闭 ticket 的标题>](link)：<一行答案摘要>

## Not yet specified

<!-- 参见 "Fog of war"：范围之内、你还无法生成 ticket 的迷雾；随着 frontier 推进而 graduate -->

## Out of scope

<!-- 参见 "Out of scope"：被判定超出 destination 的工作；已关闭，永不 graduate -->
```

### Tickets

每个 ticket 都是 map 的一个 **child issue**；tracker 的 issue id 就是它的身份。它的 body 就是问题本身，体量适合一个 100K token 的 agent 会话：

```markdown
## 问题

<此 ticket 要解决的 decision 或调查>
```

每个 ticket 携带一个 `wayfinder:<type>` label，`research`、`prototype`、`grilling`、`task` 之一（见 [Ticket Types](#ticket-types)）。

一个会话通过**先把 ticket 分配**给驱动 map 的开发者来 **claim** 它，在任何工作之前，这样并发的会话会跳过它。那个 assignee _就是_ claim：一个打开、未分配的 ticket 就是未 claim 的。

blocking 使用 tracker 的**原生**依赖关系：这至关重要，因为它让 frontier 在 tracker 自己的 UI 里_可视化地_呈现，人类不用打开 map 就能看到哪些可以领取。只有在 tracker 缺乏原生 blocking 时才回退到 body 约定。当一个 ticket 阻塞它的所有 tickets 都关闭时，它就是 **unblocked** 的；**frontier** 是那些打开、unblocked、未 claim 的 child issues，已知的边缘。

**完成标准**：每个 chart 出来的 ticket 都能在 tracker UI 上查到 frontier（= 已勾选 sub-issue 关系 + 阻塞边），而不是只在 map 的 Decisions so far 文本里或 issue body 文字里看到"Blocks: #N"。Tracker 原生 API / CLI / UI 任一路径都可以，但接线**必须落地到原生关系**，不能停在"我在 body 里写了 Blocks: #N"这种降级方案上。

答案不是 body 的一部分；它在 resolve 时记录（见 [通过 Map 工作](#通过-map-工作)）。resolve 一个 ticket 时创建的资产从 issue 链接出来，而不是粘贴进去。

## Ticket Types

每个 ticket 要么是 **HITL**（人在环中，与一个能为自己发言的人类_一起_工作），要么是 **AFK**，由 agent 独自驱动。一个 HITL ticket 只能通过那种现场交流来解决；agent 绝不代表人类那一方（一个自己回答自己问题的 grilling agent 已经破坏了这一点）。

- **Research**（AFK）：阅读文档、第三方 API 或本地资源（如知识库），以浮现某个 decision 所等待的事实。由调用 Skill 工具并传入 "research" 的 **subagent** 解决。当需要当前工作目录之外的知识时使用。
- **Prototype**（HITL）：通过调用 Skill 工具并传入 "prototype"，制作一个廉价、粗糙、具体的工件（一份提纲、一个粗略想法、一个桩（stub）、或 UI/逻辑代码）来提升讨论的保真度。把 prototype 作为资产链接。当"它应该长什么样"或"它应该怎么表现"是关键问题时使用。
- **Grilling**（HITL）：对话。默认情形。始终调用 Skill 工具两次，分别传入 "grilling" 和 "domain-modeling"。
- **Task**（HITL 或 AFK）：在做出*decision*之前必须完成的动手工作：没有要决定、prototype 或 research 的内容，但讨论被阻塞直到完成。注册服务以便判断它的 API、开通访问权限、移动数据以便看到它的形状。这是唯一种产出**执行方案**而非 decision 的类型：它通过识别要改什么、怎么改、波及范围来解除 decision 的阻塞。它的"解决"是交付一份精确的执行规范（影响文件列表、变更要点、风险、acceptance criteria），**不是实际修改代码**。Agent 在能做到的地方独自驱动（AFK）；否则交给人类一个精确的检查清单（HITL）。当工作完成时解决；答案记录做了什么以及任何后续 tickets 依赖的结果事实（凭据位置、新 URL、行数）。

## Fog of war

map 是_故意_不完整的：不要绘制你还看不到的东西。在活跃的 tickets 之外，是 **fog of war**：你能判断即将到来、但还无法确定的 decisions 和调查的模糊视野，因为它们挂在仍然打开的问题上。解决一个 ticket 会清除它前方的迷雾，把现在可以 spec 化的内容 graduate 成新的 tickets，一次一个，直到通往 destination 的路清晰、不再有 tickets 剩余。

map 的 **Not yet specified** 一节就是写下那个模糊视野的地方：可疑的问题、以后要重新审视的领域。它是_朝向_ destination 的未发现 frontier：这里的一切都在 scope 之内，只是还不够锐化到能生成 ticket。按视野所允许的，写得粗略或完整都可以；它同时充当协作者的路标，让他们看到这项工作朝哪个方向走。

**是迷雾还是 ticket？** 判断标准是你现在能否精确地陈述问题，_不是_你现在能否回答它。

- **是 ticket 当**问题已经锐利，即使它被阻塞、你还不能对它采取行动。
- **是 Not yet specified 当**你还不能把它表述得那么锐利。不要预先将迷雾切成 ticket 大小的块：它比 ticket 更粗颗粒，一块迷雾可能 graduate 成几个 tickets，也可能一个都没有，一旦 frontier 到达它。

**Not yet specified** 排除了已经决定的内容（Decisions so far）、已经是活跃 ticket 的内容，以及 out of scope 的内容（下一节）。

## Out of scope

迷雾只_朝向_ destination 聚集。destination 固定了 scope，所以超出它的工作就是 **out of scope**：它不是迷雾，不属于 **Not yet specified**。它在 map 上有自己独立的 **Out of scope** 一节：你有意识地排除在_这项_工作之外的东西。把它放在这里的是 scope，而不是锐度。

out of scope 的工作从不 graduate（frontier 在 destination 处停止），所以只有当 destination 被重新绘制时它才会回来，而且是以一项全新的工作，而不是恢复。

把某件事划为 out of scope 是一个划定 scope 的行为，不是路线上的一个步骤。当一个已经存在的 ticket 最终落在 destination 之外（绘制时误划入 scope，或由一次 resolution 暴露出来），**关闭它**（一个已关闭的 ticket 明确不在 frontier 上），并在 **Out of scope** 一节留下一行：要点加上它为什么 out of scope，并链接那个已关闭的 ticket。它不进入 **Decisions so far**，后者记录的是实际走过的路线；scope 边界不是路线上的一个步骤。

## 调用

两种模式。无论哪种，**每个会话最多只解决一个 ticket**，research 类型的 ticket 除外，可以在 map 被创建的同一个会话里，立即自动并行启动多个 **Research tickets** 的 subagents。

### 绘制 Map

用户用一个模糊的想法调用。

1. **命名 destination。** 调用 Skill 工具两次，分别传入 "grilling" 和 "domain-modeling"，确定这个 map 正在通往什么：spec、decision 或变更。destination 固定了 scope，所以先解决它。
2. **绘制 frontier。** 再次 grilling，这次**广度优先**：在整个空间展开，而不是在任何一个线程上深挖，浮现出开放的 decisions 和现在可以迈出的第一步。**如果这没有浮现任何迷雾**（通往 destination 的路已经清晰，整个旅程小到一个会话就能装下），你就不需要 map。停下来问用户想怎么继续。
3. **创建 map**（label `wayfinder:map`）：填好 Destination 和 Notes，Decisions so far 为空，把迷雾勾勒进 **Not yet specified**。
4. **创建 tickets 并连接阻塞边**。顺序：
   1. **探测**：用一次小的 GraphQL query（或其他 tracker 等价手段）确认 tracker 暴露的原生关系能力（sub-issue / blocked-by / 自定义字段）。如果只有 body 约定可用，停下来跟用户确认走降级。详见 `references/<tracker>.md`。
   2. **批量发**：用脚本（不是 shell heredoc）批量创建 map + 子 tickets，body 写到临时文件再用 `--body-file`，避免转义陷阱。
   3. **一次接线**：拿到全部 id 后，一次性调用原生 mutation 把 sub-issue + blocked-by 接好。**完成标准**：跑一次 GraphQL query 列出子 tickets 的 `blockedBy`，确认真阻塞关系已落库。

   接线将它们排序为 frontier 和被阻塞；所有你现在还不能明确的内容留在迷雾中：即 **Not yet specified** 部分。
5. **触发 research subagents。** 对你刚创建的每个 `research` ticket，启动一个调用 Skill 工具并传入 "research" 的 subagent 并行解决它，把它的发现捕获到一个一次性的 `research/<name>` 分支上，并从 ticket 留下一个 context pointer。
6. 停止：绘制 map 是一个会话的工作；它不手工解决任何东西。

### 通过 Map 工作

用户用一个 map（URL 或编号）调用。ticket 是**可选的**：没有指定的话，由你来选下一个 decision，而不是用户。

> **约束：** 这是 decision 层工作。任何 ticket 的"解决"产出都是信息（decision、方案、规范）：将答案发布为 resolution comment、关闭 issue、追加到 map 的 Decisions so far，同时将新浮现的内容 graduate 为新 ticket、清除迷雾、处理 out of scope 和无效化部分。代码执行始终在 wayfinder 会话之外进行。

1. 加载 **map**：低分辨率视图，不是每个 ticket 的 body。
2. 选择 ticket。如果用户指定了一个，就用它。否则按顺序取第一个 frontier ticket。**claim 它**：在任何工作开始前把它分配给你自己。
3. 解决它，按 ticket 类型决定"解决"的含义：
   - **Research / Grilling / Prototype**：通过 research、对话或 prototype 来锁定 decision。产出记录在 resolution comment 中。
   - **Task**：**产出执行方案**：分析影响文件、变更要点、风险和执行顺序，写成 resolution comment。**禁止直接修改代码**。执行由后续 feature 分支完成。

   按需获取任何相关或已关闭 ticket 的完整正文；对 `## Notes` 块中指定的 skill 调用 Skill 工具。如有疑问，调用 Skill 工具两次，分别传入 "grilling" 和 "domain-modeling"。
4. 记录 resolution：把答案作为 **resolution comment** 发布，**关闭**该 issue，并把 **context pointer** 追加到 map 的 Decisions so far。（不是以独立评论追加）
5. 添加新浮现的 tickets（先创建、再接线）；将答案已使其 spec 化的迷雾逐一 graduate，把每个已 graduate 的片段从 **Not yet specified** 中清除，让它只作为新 ticket 存在。如果答案揭示某个 ticket（这一个或其他）落在 destination 之外，**把它划为 out of scope**，而不是在路上解决它。如果该 decision 使 map 的其他部分失效，更新或删除那些 tickets。

用户可能会并行运行 unblocked 的 tickets，所以要预期其他会话在并发编辑 tracker。
