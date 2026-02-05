---
name: langgraph-validator
description: Validates LangGraph implementations for correctness, consistency, and integration readiness. Use this skill when implementing, reviewing, or debugging any LangGraph code - agents, nodes, subgraphs, state schemas, or graph compositions. Prevents common LangGraph failures including orphaned nodes, state key mismatches, broken conditional edges, and integration incompatibilities. Triggers on LangGraph development tasks, code reviews, or when debugging graph execution issues.
---

# LangGraph Implementation Validator

Prevents the #1 cause of LangGraph failures: graphs that look correct but fail at runtime due to state mismatches, missing edges, or integration incompatibilities.

## Core Failure This Skill Prevents

```
Developer: Graph runs but agent output is empty
Debug: 3 hours later... state key was "messages" in node A, "message" in node B
```

```
Developer: Graph hangs indefinitely  
Debug: Conditional edge returns "continue" but no edge defined for that route
```

This skill catches these issues before runtime.

## The Five Validation Protocols

### 1. Graph Structure Validation (MANDATORY)

Before considering any LangGraph implementation complete, validate structure:

```markdown
## Graph Structure Validation

### Node Inventory
- [ ] All nodes listed: [node1, node2, ...]
- [ ] Entry point defined: `graph.set_entry_point("node_name")`
- [ ] Finish point(s) defined: `END` reachable from all paths

### Edge Completeness  
- [ ] Every node has outgoing edge (except END)
- [ ] Every node (except entry) has incoming edge
- [ ] No orphaned nodes (unreachable from entry)

### Conditional Edge Validation
For each conditional edge:
- [ ] `path_map` covers ALL possible return values from condition function
- [ ] Default/fallback route defined for unexpected values
- [ ] Condition function return type matches path_map keys exactly

### Cycle Detection
- [ ] Intentional cycles documented with exit condition
- [ ] No unintentional infinite loops
- [ ] Cycle exit conditions are reachable

**Structure Issues Found**: [list or "None"]
```

### 2. State Schema Validation (MANDATORY)

Validate state consistency across all nodes:

```markdown
## State Schema Validation

### State Definition
```python
class GraphState(TypedDict):
    # List all keys with types
    key1: type1
    key2: type2
```

### Node State Usage Matrix

| Node | Reads | Writes | Reducer Needed |
|------|-------|--------|----------------|
| node_a | key1 | key2 | No |
| node_b | key2 | key1, key3 | key1: Yes |

### Consistency Checks
- [ ] All read keys exist in state schema
- [ ] All written keys exist in state schema
- [ ] Key names are EXACT match (case-sensitive)
- [ ] Types are compatible across read/write
- [ ] Reducers defined for keys written by multiple nodes
- [ ] No nodes write to keys they also read without reducer

### State Flow Verification
For each key:
- [ ] `key1`: Written by [nodes] → Read by [nodes] ✓
- [ ] `key2`: Written by [nodes] → Read by [nodes] ✓

**State Issues Found**: [list or "None"]
```

### 3. Agent-to-Spec Compliance Validation

When implementing from a spec (like TiC agent specs):

```markdown
## Spec Compliance Validation

### Spec Reference: [Agent Name]

### Responsibility Coverage
| Spec Responsibility | Implementation | Status |
|---------------------|----------------|--------|
| "Parse TOC JSON structure" | `parse_toc()` in node | ✓ |
| "Classify plans by type" | `classify_plan()` tool | ✓ |
| "Estimate processing requirements" | NOT IMPLEMENTED | ⚠️ |

### Input/Output Matching
**Spec Inputs:**
- TOC files from Download Agent → Mapped to: `state["toc_files"]` ✓
- Payer-specific TOC expectations → Mapped to: ??? ⚠️

**Spec Outputs:**
- Parsed plan catalog → Produced by: `state["plans"]` ✓
- Prioritized file list → Produced by: `state["priority_list"]` ✓

### Model Assignment
- Spec: GPT-OSS-20B
- Implementation: `ChatOllama(model="gpt-oss-20b")` ✓

### CLI Command Mapping
- Spec: `tic-agent toc-expert parse --file <path>`
- Implementation: Entry point exists? ✓

**Compliance Issues Found**: [list or "None"]
```

### 4. Integration Validation

Validate that components work together:

```markdown
## Integration Validation

### Subgraph Composition
For each subgraph:
- [ ] Input state keys match parent graph output
- [ ] Output state keys match parent graph expectations
- [ ] Entry/exit points properly exposed

### Cross-Agent Data Flow
| Source Agent | Output Key | Target Agent | Input Key | Compatible |
|--------------|------------|--------------|-----------|------------|
| download_agent | raw_files | integrity_checker | files | ✓ Type match |
| schema_expert | validation_result | mrf_expert | schema_status | ⚠️ Key mismatch |

### Shared State Contracts
- [ ] All agents agree on state key names
- [ ] All agents agree on state key types
- [ ] Reducer functions handle multi-writer keys

### Error Propagation
- [ ] Error states flow correctly to escalation
- [ ] Partial failures don't corrupt state
- [ ] Cleanup runs on failure paths

**Integration Issues Found**: [list or "None"]
```

### 5. Runtime Readiness Validation

Verify the graph is ready to execute:

```markdown
## Runtime Readiness Validation

### Dependencies
- [ ] All imported modules available
- [ ] Model endpoints reachable (Ollama/vLLM)
- [ ] Tools have required dependencies

### Configuration
- [ ] Model names match deployed models
- [ ] Timeouts configured appropriately
- [ ] Retry policies defined

### Checkpointing (if using persistence)
- [ ] Checkpointer configured: `SqliteSaver` / `PostgresSaver` / etc.
- [ ] State is serializable (no lambdas, no open files)
- [ ] Resume tested from checkpoint

### Resource Requirements
- [ ] Estimated VRAM per model call
- [ ] Concurrent execution limits defined
- [ ] Rate limiting configured for external APIs

### Observability
- [ ] Logging at node entry/exit
- [ ] Tracing enabled (LangSmith or equivalent)
- [ ] Metrics collection configured

**Readiness Issues Found**: [list or "None"]
```

## Validation Workflow

```
1. RECEIVE LangGraph code/implementation
   ↓
2. VALIDATE graph structure (nodes, edges, entry/exit)
   ↓
3. VALIDATE state schema (keys, types, reducers)
   ↓
4. IF implementing from spec → VALIDATE spec compliance
   ↓
5. IF composing graphs → VALIDATE integration points
   ↓
6. VALIDATE runtime readiness
   ↓
7. REPORT all issues with specific fixes
   ↓
8. VERIFY fixes before marking complete
```

## Common LangGraph Issues Checklist

Use this quick checklist to catch the most frequent problems:

### Graph Definition Issues
```
- [ ] `add_node()` called for every node
- [ ] `add_edge()` or `add_conditional_edges()` for every node
- [ ] `set_entry_point()` called exactly once
- [ ] `END` is reachable from all paths
- [ ] Conditional edge functions return strings matching path_map keys
```

### State Issues
```
- [ ] State class uses TypedDict (not regular dict)
- [ ] Annotated types used for reducer keys: `messages: Annotated[list, add_messages]`
- [ ] No mutable default values in state
- [ ] State keys are strings (not variables that might be None)
- [ ] Node return dicts only contain defined state keys
```

### Tool/Agent Issues
```
- [ ] Tools are bound to model: `model.bind_tools([tool1, tool2])`
- [ ] Tool schemas match expected input types
- [ ] Tool nodes handle ToolMessage correctly
- [ ] Agent executor handles stop conditions
```

### Async Issues
```
- [ ] All async nodes use `async def`
- [ ] Awaits used consistently
- [ ] No mixing sync/async without proper handling
- [ ] Event loop management correct
```

## Anti-Patterns to Flag

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| Key typo | State appears empty | Exact string matching validation |
| Missing edge | Graph hangs | Edge completeness check |
| Wrong condition return | Unexpected path taken | Path_map coverage validation |
| No reducer | State overwritten | Multi-writer analysis |
| Mutable default | State bleeds between runs | State schema review |
| Sync in async | Blocking | Async consistency check |
| Unserializable state | Checkpoint fails | Serialization test |

## Validation Output Format

When reporting validation results:

```markdown
## LangGraph Validation Report

**Graph**: [name/file]
**Validation Date**: [date]
**Status**: ✅ PASS / ⚠️ WARNINGS / ❌ FAIL

### Critical Issues (must fix)
1. **[Issue Type]**: [description]
   - Location: [file:line or node name]
   - Impact: [what breaks]
   - Fix: [specific remediation]

### Warnings (should fix)
1. **[Issue Type]**: [description]
   - Risk: [potential problem]
   - Recommendation: [suggested change]

### Passed Checks
- ✅ Graph structure complete
- ✅ State schema consistent
- ✅ All edges defined
...

### Recommendations
- [Optional improvements]
- [Best practices not followed]
```

## Quick Reference

- **Always validate structure** before testing execution
- **Always validate state schema** when nodes share data
- **Always validate integration** when composing subgraphs
- **Validate spec compliance** when implementing from design docs
- **Check runtime readiness** before deployment
