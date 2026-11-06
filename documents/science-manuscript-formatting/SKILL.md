---
name: science-manuscript-formatting
description: Use when a manuscript draft needs to become a submittable file — you have the content (from science_paper_plan or your own draft) and now need it in the target journal's actual layout; also use when a submission was desk-rejected for formatting (word count over, too many figures, uncited references, wrong reference style), when the same paper must be retargeted from one journal to another without rewriting, or when a submission system demands DOCX or JATS rather than PDF.
---

# 排版与出件：一份源，四个产物，换刊只改一行

## 为什么这一层是机械的（也正因如此才能自动化）

写作里有一部分判断只有作者能做：这个 claim 成不成立、这个 gap 真的存在吗、这条审稿意见怎么回。
这些在 M2/M4 里，靠 `science_paper_audit` 和 `science_gap_matrix`。

剩下那一部分是**纯机械的**：字数有没有超、图有几张、引用的 key 在文献表里有没有、
参考文献该用 `[1]` 还是 `(Jordan et al., 2024)`、页边距多少毫米、要不要连续行号。
这些东西完全由**目标期刊**决定，跟内容无关——所以只要你把「刊」告诉机器，它就该自己算完。

这就是 `paper.md` 的设计前提：**正文里不写任何格式**。

```markdown
---
title: Orthogonalized Momentum Bounds the Effective Learning Rate
journal: nature          # ← 换刊只改这一行
keywords: [muon, optimizer, orthogonalization]
authors:
  - name: Zhang Wei
    affiliation: 1
    corresponding: true
    email: zhang@example.edu
affiliations:
  - id: 1
    name: "Institute of Computing, Beijing, China"
abstract: |
  一句话背景 → 一句话缺口 → 一句话做法 → 一句最硬的结果（带数字）→ 一句话意义。
references:
  - key: jordan2024muon
    type: article-journal
    title: "Muon: An optimizer for hidden layers in neural networks"
    authors:
      - {family: Jordan, given: Keller}
    year: 2024
    journal: arXiv preprint
    doi: 10.1234/example.001
---

# Introduction

Momentum methods dominate large-scale training [@jordan2024muon]. ...

![Effective learning rate versus step count.](figures/fig1.png){#fig:lre}

$$
\eta_{\mathrm{eff}} \le \frac{\|\mathbf{m}_t\|_2}{\sqrt{d}}
\label{eq:bound}
$$

| Optimizer | Steps |
| --- | --- |
| SGD | 12000 |
: Comparison of optimizers. {#tab:cmp}
```

`journal: nature` 改成 `journal: cell`，PDF 从 Nature 投稿版式变成 Elsevier 双栏，
参考文献从上标数字变成 `(Jordan et al., 2024)`，**正文一个字没动**。

## 一、先建稿，别从空文件开始

```
science_manuscript_new({
  id: "muon-bound",
  title: "<你的标题>",
  journal: "nature",
  design: "theory",
  keywords: ["muon", "optimizer"],
  authorName: "Zhang Wei"
})
```

落盘 `$DSH_HOME/science/manuscripts/muon-bound/`：

```
paper.md          ← 唯一真源，带 YAML 头和 Markdown 骨架
references.yml    ← 文献库（也可以直接写在 paper.md 的 references 里）
figures/          ← 图片
build/            ← 产物，可随时删
```

骨架里的 `<!-- TODO: ... -->` 是**给检查器看的**，不是给人看的。
填完跑 lint，剩下的 TODO 会变成具体条目报出来。

已经有稿子的不用建：只要目录里有 `paper.md`，后面三个工具都能直接用。

## 二、写完先查要件，别先出 PDF

```
science_manuscript_lint({ id: "muon-bound" })
```

输出分四级，`block` 是投稿系统会直接拒的，`warn` 是编辑会皱眉的：

| 代码 | 级别 | 意思 | 怎么改 |
|---|---|---|---|
| `words-over-hard` | block | 超上限 25% 以上 | 砍重复的结果描述，不要缩字号 |
| `abstract-long` | block | 摘要超字数 | 摘要按五句写，删背景铺垫 |
| `figures-over` | block | 图超张数 | 挪补充材料，正文只留被直接论证的 |
| `cite-undefined` | block | 引用了不存在的 key | 补 `references.yml` 或删引用 |
| `xref-dangling` | block | `\ref{}` 指向不存在的标签 | 检查 `{#fig:...}` 有没有拼错 |
| `no-corresponding` | block | 没标通讯作者 | `corresponding: true` + `email` |
| `section-intro-missing` | block | 缺引言 | 补 `# Introduction` |
| `cite-uncited` | warn | 文献表里有没被引的条目 | 正文引用它，或者删掉 |
| `words-thin` | info | 不到上限一半 | 顶刊常见退稿理由「内容量不足」 |
| `xref-unused` | info | 标签没被引用 | 图必须在正文里被提到 |

**`cite-uncited` 这一条最值钱**：挂在文献表里但正文没引的条目，Word 插件不会告诉你，
编辑一眼看到就会觉得你在凑引用数。这是 desk reject 的常见理由，而且改起来是纯机械的。

期刊没收录时（`journal` 写了个 `journals.json` 里没有的 id），工具不猜数字，
只报能算的量，限制项标 `words-unbounded`。要真检查就在 `data/journals.json` 里补这个刊。

