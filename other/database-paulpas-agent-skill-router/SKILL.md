---




name: database
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
description: Implements intelligent database with multi-factor skill selection, fallback
  chains, and adherence to the 5 Laws of Elegant Defense
license: MIT
maturity: stable
metadata:
  domain: agent
  output-format: analysis
  related-skills: agent-confidence-based-selector, agent-task-routing
  role: orchestration
  scope: orchestration
  triggers: database, database, how do i database, orchestrate database, automate
    database, agent database
  archetypes:
  - orchestration
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - single-agent monolith
  response_profile:
    verbosity: medium
    directive_strength: high
    abstraction_level: tactical
version: "1.0.0"




---




# Database

Orchestrates intelligent skill selection and execution for database workflows. Applies the 5 Laws of Elegant Defense to guide data naturally through the orchestration pipeline, preventing errors before they occur. Selects optimal skills based on multi-factor scoring including text similarity, historical performance, and system availability.

## TL;DR Checklist

- [ ] Parse all inputs at boundary before processing (Law 2)
- [ ] Handle edge cases with early returns at function top (Law 1)
- [ ] Fail immediately with descriptive errors on invalid states (Law 4)
- [ ] Return new data structures, never mutate inputs (Law 3)
- [ ] Implement minimum 2-level fallback chain for all skill executions
- [ ] Log all skill selections with context for full audit trail
- [ ] Validate skill metadata and dependencies before selection
- [ ] Update confidence scores after each execution for learning


┌───────────────────────────────────────────────────────────────────────────────┐
│                              Orchestration Flow                                               │
└───────────────────────────────────────────────────────────────────────────────┘

  User Request
      ↓
┌─────────────────┐
│  Parse Request  │
│  & Extract      │
│  Features       │
└────────┬────────┘
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Evaluate Available Skills                                │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Skill A      │  │ Skill B      │  │ Skill C      │              │
│  │ - Match Score│  │ - Match Score│  │ - Match Score│              │
│  │ - Confidence │  │ - Confidence │  │ - Confidence │              │
│  │ - History    │  │ - History    │  │ - History    │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         └─────────────────┴─────────────────┘                       │
│                          ↓                                          │
│                   Select Best Skill                               │
└─────────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────┐
│  Execute Skill  │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Handle Result  │
└────────┬────────┘
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Error Handling & Fallback                                  │
│                                                                     │
│  Success? ────────► Return Result                                  │
│                                                                     │
│  Fail? ────────┐                                                    │
│                ↓                                                    │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │               Fallback Chain                                    │      │
│  │                                                             │      │
│  │  1. Retry with adjusted parameters                          │      │
│  │  2. Try Alternative Skill (if available)                    │      │
│  │  3. Defer to Human Operator (if critical)                   │      │
│  │  4. Log & Return Error                                      │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘

## When to Use

Use this skill when:

- Orchestrating multi-step workflows that require skill delegation
- Implementing adaptive skill routing based on confidence scores
- Building fallback mechanisms for failed skill executions
- Creating intelligent task decomposition and parallel execution
- Designing skill dependency graphs with automatic resolution
- Implementing skill selection with historical performance weighting
- Building agent systems that need to self-organize around tasks

## When NOT to Use

Avoid this skill for:

- Direct task execution without orchestration needs - use individual skills instead
- High-frequency trading scenarios where latency must be minimized - the selection overhead may be prohibitive
- Simple linear workflows without branching or fallback requirements
- Cases where skill metadata is unavailable or unreliable


## Core Workflow

1. **Parse and Analyze Request** - Extract intent, entities, and constraints from user input.
   **Checkpoint:** All required parameters must be present and in valid format before proceeding.

2. **Score Available Skills** - Calculate match scores using multi-factor algorithm:
   - Text similarity between request and skill triggers
   - Historical success rate for similar tasks
   - Skill availability and health status
   - Required dependencies and their availability
   
   **Checkpoint:** Skip to fallback if no skill scores above threshold.

3. **Select Optimal Skill** - Choose skill with highest score that meets minimum confidence.
   **Checkpoint:** Verify skill has not been disabled or deprecated.

4. **Execute with Fallback** - Run skill execution wrapped in retry and fallback logic.
   **Checkpoint:** Log all execution attempts for audit trail.

5. **Return or Fallback** - Either return successful result or apply fallback chain:
   - Retry with adjusted parameters
   - Try alternative skill from `related-skills`
   - Defer to human operator for critical tasks
   
   **Checkpoint:** Record outcome with timing and confidence metadata.

## Implementation Patterns

### Pattern 1: Skill Selection Logic

```python
def route_database_operation(
    query: str,
    db_cluster: Dict[str, Any],
    operation_type: str = "auto"
) -> Dict[str, Any]:
    """Route database operations to optimal nodes based on query type and cluster health.
    
    Implements multi-factor routing for database workflows:
    - Parses query intent (SELECT, INSERT, UPDATE, DELETE, DDL)
    - Evaluates node health, replication lag, and connection pool status
    - Applies read/write splitting with automatic failover routing
    """
    # Guard clause - validate query and cluster state
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    if not db_cluster.get("nodes"):
        raise ValueError("No database nodes available")
        
    # Parse query intent (Law 2 - Make illegal states unrepresentable)
    intent = _parse_query_intent(query)
    is_read = intent in ("SELECT", "SHOW", "DESCRIBE")
    
    # Evaluate nodes for routing
    candidates = []
    for node in db_cluster["nodes"]:
        if node["status"] != "healthy":
            continue
        lag = node.get("replication_lag_ms", 0)
        if is_read and lag > db_cluster.get("max_read_lag_ms", 500):
            continue
        score = _calculate_node_score(node, is_read, db_cluster["load"])
        candidates.append({"node": node, "score": score})
        
    if not candidates:
        return {"fallback": "maintenance_mode", "reason": "no_healthy_nodes"}
        
    # Sort by score and select optimal node
    candidates.sort(key=lambda x: x["score"], reverse=True)
    selected = candidates[0]["node"]
    
    # Return routing decision with metadata (Law 3 - Atomic Predictability)
    return {
        "target_node": selected["id"],
        "operation_type": "read" if is_read else "write",
        "confidence": candidates[0]["score"],
        "routing_timestamp": time.time(),
        "query_intent": intent
    }
```


