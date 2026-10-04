---
name: light-typesetting
description: 根据目标期刊/会议/学校/比赛要求做 LaTeX 或 Word 排版并编译导出最终 PDF/Word。当用户需要套模板、排版、解决编译错误、导出论文时使用。处理标题层级、页边距、目录、摘要、关键词、公式、图表、算法伪代码、参考文献、附录、页眉页脚、页码、单/双栏、编号、交叉引用，并检查 LaTeX 编译错误、Word 格式问题、引用错误、图片位置、字体一致性、编号混乱。
---

# LaTeX / Word 排版与导出

## 开工前
确认目标 venue 的官方模板与要求(db01: template_url, reference_style, 单双栏, 页数限制)。`reference_style` → LaTeX 文档类/bst 的映射查 **db01 references.md §2**（与 m10 引用同源，不各读各的）；`template_url` 是易腐链接，取用前校验 200，失链回 venue 官网 author kit。优先官方模板，不自造。取模板优先级：venue 官网 author kit > Overleaf 官方模板页(`overleaf.com/gallery/tagged/…` 或 "Open as Template") > CTAN 包。注意会议模板有年度版本(如 NDSS `bare_conf_LAST-X2026.tex`)，务必用当届指定版本，旧版会被 desk-reject。从官方骨架文件改(IEEE `bare_conf.tex`、ACM `sample-*.tex`)，不从空文件起。

## LaTeX 路线
套用官方 cls，关键起手式：
- IEEEtran：`\documentclass[conference]{IEEEtran}`(会议双栏)，作者块 `\IEEEauthorblockN/A`，关键词 `IEEEkeywords` 环境，`\bibliographystyle{IEEEtran}`。宽图用 `figure*` 跨栏放页顶。
- acmart：`\documentclass[sigconf]{acmart}`(会议)/`acmsmall`(期刊)/`manuscript`(审稿)；双盲加 `[review,anonymous]`；填 `\acmConference`、`\setcopyright`、CCS `\ccsdesc`(从 dl.acm.org/ccs 生成)、`\keywords`，缺版权会出红框。
- llncs：`\documentclass{llncs}`，机构用 `\inst{}` 编号，必填 `\titlerunning/\authorrunning`，`\bibliographystyle{splncs04}`。
- elsarticle：投稿 `[preprint,review,12pt]`(出行号宽行距)，前置信息放 `frontmatter`，参考文献按期刊指定 `elsarticle-num`/`-harv`。
- 中文：`ctex` 文档类/宏包 + XeLaTeX 或 LuaLaTeX。
结构件：abstract、keywords、章节层级、公式(amsmath/mathtools)、图表(graphicx + booktabs 三线表 + subcaption)、算法(algorithm2e 或 algpseudocode)、参考文献、附录。
交叉引用用 `\label`+`cleveref` 的 `\cref`(自动带 Fig./Eq. 前缀)；hyperref 先加载、cleveref 后加载。
参考文献两套体系不可混：传统 bibtex + venue `.bst`，或现代 biblatex + biber。国标用 `gbt7714` 包(`\bibliographystyle{gbt7714-numerical}` 顺序编码 / `gbt7714-author-year`)，条目必须带 `langid` 区分中英文，否则"等/et al."与文献类型标识`[C]/[J]`会错。

## 编译与环境
- 用 `latexmk` 自动收敛多轮编译：`latexmk -pdf file.tex`(pdflatex)；中文/特殊字体用 `-xelatex` 或 `-lualatex`；minted/TikZ 外部化加 `-shell-escape`；CI 用 `-interaction=nonstopmode`；`-pvc` 持续预览；清理 `-c`(留 PDF)/`-C`(全删)。可用 `latexmkrc` 设 `$pdf_mode`(1=pdflatex/4=lualatex/5=xelatex)。
- 缺包：TeX Live 用 `tlmgr install <pkg>`(先 `tlmgr update --self`)，查归属 `tlmgr search --global --file <name.sty>`；轻量环境用 TinyTeX，`tinytex::latexmk()` 编译时自动探测安装缺失包。
- 逐条排查 error/warning：缺包、未定义引用(跑够轮数/bibtex)、overfull/underfull hbox、图片找不到；字体与数学字体保持一致。
- **投稿出包前净化(借 arxiv-latex-cleaner)**：交 arXiv/会议前清掉源码里的隐私与体积包袱——注释里的真名/草稿/内部链接(`%` 注释 arXiv 会随源公开)、未引用的图片与 `.bib` 条目、`\todo`、超大原图。可用 `arxiv-latex-cleaner <dir>` 一键(去注释+压图+删冗余)，或手动核对后再打包。配合 `submission_check.py` 先扫合规雷区，双保险。

