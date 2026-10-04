---
name: light-literature-search
description: 强大地搜索并规范化整理科研资料。当用户需要调研某研究方向、找文献综述、了解某领域有哪些工作、搜集中英文论文/专利/标准/政策/数据集/开源项目/竞赛方案/行业报告/技术博客/官方文档时使用。不只罗列结果，而是筛选去重分类、判断可信度与重要性，整理为文献表、研究脉络、代表方法、优缺点对比与可复用资源。
---

# 资料搜索与规范化整理

## 目标
帮用户真正快速理解一个方向，而非堆搜索结果。产出可直接用于写综述、提 idea、做方案的结构化资料。

## 输入澄清（缺失则先问或合理假设）
研究方向、核心问题、关键词（中英文）、目标期刊/会议、项目背景、时间范围、语言偏好、深度（速览/中等/穷尽）。

## 检索策略
1. **多源并行**：英文论文(arXiv/OpenAlex/Semantic Scholar/Crossref/DOAJ)、生医论文(PubMed/Europe PMC，详见下"优先免费无 key 的学术 API"与生医纪律)、中文论文(优先 OpenAlex/Crossref 按 ISSN 检中文期刊；知网/万方/维普/CSCD 无免费 API，走机构访问或浏览器取元数据，详见下"中文文献检索")、专利(Google Patents/CNIPA/Espacenet/Lens)、标准、政策、数据集(HF/Kaggle/OpenML)、开源(GitHub/PwC)、竞赛方案、行业报告、技术博客、官方文档。
2. **多角度扫**（multi-modal sweep）：按概念、按方法、按作者/团队、按时间、按引用关系分别检索，互补盲区。
   - **跨领域轴（创新高发区）**：窄应用领域近三年好文常稀少，但前沿创新多靠**把别的领域的最新方法迁移过来**（如 CV 目标检测/扩散模型/Transformer SOTA → 病理识别、畜牧行为、遥感）。此时**别把"应用词+方法词"拼成一个 query**（实测拼词+被引排序会顶出通用高被引跑题文），改用 `scripts/cross_domain_search.py` 做应用轴 × 方法轴正交检索，方法轴强时效抓 SOTA，迁移判断交研究者（喂 m03）。
3. **检索式构造**：给出每个库的实际可用 query（布尔逻辑、字段限定、同义词扩展、中英对照）。
4. **滚雪球**：从代表作做前向(被引)+后向(参考)追踪。

