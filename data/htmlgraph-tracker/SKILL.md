---
name: htmlgraph-tracker
description: HtmlGraph workflow skill combining session tracking, orchestration, and parallel coordination. Activated automatically at session start. Enforces delegation patterns, manages multi-agent workflows, ensures proper activity attribution, and maintains feature awareness. Use when working with HtmlGraph projects, spawning parallel agents, or coordinating complex work.
---

# HtmlGraph Workflow Skill

Use this skill when HtmlGraph is tracking the session to ensure proper activity attribution, documentation, and orchestration patterns. Activate this skill at session start via the SessionStart hook.

---

## 📚 REQUIRED READING

**→ READ [../../../AGENTS.md](../../../AGENTS.md) FOR COMPLETE SDK DOCUMENTATION**

The root AGENTS.md file contains:
- ✅ **Python SDK Quick Start** - Installation, initialization, basic operations
- ✅ **Deployment Instructions** - Using `deploy-all.sh` script
- ✅ **API & CLI Reference** - Alternative interfaces
- ✅ **Best Practices** - Patterns for AI agents
- ✅ **Complete Workflow Examples** - End-to-end scenarios

**This file (SKILL.md) contains Claude Code-specific instructions only.**

**For SDK usage, deployment, and general agent workflows → USE AGENTS.md**

---

## When to Activate This Skill

- At the start of every session when HtmlGraph plugin is enabled
- When the user asks about tracking, features, or session management
- When drift detection warnings appear
- When the user mentions htmlgraph, features, sessions, or activity tracking
- When discussing work attribution or documentation
- When planning multi-agent work or parallel execution
- When using Task tool to spawn subagents
- When coordinating concurrent feature implementation

**Trigger keywords:** htmlgraph, feature tracking, session tracking, drift detection, activity log, work attribution, feature status, session management, orchestrator, parallel, concurrent, delegation, Task tool, multi-agent, spawn agents

---

## Core Responsibilities

### 1. **ORCHESTRATOR MODE - Delegation Over Direct Execution** (CRITICAL)

**CRITICAL: When operating in orchestrator mode, delegate ALL operations except strategic activities.**

**Core Philosophy:** You don't know the outcome before running a tool. What looks like "one bash call" often becomes 2, 3, 4+ calls when handling failures, conflicts, hooks, or errors. Delegation preserves strategic context by isolating tactical execution in subagent threads.

**Operations You MAY Execute Directly:**
- `Task()` - Delegation itself
- `AskUserQuestion()` - Clarifying requirements
- `TodoWrite()` - Tracking work items
- SDK operations - Creating features, spikes, analytics

**ALWAYS Delegate:**
- ✅ Git operations (commit, push, branch, merge) - **ALWAYS DELEGATE**
- ✅ Code changes (multi-file edits, implementation)
- ✅ Research & exploration (codebase searches)
- ✅ Testing & validation (test suites, debugging)
- ✅ Build & deployment (package publishing)
- ✅ Complex file operations (batch operations)

**Why Git MUST be delegated:** Git operations cascade unpredictably (hooks fail, conflicts occur, tests fail in hooks). Context cost: Direct execution = 7+ tool calls vs Delegation = 2 tool calls.

**Decision Framework - Ask yourself:**
1. Will this likely be one tool call? → If uncertain, DELEGATE
2. Does this require error handling? → DELEGATE
3. Could this cascade into multiple operations? → DELEGATE
4. Is this strategic (decisions) or tactical (execution)? → Tactical = DELEGATE

**Delegation Pattern with Task ID:**
```python
from htmlgraph.orchestration import delegate_with_id, get_results_by_task_id

# Generate task ID and enhanced prompt
task_id, prompt = delegate_with_id(
    "Commit and push changes",
    "Files: CLAUDE.md, SKILL.md\nMessage: 'docs: consolidate skills'",
    "general-purpose"
)

# Delegate
Task(prompt=prompt, description=f"{task_id}: Commit and push")

# Retrieve results by task ID (works with parallel tasks!)
results = get_results_by_task_id(sdk, task_id, timeout=120)
if results["success"]:
    print(results["findings"])
```

**See:** `.claude/rules/orchestration.md` for complete orchestrator directives and delegation patterns.

#### Parallel Workflow (6-Phase Process)

When coordinating multiple agents with Task tool, follow this structured workflow:

```
1. ANALYZE   → Check dependencies, assess parallelizability
2. PREPARE   → Cache shared context, partition files
3. DISPATCH  → Generate prompts via SDK, spawn agents in ONE message
4. MONITOR   → Track health metrics per agent
5. AGGREGATE → Collect results, detect conflicts
6. VALIDATE  → Verify outputs, run tests
```

**Quick Start - Parallel Execution:**
```python
from htmlgraph import SDK

sdk = SDK(agent="orchestrator")

# 1. ANALYZE - Check if work can be parallelized
parallel = sdk.get_parallel_work(max_agents=5)
if parallel["max_parallelism"] < 2:
    print("Work sequentially instead")

# 2. PLAN - Get structured prompts with context
plan = sdk.plan_parallel_work(max_agents=3)

if plan["can_parallelize"]:
    # 3. DISPATCH - Spawn all agents in ONE message (critical!)
    for p in plan["prompts"]:
        Task(
            subagent_type="general-purpose",
            prompt=p["prompt"],
            description=p["description"]
        )

    # 4-5. AGGREGATE - After agents complete
    results = sdk.aggregate_parallel_results(agent_ids)

    # 6. VALIDATE
    if results["all_passed"]:
        print("✅ Parallel execution validated!")
```

**When to Parallelize:**
- Multiple independent tasks can run simultaneously
- Work can be partitioned without file conflicts
- Speedup factor > 1.5x
- `sdk.get_parallel_work()` shows `max_parallelism >= 2`

**When NOT to Parallelize:**
- Shared dependencies or file conflicts
- Tasks < 1 minute (overhead not worth it)
- Complex coordination required

**Anti-Patterns to Avoid:**
- ❌ Sequential Task calls (send all in ONE message for true parallelism)
- ❌ Overlapping file edits (partition work to avoid conflicts)
- ❌ No shared context caching (read shared files once, not per-agent)

---

### 2. **Use SDK, Not MCP Tools** (CRITICAL)

**IMPORTANT: For Claude Code, use the Python SDK directly instead of MCP tools.**

**Why SDK over MCP:**
- ✅ **No context bloat** - MCP tool schemas consume precious tokens
- ✅ **Runtime discovery** - Explore all operations via Python introspection
- ✅ **Type hints** - See all available methods without schemas
- ✅ **More powerful** - Full programmatic access, not limited to 3 MCP tools
- ✅ **Faster** - Direct Python, no JSON-RPC overhead

The SDK provides access to ALL HtmlGraph operations without adding tool definitions to your context.

**ABSOLUTE RULE: DO NOT use Read, Write, or Edit tools on `.htmlgraph/` HTML files.**

