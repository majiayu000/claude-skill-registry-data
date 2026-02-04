---
name: rca-analysis
description: Perform Root Cause Analysis using a multi-agent swarm approach. Use when investigating bugs, failures, performance issues, or any problem requiring systematic diagnosis. Triggers on requests like "why is X failing", "debug this issue", "find the root cause", "investigate this problem", or explicit RCA requests.
---

# Root Cause Analysis

Dispatch 3-7 specialized RCA agents in parallel to investigate a problem from different angles, then synthesize findings into a comprehensive report.

## Workflow

### 1. Parse and Size the Swarm

Given a `problem_statement`:
- Infer agent count from problem complexity (breadth of domains, surface area, symptoms)
- Set `agents_count = clamp(inferred_agents, 3, 7)` - always use at least 3 agents
- Select focus areas from the taxonomy below - ensure complementary coverage
- Output chosen count, focus areas, and rationale to console

### 2. Focus Area Taxonomy

Select areas based on problem characteristics. Mix layers and concerns as needed.

**Tech Layers:**
- `UI/Presentation` - Frontend components, rendering, user interaction
- `API/Backend` - Endpoints, request handling, response formation
- `Data/Database` - Queries, schemas, data integrity, persistence
- `Config/Infrastructure` - Environment, deployment, external services
- `Dependencies` - Third-party libs, version conflicts, compatibility

**Concerns (Cross-cutting):**
- `State Management` - Application state, caching, synchronization
- `Business Logic` - Domain rules, validation, workflows
- `Integration` - Service boundaries, contracts, data transformation
- `Performance` - Latency, throughput, resource utilization
- `Security` - Auth, authz, data protection, input validation

### 3. Dispatch Agents (Parallel)

Use the Task tool with `subagent_type="rca"` for each agent. Include these headers in each prompt:

```
<FOCUS_AREA>[Selected Area from Taxonomy]</FOCUS_AREA>

<PROBLEM_STATEMENT>
[Problem statement verbatim]
</PROBLEM_STATEMENT>
```

Ensure focus areas are complementary - cover different layers/concerns to maximize investigative breadth.

### 4. Collect and Synthesize

After all agents return their `<rca_findings>` XML blocks:

- **Parse** - Extract `<evidence>`, `<observations>`, and `<layer_status>` from each agent's XML
- **Collect** - Gather all evidence items into a unified view, grouped by type
- **Cross-Reference** - Look for:
  - Multiple agents pointing to same location/component (convergence)
  - Contradictory observations (indicates complexity)
  - Cleared layers (narrows the search)
- **Weigh** - Observations with `confidence="high"` from multiple agents carry more weight
- **Check Status** - Which layers are `suspect` vs `cleared` vs `inconclusive`?
- **Determine Verdict:**
  - Root cause identified (high confidence) - multiple agents converge
  - Root cause suspected (medium confidence) - single agent found it, others cleared
  - Inconclusive (low confidence) - need more investigation

### 5. Render Report

Use the template in [references/report-template.md](references/report-template.md).

## Resources

- **references/agent-prompt.md** - The RCA agent system prompt for Task tool dispatches
- **references/report-template.md** - The final report template structure