### 优先免费的学术 API（多数免 key；OpenAlex 2026 起需免费 key，接入口径见 references「OpenAlex 接入真相源」。端点详见 references.md，落地前再核校）
- **OpenAlex** `https://api.openalex.org/works`：`search=` 全文检索；`filter=` 组合(`from_publication_date:`、`cited_by_count:>N`、`is_oa:true`、`type:article`、`primary_topic.id:`、`authorships.author.id:`)；`sort=cited_by_count:desc`；`select=` 省字段；深翻用 `cursor=*`(`page` 上限 1 万)；带 `mailto=` 进礼貌池。`group_by=` 可一键做年度/期刊分布。摘要是 inverted index 需还原。**接入需免费 key，额度/限流口径见 references「OpenAlex 接入真相源」节。**
- **Crossref** `https://api.crossref.org/works`：`query.bibliographic/author/title=`；`filter=from-pub-date:,type:journal-article`；`sort=is-referenced-by-count&order=desc`；深翻 `cursor=*`；带 `mailto=` 提速。作 DOI 规范化与去重的"真相源"。
- **Semantic Scholar** `https://api.semanticscholar.org/graph/v1`：`/paper/search?query=&fields=title,abstract,year,authors,citationCount,influentialCitationCount,externalIds,openAccessPdf,tldr`；穷尽式扫库用 `/paper/search/bulk`(返回 `token` 续翻)；滚雪球用 `/paper/{id}/citations` 与 `/references`(看 `isInfluential`)；批量详情 `/paper/batch`(POST)。匿名限速严，量大申请 `x-api-key`。
- **arXiv** `http://export.arxiv.org/api/query`：`search_query=ti:/au:/abs:/cat:/all:` + 布尔；`start`/`max_results`(≤100) 翻页；`sortBy=submittedDate&sortOrder=descending`；请求间隔 ≥3 秒。
- **PubMed E-utilities** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`：两步式 `esearch.fcgi?db=pubmed&term=...` 取 PMID → `efetch.fcgi`/`esummary.fcgi` 取详情；`term` 支持 `[MeSH Terms]`/`[tiab]`/`[ti]`/`[au]`/`[dp]`；`retmax`/`retstart` 翻页，大集合用 `usehistory=y`+`WebEnv`/`query_key`；建议带 `&email=&api_key=`(无 key 3 req/s、有 key 10 req/s)。**MeSH 受控词检索与 Clinical Queries 临床过滤器此源独有，OpenAlex 替代不了。**
- **Europe PMC** `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=&format=json&resultType=core`：完全免 key；`pageSize`(≤1000)+`cursorMark`(传 `*`，响应 `nextCursorMark` 续翻)；返回直接含 `abstractText`、`pmid`/`pmcid`/`doi`、`isOpenAccess`/`inEPMC`/`hasPDF`、`citedByCount`；`/{source}/{id}/citations` 与 `/references` 做滚雪球；覆盖 MED+PMC+PPR。
- **DOAJ** `https://doaj.org/api/v2/search/articles/{query}?pageSize=N`：完全免 key；**按相关度排序**（非被引），补 OpenAlex/Crossref 纯被引排序顶出跑题高被引文的盲区；`bibjson` 含 title/year/author/journal/abstract/identifier(DOI)；只覆盖开放获取期刊、不出被引；已落地 `search_normalize.py` 第三源，详见 references「DOAJ API」。
- **跨源去重锚点**：优先按 DOI 归并，无 DOI 再按 arXiv id / 规范化标题+作者+年。被引数跨库不可直接比(Crossref 低估、S2 含估计、OpenAlex 口径不同、Europe PMC/PubMed 又是另一口径)，注明来源。
- **生医纪律（必做）**：涉生医/临床/系统综述方向，**PubMed+MeSH 检索式为必做项**(对齐已宣称的 PRISMA)，不能只靠 OpenAlex/S2 的全文检索冒充规范检索；MeSH 受控词与 Clinical Queries 临床过滤器是 PubMed 独有能力。**已落地脚本 `scripts/biomedical_search.py`（Europe PMC+PubMed）兑现此项**——PubMed 支持把 MeSH 检索式写在 `term` 里透传（如 `lameness[MeSH Terms] AND goat[tiab]`）；但"自由词→MeSH 主题词"的自动映射本脚本不做（需接 NCBI MeSH 库，属 P2 增强），MeSH 受控词需你按规范写好。Europe PMC 作免 key 补充(直接给 abstract+开放获取标记+引用端点)。**预印本最前沿**用 `scripts/arxiv_search.py` 补 arXiv 与 bioRxiv/medRxiv(免 key；bioRxiv 无服务端关键词检索，脚本拉时间窗后本地过滤并如实标注，预印本须按可信度分级标注)。四源(OpenAlex+Europe PMC+PubMed+arXiv/bioRxiv)并查互补盲区，前两源在 `search_normalize.py`、后多源在 `biomedical_search.py`/`arxiv_search.py`。

