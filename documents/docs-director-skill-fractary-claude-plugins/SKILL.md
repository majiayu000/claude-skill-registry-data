---
name: docs-director-skill
description: Handles multi-document operations with pattern matching and parallel execution, delegating to docs-manager-skill for each matched document
model: claude-haiku-4-5
---

# docs-director-skill

<CONTEXT>
**Purpose**: Handle multi-document operations with pattern matching and parallel execution.

**Architecture**: Director skill (Layer 2) - routes to docs-manager-skill for each matched document.

**Scope**: Pattern matching, batch operations, parallel execution with file locking.
</CONTEXT>

<CRITICAL_RULES>
1. **Pattern Matching**
   - ALWAYS expand wildcards (docs/api/**/README.md)
   - ALWAYS handle glob patterns correctly
   - NEVER process more than 50 documents without user confirmation

2. **Parallel Execution**
   - ALWAYS execute independent operations in parallel (max 10 concurrent)
   - ALWAYS use file locking (flock) to prevent conflicts
   - NEVER run index updates in parallel for same directory

3. **Delegation**
   - ALWAYS delegate single-doc operations to docs-manager-skill
   - NEVER implement document operations directly
   - ALWAYS collect and aggregate results

4. **Safety**
   - ALWAYS show preview of matched files before executing
   - ALWAYS require confirmation for destructive operations
   - ALWAYS handle partial failures gracefully

5. **Progress Reporting**
   - ALWAYS show progress for batch operations
   - ALWAYS report success/failure counts
   - ALWAYS list failed items with errors
</CRITICAL_RULES>

<INPUTS>
**Required**:
- `operation` - Operation type: "write-batch", "validate-batch", "audit", "list"
- `pattern` - File pattern or path (supports wildcards)

**For write-batch**:
- `doc_type` - Document type
- `documents` - Array of {file_path, context} objects
- `skip_validation` - Skip validation (default: false)
- `skip_index` - Skip index updates (default: false)
- `parallel` - Execute in parallel (default: true)
- `max_concurrent` - Max parallel operations (default: 10)

**For validate-batch**:
- `doc_type` - Document type (optional, can auto-detect)

**For audit**:
- `doc_types` - Filter by doc types (optional)
- `status` - Filter by status (optional)

**For list**:
- `doc_type` - Filter by type (optional)
- `status` - Filter by status (optional)
- `format` - Output format: "table", "json", "markdown" (default: "table")
</INPUTS>

<WORKFLOW>
## Operation: write-batch

1. **Validate Input**
   - Check documents array is not empty
   - Verify all file_paths are unique
   - Confirm if > 10 documents

2. **Expand Patterns**
   - If pattern contains wildcards, expand to file list
   - Filter by doc_type if specified

3. **Preview**
   - Show list of files to be written
   - Count: total documents
   - Wait for user confirmation (if > 10 docs)

4. **Execute in Parallel**
   ```bash
   for doc in documents; do
       # Run docs-manager-skill in background with flock
       (
           flock -x "$file_path.lock" \
           coordinate-write.sh "$file_path" "$doc_type" "$context"
       ) &

       # Limit concurrent jobs
       if (( $(jobs -r | wc -l) >= $max_concurrent )); then
           wait -n
       fi
   done
   wait  # Wait for all jobs to complete
   ```

5. **Collect Results**
   - Aggregate success/failure counts
   - List failed documents with errors
   - Update indices (one per directory, sequential)

6. **Return Summary**
   ```json
   {
     "status": "partial_success",
     "operation": "write-batch",
     "total": 25,
     "succeeded": 23,
     "failed": 2,
     "failures": [
       {"file": "docs/api/foo.md", "error": "Validation failed"},
       {"file": "docs/api/bar.md", "error": "Template not found"}
     ],
     "indices_updated": ["docs/api/README.md"]
   }
   ```

## Operation: validate-batch

1. **Expand Pattern**
   - Find all matching files
   - Auto-detect doc_type if not provided

2. **Execute Validation**
   - Run in parallel (validation is read-only, safe)
   - Collect results

3. **Aggregate Results**
   - Count errors, warnings
   - Group by error type
   - Return detailed report

## Operation: audit

1. **Scan Directories**
   - Find all doc directories (containing fractary_doc_type docs)
   - Classify documents by type

2. **Collect Metadata**
   - Count by type
   - Count by status
   - Identify missing indices
   - Identify validation issues

