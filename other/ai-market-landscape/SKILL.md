---
name: ai-market-landscape
description: "Real-time competitive analysis of the AI market. Covers foundation models, products, pricing, moats, and strategic positioning across major AI labs and emerging players."
argument-hint: "[specific area or company to focus on]"
---

# AI Market Landscape Skill

Generate a comprehensive, up-to-date analysis of the AI competitive landscape — the market context every AI PM needs.

## When to Use
- User asks "What's the current AI landscape?"
- User wants a competitive analysis of AI companies
- User needs context on a specific AI market segment (models, agents, enterprise, consumer)
- User says `/ai-market-landscape` followed by a focus area
- Before any strategy interview to build fresh market context

## Framework: AI Market Landscape (6 Sections)

### Section 1: The AI Stack (Where Value Accrues)

Map the current AI value chain:

```
Layer 5: Applications    (ChatGPT, Perplexity, Cursor, vertical SaaS)
Layer 4: Orchestration   (LangChain, agent frameworks, MCP)
Layer 3: Models          (GPT-4, Claude, Gemini, Llama, Mistral)
Layer 2: Infrastructure  (AWS, Azure, GCP, Together, Fireworks)
Layer 1: Compute         (NVIDIA, AMD, custom chips - TPU, Trainium)
```

For each layer:
- Who are the key players?
- Where is commoditization happening?
- Where is differentiation strongest?
- Where is the most value being captured today vs. in 2 years?

### Section 2: Foundation Model Landscape

Compare the major model providers:

| Dimension | Lab A | Lab B | Lab C | Lab D | Lab E |
|-----------|--------|-----------|--------|------|---------|
| Latest model | | | | | |
| Key capability | | | | | |
| Pricing (input/output per 1M tokens) | | | | | |
| Open vs. closed | | | | | |
| Primary distribution | | | | | |
| Enterprise strategy | | | | | |
| Safety approach | | | | | |
| Funding / valuation | | | | | |

### Section 3: Product Landscape

Map AI products by category:

**Consumer AI:**
- General assistants (ChatGPT, Claude, Gemini)
- Search (Perplexity, SearchGPT, Gemini)
- Creative (Midjourney, DALL-E, Suno, Runway)
- Productivity (Notion AI, Copilot, Jasper)

**Developer AI:**
- Code (Cursor, GitHub Copilot, Claude Code, Windsurf)
- APIs & platforms (major LLM provider APIs, cloud AI platforms)
- Infrastructure (Vercel AI SDK, LangChain, LlamaIndex)

**Enterprise AI:**
- Horizontal (Microsoft Copilot, Google Workspace AI, Salesforce Einstein)
- Vertical (Harvey for law, Abridge for healthcare, Palantir AIP)

**Agents & Automation:**
- Computer use agents (browser and desktop automation)
- Workflow automation (Make, Zapier AI, n8n)
- Autonomous coding (Devin, Claude Code, Codex)

### Section 4: Strategic Dynamics

Analyze the key strategic questions shaping the market:

**Open vs. Closed:**
- Open-weight model strategies vs. closed-model approaches
- Impact on commoditization, developer loyalty, enterprise adoption
- Where does open-source win? Where does it lose?

**Consumer vs. Enterprise:**
- Consumer-first strategies (chatbot → enterprise upsell)
- Enterprise-first strategies (API → consumer product)
- Google's distribution advantage (Android, Chrome, Workspace, Search)

**Horizontal vs. Vertical:**
- Can horizontal AI products win vertical use cases?
- When do vertical AI startups have a wedge?
- The data moat question: does proprietary data still matter?

**Agents & Autonomy:**
- Where is agentic AI working today vs. hype?
- Trust and safety challenges with autonomous agents
- The "human-in-the-loop" spectrum

### Section 5: Market Sizing & Trends

**Current market data** (research the latest):
- Total AI market size and growth rate
- AI infrastructure spend
- Enterprise AI adoption rates
- Consumer AI MAU trends
- Developer tool market

**Key trends to track:**
- Model capability improvement curves
- Price per token trajectory (deflationary)
- Multimodal adoption
- AI regulation (EU AI Act, US executive orders)
- AI talent market dynamics

### Section 6: Implications for Product Decisions

Based on the landscape, highlight:
- **Key questions** each company is wrestling with right now
- **Strategic tensions** shaping product roadmaps
- **Product opportunities** where each company has a gap
- **Open debates** in the AI product community

## Output Format
Write as an analyst briefing — data-driven, opinionated, and actionable. Use tables for comparisons. Include specific numbers and sources. Aim for ~2500 words.

## Research-First Workflow (CRITICAL)
This skill is ONLY valuable with fresh data:
1. **Research extensively** — Do 10-15 web searches covering: latest model releases, funding rounds, product launches, market reports, earnings calls, developer surveys, and thought leader commentary.
2. **Cite everything** — Include `[linked source](url)` inline for all data points.
3. **Date the analysis** — Include "As of [date]" so the user knows the freshness.
4. **Display** the complete landscape analysis.

## What Good Looks Like
- Demonstrates you follow the AI market closely
- Shows you understand competitive dynamics beyond surface level
- Provides specific data points to drop in strategy discussions
- Reveals understanding of where value accrues vs. commoditizes
- Builds the context needed for "what would you build?" questions
