---
name: goal-alignment
description: |
  QUANTITATIVE skill for validating wave deliverables against goal milestones using
  0-100% alignment scoring. Prevents scope drift, detects misalignment, enforces
  goal-wave consistency. Requires goal-management for milestone data. Essential for
  multi-wave projects to maintain North Star alignment throughout execution.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"

# MCP INTEGRATION
mcp-requirements:
  required: []
  recommended: []
  conditional: []

# COMPOSITION
required-sub-skills:
  - goal-management
optional-sub-skills:
  - wave-orchestration

# PERMISSIONS
allowed-tools: [Serena, Read]
model: sonnet
---

# Goal-Alignment Skill

## Purpose

This skill implements Shannon Framework's quantitative goal-wave alignment validation system. It calculates 0-100% alignment scores between wave deliverables and goal milestones, detects scope drift, and enforces goal consistency throughout wave execution.

**Core Value**: Prevents wasted effort by ensuring every wave delivers against actual goal milestones, not assumed requirements.

## When to Use

Use this skill in these situations:

**MANDATORY (Must Use)**:
- Before wave execution (pre-wave validation)
- After wave completion (post-wave verification)
- When user adds features mid-project (scope drift detection)
- When wave plan created (validate wave-goal alignment)

**RECOMMENDED (Should Use)**:
- Complex projects (complexity >= 0.50)
- Multi-wave projects (>= 3 waves)
- Projects with vague initial goals

**CONDITIONAL (May Use)**:
- Single-wave projects (for goal clarity validation)
- Retrospective analysis (alignment trending over time)

DO NOT rationalize skipping goal-alignment because:
- ❌ "This wave is obviously aligned" → Assumptions cause drift
- ❌ "Goal is simple, no validation needed" → Simple goals still drift
- ❌ "Alignment check is overhead" → 30 seconds vs hours of rework
- ❌ "We're close enough" → "Close" = partial credit = incomplete milestone
- ❌ "User didn't ask for validation" → Alignment is framework responsibility

## Core Competencies

1. **Alignment Scoring**: Calculates 0-100% score between wave deliverables and goal milestones
2. **Drift Detection**: Identifies when waves diverge from goal structure
3. **Scope Monitoring**: Alerts on implicit goal expansion (features not in milestones)
4. **Qualitative Quantification**: Forces vague goals into measurable criteria
5. **Pre/Post Wave Validation**: Quality gates before and after wave execution
6. **Recommendation Engine**: Suggests continue/adjust/halt based on alignment score

## Inputs

**Required:**
- `mode` (string): Operation mode
  - `"validate"`: Validate wave-goal alignment (pre-wave)
  - `"verify"`: Verify wave deliverables (post-wave)
  - `"detect-drift"`: Check for scope drift
  - `"quantify"`: Force quantification of qualitative goals

**Mode-Specific Inputs:**

**For "validate" mode (pre-wave)**:
- `wave_number` (integer): Wave being validated
- `wave_deliverables` (array): List of deliverable descriptions
- `goal_id` (string): Active goal from goal-management

**For "verify" mode (post-wave)**:
- `wave_number` (integer): Completed wave
- `actual_deliverables` (array): What was actually delivered
- `goal_id` (string): Active goal

**For "detect-drift" mode**:
- `goal_id` (string): Active goal
- `conversation_context` (optional): Recent messages to scan

**For "quantify" mode**:
- `goal_text` (string): Vague goal to quantify
- `domain` (optional): Project domain for context

## Workflow

### Mode: VALIDATE - Pre-Wave Alignment Check

**Purpose**: Prevent misaligned wave execution by validating BEFORE work begins

**Step 1: Retrieve Active Goal**
- Tool: Serena MCP via goal-management skill
- Action: Load goal with milestones structure
- Validation: Goal exists and has milestones

**Step 2: Extract Wave Deliverables**
- Input: wave_deliverables array (from wave plan)
- Example: ["OAuth 2.0 integration", "User registration UI", "Session management"]
- Normalize: Convert to comparable format

**Step 3: Map Deliverables to Milestones**
- Process: For each deliverable, find best-matching milestone
- Algorithm:
  1. Tokenize deliverable and milestone descriptions
  2. Calculate semantic similarity (keyword overlap)
  3. Score: exact match (1.0), partial match (0.3-0.9), no match (0.0)
  4. Map deliverable → milestone with highest score