3. **Generate Report**
   ```markdown
   # Documentation Audit Report

   ## Summary
   - Total Documents: 156
   - Document Types: 8
   - Missing Indices: 2
   - Validation Issues: 5

   ## By Type
   | Type          | Count | Status Distribution        |
   |---------------|-------|----------------------------|
   | api           | 45    | draft: 12, published: 33   |
   | adr           | 32    | accepted: 28, superseded: 4|
   | guide         | 28    | published: 28              |

   ## Issues
   - docs/api/deprecated/: Missing index
   - docs/dataset/metrics.md: Missing fractary_doc_type field
   ```

## Operation: list

1. **Invoke doc-lister Skill**
   - Pass pattern and filters
   - Get structured document list

2. **Format Output**
   - Table, JSON, or Markdown
   - Apply sorting

3. **Return Results**
</WORKFLOW>

<COMPLETION_CRITERIA>
- All matched documents processed
- Results aggregated correctly
- Indices updated (batch write operations)
- Progress reported throughout
- Final summary returned
</COMPLETION_CRITERIA>

<OUTPUTS>
**Batch Write Success**:
```json
{
  "status": "success",
  "operation": "write-batch",
  "total": 25,
  "succeeded": 25,
  "failed": 0,
  "indices_updated": ["docs/api/README.md", "docs/guides/README.md"]
}
```

**Batch Write Partial**:
```json
{
  "status": "partial_success",
  "operation": "write-batch",
  "total": 25,
  "succeeded": 23,
  "failed": 2,
  "failures": [
    {"file": "docs/api/foo.md", "error": "Validation failed: missing endpoint"},
    {"file": "docs/api/bar.md", "error": "Template rendering error"}
  ],
  "indices_updated": ["docs/api/README.md"]
}
```

**Audit Report**:
```json
{
  "status": "success",
  "operation": "audit",
  "summary": {
    "total_documents": 156,
    "doc_types": 8,
    "missing_indices": 2,
    "validation_issues": 5
  },
  "by_type": { ... },
  "issues": [ ... ]
}
```
</OUTPUTS>

<DOCUMENTATION>
Output structured messages:

**Start (Batch Operation)**:
```
🎯 STARTING: docs-director-skill
Operation: write-batch
Pattern: docs/api/**/*.md
Total matches: 25 documents
───────────────────────────────────────
```

**Preview**:
```
📋 Preview of documents to process:

1. docs/api/auth/login/README.md (api)
2. docs/api/auth/logout/README.md (api)
3. docs/api/users/create/README.md (api)
... (22 more)

Proceed with batch write? [y/N]
```

**During Execution**:
```
Processing batch (25 documents, max 10 parallel)...

[1/25] ✅ docs/api/auth/login/README.md
[2/25] ✅ docs/api/auth/logout/README.md
[3/25] ❌ docs/api/users/create/README.md (validation failed)
[4/25] ✅ docs/api/users/update/README.md
...

Progress: 15/25 (60%) | Success: 14 | Failed: 1
```

**Indexing Phase**:
```
Updating indices (sequential)...
   ✅ docs/api/README.md (23 documents)
   ✅ docs/guides/README.md (2 documents)
```

**Completion**:
```
✅ COMPLETED: docs-director-skill
Operation: write-batch
Results:
  Total: 25
  Succeeded: 23
  Failed: 2
  Indices Updated: 2

Failed documents:
  ❌ docs/api/users/create/README.md
     Error: Validation failed - missing required field 'endpoint'
  ❌ docs/api/admin/delete/README.md
     Error: Template rendering failed - invalid JSON
───────────────────────────────────────
Next: Review failed documents and retry
```
</DOCUMENTATION>

<ERROR_HANDLING>
**Pattern Match Failures**:
- No files matched pattern → warn user, suggest pattern fixes
- Too many files (>50) → require explicit confirmation

**Partial Failures**:
- Some documents fail → continue with others
- Collect all failures → report at end
- Update indices for successful documents only

**Parallel Execution Errors**:
- File lock timeout → retry with backoff
- Process killed → report incomplete operation
- Suggest sequential mode for debugging

**Resource Limits**:
- Too many concurrent jobs → throttle to max_concurrent
- Disk space low → abort operation
- Memory pressure → reduce parallelism

**Index Update Conflicts**:
- Multiple docs in same directory → batch index update
- Run index updates sequentially (never parallel for same dir)
- Use flock to prevent concurrent index writes
</ERROR_HANDLING>
