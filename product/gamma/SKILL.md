---
name: gamma
description: Alternative presentation generation path via Gamma MCP with prompt templates and decision tree for Gamma vs PPTX
tier: 1 (universal)
auto-fire: /deck (gamma path)
user-invocable: false
---

# Gamma — Alternative Presentation Path Skill

## Purpose

Defines the Gamma presentation generation path as an alternative to native .pptx. Documents when to use Gamma vs. PPTX, prompt templates for Gamma generation, setup requirements, and known limitations.

## When Referenced

- **/deck** — offers Gamma as an alternative when available
- **/setup** — configures Gamma connector status ({{GAMMA_CONNECTED}})

## Core Framework

### When to Use Gamma vs. PPTX

| Factor | Use Gamma | Use PPTX |
|--------|-----------|----------|
| **Speed** | When you need a polished deck in seconds | When you need precise control over layout |
| **Design quality** | When visual design matters more than pixel-perfect branding | When strict brand guidelines must be followed |
| **Collaboration** | When the deck will be shared via link for collaborative editing | When the deck must be a standalone .pptx file |
| **Customization** | When the template structure is flexible | When specific slides must follow exact formats |
| **Offline** | Not suitable (web-based) | Best choice (generates local file) |
| **Brand tokens** | Gamma applies its own themes — limited brand control | Full brand token control (logo, colors, fonts) |

**Default recommendation:** Use PPTX for formal customer-facing presentations. Use Gamma for quick internal decks, brainstorming, or when visual polish is prioritized over brand precision.

### Gamma Generation via MCP

When Gamma MCP is available ({{GAMMA_CONNECTED}} = true), SalesSidekick can generate presentations directly through the Gamma tool.

**Generation flow:**
1. Build the content outline from deal/account data (same content as PPTX templates)
2. Format as a Gamma input prompt
3. Call Gamma MCP generate tool
4. Return the Gamma URL to the user for review and editing

### Prompt Templates

When generating via Gamma, use these structured prompts mapped to the 5 deck templates:

#### Discovery Deck Prompt
```
Create a sales discovery presentation for a meeting with [Company Name].

About us: {{COMPANY}} — {{PRODUCT_DESCRIPTION}}
Their industry: [Industry]
Their size: [Account Size]

Include slides for:
1. Title slide with both company names
2. Brief about us (who we are, what we do)
3. Industry context and trends
4. Common challenges for [Industry] companies
5. Our approach (methodology, not features)
6. 2-3 proof points or case studies
7. Discovery questions to explore
8. Proposed next steps
```

#### POV Deck Prompt
```
Create a Point of View presentation for [Company Name].

Executive anchor: [2-sentence business challenge framing]
Blind spot: [Insight they haven't quantified]
Math of pain: [Quantified cost of inaction]
Our approach: [How we solve it — methodology]
Proof point: [Relevant case study]

Include slides for each POV component plus a recommended next step.
```

#### Executive Summary Prompt
```
Create an executive summary presentation for [Company Name].

Business context: [Their situation from discovery]
Requirements: [Confirmed decision criteria]
Proposed solution: [Our recommendation]
Business impact: [ROI projections]
Investment: [Pricing overview]

Include implementation timeline and decision next steps.
```

#### QBR Prompt
```
Create a Quarterly Business Review presentation for [Customer Name].

Relationship: [Account overview, key contacts]
Outcomes achieved: [Metrics and wins this quarter]
Value delivered: [ROI realized]
Growth opportunities: [Expansion possibilities]

Include a next-quarter plan slide.
```

#### Competitive Displacement Prompt
```
Create a competitive comparison presentation: {{COMPANY}} vs [Competitor].

Their requirements: [Decision criteria]
Our differentiators: [3 key advantages]
Customer evidence: [Case study of similar switch]
Total value comparison: [TCO or value analysis]

Focus on approach differences, not feature checklists. Include a transition plan.
```

### Setup Requirements

For Gamma to work:
1. Gamma MCP server must be configured and accessible
2. {{GAMMA_CONNECTED}} must be set to `true` during /setup
3. User must have a Gamma account

### Known Limitations

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| **No offline access** | Gamma decks are web-only | Use PPTX for offline needs |
| **Limited brand control** | Gamma uses its own themes, not pixel-perfect brand tokens | Choose a Gamma theme that's close, then manually adjust |
| **No programmatic editing** | Can't modify specific slides after generation | User edits in Gamma's editor |
| **Content length** | Very long content may not fit Gamma's card format well | Keep content concise, let Gamma optimize layout |
| **Export limitations** | Export to PPTX/PDF possible but may lose Gamma-specific formatting | Review export before presenting |

### Gamma vs. PPTX Decision Tree

```
Does the user need a .pptx file? → YES → Use PPTX
                                   → NO ↓
Is Gamma connected? → NO → Use PPTX (only option)
                     → YES ↓
Does the user have strict brand guidelines? → YES → Use PPTX
                                             → NO ↓
Is speed more important than layout control? → YES → Use Gamma
                                              → NO → Use PPTX
```

## Personalization Notes

- {{GAMMA_CONNECTED}} is a connector status variable set during /setup
- Gamma themes are selected by the user in Gamma's interface — not controlled by SalesSidekick
- Content inputs (company data, case studies, competitive info) come from the same sources as PPTX
- Prompt templates reference {{COMPANY}} and {{PRODUCT_DESCRIPTION}} (Tier 2 variables)
