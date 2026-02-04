---
name: context-restoration
description: |
  Restore previous session state from Serena MCP checkpoints. Retrieves checkpoint by ID or
  auto-selects most recent, deserializes context, restores command/skill/phase/wave state.
  Use when: resuming after context loss, continuing previous session, recovering from interruption.

skill-type: PROTOCOL
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      purpose: Checkpoint retrieval

allowed-tools: Serena, Read
---

# Context Restoration Skill

## Purpose

Restore complete session state after context loss events (auto-compact, session break, interruption).

**Zero Context Loss Promise**: When combined with context-checkpoint skill, users can resume exactly where they left off regardless of auto-compact events or session boundaries.

---

## Inputs

**Required:**
- `checkpoint_id` (string): Unique checkpoint identifier (e.g., "SHANNON-W2-20251103T143000")

**Optional:**
- `auto_select` (boolean): Automatically select most recent checkpoint if ID not provided (default: true)
- `project_id` (string): Filter checkpoints by specific project
- `validate_integrity` (boolean): Verify checkpoint integrity via SHA-256 hash (default: true)

---

## When to Use This Skill

Activate context-restoration when:

1. **After Auto-Compact** - Claude Code compressed conversation history
2. **New Session Start** - User returns after hours/days
3. **Context Loss Detection** - Claude doesn't remember recent work
4. **Project Switching** - Loading different project context
5. **Error Recovery** - Restoring from last known good state

---

## Workflow

### Step 1: Identify Checkpoint

```yaml
Input Options:
  - Checkpoint ID: "precompact_checkpoint_20250930T143000Z"
  - Auto Mode: Find most recent checkpoint automatically
  - Project-Specific: Latest checkpoint for specific project
  - Phase-Specific: Checkpoint from specific phase
```

**Auto-Detection Logic**:
```python
# Priority order for auto-selection:
1. Read "latest_checkpoint" pointer from Serena
2. If not found, list all checkpoints and sort by timestamp
3. Select most recent checkpoint
4. Validate checkpoint is not corrupted
```

### Step 2: Retrieve Checkpoint from Serena

**Serena MCP Operation**:
```python
# Method 1: Direct retrieval (if ID known)
checkpoint_data = read_memory(checkpoint_id)

# Method 2: Auto-selection
latest_key = read_memory("latest_checkpoint")
checkpoint_data = read_memory(latest_key)

# Method 3: Search and filter
all_keys = list_memories()
checkpoint_keys = [k for k in all_keys if "checkpoint" in k]
sorted_keys = sorted(checkpoint_keys, reverse=True)
checkpoint_data = read_memory(sorted_keys[0])
```

### Step 3: Deserialize Checkpoint JSON

**Checkpoint Structure**:
```json
{
  "metadata": {
    "timestamp": "2025-09-30T14:30:00Z",
    "checkpoint_type": "precompact|manual|wave|phase|time",
    "session_id": "unique_session_identifier",
    "shannon_version": "4.0.0"
  },

  "project_state": {
    "project_id": "taskapp_v1",
    "active_phase": "implementation",
    "current_wave": 3,
    "total_waves": 5
  },

  "serena_memory_keys": [
    "spec_analysis_taskapp",
    "phase_plan_taskapp",
    "wave_1_complete_taskapp",
    "wave_2_complete_taskapp",
    "wave_3_results_frontend",
    "project_decisions_taskapp",
    "todo_list_taskapp"
  ],

  "active_work": {
    "current_focus": "Implementing authentication system",
    "in_progress_files": [
      "/path/to/auth.ts",
      "/path/to/login.tsx"
    ],
    "pending_tasks": [
      "Complete JWT token generation",
      "Add refresh token logic",
      "Test login flow"
    ]
  },

  "wave_context": {
    "completed_waves": [
      {
        "wave_number": 1,
        "name": "Frontend Components",
        "status": "complete",
        "agents": ["frontend-architect", "implementation-worker"],
        "results_key": "wave_1_complete_taskapp"
      }
    ],
    "pending_waves": [
      {
        "wave_number": 3,
        "name": "Database Integration",
        "status": "in_progress"
      }
    ]
  },

  "agent_context": {
    "active_agents": ["implementation-worker"],
    "agent_handoff_data": {
      "from_agent": "backend-architect",
      "to_agent": "implementation-worker",
      "context": "Complete auth implementation per plan"
    }
  },

  "key_decisions": [
    {
      "decision": "Use JWT with refresh tokens",
      "rationale": "Security best practice",
      "timestamp": "2025-09-30T14:15:00Z"
    }
  ],

  "validation_status": {
    "phase_2_gates": "passed",
    "phase_3_gates": "in_progress",
    "tests_passing": true,
    "known_issues": []
  }
}
```