### 中文文献检索（必做，勿只做英文）
中文核心成果大量在知网/万方等库，但这些库**无公开免费 API**；OpenAlex/Crossref 却**已收录大量中文期刊**(按 ISSN 可直接命中)，应作为低门槛主力(OpenAlex 需免费 key，Crossref 免 key)，机构访问的中文库作补充。
- **OpenAlex 检中文期刊（已实测可用）**：按刊名/ISSN 定位 source 再拉 works。例：计算机学报 = `https://api.openalex.org/sources/issn:0254-4164`(实测 OpenAlex ID `S4210175330`、`country_code:CN`、1264 篇)，再 `GET /works?filter=primary_location.source.id:S4210175330&sort=cited_by_count:desc`。**坑**：OpenAlex 常把中文论文的标题/摘要存成英译，`group_by=language` 可能显示 `en` 而非 `zh`，故按 source.id 检索比按 `language:zh` 更可靠。
- **Crossref 检中文期刊（已实测可用）**：`https://api.crossref.org/journals/0254-4164`(实测命中"Chinese Journal of Computers"、出版商 China Science Publishing & Media、1264 DOI)；`/journals/{ISSN}/works?query=` 在刊内检索。先用中文核心刊 ISSN 清单批量探源。
- **知网 CNKI / 万方 Wanfang / 维普 VIP / CSCD（无公开 API，仅网页或机构订阅）**：均需机构/IP 授权或人工网页检索，无对外免费 API。用 browser-use / agent-browser 走"真人式浏览"取**元数据/摘要/链接**(遵守 robots/ToS，不抓全文)；或让用户在机构账号下导出题录(EndNote/RefWorks/NoteExpress/RIS 格式)再入库。CSCD(中国科学引文数据库)被引数据同样仅机构端可得，标"免费源不可得"。
- **百度学术 / 谷歌学术（无官方 API）**：仅网页，反爬强；只作发现入口，命中后回 OpenAlex/Crossref 按 DOI 或刊名核实元数据再入表，不直接采信其页面被引数。
- **中文主题词检索建议**：① 中英双语同义词都要试(如"大语言模型/大模型/LLM/large language model")；② 用《汉语主题词表》/学科规范词 + 同领域核心刊高频关键词扩展；③ 简繁体、全半角、专有名词缩写都要兼顾；④ 优先锁定中文核心刊范围(北大核心/CSCD/CSSCI)，可先建目标刊 ISSN 清单再逐刊检索。
- **GB/T 7714 引用格式**：中文条目按 GB/T 7714-2015 著录。期刊示例：`主要责任者. 题名[J]. 刊名, 年, 卷(期): 起止页码.`；带 DOI 末尾加 `DOI: 10.xxxx/xxxx.`。文献类型标识：专著[M]、期刊[J]、论文集[C]、学位论文[D]、报告[R]、标准[S]、专利[P]、电子资源[EB/OL]。入表时中英文条目分别按各自规范(中文 GB/T 7714、英文 APA/IEEE 等)著录并注明。

### 无 API 的源用浏览器 agent 取数
知网/万方网页、政府标准/政策站、Google Scholar 等无开放 API 或反爬时，用 **browser-use**(本地 Python+Playwright) 或 **Browserbase/Stagehand agent-browser**(云端，`observe→act→extract` 抽结构化字段)走"真人式浏览"取元数据。只取元数据/摘要/链接，遵守 robots/ToS 与版权；结果非确定，须二次校验。

### 补充网络检索
arXiv/学术库覆盖不到的官方文档、技术博客、项目页、行业报告：用 **Exa**(`/search` neural/keyword + `contents` 取正文高亮，`/findSimilar` 以网页为种子滚雪球) 或 **Parallel Search**(为 LLM 优化、返回排序摘录)。网络结果一律回到 DOI/OpenAlex 核实元数据后才入表。

## 整理流程（不可省）
- **筛选**：相关度阈值，剔除明显跑题。综述类任务按 PRISMA 思想留痕：记录每个库的检索式与命中数 → 去重数 → 标题/摘要筛掉多少 → 全文筛掉多少 → 最终纳入，全程可复现。
- **去重**：跨库按 DOI 优先，无 DOI 按 arXiv id / 规范化标题+作者+年 归并。
- **分类**：按子方向/方法族/任务/时间分组。
- **可信度判断**：来源层级(顶刊顶会 > 普刊 > 预印本 > 博客)、被引量(注明来源库)、团队、是否同行评审、是否可复现。S2 的 `influentialCitationCount`/`tldr` 可辅助快筛，但属模型估计，不作硬证据。
- **重要性排序**：奠基/里程碑/SOTA/综述/最相关 优先。可用 OpenAlex `group_by` 出年度/期刊分布辅助判断热度与脉络。

