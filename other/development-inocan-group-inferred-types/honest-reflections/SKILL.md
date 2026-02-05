---
name: honest-reflections
description: |
  Systematic gap analysis for claimed vs actual work completion. Uses 100+ sequential thoughts
  to identify assumptions, partial completions, missing components, and rationalization patterns.
  Validates completion claims against original plans, detects scope deviations, reveals quality gaps.
  Essential for self-assessment before declaring work complete. Use when: claiming completion,
  final reviews, quality audits, detecting rationalization patterns in own work.

skill-type: PROTOCOL
shannon-version: ">=4.1.0"

mcp-requirements:
  required:
    - name: sequential
      purpose: Systematic 100+ thought reflection process
      fallback: native-thinking (degraded - less systematic)
      degradation: medium
  recommended:
    - name: serena
      purpose: Store reflection results for learning
      fallback: local-storage
      degradation: low

required-sub-skills: []

optional-sub-skills:
  - systematic-debugging
  - confidence-check

allowed-tools: [Read, Grep, Sequential, Serena]
---

# Honest Reflections Skill

## Overview

**Purpose**: Systematic gap analysis using 100+ sequential thoughts to identify discrepancies between claimed completion and actual delivery. Prevents premature completion declarations by revealing assumptions, partial work, missing components, and rationalization patterns.

**Core Value**: Catches the moment when you're about to claim "100% complete" on 50% completion.

**Key Innovation**: Self-assessment protocol that replicates critical external review, catching gaps before they become credibility issues.

---

## When to Use This Skill

### MANDATORY (Must Use)

Use this skill when:
- **Before declaring work "complete"**: Any statement like "all done", "100% finished", "scope complete"
- **Final commit before handoff**: Last commit of major work session
- **Completion milestones**: MVP complete, phase complete, project done
- **Quality gate reviews**: Before presenting work to stakeholders
- **After long work sessions**: 6+ hours of continuous work without checkpoint

### RECOMMENDED (Should Use)

- After each major phase of multi-phase project
- When tempted to rationalize skipping remaining work
- Before creating handoff documentation
- When user asks "is it really complete?"
- Periodic self-audits (weekly for long projects)

### CONDITIONAL (May Use)

- Mid-project health checks
- When feeling uncertainty about completeness
- After receiving feedback suggesting gaps
- Learning from past incomplete deliveries

### DO NOT Rationalize Skipping Because

❌ "Work looks complete" → Appearances deceive, systematic check required
❌ "I'm confident it's done" → Confidence without verification is overconfidence
❌ "Takes too long" → 30-minute reflection prevents hours of rework
❌ "Already did self-review" → Mental review misses 40-60% of gaps
❌ "User didn't explicitly ask" → Professional responsibility to verify completion

---

## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically skip honest reflection to avoid discovering gaps. Below are the 6 most common rationalizations detected in baseline testing, with mandatory counters.

### Rationalization 1: "Obviously Complete, No Need to Reflect"

**Example**: Agent finishes implementing 8 features, thinks "all features done", declares complete without checking original spec that required 12 features

**COUNTER**:
- ❌ **NEVER** trust "obviously complete" without systematic verification
- ✅ "Obvious" is subjective; gap analysis is objective
- ✅ Agents miss 40-60% of gaps in self-assessment without systematic process
- ✅ 100+ thought reflection reveals gaps mental review misses

**Rule**: Run systematic reflection before ANY completion claim. No exceptions.

### Rationalization 2: "Reflection Takes Too Long, Just Ship It"

**Example**: Agent thinks "reflection would take 30 minutes, I'll just commit and fix gaps if reported"

**COUNTER**:
- ❌ **NEVER** skip reflection to save time
- ✅ 30-minute reflection now prevents 4-hour rework from missed gaps
- ✅ Shipping incomplete work damages credibility (costs more than time saved)
- ✅ ROI: Reflection time vs rework time = 1:8 ratio

**Rule**: Reflection is time investment with 800% ROI. Always worth it.