Use the SDK (or API/CLI for special cases) to ensure all HTML is validated through Pydantic + justhtml.

❌ **FORBIDDEN:**
```python
# NEVER DO THIS
Write('/path/to/.htmlgraph/features/feature-123.html', ...)
Edit('/path/to/.htmlgraph/sessions/session-456.html', ...)
with open('.htmlgraph/features/feature-123.html', 'w') as f:
    f.write('<html>...</html>')
```

✅ **REQUIRED - Use SDK (BEST CHOICE FOR AI AGENTS):**
```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# Work with ANY collection (features, bugs, chores, spikes, epics, phases)
sdk.features    # Features with builder support
sdk.bugs        # Bug reports
sdk.chores      # Maintenance tasks
sdk.spikes      # Investigation spikes
sdk.epics       # Large bodies of work
sdk.phases      # Project phases

# Create features (fluent interface)
feature = sdk.features.create("Title") \
    .set_priority("high") \
    .add_steps(["Step 1", "Step 2"]) \
    .save()

# Edit ANY collection (auto-saves)
with sdk.features.edit("feature-123") as f:
    f.status = "done"

with sdk.bugs.edit("bug-001") as bug:
    bug.status = "in-progress"
    bug.priority = "critical"

# Vectorized batch updates (efficient!)
sdk.bugs.batch_update(
    ["bug-001", "bug-002", "bug-003"],
    {"status": "done", "resolution": "fixed"}
)

# Query across collections
high_priority = sdk.features.where(status="todo", priority="high")
in_progress_bugs = sdk.bugs.where(status="in-progress")

# All collections have same interface
sdk.chores.mark_done(["chore-1", "chore-2"])
sdk.spikes.assign(["spike-1"], agent="claude")
```

**Why SDK is best:**
- ✅ 3-16x faster than CLI (no process startup)
- ✅ Type-safe with auto-complete
- ✅ Context managers (auto-save)
- ✅ Vectorized batch operations
- ✅ Works offline (no server needed)
- ✅ Supports ALL collections (features, bugs, chores, spikes, epics, etc.)

✅ **ALTERNATIVE - Use CLI (for one-off commands):**
```bash
# CLI is slower (400ms startup per command) but convenient for one-off queries
uv run htmlgraph feature create/start/complete
uv run htmlgraph status
```

⚠️ **AVOID - API/curl (use only for remote access):**
```bash
# Requires server + network overhead, only use for remote access
curl -X PATCH localhost:8080/api/features/feat-123 -d '{"status": "done"}'
```

**Why this matters:**
- Direct file edits bypass Pydantic validation
- Bypass justhtml HTML generation (can create invalid HTML)
- Break the SQLite index sync
- Skip event logging and activity tracking
- Can corrupt graph structure and relationships

**NO EXCEPTIONS: NEVER read, write, or edit `.htmlgraph/` files directly.**

Use the SDK for ALL operations including inspection:

```python
# ✅ CORRECT - Inspect sessions/events via SDK
from htmlgraph import SDK
from htmlgraph.session_manager import SessionManager

sdk = SDK(agent="claude-code")
sm = SessionManager()

# Get current session
session = sm.get_active_session(agent="claude-code")

# Get recent events (last 10)
recent = session.get_events(limit=10, offset=session.event_count - 10)
for evt in recent:
    print(f"{evt['event_id']}: {evt['tool']} - {evt['summary']}")

# Query events by tool
bash_events = session.query_events(tool='Bash', limit=20)

# Query events by feature
feature_events = session.query_events(feature_id='feat-123')

# Get event statistics
stats = session.event_stats()
print(f"Total: {stats['total_events']}, Tools: {stats['tools_used']}")
```

❌ **FORBIDDEN - Reading files directly:**
```python
# NEVER DO THIS
with open('.htmlgraph/events/session-123.jsonl') as f:
    events = [json.loads(line) for line in f]

# NEVER DO THIS
tail -10 .htmlgraph/events/session-123.jsonl
```

**Documentation:**
- Complete SDK guide: `docs/SDK_FOR_AI_AGENTS.md`
- Event inspection: `docs/SDK_EVENT_INSPECTION.md`
- Agent best practices: `docs/AGENTS.md`

### 2. Feature Awareness (MANDATORY)
Always know which feature(s) are currently in progress:
- Check active features at session start: run `uv run htmlgraph status`
- Reference the current feature when discussing work
- Alert immediately if work drifts from the assigned feature

### 3. Step Completion (CRITICAL)
**Mark each step complete IMMEDIATELY after finishing it:**
- Use SDK to complete individual steps as you finish them
- Step 0 = first step, step 1 = second step (0-based indexing)
- Do NOT wait until all steps are done - mark each one as you finish
- See "How to Mark Steps Complete" section below for exact commands

### 4. Continuous Tracking (CRITICAL)

**ABSOLUTE REQUIREMENT: Track ALL work in HtmlGraph.**

HtmlGraph tracking is like Git commits - never do work without tracking it.

**Update HtmlGraph immediately after completing each piece of work:**
- ✅ Finished a step? → Mark it complete in SDK
- ✅ Fixed a bug? → Update bug status
- ✅ Discovered a decision? → Document it in the feature
- ✅ Changed approach? → Note it in activity log
- ✅ Completed a task? → Mark feature/bug/chore as done

**Why this matters:**
- Attribution ensures work isn't lost across sessions
- Links between sessions and features preserve context
- Drift detection helps catch scope creep early
- Analytics show real progress, not guesses

**The hooks track tool usage automatically**, but YOU must:
1. Start features before working (`uv run htmlgraph feature start <id>`)
2. Mark steps complete as you finish them (use SDK)
3. Complete features when done (`uv run htmlgraph feature complete <id>`)

### 5. Activity Attribution
HtmlGraph automatically tracks tool usage. Action items:
- Use descriptive summaries in Bash `description` parameter
- Reference feature IDs in commit messages
- Mention the feature context when starting new tasks

### 6. Documentation Habits
For every significant piece of work:
- Summarize what was done and why
- Note any decisions made and alternatives considered
- Record blockers or dependencies discovered

## Working with Tracks, Specs, and Plans

### What Are Tracks?

**Tracks are high-level containers for multi-feature work** (conductor-style planning):
- **Track** = Overall initiative with multiple related features
- **Spec** = Detailed specification with requirements and acceptance criteria
- **Plan** = Implementation plan with phases and estimated tasks
- **Features** = Individual work items linked to the track

**When to create a track:**
- Work involves 3+ related features
- Need high-level planning before implementation
- Multi-phase implementation
- Coordination across multiple sessions or agents

**When to skip tracks:**
- Single feature work
- Quick fixes or enhancements
- Direct implementation without planning phase

---

### Creating Tracks with TrackBuilder (PRIMARY METHOD)

