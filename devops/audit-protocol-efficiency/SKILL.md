---
name: audit-protocol-efficiency
description: Analyze session execution patterns for efficiency improvements (execution time, token usage, quality)
allowed-tools: Read, Write, Bash, Grep, Skill
---

# Audit Protocol Efficiency Skill

**Purpose**: Identify opportunities to improve protocol efficiency by reducing execution time, token usage, and increasing deliverable quality through pattern analysis.

**When to Use**:
- After protocol compliance audit passes (no CRITICAL/HIGH violations)
- To optimize frequently executed workflow patterns
- When identifying bottlenecks in task execution
- For continuous protocol improvement

## MANDATORY PRECONDITION

**Check compliance first**:
```bash
# Run audit-protocol-compliance FIRST
Skill: audit-protocol-compliance

# IF violations contain CRITICAL or HIGH severity:
#   SKIP efficiency audit
#   OUTPUT: {
#     "status": "SKIPPED",
#     "reason": "Major protocol violations must be fixed before efficiency optimization"
#   }
# ELSE:
#   PROCEED with efficiency analysis
```

## Skill Workflow

**Overview**: Parse timeline → Analyze efficiency patterns → Recommend improvements → Quantify impact

### Phase 1: Get Structured Timeline

**Invoke parse-conversation-timeline skill**:
```bash
Skill: parse-conversation-timeline
```

### Phase 2: Analyze Execution Time Opportunities

**Query timeline for sequential operations that could be parallel**:

```bash
# Find sequential Task calls
jq '.timeline[] | select(.type == "tool_use" and .tool.name == "Task")' timeline.json

# Count messages containing Task tools
# IF Task tools spread across >1 message for same purpose:
#   → Parallelization opportunity

# Example: 3 separate messages for architect, quality, style
# → Should be single message with 3 parallel Task calls
# → Savings: (3 - 1) × avg_message_tokens
```

**Detect redundant verifications**:
```bash
# Find duplicate git status checks
jq '.timeline[] | select(.tool.name == "Bash" and (.tool.input.command | contains("git status")))' timeline.json

# Count occurrences
# IF > 3 git status calls in same state:
#   → Redundancy opportunity
```

**Identify late error detection**:
```bash
# Find validation after all work done
# Pattern: Multiple file creations followed by single checkstyle check
# Better: Validate after each component for fresh context
```

### Phase 3: Analyze Token Usage Opportunities

**Find large tool outputs**:
```bash
# Query timeline for tool results with large content
jq '.timeline[] | select(.type == "tool_result") | {tool_use_id, content_preview, estimated_tokens}' timeline.json

# IF tool result > 5000 tokens AND not essential:
#   → Context reduction opportunity
```

**Detect duplicate Read operations**:
```bash
# Find files read multiple times
jq '.timeline[] | select(.type == "tool_use" and .tool.name == "Read") | .tool.input.file_path' timeline.json | sort | uniq -c

# IF same file read 3+ times:
#   → Caching opportunity (read once, reference later)
```

**Identify late protocol file loading**:
```bash
# Find protocol document reads during IMPLEMENTATION (should be in INIT)
jq '.timeline[] | select(.type == "tool_use" and .tool.name == "Read" and (.tool.input.file_path | contains("docs/project")))' timeline.json

# IF protocol files loaded after INIT:
#   → Prefetching opportunity
```

### Phase 4: Analyze Quality Opportunities

**Find missing validation before major operations**:
```bash
# Pattern: Merge without prior checkstyle validation
# Pattern: Commit without verifying build success
# → Fail-fast opportunities
```

**Detect unclear protocol sequences**:
```bash
# Count retries, failed attempts, corrections
# IF high retry rate on specific operation:
#   → Clarity improvement opportunity
```

### Phase 4.5: Validate Recommendation Safety

**CRITICAL**: Before generating recommendations, verify they preserve correctness.

Apply safety checks to EACH proposed optimization:

#### 1. Correctness Preservation Test
**Question**: Does this optimization sacrifice correctness for speed?

