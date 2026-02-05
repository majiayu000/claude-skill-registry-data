---
name: findings
description: |
  Persistent memory system for Claude Code. Captures discoveries, tech debt, and unfinished work
  that persists across sessions. Use for cross-session continuity and sharing findings with team.
  Triggers: "remember this", "capture finding", "what did I find", "session context", "load context",
  "save session", "findings", "discoveries", "tech debt to track", "don't forget", "note for later",
  "carry forward", "handoff notes", "open findings", "ready to work on".
---

# Findings - Persistent Memory for Claude Code

A git-tracked memory system that solves the "50 First Dates" problem: Claude wakes up each session
with no memory of what was discovered yesterday. This skill provides persistent storage for findings,
discoveries, and session context.

## The Problem

Without persistent memory:
- Discoveries are forgotten between sessions
- Tech debt identified in reviews is lost
- No handoff between Claude sessions
- Team can't see what AI agents found

## The Solution

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION CONTINUITY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session 1                   Session 2                           │
│  ─────────                   ─────────                           │
│  • Discovers N+1 query       • Loads context                     │
│  • Captures finding          • Sees open findings                │
│  • Saves session context     • Continues work                    │
│                                                                  │
│        ┌──────────────────────────────────────┐                  │
│        │  .findings/findings.jsonl            │ ◄── Git-tracked  │
│        │  (Persistent, team-visible)          │                  │
│        └──────────────────────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### At Session Start

```bash
# Load context from previous sessions
python3 skills/findings/scripts/session_context.py --load

# See what's ready to work on
python3 skills/findings/scripts/query_findings.py --ready
```

### During Session

```bash
# Capture a discovery
python3 skills/findings/scripts/query_findings.py --capture \
  --title "N+1 query in OrderService.GetAllWithDetails" \
  --severity medium \
  --type discovery \
  --category performance \
  --file "src/Services/OrderService.cs" \
  --line 145

# See open findings
python3 skills/findings/scripts/query_findings.py --open

# Search findings
python3 skills/findings/scripts/query_findings.py --search "N+1"
```

### At Session End

```bash
# Save session context with handoff notes
python3 skills/findings/scripts/session_context.py --save \
  --notes "Fixed N+1 in GetAllWithDetails, still need to address GetOrderHistory"
```

## CLI Reference

### query_findings.py

| Command | Description |
|---------|-------------|
| `--capture --title "..."` | Capture a new finding |
| `--open` | Show open findings |
| `--ready` | Show findings ready to work on (not blocked) |
| `--blocked` | Show blocked findings |
| `--branch` | Show findings for current git branch |
| `--search "term"` | Search in title and description |
| `--show f-abc123` | Show details for a finding |
| `--resolve f-abc123` | Mark finding as resolved |
| `--promote f-abc123 --promote-to AB#1234` | Link to ADO work item |
| `--stats` | Show statistics |
| `--compact` | Analyze JSONL for compaction |
| `--archive-older-than DURATION` | Archive old closed findings (e.g., 30d, 90d) |
| `--summarize-older-than DURATION` | Create summary of old findings |
| `--use-sqlite` | Enable SQLite cache for faster queries |
| `--rebuild-sqlite` | Rebuild SQLite cache from JSONL |

### Capture Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title` | Finding title (required) | - |
| `--description, -d` | Detailed description | "" |
| `--type, -t` | discovery, todo, question, note, tech-debt, bug | discovery |
| `--severity, -s` | critical, high, medium, low, info | medium |
| `--category, -c` | performance, security, thread-safety, etc. | other |
| `--file` | File path where found | - |
| `--line` | Line number | - |
| `--snippet` | Code snippet | - |
| `--function` | Function name | - |
| `--tags` | Space-separated tags | - |
| `--priority, -p` | 1-4 (like ADO) | 3 |
| `--during` | What activity found this | - |
| `--eval` | Link to eval-framework result | - |
| `--ado` | Link to ADO work item | - |

### session_context.py

| Command | Description |
|---------|-------------|
| `--load` | Start session, load previous context |
| `--save` | End session, save handoff notes |
| `--show` | Show current context summary |
| `--onboard` | Output full onboarding prompt |
| `--notes "..."` | Handoff notes (use with --save) |
| `--questions "..." "..."` | Open questions (use with --save) |

### Output Formats

All commands support:
- `--json` - JSON output for programmatic use
- `--table` - Tabular output
- `--verbose, -v` - Detailed output

## Cross-Repo Global Store

The findings system supports a **global store** that aggregates findings across all your repositories.
This enables cross-project pattern discovery and search.