**IMPORTANT: Use the TrackBuilder for deterministic track creation with minimal effort.**

The TrackBuilder provides a fluent API that auto-generates IDs, timestamps, file paths, and HTML files.

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# Create complete track with spec and plan in one command
track = sdk.tracks.builder() \
    .title("User Authentication System") \
    .description("Implement OAuth 2.0 authentication with JWT") \
    .priority("high") \
    .with_spec(
        overview="Add secure authentication with OAuth 2.0 support for Google and GitHub",
        context="Current system has no authentication. Users need secure login with session management.",
        requirements=[
            ("Implement OAuth 2.0 flow", "must-have"),
            ("Add JWT token management", "must-have"),
            ("Create user profile endpoint", "should-have"),
            "Add password reset functionality"  # Defaults to "must-have"
        ],
        acceptance_criteria=[
            ("Users can log in with Google/GitHub", "OAuth integration test passes"),
            "JWT tokens expire after 1 hour",
            "Password reset emails sent within 5 minutes"
        ]
    ) \
    .with_plan_phases([
        ("Phase 1: OAuth Setup", [
            "Configure OAuth providers (1h)",
            "Implement OAuth callback (2h)",
            "Add state verification (1h)"
        ]),
        ("Phase 2: JWT Integration", [
            "Create JWT signing logic (2h)",
            "Add token refresh endpoint (1.5h)",
            "Implement token validation middleware (2h)"
        ]),
        ("Phase 3: User Management", [
            "Create user profile endpoint (3h)",
            "Add password reset flow (4h)",
            "Write integration tests (3h)"
        ])
    ]) \
    .create()

# Output:
# ✓ Created track: track-20251221-220000
#   - Spec with 4 requirements
#   - Plan with 3 phases, 9 tasks

# Files created automatically:
# .htmlgraph/tracks/track-20251221-220000/index.html  (track metadata)
# .htmlgraph/tracks/track-20251221-220000/spec.html   (specification)
# .htmlgraph/tracks/track-20251221-220000/plan.html   (implementation plan)
```

**TrackBuilder Features:**
- ✅ Auto-generates track IDs with timestamps
- ✅ Creates index.html, spec.html, plan.html automatically
- ✅ Parses time estimates from task descriptions `"Task (2h)"`
- ✅ Validates requirements and acceptance criteria via Pydantic
- ✅ Fluent API with method chaining
- ✅ Single `.create()` call generates everything

---

### Linking Features to Tracks

After creating a track, link features to it:

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# Get the track ID from the track you created
track_id = "track-20251221-220000"

# Create features and link to track
oauth_feature = sdk.features.create("OAuth Integration") \
    .set_track(track_id) \
    .set_priority("high") \
    .add_steps([
        "Configure OAuth providers",
        "Implement OAuth callback",
        "Add state verification"
    ]) \
    .save()

jwt_feature = sdk.features.create("JWT Token Management") \
    .set_track(track_id) \
    .set_priority("high") \
    .add_steps([
        "Create JWT signing logic",
        "Add token refresh endpoint",
        "Implement validation middleware"
    ]) \
    .save()

# Features are now linked to the track
# Query features by track:
track_features = sdk.features.where(track=track_id)
print(f"Track has {len(track_features)} features")
```

**The track_id field:**
- Links features to their parent track
- Enables track-level progress tracking
- Used for querying related features
- Automatically indexed for fast lookups

---

### Track Workflow Example

**Complete workflow from track creation to feature completion:**

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# 1. Create track with spec and plan
track = sdk.tracks.builder() \
    .title("API Rate Limiting") \
    .description("Protect API endpoints from abuse") \
    .priority("critical") \
    .with_spec(
        overview="Implement rate limiting to prevent API abuse",
        context="Current API has no limits, vulnerable to DoS attacks",
        requirements=[
            ("Implement token bucket algorithm", "must-have"),
            ("Add Redis for distributed limiting", "must-have"),
            ("Create rate limit middleware", "must-have")
        ],
        acceptance_criteria=[
            ("100 requests/minute per API key", "Load test passes"),
            "429 status code when limit exceeded"
        ]
    ) \
    .with_plan_phases([
        ("Phase 1: Core", ["Token bucket (3h)", "Redis client (1h)"]),
        ("Phase 2: Integration", ["Middleware (2h)", "Error handling (1h)"]),
        ("Phase 3: Testing", ["Unit tests (2h)", "Load tests (3h)"])
    ]) \
    .create()

# 2. Create features from plan phases
for phase_idx, (phase_name, tasks) in enumerate([
    ("Core Implementation", ["Implement token bucket", "Add Redis client"]),
    ("API Integration", ["Create middleware", "Add error handling"]),
    ("Testing & Validation", ["Write unit tests", "Run load tests"])
]):
    feature = sdk.features.create(phase_name) \
        .set_track(track.id) \
        .set_priority("critical") \
        .add_steps(tasks) \
        .save()
    print(f"✓ Created feature {feature.id} for track {track.id}")

# 3. Work on features
# Start first feature
first_feature = sdk.features.where(track=track.id, status="todo")[0]
with sdk.features.edit(first_feature.id) as f:
    f.status = "in-progress"

# ... do the work ...

# Mark steps complete as you finish them
with sdk.features.edit(first_feature.id) as f:
    f.steps[0].completed = True

# Complete feature when done
with sdk.features.edit(first_feature.id) as f:
    f.status = "done"

