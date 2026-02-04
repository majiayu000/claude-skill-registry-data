---
name: goal-management
description: |
  FLEXIBLE skill for North Star goal tracking with Serena MCP persistence.
  Parses vague goals into measurable criteria, tracks progress percentages,
  maintains goal history, integrates with wave execution. Prevents goal drift
  and context loss through structured storage. Essential for multi-session projects.

skill-type: FLEXIBLE
shannon-version: ">=4.0.0"

# MCP INTEGRATION
mcp-requirements:
  required:
    - name: serena
      purpose: Persistent goal storage in knowledge graph (shannon/goals)
      fallback: ERROR - Cannot manage goals without persistent storage
  recommended: []
  conditional: []

# COMPOSITION
required-sub-skills: []
optional-sub-skills:
  - context-preservation
  - wave-orchestration

# PERMISSIONS
allowed-tools: [Serena, Read, Write, Grep]
model: sonnet
---

# Goal Management Skill

## Purpose

This skill implements Shannon Framework's North Star goal tracking system through structured goal parsing, progress monitoring, and Serena MCP persistence. It transforms vague aspirations into measurable objectives and ensures goals survive context compaction.

**Core Value**: Guarantees goal alignment across multi-session projects by maintaining persistent, measurable goal state with history tracking.

## When to Use

Use this skill in these situations:

**MANDATORY (Must Use)**:
- User provides project specification with goals (parse immediately)
- User asks "What's our goal?" or "What's our progress?"
- Before wave execution (validate wave aligns with goal)
- After wave completion (update goal progress)
- During checkpoint creation (include goal state)

**RECOMMENDED (Should Use)**:
- User sets multiple concurrent goals (establish priority)
- Complex projects (complexity ≥ 0.50) needing North Star
- Multi-session projects (goal persistence critical)
- When goal clarity is low (parse and validate)

**CONDITIONAL (May Use)**:
- User requests goal history review
- Retrospective analysis (velocity, patterns)
- Goal completion ceremonies

DO NOT rationalize skipping goal management because:
- ❌ "This goal is simple and obvious" → Vague goals lead to drift
- ❌ "I'll remember the goal" → Context compaction erases memory
- ❌ "User didn't explicitly ask for tracking" → Goal tracking is Shannon infrastructure
- ❌ "Goal is already clear" → Parsing adds structure and measurement
- ❌ "Only one goal, no need to store" → Even single goals need persistence

## Core Competencies

1. **Goal Parsing**: Converts vague goals into structured format with measurable criteria
2. **Progress Tracking**: Calculates completion percentages based on milestone status
3. **Serena Storage**: Persists goals to shannon/goals namespace with rich metadata
4. **Priority Management**: Supports multiple goals with North Star designation
5. **History Tracking**: Maintains goal lifecycle (created, updated, completed, archived)
6. **Wave Integration**: Links goals to wave execution for alignment validation

## Inputs

**Required:**
- `mode` (string): Operation mode
  - `"set"`: Create new goal or update existing
  - `"list"`: Display all active goals
  - `"show"`: Display specific goal details
  - `"update"`: Update goal progress or metadata
  - `"complete"`: Mark goal as complete
  - `"clear"`: Remove goals (archive)
  - `"history"`: Show goal history
  - `"restore"`: Restore goal from checkpoint

**Mode-Specific Inputs:**

**For "set" mode:**
- `goal_text` (string): User's goal description (can be vague)
- `priority` (string): "north-star" | "high" | "medium" | "low" (default: "medium")
- `deadline` (optional string): ISO date (YYYY-MM-DD)

**For "update" mode:**
- `goal_id` (string): Goal identifier from Serena
- `progress` (optional integer): 0-100 percentage
- `notes` (optional string): Progress notes

**For "complete" mode:**
- `goal_id` (string): Goal to mark complete

**For "show" mode:**
- `goal_id` (string): Goal to display

## Workflow

### Mode: EMERGENCY-SET (Fast Path for PreCompact)

**Trigger**: Token usage > 90% OR PreCompact hook active

**Purpose**: Prevent goal loss during context compaction by using fast-path storage

**Process**:
1. Skip detailed milestone parsing (defer to next session)
2. Store minimal goal structure: {goal_text, priority, created_at, needs_parsing: true}
3. Create Serena entity (5 seconds max)
4. Mark: needs_parsing=true for later completion
5. Return: goal_id immediately

