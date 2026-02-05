---
name: process-sessions
description: Process ephemeral session notes and extract valuable knowledge into permanent documentation
group: docent
keywords: [knowledge-management, documentation, sessions, cleanup, review, process sessions, extract knowledge]
version: 1.0.0
author: docent
---

# Process Session Notes Runbook

This runbook guides you through reviewing ephemeral session notes, extracting valuable knowledge, and cleaning up processed sessions.

## Purpose

Session notes (`.docent/sessions/*.md`) capture detailed work logs from AI agent sessions - objectives, context, work performed, results, and lessons learned. This runbook helps:

1. Extract valuable insights into permanent documentation
2. Archive or delete processed ephemeral notes
3. Keep the sessions directory manageable
4. Prevent loss of important knowledge

## Prerequisites

- `.docent/sessions/` directory with session notes
- Write access to documentation directories
- Understanding of current project priorities

## Procedure

### Step 1: List Session Notes

**Purpose:** Identify all session notes to process

**Commands:**

```bash
# List all session notes sorted by modification time
ls -lt .docent/sessions/*.md

# Count total sessions
ls -1 .docent/sessions/*.md | wc -l
```

**Review:** Note which sessions are recent vs historical

---

### Step 2: Review Each Session Note

**Purpose:** Read through sessions to identify valuable content

**Action:** For each session note, read and look for:

**High-value knowledge:**

- **Architecture decisions** → Should become ADRs
- **Important discoveries** → Should be in guides or architecture docs
- **Problems solved** → Should be in troubleshooting guides
- **Lessons learned** → Should be documented to prevent future issues
- **Code reference updates** → May need to be captured in changelogs

**Medium-value knowledge:**

- Implementation patterns discovered
- Configuration changes made
- Dependencies updated
- Tool usage insights

**Low-value ephemeral content:**

- Routine implementation steps
- Standard git operations
- Normal debugging process
- Obvious code changes

**Decision Point:** For each piece of knowledge, ask:

- Will this help future developers?
- Does this explain "why" something was done?
- Would I want to know this 6 months from now?
- Is this already documented elsewhere?

---

### Step 3: Extract Architecture Decisions

**Purpose:** Capture significant technical decisions as ADRs

**Action:** For architecture decisions found in session "Lessons Learned" or "Context" sections

**Use `/docent:tell` to create ADR:**

```
/docent:tell create an ADR documenting [the decision]

Context from session:
- Decision: [what was decided]
- Rationale: [why it was decided]
- Date: [session date]
- Trade-offs: [from Lessons Learned section]
```

**Location:** `.docent/adr/`

**Example Decisions to Extract:**

- Technology choices (database, framework, library)
- API design decisions
- Data model changes
- Performance optimization approaches
- Security implementation choices

---

### Step 4: Extract Implementation Insights

**Purpose:** Document useful patterns and discoveries

**Action:** For valuable implementation details from "Work Performed" or "Results" sections

**Use `/docent:tell`:**

```
/docent:tell add to [relevant guide]:

From [session-date]: [insight or pattern discovered]
```

**Common locations:**

- Implementation patterns → `.docent/guides/`
- API usage → `.docent/guides/api-usage.md`
- Tool configuration → `.docent/guides/setup.md`
- Troubleshooting solutions → `.docent/guides/troubleshooting.md`

**Example Insights to Extract:**

- "Config X requires Y to work properly"
- "The build fails if Z is not set"
- "Performance improves 50% with W approach"

---

### Step 5: Update CHANGELOG and Documentation

**Purpose:** Ensure user-facing changes are documented

**Action:** Review "Results" section for changes that affect users or developers

**Update locations:**

- **CHANGELOG.md** - User-visible changes, new features, breaking changes
- **README.md** - New setup steps, changed requirements
- **Architecture docs** - Structural changes, new patterns

**Commands:**

```bash
# Check what's already in CHANGELOG
head -20 CHANGELOG.md

# Edit CHANGELOG if needed
# (Use Edit tool)
```

**Example CHANGELOG entries:**

```markdown
## [Unreleased]

### Added
- New session processing runbook for knowledge management

### Changed
- Documentation structure consolidated from docs/ to .docent/

### Fixed
- Broken links in architecture documentation
```

---

### Step 6: Capture Lessons Learned

**Purpose:** Prevent repeating mistakes and preserve insights

**Action:** Extract key points from "Lessons Learned" sections

**Use `/docent:tell`:**

```
/docent:tell document lesson learned:

[Copy lesson from session notes]
```

**Common documentation targets:**

- Project conventions → `.docent/guides/conventions.md`
- Common pitfalls → `.docent/guides/troubleshooting.md`
- Best practices → `.docent/guides/best-practices.md`
- Tool gotchas → `.docent/guides/tooling.md`

---

### Step 7: Clean Up Session Notes

**Purpose:** Remove ephemeral content after extraction

**Decision Point:** What to do with processed sessions?

**Option A: Archive by Year (Recommended)**

Keep history organized but clearly mark as processed:

```bash
# Create archive structure
mkdir -p .docent/sessions/archive/$(date +%Y)

# Move processed sessions
mv .docent/sessions/2025-10-*.md .docent/sessions/archive/2025/
```

**Benefits:**

- Preserves complete history
- Easy to reference if needed
- Keeps active directory clean

**Option B: Delete Ephemeral Sessions**

Completely remove sessions after extraction:

```bash
# Review one more time
ls .docent/sessions/2025-10-*.md

# Delete after confirming extraction is complete
rm .docent/sessions/2025-10-*.md
```

