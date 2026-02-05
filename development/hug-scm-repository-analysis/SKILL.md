---
name: Hug SCM Repository Analysis
description: Expert-level Git repository investigation using Hug SCM tools for understanding code evolution, tracking down bugs, analyzing changes, and managing development workflows
version: 1.0.0
---

# Hug SCM Repository Analysis Skill

This skill equips AI assistants with expert knowledge for investigating Git repositories using Hug SCM's humane interface. Hug transforms complex Git operations into intuitive, safe commands organized by semantic prefixes.

## Core Philosophy & Value Proposition

Hug provides **four layers of value** over raw Git:

### 1. Humanization (Better UX for Git)
- **Brevity Hierarchy**: Shorter = safer (`hug a` stages tracked only; `hug aa` stages everything)
- **Memorable Commands**: `hug back 1` vs `git reset --soft HEAD~1`
- **Progressive Destructiveness**: `discard < wipe < purge < zap < rewind`
- **Semantic Prefixes**: Commands grouped by purpose (`h*` = HEAD, `w*` = working dir, etc.)
- **Built-in Safety**: Auto-backups, confirmations, dry-run on destructive operations
- **Clear Feedback**: Informative messages with ✅ success, ⚠️ warnings, colored output

### 2. Workflow Automation
- **Combined Operations**: `--with-files` = log + file listing in one command
- **Temporal Queries**: `-t "3 days ago"` instead of date math
- **Smart Defaults**: Sensible scoping, interactive file selection
- **Interactive Modes**: Gum-based selection with `--` or `-i`

### 3. Computational Analysis ⭐ (Impossible with Pure Git)
- **Co-change Detection**: Statistical correlation analysis of files that change together
- **Ownership Calculation**: Recency-weighted expertise detection (who knows this code)
- **Dependency Graphs**: Graph traversal to find related commits via file overlap
- **Activity Patterns**: Temporal histograms showing when/how team works
- **Churn Analysis**: Line-level change frequency to identify code hotspots
- **Statistical Metrics**: Aggregated insights across files/authors/branches

*These features require Python-based data processing, graph algorithms, and statistical analysis—beyond what Git's plumbing commands can provide.*

### 4. Machine-Readable Data Export 🤖
- **JSON Output**: `--json` flag on analyze, stats, and churn commands
- **Automation Ready**: Build dashboards, integrate with CI/CD, create custom reports
- **Structured Data**: All computational analysis exports to JSON for external tools

## When to Use This Skill

Use this skill when the user asks to:
- Investigate repository history or understand what changed
- Find when bugs were introduced or features were added
- Analyze file evolution or track authorship
- Prepare commits for review or clean up history
- Recover from mistakes or undo operations
- Understand project activity patterns

## Command Prefixes Quick Reference

| Prefix | Category | Use For |
|--------|----------|---------|
| `h*` | HEAD Operations | Undoing commits, squashing, reviewing recent changes |
| `w*` | Working Directory | Discarding changes, cleaning up, managing WIP |
| `s*` | Status & Staging | Checking state, staging changes, viewing diffs |
| `b*` | Branching | Creating, switching, listing, deleting branches |
| `c*` | Commits | Committing, amending, cherry-picking, moving commits |
| `l*` | Logging | Viewing history, searching commits, analyzing changes |
| `f*` | File Inspection | Blame, contributors, file history, churn analysis |
| `t*` | Tagging | Creating, managing, querying tags |
| `analyze` | Advanced Analysis | Co-changes, activity patterns, dependencies, expertise |
| `stats` | Statistics | File/author/branch metrics and insights |

## Essential Investigation Workflows

### 1. Understanding Repository State

**Start every investigation with a status check:**

```bash
# Quick overview
hug s

# Detailed status with untracked files
hug sla

# See what's staged vs unstaged
hug ss  # staged only
hug su  # unstaged only
hug sw  # working dir summary
```

### 2. Investigating Recent Changes

**When you need to know "what happened recently":**

```bash
# See files changed in last N commits
hug h files 5

# See files changed in last week (temporal!)
hug h files -t "1 week ago"

# See what hasn't been pushed yet
hug lol  # log outgoing long
```