## 三、出件

```
science_manuscript_build({ id: "muon-bound", targets: ["all"] })
```

| target | 产物 | 什么时候用 |
|---|---|---|
| `pdf` | `build/<刊>.pdf` | 自己看排版结果、投稿系统要 PDF |
| `docx` | `build/<刊>.docx` | 期刊要 Word（IEEE、Elsevier、多数中文刊） |
| `jats` | `build/<刊>.jats.xml` | PLOS、BMC、Frontiers、eLife、SciELO 这类吃 XML 的系统 |
| `html` | `build/<刊>.html` | 浏览器里看版式预览，不需要装任何东西 |
| `latex` | `build/<刊>.tex` | 要手工改细节、或交给合作者用 Overleaf 继续编 |

四个产物的**引文是同一份**——`cite.js` 解析一次，四处输出同样的字面量文本。
这是刻意的：不接 BibTeX、不发 `\cite{}`，就不会出现「PDF 里是 `[1]`、Word 里是 `(Jordan, 2024)`
而两者都对不上」这种投稿前才发现的问题。

### PDF 编译失败怎么办

`build` 的返回里，失败项带 `hint`：

- `File 'xxx.cls' not found` → 自动跑 `mpm --install`，装不上就降级到 `article`，
  并在 `warnings` 里记一条（版式细节会丢，投稿前建议补装）
- `Missing $ inserted` → 数学符号落在正文里了，`hint` 会给出**出错行号和那行内容**
- `Undefined control sequence` → 用了不存在的命令，通常是公式环境没闭合

工具会先 `kpsewhich` 查类、缺了就补装、再失败才降级，最多两轮。
所以「Springer 的 `sn-jnl` 没装」不会让整个构建挂掉，只会让版式退化成通用稿。

### DOCX 里的公式

Word 要 OMML 才是可编辑公式。目前用 Unicode 近似（`\frac{a}{b}` → `a/b`、`\alpha` → `α`、
`x_{ij}` → `xᵢⱼ`），转不了的命令**原样保留**并计入 `warnings`：

```
DOCX 里 2 个 TeX 命令没能转成 Unicode：\mathbb, \mathbb
```

看到这条就在 Word 里手工把那几个公式改成「插入 → 公式」。这是已知限制，不是 bug。

## 四、看环境

```
science_format_check({})
```

给出：哪些 TeX 引擎在、哪些 `.cls` 装了、`python-docx` 能不能 import、
13 个期刊族的版式参数表、当前能出哪几种格式。

**在怀疑构建有问题之前先跑这个。** 大部分「出不来 PDF」是引擎不在，不是代码错。

## 五、支持哪些刊

改 `journal` 字段能选的是 `data/journals.json` 里那 53 个刊（Nature、Science、Cell、PNAS、
PLOS 系、IEEE 系、APS 系、Springer 系…）。这些刊映射到 13 个版式族：

| 族 | LaTeX 类 | 页尺寸 | 字号 | 行距 | 行号 | 引文 |
|---|---|---|---|---|---|---|
| `elsevier` | elsarticle | A4 | 12pt | 双 | 有 | APA |
| `cell` | elsarticle | Letter | 12pt | 双 | 有 | Cell |
| `springer-nature` | sn-jnl | A4 | 12pt | 双 | 有 | Nature |
| `nature` | article | A4 | 12pt | 双 | 有 | Nature |
| `science` | article | Letter | 12pt | 双 | 有 | Nature |
| `plos` | article | Letter | 12pt | 双 | 有 | Vancouver |
| `ieee` | IEEEtran | Letter | 10pt | 双 | 无 | IEEE |
| `aps` | revtex4-2 | Letter | 12pt | 双 | 有 | Nature |
| `acs` | achemso | Letter | 12pt | 双 | 有 | APA |
| `mlr` | article | Letter | 11pt | 单 | 无 | IEEE |
| `bmc` | article | A4 | 12pt | 双 | 有 | Vancouver |
| `wiley` | article | A4 | 12pt | 双 | 有 | APA |
| `nejm` | article | Letter | 12pt | 双 | 有 | Vancouver |
| `generic` | article | A4 | 12pt | 双 | 有 | APA |

不在表里的刊不用改代码：写 `publisher: "IEEE"` 用出版社族兜底（支持 46 个出版社别名），
再不行就走 `generic`（A4 双倍行距带行号，投稿稿的通用形态）。

> 注意：这里的参数都是**投稿稿**形态，不是排版厂最终形态。
> IEEE 投稿要求单栏双倍行距 10pt，所以 `ieee` 族是单栏；双栏是录用后的事。

## 六、和 M4 的接法

`science_paper_plan` 给出标题草稿、贡献句、图表清单——那是**内容骨架**。
把它按 `paper.md` 的格式摊平，填进 `# Introduction / # Results / # Discussion`，
再跑 lint + build，就是一条从「GitHub 上还没写成论文的知识」到「能投的 PDF」的完整链路。

M4 的铁律在 M5 依然成立：`paper_plan` 给的标题和摘要是骨架，标着 `draftIsRough`。
**排版不会让它变成真结论**——lint 只查要件，不查论证。
