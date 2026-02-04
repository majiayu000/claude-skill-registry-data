---
name: delete-content
description: Delete files from knowledge base with directory governance. Use when user wants to remove or delete content. Reads RULE.md to check deletion permissions and handles dependencies.
---

# Delete Content Skill

Generic file deletion Skill that checks RULE.md permissions and handles dependencies safely.

## When to use this Skill

- User says "delete", "remove", "trash"
- User requests content deletion
- User wants to clean up old files

## Workflow

### 1. Identify Target File

**If user provides file path**:
- Verify file exists using `ls` or Read
- Confirm file identity

**If user provides topic/title only**:
- Search for file using Grep or Glob
- Pattern: `**/*keyword*.md`
- If multiple matches: present list, ask user to choose
- If no matches: report not found

**Search strategies**:
1. Filename match: `find . -name "*keyword*"`
2. Content match: `grep -r "keyword" .`
3. README.md index: Search README.md files for references

### 2. Read Directory RULE.md

**Locate and read RULE.md**:
1. Check file's directory for RULE.md
2. If not found, check parent directories (inheritance)
3. Parse RULE.md for deletion rules

**Check for**:
- Are deletions allowed? (some directories may be immutable or archive-only)
- Archive-instead rules (move to archive instead of delete)
- Backup requirements (create backup before delete)
- Dependency rules (check cross-references)
- Confirmation requirements

**Example RULE.md deletion rules**:
```markdown
## Deletion Rules
- Deletions allowed with confirmation
- Check for cross-references before deleting
- Move to Archive/ subdirectory instead of permanent deletion
```

### 3. Check Dependencies

**Search for cross-references**:
1. Use Grep to find links to this file: `grep -r "filename" .`
2. Search for references in README.md files
3. Check for reverse links (files this file links to)
4. Identify files that depend on this content

