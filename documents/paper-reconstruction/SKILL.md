---
name: paper-reconstruction
description: "For all readers, with a specialty in experimental and behavioral research: reconstruct, replicate, adapt, and extend paper-grounded studies / 面向所有读者、专长是实验与行为研究：根据论文重组、复现、改造并发展研究。Use when a user asks in English or Chinese to reconstruct, reproduce, implement, program, audit, adapt, or extend an experiment, survey, longitudinal study, interactive task, organizational or field protocol; produce platform-tailored reports or migrate E-Prime, PsychoPy, MATLAB/Psychtoolbox, jsPsych, Qualtrics/SoSci, oTree, Inquisit, Gorilla, or another platform; define materials, event logs, wave plans, data dictionaries, and analysis contracts for R, Python, SPSS, Mplus, MATLAB, Stata, SAS, JASP/Jamovi, or other tools；中文触发包括平台适配报告、论文重组复现、复现实验、问卷或纵向流程重建、研究创新、搭实验、写程序、被试流程、材料重建、平台迁移、数据字典与统计复现。"
---

# 论文重组复现 / Paper Reconstruction

> **一句话定位：** 面向所有读者、专长是实验与行为研究，按论文证据与用户平台偏好重建来源、参与者流程、材料和分析的复现报告与实施蓝图；不替代单纯阅读，也不默认生成或验证实验程序。

这里的“重组”始终以论文证据为对象，不是脱离原文的泛化范式创作。

## 任务边界

- 用于从论文或研究设计重建实验对象、被试流程、程序/现场协议、材料、日志、数据和分析。
- 问卷或纵向研究可重建招募、波次、匿名匹配、量表呈现、流失管理、数据结构与分析；纯理论、综述、Meta 或共识阅读优先转用 `paper-anatomy`。
- 用于把用户的新想法建立在原研究之上：区分理论不变量与可调参数，并检查理论增量、被试可理解性、混淆、测量、实施和当前文献位置。
- 若用户只想读懂理论、结果或讨论，不要求落地复现，转用 `paper-anatomy`。
- 同时要求解读与复现时，先完成支撑实现的最小论文解剖，再输出统一的重组复现包。
- 发表文章优先，补充材料校准，开放程序和材料增强；任何缺失都必须标成缺失、假设或待验证项。

## 按需加载

1. 每次读取 `references/reconstruction-protocol.md`。
   生成或修改报告时同时读取 `../paper-anatomy/references/reader-expression.md`：概念先解释再标注专业名称，连接经历、数据与原文结果，按小标题区分实施建议，最后内部复核表达。
2. 收到 PDF 时读取 `../paper-anatomy/references/source-grounding.md`，并运行共享的 `../paper-anatomy/scripts/prepare_paper.py`；不要在本 Skill 内复制另一份索引脚本。
3. 每次读取 `references/replication-source-ledger.md`，在内部逐项检查 DOI、附录、Supplement、OSF、预注册、数据、代码、材料及更正信息；除非用户要求审计清单，否则不把完整来源账本写进报告。
4. 每次读取 `references/replication-deliverables.md`，先确定概念/程序/统计/直接复制层级并选择最小充分产物。
5. 需要平台适配报告（platform-tailored report）、程序复现、直接复制或平台迁移时，读取 `references/platform-selection.md`；目标不是 E-Prime 时再读取 `references/platform-adapters.md`，仅加载其中指向的所选平台深度参考。
6. 横断问卷、纵向/多波、组织档案链接或问卷平台任务，读取 `references/survey-longitudinal-path.md` 和 `references/domain-adaptation.md`。
7. 需要统计复现、分析代码或分析接口时，读取 `references/analysis-environment.md`；只有用户选择 R 时才读取 `references/r-reproducibility-guide.md`。
8. 涉及组织行为、社会互动、行为决策、健康/运动、教育/HCI、现场研究或跨领域迁移时，读取 `references/domain-adaptation.md`。
9. 目标平台为 E-Prime 时读取 `references/eprime-execution-path.md`；仅在用户要求构建文件时复制 `assets/eprime-starter/`。其他平台的重复关系遵循共同设计语义，不因此加载 E-Prime 参考。
10. 正式报告或保存 Markdown 时，读取 `references/output-contract.md`。
11. 同篇论文在两 Skill 间交接、复用既有结果或比较平台版本时，读取 `../paper-anatomy/references/study-evidence-contract.md`；共享已核验设计，不用旧报告代替原始证据。

