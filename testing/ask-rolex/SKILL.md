---
name: ask-rolex
description: 询问哪个 skill 或 flow 适合当前场景。本仓库所有 user-invoked skill 的路由器。
disable-model-invocation: true
---

# Ask Rolex

你不必记住每个 skill，问 **`/ask-rolex`** 就行：根据当前场景选入口和下一步。

**调用边界**：下文 `/skill` 是导航标签。user-invoked 入口只向用户建议手动调用，不由 agent 自动启动；model-invoked skill 可由 agent 用 Skill 工具加载，每次传入一个名称。以各 skill 的 `disable-model-invocation` flag 为准。

需要查看完整的分阶段流程图、辅助场景和 skill 链接时，读 [Skill 使用地图](../../../docs/skill-map.md)；这里负责路由判断，不重复维护大段图。

一个 **flow** 是一条贯穿多个 skill 的路径。大部分路径沿着一条 **main flow** 走，几条 **on-ramp** 汇入其中。其余的都是 standalone，或者是一个在底层运行的词汇层。

## main flow：想法 → 交付

大多数工作走的路线。你有一个想法，想把它做出来。

- **整段任务模糊，不知道缺什么、想要什么或哪些决策待定？** 建议用户手动调用 **`/unknowns`**：它按四象限编排盲点扫描、候选探索（需要实物时做 prototype）和访谈收敛，交付 unknowns map，而不是直接实现。地图交给用户后，按需继续 `/grill-with-docs`，或把已确认的决定带入 `/to-plan`、`/to-spec`；构建是另一件任务。这是完整澄清入口，下面两个单项分支是替代入口，不是再跑一遍的必经关卡。

0. **分支：只需扫描陌生地带的盲点吗？** 如果它落在 codebase 里你没碰过的区域，或者一个你不熟悉的领域（一种没接触过的技术、一类没做过的设计），先用 **`/blind-spot-pass`**（model-invoked，agent 可用 Skill 工具加载）：把你的 **unknown unknowns** 翻出来讲清楚，再带着发现进入候选探索或步骤 1。熟悉的领域直接跳过——它的价值与你的盲区成正比。
0.5. **分支：判断标准是看到才认得的吗？** 如果你不知道有哪些可能，或者标准说不出来但看到能认出（审美、口味、"就要这个感觉"），先 **`/brainstorm`** 发散：列举介入点，或产出多个截然不同的方向交给 prototype 供你反应。grilling 中途发现剩下的决策要看到实物才能定时，也会转手调用它。
1. **`/grill-with-docs`** 通过 interview 打磨想法。只要你在**工作目录**里工作，就从这里开始：它是有状态的，会把学到的东西保留在 `GLOSSARY.md` 和 ADR 中。（没有工作目录？改用 `/grill-me`，见 Standalone。两者运行同一个 `/grilling` 原语；`grill-with-docs` 是会留下书面痕迹的那个，所以只要有仓库可以留下痕迹，它就是两者中更好的那个。）
2. **分支：你能在对话中解决每个问题吗？** 如果一个问题需要可运行的答案（状态、业务逻辑、一个你必须亲眼看到的 UI），就绕行一个 prototype，用 **`/handoff`** 双向桥接（prototype 住在自己的目录里，这正是 `/handoff` 的用途；见 Phase boundaries）：
   - **`/handoff`** 转出，然后针对那个文件开一个新的 session，
   - **`/prototype`** 用 throwaway 代码回答那个问题，
   - **`/handoff`** 把你学到的东西转回来，并从原始想法线程引用它。
