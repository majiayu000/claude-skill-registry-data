---
name: read-docs
description: Read project documentation from ./docs with access logging. Use when you need to consult documentation, understand architecture, or learn about project components. Tracks doc usage and helpfulness.
---

# Read Documentation - Documentation Reading with Access Logging

## When to Use This Skill

Use this skill when:
- You need to read project documentation from the `./docs` folder
- You want to understand architecture, design decisions, or implementation details
- You're looking for guidance on how to implement something
- You need to learn about specific components or subsystems
- The user asks you to "check the docs" or "read the documentation"

## Core Philosophy

**Track What's Useful**: Every documentation access is logged with a helpfulness score to understand which docs are valuable and which need improvement. When docs are missing or inadequate, request new documentation.

## Documentation Location

All project documentation is located in:
```
./docs/
```

Browse this directory to find relevant documentation files.

## Workflow

### Phase 1: Find Relevant Documentation

1. **List available docs**
   ```bash
   find ./docs -type f -name "*.md" | sort
   ```

2. **Search for relevant topics**
   ```bash
   grep -r "keyword" ./docs/
   ```
   Use Grep tool with appropriate patterns to find docs about specific topics.

3. **Read the documentation**
   Use the Read tool to view the documentation file.

### Phase 2: Log Your Access

After reading a documentation file, you MUST append an access log entry to the end of that file.

**Access Log Format:**
```
2025-12-26T10:41:33Z +1 Accessed to understand rendering issues
```

**Components:**
- **Timestamp**: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ in UTC)
- **Score**: One of `+1`, `+0`, or `-1`
- **Comment**: Short description of why you accessed the doc

**Scoring Guidelines:**
- `+1`: The doc was helpful and contained the information you needed
- `+0`: The doc was somewhat relevant but didn't fully answer your question
- `-1`: The doc was not helpful, outdated, or contained incorrect information

**Implementation:**
Use the helper script for atomic append operations:

```bash
# Log documentation access
.claude/scripts/log-doc-access.sh ./docs/architecture.md +1 "Accessed to understand BVH acceleration structure"
```

The helper script handles UTC timestamp generation and atomic appending automatically.

### Phase 3: Request Missing or Inadequate Documentation

If any of the following are true:
- **No relevant documentation exists** for your topic
- **Documentation is incomplete** and missing key information
- **Documentation is out of date** and no longer matches the code

Then you MUST add a documentation request to `./docs/documentation-requests.md`.

**When to Request Documentation:**

1. **No docs found**: You searched but couldn't find any documentation on the topic
2. **Incomplete docs**: The doc exists but is missing critical details you need
3. **Outdated docs**: The doc contradicts the actual code or describes old behavior
4. **Scored -1 or +0**: If you logged a -1 or +0 score, consider whether a doc request is needed

**Documentation Request Format:**
```
## [Topic/Component Name]
- **Requested**: 2025-12-26T10:41:33Z
- **Requested by**: Agent working on [brief context]
- **Reason**: [Why documentation is needed]
- **Current state**: [None/Incomplete/Outdated]
- **Needed information**: [What should be documented]
```

**Implementation:**
Use atomic append to add the request:

```bash
cat >> ./docs/documentation-requests.md << 'EOF'

## BVH Split Algorithm Details
- **Requested**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Requested by**: Agent debugging BVH performance issue
- **Reason**: Need detailed explanation of median-split algorithm implementation
- **Current state**: Incomplete (./docs/bvh.md mentions it but lacks details)
- **Needed information**: Step-by-step algorithm, when to use SAH vs median, performance characteristics
EOF
```

**Important**: If you logged access with -1 or +0 score, ALSO add a documentation request explaining what was missing.

### Phase 4: Use the Information

Apply the information you learned from the documentation (or work around the gaps) to complete your task.

## Complete Example - Documentation Found and Helpful

```bash
# Step 1: Find relevant docs
find ./docs -type f -name "*.md"

# Step 2: Read the documentation
# (Use Read tool to view ./docs/rendering.md)

# Step 3: Log access
.claude/scripts/log-doc-access.sh ./docs/rendering.md +1 "Accessed to learn about progressive rendering passes"

# Step 4: Use the information in your work
```

## Complete Example - Documentation Missing

```bash
# Step 1: Search for docs on texture mapping
grep -r "texture" ./docs/

# Step 2: No relevant docs found!

# Step 3: Add documentation request
cat >> ./docs/documentation-requests.md << 'EOF'

## Texture Mapping Implementation
- **Requested**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Requested by**: Agent implementing texture support
- **Reason**: No documentation exists on how textures are loaded and applied
- **Current state**: None
- **Needed information**: Texture loading, UV coordinate handling, sampling methods, supported formats
EOF

# Step 4: Inform user and proceed based on code inspection
```

## Complete Example - Documentation Outdated

```bash
# Step 1: Read ./docs/materials.md
# (Use Read tool)

# Step 2: Notice the doc describes old Material interface, but code has changed

# Step 3: Log access with -1 score
.claude/scripts/log-doc-access.sh ./docs/materials.md -1 "Information outdated, Material interface has changed"

# Step 4: Add documentation request
cat >> ./docs/documentation-requests.md << 'EOF'

## Material Interface (Update Needed)
- **Requested**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Requested by**: Agent implementing new material type
- **Reason**: Documentation describes old interface that no longer matches code
- **Current state**: Outdated (./docs/materials.md)
- **Needed information**: Updated interface with new BSDF methods, PDF_f function, current material types
EOF

# Step 5: Proceed based on actual code
```

