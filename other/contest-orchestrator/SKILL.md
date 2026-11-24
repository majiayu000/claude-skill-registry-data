---
name: contest-orchestrator
description: 数学建模竞赛唯一主控流程：题目解析、选题与模型规划、baseline、求解、图表、论文、评审、交付门禁和 replay；支持 AUTO/COLLAB/LOCK 与主会话—fork 分支协作。
metadata:
  version: "4.19"
  changelog: |
    v4.19（开发版）: H4 节点取消，其蓝图设计职责并入 H5（建模与求解）；H3 直接到 H5，H6-H9 编号不变；H5 内部四阶段迭代（蓝图设计→快速验证→优化迭代→完善冻结）
    v4.18: 稳定版
---

# contest-orchestrator

数学建模竞赛唯一主控入口。当前为 4.19 开发版（H4 已并入 H5）；版本标识以 `VERSION` 为准，完整发布检查尚未通过。版本发布必须完成静态检查、负例、replay、真实项目闭环和安全审计。

主会话负责范围、事实、权限、冻结、节点裁决和最终交付；fork 分支负责获得授权的赛题求解、实验、图表或论文工作。正式项目、数据、replay 和交付包写入项目工作区，不写入 skill 安装目录。

## 1. 启动与模式

先确定任务范围，再按需读取一个工作模式。未指定模式时，使用范围路由器识别最小任务范围；不读取未选模式的完整规则。

```text
python scripts/mode_router.py --mode <mode> [--variant <variant>]
python scripts/scope_router.py --prompt "用户原话" --workspace <项目根>
```

选择 `full-contest-mathorcup` 时，范围路由器加 `--mode full-contest-mathorcup`，使阶段与门禁输出采用 M1–M5。

可用模式：

- `full-contest-legacy`：完整竞赛流程，兼容 v4.16 稳定基线规则。
- `full-contest-4-18`：稳定协作流程，使用 G0–G6 节点门禁。
- `full-contest-harness`：受控自动化测试流程，使用 H0–H9。
- `full-contest-mathorcup`：MathorCup 大数据竞赛流程，使用 M1–M5；逐节点人工确认，固定子 agent 使用 Luna/Sol 且推理强度均为 `max`，详见 `references/modes/full-contest-mathorcup.md`。
- `subproblem`、`paper`、`figures`、`delivery-audit`、`skills-optimization`：分别处理单问、论文、图表、交付审计和技能优化。

单次任务只能有一个 `active_mode`。模式文件只规定边界和阶段；题型、专业写作和图表工作由对应 skill 执行。调用外部 skill 前必须读取 `references/external_skill_adapters.md`；外部 skill 只能执行当前任务卡中的专业子任务，不得切换模式、扩大范围或替代主会话决策。

### Harness 硬门禁

仅当 `active_mode=full-contest-harness` 时，主 agent 必须在 H0 前实际调用 `superpowers:using-superpowers`，并按 [Harness 模式](references/modes/full-contest-harness.md) 登记固定角色、任务卡、模型与推理强度、真实调用和派发证据。任务卡显式指定节点绑定的 `model` 与 `reasoning_effort`；主会话负责裁决，固定角色承担各自专业任务；必要调用、实例或任务卡缺失时保持 `BLOCKED_INPUT` 或 `PAUSE`。H5 使用唯一主解题实例覆盖全部小问，H6 必须独立于 H5；创建角色与正式派发分开。

H2、H3、H5–H9 均保留人工批准门。重要产物先组成 `review_packet`，由用户明确批准并绑定当前 SHA-256；审查包或产物变化时按影响范围回流。H8 必须实际调用 `academic-writing` 与 `mathmodel-latex-skill`，H9 必须实际调用 `bzd-review-paper` 与 `mathmodel-latex-skill`，各调用均登记可定位的 `evidence_ref`。预载协议不算实际调用。

使用 `templates/harness_control.yaml` 初始化控制记录；比赛期间使用 `validation.profile=competition_fast` 和 `.contest/change_impact_card.yaml` 选择增量复核。进入下一节点或完成变更复核前运行：

