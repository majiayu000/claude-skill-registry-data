---
name: dyz-med-screening-pipeline
description: >-
  管理系统综述、Meta 分析或范围综述从检索导入、保守去重、标题摘要与全文筛选，到研究/报告关联、数据提取
  和 PRISMA 计数的可审计证据链。当用户要执行文献筛选、记录纳排理由或准备证据合成输入时使用；研究问题与
  方案设计不是本技能的主要任务，流程图交给 dyz-med-flowchart，原始研究数据统计与合并模型交给 dyz-med-analyze。
  Use for systematic review and meta-analysis screening, extraction and PRISMA counts.
---

# 系统综述与范围综述筛选管线

## 核心原则

1. 方案控制筛选；任何方案修订都保留版本、日期、理由以及是否已看到筛选或结果数据。
2. 保存原始导出和检索日志。标准化、去重和筛选只生成派生文件，不覆盖原始记录。
3. 每个 PRISMA 数字必须能从行级记录或事件日志重建，不能凭记忆填写。
4. 区分 `record`、`report` 和 `study`；一项研究可能有多条记录和多份报告。
5. AI 可辅助排序或建议，但不能假装成第二名独立人工审查者。人工决定、冲突和裁决者分别记录。
6. 只有实际获取并核对的全文才能支持纳排和数据提取；不编造摘要、全文状态或数值。
7. 本技能不生成合并效应。把已验证提取数据交给获批的统计分析流程。

## 开始前确认

至少记录：

- 综述类型、研究问题、目标和 PICO/PCC；
- 纳入/排除标准及其操作化定义；
- 信息来源、平台、时间范围、语言和发布日期限制；
- 主要/次要结局或范围综述 charting 字段；
- 标题摘要、全文和提取的审查者安排及冲突解决；
- 注册/方案位置，或未注册的如实说明；
- 自动化工具的角色、人工复核点和数据隐私要求。

若方案仍不完整，生成 `protocol-check.md` 列出缺项。用户决定先开始时，记录为方案偏离；以后修订标准时不要
覆盖旧版本，也不要把事后修改写成预设。

## 工作流

### 1. 记录检索与导入

接收数据库和其他来源的原始导出，如 RIS、NBIB、BibTeX、CSV、XML 或平台原生格式。每个来源记录：

```text
数据库/平台 | 接口 | 完整检索式 | 检索日期 | 覆盖时间
命中数 | 导出格式 | 原始文件 | 文件哈希 | 限制条件
```

网页发现、引文追踪和无法复现的检索必须单列来源与方法；不要把公开网页发现称为对 CNKI、Embase 等数据库的
完整结构化检索。

### 2. 标准化并保守去重

派生一个规范化记录表，保留原始来源行号和原始标识。优先标准化：

- DOI、PMID、注册号和其他稳定 ID；
- 标题、作者、年份、期刊和摘要；
- 来源、导出文件、来源记录 ID 和导入批次。

去重规则：

- 完全一致的稳定 ID 可建立高置信重复组；
- 标题/作者/年份的模糊匹配只标为候选，需人工确认；
- 不删除原始记录，保留 `duplicate_of`、判定依据和审查者；
- 区分真正重复、同一研究的不同报告、会议摘要与全文更新。

### 3. 标题摘要筛选

每个规范化记录一行，至少包含：

```text
record_id, title, abstract
reviewer_1_decision, reviewer_1_reason
reviewer_2_decision, reviewer_2_reason
consensus_decision, adjudicator, conflict_status
protocol_version, screened_at
```

决策使用 `include`、`exclude` 或 `uncertain`。信息不足时进入全文，不因“可能不符合”过早排除。AI 建议放在
独立字段，不能复制为两名审查者的决定。

### 4. 全文获取与筛选

为每份待获取报告建立一行：

```text
report_id, citation
full_text_status, full_text_path_or_url
decision, primary_exclusion_reason, reason_detail
reviewers, adjudicator, protocol_version, decided_at
```