## Word 路线
- 套用官方 .docx 模板；用样式(Styles)而非手动格式控制层级。
- 题注与交叉引用、自动编号、参考文献(Zotero/EndNote 插件域)、页眉页脚页码、分栏。
- 检查：字体一致、编号连续、图表位置、域更新。
- 生成/转换：Pandoc md→docx 套样式 `pandoc in.md -o out.docx --reference-doc=ref.docx`(ref.docx 提供标题/正文/题注样式)，参考文献 `--citeproc --bibliography=refs.bib --csl=style.csl`(CSL 体系，非 .bst)。编辑既有 docx 可解包改 `word/document.xml`/`styles.xml` 再打包(保留原结构不重排)；修订红线用 OOXML `<w:ins>/<w:del>`。复杂公式转 docx 走 OMML 可能走样。
- 内容提取(非还原版式)：MarkItDown 把 pdf/docx/pptx 转 markdown 喂下游；python-docx 批处理。
- 详细可执行清单见 [references.md](references.md) "Word 学术排版"大节：核心 checklist(样式/多级列表/题注交叉引用/域 F9 刷新/分节符/自动目录/插件/文档检查器)、22 条常见错误对照表(现象→原因→修法)、中文学位论文模板纪律(以本校研究生院官方 .docx 为准)。

## 端到端 walkthrough（内容+引用+图 → 模板 → 编译 → precheck → PDF）
以 IEEE 会议双栏为例，其它 venue 把模板文件名替换即可：
1. **选模板骨架**：从 `templates/` 拷官方骨架起手，不从空文件写。
   - IEEE→`ieee_bare_conf.tex`，ACM→`acm_sigconf.tex`，Springer LNCS→`springer_llncs.tex`，Elsevier→`elsevier_elsarticle.tex`，中文→`ctex_chinese.tex`。
   - 五份骨架结构完整、可直接编译（见各文件头注释的编译命令）。**编译验证（2026-06-12，Tectonic）**：五份全部 `tectonic <f>.tex` 退出 0 产出 PDF（IEEE/ACM/Springer/Elsevier 走 pdflatex 路径，ctex_chinese 走 XeLaTeX 路径自动装中文字体）；留痕 `_verification_log/R7-tex-compile.md`。
2. **灌内容**：填 title/author/abstract/keywords、章节正文(来自 m07/m08)、公式(`amsmath`)、三线表(`booktabs`)、算法(`algorithm2e`/`algpseudocode`)。图(来自 m11)用 `\includegraphics` 替换骨架里的 `\rule{}` 占位框；宽图用 `figure*` 跨双栏放页顶。
3. **挂引用**：引用(来自 m10)写进 `refs.bib`，正文 `\cite{key}`，启用骨架里注释的 `\bibliographystyle{IEEEtran}`+`\bibliography{refs}`(替换演示用 `thebibliography`)。交叉引用用 `\label`+`\cref`。
4. **编译收敛**：`latexmk -pdf -interaction=nonstopmode file.tex`(中文用 `-xelatex`)。latexmk 自动跑够轮数 + bibtex/biber 直到引用/目录收敛。缺包：TeX Live `tlmgr install`、MiKTeX `miktex packages install <pkg>` 并 `initexmf --update-fndb`。
5. **precheck**：`python scripts/precheck_log.py file.log`(加 `--json` 出结构化；**交付门用 `--strict`** 把 undefined ref/cite/重复 label 提升为致命阻断)。脚本先把 79 列硬折行 de-wrap 拼回再匹配，消除长引用名漏报。退出码非 0 = 有致命错误。按输出类别查 `references/latex_errors.md` 的「症状→根因→修法」表逐条修。
6. **投稿合规/匿名扫描**：`python scripts/submission_check.py --tex paper.tex --pdf paper.pdf --double-blind --max-pages 8` —— 扫 desk-reject 雷区：双盲未匿名 `\author`/致谢/基金/可识别链接、PDF 元数据 `/Author` 露名、超页数、残留 TODO。高危项投稿前必清（这些不是内容问题但照样被编辑一眼拒）。
7. **复核出 PDF**：过下面检查清单，确认页数/版式/匿名合规后交付 PDF + 可编译源工程 + 合规核对表。

