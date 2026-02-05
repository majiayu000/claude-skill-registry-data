---
name: refine-prompts
description: "Refine vague or unclear prompts into precise, actionable instructions. Use when user asks to clarify or improve instructions or when input is vague. Not for already clear prompts or simple questions."
user-invocable: true
---

# Prompt Refinement

Refine vague or unclear prompts into precise, actionable instructions using L1/L2/L3/L4 methodology.

---

## Critical Methodology (MANDATORY)

**MANDATORY**: Understand L1/L2/L3/L4 refinement levels before refining prompts.

**WRONG LEVEL = POOR RESULTS**:

- **L1 (too simple)**: Misses critical context → Claude makes wrong assumptions
- **L2/L3 (appropriate)**: Right balance → Good results
- **L4 (too complex)**: Template for simple task → Wasted tokens, over-constrained

**LEVEL SELECTION CRITERIA:**

- **L1**: Single-sentence outcome (quick clarifications)
- **L2**: Context-rich paragraph (most prompts - **DEFAULT**)
- **L3**: Structured bullets (complex tasks, multiple constraints)
- **L4**: Template/framework (ONLY for reusable patterns)

**CRITICAL**: Default to L2. Only use L3/L4 when justified. Over-structuring wastes tokens and under-structuring misses requirements.

---

## Core Methodology

**FROM_SCRATCH method**: Convert user's goal/topic into outcome + minimal context + hard constraints
**REFINE method**: Delete fluff, keep only constraints that actually change the answer

**Default**: Produce prompts as a single plain-text paragraph (no Markdown)
**Escalate**: Use keypoints (L3) and templates (L4) only when justified

## Non-Negotiables to Preserve

**Always keep:**

- Tech stack/platform/environment constraints
- Forbidden approaches ("no external deps", "no web calls")
- Compliance requirements
- Hard output format requirements (must be JSON / must be ≤N words)
- Measurable success targets (latency, accuracy, coverage)

## Execution Process

**When user provides prompt to refine:**

### STEP 1: Parse Input

- Extract user's raw prompt text
- Determine if FROM_SCRATCH or REFINE scenario
- Identify missing context, constraints, or deliverables

### STEP 2: Apply Refinement

- **FROM_SCRATCH**: Convert goal → outcome + context + hard constraints
- **REFINE**: Remove step-by-step instructions, obvious best practices, tone fluff, redundant examples
- **Keep**: Only constraints that actually change the answer

### STEP 3: Structure Output

Generate exactly:

- **L1**: One-sentence outcome statement
- **L2**: Context-rich paragraph with constraints (no Markdown)
- **L3**: Structured bullets (Task/Constraints/Output)
- **L4**: Template/framework (only if complex/reusable)
- **Rationale**: 2-4 sentences explaining minimal-yet-sufficient approach

### STEP 4: Deliver

Output ONLY the refined prompt in the exact format:

```
L1: [outcome statement]
L2: [context-rich paragraph with constraints]
L3:
- **Task:** [description]
- **Constraints:** [key constraints]
- **Output:** [deliverables]
L4:
```

[TEMPLATE ONLY IF JUSTIFIED - use ```code blocks for templates]

```
Rationale: [2-4 sentences explaining approach]
```

## Example

**Input**: "Create a marketing website"

**Output:**

```
L1: Create a conversion-optimized landing page
L2: You are a senior web developer creating a high-converting landing page for [PRODUCT]. Focus on clear value proposition, social proof placement, and frictionless CTA design. Use modern CSS Grid/Flexbox layouts with mobile-first approach. Ensure WCAG 2.1 AA accessibility compliance. Prioritize page speed optimization and SEO fundamentals. Output a complete, deployable website with semantic HTML, optimized images, and conversion tracking setup.
L3:
- **Task:** Create landing page for [PRODUCT] with conversion optimization
- **Constraints:** Mobile-first responsive design; WCAG 2.1 AA accessibility; <3s load time; semantic HTML; SEO-ready
- **Output:** Complete deployable website with HTML/CSS/JS files + performance audit + accessibility report
L4:
```

# Landing Page Requirements

## Value Proposition

- [Clear benefit statement in headline]
- [Supporting subheading]
- [Visual hero element]

## Conversion Elements

- [Primary CTA placement]
- [Secondary CTA for hesitant users]
- [Social proof testimonials]

## Technical Specs

- Responsive breakpoints: 320px, 768px, 1024px
- Performance budget: <150KB total, <3s load
- Accessibility: WCAG 2.1 AA checklist

```
Rationale: The refined prompt provides clear technical constraints (mobile-first, WCAG compliance, performance budget) while maintaining creative flexibility. The L4 template ensures consistent deliverable structure across different landing pages while allowing product-specific customization.
```

## Critical Rules

- **Output ONLY the refined prompt** - never the methodology
- **Use L4 template** only for complex or reusable scenarios
- **Maintain all non-negotiable constraints** from original input
- **Ask at most ONE question** if ambiguity blocks producing useful refinement

**Contrast:**

```
Good: Output L1→L2→L3→L4→Rationale format
Good: Remove fluff, keep constraints that change answers
Bad: Include methodology explanation in output
Bad: Use L4 when simple prompt
```

**Validation check:** Refinement provides clear, actionable instructions if it includes: 1) L1 outcome statement, 2) L2 context with constraints, 3) L3 structure, 4) L4 template if needed.

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---

<critical_constraint>
MANDATORY: Output ONLY the refined prompt (no methodology explanations)
MANDATORY: Default to L2 unless complexity justifies L3/L4
MANDATORY: Preserve all non-negotiable constraints from original input
MANDATORY: Ask at most ONE question if ambiguity blocks refinement
No exceptions. Refinement is about clarity, not elaboration.
</critical_constraint>
