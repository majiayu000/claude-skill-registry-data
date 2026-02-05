---
name: wolf-workflows
description: Workflow templates for orchestrating multi-agent development processes (feature, security, bugfix)
version: 1.0.0
---

# Wolf Workflows: Multi-Agent Orchestration Templates

**Version**: 1.0.0
**Purpose**: Provide end-to-end workflow templates that orchestrate multiple agents through complete development processes

## What This Skill Provides

Wolf Workflows provides **complete orchestration templates** for common development workflows. Each template shows:

1. **Agent Chain**: Which agents work in sequence
2. **Decision Gates**: When to proceed or block
3. **Handoff Protocols**: What each agent passes to the next
4. **Quality Gates**: Testing and validation checkpoints
5. **Success Criteria**: How to know when workflow is complete

## Available Workflows

### 1. Feature Development Workflow
**Template**: `templates/feature-workflow-template.md`
**Agent Chain**: pm-agent → [research-agent] → architect-lens-agent → coder-agent → qa-agent → code-reviewer-agent → [devops-agent]

**Use When**:
- Implementing new features or enhancements
- Building user-facing functionality
- Adding system capabilities

**Duration**: Varies by feature size (hours to weeks)

**Key Phases**:
- Requirements definition (pm-agent)
- Research & feasibility (research-agent, optional)
- Architecture design (architect-lens-agent)
- Implementation (coder-agent)
- Quality assurance (qa-agent)
- Code review (code-reviewer-agent)
- Deployment (devops-agent, optional)

**Decision Gates**:
- ✅ Requirements approved → Design
- ✅ Design approved → Implementation
- ✅ Tests passing → Review
- ✅ Review approved → Merge
- ✅ Merge complete → [Optional] Deployment

---

### 2. Security Review Workflow
**Template**: `templates/security-workflow-template.md`
**Agent Chain**: pm-agent → [research-agent] → architect-lens-agent → coder-agent → qa-agent (security lens) → code-reviewer-agent

**Use When**:
- Conducting security audits
- Remediating vulnerabilities (CVEs)
- Implementing security features (auth, encryption, etc.)
- Responding to security incidents

**Duration**: Hours to days (depends on severity)

**Key Phases**:
- Threat modeling (pm-agent with STRIDE analysis)
- Security research (research-agent, optional)
- Security architecture (architect-lens-agent with defense-in-depth)
- Secure implementation (coder-agent with security lens)
- Security testing (qa-agent with OWASP Top 10 validation)
- Security review (code-reviewer-agent with security lens)

**Security Gates (MANDATORY)**:
- ✅ Threat model documented → Design
- ✅ Security scan clean (0 critical, ≤5 high) → Review
- ✅ Penetration tests passing → Merge
- ✅ Security review approved → Deployment

**Security Lens**: MANDATORY for this workflow

---

### 3. Bugfix Workflow
**Template**: `templates/bugfix-workflow-template.md`
**Agent Chain**: pm-agent (triage) → [research-agent] (root cause) → coder-agent (fix) → qa-agent (regression) → code-reviewer-agent

**Use When**:
- Investigating and fixing bugs
- Resolving production incidents
- Addressing regression issues
- Fixing test failures

**Duration**: Hours to days (depends on bug severity)

**Bug Severities**:
- **CRITICAL (P0)**: System down, data loss, security breach → Same day fix
- **HIGH (P1)**: Major feature broken → 1-3 days
- **MEDIUM (P2)**: Minor feature broken, workaround exists → 1-2 weeks
- **LOW (P3)**: Cosmetic issue → Next sprint

**Key Phases**:
- Bug triage & reproduction (pm-agent)
- Root cause analysis (research-agent or coder-agent)
- Fix implementation (coder-agent with RED-GREEN-REFACTOR)
- Regression testing (qa-agent)
- Code review (code-reviewer-agent)

**Bug Resolution Gates**:
- ✅ Bug reproduced → Root cause analysis
- ✅ Root cause identified → Fix implementation
- ✅ Fix validated → Regression testing
- ✅ Regression tests added → Code review
- ✅ No new bugs introduced → Merge