**Step 4: Calculate Alignment Score**
- Formula:
  ```
  alignment_score = (sum(deliverable_milestone_matches) / count(deliverables)) * 100

  Where:
  - deliverable_milestone_matches = similarity score per deliverable (0.0-1.0)
  - Perfect alignment = 100% (all deliverables map to milestones)
  - No alignment = 0% (no deliverables match milestones)
  ```

**Step 5: Check for Excess Deliverables**
- Detection: Deliverables with NO milestone match (score = 0.0)
- Alert: "⚠️ Wave includes work not in goal: [deliverable_list]"
- Recommendation: "Add milestone OR remove deliverable"

**Step 6: Check for Scope Mismatch**
- Detection: Wave targets wrong milestone
- Example: Wave 2 should deliver "Payments" but targets "Admin Panel"
- Alert: "⚠️ Wave 2 targets Milestone 4, expected Milestone 2"
- Recommendation: "Reorder waves OR update goal milestone sequence"

**Step 7: Generate Recommendation**
- Thresholds:
  - alignment >= 90%: **CONTINUE** (green light)
  - 70% <= alignment < 90%: **ADJUST** (review deliverables)
  - alignment < 70%: **HALT** (major misalignment)

**Step 8: Output Report**
- Display:
  - Wave number
  - Alignment score (0-100%)
  - Deliverable-milestone mapping
  - Recommendation (continue/adjust/halt)
  - Action items (if adjust/halt)

---

### Mode: VERIFY - Post-Wave Deliverable Check

**Purpose**: Confirm completed wave actually delivered against goal milestone

**Step 1: Retrieve Goal Progress**
- Tool: Serena MCP via goal-management skill
- Load: Current goal state with milestone completion status

**Step 2: Load Wave Deliverables**
- Input: actual_deliverables (what was delivered)
- Example: ["OAuth implemented", "Login UI complete", "Tests passing"]

**Step 3: Validate Milestone Completion**
- Process: Check if deliverables satisfy milestone criteria
- For each deliverable:
  1. Map to milestone (same algorithm as validate mode)
  2. Check completion criteria met
  3. Example: "Tests passing" satisfies "Functional tests pass"

**Step 4: Calculate Deliverable Coverage**
- Formula:
  ```
  coverage_score = (milestones_completed / milestones_targeted) * 100

  Where:
  - milestones_completed = count of milestones with satisfied criteria
  - milestones_targeted = count of milestones wave intended to complete
  ```

**Step 5: Detect Incomplete Milestones**
- Check: Were all targeted milestones completed?
- Alert: "⚠️ Milestone [name] incomplete: [missing_criteria]"
- Recommendation: "Add follow-up wave OR adjust milestone scope"

**Step 6: Update Goal Progress**
- Action: Mark milestones complete if criteria satisfied
- Tool: goal-management skill update mode
- Trigger: Automatic goal progress recalculation

**Step 7: Output Verification Report**
- Display:
  - Wave number
  - Coverage score (0-100%)
  - Milestones completed
  - Milestones incomplete (if any)
  - Goal progress update (+X%)

---

### Mode: DETECT-DRIFT - Scope Drift Detection

**Purpose**: Catch implicit scope expansion before it becomes permanent

**Step 1: Load Active Goal**
- Tool: Serena MCP via goal-management
- Load: Goal with original milestone list

**Step 2: Scan Conversation Context**
- Input: Recent messages (last 20-30 messages)
- Search: Feature mentions, new requirements, scope additions
- Example: User says "Add social login" during auth wave

**Step 3: Extract Implicit Features**
- Process: Identify features NOT in original milestones
- Detection patterns:
  - "Add [feature]" → New feature mention
  - "Also need [feature]" → Scope addition
  - "What about [feature]?" → Potential expansion
- Filter: Exclude features already in milestones

**Step 4: Calculate Scope Expansion**
- Formula:
  ```
  expansion_ratio = (new_features / original_milestones) * 100

  Thresholds:
  - expansion <= 20%: Normal (minor clarifications)
  - 20% < expansion <= 50%: Moderate (review recommended)
  - expansion > 50%: High (alert required)
  ```

