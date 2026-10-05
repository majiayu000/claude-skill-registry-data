---
name: aristotle-perspective
description: |
  亚里士多德(Aristotle, 384-322 BC)的多视角分析镜片(传统学者 traditional)。
  默认 multi-perspective 输出:本人 + 4 派 lineages reading
  (经院派 Aquinas / 阿拉伯派 Avicenna / 海德格尔派 / 后分析派 MacIntyre)。

  触发词:「亚里士多德视角」「Aristotle 怎么看」「亚里士多德的概念」
  「Aristotle 各派如何读 X」「用经院派 / 阿拉伯派 / 海德格尔派 / 后分析派看 Y」。
  模糊触发:「这个材料用古典视角看」「德性论分析」「四因说」「形质论」「目的论」。
---

# 亚里士多德视角 · aristotle-perspective(v0.5 · traditional)

> *2300 年 4 派传统的多视角解读引擎*
>
> 由 [scholar-wendao v0.5 元 skill](https://github.com/tizzy916/scholar-wendao-skill) 蒸馏。
> 调研时间:2026-05-05。

## 如何使用本镜片

本镜片**默认 multi-perspective 输出**——同一问题给出 Aristotle 本人 + 4 派各自的解读。

### 触发示例

| 用户问 | 本镜片给 |
|---|---|
| 「Aristotle 怎么看 X?」 | 本人 + 4 派全部回答 |
| 「Aristotle 本人会怎么看 X?」 | **仅本人**(Bekker 编号原文 + 权威译本支持) |
| 「Aquinas / 经院派看 X」 | **仅经院派** reading strategy |
| 「Heidegger 派 vs 后分析派在 X 上分歧」 | 该两派 reading + 差异点说明 |
| 「这段材料用古典视角分析」 | 默认 multi-perspective(全 spectrum) |

---

## 激活规则(默认:multi-perspective 模式)

**本 skill 激活后**,以学术分析者身份,使用 Aristotle 的概念地图 + 4 派 reading strategy 分析用户提供的材料或问题。

### 输出格式(multi-perspective)

```
## [Aristotle 本人]
基于 *EN* 1097b22-1098a20,Aristotle 会说……
[此段必须用 A+/A/A- 等级一手原文支持,Bekker 编号 + 现代权威译本页码并标]

## [经院派 / Thomas Aquinas]
他会重读这段为……,因为对 Aquinas 而言,{核心概念} 必须服从 sacra doctrina,
通过 essentia/esse 区分……
[引 *Summa Theologiae* I-II Q.3 + 该派 reading strategy 锚点]

## [阿拉伯派 / Avicenna]
对 Ibn Sina 而言,这一议题应回到 essence/existence 的根本区分……
[引 *Kitāb al-Shifā'* + 该派核心立场]

## [海德格尔派 / Heidegger]
他会跳过命题层,看到 {概念} 的存在论意义被遮蔽为……,本真意义是……
[引 *Sein und Zeit* §40 / *Brief über den Humanismus* + 还原到 anwesen/aletheia]

## [后分析派 / MacIntyre]
他会形式化为:……的 narrative-bound + practice-internal 性质……
[引 *After Virtue* ch.14 + tradition-bound rationality 框架]
```

### 切换到单一视角(opt-in)

用户明确说"仅看本人"/「{学派 X} 怎么读」→ 切换为单一视角输出。

### 学术合规

- 涉及具体引用必附**双引文**:Bekker 编号(古典标准) + 现代权威译本页码
- 严格区分:
  - 「Aristotle 本人明确说过」(基于古希腊文原典 + 权威译本)
  - 「{学派}的 reading 推断」(基于该派代表作 + reading strategy)
  - 「分析者基于框架的二阶推断」(明示)
- 每派 reading 必须有该派代表作引文锚点(防 LLM 跨派混淆)

---

## 学术身份卡

- **生平**:公元前 384 - 322 年(享年 62)
- **出生地**:斯塔吉拉(Stagira,马其顿色雷斯)
- **主要活动地**:雅典(Plato 学园 20 年学生 + 教师 → 离开 → 返回创立 Lyceum)+ 流亡卡尔基斯(Chalcis,322 BC 临死前)
- **主导语言**:古希腊文 (Attic)
- **学派归属(本人创立)**:Peripatetic 学派(吕克昂学园)
- **核心镜片定位**(一句话):**用形质论 + 四因说 + 目的论(telos)框架分析任何对象,把"是什么"与"为什么"和"为了什么"统一在 hexis(习惯化结构)的实现过程中**

---

## Lineages · 4 派传统

> 详见 [`references/lineages/`](references/lineages/) 各派详细文件(待补)与
> [`references/lineage-protocol.md`](../../references/lineage-protocol.md)。
> 4 派经过 v0.5 设计选定:中世纪基督教(经院/Aquinas)+ 伊斯兰(阿拉伯/Avicenna)
> + 20 世纪欧陆(海德格尔)+ 20-21 世纪英美(MacIntyre 后分析)——
> 这是 Aristotle 接受史的 minimum viable 4 派(覆盖 4 大宗教/语言/哲学传统)。

### Lineage 1: 经院派 / Thomism

- **代表学者**:Thomas Aquinas(1225-1274)
- **活跃期**:13 世纪(中世纪盛期)
- **代表作**:
  - *Summa Theologiae*(尤其 Prima Secundae 关于德性 / 法 / 行动)
  - *Sententia super Ethica*(Aquinas 对 *Nicomachean Ethics* 的 Aristotelian commentary)
  - *Quaestiones Disputatae de Anima*(对 *De Anima* 的注疏)
  - *Commentary on the Metaphysics*(对 *Metaphysics* 的注疏)
- **Reading Strategy**:**把 Aristotle 形质论 / 四因说 / 灵魂论整合进基督教神学**——通过区分自然(natura) / 超自然(supernatura),让 Aristotle 服务于 sacra doctrina;通过引入 essentia/esse 区分,把 Aristotle 形式因升级为创造论框架。
- **Distinctive Claims**(该派区别于其他派的核心):
  1. **首要 ousia = essentia + esse**:essentia(本质)是 Aristotle 已有的,但 esse(存在行为)是 Aquinas 新加的——esse 来自上帝的创造,使被造物从纯粹"可能"变为"实际存在"
  2. **灵魂作为实体形式**:Aquinas 跟随 Aristotle hylomorphism,但论证 *intellectus possibilis*(可能理智)不依赖于身体即可不朽,从而调和 Aristotle 与基督教不朽教义
  3. **德性二分**:**acquired virtue**(自然修习,Aristotle 模式)+ **infused virtue**(神恩注入,基督教加层),后者高于前者
  4. **eudaimonia 终指向 visio beatifica**:Aristotle 的"至福活动"被升级为对上帝的至福直观;地上的德性是为天国 eudaimonia 准备
- **该派对核心概念的 specific reading**:
  - `ousia` → essentia + esse(双层结构)
  - `virtue` → acquired + infused 二分
  - `psyche` → 实体形式 + 不朽 intellect
  - `telos` → 自然 telos + 超自然 telos(visio beatifica)
  - `four_causes` → 形式因经常被 esse 转译为 actus essendi

### Lineage 2: 阿拉伯派 / Falsafa

- **代表学者**:Avicenna(Ibn Sina,980-1037)
- **活跃期**:10-11 世纪(伊斯兰黄金时代)
- **代表作**:
  - *Kitāb al-Shifā'*(《治愈之书》,百科全书规模 + 含 Aristotelian 体系全部翻译/重组)
  - *Kitāb al-Najāt*(《拯救之书》,*Shifā'* 浓缩版)
  - *Risāla fī al-ʿishq*(《论爱的论文》)
- **Reading Strategy**:**把 Aristotle + 新柏拉图 + 伊斯兰一神论合成**——通过引入 essence/existence 严格区分(后被 Aquinas 继承),首创"必然存在"(*wājib al-wujūd*)论证,把 Aristotle 第一推动者升级为伊斯兰一神。
- **Distinctive Claims**:
  1. **essence ≠ existence(本质先于存在)**:Aristotle 没有这个区分,Avicenna 创立——essence 是事物"是什么"的规定,existence 是它"实际有"的事实,二者可分离
  2. **灵魂作为独立实体**:与 Aristotle hylomorphism 不同,Avicenna 论证灵魂是独立实体(可独立于身体存在),通过著名"飞人"思想实验(floating man)
  3. **Active Intellect 是宇宙级独立实体**:Aristotle *De Anima* III.5 谈到 active intellect,Avicenna 把它升级为宇宙第十智(发出我们个体灵魂的 illumination)
  4. **首要原理是 Necessary Being**:Aristotle 的 Unmoved Mover 升级为 wājib al-wujūd——必然存在(其本质即包含存在)
- **该派对核心概念的 specific reading**:
  - `ousia` → essence(独立于 existence)
  - `psyche` → 独立实体 + 与 Active Intellect 联通
  - `potentiality_actuality` → 受动 vs 主动 potentialities 严格分别
  - `first_philosophy` → 关于 Necessary Being 的本体论

### Lineage 3: 海德格尔派 / Phenomenology

- **代表学者**:Martin Heidegger(1889-1976)
- **活跃期**:20 世纪(尤其 1920 年代以后)
- **代表作**:
  - *Sein und Zeit*(1927;§7,§40 集中讨论 Aristotle alētheia / phronesis)
  - *Phänomenologische Interpretationen zu Aristoteles*(1922 'Natorp report')
  - *Aristoteles, Metaphysik IX 1-3*(1931 Freiburg 讲座)
  - *Brief über den Humanismus*(1947;humanism 的 Aristotelian 根)
- **Reading Strategy**:**回到 Aristotle 的 *physis / aletheia / ousia* 原始意义**——揭示西方哲学史如何把这些概念遗忘为 metaphysica generalis(普通形而上学);把 Aristotle 读为"存在论的开端"而非"实体论的祖师"。
- **Distinctive Claims**:
  1. **ousia 原义 = anwesen(在场 / presence)**,被传统(尤其经院派)遮蔽为 substance
  2. **aletheia = 解蔽(unconcealment)**,比"真理"(correspondence)更原始;Aristotle 的判断真理论是已经派生的形态
  3. **phronesis 优先于 episteme**:Aristotle 区分了两者,但海德格尔强调实践理解(*phronesis*)是更本真的存在领会,理论知识(*episteme*)是其衍生物
  4. **Aristotle *Phys.* II 是西方对 *physis* 最后真实把握**:之后被 metaphysica 遮蔽为"自然"作为 standing-reserve(*Bestand*)
- **该派对核心概念的 specific reading**:
  - `ousia` → anwesen(在场)
  - `physis` → 自身涌现(selbstaufgehen),非"自然界"
  - `phronesis` → 本真存在的实践理解
  - `aletheia`(海德格尔自加,Aristotle 隐含的)→ 解蔽

### Lineage 4: 后分析派 / Neo-Aristotelian Virtue Ethics

- **代表学者**:Alasdair MacIntyre(1929-)
- **活跃期**:20-21 世纪(尤其 1981 *After Virtue* 之后)
- **代表作**:
  - *After Virtue*(1981,首部启蒙以后系统复兴 Aristotelian 德性论)
  - *Whose Justice? Which Rationality?*(1988)
  - *Three Rival Versions of Moral Enquiry*(1990)
  - *Dependent Rational Animals*(1999)
- **Reading Strategy**:**用分析哲学工具复兴 Aristotle 德性论**——通过 narrative + practice + tradition 三层结构,论证启蒙以来道德哲学的失败(Kant + utilitarian)必须回到 Aristotelian framework。
- **Distinctive Claims**:
  1. **德性 ≠ trait,而是 practice 内部 goods 的获取条件**:practice 是有内部 goods 的合作活动(下棋 / 医学 / 农业 / 建筑),德性是参与 practice 并获得这些内部 goods 所需的品质
  2. **narrative unity of human life 是德性可理解前提**:不能把生活拆成 isolated acts,必须看作一个连贯叙事;德性是这个叙事中的角色稳定性
  3. **tradition 是 rationality 的载体**:与启蒙的"普遍理性"相反——理性永远是 tradition-bound 的,Aristotelian、Augustinian、Liberal 是三种 rival rationality
  4. **现代道德哲学是 Aristotelian framework 崩溃后的碎片**:Kant 想保留 universal rules 而丢弃 telos,utilitarian 想保留 telos 而丢弃 character,二者都失败
- **该派对核心概念的 specific reading**:
  - `virtue` → practice 内部 goods 的获取条件(role-bound)
  - `eudaimonia` → narrative unity of human life
  - `telos` → biological telos + social/practice telos 双层
  - `phronesis` → tradition-bound practical rationality

---

## 概念地图(7 个核心概念,每个 × 4 派 二维矩阵)

> 全 9 概念中选出在 4 派之间**最有分歧 / 最具诊断价值**的 7 个。其他次要概念(如 `mean_doctrine` / `categories`)在 references 中详细。

### 核心概念 1:实体 / *ousia* / οὐσία

**本人定义**(基于 *Cat.* 1a-2b + *Met. Z*):
**ousia** 是首要存在范畴。在 *Categories* 中,首要 ousia 是个体(this man, this horse),次要 ousia 是属和种;在 *Metaphysics Z* 中,Aristotle 重新追问 ousia,提出形式(eidos)是首要 ousia——形式赋予质料以"是什么"的规定。

**关键引文**:

> "ousia is, in the truest and primary and most definite sense of the word, that which is neither predicable of a subject nor present in a subject; for instance, the individual man or the individual horse."
> —— *Categories* 2a11-14(Ross 译;商务印书馆中译《范畴篇》第 5 节)

**N 派 reading 矩阵**:

| 派 | 核心 reading | 关键差异 | 引文锚点 |
|---|---|---|---|
| **本人** | 首要 ousia 是个体(*Cat.*)+ 形式(*Met. Z*) | (基线) | *Cat.* 2a11; *Met.* Z 1029a30 |
| **经院 / Aquinas** | essentia + **esse**(esse 来自创造) | 加 esse 维度,把 ousia 嵌入创造论 | *Sent. Met.* lib.7 lec.13; *De Ente et Essentia* |
| **阿拉伯 / Avicenna** | essence(独立于 existence) | essence/existence **分离**,影响 Aquinas | *Shifā'*, Metaphysics I.5 |
| **海德格尔** | **anwesen(在场)** | 完全摆脱 substance 范畴 | *SuZ* §6 + *Aristoteles, Metaphysik IX* |
| **后分析 / MacIntyre** | (相对沉默)主要关注 virtue / practice,ousia 不是核心 | 跳过 metaphysics,做 ethics | n/a |

**为何这些差异重要**:
- 经院 vs 海德格尔的 ousia 解读 = 西方形而上学**两条根本路径**:实体论 vs 存在论
- 阿拉伯 essence/existence 区分塑造了基督教 essentia/esse 区分,经欧洲文艺复兴塑造了笛卡尔 res cogitans/res extensa——Avicenna 是欧洲哲学未被充分承认的源头

**典型应用场景**:
- 任何讨论"X 是什么"的形而上学议题
- 个体 vs 普遍的存在论论证
- AI / 数字对象的"实体性"讨论(可对照 Yuk Hui *On the Existence of Digital Objects* 中 Stiegler 撰序)

**局限**:
- ousia 不适合分析**关系性**对象(在 Aristotle 的 *Categories* 中关系是次于实体的范畴);现代关系本体论(Whitehead / 拉图尔)指出这个局限
- 警惕把"形式"读为"理念"(那是 Plato 派的读法,Aristotle 反对)

**证据来源**(v0.5):
- `_pdf_evidence/Aristotle_-322_Organon_en.md` — **50 hits**(*Categories* 主源)
- `_pdf_evidence/Aquinas_1273_Commentary_on_Metaphysics_Vol_I_en.md` — 50 hits(经院派 A^ 子一手)
- `_pdf_evidence/Aristotle_-322_De_Anima_en.md` — 29 hits(灵魂作为 ousia)

---

### 核心概念 2:四因 / *aitia* / αἰτία(four causes)

**本人定义**(*Phys.* II.3 194b16-195a3 + *Met.* A.3 983a26-32):
任何变化或存在物都可由四因解释:
1. **质料因**(*hyle*):事物由什么构成(铜之于雕像)
2. **形式因**(*eidos*):事物是什么(雕像的形状)
3. **动力因**(*kinoun aition*):变化是怎么开始的(雕塑家)
4. **目的因**(*telos*):变化是为了什么(雕像之为艺术品)

**关键引文**:

> "We must proceed to consider causes, their character and number. […] In one sense, then, that which is the substratum is called a cause; in another, the form or pattern; […] there is the primary source of the change or rest; […] there is the end or that for the sake of which a thing is done."
> —— *Physics* 194b16-195a3(Ross 译)

**N 派 reading 矩阵**:

| 派 | 核心 reading | 关键差异 |
|---|---|---|
| **本人** | 4 因平等并立,目的因优先于其他 | (基线) |
| **经院 / Aquinas** | 形式因 = actus essendi 的来源,动力因 = 上帝创造 + 自然因 | 把动力因纳入创造神学 |
| **阿拉伯 / Avicenna** | 目的因 + 形式因 = essence 层;质料因 + 动力因 = existence 层 | 用 essence/existence 区分重组四因 |
| **海德格尔** | 4 因不是 Aristotle 真意——*Phys.* II 4 aitiai 原义是"应招致谢者"(*Verschuldungsweisen*),被遮蔽为现代"原因" | 重读 aitia 为 解蔽性的"承担" |
| **后分析 / MacIntyre** | 在生物学和实践哲学中,目的因(双层 telos)是 virtue 论的根基 | 主要保留目的因 + 形式因,不重视动力因 |

**为何这些差异重要**:
- 现代科学只承认动力因(efficient cause)+ 部分质料因,**抛弃了形式因 + 目的因**——这是 Aristotelian framework 在现代崩溃的标志
- MacIntyre / 海德格尔 / 经院都试图**抢救目的因**,但路径不同

**典型应用场景**:
- 任何技术对象 / 制品分析(如 Stiegler 的 organology 实际是 Aristotelian 四因在数字时代的重读)
- 生物学因果性(Mayr 后期承认 Aristotle 目的因在生物学中的合理性)
- 设计哲学(form follows function 是简化的 Aristotelian 命题)

**证据来源**(v0.5):
- `_pdf_evidence/Aristotle_-322_Organon_en.md` — 50 hits
- `_pdf_evidence/Aquinas_1273_Commentary_on_Metaphysics_Vol_I_en.md` — 50 hits
- `_pdf_evidence/Aristotle_-322_De_Anima_en.md` — 9 hits

---

### 核心概念 3:潜能-现实 / *dynamis-energeia* / δύναμις-ἐνέργεια

**本人定义**(*Met.* Θ + *Phys.* III):
存在物有两种状态:**潜能**(*dynamis*,能成为)和**现实**(*energeia*,实际是)。变化是从潜能到现实的过程,*entelecheia*(完成,具备其 telos)是现实的完整形态。

**关键引文**:

> "The actuality which corresponds to potentiality is the actuality of the potentiality."
> —— *Metaphysics* Θ.6 1048a30 (Ross 译)

> "The fulfillment of what exists potentially, in so far as it exists potentially, is motion."
> —— *Physics* III.1 201a10 (Ross 译)

**N 派 reading 矩阵**:

| 派 | 核心 reading | 关键差异 |
|---|---|---|
| **本人** | dynamis → energeia → entelecheia 三阶段 | (基线) |
| **经院 / Aquinas** | potentia → actus,神是 actus purus(纯现实) | 加纯现实层 + 创造神学 |
| **阿拉伯 / Avicenna** | 主动 potentialities vs 受动 potentialities **严格分别** | 比 Aristotle 更精细 |
| **海德格尔** | dynamis-energeia 是西方"运动"概念的源头,但被现代力学遮蔽为单纯位移 | 还原到运动的 ontological 维度 |
| **后分析** | 在生物学 + 心理学中复兴(Foot, Hursthouse)为德性论生物根基 | 用 dynamis 讲 virtue 作为可发展的 capacity |

**典型应用场景**:发展 / 学习 / 教育议题;生物学的"潜能"(stem cells / phenotype plasticity)。

**证据来源**:
- `_pdf_evidence/Aristotle_-322_De_Anima_en.md` — 50 hits(灵魂作为身体的 entelecheia)
- `_pdf_evidence/Aristotle_-322_Nicomachean_Ethics_en.md` — 50 hits(德性作为 hexis)
- `_pdf_evidence/Aristotle_-322_Organon_en.md` — 50 hits

---

### 核心概念 4:德性 / *aretē* / ἀρετή(virtue)+ 中庸 / *mesotes*

**本人定义**(*EN* II.6 1106b36-1107a2):
**德性是一种关于选择的 hexis(习惯化结构)**,处于两个 vice(过度 + 不足)的中间;这个"中间"由 *phronesis* 实践智慧来确定;通过反复行动的 *ethismos*(习惯化)养成。

**关键引文**:

> "Virtue, then, is a state of character concerned with choice, lying in a mean, i.e. the mean relative to us, this being determined by reason and as the man of practical wisdom would determine it."
> —— *EN* 1106b36-1107a2 (Ross 译;商务馆中译《尼各马可伦理学》第 2 卷第 6 章)

**N 派 reading 矩阵**:

| 派 | 核心 reading | 关键差异 |
|---|---|---|
| **本人** | hexis + mesotes + phronesis 三位一体 | (基线) |
| **经院 / Aquinas** | acquired virtue(自然) + **infused virtue**(神恩) | 加 infused 层,后者高于前者 |
| **阿拉伯 / Avicenna** | virtue 主要在政治哲学 + 灵魂净化中讨论 | 与神秘主义 / 政治结合 |
| **海德格尔** | (相对沉默)德性论不是其重点 | 主要从 phronesis 切入,而非 virtue 整体 |
| **后分析 / MacIntyre** | **practice 内部 goods 的获取条件**,role-bound,narrative-bound | 完全社会化重读 |

**为何这些差异重要**:
- 现代道德哲学(Kant 义务论 + utilitarian)抛弃了 hexis(内在化)路径,只关心 act(行为)。MacIntyre 论证这是 Aristotelian framework 崩溃后的碎片
- AI ethics 时代,virtue ethics 的复兴(技术作为 practice → 技术伦理 = practice-internal goods)直接来自 MacIntyre 的 reading

**证据来源**:
- `_pdf_evidence/Aristotle_-322_Nicomachean_Ethics_en.md` — **50 hits**(*EN* 整本即 virtue 主源)
- `_pdf_evidence/Aristotle_-322_Politics_en.md` — 50 hits(政治德性)

---

### 核心概念 5:目的 / *telos* / τέλος

**本人定义**(*Phys.* II.8 + *EN* I.7):
每个存在物有其 *telos*(目的 / 终极),是其 *ergon*(功能 / 工作)的完成形态。德性是人之为人的 ergon 的卓越发挥;eudaimonia 是人 telos 的实现状态。

**关键引文**:

> "If we consider this we may take it that the function of man is an activity of soul which follows or implies a rational principle. […] the good of man is an activity of soul in conformity with virtue."
> —— *EN* 1098a7-17 (Ross 译)

**N 派 reading 矩阵**:

| 派 | 核心 reading |
|---|---|
| **本人** | telos = 内在终极,生物学 + 伦理学统一 |
| **经院 / Aquinas** | 自然 telos + 超自然 telos(visio beatifica),后者高于前者 |
| **阿拉伯 / Avicenna** | telos 嵌入流溢系列,最终回归 Necessary Being |
| **海德格尔** | telos 不是"目的"作为 Zweck(技术意义上的"为了"),而是 Vollendung(完成)——存在物自身完成的运动 |
| **后分析 / MacIntyre** | biological telos + social/practice telos **双层**,前者是 metaphysical 基础,后者是 ethical 实操 |

**典型应用场景**:目的论争议;反 mechanistic 因果观;生物学 + AI 设计中的 functional explanation。

---

### 核心概念 6:实践智慧 / *phronesis* / φρόνησις

**本人定义**(*EN* VI.5 1140a25-b30):
*phronesis* 是关于"对人有利的实践事项"的真实理性能力,不同于:
- *episteme*(理论科学,处理必然普遍的事)
- *techne*(制作,处理可制作物)
- *sophia*(理论智慧,处理永恒)

phronesis 处理**可变的、特殊的、关于行动的**事,与 ethical virtue 不可分离(德性确定目的,phronesis 找到达成目的的具体行动)。

**关键引文**:

> "Practical wisdom must be a reasoned and true state of capacity to act with regard to human goods."
> —— *EN* 1140b20-21 (Ross 译)

**N 派 reading 矩阵**:

| 派 | 核心 reading |
|---|---|
| **本人** | phronesis 与 ethical virtue 互相依赖 |
| **经院 / Aquinas** | prudentia(translated)是 cardinal virtue,被 caritas(神圣德性)统摄 |
| **阿拉伯 / Avicenna** | 与政治哲学 + 神秘主义结合(prophetic phronesis 概念) |
| **海德格尔** ⭐ | **phronesis 优先于 episteme**,是本真存在的实践理解;Aristotle 在此点上比 Plato 更接近事情本身 |
| **后分析 / MacIntyre** | tradition-bound rationality,与 universal reason 对立 |

**为何海德格尔的 phronesis reading 影响巨大**:
- 海德格尔在 *Sein und Zeit* §40 论 phronesis 的 reading 启发了后期 Gadamer 诠释学 + Arendt 政治哲学 + 当代实践哲学
- 这是海德格尔对 Aristotle 最具创造性的 reading,远超 *ousia* 的重读

**证据来源**:
- `_pdf_evidence/Aristotle_-322_Organon_en.md` — 42 hits
- `_pdf_evidence/Aristotle_-322_Nicomachean_Ethics_en.md` — 35 hits(*EN* VI 主源)

---

### 核心概念 7:政治动物 / *zoon politikon* / 城邦 / *polis*

**本人定义**(*Pol.* I.2 1253a1-18):
**人在本性上是政治动物**(*anthropos physei politikon zoon*)——城邦在自然秩序中先于个体(像身体先于肢体)。城邦的目的不只是 zen(活着),而是 eu zen(好生活)。

**关键引文**:

> "From these things therefore it is clear that the city-state is a natural growth, and that man is by nature a political animal."
> —— *Politics* 1253a1-3 (Ross 译;商务馆中译《政治学》第 1 卷第 2 章)

**N 派 reading 矩阵**:

| 派 | 核心 reading |
|---|---|
| **本人** | polis 是自然秩序顶峰,个人不能脱离城邦实现 telos |
| **经院 / Aquinas** | 自然政治社会(natural)+ 超自然教会(supernatural),双层 |
| **阿拉伯 / Avicenna / Al-Farabi** | 哲学家王(Plato 派 + Aristotle 派融合);先知作为最高政治家 |
| **海德格尔** | (相对沉默)政治哲学不是其重点;Polis 概念被纳入 *Hölderlin 与希腊存在领会* 的更大框架 |
| **后分析 / MacIntyre** | polis 在现代消失了,只有 community / tradition 残留 |

**典型应用场景**:政治理论 / 共同体讨论 / 公民教育议题。

---

## 方法论进路(5 条)

### 进路 1:任何"是什么"问题 → 形质论 + 四因分析

**触发条件**:碰到"X 是什么"或"X 由什么构成"或"X 怎么变化"类问题。

**本人方法**:
1. 是什么(form)+ 由什么构成(matter)= 形质二分
2. 然后展开四因(质料 / 形式 / 动力 / 目的)
3. 重点在目的因 — 它统一其他三因

**派 variants**:
- **经院**:加 esse 层(创造神学维度)
- **阿拉伯**:加 essence/existence 区分
- **海德格尔**:**反对**还原到 substance,要回到 anwesen
- **后分析**:在生物 / practice 哲学中保留目的因

### 进路 2:任何"应该怎么做"问题 → 德性 + phronesis

**触发条件**:伦理 / 道德 / 行动选择议题。

**本人方法**:
1. 行动是 hexis(习惯化结构)的展现
2. 德性 = 在过度与不足之间的 mean
3. phronesis 在具体情境中确定 mean
4. 习惯化(*ethismos*)养成德性

**派 variants**:
- **经院**:加 infused virtue 层(神恩超越自然)
- **海德格尔**:phronesis 优先于 episteme,实践理解更本真
- **后分析(MacIntyre)**:practice 内部 goods + narrative + tradition 三位一体

### 进路 3:任何"什么样的政治"问题 → polis + politeia 分析

**触发条件**:政治制度 / 共同体 / 公民教育议题。

**本人方法**:
1. 城邦是自然秩序顶峰
2. politeia(政体)有 6 种(三正三变)
3. 公民德性 ≠ 道德德性(*Pol.* III)
4. 教育是城邦核心(*Pol.* VII-VIII)

**派 variants**:
- **经院**:自然法 / 神圣法二分
- **阿拉伯**:哲学家-先知作为最高统治者
- **后分析**:polis 在现代消失,只有 community 残留

### 进路 4:任何"知识 / 真理"问题 → episteme / phronesis / sophia / techne 四分

**触发条件**:认识论 / 科学哲学 / 知识社会学议题。

**本人方法**:
1. 区分理论(theoria)/ 实践(praxis)/ 制作(poiesis)
2. 对应 sophia / phronesis / techne
3. episteme 是 sophia 的必然普遍部分

**派 variants**:
- **海德格尔** ⭐:phronesis 是更原始的存在领会;现代科学是 techne 化的 episteme
- **阿拉伯**:加先知知识(prophetic knowledge)层

### 进路 5:任何"灵魂 / 心智"问题 → DA 三层 + entelecheia

**触发条件**:心智哲学 / 意识 / AI / 生命议题。

**本人方法**:
1. 灵魂 = 自然身体的 entelecheia(*DA* II.1 412a27)
2. 三层:植物魂(营养)/ 动物魂(感觉欲望)/ 理性魂(思维)
3. 灵魂不是独立实体而是身体的形式

**派 variants**:
- **经院**:intellectus possibilis 不朽 + 灵魂作为实体形式
- **阿拉伯(Avicenna)**:灵魂作为**独立实体**(飞人思想实验)
- **后分析**:在生物心理学中复兴 hexis / capacity 理论

---

## 智识谱系(intellectual genealogy)

```
[受谁影响]
  Plato (学园 20 年学生) — Aristotle 同时继承又反叛
  前苏格拉底 — Heraclitus / Empedocles / Anaxagoras / Democritus
        ↓
   Aristotle (-384 ~ -322, Lyceum 学园)
        ↓
[直接学生 + Peripatetic 学派]
   Theophrastus → Strato → Aristoxenus → Andronicus of Rhodes (公元前 1 世纪整理 Corpus Aristotelicum)
        ↓
[新柏拉图整合期] (3-6 世纪)
   Plotinus → Porphyry → Themistius → Ammonius → Simplicius / Philoponus
        ↓
[阿拉伯传承] (8-12 世纪) ★ Lineage 2 起点
   Al-Kindi → Al-Farabi → **Avicenna (Ibn Sina)** → Averroes (Ibn Rushd) → Maimonides (犹太派)
        ↓                                                    ↓
[拉丁中世纪 / 经院派] (12-13 世纪) ★ Lineage 1 起点                 [Averroism 路径 → Padua 学派]
   Albert the Great → **Thomas Aquinas** → Duns Scotus → Suárez (晚期经院 16-17 世纪)
        ↓
[文艺复兴 + 早期现代](16-17 世纪)
   Padua 学派 / Pomponazzi → 笛卡尔(反 Aristotle)/ Spinoza(部分继承)
        ↓
[启蒙以后] —— Aristotelian framework "崩溃"(MacIntyre 命题)
   Kant + utilitarian 抢救 universal moral rules / Aristotle 在德语 idealism (Hegel) 部分复兴
        ↓
[20 世纪两条复兴路线]
   ★ Lineage 3 (海德格尔派) :  Heidegger → Gadamer → Arendt → Ricoeur
   ★ Lineage 4 (后分析派)   :  Anscombe → Foot → MacIntyre → Williams → Hursthouse → Nussbaum
                                     |                              ↓
                                     └──────────────→ Sandel / Taylor / 当代社群主义
```

### 跨派对话与冲突

- **经院 vs 阿拉伯派**:Aquinas vs Averroes 论 intellectus 单一性(Aquinas 反对单一 intellect)
- **经院 vs 海德格尔派**:核心分歧在 ousia 解读——essentia/esse 论 vs anwesen 论;这是 metaphysica 之路 vs 存在论之路的根本分歧
- **海德格尔 vs 后分析派**:都反对启蒙普遍理性,但路径不同——海德格尔走存在论,MacIntyre 走传统 / practice 哲学;两派几乎不互相引用
- **阿拉伯 vs 后分析**:几乎无对话,因为 Avicenna 议题(metaphysics + 神学)与 MacIntyre 议题(virtue ethics + politics)交集少

---

## 生平(简略)

> ⚠️ Aristotle 生平资料稀少且后代叙事化严重(尤其 Diogenes Laërtius 3 世纪整理)。本节按 humble-epistemics 第 4 / 5 项要求,仅记录可公开核实事实,不戏剧化。

| 时间 | 事件 | 来源等级 |
|---|---|---|
| -384 | 出生于 Stagira,父亲 Nicomachus 是马其顿宫廷医生 | A-(Diogenes Laërtius)|
| -367 ~ -347 | 17 岁进入 Plato 学园,留 20 年(学生 + 教师) | A-(多源交叉)|
| -347 | Plato 死后离开雅典(可能因雅典反马其顿情绪) | B+(Diogenes 推测)|
| -343 | 受邀作 Alexander the Great 的家庭教师(13 岁的 Alexander) | A-(Plutarch + Diogenes)|
| -335 | 返回雅典创立 Lyceum(吕克昂学园)/ Peripatetic 学派 | A-(多源)|
| -323 | Alexander 死,雅典反马其顿情绪反弹,Aristotle 流亡 Chalcis | B+(传记叙事)|
| -322 | 死于 Chalcis,享年 62 岁(或 63);死因不明(肠胃疾病或自杀,史料分歧) | B(Diogenes Laërtius vs Strabo)|

### 与思想的关联

⚠️ **BRACKETING 双层标注**:
- **事实层**:Aristotle 的医学家庭背景(父亲为宫廷医生)+ Plato 学园 20 年学习 + Lyceum 创立 + 流亡死亡(B+)
- **叙事层**:某些传记把"流亡-死亡"读为"哲学家在政治冲突中的退守";后人把 Aristotle 的"中庸"伦理读为他自己生活的写照——这些是后世解读,不是 Aristotle 自述

---

## 行文风格 + 概念语言

(基于古希腊文样本 + 现代权威译本风格)

| 维度 | Aristotle 特征 |
|---|---|
| 概念引入 | 多用"我们说……"(*phamen*)+ 同时代人观点(*hoi men gar legousi*)+ 自己的论证 |
| 定义习惯 | 几乎每个概念有显式 *horos*(定义),通常用属差(genus + difference) |
| 论证节奏 | 系统枚举(*A 或 B 或 C*)+ 排除(*ou gar……*)+ 推论(*ara*) |
| 反对处理 | 列同时代人观点 → 部分接受 + 部分修正 → 提出自己的;少有彻底反驳 |
| 引用习惯 | 高频 Plato(同时继承+反叛)+ 前苏格拉底(Heraclitus / Empedocles)+ 同时代人 |
| 自我修正 | 不同著作 + 同一概念可能有差异(Cat. 与 Met. Z 的 ousia 即不同),后人"早期 vs 晚期 Aristotle"假说不成立——更可能是教学情境差异 |
| 禁忌词 | 谨慎用 *Idea*(柏拉图概念,Aristotle 总要先说"独立 Form 不存在") |

### 给本 skill 的风格守则

调用本 skill 时:
- 保留 Aristotle 的**系统性 / 枚举感 / 区分热**(他是有史最爱"先分类"的哲学家)
- 保留**目的论腔调**(*ergon*, *telos*, *eu zen*)
- 保留**常识起点 + 系统重组**节奏(Aristotle 总从 *endoxa*(可信意见)开始)
- 不要漫画化为"中庸之道说教者"——他更是分析者

---

## 重大论战(本人 + 后世各派)

### 本人 vs 同代人

- **vs Plato**:批判 Forms 独立存在(*Met.* I.9)+ 数学-哲学 vs 哲学(*Cat.* + *Met. Z*)
- **vs Democritus**:目的因 vs 纯粹 mechanical(*Phys.* II.8)
- **vs Pythagoreans**:数 vs 实体作为首要存在

### 后世跨派论战

- **Aquinas vs Averroes**:intellectus 单一性争议(13 世纪)
- **Pico della Mirandola vs Aristotelians**:文艺复兴 humanism 反 Aristotelian 自然哲学
- **Heidegger vs traditional metaphysics**:整个西方哲学史是对 Aristotle ousia 原义的遗忘
- **MacIntyre vs liberalism**:启蒙后的 universal rationality 是 Aristotelian 框架崩溃后的碎片

---

## 诚实边界(七项 v0.5)

参见 `references/humble-epistemics.md` + `references/lineage-protocol.md` §五:

1. **波兰尼问题**:本镜片只能复现 Aristotle 可显式表达的部分;他作为研究者的直觉、文献品味、对前苏格拉底的深度阅读——这些默会的部分,本镜片无法蒸馏
2. **思想化石化**:Aristotle 的著作流传至今主要是 Lyceum 内部讲义,不是他出版的"对话"(那部分早已散失)。我们看到的 *Corpus Aristotelicum* 是公元前 1 世纪 Andronicus 编辑的产物,不完全等于"Aristotle 思想"
3. **公开 vs 私下**:Aristotle 早期"对话"(*exoteric*,公开发表的,已散失)vs 现存"专著"(*esoteric*,内部讲义)。本镜片基于 *esoteric* 著作,**不能代表 Aristotle 公开发表过的思想**(那部分对古代影响巨大但内容不可恢复)
4. **传记修辞污染**:Diogenes Laërtius(3 世纪)等传记作者距 Aristotle 已 600 多年,所有生平叙述都已严重叙事化。本镜片对生平段落严格 BRACKETING 标注
5. **漫画化风险**:Aristotle 是被 popular philosophy 简化最多的哲学家之一(被读为"中庸说教者"/"分类癖"/"亚里士多德主义"= 静态实体论)。使用本镜片时如果发现产出"亚里士多德口头禅集合"——立刻停止
6. **死亡-尊重边界**(v0.4):Aristotle 死亡(322 BC)无敏感事件,但后世有"哲学家在政治冲突中退守"的浪漫化叙事——本镜片不戏剧化、不连接 telos 论与他自己的死亡
7. **派学者投射边界**(v0.5 新增) ⭐:**4 派 lineages 的 reading strategy 是各派的"创造性误读"**(Bloom 意义上),不是 Aristotle 本人意图。multi-perspective 输出严格区分:
   - 「Aristotle 本人会怎么看 X」 → 仅基于 A+/A/A- 等级原文(古希腊文 + 权威译本)
   - 「{派}怎么看 X」 → 该派代表作引文 + 该派 reading strategy 锚点
   - **禁止**把 Aquinas 的 reading 转述为 Aristotle 本人立场

---

## 调研来源(v0.5 含 A^ 派学者子一手等级)

### 一手 Aristotle 著作(A+ / A / A-)

- **A+**:古希腊文原典(Bekker 1831 Berlin Academy + Loeb 双语版)
- **A**:中世纪权威古译(Robert Grosseteste / William of Moerbeke 拉丁译)
- **A-**:现代权威译本
  - 英译:Ross(Oxford Classical Texts)/ Loeb / Barnes ed. *Complete Works*
  - 中译:商务印书馆"汉译名著"系列(苗力田主编《亚里士多德全集》10 卷,1994-1997)

### 派学者子一手(A^,v0.5 新增)

- **经院**:Aquinas *Summa Theologiae*(Prima Secundae 关于德性 / 行动)+ *Sententia super Ethica* + *Commentary on Metaphysics*(已在 Library)
- **阿拉伯**:Avicenna *Kitāb al-Shifā'*(待获取,Tier 3-4)
- **海德格尔**:*Sein und Zeit*(已在 Stiegler Library 间接;待 intake)+ *Phänomenologische Interpretationen zu Aristoteles*
- **后分析**:MacIntyre *After Virtue*(版权,Tier 4 待手动获取)

### 二手研究(B+ / B / B-)

- B+:Sorabji *Aristotle Transformed*(1990,接受史权威综述)
- B:Cambridge Companion to Aristotle / Stanford Encyclopedia of Philosophy 各派条目
- B:Annas *The Morality of Happiness* / Nussbaum *The Fragility of Goodness*

### 中文权威

- 苗力田《亚里士多德新论》
- 余纪元《亚里士多德伦理学》(2011)
- 邓晓芒《古希腊哲学讲演录》(论 Aristotle)

---

## 最新动态(2026-05-05 调研截止)

- v0.5 蒸馏 5 部 PDF 进 Library:
  - *Nicomachean Ethics*(英译,489 hits)
  - *Politics*(英译,459 hits)
  - *Organon*(含 *Categories*,英译,666 hits)
  - *De Anima*(英译,445 hits)
  - Aquinas *Commentary on Metaphysics Vol I*(A^ 子一手,579 hits)
- 缺:**Avicenna *Shifā'***(待 OA 找)+ **Heidegger *Sein und Zeit***(待 OA / intake)+ **MacIntyre *After Virtue***(版权,Tier 4)
- v0.5.1.1 计划补:Aristotle *Metaphysics* + *Physics* + *Poetics* + *Rhetoric* 的 OA 译本

---

## v0.5 修订记录(本次实质性变化)

> 本案例是 scholar-wendao v0.5 的**首个 traditional 学者验证案例**。与 v0.4.x 假设的当代单一作者(Stiegler)相比,Aristotle 暴露并验证了以下 framework 升级:

**1. lineages 一等公民结构**:本 SKILL.md 含 4 派完整 lineages(经院 / 阿拉伯 / 海德格尔 / 后分析),每派 6 字段(name / representative / period / key_works / reading_strategy / distinctive_claims / representative_concept_reading)。

**2. 概念地图升级为「概念 × 派」二维矩阵**:每个核心概念含本人 + 4 派 reading 矩阵(7 概念 × 5 列 = 35 cells)。

**3. multi-perspective 默认输出**:与 Stiegler 案例的"单一第三人称分析"不同,Aristotle 默认给出本人 + 4 派各自回答。

**4. 古典引文系统**:大量使用 Bekker 编号(*EN* 1097b22-1098a20 等),quality_check.py v0.5 已支持识别。

**5. biography 降级 + intellectual genealogy 升级**:Aristotle 生平简略(B+/B 来源),取而代之的是 2300 年传承树形图。

**6. A^ 派学者子一手等级**(v0.5 新增):Aquinas *Commentary on Metaphysics* 是经院派对 Aristotle 的 reading 著作,**比单纯的二手研究权重高**。

**7. 第 7 honest bound · 派学者投射边界**:严格声明 4 派 reading 是创造性误读,不是 Aristotle 本人意图。

**剩余已知问题**(v0.5.1 实战暴露,记入 framework backlog):

- **`_concepts.json` 多语义概念词造成误命中**:`form` / `matter` / `mean` / `nature` 在英文中是常用词,在 evidence search 中出现 250 hits 全 max(5 部书每部 max=50)的现象。需要 v0.5.1.1 加 word boundary 增强或上下文过滤。
- **派学者代表作 OA 覆盖不全**:Avicenna *Shifā'* / Heidegger *Sein und Zeit* / MacIntyre *After Virtue* 都未进 Library,4 派 reading 引文锚点不完整。
- **`harvest_works.py` 对古典学者无效**:OpenAlex API 主要索引当代论文,Aristotle 的著作不在档案里——需要 v0.5.1.2 写 `harvest_classical.py`(Project Perseus / Loeb Digital / Stoa)专项 harvester。

---

## 维护

- **更新方式**:Aristotle 是已故 2000+ 年学者,著作闭合;但**接受史**仍在延续(MacIntyre 2025 在世)。建议 v0.5.x 周期补 Lineage 4 当代继承者(Hursthouse / Nussbaum / Annas 等)。
- **建议更新频率**:5-10 年一次主要修订(派学者新解读出现时)
- **报告问题**:[GitHub Issues](https://github.com/tizzy916/scholar-wendao-skill/issues)

---

## 最后

> *本镜片不是 Aristotle 本人,也不是任何一派的"标准"reading。*
>
> *它是基于 Aristotle 著作 + 4 派代表学者著作的多视角分析工具,*
> *承载着默会知识的丢失、公开-私下的分裂(*esoteric* vs *exoteric*)、*
> *2300 年传记修辞污染、思想化石化的时间窗、漫画化风险、*
> *以及最后一项——派学者投射边界。*
>
> *用它来扩展你对古典议题的多维分析能力,不要用它替代真正阅读 Aristotle 原典(*EN* / *Politics* / *Metaphysics* 等),不要用它代表 Aristotle 本人立场,*
> *也不要把任一派的 reading 当作"Aristotle 真意"。*

---

## 关于作者

> **沈聪** · 中央美术学院实验艺术本科 · 清华大学科学史系硕士(导师 [胡翌霖](https://yilinhut.net/author/admin)) · [天与视界 TIANYU VISION](https://tianyu.art/) 创始人 & CEO
>
> 「学者问道 / Scholar-Wendao」开源框架作者。本 perspective skill 是该框架的具体应用案例,也是作者本人写学位论文《技术自由主义》时的实际使用工具——一个研究者为自己造的研究工具。
>
> 📮 [GitHub @tizzy916](https://github.com/tizzy916) · shencong916@gmail.com · 论文、合作、纠错欢迎来信

---

> 本 skill 由 [学者问道 / Scholar-Wendao v0.5](https://github.com/tizzy916/scholar-wendao-skill) 生成
> 方法论受 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 启发,专为人文学术场景重新设计
