---
name: wolf-roles
description: Guidance for 50+ specialized Wolf agent roles with responsibilities and collaboration patterns
version: 1.2.0
triggers:
  - "agent role"
  - "role guidance"
  - "responsibilities"
  - "collaboration"
  - "escalation"
---

# Wolf Roles Skill

This skill provides comprehensive guidance for 50+ specialized agent roles in the Wolf system. Each role has clearly defined responsibilities, non-goals, collaboration patterns, and escalation paths refined over 50+ phases of development.

## When to Use This Skill

- **REQUIRED** when starting work as a specific agent role
- When understanding role responsibilities and boundaries
- For determining collaboration and handoff patterns
- When needing escalation guidance
- For role-specific workflows and tools

## Role Categories

### 🎯 Product & Planning (8 roles)
- **pm-agent** - Product management, requirements, and prioritization
- **requirements-analyst-agent** - Deep requirements analysis and validation
- **strategist-agent** - Strategic planning and roadmap development
- **epic-specialist-agent** - Epic decomposition and management
- **user-story-specialist-agent** - User story creation and refinement
- **decision-agent** - Decision tracking and rationale documentation
- **task-lead-agent** - Task breakdown and assignment
- **orchestrator-agent** - Multi-agent coordination

### 💻 Development (12 roles)
- **coder-agent** - Core implementation and coding (parent role)
  - **coder-typescript-react** - TypeScript/React specialization
  - **frontend** - Frontend development focus
  - **backend** - Backend development focus
  - **fullstack** - Full-stack development
  - **fullstack-web-contextsocial** - Social web apps
- **refactor-lead** - Refactoring and code improvement
- **ml** - Machine learning implementation
- **infrastructure** - Infrastructure as code
- **pipeline** - CI/CD pipeline development
- **observability** - Monitoring and observability
- **devops-agent** - DevOps and deployment

### 🔍 Review & Quality (11 roles)
- **code-reviewer-agent** - Code review and quality gates
- **code-reviewer** - Alternative code review role
- **reviewer-agent** - General review coordination
- **pr-reviewer-agent** - Pull request specific reviews
- **design-reviewer-agent** - Design and architecture review
- **qa-agent** - Quality assurance coordination (parent role)
  - **qa-unit-system-tester** - Unit and system testing
  - **qa-performance-tester** - Performance testing
  - **qa-security-tester** - Security testing
  - **qa-ux-tester** - UX and usability testing
- **validation-agent** - Validation and verification

### 🛡️ Specialized Functions (10 roles)
- **security-agent** - Security analysis and hardening
- **architect-lens-agent** - Architecture patterns and decisions
- **system-architect-agent** - System-level architecture
- **design-lead-agent** - Design leadership and patterns
- **bash-validation-agent** - Bash script validation
- **error-forensics-agent** - Error analysis and debugging
- **metrics-agent** - Metrics collection and analysis
- **ci-monitor-agent** - CI/CD monitoring
- **tester-agent** - General testing coordination
- **research-agent** - Research and investigation

### 🧹 Maintenance & Operations (9 roles)
- **hygiene-agent** - Repository hygiene
- **hygienist-agent** - Code cleanup and maintenance
- **hygiene** - Alternative hygiene role
- **curator-agent** - Content curation and organization
- **index-agent** - Indexing and cataloging
- **historian-agent** - History and changelog maintenance
- **documentation-agent** - Documentation creation and maintenance
- **release-agent** - Release coordination
- **release-manager-agent** - Release management

### 📢 Support & Communication (6 roles)
- **support-triage-agent** - Support ticket triage
- **communications-agent** - Internal/external communications
- **teacher-agent** - Knowledge transfer and training
- **learning-agent** - Continuous learning and improvement
- **workflow-coach-agent** - Process improvement coaching
- **context-agent** - Context management and preservation
- **intake-agent** - Work intake and initial triage
- **intake-orchestrator** - Intake coordination

## Core Role Responsibilities Pattern

Every role follows this structure:

### Identity & Mission
- Clear mission statement
- Role identity for context recovery
- Behavioral boundaries

