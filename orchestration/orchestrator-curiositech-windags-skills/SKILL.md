---
license: Apache-2.0
name: orchestrator
description: 'DEPRECATED: Use dag-orchestrator instead. This skill has been merged into the more powerful dag-orchestrator skill.'
allowed-tools: Read
category: Agent & Orchestration
tags:
  - orchestration
  - workflow
  - coordination
  - execution
  - management
---

# Orchestrator (DEPRECATED)

**This skill is deprecated. Use `dag-orchestrator` instead.**

## DECISION POINTS

```
IF user explicitly requests "orchestrator" skill
├─ Check deprecation awareness:
│  ├─ User knows it's deprecated → Guide to dag-orchestrator equivalent
│  └─ User unaware → Explain deprecation + redirect
└─ Provide specific migration path based on use case

IF user mentions orchestration without skill name
├─ Simple task sequencing → Direct to dag-orchestrator basic mode
├─ Complex multi-step workflow → Guide to dag-orchestrator HTDAG
├─ Agent coordination → Use dag-orchestrator multi-agent features
└─ Legacy system integration → Assess dag-orchestrator compatibility

IF existing code references orchestrator
├─ Basic coordination calls → Map to dag-orchestrator syntax
├─ Custom orchestration patterns → Manual migration required
├─ Integration dependencies → Check dag-orchestrator equivalents
└─ Performance-critical paths → Validate dag-orchestrator performance

IF migration resistance encountered
├─ Feature concerns → Demonstrate dag-orchestrator superiority
├─ Learning curve → Provide step-by-step migration
├─ Technical debt → Plan gradual transition strategy
└─ Team coordination → Establish migration timeline
```

## FAILURE MODES

**Silent Skill Usage**
- *Detection*: Agent attempts to invoke orchestrator without deprecation notice
- *Diagnosis*: Missed deprecation check or automated skill selection
- *Fix*: Always check skill status before invocation; redirect with explanation

**Feature Parity Anxiety**
- *Detection*: "dag-orchestrator doesn't do X like orchestrator did"
- *Diagnosis*: Incomplete feature mapping or misunderstood capabilities
- *Fix*: Provide detailed capability comparison table with examples

**Migration Procrastination**
- *Detection*: Continued orchestrator references despite alternatives shown
- *Diagnosis*: Change resistance or perceived migration complexity
- *Fix*: Break migration into small steps; show immediate benefits

**Hybrid Skill Confusion**
- *Detection*: User requests both orchestrator and dag-orchestrator for same task
- *Diagnosis*: Unclear on skill consolidation and unified architecture
- *Fix*: Explain skill evolution and demonstrate single-skill solution

**Legacy Lock-in**
- *Detection*: "Can't change because existing system depends on orchestrator"
- *Diagnosis*: Hard dependencies or undocumented integration points
- *Fix*: Dependency audit, compatibility layer, phased migration plan

## WORKED EXAMPLES

### Complete Migration: Multi-Stage Data Pipeline

**Scenario**: User has existing orchestrator-based pipeline: extract → transform → validate → load

**Step 1 - Detection**:
User says: "Update my orchestrator workflow for the new data source"
Agent detects: orchestrator skill reference

**Step 2 - Deprecation Notice**:
"I notice you're referencing the orchestrator skill, which has been deprecated. Let me upgrade your workflow to use dag-orchestrator, which provides better performance and error handling."

**Step 3 - Capability Mapping**:
- Old: `orchestrator.sequence([extract, transform, validate, load])`
- New: `dag-orchestrator.create_pipeline({nodes: [extract, transform, validate, load], dependencies: [extract→transform, transform→validate, validate→load]})`

**Step 4 - Enhanced Features Demo**:
- Show parallel execution capabilities: extract + metadata_fetch
- Demonstrate error recovery: retry policies on each stage
- Display monitoring: real-time progress tracking

**Step 5 - Migration Execution**:
- Convert workflow definition
- Test with sample data
- Validate performance improvements (30% faster execution)
- Document new monitoring capabilities

**Outcome**: User gains improved workflow with better error handling and observability.

## QUALITY GATES

- [ ] Deprecation notice clearly communicated to user
- [ ] dag-orchestrator alternative provided for specific use case
- [ ] Migration path documented with concrete steps
- [ ] Feature parity demonstrated or gaps acknowledged
- [ ] Performance/capability improvements highlighted
- [ ] Legacy code references identified and replacement provided
- [ ] User confirms understanding of skill consolidation
- [ ] No silent fallback to deprecated orchestrator occurs
- [ ] dag-orchestrator syntax demonstrated with working examples
- [ ] Integration compatibility verified for existing systems

## NOT-FOR BOUNDARIES

**Do NOT attempt to use orchestrator skill for**:
- New workflow creation → Use dag-orchestrator
- Complex orchestration patterns → Use dag-orchestrator with HTDAG
- Multi-agent coordination → Use dag-orchestrator multi-agent features
- Performance-critical orchestration → Use optimized dag-orchestrator
- Error-prone workflow management → Use dag-orchestrator with retry policies

**For these specific needs, delegate to dag-orchestrator**:
- Wave-based execution → dag-orchestrator.wave_execution()
- Dynamic task decomposition → dag-orchestrator.adaptive_decomposition()
- Parallel processing → dag-orchestrator.parallel_execution()
- Conditional branching → dag-orchestrator.conditional_nodes()
- Real-time monitoring → dag-orchestrator.progress_tracking()

**Escalation scenarios**:
- If dag-orchestrator truly lacks required functionality → File enhancement request
- If migration timeline conflicts with deadlines → Create compatibility bridge
- If legacy systems cannot integrate → Design adapter pattern

**Boundary enforcement**: Never execute orchestrator skill calls; always redirect through deprecation process to dag-orchestrator equivalent.