### Step 4: Restore Context State

**Restoration Sequence**:

```python
# 4.1: Restore All Serena Memory Keys
serena_keys = checkpoint_data["serena_memory_keys"]
restored_memories = {}

for key in serena_keys:
    try:
        content = read_memory(key)
        restored_memories[key] = content
    except Exception as e:
        log_warning(f"Could not restore memory: {key}")
        missing_memories.append(key)

# 4.2: Rebuild Project Context
project_id = checkpoint_data["project_state"]["project_id"]
active_phase = checkpoint_data["project_state"]["active_phase"]
current_wave = checkpoint_data["project_state"]["current_wave"]
total_waves = checkpoint_data["project_state"]["total_waves"]

# 4.3: Restore Work State
current_focus = checkpoint_data["active_work"]["current_focus"]
pending_tasks = checkpoint_data["active_work"]["pending_tasks"]
in_progress_files = checkpoint_data["active_work"]["in_progress_files"]

# 4.4: Restore Wave Progress
completed_waves = checkpoint_data["wave_context"]["completed_waves"]
pending_waves = checkpoint_data["wave_context"]["pending_waves"]

# 4.5: Restore Agent State
active_agents = checkpoint_data["agent_context"]["active_agents"]
handoff_data = checkpoint_data["agent_context"]["agent_handoff_data"]

# 4.6: Restore Decisions
key_decisions = checkpoint_data["key_decisions"]
```

### Step 5: Reinitialize MCP Connections

**MCP Validation**:
```python
# Check required MCPs are available
required_mcps = ["serena"]  # From skill frontmatter

for mcp_name in required_mcps:
    try:
        # Test MCP connection
        test_mcp_connection(mcp_name)
    except:
        warn_user(f"MCP {mcp_name} not available - some features may not work")

# Reconnect to project-specific MCPs
project_mcps = checkpoint_data.get("project_mcps", [])
for mcp_config in project_mcps:
    try:
        initialize_mcp(mcp_config)
    except:
        warn_user(f"Could not initialize {mcp_config['name']}")
```

### Step 6: Validate Restoration

**Validation Checks**:
```python
validation_results = {
    # Checkpoint integrity
    "checkpoint_loaded": checkpoint_data is not None,
    "checkpoint_valid": validate_checkpoint_schema(checkpoint_data),

    # Memory restoration
    "memories_restored": len(restored_memories) > 0,
    "critical_memories_present": all([
        "spec_analysis" in str(restored_memories.keys()),
        "phase_plan" in str(restored_memories.keys())
    ]),

    # State validity
    "phase_valid": active_phase in ["analysis", "planning", "implementation", "testing", "deployment"],
    "wave_valid": current_wave > 0 and current_wave <= total_waves,

    # File references
    "files_exist": all([
        os.path.exists(f) for f in in_progress_files
    ]),

    # MCP availability
    "mcps_available": all([
        check_mcp_available(mcp) for mcp in required_mcps
    ])
}

all_valid = all(validation_results.values())
```

**Handling Validation Failures**:
```python
if not all_valid:
    failed_checks = [k for k, v in validation_results.items() if not v]

    # Categorize failures
    critical_failures = [f for f in failed_checks if f in CRITICAL_CHECKS]
    non_critical_failures = [f for f in failed_checks if f not in CRITICAL_CHECKS]

    if critical_failures:
        warn_user("Critical restoration issues detected:")
        for failure in critical_failures:
            print(f"  ❌ {failure}")
        print("\nAttempting partial restoration...")

    if non_critical_failures:
        info_user("Non-critical issues (can proceed):")
        for failure in non_critical_failures:
            print(f"  ⚠️  {failure}")
```

### Step 7: Present Restoration Summary

