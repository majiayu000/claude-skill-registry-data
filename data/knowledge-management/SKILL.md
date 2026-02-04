---
name: knowledge-management
description: 4-layer knowledge capture system for development sessions. Use when user says /mem (quick capture), /distill (extract patterns), /td (post-task retrospective with Before/After context), /improve (work on pending items), or /commit (atomic commits via TDG). Manages docs/learnings/, docs/knowledge-base/, and docs/retrospective/ directories.
---

# Knowledge Management System

4-layer system for capturing and organizing development knowledge.

## Commands

| Command | Layer | Output | Trigger |
|---------|-------|--------|---------|
| `/mem [topic]` | 1 | `docs/learnings/YYYY-MM/DD/HH.MM_slug.md` | Quick insight capture |
| `/distill [topic]` | 2 | `docs/knowledge-base/[topic].md` | 3+ learnings on same topic |
| `/td` | 3 | `docs/retrospective/YYYY-MM/retrospective_*.md` | Task completed |
| `/improve` | 4 | Implementation | Work on pending items |
| `/commit` | - | Git commits | Atomic commits via TDG |
| `/pr-review` | - | Learning doc + PR updates | Handle PR review feedback |
| `/pr-poll` | - | Notification daemon | Auto PR review notifications |
| `/example [lang] [name]` | - | `docs/examples/[lang]/[name].[ext]` | Save code snippets |
| `/summary weekly\|monthly` | - | `docs/summaries/YYYY-MM-weekN.md` | Session summaries |
| `/search [query]` | - | Search results | Search knowledge index |
| `/share [file]` | - | `docs/shared-knowledge/[file]` | Cross-project knowledge |
| `/flow [name]` | - | `docs/flows/[name].md` | Process flow diagrams |
| `/pattern [name]` | - | `docs/patterns/[name].md` | Design pattern docs |
| `/cleanup` | - | Archive + cleanup | Retention policy management |

## Flow

```
ทำงาน → /mem "insight" → /distill topic → /td → /improve
         (Layer 1)        (Layer 2)      (Layer 3) (Layer 4)
```

## Directory Structure

```
docs/
├── learnings/           # /mem output
│   └── YYYY-MM/DD/
├── knowledge-base/      # /distill output
├── examples/            # /example output
│   └── [language]/
├── summaries/           # /summary output
├── shared-knowledge/    # /share output (cross-project)
├── flows/               # /flow output (Mermaid diagrams)
├── patterns/            # /pattern output (design patterns)
└── retrospective/       # /td output
    └── YYYY-MM/
```

## Setup

Run init script to create directory structure:
```bash
./scripts/init.sh $PROJECT_ROOT
```

Or manually:
```bash
mkdir -p docs/{learnings,knowledge-base,retrospective}
```

---

## Command: /mem

**Quick knowledge capture** - ใช้ระหว่างทำงานเมื่อพบ insight

```bash
TZ='Asia/Bangkok' date '+%Y-%m/%d/%H.%M'  # Path format
```

**Output**: `docs/learnings/YYYY-MM/DD/HH.MM_[slug].md`

**Template**: See `references/mem-template.md`

**Key sections**: Key Insight, What We Learned, Gotchas, Tags

---

## Command: /distill

**Extract patterns** - รวม learnings เป็น reusable patterns

**When**: มี 3+ learnings เรื่องเดียวกัน หรือ weekly review

**Output**: `docs/knowledge-base/[topic-name].md`

**Template**: See `references/distill-template.md`

**Key sections**: Key Insight, The Problem, The Solution (with code), Anti-Patterns, When to Apply

**After**: Mark source learnings as "Distilled"

---

## Command: /td

**Post-task retrospective** with Before/After context

**Output**: `docs/retrospective/YYYY-MM/retrospective_YYYY-MM-DD_hhmmss.md`

**Template**: See `references/td-template.md`

### Type Classification (frontmatter)

| Type | Use When |
|------|----------|
| `feature` | New functionality |
| `bugfix` | Bug fix |
| `refactor` | Code restructure |
| `decision` | Architecture decision |
| `discovery` | Research/learning |
| `config` | Configuration changes |
| `docs` | Documentation only |

