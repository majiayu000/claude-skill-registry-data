---
name: ml-paper-writing
description: Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, verifying citations, or preparing camera-ready submissions. Includes LaTeX templates, reviewer guidelines, and citation verification workflows.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Academic Writing, NeurIPS, ICML, ICLR, ACL, AAAI, COLM, LaTeX, Paper Writing, Citations, Research]
dependencies: [semanticscholar, arxiv, habanero, requests]
---

# 顶级 AI 会议的机器学习论文写作 | ML Paper Writing for Top AI Conferences

针对 **NeurIPS、ICML、ICLR、ACL、AAAI 和 COLM** 的出版级论文写作专家级指导。本技能结合了顶尖研究者（Nanda、Farquhar、Karpathy、Lipton、Steinhardt）的写作理念与实用工具：LaTeX 模板、引用验证 API 和会议清单。

Expert-level guidance for writing publication-ready papers targeting **NeurIPS, ICML, ICLR, ACL, AAAI, and COLM**. This skill combines writing philosophy from top researchers (Nanda, Farquhar, Karpathy, Lipton, Steinhardt) with practical tools: LaTeX templates, citation verification APIs, and conference checklists.

## 核心理念：协作式写作 | Core Philosophy: Collaborative Writing

**论文写作是协作的，但 Claude 应该主动提供草稿。**

The typical workflow starts with a research repository containing code, results, and experimental artifacts. Claude's role is to:

1. **理解项目**：探索仓库、结果和现有文档
2. **提供完整初稿**：当对贡献有信心时
3. **搜索文献**：使用网络搜索和 API 查找相关引用
4. **通过反馈循环完善**：当科学家提供输入时
5. **仅在真正不确定关键决策时请求澄清**

**关键原则**：要主动。如果仓库和结果清晰，就提供完整草稿。不要阻塞等待每个部分的反馈——科学家很忙。提供一些具体的东西让他们回应，然后根据他们的反馈迭代。

---

## ⚠️ 关键：绝不捏造引用 | CRITICAL: Never Hallucinate Citations

**这是 AI 辅助学术写作中最重要的规则。**

### 问题 | The Problem
AI 生成的引用有 **约 40% 的错误率**。捏造的参考文献（不存在的论文、错误的作者、不正确的年份、伪造的 DOI）是严重的学术不端行为，可能导致直接拒稿或撤稿。

AI-generated citations have a **~40% error rate**. Hallucinated references—papers that don't exist, wrong authors, incorrect years, fabricated DOIs—are a serious form of academic misconduct that can result in desk rejection or retraction.

### 规则 | The Rule
**绝不要凭记忆生成 BibTeX 条目。始终通过编程获取。**

**NEVER generate BibTeX entries from memory. ALWAYS fetch programmatically.**

| 行动 | ✅ 正确 | ❌ 错误 |
|--------|-----------|----------|
| 添加引用 | 搜索 API → 验证 → 获取 BibTeX | 凭记忆写 BibTeX |
| 不确定某篇论文 | 标记为 `[CITATION NEEDED]` | 猜测参考文献 |
| 找不到确切论文 | 注明：“占位符 - 需验证” | 捏造听起来相似的论文 |

### 当无法验证引用时 | When You Can't Verify a Citation

如果无法通过编程验证引用，你**必须**：

If you cannot programmatically verify a citation, you MUST:

```latex
% 明确的占位符 - 需要人工验证
\cite{PLACEHOLDER_author2024_verify_this}  % TODO: 验证此引用是否存在
```

**始终告诉科学家**：“我已将 [X] 个引用标记为需要验证的占位符。我无法确认这些论文是否存在。”

**Always tell the scientist**: "I've marked [X] citations as placeholders that need verification. I could not confirm these papers exist."

### 推荐：安装 Exa MCP 用于论文搜索 | Recommended: Install Exa MCP for Paper Search

为了最佳的论文搜索体验，安装 **Exa MCP** 提供实时学术搜索：

For the best paper search experience, install **Exa MCP** which provides real-time academic search:

Claude Code:
```bash
claude mcp add exa -- npx -y mcp-remote "https://mcp.exa.ai/mcp"
```

**Cursor / VS Code**（添加到 MCP 设置）:

**Cursor / VS Code** (add to MCP settings):
```json
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

Exa MCP 支持搜索示例：

Exa MCP enables searches like:
- "查找 2023 年后发表的 RLHF 语言模型论文" | "Find papers on RLHF for language models published after 2023"
- "搜索 Vaswani 的 transformer 架构论文" | "Search for transformer architecture papers by Vaswani"
- "获取关于稀疏自编码器和可解释性的最新工作" | "Get recent work on sparse autoencoders for interpretability"

然后通过 Semantic Scholar API 验证结果并通过 DOI 获取 BibTeX。

Then verify results with Semantic Scholar API and fetch BibTeX via DOI.

---

## 工作流 0：从研究仓库开始 | Workflow 0: Starting from a Research Repository

开始论文写作时，首先理解项目：

When beginning paper writing, start by understanding the project:

```
项目理解 | Project Understanding:
- [ ] 步骤 1：探索仓库结构 | Step 1: Explore the repository structure
- [ ] 步骤 2：阅读 README、现有文档和关键结果 | Step 2: Read README, existing docs, and key results
- [ ] 步骤 3：与科学家一起确定主要贡献 | Step 3: Identify the main contribution with the scientist
- [ ] 步骤 4：查找代码库中已引用的论文 | Step 4: Find papers already cited in the codebase
- [ ] 步骤 5：搜索其他相关文献 | Step 5: Search for additional relevant literature
- [ ] 步骤 6：共同概述论文结构 | Step 6: Outline the paper structure together
- [ ] 步骤 7：迭代起草各部分 | Step 7: Draft sections iteratively with feedback
```

**步骤 1：探索仓库 | Step 1: Explore the Repository**

```bash
# 理解项目结构 | Understand project structure
ls -la
find . -name "*.py" | head -20
find . -name "*.md" -o -name "*.txt" | xargs grep -l -i "result\|conclusion\|finding"
```

寻找以下内容：

Look for:
- `README.md` - 项目概览和声明 | Project overview and claims
- `results/`, `outputs/`, `experiments/` - 关键发现 | Key findings
- `configs/` - 实验设置 | Experimental settings
- 现有的 `.bib` 文件或引用参考 | Existing `.bib` files or citation references
- 任何草稿文档或笔记 | Any draft documents or notes

**步骤 2：识别现有引用 | Step 2: Identify Existing Citations**

检查代码库中已引用的论文：

Check for papers already referenced in the codebase:

```bash
# 查找现有引用 | Find existing citations
grep -r "arxiv\|doi\|cite" --include="*.md" --include="*.bib" --include="*.py"
find . -name "*.bib"
```

这些是相关工作的高信号起点——科学家已经认为它们相关。

These are high-signal starting points for Related Work—the scientist has already deemed them relevant.

**步骤 3：澄清贡献 | Step 3: Clarify the Contribution**

在写作之前，明确与科学家确认：

Before writing, explicitly confirm with the scientist:

> "根据我对仓库的理解，主要贡献似乎是 [X]。关键结果显示 [Y]。这是您想要的论文框架吗，还是应该强调不同的方面？"

> "Based on my understanding of the repo, the main contribution appears to be [X]. The key results show [Y]. Is this the framing you want for the paper, or should we emphasize different aspects?"

**绝不要假设叙述——始终与人类验证。**

**Never assume the narrative—always verify with the human.**

**步骤 4：搜索其他文献 | Step 4: Search for Additional Literature**

使用网络搜索查找相关论文：

Use web search to find relevant papers:

```
尝试的搜索查询 | Search queries to try:
- "[主要技术] + [应用领域]" | "[main technique] + [application domain]"
- "[基线方法] comparison" | "[baseline method] comparison"
- "[问题名称] state-of-the-art" | "[problem name] state-of-the-art"
- 现有引用的作者名 | Author names from existing citations
```

然后使用下面的引用工作流验证并获取 BibTeX。

Then verify and retrieve BibTeX using the citation workflow below.

**步骤 5：提供初稿 | Step 5: Deliver a First Draft**

**要主动——提供完整草稿，而不是为每个部分征求许可。**

**Be proactive—deliver a complete draft rather than asking permission for each section.**

如果仓库提供清晰的结果且贡献显而易见：

If the repo provides clear results and the contribution is apparent:
1. 从头到尾写完整初稿 | Write the full first draft end-to-end
2. 提交完整草稿以获取反馈 | Present the complete draft for feedback
3. 根据科学家的回应迭代 | Iterate based on scientist's response

如果真正不确定框架或主要声明：

If genuinely uncertain about framing or major claims:
1. 起草你可以自信完成的部分 | Draft what you can confidently
2. 标记具体的不确定性："我将 X 框定为主要贡献——如果您想强调 Y，请告诉我" | Flag specific uncertainties: "I framed X as the main contribution—let me know if you'd prefer to emphasize Y instead"
3. 继续起草而不是阻塞 | Continue with the draft rather than blocking

**在草稿中包含的问题**（而不是之前）：

**Questions to include with the draft** (not before):
- "我强调 X 作为主要贡献——根据需要调整" | "I emphasized X as the main contribution—adjust if needed"
- "我突出了结果 A、B、C——让我知道是否还有其他更重要的" | "I highlighted results A, B, C—let me know if others are more important"
- "相关工作部分包括 [论文]——添加任何我遗漏的" | "Related work section includes [papers]—add any I missed"

---

## 何时使用此技能 | When to Use This Skill

使用此技能当：

Use this skill when:
- **从研究仓库开始写论文** | **Starting from a research repo** to write a paper
- **起草或修改**特定部分 | **Drafting or revising** specific sections
- **查找和验证引用**用于相关工作 | **Finding and verifying citations** for related work
- **格式化**会议提交 | **Formatting** for conference submission
- **重新提交**到其他场所（格式转换） | **Resubmitting** to a different venue (format conversion)
- **与科学家反馈迭代**草稿 | **Iterating** on drafts with scientist feedback

**始终记住**：初稿是讨论的起点，而不是最终输出。

**Always remember**: First drafts are starting points for discussion, not final outputs.

---

## 平衡主动性和协作性 | Balancing Proactivity and Collaboration

**默认：要主动。提供草稿，然后迭代。**

**Default: Be proactive. Deliver drafts, then iterate.**

| 信心水平 | 行动 |
|-----------------|--------|
| **高**（清晰的仓库，明显的贡献） | 写完整草稿，提交，根据反馈迭代 |
| **中**（有些模糊） | 写草稿并标记不确定性，继续 |
| **低**（主要未知） | 问 1-2 个针对性问题，然后起草 |

**先起草，带着草稿提问**（而不是之前）：

| 部分 | 自主起草 | 在草稿中标记 |
|---------|-------------------|-----------------|
| 摘要 | 是 | "将贡献框定为 X——根据需要调整" |
| 引言 | 是 | "强调问题 Y——如果不正确请纠正" |
| 方法 | 是 | "包括细节 A、B、C——添加缺失部分" |
| 实验 | 是 | "突出结果 1、2、3——如果需要重新排序" |
| 相关工作 | 是 | "引用论文 X、Y、Z——添加任何我遗漏的" |

**仅在需要输入时阻塞：**
- 目标场所不明确（影响页数限制、框架）
- 多个相互矛盾的框架似乎同样有效
- 结果看起来不完整或不一致
- 明确要求在继续之前审查

**不要阻塞于：**
- 措辞选择
- 部分排序
- 显示哪些具体结果（做出选择，标记它）
- 引用完整性（用你找到的内容起草，注意差距）

---

## 叙事原则 | The Narrative Principle

**最关键的洞察**：你的论文不是一系列实验——它是一个有清晰贡献并得到证据支持的故事。

**The single most critical insight**: Your paper is not a collection of experiments—it's a story with one clear contribution supported by evidence.

每篇成功的 ML 论文都围绕 Neel Nanda 所称的"叙事"展开：一个简短、严谨、基于证据的技术故事，带有读者关心的结论。

Every successful ML paper centers on what Neel Nanda calls "the narrative": a short, rigorous, evidence-based technical story with a takeaway readers care about.

**三大支柱**（在引言结束时必须非常清晰）：

**Three Pillars** (must be crystal clear by end of introduction):

| 支柱 | 描述 | 示例 |
|--------|-------------|---------|
| **什么 **(What) | 1-3 个具体新颖的主张，属于连贯主题 | "我们证明 X 在条件 Z 下实现 Y" |
| **为什么 **(Why) | 支持主张的严谨经验证据 | 强大的基线，区分假设的实验 |
| **那又怎样 **(So What) | 为什么读者应该关心 | 与公认的社区问题相联系 |

**如果你不能用一句话陈述你的贡献，你就还没有论文。**

**If you cannot state your contribution in one sentence, you don't yet have a paper.**

---

## 论文结构工作流 | Paper Structure Workflow

### 工作流 1：撰写完整论文（迭代）

Copy this checklist and track progress. **Each step involves drafting → feedback → revision:**

```
论文写作进度 | Paper Writing Progress:
- [ ] 步骤 1：定义一句话贡献（与科学家一起） | Step 1: Define the one-sentence contribution (with scientist)
- [ ] 步骤 2：起草图 1 → 获取反馈 → 修改 | Step 2: Draft Figure 1 → get feedback → revise
- [ ] 步骤 3：起草摘要 → 获取反馈 → 修改 | Step 3: Draft abstract → get feedback → revise
- [ ] 步骤 4：起草引言 → 获取反馈 → 修改 | Step 4: Draft introduction → get feedback → revise
- [ ] 步骤 5：起草方法 → 获取反馈 → 修改 | Step 5: Draft methods → get feedback → revise
- [ ] 步骤 6：起草实验 → 获取反馈 → 修改 | Step 6: Draft experiments → get feedback → revise
- [ ] 步骤 7：起草相关工作 → 获取反馈 → 修改 | Step 7: Draft related work → get feedback → revise
- [ ] 步骤 8：起草局限性 → 获取反馈 → 修改 | Step 8: Draft limitations → get feedback → revise
- [ ] 步骤 9：完成论文清单（必需） | Step 9: Complete paper checklist (required)
- [ ] 步骤 10：最终审查周期和提交 | Step 10: Final review cycle and submission
```

**步骤 1：定义一句话贡献 | Step 1: Define the One-Sentence Contribution**

**此步骤需要科学家的明确确认。**

Before writing anything, articulate and verify:
- 你的论文贡献的单一事情是什么？
- 在你的工作之前，什么是不明显或不存在的？

> "我建议将贡献框定为：'[一句话]'。这捕捉到了你想要的主要结论吗？我们应该调整重点吗？"

**步骤 2：起草图 1 | Step 2: Draft Figure 1**

图 1值得特别关注——许多读者会直接跳过它。

Figure 1 deserves special attention—many readers skip directly to it.
- 传达核心思想、方法或最引人注目的结果
- 使用矢量图形（图表用 PDF/EPS）
- 编写独立于正文的说明文字
- 确保黑白可读性（8% 的男性有色觉缺陷）

**步骤 3：撰写摘要（5 句话公式） | Step 3: Write Abstract (5-Sentence Formula)**

来自 Sebastian Farquhar (DeepMind)：

From Sebastian Farquhar (DeepMind):

```
1. 你实现了什么："我们介绍..."，"我们证明..."，"我们展示..."
2. 为什么这很难且重要
3. 你如何实现它（包含专业术语以提高可发现性）
4. 你有什么证据
5. 你最杰出的数字/结果
```

**删除**通用开场白，如"大型语言模型已经取得了显著成功..."

**Delete** generic openings like "Large language models have achieved remarkable success..."

**步骤 4：撰写引言（最多 1-1.5 页） | Step 4: Write Introduction (1-1.5 pages max)****

必须包含：

Must include:
- 2-4 条贡献列表（双栏格式每条最多 1-2 行）
- 清晰的问题陈述
- 简要方法概述
- 方法部分最晚从第 2-3 页开始

**步骤 5：方法部分 | Step 5: Methods Section**

实现可重新实现：

Enable reimplementation:
- 概念大纲或伪代码
- 列出所有超参数
- 架构细节足以复现
- 呈现最终设计决策；消融实验放入实验部分

**步骤 6：实验部分 | Step 6: Experiments Section**

对于每个实验，明确说明：

For each experiment, explicitly state:
- 支持什么主张
- 如何与主要贡献相联系
- 实验设置（详情见附录）
- 观察什么："蓝线显示 X，这证明了 Y"

要求：

Requirements:
- 误差棒及方法论（标准差 vs 标准误）
- 超参数搜索范围
- 计算基础设施（GPU 类型、总小时数）
- 种子设置方法

**步骤 7：相关工作 | Step 7: Related Work**

按方法组织，而不是逐篇论文：

Organize methodologically, not paper-by-paper:

**好：** "一条研究路线使用 Floogledoodle 的假设 [参考文献]，而我们使用 Doobersnoddle 的假设，因为..."

**Good:** "One line of work uses Floogledoodle's assumption [refs] whereas we use Doobersnoddle's assumption because..."

**坏：** "Snap 等人介绍了 X，而 Crackle 等人介绍了 Y。"

**Bad:** "Snap et al. introduced X while Crackle et al. introduced Y."

慷慨引用——审稿人可能撰写了相关论文。

Cite generously—reviewers likely authored relevant papers.

**步骤 8：局限性部分（必需） | Step 8: Limitations Section (REQUIRED)**

所有主要会议都需要这个。反直觉的是，诚实会有帮助：

All major conferences require this. Counter-intuitively, honesty helps:
- 审稿人被指示不要惩罚诚实地承认局限性
- 通过首先指出弱点来预先批评
- 解释为什么局限性不会削弱核心主张

**步骤 9：论文清单 | Step 9: Paper Checklist**

NeurIPS、ICML 和 ICLR 都需要论文清单。参见 [references/checklists.md](references/checklists.md)。

NeurIPS, ICML, and ICLR all require paper checklists. See [references/checklists.md](references/checklists.md).

---

## 顶级 ML 会议的写作理念 | Writing Philosophy for Top ML Conferences

**本节总结了来自顶尖 ML 研究者的最重要写作原则。** 这些不是可选的风格建议——它们是决定论文被接受还是被拒绝的关键因素。

**This section distills the most important writing principles from leading ML researchers.** These aren't optional style suggestions—they're what separates accepted papers from rejected ones.

> "论文是一个简短、严谨、基于证据的技术故事，带有读者关心的结论。" — Neel Nanda

> "A paper is a short, rigorous, evidence-based technical story with a takeaway readers care about." — Neel Nanda

### 背后的来源 | The Sources Behind This Guidance

本技能综合了在顶级场所发表大量论文的研究者的写作理念：

This skill synthesizes writing philosophy from researchers who have published extensively at top venues:

| 来源 | 关键贡献 | 链接 |
|--------|-----------------|------|
| **Neel Nanda** (Google DeepMind) | 叙事原则，什么/为什么/那又怎样框架 | [如何写 ML 论文](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers) |
| **Sebastian Farquhar** (DeepMind) | 5 句话摘要公式 | [如何写 ML 论文](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) |
| **Gopen & Swan** | 读者期望的 7 项原则 | [科学写作的科学](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) |
| **Zachary Lipton** | 措辞选择，消除模糊 | [技术科学写作启发法](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) |
| **Jacob Steinhardt** (UC Berkeley) | 精确性、一致的术语 | [写作建议](https://bounded-regret.ghost.io/) |
| **Ethan Perez** | 微观层面的清晰度建议 | [简单论文写作技巧](https://ethanperez.net/easy-paper-writing-tips/) |
| **Andrej Karpathy** | 单一贡献重点 | 各种讲座 |

**更深入任何这些内容，参见：**
- [references/writing-guide.md](references/writing-guide.md) - 带示例的完整解释
- [references/sources.md](references/sources.md) - 完整参考书目

### 时间分配（来自 Neel Nanda）

花费大约**相等的时间**在每一项上：

Spend approximately **equal time** on each of:
1. 摘要
2. 引言
3. 图表
4. 其他所有部分的总和

**为什么？** 大多数审稿人在到达你的方法部分之前就形成了判断。读者接触你的论文顺序是：**标题 → 摘要 → 引言 → 图表 → 可能其余部分。**

**Why?** Most reviewers form judgments before reaching your methods. Readers encounter your paper as: **title → abstract → introduction → figures → maybe the rest.**

### 写作风格指南 | Writing Style Guidelines

#### 句子级清晰度（Gopen & Swan 的 7 项原则）

这些原则基于读者实际如何处理散文。违反它们会迫使读者花费认知精力在结构上而不是内容上。

These principles are based on how readers actually process prose. Violating them forces readers to spend cognitive effort on structure rather than content.

| 原则 | 规则 | 示例 |
|-----------|------|---------|
| **主谓接近** | 保持主语和动词靠近 | ❌ "The model, which was trained on..., achieves" → ✅ "The model achieves... after training on..." |
| **强调位置** | 将重点放在句尾 | ❌ "Accuracy improves by 15% when using attention" → ✅ "When using attention, accuracy improves by **15%**" |
| **主题位置** | 先放上下文，新信息在后 | ✅ "Given these constraints, we propose..." |
| **旧信息在前** | 熟悉信息 → 不熟悉信息 | 向后链接，然后引入新信息 |
| **一个单元，一个功能** | 每段表达一个观点 | 拆分多点段落 |
| **动词中的动作** | 使用动词，不是名词化 | ❌ "We performed an analysis" → ✅ "We analyzed" |
| **新信息前的上下文** | 在呈现之前设置舞台 | 在展示方程之前解释

**完整 7 项原则及详细示例：** 参见 [references/writing-guide.md](references/writing-guide.md#the-7-principles-of-reader-expectations)

#### 微观层面技巧（Ethan Perez）

这些小的改变累积成显著更清晰的散文：

These small changes accumulate into significantly clearer prose:

- **最小化代词**：❌ "This shows..." → ✅ "This result shows..."
- **动词提前**：将动词放在靠近句首的位置
- **展开所有格**：❌ "X's Y" → ✅ "The Y of X"（当 awkward 时）
- **删除填充词**："actually," "a bit," "very," "really," "basically," "quite," "essentially"

**完整微观技巧及示例：** 参见 [references/writing-guide.md](references/writing-guide.md#micro-level-writing-tips)

#### 措辞选择（Zachary Lipton）

- **具体明确**：❌ "performance" → ✅ "accuracy" 或 "latency"（说出你的意思）
- **消除模糊**：除非真正不确定，否则删除 "may" 和 "can"
- **避免渐进词汇**：❌ "combine," "modify," "expand" → ✅ "develop," "propose," "introduce"
- **删除强化词**：❌ "provides *very* tight approximation" → ✅ "provides tight approximation"

#### 精确胜于简洁（Jacob Steinhardt）

- **一致的术语**：对同一概念使用不同术语会造成混淆。选择一个并坚持使用。
- **正式陈述假设**：在定理之前，明确列出所有假设
- **直觉 + 严谨**：在形式证明旁边提供直观解释

### What Reviewers Actually Read

Understanding reviewer behavior helps prioritize your effort:

| Paper Section | % Reviewers Who Read | Implication |
|---------------|---------------------|-------------|
| Abstract | 100% | Must be perfect |
| Introduction | 90%+ (skimmed) | Front-load contribution |
| Figures | Examined before methods | Figure 1 is critical |
| Methods | Only if interested | Don't bury the lede |
| Appendix | Rarely | Put only supplementary details |

**Bottom line**: If your abstract and intro don't hook reviewers, they may never read your brilliant methods section.

---

## Conference Requirements Quick Reference

| Conference | Page Limit | Extra for Camera-Ready | Key Requirement |
|------------|------------|------------------------|-----------------|
| **NeurIPS 2025** | 9 pages | +0 | Mandatory checklist, lay summary for accepted |
| **ICML 2026** | 8 pages | +1 | Broader Impact Statement required |
| **ICLR 2026** | 9 pages | +1 | LLM disclosure required, reciprocal reviewing |
| **ACL 2025** | 8 pages (long) | varies | Limitations section mandatory |
| **AAAI 2026** | 7 pages | +1 | Strict style file adherence |
| **COLM 2025** | 9 pages | +1 | Focus on language models |

**Universal Requirements:**
- Double-blind review (anonymize submissions)
- References don't count toward page limit
- Appendices unlimited but reviewers not required to read
- LaTeX required for all venues

**LaTeX Templates:** See [templates/](templates/) directory for all conference templates.

---

## Using LaTeX Templates Properly

### Workflow 4: Starting a New Paper from Template

**Always copy the entire template directory first, then write within it.**

```
Template Setup Checklist:
- [ ] Step 1: Copy entire template directory to new project
- [ ] Step 2: Verify template compiles as-is (before any changes)
- [ ] Step 3: Read the template's example content to understand structure
- [ ] Step 4: Replace example content section by section
- [ ] Step 5: Keep template comments/examples as reference until done
- [ ] Step 6: Clean up template artifacts only at the end
```

**Step 1: Copy the Full Template**

```bash
# Create your paper directory with the complete template
cp -r templates/neurips2025/ ~/papers/my-new-paper/
cd ~/papers/my-new-paper/

