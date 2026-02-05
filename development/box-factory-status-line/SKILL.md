---
name: box-factory-status-line
description: Practical guidance for Claude Code status lines - what to display for real workflow benefits, not just configuration syntax. Use when setting up status lines or wondering what information would actually help.
---

# Status Line Skill

This skill provides practical guidance on what makes status lines *useful*. The official docs explain how to configure them; this skill explains what to display and why.

## Fundamentals

Three core principles underpin effective status line design:

### 1. Workflow-Driven Information

Status lines exist to prevent problems, not display all available data. Choose what to show based on pain points you've experienced: cost surprise, model confusion, wrong branch commits.

### 2. Glanceable, Not Comprehensive

You'll stop reading a status line that's too long. Pick 3-4 most valuable pieces. Use multi-line community tools only if you genuinely need more.

### 3. Performance Matters

Scripts run every 300ms. Keep them fast (\<100ms ideally). Use JSON data when possible, cache slow operations, wrap git commands in existence checks.

## Workflow Selection

| If you need to...                                     | Go to...                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------------- |
| Understand what status lines are and when to use them | [Core Understanding](#core-understanding)                           |
| Solve specific workflow problems (cost, git, model)   | [Practical Workflows](#practical-workflows-why-status-lines-matter) |
| Choose between custom script and community tools      | [Decision Framework](#decision-framework)                           |
| Get started quickly with working status line          | [Quick Start](#quick-start)                                         |
| Optimize slow scripts or fix errors                   | [Performance Considerations](#performance-considerations)           |
| See complete examples for different use cases         | [Composition Patterns](#composition-patterns)                       |
| Look up available JSON fields                         | [What's Available](#whats-available-in-json-input)                  |
| Avoid common mistakes                                 | [Common Pitfalls](#common-pitfalls)                                 |

## Official Documentation

Fetch official documentation with WebFetch:

- **<https://code.claude.com/docs/en/statusline>** - Configuration and JSON schema

## Core Understanding

### What Status Lines Actually Are

Status lines are a **real-time development dashboard** at the bottom of Claude Code. Think vim statusline or tmux status bar - persistent, glanceable, always-current information.

**How they work:**

- Script runs on every message update (throttled to 300ms)
- Receives structured JSON via stdin with session data
- First line of stdout becomes the display
- ANSI colors and emojis supported

**What you DON'T need a status line skill to know:**

- JSON parsing syntax
- Configuration file locations
- How to write bash/python scripts

Claude knows all that. This skill focuses on *what to display* based on real developer workflows.

## Practical Workflows (Why Status Lines Matter)

### 1. Cost Awareness

**The problem:** You're deep in a session and suddenly realize you've burned through $15 in API costs.

**The solution:** Display session cost and daily total prominently.

```bash
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
printf "💰 \$%.4f" "$cost"
```

**Workflow benefit:** Catch runaway sessions early. Know when to switch models.

### 2. Context Window Management

**The problem:** Claude starts forgetting earlier context because you've filled the window.

**The solution:** Display context usage percentage.

**Workflow benefit:** Know when to compact (`/compact`) or start fresh before context degrades.

**Note:** The official JSON schema includes `cost` data but context percentage requires external tools like ccstatusline.

### 3. Model Visibility

**The problem:** You switched to haiku for a quick task and forgot, now wondering why responses feel different.

**The solution:** Always show current model.

```bash
model=$(echo "$input" | jq -r '.model.display_name')
echo "[$model]"
```

**Workflow benefit:** Model awareness without checking settings. Crucial when switching between opus/sonnet/haiku for different task types.

### 4. Git Branch Awareness

**The problem:** You're making changes on the wrong branch.

**The solution:** Show current git branch in status line.

```bash
if git rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")
    echo "🌿 $branch"
fi
```

**Workflow benefit:** Never commit to main accidentally. Stay oriented in multi-branch workflows.

### 5. Session Duration / Block Management

**The problem:** Claude Code 5-hour blocks expire and you lose context.

**The solution:** Display session duration or time remaining in block.

```bash
duration_sec=$(echo "$input" | jq -r '.cost.total_duration_ms / 1000 | floor')
printf "[%dm]" "$((duration_sec / 60))"
```

**Workflow benefit:** Plan commits and breaks around block boundaries. Don't lose work mid-session.

### 6. Project Orientation

**The problem:** Working across multiple projects and forgetting which terminal is which.

**The solution:** Show project directory name.

```bash
dir=$(echo "$input" | jq -r '.workspace.project_dir' | xargs basename)
echo "📁 $dir"
```

**Workflow benefit:** Instant orientation. Critical in multi-terminal setups.

## Composition Patterns

### Minimal (Model + Directory)

```bash
#!/bin/bash
input=$(cat)
model=$(echo "$input" | jq -r '.model.display_name')
dir=$(echo "$input" | jq -r '.workspace.current_dir' | xargs basename)
echo "[$model] 📁 $dir"
```

**Best for:** Simple awareness, low noise.

### Developer Standard (Model + Git + Cost)

```bash
#!/bin/bash
input=$(cat)
model=$(echo "$input" | jq -r '.model.display_name')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
dir=$(echo "$input" | jq -r '.workspace.project_dir')

branch=""
if git -C "$dir" rev-parse --git-dir > /dev/null 2>&1; then
    branch=" 🌿 $(git -C "$dir" symbolic-ref --short HEAD 2>/dev/null)"
fi

printf "[%s]%s 💰 \$%.4f\n" "$model" "$branch" "$cost"
```

**Best for:** Most development workflows. Balance of information and brevity.

### Terminal-Only Workflow

When working without an IDE (terminal-only), you need more context:

```bash
#!/bin/bash
input=$(cat)
model=$(echo "$input" | jq -r '.model.display_name')
dir=$(echo "$input" | jq -r '.workspace.project_dir')

# Full git status for terminal-only work
if git -C "$dir" rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git -C "$dir" symbolic-ref --short HEAD 2>/dev/null)
    staged=$(git -C "$dir" diff --cached --numstat | wc -l | tr -d ' ')
    unstaged=$(git -C "$dir" diff --numstat | wc -l | tr -d ' ')
    echo "[$model] $branch ✓$staged ✗$unstaged"
else
    echo "[$model] ${dir##*/}"
fi
```

**Best for:** Pure terminal development without IDE git integration.

## Community Tools (When Custom Scripts Aren't Enough)

### ccstatusline

Multi-line powerline-style status with widgets. Interactive TUI configuration.

**When to use:** You want rich visuals without writing scripts, or need widgets for context percentage/tokens.

**Install:** `npx ccstatusline@latest`

### claude-code-statusline

18 atomic components, 1-9 configurable lines, TOML configuration.

**When to use:** Complex layouts, cost projections, MCP server monitoring, Islamic prayer times integration.

**Unique features:** Cache efficiency metrics, burn rate alerts, daily/weekly/monthly cost tracking.

### ccusage statusline

Focused on cost tracking with visual burn rate indicators.

**When to use:** Cost management is your primary concern.

## Decision Framework

**Ask yourself:**

1. **What problem am I solving?**

   - If none → Don't add a status line (default is fine)
   - If cost surprise → Add cost display
   - If model confusion → Add model display
   - If git mistakes → Add branch display

2. **How much information density?**

   - Minimal → Model + directory only
   - Standard → Model + git + cost
   - Maximum → Use community tool for multi-line

3. **How performance-sensitive?**

   - Very → Avoid git commands, use only JSON data
   - Normal → Git commands are fine (cached by git)
   - Not concerned → External API calls acceptable

4. **Custom script vs community tool?**

   - Need specific format → Custom script
   - Want rich features fast → Community tool
   - Want to learn → Start custom, migrate later

## Performance Considerations

**Scripts run frequently (every 300ms throttle).** Keep them fast.

**Safe (use JSON data only):**

```bash
model=$(echo "$input" | jq -r '.model.display_name')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
```

**Usually fine (git is fast locally):**

```bash
branch=$(git symbolic-ref --short HEAD 2>/dev/null)
```

**Potentially slow (cache if needed):**

```bash
# External API calls, npm commands, slow git operations
```

**Caching pattern for slow operations:**

```bash
CACHE_FILE="/tmp/statusline_cache"
CACHE_TTL=5

if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -f%m "$CACHE_FILE"))) -lt $CACHE_TTL ]; then
    cat "$CACHE_FILE"
else
    expensive_result=$(expensive_command)
    echo "$expensive_result" > "$CACHE_FILE"
    echo "$expensive_result"
fi
```

## Common Pitfalls

### Pitfall: Too Much Information

**Problem:** Status line so long it wraps or gets truncated.

**Reality:** You'll stop reading it. Less is more.

**Fix:** Pick 3-4 most valuable pieces. Use community tools for multi-line if you need more.

### Pitfall: Slow Scripts

**Problem:** Status line lags behind, script takes 500ms+.

**Impact:** Typing feels sluggish.

**Fix:** Profile with `time echo '{}' | ./statusline.sh`. Keep under 100ms ideally.

### Pitfall: Git Commands in Non-Git Directories

**Problem:** Script fails or shows errors in non-git directories.

**Fix:** Always check:

```bash
if git rev-parse --git-dir > /dev/null 2>&1; then
    # git commands here
fi
```

### Pitfall: Missing jq

**Problem:** Script assumes jq is installed.

**Fix:** Use Python or Node instead, or check for jq:

```bash
if ! command -v jq &> /dev/null; then
    echo "[status line: jq required]"
    exit 0
fi
```

### Pitfall: Forgetting to Make Script Executable

**Problem:** Status line doesn't work.

**Fix:** `chmod +x ~/.claude/statusline.sh`

## Quick Start

**Fastest path to useful status line:**

```bash
# Create script
cat > ~/.claude/statusline.sh << 'EOF'
#!/bin/bash
input=$(cat)
model=$(echo "$input" | jq -r '.model.display_name')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
dir=$(echo "$input" | jq -r '.workspace.current_dir' | xargs basename)
printf "[%s] 📁 %s 💰 \$%.4f\n" "$model" "$dir" "$cost"
EOF

# Make executable
chmod +x ~/.claude/statusline.sh

# Configure (add to ~/.claude/settings.json)
# {
#   "statusLine": {
#     "type": "command",
#     "command": "~/.claude/statusline.sh"
#   }
# }
```

Or use `/statusline` command to have Claude Code set it up for you.

## What's Available in JSON Input

Your script receives this via stdin (partial list - see official docs for complete schema):

```json
{
  "model": {
    "id": "model-identifier",
    "display_name": "Claude 3.5 Sonnet"
  },
  "workspace": {
    "current_dir": "/path/to/current",
    "project_dir": "/path/to/project"
  },
  "cost": {
    "total_cost_usd": 0.012,
    "total_duration_ms": 45000
  },
  "session_id": "unique-id",
  "version": "1.0.80"
}
```

**Key fields for workflows:**

- `model.display_name` - Current model name
- `cost.total_cost_usd` - Session cost
- `cost.total_duration_ms` - Session duration
- `workspace.project_dir` - Project root
- `workspace.current_dir` - Current directory

## Quality Checklist

Before finalizing your status line:

**Configuration:**

- [ ] Script is executable (ran `chmod +x` on script file)
- [ ] Correct path configured in settings.json
- [ ] Fetched official docs for current JSON schema

**Performance:**

- [ ] Script runs under 100ms (tested with `time echo '{}' | ./statusline.sh`)
- [ ] Git commands wrapped in existence checks (`git rev-parse --git-dir`)
- [ ] Slow operations cached with TTL pattern if needed
- [ ] No external API calls unless absolutely necessary

**Content:**

- [ ] Displays 3-4 most valuable pieces (not everything available)
- [ ] Handles non-git directories gracefully (no errors)
- [ ] Checks for required tools (jq, etc) with fallback
- [ ] Chosen fields solve actual workflow problems (cost, model, branch)

**Testing:**

- [ ] Tested in git repository (shows branch correctly)
- [ ] Tested in non-git directory (no errors or warnings)
- [ ] Tested across multiple sessions (updates correctly)
- [ ] Status line remains readable (not truncated or wrapped)

## Documentation References

- <https://code.claude.com/docs/en/statusline> - Official configuration
- <https://github.com/sirmalloc/ccstatusline> - Powerline-style tool
- <https://github.com/rz1989s/claude-code-statusline> - Atomic component tool
- <https://ccusage.com/guide/statusline> - Cost-focused status line
