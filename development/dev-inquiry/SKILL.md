---
name: dev-inquiry
description: Developer inquiry skill for technical investigation, validation, and decision-making. Use when exploring unfamiliar technology, validating approaches with spikes, comparing options, or making architecture decisions. Covers the full thinking process from "I don't know" to confident decision.
---

# Dev Inquiry

Feynman-style technical inquiry for developers. Understand before you decide. Validate before you build.

> "The first principle is that you must not fool yourself—and you are the easiest person to fool." — Richard Feynman

## Inquiry Modes

This skill supports four modes that often chain together:

| Mode | When to Use | Trigger Phrases |
|------|-------------|-----------------|
| **Investigate** | Understand something unfamiliar | "explore", "understand", "how does X work" |
| **Spike** | Validate approach before building | "spike", "validate", "prove this works" |
| **Compare** | Evaluate options for your context | "compare", "vs", "which is better" |
| **Decide** | Make a concrete choice | "should we", "decide", "recommend" |

## How to Use This Skill

1. **Identify the mode** from the user's request
2. **Load the appropriate reference**:
   - Investigation → Read `references/investigation.md`
   - Spike validation → Read `references/spike.md`
   - Comparison → Read `references/scoring.md`
   - Decision → Read `references/scoring.md` (uses comparison + decision framework)
3. **Follow the workflow** in that reference
4. **Chain if needed** — investigation often leads to spike, spike informs comparison

## Mode Details

### Investigate Mode

For understanding unfamiliar technology from first principles.

**Process**: Admit ignorance → Simplest experiment → Poke edges → Build mental model → Explain simply

**Output**: Mental model you can teach to someone else

### Spike Mode

For validating technical feasibility before full implementation.

**Process**: Define scope (4-8 hours) → Write tests first → Implement minimal → Test with real data → Document pattern

**Output**: Proven pattern ready to replicate, or pivot decision

### Compare Mode

For evaluating multiple options against your specific context.

**Process**: Define context → Choose criteria → Weight by importance → Score with evidence → Sanity check

**Output**: Weighted comparison matrix with evidence

### Decide Mode

For making a concrete choice with documented reasoning.

**Process**: Ensure understanding (investigate if needed) → Compare options → State recommendation → Document tradeoffs → Assess reversibility

**Output**: Clear recommendation with rationale and risks

## The Natural Flow

```
"Let's explore @Observable"
        ↓ Investigation
"Can I actually build nested observation?"
        ↓ Spike (validates understanding)
"@Observable vs @StateObject for my app"
        ↓ Comparison
"Should we adopt the new Observation framework?"
        ↓ Decision
```

Each mode builds on the previous. Don't decide before you understand. Don't compare before you investigate.

## Quick Reference

| Request | Mode | Reference |
|---------|------|-----------|
| "Let's explore Swift macros" | Investigate | `references/investigation.md` |
| "I want to understand async/await" | Investigate | `references/investigation.md` |
| "Spike SwiftData before we commit" | Spike | `references/spike.md` |
| "Validate this architecture works" | Spike | `references/spike.md` |
| "Compare REST vs GraphQL" | Compare | `references/scoring.md` |
| "SwiftData vs CoreData?" | Compare | `references/scoring.md` |
| "Should we use Combine?" | Decide | `references/scoring.md` |
| "Recommend an approach" | Decide | `references/scoring.md` |

## Examples

For concrete examples across all modes, see `references/examples.md`.
