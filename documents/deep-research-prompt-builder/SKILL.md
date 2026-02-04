---
name: deep-research-prompt-builder
description: Interactive prompt builder for creating high-quality deep research prompts through adaptive interviewing. Use when users need to transform a basic research topic into a comprehensive, well-structured research prompt optimized for deep analysis. Helps build research prompts from vague ideas, enhance existing questions with best practices, and create structured prompts for any domain including product comparisons, technical documentation, academic literature, and market analysis.
---

# Deep Research Prompt Builder

Expert system for constructing high-quality research prompts through adaptive interviewing and best-practice application.

## Core Workflow

### 1. Categorize Research Topic

When user provides a topic, immediately categorize it:

- **Product/Service**: Shopping comparisons, reviews, buying guides
- **Technical**: Code patterns, architecture, implementation details
- **Academic**: Literature reviews, theoretical analysis, scientific research
- **Business**: Market analysis, competitive intelligence, trends
- **General**: Historical, cultural, educational topics

### 2. Conduct Adaptive Interview

Ask questions ONE AT A TIME. Wait for response before proceeding.

**Generate questions that directly probe the specific research topic.** Use the category examples below as inspiration, not scripts. Each question should surface something the user hasn't yet specified about their actual topic.

#### Clarification Triggers

Before proceeding with interview questions, clarify when:

- User uses ambiguous or unusual terminology
- Scope is mentioned but intent is unclear (what specifically matters about it?)
- User gives compound answers - confirm priority ordering
- Technical terms may have multiple meanings in context

#### Opening Question (All Categories)

"What specific aspect of [TOPIC] are you most interested in exploring?"

#### Category-Specific Question Examples

Use these as **inspiration only** - adapt questions to the actual topic at hand:

**Product/Service examples:**

- Research goal: current best options, specific comparisons, or understanding what makes something good?
- Key criteria and their priority order
- Preferred output format

**Technical examples:**

- Context: learning, implementing, or making architectural decisions?
- Critical aspects: performance, best practices, pitfalls, examples?
- Depth needed: overview, implementation guide, or deep analysis?

**Academic examples:**

- Purpose: literature review, hypothesis exploration, or current knowledge state?
- Time scope preferences
- Evidence standards: peer-reviewed only or broader sources?

**Business examples:**

- Focus: market landscape, competitor analysis, or trends?
- Most valuable data types
- Scope boundaries

**General examples:**

- What's driving this research?
- Perspective: comprehensive, specific angle, or comparative?
- Key debates or controversies to address?

#### Closing Question (All)

"Any specific angle or outcome you haven't mentioned that should shape this research?"

### 3. Build Enhanced Prompt

#### Prompt Construction Principles

- **Include only what was discussed or directly implied**
- Do NOT add "enhancements" the user didn't ask about
- If uncertain whether to include something, leave it out
- Scope mentions (geographic, temporal, etc.) should reflect user's stated intent, not assumed interests
- No speculative expansions beyond what user requested

Use this template structure:

```
# Research Objective
[Clear statement synthesized from topic and clarifications]

# Context and Scope
- Purpose: [Why this research matters]
- Boundaries: [Time, geography, domain limits]
- Focus Areas: [3-5 specific aspects to emphasize]

# Research Requirements

## Investigation Depth
Primary questions:
1. [Main research question]
2. [Key sub-question 1]
3. [Key sub-question 2]

Secondary considerations:
- [Related area if relevant]
- [Adjacent topic to explore]

Explicitly exclude: [What NOT to research]

## Evidence Standards
- Source types: [Academic, industry, user-generated, etc.]
- Recency: [How current sources must be]
- Credibility: [Minimum authority level]
- Citations: [How to reference sources]

## Analysis Framework
[INSERT CATEGORY-SPECIFIC FRAMEWORK - see below]

## Output Structure
### Required Sections:
1. Executive Summary (3-5 key findings)
2. Detailed Analysis by Subtopic
3. Supporting Evidence with Citations
4. Practical Implications
5. Confidence Levels and Limitations
6. Further Research Needed

### Format Requirements:
- Hierarchical headings for navigation
- Data visualization descriptions where helpful
- Balance depth with readability
- Include both synthesis and details

# Quality Instructions

## Reasoning Approach
- Think step-by-step through each research aspect
- Build from foundational understanding to nuances
- Explicitly address source contradictions
- Validate through multiple independent sources

## Critical Evaluation
- Cross-reference all major claims
- Distinguish facts from interpretations
- Note confidence levels for findings
- Acknowledge information gaps

[Additional topic-specific instructions from interview]
```