**Next Session Recovery**:
- Detect: goals with needs_parsing=true
- Prompt: "Complete goal parsing for GOAL-{id}?"
- Parse: Full milestone structure
- Update: Remove needs_parsing flag

**Priority**: Goal storage completes BEFORE PreCompact checkpoint

---

### Mode: SET - Create or Update Goal

**Step 1: Parse Goal Text**
- Action: Extract goal statement and implied criteria
- Input: Raw goal text (e.g., "Build a good e-commerce platform")
- Processing:
  1. Identify vague terms ("good", "better", "quality")
  2. Extract implied features/criteria
  3. Generate measurable milestones
  4. Create goal structure
- Output: Structured goal object

**Step 1.5: Resolve Ambiguous References**
- Action: Eliminate pronouns and ambiguous references
- Detection: Goal contains "it", "this", "that", "them"
- Processing:
  1. Search recent context (last 10 messages) for referent
  2. If found: Replace pronoun with explicit noun
  3. If not found: Prompt user for clarification ("What does 'it' refer to?")
  4. Store: Only fully explicit goal text (no pronouns)
- Example:
  - Input: "Make it production-ready"
  - Detection: "it" is pronoun
  - Search: Find "prototype" in context
  - Resolve: "Make prototype production-ready"
  - Store: Resolved text

**Step 2: Extract Measurable Criteria**
- Action: Convert vague goal into specific, testable criteria
- Processing:
  1. Map features to milestones (auth → "User can register/login")
  2. Assign weights (auth: 40%, payments: 30%, catalog: 30%)
  3. Define completion tests (functional tests exist and pass)
  4. Set success threshold (typically 100% for North Star goals)
- Output: Array of milestones with weights

**Step 3: Check for Existing Goal**
- Tool: Serena MCP `search_nodes` with query="shannon/goals"
- Action: Check if goal with similar intent already exists
- Logic: If exists → prompt user (replace/merge/create new), else proceed

**Step 4: Create Goal Entity**
- Tool: Serena MCP `create_entities`
- Entity Structure:
  ```json
  {
    "name": "goal-{timestamp}",
    "entityType": "shannon-goal",
    "observations": [
      {
        "goal_id": "GOAL-20251103T143000",
        "goal_text": "Build e-commerce platform with auth, payments, catalog",
        "priority": "north-star",
        "status": "active",
        "progress": 0,
        "created_at": "2025-11-03T14:30:00.000Z",
        "updated_at": "2025-11-03T14:30:00.000Z",
        "milestones": [
          {
            "name": "User Authentication",
            "description": "Users can register and login",
            "weight": 40,
            "status": "pending",
            "completion_criteria": "Functional auth tests pass"
          },
          {
            "name": "Payment Processing",
            "description": "Users can checkout with credit cards",
            "weight": 30,
            "status": "pending",
            "completion_criteria": "Stripe integration tests pass"
          },
          {
            "name": "Product Catalog",
            "description": "Products displayed with search",
            "weight": 30,
            "status": "pending",
            "completion_criteria": "Catalog functional tests pass"
          }
        ],
        "deadline": null,
        "wave_links": []
      }
    ]
  }
  ```

**Step 5: Create Relations**
- Tool: Serena MCP `create_relations`
- Relations:
  - goal → project (links goal to current project)
  - goal → previous_goal (if replacing)

**Step 6: Confirm to User**
- Display: Goal ID, parsed criteria, milestones, priority
- Include: Example progress update command
- Output: Goal set successfully message

### Mode: LIST - Display All Goals

**Step 1: Query Goals**
- Tool: Serena MCP `search_nodes` with query="shannon-goal active"
- Filters: status="active"

**Step 2: Sort by Priority**
- Order: north-star, high, medium, low
- Within priority: Sort by created_at (oldest first)

**Step 3: Format Output**
- Display table:
  ```
  ID              | Goal                           | Priority    | Progress | Status
  ----------------|--------------------------------|-------------|----------|--------
  GOAL-202511...  | E-commerce platform            | North Star  | 66%      | Active
  GOAL-202511...  | Add social login               | High        | 0%       | Active
  ```

**Step 4: Highlight North Star**
- Mark North Star goal with emoji/highlighting
- Show next milestone for North Star

### Mode: UPDATE - Update Goal Progress

**Step 1: Retrieve Goal**
- Tool: Serena MCP `open_nodes` with goal_id
- Validate: Goal exists and is active

