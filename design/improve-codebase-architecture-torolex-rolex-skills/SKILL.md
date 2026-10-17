---
name: improve-codebase-architecture
description: 扫描代码库找出 deepening opportunities，以可视化的 HTML report 呈现出来，然后对你挑中的那个进行 grilling。
disable-model-invocation: true
---

# 改善代码库架构

识别出代码库里的架构 friction，并提出 **deepening opportunities**：把 shallow module 变成 deep module 的重构。目标是可测试性和 AI 可导航性。

本命令以项目的 domain model 为依据，并建立在共享的设计词汇之上：

- 调用 Skill 工具，传入 "codebase-design"，获取架构词汇（**module**、**interface**、**depth**、**seam**、**adapter**、**leverage**、**locality**）及其原则（deletion test、「interface 就是测试面」、「一个 adapter = 假想的 seam，两个 = 真实的」）。在每一条建议里都精确使用这些术语，不要滑向「component」「service」「API」或「boundary」。
- `GLOSSARY.md` 里的领域语言为好的 seam 提供了命名；`docs/adr/` 里的 ADR 记录了本命令不应重新审议的 decision。

## 流程

### 1. 探索

**扫描之前先划定范围：YAGNI。** 深化一个 module 的回报在于让未来对它的修改更轻松，所以要格外关注代码库中最近有变动的部分。在开始看之前，先决定看_哪里_：

- 如果用户指明了方向（某个 module、子系统或痛点），就顺着它走，跳过下面的推断。
- 否则，往回翻一段较长的 commit 历史（`git log --oneline`），找出代码库的 hot spots（那些反复出现的文件和区域），让这些路径最先抓住你的注意力。如果改动很分散、没有明显的 hot spot，就放宽范围。

先阅读你将要触及的领域的项目 domain glossary（`GLOSSARY.md`）和任何 ADR。

然后用 `subagent_type=Explore` 的 Agent 工具走一遍代码库。不要死守僵化的启发式规则；要有机地探索，并记下你感到 friction 的地方：

- 在哪里，理解一个概念需要在许多小 module 之间来回跳？
- 哪些 module 是 **shallow** 的，interface 几乎和 implementation 一样复杂？
- 哪里把纯函数抽出来只是为了可测试性，但真正的 bug 却藏在它们的调用方式里（没有 **locality**）？
- 哪些紧耦合的 module 正在穿过它们的 seam 泄漏？
- 代码库的哪些部分没有测试，或者难以通过它们当前的 interface 来测试？

对任何你怀疑是 shallow 的东西应用 **deletion test**：删除它会聚拢复杂性，还是只是把复杂性挪个地方？「是的，会聚拢」就是你想要的信号。

### 2. 以 HTML report 呈现 candidates

把自包含的 HTML 文件写到操作系统临时目录，确保仓库里不留任何东西。临时目录从 `$TMPDIR` 解析，回退到 `/tmp`（Windows 上是 `%TEMP%`），写到 `<tmpdir>/architecture-review-<timestamp>.html`，这样每次运行都会得到一个新文件。为你打开它（Linux 用 `xdg-open <path>`，macOS 用 `open <path>`，Windows 用 `start <path>`），并告诉用户绝对路径。

report 的布局和样式用 **Tailwind via CDN**，在图形/流程/时序能可靠传达结构的地方，用 **Mermaid via CDN** 画图。把 Mermaid 与手工制作的 CSS/SVG 视觉元素混用：当关系呈图状（调用图、依赖、时序）时用 Mermaid，当你想呈现更偏编辑风格的视觉效果（体量图、剖面图、折叠动画）时用手写的 div/SVG。每个 candidate 都要有 **before/after 可视化**。要注重视觉呈现。

为每个 candidate 渲染一张卡片，包含：

- **Files**：涉及哪些文件/module
- **Problem**：当前架构为什么造成 friction
- **Solution**：用平实的语言描述会有什么变化
- **Benefits**：用 locality 和 leverage 来解释，以及测试会如何改进
- **Before / After diagram**：并排、手工绘制的对比图，说明 shallow 之处和深化方式
- **Recommendation strength**：`Strong`、`Worth exploring`、`Speculative` 之一，渲染为徽章

在 report 末尾加一节 **Top recommendation**：你会先处理哪个 candidate，为什么。

**领域用 GLOSSARY.md 的词汇，架构用 `/codebase-design` 的词汇。** 如果 `GLOSSARY.md` 定义了「Order」，就称它为「the Order intake module」，不要说「the FooBarHandler」，也不要说「the Order service」。

**ADR 冲突**：如果某个 candidate 与现有 ADR 矛盾，只有当 friction 真实到值得重新审视该 ADR 时才把它提出来。在卡片里清楚地标注（例如一个警告提示：「_与 ADR-0007 矛盾，但因为……值得重新打开_」）。不要罗列 ADR 禁止的每一个理论上的重构。

完整的 HTML 脚手架、图表模式和样式指引见 [HTML-REPORT.md](HTML-REPORT.md)。

现在还不要提出 interface。写完文件后，问用户：「你想探索其中的哪一个？」

### 3. Grilling 循环

一旦用户选中某个 candidate，调用 Skill 工具，传入 "grilling"，陪用户走一遍 decision tree：约束、依赖、深化后的 module 的形态、seam 后面是什么、哪些测试能存活。

随着 decision 逐渐成形，副作用要即时处理；调用 Skill 工具，传入 "domain-modeling"，让 domain model 始终保持最新：

- **给深化后的 module 起了个 `GLOSSARY.md` 里没有的概念名？** 把这个术语加进 `GLOSSARY.md`。如果文件还不存在，就顺手创建它。
- **对话中把一个模糊的术语厘清了？** 就地更新 `GLOSSARY.md`。
- **用户用一个有分量的理由拒绝了 candidate？** 主动提供一个 ADR，措辞可以是：「_要我把它记成一条 ADR，让以后的架构审查不再重复建议它吗？_」只有当这个理由确实会被未来的探索者用来避免重复建议同一件事时才提出；跳过一时性的理由（「现在不值得」）和不言自明的理由。
- **想为深化后的 module 探索备选的 interface？** 调用 Skill 工具，传入 "codebase-design"，用它的 design-it-twice 并行 sub-agent 模式。