```text
python scripts/check_harness_control.py <project-root> --through H<n>
```

H5 冻结后登记 `run_manifest`，运行 `scripts/check_h5_result_traceability.py <project-root> --strict`；运行命令、随机种子、结果、模型契约及适用的敏感性/鲁棒性报告均须真实登记，结果与 `canonical_report` 等证据绑定当前哈希。缺证据保持 `PAUSE`，路径、格式或哈希不一致为 `BLOCK`。H6 接口记录保留项目相对 `source_path` 和当前 `source_sha256`，结果卡与模型卡由当前独立 H6 实例核验。

#### 按当前节点读取权威协议

| 当前任务 | 读取范围与保留的义务 |
|---|---|
| H5 建模与求解 | [Harness 模式](references/modes/full-contest-harness.md) 的 H5 输入/产物分工与工具绑定；[模型总结协议](references/model_summary_protocol.md) 和[作者证据协议](references/paper_author_evidence_protocol.md)定义逐问模型、结果与读者证据交接 |
| H6 独立验证 | [H6 验证协议](references/h6_validation_protocol.md) 与当前 `h6_verification_scope.yaml`；首次按完整小问范围核验必查项与登记抽样，后续按模型、数据、关键结果或解释变化定向复核，普通正文与排版不触发 H6 |
| H7 图表 | [图表模式](references/modes/figures.md) 与所选视觉工作流；图表生成绑定批准的槽位、提示词/计划版本和当前证据，保留用户选图与最终登记 |
| H8 计划、章节、整合 | [章节执行协议](references/h8_chapter_execution.md)决定当前阶段的输入与交接；[写作者优先协议](references/h8_writer_first_protocol.md)、[模型总结协议](references/model_summary_protocol.md)、[作者证据协议](references/paper_author_evidence_protocol.md)分别负责叙事、最终模型呈现与证据转写 |

启用 `reader_evidence_protocol: "1.0"` 后，H5–H8 按作者证据协议形成真实的读者证据链。正式 H8 素材准入使用 `paper_material_readiness.yaml`；`schema_version: "2.0"` 的 `evidence_matrix` 必须覆盖逐问与全局要求。素材不足时一次提交完整 `evidence_gap_matrix.yaml`，由主会话协调 H5/H6/H7 补证，不让作者以泛泛表述填充篇幅。

先按控制记录的 `visual_workflow` 选择准备时序：`chapter_parallel` 读取[逐章批准与并行图表协议](references/harness_chapter_parallel.md)，`writer_first_draft` 读取[初稿准备协议](references/harness_writer_preparation.md)，未声明时保持历史路径。逐章流程在 H6 获批、写作计划获批后按 `writing_order` 一次完成一章；用户批准完整章节后才派发下一章及该章图表提示词，图件制作/返修可与后续章节并行。正式 H7、H8、H9 的最终闭合要求仍保留。

`paper_narrative.global.paper_spine` 是唯一最终章节主线；作者简报、章节卡和连续性包复用同一主线。作者按当前章节的冻结证据连续写作并在完整章节后检查；摘要论证卡在计划阶段冻结结构，各章回传 `abstract_contribution`，最终摘要仅由 H8C 在正文与附录定稿后撰写，并以 `scripts/check_abstract_contract.py --strict` 和 `abstract_contract_report` 闭环。

### 增量回流与验证

比赛期间项目文件发生变化时，先填写 `.contest/change_impact_card.yaml`，再运行 `scripts/validation_router.py <project-root>`。路由器根据变更卡输出唯一复核计划；计划外节点不得自动重跑，也不得以局部复核替代 H9 完整交付门禁。完整字段、允许文件类型、哈希和失败处理见 `references/incremental_validation_policy.md`。

