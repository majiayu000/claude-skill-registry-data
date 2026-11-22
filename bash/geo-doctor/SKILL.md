---
name: geo-doctor
description: 'Full GEO program: route a generative engine optimization request to the right focused skill and run the loop end to end. Use when the user says help me with GEO, wants AI assistants to recommend their software, product, site or mini program, asks for the whole process rather than one step, does not know where to start, or wants a weekly automated retest. Holds the intake, the process, the evidence rules and the autopilot. GEO doctor. For one step only, use ai-crawler-audit, ai-visibility, ai-content-writer, llms-txt or geo-publish directly.'
license: MIT
metadata:
  version: "1.8.0"
  homepage: https://github.com/Fangx-AI/geo-doctor
---

# GEO 医生（总纲）

病人是用户的**软件、产品、网站或小程序**；病症是"AI 不提它、说错它、推荐了别人"。这个技能是**分诊台 + 病历 + 复查制度**：判断现在该做哪一步，把具体工作交给对应的专科技能。

用用户的语言交流；本文件是中文的，读懂后用用户的语言转述。

## 什么时候用

- "帮我做 GEO" / "让 AI 推荐我的产品"（没说具体做哪一步）
- 要一条完整流程，或要每周自动复查
- 已经做了一半，不清楚下一步该干什么

用户点名某一步时，**直接去对应技能，不要从头走一遍**。

## 分诊表

| 用户的问题 | 去哪个技能 | 主要产出 |
| --- | --- | --- |
| AI 爬虫能不能读到我的页面 | `ai-crawler-audit` | `geo/audit.md` |
| AI 到底提不提我、推荐了谁 | `ai-visibility` | `geo/questions.csv`、`geo/runs.csv`、`geo/diagnosis.md` |
| 该写什么、AI 说错我的信息 | `ai-content-writer` | `geo/fact-card.yaml`、`geo/drafts/` |
| llms.txt、给 AI 读的站点 | `llms-txt` | `dist/` 站点、`facts.json` |
| 发到哪、怎么发、发完记账 | `geo-publish` | `geo/publish-plan.md`、`geo/outbox/`、`geo/published.csv` |

完整顺序是：**问诊 → 体检 → 事实卡 → 问题集 → 采样 → 诊断 → 写内容 → 发布 → 复查**。但不是每次都全走：已经有事实卡就不用重建，已经测过就先去诊断。

## 三条铁律（所有技能共用，任何一步都不能违反）

1. **只用事实。** 只用用户提供的材料和实际查到、能给出处的信息。不编造价格、功能、客户、案例、数据、评价；缺资料写"未知"并列出要补什么。
2. **不承诺结果。** 没人能保证任何 AI 推荐谁，推荐也买不到。效果只用复查数据说话，并写明问了几题、每题几次、哪个入口。
3. **不做投毒。** 不批量生成同质化软文，不编造用户评价和"真实体验"，不教刷评、养号、站群。细节见 [references/compliance.md](references/compliance.md)。

另外三条口径，写报告时必须分开：**发布成功 ≠ AI 提到你 ≠ AI 推荐你 ≠ AI 引用你**；AI 没回答（拒答、超时、报错）不记为"未提及"；API 的回答不冒充用户在 App 里看到的回答。

## 第 0 步：问诊

一次最多问 3 个问题，能从上下文或网站推断的不问：

1. **对象**：软件、App、网站、小程序还是产品？名称和网址？
2. **目标 AI 与市场**：国内还是海外？最想被哪个 AI 推荐？默认只做用户说的那一个；没说时，国内从豆包或 DeepSeek 开始，海外从 ChatGPT 开始，不要一上来全做。
3. **目标用户**：谁会用？他们最常遇到什么问题？

有联网能力就调研行业（同类产品、用户在哪讨论、有没有资质或广告限制），只记录能给出处的内容。写成 `geo/case.md`（病历），然后告诉用户"接下来先做体检"。

## 周更与批处理

`scripts/geo-autopilot.mjs`（零依赖）把重复劳动自动化：

```bash
node scripts/geo-autopilot.mjs gaps                          # 最近一批采样里，竞品被推荐得比我多的题
node scripts/geo-autopilot.mjs write --ai deepseek --max 3   # 给缺口题各写一篇，只用已确认事实
node scripts/geo-autopilot.mjs report                        # 推荐率趋势、逐题变化、未补的缺口
node scripts/geo-autopilot.mjs weekly --pr-body pr.md        # 采样→写稿→出报告，附 PR 说明
node scripts/geo-autopilot.mjs action                        # 写一个每周一自动跑并开 PR 的工作流
```

`write` 默认产出 draft；加 `--ready` 才把无错误的稿子标为 confirmed（供 PR 审核，合并即同意发布）。API Key 只从环境变量读。**自动开的 PR 要人审过才合并**，不要设置为自动合并。

## 运行环境与资源

- 以本 `SKILL.md` 所在目录为技能根；各专科技能的脚本和模板在它们自己的目录里，不要当成用户项目的路径。
- 根据实际能力选择执行方式，**不按平台名称假定能联网、能跑命令或能写文件**。不能写文件时，在对话里按目标文件名给出完整可复制内容并注明"待保存"；不能跑脚本时，做该步能做的人工检查，未检查项标"未验证"，**不编造得分**。
- 缺参考文件时说明缺哪个，请用户补全技能包；不要假装读过。
- 用户只收到链接或粘贴文本，不等于已经装好技能。

## 每一步结束时

用 3 到 5 行说明：做了什么、最重要的发现、下一步做什么、需要用户提供什么。详细内容写进 `geo/` 的文件，不要把长篇报告塞进对话。
