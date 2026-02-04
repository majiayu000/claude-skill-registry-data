---
name: wolf-instructions
description: Four-level instruction cascading system (Global → Domain → Project → Role) with priority-based conflict resolution
version: 1.1.0
category: agent-coordination
triggers:
  - instruction cascade
  - agent instructions
  - role boundaries
  - authority matrix
  - agent coordination
dependencies:
  - wolf-roles
  - wolf-governance
  - wolf-principles
size: large
---

# Wolf Instruction Cascading System

Four-level instruction hierarchy that ensures consistent agent behavior across 43 roles while allowing environment-specific and role-specific customization.

## Overview

Wolf's instruction system prevents duplication while enabling specialization through a clear hierarchy:

1. **Global Instructions** (21 files) - Universal policies applying to ALL agents
2. **Domain Instructions** (3 files) - Technical domain patterns (web, data, ops)
3. **Project Instructions** (3 files) - Environment-specific overrides
4. **Role Instructions** - Role-specific behavior (in role-card.md files)
5. **Variant Instructions** - Stack-specific customization

**Key Principle**: Closest instruction wins on conflicts. Project > Role/Variant > Domain > Global.

---

## 📚 Instruction Hierarchy

### Reading Order (Every Agent MUST Follow)

```
1. Read ALL Global Instructions (21 files)
   └─> Universal policies that cannot be overridden (security, governance)
   └─> Common patterns (GitHub coordination, communication, journaling)

2. Read Relevant Domain Instructions (1-3 files)
   └─> web.md (for web development roles)
   └─> data.md (for data processing roles)
   └─> ops.md (for operations/DevOps roles)

3. Read ALL Project Instructions (3 files)
   └─> repository-operations.md (GitHub CLI patterns)
   └─> multi-instance-coordination.md (Multi-repo coordination)
   └─> production-patterns.md (Production-ready patterns)

4. Read Role-Specific Instructions
   └─> Continue reading role-card.md for role behavior

5. Read Variant-Specific Instructions (if applicable)
   └─> Stack-specific tooling and patterns
```

### Priority Order (Conflict Resolution)

When instructions conflict, apply this priority (highest wins):

```
1. Project Instructions       # Environment-specific overrides
2. Role/Variant Instructions   # Specific role behavior
3. Domain Instructions         # Technical domain patterns
4. Global Instructions         # Universal agent behavior
```

**Example Conflict**:
- Global: "Use 2-space indentation"
- Project: "Use 4-space indentation for this codebase"
- **Result**: Use 4-space indentation (Project wins)

**Non-Overridable Global Policies**:
- Security standards (no plaintext secrets, auth requirements)
- Governance gates (evidence requirements, PR standards)
- Identity verification (heartbeat protocol)
- SLA requirements

---

## 🌍 Global Instructions (21 files)

Location: `/agents/instructions/global/`

### Core Coordination

#### 1. **identity-heartbeat.md**
**Purpose**: Identity verification every 5 minutes to prevent context drift

**Key Requirements**:
```markdown
Every 5 minutes, agents MUST verify:
- Current role (pm-agent, coder-agent, etc.)
- Current archetype (if applicable)
- Current phase of work
- Active lenses (performance, security, etc.)

If identity cannot be verified → STOP and request clarification
```

**When to Use**:
- Start of every agent session
- After context compaction events
- When switching between tasks
- Every 5 minutes during long sessions

#### 2. **eight-phase-methodology.md** / **wolf-8-v2-methodology.md**
**Purpose**: Standard 8-phase work methodology

**Phases**:
```
Phase 1: Introspection  - Understand requirements
Phase 2: Research       - Gather evidence
Phase 3: Strategy       - Design approach
Phase 4: Prototype      - Build proof-of-concept
Phase 5: Execute        - Implement solution
Phase 6: Validate       - Test and verify
Phase 7: Journal        - Document learnings
Phase 8: Reality Check  - Verify meets requirements
```

**When to Use**:
- All non-trivial work items
- Feature development
- Bug fixes requiring investigation
- Research spikes

#### 3. **github-coordination.md**
**Purpose**: GitHub issue/PR coordination patterns