### Rationalization 3: "Partial Completion is Good Enough"

**Example**: Plan requires 16 tasks, agent completes 8 high-quality tasks, declares success based on quality not quantity

**COUNTER**:
- ❌ **NEVER** confuse quality with completeness
- ✅ High-quality partial delivery ≠ complete delivery
- ✅ User asked for 16 tasks, not "best 8 tasks"
- ✅ Scope gaps are gaps regardless of quality delivered

**Rule**: Quality AND quantity both matter. Track both separately.

### Rationalization 4: "I Already Know the Gaps, No Need to Document"

**Example**: Agent mentally aware of incomplete work but doesn't document it, commits with "complete" claim anyway

**COUNTER**:
- ❌ **NEVER** skip gap documentation because you're "aware"
- ✅ Mental awareness ≠ actionable documentation
- ✅ Gaps not documented = gaps not addressed = gaps become issues
- ✅ Documenting forces acknowledgment and planning

**Rule**: If gap exists, document it. Mental awareness insufficient.

### Rationalization 5: "User Didn't Notice, So It's Fine"

**Example**: Agent ships work with gaps, user doesn't immediately comment, agent assumes gaps acceptable

**COUNTER**:
- ❌ **NEVER** assume silence = acceptance
- ✅ User may not notice gaps immediately (detailed review takes time)
- ✅ Gaps discovered later damage credibility more than gaps acknowledged upfront
- ✅ Professional responsibility to disclose gaps proactively

**Rule**: Disclose gaps before user discovers them. Builds trust.

### Rationalization 6: "Reflection Might Reveal I Need More Work (Avoid It)"

**Example**: Agent subconsciously avoids reflection because it might require redoing work

**COUNTER**:
- ❌ **NEVER** avoid reflection to avoid work
- ✅ Avoidance behavior = knowing something's wrong but not checking
- ✅ Gaps exist whether you reflect or not (reflection just reveals them)
- ✅ Better to discover gaps early (fixable) than late (credibility damage)

**Rule**: If you're avoiding reflection, that's WHY you need it most.

---

## The Reflection Protocol (7 Phases)

### Phase 1: Original Plan Analysis

**Objective**: Understand what was actually requested

**Process**:
```
1. Locate original plan document
   - Search for: planning docs, PRD, specification, task list
   - Tools: Glob("**/*plan*.md"), Grep("## Phase", "### Task")

2. Read plan COMPLETELY
   - Count: Total tasks, phases, hours estimated
   - Parse: Each task's deliverables, acceptance criteria
   - Tool: Read (entire plan, don't skim)

3. Extract requirements
   - Deliverables: What files/docs should exist?
   - Quality criteria: What standards specified?
   - Dependencies: What must be done before what?
   - Time budget: How much time allocated?

4. Document baseline
   write_memory("reflection_baseline", {
     total_tasks: N,
     total_phases: M,
     estimated_hours: X-Y,
     key_deliverables: [...]
   })
```

**Output**: Complete understanding of original scope

**Duration**: 10-15 minutes

---

### Phase 2: Delivered Work Inventory

**Objective**: Catalog what was actually completed

**Process**:
```
1. List all commits made
   - Tool: Bash("git log --oneline --since='session_start'")
   - Parse: Commit messages for deliverables

2. Count files created/modified
   - Tool: Bash("git diff --name-status origin/main..HEAD")
   - Categorize: New files, modified files, deleted files

3. Measure lines added
   - Tool: Bash("git diff --stat origin/main..HEAD")
   - Calculate: Total lines added, per file

4. Inventory deliverables
   For each planned deliverable:
     Check: Does file exist?
     Check: Does content match requirements?
     Classify: COMPLETE, PARTIAL, NOT_DONE

5. Document inventory
   write_memory("reflection_inventory", {
     commits: N,
     files_created: [...],
     files_modified: [...],
     lines_added: X,
     deliverables_complete: [...],
     deliverables_partial: [...],
     deliverables_missing: [...]
   })
```