# 4. Track progress
track_features = sdk.features.where(track=track.id)
completed = len([f for f in track_features if f.status == "done"])
print(f"Track progress: {completed}/{len(track_features)} features complete")
```

---

### TrackBuilder API Reference

**Methods:**

- `.title(str)` - Set track title (REQUIRED)
- `.description(str)` - Set description (optional)
- `.priority(str)` - Set priority: "low", "medium", "high", "critical" (default: "medium")
- `.with_spec(...)` - Add specification (optional)
  - `overview` - High-level summary
  - `context` - Background and current state
  - `requirements` - List of `(description, priority)` tuples or strings
    - Priorities: "must-have", "should-have", "nice-to-have"
  - `acceptance_criteria` - List of `(description, test_case)` tuples or strings
- `.with_plan_phases(list)` - Add plan phases (optional)
  - Format: `[(phase_name, [task_descriptions]), ...]`
  - Task estimates: Include `(Xh)` in description, e.g., "Implement auth (3h)"
- `.create()` - Execute build and create all files (returns Track object)

**Documentation:**
- Quick start: `docs/TRACK_BUILDER_QUICK_START.md`
- Complete workflow: `docs/TRACK_WORKFLOW.md`
- Full proposal: `docs/AGENT_FRIENDLY_SDK.md`

---

## Pre-Work Validation Hook

**NEW:** HtmlGraph enforces the workflow via a PreToolUse validation hook that ensures code changes are always tracked.

### How Validation Works

The validation hook runs BEFORE every tool execution and makes decisions based on your current work item:

**VALIDATION RULES:**

| Scenario | Tool | Action | Reason |
|----------|------|--------|--------|
| **Active Feature** | Read | ✅ Allow | Exploration is always allowed |
| **Active Feature** | Write/Edit/Delete | ✅ Allow | Code changes match active feature |
| **Active Spike** | Read | ✅ Allow | Spikes permit exploration |
| **Active Spike** | Write/Edit/Delete | ⚠️ Warn + Allow | Planning spike, code changes not tracked |
| **Auto-Spike** (session-init) | All | ✅ Allow | Planning phase, don't block |
| **No Active Work** | Read | ✅ Allow | Exploration without feature is OK |
| **No Active Work** | Write/Edit/Delete (1 file) | ⚠️ Warn + Allow | Single-file changes often trivial |
| **No Active Work** | Write/Edit/Delete (3+ files) | ❌ Deny | Requires explicit feature creation |
| **SDK Operations** | All | ✅ Allow | Creating work items always allowed |

### When Validation BLOCKS (Deny)

Validation **DENIES** code changes (Write/Edit/Delete) when ALL of these are true:

1. ❌ No active feature, bug, or chore (no work item)
2. ❌ Changes affect 3 or more files
3. ❌ Not an auto-spike (session-init or transition)
4. ❌ Not an SDK operation (e.g., creating features)

**What you see:**
```
PreToolUse Validation: Cannot proceed without active work item
- Reason: Multi-file changes (5 files) without tracked work item
- Action: Create a feature first with uv run htmlgraph feature create
```

**Resolution:** Create a feature using the feature decision framework, then try again.

### When Validation WARNS (Allow with Warning)

Validation **WARNS BUT ALLOWS** when:

1. ⚠️ Single-file changes without active work item (likely trivial)
2. ⚠️ Active spike (planning-only, code changes won't be fully tracked)
3. ⚠️ Auto-spike (session initialization, inherent planning phase)

**What you see:**
```
PreToolUse Validation: Warning - activity may not be tracked
- File: src/config.py (1 file)
- Reason: Single-file change without active feature
- Option: Create feature if this is significant work
```

**You can continue** - but consider if the work deserves a feature.

### Auto-Spike Integration

**Auto-spikes are automatic planning spikes created during session initialization.**

When the validation hook detects the start of a new session:
- ✅ Creates an automatic spike (e.g., `spike-session-init-abc123`)
- ✅ Marks it as planning-only (code changes permitted but not deeply tracked)
- ✅ Does NOT block any operations
- ✅ Allows exploration without forcing feature creation

**Why auto-spikes?**
- Captures early exploration work that doesn't fit a feature yet
- Avoids false positives from investigation activities
- Enables "think out loud" without rigid workflow
- Transitions to feature when scope becomes clear

**Example auto-spike lifecycle:**
```
Session Start
  ↓
Auto-spike created: spike-session-init-20251225
  ↓
Investigation/exploration work
  ↓
"This needs to be a feature" → Create feature, link to spike
  ↓
Feature takes primary attribution
  ↓
Spike marked as resolved
```

### Decision Framework for Code Changes

**Use this framework to decide if you need a feature before making code changes:**

```
User request or idea
  ├─ Single file, <30 min? → DIRECT CHANGE (validation warns, allows)
  ├─ 3+ files? → CREATE FEATURE (validation denies without feature)
  ├─ New tests needed? → CREATE FEATURE (validation blocks)
  ├─ Multi-component impact? → CREATE FEATURE (validation blocks)
  ├─ Hard to revert? → CREATE FEATURE (validation blocks)
  ├─ Needs documentation? → CREATE FEATURE (validation blocks)
  └─ Otherwise → DIRECT CHANGE (validation warns, allows)
```

**Key insight:** Validation's deny threshold (3+ files) aligns with the feature decision threshold in CLAUDE.md.

---

## Validation Scenarios (Examples)

### Scenario 1: Working with Auto-Spike (Session Start)

**Situation:** You just started a new session. No features are active.

```python
# Session starts → auto-spike created automatically
# spike-session-init-20251225 is now active (auto-created)

# All of these work WITHOUT creating a feature:
- Read code files (exploration)
- Write to a single file (validation warns but allows)
- Create a feature (SDK operation, always allowed)
- Ask the user what to work on
```

**Flow:**
1. ✅ Session starts
2. ✅ Validation creates auto-spike for this session
3. ✅ You explore and read code (no restrictions)
4. ✅ You ask user what to work on
5. ✅ User says: "Implement user authentication"
6. ✅ You create feature: `uv run htmlgraph feature create "User Authentication"`
7. ✅ Feature becomes primary (replaces auto-spike attribution)
8. ✅ You can now code freely

**Result:** Work is properly attributed to the feature, not the throwaway auto-spike.

---

### Scenario 2: Multi-File Feature Implementation

**Situation:** User says "Build a user authentication system"

**WITHOUT feature:**
```bash
# Try to edit 5 files without creating a feature
uv run htmlgraph something that touches 5 files

# Validation DENIES:
# ❌ PreToolUse Validation: Cannot proceed without active work item
#    Reason: Multi-file changes (5 files) without tracked work item
#    Action: Create a feature first
```

**WITH feature:**
```bash
# Create the feature first
uv run htmlgraph feature create "User Authentication"
# → feat-abc123 created and marked in-progress

# Now implement - all 5 files allowed
# Edit src/auth.py
# Edit src/middleware.py
# Edit src/models.py
# Write tests/test_auth.py
# Update docs/authentication.md

# Validation ALLOWS:
# ✅ All changes attributed to feat-abc123
# ✅ Session shows feature context
# ✅ Work is trackable
```

**Result:** Multi-file feature work is tracked and attributed.

---

### Scenario 3: Single-File Quick Fix (No Feature)

**Situation:** You notice a typo in a docstring.

```bash
# Edit a single file without creating a feature
# Edit src/utils.py (fix typo)

# Validation WARNS BUT ALLOWS:
# ⚠️  PreToolUse Validation: Warning - activity may not be tracked
#    File: src/utils.py (1 file)
#    Reason: Single-file change without active feature
#    Option: Create feature if this is significant work

# You can choose:
# - Continue (typo is trivial, doesn't need feature)
# - Cancel and create feature (if it's a bigger fix)
```

**Result:** Small fixes don't require features, but validation tracks the decision.

---

## Working with HtmlGraph

**RECOMMENDED:** Use the Python SDK for AI agents (cleanest, fastest, most powerful)

### Python SDK (PRIMARY INTERFACE - Use This!)

The SDK supports ALL collections with a unified interface. Use it for maximum performance and type safety.

```python
from htmlgraph import SDK

# Initialize (auto-discovers .htmlgraph)
sdk = SDK(agent="claude")

