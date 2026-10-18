---
name: business-job-stories
description: "Create job stories using the 'When [situation], I want to [motivation], so I can [outcome]' format with detailed acceptance criteria. Use when writing job stories, creating JTBD-style backlog items, or expressing user situations and motivations."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# Job Stories

Create job stories using the 'When [situation], I want to [motivation], so I can [outcome]' format. Generates stories with detailed acceptance criteria focused on user situations and outcomes.

**Use when:** Writing job stories, expressing user situations and motivations, creating JTBD-style backlog items, or focusing on user context rather than roles.

**Arguments:**
- `$PRODUCT`: The product or system name
- `$FEATURE`: The new feature to break into job stories
- `$DESIGN`: Link to design files (Figma, Miro, etc.)
- `$CONTEXT`: User situations or job scenarios

## Step-by-Step Process

1. **Identify user situations** that trigger the need
2. **Define motivations** underlying the user's behavior
3. **Clarify outcomes** the user wants to achieve
4. **Apply JTBD framework:** Focus on the job, not the role
5. **Create acceptance criteria** that validate the outcome is achieved
6. **Use observable, measurable language**
7. **Link to design mockups** or prototypes
8. **Output job stories** with detailed acceptance criteria

## Story Template

**Title:** [Job outcome or result]

**Description:** When [situation], I want to [motivation], so I can [outcome].

**Design:** [Link to design files]

**Acceptance Criteria:**
1. [Situation is properly recognized]
2. [System enables the desired motivation]
3. [Progress or feedback is visible]
4. [Outcome is achieved efficiently]
5. [Edge cases are handled gracefully]
6. [Integration and notifications work]

## Example Job Story

**Title:** Track Weekly Snack Spending

**Description:** When I'm preparing my weekly allowance for snacks (situation), I want to quickly see how much I've spent so far (motivation), so I can make sure I don't run out of money before the weekend (outcome).

**Design:** [Figma link]

**Acceptance Criteria:**
1. Display Spending Summary with 'Weekly Spending Overview' section
2. Real-Time Update when expense logged
3. Progress Indicator (progress bar showing 0-100% of weekly budget)
4. Remaining Budget Highlight in prominent color
5. Detailed Spending Log with breakdown by category
6. Notifications at 80% budget threshold
7. Weekend-Specific Reminder at 90% by Thursday evening
8. Easy Access and Navigation to detailed breakdown

## Output Deliverables

- Complete set of job stories for the feature
- Each story follows the 'When...I want...so I can' format
- 6-8 acceptance criteria focused on outcomes
- Stories emphasize user situations and motivations
- Clear links to design and prototypes

---

### Further Reading

- [Jobs-to-be-Done Masterclass with Tony Ulwick and Sabeen Sattar](https://www.productcompass.pm/p/jobs-to-be-done-masterclass-with) (video course)