**Key Patterns**:
```markdown
# Issue Workflow
intake → pm-ready → review-ready → qa-ready → release-ready → deployed

# PR Standards
- Link to parent issue
- Include evidence (screenshots, benchmarks, etc.)
- Follow archetype-specific PR template
- Apply appropriate labels

# Label Usage
- agent:<role> for agent assignments
- archetype:<type> for behavioral profile
- lens:<name> for overlay requirements
- status:<state> for workflow tracking
```

**When to Use**:
- Creating issues or PRs
- Transitioning workflow states
- Coordinating multi-agent workflows

#### 4. **authority-matrix.md**
**Purpose**: Agent authority boundaries and conflict resolution

**Authority Hierarchy**:
```
| Domain                  | Authority        | Examples                      |
|-------------------------|------------------|-------------------------------|
| Requirements & Scope    | PM Agent         | What to build, timeline       |
| Technical Architecture  | Reviewer Agent   | Code patterns, system design  |
| Test Strategy           | QA Agent         | What to test, coverage        |
| Performance/Security    | GLOBAL POLICY    | Cannot be overridden          |
```

**Escalation Path**:
```
Direct Conflict → Authority Agent → Orchestrator (final)
```

**When to Use**:
- Resolving conflicts between agents
- Determining decision authority
- Escalating blocked decisions

#### 5. **communication.md**
**Purpose**: Inter-agent communication standards

**Communication Channels**:
```markdown
1. GitHub Comments - Asynchronous, audit trail
2. Mailbox System - Structured messages (see wolf-scripts-agents)
3. Workflow Signals - Structured handoffs (AGENT_HANDOFF_TO)
4. Labels - State communication (agent:pm-agent)
```

**Message Format**:
```markdown
## To: <target-agent>
## From: <source-agent>
## Subject: <concise-summary>

### Context
[Background and current state]

### Request
[What needs to be done]

### Evidence
[Supporting information, links, data]

### Success Criteria
[How to know when done]
```

**When to Use**:
- Agent handoffs
- Requesting work from another agent
- Reporting completion
- Escalating issues

#### 6. **journaling.md**
**Purpose**: Work documentation requirements

**Journal Structure**:
```markdown
# YYYY-MM-DD: <Kebab-Case-Title>

## Problems Encountered
- [Specific problem with context]

## Decisions Made
- [Decision with rationale]

## Learnings
- [What was learned, pattern extracted]

## References
- [Links to issues, PRs, docs]
```

**Location**: `agents/roles/<role>/journals/YYYY-MM-DD-<slug>.md`

**When to Use**:
- After completing significant work
- When encountering novel problems
- After making architectural decisions
- For bug fixes (Reflection Report required)

### Governance & Quality

#### 7. **security-and-compliance.md**
**Purpose**: Security standards (GLOBAL POLICY - cannot be overridden)

**Mandatory Requirements**:
```markdown
✅ MUST:
- No plaintext secrets in code or configs
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize all outputs
- Follow principle of least privilege

❌ MUST NOT:
- Commit .env files
- Store credentials in code
- Bypass authentication/authorization
- Disable security features for convenience
```

**When to Use**:
- Before committing code
- When handling secrets or credentials
- Designing authentication/authorization
- Security reviews

#### 8. **sla-policy.md**
**Purpose**: Service level agreements for agent responsiveness

**SLA Tiers**:
```markdown
| Priority | Response Time | Resolution Time | Escalation |
|----------|--------------|-----------------|------------|
| P0       | 15 minutes   | 4 hours         | Immediate  |
| P1       | 2 hours      | 1 day           | 4 hours    |
| P2       | 1 day        | 1 week          | 3 days     |
| P3       | 1 week       | 1 month         | 2 weeks    |
```

**When to Use**:
- Prioritizing work items
- Setting expectations with stakeholders
- Escalating overdue items

#### 9. **validation-gates.md**
**Purpose**: Quality gates and validation requirements

**Quality Gates**:
```markdown
# Pre-commit
- Linting passes
- Unit tests pass
- Security scan (0 critical, ≤5 high)

# Pre-PR
- Fast-lane tests pass (5-10 min)
- Evidence collected per archetype
- PR template completed

# Pre-merge
- Full-suite tests pass (30-60 min)
- Archetype-specific validation
- Reviewer approval
```

**When to Use**:
- Before committing code
- Before creating PRs
- Before merging to main
- Implementing new quality gates

### Workflow & Process

#### 10. **orchestration-invariants.md**
**Purpose**: System coordination rules that ensure workflow integrity