## 可运行脚本（本目录 scripts/，均真 python 跑通、API 真 curl 记 HTTP 码）
> 无网络时所有脚本回退合成样本并打印 `[OFFLINE]`，保证管线可验证。
- `scripts/search_normalize.py`：urllib 直连 OpenAlex+Crossref**+DOAJ**（DOAJ 完全免 key、按相关度排序，补盲区；增量追踪 `--from-date` 时自动跳过 DOAJ 因其无日期过滤；`--no-doaj` 可关），还原 abstract_inverted_index，按 DOI 跨源去重归并，输出文献表 JSON+Markdown。**排序 `--sort`（治宽 query 顶跑题文的关键）**：默认 `relevance`（OpenAlex `sort=relevance_score:desc`、Crossref `sort=relevance`，去重后保留各源相关度序不按被引重排）——实测搜"dairy goat behaviour"前排全是对口的 Applied Animal Behaviour Science 行为论文；`--sort cited` 切回被引降序找高被引经典（旧默认行为，前排会是蹭词的超高被引跑题文，故仅在明确找经典时用）。
  `python scripts/search_normalize.py "dairy goat behavior" --per-page 10`（实测 OpenAlex=200 Crossref=200 DOAJ=200）。
  **定期追踪**：加 `--from-date YYYY-MM-DD`（只取该日后发表）+ `--known-dois 已读库.txt`（按 DOI 去重出新增）做增量重跑，协议见 references「文献定期追踪协议」。
  **时效优先 `--recency-boost`（要出成果须盯近几年相关工作）**：按"相关度×时效衰减"综合重排，近期相关文上浮、过老平庸文下沉，但**经典奠基文豁免**（被引同时过本批 top10% 分位且 ≥`--classic-min-cites` 绝对下限，默认 500，领域差异大可调——CS 调高、小众畜牧调低）不被时效压沉，避免漏掉该读的根。需配 `--current-year YYYY`（显式传不依赖系统时钟保可复现），`--half-life`（半衰期年数默认 4，越小越偏向最新）。每条留 `rerank_parts`（relevance/recency/is_classic）可复核。**与 `--from-date` 区别**：from-date 是硬截断只取新文（会漏经典）；recency-boost 是软加权（近期优先但不丢经典），二者按需选或组合。
  **相关度过滤（治宽 query 顶跑题文）**：`--require-terms a,b`（标题/摘要须全含，AND）/ `--exclude-terms x,y`（命中任一即剔）/ `--min-score 0.2`（标题×query 词重叠 Jaccard 截断）。剔掉的条目带 `drop_reason` 留痕进 JSON `dropped_records`（不静默丢弃，可人工复核）；每条附 `relevance_score`（启发式非真值）。宽主题检索务必加 require/exclude，否则纯被引排序会把高被引跑题文顶上来。**未加过滤时的自动护栏**：若前 5 条标题相关度均值 <0.1，输出 `[WARN]` + JSON `relevance_warning` 提示该收窄（不强改结果，只留痕提醒——治"忘了加过滤直接采信脏结果"）。
  **穷尽检索**：`--max-results N`（>per-page 才生效）用 OpenAlex/Crossref 的 `cursor=*` 深翻页取够 N 条，让"穷尽"深度档真可用（不再每源只一页）。
  **持久追踪库**：长期盯一个方向，把每轮检索 JSON 灌进 `scripts/tracker.py` 的 SQLite 库（`--ingest search.json --run 2026-06-13`），按 DOI（无 DOI 回退标题键）去重、记 new/seen/read 状态与被引快照随轮变化，`--new` 列本轮新增、`--export md` 导出——比 `--known-dois txt` 状态可留存、可查历史（借 paper-tracker）。
- `scripts/verify_citations.py`：**检索期轻量自检**（防幻觉 DOI 进文献表，非投稿终审——真实性/撤稿/嵌合/locator 终审在 m10 light-citation `verify_refs.py`，口径见「衔接」节）。DOI 内容协商回 Crossref/doi.org 核验元数据，比对标题相似度/年份/首作者，标 `VERIFIED/METADATA_MISMATCH/DOI_NOT_FOUND(疑似幻觉)/NO_DOI`。**无 DOI 条目**：先试 arXiv id 核验（打 export.arxiv.org，命中标 `ARXIV_VERIFIED` 并提示预印本未经同行评审），再按标题反查 Crossref 候选 DOI（`candidates` 按 title_sim 排序，给人工确认不自动采信），把纯人工占比降下来。
  `python scripts/verify_citations.py 10.1038/s41597-023-02555-8`（实测真 DOI=200、伪造 DOI=404）。