| 等级 | 适用变化 | 复核范围 | 默认视觉检查 |
|---|---|---|---|
| L0 | 正文措辞、普通排版、论文元数据或引用表述，模型和数字保护字段未变 | H8 叙事、主张覆盖、成品过程词检查 | 否 |
| L1 | 单张图件或图表登记变化 | H7 登记、格式、来源和 SciPilot QA | 是 |
| L2 | 单个小问的模型、代码、数据或结果变化 | 该小问 H5，定向 H6，受影响 H7/H8 | 仅受影响图表 |
| L3 | 全局数据、符号、跨问接口、全局假设或多小问关系变化 | 从 `earliest_invalid_node` 到 H8 的完整相关链 | 涉及图表时是 |

`competition_fast` 只减少与变更无关的重复验证：项目文件变化不触发技能全套测试；技能源码或检查器源码变化时，将 `skill_code_changed` 设为 `true` 并执行完整技能测试。H2、H3、H5–H9 的用户批准门、冻结哈希和 H9 完整交付门禁始终保留。上游变更后只将引用变更字段的下游产物标记为 `stale`；未受影响的产物不得重新生成。需要描述具体下游影响时，可在同一变更记录中附 `rework_patch.yaml`。

范围类型：

| 范围 | 行为 |
|---|---|
| `PLAN_ONLY` | 只生成题目理解、方案、风险和写作计划 |
| `SUBPROBLEM` | 只处理指定小问，明确输入、输出和时间边界 |
| `FULL_CONTEST` | 执行 A–G 全流程，正式交付使用 `STRICT` |
| `DELIVERY_AUDIT` | 只审计项目，不修改源项目 |

权限模式：

- `AUTO`：在已授权范围内自主推进；时间、证据或模型风险达到止损条件时进入收敛。
- `COLLAB`：G0–G6 关键节点暂停，等待用户确认后继续；确认包包括目标、证据、风险、影响、最小修改和回滚点。
- `LOCK`：冻结模型、数据、参数、结果和提交版本，只允许排版、可验证修复、图表美化和交付检查。

## 2. 全流程：FULL_CONTEST + STRICT

以下 A–G 描述共同的产物和质量要求；实际节点、派发顺序和人工批准按已选模式执行。Harness 图文时序以 `visual_workflow` 对应协议为准。

### A. 题目理解

建立条件台账、问题图、复杂度画像、数据审计、符号表和模型假设。每条假设记录简化内容、数据或题面依据、误差边界和适用范围。A 阶段通过：

```text
python scripts/check_core_execution.py <replay> --phase A
```

### B. 方案与 baseline

文献流程固定为“需求卡与检索提示词 → 用户检索并下载全文 → 用户的文献 agent 阅读全文并回传摘要、方法、数据和适用边界 → 主 Agent 摘要级整合与引用登记”。主 Agent 不主动联网检索、不替用户下载、不直接读取或解析文献全文。进入正式文献分析前，先生成 `literature_request.md` 与 `literature_request.yaml`，明确各小问覆盖、检索关键词和回传字段；用户回传 `literature_sources.yaml` 后，系统只读取题名、作者、来源、年份、DOI/官方链接、摘要和外部 agent 的结构化总结。所有 Harness profile 的文献总数硬范围为 6–11 篇，推荐 8–10 篇；中文文献必须逐小问覆盖，每个小问至少 1 篇；英文文献不设硬性最低数量，但建议覆盖全部小问。英文覆盖建议和推荐数量不阻断节点。每篇计入总数的文献均须有 `citation_key`、原文定位及在 H5 落位的模型、数据、参数、验证或结论用途。任一硬条件不通过时保持 `PAUSE`。

正式建模前必须收到并校验本题用户返回的 `literature_sources.yaml`；语言数量、总量或小问覆盖任一不通过，状态保持 `PAUSE`，不得进入建模或求解。该文件由用户检索下载文献后，交给指定文献 agent 生成结构化摘要、方法、数据、适用边界和证据定位。