# ===== ALL COLLECTIONS SUPPORTED =====
# Features (with builder support)
feature = sdk.features.create("User Authentication") \
    .set_priority("high") \
    .add_steps([
        "Create login endpoint",
        "Add JWT middleware",
        "Write tests"
    ]) \
    .save()

# Bugs
with sdk.bugs.edit("bug-001") as bug:
    bug.status = "in-progress"
    bug.priority = "critical"

# Chores, Spikes, Epics - all work the same way
chore = sdk.chores.where(status="todo")[0]
spike_results = sdk.spikes.all()
epic_steps = sdk.epics.get("epic-001").steps

# ===== EFFICIENT BATCH OPERATIONS =====
# Mark multiple items done (vectorized!)
sdk.bugs.mark_done(["bug-001", "bug-002", "bug-003"])

# Assign multiple items to agent
sdk.features.assign(["feat-001", "feat-002"], agent="claude")

# Custom batch updates (any attributes)
sdk.chores.batch_update(
    ["chore-001", "chore-002"],
    {"status": "done", "agent_assigned": "claude"}
)

# ===== CROSS-COLLECTION QUERIES =====
# Find all in-progress work
in_progress = []
for coll_name in ['features', 'bugs', 'chores', 'spikes', 'epics']:
    coll = getattr(sdk, coll_name)
    in_progress.extend(coll.where(status='in-progress'))

# Find low-lift tasks
for item in in_progress:
    if hasattr(item, 'steps'):
        for step in item.steps:
            if not step.completed and 'document' in step.description.lower():
                print(f"📝 {item.id}: {step.description}")
```

**SDK Performance (vs CLI):**
- Single query: **3x faster**
- 5 queries: **9x faster**
- 10 batch updates: **16x faster**

### CLI (For One-Off Commands Only)

**IMPORTANT:** Always use `uv run` when running htmlgraph commands to ensure the correct environment.

⚠️ CLI is slower than SDK (400ms startup per command). Use for quick one-off queries only.

```bash
# Check Current Status
uv run htmlgraph status
uv run htmlgraph feature list

# Start Working on a Feature
uv run htmlgraph feature start <feature-id>

# Set Primary Feature (when multiple are active)
uv run htmlgraph feature primary <feature-id>

# Complete a Feature
uv run htmlgraph feature complete <feature-id>
```

**When to use CLI vs SDK:**
- CLI: Quick one-off shell command
- SDK: Everything else (faster, more powerful, better for scripts)

---

## Strategic Planning & Dependency Analytics

**NEW:** HtmlGraph now provides intelligent analytics to help you make smart decisions about what to work on next.

### Quick Start: Get Recommendations

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# Get smart recommendations on what to work on
recs = sdk.recommend_next_work(agent_count=1)
if recs:
    best = recs[0]
    print(f"💡 Work on: {best['title']}")
    print(f"   Score: {best['score']:.1f}")
    print(f"   Why: {', '.join(best['reasons'])}")
```

### Available Strategic Planning Features

#### 1. Find Bottlenecks 🚧

Identify tasks blocking the most downstream work:

```python
bottlenecks = sdk.find_bottlenecks(top_n=5)

for bn in bottlenecks:
    print(f"{bn['title']} blocks {bn['blocks_count']} tasks")
    print(f"Impact score: {bn['impact_score']}")
```

**Returns**: List of dicts with `id`, `title`, `status`, `priority`, `blocks_count`, `impact_score`, `blocked_tasks`

#### 2. Get Parallel Work ⚡

Find tasks that can be worked on simultaneously:

```python
parallel = sdk.get_parallel_work(max_agents=5)

print(f"Can work on {parallel['max_parallelism']} tasks at once")
print(f"Ready now: {parallel['ready_now']}")
```

**Returns**: Dict with `max_parallelism`, `ready_now`, `total_ready`, `level_count`, `next_level`

#### 3. Recommend Next Work 💡

Get smart recommendations considering priority, dependencies, and impact:

```python
recs = sdk.recommend_next_work(agent_count=3)

for rec in recs:
    print(f"{rec['title']} (score: {rec['score']})")
    print(f"Reasons: {rec['reasons']}")
    print(f"Unlocks: {rec['unlocks_count']} tasks")
```

**Returns**: List of dicts with `id`, `title`, `priority`, `score`, `reasons`, `estimated_hours`, `unlocks_count`, `unlocks`

#### 4. Assess Risks ⚠️

Check for dependency-related risks:

```python
risks = sdk.assess_risks()

if risks['high_risk_count'] > 0:
    print(f"Warning: {risks['high_risk_count']} high-risk tasks")
    for task in risks['high_risk_tasks']:
        print(f"  {task['title']}: {task['risk_factors']}")

if risks['circular_dependencies']:
    print("Circular dependencies detected!")
```

**Returns**: Dict with `high_risk_count`, `high_risk_tasks`, `circular_dependencies`, `orphaned_count`, `recommendations`

#### 5. Analyze Impact 📊

See what completing a task will unlock:

```python
impact = sdk.analyze_impact("feature-001")

print(f"Unlocks {impact['completion_impact']:.1f}% of remaining work")
print(f"Affects {impact['total_impact']} downstream tasks")
```

**Returns**: Dict with `node_id`, `direct_dependents`, `total_impact`, `completion_impact`, `unlocks_count`, `affected_tasks`

### Recommended Decision Flow

At the start of each work session:

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# 1. Check for bottlenecks
bottlenecks = sdk.find_bottlenecks(top_n=3)
if bottlenecks:
    print(f"⚠️  {len(bottlenecks)} bottlenecks found")

# 2. Get recommendations
recs = sdk.recommend_next_work(agent_count=1)
if recs:
    best = recs[0]
    print(f"\n💡 RECOMMENDED: {best['title']}")
    print(f"   Score: {best['score']:.1f}")
    print(f"   Reasons: {', '.join(best['reasons'][:2])}")

    # 3. Analyze impact
    impact = sdk.analyze_impact(best['id'])
    print(f"   Impact: Unlocks {impact['unlocks_count']} tasks")

# 4. Check for parallel work (if coordinating)
parallel = sdk.get_parallel_work(max_agents=3)
if parallel['total_ready'] > 1:
    print(f"\n⚡ {parallel['total_ready']} tasks available in parallel")
```

### When to Use Each Feature

- **find_bottlenecks()**: At session start, during sprint planning
- **recommend_next_work()**: When deciding what task to pick up
- **get_parallel_work()**: When coordinating multiple agents
- **assess_risks()**: During project health checks, before milestones
- **analyze_impact()**: When choosing between high-effort tasks

### Advanced: Direct Analytics Access

For advanced use cases, access the full analytics engine:

```python
# Access Pydantic models with all fields
analytics = sdk.dep_analytics