**Understanding what changed:**

```bash
# Show last commit with stats
hug sh

# Show last commit with full diff
hug shp

# Show files changed in specific commit
hug shc a1b2c3d
```

### 3. Finding When Things Changed

**Three search tools for different needs:**

#### Message Search (with regex support!)

```bash
# Simple message search
hug lf "keyword"
hug lf "fix bug" --with-files        # Show files changed in each match

# HIDDEN FEATURE: Regex patterns work! (uses git --grep internally)
hug lf "fix\|bug\|resolve" -i --all  # OR patterns (case-insensitive)
hug lf "feat.*auth" --all            # Regex matching
hug lf "^Merge" --all                # Pattern matching
```

**Pro tip:** `lf` supports extended regex via `git --grep`, though not advertised!

#### Code Search - Literal String (Fast)

```bash
# Exact string matching in code diffs (Git's -S pickaxe)
hug lc "getUserById"                 # Find when this function changed
hug lc "import React" --with-files   # Show files with React imports
```

#### Code Search - Regex Patterns (Powerful)

```bash
# Regex matching in code diffs (Git's -G flag)
hug lcr "function.*User"             # Function definitions
hug lcr "class \w+" -i               # Case-insensitive class declarations
hug lcr "TODO|FIXME" --all           # OR patterns in code
hug lcr "^import.*from" -p           # Import statements with patches
```

**Decision tree:**
- Searching commit messages? → `lf` (supports regex via git --grep!)
- Exact code string? → `lc` (faster, literal matching)
- Code pattern/regex? → `lcr` (explicit regex for complex patterns)

**Examples:**

```bash
# Find commits mentioning multiple related terms
hug lf "refactor\|restructure\|reorganize" -i --all

# Find when specific function was modified
hug lc "getUserById" --with-files

# Find any import statement changes
hug lcr "^import.*from" --all

# Find file history
hug llf <file>
```

### 4. Deep File Investigation

**When debugging or understanding file evolution:**

```bash
# Find when file was created (hidden gem!)
hug fborn <file>

# See who wrote each line
hug fblame <file>

# Analyze file churn (how frequently it changes)
hug fblame --churn <file>
hug fblame --churn --since="3 months ago" <file>

# Short blame (author + line only)
hug fb <file>

# List all contributors to a file
hug fcon <file>

# Count commits per author for a file
hug fa <file>

# Full file history
hug llf <file>
```

### 5. Temporal Analysis

**Powerful feature: Most commands support time-based queries:**

```bash
# What changed in last 3 days?
hug h files -t "3 days ago"

# Commits from last week
hug l --since="1 week ago"

# Date range
hug ld "2024-01-01" "2024-01-31"
```

## Safety Features to Leverage

### Auto-Backups

**All destructive HEAD operations create automatic backups:**

```bash
# These commands auto-create hug-backup-* branches
hug h back
hug h rollback
hug h rewind
hug h squash

# List backup branches
hug bl | grep backup

# Restore from backup if needed
hug b <backup-branch-name>
```

### Dry-Run Everything

**ALWAYS preview destructive operations first:**

```bash
# Preview before executing
hug w zap-all --dry-run
hug h rollback --dry-run
hug w purge --dry-run

# Then execute with -f to skip confirmation
hug w zap-all -f  # after reviewing dry-run output
```

### Interactive Selection

**Most commands support interactive file/branch/commit selection:**

```bash
# Use -- for interactive selection with Gum
hug lc "import" --          # select file to search in
hug w discard --            # select files to discard
hug bdel --                 # select branch to delete

# --browse-root for full repo scope (default: current dir)
hug lc "import" --browse-root
```

## Common Investigation Patterns

### Pattern 1: Bug Investigation

**User reports**: "Feature X broke recently"

**Investigation flow:**

```bash
# 1. Find file/files involved
hug lf "feature X"           # search commit messages
hug lc "featureXFunction"    # search code changes

# 2. Check when file last changed
hug fborn <file>             # when was it created?
hug h steps <file>           # how many commits since change?

# 3. View file history
hug llf <file>               # see all commits

# 4. Examine suspect commits
hug shp <commit-hash>        # full diff
hug shc <commit-hash>        # files changed

# 5. Check related changes
hug h files <commit-hash>    # what else changed with it?
```

