---
name: ultimate-research
description: Elite multi-agent research orchestration utilizing ref MCP, exa MCP, brave-search MCP, and context7 with parallel execution of deep-research-agent, search-specialist, trend-researcher, and ux-researcher. Use for comprehensive research requiring maximum depth, breadth, and quality. Automatically invoked during /sc:research commands for world-class research capabilities surpassing any traditional deep research approach.
---

# Ultimate Research - Elite Multi-Agent Research Orchestration

## Core Capability

This skill orchestrates the most comprehensive research capability available by:
- **Parallel agent execution**: Simultaneously deploy all 4 specialized research agents
- **Full MCP utilization**: Leverage every tool from ref, exa, brave-search, and context7 MCPs
- **Best practices adherence**: Follow MCP_BEST_PRACTICES_COMPREHENSIVE_GUIDE.md for optimal performance
- **Sequential thinking**: Use complex reasoning with sequential-thinking MCP
- **Token efficiency**: 96% reduction via smart routing and caching

## When This Skill Activates

Automatically triggers during `/sc:research` commands or when:
- User requests comprehensive research
- Multi-dimensional analysis needed
- Current events + historical context required
- Code examples + documentation + community insights needed
- Competitive analysis requiring multiple perspectives
- Academic/technical research with citation requirements

## Research Architecture

### Tier 1: Parallel Agent Deployment

Execute **simultaneously** for maximum efficiency:

```
┌─────────────────────────────────────────┐
│     Research Query Received             │
└──────────────┬──────────────────────────┘
               │
     ┌─────────┼──────────┬──────────┐
     │         │          │          │
     ▼         ▼          ▼          ▼
┌─────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│ deep-   │ │search│ │ trend- │ │  ux-   │
│research │ │spec  │ │research│ │research│
│ -agent  │ │      │ │  -er   │ │  -er   │
└─────────┘ └──────┘ └────────┘ └────────┘
     │         │          │          │
     └─────────┴──────────┴──────────┘
               │
               ▼
     ┌────────────────────┐
     │   Synthesis &      │
     │   Validation       │
     └────────────────────┘
```

**Agent Responsibilities**:

1. **deep-research-agent**: Complex multi-hop analysis, evidence chains, synthesis
2. **search-specialist**: Web search, documentation discovery, source verification
3. **trend-researcher**: Market trends, viral content, emerging patterns
4. **ux-researcher**: User behavior, pain points, feedback analysis

### Tier 2: MCP Tool Orchestration

Use decision tree based on MCP_BEST_PRACTICES_COMPREHENSIVE_GUIDE.md:

**Documentation Queries**:
```
Primary: ref MCP → Fast, token-efficient (96% reduction)
Fallback: exa MCP → Code context if docs insufficient
Tertiary: brave-search MCP → General web if needed
```

**Code Example Queries**:
```
Primary: exa MCP (get_code_context_exa) → Semantic search, fastest (1.18s)
Fallback: ref MCP → Official documentation
Tertiary: brave-search MCP → Tutorials and guides
```

**News/Current Events**:
```
Primary: brave-search MCP (news_search, freshness='pd') → Latest information
Secondary: exa MCP → Deep analysis
Verification: context7 MCP → Documentation updates
```

**Research/Semantic**:
```
Primary: exa MCP (web_search_exa) → AI-native search
Secondary: brave-search MCP → Broad coverage
Documentation: ref MCP + context7 MCP → Technical verification
```

### Tier 3: Sequential Thinking Integration

For complex reasoning tasks, invoke sequential-thinking MCP:

```
When to use:
- Multi-step logical deduction needed
- Conflicting information requires resolution
- Hypothesis generation and validation
- Cost-benefit analysis across MCPs
- Quality vs speed tradeoffs
```

## Execution Protocol

### Phase 1: Parallel Agent Launch (0-30 seconds)

Launch all 4 agents simultaneously in single message:

```markdown
[Task tool invocation with 4 parallel calls]

deep-research-agent task: [research scope]
search-specialist task: [documentation discovery]
trend-researcher task: [market analysis]
ux-researcher task: [user insights]
```