# Verify structure is complete
ls -la
# Should see: main.tex, neurips.sty, Makefile, etc.
```

**⚠️ IMPORTANT**: Copy the ENTIRE directory, not just `main.tex`. Templates include:
- Style files (`.sty`) - required for compilation
- Bibliography styles (`.bst`) - required for references
- Example content - useful as reference
- Makefiles - for easy compilation

**Step 2: Verify Template Compiles First**

Before making ANY changes, compile the template as-is:

```bash
# Using latexmk (recommended)
latexmk -pdf main.tex

# Or manual compilation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If the unmodified template doesn't compile, fix that first. Common issues:
- Missing TeX packages → install via `tlmgr install <package>`
- Wrong TeX distribution → use TeX Live (recommended)

**Step 3: Keep Template Content as Reference**

Don't immediately delete all example content. Instead:

```latex
% KEEP template examples commented out as you write
% This shows you the expected format

% Template example (keep for reference):
% \begin{figure}[t]
%   \centering
%   \includegraphics[width=0.8\linewidth]{example-image}
%   \caption{Template shows caption style}
% \end{figure}

% Your actual figure:
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\linewidth]{your-figure.pdf}
  \caption{Your caption following the same style.}
\end{figure}
```

**Step 4: Replace Content Section by Section**

Work through the paper systematically:

```
Replacement Order:
1. Title and authors (anonymize for submission)
2. Abstract
3. Introduction
4. Methods
5. Experiments
6. Related Work
7. Conclusion
8. References (your .bib file)
9. Appendix
```

For each section:
1. Read the template's example content
2. Note any special formatting or macros used
3. Replace with your content following the same patterns
4. Compile frequently to catch errors early

**Step 5: Use Template Macros**

Templates often define useful macros. Check the preamble for:

```latex
% Common template macros to use:
\newcommand{\method}{YourMethodName}  % Consistent method naming
\newcommand{\eg}{e.g.,\xspace}        % Proper abbreviations
\newcommand{\ie}{i.e.,\xspace}
\newcommand{\etal}{\textit{et al.}\xspace}
```

**Step 6: Clean Up Only at the End**

Only remove template artifacts when paper is nearly complete:

```latex
% BEFORE SUBMISSION - remove these:
% - Commented-out template examples
% - Unused packages
% - Template's example figures/tables
% - Lorem ipsum or placeholder text

% KEEP these:
% - All style files (.sty)
% - Bibliography style (.bst)
% - Required packages from template
% - Any custom macros you're using
```

### Template Pitfalls to Avoid

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Copying only `main.tex` | Missing `.sty`, won't compile | Copy entire directory |
| Modifying `.sty` files | Breaks conference formatting | Never edit style files |
| Adding random packages | Conflicts, breaks template | Only add if necessary |
| Deleting template content too early | Lose formatting reference | Keep as comments until done |
| Not compiling frequently | Errors accumulate | Compile after each section |