**Step 2: Update Progress**
- If `progress` provided: Set directly (manual override)
- If not provided: Calculate from milestone status
  - Count completed milestones
  - Weight by milestone weights
  - progress = sum(completed_weights)

**Step 3: Update Milestone Status**
- Mark milestones complete if criteria met
- Example: "Auth tests passing" → mark "User Authentication" complete

**Step 3.5: Health Check Completed Milestones**
- Action: Verify previously completed milestones still meet criteria
- Trigger: Update mode OR checkpoint creation
- Processing:
  1. Query each "complete" milestone's completion criteria
  2. Check: Are tests still passing? (query test results)
  3. If failing: Mark milestone status="regression"
  4. Adjust: Recalculate progress (exclude regressed milestones)
  5. Alert: "⚠️ Regression detected in [milestone name]"
- Purpose: Maintain progress accuracy despite regressions
- Integration: Called automatically in update mode

**Step 4: Store Updated Goal**
- Tool: Serena MCP `add_observations`
- Update: updated_at timestamp, progress, milestone statuses

**Step 5: Check Completion**
- If progress >= 100: Prompt user to mark complete
- Display: "Goal appears complete. Run /shannon:goal complete {goal_id}?"

### Mode: COMPLETE - Mark Goal Complete

**Step 1: Retrieve Goal**
- Tool: Serena MCP `open_nodes`
- Validate: Goal exists

**Step 2: Archive Goal**
- Update: status="completed", completed_at=now()
- Create: completion observation with final notes

**Step 3: Show Goal Velocity**
- Calculate: days from created_at to completed_at
- Display: "Goal completed in X days"

**Step 4: Store in History**
- Tool: Serena MCP `add_observations`
- Relation: goal → project (mark as completed_goal)

### Mode: HISTORY - Show Goal History

**Step 1: Query Completed Goals**
- Tool: Serena MCP `search_nodes` with status="completed"
- Sort: completed_at descending (most recent first)

**Step 2: Calculate Metrics**
- Goal velocity: average days per goal
- Completion rate: completed / (completed + abandoned)
- Most common goal types

**Step 3: Display Timeline**
- Show: Goal, completed date, duration, progress
- Highlight: Patterns (recurring goal types)

### Mode: RESTORE - Restore from Checkpoint

**Step 1: Load Checkpoint**
- Input: checkpoint_id from context-restoration skill
- Extract: goals array from checkpoint metadata

**Step 2: Reconcile Goals**
- Compare: checkpoint goals vs current Serena goals
- Logic: If goal_id exists → update, else create

**Step 3: Restore Goal State**
- Update: progress, milestones, wave_links
- Preserve: created_at, goal_id
- Update: restored_at timestamp

## Anti-Rationalization Section

**🚨 PROTOCOL ENFORCEMENT 🚨**

This section addresses every rationalization pattern from RED phase baseline testing:

### Rationalization 1: "This goal is simple and obvious"

**Detection**: User states simple goal, skill skipped due to perceived clarity

**Violation**: Accept vague goal without parsing or structure

**Counter-Argument**:
- "Build good platform" → What features make it "good"?
- "Simple" goals still need milestones for progress tracking
- Vague goals lead to scope creep (adding undefined "goodness")
- Parsing cost: 30 seconds. Drift cost: hours of rework
- RED Phase Scenario 1: Vague goals accepted without measurement

**Protocol**: Parse ALL goals, regardless of perceived simplicity. Structure ensures alignment.

---

### Rationalization 2: "I'll remember the goal"

**Detection**: Single-session project, relying on memory instead of storage

**Violation**: Skip Serena storage, keep goal in context window

**Counter-Argument**:
- Human memory fails under cognitive load
- Context compaction erases non-stored data (RED Phase Scenario 3)
- 20-30 messages = goal forgotten
- Serena storage: permanent, queryable
- Even single-session projects get interrupted

**Protocol**: Store ALL goals in Serena, period. Memory is not reliable. Context window is temporary.

---

### Rationalization 3: "User didn't ask for goal tracking"

**Detection**: User states goal but doesn't request tracking explicitly

**Violation**: Skip goal management because request is implicit not explicit

**Counter-Argument**:
- Goal tracking is Shannon infrastructure, not user's job
- Users assume goals persist (like saving files)
- Shannon Framework mandates goal alignment
- RED Phase Scenario 2: User asks progress, system cannot answer
- Tracking is automatic, not optional

