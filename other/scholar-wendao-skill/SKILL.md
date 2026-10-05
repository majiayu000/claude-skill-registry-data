---
name: scholar-wendao
description: |
  学者问道：为人文社科学者构建可调用的思想分析工具。
  输入学者名/研究领域，自动多语言采集著作、二手文献、传记与学术争论，
  提炼出可在你的研究中调用的"分析镜片"——而不是聊天机器人。
  默认输出第三人称分析模式，对话/角色扮演作为 opt-in。

  触发词：「学者问道」「问道于XX」「蒸馏学者」「构建XX的分析镜片」
  「XX的研究方法」「XX视角」「scholar-wendao」「XX-perspective」「为XX建一个 skill」。
  模糊触发：「我研究XX，需要某种分析框架」「有没有一种学者视角能帮我看待这个材料」。
---

# 学者问道 · Scholar-Wendao

> *问道于古今学者* · *Ask the way of scholars across time*

## 核心理念

**学者问道不造人，构建分析镜片。**

人文社科研究者真正需要的不是"和福柯聊天"，而是**把福柯的分析镜片装到自己的研究流程里**——读到一段材料，能立刻问"用这个学者的概念框架看，会怎么解读"。

一个好的学者 perspective skill 是一套**可运行的学术分析工具箱**：

- 他用什么**概念地图**理解问题？（核心理论术语网络）
- 他的**方法论进路**是什么？（碰到一个现象先问什么、怎么组织证据、如何论证）
- 他的**学派定位**与**智识谱系**？（受谁影响、影响了谁、与同代人的差异化）
- 他的**论战与立场转变**？（公开争论暴露的真实判断）
- 他的**行文风格与概念语言**？（学术写作中的概念使用方式，不是"语气"）
- 他的**人格与处世**？（性格、家庭、形成性事件——影响思想但常被忽略）
- 他**做不到什么**？（默会知识、化石化、传记修辞污染——诚实边界）

**关键区分**：捕捉的是 **HOW they analyze**，不是 **WHAT they wrote**。

**与人格 skill 通用工具的根本差异**：
- 默认输出**第三人称分析**（"从 Stiegler 的 organology 视角看，这个现象的技术外在化逻辑是……"），而非第一人称扮演
- 对话/角色扮演为 opt-in，必须用户主动激活
- 信息源严格分级（一手 / 二手 / 传记类 / 学生回忆，每条标注）
- 直面六大学术批评（默会知识、思想化石化、公开 vs 私下、传记修辞、漫画化、死亡-尊重边界）

---

## 双工作流架构（v0.4.2）

scholar-wendao 的执行被显式分为两个**独立可触发**的子工作流，加一个共享数据层。

```
                       ┌─ _library_config.md (配置)
共享数据层 ──────────────┼─ _acquisition_manifest.{md,json} (资料状态 + 4 tier 标注)
                       ├─ {Vault}/Library/{_files,Cards}/ (Vault 内的真源)
                       └─ examples/{slug}-perspective/_pdf_evidence/ (蒸馏证据)

┌─ Workflow A · 图书馆建设(Library Building)─────────────────────┐
│ 触发: "搜集 X 的资料" / "为 X 建库" / "build-library X"        │
│   A.0 配置（_library_config.md）                                │
│   A.1 Metadata 全收集（无漏 manifest）                          │
│   A.2 Tier 1+2 自动下载（OA / yt-dlp / scrape）                │
│   A.3 Tier 3+4 manifest 输出（待手动 / 浏览器助手项）           │
│   A.4 用户主动导入 ← intake_manual_pdf.py（可重复跑）          │
│   A.5 generate_library_cards（Library → Cards）                 │
│ 退出: Library 增长 + acquisition_manifest 标记当前覆盖率        │
└──────────────────────────────────────────────────────────────────┘
                              │  (可独立运行多轮)
                              │
┌─ Workflow B · 学者蒸馏(Scholar Distillation)────────────────────┐
│ 触发: "蒸馏 X" / "做 X 的分析镜片" / "distill X"                │
│ 前置: Workflow A 至少跑过一次（Library 有 ≥ 5 部 PDF 推荐）    │
│   B.1 extract_pdf_evidence（基于 Library 当前状态）             │
│   B.2 7 agent 调研（research / biography）                      │
│   B.3 框架提炼（concepts / heuristics / genealogy / etc.）      │
│   B.4 SKILL.md 构建                                             │
│   B.5 质量验证                                                   │
│   B.6 Vault 同步（回灌 wikilinks）                              │
│ 退出: Perspective Skill 产出 + Vault wikilinks 更新             │
└──────────────────────────────────────────────────────────────────┘

默认入口 "学者问道 X" = A → B 串行（向后兼容 v0.4.1 端到端流程）
增量入口:
  - "更新 X 库" / "为 X 补料" → 仅跑 A（含 A.4 主动导入）
  - "重蒸 X" / "用新资料重做 X 镜片" → 仅跑 B（基于扩充后 Library 整体重做）
  - "更新 X 的 skill" → 轻量 update（v0.4.1 既有逻辑，仅增补不重写）
```

### 关键设计原则

1. **A 与 B 通过 `_acquisition_manifest.json` 解耦** —— B 不假设 A 已完成，只读 manifest 中已下载的部分作为 evidence 源。
2. **A.4 主动导入是一等公民**，不是 fallback。用户随时可"我有一本 PDF，加到 X 的库"，工具自动重命名 + 移到 Library + 生成 Card。
3. **资料采集的"无漏"原则 = metadata 无漏，不是 PDF 全到手** —— 反爬严格的源（annas / Sci-Hub / 部分 paywall）只能输出 Tier 3+4 manifest 让用户决策。
4. **B 不阻塞 A 未完成项** —— 蒸馏总能跑（基于已有素材），SKILL.md 质量随 Library 增长而上。
5. **"重蒸 B"是激进重做** —— Library 大幅扩充后整体重做 Phase 2.x，旧 SKILL.md 进 `_archive/`；与"轻量 update"不同。

### 4 层资料采集架构

| Tier | 自动化程度 | 适用源 | 工具 |
|---|---|---|---|
| **1 · 完全 API** | 100% 自动 | OpenAlex / Crossref / Semantic Scholar / arXiv / OAPEN / DOAB / unpaywall | `harvest_works.py` |
| **2 · 友好 scrape** | 90% 自动 | YouTube 元数据 / Vimeo / 学者主页 / ARS Industrialis / Internation / 出版社 OA 落地页 | 4 个新 harvester（v0.4.3） |
| **3 · 浏览器助手** | 50% 自动 | annas / paywall(机构 access) / Cairn 锁定文章 | 用户浏览器解 captcha → 导出 cookies → 工具用 cookies 调 API |
| **4 · 完全手动** | 0% 自动，工具辅助归档 | annas 严格反爬 / Sci-Hub / 闭源专著 / 罕见档案 | `intake_manual_pdf.py`（用户拖入 PDF → 自动改名 + 移到 Library + 生成 Card） |

每条资料在 `_acquisition_manifest.json` 中标注 `acquisition_tier: 1/2/3/4` + `priority: P0/P1/P2`。Phase A.3 输出 Tier 3+4 列表给用户决策；Phase A.4 把用户手动下的 PDF 标记为 `intake_completed`。

---

## v0.5 学者类型 + Workflow B 分支

v0.4.x 默认 framework 为**当代单一作者**优化（Stiegler 验证）。v0.5 加传统学者支持，Workflow B 内部按 `scholar_type` 分流：

```
Workflow B(蒸馏)
├── B.0 学者类型判定（Phase 0A 第 6 项 scholar_type）
│
├── [contemporary] → B.3a 现代单一作者蒸馏（向后兼容 v0.4.x）
│       Phase 2.1-2.8 现有流程不变
│       默认输出：单一第三人称分析镜片
│
├── [traditional] → B.3b 传统学者蒸馏（v0.5 新增）
│       新增 Phase 2.0' Lineages 提炼（4-6 派代表学者 + reading strategy）
│       Phase 2.1' 概念地图扩展为「概念 × 派」二维矩阵
│       Phase 2.5' biography 降级 + intellectual genealogy 升级
│       Phase 2.7' 古典引文系统(Bekker / Stephanus / 中典页码)
│       默认输出：multi-perspective（本人 + N 派各自看）
│
└── [topic] → B.3c 主题/流派蒸馏（已有的 v0.4 主题模式）
```

### 学者类型 → 三个核心差异

| 维度 | contemporary | **traditional**（v0.5 新增） | topic |
|---|---|---|---|
| 概念地图 size | 3-7 | **5-15**（允许大概念集） | 5-10 |
| 默认输出 mode | 单一第三人称 | **multi-perspective**（本人+N 派）| 领域共识+各家分歧 |
| Lineages 一等公民 | 否 | **是**（必填 4-6 派） | 否（流派 = 主题本身） |
| 概念结构 | 概念→单一定义 | **概念→本人+N 派 reading 差异** | 共识概念+争议概念 |
| 引文系统 | PDF page anchor | **Bekker/Stephanus 编号 + 译本页码并存** | 引代表论文 page anchor |
| biography 重要性 | 高（强 BRACKETING） | 低（生平稀少不可靠，重 genealogy） | 不需要 |
| 一手分级 | A+ → C(8 级) | **+ 派学者「子一手」 A^**（Aquinas/Avicenna 自己写的"是 X 这样想"著作）| 不适用 |

