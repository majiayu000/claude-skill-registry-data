---
name: beads-agent-village
description: Set up and orchestrate multi-agent workflows using Beads (shared issue tracking/memory) and MCP Agent Mail (agent messaging). Use when coordinating multiple agents, setting up agent villages, tracking work across agent sessions, or implementing swarm workflows.
---

# Beads + Agent Mail: Multi-Agent Workflows

Beads provides shared memory and issue tracking for agents. MCP Agent Mail provides agent-to-agent messaging. Together they create an "Agent Village" where agents can coordinate autonomously.

## Quick Start

### 1. Initialize Beads in Your Project

```bash
# Install Beads
go install github.com/steveyegge/beads/cmd/bd@latest

# Initialize in your project
bd init

# Run doctor to set up git hooks and configuration
bd doctor --fix
```

### 2. Configure Your Agent

Add to your `CLAUDE.md` or `AGENTS.md`:

```markdown
## Issue Tracking

Use Beads (`bd`) for all work tracking. Run `bd quickstart` to get started.

- File issues for any work taking longer than 2 minutes
- Check `bd ready --json` to find unblocked work
- Update issue status as you work
- File discovered bugs/issues immediately rather than ignoring them
```

### 3. Set Up Agent Mail (Optional)

For multi-agent coordination, add MCP Agent Mail:

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail/main/scripts/install.sh" | bash -s -- --yes
```

## Core Beads Commands

| Command | Purpose |
|---------|---------|
| `bd init` | Initialize Beads in a project |
| `bd doctor [--fix]` | Diagnose and fix issues, run migrations |
| `bd ready --json` | List unblocked work items ready for execution |
| `bd cleanup --days N` | Remove issues older than N days |
| `bd sync` | Sync database and push to git |
| `bd upgrade` | Upgrade Beads to latest version |

## Best Practices

### Keep the Database Small

Run `bd cleanup` every few days. Keep under 200-500 issues for best performance:

```bash
bd cleanup --days 2
bd sync
```

### Use Short Issue Prefixes

Configure a 2-3 character prefix for readability:

```bash
# Examples: bd-, vc-, wy-, ef-
bd config prefix my-
```

### Plan Outside, Execute Inside

1. Create your plan using your preferred planning tool
2. Iterate and refine the plan up to 5 times with the agent
3. Ask the agent to file Beads epics and issues from the plan, focusing on:
   - Dependencies between tasks
   - Detailed designs
   - Potential parallelization
4. Iterate and refine the Beads epics up to 5 times
5. Execute by having agents work through `bd ready` items

The agent will say "I don't think we can do much better than this" when iteration is complete.

### Restart Agents Frequently

- Tackle one issue per agent session
- Kill the process after completing each issue
- Beads maintains context between sessions
- Saves money and improves model performance

### File Issues Liberally

Agents should file issues for:
- Any work taking > 2 minutes
- Discovered bugs (even if "unrelated") - use `--discovered-from` to link to parent issue
- Code review findings
- Technical debt noticed during work

When doing code reviews, tell agents to file beads as they go - this produces more actionable findings.

```bash
# Link a discovered bug to the issue you were working on
bd create --title "Fix null check in auth" --discovered-from ISSUE-123
```

## Multi-Agent Coordination

### Agent Village Setup

Two approaches for multi-agent work:

**Git Worktree Model** (Recommended):
- Each agent works in its own git worktree/branch
- No file locking needed
- Use Agent Mail for coordination
- Merge work via git

**Single Folder Model**:
- All agents share one folder
- Use Agent Mail's file reservation system
- Agents negotiate file access via messaging

### Agent Mail Integration

With Beads + Agent Mail, agents can:
- Share memory (Beads issues as shared state)
- Send messages to coordinate
- Self-organize leadership and task splitting
- Work autonomously with minimal setup

Just tell agents: "Go sort it out amongst yourselves" - they will:
1. Quickly decide on a leader
2. Split up the work
3. Coordinate via messaging
4. Track progress in Beads

### Work Claiming

Agents claim work by setting status and assignee:

```bash
# Check what's available (filter by assignee if needed)
bd ready --json
bd ready --json --assignee=agent1

# Claim an issue
bd update ISSUE-123 --status in_progress --assignee agent1

# Other agents can see what's claimed
bd list --status in_progress
```

Multiple agents on different machines can query the same Beads database via git.

## Troubleshooting

### Merge Conflicts

Beads conflicts happen during rebases/merges. Ask your agent to:
- Clean up broken rebases
- Resolve conflicts intelligently
- Run `bd doctor --fix` after resolution

### Large Database Issues

If `issues.jsonl` exceeds ~25k tokens:
- Run `bd cleanup --days 2`
- Issues remain in git history for reference
- Keep working set small for agent file reading

### Daily Maintenance

Run daily:
```bash
bd doctor
bd upgrade  # weekly
```

## Example Workflow

```bash
# Morning: Check what's ready
bd ready --json

# Claim an issue
bd update ISSUE-123 --status in_progress --assignee agent1

# During work: file discovered issues with link to parent
bd create --title "Fix flaky test in auth module" --discovered-from ISSUE-123

# Complete work
bd update ISSUE-123 --status done
bd sync

# End of session: cleanup
bd cleanup --days 2
```

## Beads Viewer (bv)

A terminal UI for visualizing Beads issues and dependencies.

### Installation

One-line installer:

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.sh?$(date +%s)" | bash
```