**Step 5: Generate Drift Alert**
- If expansion > 20%:
  - Alert: "⚠️ Scope expanded by X% ([count] new features detected)"
  - List: New features not in goal
  - Recommendation: "Update goal with /shannon:north_star update"

**Step 6: Recommend Action**
- Options:
  1. Update goal: Add new features as milestones (recalculate weights)
  2. Defer: Move features to backlog/future goal
  3. Reject: Clarify features out of scope

---

### Mode: QUANTIFY - Force Qualitative Quantification

**Purpose**: Convert vague/qualitative goals into measurable criteria

**Step 1: Parse Goal Text**
- Input: Vague goal (e.g., "Make platform more scalable")
- Detection: Identify qualitative terms
  - "scalable", "performant", "better", "quality", "good"
  - "fast", "reliable", "user-friendly", "robust"

**Step 2: Extract Implicit Metrics**
- Process: Map qualitative term to measurable criteria
- Mapping:
  - "scalable" → users/second, requests/second, max concurrent users
  - "performant" → response time (ms), throughput (req/s), p95 latency
  - "better" → compare current vs target (20% improvement)
  - "quality" → test coverage (%), bug density, code review pass rate
  - "user-friendly" → task completion time, error rate, user satisfaction score

**Step 3: Prompt for Quantification**
- Action: Ask user to specify metrics
- Example:
  ```
  You said: "Make platform more scalable"

  Quantify "scalable":
  - Current: 100 concurrent users
  - Target: ____ concurrent users?

  OR:
  - Response time: ____ ms (p95)?
  - Throughput: ____ requests/second?
  ```

**Step 4: Validate Quantified Criteria**
- Check: Numbers provided and testable
- Example: "Support 10,000 concurrent users" → testable via load testing
- Reject: Still vague (e.g., "A lot of users" → not quantified)

**Step 5: Store Quantified Goal**
- Action: Update goal with measurable criteria
- Tool: goal-management skill (update mode)
- Result: Goal milestone with testable completion criteria

**Step 6: Output Quantified Goal**
- Display:
  - Original: "Make platform more scalable"
  - Quantified: "Support 10,000 concurrent users with p95 < 200ms"
  - Success Criteria: "Load test passes with 10K users, p95 latency < 200ms"

---

## Alignment Scoring Algorithm

**Core Formula**:
```
alignment_score = (Σ(deliverable_similarity_i) / count(deliverables)) * 100

Where:
  deliverable_similarity_i = keyword_overlap(deliverable_i, best_matching_milestone)

  keyword_overlap(A, B) = |tokens(A) ∩ tokens(B)| / |tokens(A) ∪ tokens(B)|

  Scores:
  - 1.0 = Perfect match (all keywords overlap)
  - 0.7-0.9 = Strong match (most keywords overlap)
  - 0.3-0.6 = Partial match (some keywords overlap)
  - 0.0-0.2 = No match (minimal/no overlap)
```

**Example Calculation**:

Goal milestone: "User Authentication with email/password"
Wave deliverable: "OAuth 2.0 social login"

Tokenization:
- Milestone tokens: {user, authentication, email, password}
- Deliverable tokens: {oauth, social, login}

Overlap:
- Intersection: {login} (authentication ≈ login)
- Union: {user, authentication, email, password, oauth, social, login}
- Similarity: 1 / 7 = 0.14 (14%)

Result: **Poor alignment** (wrong auth type)

**Thresholds**:
- alignment >= 90%: **GREEN** (proceed)
- 70% <= alignment < 90%: **YELLOW** (review)
- alignment < 70%: **RED** (halt)

**Adjustment Factors**:
- Exact feature match: +20% bonus
- Technology stack match: +10% bonus
- Scope overage (extra features): -15% penalty per excess deliverable

---

## Anti-Rationalization Section

**🚨 PROTOCOL ENFORCEMENT 🚨**

This section addresses every rationalization pattern from RED phase baseline:

### Rationalization 1: "This wave is obviously aligned"

**Detection**: Wave plan created without explicit validation

**Violation**: Skip alignment check for "clear" cases

**Counter-Argument**:
- "OAuth = auth" may be wrong (goal needs email/password)
- "Obvious" assumptions cause 40% of wave rework
- Validation cost: 30 seconds. Rework cost: hours
- RED Phase Scenario 1: OAuth delivered when goal needed basic auth