**Protocol**: Goal tracking is framework responsibility. Parse and store automatically whenever goal is stated.

---

### Rationalization 4: "Goal is already clear, no parsing needed"

**Detection**: User provides specific-sounding goal, parsing skipped

**Violation**: Accept goal without milestone extraction

**Counter-Argument**:
- "Clear" goals still need structured milestones for progress tracking
- Example: "Launch MVP" → What features define MVP?
- Parsing extracts implicit criteria
- Without milestones: Cannot calculate progress percentage
- RED Phase Scenario 2: No measurable progress tracking

**Protocol**: Parse all goals to extract milestones. Even "clear" goals need structure for measurement.

---

### Rationalization 5: "Only one goal, no need to store"

**Detection**: Single goal, complexity low, storage skipped

**Violation**: Skip Serena storage for "simple" single-goal projects

**Counter-Argument**:
- Context compaction doesn't skip single-goal projects
- Interruptions happen regardless of goal count
- RED Phase Scenario 3: Goal lost mid-project
- Future goals may be added (needs existing storage)
- Storage overhead: 5 seconds. Loss cost: hours

**Protocol**: Store all goals, even if only one. Context loss is independent of goal count.

---

### Rationalization 6: "Waves are obviously aligned with goal"

**Detection**: Wave execution without explicit goal validation

**Violation**: Execute waves without checking goal-wave alignment

**Counter-Argument**:
- Wave drift occurs without explicit validation
- RED Phase Scenario 6: Deliverables disconnect from goal
- Example: "Auth system" wave delivers OAuth but goal needs email/password
- Validation cost: 10 seconds. Drift cost: wasted wave execution
- Shannon Framework requires goal-wave alignment

**Protocol**: Before wave execution, validate wave deliverables match goal milestones. Update goal after wave.

---

### Rationalization 7: "Goal is clear even without numbers"

**Detection**: Goal uses qualitative terms without metrics
**Examples**: "More scalable", "Better performance", "Higher quality"

**Violation**: Accept goal without forcing quantification

**Counter-Argument**:
- Qualitative = subjective, cannot definitively mark complete
- "Scalable" → Define: 10K users? 100ms response?
- Shannon Framework requires measurable success criteria
- Vague completion = goal never truly finished

**Protocol**: For qualitative goals, force quantification:
1. Detect qualitative term ("scalable", "better", "quality")
2. Prompt: "Define 'scalable': [specific metric]?"
3. User provides number (10K concurrent users, 100ms p95)
4. Store: Quantified milestone with testable criteria

---

### Enforcement Mechanism

This skill is **FLEXIBLE** type but has mandatory invocation points:
- When user states goal → `set` mode
- When user asks progress → `list` or `show` mode
- Before wave execution → validate alignment
- After wave completion → `update` mode

**Violation Detection**:
If you find yourself thinking any of these:
- "This goal is too simple for tracking"
- "I'll remember the goal without storing"
- "User didn't ask for tracking"
- "Goal is already clear enough"
- "Only one goal, no storage needed"
- "Waves are obviously aligned"

**STOP**. You are rationalizing. Return to workflow. Parse and store the goal.

## Outputs

**For "set" mode:**
```json
{
  "success": true,
  "goal_id": "GOAL-20251103T143000",
  "goal_text": "Build e-commerce platform with auth, payments, catalog",
  "priority": "north-star",
  "milestones": [
    {
      "name": "User Authentication",
      "weight": 40,
      "status": "pending"
    },
    {
      "name": "Payment Processing",
      "weight": 30,
      "status": "pending"
    },
    {
      "name": "Product Catalog",
      "weight": 30,
      "status": "pending"
    }
  ],
  "progress": 0,
  "storage": "serena://shannon/goals/GOAL-20251103T143000",
  "next_action": "Execute Wave 1 for User Authentication milestone"
}
```

**For "list" mode:**
```json
{
  "success": true,
  "goals": [
    {
      "goal_id": "GOAL-20251103T143000",
      "goal_text": "Build e-commerce platform",
      "priority": "north-star",
      "progress": 66,
      "status": "active",
      "next_milestone": "Product Catalog"
    },
    {
      "goal_id": "GOAL-20251103T150000",
      "goal_text": "Add social login",
      "priority": "high",
      "progress": 0,
      "status": "active"
    }
  ],
  "north_star": "GOAL-20251103T143000"
}
```