bottlenecks = analytics.find_bottlenecks(top_n=5, min_impact=1.0)
parallel = analytics.find_parallelizable_work(status="todo")
recs = analytics.recommend_next_tasks(agent_count=3, lookahead=5)
risk = analytics.assess_dependency_risk(spof_threshold=2)
impact = analytics.impact_analysis("feature-001")
```

**See also**: `docs/AGENT_STRATEGIC_PLANNING.md` for complete guide

---

## Orchestrator Workflow (Multi-Agent Delegation)

**CRITICAL: When spawning subagents with Task tool, follow the orchestrator workflow.**

### When to Use Orchestration

Use orchestration (spawn subagents) when:
- Multiple independent tasks can run in parallel
- Work can be partitioned without conflicts
- Speedup factor > 1.5x
- `sdk.get_parallel_work()` shows `max_parallelism >= 2`

### 6-Phase Parallel Workflow

```
1. ANALYZE   → Check dependencies, assess parallelizability
2. PREPARE   → Cache shared context, partition files
3. DISPATCH  → Generate prompts via SDK, spawn agents in ONE message
4. MONITOR   → Track health metrics per agent
5. AGGREGATE → Collect results, detect conflicts
6. VALIDATE  → Verify outputs, run tests
```

### SDK Orchestration Methods (USE THESE!)

**IMPORTANT: Use SDK methods instead of raw Task prompts!**

```python
from htmlgraph import SDK

sdk = SDK(agent="orchestrator")

# 1. ANALYZE - Check if work can be parallelized
parallel = sdk.get_parallel_work(max_agents=5)
if parallel["max_parallelism"] < 2:
    print("Work sequentially instead")

# 2. PLAN - Get structured prompts with context
plan = sdk.plan_parallel_work(max_agents=3)

if plan["can_parallelize"]:
    # 3. DISPATCH - Spawn all agents in ONE message
    for p in plan["prompts"]:
        Task(
            subagent_type="general-purpose",
            prompt=p["prompt"],
            description=p["description"]
        )

    # 4-5. AGGREGATE - After agents complete
    results = sdk.aggregate_parallel_results(agent_ids)

    # 6. VALIDATE
    if results["all_passed"]:
        print("✅ Parallel execution validated!")
```

### Why SDK Over Raw Prompts?

| Raw Task Prompt | SDK Orchestration |
|-----------------|-------------------|
| No context caching | Shares context efficiently |
| No file isolation | Prevents conflicts |
| Manual prompt writing | Structured prompts |
| No aggregation | Automatic result collection |
| No feature linking | Auto-links to work items |

### Quick Reference

```python
# Check parallelizability
parallel = sdk.get_parallel_work(max_agents=5)

# Plan parallel work
plan = sdk.plan_parallel_work(max_agents=3)

# Alternative: spawn individual agents
explorer_prompt = sdk.spawn_explorer(task="Find API endpoints", scope="src/api/")
coder_prompt = sdk.spawn_coder(feature_id="feat-123", context="...")

# Full orchestration
prompts = sdk.orchestrate("feat-123", exploration_scope="src/", test_command="pytest")
```

### Anti-Patterns to Avoid

❌ **DON'T:** Write raw prompts to Task tool
```python
# BAD - bypasses SDK orchestration
Task(prompt="Fix the bug in auth.py...", subagent_type="general-purpose")
```

✅ **DO:** Use SDK to generate prompts
```python
# GOOD - uses SDK orchestration with proper context
prompt = sdk.spawn_coder(feature_id="bug-123", files_to_modify=["auth.py"])
Task(prompt=prompt["prompt"], ...)
```

❌ **DON'T:** Send Task calls in separate messages (sequential)
```python
# BAD - agents run one at a time
result1 = Task(...)  # Wait
result2 = Task(...)  # Then next
```

✅ **DO:** Send all Task calls in ONE message (parallel)
```python
# GOOD - true parallelism
for p in prompts:
    Task(prompt=p["prompt"], ...)  # All in same response
```

**See also**: `packages/claude-plugin/skills/parallel-orchestrator/SKILL.md` for detailed 6-phase workflow

---

## Work Type Classification (Phase 1)

**NEW: HtmlGraph now automatically categorizes all work by type to differentiate exploratory work from implementation.**

### Work Type Categories

All events are automatically tagged with a work type based on the active feature:

- **feature-implementation** - Building new functionality (feat-*)
- **spike-investigation** - Research and exploration (spike-*)
- **bug-fix** - Correcting defects (bug-*)
- **maintenance** - Refactoring and tech debt (chore-*)
- **documentation** - Writing docs (doc-*)
- **planning** - Design decisions (plan-*)
- **review** - Code review
- **admin** - Administrative tasks

### Creating Spikes (Investigation Work)

Use Spike model for timeboxed investigation:

```python
from htmlgraph import SDK, SpikeType

sdk = SDK(agent="claude")

# Create a spike with classification
spike = sdk.spikes.create("Investigate OAuth providers") \
    .set_spike_type(SpikeType.TECHNICAL) \
    .set_timebox_hours(4) \
    .add_steps([
        "Research OAuth 2.0 flow",
        "Compare Google vs GitHub providers",
        "Document security considerations"
    ]) \
    .save()

# Update findings after investigation
with sdk.spikes.edit(spike.id) as s:
    s.findings = "Google OAuth has better docs but GitHub has simpler integration"
    s.decision = "Use GitHub OAuth for MVP, migrate to Google later if needed"
    s.status = "done"
```

**Spike Types:**
- `TECHNICAL` - Investigate technical implementation options
- `ARCHITECTURAL` - Research system design decisions
- `RISK` - Identify and assess project risks
- `GENERAL` - Uncategorized investigation

### Creating Chores (Maintenance Work)

Use Chore model for maintenance tasks:

```python
from htmlgraph import SDK, MaintenanceType

sdk = SDK(agent="claude")

# Create a chore with classification
chore = sdk.chores.create("Refactor authentication module") \
    .set_maintenance_type(MaintenanceType.PREVENTIVE) \
    .set_technical_debt_score(7) \
    .add_steps([
        "Extract auth logic to separate module",
        "Add unit tests for auth flows",
        "Update documentation"
    ]) \
    .save()
```

**Maintenance Types:**
- `CORRECTIVE` - Fix defects and errors
- `ADAPTIVE` - Adapt to environment changes (OS, dependencies)
- `PERFECTIVE` - Improve performance, usability, maintainability
- `PREVENTIVE` - Prevent future problems (refactoring, tech debt)

### Session Work Type Analytics

Query work type distribution for any session:

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# Get current session
from htmlgraph.session_manager import SessionManager
sm = SessionManager()
session = sm.get_active_session(agent="claude")

# Calculate work breakdown
breakdown = session.calculate_work_breakdown()
# Returns: {"feature-implementation": 120, "spike-investigation": 45, "maintenance": 30}

# Get primary work type
primary = session.calculate_primary_work_type()
# Returns: "feature-implementation" (most common type)

# Query events by work type
spike_events = [e for e in session.get_events() if e.get("work_type") == "spike-investigation"]
```