- `not_retrieved` 单独计数，不同时计入全文排除原因。
- 全文排除使用一个最能解释决策的主要原因，分类必须来自方案。
- 保留全文定位、获取日期和版本。
- 补充材料、勘误和同一研究的其他报告与主报告建立关联。
- `record_id` 与 `report_id` 用独立关联表保存；不在报告行中限制为一个 record_id。可有一条记录对应多份报告，
  也可多条记录指向同一份报告。不得仅为平衡数量而合并报告。

### 5. 建立研究—报告关系

创建研究表，把多个 `report_id` 关联到同一 `study_id`。记录关联依据、主报告和补充报告。不要简单地把“纳入
报告数”当作“纳入研究数”，也不要把同一研究的多个结局报告当成多个独立研究。

### 6. 提取数据

按方案建立两层数据：

- 研究/报告层：设计、地点、样本、干预/暴露、对照、随访、资金、风险偏倚信息；
- 结局层：`study_id`、结局定义、时间点、分析人群、效应尺度、组别分母、估计值、区间或计算所需统计量。

每个关键数值记录来源文件、页码、表/图/段落和提取者。第二人验证关键结局；AI 抽取只作为待核对值，未经人工或
独立来源核对时标为 `unverified`。

不要强迫所有研究进入同一固定列集。Meta 输入前核对结局定义、时间点、estimand、效应尺度、分析人群和重复
人群；不兼容时保留叙述综合或分层，不强行合并。

### 7. 生成 PRISMA 计数

使用本技能自包含的 Python 3.10+ 标准库工具，只读取已经人工规范化的 JSON 行表和绑定清单，不导入原始
RIS/NBIB/BibTeX/CSV，不下载全文，不进行 AI 筛选、去重判定、自动纳排或合并模型拟合。业务字段及完整口径见
[PRISMA 筛选跟踪表](templates/prisma-screening-tracking-table.md)。不能把工具成功执行等同于检索完整或科学判断正确。

本工具要求实际执行的脚本也位于 `--root` 内并绑定到清单。全局安装时，从已加载的本技能 `SKILL.md` 所在目录找到 `scripts/compute_prisma_counts.py`，在用户已授权的论文输出目录中创建字节一致、保留许可的副本，例如 `paper/tools/compute_prisma_counts.py`；不覆盖已有不同版本。清单的 `tool_artifact_id` 须登记这份副本的项目相对路径、版本及实际SHA256。

在论文项目根目录运行，输入清单与两个输出引用均相对于 `--root`，输出父目录须已存在：

```powershell
python -B paper/tools/compute_prisma_counts.py paper/evidence/prisma-inputs-v1.json --root . --output paper/evidence/prisma-counts-run-001.json --check-output paper/evidence/prisma-check-run-001.json --run-id prisma-run-001
```

开发者单元测试在下载的源码仓库内运行：`python -B -m unittest discover -s tests -p test_prisma_counts.py -v`。安装副本不包含仓库测试目录。

- 清单以 `artifacts[{id,path,version,sha256}]` 明确绑定规范化数据、实际执行的计数脚本和所有影响计数的声明依赖；
  通过 `dataset_artifact_id/tool_artifact_id` 找到角色，绝不按文件名推断。清单自身也以稳定 `id/version` 和实际字节
  哈希进入输入集合；不在文件内部保存自身哈希。脚本运行前后核对输入字节，变动时拒绝产生有效计数。
- 一份数据文件保存 `records/reports/studies/record_reports/report_studies` 五个数组、`protocol_version` 和预定义
  `exclusion_reasons`。已人工决定的筛选状态是输入，不是脚本的推理结果。未知状态、重复 ID/边、冲突关系报错；
  `uncertain/pending/conflict` 和缺失必要关联标记 unverified，输出仅为 observed_only_not_final，不可画成最终流程。
- 输出 `counts` 的每项都有 `unit/count/member_ids/filter/source_artifact_id`，配套 `source_rows` 定位原始 JSON 行、
  来源 ID 和来源项 ID，`associations` 保留完整多对多边。`included.reports` 与 `included.studies` 各自取正确单位集合。