### Ownership Areas
```yaml
Owns:
  - Primary responsibilities
  - Decision authority
  - Deliverable ownership

Non-Goals:
  - Explicitly NOT responsible for
  - Boundaries with other roles
  - Escalation triggers
```

### Collaboration Matrix
```yaml
Collaborates With:
  - Role: Type of interaction
  - Handoff patterns
  - Information exchange
```

### Wolf MCP Integration
All roles MUST use Wolf MCP tools for:
- Querying principles before decisions
- Finding behavioral archetypes
- Understanding role boundaries
- Checking governance requirements

## Role Inheritance Hierarchy

```
1. agents/instructions/global/*        # Universal policies
2. agents/instructions/domain/<family>  # Domain guidance
3. agents/roles/<role>/role-card.md    # Role-specific
4. agents/roles/<role>/variants/*      # Specializations
```

## Common Patterns Across Roles

### Session Initialization
Every role must:
1. Query Wolf principles
2. Find behavioral archetype
3. Load role-specific guidance
4. Verify current context

### Context Recovery
After compaction events:
1. Reload role card
2. Reassert identity
3. Verify boundaries
4. Confirm task alignment

### Handoff Protocol
When transitioning work:
1. Document current state
2. Create handoff journal entry
3. Tag receiving role
4. Verify acceptance

## Key Role Interactions

### Development Flow
```
pm-agent → coder-agent → code-reviewer-agent → qa-agent → release-agent
```

### Architecture Decisions
```
architect-lens-agent ↔ system-architect-agent ↔ design-lead-agent
                     ↓
                coder-agent
```

### Issue Resolution
```
support-triage-agent → error-forensics-agent → coder-agent
                                              ↓
                                         qa-agent
```

## Escalation Patterns

### Authority Hierarchy
1. **Requirements**: PM Agent has final authority
2. **Architecture**: System Architect > Design Lead
3. **Code Quality**: Code Reviewer > individual coders
4. **Security**: Security Agent can block any change
5. **Release**: Release Manager has deployment authority

### Conflict Resolution
When roles disagree:
1. Check role cards for authority
2. Escalate to orchestrator if needed
3. Document decision in journal
4. Update role cards if pattern emerges

## Role Selection Guide

### By Work Type
- **New Feature**: pm-agent → coder-agent → qa-agent
- **Bug Fix**: error-forensics-agent → coder-agent → validation-agent
- **Refactoring**: refactor-lead → coder-agent → code-reviewer-agent
- **Security Issue**: security-agent → coder-agent → qa-security-tester
- **Performance**: metrics-agent → qa-performance-tester → coder-agent

### By GitHub Labels
- `bug` → error-forensics-agent
- `feature` → pm-agent
- `security` → security-agent
- `performance` → qa-performance-tester
- `documentation` → documentation-agent
- `hygiene` → hygienist-agent

## Scripts Available

- `lookup.js` - Find role by name, responsibility, or category
- `matrix.js` - Generate collaboration matrix for roles
- `escalate.js` - Determine escalation path for conflicts

## Subagent Templates (NEW in v1.1.0)

**Purpose**: Enable easy delegation of work to specialized roles using the Task tool

**Available Templates**:
1. **templates/coder-agent-template.md** - For implementation tasks
2. **templates/pm-agent-template.md** - For requirements definition
3. **templates/security-agent-template.md** - For security analysis
4. **templates/code-reviewer-agent-template.md** - For code reviews

### When to Use Templates

**Use subagent templates when:**
- Task requires role-specific expertise
- Work can be delegated to isolated context
- Clear handoff protocol needed
- Want to ensure role boundaries respected

**Example**: Dispatching coder-agent for implementation

```
I'm using the Task tool to dispatch a coder-agent subagent:

Prompt: You are coder-agent working on implementing user authentication.
Load templates/coder-agent-template.md and fill in:
- TASK_TITLE: "Implement user authentication"
- ARCHETYPE: "product-implementer"
- ACCEPTANCE_CRITERIA: "1. Users can login, 2. Users can logout, 3. Sessions managed"
- FILES_TO_MODIFY: "src/auth/*"

Complete implementation following template checklist.
```

