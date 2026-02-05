---
name: agentic-development
description: Workflow for long-running agentic development across multiple context windows. Use when working on multi-phase projects, complex feature implementations, or any development task spanning multiple sessions. Provides structured progress tracking, session handoff protocols, and incremental development patterns adapted from Anthropic's research on effective agent harnesses.
---

# Agentic Development

Structured workflow for maintaining progress across multiple AI coding sessions, preventing common failure modes: one-shotting (attempting too much), premature completion (declaring victory early), and broken handoffs (leaving work in unusable state).

## Core Files

### features.json

Structured feature tracking with explicit pass/fail states:

```json
{
  "meta": {
    "project": "project-name",
    "currentPhase": 1,
    "lastUpdated": "YYYY-MM-DD"
  },
  "features": [
    {
      "id": "p1-feature-name",
      "phase": 1,
      "category": "category-name",
      "description": "Feature description",
      "priority": "high|medium|low",
      "dependencies": [],
      "verification": ["Step 1", "Step 2", "Step 3"],
      "passes": false
    }
  ]
}
```

**Rules:**
- Only modify `passes` field during development
- Never remove or edit verification steps mid-session
- Use `currentPhase` in meta for phase detection
- Feature IDs prefixed with phase: `p1-`, `p2-`, etc.
- JSON format reduces accidental overwrites

### claude-progress.txt

Session handoff file:

```
=== Project Name - Development Progress ===

Last Updated: YYYY-MM-DD
Current Phase: N (Phase Name)
Total Features: X
Passing: Y

---

=== Session: YYYY-MM-DD ===

COMPLETED:
- [feature-id]: Brief description

IN PROGRESS:
- None (clean state preferred)

BLOCKERS:
- Any issues preventing progress

NEXT PRIORITY:
- [feature-id] from features.json

GIT COMMITS THIS SESSION:
- [hash]: [message]

NOTES:
- Context for next session
```

### init.sh

Startup script for consistent session initialization:

```bash
#!/bin/bash
set -e

# Verify directory
if [ ! -f "package.json" ]; then
  echo "ERROR: Not in project root"
  exit 1
fi

# Show progress
head -40 claude-progress.txt

# Show feature status
passing=$(grep -c '"passes": true' features.json || echo 0)
total=$(grep -c '"passes":' features.json || echo 0)
echo "Features: $passing / $total passing"

# Start dev server
npm run dev &
```

## Session Protocol

### Session Start

1. Run `pwd` to confirm working directory
2. Read `claude-progress.txt` for recent context
3. Read `features.json` to identify next incomplete feature
4. Check `git log --oneline -10` for recent changes
5. Run dev server, verify basic functionality works

### During Session

- Work on ONE feature at a time
- Commit after each working feature
- Update progress file incrementally

### Session End

1. Ensure code compiles and runs
2. Write descriptive git commit
3. Update `claude-progress.txt`
4. Mark features `"passes": true` only after verification
5. Leave codebase in clean, working state

## Verification Protocol

Features are not complete until verified. Two approaches:

### Manual Verification

```
Feature: [description]
1. Start dev server
2. Navigate to feature
3. Execute each verification step from features.json
4. Confirm expected behavior
5. Only then mark passes: true
```

### Automated Verification (Playwright MCP)

Use the `playwright-verification` skill for browser-based automated verification:

```bash
# In Claude Code CLI
claude
> /project:verify p1-feature-name    # Single feature
> /project:verify-all                 # All incomplete
```

See `skills/playwright-verification/SKILL.md` for full documentation.

**Never mark passing based solely on:**
- Code compiling
- Unit tests passing
- "It should work"

## Dependency Management

Features can declare dependencies:

```json
{
  "id": "p1-search",
  "dependencies": ["p1-list"],
  "passes": false
}
```

**Rules:**
- Don't start a feature until dependencies pass
- Verification skips features with unmet dependencies
- Dependency graph shown in claude-progress.txt

## Phase Transitions

When all features in a phase pass:

1. Update `currentPhase` in features.json meta
2. Add new phase features to features.json
3. Update claude-progress.txt with phase summary
4. Commit: "Complete phase N, begin phase N+1"

## File Structure

```
project/
├── .claude/
│   ├── settings.json          # MCP config (if using Playwright)
│   └── commands/
│       ├── verify.md          # Single feature verification
│       └── verify-all.md      # Batch verification
├── features.json              # Feature tracking
├── claude-progress.txt        # Session handoff
├── init.sh                    # Dev startup script
└── skills/
    └── playwright-verification/
        └── SKILL.md           # Verification skill docs
```

## Common Failure Modes

### One-Shotting
**Problem:** Attempting entire phase in single session
**Solution:** Work on ONE feature, verify, commit, repeat

### Premature Completion
**Problem:** Marking features passing without verification
**Solution:** Run verification steps explicitly, document results

### Broken Handoffs
**Problem:** Leaving code in non-working state
**Solution:** Always commit working code, update progress file

### Dependency Violations
**Problem:** Starting features before dependencies pass
**Solution:** Check dependency graph before starting work

## Templates

See `assets/` for starter templates:
- `features-template.json` - Empty feature list structure
- `progress-template.txt` - Session handoff template
- `init-template.sh` - Dev session startup script

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `playwright-verification` | Automated browser testing |
| `basilisk-av` | Project-specific patterns |
| `basilisk-style` | Design system reference |

## Quick Reference

```bash
# Session start
./init.sh

# Check status
grep -c '"passes": true' features.json  # Count passing
head -50 claude-progress.txt            # Recent context

# After implementing feature
claude
> /project:verify p1-feature-name

# Session end
git add -A
git commit -m "feat: implement p1-feature-name"
# Update claude-progress.txt
```