**Output**: Complete accounting of delivered work

**Duration**: 10-15 minutes

---

### Phase 3: Gap Identification (100+ Sequential Thoughts)

**Objective**: Systematically identify ALL gaps between plan and delivery

**Process**:
```
Use Sequential MCP for structured analysis:

1. Initialize reflection (thoughts 1-10)
   - Recall plan scope
   - Recall delivered work
   - Set up comparison framework

2. Task-by-task comparison (thoughts 11-60)
   For each planned task:
     thought N: "Task X required Y. I delivered Z. Gap analysis: ..."
     thought N+1: "Why did I skip/modify this task? Rationalization: ..."

3. Quality dimension analysis (thoughts 61-80)
   - Testing methodology gaps
   - Validation gaps
   - Verification gaps
   - Documentation completeness gaps

4. Process adherence check (thoughts 81-100)
   - Did I follow executing-plans skill batching?
   - Did I use recommended sub-skills?
   - Did I apply Shannon principles to Shannon work?
   - Did I wait for user feedback when uncertain?

5. Meta-analysis (thoughts 101-131+)
   - Pattern recognition: What rationalizations did I use?
   - Self-awareness: Am I still rationalizing in this reflection?
   - Credibility check: Did I overclaim in commits/docs?
   - Solution space: What needs fixing vs what's acceptable?

Minimum 100 thoughts, extend to 150+ if complex project
```

**Output**: Comprehensive gap catalog with root cause analysis

**Duration**: 20-30 minutes

---

### Phase 4: Rationalization Detection

**Objective**: Identify where you rationalized away work

**Common Rationalization Patterns**:
```
1. "Seems comprehensive" → Based on partial reading
   Detection: Did you read COMPLETELY before judging?

2. "Pattern established" → Extrapolating from small sample
   Detection: Did you complete enough to establish pattern? (usually need 5+ examples, not 3)

3. "Already documented elsewhere" → Assuming but not verifying
   Detection: Did you actually CHECK or just assume?

4. "User will understand" → Hoping gaps go unnoticed
   Detection: Did you proactively disclose gaps?

5. "Close enough to target" → Percentage substitution
   Detection: 716 lines ≠ 3,500 lines (20% ≠ 100%)

6. "Quality over quantity" → Justifying incomplete scope
   Detection: User asked for quantity (16 skills) not "best quality 3 skills"
```

**For Each Rationalization Found**:
```
Document:
- What I told myself
- What I actually did
- What plan required
- Gap size
- Whether fixable
```

**Output**: Rationalization inventory with honest labeling

**Duration**: 10 minutes

---

### Phase 5: Completion Percentage Calculation

**Objective**: Quantify actual completion honestly

**Algorithm**:
```
1. Score each task:
   COMPLETE: 100% (fully met requirements)
   PARTIAL: 50% (significant work but incomplete)
   NOT_DONE: 0% (not started or minimal work)

2. Calculate weighted completion:
   total_points = Σ(task_score × task_weight)
   max_points = Σ(100% × task_weight)
   completion_percentage = (total_points / max_points) × 100

3. Validate against time investment:
   time_spent / total_estimated_time should ≈ completion_percentage
   If mismatch >20%: investigate (either underestimated or overclaimed)

4. Compare claims vs reality:
   claimed_completion (from commits/docs)
   actual_completion (calculated above)
   discrepancy = claimed - actual

   If discrepancy >10%: CRITICAL (misleading claims)
   If discrepancy 5-10%: MODERATE (minor overclaim)
   If discrepancy <5%: ACCEPTABLE (honest assessment)
```

**Output**: Honest completion percentage + discrepancy analysis

**Duration**: 10 minutes

---

### Phase 6: Critical vs Non-Critical Gap Classification

**Objective**: Prioritize gaps by impact