### Lineage 一等公民结构（traditional 必填）

每个 traditional 学者的 SKILL.md 必须含 **lineages 章节**（4-6 派）：

```yaml
lineages:
  - name: "经院派 / Thomism"
    representative: "Thomas Aquinas"
    period: "13世纪"
    key_works:
      - "Summa Theologiae"
      - "Commentary on Nicomachean Ethics"
    reading_strategy: "把 Aristotle 形质论 / 四因说整合进基督教神学"
    distinctive_claims:
      - "首要 ousia = essence + esse(存在)"
      - "灵魂作为实体形式"
    representative_concept_reading:
      ousia: "essence + esse"
      virtue: "infused virtue 高于 acquired virtue"
  - name: "阿拉伯派"
    representative: "Avicenna (Ibn Sina)"
    ...
```

### Multi-perspective 默认输出格式（traditional）

```markdown
## [Aristotle 本人]
基于 *EN* 1097b22-1098a20，Aristotle 会说……
[此段引文用 Bekker 编号 + 现代译本页码并标]

## [经院派 / Aquinas]
他会重读这段为……，因为对他而言 *eudaimonia* 不只是地上活动 (operatio)，
而是指向至福直观 (visio beatifica)。
[引 *Summa Theologiae* I-II Q.3]

## [Heidegger 派]
他会跳过命题层，看到 *eudaimonia* 的存在论意义被遮蔽为"幸福感"。
他会回到 *physis* 与 *aletheia* 的发生……
[引 *Sein und Zeit* §40 + *Brief über den Humanismus*]

## [Anglo-American analytic / MacIntyre]
他会形式化为：德性是 practice 内部 goods 的获取条件……
[引 *After Virtue* ch.14]
```

用户在调用时若说"用 X 派看这个材料"或"X 派会怎么想 Y" → 工具直接走该派的 reading strategy 输出。

### 向后兼容

- Stiegler 等已有 contemporary 案例不受影响（_library_config 默认 `scholar_type: contemporary` 时走 v0.4.x 流程）
- v0.5.2 计划：用 traditional 框架升级 Stiegler（加 lineages: 海德格尔派 / 西蒙东派 / Derrida 派 / 中国 Stiegler 派——许煜/陆兴华），让 Stiegler 输出 mode 也支持 multi-perspective

---

## 执行流程

### Phase 0: 入口分流（v0.4.2 加双工作流分支）

收到用户请求后，先判断**触发哪个 workflow** + 哪条路径：

| 用户输入意图 | Workflow | 后续路径 |
|---|---|---|
| "**搜集 X 的资料**" / "**为 X 建图书馆**" / "build-library X" | **A 单跑** | A.0 → A.5 |
| "**蒸馏 X**" / "**做 X 的分析镜片**" / "distill X" | **B 单跑** | 检查 Library 覆盖率 → B.1 → B.6 |
| "**学者问道 X**" / "**为 X 建一个 skill**"（默认端到端） | **A → B** | 完整流程 |
| "**重蒸 X**" / "**用新资料重做 X 镜片**" | **B 重做模式** | 旧 SKILL.md 进 `_archive/` → B.1-B.6 重做 |
| "**更新 X 的 skill**" | **B 轻量 update** | 仅增补不重写（v0.4.1 既有逻辑） |
| "**我有一份 PDF 想加到 X 的库**" / "import PDF for X" | **A.4 单步** | 直接跑 `intake_manual_pdf.py` |

学者识别（直接路径 / 主题 / 诊断）的判断与 v0.4.1 一致：

| 用户输入 | 路径 | 示例 |
|---------|------|------|
| 明确的学者名 | **直接路径** → Phase 0A | "蒸馏 Bernard Stiegler"、"为福柯建一个 skill" |
| 明确的方法论主题 | **主题路径** → Phase 0A（主题模式） | "构建批判理论分析工具"、"民族志方法 perspective" |
| 模糊的研究需求 | **诊断路径** → Phase 0B | "我研究农村教育，想要一种能看穿权力关系的视角" |

---

### Phase 0A: 需求澄清（直接路径）

收到明确学者名后，确认六件事（v0.5 加第 6 项「学者类型」）：

