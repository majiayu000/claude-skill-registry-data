---
name: ai-visibility
description: 'Measure whether AI assistants actually name and recommend a brand, and diagnose why they name competitors instead. Use when the user asks if ChatGPT, Doubao, DeepSeek, Yuanbao, Qwen, Kimi, Perplexity or Google AI Overviews recommend them, wants to know which brands AI lists for their category, or wants a repeatable sampling protocol instead of one-off screenshots. Builds question sets, samples answers, compares batches and reports the gap. For page-level crawlability first, see ai-crawler-audit. For the content that closes the gap, see ai-content-writer.'
license: MIT
metadata:
  version: "1.8.0"
  homepage: https://github.com/Fangx-AI/geo-doctor
---

# AI 可见度实测

只回答一个问题：**在用户真会问的问题上，AI 提到我了吗，推荐的是谁，凭的是什么。** 用数据说话，不用感觉。

用用户的语言交流；本文件是中文的，读懂后用用户的语言转述。

## 什么时候用

- "豆包 / DeepSeek / ChatGPT 会推荐我吗？"
- "AI 一提这个行业就只报竞品的名字，为什么？"
- "怎么证明 AI 提过我？" / 要给老板或客户一份可复现的实测
- "上次做的优化有没有用？"（复查）

不接的活：页面能不能被抓到 → `ai-crawler-audit`；写内容 → `ai-content-writer`；发布 → `geo-publish`。

## 四条必须守住的证据纪律

这四条是这个技能的全部价值，违反任何一条，报告就作废：

1. **问的是用户会问的问题**，不是品牌名。问"哪款记账 App 好用"能测出可见度，问"XX 记账 App 怎么样"只能测出它认不认识这个词。
2. **"提到 / 推荐 / 引用"是三件不同的事**：提到 = 回答里出现品牌名；推荐 = 明确建议用你；引用 = 把你当来源链接。分开统计，不许合并成一个"AI 可见度"数字。
3. **AI 没回答 ≠ AI 没提到你。** 拒答、超时、返回错误单独记，不进分母，也不记成"未提及"。
4. **API 的回答不等于用户在 App 里看到的回答**。API 结果必须标"入口=API"、单独成批、只看趋势；要下结论就在真实 App 里人工采样确认。

## 流程

以本 `SKILL.md` 所在目录为技能根，模板在 `assets/`，脚本在 `scripts/geo-probe.mjs`（零依赖）。

### 1. 先出关键词表 → `geo/keywords.csv`，再出问题基线 → `geo/questions.csv`

**关键词是题的上一层。** 买家真正输入的是词（"漏拧""包夜多少钱"），题只是把词放进一个处境里说成人话。跳过词直接写题，写出来的就是厂家视角的自问自答。

- 词的来源、意图四分法、按 SERP 重叠聚类、聚类缺口，都是搜索侧的成熟做法，**直接用，别自己发明**：见 `references/keyword-scene.md`。
- 模板 `assets/keywords.csv`，字段：关键词 / 场景 / 意图 / 旅程 / 聚类 / 落地页 / 来源类型 / 来源 / 证据等级。
- 每个非导航型词至少生成一道题；每个场景至少有一个商业调研型或交易型的词；没有落地页的词写 `缺`，那就是内容任务清单。

```bash
node scripts/geo-probe.mjs keywords geo/keywords.csv --questions geo/questions.csv --brand "我的品牌,别名"
```

它会反查三件事：哪些词一题都没有、哪些题挂的词不在词表里、哪些场景只有探索没有选型。

**先问三件事，不要更多**：客户做什么（品类 + 场景）、品牌与城市商圈、有没有用户原话（没有就说"没有"，不追问）。竞品名单和问法线索**自己查**——搜索"城市 + 品类 + 推荐 / 哪家好 / 排行"，从结果和点评里挑 3–5 个写进对比题，来源列写清检索出处。

按 `references/questions.md` 写，模板见 `assets/questions.csv`。这一步不是"随手编 20 道题"：问题集本身是测量的一部分，换一套问法结论就会变，所以每道题都要有类型、形状、限定条件、来源、证据等级和判定标准。

