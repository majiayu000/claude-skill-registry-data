---
name: darwin-godwin-machine
description: |
  Hybrid cognitive architecture combining Darwinian evolution with Gödel Machine self-improvement for maximum reasoning power. Use for: complex coding problems, multi-step reasoning, architecture design, debugging hard problems, any task requiring exhaustive solution exploration with formal verification. Activates when user needs "powerful reasoning", "best possible solution", "explore all options", or faces problems where first-attempt solutions typically fail.
---

# Darwin-Gödel Machine

A cognitive architecture that evolves populations of solutions while formally verifying improvements before self-modification.

## Core Philosophy

**Darwin**: Generate diverse solution populations → Apply selection pressure → Evolve toward optimum
**Gödel**: Verify improvements formally before accepting → Enable recursive self-improvement → Prove modifications beneficial

**Combined**: Explore solution space evolutionarily, but only commit changes with verification proofs.

---

## THE EXECUTION LOOP

Every problem runs this loop. No exceptions. Depth scales with complexity.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: DECOMPOSE                                                         │
│  ├─ Parse the problem into atomic sub-problems                              │
│  ├─ Identify constraints, success criteria, edge cases                      │
│  ├─ Define fitness function: What makes a solution "better"?                │
│  └─ Estimate complexity class → determines population size & generations    │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 2: GENESIS (Population Initialization)                               │
│  ├─ Generate N diverse initial solutions (N = 3-7 based on complexity)      │
│  ├─ Ensure diversity: different algorithms, paradigms, trade-offs           │
│  ├─ Each solution must be complete and executable (no stubs)                │
│  └─ Tag each with: approach_type, expected_strengths, expected_weaknesses   │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: EVALUATE (Fitness Assessment)                                     │
│  ├─ Score each solution against fitness function (1-100)                    │
│  ├─ Test against edge cases and adversarial inputs                          │
│  ├─ Measure: correctness, efficiency, readability, robustness               │
│  └─ Rank population by composite fitness score                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 4: EVOLVE (Selection + Mutation + Crossover)                         │
│  ├─ SELECT: Keep top 50% of population                                      │
│  ├─ MUTATE: Apply mutation operators to survivors (see §Mutations)          │
│  ├─ CROSSOVER: Combine strengths of top 2 solutions into hybrid             │
│  └─ Generate new candidates to restore population size                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 5: VERIFY (Gödel Proof Gate)                                         │
│  ├─ For each evolved solution, PROVE improvement over parent                │
│  ├─ Proof types: logical deduction, test coverage, complexity analysis      │
│  ├─ REJECT any mutation that cannot be formally justified                   │
│  └─ Only verified improvements pass to next generation                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 6: CONVERGE (Termination Check)                                      │
│  ├─ If best solution meets success criteria → DELIVER                       │
│  ├─ If fitness plateau (no improvement in 2 generations) → DELIVER best     │
│  ├─ If generation limit reached → DELIVER best with caveats                 │
│  └─ Else → Return to PHASE 4 with evolved population                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 7: REFLECT (Mandatory Self-Reflection)                               │
│  ├─ SOLUTION REFLECTION: Why did winner win? What trait was decisive?       │
│  ├─ PROCESS REFLECTION: Did I explore right space? What did I miss?         │
│  ├─ ASSUMPTION AUDIT: List all assumptions, mark validated/invalidated      │
│  ├─ MUTATION ANALYSIS: Which mutations helped? Which wasted cycles?         │
│  ├─ PROOF QUALITY: Were proofs rigorous or hand-wavy?                       │
│  ├─ FAILURE ANALYSIS: What would have caught mistakes earlier?              │
│  └─ Score reasoning quality 1-10, justify score                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 8: META-IMPROVE (Recursive Self-Improvement)                         │
│  ├─ Extract: What lessons apply to future problems?                         │
│  ├─ Propose: Concrete process improvements (not vague)                      │
│  ├─ Verify: Would proposed improvement actually help?                       │
│  ├─ If verified → Add to ACTIVE_LESSONS for this conversation               │
│  └─ Apply ACTIVE_LESSONS at start of next problem in conversation           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## COMPLEXITY SCALING

| Problem Type | Population Size | Max Generations | Mutation Rate |
|--------------|-----------------|-----------------|---------------|
| Simple (one-liner fix) | 3 | 2 | Low |
| Medium (single function) | 5 | 3 | Medium |
| Complex (module/feature) | 7 | 5 | High |
| Architecture (system design) | 7 | 7 | High + Crossover |

---

## FITNESS FUNCTION TEMPLATE

Define before generating solutions:

```
FITNESS(solution) = weighted_sum(
    CORRECTNESS:   Does it produce correct output for all inputs?      (weight: 0.40)
    ROBUSTNESS:    Does it handle edge cases and failures gracefully?  (weight: 0.25)
    EFFICIENCY:    Time/space complexity relative to optimal?          (weight: 0.15)
    READABILITY:   Can a mid-level dev understand it in 30 seconds?    (weight: 0.10)
    EXTENSIBILITY: How hard to modify for likely future requirements?  (weight: 0.10)
)
```