### Pattern 2: Understanding Unpushed Work

**User asks**: "What am I about to push?"

```bash
# See local-only commits
hug lol

# Or shorter version
hug lo

# See files in local commits
hug h files -u               # -u for upstream comparison

# Review before pushing
hug l @{u}..HEAD             # commits ahead of upstream
```

### Pattern 3: Finding Hot Spots

**User asks**: "Which files change most often?"

```bash
# Recent activity
hug h files 50               # files in last 50 commits

# By time period
hug h files -t "1 month ago"

# For specific directory
cd src/
hug l --since="1 month ago" -- .
```

### Pattern 4: Authorship Analysis

**User asks**: "Who works on this code?"

```bash
# Contributors to specific file
hug fcon <file>

# Commit counts per author
hug fa <file>

# Commits by specific author
hug lau "Author Name"

# Date range for author
hug lau "Author Name" --since="1 month ago"
```

## Working with Branches

### Branch Investigation

```bash
# Current branch status
hug b

# List all branches with tracking info
hug bla

# Which branches contain a commit?
hug bwc <commit>

# Which branches point at HEAD?
hug bwp

# Which branches are merged?
hug bwm

# Which branches are NOT merged?
hug bwnm
```

### Branch Queries (Advanced)

```bash
# Tags/branches containing commit
hug bwc <commit>             # branches which contain
hug twc <commit>             # tags which contain

# Tags/branches pointing at commit
hug bwp <commit>             # branches which point
hug twp <commit>             # tags which point
```

## Advanced Investigation Techniques

### 1. Combining Commands for Insights

```bash
# Find all commits in feature branch
hug l main..feature-branch

# See what would merge
hug m feature-branch --dry-run

# Compare branches
hug l branch1..branch2
```

### 2. Using Git Aliases (when needed)

Hug preserves Git aliases, so you can still use:

```bash
# These work through Hug
hug l --all                  # all branches log
hug ll --all                 # detailed all branches
hug la                       # shortcut for above
```

### 3. Temporal Precision

```bash
# Exact time specifications
hug h files -t "2024-01-15 14:30"
hug h files -t "yesterday"
hug h files -t "3 hours ago"

# Relative specifications work
hug ld "last monday" "friday"
```

## Computational Analysis (Beyond Git's Capabilities)

These commands perform **statistical analysis and graph algorithms** impossible with raw Git alone. They require Python-based data processing and export to JSON for automation.

### 1. Co-Change Detection (Architectural Coupling)

**Problem:** Which files change together? Reveals architectural coupling.

```bash
# Analyze last 100 commits for co-changing files
hug analyze co-changes 100

# Strong coupling only (≥50% correlation)
hug analyze co-changes --threshold 0.50

# Top 10 pairs
hug analyze co-changes --top 10

# Machine-readable export
hug analyze co-changes --json
```

**Algorithm:** Builds co-occurrence matrix from commit history, calculates Jaccard-like correlation coefficients.

**Use cases:**
- Identify tightly coupled modules that should be refactored
- Find files to review together
- Detect architectural issues

### 2. Code Ownership Analysis (Expertise Detection)

**Problem:** Who owns this code? Who should review changes?

```bash
# Find experts for a file (recency-weighted)
hug analyze expert src/auth.js

# Find author's expertise areas
hug analyze expert --author "Alice"

# Custom recency decay (default: 180 days)
hug analyze expert src/auth.js --decay 90

# JSON export for dashboards
hug analyze expert src/auth.js --json
```

**Algorithm:** Recency-weighted commit analysis with exponential decay formula: `weight = commits × exp(-days_ago / decay_days)`

**Output categories:**
- Primary: >40% weighted ownership
- Secondary: >20% weighted ownership
- Historical: <20% (stale contributors)

### 3. Activity Pattern Detection (Team Health)

**Problem:** When does the team work? Are there sustainability issues?

