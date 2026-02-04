---
name: process-journals
description: Review journal entries and extract valuable knowledge into formal documentation
group: docent
keywords: [knowledge-management, documentation, journals, review, process journals, extract knowledge]
version: 1.0.0
author: docent
---

# Process Journals Runbook

This runbook guides you through reviewing journal and note entries to extract valuable knowledge into formal project documentation.

## Purpose

Journals and notes capture raw project knowledge - decisions made, discoveries, rationale, and context. This runbook helps systematically review them and extract insights into permanent documentation.

## Prerequisites

- `.docent/journals/` directory with journal entries
- `.docent/notes/` directory with notes
- Write access to documentation directories

## Procedure

### Step 1: List Recent Journal Entries

**Action:** Find journal entries from the last 7-30 days

```bash
find .docent/journals -name "*.md" -mtime -30 -type f | sort
```

**Review:** Scan the list to identify which sessions to review

### Step 2: Review Each Journal Entry

**Action:** Read through journal entries looking for:

**Knowledge worth preserving:**

- Architecture decisions → Should become ADRs
- Important discoveries → Should be in guides or READMEs
- "Why" rationale → Should be in code comments or docs
- Patterns/conventions → Should be in standards docs
- Problems solved → Should be in troubleshooting guides

**Decision Point:** For each piece of knowledge, ask:

- Is this still relevant?
- Would future developers need to know this?
- Does this explain "why" something was done?

### Step 3: Extract Architecture Decisions

**Action:** For significant technical decisions found in journals

**Use `/docent:act create-adr`** (if available) or `/docent:tell` to create ADR:

```
/docent:tell create an ADR documenting [the decision]

Context from journal:
- Decision: [what was decided]
- Rationale: [why it was decided]
- Date: [when]
- Alternatives considered: [other options]
```

**Location:** `.docent/decisions/`

### Step 4: Extract Implementation Insights

**Action:** For useful implementation details or patterns

**Use `/docent:tell`** to add to appropriate documentation:

```
/docent:tell add implementation note to [relevant doc]:

[insight from journal]
```

**Common locations:**

- Technical details → `docs/guides/`
- API usage → `docs/api/`
- Setup/configuration → `README.md` or `docs/setup.md`
- Troubleshooting → `docs/troubleshooting.md`

### Step 5: Extract Project Context

**Action:** For project evolution and timeline information

**Update project documentation:**

- Add to `CHANGELOG.md` if it's a notable change
- Update `docs/roadmap.md` with completed items
- Document in `docs/history.md` or similar

### Step 6: Clean Up Processed Journals

**Decision Point:** What to do with processed journals?

**Option A: Archive**

- Move to `.docent/journals/archive/YYYY/`
- Keeps history but clearly marks as processed

**Option B: Keep as-is**

- Leave in place for historical reference
- Add "Processed: YYYY-MM-DD" note at top

**Option C: Distill and delete**

- Extract all value into docs
- Delete the journal entry
- Use when journals are truly ephemeral

**Recommended:** Option A (archive) - preserves history without clutter

```bash
mkdir -p .docent/journals/archive/$(date +%Y)
mv .docent/journals/2025-10-*.md .docent/journals/archive/2025/
```

### Step 7: Review Notes Directory

**Action:** Process `.docent/notes/` similarly

**Notes are often:**

- TODO lists → Convert to issues or project tracking
- Research findings → Extract to guides
- Meeting notes → Extract action items and decisions
- Scratch pads → Delete if no longer relevant

**Process:**

1. Read each note file
2. Extract actionable/valuable content
3. Delete or archive the note

### Step 8: Update Documentation Index

**Action:** Ensure new/updated docs are discoverable

**Tasks:**

- Update `docs/README.md` or index if it exists
- Check cross-references are correct
- Verify internal links work

### Step 9: Commit Documentation Updates

**Action:** Create a commit with extracted knowledge

```bash
git add .docent/decisions/ docs/
git commit -m "docs: extract knowledge from journal review

- Added ADRs for [decisions]
- Updated [guides] with implementation insights
- Documented [context/rationale]

Processed journals: [date range]"
```

### Step 10: Report Summary

**Action:** Provide summary of knowledge extracted

**Report:**

- Number of journal entries reviewed
- ADRs created
- Documentation files updated
- Valuable insights extracted
- Items archived or deleted

**Example Output:**

```
📋 Journal Processing Summary

Reviewed: 3 journal entries (2025-10-23 to 2025-10-29)

Extracted:
  ✓ 2 architecture decisions → .docent/decisions/
  ✓ 4 implementation insights → docs/guides/
  ✓ 1 troubleshooting tip → docs/troubleshooting.md
  ✓ Project timeline updated → CHANGELOG.md

Archived: 3 journal files → .docent/journals/archive/2025/

Knowledge preserved and organized! 🎉
```

## Cadence

**Recommended frequency:**

- **Weekly:** Review journals from past week
- **Monthly:** Deep review of all journals, extract to formal docs
- **Before releases:** Ensure all valuable context is documented

## Error Handling

### No Journals Found

**If:** `.docent/journals/` is empty or doesn't exist

**Action:** Nothing to process - this is normal for new projects or between sessions

### Unclear What to Extract

**If:** Uncertain whether journal content is valuable

**Rule of thumb:**

- If it explains "why" → Extract it
- If it would help future debugging → Extract it
- If it's project-specific context → Extract it
- If it's just "what I did" without insight → Can skip

**When in doubt:** Extract to notes first, decide later

### Documentation Location Unclear

**If:** Not sure where extracted knowledge should go

**Ask `/docent:ask`:**

```
/docent:ask where should documentation about [topic] go?
```

Or create a new guide if appropriate.

## Tips

**Efficient Processing:**

- Block time weekly for this (15-30 min)
- Use `/docent:tell` to speed up documentation updates
- Focus on "why" not "what" (code shows what, docs explain why)
- Date journal entries for easy filtering

**Knowledge Triage:**

- **High value:** Architecture decisions, non-obvious solutions, context
- **Medium value:** Implementation tips, useful patterns, discoveries
- **Low value:** Routine work logs, obvious steps, temporary notes

**Avoid Over-Documenting:**

- Not everything needs extraction
- Focus on knowledge that has lasting value
- Routine implementation details often don't need docs

## Validation

After processing:

- Verify ADRs are well-formed and clear
- Check that extracted docs make sense on their own
- Ensure cross-references are correct
- Test that `/docent:ask` can find the extracted knowledge

## Notes

- This process turns raw journal knowledge into searchable, structured documentation
- Journals become a valuable "inbox" for project knowledge
- Regular processing prevents knowledge loss and improves project understanding
- The act of extraction forces clarity and distillation of insights