**Check for**:
- Race conditions from parallelization (agents writing to same files)
- Data loss from caching (stale reads of dynamically updated files)
- Validation gaps from reordering (checks skipped due to early exit)

**Examples**:
- ❌ UNSAFE: "Parallelize all agent invocations" (may cause merge conflicts)
- ✅ SAFE: "Parallelize independent agent invocations with separate worktrees"

#### 2. Technical Debt Assessment
**Question**: Could this create maintenance burden or technical debt?

**Check for**:
- Increased complexity (premature optimization making code harder to maintain)
- Brittle dependencies (tight coupling that breaks with small changes)
- Hidden costs (memory usage from aggressive caching)

**Examples**:
- ❌ RISKY: "Cache all file reads indefinitely" (memory bloat)
- ✅ SAFE: "Cache protocol files during task execution only"

#### 3. Implementation Feasibility
**Question**: Is implementation guidance concrete enough to execute safely?

**Check for**:
- Missing edge case handling
- Unclear ordering constraints
- Incomplete rollback procedures

**Examples**:
- ❌ VAGUE: "Read files earlier"
- ✅ CONCRETE: "During INIT phase, after task.json creation, read all protocol files matching docs/project/*.md"

#### 4. Side Effect Analysis
**Question**: Could this recommendation cause unintended side effects?

**Check for**:
- Workflow disruption (breaking existing automation)
- Context pollution (loading unnecessary information)
- State machine violations (skipping required checkpoints)

**Examples**:
- ❌ HARMFUL: "Skip validation in SYNTHESIS to save time" (violates checkpoints)
- ✅ HARMLESS: "Validate after each component instead of end" (strengthens checkpoints)

#### Safety Verdict

For EACH recommendation, assign safety rating:
- **SAFE**: No correctness/debt concerns, proceed with recommendation
- **CONDITIONAL**: Safe IF conditions met (document conditions clearly)
- **UNSAFE**: Reject recommendation, do not include in output

**Output only SAFE and CONDITIONAL recommendations.**

### Phase 5: Generate Recommendations (Enhanced)

For EACH opportunity, provide:
- **Specific protocol change** (what to add/modify)
- **Quantified impact** (tokens, time, quality)
- **Priority** (HIGH/MEDIUM/LOW)
- **Safety rating** (SAFE/CONDITIONAL/UNSAFE)
- **Implementation guidance** (concrete steps)
- **Anti-pattern examples** (NEW: ✅/❌ showing violation vs correct)

#### Anti-Pattern Format

Show concrete before/after examples:

**❌ INEFFICIENT PATTERN** (current behavior):
```
[Exact sequence that caused inefficiency]
→ Impact: [specific measurement]
```

**✅ EFFICIENT PATTERN** (recommended):
```
[Exact sequence that would be efficient]
→ Impact: [specific improvement]
```

**Example for Parallelization**:

**❌ INEFFICIENT PATTERN**:
```
Message 1 @ 10:23:45 - Task(architect, model=opus)
  Wait for completion...
Message 2 @ 10:25:12 - Task(engineer, model=opus)
  Wait for completion...
Message 3 @ 10:26:38 - Task(formatter, model=opus)
  Wait for completion...

→ Impact: 3 sequential round-trips = ~5-6 minutes total
→ Wasted: 2 round-trips (agents are independent)
```

**✅ EFFICIENT PATTERN**:
```
Message 1 @ 10:23:45 - Parallel invocation:
  - Task(architect, model=opus)
  - Task(engineer, model=opus)
  - Task(formatter, model=opus)
  All complete by 10:25:30

→ Impact: 1 parallel round-trip = ~2 minutes total
→ Saved: 2 round-trips = 3-4 minutes (60% faster)
```

**Example for Fail-Fast**:

**❌ INEFFICIENT PATTERN**:
```
1. Create FileA.java (200 lines)
2. Create FileB.java (150 lines)
3. Create FileC.java (180 lines)
4. Run checkstyle on all files
   → 53 violations across all files
5. Fix violations with stale context (15% slower)

→ Impact: Context decay = 15% slower fixes
→ Cascading errors: FileC violations caused by FileA patterns
```

