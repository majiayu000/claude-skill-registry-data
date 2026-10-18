---
name: business-release-notes
description: "Generate user-facing release notes from tickets, PRDs, or changelogs. Creates clear, engaging summaries organized by category (new features, improvements, fixes). Use when writing release notes, creating changelogs, announcing product updates, or summarizing what shipped."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

## Release Notes Generator

Transform technical tickets, PRDs, or internal changelogs into polished, user-facing release notes.

### Context

You are writing release notes for **$ARGUMENTS**.

If the user provides files (JIRA exports, Linear tickets, PRDs, Git logs, or internal changelogs), read them first. If they mention a product URL, use web search to understand the product and audience.

### Instructions

1. **Gather raw material**: Read all provided tickets, changelogs, or descriptions. Extract:
   - What changed (feature, improvement, or fix)
   - Who it affects (which user segment)
   - Why it matters (the user benefit)

2. **Categorize changes**:
   - **New Features**: Entirely new capabilities
   - **Improvements**: Enhancements to existing features
   - **Bug Fixes**: Issues resolved
   - **Breaking Changes**: Anything that requires user action (migrations, API changes)
   - **Deprecations**: Features being sunset

3. **Write each entry** following these principles:
   - Lead with the user benefit, not the technical change
   - Use plain language — avoid jargon, internal codenames, or ticket numbers
   - Keep each entry to 1-3 sentences
   - Include visuals or screenshots if the user provides them

   **Example transformations**:
   - Technical: "Implemented Redis caching layer for dashboard API endpoints"
   - User-facing: "Dashboards now load up to 3× faster, so you spend less time waiting and more time analyzing."

   - Technical: "Fixed race condition in concurrent checkout flow"
   - User-facing: "Fixed an issue where some orders could fail during high-traffic periods."

4. **Structure the release notes**:

   ```
   # [Product Name] — [Version / Date]

   ## New Features
   - **[Feature name]**: [1-2 sentence description of what it does and why it matters]

   ## Improvements
   - **[Area]**: [What got better and how it helps]

   ## Bug Fixes
   - Fixed [issue description in user terms]

   ## Breaking Changes (if any)
   - **Action required**: [What users need to do]
   ```

5. **Adjust tone** to match the product's voice — professional for B2B, friendly for consumer, developer-focused for APIs.

Save as a markdown document. If the user wants HTML or another format, convert accordingly.