### Quick Template Reference

| Conference | Main File | Key Style File | Notes |
|------------|-----------|----------------|-------|
| NeurIPS 2025 | `main.tex` | `neurips.sty` | Has Makefile |
| ICML 2026 | `example_paper.tex` | `icml2026.sty` | Includes algorithm packages |
| ICLR 2026 | `iclr2026_conference.tex` | `iclr2026_conference.sty` | Has math_commands.tex |
| ACL | `acl_latex.tex` | `acl.sty` | Strict formatting |
| AAAI 2026 | `aaai2026-unified-template.tex` | `aaai2026.sty` | Very strict compliance |
| COLM 2025 | `colm2025_conference.tex` | `colm2025_conference.sty` | Similar to ICLR |

---

## Conference Resubmission & Format Conversion

When a paper is rejected or withdrawn from one venue and resubmitted to another, format conversion is required. This is a common workflow in ML research.

### Workflow 3: Converting Between Conference Formats

```
Format Conversion Checklist:
- [ ] Step 1: Identify source and target template differences
- [ ] Step 2: Create new project with target template
- [ ] Step 3: Copy content sections (not preamble)
- [ ] Step 4: Adjust page limits and content
- [ ] Step 5: Update conference-specific requirements
- [ ] Step 6: Verify compilation and formatting
```

