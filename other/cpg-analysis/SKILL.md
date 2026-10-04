---
name: cpg-analysis
description: Deep code property graph analysis with Joern CPG (AST+CFG+PDG) and CodeQL for control flow, data flow, taint analysis, and security auditing
when-to-use: "When deep code analysis is needed — control flow, data flow, taint tracking, or security auditing"
user-invocable: true
effort: high
---

# CPG Analysis Skill


**Purpose:** Deep code analysis beyond AST. Use Joern for full Code
Property Graph (control flow, data flow, program dependencies) and CodeQL
for interprocedural taint analysis and vulnerability detection.

**These are opt-in tools.** They require Docker/JVM (Joern) or CodeQL CLI.
Use codebase-memory-mcp (Tier 1, always-on) for everyday navigation.
Use these for deep analysis when Tier 1 is not enough.

```
┌────────────────────────────────────────────────────────────────┐
│  CODE PROPERTY GRAPH = AST + CFG + CDG + DDG + PDG             │
│  ─────────────────────────────────────────────────────────────│
│  AST  = Abstract Syntax Tree (structure)                       │
│  CFG  = Control Flow Graph (execution paths)                   │
│  CDG  = Control Dependency Graph (conditional dependencies)    │
│  DDG  = Data Dependency Graph (data flow between statements)   │
│  PDG  = Program Dependency Graph (CDG + DDG combined)          │
│                                                                │
│  Tier 2 (Joern): Full CPG with 40+ query tools                │
│  Tier 3 (CodeQL): Interprocedural taint + security queries     │
└────────────────────────────────────────────────────────────────┘
```

---

## Tier Selection Guide

```
Simple symbol lookup, dependency trace, blast radius?
  → Tier 1: codebase-memory-mcp (always on, sub-ms)

Control flow paths, data flow, dead code, complex refactoring?
  → Tier 2: Joern CPG (on-demand, seconds)

Security audit, taint analysis, vulnerability detection?
  → Tier 3: CodeQL (on-demand, seconds to minutes)

Full security review before release?
  → All three tiers in sequence
```

---

## Tier 2: Joern CPG (CodeBadger MCP)

### When to Use Joern

| Scenario | Why Joern | Tier 1 Can't Do This |
|----------|-----------|---------------------|
| Trace data flow through functions | Full DDG traversal | Tier 1 has no data flow |
| Understanding control flow paths | CFG analysis with branch conditions | Tier 1 has no CFG |
| Finding dead/unreachable code | PDG reachability analysis | Tier 1 only detects unused exports |
| Complex refactoring impact | Cross-function dependency chains | Tier 1 limited to call graph |
| Auditing third-party library usage | Deep call chain traversal | Tier 1 stops at import boundary |
| Understanding exception flow | CFG includes throw/catch paths | Tier 1 ignores exceptions |

### Key MCP Tools (Joern/CodeBadger)

| Tool | Purpose | Example Query |
|------|---------|---------------|
| `generate_cpg` | Build CPG for project | First-time setup or after major changes |
| `get_cpg_status` | Check CPG build status | Verify CPG is ready before querying |
| `run_cpgql_query` | Run arbitrary CPGQL queries | `cpg.method("login").callOut.code.l` |
| `get_cpgql_syntax_help` | Query language reference | When unsure about query syntax |
| `get_cfg` | Control flow graph for a method | Understand execution paths in a function |
| `list_methods` | List all methods in project | Overview of available functions |
| `get_method_source` | Get source code of a method | Read specific function source |
| `list_calls` | List calls from/to a method | Caller/callee analysis |
| `get_call_graph` | Full call graph visualization | Understand call chains |
| `get_type_definition` | Type/class definitions | Understand type hierarchy |

### Supported Languages (Joern)

Java, Scala, C/C++, Python, JavaScript, TypeScript, PHP, Ruby, Go,
Kotlin, Swift, Lua

**Not supported:** Rust (use CodeQL for Rust)

### MCP Configuration (Joern)

```json
{
  "mcpServers": {
    "codebadger": {
      "url": "http://localhost:4242/mcp",
      "type": "http"
    }
  }
}
```

### Prerequisites