**Summary Report Format**:
```
✅ Context Restored Successfully

📦 Checkpoint Details:
   ID: precompact_checkpoint_20250930T143000Z
   Type: precompact
   Saved: 2025-09-30 14:30:00 UTC
   Age: 2 hours ago

📚 Memory Restoration:
   ✓ Restored 12 of 12 Serena memories
   ✓ Spec analysis: Available
   ✓ Phase plan: Available
   ✓ Wave results: 2 waves complete

🔄 Project State:
   Project: taskapp_v1
   Phase: Implementation (3 of 5)
   Wave: 3 of 5 (Database Integration)
   Progress: 40% complete

🎯 Current Focus:
   "Implementing authentication system"

📋 Pending Tasks:
   1. Complete JWT token generation
   2. Add refresh token logic
   3. Test login flow

📁 In-Progress Files:
   - /path/to/auth.ts
   - /path/to/login.tsx

🏆 Completed Waves:
   Wave 1: Frontend Components ✓
   Wave 2: Backend API ✓

🚀 Next Wave:
   Wave 3: Database Integration (in progress)
   Wave 4: Testing & Validation (planned)
   Wave 5: Deployment & Docs (planned)

🔌 MCP Status:
   ✓ Serena MCP: Connected

▶️  Ready to continue where you left off.
```

### Step 8: Resume Execution

**Continuation Logic**:
```python
# User can immediately continue working
# All context is restored, no re-specification needed

# If wave was in progress:
if current_wave_status == "in_progress":
    print(f"\nResuming Wave {current_wave}: {current_wave_name}")

    # Load wave plan
    wave_plan = read_memory(f"wave_{current_wave}_plan")

    # Check what was completed
    completed_steps = wave_plan["completed_steps"]
    remaining_steps = wave_plan["remaining_steps"]

    print(f"Completed: {len(completed_steps)} steps")
    print(f"Remaining: {len(remaining_steps)} steps")
    print(f"\nNext step: {remaining_steps[0]}")

# If between waves:
elif current_wave_status == "complete":
    print(f"\nWave {current_wave} is complete.")
    print(f"Ready to start Wave {current_wave + 1}: {next_wave_name}")
    print("\nType /shannon:wave to begin next wave")
```

---

## Outputs

Restoration summary object:

```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W2-20251103T143000",
  "checkpoint_type": "wave-checkpoint",
  "checkpoint_age_hours": 2,
  "restoration_timestamp": "2025-11-03T16:30:00Z",
  "memories_restored": {
    "total": 12,
    "critical": 4,
    "important": 5,
    "optional": 3
  },
  "project_state": {
    "project_id": "taskapp_v1",
    "active_phase": "implementation",
    "current_wave": 3,
    "total_waves": 5,
    "progress_percent": 40
  },
  "current_focus": "Implementing authentication system",
  "pending_tasks": [
    "Complete JWT token generation",
    "Add refresh token logic",
    "Test login flow"
  ],
  "in_progress_files": [
    "/path/to/auth.ts",
    "/path/to/login.tsx"
  ],
  "completed_waves": [
    {"wave_number": 1, "name": "Frontend Components"},
    {"wave_number": 2, "name": "Backend API"}
  ],
  "mcp_status": {
    "serena": "connected",
    "sequential": "available",
    "puppeteer": "not_available"
  },
  "validation": {
    "checkpoint_integrity": true,
    "all_memories_restored": true,
    "files_exist": true,
    "state_valid": true
  },
  "next_steps": [
    "Resume Wave 3: Database Integration",
    "Continue authentication implementation",
    "Run functional tests after JWT complete"
  ]
}
```

---

## Success Criteria

This skill succeeds if:

1. ✅ **Checkpoint Located**: Checkpoint found in Serena MCP and successfully retrieved
2. ✅ **Memories Restored**: All critical Serena memories loaded without errors
3. ✅ **State Valid**: Project state, wave context, and agent states are coherent
4. ✅ **Files Available**: All referenced in-progress files exist on filesystem
5. ✅ **MCPs Connected**: Required MCPs (Serena) are available and functional
6. ✅ **User Informed**: Clear restoration summary presented with next steps
7. ✅ **Resumable**: User can immediately continue work without re-specification

Validation:
```python
def validate_restoration(result):
    # Check checkpoint loaded
    assert result['success'] == True
    assert result['checkpoint_id'] is not None

    # Check memories restored
    assert result['memories_restored']['total'] > 0
    assert result['memories_restored']['critical'] > 0

    # Check state validity
    assert result['project_state']['project_id'] is not None
    assert result['project_state']['current_wave'] > 0
    assert result['project_state']['progress_percent'] >= 0

    # Check validation passed
    assert result['validation']['checkpoint_integrity'] == True
    assert result['validation']['state_valid'] == True

    # Check next steps provided
    assert len(result['next_steps']) >= 2
```