1. **学者身份精确锁定**：避免重名混淆（"Foucault" 是 Michel 还是 Léon？"Charles Taylor" 哪一位？）
2. **聚焦方向**（可选）：全面镜片 vs 聚焦某个维度（如只蒸馏 Stiegler 关于"技术外在化"的部分）
3. **使用场景**：用于分析某类特定材料？给写作提供概念资源？还是做思想史研究？
4. **是否更新**：检查 `~/.claude/skills/[scholar]-perspective/` 是否已存在
5. **本地一手语料**：「你手上有这个学者的一手语料吗？比如电子版专著、访谈 transcript、本人手稿、学生整理的讲座稿。有的话直接给路径，比网络搜索质量高得多」
6. **学者类型**（v0.5 新增 · 决定 Workflow B 走哪条分支）：
   - **`contemporary`** —— 当代单一作者(20-21 世纪在世或近 50 年内去世)。例：Stiegler / Yuk Hui / Latour / Haraway。**默认 mode**：单一第三人称分析镜片，向后兼容 v0.4.x 全部流程。
   - **`traditional`** —— 古典 / 经典学者(去世 ≥ 100 年 + 已形成多派解读传统)。例：Aristotle / Plato / Confucius / Kant / Hegel。**默认 mode**：**多视角输出**(本人 + N 派 lineages 解读)，启用 v0.5 新流程(Phase B.3'+ 含 lineages 蒸馏 + 概念×派矩阵)。
   - **`topic`** —— 不是单一学者而是方法论传统/流派(critical theory / ANT / 民族志方法)。**默认 mode**：领域共识 + 各家分歧。

   判断启发式：
   - 学者去世 ≥ 100 年 + 维基百科页面有"interpretation by school"小节 → traditional
   - 学者著作存在多语种古译本(拉丁 / 阿拉伯 / 经典中译) → traditional
   - 单一思想家 + 主要在世或近代 → contemporary
   - 用户输入是方法论名词(批判理论/STS) → topic

**默认行为**：用户没有更多信息 → 全面镜片 + 学术分析用途 + 无本地语料(走网络+开放档案) + scholar_type 自动判定 → 进入 Phase 0.5。

---

### Phase 0B: 需求诊断（模糊路径）

用户不知道该蒸馏谁，只有困惑或需求。这时学者问道的工作是**从研究需求反推最合适的学者**。

#### Step 1: 需求维度定位

通过 1-2 个追问定位用户的核心研究需求：

| 需求维度 | 典型表达 | 学者方向 |
|---------|---------|---------|
| 权力分析 | 「想看穿表面话语下的权力运作」「制度如何塑造主体」 | 福柯、布尔迪厄、葛兰西、阿甘本 |
| 技术与人 | 「想理解技术如何重塑人类」「数字资本主义」 | Stiegler、Simondon、芒福德、麦克卢汉 |
| 行动者-网络 | 「想避免人/物二元论」「物的行动力」 | 拉图尔、Mol、Haraway |
| 资本主义批判 | 「想分析资本逻辑对生活的渗透」 | 马克思、Wendy Brown、Boltanski、Streeck |
| 文化与象征 | 「想分析符号系统如何运作」 | 列维-斯特劳斯、Geertz、Bourdieu（作为符号社会学家） |
| 现代性反思 | 「想批判性看待启蒙、进步」 | 韦伯、阿多诺/霍克海默、查尔斯·泰勒 |
| 诠释学 | 「文本/材料的意义如何解读」 | 伽达默尔、利科、Charles Taylor |
| 知识社会学 | 「知识如何被生产、流通、合法化」 | 曼海姆、布尔迪厄、Latour |
| 殖民与后殖民 | 「想批判性分析现代性的另一面」 | Said、Spivak、Mbembe |
| 性别与身体 | 「想分析性别建构与身体经验」 | Butler、Haraway、Wittig |

**追问原则**：
- 最多 2 轮，不变成问卷
- 用户表达足够清晰 → 不追问，直接推荐
- 第二轮的目的是区分相似维度（"批判技术"是法兰克福学派路线还是 STS 路线？）

#### Step 2: 候选推荐

基于需求维度推荐 2-3 个候选学者。**先判断：人物 skill 还是主题 skill？**

- 用户的需求指向某种具体的分析视角 → 人物 skill
- 用户的需求指向某个领域的方法论传统 → 主题 skill（如"批判理论""民族志方法"）
- 不确定 → 推荐里同时包含两类，让用户选

**两个来源：**

**来源 A：本地已有 skill**——扫描 `~/.claude/skills/*-perspective/`，匹配现有学者镜片。已存在的零成本调用。

**来源 B：新蒸馏候选**——基于需求维度匹配。每个候选的展示格式：

```
### 候选 1: [学者名]  ⚡已有 skill / 🆕需要蒸馏

**核心镜片**：[此学者分析问题的独特视角，一句话]
**为什么适合你**：[直接对应用户研究需求，匹配逻辑要具体]
**学派定位**：[他属于什么传统、与同代人的差异]
**局限**：[这个视角的盲区——什么类型的问题这个镜片不擅长]
**语料可获取性**：[原文语种 + 是否有充足英/中译]
```

**推荐原则：**
- 不超过 3 个，差异化要明显（不要推荐 3 个都属于法兰克福学派）
- 已有 skill 优先展示
- 必须说清楚局限——没有万能的分析框架
- 必须说清楚语料可获取性——冷门学者蒸馏出来质量会受限

#### Step 3: 用户选择

- 选已有 skill → 直接激活
- 选新蒸馏 → 进入 Phase 0A 确认细节 → Phase 0.5 开始
- 都不满意 → 回到 Step 1 继续探索

---

### Phase 0.5 / [Workflow A.0]: 创建 skill 目录与采集预案

**收到确认后立即执行**，在调研之前完成。

#### 双路径架构（核心设计）

学者问道把"轻产物"与"重材料"严格分开，避免 skill 仓库被版权 PDF 与大文件污染：

```
路径 A · Skill 产物（轻量，可上 git）
~/.claude/skills/[scholar]-perspective/
├── SKILL.md                          # 最终产物
├── scripts/                          # 工具脚本（来自 scholar-wendao）
└── references/
    ├── research/                     # 7 个 agent 的调研结果（markdown 综述）
    │   ├── 01-monographs.md
    │   ├── 02-interviews.md
    │   ├── 03-style.md
    │   ├── 04-secondary.md
    │   ├── 05-debates.md
    │   ├── 06-genealogy.md
    │   └── 07-archive.md             # 多语言全文献清单（含获取链接）
    └── biography/                    # 生平人格素材（独立章节）
        ├── timeline.md
        ├── personality.md
        ├── relations.md
        └── controversies.md

路径 B · Library 重材料（永远不进 git，永久持有）
$SCHOLAR_WENDAO_LIBRARY/[scholar-slug]/
├── works/
│   ├── fr/                           # 学者母语原版 PDF
│   ├── en/                           # 英译本
│   └── zh/                           # 中译本（如有）
├── interviews/                       # 访谈与讲座 transcript
├── secondary/                        # 二手研究 PDF
└── biographies/                      # 传记类 PDF
```

#### Library 路径配置

`$SCHOLAR_WENDAO_LIBRARY` 是用户全局学术档案目录。优先级：

1. 用户已设置环境变量 `$SCHOLAR_WENDAO_LIBRARY` → 使用之
2. 用户使用 Obsidian 等知识库系统 → 推荐配置为已有的"数字图书馆"目录
   - 例：`export SCHOLAR_WENDAO_LIBRARY="$HOME/Documents/Obsidian/Library/_files"`
3. 都没有 → 默认 `$HOME/scholar-wendao-library/`（脚本自动创建）

#### Library 归档布局（v0.4 新增）

用户的 Library 可能采用两种命名约定，本框架两种都支持但**必须显式配置**，否则下载脚本可能造成污染（例：v0.3 实战中 download_open_access.sh 自动创建 `_files/fr/` `_files/en/` 子目录与扁平命名约定冲突）：

| 布局 | 命名 | 例 |
|---|---|---|
| `flat` | 全部 PDF 在 `_files/` 根目录，前缀+年份+语种 | `Stiegler2010_le_circuit_fr.pdf` |
| `by-language` | 按语种子目录 `_files/{fr,en,zh}/` | `_files/fr/2010_le_circuit.pdf` |

`Phase 0.5` 必须把所选布局写入 `references/research/_library_config.md` 的 `archive_layout` 字段。下载脚本（`download_open_access.sh`、`annas_acquire.py`）读此字段决定输出路径。**Phase 0.5 完成前必须确认布局**——询问用户「你的 Library 是扁平命名（建议）还是按语种子目录？」

**为什么这样设计：**
- ✅ Skill 产物可干净上 git（无版权 PDF 污染）
- ✅ Library 跨 skill 复用（蒸馏 Foucault 时已有的二手文献，蒸馏 Stiegler 时不用重下）
- ✅ 与已有学术工作流兼容（Obsidian / Calibre / Zotero / 自建文件夹都可以）
- ✅ 用户保留对自己档案的完整控制

#### Library 覆盖率扫描（v0.4 新增·"本地优先模式"判断条件具体化）

v0.3 实战暴露的问题：「在 Library 有一些 PDF」介于无和全有之间，无清晰处理路径。v0.4 把这一步具体化为可计算指标：

```
LOCAL_PDFS=$(find "$SCHOLAR_WENDAO_LIBRARY" -iname "*[Ss]cholarSlug*.pdf" -type f | wc -l)
EXPECTED_BOOKS=$(估算自学者主要专著数，可先用 5 作为 fallback)
COVERAGE=$((LOCAL_PDFS * 100 / EXPECTED_BOOKS))
```

| 覆盖率 | 模式 | 行为 |
|---|---|---|
| 0% | 纯网络 | 7 agent 全网络采集 |
| 1-30% | 本地补 | 网络 agent 优先；本地 PDF 进入 evidence 提取 |
| 31-70% | 本地优先 | 本地 PDF 全量进入 evidence；网络仅补缺口 |
| 71-100% | 纯本地 | 跳过部分网络 agent；evidence 提取作为主蒸馏源 |

扫描结果写入 `_library_config.md` 的 `coverage_report` 字段。

#### Phase 0.5 自动检查

- [ ] 路径 A 目录已创建在 `~/.claude/skills/[scholar]-perspective/`
- [ ] 解析 `$SCHOLAR_WENDAO_LIBRARY`，路径 B 目录已创建（按 slug 子目录或扁平命名前缀，依 `archive_layout`）
- [ ] **`archive_layout` 已明确**（`flat` / `by-language`，写入 `_library_config.md`）
- [ ] **`coverage_report` 已生成**（扫描 Library 现有 PDF 数量与预期主要专著数对比）
- [ ] `references/research/07-archive.md` 中的下载脚本调用使用路径 B 作为 `--output`，并传入 `archive_layout`
- [ ] 在 `references/research/_library_config.md` 记录使用的 Library 路径（供后续 update 时参照）

**完成检查**（自动执行）：

- [ ] 目录已创建
- [ ] 已读取学者所属国家/主导语言，决定信息源策略：
  - 法语学者：BnF Gallica、Persée、Cairn、本人著作的法语原版优先
  - 德语学者：DNB、SUB Göttingen、JSTOR DE
  - 英美学者：JSTOR、PhilPapers、机构仓库、本人主页
  - 中国学者：CNKI、万方、本人著作中文版、B 站/小宇宙学术访谈、官方采访（《思想的境界》《一席》《文化纵横》）；**永远排除知乎与微信公众号**
- [ ] 如果是更新模式：已读取现有 SKILL.md 的"调研时间"，标注哪些需要刷新
- [ ] 如果用户提供了本地语料 / Library 覆盖率 ≥ 30%：素材已分类入 `sources/` 或登记入 `_library_config.md`，标记为**本地优先模式**

**关键规则**：
- 每个 subagent 必须把调研结果写入对应的 md 文件。不存文件 = 没做
- **所有调研文件必须存在 skill 目录内部**（`references/research/`），绝不存到外部目录。Skill 必须自包含——复制目录就能独立使用，便于开源分发

---

### Phase 1 / [跨 A.1+A.2 与 B.2]: 多源信息采集

> **v0.4.2 拆分提示**：本节包含三件事，分属两个 workflow：
> - `harvest_works.py` + 4 harvester（metadata 全收集）= **A.1**
> - `download_open_access.sh` + Tier 1+2 自动下载 = **A.2**
> - 7 agent 调研产出 research / biography 文档 = **B.2**
>
> 单跑 Workflow A 时只跑前两件；单跑 B 时只跑 7 agent（基于 A 已下载的 Library 素材）。

#### 模式判断：本地语料 vs 网络搜索

| 模式 | 触发条件 | 策略 |
|------|---------|------|
| **纯网络** | Library 覆盖率 0%，无用户语料 | 7 个 agent 全部走网络+开放档案 |
| **本地补** | Library 覆盖率 1-30% | 网络 agent 主线；Phase 1.0 同步抽取本地 evidence |
| **本地优先** | Library 覆盖率 31-70% 或用户提供 PDF | Phase 1.0 抽取本地 evidence 为主，网络补缺口 |
| **纯本地** | Library 覆盖率 ≥ 70% 或用户明确"只用我给的" | Phase 1.0 evidence 为唯一来源，网络仅补传记类信息 |

**本地优先的执行逻辑：**

1. **先读本地素材**：将文件按 7 维度归类（一本书可能同时覆盖专著+表达+方法论）
2. **识别信息缺口**：哪些维度本地覆盖了？哪些薄弱？
3. **定向补充搜索**：仅对缺失维度启动网络 agent
4. **来源标记**：调研文件中明确区分"用户提供"vs"网络搜索"

---

#### Phase 1.0 / [Workflow B.1]：PDF 证据强制提取（v0.4 新增·本地优先 / 纯本地模式触发）

**为什么这一步必须存在**：v0.3 实战暴露——Phase 1 只读了用户已整理的 Obsidian Card 元数据，**任何一部本地 PDF 全文都没进入 Phase 2 蒸馏**，导致引文/页码/概念分期等关键细节失真（v0.3 SKILL.md 中至少 2 条引文页码不可在本地 PDF 验证）。

v0.4 强制 Phase 1.0 在 7 个 agent 启动**之前**完成：

```bash
python3 scripts/extract_pdf_evidence.py \
    --library "$SCHOLAR_WENDAO_LIBRARY" \
    --filter "{ScholarSlug}*.pdf" \
    --concepts examples/{slug}-perspective/_pdf_evidence/_concepts.json \
    --out examples/{slug}-perspective/_pdf_evidence \
    --head 30 --tail 30
```

`_concepts.json` 的多语言术语映射先用学者 1-2 个最高确定性概念冷启动（基于学者 Wikipedia 条目术语表），后续 Phase 2.1 蒸馏过程中可补全。

**输出**：每部 PDF → `_pdf_evidence/{book_basename}.md`，含：
- Head/Tail 页全文文本（前 30 + 末 30 页）
- Concept anchor search：每概念 ≤50 个带页码上下文
- `_index.json` + `_navigator.md`（概念 × 书命中矩阵 + OCR backlog 报告）

**OCR Backlog 自动检测（v0.4 新增）**：

`extract_pdf_evidence.py` 输出的 `_index.json` 含 `empty_pages` 字段。Phase 1.0 完成后必须扫描：

```python
# 任意 PDF 的 empty_pages / total head+tail pages > 50% → 标 OCR backlog
ocr_backlog = [r for r in index if r["empty_pages"] / 60.0 > 0.5]
```

OCR backlog 列表写入 `_pdf_evidence/_ocr_backlog.md`，每条记录：文件名、页数、PDF 元数据推断的真实书名、估计语言。提示用户：

> ⚠️ 检测到 N 部 PDF 无文字层（疑扫描版）。Phase 2 蒸馏将不能从这些书中抽证据。建议执行：
> ```
> brew install ocrmypdf  # 或 pip install ocrmypdf
> ocrmypdf --language fra+eng+chi_sim --skip-text input.pdf input.pdf
> ```
> OCR 完成后重跑 `extract_pdf_evidence.py --force`。

**Phase 1.0 退出条件**：
- 所有可机读 PDF 已生成 evidence markdown
- `_navigator.md` 已生成（含 9 概念 × top-3 书矩阵）
- OCR backlog 已生成并提示用户

---

#### 7 个 Agent 的任务分配（标准网络模式）

| Agent | 搜索目标 | 提取重点 | 输出文件 |
|-------|---------|---------|---------|
| 1 专著 | 学者出版的专著、代表论文、长篇序言 | 系统性论点、自创概念、引用习惯、章节结构 | `01-monographs.md` |
| 2 访谈 | 学术访谈、公开讲座、研讨会问答、播客 | 即兴回答中暴露的判断方式、被追问时的应对、改变立场的瞬间 | `02-interviews.md` |
| 3 风格 | 学者本人的写作样本（专著节选+论文+长访谈） | 行文节奏、概念使用频率、术语网络、定义习惯、辩护与让步的语态 | `03-style.md` |
| 4 二手 | 二手研究、书评、批评、传记、学位论文 | 学派分类、主要批评点、与同行比较、被引用次数最高的作品 | `04-secondary.md` |
| 5 论战 | 公开论战、立场转变、争议事件 | 论战对象与争议焦点、立场前后变化、面对批评的反应 | `05-debates.md` |
| 6 谱系 | 生平传记、师承关系、学术影响地图 | 师承（受谁影响）、学派归属、对后人的影响、与同代人的关系 | `06-genealogy.md` |
| **7 档案（新）** | **多语言全著作清单（OpenAlex/Crossref/Semantic Scholar/PhilPapers/BnF/CNKI 等）** | **完整著作元数据：标题、年份、语种、出版社、ISBN/DOI、引用数、OA 链接、获取路径** | `07-archive.md` |

#### 7 号 Agent 的特别说明（学术档案采集）

调用 `scripts/harvest_works.py`（包装 [Academix MCP](https://github.com/xingyulu23/Academix)）。Agent 7 的任务流：

1. **多语言查询**：以学者母语 + 英语 + 中文（如有）三组关键词查询，合并去重
2. **完整性检查**：交叉对比 OpenAlex / Crossref / 学者本人主页 / 维基百科书目，标注遗漏
3. **OA 标注**：每条记录标注是否开放获取，及可获取链接
4. **优先级排序**：按"奠基性专著 → 代表论文 → 重要访谈 → 编辑作品"分级
5. **输出清单**：`07-archive.md` 含完整书目 + 待采购清单（标注闭源版本的获取建议）
6. **触发下载**：对开放获取部分，调用 `scripts/download_open_access.sh` 自动下载到 `sources/works/`
7. **处理闭源**：调用 `scripts/annas_acquire.py`（包装 [annas-mcp](https://github.com/iosifache/annas-mcp)），按"原版语言 > 英译 > 其他译本"优先级，确保**至少一个语言版本被获取**

#### 每个 Agent 的硬性要求

- 调研结果**必须用 Write 工具写入** `references/research/0X-xxx.md`
- **返回前必须用 Read 或 `cat` 工具确认输出文件存在并展示前 50 行**（v0.4 新增·P1 #3 修复——v0.3 实战中多个 agent 写错路径或仅在消息里返回未真写文件）
- 每条信息标注信息源 URL 与可信度等级（一手/二手/传记类/学生回忆）
- 区分"学者本人写的"vs"他人转述的"vs"我推断的"
- 发现矛盾保留矛盾，不要和稀泥
- 如果是本地优先 / 纯本地模式：**优先引用 `_pdf_evidence/{book}.md` 中带页码的原文片段**作为论点证据，而非凭印象转述

#### 信息源优先级

| 来源类型 | 揭示什么 | 权重 |
|---|---|---|
| **用户提供的一手语料** | 完整原文，未经二手过滤 | **最高+** |
| 学者本人专著 | 系统性思考 | 最高 |
| 学者本人长访谈 | 即兴思维过程 | 最高 |
| 学者本人讲座 transcript | 教学场景的论证展开 | 高 |
| 同行评审论文 | 经过过滤的展演自我 | 高 |
| 实际学术决策（编辑作品/合作者选择） | 真实判断 vs 声称 | 高 |
| 二手学术研究 | 外部视角、定位、批评 | 中 |
| 传记 | 生平+人格，但有传记作者修辞 | 中-（需多源交叉） |
| 学生回忆 | 私下场景，但带回忆者偏见 | 中- |
| 维基百科 | 入门参考 | 低 |

#### 信息源黑名单（永远排除）

- **知乎**：洗稿严重、信息失真率高
- **微信公众号**：封闭生态、无法验证、大量二手转述
- **百度百科/百度知道**：信息陈旧不可靠

中文权威媒体可用：CNKI、万方、商务印书馆等学术出版社、《思想的境界》《一席》《文化纵横》《读书》《澎湃新闻·思想市场》、B 站原始讲座视频（非搬运号）、小宇宙学术播客。

---

### Phase A.3（v0.4.2 新增）：Tier 3+4 acquisition manifest 输出

**触发条件**：Workflow A 跑完 A.1+A.2 后。所有未能自动下载（Tier 3+4）的资料必须在此输出可读 manifest。

`_acquisition_manifest.json` 标准 schema（v0.4.2）：

```json
{
  "scholar": "Bernard Stiegler",
  "scholar_slug": "stiegler",
  "generated_at": "2026-XX-XX",
  "library_root": "/path/to/Library/_files",
  "items": [
    {
      "id": "stiegler-1994-tt1-fr",
      "title": "La technique et le temps, 1: La faute d'Épiméthée",
      "year": 1994,
      "language": "fr",
      "type": "book",
      "publisher": "Galilée",
      "isbn": "...",
      "doi": null,
      "openalex_id": "W...",
      "acquisition_tier": 4,
      "priority": "P0",
      "acquisition_status": "pending",
      "acquisition_hints": [
        "annas-archive.org（反爬严格，浏览器手动）",
        "Galilée 出版社官方网站可购电子版",
        "中国国家图书馆 / 大学图书馆机构外借"
      ],
      "intended_filename": "Stiegler1994_T_et_T_1_fr.pdf",
      "intake_completed_at": null
    }
  ]
}
```

**字段含义**：
- `acquisition_tier`：1/2/3/4 按 4 层架构标注
- `priority`：P0（核心专著，必须有）/ P1（重要论文）/ P2（补充）
- `acquisition_status`：`pending` / `intake_completed` / `acquired_via_browser` / `skipped`
- `acquisition_hints`：人类可读的"获取建议"列表（多条）
- `intended_filename`：建议的扁平命名（用于 intake 自动重命名）

**输出**：
- `_acquisition_manifest.json`（机器可读）
- `_acquisition_manifest.md`（人类可读，按 priority 排序，每条带建议）

**用户决策点**：用户阅读 manifest 后决定：
- a) 跳过未下载项（接受当前覆盖率，进 Workflow B）
- b) Tier 3：配置浏览器 cookies 重跑（v0.4.3 实现）
- c) Tier 4：手动下载若干本 → 进 Phase A.4