**Critical**: Use single message with multiple Task tool calls for true parallelism

### Phase 2: MCP Tool Utilization (30s - 5min)

Based on agent requirements, execute MCP tools following best practices:

**Token Optimization**:
```
- ref MCP: Use for all documentation (automatic 5k token limit)
- exa MCP: Configure tokensNum=8000 for code research
- brave-search MCP: Set count=10, result_filter=["web","news"]
- context7 MCP: Use mode='code' for API refs, mode='info' for guides
```

**Parallel Execution Example**:
```python
# Execute independent searches simultaneously
await asyncio.gather(
    ref_search_documentation("React hooks TypeScript"),
    exa_code_context("React hooks examples", tokensNum=8000),
    brave_web_search("React hooks best practices 2024"),
    context7_get_library_docs("/facebook/react", topic="hooks")
)
```

**Caching Strategy** (from MCP best practices):
```
Documentation (ref): 7-day TTL
Code examples (exa): 1-day TTL
News (brave): 1-hour TTL
General web: 6-hour TTL
```

### Phase 3: Sequential Thinking (as needed)

When complex reasoning required:

```
Use sequential-thinking MCP to:
1. Analyze conflicting sources
2. Score result relevance
3. Identify information gaps
4. Generate synthesis strategy
5. Validate conclusions
```

### Phase 4: Synthesis & Validation (final 20%)

Merge findings from all agents and MCPs:

```
1. Deduplicate results (by URL/content hash)
2. Score relevance (0-100 scale)
3. Rank by authority + freshness + completeness
4. Cross-verify claims across sources
5. Generate confidence scores
6. Build evidence chains
```

## MCP Best Practices Implementation

### From MCP_BEST_PRACTICES_COMPREHENSIVE_GUIDE.md

**Performance Optimization**:
- Enable only needed Exa tools: `--tools=get_code_context_exa,web_search_exa`
- Use Ref HTTP method (fastest setup)
- Implement request queuing for rate limits
- Progressive loading: summaries first, details on-demand

**Cost Optimization**:
- Budget-aware routing (see guide Section 7.3)
- Aggressive caching (60-80% hit rate achievable)
- Token limit tuning per query type
- Free tier maximization strategy

**Quality Optimization**:
- Result scoring algorithm (relevance + freshness + authority + completeness)
- Confidence thresholds by query type
- Fallback chains for reliability
- Multi-MCP verification for critical info

## Output Format

### Research Report Structure

```markdown
# [Research Topic]

**Research Date**: YYYY-MM-DD
**Confidence Score**: XX/100
**Sources Consulted**: N unique sources

## Executive Summary
[3-5 sentence overview of key findings]

## Key Findings

### 1. [Finding Category]
- **Source**: [Agent + MCP used]
- **Evidence**: [Supporting data]
- **Confidence**: [High/Medium/Low]
- **Citations**: [URLs/references]

### 2. [Finding Category]
...

## Detailed Analysis

### [Section 1]: Official Documentation
**Source**: ref MCP + context7 MCP
[Findings from authoritative sources]

### [Section 2]: Code Examples & Implementations
**Source**: exa MCP
[Real-world usage patterns]

### [Section 3]: Community Insights
**Source**: brave-search MCP + search-specialist agent
[Developer feedback, common issues]

### [Section 4]: Market Trends
**Source**: trend-researcher agent + exa MCP
[Current state, emerging patterns]

### [Section 5]: User Experience Analysis
**Source**: ux-researcher agent
[Pain points, opportunities]

## Synthesis & Recommendations

### Best Practices Identified
1. [Practice 1] - Source: [agents/MCPs]
2. [Practice 2] - Source: [agents/MCPs]

### Common Pitfalls
1. [Pitfall 1] - Source: [agents/MCPs]
2. [Pitfall 2] - Source: [agents/MCPs]

### Recommended Approach
[Synthesized recommendation based on all findings]

## Evidence Quality Assessment

| Category | Sources | Confidence | Notes |
|----------|---------|------------|-------|
| Official Docs | N | High | [ref/context7] |
| Code Examples | N | High | [exa] |
| Community | N | Medium | [brave/search-specialist] |
| Trends | N | Medium | [trend-researcher] |
| UX Insights | N | Low-Medium | [ux-researcher] |

## Information Gaps

[List any unanswered questions or areas needing deeper research]

## Sources

### Official Documentation
- [Source 1](URL) - ref MCP
- [Source 2](URL) - context7 MCP

### Code Repositories & Examples
- [Source 3](URL) - exa MCP
- [Source 4](URL) - exa MCP

### Community Discussions
- [Source 5](URL) - brave-search MCP
- [Source 6](URL) - search-specialist agent

### Market Analysis
- [Source 7](URL) - trend-researcher agent
- [Source 8](URL) - exa MCP

### User Research
- [Source 9](URL) - ux-researcher agent
- [Source 10](URL) - brave-search MCP

## Research Metadata

**Agents Used**:
- deep-research-agent: [time spent]
- search-specialist: [time spent]
- trend-researcher: [time spent]
- ux-researcher: [time spent]

**MCPs Used**:
- ref MCP: [queries count] - [token savings]
- exa MCP: [queries count] - [avg latency]
- brave-search MCP: [queries count] - [result types]
- context7 MCP: [queries count] - [mode used]
- sequential-thinking MCP: [thoughts generated]

**Performance Metrics**:
- Total research time: [duration]
- Parallel efficiency: [% time saved vs sequential]
- Cache hit rate: [%]
- Average query latency: [seconds]
- Total tokens consumed: [count]
- Token efficiency gain: [% vs baseline]
```