**✅ EFFICIENT PATTERN**:
```
1. Create FileA.java (200 lines)
2. Run checkstyle on FileA → 18 violations
3. Fix immediately with fresh context (faster)
4. Create FileB.java (150 lines)
5. Run checkstyle on FileB → 12 violations
6. Fix immediately
7. Create FileC.java → 8 violations (learned from A, B)

→ Impact: Fresh context = 15% faster fixes
→ Learning effect: Fewer violations in later files
```

### Phase 6: Self-Review Recommendations

**MANDATORY**: Before outputting recommendations, validate their quality.

Apply critical questions to EACH recommendation:

#### Critical Question 1: Impact Accuracy
**Check**: Is the quantified impact realistic and verifiable?

**Validation**:
- Token savings: Verify formula math (messages_eliminated × avg_tokens)
- Time savings: Verify percentage calculation (eliminated / total × 100%)
- Quality impact: Verify claim has evidence (measured retry rate, violation count)

**Red flags**:
- Suspiciously round numbers (e.g., "exactly 50% faster")
- Missing baseline (savings without showing current cost)
- Unverifiable claims ("much faster", "significantly better")

**If unrealistic**: Revise to show calculation or remove quantification

#### Critical Question 2: Implementation Detail
**Check**: Does implementation guidance contain enough detail to execute safely?

**Validation**:
- Specific file to modify: ✅ "docs/project/main-agent-coordination.md"
- Specific section to update: ✅ "REQUIREMENTS phase workflow"
- Exact change to make: ✅ "Add requirement: 'MUST launch...'"
- Edge cases handled: ✅ "If agents share dependencies: launch sequentially"

**Red flags**:
- Vague file references ("update documentation")
- Missing section anchor ("add to protocol somewhere")
- Unclear change ("make this better")

**If insufficient detail**: Add specific file path, section anchor, exact change text

#### Critical Question 3: Unintended Consequences
**Check**: Could this recommendation cause side effects?

**Validation**:
- Does it break existing automation? (hooks expecting specific patterns)
- Does it violate protocol invariants? (state machine checkpoints)
- Does it conflict with other recommendations? (prefetch vs context reduction)

**Red flags**:
- Recommendation assumes specific workflow (but multiple workflows exist)
- Optimization bypasses safety mechanism (validation, approval checkpoints)
- Change impacts multiple subsystems (without cross-system verification)

**If risky**: Add conditional safety requirements or reject

#### Critical Question 4: Priority Justification
**Check**: Is priority (HIGH/MEDIUM/LOW) justified by impact magnitude?

**Validation**:
- HIGH: ≥20% time savings OR ≥10k token savings OR critical quality issue
- MEDIUM: 10-20% time savings OR 5-10k token savings OR moderate quality issue
- LOW: <10% time savings OR <5k token savings OR minor quality issue

**Red flags**:
- HIGH priority with minimal quantified impact
- LOW priority but huge token/time savings
- Priority based on ease of implementation (not impact)

**If misaligned**: Adjust priority to match quantified impact

#### Self-Review Checklist

Before outputting:
- [ ] All quantified impacts verified with calculations
- [ ] All implementation guidance includes file + section + exact change
- [ ] All recommendations checked for side effects
- [ ] All priorities aligned with impact thresholds
- [ ] No UNSAFE recommendations included
- [ ] All CONDITIONAL recommendations document conditions clearly

## Output Format (Enhanced)