- Docker (for Joern backend)
- Python 3.10+ (for MCP server)
- Install: `~/.claude/install-graph-tools.sh --joern`

### Common CPGQL Queries

```scala
// Find all methods that handle user input
cpg.method.where(_.parameter.name(".*input.*|.*request.*")).name.l

// Trace data flow from parameter to return
cpg.method("processPayment").parameter.reachableBy(cpg.method("processPayment").methodReturn).l

// Find methods with high cyclomatic complexity
cpg.method.where(_.controlStructure.size > 10).name.l

// Dead code: methods with no callers
cpg.method.where(_.callIn.size == 0).filter(_.name != "main").name.l

// Exception flow: methods that can throw but callers don't catch
cpg.method.where(_.ast.isThrow.size > 0).callIn.method.filter(_.ast.isTry.size == 0).name.l
```

---

## Tier 3: CodeQL

### When to Use CodeQL

| Scenario | Why CodeQL | Other Tiers Can't Do This |
|----------|-----------|--------------------------|
| Security audit before release | Interprocedural taint analysis | Joern has basic taint, CodeQL is deeper |
| Reviewing auth/payment code | Data flow from source to sink | Cross-function, cross-file taint |
| PR security review | Targeted vulnerability scan | Pre-built OWASP query packs |
| Compliance checking | CWE/OWASP pattern matching | Curated security query suites |
| Rust security analysis | Full Rust support | Joern doesn't support Rust |

### Key MCP Tools (CodeQL)

| Tool | Purpose |
|------|---------|
| `run_query` | Execute a CodeQL query against the database |
| `find_definitions` | Locate symbol definitions |
| `find_references` | Find all references to a symbol |
| `get_results` | Parse BQRS (Binary Query Result Sets) |

### Supported Languages (CodeQL)

C/C++, C#, Go, Java, Kotlin, JavaScript, TypeScript, Python, Ruby,
Swift, **Rust**

### MCP Configuration (CodeQL)

```json
{
  "mcpServers": {
    "codeql": {
      "command": "codeql-mcp",
      "args": ["--database", ".code-graph/codeql-db"]
    }
  }
}
```

### Prerequisites

- CodeQL CLI (`brew install codeql` on macOS)
- Install: `~/.claude/install-graph-tools.sh --codeql`

### Common CodeQL Patterns

```ql
// SQL injection: user input flows to SQL query
import python
from DataFlow::PathNode source, DataFlow::PathNode sink
where TaintTracking::hasFlowPath(source, sink)
  and source instanceof RemoteFlowSource
  and sink instanceof SqlExecution
select sink, source, sink, "SQL injection from $@.", source, "user input"

// Unvalidated redirect
from DataFlow::PathNode source, DataFlow::PathNode sink
where source instanceof RemoteFlowSource
  and sink instanceof RedirectSink
select sink, "Unvalidated redirect from user input"
```

---

## Combined Workflow: Deep Analysis

When performing security review or complex refactoring, use all tiers:

```
1. SCOPE       → Tier 1: detect_changes / get_architecture
                 Identify files and modules in scope

2. STRUCTURE   → Tier 1: search_graph / trace_call_path
                 Map the call graph and dependencies

3. FLOW        → Tier 2: get_cfg / run_cpgql_query
                 Analyze control flow and data flow paths

4. SECURITY    → Tier 3: run_query with taint analysis
                 Check for vulnerabilities in data paths

5. REPORT      → Combine findings from all tiers
                 Prioritize: Critical > High > Medium > Low
```

---

## Anti-Patterns

| Anti-Pattern | Do This Instead |
|-------------|-----------------|
| Using Joern/CodeQL for simple symbol lookup | Use Tier 1 `search_graph` (sub-ms vs seconds) |
| Running full CPG build on every commit | Build CPG on-demand; use Tier 1 for continuous monitoring |
| Querying Joern without checking `get_cpg_status` | Always verify CPG is built and current before querying |
| Running CodeQL without a specific security question | Have a hypothesis first; CodeQL queries are expensive |
| Ignoring Tier 1 blast radius before deep analysis | Always scope with Tier 1 first, then go deep on flagged areas |
| Using CodeQL for non-security structural queries | Use Joern CPGQL for structural/flow queries; CodeQL for security |
