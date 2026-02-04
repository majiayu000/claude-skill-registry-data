---
name: wolf-session-init
description: **MANDATORY** Use at the start of EVERY session before any work - establishes Wolf behavioral framework and ensures all required skills are loaded and chained properly
version: 1.0.0
triggers:
  - "session start"
  - "new task"
  - "context recovery"
  - "begin work"
  - "start implementation"
---

# Wolf Session Initialization

**MANDATORY PROTOCOL - NO EXCEPTIONS**

This skill MUST be used at the start of EVERY work session to establish the complete Wolf behavioral framework. Skipping this protocol causes agents to operate without proper guidance, leading to governance violations, skipped quality gates, and wasted effort.

## When to Use This Skill

**ALWAYS** - This is not optional:
- ✅ At the start of every new session
- ✅ After context compaction or recovery
- ✅ When starting any new task or work item
- ✅ Before beginning implementation
- ✅ When role or archetype changes

**This skill replaces ad-hoc skill loading with systematic initialization.**

## MANDATORY FIRST RESPONSE PROTOCOL

```
BLOCKING GATES - Cannot proceed without completion
```

Before responding to ANY user request or starting ANY work, you **MUST** complete this checklist IN ORDER:

### Step 1: Query Wolf Principles (BLOCKING) ⚠️

**Purpose**: Load strategic decision-making guidance

**Action**: Use the Skill tool to load **wolf-principles**

**Gate**: Cannot proceed without principles loaded

**Why**: Principles guide ALL decisions. Operating without principles = operating blind.

**Verification**: Confirm you can articulate relevant principles for the task

---

### Step 2: Find Behavioral Archetype (BLOCKING) ⚠️

**Purpose**: Determine work type and behavioral profile

**Action**: Use the Skill tool to load **wolf-archetypes**

**Gate**: Cannot proceed without archetype selection

**Why**: Archetypes define priorities, evidence requirements, and quality gates specific to work type.

**Verification**: Confirm archetype selected (e.g., `product-implementer`, `security-hardener`, `reliability-fixer`)

---

### Step 3: Load Governance Requirements (BLOCKING) ⚠️

**Purpose**: Understand Definition of Done and quality gates

**Action**: Use the Skill tool to load **wolf-governance**

**Gate**: Cannot start work without knowing acceptance criteria

**Why**: Governance defines WHAT constitutes complete, acceptable work.

**Verification**: Can list DoD requirements (tests, docs, journal, review, CI)

---

### Step 4: Load Role Guidance (BLOCKING) ⚠️

**Purpose**: Understand role responsibilities and boundaries

**Action**: Use the Skill tool to load **wolf-roles**

**Gate**: Cannot execute work without understanding role boundaries

**Why**: Roles define WHO does what and HOW. Operating outside role boundaries violates governance.

**Verification**: Can articulate role responsibilities and non-goals

---

## Session Initialization Checklist

Copy this checklist at the start of EVERY session:

```
Wolf Session Initialization - MANDATORY
========================================

[ ] Step 1: Principles Loaded
    Tool: Skill tool → wolf-principles
    Result: _______________________________________

[ ] Step 2: Archetype Selected
    Tool: Skill tool → wolf-archetypes
    Result: _______________________________________

[ ] Step 3: Governance Loaded
    Tool: Skill tool → wolf-governance
    DoD Requirements: ______________________________

[ ] Step 4: Role Guidance Loaded
    Tool: Skill tool → wolf-roles
    Role: __________________________________________

[ ] All Gates Passed - Ready to Begin Work ✅
```

**ALL checkboxes MUST be checked before starting implementation.**

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"I'll check principles later"** - NO. Principles come FIRST. They guide all subsequent decisions.
- ❌ **"Task is too simple for full protocol"** - Wrong. ALL tasks follow protocol. Size doesn't matter.
- ❌ **"I already know my archetype"** - Evidence-based selection required. Don't assume.
- ❌ **"I'll skip governance for speed"** - Skipping governance SLOWS you down through rework.
- ❌ **"I remember my role from last session"** - Role cards evolve. Load current guidance.
- ❌ **"This is just exploration, no need for protocol"** - Exploration uses `research-prototyper` archetype. Still requires protocol.
- ❌ **"I'll load governance after I start coding"** - Too late. Governance guides implementation choices.

**STOP. Return to Step 1. Complete the protocol.**

## What Happens After Initialization

Once all 4 steps are complete, you have established:

### ✅ Complete Behavioral Context

1. **Strategic Guidance** (Principles)
   - Decision-making framework active
   - Trade-off evaluation criteria loaded
   - Evidence requirements understood

2. **Tactical Profile** (Archetype)
   - Work type identified
   - Evidence requirements specific to this work
   - Priority order established
   - Lenses applied if needed (security/perf/a11y/observability)