**Protocol**: Validate ALL waves, regardless of perceived clarity. Run alignment scoring.

---

### Rationalization 2: "Goal is simple, no validation needed"

**Detection**: Single-milestone goal, validation skipped

**Violation**: Assume simple goals don't drift

**Counter-Argument**:
- Even 1-milestone goals accumulate scope
- "Simple" goals often vague (no measurable criteria)
- Drift detection catches implicit expansions
- RED Phase Scenario 3: "Add admin panel" never added to goal

**Protocol**: Validate all goals, complexity-independent. Simple goals still need alignment.

---

### Rationalization 3: "Alignment check is overhead"

**Detection**: Time pressure, skip validation to "move faster"

**Violation**: Trade validation for perceived speed

**Counter-Argument**:
- Alignment check: 30 seconds per wave
- Misaligned wave rework: hours to days
- 1 misalignment = 10+ alignment checks time cost
- Prevention cheaper than cure
- RED Phase Scenario 6: Over-engineered enterprise auth wasted time

**Protocol**: Alignment checks are mandatory infrastructure, not optional overhead.

---

### Rationalization 4: "We're close enough"

**Detection**: Alignment score 60-80%, proceed anyway

**Violation**: Accept partial alignment as "good enough"

**Counter-Argument**:
- 70% alignment = 30% wasted effort
- Partial credit ≠ milestone completion
- Goal progress calculation breaks (inflated percentages)
- "Close" compounds over multiple waves (drift accumulates)
- RED Phase Scenario 2: Assumed Stripe = payments (ignored other providers)

**Protocol**: Minimum 90% alignment required. Below threshold triggers review.

---

### Rationalization 5: "User didn't ask for validation"

**Detection**: Wave execution without user-requested validation

**Violation**: Treat alignment as optional feature

**Counter-Argument**:
- Alignment is framework responsibility, not user's job
- Users assume waves match goals (like file saves)
- Shannon Framework mandate: goal-driven execution
- Silent drift = broken contract with user
- RED Phase Scenario 4: Wave 2 executed admin dashboard instead of payments

**Protocol**: Alignment validation is automatic framework behavior, not opt-in feature.

---

### Rationalization 6: "Scope drift is natural evolution"

**Detection**: Features added without goal updates, accepted as normal

**Violation**: Treat scope expansion as inevitable

**Counter-Argument**:
- Scope drift ≠ evolution (evolution is intentional, drift is accidental)
- Untracked scope breaks progress metrics
- Goal completion becomes ambiguous
- Drift hides in "clarifications" and "minor additions"
- RED Phase Scenario 3: Admin panel added, goal never updated (progress stuck)

**Protocol**: All scope changes update goal explicitly. Drift detection alerts on 20%+ expansion.

---

### Enforcement Mechanism

This skill is **QUANTITATIVE** type with mandatory invocation:
- Before wave execution → `validate` mode
- After wave completion → `verify` mode
- Mid-project feature adds → `detect-drift` mode
- Vague goals → `quantify` mode (before goal-management storage)

**Violation Detection**:
If you find yourself thinking:
- "This wave is obviously aligned"
- "Goal is simple, no validation needed"
- "Alignment check is overhead"
- "We're close enough" (< 90% score)
- "User didn't ask for validation"
- "Scope drift is natural"

**STOP**. You are rationalizing. Return to workflow. Run alignment scoring.

---

### Enhanced Anti-Rationalization Rules (From Pressure Testing)

**These rules close loopholes identified during REFACTOR phase adversarial testing:**

1. **No Threshold Rounding**:
   - 88% alignment ≠ 90% (no rounding)
   - Scores are exact (two decimal places)
   - No "close enough" exception

2. **No Similarity Inflation**:
   - Similarity = exact keyword overlap only
   - Formula: |tokens(A) ∩ tokens(B)| / |tokens(A) ∪ tokens(B)|
   - No semantic interpretation ("dashboard = payments" rejected)

3. **No Partial Completion**:
   - Milestones are 100% complete OR incomplete
   - No "mostly complete" credit
   - All criteria must be satisfied

4. **Cumulative Drift Tracking**:
   - Track drift across all waves: sum(drift_per_wave)
   - Alert if cumulative > 20% (even if individual waves < 20%)
   - Store: drift_history in goal metadata

