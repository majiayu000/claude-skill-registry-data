---
name: internet-deep-orchestrator
description: Orchestrate comprehensive 7-phase RBMAS research for multi-dimensional queries (4+ dimensions). Coordinates multiple specialist agents through SCOPE → PLAN → RETRIEVE → TRIANGULATE → DRAFT → CRITIQUE → PACKAGE methodology. Use for thorough internet research requiring multiple sources, iterative refinement, and quality gates. Triggers - research, investigate, analyze with 4+ distinct dimensions or comprehensive depth requirements.
---

# Comprehensive Deep Research Orchestration (Tier 4 RBMAS)

Guide Main Claude to coordinate comprehensive multi-phase research using 7-phase RBMAS methodology for established domains requiring 4+ dimensions of analysis.

## Quick Start

1. **Analyze query dimensions** - Identify 4+ subtopics/angles requiring deep investigation
2. **Setup progress tracking** - Use TodoWrite to track 7 RBMAS phases
3. **Execute RBMAS phases** - Follow structured methodology with quality gates
4. **Spawn specialist subagents** - Minimum 3-5 agents (web-researcher, academic-researcher, fact-checker)
5. **Validate quality** - Check citation density, source diversity, gap detection
6. **Synthesize findings** - Combine results into comprehensive report
7. **Report completion** - Deliver comprehensive analysis with citations

## 7-Phase RBMAS Methodology

### Phase 1: SCOPE
**Objective**: Break down research question into focused sub-questions

MUST:
- Analyze the research question thoroughly
- Identify 5-7 key concepts and sub-questions
- Define research boundaries and objectives
- Map dimensions to specific investigation areas

Example sub-questions for "WebRTC security":
- Cryptographic protocols (DTLS, SRTP)
- Network security (ICE, TURN vulnerabilities)
- Implementation security (browser implementations)
- Authentication mechanisms
- Attack vectors and mitigations

### Phase 2: PLAN
**Objective**: Develop comprehensive research strategy

MUST:
- Create strategy for each sub-question
- Identify required sources (web, academic, documentation)
- Plan verification and cross-referencing approach
- Estimate depth and breadth needed per dimension
- Allocate specialist agents to dimensions

### Phase 3: RETRIEVE (MANDATORY SPAWNING)
**Objective**: Gather information through specialist subagents

🚨 **CRITICAL**: Main Claude MUST spawn subagents. NEVER skip this phase.

MUST:
- Spawn 3-7 specialist subagents using Task tool
- Use web-researcher for general web queries
- Use academic-researcher for scholarly sources
- Use search-specialist for complex Boolean queries
- Spawn agents IN PARALLEL (not sequential)
- Pass all research parameters to subagents

Example subagent spawn:
```
Task(
  subagent_type: "web-researcher",
  description: "Research WebRTC cryptographic protocols",
  prompt: "Research DTLS and SRTP protocols used in WebRTC...

Focus:
- Protocol specifications
- Implementation details
- Security considerations
- Current best practices (2024-2025)

Requirements:
- Multiple authoritative sources
- Include URLs and timestamps
- Cite specifications and standards",
  model: "sonnet"
)
```

### Phase 4: TRIANGULATE (MANDATORY VERIFICATION)
**Objective**: Cross-reference and verify findings

🚨 **CRITICAL**: Main Claude MUST spawn fact-checker for critical claims.

MUST:
- Cross-reference findings across sources
- Identify consensus vs conflicting information
- Spawn fact-checker agent for critical claims
- Flag uncertainties and knowledge gaps
- Validate citations and source quality

Quality Gates:
- ✅ Citation density: Minimum 3 sources per major claim
- ✅ Source diversity: Mix of academic, industry, official docs
- ✅ Gap detection: Explicitly flag missing information

### Phase 5: DRAFT
**Objective**: Synthesize findings into coherent narrative

MUST:
- Synthesize findings from all subagents
- Organize by themes and importance
- Include evidence and citations inline
- Maintain objectivity and acknowledge limitations
- Structure report with clear sections

### Phase 6: CRITIQUE
**Objective**: Review for quality and completeness

MUST:
- Review for accuracy, completeness, and bias
- Identify gaps requiring additional research
- Verify citation accuracy
- Ensure claims properly supported
- Check against quality gates

### Phase 7: PACKAGE
**Objective**: Deliver final comprehensive report

MUST:
- Format final research report in markdown
- Include executive summary and bibliography
- Add confidence assessments per claim
- Document methodology and sources
- Save comprehensive report

## Delegation Rules (CRITICAL)

Main Claude MUST:
1. ❌ **NEVER research directly** - Always spawn subagents for information gathering
2. ✅ **ALWAYS spawn 3-7 specialist subagents** (one or more per dimension)
3. ✅ **ALWAYS spawn fact-checker** in Phase 4 for verification
4. ✅ **SPAWN agents IN PARALLEL** (not sequential) for efficiency
5. ✅ **PASS research parameters** to all subagents clearly

Minimum subagent requirements:
- 3-5 researchers (web-researcher, academic-researcher, search-specialist)
- 1 fact-checker (verification)
- Optional: synthesis-researcher (if not doing synthesis yourself)

## Quality Gates (Mandatory Validation)

Before completing Phase 7, VERIFY:

✅ **Citation Density**:
- Minimum 3 authoritative sources per major claim
- Sources include URLs and timestamps
- Mix of academic, industry, official documentation

✅ **Source Diversity**:
- NOT all sources from single domain
- Multiple independent authorities
- Recent sources (2023-2025 preferred)

✅ **Gap Detection**:
- Explicitly flag missing information
- Acknowledge conflicting data
- Note areas requiring further research

✅ **Methodology Documentation**:
- 7 phases all executed
- Subagents spawned as required
- Verification performed

## Examples

### Example 1: Comprehensive 4-Dimension Query

**Query**: "Research WebRTC security across cryptography, network, implementation, and browser dimensions"

**Response**:
```
I'll coordinate comprehensive WebRTC security research using 7-phase RBMAS methodology.

[TodoWrite: Tracks 7 phases]

Phase 1 (SCOPE): Breaking into 4 dimensions:
1. Cryptographic protocols (DTLS, SRTP)
2. Network security (ICE, TURN, STUN)
3. Implementation security (codebase analysis)
4. Browser-specific security (Chrome, Firefox, Safari)

Phase 2 (PLAN): Allocating specialists:
- academic-researcher: Cryptographic protocol research
- web-researcher: Network security and browser implementations
- search-specialist: Implementation vulnerabilities
- fact-checker: Verify critical security claims

Phase 3 (RETRIEVE): Spawning subagents...
[Spawns 4 agents IN PARALLEL using Task tool]

[Wait for agents to complete]

Phase 4 (TRIANGULATE): Verifying findings...
[Spawns fact-checker for critical claims]

Phases 5-7: Drafting, critiquing, packaging comprehensive report...

[Delivers 4-dimension comprehensive analysis with citations]
```

### Example 2: BAD - Skip Spawning (VIOLATION)

**Query**: "Research cloud gaming latency optimization comprehensively"

❌ **WRONG Response**:
```
Let me research cloud gaming latency optimization.
[Directly uses WebSearch without spawning subagents]
```

**Why Wrong**: Tier 4 MUST orchestrate subagents through 7 phases, NOT research directly.

✅ **CORRECT Response**:
```
I'll coordinate comprehensive cloud gaming latency research using RBMAS.

Phase 1 (SCOPE): 5 dimensions identified...
Phase 2 (PLAN): Strategy developed...
Phase 3 (RETRIEVE): Spawning specialists...
[Spawns web-researcher, academic-researcher, search-specialist]
```

### Example 3: Quality Gate Failure → Retry

**Scenario**: Phase 6 CRITIQUE detects gaps

**Response**:
```
Phase 6 (CRITIQUE): Quality gate check...

⚠️ Gap detected: Insufficient sources on browser-specific implementations
- Only 1 source for Firefox implementation
- No sources for Safari implementation

Returning to Phase 3 (RETRIEVE):
[Spawns additional search-specialist for browser implementations]

[After retrieval] Phase 6 (CRITIQUE): Re-checking quality gates...
✅ Citation density: Passed (3+ sources per claim)
✅ Source diversity: Passed (academic + industry + official docs)
✅ Gap detection: Passed (all dimensions covered)

Proceeding to Phase 7 (PACKAGE)...
```

## Response Style

Main Claude MUST:
- Be concise and direct (2-4 sentences per phase update)
- Use TodoWrite to track phase progress
- Report subagent spawn status clearly
- Indicate quality gate results explicitly
- Deliver comprehensive final synthesis

Main Claude MUST NOT:
- Skip phases or subagent spawning
- Research directly instead of delegating
- Ignore quality gates
- Provide superficial analysis

## Key Principles

1. **Depth over Speed**: Take time to explore thoroughly across all dimensions
2. **Source Diversity**: Use multiple independent authoritative sources
3. **Transparency**: Cite sources, acknowledge limitations, flag gaps
4. **Objectivity**: Present facts, note when conclusions are inferential
5. **Iteration**: Refine understanding through quality gates and re-retrieval
6. **Orchestration**: Coordinate multiple specialists, never research alone

## When to Use This Skill

✅ **USE** internet-deep-orchestrator when:
- Query has 4+ distinct dimensions or subtopics
- Comprehensive analysis required (not simple lookup)
- Multiple specialist perspectives needed
- Quality validation critical (citations, verification)
- Iterative refinement valuable

❌ **DON'T USE** (use other tiers instead):
- Simple lookups (Tier 1: web-researcher)
- Focused single-topic research (Tier 2: specialist agents)
- 2-3 dimension queries (Tier 3: internet-light-orchestrator)
- Novel/emerging domains (Tier 5: internet-research-orchestrator)

## Success Criteria

Phase 3 complete when:
- ✅ Minimum 3-5 subagents spawned
- ✅ All dimensions covered by specialists
- ✅ Agents spawned in parallel (not sequential)

Phase 7 complete when:
- ✅ All 7 phases executed
- ✅ Quality gates passed (citations, diversity, gaps)
- ✅ Comprehensive report delivered with bibliography
- ✅ Confidence assessments provided per claim

---

**Methodology**: RBMAS (Research-Based Multi-Agent System)
**Complexity**: Tier 4 (Comprehensive)
**Dimensions**: 4+ subtopics
**Subagents**: 3-7 specialists (minimum)
**Quality Gates**: Mandatory (citation density, source diversity, gap detection)