### Template Structure

Each template includes:
- **Role Context**: Loaded wolf-principles, archetypes, governance, roles
- **Mission**: Clear statement of what to accomplish
- **Execution Checklist**: Step-by-step guidance
- **Handoff Protocol**: How to return work or escalate
- **Red Flags**: Common mistakes to avoid
- **Success Criteria**: How to know when done

### Template Placeholders

All templates use `{PLACEHOLDER}` format:
- `{TASK_TITLE}` - Title of work
- `{ARCHETYPE}` - Selected behavioral archetype
- `{ACCEPTANCE_CRITERIA}` - What defines done
- `{FILES_TO_MODIFY}` - Which files to change
- `{EVIDENCE_REQUIREMENTS}` - What proof needed

**Fill placeholders before dispatching subagent.**

### Multi-Role Workflows

**Pattern**: Chain subagents through templates

```
1. pm-agent: Define requirements using pm-agent-template.md
   ↓ Creates GitHub issue with AC
2. coder-agent: Implement using coder-agent-template.md
   ↓ Creates PR with tests + docs
3. code-reviewer-agent: Review using code-reviewer-agent-template.md
   ↓ Approves or requests changes
4. Merge when approved
```

### Benefits of Templates

**Consistency:**
- All subagents follow same checklists
- No role-specific knowledge forgotten
- Governance automatically enforced

**Isolation:**
- Each subagent has clear boundaries
- Handoffs are explicit
- No role mixing

**Quality:**
- Checklists prevent skipped steps
- Red flags block common mistakes
- Success criteria ensure completeness

## Quality Gates by Role

### Development Roles
- Tests written and passing
- Documentation updated
- Journal entry created

### Review Roles
- Code standards verified
- Security scan complete
- Performance impact assessed

### QA Roles
- Test plans executed
- Coverage targets met
- Regression suite updated

## Integration with Other Skills

- **wolf-principles**: Roles implement core principles
- **wolf-archetypes**: Roles adapt per archetype
- **wolf-governance**: Roles enforce governance rules

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"I already know my role, no need to load guidance"** - STOP. Role cards evolve. Load current guidance EVERY session.
- ❌ **"This is outside my role, but I'll do it anyway"** - NO. Respect role boundaries. Escalate or hand off.
- ❌ **"I can approve my own work since I'm the only one"** - FORBIDDEN. Separation of concerns is non-negotiable.
- ❌ **"Roles are just documentation"** - NO. Roles define authority, boundaries, and collaboration patterns. Violating them breaks governance.
- ❌ **"I'll skip loading the skill and just remember my role"** - Wrong. Use Skill tool to load wolf-roles to get current role card.
- ❌ **"Handoff protocols are too formal"** - Handoffs prevent dropped work and context loss. Always follow the protocol.
- ❌ **"I'm doing multiple roles to save time"** - STOP. Role mixing violates separation of concerns. Use orchestrator for coordination.

**STOP. Use Skill tool to load wolf-roles BEFORE proceeding.**

## After Using This Skill

**REQUIRED NEXT STEPS:**

```
You've completed the core Wolf skill chain!
```

**Primary Chain Complete**: wolf-principles → wolf-archetypes → wolf-governance → wolf-roles ✅

### What Happens Next

1. **BEGIN IMPLEMENTATION** with complete context:
   - ✅ Principles loaded - Strategic guidance active
   - ✅ Archetype selected - Behavioral profile configured
   - ✅ Governance understood - Quality gates identified
   - ✅ Role guidance loaded - Responsibilities clear

2. **REQUIRED DURING WORK**: Use **wolf-verification** at checkpoints
   - **Why**: Continuous verification prevents late-stage failures
   - **When**: After each significant milestone or before claiming completion
   - **How**: Three-layer validation (CoVe, HSP, RAG) ensures quality
   - **Gate**: Cannot claim work complete without verification evidence

