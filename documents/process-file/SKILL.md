---
name: process-file
description: Process arbitrary files (email, PDF, Office docs, images, audio/video) and integrate with AkashicRecords for intelligent archiving. Reads file content, analyzes intent, and suggests appropriate storage location based on content and project preferences.
---

# Process File Skill

Generic file processing Skill supporting multiple file formats for parsing and intelligent archiving, fully integrated with the AkashicRecords governance system.

## When to use this Skill

- User says "read", "process"
- User says "archive", "import"
- User provides file path for processing
- User wants to integrate external files into knowledge base
- User provides email, PDF, Office documents, images, etc.

## Workflow

### 1. Initialization - Read Preferences

**Check claude.md**:
1. Read current project's claude.md
2. Look for `file-handling-preferences` related record
3. If path found, read preferences file

**If no preferences file exists**:
1. Ask user: "This is the first time using process-file skill in this project. Where would you like to create the file handling preferences?"
2. Suggest default location: `file-handling-preferences.md` in project root
3. After user confirmation, create file and record location in claude.md

**Preferences file structure**:
- Processing pattern records (by file type and content category)
- Auto processing settings (whether to allow saving without confirmation)
- Historical processing records

### 2. File Type Detection

**Detect file type**:
Determine processing method based on file extension:

| Type | Extension | Processing Tool |
|------|-----------|-----------------|
| Email | .eml | `mu view <filepath>` |
| PDF | .pdf | `markitdown <filepath>` |
| Word | .docx | `markitdown <filepath>` |
| PowerPoint | .pptx | `markitdown <filepath>` |
| Excel | .xlsx | `markitdown <filepath>` |
| Image | .jpg, .png, .gif, .webp, .bmp | Read tool (language model direct read) |
| Audio | .mp3, .wav, .m4a, .aac, .ogg | Ask user |
| Video | .mp4, .mov, .avi, .webm | Ask user |

**Tool availability check**:
- Check if required tools are installed before execution
- If `mu` not installed: Prompt `Please install maildir-utils: sudo apt install maildir-utils`
- If `markitdown` not installed: Prompt `Please install markitdown: pip install markitdown`

### 3. Content Extraction

**Email (.eml)**:
```bash
mu view <filepath>
```
Extract: sender, recipient, subject, date, body

**PDF/Office documents**:
```bash
markitdown <filepath>
```
Convert to markdown format

**Images**:
Use Read tool to directly read image, let language model analyze content:
- Identify image subject
- Extract text (if any)
- Describe image content

**Audio/Video**:
1. Ask user for suggested processing method
2. Possible options:
   - Record file metadata only
   - Use external tool for transcription
   - Record manual summary
3. Record user's chosen processing method in project claude.md

### 4. Content Analysis

**Analyze content**:
- Identify topics and keywords
- Determine content type (technical, personal, work, academic, etc.)
- Extract important information (dates, people, places, events)

**Infer user intent**:
- Archive for storage (long-term preservation)
- Project update (related to existing project)
- Record memo (personal notes)
- Data organization (batch processing)

**Match against preferences**:
- Check if preferences file has matching patterns
- If historical records exist, prioritize suggesting same processing method

### 5. Directory Discovery

**Use akashicrecords mechanism**:
1. Based on content analysis results, build search query
2. Scan knowledge base directory structure
3. Read each directory's RULE.md to understand purpose
4. Evaluate content-to-directory purpose match

**Suggestion logic**:
- Technical document + directory purpose "research" → high match
- Email + directory purpose "communications" → high match
- Personal photo + directory purpose "personal life" → high match
- No clear match → suggest Miscellaneous or ask user

### 6. User Confirmation

**Present analysis results**:
```
## File Analysis Results

**File**: [filename]
**Type**: [file type]
**Content Summary**: [brief summary]

**Inferred Intent**: [archive/update/record]

**Suggested Location**: [target directory path]
**Reason**: [why this location was chosen]

**Planned Operation**:
- Call add-content skill
- Format: [according to RULE.md]
- Filename: [suggested filename]

Do you approve this operation?
```

**Wait for confirmation**:
- Default requires user approval
- If `auto_save: true` in preferences, can skip confirmation
- User can modify suggested location or cancel

