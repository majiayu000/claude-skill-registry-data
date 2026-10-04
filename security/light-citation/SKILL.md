---
name: light-citation
description: 论文引用规划、审查与多格式生成。当用户需要处理参考文献、引用、bibtex 时使用。审查引用的关联度、真实性、权威性、时效性、数量、中外占比，是否引用了经典/最新/代表性/对比工作。避免虚假引用、过度引用、无关引用、堆砌、遗漏关键文献、低质量来源、引用与正文不匹配。生成 BibTeX/EndNote/GB-T 7714/APA/IEEE 等格式并按目标 venue 调整。
---

# 论文引用管理

## 引用规划
1. 列出论文每个需要引用的 claim/方法/数据集/对比工作。
2. 为每处匹配最合适的来源：经典奠基文献 + 最新进展 + 直接对比方法 + 必要背景。
3. 检查覆盖：领域经典是否引？最新(近 1–2 年)是否引？SOTA baseline 是否引？

## 引用审查（逐条核查）
- **真实性**：DOI/标题/作者/年份可核查，杜绝臆造（CONVENTIONS §4）。核验路径：
  - 优先 Crossref `https://api.crossref.org/works?query.bibliographic=<标题+作者+年>&mailto=<邮箱>`（礼貌池更稳），比对返回的 `title/author/issued/DOI`。
  - 单 DOI 直查 `https://api.crossref.org/works/{doi}`；查不到再用 OpenAlex `filter=title.search:...` 或 Semantic Scholar `/paper/search` 兜底。
  - 标准：每条引用都要能定位到真实记录；对不上即标"疑似臆造/需核查"，不放过。
- **关联度（locator 审计）**：每条引用不只要"真实存在"，还要"真的支撑它所附的那句话"。这是引用核验里最易被跳过、却最伤诚信的一环（对接 paper-drafting 失败模式 M2）。可操作审计见 `references/locator_audit.md`——逐条给引用配一个 locator（页码/章节/图表号/原文片段），核对"被引文献此处是否真的说了正文声称的内容"，三态判定：`supports`（原文确实支撑）/ `partial`（沾边但夸大或断章取义→改写正文或换引用）/ `unsupported`（原文根本没这意思→删或换）。key/DOI 对得上 ≠ 论点被支撑。
- **权威性 vs 开放性（须区分，别混用）**：
  - *开放性/可访问性*：`verify_refs.py` 已从 OpenAlex 同源带出 `is_oa/oa_status/venue/is_in_doaj/type/version`，给的是"能否免费拿到、什么 OA 通道"。**`oa_status==closed` 不等于低质**——顶刊大量闭源，绝不据此扣分。
  - *权威性/掠夺性*：来源层级要看 DOAJ 收录、期刊分区、掠夺性预警名单（如 Beall's list 衍生），**须人工判定**，脚本只给线索不下结论（见 `summary.authority_note`）。
  - 预印本：脚本对 `type=preprint` 或非 `publishedVersion` 产 warning，引用须注明未经同行评审或换正式版 DOI。
- **时效性**：是否遗漏近期关键工作。用 Crossref `filter=from-pub-date:` 或 OpenAlex `filter=publication_year:>` 扫近 1–2 年高被引。
- **撤稿核查（2026 投稿硬需求）**：引用已撤稿文献是诚信事故。`verify_refs.py` 已在 Crossref 同源响应里查 `update-to[]` 撤稿信号 + 标题 `RETRACTED` 前缀（判定口径与 a10 light-research-ethics `light-research-ethics/scripts/check_retractions.py` 同源），命中报 **high severity**（`is_retracted=true`，须删除或换源）。批量预筛或需更新更正/关注声明全表时，直接跑 a10 的 `light-research-ethics/scripts/check_retractions.py`（三态 RETRACTED/FLAGGED/CLEAN）。**诚实局限**：经典撤稿论文本身常不暴露 `update-to[]`（publisher 行为各异），故标题前缀作补充信号；CLEAN ≠ 保证未撤稿，高风险引用须交叉查 Retraction Watch。
- **被引关系核验**：声称"A 引用了 B"时，跑 `scripts/verify_citation_edge.py <A的DOI> <B的DOI>` 实证，不靠印象。脚本三态输出：`confirmed`（开放索引查到 A→B）/ `not_in_open_index`（OpenCitations+S2 均 200 但未含 B——**开放索引未覆盖 ≠ 未引用**，须人工查全文或 WoS/Scopus）/ `unknown`（端点非 200/限速，无法判定）。绝不据开放索引缺失就断言"未引用"。
- **数量**：是否过少(支撑不足)或过多(堆砌)。用 `is-referenced-by-count`/`cited_by_count` 辅助判断代表性。
- **中外占比**：按 venue 合理（中文期刊需足量中文文献，国际会议以英文为主）。
- **自引**：比例是否过高。