- `scripts/cn_journal_probe.py`：读 `assets/cn_core_issn.csv` 批量探 OpenAlex source 体量（id/works_count/cited_by）。11 个种子 ISSN 实测全 HTTP 200。
- `scripts/snowball.py`：引用滚雪球。给种子(DOI/OpenAlex workid/标题)做一/两跳邻居抓取——后向参考(OpenAlex `referenced_works` 批量回填 或 S2 `/paper/{id}/references`)、前向被引(OpenAlex `filter=cites:{workid}&sort=cited_by_count:desc` 或 S2 `/paper/{id}/citations`)；去重(复用 `_norm_doi`/`_norm_title`)、按被引降序、标边类型(参考/被引)与 `isInfluential`，导出 JSON+Markdown。一跳前后向都抓；两跳扩展数 `--expand-top N`（默认 3）、**方向 `--two-hop-direction`**（`backward` 追根溯源[默认,不增请求量]/`forward` 追前沿/`both` 全扩,后两者请求量更大）。`python scripts/snowball.py 10.1016/j.compag.2021.100001`(无网络走 [OFFLINE])。
- `scripts/biomedical_search.py`：**生医双源检索**（Europe PMC + PubMed E-utilities），兑现生医纪律。Europe PMC 免 key 直接返回 abstract/被引/开放标记；PubMed 两步式 `esearch→esummary`，**`term` 原样透传 MeSH 检索式**（`[MeSH Terms]`/`[tiab]`/`[ti]` 等字段限定由你写在 query 里）；跨源按 DOI 去重合并、标命中源。`python scripts/biomedical_search.py "goat lameness[MeSH Terms]" --source pubmed`。**注：本脚本不做"自由词→MeSH 主题词"自动映射（需接 NCBI MeSH 库，属 P2 增强）；MeSH 检索式需你按受控词写好透传。** key/email 经 `--api-key`/`--email` 或环境变量 `NCBI_API_KEY`/`NCBI_EMAIL` 传入。
- `scripts/arxiv_search.py`：**预印本检索**（arXiv + 可选 bioRxiv/medRxiv）。arXiv 解析 Atom XML，`search_query` 支持 `ti:/au:/abs:/cat:/all:`+布尔；bioRxiv/medRxiv 走**真实日期区间端点** `/details/{server}/{from}/{to}/{cursor}`（`--end-date YYYY-MM-DD` 往前推 `--days` 天，或 `--start-date`+`--end-date` 显式区间）+ cursor 翻页拉全区间，再**本地关键词过滤**标题/摘要（其 API 无服务端关键词检索，已如实标注；不传日期则回退拉最新一页），并读 `published` 字段标"是否已转正式发表"。`python scripts/arxiv_search.py "cancer" --source biorxiv --end-date 2026-06-14 --days 7`。预印本一律标 preprint、未经同行评审。
- `scripts/prisma_flow.py`：系统综述 PRISMA 2020 流程留痕与计数核对（**系统综述/Meta 分析专用**）。输入各阶段计数 JSON（各库命中/去重/标题摘要筛/全文按理由排除/最终纳入），脚本**勾稽核对**各阶段数字是否自洽（前阶段−排除=后阶段，抓出"凭空消失/多出"的算术错误，审稿人必查），并产出 PRISMA 流程图所需结构化数据 + 文字版流程供 m09 绘图、m07 写作。只核对计数自洽，不替你做筛选判断。`python scripts/prisma_flow.py --selftest`（含反例检测）/ `--counts counts.json --out prisma.json`。
- `scripts/pipeline.py`：**端到端编排**，把上面脚本串成一条龙——检索+相关度过滤→（可选）滚雪球→引用核验→（系统综述时）PRISMA 勾稽→汇总出 `literature_review.md` 骨架（文献表+核验摘要+待人工填的脉络/方法卡/gap 占位）。复用各脚本函数不重复实现，每步沿用其 [OFFLINE] 回退与诚实纪律，减少 agent 每次手工拼装。`python scripts/pipeline.py "dairy goat behavior" --require-terms goat --snowball --out review.md`。
- `scripts/cross_domain_search.py`：**跨领域正交双轴检索**（应用轴 × 方法轴），治"窄应用领域近三年好文稀少、但创新常靠跨领域嫁接前沿方法"的真实痛点（如用 CV 最新目标检测/Transformer 做病理识别、奶山羊行为识别）。**两轴分别检索分别排序**（`--application` 给你的领域、`--method` 给要迁移过来的前沿技术），方法轴强时效抓 SOTA、应用轴允许经典建 baseline——**不拼成一个 query**（实测拼词+被引排序会顶出 IPCC/Lancet 等通用高被引跑题文）。输出双栏文献表 + 迁移提示栏（每条方法轴前沿→你的应用的嫁接点，喂 m03）。**可迁移性由研究者判断，脚本只把两边候选找全找新、不臆断**。`python scripts/cross_domain_search.py --application "pathology image recognition" --method "vision transformer segmentation" --current-year 2026`。
- `assets/cn_core_issn.csv`：北大核心/CSCD 核心刊真实 ISSN 种子（已逐条 curl OpenAlex 核实）。
- `assets/litreview_template.md` + `assets/method_card.md`：综述+方法卡填空骨架（6 件套）。
- `examples/worked_example_dairy_goat.md`：端到端 PICO→query→命中→去重→筛选→核验 留痕实例。