## Category-Specific Frameworks

Insert appropriate framework based on category:

### Product Framework

```
## Analysis Framework
- Feature comparison matrix across top options
- Price-performance analysis
- Real user experience synthesis
- Expert review aggregation
- Long-term value assessment
- Common issues and solutions
```

### Technical Framework

```
## Analysis Framework
- Implementation complexity assessment
- Performance and scalability analysis
- Code examples and patterns
- Best practices vs anti-patterns
- Tool ecosystem and dependencies
- Migration and maintenance considerations
```

### Academic Framework

```
## Analysis Framework
- Theoretical foundations and evolution
- Methodological approaches comparison
- Key findings synthesis across studies
- Debates and controversies mapping
- Research gaps identification
- Future direction assessment
```

### Business Framework

```
## Analysis Framework
- Market dynamics and size
- Competitive landscape mapping
- Customer segment analysis
- Growth drivers and barriers
- Risk and opportunity assessment
- Strategic recommendations
```

### General Framework

```
## Analysis Framework
- Historical context and evolution
- Multiple perspective comparison
- Cultural and societal impacts
- Current state assessment
- Future implications
- Related topic connections
```

## Additional Resources

For complete example prompts across all categories, see `references/example-prompts.md`.
For advanced prompting techniques (CoT, self-consistency, role-based framing), see `references/prompt-techniques.md`.

## Prompt Enhancement Techniques

Apply these **only when directly relevant to what the user discussed**. Do not add enhancements speculatively.

### For Vague Topics (if user's topic lacks clear boundaries)

Add: "Begin by establishing clear definitions and scope based on authoritative consensus, then proceed with focused analysis."

### For Controversial Topics (if user mentions debates or conflicting views)

Add: "Present multiple viewpoints with supporting evidence. Clearly distinguish between consensus, debate, and speculation."

### For Emerging Fields (if user is researching something new/rapidly evolving)

Add: "Note the recency of this domain. Prioritize latest developments while acknowledging rapid change and limited long-term data."

### For Comparative Research (if user explicitly wants comparisons)

Add: "Develop systematic comparison criteria before analysis. Ensure fair, parallel evaluation across all options."

### For Technical Implementation (if user needs practical guidance)

Add: "Include practical examples, common gotchas, and real-world considerations beyond theoretical knowledge."

## Pre-Output Confirmation

Before generating the final prompt, briefly confirm:

"Based on our discussion, the prompt will focus on:

- [Primary goal]
- [Key criteria]
- [Scope boundaries]

Anything to add or remove before I generate it?"

## Output Format

After confirmation, preface final prompt with:
"Here's your enhanced research prompt. Copy and use this for comprehensive deep research:"

```
[Complete enhanced prompt in code block for easy copying]
```

## Quality Checklist

Before outputting, verify prompt includes:

- [ ] Clear, specific research objective
- [ ] Defined scope and boundaries
- [ ] Evidence requirements
- [ ] Output structure
- [ ] Reasoning instructions
- [ ] Quality evaluation criteria
- [ ] Topic-specific enhancements (only if discussed)
- [ ] Contains ONLY elements discussed or directly requested
- [ ] No speculative enhancements added

## Prompt Validation

To validate the generated prompt contains all required sections, run:

```bash
python scripts/validate_prompt.py prompt.txt
```

The validator checks for required sections, recommended elements, and provides a quality score. Use this before delivering the final prompt to ensure completeness.

## Interaction Guidelines

- Keep questions concise and clear
- One question at a time for better UX
- Skip questions if user provides info upfront
- Adapt depth based on user expertise signals
- If conflicting requirements, ask for priority
- If scope too broad, suggest splitting into multiple research tasks