```bash
# Hourly histogram
hug analyze activity --by-hour

# Day-of-week patterns
hug analyze activity --by-day

# Per-author breakdowns
hug analyze activity --by-author --by-hour

# Time-filtered analysis
hug analyze activity --since="3 months ago"

# Export for dashboards
hug analyze activity --json
```

**Algorithm:** Temporal aggregation with statistical summaries. Flags:
- ⚠️ Late night commits (10pm-4am)
- ⚠️ Weekend work patterns
- Peak productivity hours

**Insights:**
- Team sustainability assessment
- Timezone coverage detection
- Process problem indicators

### 4. Commit Dependency Graphs ⭐ NEW

**Problem:** Which commits are related through file overlap?

```bash
# Find commits related to specific commit
hug analyze deps abc1234

# Two-level dependency traversal
hug analyze deps abc1234 --depth 2

# Require strong coupling (3+ files overlap)
hug analyze deps abc1234 --threshold 3

# Repository-wide coupling analysis
hug analyze deps --all --threshold 5

# Export formats
hug analyze deps abc1234 --format graph   # ASCII tree (default)
hug analyze deps abc1234 --format text    # Simple list
hug analyze deps abc1234 --format json    # Machine-readable
```

**Algorithm:** File-to-commits indexing + graph traversal (BFS) based on file overlap.

**Use cases:**
- Find all commits in a logical feature
- Determine review scope ("what else changed with this?")
- Detect tightly coupled code areas
- Understand feature evolution

### 5. Statistical Metrics

**Repository-wide insights:**

```bash
# File-level statistics
hug stats file src/app.js
hug stats file src/app.js --json          # Export

# Author contributions
hug stats author "Alice"
hug stats author "Alice" --json

# Branch metrics
hug stats branch feature/auth
hug stats branch feature/auth --json
```

**Metrics include:**
- Commit counts, file counts
- Line changes (additions/deletions)
- Active periods
- Contribution percentages

### 6. Churn Analysis (Code Hotspots)

**Problem:** Which code changes most frequently?

```bash
# Line-level change frequency
hug fblame --churn src/auth.js

# Time-filtered churn
hug fblame --churn --since="3 months ago" src/auth.js

# JSON export for hotspot visualization
hug fblame --churn --json src/auth.js
```

**Algorithm:** Counts modifications per line over time using `git log -L`.

**Identifies:**
- 🔥 Hot lines (changed frequently = potential issues)
- Stable code vs volatile code
- Refactoring candidates

### Why These Are Impossible with Pure Git

**Git provides data, Hug provides analysis:**

| Git Capability | Hug Analysis |
|----------------|--------------|
| `git log --name-only` | **→ Co-change correlation** (statistical) |
| `git log --follow` | **→ Ownership calculation** (recency-weighted) |
| `git diff-tree` | **→ Dependency graphs** (graph traversal) |
| `git log --format=%ai` | **→ Activity patterns** (temporal histograms) |
| `git log -L` | **→ Churn analysis** (frequency aggregation) |

**These require:**
- Python data processing
- Statistical algorithms (correlation, exponential decay)
- Graph analysis (BFS/DFS)
- Data aggregation and export

### Machine-Readable Export

**All computational features support `--json` or `--format=json`:**

```bash
# Build custom dashboards
hug analyze co-changes --json > coupling.json
hug analyze expert --author "Alice" --json > alice-expertise.json
hug analyze activity --json > team-health.json
hug analyze deps --all --format json > commit-graph.json
hug stats file src/app.js --json > file-metrics.json
```

**Enable:**
- CI/CD integration
- Custom reporting
- Dashboard visualization (Grafana, etc.)
- Data science workflows

## Important Caveats and Limitations

### When to Use Raw Git

Hug doesn't cover every Git operation. Use raw Git for:

- Submodule operations
- Worktree management
- Advanced reflog queries
- Bisect operations
- Filter-branch/filter-repo

### Understanding Hug's Safety Trade-offs

1. **Confirmations slow down scripts**: Use `-f` or `HUG_FORCE=true` for automation
2. **Interactive mode requires Gum**: Falls back gracefully, but install Gum for best experience
3. **Some operations are intentionally verbose**: This prevents accidents