## 论文重要性量化判级（年龄 × 被引）
被引数先注明来源库（OpenAlex/Crossref/S2 口径不同不可直接比）；用**年均被引 = 被引 / max(1, 当年-发表年)** 抹平年龄，再结合绝对量与角色判级。下表为经验阈值（领域差异大，CS/生医偏高、小众畜牧/人文偏低，按子领域校准）：

| 角色 | 年龄 | 典型被引/年均被引特征 | 判定信号 |
|------|------|---------------------|---------|
| 奠基(Foundational) | ≥8 年 | 累计被引极高（领域 top 1%），年均仍 ≥50 | 被后续方法普遍引为出发点、开创问题/范式 |
| 里程碑(Milestone) | 3–8 年 | 年均被引 ≥30，进入子领域 top | 提出被广泛复用的方法族/数据集/基准 |
| SOTA / 新锐 | ≤3 年 | 绝对被引未必高，但年均增速快、刷榜 | leaderboard 居前、被最新工作密集引用 |
| 综述(Survey) | 任意 | 被引高但属二手 | 适合快速建脉络，不作原创性硬证据 |
| 最相关(Most-relevant) | 任意 | 被引可低 | 与本课题问题/数据/方法最贴合，优先精读 |
| 长尾/存疑 | 任意 | 年均被引 <1 且非新作 | 谨慎采信，核查是否同行评审/可复现 |

用 OpenAlex `group_by=publication_year` 出年度分布辅助看热度拐点；新作低被引≠不重要（看增速与 venue 等级）。

## 标准产出
1. 文献表（字段：标题、作者、年份、venue、级别、核心贡献、方法、数据集、被引、链接、可信度、相关度）。
2. 研究脉络（时间线 + 演进逻辑：问题怎么提出→怎么被解决→还剩什么）。
3. 代表性方法卡（见 db03 method_card 字段）。
4. 优缺点对比表。
5. 可复用资源清单（开源库、数据集、模板、leaderboard，含许可协议）。
6. 空白与机会（current gap，直接喂给 m03）。

**标准工件**：上述综合落盘为 `docs/literature_review.md`（交 m03/m04/m07/m10 的交接工件，命名见 CONVENTIONS §6.1）。

## 合规
受版权全文不下载；只存元数据/链接/摘要/笔记/引用关系（见 CONVENTIONS §5）。所有条目给可核查来源，不臆造 DOI。检索式与端点参数若未当场核校，标注"需核查"再用。浏览器取数遵守目标站 robots/ToS。

## 衔接
结果写入 db01/db03/db04 与项目库 db09（写入 db01 venue 行时落 `oa_id=`/`issn=`/`domain_scope=`/`if_kind=` 锚点子串 + `last_checked_date`，口径见 db01 references.md §1，便于后续 `venue_signal.py --batch` 实时复查）；gap 交给 m03 idea-generation。文献表入库后建议交 light-citation 做引用核查，规避幻觉引用。
`scripts/cross_domain_search.py` 的"迁移提示"专喂 **m03 idea-generation 的 method-transfer 型 idea**（A 领域方法迁 B 领域）——m03「新颖性核验」节已登记调用本脚本做正向方法发现，双向声明对齐。`scripts/snowball.py` 与 `search_normalize.py` 则供 m03 做"核心撞车反向核验"。
长期项目可在 db09 项目目录建 `literature/`（保存检索式+已读库 DOI），按"文献定期追踪协议"（见 references）周期增量重跑，持续盯方向新文献。

---
具体工具/API 的真实端点、参数、限流与已知坑见同目录 `references.md`。