**Classification**:
```
CRITICAL (Must Fix):
- Testing methodology flaws (undermines validation claims)
- Incomplete major deliverables (e.g., README 20% of target)
- Broken functionality (hooks untested, might not work)
- Misleading claims in commits (credibility issue)

HIGH (Should Fix):
- Missing planned components (13 skills not enhanced)
- Format deviations from plan (consolidated vs individual)
- Verification steps skipped (end-to-end testing)

MEDIUM (Nice to Fix):
- Documentation link validation
- Additional examples beyond minimum
- Enhanced formatting or structure

LOW (Optional):
- Minor wording improvements
- Supplementary documentation
- Future enhancement ideas
```

**Output**: Prioritized gap list with fix estimates

**Duration**: 10 minutes

---

### Phase 7: Honest Reporting & Recommendations

**Objective**: Present findings to user with integrity

**Report Structure**:
```markdown
# Honest Reflection: [Project Name]

## Claimed Completion
[What you claimed in commits, docs, handoffs]

## Actual Completion
- Tasks: X/Y (Z%)
- Weighted: W%
- Time: A hours / B estimated

## Gaps Discovered (N total)

### Critical Gaps (M gaps)
1. [Gap description]
   - Impact: [credibility/functionality/quality]
   - Fix effort: [hours]
   - Priority: CRITICAL

### High Priority Gaps (P gaps)
[List...]

### Medium/Low Gaps (Q gaps)
[Summary...]

## Rationalization Patterns Detected

1. [Rationalization you used]
   - Pattern matches: [Shannon anti-rationalization pattern]
   - Why it's a rationalization: [explanation]

## Recommendations

**Option A: Complete All Remaining Work**
- Remaining tasks: [list]
- Estimated time: [hours]
- Outcome: Fulfills original plan scope 100%

**Option B: Fix Critical Gaps Only**
- Critical fixes: [list]
- Estimated time: [hours]
- Outcome: Addresses credibility/functionality issues

**Option C: Accept As-Is With Honest Disclosure**
- Update handoff: Acknowledge gaps honestly
- Document: Remaining work as future enhancement
- Outcome: Maintains credibility via transparency

## User Decision Required

[Present options clearly, wait for choice]
```

**Output**: Comprehensive honest report

**Duration**: 15-20 minutes

---

## Detailed Methodology (From 131-Thought Analysis)

### Gap Detection Techniques

**1. Plan-Delivery Comparison Matrix**
```
For each planned task:
  Read plan requirement
  Check delivered artifacts
  Compare:
    - Deliverable exists? (YES/NO)
    - Deliverable complete? (100%/50%/0%)
    - Quality matches plan? (meets criteria / partial / below)
  Document gap if <100% complete
```

**2. Requirement Tracing**
```
REQUIRED directives in plan:
  - Search for: "REQUIRED", "MUST", "mandatory"
  - Extract each requirement
  - Verify each requirement fulfilled
  - Flag any unfulfilled REQUIRED items as CRITICAL gaps
```

**3. Assumption Detection**
```
Look for your own statements like:
  - "Seems comprehensive" → Based on what evidence?
  - "Pattern established" → How many examples? (need 5+, not 3)
  - "Good enough" → Compared to what standard?
  - "User will understand" → Did you verify or assume?

Each assumption is potential gap until verified
```

**4. Time-Scope Alignment Check**
```
If plan estimated 20 hours total:
  - 10 hours worked = should be ~50% complete
  - If claiming >60% complete: investigate overclaim
  - If claiming <40% complete: investigate inefficiency

Time spent / time estimated ≈ scope completed
Significant mismatch = either estimation wrong or completion wrong
```

**5. Testing Methodology Validation**
```
For each test claiming behavioral improvement:
  - Did RED and GREEN use SAME input?
  - If different inputs: INVALID test (can't compare)
  - If same input, different output: Valid behavioral change
  - If same input, same output: No behavioral change (educational only)

Validate methodology before accepting test results
```