**Benefits:**

- Cleaner repository
- Focuses on permanent docs only
- Matches gitignore patterns for ephemeral content

**Recommended Approach:**

- **Archive** sessions with significant decisions or complex work
- **Delete** sessions with only routine changes or already-documented work
- **Keep recent** sessions (last 7-14 days) for reference

---

### Step 8: Standardize Session Naming

**Purpose:** Ensure consistent naming for easier processing

**Action:** Rename sessions to follow consistent pattern

**Standard format:** `YYYY-MM-DD-session-NNN.md`

**Commands:**

```bash
# Check current naming
ls .docent/sessions/

# Rename inconsistent files
mv .docent/sessions/session-2025-10-29.md \
   .docent/sessions/2025-10-29-session-001.md
```

**Validation:**

- All sessions follow date-first format
- Sessions on same day are numbered sequentially
- Easy to sort chronologically

---

### Step 9: Update .gitignore if Needed

**Purpose:** Ensure ephemeral sessions aren't accidentally committed

**Action:** Check if sessions should be gitignored

**Commands:**

```bash
# Check current gitignore
grep -A2 -B2 session .gitignore

# Check what's currently tracked
git ls-files .docent/sessions/
```

**Decision Point:**

- **Track sessions** if they're valuable project history
- **Ignore sessions** if they're truly ephemeral agent state

**If ignoring, add to .gitignore:**

```gitignore
# Docent ephemeral session notes
.docent/sessions/
!.docent/sessions/archive/
```

**Note:** Current project tracks sessions, but you may prefer different approach

---

### Step 10: Commit Documentation Updates

**Purpose:** Save extracted knowledge

**Action:** Create commit with changes

**Commands:**

```bash
# Check what changed
git status .docent/ CHANGELOG.md

# Stage changes
git add .docent/adr/ .docent/guides/ .docent/architecture/
git add CHANGELOG.md

# Create commit
git commit -m "docs: extract knowledge from session review

- Added ADRs for [decisions]
- Updated [guides] with implementation insights
- Documented [lessons learned]
- Cleaned up ephemeral session notes

Processed sessions: [date range]"
```

---

## Validation & Verification

### Success Criteria

How do you know processing succeeded?

- [x] All valuable insights extracted to permanent docs
- [x] Session notes archived or deleted appropriately
- [x] Documentation is searchable via `/docent:ask`
- [x] CHANGELOG updated if needed
- [x] No broken references to deleted sessions
- [x] Commit created with extracted knowledge

### Health Checks

Post-processing validation:

```bash
# Verify sessions directory is clean
ls -la .docent/sessions/

# Test documentation search works
# (Use /docent:ask to find extracted content)

# Check git status
git status
```

---

## Cadence

**Recommended frequency:**

- **After each significant session** - Extract while context is fresh
- **Weekly** - Process last week's sessions in batch
- **Before releases** - Ensure all valuable knowledge is documented
- **Monthly** - Deep review and aggressive cleanup

**Time estimates:**

- Quick session (routine work): 5 minutes
- Medium session (new features): 15 minutes
- Complex session (architecture changes): 30-45 minutes

---

## Troubleshooting

### Common Issues

**Issue:** Session contains valuable content but unclear where it belongs

**Solution:**

1. Use `/docent:ask where should documentation about [topic] go?`
2. Create new guide if no appropriate location exists
3. When in doubt, extract to `.docent/notes/` and decide later

---

**Issue:** Session describes decision but lacks full context

**Solution:**

1. Search related code to understand context better
2. Check git history for related commits
3. Use `/docent:tell` to document what you can reconstruct
4. Note in ADR that details were from session reconstruction

---

**Issue:** Multiple sessions cover same topic

**Solution:**

1. Read all related sessions together
2. Extract consolidated knowledge (not duplicate content)
3. Create single comprehensive doc covering the topic
4. Archive or delete all related sessions together

---

**Issue:** Unsure if session content is still relevant

**Solution:**

1. Check if code/files referenced still exist
2. Verify approaches described are still in use
3. When in doubt, extract with date context: "As of [date], ..."
4. Mark potentially outdated content for future review

---

## Tips

**Efficient Processing:**

- Process sessions immediately after completion (context is fresh)
- Use `/docent:tell` extensively to speed up extraction
- Focus on "why" and "lessons learned" - code shows "what"
- Create templates for common extraction patterns

**Knowledge Triage:**

- **High value:** Architecture decisions, non-obvious solutions, project context
- **Medium value:** Implementation patterns, tool discoveries, configuration gotchas
- **Low value:** Routine git operations, standard debugging, obvious code changes

**Avoid Over-Documenting:**

- Not every session needs extraction
- Routine implementation details don't need permanent docs
- Code reviews and simple refactors are often self-documenting

**Session Writing Tips (for future):**

- Write "Lessons Learned" with extraction in mind
- Make "Context" section rich for future reference
- Note "why" decisions were made, not just "what" was done
- Flag high-value insights as you work

---

## Notes & Warnings

💡 **Tip:** Process sessions while memory is fresh - much faster than processing old sessions

⚠️ **Warning:** Don't delete sessions until after extraction is complete and committed

📝 **Note:** Sessions are intentionally more detailed than journals - expect significant distillation during extraction

---

## References

- [Process Journals Runbook](./process-journals.md) - Similar workflow for journal entries
- [Bootstrap Runbook](./bootstrap.md) - Initial docent setup
- [Health Check Runbook](./health-check.md) - Project health validation

---

## Change Log

**2025-10-29:** Initial version
