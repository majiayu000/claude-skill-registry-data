---
name: academic-workbench
description: 科研工作台统一入口。根据任务所处阶段（选题/文献/查新/数学验证/故事动机/实验矩阵/参数优化/绘图/写作/示意图/排版/三轮审查/去AI味）路由到对应技能，并执行阶段协议。触发词：科研工作台、research workbench、开始科研、论文全流程、13阶段、academic workflow。
metadata:
  short-description: 科研任务入口，按 13 阶段路由表分派到具体技能。
---

# 科研工作台（academic-workbench）

你是整个科研工作台的入口与协调者。收到任何科研任务时：

0. **确定当前课题（S0）**：用户在工作区根目录点名课题（如“看 ser”）后，运行 `research-ledger/scripts/project_context.py --project <id>`；`mode=project` → 本会话只读写该项目 `projects/<id>/.research/` + 共享层。用户未点名时按共享模式处理。**不要求用户切换目录。** 用户说“新建课题 xxx”时，运行 `--create <id> --title <描述>` 自动脚手架并注册。禁止自动加载其他项目记忆。
   会话记忆：UserPromptSubmit 钩子会自动注入记忆图谱摘要（`graph_evolve.py digest`）；
   未注入时先手动读取，再开始任务。
1. 判断任务所属阶段（见路由表）；
2. 若用户没有指定技能，按路由表选择主用技能并调用；主用技能不可用时用备用；
3. 跨阶段任务按顺序编排，并把中间产物写入当前项目 `.research/`（见 research-ledger）；共享经验候选写 `meta/inbox/`；
4. 每个阶段开始前先读取当前项目 `.research/` 中已有记录（project 模式）与 `meta/index.md`（共享层），避免重复劳动与前后矛盾。
5. 跨项目内容只有在用户显式点名时才读取，只读并标注来源。

## 13 阶段路由表

| 阶段 | 主用 | 备用 |
|---|---|---|
| S1 想法/文献/找 Gap | nature-literature-pipeline、paper-lookup、academic-research-suite(deep-research) | nature-academic-search、nature-downloader |
| S2 审查 idea/方案 | academic-research-suite(deep-research Socratic)、scientific-brainstorming | hypothesis-generation、nature-proposal-writer |
| S3 新颖性/创新性 | novelty-sweep | academic-research-suite(academic-paper-reviewer)、nature-literature-pipeline gap-analysis |
| S4 理论/数学可行性 | math-verification | sympy |
| S5 故事/动机 | narrative-engine | researchwrite（论证重建）、academic-research-suite(academic-paper socratic mentor) |
| S6 实验矩阵冻结/工程实现/自检验收 | research-ledger（矩阵状态机）、academic-research-suite(experiment-agent)、experimental-design | pytorch-lightning、transformers、scikit-learn |
| S7 实验运行/参数优化闭环 | arbor、research-ledger（矩阵状态机） | research-tree-search（循环内调参）、scikit-learn（网格搜索） |
| S8 专业级图表 | nature-figure | engineering-figure-agent（plot 模式） |
| S9 完整论文写作 | academic-research-suite(academic-paper + Style Calibration) | researchwrite |
| S10 架构/算法/机制图 | engineering-figure-agent | nature-figure（GPT Image 2 路由，需 OPENAI_API_KEY）、markdown-mermaid-writing |
| S11 排版/模板/参考文献 | venue-templates、nature-ref-verifier、academic-research-suite(citation-format-switcher)、visual-pdf-review（编译后视觉验收） | academic-research-suite(academic-paper format-convert) |
| S12 三轮连带审查 | research-tree-search（编排）、academic-research-suite(academic-paper-reviewer)、visual-pdf-review（视觉排版维度） | — |
| S13 去 AI 味 | academic-research-suite(Writing Quality Check) | researchwrite（anti-slop） |

调用约定：技能名可用 `$技能名` 显式引用；备用技能仅在主用不可用时使用；同一功能的多技能以路由表为准，不并行混用。

## 阶段协议

- **阶段收尾（所有门禁阶段）**：完成 S2/S3/S4/S5/S5S6/S6/S7/S9/S11/S12/S13 后，运行
  `python3 .codex/hooks/gate_check.py --pending --stage <Sx> --project <id>` 布防门禁；
  Stop 钩子自动复检，不合格自动返工（默认最多 3 轮）。钩子未启用时，进入下一阶段前必须
  `--check` 拿到 PASS，禁止跳过门禁。布防前先 `graph_evolve.py scan --project <id>`
  同步图谱，判断边候选提醒用户 `review`（机械边自动入图，判断边必须用户确认）。