### Read-Only Investigation Commands

These are always safe - no confirmations needed:

- All `l*` logging commands
- All `f*` file inspection commands
- All `s*` status commands
- Most `h files` and `h steps` commands
- Branch listing (`bl`, `bla`, `blr`)

## Integration with MCP Server

When using the Hug SCM MCP server, these tools are available:

- `hug_status` → `hug s` or `hug sla`
- `hug_log` → `hug l` with filters
- `hug_h_files` → `hug h files` (supports temporal, upstream)
- `hug_h_steps` → `hug h steps` (for precise navigation)
- `hug_show_diff` → `hug ss`, `hug su`, `hug sw`
- `hug_branch_list` → `hug bl`, `hug bla`

**The MCP server exposes read-only operations** for safe AI investigation.

## Learning More

For detailed command documentation:
- [Working Directory Commands](../docs/commands/working-dir.md)
- [HEAD Operations](../docs/commands/head.md)
- [Status & Staging](../docs/commands/status-staging.md)
- [Branching](../docs/commands/branching.md)
- [Logging](../docs/commands/logging.md)
- [File Inspection](../docs/commands/file-inspection.md)

For workflow examples:
- [Practical Workflows](../docs/practical-workflows.md)
- [Cookbook Recipes](../docs/cookbook.md)

## Quick Command Cheatsheet

```bash
# Investigation Starters
hug s                        # what's changed?
hug sla                      # full status
hug h files 10               # recent file changes
hug lol                      # what will push?

# Search Operations
hug lf "keyword"             # search messages
hug lf "keyword" --with-files # search messages, show files
hug lc "code"                # search code changes
hug lc "code" --with-files   # search code changes, show files
hug lcr "regex"              # regex code search
hug llf <file>               # file history

# Deep Inspection
hug fborn <file>             # when created
hug fblame <file>            # who wrote what
hug fblame --churn <file>    # churn analysis
hug fcon <file>              # contributors
hug h steps <file>           # commits since change

# Computational Analysis (with JSON export!)
hug analyze co-changes 100              # files that change together
hug analyze co-changes --json           # coupling data export
hug analyze expert <file>               # code ownership
hug analyze expert <file> --json        # ownership data export
hug analyze expert --author "Alice"     # expertise areas
hug analyze activity --by-hour          # team patterns
hug analyze activity --json             # activity data export
hug analyze deps <commit>               # commit dependencies
hug analyze deps --all --format json    # dependency graph export

# Statistics (with JSON export!)
hug stats file <file> --json            # file metrics
hug stats author "Alice" --json         # author data
hug stats branch feature/x --json       # branch metrics
hug fblame --churn --json <file>        # hotspot data

# Time-Based
hug h files -t "3 days ago"  # recent changes
hug ld "monday" "friday"     # date range
hug lau "Author" --since="1 month ago"

# Branch Queries
hug bwc <commit>             # which branches contain?
hug bwm                      # which merged?
hug bwnm                     # which not merged?
```

## Tips for AI Assistants

1. **Always start with status** - `hug s` or `hug sla` before any investigation
2. **Use temporal queries** - More intuitive than commit counts (`-t "3 days ago"`)
3. **Leverage file birth** - `hug fborn` is faster than manual log walking
4. **Combine commands** - Chain investigations from broad to specific
5. **Preview first** - Use `--dry-run` before suggesting destructive operations
6. **Explain the prefix** - Help users learn the mnemonic system
7. **Suggest interactive mode** - Use `--` for Gum selection when multiple options
8. **Check for backups** - Remind users about auto-backups for HEAD operations

## Next Steps

For specific workflows, see the guide files:
- [Bug Hunting Guide](./guides/bug-hunting.md) - Finding when bugs were introduced
- [Pre-Commit Review Guide](./guides/pre-commit-review.md) - Reviewing changes before commit
- [Branch Analysis Guide](./guides/branch-analysis.md) - Understanding branch differences
- [History Cleanup Guide](./guides/history-cleanup.md) - Preparing for PR/merge
