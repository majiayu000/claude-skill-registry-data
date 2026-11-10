---
name: dyz-med-flowchart
description: >-
  从可追溯的研究流程计数生成并核对随机试验、观察性研究、系统综述或范围综述流程图，交付结构化计数、
  Mermaid/可渲染图稿、图注和流程叙述。当用户要求 CONSORT、STROBE、PRISMA 或 PRISMA-ScR 流程图时使用；
  文献去重与筛选由 dyz-med-screening-pipeline 负责，其他统计图表由 dyz-med-figures-tables 负责。
  Use for PRISMA, CONSORT and observational study flow diagrams from traceable counts.
---

# 医学研究流程图生成与核对

## 核心原则

1. 流程图只呈现已有、可追溯的事件与计数；不估算缺失数字，也不为了对账改数。
2. 先确定研究设计和当前适用的报告规范，再选择节点；没有一张通用图适合所有研究。
3. 每个数字保留来源文件、字段或记录集合，正文、表格和流程图使用同一来源。
4. 系统综述的检索、去重、筛选和 PRISMA 计数由 `dyz-med-screening-pipeline` 生成；本技能只读计数并绘图。
5. 失访比例不能单独决定缺失数据处理方法。只报告流程与差异，把影响分析交给 `dyz-med-analyze` 或
   `dyz-med-sensitivity`。
6. 无法渲染时交付 `.mmd` 或图形规格并标为 `not_rendered`，不要声称已生成图片。

## 选择规范

- 随机试验：使用现行 CONSORT 2025 及与具体设计相符的扩展。
- 队列、病例对照或横断面研究：按 STROBE 研究对象条目呈现必要流程；STROBE 不要求统一固定版式。
- 系统综述/Meta：使用 PRISMA 2020 对应的流程图版本，区分数据库/注册平台与其他识别方法。
- 范围综述：按 PRISMA-ScR 报告，并采用与检索来源匹配的 PRISMA 2020 流程结构。

记录规范名称、版本、扩展和核对日期。若用户要求旧版，保留为明确的历史需求，不称为现行规范。

## 工作流

### 1. 收集结构化流程事件

为每个节点记录：

```text
node_id | label | count | parent | reason_breakdown
source_file | source_field/query | analysis_set | timepoint | notes
```

空节点分成：

- `not_applicable`：设计上不适用；
- `not_recorded`：应有但来源未记录；
- `zero`：真实计数为 0。

不要把三者混写为空白。

### 2. 按设计建立节点

#### 随机试验

按适用情况呈现：

- 评估资格、排除总数及原因、随机分配；
- 每组分配、实际接受和未接受干预及原因；
- 每组失访、停止干预及原因和时间点；
- 每个分析集纳入人数及排除原因。

不要默认“失访人数 = 未纳入分析人数”。ITT、治疗策略、改良 ITT、符合方案和安全性分析集可能使用不同分母，
必须在节点中写明分析集。

#### 观察性研究

根据设计呈现来源人群、资格评估、排除、纳入、分组/匹配、随访和最终分析。病例对照、横断面、开放队列和
数据库研究的节点不同，不强套两臂试验结构。

#### 系统综述或范围综述

只读 `dyz-med-screening-pipeline` 的单一 `prisma-counts-<run>.json` 工件，或用户已有的等价、可复算计数工件。
不创建第二套手工数字；旧 YAML 或无绑定汇总表保留为 unverified，不能仅凭文件名升级为已验证。

对新工具输出先核对独立 `prisma-check-<run>.json`：

1. 通过 artifacts 的稳定 `id=prisma-counts` 找到用户实际路径；核对版本、实际字节 SHA256 和 check.report 哈希。
2. 检查 scope.domain=prisma_counts，execution_status=completed、applicability=applicable，且
   domain_result={namespace:prisma_counts,value:reconciled}。同时要求报告 status=reconciled、finalizable=true。
3. 将 checks.inputs 与当前清单、规范化数据、实际计数脚本和所有声明依赖逐项核对；输入/版本/报告变化则旧检查
   stale，缺绑定或缺文件则 unverified。单独的 completed、文件存在、0退出码或缓存 freshness 都不能代替核对。
4. discrepancy/invalid/unverified 或存在未解决问题时，只能交付显著标记的审阅草图，注明哪些节点非最终计数；
   不能将缺失关联导致的 observed_only 值当作最终0值。不在绘图阶段补决定、补映射或手工修数字。

从该工件的 `counts[metric].count/member_ids/unit/filter` 与 `source_rows/associations` 读取：

