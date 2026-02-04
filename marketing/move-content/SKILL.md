---
name: move-content
description: Move or rename files in knowledge base with directory governance. Use when user wants to move, relocate, or rename content. Reads RULE.md of both source and target directories.
---

# Move Content Skill

Generic file move/rename Skill that respects both source and target RULE.md requirements.

## When to use this Skill

- User says "move", "relocate", "transfer", "rename"
- User requests reorganization
- User wants to reclassify content to different directory

## Workflow

### 1. Identify Source File

**If user provides file path**:
- Verify file exists
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

### 2. Determine Target Location

**If user specifies target**:
- Parse target path
- Verify target directory exists (or offer to create)
- Confirm target path with user

**If user doesn't specify target**:
- Analyze content (read source file)
- Scan available directories
- Read RULE.md files to understand purposes
- Recommend target directory based on content
- Ask user for confirmation or alternative

**Recommendation logic** (similar to add-content):
1. Analyze file content
2. Read RULE.md of potential target directories
3. Match content to directory purposes
4. Rank by suitability
5. Present top recommendation

### 3. Read Both RULE.md Files

**Read source directory RULE.md**:
1. Check if moving out is allowed
2. Check if any special handling required (e.g., "notify when file moved")
3. Understand current file format

**Read target directory RULE.md**:
1. Check if moving in is allowed
2. Check file format requirements
3. Check naming conventions
4. Check if transformation needed
5. Understand target directory structure

**Compare requirements**:
- Source format vs target format
- Source naming vs target naming
- Compatibility check

### 4. Check Compatibility

**Format compatibility**:
- Both use markdown → Compatible
- Source has frontmatter, target doesn't require → Compatible (but may want to remove)
- Source plain, target requires frontmatter → Needs transformation
- Different metadata requirements → Needs update

**Naming compatibility**:
- Source: `topic-name.md`
- Target requires: `YYYY-MM-DD-topic-name.md`
- → Needs rename during move

**Structure compatibility**:
- Source is single file
- Target requires directory structure (file + metadata)
- → Needs structure creation

**Identify required transformations**:
1. Rename (filename format change)
2. Format conversion (add/remove frontmatter)
3. Structure change (file → directory with multiple files)
4. Content adaptation (modify to fit target requirements)

### 5. User Confirmation

**Present move summary**:
```
📦 Move confirmation

Source: [source path]
Target: [target path]

Compatibility check:
✅ Format: Compatible (or ⚠️ Needs transformation)
✅ Naming: Compatible (or ⚠️ Will rename to: [new name])
✅ Structure: Compatible (or ⚠️ Will restructure)

RULE.md policies:
- Source: [policy summary]
- Target: [policy summary]

Transformations needed:
- [List of changes required]

Cross-references:
- [X] files reference this content

Proceed with move?
- Yes (execute move with transformations)
- No (cancel)
- Show me what will change
```

**If transformations needed**:
- Explain each transformation clearly
- Show before/after examples
- Get explicit confirmation

### 6. Execute Move

**Basic move** (no transformation needed):
```bash
mv [source path] [target path]
```

**Move with rename**:
```bash
mv [source path] [target directory]/[new filename]
```

**Move with transformation**:
1. Read source file
2. Apply transformations:
   - Add/remove/modify frontmatter
   - Adjust content format
   - Update internal references
3. Write to target location with new format
4. Verify target file created successfully
5. Delete source file (only after target verified)

**Move with restructure**:
1. Create target directory structure
2. Split/reorganize content per target RULE.md
3. Create all required files in target
4. Verify all files created successfully
5. Delete source file/directory

**Preserve metadata** (when possible):
- Modification timestamps
- Creation date (in frontmatter if present)
- Author information
- Tags and categories

### 7. Update Cross-References

**Find references to moved file**:
```bash
grep -r "[old path]" .
grep -r "[old filename]" .
```

**Update strategies**:
- **Relative paths**: Update to new relative path
- **Absolute paths**: Update to new absolute path
- **Title references**: No change needed if file title unchanged

