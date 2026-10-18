---
name: business-stakeholder-map
description: "Build a stakeholder map using a power/interest grid, identify communication strategies per quadrant, and generate a communication plan. Use when managing stakeholders, preparing for a launch, aligning cross-functional teams, or planning stakeholder engagement."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

## Stakeholder Mapping & Communication Plan

Map stakeholders on a Power × Interest grid and create a tailored communication plan for each group.

### Context

You are helping build a stakeholder map for **$ARGUMENTS**.

If the user provides files (org charts, project briefs, team rosters), read them first. If they describe the product or initiative, use that context to infer likely stakeholders.

### Instructions

1. **Identify stakeholders**: List all relevant individuals and groups — executives, engineering leads, designers, marketing, sales, support, legal, finance, external partners, and end users.

2. **Classify each stakeholder** on two dimensions:
   - **Power** (High/Low): Their ability to influence decisions, resources, or outcomes
   - **Interest** (High/Low): How much the project directly affects them or how engaged they are

3. **Place stakeholders in the Power × Interest grid**:

   | | High Interest | Low Interest |
   |---|---|---|
   | **High Power** | **Manage Closely** — Regular 1:1s, involve in decisions, seek their input early | **Keep Satisfied** — Periodic updates, escalate only critical issues |
   | **Low Power** | **Keep Informed** — Regular status updates, invite to demos, gather feedback | **Monitor** — Light-touch updates, available on request |

4. **For each quadrant**, recommend:
   - Communication frequency (daily, weekly, bi-weekly, monthly)
   - Communication format (1:1, email, Slack, meeting, dashboard)
   - Key messages and framing
   - Potential risks if this stakeholder is neglected

5. **Create a communication plan table**:

   | Stakeholder | Role | Power | Interest | Strategy | Frequency | Channel | Key Message |
   |---|---|---|---|---|---|---|---|

6. **Flag potential conflicts**: Identify stakeholders with competing interests and suggest alignment strategies.

Think step by step. Save the stakeholder map as a markdown document.

---

### Further Reading

- [The Product Management Frameworks Compendium + Templates](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Team Topologies: A Handbook to Set and Scale Product Teams](https://www.productcompass.pm/p/team-topologies-a-handbook-to-set)