Adjust weights based on problem priorities. User can override.

---

## MUTATION OPERATORS

Apply during EVOLVE phase to create variants:

### Code Mutations
| Operator | Description | When to Apply |
|----------|-------------|---------------|
| SIMPLIFY | Remove unnecessary complexity | When solution is >20 lines |
| GENERALIZE | Make specific code more abstract | When pattern appears 2+ times |
| SPECIALIZE | Optimize for specific use case | When generality hurts performance |
| EXTRACT | Pull out reusable component | When code can benefit others |
| INLINE | Remove unnecessary abstraction | When abstraction adds no value |
| PARALLELIZE | Add concurrency | When independent operations exist |
| MEMOIZE | Cache repeated computations | When same inputs recur |
| GUARD | Add defensive checks | When edge cases discovered |

### Architecture Mutations
| Operator | Description | When to Apply |
|----------|-------------|---------------|
| SPLIT | Decompose into smaller units | When module does too much |
| MERGE | Combine related components | When separation adds overhead |
| LAYER | Add abstraction layer | When coupling is too tight |
| FLATTEN | Remove unnecessary layers | When indirection hurts clarity |
| ASYNC | Convert to async processing | When blocking is unnecessary |
| CACHE | Add caching layer | When repeated expensive operations |
| QUEUE | Add message queue | When decoupling needed |
| RETRY | Add retry logic | When transient failures possible |

---

## ASSUMPTION TRACKING

Track assumptions throughout the ENTIRE loop, not just in reflection.

### Assumption Log Format

```
ASSUMPTION LOG:
┌─────┬─────────────────────────────┬─────────┬──────────┬───────────┐
│ ID  │ Assumption                  │ Phase   │ Risk     │ Status    │
├─────┼─────────────────────────────┼─────────┼──────────┼───────────┤
│ A1  │ Input size < 10,000         │ DECOMP  │ Medium   │ UNCHECKED │
│ A2  │ No concurrent modifications │ GENESIS │ High     │ VALIDATED │
│ A3  │ API returns JSON            │ GENESIS │ Low      │ UNCHECKED │
│ A4  │ O(n²) acceptable for N<100  │ EVOLVE  │ Medium   │ VALIDATED │
└─────┴─────────────────────────────┴─────────┴──────────┴───────────┘
```

### Assumption Risk Levels

| Risk | Definition | Action Required |
|------|------------|-----------------|
| **HIGH** | If wrong, solution is fundamentally broken | MUST validate before delivery |
| **MEDIUM** | If wrong, solution degrades but works | SHOULD validate, document if not |
| **LOW** | If wrong, minor impact | Document, validate if easy |

**RULE: HIGH risk + Weak validation = STOP. Get stronger validation or flag uncertainty.**

---

## REFLECTION OUTPUT FORMAT

```
### REFLECTION (Phase 7)

#### Solution Analysis
- Winner: [ID] 
- Decisive trait: [what made it win]
- Emerged at: [Genesis / Generation N via mutation X]
- Biggest weakness: [trade-off accepted]

#### Process Analysis  
- Approaches NOT tried: [list 2-3 with reasons]
- Highest effort area: [phase/activity] — Justified: [yes/no]
- If starting over: [what would change]

#### Assumption Audit
| Assumption | Risk | Status | Evidence |
|------------|------|--------|----------|
| ... | ... | ... | ... |

Unvalidated HIGH-risk assumptions: [count] ← MUST BE 0

#### Self-Score: [1-10]
Justification: [why this score]
```

---

## QUICK-START HEURISTICS

For rapid application without full formalism:

**When time-constrained:**
1. Generate 3 solutions (diverse approaches)
2. Score each on correctness + robustness only
3. Mutate top 1 solution once
4. Verify mutation improves fitness
5. Deliver best

**When quality is paramount:**
1. Full 7-solution population
2. 5+ generations with crossover
3. All proof types required
4. Meta-improvement phase mandatory

---

## ADVERSARIAL SELF-CHECK

Before delivering final solution, ask:

1. "What input would break this?"
2. "What assumption am I making that might be wrong?"
3. "If I had to attack this code, how would I?"
4. "What would a senior engineer critique?"
5. "Does the simplest version of this work just as well?"

If any answer reveals a flaw → one more evolution cycle.

---

## PROJECT-SPECIFIC CONTEXT

When working on this Twilio Bulk Lookup codebase, consider these fitness criteria:

**For Sidekiq Jobs:**
- Idempotency (can safely retry)
- Rate limit handling
- Error classification (retryable vs fatal)
- Memory efficiency for large batches

**For API Integrations:**
- Graceful degradation when API unavailable
- Credential security
- Response caching where appropriate
- Webhook reliability

**For Rails Models:**
- Query efficiency (N+1 prevention)
- Validation completeness
- Scope composability
- Serialization safety
