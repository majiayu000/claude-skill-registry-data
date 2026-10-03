---
name: conflict-resolution
description: >
  Use when two or more agents produce conflicting outputs, recommendations, or
  decisions. This skill provides a structured process for resolving disagreements
  between agents, ensuring conflicts are resolved fairly with clear reasoning and
  documented decisions.
---

# Conflict Resolution

## Overview
This skill handles situations where multiple agents produce conflicting information, recommendations, or decisions. Unresolved conflicts can cause downstream errors, wasted work, and system inconsistency. Use this skill whenever conflicting outputs are detected.

## When to Use
- When two agents give contradictory analysis or recommendations
- When code from different agents conflicts (different styles, approaches, versions)
- When research findings contradict each other
- When different companies have incompatible standards or approaches
- When knowledge base entries conflict with each other
- **Don't use when:** Differences are preferences with no functional impact, or one source is clearly superseded

## Core Procedures

### Step 1: Identify the Conflict
Document specifically what conflicts:
- Agent A states: [what A says]
- Agent B states: [what B says]
- Conflict point: [exactly what disagrees]

### Step 2: Assess Conflict Type
| Type | Description | Resolution Approach |
|------|-------------|-------------------|
| Factual | Different claims about reality | Source verification against authoritative source |
| Technical | Different technical approaches | Evaluate against requirements, test both |
| Standards | Different standards or conventions | Follow project/team standard, or agree on one |
| Priority | Different decisions about what matters | Escalate to decision-maker with both options |
| Temporal | One is outdated, one is current | Verify dates, supersede outdated information |

### Step 3: Resolve Conflict
Based on conflict type:

**FACTUAL CONFLICTS:**
1. Apply source-verification skill to both claims
2. Determine which claim has higher confidence
3. If both are HIGH confidence from credible sources, note context where each applies

**TECHNICAL CONFLICTS:**
1. List requirements both approaches must meet
2. Evaluate each approach against requirements
3. If both meet requirements, choose simpler/more maintainable
4. If neither clearly wins, escalate to domain specialist

**STANDARDS CONFLICTS:**
1. Check project/team documentation for stated standards
2. If standard exists, follow it
3. If no standard exists, propose one and escalate for decision
4. Document the decision for future reference

**PRIORITY CONFLICTS:**
1. Document both positions clearly
2. Evaluate trade-offs of each choice
3. Escalate to appropriate decision-maker (CEO, Council, project owner)
4. Implement the decision and document rationale

### Step 4: Document Resolution
```
CONFLICT RESOLUTION
===================
Conflict: [brief description]
Parties: [which agents or sources disagree]
Type: [factual/technical/standards/priority/temporal]

RESOLUTION:
[what was decided and why]

EVIDENCE:
[what supported the decision]

SUPERSEDES:
[which conflicting entry is now invalid - mark it as superseded]

APPLIES TO:
[scope of this resolution - what future situations this covers]
```

### Step 5: Propagate Resolution
1. Update any affected deliverables with the resolved position
2. Mark superseded/conflicting information as outdated
3. Notify affected agents of the resolution
4. Capture as knowledge for future conflicts

## Quality Checklist
- [ ] Conflict clearly identified with specific disagreement points
- [ ] Conflict type correctly classified
- [ ] Resolution based on evidence and clear reasoning
- [ ] Superseded information marked as such
- [ ] Resolution documented for future reference
- [ ] Affected parties notified

## Error Handling
- **Error:** Cannot determine authoritative source
  **Response:** Escalate to governance body (Council) with both positions documented
- **Error:** Resolution creates new conflicts with other information
  **Response:** Expand scope of resolution to cover all conflicting information
- **Error:** Parties reject the resolution
  **Response:** Escalate to their manager with full documentation of process used
- **Error:** Conflict is blocking critical work
  **Response:** Make interim decision based on best available information, flag for formal resolution

## Cross-Team Integration
**Related Skills:** source-verification, escalation-management, knowledge-capture, decision-logging
**Used By:** ALL agents, especially QualityForge (Guardian, Standards, Council) and governance agents