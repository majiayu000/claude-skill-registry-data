---
name: light-venue-matching
description: 投稿定位与期刊/会议匹配。当用户问投哪个期刊/会议、要评估录用可能性/录用概率、做投稿规划时使用。根据论文质量、方向、创新程度、实验完整性、语言水平、作者背景和预算，推荐中文/英文期刊、SCI/SSCI/EI/CCF/核心、国际/国内会议。分析投稿难度、方向匹配度、审稿周期、版面费、以可核查信号做录用可能性定性分级(高/中/低,不编百分比)、是否适合本科生/弱导师资源、预警风险，给出冲刺/稳妥/保底分层选择。
---

# 投稿定位与 venue 匹配

## 评估输入（先盘点实力）
论文质量(创新/实验完整性/理论深度)、研究方向、语言水平、作者背景(本科/硕博、是否有强导师)、时间需求(deadline/毕业要求)、预算(能否付 APC)、目标(毕业/评奖/找工作/纯发表)。

## 匹配流程
1. 用 db01 期刊会议库按方向(subject_area)筛候选；不足时按方向程序化扩候选：OpenAlex Sources `GET https://api.openalex.org/sources?filter=topics.id:<方向>,is_oa:<bool>&sort=cited_by_count:desc&per_page=50&mailto=<email>`（游标 `cursor=*` 翻页，可按 `summary_stats.2yr_mean_citedness`/`apc_usd`/`is_in_doaj` 过滤）；计算机方向直接对 CCF 目录按"领域+目标档(A/B/C)"取候选。**db01 是薄缓存**（事实字段为快照+`last_checked_date`+`oa_id=`/`issn=`锚点，见 db01 references.md §1）：先按用户方向用 `domain_scope=` 子串过滤——非 CS 用户隐藏 `中国CS`(CCF) 档、投国际刊用户隐藏 `中国语境`(中科院分区) 档，避免偏科误导；subject_area 按 references.md §3 受控大方向归一后再筛。
   - **db01 为空/无目标方向行时的冷启动（别卡在第一步）**：不依赖 db01 也能跑——① 用上面 OpenAlex Sources API 按方向现拉候选刊（拿 `display_name`/`issn`/`apc_usd`/`2yr_mean_citedness`/`is_in_doaj`）；② 每个候选现建一张**临时卡**填以下最小种子字段，跑完本流程后可回写 db01 沉淀：
     ```
     venue_name, venue_type(journal/conference), issn 或 oa_id, subject_area(按 §3 归一),
     ccf_rank 或 jcr_quartile(查到才填,否则待核查), apc_fee(币种+来源), review_cycle(周,来源),
     is_oa, is_in_doaj, domain_scope(中国CS/中国语境/通用), last_checked_date, source_url
     ```
     缺的字段标"待核查"不臆造；CS 方向无 db01 时直接查 CCF 目录官网。临时卡口径与 db01 venues.csv 一致，便于回填。
2. 按论文实力对齐 venue 级别——不只推"高大上"。给学生用"档位"(CCF A/B/C、中科院分区、北大核心/CSSCI)而非裸 IF。
3. 对每个候选填**统一对比字段**（抓取来源见括号）：
   - 影响指标：IF + JCR 分区(JCR/LetPub)、CiteScore + 分位(Scopus)、SJR/Eigenfactor 声望(Scimago/IEEE)、中科院分区大类/小类(分区表/LetPub)。**db01 的 impact_factor 看 `if_kind=` 口径**：`jcr`=真 JCR 权威快照(仅少数行,带 LetPub journalid)；`proxy`=OpenAlex 2yr 代理值，**禁当 JCR 真值引用**，真 JCR/分区须查 Clarivate/LetPub 付费源；`na`=会议无 IF。代理值与在线冲突时信在线(`venue_signal.py` 已附在线 2yr 供交叉验证)。
   - 档位：CCF A/B/C、北大核心/CSSCI/CSCD 命中情况。
   - 周期：首次决定时长 + 投稿到发表周数(JournalFinder/IEEE Recommender/LetPub)。
   - 费用与 OA：APC、是否 OA、是否 DOAJ 收录(DOAJ API `GET /api/v3/search/journals/issn:<ISSN>`)。
   - 录用可能性与背景：**官方公开接收率**(仅在该刊/会官网或正式报告披露时填具体数字并附链接，否则填"待核查—无官方公开数据")、国人发文占比(LetPub，标注为社区经验估计)、自引率、是否适合作者背景、模板与引用格式(reference_style)。**不抓取、不填写 LetPub 的"录用比例"作为概率数字**（其自承为社区投稿经验估计，非官方统计），只用下方 rubric 做定性分级。
   - 收录核查：是否被 WoS 收录及索引(SCIE/SSCI/AHCI/ESCI，查 Master Journal List)、是否被 Scopus 收录。
   **三套分区(JCR/SJR/中科院)口径不同，每项必须标来源+年份，不可混用。**
