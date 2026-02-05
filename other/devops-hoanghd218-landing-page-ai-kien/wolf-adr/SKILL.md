---
name: wolf-adr
description: Architecture Decision Records index with searchable topics and phase-based organization (120+ ADRs from 50+ phases)
version: 1.1.0
category: architecture
triggers:
  - architecture decision
  - ADR
  - design decision
  - technical decision
  - system design
dependencies:
  - wolf-principles
size: large
---

# Wolf Architecture Decision Records (ADRs)

Searchable index of 120+ Architecture Decision Records documenting Wolf's evolution through 50+ phases of development.

## Overview

Wolf's ADRs capture critical architectural decisions, including:
- **Context**: Why the decision was needed
- **Decision**: What was chosen and why
- **Consequences**: Impact and tradeoffs
- **Status**: Proposed, Accepted, Superseded, Deprecated
- **Related ADRs**: Decision dependencies

## How to Use This Skill

### Finding Relevant ADRs

1. **By Topic**: Use topic clusters below to find related decisions
2. **By Phase**: Check phase-based organization for historical context
3. **By Keywords**: Search for specific technologies or patterns
4. **Current Architecture**: See "Living Snapshot" section

### ADR Locations

All ADRs in `/docs/adr/`:
- **Current/Active**: `docs/adr/ADR-XXX-*.md` and `docs/adr/phase-*/shard-*/ADR-*.md`
- **Archived**: `docs/adr/archive/ADR-*.md`
- **Living Snapshot**: `docs/adr/phase-50/shard-50-5/current-architecture-2025-10-07.md`

---

## Topic Clusters

### 🏗️ MCP Server Architecture

**Key Decisions:**
- **ADR-017**: MCP Server Conversion Strategy (identified 15-20 packages)
- **ADR-018**: MCP Server Architecture (implementation of 3 operational servers)
- **ADR-023**: **Knowledge-First Pivot** ⭐ (critical shift from operational to knowledge-serving)
  - **Problem**: Built operational tools that duplicated agent capabilities
  - **Solution**: MCP servers should expose Wolf's accumulated knowledge
  - **Impact**: 9 of 15 tools identified as redundant; pivot to knowledge access
- **ADR-025**: Hybrid MCP Consolidation Strategy
  - **Decision**: Keep operational MCPs for Wolf-specific logic, sunset duplicates
  - **Result**: wolf-knowledge-mcp (primary), wolf-governance-mcp, wolf-evals-mcp

**When to Reference:**
- Designing new MCP servers
- Deciding operational vs. knowledge tools
- Understanding Wolf's MCP evolution

**Files**:
- `/docs/adr/archive/ADR-017-mcp-server-conversion-strategy.md`
- `/docs/adr/archive/ADR-023-mcp-server-knowledge-first-pivot.md`
- `/docs/adr/archive/ADR-025-hybrid-mcp-consolidation.md`

---

### 🔍 Verification & Quality Assurance

**Key Decisions:**
- **ADR-043**: **Verification Architecture** ⭐ (CoVe, HSP, RAG)
  - **CoVe**: Chain of Verification for systematic fact-checking
  - **HSP**: Hierarchical Safety Prompts for multi-level validation
  - **RAG**: Grounding evidence retrieval
  - **Integration**: 3-layer verification pipeline
- **ADR-0051**: Retrieval-CoVe Hybrid (combining retrieval with verification)
- **ADR-0061**: Hallucination Drift Watchdog (detecting and preventing hallucinations)
- **ADR-0050**: Policy Intelligence Engine Accuracy Enhancement

**When to Reference:**
- Implementing self-verification
- Building quality gates
- Hallucination detection
- Evidence-based validation

**Files**:
- `/docs/adr/phase-43/shard-00/ADR-0043-verification-architecture.md` (if exists)
- `/docs/adr/archive/ADR-0051-retrieval-cove-hybrid.md`
- `/docs/adr/archive/ADR-0061-hallucination-drift-watchdog.md`

---

### 🐳 Sandbox & Containerization

**Key Decisions:**
- **ADR-0063**: Sandbox Containerization Strategy
  - **Problem**: Need isolated code execution environment
  - **Solution**: Docker-based sandbox with security constraints