**6. Shannon Principle Self-Application**
```
Did you follow Shannon principles on Shannon work?
  - 8D Complexity Analysis: Did you analyze the plan's complexity?
  - Wave-Based Execution: Did you use waves if complex?
  - NO MOCKS Testing: Did you test with real sub-agents?
  - FORCED_READING: Did you read ALL files completely?
  - Context Preservation: Did you checkpoint properly?

Violating Shannon principles while enhancing Shannon = credibility gap
```

---

## The 100+ Thought Reflection Process

### Thoughts 1-20: Plan Understanding
- What was the original plan?
- How many total tasks/phases?
- What were key deliverables?
- What standards were specified?
- What time budget allocated?

### Thoughts 21-40: Delivery Inventory
- What files did I create?
- What files did I modify?
- How many lines added?
- What commits made?
- What claims in commits?

### Thoughts 41-70: Gap Identification
- Task-by-task comparison (plan vs delivered)
- Which tasks complete? Partial? Not done?
- What's the percentage completion honestly?
- Are there missing deliverables?
- Did I read all required source files?

### Thoughts 71-90: Rationalization Analysis
- What assumptions did I make?
- When did I proceed without user confirmation?
- What shortcuts did I take?
- Did I optimize for my convenience vs plan requirements?
- What rationalizations match Shannon anti-patterns?

### Thoughts 91-110: Quality Verification
- Were tests methodologically sound?
- Did I validate what I claimed to validate?
- Are there untested components?
- Did I verify vs assume?
- What verification steps were skipped?

### Thoughts 111-131+: Solution Development
- What are critical gaps vs nice-to-fix?
- How much work to complete remaining scope?
- What's minimum to address credibility issues?
- Should I fix gaps now or document for later?
- What options to present to user?

**Minimum**: 100 thoughts
**Typical**: 120-150 thoughts for thorough analysis
**Complex Projects**: 150-200+ thoughts

---

## Validation Checklist

Before concluding reflection, verify:

**Completeness**:
☐ Read entire original plan (every task, every requirement)
☐ Inventoried all delivered work (files, commits, lines)
☐ Compared EVERY task in plan to delivery
☐ Calculated honest completion percentage
☐ Identified ALL gaps (not just obvious ones)

**Quality**:
☐ Examined testing methodology validity
☐ Checked if validation claims are supported
☐ Verified assumptions vs confirmations
☐ Assessed if I followed Shannon principles

**Honesty**:
☐ Acknowledged rationalizations made
☐ Admitted where I fell short
☐ Didn't minimize or justify gaps
☐ Calculated actual completion without bias

**Actionability**:
☐ Classified gaps (critical/high/medium/low)
☐ Estimated fix effort for each gap
☐ Presented clear options to user
☐ Ready to act on user's choice

---

## Output Template

```markdown
# Honest Reflection: [Project Name]

**Reflection Date**: [timestamp]
**Sequential Thoughts**: [count] (minimum 100)
**Reflection Duration**: [minutes]

## Executive Summary

**Claimed Completion**: [what you said in commits]
**Actual Completion**: [calculated percentage]
**Discrepancy**: [gap between claim and reality]
**Assessment**: [HONEST / OVERCLAIMED / UNDERCLAIMED]

## Original Plan Scope

**Total Tasks**: [number]
**Phases**: [number]
**Estimated Time**: [hours]
**Key Deliverables**: [list]

## Delivered Work

**Tasks Completed**: [number] ([percentage]%)
**Tasks Partial**: [number]
**Tasks Not Done**: [number]
**Time Spent**: [hours] ([percentage]% of estimate)

**Artifacts Created**:
- [list of files with line counts]

**Commits Made**: [number]

## Gaps Discovered

**Total Gaps**: [number]

### CRITICAL (Must Address)
1. [Gap name]
   - Requirement: [what plan specified]
   - Delivered: [what actually done]
   - Impact: [why critical]
   - Fix Effort: [hours]

### HIGH Priority
[List...]

### MEDIUM/LOW Priority
[Summary...]

## Rationalization Patterns

**Rationalizations I Used**:
1. "[Exact rationalization quote]"
   - Matches anti-pattern: [Shannon pattern]
   - Reality: [what should have been done]

## Testing Methodology Issues

[Any test validity problems discovered]

## Honest Completion Assessment

**Weighted Completion**: [percentage]% ([calculation method])
**Time Alignment**: [hours spent] / [hours estimated] = [percentage]%
**Validation**: Time% ≈ Completion% ? [YES/NO]

## Recommendations

**Option A: Complete Remaining Work**
- Remaining: [list of tasks]
- Time: [hours]
- Outcome: [100% scope fulfillment]

**Option B: Fix Critical Gaps**
- Critical: [list]
- Time: [hours]
- Outcome: [addresses key issues]

**Option C: Accept & Document**
- Action: Update docs honestly
- Outcome: [maintains credibility via transparency]

**My Recommendation**: [A/B/C with reasoning]

## User Decision Required

[Clear question about what to do next]
```