4. **预警筛查（白名单+黑名单双向）**：
   - 白名单正面信号：被 DOAJ 收录(尤其有 DOAJ Seal)、被 WoS/Scopus 正规索引。
   - 黑名单/掠夺特征：命中《中科院国际期刊预警名单》(高/中风险)，或异常自引、超快审稿、年发文激增、国人发文占比畸高、高额 APC、虚假指标。命中即标红劝退（联动 a10）。

## 分层推荐（必给三档）
- **冲刺**：够一够可能中，回报高。
- **稳妥**：实力匹配，大概率中。
- **保底**：确保能发/能毕业。
每档给 1–3 个，附理由、**录用可能性定性分级(高/中/低，见下方 rubric，不编百分比)**、周期、费用、风险。

## 录用可能性评估 rubric（定性分级，禁编概率数字）
**铁律**：除非该刊/会官网或正式报告公开了接收率(acceptance rate)且能附链接，否则**绝不给出精确录用概率/百分比**。LetPub 等聚合站的"录用比例"是社区投稿经验估计、非官方统计，**不得当作概率数字引用**。最终只输出"高/中/低 + 逐条理由"的定性分级。

### 五个可核查信号（逐项打分，每项 高/中/低，并标来源）
1. **作者相对实力**：作者近 5 年 h-index / 代表作被引（OpenAlex Authors `GET https://api.openalex.org/authors?search=<姓名>&mailto=<email>`，取 `summary_stats.h_index`）对比该 venue 的 `summary_stats.h_index`（db01 已存或 OpenAlex Sources 查）。作者影响力接近/超过该刊典型作者→高；明显低于→低。注：h-index 同名需用机构/ORCID 排歧，标"待核查"不强行认定。
2. **方向匹配度**：论文主题与该 venue 的 `subject_area`(db01) 及近年 `representative_papers`(db01 字段) 的主题重合度。核心主题命中→高；擦边/跨界→中；明显偏离该刊 scope→低。
3. **方法/数据规模匹配**：论文用的方法、数据集规模、实验体量是否达到该 venue representative_papers 体现的门槛（如顶会常要大规模实验+SOTA 对比；领域刊看是否有该刊偏好的方法范式）。达标→高；部分达标→中；明显不足→低。
4. **官方接收率档位**：仅当有官方公开接收率时按数值定档（如 <15% 记为竞争极高、15–30% 高、>30% 中）；**无官方数据则该项填"待核查—无官方接收率"，不参与编数**，并在结论里说明该项缺失。
5. **创新性自评**：让作者/评估者按"增量改进 / 显著改进 / 新问题或新范式"三档自评，对照该 venue 档位（顶会/顶刊偏好后两档）。这是主观项，须显式标注"作者自评，非客观指标"。

### 汇总规则
- 五项多数为"高"且无致命短板（方向/方法不达标算致命）→ 总评 **高（稳妥/保底候选）**。
- 信号互有高低、存在 1 项致命短板 → 总评 **中（冲刺候选，说明短板）**。
- 方向或方法明显不达标，或作者实力远低于该刊 → 总评 **低（不建议或仅作保底外的备选）**。
- 输出格式示例见下"产出"第 1 项；每条分级后必须跟"因为…(引哪个信号+来源)"，不得只给结论。