- 各数据库、注册平台识别的记录，以及其他方法识别的记录或报告（按所选官方模板区分）；
- 筛选前删除的重复记录、自动化删除和其他删除；
- 筛选记录与排除记录；
- 寻求获取、未获取和实际评估的报告；
- 按一个主要原因分类的全文排除报告；
- 纳入报告数和纳入研究数。

严格区分 `record`、`report` 和 `study`；一项研究可能对应多份报告，记录和报告也可能多对多。
`database_register/other_record/other_direct` 分支不混算；other_direct 只有报告路径，没有标题摘要记录等式。
从记录到报告用关联边解释，不使用“筛选记录减排除记录=寻求报告”。`not_retrieved` 不属于全文排除；
retrieved 但尚未评估的报告也不能冒充 reports_assessed。领域报告自带 equations 和 differences，绘图只消费不修复。
逐数据库/方法拆框须保留该工件 source_id 分组对应的成员集合，不制造第二份独立权威汇总。

### 3. 对账

只对适用于当前结构的关系做检查。例如：

- 资格评估数与排除、随机/纳入节点之间能否解释；
- 随机总数是否与各分配组总数一致；
- 各组“接受 + 未接受”是否与分配数一致；
- PRISMA 的筛选前删除、筛选、报告获取、全文排除和纳入节点是否可从行级记录重建；
- 最终分析分母是否与 Table 1、模型输出和正文对应同一分析集。

输出 `MATCH`、`MISMATCH`、`MISSING_SOURCE` 或 `NOT_APPLICABLE`。发现差异时列出两边数值和来源，不自动修复。

### 4. 生成图稿

先使用[流程图文字骨架](templates/prisma-2020-flow-skeleton.md)确认标签，再生成 Mermaid 或项目既定图形格式。

- 使用稳定的节点 ID，标签中保留阶段、`n` 和必要原因。
- 对用户提供文本做 Mermaid 转义，避免破坏语法。
- 控制每个框的文字量；长原因清单可移到图注或补充表。
- 保存图源和渲染文件及权威计数工件的 ID/版本/哈希、metric 绑定，确保后续可编辑。系统综述不再另存可手改的
  flow-counts 数值副本；节点清单仅保存 node_id、metric、标签和来源绑定。
- 渲染后检查截断、箭头方向、字体、对齐、灰度可读性和页面尺寸。

### 5. 生成图注与流程叙述

图注说明研究设计、分析集、时间点、缩写和规范。流程叙述只使用已核对计数，并与图保持同一术语。不要在流程图
技能中推断缺失数据机制、自动建议多重插补或宣称高失访“使研究无效”。

## 输出

建议交付：

```text
paper/data/figures/flow-counts.yaml
paper/data/figures/flow-diagram.mmd
paper/data/figures/flow-diagram.<svg|png|pdf>
paper/data/figures/flow-check.md
paper/sections/flow-narrative.md
```

以上 flow-counts.yaml 仅用于非系统综述的结构化计数。系统综述直接消费已绑定的
`paper/evidence/prisma-counts-<run>.json` 与独立检查回执，图源、图注和正文均引用这一版本，不复制维护第二份计数。
既有格式不强制改名，但须提供等价行级集合、单位与当前版本绑定；不能自动将历史手填汇总标为 reconciled。

标准库计数 CLI 由筛选技能提供，流程图不重新实现它。按已安装的 `dyz-med-screening-pipeline` 中的说明，将实际计数脚本以相同字节复制到论文项目内（例如 `paper/tools/compute_prisma_counts.py`），保留许可并在清单中绑定这份副本的路径、版本和哈希，再从论文项目根目录执行。不能直接把项目外的全局安装路径作为清单中的工具工件：

```powershell
python -B paper/tools/compute_prisma_counts.py paper/evidence/prisma-inputs-v1.json --root . --output paper/evidence/prisma-counts-run-001.json --check-output paper/evidence/prisma-check-run-001.json --run-id prisma-run-001
```

它仅处理显式规范化 JSON，不下载或筛选文献；退出码0/1/2/3分别表示声明数据内闭合、错误或差异、参数错误、未核实。
无需安装 passport 才能使用独立回执；缺计数脚本或输入时报告缺项，不伪造运行结果。

## 完成标准

- [ ] 规范、版本、扩展和研究设计已确认
- [ ] 每个数字有来源，零值/不适用/未记录已区分
- [ ] 适用的分母关系已对账
- [ ] 分析集、时间点、record/report/study 用词正确
- [ ] Mermaid 或其他图源可解析
- [ ] 渲染文件已目视检查，或明确标为未渲染
- [ ] 图注、正文和相关表格使用同一已核对计数

## 参考材料

- [流程图文字骨架](templates/prisma-2020-flow-skeleton.md)
- [虚构教学示例](examples/worked-example.md)
- [规范与文献](references/规范与文献清单.md)