**Step 1: Key Template Differences**

| From → To | Page Change | Key Adjustments |
|-----------|-------------|-----------------|
| NeurIPS → ICML | 9 → 8 pages | Cut 1 page, add Broader Impact if missing |
| ICML → ICLR | 8 → 9 pages | Can expand experiments, add LLM disclosure |
| NeurIPS → ACL | 9 → 8 pages | Restructure for NLP conventions, add Limitations |
| ICLR → AAAI | 9 → 7 pages | Significant cuts needed, strict style adherence |
| Any → COLM | varies → 9 | Reframe for language model focus |

**Step 2: Content Migration (NOT Template Merge)**

**Never copy LaTeX preambles between templates.** Instead:

```bash
# 1. Start fresh with target template
cp -r templates/icml2026/ new_submission/

# 2. Copy ONLY content sections from old paper
# - Abstract text
# - Section content (between \section{} commands)
# - Figures and tables
# - Bibliography entries

# 3. Paste into target template structure
```

**Step 3: Adjusting for Page Limits**

When cutting pages (e.g., NeurIPS 9 → AAAI 7):
- Move detailed proofs to appendix
- Condense related work (cite surveys instead of individual papers)
- Combine similar experiments into unified tables
- Use smaller figure sizes with subfigures
- Tighten writing: eliminate redundancy, use active voice