### 7. Execute

**Call corresponding akashicrecords skill**:
- Add new content → `add-content` skill
- Update existing → `update-content` skill

**Format according to target RULE.md**:
- Read target directory's RULE.md
- Follow naming conventions
- Apply frontmatter format (if required)

### 8. Update Preferences

**Record this processing experience**:
```markdown
### [Date] [File Type]
- Content characteristics: [key features]
- Target location: [actual storage location]
- Processing method: [skill used]
```

**Learning pattern**:
- Accumulate user preferences
- Prioritize suggesting same method for similar content next time

## Multi-File Processing

When user provides multiple files:

### Parallel Analysis
1. Launch a subagent for each file
2. Each subagent independently executes Phase 2-5
3. Wait for all subagents to complete

### Consolidated Presentation
```
## Multi-File Processing Analysis Results

| # | Filename | Type | Content Summary | Suggested Location | Operation |
|---|----------|------|-----------------|-------------------|-----------|
| 1 | file1.pdf | PDF | [summary] | Research/ | add-content |
| 2 | photo.jpg | Image | [summary] | Personal/ | add-content |
| 3 | email.eml | Email | [summary] | Work/ | add-content |

Please choose:
- Approve all
- Confirm individually
- Cancel
```

### Batch Execution
- After user approves all, execute sequentially
- When user confirms individually, confirm each file separately

## Error Handling

### Tool Not Installed
```
Warning: Cannot process .eml file: mu tool not installed
Please run: sudo apt install maildir-utils
```

### Unsupported File Format
```
Warning: Unsupported file format: .xyz
How would you like to proceed?
1. Try reading as plain text
2. Record file metadata only
3. Skip this file
```

### Parse Failure
```
Warning: Unable to parse file content
Error: [error message]
How would you like to proceed?
1. Retry
2. Enter summary manually
3. Skip this file
```

## Integration with Governance

**Before operation**:
- Read preferences file
- Confirm akashicrecords governance structure exists

**During operation**:
- Use akashicrecords skills for actual operations
- Follow target directory's RULE.md

**After operation**:
- Update preferences file
- akashicrecords skills automatically handle README.md updates

## Examples

### Example 1: Process PDF Paper

**User**: "Read ~/Downloads/transformer-paper.pdf"

**Workflow**:
1. Check preferences → Find historical record "technical paper → Research/Papers/"
2. Detect .pdf → Use markitdown
3. Execute `markitdown ~/Downloads/transformer-paper.pdf`
4. Analyze content → AI/machine learning topic
5. Match preferences → Matches "technical paper" pattern
6. Suggest Research/Papers/AI/
7. User confirms
8. Call add-content skill
9. Update preferences file

### Example 2: Batch Process Emails

**User**: "Archive these emails: email1.eml email2.eml email3.eml"

**Workflow**:
1. Detect multiple files → Launch 3 subagents
2. Each subagent processes in parallel:
   - Parse using `mu view`
   - Analyze sender, subject, content
   - Suggest target location
3. Consolidate results into list
4. User selects "Approve all"
5. Execute add-content sequentially
6. Update preferences

### Example 3: Process Image

**User**: "Process this photo ~/Photos/vacation.jpg"

**Workflow**:
1. Detect .jpg → Use Read tool
2. Language model analyzes image content → "Beach vacation photo"
3. Check preferences → Find "travel photos → Personal/Travel/"
4. Suggest Personal/Travel/2025/
5. User confirms
6. Call add-content (convert to descriptive markdown)
7. Update preferences

## Best Practices

1. **Always check preferences first** - Prioritize historical processing patterns
2. **Confirm before saving** - Default requires user approval
3. **Update preferences after success** - Accumulate learning user preferences
4. **Use parallel processing** - Leverage subagents for multiple files
5. **Handle errors gracefully** - Provide alternatives
6. **Integrate with akashicrecords** - Use existing skills for operations

## Notes

- Preferences file path is recorded in project claude.md
- Each project can have different preferences
- Audio/video processing methods are recorded in claude.md
- This Skill does not modify files directly, operates through akashicrecords skills