## 格式生成
- **最快路径——DOI 内容协商**：对 `https://doi.org/{doi}` 带 `Accept` 头直接取格式，免转换：
  - `Accept: application/x-bibtex` → BibTeX；`application/vnd.citationstyles.csl+json` → CSL JSON；`application/x-research-info-systems` → RIS。
  - `Accept: text/x-bibliography; style=apa; locale=en-US` → 直接返回已排版书目（style 取 CSL 名：apa/ieee/chicago-author-date…）。curl 记得 `-L` 跟随重定向。
- **多格式中枢**：以 CSL JSON 存储，配 .csl 样式经 Pandoc/Zotero 渲染成任意期刊格式。`type` 字段决定模板（article-journal/paper-conference/book…），选错套错模板。
- **中文国标**：GB/T 7714-2015，安装社区 .csl（区分 `-numeric` 顺序编码 / `-author-date`），核查文献类型标识码 `[J]/[C]/[M]/[D]/[EB/OL]` 与作者 >3 取前 3 加"等"。每条 .bib 条目须带 `langid={chinese|english}`（按作者/标题是否含 CJK 判定）——缺 langid 会让"等/et al."与 `[C]/[J]` 类型标识在国标排版下出错；`doi_to_any.py` 产 BibTeX 时已自动注入。
- **无 DOI 中文文献核验兜底**：知网/万方收录的中文文献常无 DOI，落不进下面以 DOI 为入口的脚本核验，但**不得跳过真实性核查**。走 references.md「中文文献核验兜底」节：① CNKI 题录手工 → .bib 字段映射 + 逐条齐全性 checklist（含 langid 与文献类型标识）；② GB/T 7714-2015 中文条目核对速查表（≤15 行）。本技能是中文核验的**执行方**，m07（light-paper-drafting）integrity_gate.md 第 4 节是写作时的**拦截方**，两方题录三字段（题名/作者+单位/刊名+年卷期页）口径一致。
- **键名规范（与 m07/m08 正文占位同公式）**：citekey 统一用 Better BibTeX 公式 `authorYearWord`——**第一作者姓 + 年份 + 标题首个实词，全部小写**（如 `zhang2024deep`），冲突自动加 a/b/c。生成 .bib 时**按此公式 pin citekey**，不要沿用 DOI 注册商内容协商返回的原始键（那些键与正文 `\cite{}` 对不上，排版会报 undefined citation）。正文 `\cite{}` 占位与 .bib 键必须同源同公式。
- **LaTeX 后端**：先看目标模板要求——顶会模板（IEEEtran/ACM/LNCS）常锁定传统 `bibtex`+指定 .bst；现代 `biblatex+biber` 原生 UTF-8、排序更强但字段名不同（`journaltitle`/`date`）。不擅自换后端。

## 工具视角
- **元数据/真实性核验**：Crossref（DOI 权威源，礼貌池带 `mailto`，深翻页用 `cursor=*`）、OpenAlex（`filter`/`group_by` 强，摘要是倒排索引需重建；2026 起需免费 key，接入口径见 m01 references「OpenAlex 接入真相源」）、Semantic Scholar（强在引用关系与影响力，申请免费 `x-api-key` 避 429）。
- **开放获取**：Unpaywall `/{doi}?email=`，看 `is_oa`/`oa_status`/`best_oa_location.url_for_pdf`，注意 `version` 是否正式版。
- **引用关系实证**：OpenCitations `/citations/{id}`、`/references/{id}`（只覆盖开放 DOI-DOI，不当完整计数）。
- **库管理**：Zotero（Web API v3，`format=bibtex/csljson`，`include=bib&style=`）+ pyzotero（`zot.items(content='bib', style='ieee')`、`everything()` 翻页）；纯 LaTeX 流可用 JabRef（DOI/arXiv fetcher + integrity check 体检 .bib）。
- **协作互导**：与 EndNote/Mendeley 交换统一走 RIS 或 .bib；勿假设 Mendeley 历史 API 仍可用，迁移前先验证。
（各工具真实端点/参数/坑见 references.md）

## 端到端 workflow（可运行脚本串联）
> 全部脚本免外部依赖（标准库 urllib），自带 `__main__` 自测，端点已 curl 实测（HTTP 码见 references.md）。

1. **搜索/抽取** — Crossref `query.bibliographic` 或 OpenAlex `filter=title.search:` 找候选，拿到 DOI 清单；正文 `.bib`/`.tex` 里的 DOI 也可直接抽出。
2. **去重** — 合并同一工作的多版本/多 DOI（预印本 vs 正式版优先正式版）。
3. **真实性+一致性核验** — 一条命令产机读报告：
   ```bash
   # 在本技能目录（skills/light-citation/）下运行
   python scripts/verify_refs.py --file dois.txt --self-author 张 --out report.json
   ```
   读 `report.json`：`summary.high_severity_errors` 必须为 0；查不到的 DOI 标 `severity:high`（疑似臆造）；**`summary.retracted_count` 必须为 0**——任一 `is_retracted=true` 的引用须删除或换源（撤稿信号来自 Crossref `update-to[]` + 标题前缀，口径同 a10 check_retractions.py）；
   另给中外占比 `cn_ratio`、自引率 `self_citation_rate`、缺近 2 年标志 `missing_recent_2y`、预印本数 `preprint_count`、各源 HTTP 码与 OA 字段（`is_oa/oa_status/venue/is_in_doaj`，反映开放性非权威性）。
   **离线降级协议（无网/限流时核心闸门怎么办）**：脚本区分三态——①连上但查无记录(HTTP 404)→ `severity:high` 疑似臆造，真问题；②连上且查到但对不上/已撤稿→真问题；③**两源都网络不可达(HTTP 0)→ `unverified_offline=true`，记 warning 不记 high error**。`summary.unverified_offline_count>0` 时 `offline_note` 会提示：这些引用是【未核验】而非【已通过】，**核验闸门不得放行**——不可把"没连上网"当成"已核验通过"，也不可诬为"疑似臆造"；须联网后重跑 `verify_refs.py` 再下真实性结论。投稿前体检若处于离线，必须显式告知用户"引用真实性尚未核验，联网后补验"，不假装已过闸。
   **对正文声称的第三方引用关系**（"A 引用了 B"），逐条跑 `python scripts/verify_citation_edge.py <A> <B>` 实证，取三态结论而非凭印象断言。