- **S6 工程实现与实验矩阵设计**：读取并登记项目实验协议（数据划分、随机/分层策略、指标、早停、统计口径；协议缺失先补齐，禁止假设默认值）→ 冻结 `matrix.md`（方法 × 任务/数据集 × 指标，状态 `design`，每格含结构、模块、特征、超参范围、协议引用）→ 冻结基线策略（逐条标注 `reproduce`：无已发表数字或必须本地跑的方法；`cite_published`：已有已发表数字的基线默认采用原文报告的数字，注明来源、不写复现代码、不要求同协议；`excluded`：与对比叙事无关的方法，不跑不引并记录原因）→ 按矩阵实现代码（数据/特征 → 模型 → 训练 → 评估；只有 `reproduce` 基线需要实现）→ 冒烟验收（shape、loss 下降、无 NaN、同随机策略结果一致、指标计算正确）→ 三轮自我检查（逐条对照矩阵规格与实现红线，每轮至少“找问题 → 修 → 复验”，不允许一轮宣称通过）→ 产出验收报告（每条 PASS/FAIL + 证据 + 剩余风险）→ `graph_evolve.py scan --project <id>` 登记矩阵节点；全部 PASS 后矩阵转 `pending`，否则继续修复并重走冒烟。
- **S7 实验运行与参数优化闭环**：pilot 试运行（小规模，只验证运行时间/资源/稳定性，不出结论）→ 基线按 S6 策略执行（`reproduce` 才本地跑；`cite_published` 核验引用；`excluded` 不跑）并建立 go/no-go 参照 → 优化闭环（调参、消融、go/no-go 只在 pilot 数据上做，防泄漏；达到最大轮数或连续提升低于阈值立即停止并记录原因）→ 锁定配置快照 → canonical 正式评估（按项目协议完整执行，禁止实时调参）→ 台账回写（结果、命令、日志、claims、统计审核、用户抽查复现）→ `graph_evolve.py scan` + `review` 同步结论节点与矛盾边（`supersedes`/`contradicts` 必须用户确认）。达标进 S8/S9；不达标写 go/no-go 记录（原因 + 退回目标），按记录回 S2–S5。
- **S9 写作（保真门禁）**：动笔前读 narrative one-pager，按 researchwrite 保真协议建 evidence ledger 与 section function map（缺证据标 blocked，不编内容）；用户提供目标期刊/范文时先建 journal style card（target-journal-model，默认 ml_cv_nlp 基础规则），**用户确认后**逐节写；图谱中每个内部 `contradicts` 边都必须在正文有明确回应（`edge respond --where <位置>`），回写后再跑 `nature-proposal-writer/scripts/check_preservation.py` + 人工语义审计，输出契约（成稿 → Key changes → Preservation audit → Author queries）全过才算完成。
- **S11 排版流程**：先 venue-templates 生成目标期刊/会议模板骨架 → 正文与图表嵌入 → nature-ref-verifier 核验参考文献 → academic-research-suite 的 citation-format-switcher 转换格式 → 编译后用 visual-pdf-review 做视觉验收与一致性检查。投稿前另跑机械检查清单（LaTeX 引用/标签/公式卫生、AI 味词频、摘要完整性、段落形状、图注质量）；投稿信生成后做 align-check——信中每个 claim 必须能在正文找到证据，防过度声称。
- **S13 去 AI 味闭环**：先跑保全审计（`check_preservation.py` + 人工核对数字/引用/术语/claim 强度，防止去味改变科学内容）→ Writing Quality Check 检测（AI 高频词、em dash 数量、分号密度、throat-clearing 开头、过度声称）→ 按 Style Calibration 改写 → 再次 WQC 复检 + 保全复核，直到通过；可用 researchwrite 的 anti-slop 参考做补充。注意：目标是"清晰、精确、多样化的专业学术写作"，不是欺骗 AI 检测器，不引入人为同义词替换等 humanizer 行为。
- **S12 三轮审查编排**：由 research-tree-search 执行：第 1 轮完整审查 → 修订 → 第 2 轮 re-review → 修订 → 第 3 轮终检 + visual-pdf-review 视觉排版维度 + 生成返修材料。收敛标准：内容无 P1 问题、P2 低于阈值，且视觉审稿无 P0/P1 排版问题。
- **S3 查新**：任何"我觉得这个 idea 新"的判断，都必须先跑 novelty-sweep；有界检索无结果不构成新颖性证据。


## 图表标题约定（强制）

- Figure 的标题/图注在正文中、图的下方；Table 的标题在正文中、表的上方（由 S11 排版写入 \caption/表头）。
- S8/S10 出图时，图内只保留坐标轴标签、刻度、必要图例；禁止把 "Figure N"、标题、大段图注画进图片像素。若示意图草稿带标题文字，排版前须重画或裁掉。

## S6 实现纪律（强制）

- 禁止降级简化：核心模块必须真实接入 forward，禁止用近似实现冒充（如全注意力加 mask 冒充稀疏注意力）、层数/维度悄悄缩水、组件实际不生效。
- 禁止虚假实现：占位逻辑、写死输出、跳过组件、指标定义被悄悄替换、结果硬编码。
- 禁止不可复现：随机策略不生效、数据泄漏、配置与日志不落盘。
- 基线复现边界：只有标记 `reproduce` 的基线才写实现；`cite_published` 不写复现代码，`excluded` 不实现不运行。
- S6 验收报告全 PASS 前，实验矩阵不得进入 S7 运行。

## 学术诚信红线（所有阶段强制）

1. 引用必须真实：每条参考文献经 nature-ref-verifier 或等价手段核验；禁止编造 DOI/页码。
2. 数据与结果不得虚构：实验必须真实运行，结果回写 .research/ 台账并保留复现记录；AI-Scientist 已知失败模式（结果编造、bug-as-insight、方法论编造、引用幻觉）在每轮实验后对照检查。
3. 每篇论文投稿前：关键实验至少 1-2 个由用户人工抽查复现。
4. 明确告知用户哪些内容由 AI 生成、哪些需要人工核验；不隐瞒 AI 使用。