When expanding (e.g., ICML 8 → ICLR 9):
- Add ablation studies reviewers requested
- Expand limitations discussion
- Include additional baselines
- Add qualitative examples

**Step 4: Conference-Specific Adjustments**

| Target Venue | Required Additions |
|--------------|-------------------|
| **ICML** | Broader Impact Statement (after conclusion) |
| **ICLR** | LLM usage disclosure, reciprocal reviewing agreement |
| **ACL/EMNLP** | Limitations section (mandatory), Ethics Statement |
| **AAAI** | Strict adherence to style file (no modifications) |
| **NeurIPS** | Paper checklist (appendix), lay summary if accepted |

**Step 5: Update References**

```latex
% Remove self-citations that reveal identity (for blind review)
% Update any "under review" citations to published versions
% Add new relevant work published since last submission
```

**Step 6: Addressing Previous Reviews**

When resubmitting after rejection:
- **Do** address reviewer concerns in the new version
- **Do** add experiments/clarifications reviewers requested
- **Don't** include a "changes from previous submission" section (blind review)
- **Don't** reference the previous submission or reviews

**Common Conversion Pitfalls:**
- ❌ Copying `\usepackage` commands (causes conflicts)
- ❌ Keeping old conference header/footer commands
- ❌ Forgetting to update `\bibliography{}` path
- ❌ Missing conference-specific required sections
- ❌ Exceeding page limit after format change

---

## Citation Workflow (Hallucination Prevention)

**⚠️ CRITICAL**: AI-generated citations have ~40% error rate. **Never write BibTeX from memory.**

### The Golden Rule

```
IF you cannot programmatically fetch a citation:
    → Mark it as [CITATION NEEDED] or [PLACEHOLDER - VERIFY]
    → Tell the scientist explicitly
    → NEVER invent a plausible-sounding reference
```

### Workflow 2: Adding Citations

```
Citation Verification (MANDATORY for every citation):
- [ ] Step 1: Search using Exa MCP or Semantic Scholar API
- [ ] Step 2: Verify paper exists in 2+ sources (Semantic Scholar + arXiv/CrossRef)
- [ ] Step 3: Retrieve BibTeX via DOI (programmatically, not from memory)
- [ ] Step 4: Verify the claim you're citing actually appears in the paper
- [ ] Step 5: Add verified BibTeX to bibliography
- [ ] Step 6: If ANY step fails → mark as placeholder, inform scientist
```

**Step 0: Use Exa MCP for Initial Search (Recommended)**

If Exa MCP is installed, use it to find relevant papers:
```
Search: "RLHF language model alignment 2023"
Search: "sparse autoencoders interpretability"
Search: "attention mechanism transformers Vaswani"
```

Then verify each result with Semantic Scholar and fetch BibTeX via DOI.

**Step 1: Search Semantic Scholar**

```python
from semanticscholar import SemanticScholar

sch = SemanticScholar()
results = sch.search_paper("attention mechanism transformers", limit=5)
for paper in results:
    print(f"{paper.title} - {paper.paperId}")
    print(f"  DOI: {paper.externalIds.get('DOI', 'N/A')}")
```

**Step 2: Verify Existence**

Confirm paper appears in at least two sources (Semantic Scholar + CrossRef/arXiv).

**Step 3: Retrieve BibTeX via DOI**

```python
import requests

def doi_to_bibtex(doi: str) -> str:
    """Get verified BibTeX from DOI via CrossRef."""
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"}
    )
    response.raise_for_status()
    return response.text

# Example
bibtex = doi_to_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

**Step 4: Verify Claims**

Before citing for a specific claim, access the paper and confirm the attributed claim actually appears.

**Step 5: Handle Failures Explicitly**

If you cannot verify a citation at ANY step:

```latex
% Option 1: Explicit placeholder
\cite{PLACEHOLDER_smith2023_verify}  % TODO: Could not verify - scientist must confirm