文献证据通过后，才能使用题型 profile、选题评分和风险探针确定候选路线，形成 `method_transfer_map.json`、文献使用登记、`model_blueprint.yaml`、`model_contract.yaml`、接口契约和图表需求清单。需求清单仅登记正文主张、图号占位、目标小问、所需结果字段和候选来源，不得确定数据图的图型、视觉编码或版式。每个小问至少登记一条可落地的方法迁移（`adopt` 或 `adapt`）和一条实际数据、参数、测量先例或基准证据，并绑定 `citation_key`、证据定位、模型组件或数据字段及使用方式；登记不完整时不得确定模型路线、baseline 或图表需求清单。用户确认路线、文献用途和图表需求清单后，才进入正式建模。

机器门禁同步检查顺序：H3 必须登记需求清单、全文分析 agent 提示词和用户回传的 `literature_sources.yaml`；H5（建模与求解，已合并原 H4 蓝图设计职责）必须登记 `method_transfer_map.json`、`model_blueprint.yaml`、只含论证需求的 `chart_requirements.yaml` 以及完整求解产物；H5 的实际派发时间不得早于 H3 的批准时间。缺任一项保持 `PAUSE`，不得以补写节点记录替代真实文件。

先运行最简 baseline，只判断问题是否可解；未达到目标时才在已登记文献证据和路线约束下升级模型。

求解前必须完成：

- 变量、参数、中间量三集合及符号表闭环；
- 目标函数、约束、可行域、模型类别和规模量级；
- 求解方法、初始化、边界、终止条件和异常处理；
- 至少一项理论性质或可靠性说明；
- 结果文件、代码、数据和图表的源关系。

B 阶段通过：

```text
python scripts/check_core_execution.py <replay> --phase B
```

### C. 求解与图表

结果只能由代码、推导或可审计数据源生成，并即时写入 `results/`、CSV/JSON、敏感性结果和运行清单。记录随机算法的 seed、参数、环境、收敛或间隙；每个关键数字进入数字源登记或冻结表。

图表路由固定为：

| 图表类型 | 路由与登记 |
|---|---|
| 数据结果图 | `SciPilot → ModelViz → SciPilot`；登记 `generator=modelviz`、`semantic_qa=scipilot-figure-skill`、`formats=[svg,png]`、`insertion_format=svg`；页面排版另登记 `layout_mode` |
| 问题分析流程图、技术路线图、原理/机制/受力/几何和公式示意图 | 使用 `tikz-scientific-figures`，选择与路由一致的目录 `template_id`，保留可编辑 .tex 源与 SVG/PNG，登记 starter 来源与哈希；通用交付检查兼容已登记的历史 `tech-route-maker` 产物，H7 新图仍遵循当前路由 |
| Draw.io 编辑图 | 仅用户明确要求时使用，登记 `user_requested=true`，输出 SVG/PNG 并保留 `.drawio` 源文件 |

画图默认做视觉检查，确认图片美观、整洁、可读、层级清楚、标注完整；非画图默认不做视觉检查，只有用户明确要求或命令显式提供 `--visual-check` 时才渲染和检查。视觉检查不能替代公式、数字、引用、来源和结构门禁。

数据结果图的图表决策卡必须由 `scipilot-figure-skill` 基于冻结数据生成；未登记 `decision_card` 和 `decision_author=scipilot-figure-skill` 时，禁止调用 ModelViz、确定图型或生成图像。每张图必须满足：先有完整图表决策卡；数据同源；图号与题注对应；坐标轴/单位/符号与符号表一致；来源登记真实；输出包含 SVG、PNG 和可编辑源；LaTeX 使用 SVG 插入。禁止饼图、双 Y 轴、彩虹色图、无单位坐标轴和把分类点连成无意义折线。