- **四类题**：A 不带品牌的推荐（约 40%，主战场）、B 品牌事实（30%）、C 不适合场景（20%，至少 2 道）、D 使用排错（10%）。
- **两层题集**：12–18 道标 `核心` 的**仪表题**，冻结后只用于报率和复查；另外 10–20 道 `一般` 的**雷达题**每轮可换。
- **问法形状**至少覆盖 5 种（品类发现、找替代、直接对比、排错……），写法与陷阱见 `references/question-shapes.md`。形状决定 AI 会不会真的去检索：商业意图类提问触发检索的比例远高于"什么是 X"。
- **场景 × 旅程**：每题标上「客户在什么处境下问」（场景）和「在决策的哪一段」（探索/选型/对比/口碑）。先排出矩阵再写题，能看到哪一格是空的——二十道题全问"哪家好"等于只测了一个数。做法见 `references/scenario-matrix.md`。

写完先体检，再采样：

```bash
node scripts/geo-probe.mjs check geo/questions.csv --brand "我的品牌,别名"   # 体检，含矩阵覆盖率
node scripts/geo-probe.mjs matrix geo/questions.csv                        # 只看矩阵，空格就是该补的地方
```

`fail` 有就退出码 1，说明这批题现在采样出来的数不能用（最常见：A 类题里写了自家品牌名、C 类为 0、题量不足 12、证据等级非法）。`warn` 不阻塞，但要在报告里写清为什么保留——矩阵里缺选型题、缺对比题、构造题占比过高都属于这一类。

### 2. 采样 → `geo/runs/<批次>/` + `geo/runs.csv`

按 `references/sampling.md` 执行。两条路可以混用，但**必须分批记录**：

- **人工采样（结论用这个）**：在目标 AI 的 App 或网页里逐题问，把整段回答原样贴回来。同一题至少问 2 次，因为同一个模型两次回答可能不同。
- **API 采样（趋势用这个）**：有 Key 时自动问。

```bash
node scripts/geo-probe.mjs run geo/questions.csv --ai deepseek,qwen --brand "我的品牌,别名" --competitors "竞品甲,竞品乙" --times 2
node scripts/geo-probe.mjs run geo/questions.csv --ai deepseek --brand "Acme" --dry-run
node scripts/geo-probe.mjs report geo/runs.csv --out geo/report-2026-11-16.md
```

没有 Key 时 `run` 会直接告诉你缺哪个环境变量并以退出码 2 结束——这是正常路径，改用人工采样即可，不要为此去申请 Key。

### 3. 诊断 → `geo/diagnosis.md`

按 `references/diagnosis.md` 做。至少要回答：

- 每题的 A/B 类、被推荐的品牌序列、我在第几位、我缺席哪几题；
- 它推荐别人时**读了哪些网站**（回答里的引用链接和来源），这些站就是内容要打进去的地方；
- 差距的原因分类：没人写过这个题 → 有内容但没被抓到 → 被抓到但事实说错了。三类的处方完全不同。

### 4. 复查 → `geo/report-<日期>.md`

按 `references/retest.md` 做：**同一份问题集、同样的次数、同样的平台**，换一个新批次，逐题对比上一次。不许改题、不许换平台后跟旧数据直接比。

## 没有脚本或不能联网时

- 不能跑 `geo-probe`：用用户贴回来的回答做同样的统计，手工记进 `runs.csv`（格式见模板），并注明"人工采样"；问题集则按 `references/questions.md` 末尾的检查项逐条人工核对，核对不了的项目写明"未验证"。
- 不能联网：只做问题集和统计，把"要去哪个 AI、问哪几题"写成清单交给用户；不要凭空写出回答。

参考 `references/ai-sources-cn.md`（国内 AI 从哪些平台取信息）和 `references/ai-sources-global.md`（ChatGPT、Claude、Perplexity、Google、Copilot 的来源与要放行的爬虫），用来解释"为什么它读的是那几个站"。

## 产出

`geo/questions.csv`、`geo/runs/<批次>/`、`geo/runs.csv`、`geo/diagnosis.md`、`geo/report-<日期>.md`。已有批次不覆盖，新增批次并标日期。

## 结束时

用 3 到 5 行给结论：问了几题、每题几次、我在几题里被提到、被推荐的是谁、最该补的是哪一题。数字后面必须跟口径（平台、入口、次数），没有口径的数字不许说。