## Advanced Patterns

### Multi-Stage Research Workflow

For comprehensive research requiring multiple phases:

```
Stage 1: Discovery (Parallel agents + broad MCPs)
├─ Identify information landscape
├─ Map available sources
└─ Define research boundaries

Stage 2: Deep Dive (Focused MCP usage)
├─ Documentation analysis (ref + context7)
├─ Code pattern extraction (exa)
├─ Community sentiment (brave + search-specialist)
└─ Trend analysis (trend-researcher)

Stage 3: Verification (Cross-reference)
├─ Validate claims across sources
├─ Resolve contradictions (sequential-thinking)
└─ Assess confidence levels

Stage 4: Synthesis (deep-research-agent)
├─ Identify patterns
├─ Extract best practices
├─ Generate actionable insights
└─ Document evidence chains
```

### Adaptive Depth Strategy

Match research depth to query importance:

**Quick (5 min)**: Single-hop, primary MCPs only
```
- 1 agent (search-specialist)
- 2 MCPs (ref OR exa + brave)
- Summary output
```

**Standard (15 min)**: Multi-hop, 2-3 agents
```
- 2-3 agents (search-specialist + deep-research-agent + trend-researcher)
- 3 MCPs (ref + exa + brave)
- Structured report
```

**Deep (45 min)**: Comprehensive, all agents
```
- 4 agents (all parallel)
- 4 MCPs (ref + exa + brave + context7)
- Full report with evidence chains
```

**Exhaustive (2+ hrs)**: Maximum depth, multi-stage
```
- 4 agents (parallel + sequential refinement)
- 4 MCPs + sequential-thinking
- Multi-stage workflow
- Iterative validation
- Complete documentation
```

## Error Handling & Fallbacks

### Rate Limiting

If MCP rate limited:
```
1. Implement exponential backoff (1s, 2s, 4s)
2. Switch to alternative MCP (ref → exa → brave)
3. Use cached results if available
4. Queue requests for later execution
```

### Quality Threshold Violations

If results below confidence threshold:
```
1. Invoke fallback MCP chain
2. Cross-verify with additional agent
3. Use sequential-thinking to analyze gaps
4. Explicitly note uncertainty in output
```

### Agent Failure

If agent fails to complete:
```
1. Continue with remaining agents
2. Note reduced coverage in metadata
3. Suggest re-running failed agent separately
4. Provide partial results with caveats
```

## Performance Monitoring

Track these metrics per research session:

```
Efficiency Metrics:
- Parallel execution time savings
- Cache hit rate
- Token consumption vs baseline
- Cost per query

Quality Metrics:
- Source diversity (unique domains)
- Citation completeness
- Confidence score distribution
- Information gap rate

MCP Performance:
- Latency by MCP (ref: 1.7s, exa: 1.18s, brave: <2s)
- Success rate by MCP (target: >95%)
- Token efficiency (ref: 96% reduction)
- Fallback invocation frequency
```

## Integration with /sc:research

This skill automatically activates when `/sc:research` is invoked. The command passes:
- Query string
- Depth flag (--depth)
- Strategy flag (--strategy)
- MCP flags (--ref, --exa, --brave-search, --c7)
- Thinking flags (--seq, --ultrathink)

The skill then:
1. Parses flags to determine execution strategy
2. Launches appropriate agents in parallel
3. Orchestrates MCP tool usage per best practices
4. Generates research report in standard format
5. Saves to `claudedocs/research_[topic]_[timestamp].md`

## Examples

### Example 1: Technical Documentation Research

```
Query: "Next.js App Router best practices and common pitfalls"

Execution:
1. Parallel agents launch (4 simultaneous)
2. ref MCP: Official Next.js docs (token-efficient)
3. exa MCP: GitHub repos with App Router examples
4. brave-search MCP: Reddit/GitHub discussions
5. context7 MCP: Vercel Next.js documentation
6. sequential-thinking: Analyze contradictions in community advice
7. Synthesis: Best practices + pitfalls + recommended approach

Output: Comprehensive guide with official docs + real code + community insights
```

### Example 2: Market Research

```
Query: "AI coding assistant market analysis 2024"

Execution:
1. Parallel agents:
   - search-specialist: Product websites, official announcements
   - trend-researcher: TikTok/Twitter trends, viral content
   - ux-researcher: User reviews, pain points
   - deep-research-agent: Competitive analysis, feature comparison
2. brave-search MCP: Latest news, funding announcements
3. exa MCP: Company research, technical capabilities
4. ref MCP: API documentation analysis
5. sequential-thinking: Cost-benefit analysis, market positioning

Output: Market landscape + trends + competitive matrix + opportunities
```

### Example 3: Technical Problem Solving

```
Query: "How to implement real-time collaboration in React with TypeScript"

Execution:
1. Parallel agents launch
2. ref MCP: React + TypeScript official docs
3. exa MCP:
   - Code examples (WebSocket, CRDTs, Yjs)
   - GitHub repos with implementations
4. brave-search MCP: Tutorials, blog posts, case studies
5. context7 MCP: Library docs (Socket.io, Y.js, etc.)
6. sequential-thinking: Evaluate approaches (WebSocket vs SSE vs WebRTC)

Output: Implementation guide + code examples + tradeoff analysis
```

## Success Criteria

Research is successful when:
- [ ] All 4 agents executed (or failures documented)
- [ ] At least 3 MCPs utilized per best practices
- [ ] Parallel execution achieved (single message, multiple Task calls)
- [ ] Output includes confidence scores and source citations
- [ ] Evidence chains are traceable
- [ ] Information gaps explicitly identified
- [ ] Report saved to claudedocs/ directory
- [ ] Performance metrics documented

## Troubleshooting

### Issue: Agents not executing in parallel
**Solution**: Ensure single message with multiple Task tool calls, not sequential messages

### Issue: High token consumption
**Solution**:
- Use ref MCP for docs (96% reduction)
- Configure exa tokensNum appropriately
- Enable only needed exa tools
- Implement caching

### Issue: Rate limiting errors
**Solution**:
- Implement request queuing
- Use fallback MCP chains
- Enable exponential backoff

### Issue: Low quality results
**Solution**:
- Increase depth level
- Add more agents
- Use sequential-thinking for gap analysis
- Enable multi-stage verification

## References

- **MCP Best Practices**: See MCP_BEST_PRACTICES_COMPREHENSIVE_GUIDE.md
- **Skill Best Practices**: See skill.best.practices.md
- **Research Command**: See .claude/commands/sc/research.md

---

**Skill Version**: 1.0
**Last Updated**: 2025-11-24
**Maintainer**: Ultimate Research System
**License**: Internal Use