**Invariants** (conditions that must ALWAYS be true):
```markdown
1. Every issue has exactly one assigned agent at a time
2. Workflow states only transition forward (no backward transitions except needs-rework)
3. Evidence is collected before workflow state advances
4. Handoffs include structured context (not "figure it out")
5. No work starts without clear acceptance criteria
```

**When to Use**:
- Designing multi-agent workflows
- Validating workflow transitions
- Debugging coordination issues

#### 11. **research-policy.md**
**Purpose**: Research phase standards (NEW vs OLD classification)

**Research Requirements**:
```markdown
# NEW Technology (<2 years old)
- NO research required, proceed with implementation

# OLD Technology (≥2 years old)
- MANDATORY research phase
- Web research for current best practices
- Document findings before proceeding
```

**When to Use**:
- Before starting feature development
- Evaluating technology choices
- Updating legacy systems

#### 12. **labels.md**
**Purpose**: Label standardization and taxonomy

**Label Categories**:
```markdown
# Agent Assignment
agent:<role>  (e.g., agent:pm-agent, agent:coder-agent)

# Behavioral Profile
archetype:<type>  (e.g., archetype:security-hardener)

# Overlay Requirements
lens:<name>  (e.g., lens:performance, lens:security)

# Workflow State
status:<state>  (e.g., status:pm-ready, status:review-ready)

# Priority
priority:P0, priority:P1, priority:P2, priority:P3

# Type
type:bug, type:feature, type:refactor, type:research
```

**When to Use**:
- Creating or updating issues/PRs
- Filtering work items
- Triggering automation

### Additional Global Instructions

#### 13. **command-grammar.md**
**Purpose**: Message prefixes and flags for meta-communication

**Prefixes** (single-message scope):
```markdown
OOC:        # Out of character - normal conversation
AS:<role>:  # Temporarily act as different agent
META:       # System/meta discussion
```

**Flags** (combine with prefixes):
```markdown
NOJOURNAL   # Don't write to Problems/Decisions/Learnings
NOTOOLS     # Don't execute scripts or external tools
NOCI        # Don't modify CI/CD settings
DRYRUN      # Generate plans only, no actual changes
```

**Example**: `OOC: NOJOURNAL NOTOOLS Explain this code pattern`

#### 14. **mailbox-communication.md**
**Purpose**: Async inter-agent communication using file-based mailboxes

See **wolf-scripts-agents** skill for implementation details.

#### 15. **report-template.md**
**Purpose**: Standardized output format for agent reports

#### 16. **wolf-ethos.md**
**Purpose**: Wolf's philosophical foundation and values

#### 17. **compaction-recovery.md**
**Purpose**: Recovering agent state after context compaction

---

## 🔧 Domain Instructions (3 files)

Location: `/agents/instructions/domain/`

### web.md
**Applies to**: Frontend/backend web development roles

**Key Patterns**:
```markdown
# Frontend
- React/Next.js patterns
- Component structure
- State management
- Responsive design
- Accessibility (a11y)

# Backend
- API design (REST, GraphQL)
- Authentication/authorization
- Database patterns
- Caching strategies
- Error handling
```

**When to Use**:
- Web application development
- API design and implementation
- Frontend component work

### data.md
**Applies to**: Data processing and analytics roles

**Key Patterns**:
```markdown
# Data Processing
- ETL pipelines
- Data validation
- Schema migrations
- Performance optimization

# Analytics
- Query optimization
- Aggregation patterns
- Reporting standards
```

**When to Use**:
- Database schema changes
- Data pipeline development
- Analytics implementation

### ops.md
**Applies to**: DevOps and operations roles

**Key Patterns**:
```markdown
# Infrastructure
- Docker containerization
- CI/CD pipelines
- Deployment strategies
- Monitoring and alerting

# Operations
- Incident response
- Performance tuning
- Capacity planning
- Security hardening
```

**When to Use**:
- Infrastructure changes
- CI/CD modifications
- Deployment procedures
- Operational improvements

---

## 📁 Project Instructions (3 files)

Location: `/agents/instructions/project/`

### repository-operations.md
**Purpose**: GitHub CLI patterns and repository naming conventions

**Key Patterns**:
```bash
# Issue Operations
gh issue create --title "..." --body "..." --label "..."
gh issue edit <number> --add-label "status:pm-ready"
gh issue view <number> --json title,body,labels

# PR Operations
gh pr create --title "..." --body "..." --base main
gh pr view <number> --json closingIssuesReferences,isDraft
gh pr merge <number> --squash

# Repository Operations
gh repo view --json name,description,topics
```

