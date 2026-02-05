---
name: codex-collaboration
description: "Codex CLI integration for code review and consultation. Use when: (1) code needs review before commit, (2) need expert consultation on implementation approach, (3) debugging assistance needed. This skill provides Codex interaction patterns only - workflow orchestration is defined in project CLAUDE.md."
---

# Codex Collaboration Skill

Provides Codex CLI interaction patterns for code review and consultation.

## Codex CLI Commands

### Code Review (Primary Use)
```bash
# Standard review
codex review --uncommitted

# Review specific changes
codex exec -m gpt-5.2 "
Review this implementation:
$(git diff)

Check:
1. Correctness
2. Bugs
3. Security
4. Code quality
5. Edge cases

Verdict: PASS or FAIL with issues
"
```

### Consultation
```bash
# Ask for guidance
codex exec -m gpt-5.2 "
Context: [CONTEXT]
Question: [SPECIFIC_QUESTION]
"

# Interactive session
codex "Help me with [TOPIC]"
```

### Full Auto Execution
```bash
# Let Codex make changes
codex --full-auto "Implement [TASK]"

# With workspace access
codex -C /path/to/project --full-auto "Task"
```

## Review Gate Pattern

```
Code Change
    │
    ▼
codex review
    │
    ├── PASS → git commit
    │
    └── FAIL → Fix issues → Re-review
```

### Review Result Handling

**PASS:**
```bash
git add .
git commit -m "type(scope): description"
```

**FAIL:**
1. Parse issues from output
2. Fix each issue
3. Re-submit: `codex review`
4. Repeat until PASS

## Model Options

- `gpt-5.2` - Latest flagship (recommended)
- `gpt-5.1-codex-mini` - Faster, cheaper

## Usage Examples

### Before Commit
```bash
# After implementing a feature
codex review
# If PASS, commit
# If FAIL, fix and re-review
```

### When Stuck
```bash
codex exec -m gpt-5.2 "
I'm implementing [TASK].
Current code: [CODE]
Issue: [PROBLEM]
What's the best approach?
"
```

### Architecture Decision
```bash
codex exec -m gpt-5.2 "
Option A: [APPROACH_A]
Option B: [APPROACH_B]
Constraints: [CONSTRAINTS]
Which is better and why?
"
```