### Automatic Work Type Inference

**Work type is automatically inferred from feature_id prefix:**

```python
# When you start a spike:
sdk.spikes.start("spike-123")
# → All events auto-tagged with work_type="spike-investigation"

# When you start a feature:
sdk.features.start("feat-456")
# → All events auto-tagged with work_type="feature-implementation"

# When you start a chore:
sdk.chores.start("chore-789")
# → All events auto-tagged with work_type="maintenance"
```

**No manual tagging required!** The system automatically categorizes your work based on what you're working on.

### Why This Matters

Work type classification enables you to:

1. **Differentiate exploration from implementation** - "How much time was spent researching vs building?"
2. **Track technical debt** - "What % of work is maintenance vs new features?"
3. **Measure innovation** - "What's our spike-to-feature ratio?"
4. **Session context** - "Was this primarily an exploratory session or implementation?"

**Example Session Analysis:**

```python
# After a long session, analyze what you did:
session = sm.get_active_session(agent="claude")
breakdown = session.calculate_work_breakdown()

print(f"Primary work type: {session.calculate_primary_work_type()}")
print(f"Work breakdown: {breakdown}")

# Output:
# Primary work type: spike-investigation
# Work breakdown: {
#   "spike-investigation": 65,
#   "feature-implementation": 30,
#   "documentation": 10
# }
# → This was primarily an exploratory/research session
```

## Research Checkpoint - MANDATORY Before Implementation

**CRITICAL: Always research BEFORE implementing solutions. Never guess.**

HtmlGraph enforces a research-first philosophy. This emerged from dogfooding where we repeatedly made trial-and-error attempts before researching documentation.

**Complete debugging guide:** See [DEBUGGING.md](../../../DEBUGGING.md)

### When to Research (Before ANY Implementation)

**STOP and research if:**
- ❓ You encounter unfamiliar errors or behaviors
- ❓ You're working with Claude Code hooks, plugins, or configuration
- ❓ You're implementing a solution based on assumptions
- ❓ Multiple attempted fixes have failed
- ❓ You're debugging without understanding root cause
- ❓ You're about to "try something" to see if it works

### Research-First Workflow

**REQUIRED PATTERN:**
```
1. RESEARCH     → Use documentation, claude-code-guide, GitHub issues
2. UNDERSTAND   → Identify root cause through evidence
3. IMPLEMENT    → Apply fix based on understanding
4. VALIDATE     → Test to confirm fix works
5. DOCUMENT     → Capture learning in HtmlGraph spike
```

**❌ NEVER do this:**
```
1. Try Fix A    → Doesn't work
2. Try Fix B    → Doesn't work
3. Try Fix C    → Doesn't work
4. Research     → Find actual root cause
5. Apply fix    → Finally works
```

### Available Research Tools

**Debugging Agents (use these!):**
- **Researcher Agent** - Research documentation before implementing
  - Activate via: `.claude/agents/researcher.md`
  - Use for: Documentation research, pattern identification

- **Debugger Agent** - Systematically analyze errors
  - Activate via: `.claude/agents/debugger.md`
  - Use for: Error analysis, hypothesis testing

- **Test Runner Agent** - Enforce quality gates
  - Activate via: `.claude/agents/test-runner.md`
  - Use for: Pre-commit validation, test execution

**Claude Code Tools:**
```bash
# Built-in debug commands
claude --debug <command>        # Verbose output
/hooks                          # List active hooks
/hooks PreToolUse              # Show specific hook
/doctor                         # System diagnostics
claude --verbose               # Detailed logging
```

**Documentation Resources:**
- Claude Code docs: https://code.claude.com/docs
- Hook documentation: https://code.claude.com/docs/en/hooks.md
- GitHub issues: https://github.com/anthropics/claude-code/issues

### Research Checkpoint Questions

**Before implementing ANY fix, ask yourself:**
- [ ] Did I research the documentation for this issue?
- [ ] Have I used the researcher agent or claude-code-guide?
- [ ] Is this approach based on evidence or assumptions?
- [ ] Have I checked GitHub issues for similar problems?
- [ ] What debug tools can provide more information?
- [ ] Am I making an informed decision or guessing?

### Example: Correct Research-First Pattern

**Scenario**: Hooks are duplicating

**✅ CORRECT (Research First):**
```
1. STOP - Don't remove files yet
2. RESEARCH - Read Claude Code hook loading documentation
3. Use /hooks command to inspect active hooks
4. Check GitHub issues for "duplicate hooks"
5. UNDERSTAND - Hooks from multiple sources MERGE
6. IMPLEMENT - Remove duplicates from correct source
7. VALIDATE - Verify fix with /hooks command
8. DOCUMENT - Create spike with findings
```

**❌ WRONG (Trial and Error):**
```
1. Remove .claude/hooks/hooks.json - Still broken
2. Clear plugin cache - Still broken
3. Remove old plugin versions - Still broken
4. Remove marketplaces symlink - Still broken
5. Finally research documentation
6. Find root cause: Hook merging behavior
```

### Documenting Research Findings

**REQUIRED: Capture all research in HtmlGraph spike:**

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

spike = sdk.spikes.create("Research: [Problem]") \
    .set_spike_type(SpikeType.TECHNICAL) \
    .set_findings("""
## Problem
[Brief description of issue]

## Research Sources
- [Documentation]: [Key findings]
- [GitHub issue #123]: [Relevant discussion]
- [Debug output]: [What it revealed]

## Root Cause
[What the research revealed]

## Solution Options
1. [Option A]: [Pros/cons based on docs]
2. [Option B]: [Pros/cons based on docs]

## Implemented Solution
[What you chose and why, with evidence]

## Validation
[How you confirmed it works]
    """) \
    .save()
```

### Integration with Pre-Work Validation

The validation hook already prevents multi-file changes without a feature. Research checkpoints add another layer:

1. **Pre-Work Validation** - Ensures work is tracked
2. **Research Checkpoint** - Ensures decisions are evidence-based

Both work together to maintain quality and prevent wasted effort.

---

## Feature Creation Decision Framework

**CRITICAL**: Use this framework to decide when to create a feature vs implementing directly.

### Quick Decision Rule

Create a **FEATURE** if ANY apply:
- Estimated >30 minutes of work
- Involves 3+ files
- Requires new automated tests
- Affects multiple components
- Hard to revert (schema, API changes)
- Needs user/API documentation

Implement **DIRECTLY** if ALL apply:
- Single file, obvious change
- <30 minutes work
- No cross-system impact
- Easy to revert
- No tests needed
- Internal/trivial change

### Decision Tree (Quick Reference)

```
User request received
  ├─ Bug in existing feature? → See Bug Fix Workflow in WORKFLOW.md
  ├─ >30 minutes? → CREATE FEATURE
  ├─ 3+ files? → CREATE FEATURE
  ├─ New tests needed? → CREATE FEATURE
  ├─ Multi-component impact? → CREATE FEATURE
  ├─ Hard to revert? → CREATE FEATURE
  └─ Otherwise → IMPLEMENT DIRECTLY