```
┌─────────────────────────────────────────────────────────────────┐
│                      TWO-TIER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Per-Repo (Local)                    Global (Centralized)       │
│   ─────────────────                   ────────────────────       │
│   .findings/findings.jsonl            ~/.claude/findings/        │
│   - Git-tracked                       - NOT git-tracked          │
│   - Team-visible                      - Personal aggregation     │
│   - Repo-specific                     - Cross-repo patterns      │
│                                                                  │
│        ┌──────────┐                       ┌──────────────┐       │
│        │ repo-a/  │ ───push──────────────►│              │       │
│        │ findings │                       │    global    │       │
│        └──────────┘                       │   findings   │       │
│        ┌──────────┐                       │    store     │       │
│        │ repo-b/  │ ───push──────────────►│              │       │
│        │ findings │                       │              │       │
│        └──────────┘                       └──────────────┘       │
│                                                  │               │
│        Any Repo ◄────────────────cross-repo search               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Global Store Commands

```bash
# Push local findings to global store
python3 query_findings.py --push-to-global

# Query global store (all repos)
python3 query_findings.py --global

# Search across all repositories
python3 query_findings.py --all-repos --search "N+1 query"

# Find similar findings across repos
python3 query_findings.py --similar "N+1 query in OrderService"

# Filter by source repo
python3 query_findings.py --global --from-repo "my-project"
```

### sync_findings.py

Dedicated script for sync operations:

| Command | Description |
|---------|-------------|
| `--push` | Push all local findings to global |
| `--push --id f-abc123` | Push specific finding |
| `--repos` | List all registered repositories |
| `--status` | Show sync status for current repo |
| `--stats` | Show global statistics |
| `--search "term"` | Search across all repos |
| `--similar "text"` | Find similar findings |
| `--global` | Query global findings |
| `--global --open` | Query open global findings |

### Privacy

Findings with `private` tag are not synced to global:

```bash
# This finding stays local only
python3 query_findings.py --capture \
  --title "Internal investigation notes" \
  --tags private sensitive
```

Configure privacy in `~/.claude/findings/config.json`:

```json
{
  "privacy": {
    "exclude_tags": ["private", "sensitive", "personal"]
  }
}
```

## Storage

### Local (Per-Repo)

```
.findings/
├── findings.jsonl        # Git-tracked (source of truth)
├── index.json            # Git-ignored (fast lookup cache)
├── session-context.json  # Git-ignored (current session state)
└── .gitignore           # Excludes local files
```

### Global (Cross-Repo)

```
~/.claude/findings/
├── global-findings.jsonl  # All synced findings
├── index.json             # Fast lookup cache
├── repositories.json      # Registry of known repos
└── config.json            # Sync and privacy settings
```

### findings.jsonl Format

One JSON object per line (append-only log):

```json
{
  "id": "f-a1b2c3d4",
  "version": 1,
  "title": "N+1 query in OrderService",
  "finding_type": "discovery",
  "severity": "medium",
  "category": "performance",
  "status": "open",
  "evidence": {
    "file": "src/Services/OrderService.cs",
    "line": 145
  },
  "branch": "feature/AB#1234-order-optimization",
  "discovered_at": "2025-12-15T10:30:00Z",
  "created_at": "2025-12-15T10:30:00Z"
}
```

## Integration with Other Skills

### With architecture-review

During architecture reviews, capture findings:

```bash
# Capture finding from review
python3 skills/findings/scripts/query_findings.py --capture \
  --title "Thread safety issue in StateManager" \
  --severity critical \
  --type discovery \
  --category thread-safety \
  --during "architecture-review" \
  --eval "arch-review-2025-12-15-eval-abc123"
```

### With azure-devops

Promote findings to official work items:

```bash
# Option 1: Auto-create ADO work item from finding (recommended)
python3 skills/findings/scripts/promote_to_ado.py f-abc123

# Option 2: Promote as specific type
python3 skills/findings/scripts/promote_to_ado.py f-abc123 --type Bug

# Option 3: Dry run to see what would be created
python3 skills/findings/scripts/promote_to_ado.py f-abc123 --dry-run

# Option 4: Manual linking (if you created the item separately)
python3 skills/findings/scripts/query_findings.py \
  --promote f-abc123 --promote-to AB#5678
```

### With eval-framework

Extract findings from evaluation results:

```bash
# Import all findings from an eval result
python3 skills/findings/scripts/findings_from_eval.py \
  --eval-file .eval-results/arch-review-2025-12-15.yaml

# Import only high+ severity, skip already-fixed
python3 skills/findings/scripts/findings_from_eval.py \
  --eval-file .eval-results/arch-review-2025-12-15.yaml \
  --min-severity high --skip-fixed