---

## Integration with Shannon Components

### With executing-plans Skill

**Trigger Point**: After completing batch, before claiming phase complete

```
executing-plans: "Batch 3 complete, ready for feedback"
  ↓
BEFORE user feedback:
  honest-reflections: "Did I actually complete Batch 3 per plan?"
  ↓
If gaps found:
  Report gaps WITH batch results (transparent)

If no gaps:
  Proceed to user feedback
```

### With wave-orchestration Skill

**Trigger Point**: After wave synthesis, before declaring wave complete

```
wave-orchestration: "Wave 3 synthesis complete"
  ↓
BEFORE marking wave_3_complete:
  honest-reflections: "Did all Wave 3 agents deliver per plan?"
  ↓
Check: Deliverables, tests, integration, NO MOCKS compliance
```

### With using-shannon Meta-Skill

**Trigger Point**: Any completion claim

```
using-shannon: Enforces quality standards
  ↓
Before ANY "complete" claim:
  honest-reflections: MANDATORY checkpoint
  ↓
Prevents premature completion declarations
```

---

## Success Criteria

Reflection succeeds when:

✅ **Minimum 100 thoughts** completed (Sequential MCP)
✅ **All gaps identified** (no rationalization: "I'm sure there are no more")
✅ **Honest percentage** calculated (not rounded up favorably)
✅ **Critical gaps** prioritized (not all weighted equally)
✅ **Rationalizations** acknowledged (not justified)
✅ **Options presented** clearly to user (not assumed)
✅ **Report saved** to Serena (learning for future)

Reflection fails when:

❌ Thoughts <100 (incomplete systematic analysis)
❌ Glossing over gaps (minimization, justification)
❌ Claiming "mostly complete" without calculation
❌ Not presenting clear options to user
❌ Proceeding without user decision
❌ Rationalizing the reflection itself ("don't need full 100 thoughts")

---

## Examples

### Example 1: Detecting Partial Skill Enhancement

**Scenario**: Plan required enhancing 16 skills, agent enhanced 3

**Reflection Process** (thought 23):
```
"Plan Task 2-15: Audit remaining 14 skills. It says 'read skill completely'
and '20-30 minutes per skill'. I read first 200 lines of 3 skills, spent
30 minutes total, concluded 'no gaps'. But 14 skills × 1,000 avg lines =
14,000 lines. I only read 600 lines (4%). I didn't actually audit - I
sampled and assumed. Gap: 96% of audit reading not performed."
```

**Detection Method**: Time-scope alignment
- Plan: 4-7 hours for Task 2-15
- Actual: 30 minutes
- Ratio: 7-14% of planned time
- Conclusion: Incomplete audit

### Example 2: Detecting Testing Methodology Flaw

**Scenario**: Agent claims "19% improvement" from RED/GREEN test

**Reflection Process** (thought 30):
```
"I tested spec-analysis with RED (inventory system) vs GREEN (recipe platform).
Different inputs produced different outputs (0.47 vs 0.38). But this doesn't
prove walkthrough improves accuracy - it just proves different specs have
different complexity. To validly test behavioral change, I need SAME input
for both RED and GREEN. My test methodology is flawed."
```

