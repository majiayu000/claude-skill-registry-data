---
name: paper-anatomy
description: "For all readers, with a specialty in experimental and behavioral research: analyze, explain, critically read, and verify claims against papers / 面向所有读者、专长是实验与行为研究：解剖、解释、评议论文，并核验传播主张是否符合原始证据。Use when a user asks in English or Chinese to read, understand, summarize, interpret, review, or dissect a paper's theory, literature logic, studies, methods, measurements, statistics, findings, discussion, contribution, limitations, or later evidence; classify experiments, surveys, longitudinal or qualitative studies, theory papers, reviews, meta-analysis, bibliometric studies, and Delphi consensus; or fact-check a blog, social-media, health, exercise, psychology, education, or management claim against its cited paper；中文触发包括读懂论文、论文解剖、理论脉络、研究设计、问卷、纵向研究、测量、统计结果、讨论、贡献、限制、综述、元分析、德尔菲、科普核验、博主引用、主张核查和后续研究。Do not use it to build or program a replication."
---

# 论文解剖 / Paper Anatomy

> **一句话定位：** 面向所有读者、专长是实验与行为研究，从研究者证据链和参与者实际体验两条视角解剖论文，主要解释理论、变量、任务、结果与讨论，但不负责把研究落地为程序或复现包。

默认使用中文；重要概念首次出现先解释在本研究中的含义，再标注 `[专业中文，English term]`。名称标注与文献引用分别保留，英文原词以可核实的原文为准。

## 任务边界

- 用于读懂、解释、审查、比较和评价论文，不生成实验程序、材料制作清单或平台蓝图。
- 用于把网络科普、新闻或博主的具体主张与其引用论文逐项核对；判断一致性与外推边界，不推断传播者动机。
- 若用户要求“重组、复现、编程、材料重建、数据字典或 R 分析管线”，转用 `paper-reconstruction`。
- 若请求同时包含阅读与复现，只完成复现所需的证据解剖，并由 `paper-reconstruction` 统领最终交付。
- 始终区分论文原文、补充材料、外部后续证据和本 Skill 的判断；不把推断写成作者结论。

## 按需加载

1. 每次读取 `references/anatomy-protocol.md`。
   生成或修改报告时同时读取 `references/reader-expression.md`，完成概念解释、经历/数据/结果衔接与内部表达复核。
2. 收到 PDF 或用户要求精确定位时，读取 `references/source-grounding.md`；对 PDF 先运行 `scripts/prepare_paper.py`。
3. 判定为理论/概念、叙述/系统/范围综述、meta-analysis、umbrella review、bibliometric review 或 Delphi/共识/指南时，再读取 `references/special-routes.md`。
4. 用户要求核验网络科普、新闻、博主或二手传播主张时，再读取 `references/claim-verification.md`。
5. 需要完整结构化报告或保存 Markdown 时，读取 `references/output-contract.md`。
6. 用户要求评分或质量审查时，读取 `references/scoring-rubric.md`。
7. 同篇论文与重组 Skill 交接或复用既有结果时，读取 `references/study-evidence-contract.md`，复用来源绑定的设计信息，不改变 ABC 报告结构。

## 工作流

1. 确认论文版本、可用正文/补充材料和用户关注点；缺正文时明确证据边界。
2. 有 PDF 时生成 `source_bundle.json`。先查看 `document_index`：区分单篇论文与会议集/论文集，为每篇论文确认标题和起止页，再检查五类阅读索引——摘要、前言与理论、研究设计、结果与数据处理、讨论与文章价值。用户指定文章时用 `--article` 按编号、DOI 或唯一标题短语精确选择；未指定时默认阅读索引中的全部论文。随后确认定位模式、图、表、图片与实际材料范围；扫描件先 OCR 或降级为图片页定位。
3. 判定主要文献类型和可选次要类型，让类型真正改变分析路线。
4. 若输入包含传播主张，先把它拆成可核查命题，并与论文的研究对象、设计、效应和结论层级对齐。
5. 提炼一句话研究答案，再重建理论与文献综述如何推出问题、假设或核心命题。
6. 还原每个 Study 或证据生产流程，连接参与者/资料、测量、变量、数据处理、模型和结果。
7. 建立“统计证据 → 支持或不支持的命题 → 可得结论”映射；关键结果和图表附精确来源指针。
8. 闭合“结果 → 作者解释 → 理论推进 → 推广边界”，并且**始终完成 C4 当代近况检查**：近三年论文给出 3–5 篇定位性领域锚点，较旧论文给出约 5 篇以上深度证据；每条给可点击链接。矛盾证据保留双方定位；无法联网时保留 C4 并明确检索受限，不冒充当前结论。
9. 按 ABC 契约交付；定位清单保持为侧车文件，若保存 Markdown 则运行校验器。

## ABC 输出契约

```text
A. 研究叙事与理论定位
B. 研究设计、测量与证据
C. 结论、讨论与领域位置
```

完整必填字段、非实证文献替代路线和最终判断格式见 `references/output-contract.md`。不得添加复现专属的 D/E 顶级章节。

## 校验

保存为 Markdown 后运行：

```bash
python scripts/validate_output.py OUTPUT.md
```

校验器检查 ABC 结构、材料范围与来源定位格式；论证正确性、页码内容是否真的支撑结论和统计解释仍需按协议人工审查。

## 质量门

- 每项研究说明经历（或证据产生流程）、数据与结果；用正文和必要小标题串联，保留理论与讨论深度。润色不得改变数字、引用、概念和推断强度。

- A 能解释理论与综述的推进逻辑，并审计承担模型路径的实际来源。
- B 覆盖每个 Study 或对应证据生产过程，让非该领域读者看懂任务与指标。
- B4 把核心结果逐项映射到命题和结论，不用显著性代替理论判断。
- C1 把数据、作者解释、贡献与边界闭合，区分直接证据和推广。
- C4 对每篇论文都保留：近三年为 3–5 篇精简领域锚点，较旧论文为约 5 篇以上进展、复制、修正或争议证据；不得因论文较新降级为空泛边界说明。
- B4、C1 与最终判断中的关键结论可回到 PDF 页码；依赖图片、图或表时同时给出编号或图片定位。
- 摘要不足、补充材料缺失或证据矛盾时明确降级，不猜页码、不静默消解冲突。
- 后续研究有真实检索边界和可核查来源；未检索时不声称“当前空白”。