**Offer to update**:
```
Found references in:
- [file1.md] (line 45)
- [file2.md] (line 12, 89)

Would you like me to update these references?
- Yes, update all
- Yes, but let me review each
- No, I'll update manually
```

**Execute reference updates**:
- Use Edit tool to update each file
- Change old path to new path
- Verify updates successful
- Report which files were updated

### 8. Governance Update

**Update source directory README.md**:
1. Read source README.md
2. Remove entry for moved file
3. Add to "Recent Changes": "Moved filename.md to [target]"
4. Update "Last updated" timestamp
5. Save source README.md

**Update target directory README.md**:
1. Read target README.md
2. Add entry for moved file (with description)
3. Add to "Recent Changes": "Added filename.md from [source]"
4. Update "Last updated" timestamp
5. Save target README.md

**Update parent README.md files if needed**:
- If directories changed significance
- If directory now empty/no longer empty

**Verify updates**:
- Both README.md files valid markdown
- Entry removed from source, added to target
- Timestamps current

### 9. Report to User

**Confirm move complete**:
```
✅ File moved successfully

From: [old path]
To: [new path]

Transformations applied:
- [List of changes]

Cross-references updated:
- [X] files updated
- [List of files]

README.md updated:
- [source directory]/README.md (removed entry)
- [target directory]/README.md (added entry)

Note: [Any important notes, e.g., "Format changed to match target requirements"]
```

## Special Cases

### Rename in Same Directory

If user only wants to rename (not move):
```
User: "Rename transformer-draft to transformer-architecture"
```

**Process**:
1. Identify source file
2. Check RULE.md for naming conventions
3. Verify new name follows conventions
4. Execute rename: `mv old-name.md new-name.md`
5. Update references to this file
6. Update README.md (change entry name)
7. Report rename complete

### Move Entire Directory

If user wants to move entire directory:
```
User: "Move the AI research folder to Projects"
```

**Process**:
1. Identify source directory
2. Read source and target RULE.md
3. Check all files in directory for compatibility
4. Identify all external references
5. Present comprehensive summary
6. Request confirmation
7. Execute directory move: `mv [source dir] [target dir]/`
8. Update all cross-references
9. Update README.md in both locations
10. Update parent README.md files

### Incompatible Format Requires Manual Intervention

If automatic transformation not possible:
```
Source: Complex structured data
Target: Requires specific format that can't be auto-converted
```

**Process**:
1. Detect incompatibility
2. Warn user: "Automatic conversion not possible"
3. Explain what manual changes needed
4. Offer: "I can move the file, but you'll need to manually reformat"
5. Or: "I can create target structure and copy content, but you'll need to reorganize"
6. User decides next steps

### Move with Merging

If target already has file with same name:
```
User: "Move note.md to Research/"
Research/note.md already exists
```

**Process**:
1. Detect name conflict
2. Read both files
3. Options:
   - Rename: "note-2.md" or "note-YYYYMMDD.md"
   - Merge: Combine contents (if compatible)
   - Replace: Overwrite existing (with backup)
4. Present options to user
5. Execute chosen strategy

### Preserve Directory Structure

If moving subdirectory that has its own structure:
```
Moving: Research/AI/transformers/
Target: Projects/AIResearch/
```

**Process**:
1. Check if should preserve subdirectory structure
2. Option A: `Projects/AIResearch/transformers/` (preserve)
3. Option B: `Projects/AIResearch/` (flatten)
4. Ask user preference
5. Execute accordingly
6. Update all README.md in hierarchy

## Error Handling

### Source File Not Found
```
User: "Move transformer note to Projects"
→ Search for file
→ No matches
→ Report: "I couldn't find transformer note to move"
```

### Target Directory Doesn't Exist
```
User: "Move file.md to NewCategory/"
NewCategory/ doesn't exist
→ Ask: "NewCategory doesn't exist. Create it?"
→ If yes: create directory, create RULE.md/README.md, then move
→ If no: cancel
```

### RULE.md Forbids Moving Out
```
Source RULE.md: "Files cannot be moved out of this directory"
→ Warn: "Source RULE.md forbids moving files out"
→ Ask: "Override this rule?"
→ If yes: proceed with warning note
→ If no: cancel
```