---

### Phase A.4（v0.4.2 新增）：用户主动导入

**触发条件**：用户已手动下载若干 PDF（从 annas / 出版社 / 机构图书馆）。

```bash
python3 scripts/intake_manual_pdf.py \
    ~/Downloads/Bifurquer-Stiegler.pdf \
    --config examples/stiegler-perspective/references/research/_library_config.md \
    --year 2020 \
    --slug Bifurquer \
    --lang fr \
    [--manifest-id stiegler-2020-bifurquer-fr]   # 可选：关联 manifest 条目
```

**自动行为**：
1. 重命名为扁平命名 `{file_prefix}{year}_{slug}_{lang}.pdf`
2. 移动到 `{library_files_path}` 目录
3. 跑 `extract_pdf_evidence.py`（仅对该新 PDF）→ `_pdf_evidence/{slug}.md`
4. 跑 `generate_library_cards.py`（增量）→ Card
5. 在 `_acquisition_manifest.json` 中标记 `acquisition_status: intake_completed`
6. 输出报告：哪部 PDF 加进来了，evidence 头/尾命中数，Card 路径

**Phase A.4 是可重复入口**：用户可以每天补一两本，scholar-wendao 累积式增长 Library。

---

### Phase 1.5 / [Workflow B 内]: 调研 Review 检查点

