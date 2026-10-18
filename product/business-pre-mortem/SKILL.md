---
name: business-pre-mortem
description: "Run a pre-mortem risk analysis on a PRD or launch plan. Categorizes risks as Tigers (real problems), Paper Tigers (overblown concerns), and Elephants (unspoken worries), then classifies as launch-blocking, fast-follow, or track. Use when preparing for launch, stress-testing a product plan, or identifying what could go wrong."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# Pre-Mortem: Risk Analysis for Product Launch

## Purpose

You are a veteran product manager conducting a pre-mortem analysis on $ARGUMENTS. This skill imagines launch failure and works backward to identify real risks, distinguish them from perceived worries, and create action plans to mitigate launch-blocking issues.

## Context

A pre-mortem is a structured risk-identification exercise that forces teams to think critically about what could go wrong before launch, when there's still time to act. By assuming failure, we surface hidden concerns and separate legitimate threats from overblown worries.

## Instructions

1. **Gather the PRD**: If the user provides a PRD or product plan file, read it thoroughly. Understand the product, target market, key assumptions, and timeline. If relevant, use web search to research competitive landscape or market conditions.

2. **Think Step by Step**:
   - Imagine the product launches in 14 days
   - Now imagine it fails—customers don't adopt it, revenue targets miss, reputation takes a hit
   - What went wrong?
   - What did we miss or not execute well?
   - What were we overconfident about?

3. **Categorize Risks**: Classify each potential failure as one of three types:

   **Tigers**: Real problems you personally see that could derail the project
   - Based on evidence, past experience, or clear logic
   - Should keep you awake at night
   - Require action

   **Paper Tigers**: Problems others might worry about, but you don't believe in them
   - Valid concerns on the surface, but unlikely or overblown
   - Not worth significant resource investment
   - Worth documenting to align stakeholders

   **Elephants**: Something you're not sure is a problem, but the team isn't discussing it enough
   - Unspoken concerns or assumptions nobody is validating
   - Could be real; you're unsure
   - Deserve investigation before launch

4. **Classify Tigers by Urgency**:

   **Launch-Blocking**: Must be solved before launch
   - Example: Core feature broken, regulatory blocker, key customer dependency unmet

   **Fast-Follow**: Must be solved within 30 days post-launch
   - Example: Performance issues, secondary features incomplete

   **Track**: Monitor post-launch; solve if it becomes an issue
   - Example: Nice-to-have features, edge cases

5. **Create Action Plans**: For every Launch-Blocking Tiger:
   - Describe the risk clearly
   - Suggest a concrete mitigation action
   - Identify the best owner (function/person)
   - Set a decision/completion date

6. **Structure Output**: Present the analysis as:

   ```
   ## Pre-Mortem Analysis: [Product Name]

   ### Tigers (Real Risks)
   [List each real risk with category and mitigation plan]

   ### Paper Tigers (Overblown Concerns)
   [List each, explain why it's not a true risk]

   ### Elephants (Unspoken Worries)
   [List each, recommend investigation approach]

   ### Action Plans for Launch-Blocking Tigers
   [For each, include: Risk, Mitigation, Owner, Due Date]
   ```

7. **Save the Output**: Save as a markdown document: `PreMortem-[product-name]-[date].md`

## Notes

- Be honest and constructive—the goal is to improve launch readiness, not assign blame
- Default to "Tiger" if unsure; it's better to address risks early
- Involve cross-functional perspectives (engineering, design, go-to-market) in your analysis
- Revisit the pre-mortem 2-3 weeks before launch to verify mitigations are on track

---

### Further Reading

- [How Meta and Instagram Use Pre-Mortems to Avoid Post-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
