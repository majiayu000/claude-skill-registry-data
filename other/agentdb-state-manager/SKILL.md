---
name: agentdb-state-manager
version: 1.0.0
description: |
  Persistent state management using AgentDB (DuckDB) for workflow analytics and checkpoints.

  Provides read-only analytics cache synchronized from TODO_*.md files, enabling:
  - Complex dependency graph queries
  - Historical workflow metrics
  - Context checkpoint storage/recovery
  - State transition analysis

  Use when: Data gathering and analysis for workflow state tracking

  Triggers: "analyze workflow", "query state", "checkpoint", "workflow metrics"
---

# AgentDB State Manager Skill

## Purpose

The AgentDB State Manager provides persistent database storage for workflow state tracking using DuckDB through Claude Code's AgentDB integration. This skill enables:

- **Read-only analytics**: Complex queries over workflow history without parsing files
- **Checkpoint management**: Store/recover context checkpoints at 100K token threshold
- **Dependency resolution**: Query task dependencies and critical paths
- **Metrics analysis**: Historical trends, time-in-phase, bottleneck identification

**Primary source of truth:** TODO_*.md files (AgentDB is an analytics cache)

**Primary purpose:** Data gathering and analysis

**Workflow phase:** Cross-phase (Utilities) - All phases (1-6)

## When to Use

Use this skill when:
- Querying complex task dependencies or critical paths
- Analyzing workflow metrics (time-in-phase, completion rates)
- Storing context checkpoints at 100K tokens
- Tracking state transitions and historical trends
- Avoiding repetitive TODO file parsing for analytics

**Triggered by keywords:** "analyze workflow", "query state", "checkpoint", "workflow metrics", "task dependencies"

## Integration with Workflow

**Phase integration:** Cross-phase (Utilities)

This skill integrates with all workflow phases:

**Phase 0 (Setup):**
- Initialize AgentDB schema on first use
- Load canonical state definitions from workflow-states.json

**Phase 1 (Planning - BMAD):**
- Track BMAD Q&A responses
- Store epic definitions and requirements

**Phase 2 (Specification + Implementation):**
- Sync tasks from TODO_*.md to AgentDB
- Query task dependencies for parallel execution
- Track implementation progress

**Phase 3 (Quality):**
- Store quality gate results
- Track test coverage trends
- Historical quality metrics

**Phase 4 (Integration):**
- Store as-built deviation data
- Metrics for feedback loop
- Compare planning vs actual

**Phase 5 (Release):**
- Release workflow state tracking
- Final QA checkpoint data

**Phase 6 (Hotfix):**
- Hotfix-specific state tracking
- Emergency rollback data

**Context checkpoints (all phases):**
- Store checkpoint at 100K tokens
- Faster resume with structured queries vs file parsing

**Orchestrator integration:**
- workflow-orchestrator optionally calls AgentDB for complex queries
- Fallback to file parsing if AgentDB unavailable
- Automatic sync after TODO file updates

## Official Documentation Alignment

This skill follows the local workflow system patterns which extend official Claude Code skill specifications:

**Official Claude Code Skills:**
- Specification: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- Building Agents: https://docs.claude.com/en/docs/agents-and-tools/building-agents
- AgentDB Documentation: (Reference from TODO_agentdb-prompt-template.md)

**Local Pattern Extensions:**

**file_structure:**
- Local: ['SKILL.md', 'CLAUDE.md', 'README.md', 'CHANGELOG.md', 'ARCHIVED/', 'scripts/', 'templates/']
- Official: ['skill.md', 'README.md']
- Rationale: Extended structure supports multi-phase workflow with version tracking, context files, and archived materials

**frontmatter:**
- Local: YAML with 'name', 'version', 'description' fields
- Official: YAML with 'name', 'description' fields only
- Rationale: 'version' field enables semantic versioning integration with validate_versions.py and UPDATE_CHECKLIST.md workflow

**directory_organization:**
- Local: scripts/, templates/ subdirectories
- Official: Flat structure with skill.md
- Rationale: Separates Python code (scripts/) from templates (workflow-states.json) for better maintainability

These extensions support the multi-phase workflow system while maintaining compatibility with core Claude Code concepts.

## Architecture

### Data Flow (Read-Only Analytics Mode)

```
TODO_*.md (source of truth)
    ↓
sync_todo_to_db.py
    ↓
AgentDB (DuckDB)
    ↓
query_state.py / analyze_metrics.py
    ↓
Analytics results
```

### Session ID Generation

AgentDB requires a session ID for database identification. This skill uses:

**Method: Timestamp-based (reproducible)**
```python
from datetime import datetime
import hashlib

# Generate session ID from current timestamp
current_time = datetime.utcnow().isoformat()
session_id = hashlib.md5(current_time.encode()).hexdigest()[:16]
# Example: "f8e7d6c5b4a39281"
```

**Rationale:** Provides reproducible session IDs across agent invocations within the same timeframe, balancing uniqueness with reproducibility.

### Schema Design (Immutable Append-Only)

**Core principle:** NEVER UPDATE or DELETE records - always INSERT new records

**Primary table: workflow_records**
```sql
CREATE TABLE IF NOT EXISTS workflow_records (
    record_id UUID PRIMARY KEY DEFAULT uuid(),
    record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
    object_id VARCHAR NOT NULL,     -- Stable ID for workflow object
    object_type VARCHAR NOT NULL,   -- 'feature', 'task', 'epic', etc.
    object_state VARCHAR NOT NULL,  -- '20_in-progress', '99_done', etc.
    object_metadata JSON             -- Framework, dependencies, etc.
);

CREATE INDEX idx_records_object
ON workflow_records(object_id, record_datetimestamp DESC);
```

**Current state query pattern:**
```sql
-- Get latest state for each object
SELECT DISTINCT ON (object_id)
    object_id, object_type, object_state, object_metadata
FROM workflow_records
WHERE object_type = 'task'
ORDER BY object_id, record_datetimestamp DESC;
```

## Usage

### 1. Initialize AgentDB (First Use)

```bash
# Initialize database schema and load state definitions
python .claude/skills/agentdb-state-manager/scripts/init_database.py
```

**What it does:**
- Creates workflow_records table
- Loads workflow-states.json
- Sets up indexes for efficient queries
- Stores session metadata

### 2. Sync TODO Files to AgentDB

```bash
# Sync all TODO_*.md files to database
python .claude/skills/agentdb-state-manager/scripts/sync_todo_to_db.py

# Sync specific TODO file
python .claude/skills/agentdb-state-manager/scripts/sync_todo_to_db.py \
  TODO_feature_20251023T143000Z_my-feature.md
```

**What it does:**
- Parses YAML frontmatter from TODO files
- Converts to immutable append-only records
- Stores workflow progress, tasks, quality gates
- Preserves full state history

### 3. Query Current Workflow State

```bash
# Get current state of all workflows
python .claude/skills/agentdb-state-manager/scripts/query_state.py

# Query specific workflow
python .claude/skills/agentdb-state-manager/scripts/query_state.py \
  --slug my-feature

# Query task dependencies
python .claude/skills/agentdb-state-manager/scripts/query_state.py \
  --dependencies --task impl_003
```

**What it does:**
- Queries latest state for each object
- Resolves task dependencies
- Identifies blocked tasks
- Shows critical path

### 4. Analyze Workflow Metrics

```bash
# Generate metrics report
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py

# Historical trends
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py \
  --trends --days 30

# Bottleneck analysis
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py \
  --bottlenecks
```

**What it does:**
- Calculates time-in-phase for workflows
- Identifies bottlenecks and slow phases
- Tracks quality gate pass/fail rates
- Compares planning estimates vs actual

### 5. Context Checkpoint Management

```bash
# Store checkpoint at 100K tokens
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py \
  store --todo TODO_feature_*.md

# List available checkpoints
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py list

# Restore from checkpoint
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py \
  restore --checkpoint-id <uuid>
```

**What it does:**
- Stores complete workflow state to AgentDB
- Records token count, phase, step, last task
- Provides resume instructions
- Faster recovery than parsing TODO files

## Best Practices

### 1. AgentDB as Analytics Cache

**✓ DO:** Treat TODO_*.md files as source of truth
**✗ DON'T:** Modify TODO files based on AgentDB state

**Rationale:** Files are git-tracked and permanent; AgentDB sessions last 24 hours

### 2. Sync After TODO Updates

**✓ DO:** Run sync_todo_to_db.py after every TODO file update
**✗ DON'T:** Let AgentDB state drift from file state

**Rationale:** AgentDB is a cache - it must stay synchronized

### 3. Use for Complex Queries Only

**✓ DO:** Use AgentDB for dependency graphs, metrics, historical analysis
**✗ DON'T:** Use for simple current state queries (parse TODO file instead)

**Rationale:** Minimize token overhead - use database for queries that justify the cost

### 4. Immutable Records

**✓ DO:** Always INSERT new records for state changes
**✗ DON'T:** UPDATE or DELETE existing records