---

## Examples

### Example 1: Auto-Restore Most Recent Checkpoint

**Input:**
```json
{
  "auto_select": true
}
```

**Process:**
1. Read "latest_checkpoint" pointer from Serena
2. Retrieve checkpoint: "SHANNON-W2-20251103T143000"
3. Deserialize checkpoint JSON
4. Restore 12 Serena memories
5. Rebuild project state (Wave 2 complete, Wave 3 in progress)
6. Validate integrity (all checks pass)
7. Present restoration summary

**Output:**
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W2-20251103T143000",
  "checkpoint_age_hours": 2,
  "memories_restored": {"total": 12, "critical": 4},
  "project_state": {
    "project_id": "taskapp_v1",
    "current_wave": 3,
    "progress_percent": 40
  },
  "current_focus": "Implementing authentication system",
  "next_steps": [
    "Resume Wave 3: Database Integration",
    "Continue authentication implementation"
  ]
}
```

### Example 2: Restore Specific Checkpoint

**Input:**
```json
{
  "checkpoint_id": "SHANNON-W1-20251103T120000",
  "validate_integrity": true
}
```

**Process:**
1. Retrieve specified checkpoint from Serena
2. Verify SHA-256 integrity hash
3. Restore Wave 1 state (earlier checkpoint)
4. Warn user about potential loss of later work
5. Present restoration summary with confirmation

**Output:**
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W1-20251103T120000",
  "checkpoint_age_hours": 6,
  "warning": "This checkpoint is from 6 hours ago. Work after this point may be lost.",
  "project_state": {
    "current_wave": 1,
    "progress_percent": 15
  },
  "next_steps": ["Resume from Wave 1 completion"]
}
```

### Example 3: Restoration with Missing Memories

**Input:**
```json
{
  "checkpoint_id": "SHANNON-W3-20251103T150000"
}
```

**Process:**
1. Retrieve checkpoint from Serena
2. Attempt to restore 15 memories
3. 3 memories missing (2 optional, 1 important)
4. Partial restoration successful
5. Warn user about incomplete context

**Output:**
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W3-20251103T150000",
  "memories_restored": {"total": 12, "missing": 3},
  "warnings": [
    "3 memories could not be restored",
    "Missing: wave_2_agent_states (important)",
    "Context may be incomplete for Wave 3"
  ],
  "next_steps": [
    "Review missing context before continuing",
    "Consider re-running Wave 2 synthesis if needed"
  ]
}
```

---

## Restoration Scenarios

### Scenario 1: Auto-Compact Recovery

**Context**: Claude Code auto-compacted, context lost

**Restoration**:
```python
# User notices context loss
# User: "What were we working on?"

# Auto-detection triggers
if detect_context_loss():
    print("🔍 Context loss detected. Checking for recent checkpoint...")

    # Find most recent checkpoint
    latest = read_memory("latest_checkpoint")
    checkpoint = read_memory(latest)

    if checkpoint:
        print(f"✓ Found checkpoint: {latest}")
        print(f"  Saved: {checkpoint['metadata']['timestamp']}")
        print("\nRestoring context...")

        restore_from_checkpoint(checkpoint)

        print("✅ Context restored. Resuming from saved state.")
    else:
        print("❌ No checkpoint found. Unable to restore context.")
```

### Scenario 2: Specific Checkpoint Recovery

**Context**: User wants to restore from specific checkpoint (not latest)

**Restoration**:
```python
# User: /shannon:restore precompact_checkpoint_20250930T120000Z

checkpoint_id = "precompact_checkpoint_20250930T120000Z"

# Retrieve specific checkpoint
checkpoint = read_memory(checkpoint_id)

if checkpoint:
    print(f"Found checkpoint: {checkpoint_id}")
    print(f"Saved: {checkpoint['metadata']['timestamp']}")
    print(f"Type: {checkpoint['metadata']['checkpoint_type']}")
    print(f"\nThis will restore state from that point in time.")
    print(f"Current work after this checkpoint will be lost.")

    # Confirm before restoring
    confirm = input("Continue? (yes/no): ")

    if confirm.lower() == "yes":
        restore_from_checkpoint(checkpoint)
        print("✅ Restored from checkpoint")
    else:
        print("Cancelled")