Or build from source (requires Go 1.21+):

```bash
git clone https://github.com/Dicklesworthstone/beads_viewer.git
cd beads_viewer
go install ./cmd/bv
```

### Usage

Navigate to any Beads-initialized project and run:

```bash
bv
```

The viewer automatically discovers `.beads/beads.jsonl` in your current directory.

### Key Navigation

| Key | Action |
|-----|--------|
| `j`/`k` | Navigate items |
| `/` | Fuzzy search |
| `b` | Kanban board view |
| `i` | Insights dashboard |
| `g` | Dependency graph |
| `h` | History (commit correlation) |
| `?` | Show all keyboard shortcuts |
| `` ` `` | Built-in tutorial |
| `q` | Quit |

### Custom Directory

For monorepos or non-standard layouts:

```bash
BEADS_DIR=/path/to/shared/beads bv
```

## Using Beads Viewer with Agents

bv is a graph-aware triage engine for Beads projects. Instead of parsing JSONL or hallucinating graph traversal, use robot flags for deterministic, dependency-aware outputs with precomputed metrics (PageRank, betweenness, critical path, cycles, HITS, eigenvector, k-core).

**Scope boundary:** bv handles *what to work on* (triage, priority, planning). For agent-to-agent coordination (messaging, work claiming, file reservations), use [MCP Agent Mail](https://github.com/Dicklesworthstone/mcp_agent_mail).

**CRITICAL: Use ONLY `--robot-*` flags. Bare `bv` launches an interactive TUI that blocks your session.**

### The Workflow: Start With Triage

**`bv --robot-triage` is your single entry point.** It returns everything you need in one call:
- `quick_ref`: at-a-glance counts + top 3 picks
- `recommendations`: ranked actionable items with scores, reasons, unblock info
- `quick_wins`: low-effort high-impact items
- `blockers_to_clear`: items that unblock the most downstream work
- `project_health`: status/type/priority distributions, graph metrics
- `commands`: copy-paste shell commands for next steps

```bash
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick + claim command
```

### Planning Commands

| Command | Returns |
|---------|---------|
| `--robot-plan` | Parallel execution tracks with `unblocks` lists |
| `--robot-priority` | Priority misalignment detection with confidence |

### Graph Analysis

| Command | Returns |
|---------|---------|
| `--robot-insights` | Full metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core, articulation points, slack |
| `--robot-label-health` | Per-label health: `health_level` (healthy/warning/critical), `velocity_score`, `staleness`, `blocked_count` |
| `--robot-label-flow` | Cross-label dependency: `flow_matrix`, `dependencies`, `bottleneck_labels` |
| `--robot-label-attention [--attention-limit=N]` | Attention-ranked labels by: (pagerank × staleness × block_impact) / velocity |

### History & Change Tracking

| Command | Returns |
|---------|---------|
| `--robot-history` | Bead-to-commit correlations: `stats`, `histories` (per-bead events/commits/milestones), `commit_index` |
| `--robot-diff --diff-since <ref>` | Changes since ref: new/closed/modified issues, cycles introduced/resolved |

### Other Robot Commands

| Command | Returns |
|---------|---------|
| `--robot-burndown <sprint>` | Sprint burndown, scope changes, at-risk items |
| `--robot-forecast <id\|all>` | ETA predictions with dependency-aware scheduling |
| `--robot-alerts` | Stale issues, blocking cascades, priority mismatches |
| `--robot-suggest` | Hygiene: duplicates, missing deps, label suggestions, cycle breaks |
| `--robot-graph [--graph-format=json\|dot\|mermaid]` | Dependency graph export |
| `--export-graph <file.html>` | Self-contained interactive HTML visualization |

### Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work (no blockers)
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank scores
bv --robot-triage --robot-triage-by-track    # Group by parallel work streams
bv --robot-triage --robot-triage-by-label    # Group by domain
```

### Understanding Robot Output

All robot JSON includes:
- `data_hash` — Fingerprint of source beads.jsonl (verify consistency across calls)
- `status` — Per-metric state: `computed|approx|timeout|skipped` + elapsed ms
- `as_of` / `as_of_commit` — Present when using `--as-of`; contains ref and resolved SHA

**Two-phase analysis:**
- **Phase 1 (instant):** degree, topo sort, density — always available immediately
- **Phase 2 (async, 500ms timeout):** PageRank, betweenness, HITS, eigenvector, cycles — check `status` flags

**For large graphs (>500 nodes):** Some metrics may be approximated or skipped. Always check `status`.

### jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.status'                         # Check metric readiness
bv --robot-insights | jq '.Cycles'                         # Circular deps (must fix!)
bv --robot-label-health | jq '.results.labels[] | select(.health_level == "critical")'
```

**Performance:** Phase 1 instant, Phase 2 async (500ms timeout). Prefer `--robot-plan` over `--robot-insights` when speed matters. Results cached by data hash.

Use bv instead of parsing beads.jsonl—it computes PageRank, critical paths, cycles, and parallel tracks deterministically.

## Resources

- [Beads GitHub](https://github.com/steveyegge/beads)
- [Beads Viewer](https://github.com/Dicklesworthstone/beads_viewer)
- [MCP Agent Mail](https://github.com/Dicklesworthstone/mcp_agent_mail)
- [Vibe Coding Book](https://www.amazon.com/dp/1966280025)