**Rationale:** Preserves full history for temporal analysis

### 5. Session Lifetime Awareness

**✓ DO:** Re-initialize at session start if needed
**✗ DON'T:** Assume AgentDB persists across days

**Rationale:** 24-hour auto-deletion - treat as ephemeral cache

## Scripts Reference

### init_database.py
**Purpose:** Initialize AgentDB schema and load state definitions
**When to run:** First use in a session, or if schema corrupted
**Token cost:** ~300-400 tokens

### sync_todo_to_db.py
**Purpose:** Sync TODO_*.md files to AgentDB
**When to run:** After every TODO file update
**Token cost:** ~200-300 tokens per TODO file

### query_state.py
**Purpose:** Query current workflow state and dependencies
**When to run:** Complex state queries (dependency graphs, critical paths)
**Token cost:** ~100-200 tokens per query

### analyze_metrics.py
**Purpose:** Historical metrics and trend analysis
**When to run:** End of phase, workflow retrospectives
**Token cost:** ~400-600 tokens (complex queries)

### checkpoint_manager.py
**Purpose:** Store/restore context checkpoints
**When to run:** At 100K token threshold, or before context reset
**Token cost:** ~200-400 tokens (store + verify)

## Token Efficiency

### Before AgentDB (Manual File Parsing)

**Complex dependency query:**
1. Read TODO_*.md file (~1,500 tokens)
2. Parse YAML frontmatter (~500 tokens)
3. Iterate through tasks (~1,000 tokens)
4. Resolve dependencies (~800 tokens)
**Total:** ~3,800 tokens

### After AgentDB (Database Query)

**Same query:**
1. Run query_state.py --dependencies (~200 tokens)
2. Parse SQL results (~100 tokens)
**Total:** ~300 tokens

**Savings:** ~3,500 tokens (92% reduction) for complex queries

### Context Checkpoint Recovery

**Before AgentDB:**
- Parse TODO_*.md (~1,500 tokens)
- Reconstruct state (~1,000 tokens)
- Determine next step (~800 tokens)
**Total:** ~3,300 tokens

**After AgentDB:**
- Query checkpoint table (~150 tokens)
- Load resume instructions (~100 tokens)
**Total:** ~250 tokens

**Savings:** ~3,050 tokens (92% reduction)

## Integration with Other Skills

### workflow-orchestrator
- Calls query_state.py for complex next-step determination
- Uses checkpoint_manager.py at 100K tokens
- Falls back to file parsing if AgentDB unavailable

### workflow-utilities
- todo_updater.py triggers sync_todo_to_db.py after updates
- Dual write: update file + sync to database

### speckit-author
- Uses AgentDB for as-built metrics (update_asbuilt.py)
- Queries historical planning accuracy

### quality-enforcer
- Stores quality gate results to AgentDB
- Tracks coverage trends over time

### bmad-planner
- Stores BMAD Q&A responses
- Epic definition tracking

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Claude Code usage context
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[templates/workflow-states.json](templates/workflow-states.json)** - Canonical state definitions

## Related Skills

- **workflow-orchestrator** - Calls AgentDB for complex queries
- **workflow-utilities** - Triggers sync after TODO updates
- **speckit-author** - Uses for as-built metrics
- **quality-enforcer** - Stores quality gate results
- **bmad-planner** - Stores planning data

## Limitations

1. **Session lifetime:** AgentDB persists for 24 hours, then auto-deleted
2. **Source of truth:** TODO_*.md files remain authoritative
3. **Sync overhead:** ~200-300 tokens per sync operation
4. **DuckDB constraints:** Optimized for OLAP (analytics), not OLTP (transactions)
5. **No vector search:** Unlike PostgreSQL pgvector

## Academic References

This skill implements the **MIT Agent Synchronization Pattern** based on:

> **Meng, E., & Jackson, D. (2025).** "What You See Is What It Does: A Structural Pattern for Legible Software."
> *Onward! at SPLASH 2025*. arXiv:2508.14511v1.
> https://arxiv.org/abs/2508.14511

**Key concepts from the paper:**
- **Concepts**: Fully independent services (implemented as agents/worktrees)
- **Synchronizations**: Event-based rules mediating between services (implemented as `agent_synchronizations` table)

The pattern improves incrementality, integrity, and transparency in multi-agent workflows.

## Version History

**v1.0.0 (2025-11-02):**
- Initial release
- Read-only analytics mode
- Sync from TODO files to AgentDB
- Complex query support (dependencies, metrics)
- Context checkpoint storage
- All phases (1-6) integration