## 工作流

1. 确认论文版本、目标 Study 和复现层级：概念、程序、统计或直接复制；不要为无关产物询问平台。
2. 输入为 PDF 时先生成 `source_bundle.json` 并读取 `document_index`：区分单篇论文与会议集/论文集，为每篇确认标题和起止页，并定位摘要、前言与理论、研究设计、结果与数据处理、讨论与文章价值。用户指定文章时用 `--article` 按序号、`paper_id`、DOI 或唯一标题短语精确选择；未指定时默认处理索引中的全部论文。选择不唯一时停止并要求更精确目标，不猜测。
3. 完成内部来源审计：规范化 DOI，核对所选论文正文、附录、Supplement、OSF、预注册、数据、代码与材料的版本、访问状态和读取范围。报告只在开头概括实际读取范围和关键证据边界，具体缺失或冲突放入 D1/D3；用户要求时才附完整清单。
4. 提取研究问题、理论来源、核心发现、变量、指标、模型和图表对应关系；复用 `source_bundle.json` 的目标论文页码、图表和链接候选，但不把索引全文写进 ABCDE 报告。
5. 判定实验、问卷、纵向、互动或现场研究类型；为每个 Study 建立参与者/受访者流程，纵向研究增加波次、匿名匹配、提醒和流失状态。
6. 平台适配报告、程序复现、直接复制或迁移均解析目标实施平台：已说明则采用，否则按研究类型询问一次。计算机化行为实验无偏好时声明默认 E-Prime 3.0；问卷/纵向未回答时保持平台中立。另行确定交付形式：默认 `report`（报告与蓝图），用户要求代码才为 `code`，明确要求且有运行条件才为 `runtime-check`。MATLAB 的实施与分析用途分开；工具箱不明时不自动断言使用 Psychtoolbox。
7. 识别原平台或现场协议，按目标平台输出原生组件、文件、随机化、设备/同步、日志、运行状态和迁移差异；社会互动要明确真人、延迟、主试控制、预生成或虚构。
8. 只有需要分析代码、统计复现或分析接口时才解析分析环境：已说明则采用；否则询问一次。未回答时输出平台中立分析契约，不默认 R。
9. 在确有实施需求时重建材料清单；随后闭合事件/问卷日志、稳定 ID、数据字段、**原文分析路线**与验证测试。不要为了填充模板生成泛化的“自建材料包”；来源冲突必须进入验证计划。
10. 对 E-Prime bundle 运行 `scripts/audit_replication_bundle.py`；对其他平台的结构化计划运行 `scripts/validate_platform_plan.py`，保持组件、流程、字段和分析语义统一。
11. 用户提出新想法时，先写出“原文限制或范式结构 → 理论/相邻文献 → 可检验问题”，再给设计；每个优先 idea 至少有两个可追溯支点（如原文限制 + 后续文献，或理论 + 相邻实证），并标为 `已检索确认`、`部分支持` 或 `待检索确认`。不得把未检索的灵感写成领域空白。
12. 按适用的 ABCDE 部分交付；`source_bundle.json` 始终作为本地定位侧车，不新增索引章节、不粘贴逐页文本，只在报告中保留目标范围和必要的页码/图表来源指针。最小交付优先，保存为正式 Markdown 或结构化包时运行对应校验器。

## ABCDE 输出契约