H7 图表 agent 在调用任何图表生成 skill 前，必须汇总生成 `visual_argument_plan.yaml`（`prepared_by=h7-figure-agent`）。该计划先回答“读者在这里需要理解什么、什么证据能降低理解成本、没有图会遗漏什么”，再决定是否需要视觉表达、每个槽位的表示方式和采用哪条路由。每个有图槽位还必须填写 `figure_intent`，明确读者问题、解释关系、必须出现/禁止出现内容、正文落位、图前/图后论证功能、唯一生成路由、模板状态、精确 `template_id`、`visible_element_map` 和 `canvas_profile`；H5→H6→H7 的 `visual_evidence_packet.yaml` 仍保持轻量证据接口。每个小问必须审计 `orientation`、`mechanism`、`model_structure`、`algorithm_process`、`result_evidence`、`validation_robustness` 六类视觉义务；结构化模型、迭代/启发式算法、机理/空间关系和主要结果的硬性义务由 H5 模型总结卡推断，不能用“文字已足够”规避。数据结果槽位才交由 `scipilot-figure-skill` 生成数据图决策卡；流程图、技术路线图和示意图分别交由对应专业 skill。多小问或存在跨问接口时必须增加 `global_story` 槽位。该计划不设脱离论证的固定总图数，但必须重新计算必需视觉槽位、必需图槽位和计划图数，且一张图不得同时填充多个槽位。

阶段一只提交视觉论证计划及 `.contest/reviews/H7_visual_plan_review_packet.yaml` 供用户审查；用户批准必须以 `.contest/approval_log.yaml` 中 `gate: H7_VISUAL_PLAN` 且覆盖当前计划 SHA-256 的记录为准。独立批准缺失时，H7 不得进入图型选择、模板检索、生成和登记；计划审查期间 H7 保持 `status: draft`，完成图表生成、质量检查和登记后才转为 `review_pending` 并提交普通 H7 最终审查包。批准后，阶段二才由 SciPilot 形成数据图决策卡或指定流程图、路线图和示意图路由。最终 `figure_registry` 的每张图必须用 `visual_slot_ids` 绑定已批准槽位，并复制计划的 `generation_route` 为 `generator`、登记 `template_status`、`template_id`、`visible_element_map`、`canvas_profile`、`template_sha256`、`template_fixture`、`visual_qa`、`claim` 和 `reader_takeaway`；流程图和 TikZ 图还必须登记 `starter_source`，并在可编辑源中保留模板来源标记。对应 starter fixture 未通过、视觉检查缺失、模板哈希不一致、计划外图表、必需槽位未闭合或注册表与计划不一致时 H7/H8 均 BLOCK。H8 只读取批准计划，不得新增图表来增加篇幅。

页面排版由 `mathmodel-latex-skill` 按登记的 `layout_mode` 执行，不由 SciPilot 或 ModelViz 改变图表语义。允许的入口只有 `single`、`side_by_side`、`wrap_short` 和 `tall_constrained`；具体宏与尺寸规则以 `references/figure_policy.md` 和 `mathmodel-latex-skill` 的布局契约为准。

H5→H6→H7 使用 `visual_evidence_packet.yaml` 传递最小图表证据：H5 生成，H6 以当前实例核验，H7 将信息单元绑定到视觉槽位和 `figure_registry`；标准图至少两个独立信息单元，单一证据只能使用带理由的 `compact`。

C 阶段通过：

```text
python scripts/check_core_execution.py <replay> --phase C
```

### D. 论文写作

写作前生成 `paper_outline.md` 与 `appendix_plan.yaml`，覆盖摘要、问题重述、问题分析、模型假设、符号说明、问题引入、模型建立、模型求解与结果分析、灵敏度分析、模型评价与改进、结论、参考文献和附录；摘要另由 H8A 生成 `abstract_argument_card.yaml`，由 H8C 在正文和附录定稿后最后写作。一级标题使用中文序号；“模型假设”和“符号说明”是两个独立一级章节；建模问题统一置于“模型建立与求解”一级章节下。建模问题章节必须读取 `references/model_summary_protocol.md`，按“问题引入与建模思路段 → 模型建立 → 模型求解与结果分析”的读者路径组织正文。

正文要求：

