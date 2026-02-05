---
name: needs-articulation
description: Distinguish user wants from underlying needs to guide solution design. Use when stakeholders make feature requests or during Define phase.
---

# Needs Articulation

## Overview
Clearly articulate what stakeholders actually need (vs. what they ask for) to guide solution design.

## When to Use
- After conducting research with stakeholders
- When stakeholders make feature requests
- During Define phase when framing the problem
- When evaluating ideas against user needs

## How to Apply

### 1. Distinguish Wants from Needs
Users often express solutions, not underlying needs:

**User says**: "I want a dashboard with 20 widgets"
**Underlying need**: "I need to monitor system health without checking multiple places"

**User says**: "Add more features like Tool X"
**Underlying need**: "I need to accomplish Y task more efficiently"

### 2. Ask "Why" Repeatedly
Use the 5 Whys technique:

**Request**: "Make the button bigger"
- **Why?** "Hard to click on mobile"
- **Why?** "I'm wearing gloves in the field"
- **Why?** "Can't remove gloves, hands get dirty/cold"
- **Why?** "Environmental conditions require protective equipment"

**Need**: Design for gloved interaction in field conditions

### 3. Express as User Needs
Format: **[Stakeholder]** needs **[capability]** so they can **[outcome]**

Examples:
- "Field technicians need offline data access so they can work in low-connectivity areas"
- "Managers need aggregated team metrics so they can identify bottlenecks quickly"
- "New users need clear onboarding so they can become productive without training"

### 4. Validate Needs
Check with stakeholders:
- Show them your articulation
- Ask if it captures their situation accurately
- Look for recognition: "Yes, that's exactly it!"
- Refine based on feedback

### 5. Prioritize Needs
Not all needs are equal:
- **Critical**: Without this, solution fails for this stakeholder
- **Important**: Significantly impacts experience or efficiency
- **Nice-to-have**: Improves experience but not essential

### 6. Document in currentstate.json
Update stakeholder profiles:

```json
{
  "id": "s1",
  "name": "Field Technician",
  "type": "group",
  "needs": [
    "Work effectively in low/no connectivity areas",
    "Quick data capture with minimal interaction",
    "Reliable sync when back online"
  ],
  "pain_points": [
    "Data loss when connection drops",
    "Too many steps to log information",
    "Interface unusable with gloves"
  ]
}
```

## Red Flags

Watch out for:
- **Assumed needs**: "Users need feature X" (no, they need outcome Y)
- **Technology-first**: "Users need an API" (no, they need integration)
- **One size fits all**: Different stakeholders have different needs
- **Feature requests**: Focus on the problem, not the solution

## Tips
- Listen for frustration and workarounds
- Observe behavior, not just stated preferences
- Test your articulation with stakeholders
- Needs are timeless, solutions change
- One pain point may reveal multiple needs
- Prioritize ruthlessly
- Keep updating as you learn more
