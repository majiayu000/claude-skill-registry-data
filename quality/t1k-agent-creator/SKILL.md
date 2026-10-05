---
name: t1k:agent-creator
description: "Create or update TheOneKit agent .md files with canonical structure. Use when adding a new agent, updating maxTurns/model, or fixing frontmatter fields."
keywords: [agent, create, update, maxturn, model, frontmatter, scaffold]
version: 1.0.0
effort: medium
argument-hint: "[agent-name]"
origin: theonekit-core
repository: The1Studio/theonekit-core
module: null
protected: true
---

# Agent Creator

Create new agent .md files or update existing ones for TheOneKit. Enforces the canonical agent structure.

## Required Frontmatter

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | kebab-case, must match filename |
| `description` | Yes | 2-5 `<example>` blocks with `<commentary>` |
| `model` | Yes | `inherit`, `sonnet`, `opus`, or `haiku` |
| `maxTurns` | Yes | 15-50 based on role |
| `color` | Suggested | Consistent per role |
| `origin/module/protected` | NO | CI-injected only — never add manually |

## Recommended maxTurns

| Role | Range |
|------|-------|
| implementer / kit-developer | 40-50 |
| debugger | 35-40 |
| tester | 30-35 |
| planner / brainstormer | 25-30 |
| reviewer | 25-30 |
| docs / git / utility | 15-25 |

## Required Body Sections (in order)

1. **Opening:** "You are a [specific role]..."
2. **Routing guard** (if applicable): scope boundary + delegation targets
3. **Mandatory skills:** Ordered table with activation triggers
4. **Constraints:** Enforced rules (NEVER/ALWAYS/DO NOT)
5. **Workflow:** Numbered steps with verification checkpoints
6. **Output format:** Structured markdown template
7. **Completion gates:** Verifiable, tool-referenced, severity-marked (BLOCKING/MANDATORY)
8. **Module awareness** (if applicable)

## Process

1. Ask user for: role name, scope, which kit/layer, key skills
2. Read 2 existing agents as reference (matching role type)
3. Draft agent following canonical structure
4. Validate:
   - All required frontmatter present
   - 2+ examples in description
   - All 7 body sections present
   - Completion gates are verifiable
   - maxTurns justified
5. If routing needed: update `t1k-routing-{layer}.json`
6. If activation needed: update `t1k-activation-{layer}.json`

## Cognitive Framing (MANDATORY for all new agents)

Every new agent MUST include a persona line as the first sentence of the body (after frontmatter).

**Format:** "You are a **{Role Title}** who/performing {behavioral description in 1-2 sentences}."

**Examples:**
- "You are a **Staff Engineer** hunting production bugs — you distrust obvious answers and prove root cause before proposing any fix."
- "You are a **Detective** performing systematic investigation. You form hypotheses, gather evidence, and never assume."
- "You are a **Tech Lead** designing system architecture — you optimize for long-term maintainability over short-term convenience."
- "You are a **QA Lead** performing systematic verification — you hunt for untested code paths and think like someone burned by production incidents."

**Why it matters:** The persona shapes reasoning quality throughout the agent's entire run. Generic descriptions ("you are a developer") produce generic, shallow output. Specific behavioral frames ("you distrust obvious answers") activate different reasoning patterns.

**Validation:** If the opening line does not name a concrete role with a behavioral trait, reject and rewrite.

## Anti-Patterns to Avoid

- Vague role ("a developer") — must be specific with behavioral trait
- Missing cognitive framing persona as first body line
- "Activate skills as needed" (must be explicit)
- No completion gates
- No routing guard when scope overlaps with other agents
- maxTurns >50
- Adding origin/module/protected manually