## 工具/数据视角（各司其职，别混口径）
- **程序化拉候选/元数据**：OpenAlex Sources（免费 REST，`api.openalex.org/sources`，按 ISSN/topic/OA/APC/h-index 过滤，cursor 翻页，加 `mailto` 进礼貌池）。
- **影响指标**：JCR(JIF，2 年窗，现 1 位小数，2024 起 SCIE+SSCI+ESCI 统一排名，需订阅) ｜ Scopus CiteScore(4 年窗、分母含会议/综述，免费) ｜ Scimago SJR(类 PageRank 声望加权，Scopus 数据，门户可下 Excel) ｜ Eigenfactor/Article Influence(IEEE Recommender 内置)。
- **收录核查**：WoS Master Journal List(免费查是否收录 + SCIE/SSCI/AHCI/ESCI) ｜ Scopus Source List ｜ **EI 核查**：权威源 = Engineering Village 官方 **Compendex Source List**（从产品页 "View source list" 现取当期 Excel，按刊名/ISSN 查；严禁引过期第三方"EI 源刊"站），详见 references.md「EI 核查路径」。
- **国内会议正规性**：CCF 目录(计算机)定档 + 一级学会官网核主办方 + 出版检索去向复核；假会议三红线(交钱包录/检索承诺无出处/主办方冒名)，详见 references.md「国内会议信号源」。
- **国内档位**：CCF A/B/C 目录(计算机十大领域) ｜ 中科院分区(大类/小类，1 区约前 5%，附预警名单) ｜ 北大核心(中文核心，约 4 年一版) ｜ CSSCI(南大核心，社科) ｜ CSCD(理工)。
- **稿件-期刊匹配工具**(只发现候选，有出版商偏向)：Elsevier JournalFinder、Springer Journal Suggester、IEEE Publication Recommender——输入题目/摘要，返回同社旗下刊 + 周期/接受率/APC/OA。
- **一站查中国友好画像**：LetPub(IF/JCR 分区/中科院分区/审稿周期/录用率/国人占比/APC/预警 一处看，但关键值回官方二次核实)。
- **OA 合规**：DOAJ(免费 API `doaj.org/api/v3/search/journals/{query}`，收录=正面信号，有 Seal 更佳)。

db01 是薄缓存：事实字段为快照，每条标 `last_checked_date`，投前用 `venue_signal.py` 实时复查，**冲突默认信在线**（例外：`if_kind=jcr` 的真 JCR 值 OpenAlex 查不到，本地快照即权威，不被代理值覆盖）；`reference_style` → LaTeX cls/bst 映射与 subject_area 归一表见 db01 references.md。具体端点/参数/坑见本技能 references.md。

## 脚本：五信号对照查询（`scripts/venue_signal.py`）
评估一个候选 venue 时，先跑本脚本拿五信号对照 JSON，再据此填对比表的可核查信号列——比手查更快且口径统一：
```bash
# 期刊 + 作者：五信号全开（作者匹配度需 --author）
python scripts/venue_signal.py --issn 1234-5678 --author "Zhang San" --venues-csv <db01路径>/venues.csv
# 仅期刊：信号1/2/5（审稿周期/分区从 db01 卡取）
python scripts/venue_signal.py --issn 1234-5678 --card-fields review_cycle="约8周" apc_fee="1800 USD" cas_quartile="2区"
```
- 输出五信号：①发文量趋势(counts_by_year)②自引率粗查(**外向 outgoing**，本刊引本刊比例)③审稿周期(db01 卡)④作者与该刊主题重叠⑤APC 与分区(db01 卡+OpenAlex)+ 白名单 DOAJ。
- **每信号独立降级**：取数失败标 `status:"unavailable"`+reason，不编数；能查多少出多少。
- **最低可评估门槛**：`summary.signals_ok < 2` 时只给"数据不足，暂不下定性结论"（防数据稀疏退化成主观硬凑）；补 --issn/--author 或换有 OpenAlex 覆盖的刊再评。
- **脚本信号 ≠ 完整评估**：`summary.rubric_coverage` 显式列脚本可程序化覆盖维度 vs 仍须人工维度（真实接收率/创新性与刊调性匹配/incoming 自引率/口碑）——跑完脚本不等于完成 venue 评估，别把信号当结论。
- **作者匹配度**按姓名取首个命中、未排歧，输出带 `disambiguation_caveat`，须 ORCID/机构二次确认，对应 rubric「作者相对实力」的 h-index 同名排歧纪律。
- 自引率是**外向(outgoing)自引粗估**（非官方入向 incoming 期刊自引率，两者口径不同）：输出标 `self_ref_direction`+`threshold_note`，**25%/40% 仅作参考提示非掠夺判据**（综述刊/窄领域刊 outgoing 天然偏高），掠夺判定须看 incoming+领域+预警名单（联动 a10），不可仅凭 outgoing 单独劝退。
- **DOAJ 白名单核查**：输出 `whitelist.doaj`（直查 doaj.org 官方库，免 key）——`in_doaj`(True/False/None)、`doaj_hits`、`doaj_seal`；与 OpenAlex 的 `is_in_doaj` 并列做交叉确认（OpenAlex 标志可能滞后）。**查询失败标 `in_doaj:None`+unavailable，绝不当成"未被收录"**；DOAJ 未收录可能只是非 OA 刊，勿单独据此劝退。喂预警筛查白名单环节。
- OpenAlex 接入口径（key/限流/计费）见 m01 references「OpenAlex 接入真相源」节，脚本不复写数字。