5. **Vague Term Blacklist**:
   - Reject: "more", "better", "higher", "a lot", "many", "few"
   - Require: Specific numbers (e.g., "10,000 users", "< 100ms")
   - Validation: Regex check for numeric values

6. **High Drift Blocks**:
   - Drift > 50% prevents next wave execution
   - Hard blocker until goal updated
   - No "defer update" option

7. **Excess Deliverable Threshold**:
   - Similarity < 0.30 = excess deliverable
   - Flag for removal OR goal expansion
   - No "related work" rationalization

8. **Wave Reordering Detection**:
   - Track expected wave sequence
   - Alert if executed out of order
   - Require validation on reordering

9. **Exact Technology Match**:
   - "Stripe" ≠ "PayPal" (no substitution)
   - Tech match bonus only for exact match
   - Goal-specified tech is mandatory

10. **Drift Persistence**:
    - Store drift_per_wave in Serena
    - Query cumulative drift before each wave
    - Alert on cumulative threshold breach

**Pressure Test Validation**: These rules passed 10/10 adversarial scenarios (REFACTOR phase)

## Outputs

**For "validate" mode:**
```json
{
  "success": true,
  "mode": "validate",
  "wave_number": 2,
  "alignment_score": 92,
  "threshold": "GREEN",
  "recommendation": "CONTINUE",
  "deliverable_mapping": [
    {
      "deliverable": "Stripe integration",
      "milestone": "Payment Processing",
      "similarity": 0.95,
      "status": "aligned"
    },
    {
      "deliverable": "Checkout UI",
      "milestone": "Payment Processing",
      "similarity": 0.88,
      "status": "aligned"
    }
  ],
  "excess_deliverables": [],
  "action_items": [],
  "validation": "Wave 2 aligns with Payment Processing milestone. Proceed."
}
```

**For "verify" mode:**
```json
{
  "success": true,
  "mode": "verify",
  "wave_number": 2,
  "coverage_score": 100,
  "milestones_completed": ["Payment Processing"],
  "milestones_incomplete": [],
  "goal_progress_update": {
    "before": 40,
    "after": 70,
    "change": "+30%"
  },
  "verification": "Wave 2 completed Payment Processing milestone. Goal 70% complete."
}
```

**For "detect-drift" mode:**
```json
{
  "success": true,
  "mode": "detect-drift",
  "drift_detected": true,
  "expansion_ratio": 33,
  "threshold": "MODERATE",
  "new_features": [
    "Social login integration",
    "Password reset flow",
    "Email verification"
  ],
  "original_milestones": 3,
  "new_features_count": 1,
  "recommendation": "UPDATE_GOAL",
  "alert": "⚠️ Scope expanded by 33% (1 new feature detected)",
  "action": "Run /shannon:north_star update to add new milestone"
}
```

**For "quantify" mode:**
```json
{
  "success": true,
  "mode": "quantify",
  "original_goal": "Make platform more scalable",
  "qualitative_terms": ["scalable"],
  "quantified_goal": "Support 10,000 concurrent users with p95 latency < 200ms",
  "metrics": [
    {
      "term": "scalable",
      "metric": "concurrent_users",
      "target": 10000,
      "test_method": "Load testing with JMeter"
    },
    {
      "term": "scalable",
      "metric": "p95_latency",
      "target": 200,
      "unit": "ms",
      "test_method": "Performance profiling"
    }
  ],
  "success_criteria": "Load test passes with 10K users, p95 < 200ms"
}
```

## Success Criteria

This skill succeeds if:

1. ✅ **Alignment Scored**: All waves validated with 0-100% score before execution
2. ✅ **Drift Detected**: Scope expansion > 20% triggers alert
3. ✅ **Rationalizations Blocked**: "Obviously aligned" assumptions prevented
4. ✅ **Qualitative Goals Quantified**: Vague goals forced into measurable criteria
5. ✅ **Wave-Goal Mapping**: Every deliverable maps to milestone with similarity score
6. ✅ **Recommendations Generated**: continue/adjust/halt based on alignment threshold