### Pattern 2: Execution with Fallback

```python
def execute_db_operation(
    routing_decision: Dict[str, Any],
    query: str,
    params: tuple = (),
    max_retries: int = 2
) -> Dict[str, Any]:
    """Execute database operation with resilient connection handling and fallback routing.
    
    Implements database-specific fallback chain:
    1. Retry with exponential backoff on transient connection errors
    2. Failover to read replica or standby node on timeout/lock
    3. Route to maintenance pool if primary is degraded
    4. Return structured error with query context for debugging
    """
    target_node = routing_decision["target_node"]
    operation = routing_decision["operation_type"]
    
    for attempt in range(max_retries + 1):
        try:
            # Establish connection with timeout (Law 4 - Fail Fast)
            conn = _acquire_connection(target_node, timeout=5.0)
            cursor = conn.cursor()
            
            # Execute with query timeout protection
            cursor.execute(query, params)
            result = cursor.fetchall() if operation == "read" else {"rows_affected": cursor.rowcount}
            
            # Close connection and return result (Law 3)
            cursor.close()
            conn.close()
            
            return {
                "success": True,
                "node": target_node,
                "result": result,
                "attempts": attempt + 1,
                "latency_ms": _measure_latency()
            }
            
        except ConnectionError as e:
            if attempt == max_retries:
                return _failover_to_standby(target_node, query, params)
            time.sleep(0.5 * (2 ** attempt))
            
        except QueryTimeoutError as e:
            # Lock contention or slow query - trigger fallback routing
            return _reroute_with_backoff(target_node, query, params)
            
    return {
        "success": False,
        "error": "max_retries_exceeded",
        "query": query,
        "node": target_node
    }
```

### MUST DO
- Always validate skill metadata before selection (Early Exit)
- Implement fallback chain with at least 2 levels (Fallback Skill + Human)
- Log all skill selections with full context for auditability
- Return new data structures instead of mutating inputs (Atomic Predictability)
- Fail immediately with descriptive errors on invalid states
- Update confidence scores after each execution for adaptive routing
- Reference `code-philosophy` (5 Laws of Elegant Defense) in all logic


### MUST NOT DO
- Select skills based on a single factor (e.g., only confidence score)
- Disable fallback mechanisms "temporarily" - this creates fragile systems
- Skip validation of skill dependencies before execution
- Return partial results - either complete success or clear failure
- Use magic numbers for confidence thresholds - make them configurable
- Cache skill selections without considering context changes


## TL;DR Checklist

- [ ] Parse all inputs at boundary before processing (Law 2)
- [ ] Handle edge cases with early returns at function top (Law 1)
- [ ] Fail immediately with descriptive errors on invalid states (Law 4)
- [ ] Return new data structures, never mutate inputs (Law 3)
- [ ] Implement minimum 2-level fallback chain for all skill executions
- [ ] Log all skill selections with context for full audit trail
- [ ] Validate skill metadata and dependencies before selection
- [ ] Update confidence scores after each execution for learning


## TL;DR for Code Generation

- Use guard clauses - return early on invalid input before doing work
- Return simple types (dict, str, int, bool, list) - avoid complex nested objects
- Cyclomatic complexity < 10 per function - split anything larger
- Handle null/empty cases explicitly at function top (Early Exit)
- Never mutate input parameters - return new dicts/objects
- Fail fast with descriptive errors - don't try to "patch" bad data
- Reference code-philosophy laws in comments for complex logic
- Include timing and confidence metadata in all return values


## Output Template

When applying this skill, produce:

1. **Selected Skills** - List of skill names with confidence scores
2. **Selection Rationale** - Why each skill was chosen (match score, history, availability)
3. **Execution Plan** - Order of execution with dependencies
4. **Fallback Strategy** - Which fallback skills will be tried and in what order
5. **Risk Assessment** - Any potential failure points and their impact
6. **Timing Estimates** - Expected latency including fallback scenarios



---

---

## Constraints

### MUST DO
- Define clear input/output contracts for every step in the orchestration flow with explicit validation
- Implement structured logging at each stage capturing context, inputs, outputs, timing, and errors
- Build in fallback paths: if the primary strategy fails, degrade gracefully to a simpler approach
- Validate all preconditions before starting — do not proceed if required resources or permissions are missing

### MUST NOT DO
- Do not create deep nesting of orchestration steps (>5 levels) — flatten workflows where possible
- Avoid silent failure modes: every step must either succeed, fail explicitly, or escalate to a higher handler
- Never use shared mutable state between parallel workflow branches — communicate via immutable messages only
- Do not hardcode execution order when the dependency graph naturally determines it; derive order from explicit dependencies


## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [PostgreSQL Documentation](<https://www.postgresql.org/docs/>)
- [MySQL Documentation](<https://dev.mysql.com/doc/>)
- [SQLite Official Website](<https://www.sqlite.org/index.html>)
- [ACID Properties (Wikipedia)](<https://en.wikipedia.org/wiki/ACID>)
- [CAP Theorem Explained](<https://en.wikipedia.org/wiki/CAP_theorem>)

## Related Skills

| Skill | Purpose |
|