#### Step 1.5.0：主流程文件存在性兜底验证（v0.4 新增·P1 #3 修复）

**所有 agent 返回后，主流程必须立刻执行**：

```bash
for f in references/research/0{1..7}-*.md; do
    if [ ! -s "$f" ]; then
        echo "❌ 缺失或空文件: $f"
        # 主流程兜底：根据 agent 返回消息中的内容自写该文件
        # 如果消息中也无内容 → 标记为"信息不足维度"
    else
        echo "✓ $f ($(wc -l < "$f") 行)"
    fi
done
```

**触发条件**：v0.3 实战中至少 3 个 agent 出现"返回声明完成但文件不存在 / 写到错误路径"。Phase 1.5 第一步永远是 `ls -la references/research/` 验证 + 缺失项兜底。

#### Step 1.5.1：调研质量摘要

**所有 agent 完成 + 文件存在性验证通过后，暂停展示调研质量摘要：**

```
┌──────────────────┬──────────┬──────────────────────────┐
│ Agent            │ 来源数量  │ 关键发现                  │
├──────────────────┼──────────┼──────────────────────────┤
│ 1 专著           │ 12 本    │ 核心概念: 第三持存、组织学..│
│ 2 访谈           │ 8 段     │ 立场转变: 2015 年后...     │
│ 3 风格           │ 30K 字样本│ 高频术语: tertiary..      │
│ 4 二手           │ 25 篇    │ 主要批评: ...             │
│ 5 论战           │ 4 起     │ 与 Latour 之争...         │
│ 6 谱系           │ 完整     │ 师承: 德里达...           │
│ 7 档案           │ 47 本+200篇│ OA 覆盖率: 60%, 闭源 X 本│
├──────────────────┼──────────┼──────────────────────────┤
│ Phase 1.0 PDF    │ N 部     │ M 部可读 / K 部 OCR backlog│
├──────────────────┼──────────┼──────────────────────────┤
│ 矛盾点           │ 3 处     │ Agent1 vs Agent4 在 Y...  │
│ 信息不足维度      │ 1 处     │ 私人通信很难采集到         │
└──────────────────┴──────────┴──────────────────────────┘
```

用户确认调研质量 OK → Phase 2。
用户觉得某维度不够 → 补充调研后再继续。

---

### Phase 2 / [Workflow B.3]: 框架提炼（Synthesis）

7 个 agent 的素材汇总后，执行结构化提炼。先读取 `references/extraction-framework.md` 获取**学者版三重验证**方法论。

#### 2.1 概念地图提取（3-7 个核心概念）

学者的"心智模型" = 他的核心理论概念及其相互关系。**不是普通用词，是被他系统化为分析工具的术语**。

操作步骤：

1. **扫描**：从 `01-monographs.md` 到 `05-debates.md` 列出所有候选概念
2. **三重验证**：每个候选执行——
   - **概念体系化使用**：在 ≥2 部不同时期/不同主题的著作中作为分析工具被反复使用？
   - **推断生成性**：用这个概念能否推断学者对新现象的可能立场？
   - **学派区分度**：是否区别于同代/同流派学者？（如果福柯和阿甘本都用"主权"，区分度低）
   - 三重通过 → 核心概念；仅 1-2 重 → 降级为"次级概念"；0 重 → 丢弃
3. **取舍**：3-7 个核心概念。宁少勿多
4. **PDF 证据锁定**（v0.4 新增·本地优先 / 纯本地模式强制）：
   - 对每个核心概念，从 `_pdf_evidence/_navigator.md` 的「概念 × 书」矩阵读出 top-3 anchor 书
   - 打开对应 `_pdf_evidence/{book}.md`，读完该概念在该书的所有 hits
   - 每条引文必须能锁定到具体页码（`p.{N}`）
   - **概念定义、关键引文、引文页码必须能在某一份 `_pdf_evidence/{book}.md` 中直接搜到**——禁止凭印象引用，禁止从二手文献转引
   - 概念末尾"反复出现的著作"小节必须按 evidence 出现频次而非常识权重排序
5. **记录格式**：每个概念——
   - 名称（含原语）
   - 一句话定义（含来源文献页码）
   - 反复出现的著作（每条标 evidence 命中数 / 来源 anchor）
   - 典型应用场景
   - 与该学者其他概念的关系
   - 局限性
   - 关键引文（每条带书名+页码，必须可在 evidence 中定位）
   - **证据来源**（v0.4 新增）：列出该概念在哪些 `_pdf_evidence/{book}.md` 出现及命中数

**v0.4 概念条目模板**：

```markdown
### 核心概念 N：{中文名} *{原语}* / {English}

**定义**（{学者+年}+{源著}, p. {N}）：…

**[v0.4 选填] 子分期 / 进化 / 内部分类**（来自 evidence 系统讲述，例如 Stiegler 的"四阶段第三持存"必须直接来自 _pdf_evidence/Stiegler2020_Nanjing_Lectures.md pp. 22-39）：…

**反复出现的著作**：
- *Book A*（year）— evidence: `_pdf_evidence/{book_A}.md` (N hits)
- *Book B*（year）— evidence: `_pdf_evidence/{book_B}.md` (M hits)

**典型应用场景**：…

**与其他概念的关系**：…（每条尽量挂一个 page anchor）

**局限**：…

**关键引文**（必须可在 evidence 中定位）：
> "..."  —— *{Book}*, p. {N}

**证据来源**（v0.4）：
- `_pdf_evidence/{book_A}.md` — N hits（主源）
- `_pdf_evidence/{book_B}.md` — M hits
- `_pdf_evidence/{book_C}.md` — K hits
```

#### 2.2 方法论手稿（5-10 条分析进路）

学者面对一个新现象时，他的**第一步问什么、用什么数据、怎么组织论证**。可表述为"如果碰到 X 类材料/问题，则按 Y 路径展开分析"。

格式示例（Stiegler）：
- **遇到任何"技术对象"**：先追问其作为"第三持存"如何外在化人类记忆 → 再追问这种外在化是 pharmakon（毒-药）的哪一面 → 再追问当前的资本主义条件如何决定其偏向

#### 2.3 学术坐标

| 维度 | 提取内容 |
|---|---|
| 学派归属 | 后结构主义？批判理论第二代？分析哲学？混合？ |
| 主要立场 | 在该领域的核心分歧上他站哪边 |
| 自我定位 vs 他者定位 | 学者自称属于 X，但学术界普遍归他为 Y |
| 时代位置 | 在该领域思想史上的承前启后 |

#### 2.4 行文风格 + 概念语言

不是"语气"或"幽默感"，而是**学者在写作中如何使用概念、组织论证、回应反对**：

| 维度 | 提取内容 |
|------|---------|
| 概念引入方式 | 自创术语？借用并重定义？保持开放性的隐喻？ |
| 定义习惯 | 总是先精确定义？还是边写边演化？ |
| 论证节奏 | 演绎链条？归纳堆叠？多线索辩证？ |
| 反对处理 | 直接驳斥？容纳吸收？战略性沉默？ |
| 引用习惯 | 主要引同代人还是经典？引敌手吗？引谁的频率最高？ |
| 自我修正 | 公开承认前期错误吗？默默改？还是从不承认？ |

#### 2.5 智识谱系

```
[受谁影响] → 学者本人 → [影响了谁]
        ↕
   [横向对话/争论] ← 同代人

明确标注：
- 师承（导师/直接受教）
- 远程谱系（精神导师）
- 重要对话者（同代）
- 批判对象
- 被批判的位置
- 后继者
```

#### 2.6 论战与立场转变

学者最有信息量的不是稳定论点，而是**改变立场的瞬间**和**论战中暴露的判断**。

每条记录格式：
- 时间、议题、对手
- 学者的立场（变化前 / 变化后）
- 这次变化暴露了他什么底层判断
- 他事后是否反思/承认这次变化