3. **Quality Framework** (Governance)
   - Definition of Done understood
   - Quality gates identified
   - Approval requirements known
   - Compliance requirements clear

4. **Execution Context** (Role)
   - Responsibilities clear
   - Boundaries understood
   - Collaboration patterns loaded
   - Escalation paths identified

### 🚀 Ready to Execute

With initialization complete, you can now:
- Begin implementation with confidence
- Make decisions aligned with principles
- Produce evidence meeting archetype requirements
- Follow governance gates automatically
- Operate within role boundaries

## Common Initialization Patterns

### Pattern 1: New Feature Development

```yaml
Session Start:
  Step 1: Query principles → Focus on #1 (Artifact-First), #9 (Incremental Value)
  Step 2: Find archetype → Result: product-implementer
  Step 3: Load governance → DoD: AC met, tests, docs, journal, review
  Step 4: Load role → Role: coder-agent

Ready to Code:
  - Write tests first
  - Implement incrementally
  - Update docs continuously
  - Create journal entry
  - Request review from code-reviewer-agent
```

### Pattern 2: Security Issue

```yaml
Session Start:
  Step 1: Query principles → Focus on #5 (Evidence-Based), #2 (Role Isolation)
  Step 2: Find archetype → Result: security-hardener
  Step 3: Load governance → DoD: Threat model, scan, pen test
  Step 4: Load role → Role: security-agent

Ready to Secure:
  - Create threat model
  - Run security scans
  - Implement defense-in-depth
  - Document in journal
  - Can block merges if gates fail
```

### Pattern 3: Bug Fix

```yaml
Session Start:
  Step 1: Query principles → Focus on #3 (Research-Before-Code), #6 (Self-Improving)
  Step 2: Find archetype → Result: reliability-fixer
  Step 3: Load governance → DoD: Root cause, regression test, monitoring
  Step 4: Load role → Role: error-forensics-agent → coder-agent

Ready to Fix:
  - Document root cause analysis
  - Add regression test (watch it fail)
  - Implement fix (watch test pass)
  - Enhance monitoring
  - Create journal entry with learnings
```

## Context Recovery Protocol

If context is compacted or lost during session, re-run initialization:

```yaml
Context Lost Event:
  1. Detect: Unable to recall principles/archetype/governance/role
  2. Stop: Halt current work immediately
  3. Re-initialize: Run full 4-step protocol again
  4. Verify: Confirm context matches pre-compaction state
  5. Resume: Continue work with restored context
```

**Why**: Operating with partial context is worse than stopping to recover. Incomplete context leads to governance violations.

## Anti-Patterns (Forbidden)

### ❌ Partial Initialization
- Loading only principles but skipping archetype
- Loading role but skipping governance
- ANY incomplete initialization

**Why**: Each step builds on the previous. Missing steps = missing critical context.

### ❌ Assumed Context
- "I remember from last session"
- "This is obvious, no need to load"
- "I already know what to do"

**Why**: Context evolves. Role cards update. Governance changes. Always load fresh.

### ❌ Post-Hoc Loading
- Starting implementation, then loading governance
- Coding first, checking archetype later
- "I'll initialize once I understand the task"

**Why**: Initialization GUIDES work. Loading after starting = rework.

## After Using This Skill

**REQUIRED NEXT STEPS:**

Session initialization is COMPLETE. You are now ready to begin work with full behavioral context.

### RECOMMENDED NEXT SKILLS (depending on task):

1. **If implementing code**: Use **wolf-workflows** to select appropriate workflow (feature, security, bugfix)
   - **Why**: Workflows orchestrate multi-agent processes with decision gates
   - **MCP Tool**: Load wolf-workflows skill to select template

2. **If needs research**: Use **wolf-workflows bugfix or research patterns**
   - **Why**: Research-before-code prevents wrong implementation
   - **Pattern**: Time-boxed spikes with proof-of-concept

3. **During implementation**: Use **wolf-verification** for checkpoint validation
   - **Why**: Catch issues early rather than at review time
   - **Tool**: Use Skill tool to load wolf-verification skill

4. **For architecture decisions**: Use **wolf-adr** to document decisions
   - **Why**: Future teams need context for why decisions were made
   - **Tool**: Load wolf-adr skill when making architectural choices

### Optional Skills (context-dependent):

- **wolf-instructions**: Load domain/project-specific guidance
- **wolf-scripts-core**: Automated archetype/governance validation
- **wolf-scripts-agents**: Multi-agent coordination scripts

**Session initialization ALWAYS comes first. Other skills follow as needed.**

---

## Good/Bad Examples

### Example 1: Proper Session Initialization

<Good>
**Scenario**: Agent starts new feature task