- **ADR-0064**: Sandbox Quota Enforcement Architecture
  - **Resource Limits**: CPU, memory, disk I/O quotas
  - **Enforcement**: Pre-execution checks and runtime monitoring
- **ADR-0065**: Sandbox Security Architecture
  - **Security Layers**: Network isolation, filesystem restrictions, capability dropping

**When to Reference:**
- Implementing code execution environments
- Setting resource limits
- Security hardening for sandboxes

**Files**:
- `/docs/adr/archive/ADR-0063-sandbox-containerization-strategy.md`
- `/docs/adr/archive/ADR-0064-sandbox-quota-enforcement-architecture.md`
- `/docs/adr/archive/ADR-0065-sandbox-security-architecture.md`

---

###⚙️ CI/CD & GitHub Actions

**Key Decisions:**
- **ADR-072**: **GitHub Actions Workflow Standards** ⭐ (mandatory patterns)
  - **Problem**: 37% failure rate due to missing checkout steps, 100% failure with wrong API fields
  - **Solution**: Mandatory checkout step, correct API field names, permissions declaration
  - **Impact**: Prevents infrastructure failures across all workflows
- **ADR-071**: CI Workflow Optimization Strategy (workflow consolidation, cost management)
- **ADR-056**: Composite Actions Standard
  - **Reusable Workflows**: Extract common patterns into composite actions
  - **Benefits**: DRY, consistency, maintainability
- **ADR-048-5**: Actions Audit (audit trail for GitHub Actions)
- **ADR-070**: Agent Build Pipeline (agent-specific CI/CD)

**When to Reference:**
- Creating new GitHub workflows
- Fixing workflow failures
- Implementing composite actions
- Workflow optimization

**Files**:
- `/docs/adr/ADR-072-github-actions-workflow-standards.md`
- `/docs/adr/archive/ADR-056-composite-actions.md` (if exists)
- `/docs/adr/archive/ADR-070-agent-build-pipeline.md`

---

### 📦 Packaging & Dependencies

**Key Decisions:**
- **ADR-016**: Dependency Optimization Strategy
  - **Approach**: Fork and optimize 279 npm packages
  - **Result**: 83.3% of dependencies optimized via `jdmiranda/*` repos
  - **Branches**: All forks use `perf/*` branches
- **ADR-055**: Packaging Standard
  - **Conventions**: Package naming, versioning, distribution
  - **Quality Gates**: Build, test, publish standards

**When to Reference:**
- Adding new dependencies
- Optimizing existing packages
- Package publishing decisions

**Files**:
- `/docs/adr/archive/ADR-016-dependency-optimization-strategy.md`
- `/docs/adr/archive/ADR-055-packaging-standard.md`

---

### 📊 Metrics, Monitoring & Evals

**Key Decisions:**
- **ADR-0048-2**: Metrics Framework
  - **Categories**: Agent efficiency, workflow latency, quality scores
  - **Collection**: Privacy-preserving metrics with PII redaction
- **ADR-0061**: Baseline-Target Tracking (performance baseline establishment)
- **wolf-evals-mcp**: Agent efficiency metrics (latency, efficiency, token tracking)

**When to Reference:**
- Implementing telemetry
- Performance monitoring
- Establishing baselines
- Efficiency tracking

**Files**:
- `/docs/adr/archive/ADR-0048-2-metrics.md`
- `/docs/adr/archive/ADR-0061-baseline-target-tracking.md`

---

### 🛡️ Security & Compliance

**Key Decisions:**
- **ADR-0065**: Sandbox Security Architecture (isolation, restrictions, capability dropping)
- **Security Hardener Archetype**: Threat reduction priority, defense-in-depth
- **Governance Framework**: Mandatory security validation for security-labeled work

**When to Reference:**
- Security architecture decisions
- Threat modeling
- Compliance requirements
- Secure code execution

---

### 🎭 Agent Roles & Behavioral Archetypes

**Key Decisions:**
- **ADR-0049**: Role Card Integrity
  - **Problem**: Role card drift and inconsistency
  - **Solution**: Validation framework, schema enforcement
- **Archetype System**: 11 behavioral profiles (ADR embedded in archetype registry)
  - product-implementer, security-hardener, perf-optimizer, reliability-fixer, etc.
- **Lens System**: 4 overlay lenses (performance, security, accessibility, observability)

**When to Reference:**
- Defining new agent roles
- Modifying existing archetypes
- Understanding agent behavioral adaptation