- 全文只设置一次“符号说明”章节；局部符号在正文首次出现处给出含义、单位或量纲、取值域和变量类型，全文符号、单位、上下标一致；
- “模型假设”和“符号说明”分别设置为全局一级章节；不得合并成“模型假设与统一符号”，也不得在每个小问重复生成独立符号章节；
- 每个问题标题后先写不编号的问题引入与建模思路段，交代任务、已知条件、关键困难、输出目标和前后小问关系；
- 每个问题默认只设“模型建立”和“模型求解与结果分析”两个编号小节；小节内使用无编号加粗引导词，不把任务卡字段变成目录；
- 建模与求解章节是正文论证中心；问题分析、模型评价、结论等支撑章节必须明确承接或回收核心章节主张，不得与建模章节割裂成独立文章；
- 推导完成后在“模型建立”小节末尾给出唯一的“最终求解模型”框，集中绑定决策变量、参数、目标/状态关系、约束/边界、来源公式和求解接口；
- “模型求解与结果分析”必须同时包含算法依据、实现条件、主要结果和结果意义；灵敏度或稳健性仅在有独立证据时单独成节，否则并入结果分析；
- 每个公式标注来源、推导链、含义、单位和边界条件；
- 每个算法说明选择理由、参数依据、终止条件和异常处理；
- 每个结论绑定结果文件、图表、表格或引用；
- 模型建立与求解保持全文核心体量，不能用空白页、重复公式或强制分页填充；
- 附录只放真实触发且支撑正文的内容；程序题默认在论文附录展示核心代码，完整源码登记到支撑材料，
  由 `appendix_plan.yaml` 的 `appendix_code_mode`、`core_source_files`、`full_source_files` 和
  `support_source_files` 统一管理；推导、数据验证和 AI 工具说明按附录计划登记；
- 数字只从权威结果源或冻结表进入论文，禁止手工改写未核验数字。

国赛 2026 规则：电子版不设目录；按湖南赛区确认口径，摘要不计入正文页数，正文页数从正文主体起计，包含正文主体、参考文献前的 AI 工具使用声明和参考文献，最多 30 页。提交论文文件总页数最多 51 页。当前国赛个人 profile 将总 PDF 35–51 页作为推荐区间，用于内容容量规划和人工复核；不得以重复或无效材料达到推荐下限。论文 PDF 必须是含文本层的非图片 PDF，论文文件不超过 20 MB；支撑材料使用 ZIP 或 RAR，文件不超过 20 MB，附录列出文件清单。全国规则与赛区口径存在差异时，以当前参赛赛区正式通知为准。

使用 AI 时，正文在参考文献前放置“AI工具使用声明”，支撑材料提供 `AI工具使用详情.pdf`，说明实际使用的工具名称与版本、用途与环节、关键提示/交互摘要、采纳、人工修改和核验情况。不要求把 AI 工具列入参考文献；声明可以简洁，但必须真实覆盖实际使用范围，突出参赛队主导核心建模、分析和结论，不得隐瞒使用或虚构未使用。

论文写作链固定为：`academic-writing` 数模学术写作适配层 → 必要时 `humanizer-zh`。两者只能处理允许的普通正文表达，不得改动公式、数字、引用、专业术语、表格、图表编号、模型逻辑和受保护结构。修改后重新运行一致性检查。

成品必须删除元话语、内部交流、提示词、评审过程、交接信息、用户信息、修改轮次、调试信息和未确认内容，只保留定稿事实、推导、证据、结果与结论。摘要按 profile 检查字数、逐问结论、数字溯源、独立总评和关键词格式；正文和摘要必须通过防 AI 痕迹硬性质控。

D 阶段通过：

```text
python scripts/check_core_execution.py <replay> --phase D
python scripts/check_math_contract.py <paper.md>
```

### E. Critic 评审

逐小问检查题面覆盖、假设、符号、公式推导、模型—代码—数据—图表一致性、结果可靠性、摘要、AI 痕迹、匿名、页数、引用和附录。每条问题记录位置、证据、影响、最小修改和修复后的验证状态；没有证据时不得把推测写成缺陷结论。

### F. 交付门禁

```text
python scripts/delivery_all.py <项目根> --strict
python scripts/delivery_all.py <项目根> --strict --research-evidence-strict
```