**Agent Actions**:
1. ✅ Loads wolf-session-init skill
2. ✅ Uses Skill tool to load wolf-principles → Receives principles #1, #9
3. ✅ Uses Skill tool to load wolf-archetypes → Receives archetype: product-implementer
4. ✅ Uses Skill tool to load wolf-governance → Receives DoD: tests, docs, journal, review
5. ✅ Uses Skill tool to load wolf-roles → Receives role card with responsibilities
6. ✅ Completes checklist: All 4 steps checked ✅
7. ✅ Begins implementation with full context

**Why GOOD**:
- Followed 4-step protocol in order
- Used Skill tool to load each component
- Verified all gates before starting work
- Has complete behavioral context (principles, archetype, governance, role)
- Can articulate DoD, evidence requirements, and role boundaries
</Good>

---

### Example 2: Skipped Initialization (Common Failure)

<Bad>
**Scenario**: Agent starts new feature task

**Agent Actions**:
1. ❌ Reads task description
2. ❌ Immediately starts writing code without initialization
3. ❌ Halfway through, realizes requirements unclear
4. ❌ Guesses at architecture instead of following principles
5. ❌ Completes implementation
6. ❌ Code reviewer rejects: Missing tests, wrong archetype, violated governance
7. ❌ 3 days of rework required

**Why BAD**:
- Skipped entire initialization protocol
- Operated without principles (made arbitrary decisions)
- No archetype selected (used wrong priorities and evidence requirements)
- No governance loaded (didn't know DoD)
- No role loaded (violated boundaries)
- Result: Expensive rework that initialization would have prevented
- **Time wasted**: 3 days vs 5 minutes of initialization
</Bad>

---

### Example 3: Partial Initialization (Also Wrong)

<Bad>
**Scenario**: Agent starts bug fix task

**Agent Actions**:
1. ⚠️ Loads wolf-session-init skill
2. ✅ Uses Skill tool to load wolf-principles → Receives principles
3. ❌ Skips archetype selection ("I know it's a bug fix")
4. ❌ Skips governance loading ("I'll check later")
5. ✅ Uses Skill tool to load wolf-roles → Receives role
6. ❌ Starts implementation with partial context
7. ❌ Code reviewer rejects: Missing regression test (governance requirement), wrong evidence type (archetype requirement)

**Why BAD**:
- Partial initialization is NOT sufficient
- Assumed archetype without evidence-based selection (should be reliability-fixer, not generic)
- Skipped governance (didn't know regression test required)
- Each step builds on previous - missing steps = missing critical context
- **Time wasted**: 1 day of rework vs 2 extra minutes to complete initialization
</Bad>

---

## Integration with Other Skills

After completing session initialization, you may invoke other specialized skills:

- **wolf-verification**: For checkpoint validation during work
- **wolf-scripts-core**: For automated archetype/governance checks
- **wolf-adr**: For architecture decision documentation
- **wolf-instructions**: For domain/project-specific guidance

**But initialization ALWAYS comes first.**

## Success Metrics

### Before Session Initialization Skill

- Agents skip archetype selection: ~60%
- Agents skip governance checks: ~70%
- Agents claim completion without verification: ~50%
- Agents operate outside role boundaries: ~40%

### After Session Initialization Skill

- Agents skip archetype selection: <5% (blocked by gates)
- Agents skip governance checks: <10% (blocked by gates)
- Agents claim completion without verification: <5% (checklist required)
- Agents operate outside role boundaries: <5% (role card loaded)

## Validation

To verify initialization worked correctly, agent should be able to answer:

1. **Principles**: What principles guide this work?
2. **Archetype**: What is my behavioral archetype and why?
3. **Governance**: What is my Definition of Done?
4. **Role**: What are my responsibilities and boundaries?

**Cannot answer all 4? Initialization incomplete. Return to Step 1.**

---

## Summary

**Wolf Session Initialization is MANDATORY and BLOCKING.**

```
Every session MUST start with:
1. Query principles
2. Find archetype
3. Load governance
4. Load role

No exceptions. No shortcuts. No assumptions.
```

**Why**: These 4 steps establish the complete behavioral context needed to produce high-quality, governance-compliant work efficiently.

**When to use**: At the start of EVERY session, BEFORE any work begins.

**Verification**: Complete the checklist. If you can't check all boxes, initialization is incomplete.

---

## Verification Checklist

Before claiming session initialization is complete:

- [ ] Used Skill tool to load wolf-principles and received principles
- [ ] Used Skill tool to load wolf-archetypes and received archetype
- [ ] Used Skill tool to load wolf-governance and received governance requirements
- [ ] Used Skill tool to load wolf-roles and received role card
- [ ] Can articulate principles guiding this work
- [ ] Can explain archetype and why it was selected
- [ ] Can list Definition of Done requirements
- [ ] Can describe role responsibilities and boundaries

**Can't check all boxes? Initialization incomplete. Return to Step 1.**

---

*Last Updated: 2025-11-14*
*Phase: Skill-Chaining Enhancement v3.0.0*
*Version: 1.1.0*
