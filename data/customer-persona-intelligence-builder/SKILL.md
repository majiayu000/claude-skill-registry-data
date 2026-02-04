---
name: customer-persona-intelligence-builder
description: "Synthesize research, data, and insights to create a rich, actionable buyer persona with demographics, psychographics, jobs-to-be-done, pain points, motivations, buying journey, and channel preferences. Use when the user needs to understand their target customer deeply or create a customer persona for marketing strategy."
---

# Customer Persona Intelligence Builder

This skill creates a comprehensive, research-backed customer persona that goes beyond surface-level demographics. It synthesizes external research, industry data, and behavioral insights to create an actionable profile that can be used to inform marketing strategy, content creation, campaign development, and product positioning.

The persona is structured to be easily referenced by AI assistants when creating targeted marketing materials.

## When to Use This Skill

Use this skill when:
- User needs to create a customer persona or ideal customer profile (ICP)
- User wants to understand their target audience more deeply
- User is developing marketing strategy and needs customer insights
- User asks to research or profile a specific customer segment
- User needs a persona document to guide content creation

## Input Required

The user needs to provide only TWO simple inputs:

### 1. Target Customer Type
Who are you trying to reach?

Examples:
- "B2B marketing managers at SaaS companies"
- "First-time homebuyers in urban areas"
- "E-commerce founders doing $500K-$2M in revenue"
- "HR directors at mid-market companies"
- "Freelance graphic designers"
- "Tech startup CTOs"

### 2. What You're Selling
Brief description of your product or service (1-3 sentences)

Examples:
- "Marketing automation platform for B2B companies"
- "Eco-friendly cleaning products for homes"
- "AI-powered recruiting software"
- "Online courses for learning web development"
- "Fractional CFO services for startups"

## Workflow

### Step 1: Research Planning
Based on the target customer type and product, identify what research would be most valuable:

Key research areas:
- Industry/market data about this customer segment
- Demographic and psychographic profiles
- Common pain points and challenges in their role/life
- Buying behavior and decision-making patterns
- Media consumption and channel preferences
- Current trends affecting this audience
- Jobs-to-be-done for similar products/services
- How they currently solve the problem your product addresses

### Step 2: External Research
Use web_search to gather comprehensive insights. Conduct multiple searches (typically 3-7) to build a complete picture.

Recommended search queries:

**Demographics & Market Size:**
- "[Customer type] demographics latest"
- "[Customer type] statistics market research"
- "Profile of [customer type]"

**Pain Points & Challenges:**
- "[Customer type] biggest challenges latest"
- "[Customer type] pain points frustrations"
- "What [customer type] struggle with"

**Buying Behavior:**
- "How [customer type] make purchasing decisions"
- "[Customer type] buying process"
- "[Product category] buyer journey"

**Channel & Content Preferences:**
- "Where [customer type] consume content"
- "[Customer type] social media usage"
- "[Customer type] preferred communication channels"

**Industry Trends:**
- "[Industry] trends latest"
- "Future of [industry/role]"
- "[Customer type] priorities latest"

**Jobs-to-be-Done:**
- "Why [customer type] buy [product category]"
- "[Product category] use cases"
- "What [customer type] need from [product category]"

**Important:** Always search for the most recent data available. Include "latest" or "current year" in search queries to get current information.

### Step 3: Synthesize Research into Persona
After gathering research, synthesize findings into a comprehensive, structured persona document.

## Output Format

Create a detailed persona document with the following structure:

```
[Persona Name] - The [Descriptive Title]
Example: "Sarah Chen - The Growth-Focused Marketing Manager"

PERSONA OVERVIEW
Role/Title: [Primary role or customer type]
Key Characteristic: [One sentence that captures their essence]

DEMOGRAPHICS
Age Range: [e.g., 28-42]
Location: [Geographic info]
Education: [Education level/background]
Income Range: [If B2C; for B2B, use company size/budget]
Experience Level: [Years in role/industry]
Career Stage: [e.g., "Mid-career, aspiring to senior leadership"]
Sources: [List sources for demographic data]

PSYCHOGRAPHICS
Core Values:
[Value 1]: [Brief explanation]
[Value 2]: [Brief explanation]
[Value 3]: [Brief explanation]
Personality Traits:
[Trait 1]: [How this manifests in behavior]
[Trait 2]: [How this manifests in behavior]
[Trait 3]: [How this manifests in behavior]
Attitudes & Beliefs:
[About their work/life]
[About technology/change]
[About spending/investment]
Lifestyle Patterns: [Description of daily life, work-life balance, priorities]
Sources: [List sources]

GOALS & ASPIRATIONS
Professional Goals:
[Goal 1] - [Why this matters to them]
[Goal 2] - [Why this matters to them]
[Goal 3] - [Why this matters to them]
Personal Goals: (if relevant) [What they're trying to achieve in their personal life]
Success Metrics: How they measure success:
[Metric 1]
[Metric 2]
[Metric 3]
Sources: [List sources]

PAIN POINTS & CHALLENGES
Top Frustrations:
[Pain Point 1]
Impact: [How this affects them]
Current workaround: [How they currently cope]
Emotional toll: [How this makes them feel]
[Pain Point 2]
Impact: [How this affects them]
Current workaround: [How they currently cope]
Emotional toll: [How this makes them feel]
[Pain Point 3]
Impact: [How this affects them]
Current workaround: [How they currently cope]
Emotional toll: [How this makes them feel]
What Keeps Them Up at Night: [2-3 sentences about their deepest concerns]
Sources: [List sources]

MOTIVATIONS & DRIVERS
Primary Motivators:
[Motivator 1]: [Why this drives them]
[Motivator 2]: [Why this drives them]
[Motivator 3]: [Why this drives them]
Decision-Making Drivers: What influences their choices:
[Driver 1]
[Driver 2]
[Driver 3]
Aspirational Identity: Who they want to become or how they want to be perceived
Sources: [List sources]

FEARS & OBJECTIONS
Fears:
[Fear 1]: [Why this scares them]
[Fear 2]: [Why this scares them]
[Fear 3]: [Why this scares them]
Common Objections: When considering solutions like yours:
[Objection 1]: [The concern]
[Objection 2]: [The concern]
[Objection 3]: [The concern]
Risk Aversion Level: [Low/Medium/High] - [Explanation]
Sources: [List sources]

WORK CONTEXT (for B2B personas)
Daily Responsibilities:
[Responsibility 1]
[Responsibility 2]
[Responsibility 3]
Tools & Technology They Use: [List relevant tools, platforms, software they're familiar with]
Reporting Structure:
Reports to: [Role]
Manages: [Number/type of people]
Collaborates with: [Other departments/roles]
Key Performance Indicators: How their performance is measured:
[KPI 1]
[KPI 2]
[KPI 3]
Decision-Making Authority:
Budget authority: [Level of financial decision-making power]
Influence level: [Are they a decision-maker, influencer, or user?]
Approval process: [Who else is involved in decisions?]
Sources: [List sources]

JOBS-TO-BE-DONE
When they "hire" a product like yours, they're trying to:
Functional Jobs:
[Functional job 1]: [Specific task or outcome]
[Functional job 2]: [Specific task or outcome]
[Functional job 3]: [Specific task or outcome]
Emotional Jobs:
[Emotional job 1]: [How they want to feel]
[Emotional job 2]: [How they want to feel]
Social Jobs:
[Social job]: [How they want to be perceived]
Sources: [List sources]

BUYING JOURNEY
Awareness Stage:
How they become aware of problems: [Description]
Trigger events: [What makes them start looking for solutions]
Information sources: [Where they learn about options]
Consideration Stage:
Research behavior: [How they evaluate solutions]
Key decision criteria: [What matters most to them]
[Criterion 1]
[Criterion 2]
[Criterion 3]
Comparison process: [How they compare alternatives]
Decision Stage:
Final decision factors: [What seals the deal]
Timeline: [How long the process typically takes]
Stakeholders involved: [Who influences or approves]
Post-Purchase:
Onboarding expectations: [What they need to feel successful]
Success indicators: [How they measure if it was the right choice]
Sources: [List sources]

CHANNEL & CONTENT PREFERENCES
Primary Channels: Where they spend time and consume content:
[Channel 1] - [How they use it, what they consume]
[Channel 2] - [How they use it, what they consume]
[Channel 3] - [How they use it, what they consume]
Content Types They Engage With:
Content type 1: [Why this resonates]
Content type 2: [Why this resonates]
Content type 3: [Why this resonates]
Communication Preferences:
Preferred medium: [Email, phone, chat, in-person]
Communication style: [Formal vs casual, brief vs detailed]
Best time to reach: [When they're most receptive]
Trusted Sources: Who/what they trust for recommendations:
[Source 1]
[Source 2]
[Source 3]
Sources: [List sources]

MESSAGING THAT RESONATES
Language They Use: Key phrases and terminology from their world:
[Phrase 1]
[Phrase 2]
[Phrase 3]
Message Themes That Land:
[Theme 1]: [Why this works]
[Theme 2]: [Why this works]
[Theme 3]: [Why this works]
Proof Points That Matter: What builds credibility with them:
[Proof point 1]
[Proof point 2]
[Proof point 3]
Objections to Overcome: How to address their concerns:
[Objection]: [How to counter it]
[Objection]: [How to counter it]

ACTIVATION GUIDE
How to Reach Them:
[Tactic 1]: [Specific approach]
[Tactic 2]: [Specific approach]
[Tactic 3]: [Specific approach]
Content to Create: Priority content types for this persona:

Key Messages: Primary messages to emphasize:
[Message 1]
[Message 2]
[Message 3]
Channel Strategy:
Primary focus: [Main channel with rationale]
Secondary channels: [Supporting channels]
Avoid: [Channels that won't work]
Campaign Ideas: 3 specific campaign concepts for this persona:
[Campaign idea 1]
[Campaign idea 2]
[Campaign idea 3]

PERSONA SUMMARY
One-Sentence Description: [Capture the essence of this persona in one compelling sentence]
Best Way to Win Them: [2-3 sentences summarizing the key to success with this persona]
What Makes Them Unique: [What distinguishes them from other customer segments]

RESEARCH SOURCES
List all sources used to build this persona:
Demographics & Market Data:
[Source 1 with URL]
[Source 2 with URL]
Pain Points & Challenges:
[Source 1 with URL]
[Source 2 with URL]
Buying Behavior:
[Source 1 with URL]
[Source 2 with URL]
Channel Preferences:
[Source 1 with URL]
[Source 2 with URL]
Industry Trends:
[Source 1 with URL]
[Source 2 with URL]

Persona created: [Date]
Based on research current as of: [Current month and year]
```

