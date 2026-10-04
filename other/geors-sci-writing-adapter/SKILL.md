---
name: geors-sci-writing-adapter
description: "地理学与遥感 SCI 写作适配 skill。用于地理/遥感/城市暴露/体育公园与绿地暴露论文的英文写作、章节重构、标题摘要、Introduction gap chain、Methods 数据与空间流程叙述、Results 结果解释、Discussion 机制与局限、Conclusion、cover letter 和投稿前检查。适合遥感定量反演、时空变化分析、绿色暴露、热暴露、体育设施可达性、空间公平、城市健康、GIS/RS 论文写作。该 skill 是对 xiangyu-Ge/sci-writing-geors 思路的原创 Codex 适配；因上游未声明明确许可证，不复制上游参考全文，只保留来源说明和本地原创工作流。"
---

# GeoRS SCI Writing Adapter

本 skill 面向地理学、遥感、城市暴露、体育地理和空间公平论文写作。它的定位不是通用润色，而是把你的研究问题、空间方法、遥感/GIS 指标、统计结果和期刊叙事组织成可投稿的英文 SCI 论文。

## 使用边界

- 适合：地理/遥感 SCI 论文、绿地/热暴露、体育公园或体育设施可达性、空间公平、城市健康、遥感定量反演、时空变化分析、GIS 方法叙述、cover letter。
- 不适合：编造文献、替换真实结果、把相关写成因果、绕过目标期刊近作校准、复制未授权上游文本。
- 上游 `xiangyu-Ge/sci-writing-geors` 未发现明确 LICENSE。本地封装采用原创说明与工作流，不复制其 `references/` 全文。

## 先判定论文类型

收到写作任务后，先把论文放入一个主类型；如果是组合论文，标注主线和副线。

| 类型 | 核心问题 | 写作重点 |
|---|---|---|
| 遥感定量反演 | 用遥感和辅助变量估计某个地表/土壤/环境属性 | 数据源、样本设计、特征构建、模型验证、不确定性、空间外推边界 |
| 时空变化分析 | 某种地表过程如何变化、在哪里变化、为什么变化 | 趋势检测、空间格局、驱动因子、尺度效应、归因确定性 |
| 暴露与可达性 | 绿地、热环境、公园或体育设施如何影响人群机会或健康 | 暴露窗口、空间单元、可达性算法、人群权重、公平性和机制 |
| 方法或模型比较 | 哪种模型/指标/空间尺度更稳健 | baseline、验证切分、稳健性、可解释性、可复现性 |

若用户没有说明目标期刊，默认询问目标期刊或期刊族。没有目标时，按 `Cities / Sustainable Cities and Society / UFUG / RSE / ISPRS J P&RS / TGRS / IJRS / JAG / Catena / Geoderma` 的风格差异给出通用版。

## 工作流

1. 确认输入：论文类型、目标期刊、研究对象、数据来源、主要结果、需要处理的章节、语言方向和修改幅度。
2. 建立 claim-evidence map：每个段落先说明要证明什么，再说明支撑它的数据、图表或文献。
3. 选择章节 playbook：标题/摘要/引言/方法/结果/讨论/结论/投稿信分别处理。
4. 写作或改写：保留事实、数值、方向、引用键和方法边界；只改善结构、逻辑和表达。
5. 自检：检查因果语言、空间尺度、暴露/可达性/可用性/使用混淆、期刊定位、图表与 claim 的对应关系。
6. 科学内容稳定后，调用共享 `agent-auto-sci-scicomm/references/academic_prose_style_guard.md`，检查正向优先表达、防御性对照 cluster 和同一边界的语义重复；不得因此弱化方法、因果或不确定性边界。
7. 交付：给出改后文本、修改理由、仍需用户确认的数据/文献/期刊规范。

Academic Prose Style Guard 是写作 QC，不是 primary research router。它适用于本文 skill 生成的 manuscript prose、Discussion、Introduction、Conclusion、Abstract、rebuttal 和 substantial academic interpretation。

## 参考文件

读 `references/geors-writing-playbook.md` 获取详细章节写法、常见句段功能、投稿前检查表和与本仓库其他 skill 的协作方式。