#### 2.7 人格与处世（独立章节）

学者的思想与生平经常深度耦合（Stiegler 的"技术外在化"理论与他狱中读哲学的经验）。**但生平整合必须严格分级标注信息源**：

```
[事件] · 时间 · 事件描述
  ├ 来源类型: [本人自述 / 他者描述 / 传记作者推断]
  ├ 多源交叉验证: [是 / 否 / 部分]
  └ 与思想的关联: [本人明确说 / 他者推断 / 我们的判断]
```

**人格描写的来源分级**（参见 `references/biography-protocol.md`）：

| 来源 | 可信度 | 限制 |
|---|---|---|
| 学者本人在访谈中谈自己 | 中（自我呈现） | 公开自我可能有修饰 |
| 学者私人通信（已出版） | 高 | 但已被编辑选择过 |
| 终身合作者/亲属回忆 | 中-高 | 有情感倾向 |
| 学生回忆 | 中 | 师生关系不对等可能扭曲 |
| 学术对手回忆 | 中- | 可能贬损 |
| 传记作者描述 | 低-中 | 文学化处理严重 |
| 媒体二手报道 | 低 | 普遍失真 |

#### 2.8 诚实边界（最厚的章节）

参见 `references/humble-epistemics.md`，必须明确写出六大局限：

1. **波兰尼问题**：本镜片只能复现可显式表达的部分，学者的研究直觉与品味是默会的
2. **思想化石化**：截止到调研时间点的快照，之后的演变需要 update
3. **公开 vs 私下**：所有公开材料都是经过过滤的展演自我
4. **传记修辞污染**：所有传记类信息已分级标注，但仍然可能被叙事框架扭曲
5. **漫画化风险**：使用本镜片时如果发现自己在生产"段子集合"而非智识分析，立刻停止
6. **死亡-尊重边界**（v0.4 新增）：涉及学者死亡 / 自杀 / 监禁 / 重大创伤事件时，仅记录可公开核实的事实，不戏剧化、不连接因果、不用学者第一人称回应（即使在对话模式中）

---

#### 2.9 / [Workflow A.5] Library Card 自动生成（v0.4.1 新增 · 学者问道核心差异化）

**为什么这一步存在**：scholar-wendao 的真正定位不是只产出 SKILL.md，而是 **同时为用户的图书馆体系增建标准 Card**——让蒸馏过程变成研究知识库的实际增长。每个进入 Library 的 PDF 都应当配套生成符合用户 Vault 命名约定的 markdown Card，这样研究者在写作时可直接 `[[Cards/{ScholarSlug}{year}]]` 引用。

**触发条件**：本地优先 / 纯本地模式（即 `_pdf_evidence/` 已生成）。

**操作步骤**：

调用 `scripts/generate_library_cards.py`，对每部已抽取 evidence 的 PDF 执行：

1. **读源**：
   - `_pdf_evidence/{book}.md`（PDF 提取的页码上下文 + 概念命中）
   - `references/research/07-archive.json`（OpenAlex 元数据：title / year / language / coauthors / DOI / publisher）
   - 已有 Card（如果存在 `{vault_cards_path}/{ScholarSlug}{year}.md`）—— **增量更新模式**，保留用户手写的"文献笔记 wikilink""引用章节"等

2. **填充 Card 模板**（参见 `references/library-card-template.md`）：
   - frontmatter：`title / author / year / grade / has_pdf / status / tags / versions`
   - 关键词（从 evidence 的 concept_hits top-3 推断）
   - 完整引用（APA 7th，自动构造）
   - 多语言版本表（按 archive.json 的 versions 字段）
   - 一句话摘要（取自 evidence head pages 第一段，或 LLM 摘要）
   - 论文引用摘录（取自 evidence head/tail/concept_hits 中的高质量片段，带页码）
   - 关联：自动加"人物：[[{vault_people_path}/{ScholarName}]]"+"文献笔记：[[…读书笔记]] (待写)"

3. **写出**：
   - 路径：`{vault_archive_path}/{vault_cards_path}/{ScholarSlug}{year}.md`
   - 增量模式：合并现有 Card 的"📝 论文引用摘录"、"🔗 关联"、"## 一句话摘要"段（用户可能已手写过）

**v0.4.1 关键设计点**：Library Cards 写到用户的 Vault，**不**写到项目仓库的 `examples/{slug}-perspective/`。项目仓库内的 `examples/{slug}-perspective/` 仅保留：
- `SKILL.md`（perspective skill 主产物）
- `_vault_paths.md`（指向 Vault 内真实素材路径的索引）

这样的双源架构：用户 Vault 是单一真源 + 项目仓库是开源共享层。

---

### Phase 2.5 / [Workflow B 内]: 提炼确认检查点

Phase 2 完成后暂停展示提炼摘要：

```
提炼结果摘要：
- 核心概念：N 个（列出名称及原语）
- 方法论进路：N 条
- 学术坐标：[学派 / 立场 / 时代位置]
- 行文风格：[3 个关键特征]
- 智识谱系：[N 位上游 / N 位下游 / N 位横向对话者]
- 重大立场转变：N 处
- 内在张力：N 对
- 信息分级标注：一手 X% / 二手 Y% / 传记类 Z%
```

用户确认 → Phase 3。
不满意 → 回到 Phase 2 调整。

---

### Phase 3 / [Workflow B.4]: Skill 构建

将 Phase 2 提炼结果组装为可运行的 SKILL.md。

#### Step 1: 读取模板
读取 `references/scholar-template.md` 获取标准结构。

#### Step 2: 填充内容

| 模板 Section | 填充来源 |
|---|---|
| frontmatter description | 学者名 + 学派 + 触发词 + "默认第三人称分析镜片，对话模式 opt-in" |
| **激活默认模式（核心）** | 第三人称分析（"从 [学者] 的 [概念] 视角看..."）|
| **可选对话模式（opt-in）** | 用户主动说「切换到对话模式」「让我和 [学者] 直接对话」时启用，但全程保持元意识标注 |
| 学术身份卡 | 学派 + 学术坐标 + 一句话核心镜片 |
| 概念地图 | Phase 2.1 结果 |
| 方法论手稿 | Phase 2.2 结果 |
| 学术坐标 | Phase 2.3 结果 |
| 行文风格 + 概念语言 | Phase 2.4 结果 → 转为分析时如何使用术语的指引 |
| 智识谱系 | Phase 2.5 结果 |
| 重大论战与立场转变 | Phase 2.6 结果 |
| 人格与处世 | Phase 2.7 结果（独立章节，不塞进时间线） |
| 诚实边界 | Phase 2.8 结果（每条具体到操作层面） |
| 调研来源 | 7 个 agent 的引用汇总，分一手/二手/传记/访谈各自标注 |
| 创建者归属 | 固定内容："本 skill 由 [学者问道](https://github.com/tizzy916/scholar-wendao-skill) 生成 / 致敬 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 的方法论启发" |

#### Step 3: 默认输出模式（关键差异化）

生成的 perspective skill **默认是分析镜片模式**：

```markdown
## 激活规则（默认：分析镜片模式）

**本 skill 激活后，以学术分析者身份，使用 [学者] 的概念地图和方法论进路分析用户提供的材料或问题。**

### 输出格式
- 第三人称引用学者："从 [学者] 的 [概念 X] 视角看..."、"按照 [学者] 的方法论进路，分析这个材料应该先..."
- 显式标注使用了哪个概念："此处运用 [概念 Y]，因为..."
- 指出概念局限："但 [学者] 这个镜片对此类材料有以下盲区..."
- 不假装自己是该学者
- 不模仿语气、不模仿口头禅
- 必要时承认"超出 [学者] 思考过的范围，这是我（分析者）基于其框架的推断"

### 学术合规
- 涉及具体引用时附上来源（书名+章节）
- 区分"[学者] 明确说过"和"基于 [学者] 框架推断"
- 遇到本镜片不擅长的问题，明确说"此问题超出 [学者] 框架的有效范围"

### 可选：切换到对话模式（opt-in）
当用户**明确**说「切换到对话模式」「让我直接和 [学者] 对话」「角色扮演 [学者]」时，可以进入对话模式。但：
- 必须在第一回合声明："我以 [学者] 的视角与你对话，基于公开著作推断，**非本人观点**。任何此对话内容不可作为 [学者] 真实立场引用"
- 整个对话过程保持元意识：遇到无法基于 [学者] 著作推断的问题，明确退出角色说"超出范围"
- 用户说「退出」「切回分析模式」时立即恢复
```

#### Step 4: 质量自检

读取 `references/extraction-framework.md` 末尾的质量自检清单，逐项检查。不通过的项标注，回到对应 Phase 修复。

#### Step 5: 输出

将完成的 SKILL.md 写入 `~/.claude/skills/[scholar]-perspective/SKILL.md`，并在 `~/.agents/skills/` 创建软链接。

---

### Phase 4 / [Workflow B.5]: 质量验证

生成 skill 后，用子 agent 执行 4 项测试（独立 agent 避免自评偏差）：

#### 4.1 已知测试（Sanity Check）
选 3 个该学者公开表态过的议题，spawn 子 agent 带新 skill 分析，对比实际立场。
- 方向一致 → 模型有效
- 偏离 → 调整概念地图权重