```

### Examples

**✅ CREATE FEATURE:**
- "Add user authentication" (multi-file, tests, docs)
- "Implement session comparison view" (new UI, Playwright tests)
- "Fix attribution drift algorithm" (complex, backend tests)

**❌ IMPLEMENT DIRECTLY:**
- "Fix typo in README" (single file, trivial)
- "Update CSS color" (single file, quick, reversible)
- "Add missing import" (obvious fix, no impact)

### Default Rule

**When in doubt, CREATE A FEATURE.** Over-tracking is better than losing attribution.

See `docs/WORKFLOW.md` for the complete decision framework with detailed criteria, thresholds, and edge cases.

## Session Workflow Checklist

**MANDATORY: Follow this checklist for EVERY session. No exceptions.**

### Session Start (DO THESE FIRST)
1. ✅ Activate this skill (done automatically)
2. ✅ **AUTO-SPIKE CREATED:** Validation hook automatically creates an auto-spike for session exploration (see "Auto-Spike Integration" section)
3. ✅ **RUN:** `uv run htmlgraph session start-info` - Get comprehensive session context (optimized, 1 call)
   - Replaces: status + feature list + session list + git log + analytics
   - Reduces context usage from 30% to <5%
4. ✅ Review active features and decide if you need to create a new one
5. ✅ Greet user with brief status update
6. ✅ **RESEARCH CHECKPOINT:** Before implementing ANY solution:
   - Did I research documentation first?
   - Am I using evidence or assumptions?
   - Should I activate researcher/debugger agent?
7. ✅ **DECIDE:** Create feature or implement directly? (use decision framework)
8. ✅ **If creating feature:** Use SDK or run `uv run htmlgraph feature start <id>`

### During Work (DO CONTINUOUSLY)
1. ✅ Feature MUST be marked "in-progress" before you write any code
   - ⚠️ **VALIDATION NOTE:** Validation will warn or deny multi-file changes without active feature (see "Pre-Work Validation" section)
   - Single-file changes are allowed with warning
   - 3+ file changes require active feature to proceed
2. ✅ **CRITICAL:** Mark each step complete IMMEDIATELY after finishing it (use SDK)
3. ✅ Document ALL decisions as you make them
4. ✅ Test incrementally - don't wait until the end
5. ✅ Watch for drift warnings and act on them immediately

#### How to Mark Steps Complete

**IMPORTANT:** After finishing each step, mark it complete using the SDK:

```python
from htmlgraph import SDK

sdk = SDK(agent="claude")

# Mark step 0 (first step) as complete
with sdk.features.edit("feature-id") as f:
    f.steps[0].completed = True

# Mark step 1 (second step) as complete
with sdk.features.edit("feature-id") as f:
    f.steps[1].completed = True

# Or mark multiple steps at once
with sdk.features.edit("feature-id") as f:
    f.steps[0].completed = True
    f.steps[1].completed = True
    f.steps[2].completed = True
```

**Step numbering is 0-based** (first step = 0, second step = 1, etc.)

**When to mark complete:**
- ✅ IMMEDIATELY after finishing a step
- ✅ Even if you continue working on the feature
- ✅ Before moving to the next step
- ❌ NOT at the end when all steps are done (too late!)

**Example workflow:**
1. Start feature: `uv run htmlgraph feature start feature-123`
2. Work on step 0 (e.g., "Design models")
3. **MARK STEP 0 COMPLETE** → Use SDK: `with sdk.features.edit("feature-123") as f: f.steps[0].completed = True`
4. Work on step 1 (e.g., "Create templates")
5. **MARK STEP 1 COMPLETE** → Use SDK: `with sdk.features.edit("feature-123") as f: f.steps[1].completed = True`
6. Continue until all steps done
7. Complete feature: `uv run htmlgraph feature complete feature-123`

### Session End (MUST DO BEFORE MARKING COMPLETE)
1. ✅ **RUN TESTS:** `uv run pytest` - All tests MUST pass
2. ✅ **VERIFY ATTRIBUTION:** Check that activities are linked to correct feature
3. ✅ **CHECK STEPS:** ALL feature steps MUST be marked complete
4. ✅ **CLEAN CODE:** Remove all debug code, console.logs, TODOs
5. ✅ **COMMIT WORK:** Git commit your changes IMMEDIATELY (allows user rollback)
   - Do this BEFORE marking the feature complete
   - Include the feature ID in the commit message
6. ✅ **COMPLETE FEATURE:** Use SDK or run `uv run htmlgraph feature complete <id>`
7. ✅ **UPDATE EPIC:** If part of epic, mark epic step complete

**REMINDER:** Completing a feature without doing all of the above means incomplete work. Don't skip steps.

## Handling Drift Warnings

When you see a drift warning like:
> Drift detected (0.74): Activity may not align with feature-self-tracking

Consider:
1. **Is this expected?** Sometimes work naturally spans multiple features
2. **Should you switch features?** Use `uv run htmlgraph feature primary <id>` to change attribution
3. **Is the feature scope wrong?** The feature's file patterns or keywords may need updating

## Session Continuity

At the start of each session:
1. Review previous session summary (if provided)
2. Note current feature progress
3. Identify what remains to be done
4. Ask the user what they'd like to work on

At the end of each session:
1. The SessionEnd hook will generate a summary
2. All activities are preserved in `.htmlgraph/sessions/`
3. Feature progress is updated automatically

## Best Practices

### Commit Messages
Include feature context:
```
feat(feature-id): Description of the change

- Details about what was done
- Why this approach was chosen

🤖 Generated with Claude Code
```

### Task Descriptions
When using Bash tool, always provide a description:
```bash
# Good - descriptive
Bash(description="Install dependencies for auth feature")

# Bad - no context
Bash(command="npm install")
```

### Decision Documentation
When making architectural decisions:

1. Track with `uv run htmlgraph track "Decision" "Chose X over Y because Z"`
2. Or note in the feature's HTML file under activity log

## Dashboard Access

View progress visually:
```bash
uv run htmlgraph serve
# Open http://localhost:8080
```

The dashboard shows:
- Kanban board with feature status
- Session history with activity logs
- Graph visualization of dependencies

## Key Files

- `.htmlgraph/features/` - Feature HTML files (the graph nodes)
- `.htmlgraph/sessions/` - Session HTML files with activity logs
- `index.html` - Dashboard (open in browser)

## Integration Points

HtmlGraph hooks track:
- **SessionStart**: Creates session, provides feature context
- **PostToolUse**: Logs every tool call with attribution
- **UserPromptSubmit**: Logs user queries
- **SessionEnd**: Finalizes session with summary

All data is stored as HTML files - human-readable, git-friendly, browser-viewable.
