---
name: doc-intelligence
description: This skill orchestrates comprehensive documentation intelligence operations. Use when asked to "analyze documentation", "learn from docs", "create SOPs from documentation", "maximize documentation understanding", or any request involving systematic multi-agent documentation analysis with parallelization.
---

# Documentation Intelligence System

## Overview

This skill enables systematic, parallelized analysis of documentation using multiple specialized agents. It maximizes throughput by running independent sections in parallel while respecting dependencies, then consolidates findings into actionable SOPs.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      META-ORCHESTRATOR                               │
│  (Coordinates all phases, manages dependencies, tracks progress)     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DOC-OVERVIEW  │    │ PROMPT-ENGINEER │    │   CONSOLIDATOR  │
│  (Structure     │    │ (Optimize all   │    │  (Synthesize    │
│   discovery)    │    │  agent prompts) │    │   findings)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                                            │
          ▼                                            ▼
┌─────────────────────────────────────────┐  ┌─────────────────┐
│         SECTION-ANALYZERS               │  │  SOP-GENERATOR  │
│  (Parallel execution per section)       │  │  (Create SOPs)  │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐   │  └─────────────────┘
│  │ S1 │ │ S2 │ │ S3 │ │ S4 │ │... │   │
│  └────┘ └────┘ └────┘ └────┘ └────┘   │
└─────────────────────────────────────────┘
```

## Workflow Phases

### Phase 0: Structure Discovery
**Agent:** doc-overview
**Action:** Scan documentation structure
**Output:**
- Complete section/subsection map
- Dependency graph
- Parallelization tiers
- Agent assignments

### Phase 1-N: Parallel Section Analysis
**Agent:** section-analyzer (multiple instances)
**Action:** Deep-dive each section based on tier
**Parallelization:** Launch all agents in current tier simultaneously
**Output:** Structured analysis per section

### Phase P: Prompt Optimization
**Agent:** prompt-engineer
**Action:** Optimize prompts based on section findings
**Output:** Refined prompts for future runs

### Phase C: Consolidation
**Agent:** consolidator
**Action:** Synthesize all section analyses
**Output:**
- Unified knowledge model
- Cross-cutting patterns
- Integration synergies
- Knowledge gaps

### Phase S: SOP Generation
**Agent:** sop-generator
**Action:** Create procedures from consolidated knowledge
**Output:** Standard Operating Procedures

## Parallelization Strategy

### Maximum Throughput Mode (20x subscription)
```
Launch all Tier 0 sections simultaneously (up to 20 agents)
As each completes, launch dependent Tier 1 sections
Continue until all tiers complete
Run consolidation
Generate SOPs in parallel for independent workflows
```

### Dependency Rules
```
independent → Can run immediately
soft_dependency → Can run, will be enhanced by dependency
hard_dependency → Must wait for dependency to complete
```

## Cross-Agent Communication

### Shared Context Protocol
```json
{
  "terminology": {
    "term": "definition agreed by all agents"
  },
  "cross_references": [
    {"from": "section_a", "to": "section_b", "type": "extends"}
  ],
  "questions": [
    {"from": "agent_x", "question": "...", "answered_by": "agent_y"}
  ]
}
```

### Message Types
- **TERM_DEFINITION:** New terminology established
- **CROSS_REF:** Cross-reference discovered
- **QUESTION:** Question for other agents
- **ANSWER:** Answer to previous question
- **CONFLICT:** Conflicting information found
- **SYNERGY:** Integration opportunity identified

## Usage Examples

### Full Documentation Analysis
```
"Use doc-intelligence to analyze the Claude Code documentation completely,
identify all sections and dependencies, analyze each in parallel,
consolidate findings, and generate SOPs for common workflows."
```

### Specific Section Deep-Dive
```
"Analyze the 'Build with Claude Code' section using doc-intelligence,
with special focus on Plugins and MCP integration patterns."
```

### SOP-Focused Analysis
```
"Use doc-intelligence to create SOPs for setting up a new Claude Code
project with MCP servers and custom hooks."
```

## Progress Monitoring

### Status Dashboard Format
```
╔════════════════════════════════════════════════════════════╗
║ Documentation Intelligence Operation                        ║
╠════════════════════════════════════════════════════════════╣
║ Phase: 2 of 5 (Parallel Analysis)                          ║
║ Progress: ████████░░░░░░░░░░░░ 40%                        ║
║ Active Agents: 12/20                                        ║
║ Sections Complete: 8/20                                     ║
║ Est. Remaining: 15 minutes                                  ║
╠════════════════════════════════════════════════════════════╣
║ Current Tier: 1 (8 sections parallel)                      ║
║ Waiting: Tier 2 (4 sections, blocked on dependencies)      ║
╚════════════════════════════════════════════════════════════╝
```

## Output Artifacts

After completion, you will have:
1. **documentation-topology.md** - Complete structure map
2. **section-analyses/** - Individual section reports
3. **optimized-prompts.md** - Refined prompts for each section
4. **consolidated-intelligence.md** - Synthesized knowledge
5. **sops/** - Standard Operating Procedures
6. **CLAUDE.md updates** - Integrated learnings

## Continuous Improvement

### Learning Loop
```
Execute → Capture patterns → Update prompts → Execute better
           ↑                                      │
           └──────────────────────────────────────┘
```

### Revision Triggers
- New documentation version released
- Execution feedback received
- Knowledge gaps identified
- Better patterns discovered

## Integration with Memory Systems

### claude-mem Integration
- Store successful analysis patterns
- Remember cross-section learnings
- Cache optimized prompts
- Track improvement metrics

### CLAUDE.md Updates
- Add discovered best practices
- Update agent configurations
- Record successful workflows
- Note areas for improvement