#### 4.2 边缘测试（Edge Case）
选 1 个该学者没公开讨论过但相关的议题，用 skill 推断。
- 期望："基于概念 X 和方法论进路 Y 的推断，可能...但超出学者明确框架"
- 不应该斩钉截铁地代学者发言

#### 4.3 漫画化检测（Caricature Test）⭐ 学者问道独有
用 skill 分析一段日常材料（如新闻报道、社交媒体帖子）。
- **PASS**：分析中调用了概念，但保持智识严肃性
- **FAIL**：变成"学者口头禅集合"或"段子机器人"
- 如果 FAIL，说明在 Phase 2.4（行文风格）抓得过表面，回去重做

#### 4.4 默会知识声明检查
检查 SKILL.md 是否明确包含：
- [ ] 波兰尼问题声明
- [ ] 化石化时间标注
- [ ] 公开 vs 私下区分
- [ ] 传记修辞污染说明
- [ ] 漫画化风险警示
- [ ] 信息源分级标注
- [ ] **死亡-自杀-尊重边界声明**（v0.4 新增·见 `humble-epistemics.md` 第六项）

#### 4.5 引文 page-anchor 强制核验（v0.4 新增·P0 #2 实施）

**触发条件**：本地优先 / 纯本地模式（即 `_pdf_evidence/` 已生成的情况）。

**检查规则**：

```python
# 概念地图中每条带页码的引文：
# 模式 "p. N" 或 "p.{N}" 或 "页 N"
for citation in extract_citations(skill_md):
    book = citation.source_book
    page = citation.page
    quote = citation.quote_text
    evidence_md = f"_pdf_evidence/{slug(book)}.md"
    if not evidence_md_exists:
        warn("引文 anchor 不可证（evidence 文件缺失）")
        continue
    # 读 evidence_md 中 p.{page} 段落，比对 quote 头 80 字符
    if not quote_substring_in_evidence_page(quote, evidence_md, page):
        FAIL(f"引文不可定位: '{quote[:60]}...' 标 {book} p.{page}，"
             f"但 evidence_md 该页无此文本")
```

**v0.3 实战教训**：v0.3 SKILL.md 至少 2 条引文页码不可证（*WMLWL* 引文 p.19 不存在 / *Pharmacology* organology 定义实际在 p.43 而非 p.46）。这些引文都是凭 Obsidian Card 摘录或印象写出。v0.4 必须 fail-fast。

**不通过处理**：
- 该条引文末尾标注「⚠️ v{X} 引文页码不可在本地 PDF 中验证」
- 在 evidence 中找替代引文，或删除该条
- 在 SKILL.md 末尾"v0.X 修订记录"小节记下变更

#### 4.6 Narrative-Bracketing 自动检测（v0.4 新增·P1 #4）

**触发条件**：人格与处世章节（Phase 2.7 输出），尤其是含"形成性事件"段落。

**v0.3 教训**：Stiegler "1978 年武装抢劫服刑 5 年期间读哲学"段落，子 agent 的 prompt 强调了 narrative-bracketing（事实层 + 叙事层并标），但主 SKILL.md 输出无强制校验，结果可能出现"狱中读哲学"作为浪漫化叙事写入而无双层标注。

**检查**：

```python
formative_events = extract_formative_events(skill_md)  # heuristic：日期+事件+影响
for event in formative_events:
    has_fact_layer = bool(re.search(r"事实层|fact-level|来源等级", event.text))
    has_narrative_layer = bool(re.search(r"叙事层|narrative-level|学者自述|传记修辞", event.text))
    if not (has_fact_layer and has_narrative_layer):
        WARN(f"形成性事件 '{event.summary[:40]}' 缺 BRACKETING 双层标注")
```

#### 4.7 通过标准

| 检查项 | 通过标准 | 不通过信号 |
|---|---|---|
| 概念地图数量 | 3-7 个，每个有 ≥2 来源 | <3 或 >10 |
| 每个概念的局限性 | 明确写出失效条件 | 只写优点 |
| 方法论进路具体性 | 可被新材料触发 | 只适用于原始案例 |
| 智识谱系完整性 | 上游+横向+下游都有 | 单线孤立 |
| 信息源分级 | 每条调研有等级标注 | 无标注/混淆 |
| 一手来源占比 | >50% | 主要靠二手转述 |
| 漫画化检测 | PASS | FAIL |
| **诚实边界（六项）** | 全部声明（含自杀-尊重边界） | 缺任意一条 |
| **引文 page-anchor 核验** | 100% 引文可在 evidence 定位 | 任何一条不可证 |
| **Narrative-Bracketing** | 形成性事件双层标注 | 缺事实/叙事层 |
| **PDF Evidence 覆盖** | 每核心概念 ≥1 个证据来源 | 0 evidence 来源 |

验证通过 → 交付。不通过 → 标注薄弱环节，回到对应 Phase。
**迭代上限**：Phase 2→4 最多循环 2 次。2 轮后仍不达标 → 在诚实边界中标注薄弱维度，交付当前最优版本。

---

### Phase 5 / [Workflow B.5 子步骤]: 双 Agent 精炼（可选，开源前推荐）

