---
name: business-pestle-analysis
description: "Perform a PESTLE analysis covering Political, Economic, Social, Technological, Legal, and Environmental factors. Use when assessing the macro environment, doing strategic planning, or evaluating external factors affecting your business."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# PESTLE Analysis

## Metadata
- **Name**: pestle-analysis
- **Description**: Perform a PESTLE analysis covering Political, Economic, Social, Technological, Legal, and Environmental factors. Use when assessing macro-environment, evaluating market entry risks, or doing strategic planning.
- **Triggers**: PESTLE analysis, macro environment, market environment, external factors analysis

## Instructions

You are a strategic analyst conducting a PESTLE analysis for $ARGUMENTS.

Your task is to evaluate the macro-environmental factors that could impact product strategy, market entry, or business viability.

## Input Requirements
- Industry and market context
- Geographic market or region(s)
- Product or business type
- Current strategic challenges or questions
- Any known regulatory or market changes

## PESTLE Analysis Framework

### 1. Political
What government policies, regulations, and political stability affect the business?

- Government policies and incentives
- Tax regulations and tariffs
- Political stability and risk
- Government spending and subsidies
- Trade agreements and regulations
- Licensing and permits required
- Government relationships and lobbying needs

### 2. Economic
What economic conditions and financial factors matter?

- Economic growth and GDP trends
- Interest rates and inflation
- Currency exchange rates
- Consumer spending and confidence
- Employment and labor costs
- Disposable income trends
- Access to financing and capital

### 3. Social
What demographic and cultural trends shape the market?

- Population demographics and trends
- Cultural attitudes and values
- Consumer lifestyle and behaviors
- Education and skills availability
- Health and wellness trends
- Social media and digital adoption
- Diversity and inclusion preferences

### 4. Technological
What technological advances or disruptions are relevant?

- Emerging technologies (AI, blockchain, cloud, etc.)
- Digital transformation trends
- Cybersecurity and data privacy requirements
- Automation and robotics
- Internet of Things (IoT) and connectivity
- Research and development capabilities
- Technology adoption rates and digital literacy

### 5. Legal
What laws, regulations, and compliance requirements apply?

- Data protection and privacy laws (GDPR, CCPA, etc.)
- Employment and labor laws
- Intellectual property and patent laws
- Consumer protection laws
- Industry-specific regulations
- Compliance costs and audit requirements
- Liability and insurance requirements

### 6. Environmental
What environmental, climate, and sustainability factors exist?

- Climate change and environmental regulations
- Carbon emissions and sustainability requirements
- Natural resource availability and scarcity
- Waste management and circular economy trends
- Renewable energy adoption
- ESG (Environmental, Social, Governance) expectations
- Green certification and eco-friendly standards

## Output Process
1. For each PESTLE category, identify 3-5 relevant factors
2. Assess impact on product/business (High, Medium, Low)
3. Assess probability or likelihood (High, Medium, Low)
4. Prioritize factors by impact x probability
5. Develop strategic responses:
   - Which factors are opportunities to leverage?
   - Which factors are threats to mitigate or avoid?
   - Which factors require compliance or adaptation?
6. Identify key metrics or leading indicators to monitor
7. Build contingency plans for high-impact factors
8. Document assumptions and unknowns requiring research

## Strategic Applications
- Market entry assessment: Is this market viable to enter?
- Risk assessment: What macro risks could derail our strategy?
- Opportunity identification: What external shifts create new possibilities?
- Scenario planning: How would strategy change under different conditions?
- Regulatory roadmap: What compliance needs must we plan for?

## Notes
- PESTLE is complementary to SWOT (macro vs. micro analysis)
- Some factors span multiple categories (e.g., regulations affect legal, political, and economic)
- Geographic and industry context matter significantly
- Trends evolve; re-assess PESTLE annually or when markets shift
- Use PESTLE early in strategy development to avoid blind spots

---

### Further Reading

- [The Product Management Frameworks Compendium + Templates](https://www.productcompass.pm/p/the-product-frameworks-compendium)
