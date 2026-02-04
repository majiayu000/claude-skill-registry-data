---
name: docs-manager-skill
description: Orchestrates complete single-document workflows with automatic validation and indexing in a write→validate→index pipeline
model: claude-haiku-4-5
---

# docs-manager-skill

<CONTEXT>
**Purpose**: Orchestrate complete single-document workflows with automatic validation and indexing.

**Architecture**: Coordination skill (Layer 2) - manages write → validate → index pipeline for single documents.

**Scope**: ONE document at a time (director handles multi-doc operations).
</CONTEXT>

<CRITICAL_RULES>
1. **Single Document Focus**
   - ALWAYS operate on exactly ONE document
   - NEVER handle wildcards or patterns (that's docs-director-skill's job)

2. **Workflow Coordination**
   - ALWAYS execute: write → validate → index (3-phase pipeline)
   - NEVER skip validation unless explicitly requested
   - ALWAYS update index after successful write+validate

3. **Type Context Loading**
   - ALWAYS load type context before operations
   - NEVER proceed without valid doc_type

4. **Error Handling**
   - STOP immediately on validation errors
   - REPORT all failures clearly
   - ROLLBACK if index update fails (delete written file)

5. **Operation Skills**
   - ALWAYS use operation skills (doc-writer, doc-validator, doc-lister)
   - NEVER implement operations directly
</CRITICAL_RULES>

<INPUTS>
**Required**:
- `operation` - Operation type: "write", "update", "validate", "index"
- `file_path` - Target document path

**For write/update**:
- `doc_type` OR auto-detect from path/content
- `context` - Conversational context (what user wants)
- `template_data` - Explicit template variables (optional)
- `skip_validation` - Skip validation step (default: false)
- `skip_index` - Skip index update (default: false)

**For validate**:
- `doc_type` OR auto-detect

**For index**:
- `doc_type` - Required
- `directory` - Directory to index (default: parent of file_path)
</INPUTS>

<WORKFLOW>
## Operation: write

1. **Classify Document Type**
   - If doc_type provided: use it
   - Else: invoke doc-classifier skill to auto-detect from path

2. **Load Type Context**
   - Load schema.json, template.md, standards.md from types/{doc_type}/
   - Build context bundle: conversational + type-specific + template_data

3. **Invoke doc-writer Skill**
   - Pass: file_path, doc_type, context bundle
   - Receive: written file path

4. **Validate Document** (unless skip_validation=true)
   - Invoke doc-validator skill
   - Pass: file_path, doc_type
   - If validation fails: STOP, report errors
   - If validation succeeds: continue

5. **Update Index** (unless skip_index=true)
   - Determine directory from file_path
   - Invoke index-updater.sh script
   - Pass: directory, doc_type

6. **Return Success**
   ```json
   {
     "status": "success",
     "operation": "write",
     "file_path": "docs/api/user-login/README.md",
     "doc_type": "api",
     "validation": "passed",
     "index_updated": true
   }
   ```

## Operation: update

Same as write, but:
- Read existing file first
- Merge existing content with new context
- Bump version if version field exists

## Operation: validate

1. **Classify Document Type**
   - Auto-detect if not provided

2. **Invoke doc-validator Skill**
   - Pass: file_path, doc_type
   - Return validation results

## Operation: index

1. **Invoke index-updater.sh**
   - Pass: directory, doc_type
   - Return index update status
</WORKFLOW>

<COMPLETION_CRITERIA>
- Document written successfully (for write/update)
- Validation passed (unless skipped)
- Index updated (unless skipped)
- All operation skills invoked correctly
- Clear success/failure status returned
</COMPLETION_CRITERIA>

<OUTPUTS>
**Success**:
```json
{
  "status": "success",
  "operation": "write|update|validate|index",
  "file_path": "path/to/file",
  "doc_type": "api",
  "validation": "passed|skipped|failed",
  "index_updated": true|false,
  "artifacts": ["README.md", "endpoint.json"]
}
```

**Failure**:
```json
{
  "status": "error",
  "operation": "write|update|validate|index",
  "error": "Validation failed: missing required field 'endpoint'",
  "file_path": "path/to/file",
  "validation_errors": ["error1", "error2"]
}
```
</OUTPUTS>

<DOCUMENTATION>
Output structured messages:

**Start**:
```
🎯 STARTING: docs-manager-skill
Operation: write
File: docs/api/user-login/README.md
Doc Type: api
───────────────────────────────────────
```

**During Execution**:
```
Step 1/5: Classifying document type...
   ✅ Detected: api (confidence: 100, method: path)

Step 2/5: Loading type context...
   ✅ Loaded: schema.json, template.md, standards.md

Step 3/5: Writing document...
   ✅ Generated: docs/api/user-login/README.md

Step 4/5: Validating document...
   ✅ Validation passed (0 errors, 0 warnings)

Step 5/5: Updating index...
   ✅ Index updated: docs/api/README.md
```

**Completion**:
```
✅ COMPLETED: docs-manager-skill
Operation: write
File: docs/api/user-login/README.md
Artifacts:
  - docs/api/user-login/README.md
  - docs/api/README.md (index)
───────────────────────────────────────
Next: Document ready for review
```
</DOCUMENTATION>

<ERROR_HANDLING>
**Validation Errors**:
- Stop pipeline immediately
- Report all validation errors
- Do NOT update index
- Do NOT delete written file (user may want to fix manually)

**Index Update Errors**:
- Report error
- Document is still valid (validation passed)
- Suggest manual index update

**Type Detection Errors**:
- Cannot proceed without valid doc_type
- Suggest manual doc_type specification
- List available doc_types

**Script Execution Errors**:
- Report script path and error message
- Suggest checking script permissions
- Provide command to run script manually for debugging
</ERROR_HANDLING>
