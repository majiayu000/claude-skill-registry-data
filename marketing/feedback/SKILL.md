---
name: feedback
description: Collect content feedback and identify patterns for rule updates
---

# Feedback Skill

## Overview

Simple feedback system for content quality. Collect ratings, identify patterns, and get recommendations for rule updates.

**Philosophy:** Lightweight pattern identification → Manual rule improvements

---

## Operations

**rate** - Collect feedback on content quality
- Entry: `feedback-skill rate <path>`
- Collects: Rating (1-5), issue category, optional comment
- Output: Stores in `.kurt/kurt.sqlite`
- Subskill: `subskills/rate.md`

**dashboard** - View feedback trends and summary
- Entry: `feedback-skill dashboard [--days <n>]`
- Shows: Overall stats, issue breakdown, rating trends, recent feedback
- Output: Console summary
- Subskill: `subskills/dashboard.md`

**patterns** - Identify recurring issues and recommend updates
- Entry: `feedback-skill patterns [--days <n>] [--min-frequency <n>]`
- Shows: Issues that occur ≥3 times with recommendations
- Output: Recommended `writing-rules-skill` commands
- Subskill: `subskills/patterns.md`

---

## Routing Logic

Parse arguments → Route to subskill:

```bash
OPERATION=$1
shift

case "$OPERATION" in
    "rate")
        .claude/skills/feedback-skill/subskills/rate.md "$@"
        ;;

    "dashboard")
        .claude/skills/feedback-skill/subskills/dashboard.md "$@"
        ;;

    "patterns")
        .claude/skills/feedback-skill/subskills/patterns.md "$@"
        ;;

    *)
        echo "Unknown operation: $OPERATION"
        echo ""
        echo "Available operations:"
        echo "  rate       - Rate content quality"
        echo "  dashboard  - View feedback trends"
        echo "  patterns   - Identify recurring issues"
        exit 1
        ;;
esac
```

---

## Data Storage

### SQLite (`.kurt/kurt.sqlite`)

**feedback_events** (simplified schema)
```sql
CREATE TABLE feedback_events (
    id TEXT PRIMARY KEY,           -- UUID
    created_at TEXT NOT NULL,      -- ISO 8601 timestamp
    rating INTEGER NOT NULL,       -- 1-5
    comment TEXT,                  -- Optional text feedback
    issue_category TEXT,           -- tone|structure|info|comprehension|length|examples|other
    asset_path TEXT,               -- Path to rated content
    project_id TEXT                -- Optional project context
);
```

**Removed tables** (from previous complex version):
- `improvements` - No automated execution tracking
- `workflow_retrospectives` - Workflows removed
- `workflow_phase_ratings` - Workflows removed
- `feedback_loops` - Too complex for simple system

---

## Simple Feedback Flow

```
1. User creates content

2. User rates content (optional):
   feedback-skill rate <path>
   → Rating: 1-5
   → Issue category (if ≤3)
   → Optional comment

3. View trends over time:
   feedback-skill dashboard
   → Overall stats
   → Issue breakdown
   → Rating trends

4. When patterns emerge (≥3 occurrences):
   feedback-skill patterns
   → Shows recurring issues
   → Recommends rule update commands

5. User manually updates rules:
   writing-rules-skill style --type X --update
   writing-rules-skill structure --type X --update
   writing-rules-skill persona --audience-type X --update
```

**No automation. User decides when to act.**

---

## Issue Categories

Simple, content-focused categories:

| Category | Description | Related Rule |
|----------|-------------|--------------|
| `tone` | Wrong tone or style | style |
| `structure` | Poor organization | structure |
| `info` | Missing information | persona, sources |
| `comprehension` | Hard to understand | style, structure |
| `length` | Too long or short | persona |
| `examples` | Code example issues | structure |
| `other` | Manual review | - |

---

## Integration Points

### From content-writing-skill

**Optional integration** (not required):

```bash
# After draft creation
echo ""
echo "Rate this draft? (y/N): "
read -r RESPONSE

if [ "$RESPONSE" = "y" ] || [ "$RESPONSE" = "Y" ]; then
    feedback-skill rate "$DRAFT_PATH"
fi
```

### To writing-rules-skill

**patterns.md recommends commands:**

```
Tone Issues (5× in last 30 days)
→ writing-rules-skill style --type technical-docs --update

Structure Issues (3× in last 30 days)
→ writing-rules-skill structure --type tutorial --update
```

User copies and runs command to update rules.

---

## Configuration

Minimal configuration in `.kurt/feedback/feedback-config.yaml`:

```yaml
feedback:
  enabled: true
  min_pattern_frequency: 3  # Minimum occurrences to show pattern
  default_time_window_days: 30
```

**Removed from config:**
- Issue mappings with automated commands (too complex)
- Improvement execution settings (no automation)
- Workflow-related configuration (workflows removed)

---

## Design Principles

1. **Simple and lightweight:** Just collect → analyze → recommend
2. **Pattern-based:** Only show issues that occur multiple times
3. **Manual execution:** User runs update commands (no automation)
4. **Non-blocking:** Feedback collection never interrupts workflow
5. **Content-focused:** Only content quality (no projects/workflows)
6. **Privacy-conscious:** Minimal data storage

---

## Example Usage

### Rate a draft:
```bash
feedback-skill rate projects/my-tutorial/draft.md
```

### View feedback trends:
```bash
feedback-skill dashboard
feedback-skill dashboard --days 7
```

### Check for patterns:
```bash
feedback-skill patterns
feedback-skill patterns --min-frequency 5
```

### After pattern identified, update rules:
```bash
# Copy recommended command from patterns output
writing-rules-skill style --type technical-docs --update
```

---

## Getting Started

1. **Create content** (drafts, outlines)

2. **Rate content occasionally:**
   ```bash
   feedback-skill rate path/to/draft.md
   ```

3. **After several ratings, check dashboard:**
   ```bash
   feedback-skill dashboard
   ```

4. **When patterns emerge, check recommendations:**
   ```bash
   feedback-skill patterns
   ```

5. **Update rules based on patterns:**
   ```bash
   writing-rules-skill style --type X --update
   ```

---

## What Changed from Previous Version

**Removed:**
- Project plan feedback (Loop 2)
- Workflow retrospectives (Loop 3)
- Automated improvement execution
- Validation and effectiveness tracking
- Complex feedback loop completion metrics
- Multiple feedback types (now just content quality)

**Kept (simplified):**
- Content rating with issue identification
- Pattern analysis across feedback
- Trend visualization in dashboard
- Manual rule update recommendations

**Result:** ~2,000 fewer lines of code, simpler user experience

---

*This skill provides lightweight feedback collection and pattern analysis to guide manual rule improvements.*