## Quality Standards

The persona must meet these requirements:
- ✅ Research-backed - Every major claim supported by external sources
- ✅ Specific and detailed - No vague generalities; concrete behaviors and traits
- ✅ Actionable - Clear guidance on how to reach and convert this persona
- ✅ Comprehensive - Covers all key dimensions (demographics through activation)
- ✅ Well-cited - All sources properly attributed with URLs when available
- ✅ Current - Based on latest available data
- ✅ Realistic - Grounded in real behaviors and patterns, not stereotypes
- ✅ AI-friendly format - Structured to be easily parsed and referenced by AI assistants

## Research Best Practices

### Search Strategy
- Conduct 3-7 targeted web searches to gather comprehensive data
- Prioritize recent data (last 1-2 years) over older sources
- Look for original research (industry reports, surveys, studies) over aggregated content
- Cross-reference findings from multiple sources
- Search for both quantitative data (statistics, demographics) and qualitative insights (pain points, behaviors)

### Source Quality
Prioritize:
- Industry research firms (Gartner, Forrester, McKinsey, etc.)
- Government statistics and census data
- Academic research and peer-reviewed studies
- Original company surveys and reports
- Reputable business publications (HBR, Forbes, WSJ, etc.)

Use with caution:
- Blog posts (unless from recognized experts)
- Forums and social media (good for language/pain points, not statistics)
- Outdated sources (older than 2-3 years unless no recent data available)

### Citation Requirements
- Include URL or publication name for every source
- Group citations by section in the final "Research Sources" section
- Use inline citations (📚 Sources:) at the end of each major section
- If a claim can't be sourced, clearly label it as "inferred" or "based on industry patterns"

### Synthesis Guidelines
- Don't just copy information - synthesize insights across sources
- Look for patterns and themes across multiple sources
- When sources conflict, note the discrepancy and use the most recent/credible source
- Add context to statistics (e.g., "32% of marketing managers report X, up from 18% in 2023")

## Response Tone
- Professional and strategic
- Data-driven but humanizing
- Empathetic and understanding of customer challenges
- Concrete and specific, avoiding marketing jargon
- Written in third person about the persona (e.g., "Sarah values..." not "You value...")

## Common Pitfalls to Avoid
- ❌ Creating generic, stereotype-based personas
- ❌ Listing features without explaining the underlying motivations
- ❌ Using outdated data or sources
- ❌ Forgetting to cite sources for key insights
- ❌ Making claims that aren't backed by research
- ❌ Being too broad or vague in descriptions
- ❌ Focusing only on demographics without psychographics
- ❌ Ignoring the buying journey and decision-making process
- ❌ Creating a persona that's not actionable for marketing

## Example Opening

When a user provides "B2B marketing managers at SaaS companies" and "Marketing automation platform," your response should begin:

```
I'll create a comprehensive customer persona for B2B marketing managers at SaaS companies interested in marketing automation platforms. Let me conduct research to gather current insights about this audience...

[Conduct 4-6 web searches gathering demographic data, pain points, buying behavior, channel preferences, and industry trends]

Based on my research, here's your detailed customer persona:

[Persona Name] - The [Descriptive Title]
[Continue with full structured persona...]
```

## Usage by AI Assistants

This persona document is designed to be easily referenced by AI assistants. When creating marketing materials, the AI can:
- Reference specific pain points when crafting messaging
- Use the persona's language and terminology
- Target the right channels based on preferences
- Address objections proactively
- Align content with their goals and motivations
- Match tone to their communication preferences

Example AI usage: "Create a LinkedIn post for [Persona Name] that addresses their pain point around [specific challenge] and uses language they relate to like [key phrases]."

## Final Notes

- Always start with external research - never rely solely on assumptions
- The best personas feel like real people, not statistical aggregates
- Update personas periodically as markets and behaviors evolve
- Use this persona as a living document to inform all marketing decisions
- When in doubt, add more specificity and detail rather than staying general
