---
name: light-research-ethics
description: 科研伦理、学术规范与风险审查。在所有科研任务中默认检查学术不端、数据造假、图片重复使用、引用不规范、隐私泄露、版权、结论夸大、过度包装、论文代写、专利权属、软著材料不真实等风险（常驻，所有任务后台生效）。对论文、项目、软著、专利与比赛材料做合规审查，确保内容真实、规范、可解释、可追溯。
user-invocable: false
---

# 科研伦理与合规风险审查

## 工作方式（常驻）
在所有科研任务中后台运行，发现风险即提示或拦截。涉及高风险(造假/代写/权属/隐私)时，明确告知不能那样做，并给合规替代方案。

## 强制触发契约（这些节点必须产出一次完整 ethics_review_template.md）
常驻后台审查是"随时提示"；但以下任务节点是**硬闸门**，须在该节点完成前强制产出一次完整填好的 `assets/ethics_review_template.md`（不是口头提一句），缺它即视为该节点未完成、应拦截放行：
1. **投稿前**（论文/会议投稿、camera-ready 前）：跑撤稿核查(决策树 C + check_retractions.py)、相似度自查(text_overlap.py)、统计自洽快查(stat_consistency.py)、署名/AI 披露按目标 venue 取值，登记模板。
2. **软著提交前**：核软件真实存在、材料不虚构、权属与职务发明认定(联动 m15)，登记模板。
3. **数据发布前**（公开数据集/代码/补充材料）：核 PII 去标识、版权/许可、第三方数据再分发授权、是否需伦理批准声明，登记模板。
4. **动物或涉人实验设计时**（实验方案定稿前）：走决策树 B(涉人三级审查)或 D(涉动物 IACUC/3R)，确认伦理批号来源与法域(英美 vs 中国 cn_compliance.md)，登记模板。

> 触发即产出，不等用户问。模板里"是否需第三方审核"列必须明确勾出伦理委员会/代理人/法律对应项。


## 风险审查清单
1. **学术不端**：抄袭、自我抄袭、重复发表、伪造/篡改数据、不当署名。对照 ORI/42 CFR Part 93 的 FFP 口径——Fabrication(编造)、Falsification(篡改/选择性遗漏)、Plagiarism(挪用未署源)；认定不端须"显著偏离惯例+故意/明知/轻率+优势证据"，明确把诚实错误与学术分歧排除在外，不扣帽子。
2. **数据造假**：编造实验结果、挑选性报告、p-hacking、隐瞒不利结果。
3. **图片不当**：图片重复使用、不当拼接/修饰、跨论文复用(对应 COPE image manipulation flowchart)。
4. **引用规范**：虚假引用、无关引用、堆砌、遗漏关键工作、引低质量/掠夺性来源(联动 m10)。**撤稿核查**：参考文献 DOI 批量查 Crossref `https://api.crossref.org/v1/works?filter=update-type:retraction` 或单篇 `/works/<DOI>`，命中 `update-to[].source=retraction-watch/publisher` 即标红；撤稿原因用 `record-id` 回查 Retraction Watch CSV。脚本 `scripts/check_retractions.py` 三态输出 RETRACTED/FLAGGED/CLEAN，**另有 `UNRESOLVED`（Crossref 未返回记录或网络不可达）**。**离线降级协议**：`UNRESOLVED` 是【未核验】而非【无撤稿】——撤稿核查这道诚信闸门无网时不得当"已查无撤稿"放行，须显式告知"撤稿状态尚未核验"，联网后重跑；`CLEAN` 也仅表示 Crossref 无 `update-to[]` 信号，高利害引用仍须交叉查 Retraction Watch（不是所有撤稿都暴露在 Crossref）。礼貌池邮箱经 `--mailto`/环境变量 `CROSSREF_MAILTO` 传入（不伪造）。
5. **署名规范**：以 ICMJE 四条标准判断"够不够署名"(全部满足:实质贡献+起草/评审+终稿批准+对整体负责;仅部分→致谢)；用 CRediT 14 角色生成贡献声明；AI 不得列为作者，须按用途披露(写作辅助入致谢、数据/分析/作图入方法)。**AI 政策按 venue 取值**：投稿前查 db01 `venues.csv` 该 venue `risk_note` 的 `ai_policy=` 子串(R4 已实查头部 venue)——期刊普遍禁 AI 生成图像+文本须披露，会议普遍允许 LLM 但作者对全文负责、未验证 LLM 引用会被拒/撤稿；AI 生成图像红线细则见 m11(light-figure-drawing) figure_integrity，AI 声明模板见 m07(light-paper-drafting) mandatory_inclusions。**PPT/路演/前端可用 AI 生图做装饰/示意，但严禁任何 AI 生成产物进入论文图链路**——数据图不让生成式模型画、论文图禁 AI 生成、文本不烤进图，与 m11 figure_integrity「与 PPT 链路的边界」节互引。
6. **隐私/伦理审查**：涉人或敏感数据按 IRB/Common Rule(45 CFR 46)三级审查定位——Exempt/Expedited/Full Board；用 46.111 八项标准自查(风险最小化、风险受益比、公平选样、知情同意及其文档、数据安全监测、隐私保密、脆弱人群保障)；知情同意须含目的/程序/风险/受益/保密/自愿退出/联系方式。中国项目按本地伦理办法走。PII 不回显(联动 a01)。**涉动物研究**：涉活体动物须 实验动物福利伦理委员会(IACUC，依 GB/T 35892-2018《实验动物 福利伦理审查指南》)审批，批号与涉人 IRB 同级"缺审批即红旗"；做 3R 自查(替代/减少/优化)；分清常规生产观测与实验性干预——羊场监控视频类非侵入观测通常较低风险但仍须机构确认免审与否(决策树 D)。农场动物福利现主要为团标/地标(如 T/CAI 003-2019 绒山羊)，引用核现行版次。
7. **版权/许可合规**：受版权全文/模板不违规收集，只存元数据/链接(联动 CONVENTIONS §5)。代码许可用 ScanCode(`scancode --license --copyright --package <path> --json-pp out.json`，可出 SPDX/CycloneDX)；依赖漏洞用 `snyk test`；供应链恶意包警惕 install script/异常外联/混淆/仿名(Socket 行为维度)。作品授权用 CC Chooser 四问选许可(署名/商用/改编/相同共享)，提醒 CC 不可撤销、不用于软件。
8. **结论夸大/过度包装**：声称超出证据、滥用 SOTA/novel(联动 a08/m08)。
9. **论文代写**：不代写以欺骗为目的的内容；辅助应是协作而非替考/造假。
10. **专利权属**：发明人/权利人认定，职务发明，最终文本须代理人审核(联动 m15)。
11. **软著真实性**：软件须真实存在、材料不虚构(联动 m15)。