# Link existing finding to eval result
python3 skills/findings/scripts/link_eval_results.py \
  --finding f-abc123 --eval arch-review-2025-12-15-eval-xyz

# Show findings linked to an eval
python3 skills/findings/scripts/link_eval_results.py \
  --show-eval arch-review-2025-12-15-eval-xyz
```

### Dependency Management

Track blocking relationships between findings:

```bash
# Mark one finding as blocking another
python3 skills/findings/scripts/query_findings.py \
  --block f-auth-fix f-user-registration

# Remove blocking relationship
python3 skills/findings/scripts/query_findings.py \
  --unblock f-auth-fix f-user-registration

# Mark findings as related
python3 skills/findings/scripts/query_findings.py \
  --relate f-abc123 f-def456

# Show dependencies for a finding
python3 skills/findings/scripts/query_findings.py --show-deps f-abc123

# Show only ready (unblocked) findings
python3 skills/findings/scripts/query_findings.py --ready

# Show blocked findings
python3 skills/findings/scripts/query_findings.py --blocked
```

## Finding Types

| Type | Use Case |
|------|----------|
| `discovery` | Something found during exploration or review |
| `todo` | Task to complete |
| `question` | Question to investigate |
| `note` | General note or observation |
| `tech-debt` | Technical debt to address |
| `bug` | Bug found but not yet filed |

## Categories

Aligned with eval-framework for consistency:

| Category | Description |
|----------|-------------|
| `thread-safety` | Concurrency, race conditions, deadlocks |
| `resource-management` | Memory leaks, connection leaks |
| `error-handling` | Exception handling, recovery |
| `state-management` | State machines, persistence |
| `external-operations` | Timeouts, retries, external calls |
| `api-web-layer` | Validation, input handling |
| `configuration` | Config, secrets, credentials |
| `code-consistency` | Patterns, dead code, naming |
| `security` | Auth, injection, XSS |
| `performance` | Optimization, N+1 queries |
| `architecture` | Design, structure, patterns |
| `testing` | Test coverage, testability |
| `documentation` | Missing or outdated docs |
| `other` | Default category |

## Workflow Examples

### Daily Workflow

```bash
# Morning: Start session
python3 skills/findings/scripts/session_context.py --load

# See what's ready
python3 skills/findings/scripts/query_findings.py --ready

# Work on a finding...

# End of day: Save context
python3 skills/findings/scripts/session_context.py --save \
  --notes "Worked on f-abc123, needs testing" \
  --questions "Should we use Include() or explicit loading?"
```

### Code Review Workflow

```bash
# During review, capture findings
python3 skills/findings/scripts/query_findings.py --capture \
  --title "Missing null check in ProcessOrder" \
  --severity high \
  --type bug \
  --file "src/Orders/OrderProcessor.cs" \
  --line 89

# After review, show all findings
python3 skills/findings/scripts/query_findings.py --branch
```

### Architecture Review Workflow

```bash
# Capture multiple findings during review
for finding in findings_from_review; do
  python3 skills/findings/scripts/query_findings.py --capture \
    --title "$finding" \
    --during "architecture-review" \
    --eval "$EVAL_ID"
done

# Later, promote critical ones to ADO
python3 skills/findings/scripts/query_findings.py --open --filter-severity critical
```

## Best Practices

1. **Capture liberally** - It's cheap to store findings, expensive to rediscover them
2. **Use meaningful titles** - The title should explain the issue
3. **Link to evidence** - Include file, line, snippet when possible
4. **Set appropriate severity** - Helps prioritize work
5. **Save session context** - Handoff notes make the next session productive
6. **Review before ADO promotion** - Not everything needs to be a work item
7. **Compact periodically** - Run `--compact --compact-apply` to clean up

## Troubleshooting

### "No findings found" but I know there are some

```bash
# Rebuild index from JSONL
rm .findings/index.json
python3 skills/findings/scripts/query_findings.py --stats
```

### JSONL file getting large

```bash
# Check compaction potential
python3 skills/findings/scripts/query_findings.py --compact

# Apply compaction
python3 skills/findings/scripts/query_findings.py --compact --compact-apply
```

### Session context not loading

```bash
# Check context file exists
cat .findings/session-context.json

# Reset if corrupted
rm .findings/session-context.json
python3 skills/findings/scripts/session_context.py --load
```

## References

- Inspired by [beads](https://github.com/steveyegge/beads) - Git-based issue tracker for AI agents
- Design doc: [docs/memory-system-design.md](/Users/sean/source/tools/claude-tools/docs/memory-system-design.md)