**Categorize dependencies**:
- **Incoming**: Files that link to this file (will break if deleted)
- **Outgoing**: Files this file links to (won't break, but orphans references)
- **Bidirectional**: Cross-referenced files (mutual dependencies)

**Severity assessment**:
- Critical: Many incoming links, part of important workflow
- Warning: Some incoming links, moderately used
- Low: Few or no dependencies

### 4. User Confirmation

**Present deletion summary**:
```
⚠️  Delete confirmation required

File: [path to file]
Size: [file size]
Last modified: [timestamp]

Dependencies found:
- [file1.md] links to this file
- [file2.md] links to this file
(Total: X files reference this content)

RULE.md policy: [deletion policy summary]

Are you sure you want to delete this file?
- Yes, delete permanently
- Yes, move to archive (if RULE.md allows)
- No, cancel
- Show me the dependencies first
```

**If user requests dependency review**:
- Show each file that references this content
- Show the context (line where reference appears)
- Allow user to reconsider

### 5. Execute Deletion

**Based on RULE.md policy**:

**Permanent deletion**:
```bash
rm [file path]
```
- Only if RULE.md allows or user explicitly overrides
- Use Bash tool with rm command
- Verify deletion successful

**Archive instead**:
```bash
# Create archive directory if not exists
mkdir -p Archive/
# Move file to archive
mv [file path] Archive/[filename]
```
- Follow RULE.md archive structure
- Preserve filename or add timestamp
- Update archive README.md

**Backup then delete**:
```bash
# Create backup
cp [file path] [backup path]
# Then delete original
rm [file path]
```
- Create backup per RULE.md specification
- Verify backup successful before deleting

### 6. Governance Update

**Update README.md**:
1. Read current README.md
2. Find entry for deleted file
3. Remove entry from file list
4. Add to "Recent Changes" section:
   ```markdown
   - YYYY-MM-DD: Removed filename.md
   ```
5. Update "Last updated" timestamp
6. Save README.md

**Update parent README.md if needed**:
- If directory now empty, update parent
- Note directory is empty or removed

**Handle cross-references**:
- Update files that referenced deleted content (if possible)
- Or add note in README.md: "Files with broken references: [list]"
- Offer to update broken links

**Verify cleanup**:
- Ensure no orphaned references
- Check README.md is valid markdown
- Confirm directory structure intact

### 7. Report to User

**Confirm deletion complete**:
```
✅ File deleted successfully

Deleted: [path to file]
Method: [permanent deletion / moved to archive / backed up then deleted]

README.md updated:
- [directory]/README.md

Dependencies handled:
- [X] files need attention (broken links)
- [List of affected files]

Recommendation: Review affected files to update/remove broken links
```

**If archived instead**:
```
✅ File archived successfully

Original: [original path]
Archived to: [archive path]
Archive method: [per RULE.md policy]

README.md updated:
- [directory]/README.md
- Archive/README.md

Note: File preserved in archive, not permanently deleted
```

## Special Cases

### Immutable Directory

If RULE.md specifies immutable:
```markdown
## RULE.md says: "This directory is immutable - no deletions allowed"
```

**Process**:
1. Warn user: "RULE.md indicates this directory should not have deletions"
2. Explain policy reasoning
3. Ask: "Do you want to override this rule?"
4. If yes: proceed with deletion and log rule override
5. If no: cancel operation

### Archive-Only Policy

If RULE.md requires archival instead:
```markdown
## RULE.md says: "Move to Archive/ instead of deleting"
```

**Process**:
1. Don't offer permanent deletion
2. Execute archive operation
3. Update both original and archive README.md
4. Report archive location

### Batch Deletion

If user requests deleting multiple files:
```
User: "Delete all old notes from last year"
```

**Process**:
1. Identify all matching files
2. Check each file's RULE.md
3. Check dependencies for each
4. Present summary: "X files match, Y have dependencies"
5. Request batch confirmation
6. Execute deletions one by one
7. Report summary of all deletions

### Directory Deletion

If user wants to delete entire directory:
```
User: "Delete the old-project directory"
```

**Process**:
1. Read directory RULE.md for deletion rules
2. Check parent directory RULE.md for subdirectory rules
3. Scan all files in directory for external dependencies
4. Present comprehensive summary
5. Warn: "This will delete X files and Y subdirectories"
6. Request explicit confirmation
7. Execute recursive deletion or archive
8. Update parent README.md

### Soft Delete (Mark as Deleted)

If RULE.md specifies soft delete:
```markdown
## RULE.md says: "Mark files as deleted in frontmatter instead of removing"
```

**Process**:
1. Don't delete file physically
2. Update frontmatter: `status: deleted`
3. Update README.md: mark as `[DELETED] filename.md`
4. File stays but marked as obsolete

## Error Handling

### File Not Found
```
User: "Delete the transformer note"
→ Search for file
→ No matches found
→ Report: "I couldn't find a file about transformers. Nothing to delete."
```

### Multiple Matches
```
User: "Delete the transformer note"
→ Find 3 files with "transformer"
→ Present list: "I found 3 files. Which one to delete?"
→ User selects → Proceed
```

### RULE.md Forbids Deletion
```
RULE.md says: "Immutable directory"
→ Warn: "RULE.md forbids deletions in this directory"
→ Explain reasoning
→ Ask for override confirmation
→ If confirmed: proceed with warning note
```

### High-Impact Dependencies
```
File has 50+ incoming references
→ Warn: "⚠️  HIGH IMPACT: 50+ files reference this content"
→ Show most critical dependencies
→ Recommend: "Consider archiving instead of deleting"
→ Require explicit "yes, delete anyway" confirmation
```

### Deletion Fails
```
Bash rm command fails (permissions, file locked, etc.)
→ Report error clearly
→ Show exact error message
→ Suggest: "Check file permissions or if file is open in another program"
→ Offer alternatives: archive, rename, mark as deleted
```

### Broken References After Deletion
```
Deletion successful but broken links remain
→ Report: "Deletion complete, but broken references detected in:"
→ List affected files
→ Offer: "Would you like me to update these files to remove broken links?"
→ If yes: update files to remove/fix references
```

## Integration with Governance

This Skill automatically invokes the governance protocol:

**Before deletion**:
- Locate and read RULE.md
- Validate deletion is allowed
- Check dependency policy

**During deletion**:
- Follow RULE.md deletion method (delete, archive, backup)
- Execute safely

**After deletion**:
- Update README.md
- Handle broken references
- Verify cleanup complete

## Examples

### Example 1: Simple Deletion

**User**: "Delete the old transformer draft"

**Skill workflow**:
1. Searches for file → Finds `Research/AI/2025-10-15-transformer-draft.md`
2. Reads Research/AI/RULE.md → Deletions allowed with confirmation
3. Checks dependencies → No references found
4. Asks confirmation: "Delete transformer-draft.md? No dependencies found."
5. User confirms
6. Executes `rm Research/AI/2025-10-15-transformer-draft.md`
7. Updates Research/AI/README.md (removes entry)
8. Reports: "✅ Deleted transformer-draft.md"

### Example 2: Archive Instead

**User**: "Delete the 2024 work logs"

**Skill workflow**:
1. Finds Work/WorkLog/2024/ directory
2. Reads Work/WorkLog/RULE.md → "Move old logs to Archive/ instead of deleting"
3. Checks dependencies → Some cross-references to meeting notes
4. Presents: "Found 2024 logs (52 files). RULE.md policy: archive instead of delete"
5. User confirms
6. Creates `Work/WorkLog/Archive/2024/` if not exists
7. Executes `mv Work/WorkLog/2024/* Work/WorkLog/Archive/2024/`
8. Updates README.md files
9. Reports: "✅ Archived 52 log files to Archive/2024/"

### Example 3: High-Impact Deletion

**User**: "Delete the core-concepts document"

**Skill workflow**:
1. Finds `Research/core-concepts.md`
2. Reads Research/RULE.md → Deletions allowed
3. Checks dependencies → 25 files reference this document
4. Warns: "⚠️  HIGH IMPACT: 25 files reference core-concepts.md"
5. Shows first 5 most critical dependencies
6. Recommends: "This is a foundational document. Consider archiving instead?"
7. User still chooses delete
8. Asks: "Are you absolutely sure? Type 'delete core-concepts' to confirm"
9. User confirms
10. Executes deletion
11. Updates README.md
12. Reports broken references: "25 files need attention"
13. Offers to help fix broken links

## Best Practices

1. **Always check dependencies** - Prevent broken knowledge base
2. **Read RULE.md first** - Respect deletion policies
3. **Archive when possible** - Preserve content instead of permanent deletion
4. **Confirm before deleting** - No accidental deletions
5. **Update README.md immediately** - Keep index accurate
6. **Handle broken links** - Offer to fix cross-references
7. **Report clearly** - User should know what was deleted and impact
8. **Follow RULE.md policies** - Even if user requests override

## Notes

- This Skill works with any directory structure by reading RULE.md
- Checks for dependencies to prevent broken knowledge base
- Offers archival as safer alternative to permanent deletion
- Always requires confirmation for destructive operations
- Maintains README.md index integrity
- Works in parallel with CLAUDE.md subagents
- Never deletes RULE.md files (requires explicit governance agent action)
