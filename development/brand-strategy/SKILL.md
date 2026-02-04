---
name: brand-strategy
description: This skill should be used when translating research insights into actionable brand strategy frameworks. Use this when developing positioning statements, messaging architectures, audience strategies, or voice guidelines based on completed research. This skill provides strategic synthesis workflows, validation frameworks, and strategy document templates for evidence-based brand strategy development.
---

# Brand Strategy

## Overview

This skill enables evidence-based brand strategy development by providing workflows for synthesizing research insights into strategic frameworks. Use this skill when research has been completed and strategic decisions need to be made across positioning, messaging, audience, or voice dimensions.

## When to Use This Skill

Invoke this skill when:
- Research findings need to be translated into strategic recommendations
- Positioning statements or messaging frameworks need to be developed
- Strategic decisions require validation against market evidence
- A comprehensive brand strategy document needs to be created
- Existing strategy needs to be updated based on new research insights

## Core Strategic Workflow

### Phase 1: Research Foundation Review

Before developing strategy, establish the research foundation:

1. **Identify Available Research**: Review `/research/` directory for completed research domains
   - Start with each domain's `RESEARCH.md` entry point
   - Identify most recent research runs (`/{YYYY-MM-DD}/`)
   - Note available exports and key findings

2. **Load Relevant Research**: Based on strategic objective, load specific research files
   - Category landscape research → competitive positioning insights
   - Customer insight research → audience needs and pain points
   - Voice/tone research → language patterns and preferences

3. **Extract Strategic Patterns**: Synthesize across research domains
   - Identify contradictions that need resolution
   - Map competitive white space opportunities
   - Note validation gaps requiring additional research

### Phase 2: Strategic Framework Development

Develop strategy using the strategist agent (`.claude/agents/strategist.md`) which provides:
- Evidence-based positioning development
- Messaging architecture construction
- Audience strategy prioritization
- Voice guideline creation

**Core Strategic Deliverables:**

1. **Positioning Statement**
   - Format: "We are [what] for [whom] in [context]"
   - Must include: rationale, evidence footnotes, differentiation analysis
   - Template: `assets/positioning-template.md`

2. **Messaging Architecture**
   - Core theme and 3-5 content pillars
   - Value propositions for each audience segment
   - Proof points backing each claim
   - Template: `assets/messaging-template.md`

3. **Audience Strategy**
   - Segment definitions with characteristics
   - Prioritization with strategic rationale
   - Needs, pain points, decision criteria
   - Template: `assets/audience-template.md`

4. **Voice Guidelines**
   - 3-5 vocal attributes with examples
   - Language patterns to embrace and avoid
   - Concrete demonstrations of voice in action
   - Template: `assets/voice-template.md`

### Phase 3: Strategic Validation

Before finalizing strategy, validate using the framework in `references/validation-checklist.md`:

1. **Evidence Check**: Every claim footnoted to research
2. **Differentiation Test**: Strategy is distinct from competitors
3. **Execution Feasibility**: Can be implemented consistently
4. **Strategic Coherence**: All elements reinforce each other

### Phase 4: Strategy Documentation

Document strategy in `/strategy/` directory following these principles:

**File Organization:**
```
/strategy/
├── STRATEGY.md (entry point, progressive disclosure)
├── /core/
│   ├── narrative.md
│   └── positioning.md
├── /messaging/
│   ├── pillars.md
│   └── value-propositions.md
├── /voice/
│   ├── tone-guidelines.md
│   └── vocabulary.md
└── /audience/
    └── personas/
```

**Documentation Standards:**
- Every strategic claim must be footnoted to research
- Use format: `[^reference-name]: [Context], /path/to/file.md:line-number`
- Strategy files should be polished and client-ready
- Create or update `STRATEGY.md` as navigation entry point

## Common Strategic Scenarios

### Scenario 1: Developing Positioning from Category Research

**Input**: Completed category landscape research showing competitive positioning and white space
**Process**:
1. Load `/research/category-landscape/RESEARCH.md` and latest findings
2. Map competitive positioning territories using insights
3. Identify white space opportunities
4. Draft positioning statement using `assets/positioning-template.md`
5. Validate against checklist in `references/validation-checklist.md`
6. Document in `/strategy/core/positioning.md` with research footnotes

### Scenario 2: Creating Messaging Architecture from Customer Insights

**Input**: Customer research showing needs, pain points, desired outcomes
**Process**:
1. Load `/research/customer-insight/RESEARCH.md` and findings
2. Extract core customer themes and patterns
3. Map themes to content pillars using `assets/messaging-template.md`
4. Develop value propositions for each audience segment
5. Validate messaging against customer research evidence
6. Document in `/strategy/messaging/` with research footnotes

### Scenario 3: Building Comprehensive Brand Strategy

**Input**: Multiple completed research domains (category, customer, voice)
**Process**:
1. Review all available research via `RESEARCH.md` entry points
2. Use `assets/full-strategy-template.md` as structure
3. Develop positioning, messaging, audience, voice in sequence
4. Validate strategic coherence across all dimensions
5. Document complete strategy in `/strategy/` directory
6. Create `STRATEGY.md` navigation entry point

## Resources

### references/
Strategic frameworks and validation tools:
- `validation-checklist.md` - Framework for validating strategy before finalization
- `strategic-principles.md` - Core principles governing strategic decisions

### assets/
Strategy document templates:
- `positioning-template.md` - Structure for positioning statements
- `messaging-template.md` - Framework for messaging architecture
- `audience-template.md` - Format for audience strategy
- `voice-template.md` - Template for voice guidelines
- `full-strategy-template.md` - Comprehensive brand strategy document structure