**Files**:
- `/docs/adr/archive/ADR-0049-role-card-integrity.md`
- `/agents/archetypes/registry.yml` (contains embedded archetype decisions)
- `/agents/lenses/registry.yml` (contains lens application rules)

---

### 📝 Governance & Process

**Key Decisions:**
- **ADR-0048-7**: Conditional Approvals (automated approval workflows)
- **ADR-0048-10**: Research Hygiene (research phase standards)
- **ADR-047-C**: Output Summary Validation (standardized output format)
- **Emergency Governance Activation**: Override mechanisms for critical issues

**When to Reference:**
- Governance policy decisions
- Approval workflow design
- Process standardization

**Files**:
- `/docs/adr/archive/ADR-0048-7-conditional-approvals.md`
- `/docs/adr/archive/ADR-0048-10-research-hygiene.md`
- `/docs/adr/archive/ADR-047-C-output-summary-validation.md`

---

### 🧪 Research & Experimentation

**Key Decisions:**
- **ADR-0053**: Research Agent Workflow
  - **Process**: Hypothesis → Experiment → Validation → Documentation
  - **Time-boxing**: Fixed duration for research spikes
- **Research-Prototyper Archetype**: Hypothesis testing, feasibility analysis

**When to Reference:**
- Planning research spikes
- Experimentation workflows
- Proof-of-concept development

**Files**:
- `/docs/adr/archive/ADR-0053-research-agent-workflow.md`

---

### 🔧 Tooling & Infrastructure

**Key Decisions:**
- **wolfctl**: Safe command runner with policy enforcement
  - **Command Policy**: `tools/wolfctl/command-policy.json`
  - **Hardened Shell**: Policy-enforced execution
- **ADR-024**: MCP Tool Candidates Comprehensive Discovery
  - **Survey**: Identified 15-20 candidate packages for MCP conversion
- **ADR-0069**: Claude Code SDK Integration (Phase 3 before/after analysis)

**When to Reference:**
- Tool development decisions
- Infrastructure patterns
- SDK integration approaches

**Files**:
- `/docs/adr/archive/ADR-024-mcp-tool-candidates-comprehensive-discovery.md`
- `/docs/adr/archive/ADR-0069-claude-code-sdk-integration.md`

---

## Phase-Based Organization

### Phase Evolution

**Phases 1-40**: Foundation
- Agent role definitions
- Core principles establishment
- Initial workflow patterns

**Phases 41-45**: Quality Systems
- Verification frameworks (CoVe, HSP, RAG)
- Testing pipelines
- Quality gates

**Phases 46-50**: MCP Integration
- ADR-017: MCP conversion strategy
- ADR-023: Knowledge-first pivot ⭐
- ADR-025: Hybrid consolidation
- wolf-knowledge-mcp operational

**Phase 50+ (Current)**: Refinement
- ADR-072: Workflow standards
- Composite actions
- Enhanced verification

### Key Phase Milestones

| Phase | Key Decision | ADR | Impact |
|-------|--------------|-----|--------|
| 43 | Verification Architecture | ADR-043 | 3-layer verification (CoVe/HSP/RAG) |
| 46-48 | MCP Server Strategy | ADR-017/018 | Operational MCP servers built |
| 49 | Knowledge-First Pivot | ADR-023 | Recognized operational redundancy |
| 50 | Hybrid Consolidation | ADR-025 | wolf-knowledge-mcp primary |
| 50+ | Workflow Standards | ADR-072 | Mandatory GitHub Actions patterns |

---

## Living Architecture Snapshot

**Current Architecture (October 2025)**

The most comprehensive current view is at:
`/docs/adr/phase-50/shard-50-5/current-architecture-2025-10-07.md`

This living document synthesizes all 50+ phases into a current system snapshot, including:
- 4 active MCP servers
- 44 agent roles with inheritance
- 3-layer verification architecture
- Docker-based sandbox infrastructure
- GitHub-native workflow integration
- 335 npm packages (279 optimized forks)

**When to Use**: Starting new work, onboarding, architecture review, system understanding

---

## ADR Format Standard

Wolf ADRs follow this structure:

```markdown
# ADR-XXX: Title

**Status**: Proposed | Accepted | Superseded | Deprecated
**Date**: YYYY-MM-DD
**Deciders**: Role names
**Related ADRs**: Links to related decisions

---

## Context
[Why this decision is needed, background, constraints]

## Problem Statement
[Specific problem being solved]

## Decision
[What was chosen and why]

## Consequences
[Impact, tradeoffs, what changes]

## Alternatives Considered
[Other options and why rejected]

---

## References
[Related docs, issues, PRs]
```

---

## How to Navigate ADRs

### By Status
- **Proposed**: Under review, not yet implemented
- **Accepted**: Approved and active
- **Superseded**: Replaced by newer ADR
- **Deprecated**: No longer applicable

### By Priority
- ⭐ **Critical ADRs** (starred above): Must-read for architecture understanding
- **Topic ADRs**: Read when working in specific domain
- **Historical ADRs**: Context for evolution, not always current

### Search Strategies

**Problem-Based**: "I need to solve X"
→ Check topic cluster for X
→ Read ADRs in that cluster
→ Follow related ADRs

**Technology-Based**: "I'm working with Y"
→ Search ADR index for Y
→ Check current architecture doc
→ Trace decision history

**Phase-Based**: "What changed in Phase Z?"
→ Look at phase-Z ADRs
→ Compare with previous phase
→ Understand evolution

---

## Integration with Wolf Skills

**Wolf ADR skill** integrates with other Wolf skills:

- **wolf-governance**: Search governance rules (may include ADR references)
  - Use: `Skill tool → wolf-governance`
  - Purpose: Understand governance requirements that drive ADR creation

- **wolf-principles**: Query principles (foundational to many ADRs)
  - Use: `Skill tool → wolf-principles`
  - Purpose: Ensure ADRs align with Wolf's 10 core principles

---

## Best Practices

### Creating ADRs
- ✅ Document **why** not just **what**
- ✅ Include alternatives considered
- ✅ Link related ADRs
- ✅ Update status when superseded
- ❌ Don't create ADRs for trivial decisions
- ❌ Don't skip consequences section

### Using ADRs
- ✅ Read current architecture first for overview
- ✅ Trace decision history for context
- ✅ Check status before applying patterns
- ✅ Reference ADRs in new decisions
- ❌ Don't assume old ADRs are current
- ❌ Don't skip related ADRs

### Maintaining ADRs
- ✅ Mark superseded ADRs clearly
- ✅ Keep index up to date
- ✅ Archive old ADRs properly
- ✅ Update living architecture doc
- ❌ Don't delete ADRs (archive instead)
- ❌ Don't modify accepted ADRs (create new superseding ADR)

---

## Related Skills

- **wolf-principles**: Foundation for many ADRs
- **wolf-governance**: Process decisions documented in ADRs
- **wolf-archetypes**: Behavioral archetype decisions
- **wolf-workflows-ci**: GitHub Actions patterns from ADR-072
- **wolf-verification**: Verification architecture from ADR-043

---

## When ADRs Are REQUIRED vs OPTIONAL

### REQUIRED (MUST create ADR)

✅ **Architectural Changes:**
- Changing system architecture or major component structure
- Adding/removing services or significant dependencies
- Modifying data flow or integration patterns
- Infrastructure architecture decisions

✅ **Process Changes:**
- Modifying Wolf's core workflows or methodology
- Changing governance policies or quality gates
- Updating agent role definitions or responsibilities
- Altering approval hierarchies or authority matrix

✅ **Tool Selections:**
- Choosing between competing technologies or frameworks
- Adopting new core dependencies (databases, frameworks, etc.)
- Changing build systems or CI/CD platforms
- MCP server architecture decisions

✅ **Security Decisions:**
- Authentication/authorization approaches
- Security architecture or threat mitigation strategies
- Compliance framework changes

### OPTIONAL (Consider creating ADR)

⚠️ **Significant Patterns:**
- New code patterns that will be reused across codebase
- Design patterns that affect multiple components
- Performance optimization strategies

⚠️ **Experimental Approaches:**
- Research spikes with significant findings
- Proof-of-concept results that inform future direction

### NOT REQUIRED (Skip ADR)

❌ **Trivial Decisions:**
- Bug fixes (use journal entry instead)
- Refactoring without behavior change (use journal entry)
- Minor code cleanup or formatting
- Documentation updates (unless process change)