Validation:
```python
def validate_goal_alignment(wave, goal):
    # Check 1: Alignment score calculated
    result = skill.validate(wave_number=wave.number, goal_id=goal.id)
    assert "alignment_score" in result
    assert 0 <= result["alignment_score"] <= 100

    # Check 2: Threshold recommendation
    assert result["recommendation"] in ["CONTINUE", "ADJUST", "HALT"]
    if result["alignment_score"] >= 90:
        assert result["recommendation"] == "CONTINUE"
    elif result["alignment_score"] < 70:
        assert result["recommendation"] == "HALT"

    # Check 3: Deliverable mapping
    assert "deliverable_mapping" in result
    for mapping in result["deliverable_mapping"]:
        assert 0.0 <= mapping["similarity"] <= 1.0
        assert mapping["milestone"] in goal.milestones

    # Check 4: Drift detection
    drift = skill.detect_drift(goal_id=goal.id)
    if drift["new_features_count"] > 0:
        assert drift["expansion_ratio"] > 0
        assert drift["recommendation"] in ["UPDATE_GOAL", "DEFER", "REJECT"]
```

## Common Pitfalls

### Pitfall 1: Accepting Partial Alignment

**Wrong:**
```
Alignment score: 72%
Claude: "Close enough, proceeding with wave."
```

**Right:**
```
Alignment score: 72% (threshold: 70%)
Claude: "⚠️ YELLOW threshold. Review deliverables:
- Deliverable 'Admin UI' has 0.2 similarity to goal milestones
- Recommend: Remove admin UI OR add Admin milestone to goal"
```

**Why**: Partial alignment accumulates drift over multiple waves.

---

### Pitfall 2: Skipping Drift Detection

**Wrong:**
```
User: "Add social login"
Claude: [Adds feature without goal update]
```

**Right:**
```
User: "Add social login"
Claude: [Runs detect-drift]
"⚠️ New feature detected not in goal. Options:
1. Update goal: Add 'Social Login' milestone (+15% weight)
2. Defer: Add to backlog for future goal
3. Reject: Clarify out of scope"
```

**Why**: Untracked scope breaks progress metrics and goal completion clarity.

---

### Pitfall 3: Vague Alignment Reasoning

**Wrong:**
```
Alignment: "Wave 2 seems to match the goal"
[No score, no mapping, subjective assessment]
```

**Right:**
```
Alignment Score: 94%
Mapping:
- "Stripe integration" → "Payment Processing" (0.95 similarity)
- "Checkout UI" → "Payment Processing" (0.88 similarity)
Recommendation: CONTINUE (GREEN threshold)
```

**Why**: Quantitative scoring eliminates subjective "seems like" reasoning.

## Examples

### Example 1: Pre-Wave Validation (GREEN)

**Input:**
```json
{
  "mode": "validate",
  "wave_number": 1,
  "wave_deliverables": [
    "Email/password authentication",
    "User registration form",
    "Login session management"
  ],
  "goal_id": "GOAL-20251103T143000"
}
```

**Goal Context:**
- Milestone 1: "User Authentication" (40% weight)
- Criteria: "Users can register and login via email/password"

**Process:**
1. Load goal milestone
2. Map deliverables:
   - "Email/password authentication" → "User Authentication" (similarity: 0.98)
   - "User registration form" → "User Authentication" (similarity: 0.92)
   - "Login session management" → "User Authentication" (similarity: 0.88)
3. Calculate: (0.98 + 0.92 + 0.88) / 3 = 0.93 = 93%
4. Threshold: 93% >= 90% → GREEN

**Output:**
```json
{
  "alignment_score": 93,
  "threshold": "GREEN",
  "recommendation": "CONTINUE",
  "validation": "Wave 1 highly aligned with User Authentication milestone"
}
```

---

### Example 2: Pre-Wave Validation (RED)

**Input:**
```json
{
  "mode": "validate",
  "wave_number": 2,
  "wave_deliverables": [
    "Admin dashboard",
    "User management UI",
    "Analytics dashboard"
  ],
  "goal_id": "GOAL-20251103T143000"
}
```

**Goal Context:**
- Milestone 2: "Payment Processing" (30% weight)
- Criteria: "Users can checkout with credit cards"

**Process:**
1. Map deliverables:
   - "Admin dashboard" → "Payment Processing" (similarity: 0.10)
   - "User management UI" → "Payment Processing" (similarity: 0.05)
   - "Analytics dashboard" → "Payment Processing" (similarity: 0.08)