**When to Use**:
- Automating GitHub operations
- Workflow scripting
- Repository management

### multi-instance-coordination.md
**Purpose**: Coordinating multiple copies of the repository

**Key Patterns**:
```markdown
# Naming Convention
- Primary: WolfAgents (canonical)
- Copy 1: WolfAgents_1
- Copy 2: WolfAgents_2

# Coordination
- Use labels to indicate which copy is primary for work
- Sync changes via patches or cherry-picks
- Avoid duplicate work across copies
```

**When to Use**:
- Working across multiple repo copies
- Syncing changes between copies
- Coordinating parallel development

### production-patterns.md
**Purpose**: Production-ready code standards

**Key Patterns**:
```markdown
# Error Handling
- Try/catch for all external calls
- Graceful degradation
- User-friendly error messages

# Logging
- Structured logging
- Appropriate log levels
- No sensitive data in logs

# Performance
- Caching where appropriate
- Database query optimization
- Resource cleanup
```

**When to Use**:
- Production code development
- Code review for production readiness
- Debugging production issues

---

## Integration with Role Cards

Every role card should include this standard instruction cascade section:

```markdown
## Instruction Cascade (READ THESE FIRST)

Before starting any work, read these instruction files in order:

### Global Instructions (Required for ALL agents)
1. `agents/instructions/global/identity-heartbeat.md`
2. `agents/instructions/global/eight-phase-methodology.md`
3. `agents/instructions/global/github-coordination.md`
4. `agents/instructions/global/authority-matrix.md`
5. `agents/instructions/global/communication.md`
6. `agents/instructions/global/security-and-compliance.md`

### Domain Instructions (Select relevant)
- `agents/instructions/domain/web.md` (for web development)
- `agents/instructions/domain/data.md` (for data processing)
- `agents/instructions/domain/ops.md` (for operations)

### Project Instructions (Required for ALL agents)
1. `agents/instructions/project/repository-operations.md`
2. `agents/instructions/project/multi-instance-coordination.md`
3. `agents/instructions/project/production-patterns.md`

### Role-Specific Instructions
Continue reading this role card for role-specific guidance.
```

---

## Best Practices

### Reading Instructions
- ✅ Read ALL global instructions at session start
- ✅ Re-read after context compaction
- ✅ Apply priority order for conflicts
- ✅ Verify identity every 5 minutes
- ❌ Don't skip global instructions for "simple" tasks
- ❌ Don't assume instructions haven't changed

### Conflict Resolution
- ✅ Apply priority order (Project > Role > Domain > Global)
- ✅ Document why higher-priority instruction was applied
- ✅ Escalate if uncertain about conflict resolution
- ✅ Never override GLOBAL POLICY items (security, governance)
- ❌ Don't silently ignore conflicting instructions
- ❌ Don't skip escalation when blocked

### Maintaining Instructions
- ✅ Update global instructions for universal changes
- ✅ Update domain for technical pattern changes
- ✅ Update project for environment-specific needs
- ✅ Keep role cards for role-specific behavior
- ❌ Don't duplicate content across levels
- ❌ Don't create circular dependencies

---

## Related Skills

- **wolf-roles**: Role-specific instruction integration
- **wolf-governance**: Governance policies referenced in instructions
- **wolf-principles**: Foundational principles underlying instructions
- **wolf-scripts-agents**: Mailbox communication implementation

---

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"Global instructions override project instructions"** - BACKWARDS. Project instructions have HIGHEST priority. Project > Role > Domain > Global.
- ❌ **"I can skip instruction loading to save time"** - FORBIDDEN. Instructions contain critical policies. Skipping them violates governance and security.
- ❌ **"Instructions haven't changed since last session"** - Wrong assumption. Always re-read instructions at session start and after compaction.
- ❌ **"Global policy can be overridden for convenience"** - NO. Security, governance, and identity verification are GLOBAL POLICY and cannot be overridden. Ever.
- ❌ **"I'll just follow the instructions I remember"** - STOP. Memory is unreliable. Read current instruction files.

**STOP. Load instructions in correct cascade order BEFORE proceeding.**

## After Using This Skill

**RECOMMENDED NEXT STEPS:**