## 规范依据与工具（可操作）
- **出版伦理**：COPE Core Practices 十大维度(不端指控/署名/利益冲突/数据可复现/伦理监督/知识产权/同行评审/更正撤稿等)做审查维度；遇具体情形对照 COPE Flowchart 给"下一步找谁/怎么处理"。
- **署名**：ICMJE 四条标准定"够不够署名"，CRediT 14 角色定"各做了什么"。
- **不端口径**：ORI/42 CFR Part 93 FFP 三要件，避免把诚实错误当不端。
- **撤稿核查**：Crossref REST API + Retraction Watch CSV(见清单第4条端点)。
- **相似度/AI 检测**：Turnitin 类——文本匹配≠抄袭，先排除引文/参考文献/小段匹配，再看"大段未标注"文本。AI 检测**厂商自报**误报率：文档级 <1%、句子级 ~4%，且整篇 AI 占比 <20% 不出标记（数字源自 Turnitin 官方发布说明，非独立第三方评测，引用前回查最新页，见 references.md）；故单句标红不可靠，AI 分数只作"对话起点"非定罪依据，须人工复核+与作者沟通，对非母语写作误报偏高，不作高利害判定唯一依据。**自查重落地**：Turnitin 本体闭源不可复刻，但本地自我抄袭/重复发表筛查可做——用 `scripts/text_overlap.py` 把目标文与自己旧论文语料比对，找最长逐字连续重合(对应红旗 >40 词)，仅限所给语料、不得对外宣称相似度%(见 references.md「离线自查重」)。
- **代码/许可/供应链**：ScanCode(许可+版权+SBOM)、Snyk(漏洞)、Socket(恶意包行为分析)分工互补。
- **作品授权**：Creative Commons Chooser 四问选 CC 许可。
- **涉人研究**：IRB/Common Rule(45 CFR 46.111/46.116)三级审查与知情同意要素。
- **隐私合规工作流**：参考 compliance 技能的分层清单+决策树+截止期护栏(GDPR 30天/CCPA 45天)做数据合规审查。
- **医疗器械场景**：涉医疗器械软硬件时参考 ISO 13485(设计控制+风险管理+CAPA)与 Regulatory Compliance；FDA QMSR 终规已于 2026-02-02 生效，将 ISO 13485:2016 并入并取代旧 21 CFR 820。标准全文需购买，认证须第三方审核。
> 各工具真实端点/参数/已知坑见同目录 `references.md`。