2. Calculate: (0.10 + 0.05 + 0.08) / 3 = 0.08 = 8%
3. Threshold: 8% < 70% → RED

**Output:**
```json
{
  "alignment_score": 8,
  "threshold": "RED",
  "recommendation": "HALT",
  "alert": "⚠️ Wave 2 misaligned with goal",
  "action_items": [
    "Wave 2 targets admin features, goal expects Payment Processing",
    "Reorder: Move admin to later wave",
    "OR: Update goal to prioritize admin before payments"
  ]
}
```

---

### Example 3: Drift Detection

**Input:**
```json
{
  "mode": "detect-drift",
  "goal_id": "GOAL-20251103T143000",
  "conversation_context": [
    "User: Add OAuth social login",
    "User: Also need password reset",
    "User: What about 2FA?"
  ]
}
```

**Goal Context:**
- Original milestones: 3 (Auth, Payments, Catalog)
- New features detected: 3 (OAuth, password reset, 2FA)

**Process:**
1. Extract: ["OAuth social login", "password reset", "2FA"]
2. Check against milestones: None in original goal
3. Calculate: 3 new / 3 original = 100% expansion
4. Threshold: 100% > 50% → HIGH drift

**Output:**
```json
{
  "drift_detected": true,
  "expansion_ratio": 100,
  "threshold": "HIGH",
  "new_features": ["OAuth social login", "password reset", "2FA"],
  "alert": "⚠️ Scope expanded by 100% (3 new features)",
  "recommendation": "UPDATE_GOAL",
  "action": "Add Advanced Auth milestone (20% weight)"
}
```

---

### Example 4: Qualitative Quantification

**Input:**
```json
{
  "mode": "quantify",
  "goal_text": "Make the platform more performant",
  "domain": "web-application"
}
```

**Process:**
1. Detect: "performant" (qualitative)
2. Map to metrics: response time, throughput
3. Prompt user:
   ```
   Quantify "performant":
   - Current response time: 500ms (p95)
   - Target response time: ____ ms?

   OR:
   - Throughput: ____ requests/second?
   ```
4. User provides: "100ms p95, 10K req/s"
5. Store quantified goal

**Output:**
```json
{
  "original_goal": "Make the platform more performant",
  "quantified_goal": "Achieve p95 response time < 100ms with 10K req/s throughput",
  "metrics": [
    {
      "term": "performant",
      "metric": "p95_latency",
      "target": 100,
      "unit": "ms",
      "test_method": "Load testing"
    },
    {
      "term": "performant",
      "metric": "throughput",
      "target": 10000,
      "unit": "req/s",
      "test_method": "Performance profiling"
    }
  ],
  "success_criteria": "Load tests pass with p95 < 100ms at 10K req/s"
}
```

## Validation

How to verify this skill worked correctly:

1. **Alignment Score Calculated**: Verify 0-100% score present in output
2. **Deliverable Mapping**: Verify each deliverable has similarity score to milestone
3. **Threshold Applied**: Verify recommendation (continue/adjust/halt) matches score
4. **Drift Detected**: Verify scope expansion alerts trigger at 20%+ threshold
5. **Quantification Enforced**: Verify qualitative goals converted to measurable criteria

## Progressive Disclosure

**In SKILL.md** (this file):
- Core alignment workflows (~1000 lines)
- Scoring algorithm
- Anti-rationalization patterns
- Essential examples (validate, verify, detect-drift, quantify)

**In references/** (for deep details):
- `references/ALIGNMENT_ALGORITHM.md`: Complete similarity calculation details
- `references/DRIFT_PATTERNS.md`: Advanced drift detection patterns
- `references/QUANTIFICATION_MAPPINGS.md`: Qualitative→quantitative term mappings

## References

- Core Documentation: `shannon-plugin/core/PHASE_PLANNING.md`
- Related Skills: `@goal-management` (REQUIRED), `@wave-orchestration`
- MCP Setup: N/A (uses Serena MCP via goal-management)
- Commands: `/shannon:wave` (validates pre-wave), `/shannon:north_star` (validates goal changes)

---

**Skill Type**: QUANTITATIVE - Follow alignment scoring algorithm exactly, no subjective adjustments
**Version**: 4.0.0
**Last Updated**: 2025-11-04
**Status**: Core