❌ **Implementation Details:**
- Variable naming conventions
- File organization within existing structure
- Code comment standards

**Rule of Thumb**: If the decision affects future work or needs to be understood months later by different agents, create an ADR.

---

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"ADRs are optional documentation"** - NO. ADRs are REQUIRED for architectural, process, and tool decisions. They prevent repeated debates.
- ❌ **"I'll write the ADR later"** - FORBIDDEN. ADRs must be created BEFORE or DURING decision-making, not after. Later = never.
- ❌ **"This decision is too small for an ADR"** - Wrong metric. If it affects future work or needs historical context, ADR is required.
- ❌ **"I can modify an accepted ADR"** - NO. Accepted ADRs are immutable. Create a new superseding ADR instead.
- ❌ **"ADR format doesn't matter"** - False. Wolf has a standard ADR format. Follow it for consistency and discoverability.

**STOP. Create ADR using standard format BEFORE making architectural/process decisions.**

## After Using This Skill

**RECOMMENDED NEXT STEPS:**

```
ADRs document decisions - used for context and reference
```

1. **Creating an ADR**: Use wolf-governance for quality gates
   - **When**: Before making architectural/process/tool decisions
   - **Why**: ADRs are part of Definition of Done for architectural changes
   - **Tool**: Use Skill tool to load wolf-governance