---

## How to Use Workflow Templates

### Step 1: Select Workflow Type

**Decision Tree**:
```
Are you building a new feature?
  YES → Use Feature Development Workflow
  NO ↓

Are you addressing a security concern?
  YES → Use Security Review Workflow
  NO ↓

Are you fixing a bug?
  YES → Use Bugfix Workflow
  NO → Consult with pm-agent for custom workflow
```

### Step 2: Read Complete Workflow Template

**Don't skim.** Read the entire workflow template from start to finish to understand:
- All phases and agents involved
- Decision gates and quality gates
- Handoff protocols between agents
- Success criteria for completion

### Step 3: Identify Your Current Phase

Determine where you are in the workflow:
- Starting from scratch → Phase 1
- Requirements defined → Phase 2 or 3
- Implementation in progress → Phase 4
- Testing → Phase 5
- Review → Phase 6

### Step 4: Load Required Skills (PRIMARY CHAIN)

**MANDATORY**: Load the primary skill chain before starting workflow:

```
1. wolf-principles (REQUIRED)
2. wolf-archetypes (REQUIRED)
3. wolf-governance (REQUIRED)
4. wolf-roles (REQUIRED)
```

### Step 5: Follow Workflow Sequentially

**Don't skip phases.** Each phase builds on the previous:
- Phase 1 defines what to build
- Phase 2 researches how to build it (optional)
- Phase 3 designs the architecture
- Phase 4 implements the design
- Phase 5 validates the implementation
- Phase 6 reviews for quality and merge

**Skipping phases = rework.** The workflow exists to prevent costly mistakes.

### Step 6: Pass Through Decision Gates

At each decision gate, validate completion before proceeding:
- ✅ **PASS** → Proceed to next phase
- ❌ **FAIL** → Return to current or previous phase for fixes

**Never skip decision gates.**

### Step 7: Hand Off Between Agents

When transitioning between agents, provide **complete handoff package**:
- Artifacts from previous phase
- Context and background
- Requirements or acceptance criteria
- Specific areas to focus

Use handoff templates from workflow for consistency.

---

## Workflow Customization

### When to Modify Workflows

**Allowed Modifications**:
- ✅ Skip optional phases (e.g., research-agent if not needed)
- ✅ Adjust timelines based on scope
- ✅ Add additional lenses (performance, accessibility, etc.)
- ✅ Add custom validation steps

**FORBIDDEN Modifications**:
- ❌ Skip mandatory phases (requirements, design, testing, review)
- ❌ Remove decision gates
- ❌ Skip quality gates
- ❌ Remove handoff protocols

### Scaling Workflows

**For Small Tasks** (hours):
- Collapse research phase → coder-agent does quick investigation
- Lightweight design → architect-lens-agent provides guidance in ADR
- Fast-Lane testing only → qa-agent runs subset of tests

**For Large Tasks** (weeks):
- Break into smaller workflows → multiple feature workflows in parallel
- Add milestones → weekly progress checkpoints
- Add design reviews → architect-lens-agent review sessions

**For Critical Tasks** (production incidents):
- Expedite decision gates → faster approval cycles
- Parallel work → multiple agents work simultaneously where safe
- Continuous monitoring → devops-agent monitors during implementation

---

## Integration with Wolf Framework

### Principles Applied

All workflows enforce Wolf's core principles:

1. **Artifact-First Development** → ADRs, requirements docs, test reports
2. **Test-First Development** → Tests before implementation
3. **Research-Before-Code** → Investigation before building
4. **Advisory-First Enforcement** → Warnings before blocks
5. **Evidence-Based Decision Making** → Data drives decisions
6. **Guardrails Through Automation** → Automated quality gates
7. **Portability-First Thinking** → Multi-environment design
8. **Defense-in-Depth** → Multiple security layers
9. **Incremental Value Delivery** → Small, frequent deliveries
10. **Self-Documenting Systems** → Clear, discoverable documentation

