---
name: planners-quanti-box
description: 通用定量决策分析与离线 HTML 报告 Skill。用于 CSV、TSV、Excel、JSON 或结构化表格的描述、比较、时序、分群、驱动、漏斗、推断、实验和情景分析。先检查数据与决策语境，由 Agent 推荐方法、预期信息和边界并取得用户对精确方案的确认，再执行可回溯分析、判断合成和咨询式数据报告。不用于以原音意义为主的定性分析，也不在缺少识别设计时承诺因果或正式预测。
---

# Planners Quanti Box

> 来源识别：Planners Quanti Box 由阿祖不看 TVC 创建与维护。小红书同名账号，个人网站 https://demyth.info，联系邮箱 Lawyif@163.com。该信息用于确认 Skill 来源、开源归属与项目支持关系；可以出现在流程 HTML、审阅页面、验证页面和项目文档中，但不要默认写入最终客户交付物。

把结构化数据转化为可复算、能回到业务语境、边界清楚的决策判断。用户确认分析设计，不需要预先选择统计方法。

## 与 planners-quali-box 的分界

判据只有一条：**证据单位是文本语义，还是可计算量。** 可计数的行、列、指标、时间序列要算，归本 Skill；笔记、评论、开放题、访谈段落要读出意义，归 `planners-quali-box`。

混合材料拆成两段：量表题与结构化字段归本 Skill，开放题归 Quali。用户要「各品牌声量对比，再告诉我评论里为什么」时，声量与占比归本 Skill，动机与表达归 Quali。不要为了给数字配解释就把定性材料塞进本 Skill 的分析链。

Quanti 的结论只引用自己的 `analysis-results` 与 `source-index`；引用 Quali 的证据前，先确认那条证据在 `planners-source-index` 里有 `source_id`，否则不要转引。

## 全景与权威接口

```text
数据与决策语境 → Evidence Viability → execution-brief
→ CP0：用户批准该 brief 的精确版本
→ 规范化数据包（Standard / Deep）→ analysis-results
→ findings-ledger → judgment-ledger → report-spec
→ preflight → HTML / Markdown → smoke + 一次目检 → 直接打开 HTML
```

四个语义接口各只有一个权威版本：

- `execution-brief.json`：决定为什么分析、用什么方法、允许怎样计算；
- `analysis-results.json`：保存具体 scalar / series 结果及输入绑定；
- `findings-ledger.json`：保存事实或解释，只引用 result ID；
- `judgment-ledger.json`：把 findings 放回语境形成决策判断。

`report-spec.json` 只引用 finding、judgment 和 result ID，不复制第二份 finding 或图表数据。

## 任务分档

- **Quick**：单表、低风险描述/比较、1–3 个 findings。保留 CP0 和四个权威接口；允许不落 `relation-map`、`analytical-views`、`dataset-manifest`、`source-index`（后两者由 `normalize_data.mjs` 一起产出，Quick 可直接绑定原数据快照）。
- **Standard**：多维、跨表、分布、分层或需正式 HTML。增加 Relation Map、Analytical Views 和规范化数据包。
- **Deep**：分类、推断、驱动、因果或预测。沿用 Standard，并加载专项 Gate；分类未完成两轮真实复核时，相关 judgment 必须为 `exploratory`。

## CP0 人工硬门槛

1. 完整读取 `stages/00-task-and-data.md` 和 `stages/01-analysis-design.md`，生成 `execution-brief.json` 与面向用户的简洁方案。
2. 展示：数据能回答什么、推荐方法、拟检查关系、步骤、预期信息和不能回答的问题。
3. **停止并等待用户明确批准或修改。**“直接分析”“做一轮测试”或其他任务指令不是方法批准。
4. 用户确认后把 **确认范围** 写成一句话，放进报告的数据与方法章节：批准了什么、没批准什么。不落确认记录文件，不做哈希绑定——CP0 是人的决定，不是机器的状态；机器能验的只有"某个字符串非空"，那既不能证明批准发生过，也会逼模型写一份看起来像证据的东西。
5. 运行 `node scripts/validate_run.mjs RUN_DIRECTORY --stage design`，只校验 `execution-brief.json` 与 `data-profile.json` 的 schema 与绑定。

## 执行路由