```json
{
  "status": "COMPLETED",
  "precondition": {
    "compliance_check": "No CRITICAL/HIGH violations",
    "safe_to_optimize": true
  },
  "efficiency_opportunities": [
    {
      "id": "EFF-1",
      "category": "execution_time",
      "priority": "HIGH",
      "safety_rating": "SAFE",
      "issue": "3 separate messages launching agents sequentially",
      "impact": "67% more round-trips than necessary",

      "anti_pattern_example": {
        "inefficient": "Message 1: Task(architect)\nMessage 2: Task(engineer)\nMessage 3: Task(formatter)\n→ Impact: 3 round-trips = ~6 minutes",
        "efficient": "Message 1: Task(architect) + Task(engineer) + Task(formatter)\n→ Impact: 1 round-trip = ~2 minutes\n→ Saved: 4 minutes (67% faster)"
      },

      "recommended_changes": [
        {
          "type": "PROCEDURE",
          "file": "docs/project/main-agent-coordination.md",
          "section": "REQUIREMENTS Phase Workflow",
          "anchor": "#requirements-phase-workflow",
          "change": "Add requirement: 'MUST launch all independent agents in single message with parallel Task calls'",
          "rationale": "Reduce message overhead by eliminating sequential delays",
          "edge_cases": [
            "If agents share dependencies: Launch sequentially",
            "If agent outputs feed into next agent: Launch sequentially"
          ]
        },
        {
          "type": "EXAMPLE",
          "file": "docs/project/main-agent-coordination.md",
          "section": "REQUIREMENTS Phase Examples",
          "anchor": "#requirements-examples",
          "change": "Add ✅/❌ example showing parallel vs sequential invocation",
          "rationale": "Provide clear implementation pattern"
        }
      ],

      "quantified_impact": {
        "token_savings": 8000,
        "token_calculation": "(3 messages - 1 message) × 4000 avg_tokens = 8000",
        "time_savings": "67% fewer round-trips",
        "time_calculation": "(3 round-trips - 1) / 3 = 0.67 = 67%",
        "quality_impact": "None (parallelization maintains quality)"
      },

      "self_review": {
        "impact_accuracy": "VERIFIED: Math correct, baseline documented",
        "implementation_detail": "VERIFIED: File path, section anchor, exact change specified",
        "side_effects": "NONE: Agents use separate worktrees, no conflicts",
        "priority_justified": "HIGH: 67% time savings exceeds 20% threshold"
      }
    },
    {
      "id": "EFF-2",
      "category": "quality",
      "priority": "MEDIUM",
      "safety_rating": "CONDITIONAL",
      "safety_conditions": [
        "Preserve fail-fast only for independent components",
        "Do NOT split validation of tightly coupled code"
      ],
      "issue": "Late validation after creating all files (53 violations)",
      "impact": "Fixes applied with stale context, 15% slower",

      "anti_pattern_example": {
        "inefficient": "1. Create FileA (18 violations)\n2. Create FileB (15 violations)\n3. Create FileC (20 violations)\n4. Run checkstyle: 53 violations\n5. Fix all with stale context\n→ Impact: Context decay = 15% slower",
        "efficient": "1. Create FileA, validate: 18 violations, fix\n2. Create FileB, validate: 12 violations, fix\n3. Create FileC, validate: 8 violations, fix\n→ Impact: Fresh context + learning = 15% faster + 35% fewer violations"
      },

      "recommended_changes": [
        {
          "type": "PROCEDURE",
          "file": "docs/project/main-agent-coordination.md",
          "section": "IMPLEMENTATION Best Practices",
          "anchor": "#implementation-best-practices",
          "change": "Add fail-fast requirement: 'Validate after each logical component, not after all files. Fresh context enables faster fixes and prevents cascading errors.'",
          "rationale": "Fresh context = faster fixes, prevent cascading errors",
          "edge_cases": [
            "For tightly coupled files (interface + impl): Validate together",
            "For test files: Validate with corresponding source file"
          ]
        }
      ],

      "quantified_impact": {
        "token_savings": 0,
        "token_calculation": "No direct token savings (same validation count)",
        "time_savings": "15% faster fixes",
        "time_calculation": "Measured: avg 8 min/violation with stale context, 6.8 min with fresh = 15% faster",
        "quality_impact": "Earlier error detection prevents cascading issues (35% fewer violations in later files)"
      },

      "self_review": {
        "impact_accuracy": "VERIFIED: Based on measured violation fix times",
        "implementation_detail": "VERIFIED: File, section, exact text, edge cases documented",
        "side_effects": "CONDITIONAL: Safe for independent components only",
        "priority_justified": "MEDIUM: 15% time savings in 10-20% threshold"
      }
    }
  ],
  "summary": {
    "total_opportunities": 2,
    "by_priority": {
      "high": 1,
      "medium": 1,
      "low": 0
    },
    "by_safety": {
      "safe": 1,
      "conditional": 1,
      "unsafe_rejected": 0
    },
    "estimated_total_token_savings": 8000,
    "estimated_time_improvement": "Combined: 50% fewer round-trips + 15% faster fixes per iteration"
  },
  "verification": {
    "self_review_completed": true,
    "all_impacts_verified": true,
    "all_implementation_details_complete": true,
    "no_unsafe_recommendations": true
  }
}
```

