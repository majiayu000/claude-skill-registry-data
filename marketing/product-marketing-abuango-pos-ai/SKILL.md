---
name: product-marketing
description: Execute product marketing workflows including GTM strategy, positioning, competitive analysis, campaign planning, and launch coordination. Use when creating marketing plans, positioning documents, GTM strategies, or when user mentions "product marketing", "GTM", "go to market", "positioning", "competitive analysis", "launch plan", or "marketing campaign".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Product Marketing Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Execute product marketing workflows for any product context. This skill loads the appropriate product marketing agent and guides GTM strategy, positioning, campaigns, and launch coordination.

## Context Resolution

1. **Identify the product context**
   - Determine which product/team this marketing work is for
   - Load the corresponding marketing agent from `.ai/agents/mkt-{product}-product.md`
   - Load the product context from `contexts/{product}/`

2. **Available Marketing Agents**

   | Product | Agent File | Focus |
   |---------|-----------|-------|
   | {product-name} | `.ai/agents/mkt-{product}-product.md` | Your product description |

## Workflows

### 1. GTM Strategy (`/product-marketing gtm {product}`)

Create or update a Go-To-Market strategy for a product or feature.

**Process:**
1. Read the product marketing agent for context
2. Read current product status from `contexts/{product}/status.yaml`
3. Read any existing GTM documents from the product context
4. Generate GTM strategy covering:
   - Target segments and personas
   - Positioning and messaging
   - Channel strategy
   - Launch timeline
   - Success metrics
   - Budget allocation (if applicable)

**Output:** Save to `contexts/{product}/notes/{date}-doc-gtm-strategy.md`

### 2. Positioning Document (`/product-marketing positioning {product}`)

Create or refine product positioning.

**Process:**
1. Load marketing agent for competitive landscape and messaging framework
2. Analyze current product capabilities from team context
3. Generate positioning document:
   - Target audience definition
   - Market category
   - Key differentiators
   - Value propositions by persona
   - Competitive positioning matrix
   - Messaging pillars with proof points

**Output:** Save to `contexts/{product}/notes/{date}-doc-positioning.md`

### 3. Competitive Analysis (`/product-marketing competitive {product}`)

Conduct competitive analysis for a product.

**Process:**
1. Load marketing agent for existing competitive intel
2. Research competitors (web search if available)
3. Generate analysis:
   - Competitive landscape map
   - Feature comparison matrix
   - Pricing comparison
   - Strengths/weaknesses analysis
   - Differentiation opportunities
   - Recommended counter-positioning

**Output:** Save to `contexts/{product}/notes/{date}-research-competitive-analysis.md`

### 4. Campaign Planning (`/product-marketing campaign {product} {campaign-name}`)

Plan a marketing campaign for a launch or initiative.

**Process:**
1. Load marketing agent and product context
2. Define campaign scope and objectives
3. Generate campaign plan:
   - Campaign brief (objective, audience, timeline)
   - Channel strategy and content plan
   - Email sequences
   - Social media calendar
   - Landing page requirements
   - Success metrics and KPIs
   - Post-campaign analysis framework

**Output:** Save to `contexts/{product}/projects/{campaign-name}/plan.md`

### 5. Feature Launch (`/product-marketing launch {product} {feature}`)

Execute the feature launch playbook from the marketing agent.

**Process:**
1. Load marketing agent's Feature Launch Playbook
2. Determine launch timeline and current position
3. Generate launch checklist:
   - Pre-launch tasks (T-30 to T-7)
   - Launch day tasks
   - Post-launch tasks (T+7 to T+30)
   - Content requirements (blog, email, social)
   - Stakeholder communication plan

**Output:** Save to `contexts/{product}/notes/{date}-doc-launch-{feature}.md`

### 6. Content Brief (`/product-marketing content {product} {topic}`)

Create a content brief for marketing content.

**Process:**
1. Load marketing agent for brand voice and content strategy
2. Generate content brief:
   - Content type and format
   - Target audience and intent
   - Key messages and talking points
   - SEO keywords (if applicable)
   - Call to action
   - Distribution channels
   - Brand voice reminders

**Output:** Save to `contexts/{product}/notes/{date}-doc-content-brief-{topic}.md`

## Integration with Development Workflow

Product marketing should be involved in the feature lifecycle:

```
Feature Ideation → PM provides market context
Sprint Planning  → PM reviews for user-facing impact
Development      → PM prepares launch materials
Pre-Launch       → PM finalizes campaigns (T-14 days)
Launch Day       → PM executes GTM campaign
Post-Launch      → PM analyzes adoption and feedback
```

**Cross-handoff pattern:**
When engineering completes a feature, use `/cross-handoff` to hand off to product marketing for launch preparation.

## Output Standards

All product marketing documents should:
- Use the product's brand voice (defined in the marketing agent)
- Include specific metrics and proof points where available
- Be actionable (not just analysis — include next steps)
- Reference competitive context
- Follow the note naming convention: `{date}-{category}-{topic}.md`
- Categories: `doc` (strategy docs), `research` (analysis), `jotting` (ideas)

## Key Principle

> **Features don't sell products. Positioning does.**
> Every marketing deliverable should connect product capabilities to customer outcomes, not just list features.

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