else:
    print(f"❌ Checkpoint not found: {checkpoint_id}")

    # Show available checkpoints
    all_checkpoints = list_checkpoint_keys()
    print(f"\nAvailable checkpoints:")
    for cp in all_checkpoints[-5:]:  # Show last 5
        print(f"  - {cp}")
```

### Scenario 3: Project Switch Recovery

**Context**: User switching from Project A to Project B

**Restoration**:
```python
# User: "Switch to project taskapp_v2"

# Save current project state (if active)
if current_project:
    print(f"Saving {current_project} state...")
    create_checkpoint("manual")
    print(f"✓ {current_project} state saved")

# Load new project state
target_project = "taskapp_v2"

# Find most recent checkpoint for target project
project_checkpoints = find_project_checkpoints(target_project)

if project_checkpoints:
    latest = project_checkpoints[0]
    checkpoint = read_memory(latest)

    print(f"\nLoading {target_project}...")
    restore_from_checkpoint(checkpoint)
    print(f"✅ Switched to {target_project}")
else:
    print(f"\n⚠️  No checkpoint found for {target_project}")
    print("Starting fresh project context")
```

## Error Handling

### Missing Checkpoint

```python
def handle_missing_checkpoint(checkpoint_id):
    """Handle case where checkpoint doesn't exist"""

    print(f"❌ Checkpoint not found: {checkpoint_id}")

    # Search for similar checkpoints
    all_keys = list_memories()
    similar = fuzzy_match_keys(checkpoint_id, all_keys)

    if similar:
        print("\nDid you mean one of these?")
        for key in similar[:5]:
            print(f"  - {key}")

    # Show all available checkpoints
    checkpoint_keys = [k for k in all_keys if "checkpoint" in k]

    if checkpoint_keys:
        print("\nAll available checkpoints:")
        for key in sorted(checkpoint_keys, reverse=True)[:10]:
            cp_data = read_memory(key)
            timestamp = cp_data.get("metadata", {}).get("timestamp", "unknown")
            print(f"  - {key} ({timestamp})")
    else:
        print("\n⚠️  No checkpoints available")
        print("Consider running /shannon:checkpoint to create one")
```

### Corrupted Checkpoint

```python
def handle_corrupted_checkpoint(checkpoint_id, error):
    """Handle checkpoint that exists but is corrupted"""

    print(f"❌ Checkpoint corrupted: {checkpoint_id}")
    print(f"Error: {error}")

    # Try to extract partial data
    try:
        raw_data = read_memory(checkpoint_id)

        # Check what's salvageable
        if "project_state" in raw_data:
            print("\n✓ Project state recoverable")

        if "serena_memory_keys" in raw_data:
            print("✓ Memory keys list recoverable")

            # Try to restore memories directly
            keys = raw_data["serena_memory_keys"]
            print(f"\nAttempting to restore {len(keys)} memories directly...")

            restored = {}
            for key in keys:
                try:
                    restored[key] = read_memory(key)
                except:
                    pass

            print(f"✓ Restored {len(restored)} of {len(keys)} memories")

            if len(restored) > 0:
                print("\nPartial restoration successful")
                return restored

    except Exception as e:
        print(f"Cannot salvage checkpoint: {e}")

    # Suggest alternatives
    print("\nSuggested actions:")
    print("  1. Try restoring from different checkpoint")
    print("  2. Check Serena memory keys manually")
    print("  3. Re-analyze project if needed")
```

### Missing Memory Keys

```python
def handle_missing_memories(checkpoint_data, missing_keys):
    """Handle case where some memory keys don't exist"""

    print(f"⚠️  {len(missing_keys)} memories could not be restored:")

    # Categorize by importance
    critical = []
    important = []
    optional = []

    for key in missing_keys:
        if any(x in key for x in ["spec_analysis", "phase_plan"]):
            critical.append(key)
        elif any(x in key for x in ["wave_", "decisions"]):
            important.append(key)
        else:
            optional.append(key)

    if critical:
        print("\n❌ CRITICAL memories missing:")
        for key in critical:
            print(f"  - {key}")
        print("\nThese are required for proper restoration.")
        print("Recommend re-running specification analysis.")
        return False

    if important:
        print("\n⚠️  IMPORTANT memories missing:")
        for key in important:
            print(f"  - {key}")
        print("\nYou can continue but some context will be incomplete.")

    if optional:
        print(f"\nℹ️  {len(optional)} optional memories missing (not critical)")

    # Ask user if they want to continue
    if important:
        response = input("\nContinue with partial restoration? (yes/no): ")
        return response.lower() == "yes"

    return True  # Can continue if only optional missing