### Archetypes Applied

Workflows automatically select appropriate archetypes:

- **Feature Development** → Determined by wolf-archetypes (could be rapid-prototyper, security-guardian, etc.)
- **Security Review** → Always security-guardian
- **Bugfix** → Always bug-hunter

### Governance Applied

All workflows enforce governance requirements:

- **Quality Gates**: Fast-Lane (60% coverage) + Full-Suite (90% E2E success)
- **ADR Requirements**: Architecture decisions documented
- **Rollback Plans**: Deployments have rollback procedures
- **Security Scans**: 0 critical, ≤5 high vulnerabilities

---

## Workflow Orchestration Patterns

### Pattern 1: Sequential Agent Chain (Most Common)

```
Agent 1 → Agent 2 → Agent 3 → Agent 4
```

Each agent completes their phase before next agent starts.

**Example**: Feature workflow (pm → architect → coder → qa → reviewer)

**When to Use**: Most workflows, especially when each phase depends on previous

---

### Pattern 2: Parallel Agent Work (Advanced)

```
Agent 1 → Agent 2A (parallel with) Agent 2B → Agent 3
```

Multiple agents work simultaneously on independent tasks.

**Example**: Multiple coders implementing independent components

**When to Use**: Large features with independent components

**Caution**: Only parallelize truly independent work. Dependencies = rework.

---

### Pattern 3: Iterative Agent Loop (Bug Resolution)

```
Agent 1 → Agent 2 → Agent 3 ↩ (back to Agent 2 if failed)
```

Agent work iterates until quality gate passes.

**Example**: Bugfix workflow (coder → qa → reviewer, loop back to coder if tests fail)

**When to Use**: Bug fixes, security remediation, any work with validation loops

---

### Pattern 4: Optional Agent Branches (Conditional)

```
Agent 1 → [Agent 2 optional] → Agent 3
```

Some agents only participate if needed.

**Example**: Feature workflow with optional research-agent

**When to Use**: Complex features that may need research, features that may need deployment

---

## After Using This Skill

### REQUIRED NEXT SKILL: wolf-roles

After selecting a workflow, you MUST use `wolf-roles` to:
1. Understand each agent's role in the workflow
2. Load role-specific templates for your current agent
3. Understand responsibilities and non-goals

**How to Use**:
```bash
Use wolf-roles skill → Select your agent role → Load agent template
```

### RECOMMENDED: wolf-governance

Use `wolf-governance` to understand:
- Quality gates specific to your workflow
- ADR requirements
- Testing requirements
- Security requirements

---

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"Skip the workflow, just start coding"** - STOP. Workflows prevent rework. Follow the process.
- ❌ **"Requirements can be defined during implementation"** - BACKWARDS. Requirements BEFORE design. Design BEFORE code.
- ❌ **"This bug is simple, skip root cause analysis"** - DANGEROUS. Symptoms ≠ root cause. Find the real problem.
- ❌ **"Design phase is too slow, design while coding"** - Wrong. Design upfront is faster than refactoring later.
- ❌ **"Testing can happen after merge"** - FORBIDDEN. Tests BEFORE merge. Always.
- ❌ **"Security workflow is overkill for this"** - NO. Security is never overkill. Use the workflow.
- ❌ **"Skip decision gates to move faster"** - DANGEROUS. Gates catch mistakes. Skipping gates = expensive mistakes.
- ❌ **"One agent can do multiple phases"** - NO. Role separation prevents scope creep and ensures quality.

**STOP. Follow the workflow. Trust the process. It exists because skipping phases causes expensive rework.**

---

## Verification Checklist

After using a workflow, verify completion:

- [ ] All mandatory phases completed (no skipped phases)
- [ ] All decision gates passed (no bypassed gates)
- [ ] All quality gates passed (Fast-Lane + Full-Suite)
- [ ] Handoff protocols followed (complete handoff packages between agents)
- [ ] Artifacts created (ADRs, test reports, documentation)
- [ ] Success criteria met (workflow-specific criteria satisfied)
- [ ] No rework required (work doesn't need to be redone)

If ANY item is unchecked → Workflow not complete. Return to incomplete phase.

---

## Good/Bad Examples

### Good Example: Following Feature Workflow

<Good>
**Scenario**: Team wants to add user authentication

**Agent Actions**:
1. pm-agent defines requirements, acceptance criteria, applies security lens
2. architect-lens-agent designs authentication architecture, creates ADR, includes defense-in-depth
3. coder-agent writes tests first, implements auth following ADR, applies security lens
4. qa-agent runs security tests (OWASP Top 10), validates acceptance criteria
5. code-reviewer-agent reviews security controls, approves
6. Feature merged with comprehensive auth system

**Why GOOD**:
- Followed workflow sequentially
- All phases completed
- Security lens applied throughout
- Quality gates passed
- Artifacts created (ADR, tests, security scan results)
</Good>

---

### Bad Example: Skipping Workflow Phases

<Bad>
**Scenario**: Team wants to add user authentication (same as above)

**Agent Actions**:
1. coder-agent starts implementing auth without requirements or design
2. Realizes midway that approach is wrong (should use OAuth, not custom auth)
3. Refactors implementation (2 days wasted)
4. Discovers security vulnerabilities during review
5. Refactors again to fix security issues (another 2 days wasted)
6. Total time: 5 days (should have been 2 days with workflow)

**Why BAD**:
- Skipped requirements definition (pm-agent)
- Skipped architecture design (architect-lens-agent)
- Skipped security lens
- Coded before designing
- Result: 3 days of rework that workflow would have prevented
</Bad>

---

### Good Example: Following Bugfix Workflow with Root Cause Analysis

<Good>
**Scenario**: Production bug - users can't log in

**Agent Actions**:
1. pm-agent triages: CRITICAL (P0), reproduces bug consistently
2. research-agent does root cause analysis: database connection pool exhausted
3. coder-agent writes regression test (simulates high load), implements connection pool management fix
4. qa-agent verifies bug fixed, regression test passes, no new bugs introduced
5. code-reviewer-agent reviews, approves, checks for similar bugs elsewhere
6. Bug fixed in 4 hours, will not recur

**Why GOOD**:
- Reproduced bug before fixing
- Found root cause (not just symptom)
- Added regression test
- Verified no new bugs
- Checked for similar issues
</Good>

---

### Bad Example: Symptom Patching Without Root Cause

<Bad>
**Scenario**: Production bug - users can't log in (same as above)

**Agent Actions**:
1. coder-agent sees error message "connection timeout", increases timeout value
2. Deploys to production
3. Bug returns next week (connection pool still exhausting, just takes longer now)
4. Realizes initial fix was wrong, does proper investigation
5. Finds real root cause: connection pool exhaustion
6. Implements proper fix
7. Total time: 2 weeks + 2 production incidents

**Why BAD**:
- Skipped bug reproduction (pm-agent)
- Skipped root cause analysis (research-agent)
- Patched symptom instead of fixing cause
- No regression test added
- Bug recurred because root cause not addressed
- Result: 2 weeks of incident response that workflow would have prevented
</Bad>

---

## Summary

**Wolf Workflows** provides end-to-end orchestration templates for:
1. **Feature Development** - Build new functionality systematically
2. **Security Review** - Address security concerns with defense-in-depth
3. **Bugfix** - Resolve bugs systematically with root cause analysis

**Always**:
- Select appropriate workflow for your task
- Follow workflow sequentially (don't skip phases)
- Pass through all decision gates
- Create all required artifacts
- Use handoff protocols between agents

**Never**:
- Skip phases to "move faster" (causes rework)
- Bypass decision gates (catches mistakes)
- Remove quality gates (ensures quality)
- Work without workflow (workflow prevents expensive mistakes)

**Workflows exist to prevent rework. Trust the process.**

---

## Version History

- **v1.0.0** (2025-11-14): Initial release with 3 workflow templates (feature, security, bugfix) following Phase 3 skill-chaining patterns