4. **GB/T 7714 渲染 / 多格式生成** — 逐 DOI 出 BibTeX + CSL JSON + 国标排版文本：
   ```bash
   python scripts/doi_to_any.py 10.1038/s41597-023-02555-8 --format all
   ```
   `--format gbt7714` 直接给顺序编码制中文书目；CSL JSON 可再喂 Pandoc 配 .csl 渲染任意期刊样式。
   生成 .bib 时按 `authorYearWord` 公式 pin citekey（见上"键名规范"），中文条目自动带 `langid=chinese`。
5. **抽正文 citekey ↔ .bib 键对账** — 跑 `python scripts/citekey_audit.py --tex paper.tex --bib refs.bib`（支持 LaTeX `\cite*` 与 pandoc `[@key]` 两种语法）：求双向差集——**缺失键**（正文引了 .bib 没有→编译出 `??`，必修）、**冗余键**（.bib 有正文没引→投稿前清理）、**.bib 重复定义键**（必修）；`--check-naming` 另校验是否合 `authorYearWord` 惯例。两侧 citekey 公式一致（m07/m08 占位即用此公式）才能对上。
6. **投稿前体检** — 逐项过 `assets/citation_checklist.md`（真实性/关联度/中外·SOTA·经典覆盖/数量健康度/格式），
   并用其中"被引阈值分档表"按文献年龄判代表性。
7. **产出报告** — 汇总 `report.json` + checklist 结论，给补引/删引/换源/改格式的修改清单。

## 脚本与资产
- `scripts/doi_to_any.py` — DOI 内容协商 → BibTeX / CSL JSON / GB-T 7714，BibTeX 按 CJK 自动注入 `langid`，含真 DOI 自测。**GB/T 7714 CJK 作者特判**：中文名整名连写、不套西文缩写（"张伟"非"张 W."）；电子资源 `[EB/OL]` 带访问日期（缺则显式"访问日期待补"占位不静默丢）。
- `scripts/verify_refs.py` — 批量 DOI 经 Crossref+OpenAlex 双源核验，产机读 JSON 报告（含 OA 开放性字段、预印本计数、**撤稿检测** `is_retracted`/`retracted_count`，口径同 a10 check_retractions.py）。**撤稿覆盖度诚实声明**：summary 显式区分"已用信号"(Crossref update-to + 标题 RETRACTED)与"未覆盖经典撤稿"，`retracted_count=0 ≠ 保证干净`，高风险引用提示交叉查 Retraction Watch / 跑 a10 第二跳。**嵌合引用检测**（Chimeric，借 PHY041）：传 `claimed={first_author,title}` 时，若 DOI/标题真实但声称首作者不在真实作者列表→标 `is_chimeric`（真标题配错作者的 AI 幻觉）。**自引按作者姓精确匹配**（非整串子串，降 Wang/Li 等高频姓误报）。含真/假 DOI 自测。
- `scripts/verify_citation_edge.py` — 实证引用边"A 引用了 B"，OpenCitations 双向 + Semantic Scholar 兜底，三态输出（confirmed/not_in_open_index/unknown），含真 DOI 自测。
- `assets/citation_checklist.md` — 投稿前体检清单 + 被引阈值分档表 + 中外/SOTA/经典覆盖自检表。

## 产出
1. 引用审查报告（问题清单 + 修改建议：补引/删引/换源/改格式）。**标准工件：`citation_audit.md`**（真实性 + locator，命名见 CONVENTIONS §6.1）。
2. 规范化 .bib / 对应格式文件。**标准工件：`refs.bib`**（交 m12）。
3. 正文引用位置与编号核对。

## 衔接
与 m07/m08/m12 协同；缺关键文献回 m01 补检；格式随 m13 选定 venue 调整(引用样式查 db01 `reference_style` 字段 → LaTeX bst/CSL 映射见 **db01 references.md §2**，与 m12 排版同源)；引用库登记 db09。虚假/掠夺性来源风险上报 a10。

---
工具真实端点、参数、限速与已知坑详见同目录 `references.md`。