### Required: Before/After Context

```markdown
## Context: Before
- **Problem**: ปัญหาที่เจอ
- **Existing Behavior**: พฤติกรรมเดิม
- **Metrics**: ตัวเลขก่อนแก้

## Context: After
- **Solution**: วิธีแก้
- **New Behavior**: พฤติกรรมใหม่
- **Metrics**: ตัวเลขหลังแก้
```

### Decisions Table

```markdown
| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
```

---

## Command: /commit

**Atomic commits** via TDG plugin

**Delegates to**: `/tdg:atomic-commit` from https://github.com/chanwit/tdg

**What it does**:
- Analyzes staged/unstaged changes
- Detects mixed concerns (multiple unrelated changes)
- Helps create clean, focused atomic commits
- Each commit is a complete unit of work

**Usage**: Simply run `/commit` and it will invoke TDG's atomic-commit skill.

---

## Command: /improve

**Work on pending items** from all knowledge sources

**Scan order** (priority):
1. `docs/knowledge-base/` - Patterns to apply
2. `docs/retrospective/` - Future Improvements (`- [ ]`)
3. `docs/learnings/` - Gotchas to fix (skip if "Distilled")

**Workflow**:
1. Extract unchecked items
2. Present prioritized list
3. User selects items
4. Implement & commit
5. Update source file (`- [ ]` → `- [x]`)

---

## Search Commands

```bash
# Find by type
grep -l "type: bugfix" docs/retrospective/**/*.md

# Search content
grep -r "mongodb" docs/

# Recent learnings
find docs/learnings -name "*.md" -mtime -7
```

---

## Command: /pr-poll

**Automatic PR review notifications** - Polling daemon ตรวจสอบ PR reviews

**What it does**:
- Poll GitHub for user's open PRs
- Detect new reviews, comments, and review decisions
- Send macOS notifications with review details
- Suggest running `/pr-review` to respond

**Usage**:
```bash
/pr-poll              # Show daemon status
/pr-poll start        # Start polling daemon
/pr-poll stop         # Stop daemon
/pr-poll check        # Check once without daemon
```

**Notification sounds**:
- APPROVED → Glass
- CHANGES_REQUESTED → Basso
- COMMENTED → Ping

**Files**:
- `~/.pr-review-poll.pid` - Daemon PID
- `~/.pr-review-poll.log` - Daemon logs
- `~/.pr-review-state.json` - PR state tracking

---

## Command: /cleanup

**Retention policy management** - จัดการไฟล์เก่าด้วย retention policy

**What it does**:
- Delete old auto-captured files (configurable retention period)
- Archive old files before deletion (optional)
- Dry-run mode to preview changes
- Clean draft learnings that haven't been distilled

**Usage**:
```bash
/cleanup                    # Preview (30 days default)
/cleanup 7                  # Preview with 7 days retention
/cleanup 14 --archive       # Archive & delete files older than 14 days
/cleanup --all              # Clean all targets
```

**Protected directories** (never auto-deleted):
- `docs/retrospective/` - Permanent records
- `docs/knowledge-base/` - Distilled knowledge

---

## Auto-Capture

บันทึก session อัตโนมัติเมื่อจบงาน

### Options

| Option | Command | Trigger |
|--------|---------|---------|
| Hooks | - | Auto on session stop |
| Wrapper | `claude` (alias) | Interactive prompt |
| AI-Powered | `./scripts/ai-capture.sh` | Manual with AI analysis |

### Setup (Hooks - Recommended)

```bash
# Add to ~/.claude/settings.json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/knowledge-management/scripts/auto-capture.sh . 2>/dev/null || true"
      }]
    }]
  }
}
```

### Output

`docs/auto-captured/YYYY-MM/DD/HH.MM_session-*.md`

See `AUTO-CAPTURE.md` for full documentation.

---

## References

- `references/mem-template.md` - Full /mem template
- `references/distill-template.md` - Full /distill template  
- `references/td-template.md` - Full /td template
- `references/improve-workflow.md` - /improve detailed workflow