**For "update" mode:**
```json
{
  "success": true,
  "goal_id": "GOAL-20251103T143000",
  "progress": 66,
  "progress_change": "+30%",
  "milestones_completed": ["User Authentication", "Payment Processing"],
  "milestones_remaining": ["Product Catalog"],
  "estimated_completion": "2025-11-10 (based on velocity)"
}
```

## Success Criteria

This skill succeeds if:

1. ✅ **Goal Parsed**: Vague goal converted to structured format with measurable milestones
2. ✅ **Serena Storage**: Goal entity created in shannon/goals namespace
3. ✅ **Progress Trackable**: Progress percentage calculable from milestone status
4. ✅ **Survives Compaction**: Goal retrievable after context loss
5. ✅ **Wave Integration**: Goals linked to wave execution with alignment validation

Validation:
```python
def validate_goal_management(goal_id):
    # Check 1: Goal exists in Serena
    goal = serena.open_nodes([goal_id])
    assert goal is not None

    # Check 2: Has structured milestones
    data = json.loads(goal.observations[0])
    assert "milestones" in data
    assert len(data["milestones"]) > 0
    assert all("weight" in m for m in data["milestones"])

    # Check 3: Progress calculable
    progress = calculate_progress(data["milestones"])
    assert 0 <= progress <= 100

    # Check 4: Can restore after compaction
    # (Simulate compaction by creating new context)
    restored_goal = serena.search_nodes("shannon-goal active")
    assert goal_id in [g.name for g in restored_goal]
```

## Advanced Features

### Milestone Dependency Validation

**Purpose**: Prevent circular dependencies in milestone structure

**When**: Goal creation (set mode)

**Process**:
1. Extract dependencies from milestone descriptions
2. Build dependency graph (milestones as nodes, dependencies as edges)
3. Perform topological sort to check for cycles (DAG validation)
4. If cycle detected: Alert user with cycle path
5. Recommend: Break cycle by removing dependency or splitting milestone

**Example**:
- Milestone A: "Auth system" (depends on "Database")
- Milestone B: "Database" (depends on "Auth for admin")
- Detection: Cycle (A→B→A)
- Alert: "⚠️ Cannot execute: circular dependency detected (Auth→Database→Auth)"
- Fix: Remove admin auth dependency from database milestone

---

### Scope Monitoring

**Purpose**: Detect and alert on implicit goal expansion (scope creep)

**Trigger**: User adds features to active goal context

**Process**:
1. Track: Features mentioned in conversations about active goal
2. Compare: Current features vs original milestone list
3. Count: New features not in original milestones
4. Threshold: 2+ additions = scope creep alert
5. Recommend: "Update goal scope explicitly with /shannon:goal update" OR "Split into new goal"

**Example**:
- Original Goal: "Build auth system" (1 milestone: email/password)
- User mentions: "Add OAuth", "Add 2FA", "Add passwordless login"
- Detection: 3 features added beyond original scope (300% expansion)
- Alert: "⚠️ Scope expanded 3x beyond original goal. Update milestones?"
- Options:
  1. Update goal: Add 3 new milestones
  2. Split: Create "Advanced Auth" as separate goal
  3. Defer: Move to backlog

**Benefits**:
- Prevents hidden scope creep
- Maintains progress accuracy
- Forces explicit goal updates
- Preserves velocity metrics

---

## Common Pitfalls

### Pitfall 1: Accepting Vague Goals Without Structure

**Wrong:**
```
User: "Build a good platform"
Claude: "Got it, building a good platform."
[No parsing, no milestones, no storage]
```

**Right:**
```
User: "Build a good platform"
Claude: "Parsing goal... 'good' implies:
- User authentication (40%)
- Payment processing (30%)
- Product catalog (30%)
Is this correct? [Goal stored in Serena as GOAL-202511...]"
```

**Why**: Vague goals lead to scope creep and drift. **Always parse into measurable criteria**, even if goal seems clear.

---

### Pitfall 2: Skipping Storage for "Simple" Goals

**Wrong:**
```
Single goal project, complexity low.
"I'll keep it in context, no need for Serena storage."
```

**Right:**
```
Even single-goal projects get interrupted.
Storing goal in Serena: shannon/goals/GOAL-202511...
Progress survives context compaction.
```