交付前必须通过模型、数据、结果、引用、图表、符号、推导、算法、摘要、附录、代码可复现、匿名、AI 工具说明、PDF 文本层、PDF 大小、LaTeX 警告、版面源规则、正式交付漂移和文件哈希检查。任何 `FAIL`、严格模式 `WARN` 或 `UNKNOWN` 均不得宣称交付完成。正式 PDF 必须由当前源文件生成并与交付清单一致。

### G. replay 与经验沉淀

保存决策、快照、经验使用、证据索引、运行清单和回放记录。只将已经验证、可复用且不依赖特定对话过程的规则写入经验库；不把未确认材料、临时数据、原始日志或内部交流写入长期规则。新版本完成静态、单元/回归、负例、隔离 replay、真实项目闭环和安全审计后，才可登记为稳定版；未通过时保留当前稳定版。

## 3. 主会话—fork 协作

主会话控制范围、事实、权限、冻结、冲突和最终交付；fork 分支执行授权的赛题、实验、图表或论文节点。分支回流必须提供：

1. 当前阶段和完成目标；
2. 可验证证据及相对路径；
3. 可复现命令、环境和验证状态；
4. 阻塞项、风险、禁止动作和未授权事项；
5. 下一节点首个状态报告。

回流前检查源文件、结果文件、登记表和当前 PDF 的新鲜度、SHA-256、来源关系与版本状态。节点产物只能进入授权工作区；论文交付物不得含内部日志、过程轨迹或未定稿内容。

## 4. 权威文件与按需加载

- 范围与模式：`references/task_scope_routing.md`、`references/mode_state_machine.md`、`references/collab_gate_policy.md`。
- 规划与证据：`references/evidence_first_planning.md`、`references/evidence_integrity.md`、`references/modeling_contract_hardening.md`、`references/research_evidence_contract.md`。
- 图表与论文：`references/figure_policy.md`、`references/figure_template_catalog.yaml`、`references/citation_policy.md`、`references/paper_review_and_absorption_lessons.md`、`references/paper_replay_lessons.md`、`references/appendix_coverage_policy.md`、`references/layout_and_delivery_drift.md`。
- H8 写作：`references/h8_chapter_execution.md`、`references/h8_writer_first_protocol.md`、`references/paper_author_evidence_protocol.md`；前者定义阶段路由，后两者定义读者优先的正文生成方式与证据转写契约。
- 增量复核：`references/incremental_validation_policy.md`；机器执行入口为 `scripts/validation_router.py`，项目模板为 `templates/competition_run_profile.yaml`、`templates/change_impact_card.yaml`，卡片结构为 `schemas/change_impact_card.schema.json`。
- 外部 skill：`references/external_skill_adapters.md`。其中的路由、输入输出、证据登记和视觉检查策略是唯一适配契约。
- 建模契约：`core/universal_modeling_contract.md`、`core/modeling_chapter_contract.md`、`core/appendix_contract.md`、`core/paper_hard_requirements.md`、`planner/modeling_profiles.yaml`。
- 机器可读路由：`manifest.yaml`、`scripts/script_registry.yaml`；版本唯一来源为 `VERSION`；范围唯一入口为 `scripts/scope_router.py`；增量复核入口为 `scripts/validation_router.py`；完整交付入口为 `scripts/delivery_all.py`；项目只读审计入口为 `scripts/audit_project.py`。

只在命中任务范围时加载对应参考材料；历史归档和 `scripts/archive/` 不参与运行时路由。

## 5. B 题项目初始化（优化决策类）

```text
python scripts/init_b_project.py <项目目录> --name "项目名称"
```

从 `templates/b_project_template/` 创建待填写骨架、目录和项目 README，并填入项目名与日期；已有文件冲突时停止，不覆盖比赛输入。新项目保留 H4 并入 H5 的结构，批准、派发和验证记录等待真实任务发生后登记，初始化不代表节点完成。

项目生成的 README 说明目录与使用步骤；字段、配置和历史兼容问题按需查看 [B 题配置说明](references/b_project_gotchas.md)。实际求解、科学核验、逐章批准和 H9 完整交付仍按当前模式执行。