- `database_register`、`other_record`、`other_direct` 分支独立；直接识别报告的其他方法没有记录筛选等式。
  保留记录数不能直接当作报告数。跨分支同一报告的归属必须由人工先核对，本版不自动分配或重复相加。
- `not_retrieved` 不属于全文排除；retrieved 但 decision=pending 是待评估，不能当作已评估。每份排除报告恰好一个
  方案内主要原因。`equations` 只核对同单位分区；可选 `expected_counts` 仅用于比较旧汇总，差异不改写计算值。
- `--output` 是唯一权威计数工件；先落盘，再由独立 `--check-output` 回执绑定其实际哈希，无自哈希循环。回执使用
  R2 同形 `artifacts/checks`，scope/namespace=`prisma_counts`，不修改 passport，也不依赖兄弟技能导入或安装。
  输入/版本或报告字节变更后旧检查不能沿用；流程图使用这一工件及其回执，不创建并行的手填数字副本。
- 退出码：0=reconciled（仅声明数据内计数闭合）；1=结构/绑定/执行错误或 discrepancy（详看回执区分）；
  2=CLI 参数错误；3=unverified。正常查出差异仍为 completed；无效输入为 failed、domain_result=null。
  预检绑定失败时若无法获得完整输入集合，失败回执也不能注册为有效检查；不得补造缺失绑定。
- 输入和已有输出绝不覆盖。每次使用新输出路径及新的 `--run-id`；stdout 仅给状态、路径和问题数量。

根据实际来源选择适用的 PRISMA 2020 流程图版本。计数和契约核验不证明全文已读、双人独立审查、研究关联真实
或纳排判断适当；这些仍需人审。工具只做单次声明数据集的计数，不自动识别更新综述旧/新研究或重新筛选。

### 8. 验证与交接

至少验证：

- 原始导出、规范化记录和重复组之间可追溯；
- 每个筛选决定对应方案版本和审查者；
- 不确定记录没有被静默排除；
- 未获取全文与全文排除分开；
- 全文排除原因总和与排除报告数一致；
- 纳入报告均关联到研究，研究数与报告数口径清楚；
- 关键提取值有页/表定位和验证状态；
- PRISMA 计数可从行级数据复算；
- Meta 输入没有重复人群、方向错误或不兼容尺度。

把可合成且已验证的结局数据交给 `dyz-med-analyze` 制定并审批统计计划。没有成功执行的合并模型输出时，不写入合并
效应、异质性、预测区间或小研究效应结论。

## 建议输出

```text
paper/evidence/protocol-check.md
paper/evidence/search/search-log.csv
paper/evidence/search/raw/
paper/evidence/search/records-normalized.csv
paper/evidence/search/duplicate-groups.csv
paper/evidence/screening/title-abstract.csv
paper/evidence/screening/full-text.csv
paper/evidence/studies.csv
paper/evidence/extraction/study-level.csv
paper/evidence/extraction/outcome-level.csv
paper/evidence/prisma-inputs-v1.json
paper/evidence/screening/normalized-screening-v1.json
paper/evidence/prisma-counts-run-001.json
paper/evidence/prisma-check-run-001.json
paper/evidence/review-events.csv
```

人工台账可适配已有目录和字段，但不得丢失来源、版本、审查者、决定和时间戳。计数工具不直接读取这些任意格式
台账；须显式导出为模板规定的 JSON 结构，保留 decision_source 指向实际决定记录，不自动猜列名或补值。

## 完成标准

- [ ] 方案或方案偏离有版本记录
- [ ] 原始导出与检索式完整保存
- [ ] 去重决定可审计且未误合并不同报告
- [ ] 标题摘要和全文决定可追溯
- [ ] AI 未被伪装成独立双审查者
- [ ] record、report、study 已正确关联
- [ ] 关键提取值有来源定位和验证状态
- [ ] PRISMA 计数可由行级记录复算
- [ ] 未执行的 Meta 分析没有被写成结果

## 参考材料

- [PRISMA 筛选跟踪表](templates/prisma-screening-tracking-table.md)
- [虚构教学示例](examples/worked-example.md)
- [规范与文献](references/规范与文献清单.md)
