---
name: wrap-up
description: End-of-day command to capture what happened, consolidate notes, and set up for tomorrow. Use when the user types /wrap_up, says "end of day", "wrapping up", or "done for the day". Gathers git activity, integrates /note entries, and creates a daily summary in activity.md.
---

# End of Day Wrap-up

> End-of-day command to capture what happened, consolidate notes, and set up for tomorrow.

## When to Use
- End of a work session
- End of the day
- When switching contexts for a while
- RA may suggest this after 4pm based on user preferences

## Execution Steps

### 1. Gather Today's Context

**Check git activity:**
```bash
# Files changed today
git diff --stat

# Commits made today
git log --oneline --since="midnight" --author="$(git config user.name)"

# Uncommitted changes
git status --short
```

**Read existing context:**
- `.research/logs/activity.md` - Check for any `/note` entries from today
- `tasks.md` - Check for completed tasks today
- Recent file modifications in key directories (`scripts/`, `manuscript/`, `data/`)

### 2. Check for Today's Notes

Look for entries in `activity.md` that match today's date pattern `## [YYYY-MM-DD]`.

If notes exist:
- Extract them to integrate into the full summary
- These become the seed for the "Notes" section

### 3. Draft Activity Entry

Generate a draft using the Quick Session Entry template:

```markdown
## [YYYY-MM-DD]

**Session focus**: [Inferred from git commits and file changes]

**Accomplished**:
- [Generated from git commits]
- [Generated from file changes]
- [Any completed tasks from tasks.md]

**Decisions made**:
- [Ask user if not apparent]

**Next steps**:
- [Suggest based on context]

**Notes**:
- [Integrate any /note entries from today]
- [Any observations from the work]
```

### 4. Present Draft to User

Show the draft and ask:

```
Here's a summary of today's work:

[DRAFT ENTRY]

---

**Anything to add or change?**
- Decisions you made?
- Challenges you hit?
- Thoughts for tomorrow?

(Or say "looks good" to save as-is)
```

### 5. Integrate User Feedback

If user provides additional input:
- Incorporate their comments into appropriate sections
- Add any mentioned decisions to "Decisions made"
- Add any mentioned challenges to "Notes"
- Update "Next steps" if they specify priorities

### 6. Save Entry

Prepend the final entry to `.research/logs/activity.md`:
- Add after the templates section (after the `---` separator following "Digital Documentation Standards")
- Ensure proper formatting with blank lines

### 7. Offer Follow-up Actions

```
Entry saved! Before you go:

A) Commit your changes? [if uncommitted work exists]
B) Update tasks.md? [if accomplishments suggest completed tasks]
C) All set - see you next time!
```

## Example Output

```
📝 Wrapping up your day...

Based on your git activity and file changes, here's today's summary:

---

## 2024-12-02

**Session focus**: Pipeline development - preprocessing stage

**Accomplished**:
- Added data validation script (`scripts/validate_input.py`)
- Fixed edge case in preprocessing (commit: "handle empty rows")
- Updated params.yaml with new threshold values

**Decisions made**:
- [None detected - any decisions to note?]

**Next steps**:
- Run full pipeline with new validation
- Review output quality metrics

**Notes**:
- From earlier: "Realized the preprocessing step might be dropping too many samples"

---

**Anything to add or change?**
```

## Edge Cases

### No git activity today
```
I don't see any git commits or file changes today. 

Did you work on something outside this project, or would you like to 
log some notes about planning/thinking work?
```

### User says "nothing to add"
Save the draft as-is with a confirmation:
```
Saved! Your next session will pick up right where you left off.
```

### Very short session
If minimal activity, offer a simpler format:
```
Looks like a lighter session. Quick note instead of full entry?

> [User provides brief note]

Got it, added to today's log.
```

## Related Skills
- `note` - Add quick thoughts during the day (integrated by /wrap_up)
- `next` - Start of session, will reference this entry
- `weekly-review` - Aggregates these daily entries
