---
name: sequential-thinking
description: Apply step-by-step analysis for complex problems with revision capability. Use for multi-step reasoning, hypothesis verification, adaptive planning, problem decomposition, architecture decisions, debugging complex issues.
---

# Sequential Thinking

Structured problem-solving via manageable, reflective thought sequences with dynamic adjustment.

## When to Apply

- Complex problem decomposition
- Adaptive planning with revision capability
- Analysis needing course correction
- Problems with unclear/emerging scope
- Multi-step solutions requiring context
- Hypothesis-driven investigation
- Architecture decisions
- Debugging complex interactions

## Core Process

### 1. Start with Loose Estimate

```
Thought 1/5: [Initial analysis]
```

Adjust dynamically as understanding evolves.

### 2. Structure Each Thought

- Build on previous context explicitly
- Address one aspect per thought
- State assumptions, uncertainties, realizations
- Signal what next thought should address

### 3. Dynamic Adjustment

| Situation | Action |
|-----------|--------|
| More complexity discovered | Expand total (1/5 → 1/8) |
| Simpler than expected | Contract total (1/5 → 1/3) |
| New insight invalidates previous | Mark as REVISION |
| Multiple valid approaches | BRANCH and compare |

### 4. Revision Pattern

When new insight invalidates previous thinking:

```
Thought 5/8 [REVISION of Thought 2]:
- Original: [What was stated]
- Why revised: [New insight discovered]
- Impact: [What changes downstream]
- Corrected: [New understanding]
```

### 5. Branching Pattern

When multiple approaches are viable:

```
Thought 4/7 [BRANCH A from Thought 2]:
Approach: Use WebSocket for real-time
Pros: Low latency, bidirectional
Cons: Connection management complexity

Thought 4/7 [BRANCH B from Thought 2]:
Approach: Use Server-Sent Events
Pros: Simpler, HTTP-based
Cons: Unidirectional only

Thought 5/7 [CONVERGENCE]:
Decision: Branch A (WebSocket) because bidirectional needed
```

### 6. Hypothesis Testing

```
Thought 6/9 [HYPOTHESIS]:
The bug is caused by race condition in state update
Evidence: Intermittent failures, timing-dependent
Test: Add mutex lock around state mutation

Thought 7/9 [VERIFICATION]:
Test result: Lock added, ran 100 iterations
Outcome: 0 failures (was 15/100)
Conclusion: Hypothesis CONFIRMED
```

### 7. Completion

Mark final thought: `Thought N/N [FINAL]`

Complete when:
- Solution verified
- All critical aspects addressed
- Confidence achieved
- No outstanding uncertainties

## Application Modes

**Explicit Mode**: Use visible thought markers when:
- Complexity warrants visible reasoning
- User requests breakdown
- Debugging complex issues
- Architecture decisions

```
Thought 1/4: Analyzing authentication flow...
Thought 2/4: Identified gap in token refresh...
Thought 3/4 [HYPOTHESIS]: Race condition in refresh...
Thought 4/4 [FINAL]: Solution: mutex + retry logic
```

**Implicit Mode**: Apply methodology internally for:
- Routine problem-solving
- Simple decisions
- Well-understood patterns

## Example: Debugging Memory Leak

```
Thought 1/5: Initial symptoms
- Memory grows over time (100MB → 2GB in 24h)
- No obvious patterns in user actions
- Garbage collection running normally

Thought 2/5: Gathering evidence
- Heap snapshot shows growing array of DOM nodes
- Nodes are detached but referenced
- Event listeners attached to each

Thought 3/5 [HYPOTHESIS]:
Event listeners preventing GC of removed DOM nodes
Test: Check removeEventListener calls

Thought 4/5 [VERIFICATION]:
Found: addEventListener without corresponding remove
Location: useEffect cleanup missing in Modal component
Confirmed: Memory stable after fix

Thought 5/5 [FINAL]:
Root cause: Missing cleanup in useEffect
Fix: Add return () => element.removeEventListener(...)
Prevention: ESLint rule for exhaustive-deps
```

## Example: Architecture Decision

```
Thought 1/6: Requirements analysis
- 10K concurrent users
- Real-time updates needed
- Mobile + Web clients

Thought 2/6 [BRANCH A]: Monolithic approach
- Single deployment
- Simpler initially
- Scaling challenges at 10K+

Thought 2/6 [BRANCH B]: Microservices
- Independent scaling
- Complex deployment
- Better for real-time

Thought 3/6 [CONVERGENCE]:
Decision: Start monolithic, prepare for extraction
Rationale: YAGNI, but design with boundaries

Thought 4/6 [REVISION of Thought 3]:
New info: Team has K8s experience
Revised: Microservices viable from start
Impact: Architecture changes, timeline same

Thought 5/6: Final architecture
- API Gateway → Auth Service → Core Service
- WebSocket Service for real-time
- Shared database initially

Thought 6/6 [FINAL]:
Recommended: Microservices with shared DB
Key decisions documented
Trade-offs explained
Next: Create detailed design doc
```

## Integration with Other Skills

- Use with `systematic-debugging` for complex bugs
- Use with `test-driven-development` for test strategy
- Use with `visual-preview` to generate diagrams
