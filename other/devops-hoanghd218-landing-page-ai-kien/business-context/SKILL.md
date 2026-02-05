---
name: business-context
description: Access shared business context including company identity, mission, org chart, staff directory, and policies. Use this when an agent needs to understand the business they work for, organizational structure, who's who, or business policies. Returns content from org/business/ directory.
---

# Business Context

The Business Context skill provides read-only access to organizational information for Aphebis.

## Purpose

All agents need to understand the business they work for. Without shared context, each agent would need business information baked into its definition—creating maintenance overhead and potential inconsistencies.

This skill is the **single source of truth** for business context. Edit files in `org/business/` once, and all agents have access.

## Data Structure

```
org/business/
├── README.md         # This directory's overview
├── company.md        # Company identity, stage, industry
├── mission.md        # Mission, vision, values
├── org-chart.md      # Organizational structure, reporting
├── staff.md          # Humans, AI agents, skills
└── policies.md       # Financial, risk, technical policies
```

## Available Queries

| Query | Returns | Use When... |
|-------|---------|-------------|
| `company` | Company identity, stage, industry, description | You need to understand what Aphebis is |
| `mission` | Mission, vision, values, what we're not | You need to understand our purpose and principles |
| `org-chart` | Organizational structure, reporting relationships | You need to know who reports to whom, how the org works |
| `staff` | Personnel (humans + AI agents), contact protocols | You need to know who works here, how to reach them |
| `policies` | Financial, risk, technical, communication policies | You need to understand our constraints and guidelines |
| `all` | Complete business context summary | You need a comprehensive overview |

## Usage Patterns

### When an Agent Needs Context

**Before advising on a decision:**
```
"I need to understand Aphebis's risk tolerance before I can advise."
→ Invoke business-context with query: "policies"
→ Returns financial and risk policies for context
```

**Before making a recommendation:**
```
"Let me check our mission to ensure this aligns."
→ Invoke business-context with query: "mission"
→ Returns mission, vision, values
```

**When coordinating work:**
```
"Who should handle this technical question?"
→ Invoke business-context with query: "staff"
→ Returns staff directory with roles and reporting
```

### Direct File Access

If you need the raw file content for processing:
1. Read the file directly from `org/business/{filename}.md`
2. The files are plain markdown, easily parseable
3. Use this when you need to extract specific information programmatically

## Scope

This skill is **READ-ONLY**. It cannot modify business context files.

**To update business context:**
- Edit files directly in `org/business/`
- Changes are immediately available to all agents
- Git provides version history

## Integration Guidelines

### For Agent Creators

When creating a new agent:

1. **Add the agent to staff.md** - Document the agent's role, manager, model
2. **Reference this skill in agent instructions** - Tell the agent when to query context
3. **Consider adding to org-chart.md** - If the agent has a management role

Example agent instruction:
```
When making business recommendations, always invoke the business-context skill
first to understand our current mission, values, and policies.
```

### For Skill Creators

When creating a new skill:

1. **Add the skill to staff.md** - Document purpose, access, notes
2. **Consider if skill needs business context** - Many operational skills don't need it
3. **Update org-chart.md if relevant** - For skills that fit into reporting structure

## Examples

### Example 1: Business Planning

**Agent:** business-manager
**Situation:** Evaluating a new market opportunity

```
"Before I assess this market opportunity, I need to understand our strategic
position and risk tolerance."

→ business-context query: "company" + "policies"

→ Returns: Aphebis is bootstrapped, risk-tolerant on product/technical,
         risk-averse on legal/compliance, must prove ROI for expenses

→ Agent now has proper context to evaluate the opportunity
```

### Example 2: Technical Decision

**Agent:** technical-strategy-advisor
**Situation:** Recommending a technology stack

```
"I need to understand our technical policies and constraints before
recommending an architecture."

→ business-context query: "policies"

→ Returns: Agent-first architecture, MCP-native, simple scales,
         no vendor lock-in

→ Agent ensures recommendation aligns with policies
```

### Example 3: Agent Coordination

**Agent:** Any agent
**Situation:** Unsure who to escalate to

```
"Who handles compliance questions?"

→ business-context query: "staff"

→ Returns: Technical Strategy Advisor handles compliance; reports to Alex

→ Agent knows to escalate to technical-strategy-advisor
```

## Error Handling

If a query fails:
1. Check that the file exists in `org/business/`
2. Verify the query name matches available options
3. If file is missing, state: "Business context file '{name}.md' not found."
4. Suggest the user create the file or try a different query

## Future Enhancements

Potential additions to the business context system:
- `products.md` - Product catalog, features, roadmap
- `competitors.md` - Competitive landscape analysis
- `customers.md` - Customer personas, segments (when we have them)
- `metrics.md` - Key business metrics (when we track them)
- `context-summary.json` - Machine-readable quick reference

Additions should follow the same pattern:
1. Create `.md` file in `org/business/`
2. Add query option to this skill definition
3. Update this README with the new category