3. **分支：这是多 session 构建吗？** 想在动手前先审阅关键决策，就在 spec 之前跑一次 **`/to-plan`**：它把最可能变的决策（data model、type interface、UX flow）置顶供你反应，机械性重构沉底。
   - **是** → **`/to-spec`**（把线程变成一份 spec），然后 **`/to-tickets`** 把它拆成 tracer-bullet tickets，每个都声明自己的 **blocking edges**。然后用两种方式之一推进 tickets：
     - 对每个 ticket 跑 **`/implement`**，**每两个之间 `/clear` context**。在本地 tracker 上，就是 `.scratch/<feature>/issues/` 下每个 ticket 一个文件，按 blocker 优先手工推进；在真实的 tracker 上，这些 edges 变成原生的阻塞链接，所以任何 blocker 都已完成的 ticket 都可以被拿走。每个 ticket 都是自包含的，所以上一个 ticket 的 context 是可以随手丢弃的。
     - 用 **`/implement-spec`** 一次跑完整个 spec。它把 tickets 读成一张 **task graph**，在就绪的 **frontier** 上并行跑 implementer subagent，把所有东西落到一个 **integration branch** 上。当你更想编排整个构建、而不是亲自驱动每个 ticket 时，用它。

   **拆票后想复核切片边界？** 在 `/to-tickets` 或 `/triage` 得到 agent-ready tickets 后、推进前，建议用户手动调用 **`/vertical-slice-review`**。它逐票核验是否贯穿 schema/API/UI/tests、能否独立 demo、是否能放进一个 context window，并核对 blocking edges；必要时重拆并由强模型顾问复核。确认后的方案再交 `/implement`、`/implement-spec` 或 `/afk-issue-loop`，不是交付后的代码 review。

   **开始多步骤交付时**，agent 可用 Skill 工具加载 **`/pre-implement`**：为当前任务新建 `.agents/notes/<task-slug>-implementation-notes.md`，随实现记录决策与原因；偏离 plan/spec 时选保守方案并记录 Deviations。它伴随 `/implement` 或 `/implement-spec` 的交付，不替代 spec、tickets 或测试。单行为不需要完整 spec 时，可在同一 context 中建议用户手动调用 `/implement` 就地完成。

   无论走哪条路，代码都是靠 **`/tdd`**（一次一个 red → green 切片）构建、用 **`/code-review`**（对 diff 做一次双轴 review：Standards + Spec）收尾的。`/implement` 对每个 ticket 都运行这两者；`/implement-spec` 的每个 implementer 各自驱动 `/tdd`，最后在 integration branch 上跑一次 `/code-review`。当你只想以 test-first 的方式构建一个具体行为、不需要完整 spec 时，单独使用 **`/tdd`**；当你想针对某个 fixed point review 一个 branch 或 PR 时，单独使用 **`/code-review`**。

   当工作以 pull request 的形式提交时，**`/pr`** 负责打磨 body：展示这次改动的最小可视化（diagram、diff-sketch 或文件树）、证明它可用的 before/after 证据，以及单向/双向门（one-way/two-way door）判断。它是 model-invoked 的，所以 agent 每次写 PR 时都会伸手去够它。

   **实现完成、想确认自己真正理解变更再合并？** 建议用户手动调用 **`/quiz-me`**：先出 HTML 报告，讲清背景、直觉、改动和依赖的既有 code path，再一次一题测验。只有用户触发后，满分才成为 merge 门禁；它不替代 `/code-review`，也不是所有交付的强制步骤。

   **成果需要 reviewer 或专家的 buy-in／批准？** 建议用户手动调用 **`/to-pitch`**，把 prototype、spec 与 implementation notes（尤其 Deviations）打包成可直接分享的文档：demo 在前，explainer 补背景，pitch 说明未知与失败点如何处置。它可用于 PR 描述等目的地，但与 `/pr` 的文案打磨职责不同，也不依赖 `/retro`。

4. **`/retro`** 闭环。一次构建之后——尤其是走得磕磕绊绰的那次——它回看这个 session，针对 agent 的**环境**而不是代码提出改进：navigation 指针、自动化检查、`/code-review` 强制执行的 coding standards、steering 文件、工具链。机械性错误变成确定性检查；判断性取舍变成 coding standards。下一次构建就从一个更好的环境开始。

### context hygiene

把步骤 1–3 保持在**一个不间断的 context window** 里（在 `/to-tickets` 完成之前不要 compact 或 clear），这样 grilling、spec 和 tickets 都建立在同一套思考之上。每个 `/implement` 随后从 ticket 出发、全新开始。`/retro` 要在它所回看的那个 session 里、clear 之前运行；clear 之后，就让它指向那个 session 的日志。

这个做法的上限是 **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**：模型仍能敏锐推理的 context window（在最新模型上约 150k tokens）。如果 session 在 `/to-tickets` 之前逼近这个上限，不要在降级状态下硬撑；在最近的 phase boundary 处 **`/compact`**，然后继续（见 Phase boundaries）。

## On-ramps

一种产生工作、然后汇入 main flow 的起始场景。

- **bug 和请求堆积** → **`/triage`**。它把 issue 推过各个 triage role，产出 agent-ready 的 issue，后续由 **`/implement`** 拾取。

  triage 只用于**不是你创建的** issue：bug 报告、外部进来的功能请求、任何原始到达的东西。`/to-tickets` 产出的 tickets 已经是 agent-ready 的，所以**不要对它们做 triage**。

- **有东西坏了** → **`/diagnosing-bugs`**。用于那些难啃的：第一眼看不出来的 bug、间歇性的 flake、在两个已知良好状态之间悄悄溜进来的 regression。在建立起**紧密的 feedback loop**（一条已经在这_个_ bug 上变红的命令）之前，它拒绝空想，然后用一条 regression test 修复。当真正的发现是没有好的 seam 能把 bug 锁住时，它的 post-mortem 会交接给 **`/improve-codebase-architecture`**。

