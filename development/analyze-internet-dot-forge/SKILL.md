---
name: analyze
description: "Run codebase analysis via Analyst agent. Triggers: \"forge analyze\", \"analyze codebase\", \"code analysis\", \"architecture analysis\", \"impact analysis\", \"dependency trace\"."
---

<Purpose>
On-demand codebase analysis using the Analyst agent and codebase-memory-mcp tools.
Produces architecture maps, impact reports, dependency traces, or quality assessments
depending on what the user asks for. Can run standalone or feed results into an active
Forge phase (design, develop, fix).

This skill must produce a durable analysis artifact and analysis metadata, not just
an ephemeral chat answer.
</Purpose>

<Use_When>
- User asks "forge analyze", "analyze this codebase", "code analysis"
- KO: "코드 분석", "아키텍처 분석"  JA: "コード分析", "アーキテクチャ分析"  ZH: "代码分析", "架构分析"
- User wants architecture mapping before making changes
- User asks "what would break if I change X?"
- User asks about dependencies, coupling, dead code, or complexity
- During design phase to map existing code before architecture decisions
- During fix/troubleshoot to trace dependencies for root cause analysis
</Use_When>

<Do_Not_Use_When>
- User wants external library/framework research (use Researcher instead)
- User wants to verify a specific technical claim (use Fact-Checker instead)
- User wants bug diagnosis with reproduction (use Troubleshooter instead)
</Do_Not_Use_When>

<Steps>

## 1. Determine analysis type

Based on the user's request, select one or more:

| Request | Analysis Type | Primary Tool |
|---------|--------------|--------------|
| "architecture analysis", "map the codebase" | Architecture Mapping | get_architecture, search_graph |
| "what breaks if I change X?", "impact analysis" | Impact Analysis | trace_call_path, detect_changes |
| "dependency trace", "who calls X?" | Dependency Tracing | trace_call_path, query_graph |
| "code quality", "dead code", "complexity" | Quality Assessment | search_graph (degree filters) |
| No specific request | Architecture Mapping (default) | get_architecture |

## 2. Ensure codebase is indexed

Check if codebase-memory-mcp has current data:
- Use index_status to check freshness
- If stale or unindexed: run index_repository first
- If recently indexed: proceed directly

## 2b. Check graph health before trusting graph-only conclusions

Before choosing the analysis path, inspect whether the current graph is sufficient
for the requested mode.

- If function/call relationships are sparse or absent:
  - downgrade impact/dependency analysis to file/module scope
  - use `search_code` and LSP/grep fallback
  - report confidence explicitly
- Never present precise caller/callee claims when the graph cannot support them

## 3. Dispatch Analyst

Dispatch the Analyst agent (forge:analyst) with the selected analysis type:

```
Agent(subagent_type="forge:analyst", prompt="Run {analysis_type} on {target}")
```

The Analyst uses codebase-memory-mcp tools:
- **get_architecture** — module structure, layer boundaries
- **search_graph** — find functions, classes, routes and relationships
- **trace_call_path** — call chains, dependency trees, impact radius
- **query_graph** — custom Cypher queries for complex patterns
- **detect_changes** — what changed and blast radius
- **search_code / LSP fallback** — when graph fidelity is too weak for symbol-level confidence

## 4. Present results

Format the Analyst's output based on type:

**Architecture Report:**
```
## Module Map
{modules with inbound/outbound dependency counts}
## Coupling Hotspots
{high-coupling pairs}
## Patterns
{architectural patterns detected}
```

**Impact Report:**
```
## Change: {target}
## Direct Impact: {files/functions}
## Transitive Impact: {callers of callers}
## Risk: isolated | local | systemic
```

**Dependency Report:**
```
## {function/module}
## Callers (who depends on this): {list}
## Callees (what this depends on): {list}
## Call depth: {N levels}
```

**Quality Report:**
```
## Dead Code: {unused exports/functions}
## Complexity Hotspots: {ranked}
## Refactor Candidates: {effort vs impact}
```

## 5. Feed into active phase (optional)

If a Forge project is active (.forge/state.json exists):
- Save analysis to `.forge/design/codebase-analysis.md`
- Record analysis metadata via:
  `node scripts/forge-lane-runtime.mjs record-analysis --type <kind> --target <target> --artifact .forge/design/codebase-analysis.md --graph-health <health> --confidence <level> --risk <level> --summary "<summary>"`
- CTO, Lead, or Troubleshooter can reference this in their phase work
- Use `node scripts/forge-lane-runtime.mjs analysis-status --json` when checking freshness before design/develop/fix

</Steps>

<Tool_Usage>
- Use Agent tool to dispatch forge:analyst
- Analyst uses codebase-memory-mcp tools internally
- Results saved to .forge/design/codebase-analysis.md if Forge project is active
- For quick queries, Analyst can run without full Forge project context
</Tool_Usage>

<State_Changes>
- If Forge project active: updates .forge/design/codebase-analysis.md
- No phase transition — this is an on-demand utility, not a phase gate
</State_Changes>