```
Instructions provide context - used during workflow execution
```

1. **Integration with wolf-session-init**: Instructions are loaded as part of session initialization
   - **When**: wolf-session-init Step 4 loads role-specific guidance, which includes instruction cascade
   - **Why**: Ensures all agents have consistent context before starting work
   - **This skill**: Provides detailed instruction hierarchy and conflict resolution rules

2. **During Work**: Reference instructions for specific situations
   - Identity verification: `identity-heartbeat.md` (every 5 minutes)
   - Workflow transitions: `github-coordination.md`
   - Security decisions: `security-and-compliance.md`
   - Inter-agent communication: `communication.md`

3. **No specific next skill**: Instructions are referenced throughout work, not a sequential step
   - Use this skill to understand instruction hierarchy
   - Use wolf-roles to see how instructions integrate with role cards
   - Use wolf-governance for governance policies referenced in instructions

### Cascade Resolution Checklist

Before claiming instructions loaded correctly:

- [ ] Read ALL 21 global instruction files (identity-heartbeat, github-coordination, authority-matrix, etc.)
- [ ] Read relevant domain instruction (web.md, data.md, or ops.md based on role)
- [ ] Read ALL 3 project instruction files (repository-operations, multi-instance-coordination, production-patterns)
- [ ] Understand priority order for conflicts (Project > Role > Domain > Global)
- [ ] Verified GLOBAL POLICY items cannot be overridden (security, governance, identity)

**Can't check all boxes? Instruction loading incomplete. Return to this skill.**

### Good/Bad Example: Instruction Priority Resolution

<Good>
**Scenario**: Indentation standard conflict

**Instructions Found**:
- Global (`global/code-standards.md`): "Use 2-space indentation for all code"
- Domain (`domain/web.md`): "React projects use 2-space indentation"
- Project (`project/production-patterns.md`): "This codebase uses 4-space indentation to match existing code"
- Role (coder-agent role-card): No specific guidance

**Agent Decision**:
✅ Uses 4-space indentation (Project instruction wins)

**Rationale Documented**:
```markdown
Conflict Resolution:
- Global: 2-space
- Domain: 2-space
- Project: 4-space ← HIGHEST PRIORITY
- Role: (none)

Decision: Use 4-space indentation per Project instruction.
Reason: Project-level instruction has highest priority in cascade.
         Consistency with existing codebase takes precedence.
```

**Why this is correct**:
- Correctly identified conflict across instruction levels
- Applied priority order (Project > Domain > Global)
- Documented decision with clear rationale
- Maintains consistency with existing codebase
</Good>

<Bad>
**Scenario**: Security override attempt

**Instructions Found**:
- Global (`global/security-and-compliance.md`): "GLOBAL POLICY: No plaintext secrets in code. Use environment variables."
- Project (`project/production-patterns.md`): "For this specific microservice, hardcode API key for convenience"

**Agent Decision**:
❌ Hardcoded API key because "Project instruction has highest priority"

**Why this is WRONG**:
- GLOBAL POLICY items CANNOT be overridden
- Security standards are non-overridable
- Project instruction violates GLOBAL POLICY and should be rejected
- Agent should escalate the conflicting instruction

**What Should Have Been Done**:
```markdown
Conflict Detected:
- Global: No plaintext secrets (GLOBAL POLICY - cannot override)
- Project: Hardcode API key (VIOLATES GLOBAL POLICY)

Decision: REJECT Project instruction. Follow Global policy.
Reason: Security standards are GLOBAL POLICY and non-overridable.
Action: Escalate to governance team - Project instruction needs correction.
```

**Correct Approach**:
1. Identify GLOBAL POLICY violation
2. Reject conflicting Project instruction
3. Follow Global security policy
4. Escalate to governance team
5. Document why Project instruction was rejected
6. Propose alternative (use environment variables)
</Bad>

---

**Total Instruction Files**:
- Global: 21 files
- Domain: 3 files
- Project: 3 files
- Role: 43 role cards
- Variants: Various stack-specific

**Priority Levels**: 4 (Project > Role/Variant > Domain > Global)
**EXCEPTION**: GLOBAL POLICY items (security, governance, identity) CANNOT be overridden

**Last Updated**: 2025-11-14
**Phase**: Superpowers Skill-Chaining Enhancement v2.0.0
**Maintainer**: Governance Team