## Optimization Categories

### 1. Parallelization
**Pattern**: Independent operations executed sequentially
**Detection**: Multiple Read/Task calls in separate messages
**Fix**: Batch in single message
**Savings**: (messages_before - 1) × avg_tokens_per_message

### 2. Prefetching
**Pattern**: Late loading of predictable dependencies
**Detection**: Protocol files read during IMPLEMENTATION (not INIT)
**Fix**: Load all predictable files during INIT
**Savings**: Avoided round-trips × (read_tokens + response_tokens)

### 3. Fail-Fast Validation
**Pattern**: Validate after all work done (late error detection)
**Detection**: Single validation at end with many violations
**Fix**: Validate after each component
**Savings**: 15% time reduction from fresh context

### 4. Context Reduction
**Pattern**: Verbose outputs, duplicate reads
**Detection**: Large tool results, repeated file reads
**Fix**: Summarize outputs, cache reads
**Savings**: Reduced token count per message

### 5. Procedural Clarity
**Pattern**: Multiple retries, confusion, corrections
**Detection**: High retry rate on specific operations
**Fix**: Add clearer documentation, examples, fail-fast checks
**Savings**: Reduced rework iterations

## Quantification Methodology

**Token Savings**:
```
Parallelization: (messages_eliminated) × (avg_message_tokens)
Prefetching: (avoided_reads) × (read_tokens + response_tokens)
Context Reduction: (original_tokens - optimized_tokens) × (frequency)
```

**Time Savings**:
```
Round-trip reduction: (eliminated_round_trips) / (total_round_trips) × 100%
Fail-fast improvement: estimated 10-20% per iteration
```

**Quality Impact**:
```
Earlier error detection: Prevents cascading issues
Better context: Improved decision accuracy
Clearer procedures: Reduced confusion and retries
```

## Verification Checklist (Enhanced)

Before outputting efficiency recommendations:

**Phase Completion**:
- [ ] Compliance audit passed (no CRITICAL/HIGH violations)
- [ ] Timeline analyzed for parallelization opportunities
- [ ] Token usage patterns identified
- [ ] Quality improvement opportunities found
- [ ] Safety checks applied to all recommendations (Phase 4.5)
- [ ] Self-review completed for all recommendations (Phase 6)

**Per-Recommendation Quality**:
- [ ] Each recommendation has safety rating (SAFE/CONDITIONAL)
- [ ] Each recommendation has anti-pattern example (❌/✅)
- [ ] Each recommendation has quantified impact with calculations shown
- [ ] Each recommendation has specific file + section + anchor
- [ ] Each recommendation has edge cases documented
- [ ] Priority assigned and justified by impact thresholds
- [ ] Implementation guidance is concrete and executable
- [ ] No UNSAFE recommendations included

**Output Quality**:
- [ ] JSON is valid and well-formed
- [ ] Verification section confirms self-review completion
- [ ] Summary includes breakdown by_priority and by_safety
- [ ] All calculations are mathematically correct

## Related Skills

- **audit-protocol-compliance**: Must pass before efficiency audit
- **parse-conversation-timeline**: Provides structured data for analysis
- **/optimize-doc**: Optimizes documentation clarity (complementary, different purpose)