参考 [女娲.skill 的 Phase 5](https://github.com/alchaincyf/nuwa-skill/blob/main/SKILL.md)，但增加学术合规检查维度。

**并行启动：**

**Agent A（结构评估）**：
- 8 维度评估：激活规则清晰度、概念地图深度、方法论可操作性、信息源分级严格度、诚实边界具体性、漫画化检测健壮性、引用规范、跨语言素材整合
- 输出最弱 2-3 个维度的具体改进建议

**Agent B（学术合规审）**：
- 检查所有概念引用是否附原文出处
- 检查"明确说过"vs"框架推断"区分是否清晰
- 检查传记类信息是否符合 `biography-protocol.md` 的分级标准
- 检查是否避免了对学者人格的过度推断（特别是已故学者）
- 输出 2-3 处具体修订建议

主 agent 综合两份报告 → 应用不冲突的改进 → 展示变更摘要请用户确认。

---

### Phase 5.5 / [Workflow B.6]: Vault 同步（v0.4.1 新增 · 端到端工作流的关键步骤）

**为什么这一步存在**：scholar-wendao 是为 agent 准备的 **学术研究全栈工作流系统**——它的输出不只是给 GitHub 看的 demo，而是要 **进入用户的真实研究知识库**。前面所有 Phase 产出的素材如果只留在项目仓库的 `examples/{slug}-perspective/`，就只是 demo。Phase 5.5 的工作是把它们落到用户 Vault 的对应位置，让蒸馏过程同时增长用户的图书馆 + 概念笔记 + 谱系网络。

**触发条件**：用户在 `_library_config.md` 中配置了 `vault_archive_path` 字段。

**配置项**（`_library_config.md`）：

```yaml
vault_archive_path: "$HOME/Documents/Obsidian/MyVault/02 · Knowledge"
library_files_path: "Library/_files"      # PDF 落点（已有路径）
library_cards_path: "Library/Cards"        # Card 落点
concepts_path: "Concepts"                  # 概念笔记落点
permanent_notes_path: "Permanent Notes"   # 谱系永久笔记落点
moc_path: "MOC Maps"                      # 主题地图落点
people_path: "People"                     # 人物志落点
project_workspace_path: "Projects/scholar-wendao/{slug}"  # research/biography 落点
```

**操作步骤**：调用 `scripts/sync_to_vault.py` 执行：

1. **PDF Library**：
   - `_files/{ScholarSlug}{year}.pdf` 已经在用户 Vault 里（download_open_access.sh 直接下到那里）—— 不需移动
   - 验证扁平命名一致性（`flat` archive_layout）

2. **Library Cards**（来自 Phase 2.9）：
   - 从项目仓库的 `_pdf_evidence/` + `07-archive.json` 生成 → 写到 `{vault}/{library_cards_path}/{ScholarSlug}{year}.md`
   - 增量模式：保留用户已手写的内容

3. **概念笔记**（Concepts）：
   - 检测 Vault 内是否已有匹配的概念笔记（如 `第三持存.md`）
   - 已有 → 末尾追加"📎 v{X} PDF 证据来源"小节，链接到对应 Cards
   - 不存在 → 不创建（避免污染用户已有的概念体系，等用户主动建）

4. **永久笔记**（Permanent Notes / 谱系）：
   - 类似 Concepts：仅在已有谱系笔记上追加 wikilink，不创建新文件

5. **MOC**（主题地图）：
   - 检测 `{vault}/{moc_path}/{学者中文名}研究 MOC.md` 是否存在
   - 已有 → 在末尾"🔬 v{X} 蒸馏素材"小节追加：
     - 链接到 perspective skill SKILL.md
     - 链接到 Library Cards（按年份分组）
     - 链接到 research/ 文档
     - 链接到 biography 时间线
   - 不存在 → 创建新 MOC（最小骨架），用户后续手动扩展

6. **人物志**（People）：
   - 类似：在已有 `{ScholarName}.md` 末尾追加 v{X} 蒸馏 biography 的精华摘录 + 完整文档 wikilink

7. **research / biography 工作区**：
   - 复制（or 软链）`references/research/` + `references/biography/` 到 `{vault}/{project_workspace_path}/`
   - markdown 内的相对路径引用全部 wikilink 化

8. **项目仓库瘦身**：
   - 在项目仓库 `examples/{slug}-perspective/` 生成 `_vault_paths.md`（索引,内容是 Vault 路径列表）
   - 选项 (a) 极简：删除 `references/` 和 `_pdf_evidence/`（仅保留 SKILL.md + _vault_paths.md）
   - 选项 (b) 轻量（默认）：保留 `references/research/` 7 篇 + `_pdf_evidence/_navigator.md`，作为开源访客可见的"产出形态"参考
   - 选项 (c) 照旧：保留全部（Vault 也有副本，双份）

**Phase 5.5 退出条件**：
- 用户 Vault 内的 7 个目标位置全部接收到对应素材
- 项目仓库 `examples/{slug}-perspective/` 已按选项 a/b/c 处理
- `_vault_paths.md` 写入完整路径索引

---

### Phase 6 / [共享层]: GitHub 工作流（v0.4.1 新增 · 端到端可重现）

**为什么这一步存在**：scholar-wendao 的开源价值在于 **整套工作流可被其他研究者复用**。Phase 6 把项目仓库的更新提交并推送，让蒸馏成果可被开源社区追溯。

**触发条件**：在 Phase 5.5 完成后，且项目仓库有 staged 改动。

**操作步骤**：

1. **生成 commit message**：
   - 标题：`v{X}: {ScholarName} perspective skill — distilled from {N} PDFs + {M} non-book sources`
   - 摘要：核心概念列表 + quality_check 得分 + page-anchor 通过率 + Vault 同步路径概览
   - 工具尾行：`Created by https://github.com/tizzy916/scholar-wendao-skill`

2. **stage + commit**：
   ```bash
   git add SKILL.md scripts/ references/ examples/{slug}-perspective/ README.md
   git commit -F <(echo "$COMMIT_MSG")
   ```

3. **询问 push**（不直接 push，用户确认）：
   - 默认推送到 `origin/main`
   - 如果用户配置了 `dev_branch`，推送到 dev 分支让用户 review 后 merge

**Phase 6 不应该**：
- 把 Vault 内素材推到 git（Vault 内可能含版权 PDF + 私人笔记）
- 在用户未确认时执行 `git push --force` 或修改历史

---

## 更新与重蒸（v0.4.2 双工作流细分）

v0.4.2 区分三种"再次跑"的语义。agent 必须根据用户表达准确路由：

### 模式 A · 仅补料（"为 X 补料" / "更新 X 的图书馆"）

**触发**：用户已有 X 的 skill + Library，想新加几本书 / 几个讲座链接到库里。

**行为**：仅跑 Workflow A（A.0/A.1/A.2/A.3/A.4/A.5），不动 SKILL.md。
- 新 PDF 通过 A.4 主动导入 → Library/_files
- 增量更新 / 新建 Library Cards
- 更新 acquisition_manifest 标注新增项

### 模式 B · 轻量 update（"更新 X 的 skill"）

**触发**：用户已有 X 的 skill，最近有新文献 / 新讲座，想增量补充而非重做。

**行为**：v0.4.1 既有逻辑：
1. 读取现有 SKILL.md 的"调研时间"，标注距今多久
2. 启动 Agent 1（新著作）+ Agent 2（新访谈）+ Agent 7（档案增量更新）
3. 对比新信息 vs 现有内容：
   - 新信息强化现有概念 → 补充案例
   - 新信息冲突 → 标注立场转变（不删除旧版，记入论战 section）
   - 出现新概念 → 考虑增加
4. 更新 SKILL.md 的"最新动态"+ 调研时间
5. **不重写整个 skill，只增量**

### 模式 C · 重蒸（"重蒸 X" / "用新资料重做 X 的镜片"）

**触发**：Library 经过多轮 A.4 大幅扩充（如新加了 10+ 部关键专著），现有 SKILL.md 基于的 evidence 已不充分，需要整体重做。

**行为**：
1. **archive 旧版**：把当前 `examples/{slug}-perspective/SKILL.md` 移到 `examples/{slug}-perspective/_archive/SKILL_v{X}_{date}.md`
2. **重跑 Workflow B 全部**（B.1 → B.6）
3. **diff 新旧**：在 commit message 中 highlight 哪些概念因新材料而**实质改变**
4. **保留**：用户在旧 SKILL.md "## 引用章节"、"📝 论文引用摘录" 等手写小节由 Phase 5.5 增量合并保留

模式 C 与模式 B 的区别：B 是"加几条"，C 是"基于扩充后 evidence 重新组织所有概念定义、引文、谱系"。

---

## 品味守则（速查）

| 原则 | 一句话 |
|------|--------|
| 概念体系化 > 金句 | 一个反复使用的术语网络比 50 句精彩论断更揭示思维 |
| 论战 > 一致 | 改变立场和被批评的瞬间最有信息量 |
| 一手 > 二手 | 直接读学者本人，比读"X 学者研究"更接近真相 |
| 局限 > 包装 | 把局限明确说出来，比把局限藏起来更可信 |
| 镜片 > 替身 | 我们要的是分析工具，不是代言人 |

### 绝不做的事
- 编造该学者没说过的话
- 把通用学术常识包装成此学者的"独特见解"
- 忽略对该学者的尖锐批评（即使合规要求婉转处理也要保留）
- 在信息不足时强行生成完整 skill（宁可写出诚实的 60 分）
- 用第一人称扮演作为默认输出（必须用户主动 opt-in）
- 把传记作者的修辞当事实

---

## 特殊场景

### 已故学者 vs 在世学者
- **已故学者**：闭合语料，调研时间标注一次即可
- **在世学者**：标注调研截止日期，建议每 12-24 个月做一次 update

### 中国学者 vs 西方学者
- **中国学者**：CNKI/万方/商务馆/三联书店为主、本人讲座（B 站原始）、官方采访（《思想的境界》《一席》《文化纵横》《读书》）。**永远排除知乎、微信公众号、百度百科**
- **西方学者**：本人著作 + JSTOR + PhilPapers + Google Books + 机构主页
- **中文译介过来的西方学者**：**优先读原语**，中译只作为参考。表达 DNA 必须基于原文，否则就是在蒸馏译者而非作者

### 主题 skill（如"批判理论""民族志方法"）
输入不是单个学者而是方法论传统时：

| Phase | 人物 skill | 主题 skill 变体 |
|---|---|---|
| 0A | 确认学者+聚焦 | 确认主题边界+流派范围 |
| 0.5 | `[scholar]-perspective/` | `[topic]-framework/` |
| 1 | 7 agent 围绕一人 | 先确定主题的 3-5 个核心人物，每人 1-2 个 agent（不是 7 个） |
| 2.1 | 一人的概念地图 | **领域共识**+**各家分歧** |
| 2.4 | 一人的行文风格 | 不模仿，用中性专业表达 |
| 2.7 | 一人人格 | 跳过（主题没有人格） |
| 3 | 用 scholar-template | 调整模板：去掉学术身份卡，改为"领域概览"+"流派对比" |

### 冷门学者（公开信息 <10 条来源）
1. Phase 0.5 就告知用户"信息量受限，质量会打折"
2. 概念地图减至 2-3 个，每个标注"基于有限信息推测"
3. 诚实边界 section 加大，列出"哪些维度信息不足"
4. 鼓励用户提供一手语料

### 蒸馏用户的导师/师兄/同事
1. 学者问道无法从公开渠道蒸馏私人学者
2. 引导用户提供：导师的论文/讲义、合作论文、面谈录音、给学生的反馈邮件
3. Phase 1 改为分析用户提供的素材
4. 注意"师生关系不对等"——学生的回忆可能美化或贬损，多源交叉

---

## 最后

> *学者问道的 skill 不是替代学者，是把他的分析镜片借给你。*
>
> *用别人的概念地图，看自己的研究材料；用别人的方法论，问自己未问的问题。*
>
> *不为了模仿他们，是为了拓展你的思维边界——这是与古今学者建立的真正学术对话。*

---

## 关于作者 / About the Author

沈聪,中央美术学院实验艺术学院本科,清华大学科学史系硕士(导师 [胡翌霖](https://yilinhut.net/author/admin)),科技文创公司 [天与视界 TIANYU VISION](https://tianyu.art/) 创始人 & CEO。学术训练横跨实验艺术、科学史与技术哲学;创业方向是用 AI 做科研可视化、科学传播与科艺融合。

「学者问道」诞生于一个具体的写作困境——做学位论文《技术自由主义》时,他不需要"和 Stiegler 聊天",而是需要把多位学者(Stiegler、Rancière、Arendt、Aristotle……)的分析镜片装进自己的研究流程,边读材料边能立刻调用。市面上没有这样的工具,只能自己造——这就是学者问道。

📮 [GitHub @tizzy916](https://github.com/tizzy916) · shencong916@gmail.com · 欢迎纠错、合作、交流

---

> 本 skill 由 [学者问道](https://github.com/tizzy916/scholar-wendao-skill) 生成
> 方法论受 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 启发，专为人文学术场景重新设计