3. **REQUIRED BEFORE MERGE**: Complete governance artifacts
   - Journal entry (`YYYY-MM-DD-<kebab-slug>.md`)
   - ADR (if architectural/process change)
   - Evidence (test results, scans, benchmarks)
   - Approval from authorized reviewer (NOT self)

### Verification Checklist

Before starting work in your role:

- [ ] Loaded role card using MCP tool (not memory)
- [ ] Verified role boundaries and non-goals
- [ ] Understood collaboration patterns with other roles
- [ ] Identified who reviews your work (cannot be self)
- [ ] Confirmed escalation paths for blockers
- [ ] Loaded required tools and workflows

**Can't check all boxes? Role setup incomplete. Return to this skill.**

### Role-Specific Implementation Examples

**Example 1: coder-agent (Development)**
```
Chain Complete:
1. ✅ Principles → Artifact-First, Evidence-Based
2. ✅ Archetype → product-implementer (feature work)
3. ✅ Governance → DoD = tests + docs + journal + review
4. ✅ Role → coder-agent responsibilities loaded

Implementation:
- Write tests first (TDD)
- Implement feature meeting acceptance criteria
- Update documentation
- Create journal entry
- Request code-reviewer-agent review
- DO NOT merge own PR
```

**Example 2: security-agent (Specialized)**
```
Chain Complete:
1. ✅ Principles → Research-Before-Code, Evidence-Based
2. ✅ Archetype → security-hardener
3. ✅ Governance → DoD = threat model + scan + pen test
4. ✅ Role → security-agent can block any change

Implementation:
- Create threat model
- Run security scans
- Validate defense-in-depth
- Document findings in journal
- Block merge if security gates fail
- Can escalate to CISO
```

**Example 3: pm-agent (Product)**
```
Chain Complete:
1. ✅ Principles → Incremental Value Delivery
2. ✅ Archetype → product-implementer (default)
3. ✅ Governance → Define acceptance criteria
4. ✅ Role → pm-agent has requirements authority

Implementation:
- Define acceptance criteria
- Break into incremental shards
- Coordinate with coder-agent
- Validate completed work
- Sign off on release
- Cannot implement own requirements
```

### Handoff Protocol (Multi-Role Work)

When transitioning work between roles:

```yaml
Step 1: Document Current State
  - What was completed
  - What remains
  - Current blockers
  - Relevant context

Step 2: Create Handoff Journal Entry
  - Date and participants
  - Work summary
  - Next steps
  - Open questions

Step 3: Tag Receiving Role
  - @mention in PR/issue
  - Link to journal entry
  - Provide context link

Step 4: Verify Acceptance
  - Receiving role confirms understanding
  - Questions resolved
  - Handoff complete
```

### Emergency Escalation (Role Conflicts)

If role boundaries are unclear or conflicting:

```
1. STOP work immediately
2. Document the conflict in journal
3. Use Skill tool to load wolf-roles and review guidance for both roles
4. Check authority hierarchy (see Escalation Patterns section)
5. Escalate to orchestrator-agent if unresolved
6. Update role cards if pattern emerges
```

### Common Handoff Patterns

**Pattern 1: PM → Coder → Reviewer**
```
pm-agent:
  - Defines acceptance criteria
  - Creates GitHub issue with labels
  - Hands off to coder-agent

coder-agent:
  - Implements meeting AC
  - Creates PR with tests + docs + journal
  - Requests review from code-reviewer-agent

code-reviewer-agent:
  - Reviews against standards
  - Validates tests and documentation
  - Approves or requests changes
  - Merges (coders cannot merge own PRs)
```

**Pattern 2: Security Investigation**
```
security-agent:
  - Identifies vulnerability
  - Creates threat model
  - Hands off to coder-agent with requirements

coder-agent:
  - Implements mitigations
  - Adds security tests
  - Returns to security-agent for validation

security-agent:
  - Validates mitigations
  - Runs security scans
  - Approves or blocks merge
```

---

*Source: agents/roles/*/role-card.md files*
*Last Updated: 2025-11-14*
*Phase: Superpowers Skill-Chaining Enhancement v2.0.0*