### RULE.md Forbids Moving In
```
Target RULE.md: "Only specific file types allowed"
Source file doesn't match
→ Warn: "Target RULE.md restrictions prevent this move"
→ Explain restrictions
→ Suggest: "Convert file format first or choose different target"
```

### Transformation Fails
```
Attempting to add required frontmatter
Transformation fails (invalid YAML, etc.)
→ Report error
→ Keep source file intact
→ Don't create partial target
→ Suggest manual review
```

### Cross-Reference Update Fails
```
Move successful but can't update all references
Some files locked, permission denied, etc.
→ Report: "Move complete, but couldn't update all references"
→ List files that need manual update
→ Provide old and new paths for manual fixing
```

## Integration with Governance

This Skill automatically invokes the governance protocol:

**Before move**:
- Read both source and target RULE.md
- Validate move is allowed
- Check compatibility

**During move**:
- Apply required transformations
- Preserve important metadata
- Execute safely (verify target before deleting source)

**After move**:
- Update both source and target README.md
- Update cross-references
- Verify complete

## Examples

### Example 1: Simple Move

**User**: "Move transformer-draft from Research/AI to Projects/"

**Skill workflow**:
1. Finds `Research/AI/transformer-draft.md`
2. Reads Research/AI/RULE.md → Moves allowed
3. Reads Projects/RULE.md → Files named `project-name.md`, requires frontmatter
4. Detects: needs frontmatter addition
5. Confirms: "Move to Projects/, will add required frontmatter"
6. User confirms
7. Reads source file
8. Adds frontmatter with title, date, status
9. Writes to `Projects/transformer-draft.md`
10. Updates cross-references (found 2)
11. Updates both README.md files
12. Reports: "✅ Moved with frontmatter added"

### Example 2: Move with Rename

**User**: "Move the old transformer note to ReadLater"

**Skill workflow**:
1. Finds `Research/transformer-old.md`
2. Reads Research/RULE.md and ReadLater/RULE.md
3. ReadLater requires: `Articles/YYYY/MM/YYYY-MM-DD_title/article.md`
4. Detects: needs complete restructure
5. Warns: "Target requires directory structure, not single file"
6. Shows transformation: `transformer-old.md` → `Articles/2025/10/2025-10-28_transformer-old/article.md`
7. User confirms
8. Creates directory structure
9. Moves and renames file
10. Creates metadata.yaml (as ReadLater requires)
11. Updates README.md files
12. Reports: "✅ Moved and restructured per ReadLater requirements"

### Example 3: Directory Move

**User**: "Move the old-research folder to Archive"

**Skill workflow**:
1. Finds `Research/old-research/` (15 files)
2. Reads Research/RULE.md and Archive/RULE.md
3. Checks all 15 files for external references → Found 3 references
4. Confirms: "Move old-research/ (15 files) to Archive/? 3 external references found"
5. User confirms
6. Executes: `mv Research/old-research/ Archive/`
7. Updates 3 files with broken references
8. Updates README.md:
   - Research/README.md (removes subdirectory)
   - Archive/README.md (adds subdirectory)
9. Reports: "✅ Moved 15 files, updated 3 references"

## Best Practices

1. **Check both RULE.md files** - Source and target may have different rules
2. **Verify compatibility** - Ensure file can fit in target format
3. **Transform carefully** - Preserve content integrity during format changes
4. **Update cross-references** - Prevent broken links
5. **Update both README.md** - Source (remove) and target (add)
6. **Verify before deleting source** - Ensure target created successfully
7. **Report transformations clearly** - User should know what changed
8. **Handle errors gracefully** - Don't leave partial state

## Notes

- This Skill works with any directory structure by reading RULE.md
- Respects both source and target governance rules
- Handles format transformations automatically when possible
- Updates cross-references to prevent broken knowledge base
- Maintains README.md indexes in both locations
- Works in parallel with CLAUDE.md subagents
- Can rename, move, and restructure all in one operation