```text
A. 论文重组复现目标与文献证据
B. 被试视角流程
C. 程序与现场协议蓝图
D. 材料、数据与分析复现
E. 实验参数沉淀与研究发展
```

完整字段、行动顺序和反馈表见 `references/output-contract.md`。不得在 ABCDE 之外增加互相竞争的顶级输出结构。

## 不可妥协规则

1. 多 Study 均有完整或精简流程，或明确说明不展开的证据理由。
2. 原平台必须明示；现场流程本身也是一种运行平台。
3. 社会互动必须说明真假、同步方式、角色状态、支付和日志边界。
4. 伪代码说明用途，关键行配简短中文括注；不能把概念建议冒充原作者代码。
5. 数据结构可直接进入分析：稳定 ID、条件、试次、原始反应、派生指标和排除标记齐全。
6. 未知列名使用显式占位符；只有模型、变量与目标分析环境足够确定时才给可运行代码骨架。
7. 缺少原程序不自动等于严重缺口；必须说明今天如何自建、验证及牺牲的复现层级。
8. 所有平台不得把“并行”作为未定义关系；必须写成 `serial`、`serial-repeat`、`interleaved-repeat`、`nested-repeat`、`conditional` 或带同步契约的 `parallel-external`。
9. 纯报告保持 `design-only`。E-Prime 没有 `.es3`、生成的 `.ebs3`、烟雾运行记录和产物哈希时不得标为 `runtime-verified`；其他平台同样需要真实运行证据，不能套用 E-Prime 文件后缀。
10. 中性 starter 只能作为结构脚手架；第一份真正标记为 `runtime-verified` 的程序案例必须对应一篇明确论文，并保留 DOI、材料来源、实现差异和运行证据。

## 校验

保存为 Markdown 后运行：

```bash
python scripts/validate_output.py OUTPUT.md
```

校验器检查 ABCDE、关键实现字段、行动顺序和反馈表；链接是否真的可访问、版本是否正确、实现是否符合论文仍需人工核查。

生成结构化复现包后运行：

```bash
python scripts/audit_replication_bundle.py BUNDLE_DIRECTORY
```

语义审计器检查跨文件命名和依赖；E-Prime/E-Run 是否真实运行仍由运行状态门和烟雾测试证明。

## 质量门

- 报告使用“含义说明 [专业名称]”，专业名称标注不替代真实引用。参与者经历、数据字段/指标与原文结果彼此衔接；建议实施的方案不写成已经运行的发现。保留理论、分析与有来源的 idea。

- A 在开头简要说明实际读取范围和关键证据边界，理论、变量、分析和图表均能回到论文证据；完整来源检查保留在内部，具体缺失或冲突进入 D1/D3。
- B 只还原参与者或受访者实际看见、听见、完成和可能如何理解的流程；程序、主试后台动作、数据保存与实现决定集中到 C。
- B/C 使用同一套步骤和条件名称，让参与者体验可以逐项映射到 C 的程序或现场实现。
- C0 同时记录原论文平台、研究者目标平台及选择来源：用户明确、团队惯用、论文原平台、E-Prime 3.0 行为实验默认或平台中立。
- E-Prime 的 Proc/List 或其他平台的原生组件、调用关系、条件、日志责任和运行状态明确；问卷/纵向同时闭合题项、逻辑、波次、匹配、流失和导出字段。
- C5 以原文真实的统计方法、模型、对比和分析软件为中心；不要用试次字段表或默认 R 管线取代原分析路线。
- D 依次连接来源/材料状态、最小数据字段和验证差异处理；跨文件名称通过语义审计。只有真正需要实施时，才另列自建材料。
- 正文、Supplement、OSF、数据或代码矛盾时保留版本差异，并把消解测试加入 D3。
- E 只沉淀从论文复现得到的参数与经文献校准的发展方向；每个优先 idea 显式写出证据起点、理论依据、可检验设计与证据状态，不把用户想法冒充证据。