## Access Log Examples

### Helpful documentation (+1)
```
2025-12-26T10:41:33Z +1 Accessed to understand rendering issues
2025-12-26T11:15:20Z +1 Needed info on BVH construction algorithm
2025-12-26T14:22:45Z +1 Referenced for BDPT implementation details
```

### Somewhat helpful (+0)
```
2025-12-26T10:45:12Z +0 Partial information about texture mapping
2025-12-26T13:30:00Z +0 Found overview but needed more detail
```
*Note: Consider adding a documentation request for missing details*

### Not helpful (-1)
```
2025-12-26T11:00:00Z -1 Information was outdated, code has changed
2025-12-26T15:45:30Z -1 Doc didn't cover the topic I needed
```
*Note: You MUST add a documentation request when logging -1*

## Important Notes

### Atomic Appends
Always use atomic operations when appending:
- Use `.claude/scripts/log-doc-access.sh` for access logs (handles atomicity automatically)
- Use `cat >> file << 'EOF'` for multi-line documentation requests
- Do NOT read the file, modify it in memory, and write it back
- This prevents race conditions when multiple agents access docs simultaneously

### Always Log Access
You MUST log every documentation access, even if:
- The doc wasn't helpful (use `-1`)
- You only skimmed it (use `+0`)
- You accessed it multiple times (log each access)

### Always Request Missing Docs
You MUST add a documentation request when:
- No relevant docs exist
- Docs are incomplete (scored +0 or -1)
- Docs are outdated (scored -1)

Don't silently work around missing docs - request them so they can be created!

### Comment Quality
Keep comments short but informative:
- ✅ Good: "Accessed to understand BVH split algorithm"
- ✅ Good: "Needed info on BDPT light path construction"
- ✅ Good: "Checking how materials are defined"
- ❌ Bad: "Read the doc"
- ❌ Bad: "Information needed"

### Timestamp Format
The helper script automatically generates timestamps in UTC timezone and ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`). This ensures consistent timestamps regardless of system timezone.

## Benefits of Access Logging and Requests

The system helps:
1. **Identify valuable documentation** - High +1 scores show what's useful
2. **Find gaps** - Documentation requests reveal missing topics
3. **Detect outdated docs** - Multiple -1 scores and requests indicate problems
4. **Track usage patterns** - See which topics are frequently consulted
5. **Prioritize documentation work** - Most-requested docs should be written first
6. **Improve documentation** - Comments reveal what people are looking for

## Integration with Other Skills

This skill works well with:
- **fix-bug skill**: Read docs to understand how systems should work before debugging
- **docs-maintainer agent**: Access logs and requests guide documentation improvements
- **Feature development**: Consult architecture docs before implementing

## Example Workflow - Complete Session

```
User: "How does the BDPT integrator handle light paths?"

1. Search for BDPT documentation:
   grep -r "BDPT" ./docs/

2. Found ./docs/integrators.md, read it:
   (Use Read tool)

3. Doc explains basic BDPT but lacks light path details:
   - Log access with +0 score:
     .claude/scripts/log-doc-access.sh ./docs/integrators.md +0 "Found BDPT overview but lacks light path details"

   - Add documentation request:
     cat >> ./docs/documentation-requests.md << 'EOF'

## BDPT Light Path Construction (Details Needed)
- **Requested**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Requested by**: Agent explaining BDPT to user
- **Reason**: Documentation explains BDPT concept but not implementation details
- **Current state**: Incomplete (./docs/integrators.md)
- **Needed information**: Light path construction algorithm, connection strategies, MIS weight calculation, splat handling
EOF

4. Examine code to fill in gaps and explain to user
```

## Common Pitfalls to Avoid

- **Don't forget to log** - Every read must be logged
- **Don't forget to request** - Missing/inadequate docs need requests
- **Don't use non-atomic operations** - Always use `echo >> file` or `cat >> file`
- **Don't use local timezone** - Always use UTC with `date -u`
- **Don't write vague comments** - Be specific about why you accessed the doc
- **Don't skip logging on -1** - Negative scores are valuable feedback
- **Don't skip requesting on -1/+0** - Document what was inadequate

## Special Considerations

### Multiple Accesses
If you access the same doc multiple times in one task, log each access:
```bash
# First access - found overview
.claude/scripts/log-doc-access.sh ./docs/renderer.md +0 "Initial overview of renderer architecture"

# Second access - found specific detail
.claude/scripts/log-doc-access.sh ./docs/renderer.md +1 "Found tile worker pool implementation details"
```

### Documentation Requests File
The `./docs/documentation-requests.md` file may not exist initially. That's okay - your first append will create it:
```bash
cat >> ./docs/documentation-requests.md << 'EOF'
# Documentation Requests

This file tracks requests for new or improved documentation.

## First Request Topic
...
EOF
```

### Parallel Agents
The atomic append operations (helper script and `cat >>`) are safe for parallel access:
- Each agent's append is independent
- No need for locks or synchronization
- Logs and requests may be out of chronological order (that's okay)

### Request Deduplication
Don't worry about duplicate requests - it's better to log multiple requests for the same missing doc than to miss documenting what's needed. Multiple requests indicate high priority!