- **一个巨大而模糊（foggy）的工程量：绿地项目，或一个超大功能构建，一个 session 装不下** → **`/wayfinder`**，这是这里认知负担最重的 flow。当从这里到 destination 之间的路还看不见时，它会在 issue tracker 上绘出一张由 **decision tickets** 组成的**共享 map**，并一次一个地解决它们，产出的是 **decisions，而不是 deliverables**，直到 fog 被推回去、路线清晰。**`/grill-with-docs`** 打磨的是你能在一个 session 里握住的想法，wayfinder 针对的则是你握不住的那种，而且它更慢、更密，所以只把它留给那种情况，绝不要用于一个范围清晰的功能。

  当 map 清晰之后，**它做 handoff，而不是构建**：在 **`/to-spec`** 处汇入 main flow，后者把 map 上相互链接的 decisions 折叠成一份可构建的计划，然后照常走 `/to-tickets` 和 `/implement`。把 map 直接循环进 `/implement` 会跳过那个折叠、丢掉相互链接的细节，所以只有当工程量确实很小的时候，才直接去 `/implement`。

## 代码库健康

不是功能工作，只是维护。

- **`/improve-codebase-architecture`** 只要你有空闲时间就运行它，让代码库保持对 agent 友好、适合在其中操作。它会浮出 **deepening opportunities**（加深机会）；挑中一个就_产生一个想法_，你可以把它带进 main flow 的 `/grill-with-docs`。它是找出候选者的勘察；**`/codebase-design`**（见下）是你设计所选对象的工作台。

## 底层词汇

两个 model-invoked 的参考，运行在其他 skill 的_下层_，各自是自己词汇的唯一权威来源。当问题出在**词语**而不是流程上时，直接伸手去拿它们；或者让上面的 skill 把它们拉进来。

- **`/domain-modeling`**：打磨项目的_领域_语言：挑战一个模糊的术语，解决一个过载的词（一个 "account" 干三份活），把难以逆转的 decision 记录成一条 ADR。它是 `/grill-with-docs` 驱动的主动纪律，让 `GLOSSARY.md` 保持为一份干净的 glossary。
- **`/codebase-design`** 是用于设计模块_形状_的 deep module 词汇（module、interface、depth、seam、adapter、leverage、locality）：大量行为藏在干净 seam 上的一个小 interface 后面。`/tdd` 和 `/improve-codebase-architecture` 都讲这门语言。

## Phase boundaries

一个 **phase** 是 session 内的一块工作：grilling、实现、QA。在它们两者之间的 **boundary** 上，你有五个选项，而在它们之间做选择，是整个 map 里最模糊的一个 decision：

- **Continue（继续）**：原地不动。不花任何成本，也不损失任何东西。
- **`/clear`**：清空 context window，当这里没有任何东西对接下来重要时。
- **`/handoff`** 写一个可移植的 markdown 文件。范围很窄：只用于**新的 harness**、**新的目录**、**一位同事**，或**在 phase 中途**分叉一个旁支任务。它换来的是可移植性。
- **sub-agent**：把一个严格限定范围的任务送到它自己的窗口，拿回一份报告。
- **`/compact`** 压缩当前 context，并用它开启一个新的 session。**默认选项**，在树的底部，而不是最先伸手就能拿到的地方。

阅读 [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) 了解那棵有序的树：五个问题、每个分支背后的推理，以及为什么 primary-source 的成本让 **Continue** 成为最先被排除的那个。要在 boundary 处做 decision；在 phase 中途，要么继续，要么把其余部分拆给 sub-agent。

## Standalone

完全脱离 main flow。

