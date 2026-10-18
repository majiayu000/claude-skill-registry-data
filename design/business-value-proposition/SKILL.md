---
name: business-value-proposition
description: "Design a detailed value proposition using a 6-part JTBD template — Who, Why, What before, How, What after, Alternatives. Use when creating a value proposition, analyzing customer value delivery, or articulating why customers should choose your product."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# Value Proposition

## Metadata
- **Name**: value-proposition
- **Description**: Generate a detailed value proposition using a 6-part template with JTBD framing. Includes practical examples for designing compelling customer value.
- **Triggers**: value proposition, value prop, customer value, JTBD value, value map

## Instructions

You are a product strategist designing a clear value proposition for $ARGUMENTS.

Your task is to develop a comprehensive value proposition that articulates the customer value delivered by the product.

## Input Requirements
- Product description and features
- Target customer segment and their problems
- Competitive alternatives and current solutions
- Customer insights or market data

## Value Proposition Template

### 6-Part Structure

**1. Who**
- Who is this value proposition for?
- What customer segment are we addressing?
- What are their characteristics and constraints?

**2. Why (Problem)**
- What is the customer's core problem or need?
- What's the Job to Be Done (JTBD)?
- What desired outcomes are they trying to achieve?

**3. What Before**
- What is the customer's current situation?
- What are they using today to solve this problem?
- What friction or pain exists in the current approach?

**4. How (Solution)**
- How does the product solve the problem?
- What specific features or capabilities deliver value?
- Why is this solution better than alternatives?

**5. What After**
- What is the improved outcome or future state?
- How does the customer's life/work change?
- What becomes possible that wasn't before?

**6. Alternatives**
- What other solutions could customers use?
- Why would they choose us instead?
- What's the switching cost or friction from alternatives?

## Example: Canva
- **Who**: Non-designers who need to create marketing graphics
- **Why**: They need professional-looking designs but can't hire designers or use complex tools
- **What Before**: Using PowerPoint, Photoshop (too complex), or hiring expensive designers
- **How**: Drag-and-drop templates, built-in design elements, AI design assistance, intuitive interface
- **What After**: Create professional designs in minutes, launch campaigns faster, save design costs
- **Alternatives**: Photoshop (complex), Fiverr (slow, expensive), Canva competitors (fewer templates, harder UX)

## Output Process
1. Identify and profile the target customer segment
2. Define the core problem and JTBD
3. Describe the current state and friction points
4. Articulate how the product solves the problem
5. Envision the improved outcome
6. Compare against competitive alternatives
7. Create a concise value prop statement (1-2 sentences)
8. Develop a positioning statement for marketing use

### Domain Context

**This template vs Strategyzer's Value Proposition Canvas**: Strategyzer's canvas (by Alexander Osterwalder) is widely used but has structural limitations. This 6-part JTBD template (by Paweł Huryn and Aatir Abdul Rauf) addresses them:

- **Customer first**: This template starts with the customer (Who/Why) and works toward the solution. Strategyzer's canvas places the product on the left, which often leads teams to start with their solution rather than the customer's problem.
- **One segment at a time**: This template is designed for one segment per pass. Strategyzer's canvas encourages mapping multiple products/services simultaneously, which dilutes focus.
- **Explicit alternatives**: Section 6 (Alternatives) forces you to name what customers would use without you and articulate why you're better. Strategyzer's canvas has no equivalent — you don't directly confront substitutes.
- **Simpler structure**: "What before → How → What after" is easier to fill out than separating Customer Jobs, Pains, and Gains on one side and Pain Relievers, Gain Creators, and Products on the other. The separation often creates confusion about where things go.
- **Actionable output**: The final Value Proposition Statement is ready for marketing, sales, and onboarding. Strategyzer's canvas doesn't produce a reusable statement.

Use Strategyzer's Value Proposition Canvas when you need a detailed pains/gains decomposition for a mature product with complex customer needs. Use this 6-part template for clarity, speed, and actionable output.

## Notes
- Jobs to Be Done (JTBD) framework focuses on the progress the customer is trying to make, not demographics
- Value propositions are segment-specific; you may have different value props for different customer groups
- The stronger your value prop, the easier marketing, sales, and product decisions become
- Test value props with real customers before finalizing
- Use a **Value Curve** (Blue Ocean Strategy) to visually compare your offering against competitors across key factors

---

### Templates

- [Value Proposition Template (PPTX)](https://docs.google.com/presentation/d/1RXH1Udj71aXQJzGeqYSOStnfQ-6dNz14/edit?slide=id.g2a98aeea3b1_0_247#slide=id.g2a98aeea3b1_0_247)

---

### Further Reading

- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
- [How to Achieve Product-Market Fit? Part I: Market and Value Proposition](https://www.productcompass.pm/p/how-to-achieve-the-product-market)
- [Jobs-to-be-Done Masterclass with Tony Ulwick and Sabeen Sattar](https://www.productcompass.pm/p/jobs-to-be-done-masterclass-with) (video course)
- [Product Innovation Masterclass](https://www.productcompass.pm/p/product-innovation-masterclass) (video course)