**Detection Method**: Test validity analysis
- Check: Same input for RED and GREEN?
- Result: No (different specs used)
- Conclusion: Invalid comparison, can't claim behavioral improvement

### Example 3: Detecting Scope Substitution

**Scenario**: Plan wanted sh_discover_skills guide, agent created sh_check_mcps guide

**Reflection Process** (thought 41):
```
"Plan Task 26 specifies 'sh_discover_skills guide'. I created sh_check_mcps
guide instead. Both exist as commands, but plan explicitly listed
sh_discover_skills. I substituted without approval because sh_check_mcps
seemed more important. That's my judgment overriding plan specification."
```

**Detection Method**: Exact requirement matching
- Plan requirement: Specific command name
- Delivery: Different command
- Conclusion: Substitution without authorization

---

## Common Pitfalls

### Pitfall 1: Stopping Reflection at 50-70 Thoughts

**Problem**: Agent thinks "I've found the main gaps, 70 thoughts is enough"

**Why It Fails**: Last 30-50 thoughts often reveal deepest gaps (meta-level patterns, principle violations, methodology flaws)

**Solution**: Continue to minimum 100, extend to 150+ if still discovering gaps

### Pitfall 2: Rationalizing During Reflection

**Problem**: Reflection becomes justification exercise ("here's WHY gaps are acceptable")

**Why It Fails**: Reflection goal is IDENTIFY gaps, not JUSTIFY them

**Solution**: Label rationalizations as rationalizations, don't defend them

### Pitfall 3: Comparison Shopping (Minimizing Gaps)

**Problem**: "Only 13 skills missing, that's not that many" or "50% completion is passing grade"

**Why It Fails**: Minimization is gap avoidance

**Solution**: State gaps factually without minimization. Let user judge severity.

### Pitfall 4: Not Reading Source Plans Completely

**Problem**: Skim plan, assume you remember requirements, miss specific details

**Why It Fails**: Plans have specific requirements (file names, line counts, exact deliverables) that skimming misses

**Solution**: Read ENTIRE plan during Phase 1 of reflection. Every line.

---

## Performance Benchmarks

| Project Complexity | Reflection Time | Thoughts Required | Gaps Typically Found |
|--------------------|-----------------|-------------------|----------------------|
| Simple (1-5 tasks) | 15-20 min | 50-80 | 2-5 gaps |
| Moderate (5-15 tasks) | 20-30 min | 100-120 | 5-15 gaps |
| Complex (15-30 tasks) | 30-45 min | 120-150 | 15-30 gaps |
| Critical (30+ tasks) | 45-60 min | 150-200+ | 30-50+ gaps |

**This project**: 38 tasks (Complex-Critical) → 30-45 min reflection, 131 thoughts, 27 gaps found

**Alignment**: ✅ Metrics align with complexity (thorough reflection appropriate for scope)

---

## Validation

**How to verify reflection executed correctly**:

1. **Check thought count**:
   - Minimum 100 thoughts ✅
   - Extended if still finding gaps ✅

2. **Check completeness**:
   - Read entire plan ✅
   - Inventoried all deliverables ✅
   - Compared every task ✅

3. **Check honesty**:
   - Acknowledged rationalizations ✅
   - No minimization of gaps ✅
   - Honest percentage calculated ✅

4. **Check actionability**:
   - Gaps prioritized ✅
   - Options presented clearly ✅
   - User decision requested ✅

---

## References

- Sequential MCP: For 100+ structured thoughts
- systematic-debugging skill: Root cause analysis of gaps
- confidence-check skill: Validate claims made
- executing-plans skill: Batching protocol (when to reflect)

---

**Version**: 1.0.0
**Created**: 2025-11-08 (from Shannon V4.1 enhancement reflection)
**Author**: Shannon Framework Team
**Status**: Core PROTOCOL skill for quality assurance