- **`/grill-me`**：和 `/grill-with-docs` 同样不留情面的 interview，但**无状态**：它不在本地保存任何东西，也不构建 `GLOSSARY.md`。当你**不在工作目录里**工作时使用它（打磨一份计划、一个设计、一段文字，任何底下没有 repo 的东西）。如果你在工作目录里，就改用 `/grill-with-docs`：它运行同样的 interview 并留下书面痕迹，所以严格来说它是更好的那个。
- **`/grilling`** 是 interview 原语本身：轮次（rounds）、frontier，事实是 agent 的职责，decision 是你的。`/grill-me` 和 `/grill-with-docs` 是两个具名的进入方式，`/triage`、`/wayfinder` 和 `/improve-codebase-architecture` 内部都在运行它。只有当你想直接要一场不带任何包装的 interview 时，才直接伸手去拿它。
- **`/prototype`** 是一个小的、throwaway 的程序，回答一个设计问题：这个状态模型感觉对吗，或者这个 UI 应该长什么样。throwaway 是对代码书写方式的一种约束，而不是销毁它的承诺：答案会融入真实的代码，prototype 本身则作为 **primary source** 保存在 main 之外的 `prototype/<name>` 分支上，由实现 issue 指向它。它是 main flow 第 2 步里的那个绕行，但任何时候一个设计问题难以在纸面上定夺，都可以使用它。
- **`/research`**：把阅读的跑腿活委托给一个 **background agent**：它对照 **primary sources** 调查一个问题，然后在仓库里留下一份带引用的 Markdown 文件。它阅读的时候你继续干活。它产出的文件，是要带_进_ main flow、供 `/grill-with-docs` 使用的东西，因为 research 喂养思考，而不是取代思考。
- **`/to-questionnaire`**：当挡住你的东西不在你脑子里、也不在代码库里，而是在**别人的**脑子里时，这个 skill 会写一份问卷给他们去填。它是 `/grill-me` 的反面：它不是就那个主题采访你，而是采访你关于**发送（send）**（发给谁、你需要拿回什么），并把问题对准那个缺口。拿回来的东西，是 `/grill-with-docs` 或 `/to-spec` 的素材。
- **`/wizard`** 用于那些只有**人类**才能完成的步骤：开通基础设施、设置凭据或 CI secrets、在一个陌生的第三方 dashboard 里点来点去、运行一次性的迁移或切换。它生成一个交互式 bash 脚本，打开每个 URL、捕获每个值，并写进 `.env` 和 GitHub secrets，这样那套流程就不再是每次都需要你向 agent 重新解释的东西了。它是 model-invoked 的，所以 agent 一撞上只有你能通过的墙，就会伸手去够它。如果 agent 能自己做，它就应该自己做；这个 skill 是为真正有 human in the loop 的情况准备的。
- **`/wait-what`** 是针对一条没能落地的消息的矫正。对话中途、任何其他 skill 里没听懂时，建议用户手动调用，agent 会用你缺失的 context、用通俗易懂的语言、用 `GLOSSARY.md` 的词汇，重新讲解它刚刚说的话。它是事后生效的；`/grill-with-docs` 是事前的治愈，因为早早约定好的共享语言，才正是阻止行话出现的东西。
- **`/teach-me`**：跨多个 session 学习一个概念，把当前目录当作一个有状态的工作区。
- **`/writing-for-agents`** 是编写 agent 消费的文档时的参考：skills、AGENTS.md、被指向的文档。
- **`/writing-great-skills`**：编写和编辑 skill 时，建议用户手动调用的参考指南；agent 需要自主到达文档写作纪律时，用 model-invoked 的 `/writing-for-agents`。
- **`/afk-issue-loop [issue numbers]`**：在 `/to-tickets` 或 triage 后，需要无人值守批量交付时，建议用户手动调用。入口仅解析输入并启动独立本地脚本，报告 started、运行身份、日志和 stop；脚本通过 CLI 执行当前全部就绪票的固定批次、不补位，逐票独立审查，批末单 Merger 汇总关闭；剩余全 blocked 且无在途或可推进交付时报告并结束。确认启动后可结束发起会话，启动不等于交付。输入、Provider 配置与失败续做边界见 [执行规范](../../personal/afk-issue-loop/SKILL.md)。
- **`/clean-branches`**：清理本地和远程已合并的 Git 分支；model-invoked，agent 可加载。用于合并后的 Git 运维，不是 `/retro` 的产物。

## 前置条件

**`/setup-rolex-skills`**：在第一个工程 flow 之前，建议用户手动调用，配置其他 skill 所假定的 issue tracker、triage 标签和文档布局。自定义 issue tracker 也能用。

## 跨流程辅助

- **浏览器或网页任务**（搜索、读取 URL、交互、抓取、诊断）→ agent 用 Skill 工具加载 **`/browser-tools`**，由它选工具、交接与失败回退。它为 `/research` 等需要网页证据的工作提供工具路由，不取代调研流程。
- **gh / GitHub API 请求** → 发请求前，agent 用 Skill 工具加载 **`/github-api-rate-limits`**，尤其分页、循环或批量调用，以及遇到 403/429、RATE_LIMITED 或 Retry-After 时。它管理 REST / GraphQL 独立预算与限流恢复，是 `/triage`、`/to-tickets`、PR 操作等使用 GitHub 时的护栏，不是新交付阶段。
- **强模型顾问**：目标不清、高影响多方案、关键权衡不明时，建议用户手动调用 **`/ask-advisor`**，把当前决策点、约束和上下文交给强模型顾问；拿到建议后继续原来的澄清、规划或实现流程。这里的入口是 skill，而不是绕过它直接派顾问 Agent。
- **下一步建议**：想知道最自然的后续请求时，建议用户手动调用 [next-steps](../../personal/next-steps/SKILL.md)：预测最多三个请求，展示标题与完整 prompt，回复编号直接执行。它留在当前会话，不做待办规划；转移到新的 agent 或新 context 用 **`/handoff`**。调用采用当前宿主真实语法（pi：`/skill:next-steps`）。