2. **Understanding Decisions**: Use wolf-principles for decision framework
   - **When**: Evaluating alternatives for ADR
   - **Why**: Principles guide decision-making (e.g., Research-First, Evidence-Based)
   - **Tool**: Use Skill tool to load wolf-principles (focus on Principle #5: Evidence-Based Decisions)

3. **No specific next skill**: ADRs are referenced throughout work
   - This skill provides ADR index and navigation
   - wolf-governance specifies when ADRs are required
   - wolf-principles guide ADR content (alternatives, consequences)

### ADR Creation Checklist

Before claiming ADR complete:

- [ ] Status clearly marked (Proposed, Accepted, Superseded, Deprecated)
- [ ] Context section explains WHY decision is needed (not just WHAT)
- [ ] Decision section documents WHAT was chosen AND WHY
- [ ] Consequences section lists tradeoffs and impacts (positive AND negative)
- [ ] Alternatives Considered section documents rejected options with rationale
- [ ] Related ADRs linked (if decision builds on or supersedes previous ADRs)
- [ ] ADR follows standard format (Context → Problem → Decision → Consequences → Alternatives)

**Can't check all boxes? ADR incomplete. Return to this skill.**

### Good/Bad Examples: ADR Quality

#### Example 1: Well-Structured ADR

<Good>
**ADR-072: GitHub Actions Workflow Standards**

**Status**: Accepted
**Date**: 2025-10-15
**Deciders**: DevOps Team, Code Reviewers
**Related ADRs**: ADR-071 (CI Workflow Optimization), ADR-056 (Composite Actions)

---

## Context

GitHub Actions workflows across WolfAgents had a 37% failure rate due to:
1. Missing checkout steps (37% of failures)
2. Incorrect API field usage (100% failure when wrong fields used)
3. Undeclared permissions causing authorization failures

Investigation of 43 workflows revealed systemic anti-patterns. Need standardized patterns to prevent infrastructure failures.

## Problem Statement

How do we prevent recurring workflow failures caused by missing checkout steps, incorrect GitHub API usage, and permission errors?

## Decision

**Mandate the following standards for all GitHub Actions workflows:**

1. **Mandatory Checkout Step:**
   ```yaml
   - uses: actions/checkout@v4  # MUST be first step
   ```
   Rationale: Without checkout, workflows cannot access repository files.

2. **Correct API Field Names:**
   - Use `closingIssuesReferences` not `closes` for gh pr view
   - Use `labels` not `label` for gh issue view
   Rationale: GitHub CLI expects specific field names; typos cause 100% failure.

3. **Explicit Permissions:**
   ```yaml
   permissions:
     contents: read
     pull-requests: write
     issues: write
   ```
   Rationale: Prevent authorization failures with least-privilege declarations.

## Consequences

**Positive:**
- ✅ Eliminates 37% of workflow failures (missing checkout)
- ✅ Prevents 100% failure rate from API field typos
- ✅ Clear permission boundaries prevent security issues
- ✅ Reusable pattern across all 43+ workflows

**Negative:**
- ⚠️ Requires updating all existing workflows (one-time cost)
- ⚠️ Adds 3-5 lines to each workflow (minimal verbosity)

## Alternatives Considered

**Alternative 1:** Documentation only (no enforcement)
- Rejected: Documentation alone didn't prevent recurring failures
- Teams repeatedly forgot checkout step despite documentation

**Alternative 2:** Pre-commit hooks to validate workflows
- Rejected: Hooks can be bypassed; workflow validation happens too late
- Better to mandate in CI template

**Alternative 3:** Composite action wrapper
- Rejected: Hides checkout step, makes debugging harder
- Mandatory explicit step is more transparent

---

## References
- Issue #789: 37% workflow failure analysis
- PR #845: Workflow standards implementation
- docs/governance/workflow-validation.md

---

**Why this is excellent**:
- ✅ Context explains WHY (failure rates, specific problems)
- ✅ Decision documents WHAT + WHY + HOW (with code examples)
- ✅ Consequences lists both positive AND negative impacts
- ✅ Alternatives explained with rejection rationale
- ✅ Quantified impact (37% failure rate, 100% API field failures)
- ✅ Related ADRs linked for context
- ✅ References provide evidence trail
</Good>

<Bad>
**ADR-999: Use Docker**

**Status**: Proposed
**Date**: 2025-10-20

---

## Context

We should use Docker.

## Decision

Use Docker for containerization.

## Consequences

It will be good.

---

**Why this is terrible**:
- ❌ No context about WHY Docker is needed
- ❌ No problem statement (what problem does Docker solve?)
- ❌ Decision lacks rationale (WHY Docker vs alternatives?)
- ❌ "It will be good" is not a consequence (no tradeoffs, no specifics)
- ❌ No alternatives considered (why not Podman, VMs, native execution?)
- ❌ No related ADRs (surely there are related infra decisions?)
- ❌ No references (no evidence, no analysis)
- ❌ Not enough detail to understand decision months later

**What this should include**:
```markdown
## Context
Current code execution happens on host machine, causing:
1. Security concerns (untrusted code access to host)
2. Resource contention (no isolation between jobs)
3. Dependency conflicts (version mismatches)

Analyzed 200+ execution failures: 45% due to dependency conflicts, 30% resource contention.

## Problem Statement
How do we provide isolated, reproducible code execution environments with resource limits and security boundaries?

## Decision
Use Docker containers for code execution with:
- Resource limits (CPU, memory, disk quotas)
- Network isolation
- Filesystem restrictions
- Capability dropping

Rationale:
- Industry standard (widespread knowledge, tooling)
- Strong isolation model (namespaces, cgroups)
- Reproducible environments (Dockerfile = config as code)
- Resource control (native cgroup support)

## Consequences
Positive:
- ✅ Eliminates 45% of dependency conflict failures
- ✅ Prevents resource contention (isolated CPU/memory)
- ✅ Stronger security boundaries (container escape harder than process escape)
- ✅ Reproducible across dev/CI/prod

Negative:
- ⚠️ Adds Docker dependency (ops overhead)
- ⚠️ Container startup latency (200-500ms vs instant process)
- ⚠️ Increased disk usage (images ~100-500MB)
- ⚠️ Requires Docker daemon (privilege escalation risk)

## Alternatives Considered
1. **Podman**: rootless containers
   - Rejected: Less mature tooling, team unfamiliar
   - May revisit if Docker security concerns grow

2. **VMs (Firecracker)**: microVMs
   - Rejected: Higher overhead (2-3 second startup)
   - Overkill for current security requirements

3. **Native Execution with chroot**: OS-level isolation
   - Rejected: Weaker isolation, no resource limits
   - Insufficient for untrusted code

## References
- Spike results: docs/research/containerization-spike-2025-10.md
- Security analysis: docs/security/execution-isolation-threats.md
- Performance benchmarks: docs/benchmarks/container-overhead.md
```

Now THAT would be an acceptable ADR.
</Bad>

---

**Total ADRs**: 120+
**Active ADRs**: ~70
**Archived ADRs**: ~50
**Living Documents**: 1 (current-architecture)

**Last Updated**: 2025-11-14
**Phase**: Superpowers Skill-Chaining Enhancement v2.0.0
**Maintainer**: Architecture Team