Word 路线：用 `assets/docx_template.js`(docx-js)以代码生成带样式/TOC/页眉页脚页码的 .docx(`npm install docx && node docx_template.js`)，A4 与 US Letter 在 `PAGE` 常量切换；或 Pandoc `md→docx --reference-doc`。

## 检查清单（导出前）
□ 编译/打开无报错(跑 precheck_log.py 退出码为 0) □ 所有 \ref/题注解析正确 □ 图表清晰且位置合理 □ 参考文献格式符合 venue □ 页数/页边距/字号合规 □ 公式编号连续 □ 算法格式正确 □ 摘要关键词齐全 □ 字体统一 □ 匿名要求(双盲去作者信息)。

## 产出
最终 PDF（+ Word 版如需）+ 可编译源工程 + 一份"格式合规核对表"。

落盘工件名（CONVENTIONS §6.1，下游 m13/m14/提交 消费）：最终 `paper.pdf` + 可编译源工程 + 格式合规核对表。

## 本技能资产
- `scripts/precheck_log.py`：扫 LaTeX `.log` 抓 undefined refs/citations、multiply-defined labels、overfull/underfull hbox、missing figure/file、undefined control sequence、致命 LaTeX/TeX error，按严重度汇总报告(`--json`/`--max`)，致命项退出码 1。**`--strict`** 把 undefined ref/cite/重复 label 提升为致命（交付门拦截）；**先 de-wrap** 把 79 列硬折行拼回再匹配（消除长引用名被折断的漏报）。无参数跑内置样例自测。
- `scripts/submission_check.py`：投稿前合规/匿名雷区扫描——双盲未匿名 `\author`/`\thanks`/致谢/基金/可识别链接(github/orcid)、PDF 元数据 `/Author` 露名、页数上限、残留 TODO/XXX。`--tex`/`--pdf`/`--double-blind`/`--max-pages`，高危项退出码 1。纯标准库扫静态雷区，不替代 venue 投稿须知核对。
- `templates/`：五份最小可编译骨架——`ieee_bare_conf.tex`/`acm_sigconf.tex`/`springer_llncs.tex`/`elsevier_elsarticle.tex`/`ctex_chinese.tex`，文件头注明编译命令与 venue 注意事项。
- `assets/docx_template.js`：docx-js 完整模板，含 Document/Packer 样板、DXA 尺寸换算表、Heading 样式 + outlineLevel、**真·多级列表(numbering LevelFormat 自动连号，替手敲编号)**、**默认字体含 eastAsia CJK(中英混排不回退默认字体)**、TableOfContents、页眉/页脚 + 页码、A4 vs US Letter 显式页面设置、booktabs 风格三线表。
- `references/latex_errors.md`：常见编译错误对照表(致命错误/警告/bibtex/中文 五大类，症状日志→根因→修法)。
- `references.md`：逐工具真实端点/选项/配置与已知坑。

## 衔接
图来自 m11，引用来自 m10，内容来自 m07/m08，目标来自 m13。投稿匿名/页数风险提示用户。版本入 db09。交付前过 a08(light-self-review)自检闸门。

---
工具真实端点/选项/配置与已知坑见同目录 `references.md`。