## 产出
1. 候选 venue 对比表（含上述字段 + 推荐档位 + **录用可能性定性分级**）。表骨架见 `templates/venue_compare_table.md`，填表即可保证字段不漏列、口径统一。分级列写法举例：
   `中｜方向匹配=高(主题命中CVPR scope,db01 subject_area=计算机视觉);作者实力=中(作者h-index=18 vs 该会代表作者多>40,OpenAlex Authors);方法规模=中(单数据集,顶会偏好多数据集SOTA);官方接收率=待核查(CVPR官网未稳定公开逐年录用率);创新性=作者自评"显著改进"(主观)`
   —— 注意：**全程无百分比**，"待核查"如实保留。
2. 投稿策略建议（先投哪、被拒后转投顺序）。
3. 风险提示（预警/周期长/费用高/匿名要求）。

## 转投顺序：可执行排序规则（不靠拍脑袋）
> **方向匹配度量化（借 journal_targeter 的 suitability 思路）**：上面"方向匹配度 高/中/低"可落成**可解释相似度**而非拍脑袋——用 venue_signal 信号④（作者/论文主题与该刊近年发文的 OpenAlex topics 重叠度）+ 标题/摘要关键词与该刊 scope 的词重叠，给每个候选一个 0-1 匹配分 + **列出命中/缺失的主题词**（可解释，便于人工复核为何这个刊更配）。匹配分是启发式参考非真值，最终人工定。
被拒后从候选池里选下一个投哪——按以下**字典序**对剩余候选排序，逐条取下一个，而非凭感觉：

1. **方向匹配度 ↓**（高>中>低）：scope 越贴合越优先，错配重投是浪费周期。来源：db01 `subject_area` 命中 / OpenAlex 作者主题重叠（venue_signal 信号4）。
2. **录用可能性信号 ↓**（高>中>低）：用五信号汇总档位，不是百分比。被高档拒了就往下一档走，别原地平移同档。
3. **审稿周期 ↑**（短>长）：同档同匹配时，周期短的先投（毕业/deadline 敏感者尤甚）。来源：db01 `review_cycle`。
4. **APC ↑**（低>高）：预算敏感（本科生/无经费）时此项权重前移；有经费可下调优先级。来源：db01 `apc_fee`。
5. **预警状态**：命中中科院预警名单/掠夺特征的**直接剔除候选池**，不参与排序（联动 a10）。

实操：被拒后回本技能，对剩余候选按上述键排序给 fallback 链（如 `A刊(稳)→B刊(稳)→C会(保)`），并标明每步的降档理由。**按拒稿原因调权**：若被拒理由是"scope 不符"→ 方向匹配权重再加强；若是"创新性不足/被审稿人比下去"→ 整体降一档投，别在同档硬刚。降档与剔除都写进决策记录入 db09。

## 衔接
选定后 → m12 套对应模板、m10 调引用格式；投稿记录与决策入 db09；被拒后转投时回本技能重排。所有期刊数据投前重新核查(CONVENTIONS §1)。**db09 是 venue_signal.py 的下游消费方**:db09 decision_log/project_card 内嵌的 venue 计量值为带 last_checked 的快照,投前用 `venue_signal.py --issn` 重核、冲突信在线,口径互指不复写。

> 工具真实端点/参数/已知坑详见同目录 references.md。