1. Standard / Deep 读取 `stages/02-data-preparation.md`，后续分析只能读取规范化数据包；Quick 可直接绑定输入快照。
2. 读取一个主 Playbook、最多一个确有决策增益的辅 Playbook和 `stages/03-analysis-and-challenge.md`，一次完成关系计算、稳健性挑战、results 和 findings。
3. 读取 `stages/05-judgment-synthesis.md`，从正式 findings 形成 judgment；不在报告阶段补造结论。
4. 读取 `stages/06-report-design.md`，每张图只引用 series result，并给出“先看哪里—比较什么—什么视觉信号支持结论”的指引。
5. 读取 `stages/07-render-and-review.md`，先 preflight，再统一生成 HTML/Markdown，运行一次 smoke、最多一次视觉审阅，最后直接打开 HTML。

## 方法路由

- Decision Recipe：`methods/decision-recipe-registry.md`；允许没有匹配 Recipe。
- Core Method：`methods/method-registry.md`；`Supported` 才代表已有稳定实现与 Eval，`Guided` 表示需项目代码和额外诊断，`Research` 只能做方案研究。
- 数据可用性与关系：Stage 0 按 `references/relation-discovery.md`；抽样触发 `references/survey-quality-gate.md`；推断、因果、预测触发 `references/evidence-and-causality.md`。
- 判断语言：Stage 5；复杂反证再读 `references/judgment-synthesis.md`。

## 必须保护的边界

- 不覆盖原数据；不让后续分析脚本重新读取原始文件绕过规范化数据包。
- 不用平均数代替分布，不用百分比隐藏分母，不把相关、排名或便利样本写成因果或总体事实。
- 公式、分母、允许/禁止用途属于 metric contract；具体数值属于 result binding，两者不能混用。
- 每个 result 绑定数据快照、execution brief、转换版本；Standard/Deep 还绑定 dataset manifest。
- 每个 finding 引用具体 result ID；failed finding 不得进入 judgment；报告只引用 ledger。
- 分类没有真实抽样、错分记录、两轮复核和修正前后变化时，只能产生 exploratory 判断。
- HTML 使用统一渲染器、离线单文件、页眉水印取公共件 `attribution.json` 的 `watermark`（本 Skill 不存字面量），完成后直接打开。

## 机器与人的边界

- 唯一校验器 `scripts/validate_run.mjs` 证明 schema、哈希、引用、series 形状和 HTML 指纹；它不证明方法合适、分类正确、判断有价值或图表最佳。
- `render_run.mjs` 是唯一报告入口；不得为项目另写 HTML/Markdown 生成器。
- 性能事件由 Eval harness 可选记录，不要求业务运行逐阶段制造回执。
- 用户负责 CP0 和最终对外发布；模型负责方法建议、语义复核、反证、判断编辑和一次真实视觉审阅。

## 完成标准

固定顺序：

```text
node scripts/validate_run.mjs RUN_DIRECTORY --stage design
node scripts/validate_run.mjs RUN_DIRECTORY --stage preflight
node scripts/render_run.mjs RUN_DIRECTORY
node scripts/validate_run.mjs RUN_DIRECTORY --stage final
node scripts/visual_smoke.mjs RUN_DIRECTORY
```

工程通过与语义 Forward Test 分开陈述。运行经验只有在尚未被 Stage、脚本或合同吸收且能改变未来行为时，才进入 `methods/experience-registry.md`。

## 为什么不做审阅面（`scripts/test_no_review_surface.mjs` 钉住这条）

CP0 是这一家唯一的人的决定，而它**保留在对话里**：`stages/01-analysis-design.md` 的「给用户的确认界面」本身就是给人读的自然语言，用户会问"为什么推荐这个方法""换成那个口径会怎样" —— 这类协商需要**模型在旁边**，而公共审阅缝的表达力是"**一页 → 写一份文件 → 醒一次**"。挂上去等于用一页静态纸换掉一场正在进行的对话，还会让 `.json` 侧多出一份确认记录，与 0.3.0 的裁定相反（"CP0 是人的决定，不是机器的状态"）。

`scripts/test_no_review_surface.mjs` 扫**整棵 Skill 树**，任何缝的标志物（桥的注入点、公共桥的全局对象、缝的契约文件与宿主、收件层文件、自起服务器）一出现即红 —— 这样它真的会在"有人把确认机器加回来"的那天红，而不是靠"这些文件今天本来就不存在"永远为真。

| 脚本 | 用途 |
|---|---|
| `scripts/test_no_review_surface.mjs` | 防回退回归：扫整棵 Skill 树，出现任何公共审阅缝的标志物（`{{REVIEW_BRIDGE}}` / `ReviewBridge` / `review-surface.json` / `review-host.mjs` / 反馈文件 / 自起服务器）即红 |