**Why**: Context compaction doesn't discriminate by complexity. **Always store in Serena**, regardless of goal count.

---

### Pitfall 3: No Wave-Goal Alignment Check

**Wrong:**
```
Executing Wave 2: Auth system implementation.
[No check if auth aligns with goal milestones]
```

**Right:**
```
Validating Wave 2 against goal GOAL-202511...
Goal milestone: "User Authentication" (40% weight)
Wave 2 deliverables: Email/password auth
✅ Alignment verified. Proceeding with wave.
```

**Why**: Waves can drift without explicit validation. **Always validate wave deliverables match goal milestones** before execution.

## Examples

### Example 1: Setting North Star Goal

**Input:**
```json
{
  "mode": "set",
  "goal_text": "Launch MVP with user accounts and payment processing",
  "priority": "north-star"
}
```

**Process:**
1. Parse goal text → Extract features (accounts, payments)
2. Generate milestones:
   - User accounts (50%): Register, login, profile
   - Payment processing (50%): Stripe integration, checkout
3. Create goal entity in Serena (shannon/goals)
4. Set priority=north-star
5. Initialize progress=0

**Output:**
```json
{
  "success": true,
  "goal_id": "GOAL-20251103T143000",
  "goal_text": "Launch MVP with user accounts and payment processing",
  "priority": "north-star",
  "milestones": [
    {"name": "User Accounts", "weight": 50, "status": "pending"},
    {"name": "Payment Processing", "weight": 50, "status": "pending"}
  ],
  "progress": 0,
  "next_action": "Execute Wave 1 for User Accounts milestone"
}
```

---

### Example 2: Updating Progress After Wave

**Input:**
```json
{
  "mode": "update",
  "goal_id": "GOAL-20251103T143000",
  "notes": "Wave 1 complete: Auth tests passing"
}
```

**Process:**
1. Retrieve goal from Serena
2. Check milestone completion criteria
3. "Auth tests passing" → mark "User Accounts" complete
4. Calculate progress: 50% (1 of 2 milestones complete)
5. Update Serena with new progress

**Output:**
```json
{
  "success": true,
  "goal_id": "GOAL-20251103T143000",
  "progress": 50,
  "progress_change": "+50%",
  "milestones_completed": ["User Accounts"],
  "milestones_remaining": ["Payment Processing"],
  "next_action": "Execute Wave 2 for Payment Processing"
}
```

---

### Example 3: Listing Multiple Goals

**Input:**
```json
{
  "mode": "list"
}
```

**Process:**
1. Query Serena for all active goals
2. Sort by priority (north-star first)
3. Format as table
4. Highlight North Star

**Output:**
```
Active Goals:

⭐ North Star Goal:
ID: GOAL-20251103T143000
Goal: Launch MVP with user accounts and payment processing
Progress: 50% (1/2 milestones)
Next: Payment Processing

Other Goals:
ID: GOAL-20251103T150000
Goal: Add social login (Facebook, Google)
Priority: High
Progress: 0%
```

## Validation

How to verify this skill worked correctly:

1. **Goal Stored**: Query Serena `search_nodes("shannon-goal")`, verify goal exists
2. **Milestones Structured**: Open goal, verify milestones array with weights
3. **Progress Calculable**: Verify progress=sum(completed_milestone_weights)
4. **Survives Compaction**: In new session, query goal_id, verify retrieval
5. **Wave Links**: Verify goal.wave_links array populated after wave execution

## Progressive Disclosure

**In SKILL.md** (this file):
- Core goal management workflows (~800 lines)
- Anti-rationalization patterns from RED phase
- Essential examples (set, update, list)

**In examples/** (for deep details):
- `examples/north-star-example.md`: Complete goal lifecycle
- `examples/multi-goal-example.md`: Priority management
- `examples/wave-integration-example.md`: Goal-wave alignment

## References

- Core Documentation: `shannon-plugin/core/PROJECT_MEMORY.md`
- Related Skills: `@context-preservation`, `@wave-orchestration`, `@phase-planning`
- MCP Setup: `/shannon:check_mcps` for Serena MCP configuration
- Commands: `/shannon:north_star`, `/shannon:checkpoint` (both use this skill)

---

**Skill Type**: FLEXIBLE - Adapts to user's goal complexity and project scale
**Version**: 4.0.0
**Last Updated**: 2025-11-03
**Status**: Core
