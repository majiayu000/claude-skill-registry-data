---
name: science-journal-intel
description: Use when you need to know how a journal actually behaves rather than what its aims-and-scope page claims — its real subfield mix over the last two years, first-round review duration and comment difficulty from authors, Chinese-author review speed and accept-rate wording; also use when a manuscript was rejected for "scope" and you need evidence about which journals genuinely publish that kind of work.
---

# 期刊情报：看它发过什么，不看它说自己喜欢什么

## 为什么需要这一层

`aims & scope` 是营销文案。真正决定送审的是**编辑桌上那堆稿子的分布**。
一本刊过去两年在你这个子领域发了 0 篇，你的 cover letter 写得再好也过不了初筛；
发了 9%，那就是它的主场之一。这个差别 scope 关键词永远告诉不了你。

`science_journal_intel` 把三个独立来源拼成一张卡：

| 源 | 回答的问题 | 记的是什么 |
|---|---|---|
| OpenAlex | 它**实际**在发什么 | 近两年每篇论文的 primary topic，按 subfield 汇总占比 |
| SciRev | 作者**实际**经历了什么 | 首轮月数、总量月数、即时拒天数、审稿轮数、意见难度、样本数 |
| LetPub | 中国作者**实际**怎么说 | 审稿速度档、录用比例措辞、中科院分区、IF |

三个源互相独立：谁挂了就在 `degraded[]` 里点名，其余照常给结论。

## 一、用 topicFootprint 判断「这是不是我的主场」

```
science_journal_intel({ journalId: "nature", title: "<你的标题>", keywords: ["protein folding"] })
```

输出里的 `topicFootprint` 有两层：

1. `topSubfields`：该刊近两年产出按子领域的分布。**看最大值**——
   最大子领域只有 9%，说明它是综合刊（Nature 就是这样，Molecular Biology 9.1%）；
   最大子领域 45%，说明它是专刊，投不进去的领域基本没戏。
2. `hitShare`：你的子领域占该刊产出的比例。这是**加权后的命中**，
   稿件标题+关键词先被映射到 1–4 个子领域，再逐一对分布取占比求和。

读法：

| hitShare | 含义 | 动作 |
|---|---|---|
| ≥ 5% | 主场，编辑天然认这类稿 | 直接投，cover letter 提一句连续性即可 |
| 1–5% | 边缘，需要读者相关性论证 | 投，但第 4 段必须写「为什么本刊读者会关心」 |
| < 1% | 几乎不发这类 | 换刊；除非你有跨领域意义（那就按综合刊投，别按专刊投） |
| 0（未命中） | 近两年零篇 | 强烈考虑换刊，风险等同于赌博 |

**铁律**：`hitShare` 是**统计事实**——该刊近两年产出中落在你子领域的比例。
它**不是**录用概率，也不做任何概率推算。没有任何工具能预测录用，只能告诉你「这类工作在这本刊出现过几次」。

## 二、用 reviewReality 排时间表，不用它做取舍

SciRev 的数据是作者自报的实际经历，回答的是「投进去要等多久、会被怎么打」：

- `firstReviewMonths` / `handlingMonths`：**首轮**和**从投到终审决定**的月数。
  毕业/结题倒排时间时用总量，不要用首轮自我安慰。
- `immediateRejectDays`：desk reject 平均几天。这个数字小说明初筛快，等你等到第 20 天还没动静，
  大概率已经进外审了——可以据此决定要不要催稿。
- `commentDifficulty`（1–5）：审稿意见的严厉程度。≥4 的刊要预留一轮大改的实验量。
- `reviewCount`：样本量。**< 10 条时只当参考**，工具会把 confidence 降到 low。

SciRev 没有该刊 → `degraded` 里有 `scirev`，`reviewReality` 缺失。
这时候不要用 LetPub 的速度档去替代月数——量纲不同，会把 6 周当成 6 个月。

## 三、用 chinaIntel 看中国作者的真实反馈

LetPub 是中文社群的投稿经验，价值在两点、也只有这两点：

1. **审稿速度档**（很快 / 快 / 一般 / 慢 / 很慢），带区间周数时用周数。
2. **录用比例的措辞**：`较难` / `容易` / `约 X%` / `以约稿为主`。
   最后一种最重要——`invited-only` 意味着自由投稿通道基本关着，别浪费三个月。

LetPub 是自由文本，噪声大（广告行、`/`、`IF 0` 都出现过）。
工具已经过滤，但**它永远不参与排序打分**，只作弱信号呈现。

## 四、和 science_journal_fit 配合

```
science_journal_fit({ title, keywords, band, design, minTopicShare: 0.01 })
```

- 当 ≥80% 的候选刊都有 OpenAlex 画像时，fit 自动切到**实证层**
  （权重：声明 scope 0.28 / 实证 footprint 0.32 / 设计 0.18 / 档位 0.12 / 格式 0.06 / 加速 0.04）。
  输出里 `intel: "empirical"`，每本候选带 `footprint` 百分比。
- 覆盖率不足 80% 时**整批退回声明层**（`intel: "declared"`），并在 `intelNote` 里说明原因。
  这是刻意的：同一次排序里混用两套权重，分数就不可比了。
- `minTopicShare` 直接剔除「几乎不发你这类」的刊。0.01 = 1% 是保守起点。

## 五、全量补数据

```
science_journal_refresh({ dryRun: true })                    # 先看预算
science_journal_refresh({ journalIds: ["nature"], dryRun: false })
```

53 刊 × 3 源 ≈ 200 个请求，约 10 分钟（受 OpenAlex 每 IP 每日额度与 LetPub 0.3 rps 限速约束）。
单刊急着看就用 `science_journal_intel({ journalId, refresh: true })`，只花 4–5 个请求。

数据超过 90 天会自动降级 confidence 并标 `stale`，届时重跑 refresh 即可。

## 六、常见误读

- **「综合刊 hitShare 也有 9%，那综合刊最好投」**——错。综合刊的 9% 是它最大子领域的天花板，
  意味着任何一个具体子领域的稿子都不占多数；专刊的 30% 才是真的「来者不拒那一类」。
  两者不可直接比大小，要结合 `maxSubfieldShare` 一起读。
- **「SciRev 说首轮 2 个月，所以 2 个月就有结果」**——那是中位数，尾部可以到 6 个月。
- **「LetPub 分割区高 = 好投」**——分区是评价，不是门槛。分区高的刊往往 desk reject 更快。
- **「footprint 高就能中」**——footprint 只说明这类工作在它那里出现过。质量、新颖性、写作都不在它的测量范围内。