```

### MCP Unavailable

```python
def handle_mcp_unavailable(mcp_name):
    """Handle case where required MCP is not available"""

    print(f"❌ Required MCP not available: {mcp_name}")

    if mcp_name == "serena":
        print("\nSerena MCP is REQUIRED for context restoration.")
        print("Without Serena, cannot retrieve checkpoint data.")
        print("\nPlease install Serena MCP and try again:")
        print("  1. Check MCP configuration")
        print("  2. Restart Claude Code")
        print("  3. Verify Serena is running")
        return False
    else:
        print(f"\n{mcp_name} MCP is recommended but not critical.")
        print("Restoration will continue with reduced functionality.")
        return True
```

## Best Practices

### 1. Always Validate Before Restoring

```python
# Don't blindly restore - validate first
checkpoint = read_memory(checkpoint_id)

# Check age
age = calculate_age(checkpoint["metadata"]["timestamp"])
if age > timedelta(days=7):
    warn_user(f"Checkpoint is {age.days} days old")

# Check compatibility
if checkpoint["metadata"]["shannon_version"] != CURRENT_VERSION:
    warn_user("Checkpoint from different Shannon version")

# Check project
if checkpoint["project_state"]["project_id"] != current_project:
    confirm_user("Restoring different project. Continue?")
```

### 2. Prefer Auto-Selection Unless Specific Need

```python
# Good: Let skill find best checkpoint
restore_from_latest()

# Acceptable: User has specific reason
restore_from_checkpoint("phase_2_complete_checkpoint")

# Avoid: Randomly picking old checkpoints
restore_from_checkpoint("checkpoint_from_last_week")
```

### 3. Log Restoration Events

```python
# Create audit trail
write_memory(f"restore_log_{timestamp()}", {
    "checkpoint_used": checkpoint_id,
    "restoration_time": current_time(),
    "memories_restored": len(restored_memories),
    "success": all_valid,
    "missing_memories": missing_keys,
    "warnings": warnings
})
```

### 4. Handle Graceful Degradation

```python
# If full restoration fails, try partial
if not restore_all_context():
    print("Full restoration failed. Attempting partial...")

    # Restore in priority order
    for priority in ["critical", "important", "optional"]:
        try:
            restore_by_priority(priority)
        except:
            continue

    print("Partial restoration complete")
    print("Some features may be unavailable")
```

## Integration with Other Skills

### With context-checkpoint

```python
# Checkpoint saves state
checkpoint_id = context_checkpoint.create()

# Restoration loads state
context_restoration.restore(checkpoint_id)

# Round-trip preservation
assert original_state == restored_state
```

### With spec-analysis

```python
# If spec analysis missing after restore
if "spec_analysis" not in restored_memories:
    print("⚠️  Specification analysis not found in checkpoint")
    print("Re-running analysis...")

    # Trigger spec-analysis skill
    spec_analysis.analyze(project_path)
```

### With wave-orchestration

```python
# Restore wave context for continuation
wave_context = {
    "current_wave": checkpoint["project_state"]["current_wave"],
    "completed_waves": checkpoint["wave_context"]["completed_waves"],
    "pending_waves": checkpoint["wave_context"]["pending_waves"]
}

# Pass to wave orchestration
wave_orchestration.resume(wave_context)
```

## References

- **CONTEXT_MANAGEMENT.md**: Core checkpoint/restore patterns
- **PreCompact Hook**: Auto-checkpoint before compact
- **Serena MCP**: Persistent memory storage

## Summary

Context restoration provides zero-downtime recovery from context loss events through:

1. **Checkpoint Retrieval**: Load saved state from Serena MCP
2. **State Deserialization**: Parse checkpoint JSON structure
3. **Context Restoration**: Rebuild project/wave/agent state
4. **Validation**: Ensure integrity and availability
5. **Continuation**: Resume from exact interruption point

**Result**: Users experience seamless continuation across session boundaries with complete preservation of work state.
