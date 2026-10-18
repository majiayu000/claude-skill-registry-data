---
name: business-user-research
description: Plan, conduct, and synthesize user research. Trigger with "user research plan", "interview guide", "usability test", "survey design", "research questions", or when the user needs help with any aspect of understanding their users through research.
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# User Research

Help plan, execute, and synthesize user research studies.

## Research Methods

| Method | Best For | Sample Size | Time |
|--------|----------|-------------|------|
| User interviews | Deep understanding of needs and motivations | 5-8 | 2-4 weeks |
| Usability testing | Evaluating a specific design or flow | 5-8 | 1-2 weeks |
| Surveys | Quantifying attitudes and preferences | 100+ | 1-2 weeks |
| Card sorting | Information architecture decisions | 15-30 | 1 week |
| Diary studies | Understanding behavior over time | 10-15 | 2-8 weeks |
| A/B testing | Comparing specific design choices | Statistical significance | 1-4 weeks |

## Interview Guide Structure

1. **Warm-up** (5 min): Build rapport, explain the session
2. **Context** (10 min): Understand their current workflow
3. **Deep dive** (20 min): Explore the specific topic
4. **Reaction** (10 min): Show concepts or prototypes
5. **Wrap-up** (5 min): Anything we missed? Thank them.

## Analysis Framework

- **Affinity mapping**: Group observations into themes
- **Impact/effort matrix**: Prioritize findings
- **Journey mapping**: Visualize the user experience over time
- **Jobs to be done**: Understand what users are hiring your product to do

## Deliverables

- Research plan (objectives, methods, timeline, participants)
- Interview guide (questions, probes, activities)
- Synthesis report (themes, insights, recommendations)
- Highlight reel (key quotes and observations)