% Option 2: Note in text
... as shown in prior work [CITATION NEEDED - could not verify Smith et al. 2023].
```

**Always inform the scientist:**
> "I could not verify the following citations and have marked them as placeholders:
> - Smith et al. 2023 on reward hacking - could not find in Semantic Scholar
> - Jones 2022 on scaling laws - found similar paper but different authors
> Please verify these before submission."

### Summary: Citation Rules

| Situation | Action |
|-----------|--------|
| Found paper, got DOI, fetched BibTeX | ✅ Use the citation |
| Found paper, no DOI | ✅ Use arXiv BibTeX or manual entry from paper |
| Paper exists but can't fetch BibTeX | ⚠️ Mark placeholder, inform scientist |
| Uncertain if paper exists | ❌ Mark `[CITATION NEEDED]`, inform scientist |
| "I think there's a paper about X" | ❌ **NEVER cite** - search first or mark placeholder |

**🚨 NEVER generate BibTeX from memory—always fetch programmatically. 🚨**

See [references/citation-workflow.md](references/citation-workflow.md) for complete API documentation.

---

## Common Issues and Solutions

**Issue: Abstract too generic**

Delete first sentence if it could be prepended to any ML paper. Start with your specific contribution.

**Issue: Introduction exceeds 1.5 pages**

Split background into Related Work. Front-load contribution bullets. Methods should start by page 2-3.

**Issue: Experiments lack explicit claims**

Add sentence before each experiment: "This experiment tests whether [specific claim]..."

**Issue: Reviewers find paper hard to follow**

- Add explicit signposting: "In this section, we show X"
- Use consistent terminology throughout
- Include figure captions that stand alone

**Issue: Missing statistical significance**

Always include:
- Error bars (specify: std dev or std error)
- Number of runs
- Statistical tests if comparing methods

---

## Reviewer Evaluation Criteria

Reviewers assess papers on four dimensions:

| Criterion | What Reviewers Look For |
|-----------|------------------------|
| **Quality** | Technical soundness, well-supported claims |
| **Clarity** | Clear writing, reproducible by experts |
| **Significance** | Community impact, advances understanding |
| **Originality** | New insights (doesn't require new method) |

**Scoring (NeurIPS 6-point scale):**
- 6: Strong Accept - Groundbreaking, flawless
- 5: Accept - Technically solid, high impact
- 4: Borderline Accept - Solid, limited evaluation
- 3: Borderline Reject - Solid but weaknesses outweigh
- 2: Reject - Technical flaws
- 1: Strong Reject - Known results or ethics issues

See [references/reviewer-guidelines.md](references/reviewer-guidelines.md) for detailed reviewer instructions.

---

## Tables and Figures

### Tables

Use `booktabs` LaTeX package for professional tables:

```latex
\usepackage{booktabs}
\begin{tabular}{lcc}
\toprule
Method & Accuracy ↑ & Latency ↓ \\
\midrule
Baseline & 85.2 & 45ms \\
\textbf{Ours} & \textbf{92.1} & 38ms \\
\bottomrule
\end{tabular}
```

**Rules:**
- Bold best value per metric
- Include direction symbols (↑ higher is better, ↓ lower is better)
- Right-align numerical columns
- Consistent decimal precision

### Figures

- **Vector graphics** (PDF, EPS) for all plots and diagrams
- **Raster** (PNG 600 DPI) only for photographs
- Use **colorblind-safe palettes** (Okabe-Ito or Paul Tol)
- Verify **grayscale readability** (8% of men have color vision deficiency)
- **No title inside figure**—the caption serves this function
- **Self-contained captions**—reader should understand without main text

---

## References & Resources

### Reference Documents (Deep Dives)

| Document | Contents |
|----------|----------|
| [writing-guide.md](references/writing-guide.md) | Gopen & Swan 7 principles, Ethan Perez micro-tips, word choice |
| [citation-workflow.md](references/citation-workflow.md) | Citation APIs, Python code, BibTeX management |
| [checklists.md](references/checklists.md) | NeurIPS 16-item, ICML, ICLR, ACL requirements |
| [reviewer-guidelines.md](references/reviewer-guidelines.md) | Evaluation criteria, scoring, rebuttals |
| [sources.md](references/sources.md) | Complete bibliography of all sources |

### LaTeX Templates

Templates in `templates/` directory: **ICML 2026**, **ICLR 2026**, **NeurIPS 2025**, **ACL/EMNLP**, **AAAI 2026**, **COLM 2025**.

**Compiling to PDF:**
- **VS Code/Cursor**: Install LaTeX Workshop extension + TeX Live → Save to auto-compile
- **Command line**: `latexmk -pdf main.tex` or `pdflatex` + `bibtex` workflow
- **Online**: Upload to [Overleaf](https://overleaf.com)

See [templates/README.md](templates/README.md) for detailed setup instructions.

### Key External Sources

**Writing Philosophy:**
- [Neel Nanda: How to Write ML Papers](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers) - Narrative, "What/Why/So What"
- [Farquhar: How to Write ML Papers](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) - 5-sentence abstract
- [Gopen & Swan: Science of Scientific Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) - 7 reader expectation principles
- [Lipton: Heuristics for Scientific Writing](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) - Word choice
- [Perez: Easy Paper Writing Tips](https://ethanperez.net/easy-paper-writing-tips/) - Micro-level clarity

**APIs:** [Semantic Scholar](https://api.semanticscholar.org/api-docs/) | [CrossRef](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | [arXiv](https://info.arxiv.org/help/api/basics.html)

**Venues:** [NeurIPS](https://neurips.cc/Conferences/2025/PaperInformation/StyleFiles) | [ICML](https://icml.cc/Conferences/2025/AuthorInstructions) | [ICLR](https://iclr.cc/Conferences/2026/AuthorGuide) | [ACL](https://github.com/acl-org/acl-style-files)

