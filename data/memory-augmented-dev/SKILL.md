---
name: memory-augmented-dev
description: Development with persistent memory checks and automatic logging
---

# Memory-Augmented Development

## Purpose
Ensures every development task leverages past learnings and contributes to organizational memory. Search before implementing, document after completing.

## When This Activates
- User asks to implement a feature
- User requests bug fixes or refactoring
- Any coding task that could benefit from past patterns
- Keywords: "implement", "build", "fix", "refactor", "add feature"

## Instructions

### Phase 1: Research (Before Implementation)

1. **Semantic Search for Patterns**
   Use `search-enhanced` to find relevant past work:
   ```
   search-enhanced(
     query: "<feature area> implementation patterns",
     filters: {type: "code"}
   )
   ```

2. **Review Past Decisions**
   ```
   list-memories-by-tag(["<feature-area>", "architecture", "decisions"])
   ```

3. **Check Recent Context**
   ```
   get-recent-context(project: "<current-project>")
   ```

4. **Analyze Retrieved Memories**
   - What patterns were successful?
   - What mistakes were made?
   - What decisions inform this work?

### Phase 2: Implementation

5. **Apply Patterns Found**
   - Use established code patterns
   - Follow past architectural decisions
   - Avoid documented mistakes

6. **Note Deviations**
   - If deviating from patterns, document why
   - Prepare justification for memory storage

### Phase 3: Documentation (After Implementation)

7. **Store Memory with Rich Metadata**
   ```
   store-dev-memory({
     type: "code",
     content: "Detailed description of implementation",
     project: "<project-name>",
     tags: ["<feature>", "<technology>", "<pattern-used>"],
     metadata: {
       implementation_status: "complete",
       key_decisions: ["Decision 1", "Decision 2"],
       files_created: ["file1.py", "file2.py"],
       files_modified: ["existing.py"],
       code_changes: "Summary of major changes",
       dependencies_added: ["package1", "package2"],
       testing_notes: "How to test this"
     },
     relationships: [
       {
         memory_id: "<related-memory-hash>",
         type: "builds_on"
       }
     ]
   })
   ```

8. **Store Decisions Separately**
   ```
   store-dev-memory({
     type: "decision",
     content: "Why we chose approach X over Y",
     project: "<project-name>",
     tags: ["decision", "<topic>"],
     metadata: {
       alternatives_considered: ["Approach Y", "Approach Z"],
       decision_rationale: "Explanation",
       decision_date: "<date>",
       who_decided: "<name>"
     }
   })
   ```

## Tool Reference

### search-enhanced
- **Purpose**: Semantic search across all memories
- **Parameters**:
  - `query` (string): Search terms
  - `filters` (object): Optional filters
    - `type`: "code" | "decision" | "conversation" | "reference"
    - `tags`: Array of tags to match
    - `project`: Project name
    - `date_from`, `date_to`: Date range
  - `limit` (int): Max results (default: 10)
- **Returns**: Array of memories with similarity scores
- **Example**: `search-enhanced("authentication JWT patterns", filters={type: "code"})`

### list-memories-by-tag
- **Purpose**: Get all memories with specific tags
- **Parameters**:
  - `tags` (array): Tags to search for
  - `project` (string): Optional project filter
- **Returns**: Array of memories
- **Example**: `list-memories-by-tag(["authentication", "security"])`

### get-recent-context
- **Purpose**: Get recent memories for session continuity
- **Parameters**:
  - `project` (string): Project name
  - `limit` (int): Number of recent items (default: 10)
- **Returns**: Array of recent memories, ordered by date
- **Example**: `get-recent-context(project: "hrdag-api")`

### store-dev-memory
- **Purpose**: Store new memory with full metadata
- **Parameters**: See Phase 3 examples above
- **Returns**: Memory ID (hash)
- **Example**: See detailed examples below

### get-dev-memory
- **Purpose**: Retrieve specific memory by ID
- **Parameters**:
  - `memory_id` (string): Memory hash ID
- **Returns**: Full memory object
- **Example**: `get-dev-memory(memory_id: "abc123def456")`

## Examples

### Example 1: Implementing Authentication

**User says**: "Add JWT authentication to the API"

**You do**:

1. **Research**
   ```
   search-enhanced("authentication JWT patterns", filters={type: "code"})
   list-memories-by-tag(["authentication", "security"])
   ```
   Result: Found memory showing JWT implementation from 3 months ago

2. **Implement**
   Apply the JWT pattern found, using similar code structure

3. **Document**
   ```
   store-dev-memory({
     type: "code",
     content: "Implemented JWT authentication with refresh tokens for API v2",
     project: "hrdag-api",
     tags: ["authentication", "jwt", "security", "api-v2"],
     metadata: {
       implementation_status: "complete",
       key_decisions: [
         "Used JWT over session-based auth for stateless API",
         "Refresh token rotation every 7 days"
       ],
       files_created: ["auth/jwt_manager.py", "auth/middleware.py"],
       files_modified: ["api/routes.py", "config/settings.py"],
       dependencies_added: ["PyJWT==2.8.0"],
       testing_notes: "Test with curl scripts in tests/auth/"
     },
     relationships: [{
       memory_id: "<hash-of-3-month-old-auth-memory>",
       type: "builds_on"
     }]
   })
   ```

### Example 2: Fixing Data Recovery Bug

**User says**: "The zip disk recovery keeps failing on bad sectors"

**You do**:

1. **Research**
   ```
   search-enhanced("zip disk recovery errors", filters={type: "code"})
   list-memories-by-tag(["data-recovery", "bugs", "zip-disk"])
   ```
   Result: Found memory about ddrescue parameters and common failures

2. **Implement**
   Applied lessons about proper ddrescue flags and error handling

3. **Document**
   ```
   store-dev-memory({
     type: "code",
     content: "Fixed zip disk recovery by adjusting ddrescue retry parameters",
     project: "vintage-data-recovery",
     tags: ["data-recovery", "zip-disk", "bugfix", "ddrescue"],
     metadata: {
       implementation_status: "complete",
       key_decisions: [
         "Increased retry count from 3 to 10 for bad sectors",
         "Added sector size specification for old media"
       ],
       files_modified: ["recovery_scripts/zip_disk_reader.sh"],
       testing_notes: "Tested on 5 failing disks, 3 now readable"
     },
     relationships: [{
       memory_id: "<hash-of-ddrescue-lessons>",
       type: "applies"
     }]
   })
   ```

## Rules

- ✅ **Always search memory before implementing** - Check for patterns first
- ✅ **Store learnings after every task** - Every task generates knowledge
- ✅ **Be specific in descriptions** - Detail what was actually done
- ✅ **Link related memories** - Create relationships to related work
- ✅ **Include key decisions** - Future you needs to know why
- ✅ **Tag appropriately** - Use consistent, searchable tags
- ❌ **Don't skip research phase** - No matter how simple the task seems
- ❌ **Don't forget to store** - Even small fixes generate learnings
- ❌ **Don't store generic descriptions** - "Fixed bug" isn't useful
- ❌ **Don't skip relationships** - Context comes from connections
- ❌ **Don't omit metadata** - Files, decisions, tests matter

## Success Metrics

- Every feature implementation references at least 1 past memory
- Every completed task stores at least 1 new memory
- Memory retrieval takes <500ms
- 90% of new implementations find relevant patterns in memory