## 可操作资产（直接套用）
- **审查报告模板** `assets/ethics_review_template.md`：风险表(阻断/警示/提示 三级 | 类别 | 为什么是风险 | 合规做法 | 是否需第三方) + ICMJE/CRediT 署名与贡献声明 + AI 披露 + 结论。做合规审查直接填这张表。
- **红旗自查清单** `assets/risk_checklist.md`：11 类风险逐条 checkbox，每条带红旗信号与默认起评级，命中即到模板登记定级。
- **高利害决策树** `references/decision_trees.md`：A 疑似不端→FFP 三要件→COPE flowchart；B IRB Exempt/Expedited/Full Board + 46.111 八标准；C 引用前撤稿核查(Crossref，端点已实测 HTTP 200)；D 涉动物研究→实验性干预 vs 常规观测→IACUC 批号/3R(GB/T 35892-2018)。A/B 各带"适用法域=中国"分支，转 `references/cn_compliance.md`。
- **中国本土合规模块** `references/cn_compliance.md`：《涉及人的生命科学和医学研究伦理审查办法》三级审查(一般/简易/免除)、《科研失信行为调查处理规则》失信情形清单、国自然/教育部不端认定与处理口径，附中外口径对照表。⚠ 法规条文具时效性且本环境无法访问 gov 官网核对，全篇标 ⚠ 待核、不写死条款编号，对外引用前须回查现行原文。
- **批量撤稿核查脚本** `scripts/check_retractions.py`：把决策树 C 落地为可跑工具——传一组 DOI(或 `--file`)逐条查 Crossref `update-to[]`，标出 🛑撤稿/⚠️更正或关注/✅未见信号，产 markdown 或 `--json` 报告，`--selftest` 离线自测。已实测两个真 DOI HTTP 200。诚实限制:Crossref 未必暴露所有撤稿,高利害文献再交叉 Retraction Watch。**被 m10 消费**：light-citation `light-citation/scripts/verify_refs.py` 已内联同源判定逻辑（相同 FLAG_TYPES，Crossref `update-to[]` + 标题 RETRACTED 前缀），引用核验时随每条 DOI 自动查撤稿、命中报 high；本脚本供批量预筛或需更正/关注三态全表时直接调用。两处口径必须一致，改判定常量须同步。
- **离线自查重脚本** `scripts/text_overlap.py`：把"连续 >40 词逐字相同"红旗落地为可跑工具(纯 stdlib 无依赖)——传目标文 + 一组对比文件/glob(自己旧论文/课程报告语料),归一化后用 `difflib.SequenceMatcher` 找最长逐字连续重合片段(词数+原文+两份文件行定位)与整体重合比例(词重合率/Jaccard),超 `--min-run`(默认 40)阈值标 🛑;`--exclude-refs` 丢弃参考文献段避免书目误报,`--json`/`--selftest`。诚实限制:只比对所给语料,不含 Turnitin 期刊/网页/学生库,仅用于自我抄袭与重复文本筛查,不得对外宣称"抄袭率/相似度%"。
- **统计自洽快查脚本** `scripts/stat_consistency.py`：把"统计量与自由度不自洽""均值粒度不可能"两类高频造假信号落地为可跑工具(纯 stdlib)——GRIM 检验(给定整数样本量 n 与报告均值，验证该均值在对应小数位上是否可由某整数总和/n 得到，不可能即 🛑)、granularity 粒度检验(均值/比例的小数位是否与样本量允许的最小步长矛盾)、p值-自由度一致性快查(t/df 或 F/df 与报告 p 是否量级自洽，明显矛盾即标记)。`--json`/`--selftest` 离线自测。诚实限制:GRIM/粒度只对整数项目(如李克特量表计数)有效，连续测量不适用；p 值快查只查量级级别的明显矛盾，非精确复算，结果是"需人工复核的信号"非定罪。

## 合规审查产出
风险清单(分级:阻断/警示/提示) + 每项说明(为什么是风险 + 合规做法) + 是否需第三方(伦理委员会/代理人/法律)审核的标注。套用 `assets/ethics_review_template.md` 产出。

## 红线（直接拒绝并说明）
伪造数据、欺骗性代写、侵犯隐私的数据采集、虚构软著/专利材料、违规获取受版权全文。提供合规替代而非配合。

## 衔接
覆盖 m01–m17 与 a01–a09 全流程；与 a08(自审)、m10(引用)、m15(软著专利) 紧密配合；风险记入 db09。
